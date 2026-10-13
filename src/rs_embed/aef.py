"""Direct, credential-free access to official AlphaEarth Foundations COGs.

The index is deliberately supplied by the caller: a global index is large and
must not be downloaded implicitly for every point query. Pixel reads use HTTP
range requests through Rasterio. No Earth Engine initialization is performed.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np

from .core.embedding import Embedding
from .core.errors import ModelError
from .core.specs import BBox

AEF_BUCKET = "gs://alphaearth_foundations"
AEF_BASE_URL = "https://storage.googleapis.com/alphaearth_foundations/satellite_embedding/v1/annual"
AEF_INDEX_URL = f"{AEF_BASE_URL}/aef_index.csv"
AEF_ATTRIBUTION = "The AlphaEarth Foundations Satellite Embedding dataset is produced by Google and Google DeepMind."


def dequantize_aef(values: Any) -> np.ndarray:
    """Decode signed int8 AEF values; -128 and existing masks become NaN.

    Decode *before* aggregation. The GCS values are not the float vectors
    returned by Earth Engine. See Google's ``aef_on_gcs_readme``.
    """
    arr = np.ma.asarray(values)
    raw = np.asarray(arr.data)
    if raw.dtype.kind != "i" or np.any((raw < -128) | (raw > 127)):
        raise ValueError("AEF COG values must be signed integers in [-128, 127].")
    floats = raw.astype(np.float32)
    result = np.sign(floats) * np.square(floats / np.float32(127.5))
    return np.where((raw == -128) | np.ma.getmaskarray(arr), np.nan, result).astype(np.float32)


def aef_url(path: str) -> str:
    """Convert an official ``gs://`` index entry to anonymous HTTPS."""
    if path.startswith(f"{AEF_BUCKET}/"):
        return (
            "https://storage.googleapis.com/alphaearth_foundations/" + path[len(AEF_BUCKET) + 1 :]
        )
    if path.startswith("https://storage.googleapis.com/alphaearth_foundations/"):
        return path
    raise ValueError("Expected an official alphaearth_foundations GCS or HTTPS URL.")


def find_aef_tiles(index: Any, *, spatial: BBox, year: int) -> list[str]:
    """Find candidate COG URLs using a local official CSV/Parquet index or DataFrame.

    Bounds filtering is conservative; COG masks decide pixel validity. This
    avoids silently discarding valid data at curved UTM-zone boundaries.
    CSV files are scanned in chunks. Parquet support needs ``pyarrow``.
    """
    import pandas as pd

    spatial.validate()
    if not np.isfinite([spatial.minlon, spatial.minlat, spatial.maxlon, spatial.maxlat]).all():
        raise ValueError("AEF index query bounds must be finite.")
    if spatial.crs.upper() != "EPSG:4326":
        raise ValueError("AEF index queries require an EPSG:4326 BBox.")
    if isinstance(year, bool) or not isinstance(year, (int, np.integer)):
        raise ValueError("year must be an integer present in the supplied index.")
    columns = ["path", "year", "wgs84_west", "wgs84_south", "wgs84_east", "wgs84_north"]
    if isinstance(index, (str, Path)):
        path = Path(index)
        if not path.is_file():
            raise FileNotFoundError("Supply a downloaded local AEF index file.")
        if path.suffix.lower() in {".parquet", ".pq"}:
            chunks = [pd.read_parquet(path, columns=columns)]
        else:
            chunks = pd.read_csv(path, usecols=columns, chunksize=50_000)
    elif isinstance(index, pd.DataFrame):
        missing = set(columns) - set(index.columns)
        if missing:
            raise ValueError(f"AEF index missing columns: {sorted(missing)}")
        chunks = [index]
    else:
        raise TypeError("index must be a local CSV/Parquet path or pandas DataFrame.")
    matches = []
    for frame in chunks:
        keep = (
            (frame["year"] == year)
            & (frame["wgs84_west"] <= spatial.maxlon)
            & (frame["wgs84_east"] >= spatial.minlon)
            & (frame["wgs84_south"] <= spatial.maxlat)
            & (frame["wgs84_north"] >= spatial.minlat)
        )
        matches.extend(aef_url(str(path)) for path in frame.loc[keep, "path"])
    return sorted(set(matches))


def sample_aef(
    lonlat: Any,
    *,
    tiles: Sequence[str | Path],
    strict: bool = True,
) -> Embedding:
    """Sample ``(N, 2)`` [longitude, latitude] points from official AEF COGs.

    ``tiles`` are HTTPS/GCS URLs from :func:`find_aef_tiles` or local signed
    int8 COG files. Supply one year only. Output shape is ``(N, 64)``;
    uncovered/masked points raise by default, or return NaN with strict=False.
    Overlaps use the first fully valid vector. Never mixes bands across tiles.
    """
    points = np.asarray(lonlat, dtype=np.float64)
    if points.ndim != 2 or points.shape[1] != 2 or not np.isfinite(points).all():
        raise ValueError("lonlat must be a finite (N, 2) array in [longitude, latitude] order.")
    if (np.abs(points[:, 0]) > 180).any() or (np.abs(points[:, 1]) > 90).any():
        raise ValueError("Longitude must be within [-180, 180], latitude within [-90, 90].")
    if isinstance(tiles, (str, Path)):
        raise TypeError("tiles must be a sequence of paths, not a single string.")
    try:
        import rasterio
        from pyproj import Transformer
        from rasterio.transform import rowcol
    except ImportError as exc:
        raise ModelError(
            "Direct AEF COG access requires Rasterio. From the earth-embedding repository, "
            'install the optional dependencies with: pip install -e ".[aef]"'
        ) from exc

    result = np.full((len(points), 64), np.nan, dtype=np.float32)
    source_for_point: list[str | None] = [None] * len(points)
    sources = []
    for tile in tiles:
        unresolved = np.flatnonzero(~np.isfinite(result).all(axis=1))
        if not len(unresolved):
            break
        name = str(tile)
        uri = aef_url(name) if name.startswith(("gs://", "https://")) else name
        # HTTP errors remain errors: a missing tile is not an empty observation.
        with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR"):
            with rasterio.open(uri) as src:
                if src.count != 64 or any(dtype != "int8" for dtype in src.dtypes):
                    raise ModelError(
                        "Expected a 64-band signed int8 AEF COG; do not decode EE float exports."
                    )
                if src.crs is None:
                    raise ModelError("AEF COG is missing its coordinate reference system.")
                # A global point batch may include coordinates outside this
                # tile's UTM projection domain. Preserve those rows for other
                # tiles instead of letting one unprojectable point abort all.
                transformer = Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)
                xs, ys = transformer.transform(
                    points[unresolved, 0], points[unresolved, 1], errcheck=False
                )
                projectable = np.isfinite(xs) & np.isfinite(ys)
                unresolved = unresolved[projectable]
                xs, ys = np.asarray(xs)[projectable], np.asarray(ys)[projectable]
                if not len(unresolved):
                    continue
                rows, cols = rowcol(src.transform, xs, ys)
                inside = (np.asarray(rows) >= 0) & (np.asarray(rows) < src.height)
                inside &= (np.asarray(cols) >= 0) & (np.asarray(cols) < src.width)
                positions = unresolved[inside]
                xy = list(zip(np.asarray(xs)[inside], np.asarray(ys)[inside], strict=True))
                if not xy:
                    continue
                raw = np.ma.vstack(list(src.sample(xy, masked=True)))
                decoded = dequantize_aef(raw)
                valid = np.isfinite(decoded).all(axis=1)
                result[positions[valid]] = decoded[valid]
                for pos in positions[valid]:
                    source_for_point[int(pos)] = uri
                sources.append(uri)
    valid = np.isfinite(result).all(axis=1)
    if strict and not valid.all():
        missing = np.flatnonzero(~valid).tolist()
        raise ModelError(
            f"No valid AEF vector for point indices {missing[:20]}; check year, coverage and masks."
        )
    return Embedding(
        data=result,
        meta={
            "model": "gse",
            "type": "precomputed",
            "backend": "gcs",
            "coordinate_order": "lon,lat",
            "bands": [f"A{i:02d}" for i in range(64)],
            "sources": sources,
            "source_for_point": source_for_point,
            "valid_points": int(valid.sum()),
            "dequantization": "sign(x) * (x / 127.5) ** 2; -128 -> NaN",
            "license": "CC-BY-4.0",
            "attribution": AEF_ATTRIBUTION,
        },
    )
