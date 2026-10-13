"""Package a bounded SF Bay Area regional demo from public official COGs.

python scripts/prepare_bayarea_demo.py
Optionally supply --index path/to/aef_index.parquet to rediscover the four tiles.
Only four small AEF overviews and a bounded WorldCover window are read.
No imagery/model inference, EE credentials, or manuscript files are used.
"""

import argparse
import hashlib
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from pyproj import Transformer
from rasterio.features import geometry_mask
from rasterio.windows import Window, from_bounds

from earth_embedding import BBox, dequantize_aef, find_aef_tiles, sample_aef

BOUNDS = [-122.6, 37.3, -121.6, 38.3]
WC = "https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_N36W123_Map.tif"
ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path)
    args = parser.parse_args()
    start = time.perf_counter()
    pinned = json.loads((ROOT / "src/rs_embed/data/demos/bayarea/manifest.json").read_text())
    tiles = (
        find_aef_tiles(args.index, spatial=BBox(*BOUNDS), year=2021)
        if args.index
        else pinned["tiles"]
    )
    if set(tiles) != set(pinned["tiles"]):
        raise ValueError("Regional AEF source URLs differ from the pinned manifest.")
    expected_aef = {r["url"]: r["raw_sha256"] for r in pinned["aef_sources"]}
    cache = ROOT / "work/bayarea-source-cache"
    cache.mkdir(parents=True, exist_ok=True)
    rows, vectors, receipts = [], [], []
    to_geo = Transformer.from_crs(32610, 4326, always_xy=True)
    env = dict(
        GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_TIMEOUT=45, GDAL_HTTP_MAX_RETRY=1
    )
    for url in tiles:
        filename = cache / (hashlib.sha256(url.encode()).hexdigest()[:16] + ".npz")
        if filename.exists():
            with np.load(filename) as z:
                raw, transform = z["raw"], rasterio.Affine(*z["transform"][:6])
        else:
            with rasterio.Env(**env), rasterio.open(url, overview_level=6) as src:
                assert src.crs.to_epsg() == 32610 and abs(src.transform.a) == 1280
                raw, transform = src.read(), src.transform
            np.savez_compressed(filename, raw=raw, transform=np.array(transform))
        raw_hash = hashlib.sha256(raw.tobytes()).hexdigest()
        if raw_hash != expected_aef[url]:
            raise ValueError(f"AEF source/cache SHA-256 mismatch: {url}")
        receipts.append(dict(url=url, overview_level=6, raw_sha256=raw_hash, raw_bytes=raw.nbytes))
        decoded = dequantize_aef(raw)
        for r in range(raw.shape[1]):
            for c in range(raw.shape[2]):
                x, y = transform * (c + 0.5, r + 0.5)
                lon, lat = to_geo.transform(x, y)
                if not (BOUNDS[0] <= lon <= BOUNDS[2] and BOUNDS[1] <= lat <= BOUNDS[3]):
                    continue
                corners = [
                    to_geo.transform(*(transform * p))
                    for p in [(c, r), (c + 1, r), (c + 1, r + 1), (c, r + 1)]
                ]
                row = dict(
                    tile_id=f"bay_x{int(x)}_y{int(y)}",
                    center_lon=lon,
                    center_lat=lat,
                    minlon=min(p[0] for p in corners),
                    minlat=min(p[1] for p in corners),
                    maxlon=max(p[0] for p in corners),
                    maxlat=max(p[1] for p in corners),
                    utm_easting=x,
                    utm_northing=y,
                    aef_valid=bool(np.isfinite(decoded[:, r, c]).all()),
                )
                for i, (lo, la) in enumerate(corners):
                    row[f"lon{i}"], row[f"lat{i}"] = lo, la
                rows.append(row)
                vectors.append(decoded[:, r, c])
    table = pd.DataFrame(rows)
    x = np.asarray(vectors, dtype=np.float32)
    assert not table.tile_id.duplicated().any()
    print("AEF candidates", len(table), "valid", int(table.aef_valid.sum()), flush=True)
    wc_cache = cache / "worldcover-window.npz"
    if wc_cache.exists():
        with np.load(wc_cache) as z:
            landcover, wc_transform = z["landcover"], rasterio.Affine(*z["transform"][:6])
    else:
        with rasterio.Env(**env), rasterio.open(WC) as src:
            window = from_bounds(
                table.minlon.min(),
                table.minlat.min(),
                table.maxlon.max(),
                table.maxlat.max(),
                src.transform,
            )
            window = Window(
                np.floor(window.col_off),
                np.floor(window.row_off),
                np.ceil(window.width) + 2,
                np.ceil(window.height) + 2,
            )
            landcover = src.read(1, window=window)
            wc_transform = src.window_transform(window)
        np.savez_compressed(wc_cache, landcover=landcover, transform=np.array(wc_transform))
    if hashlib.sha256(landcover.tobytes()).hexdigest() != pinned["worldcover_window"]["sha256"]:
        raise ValueError(
            "WorldCover source/cache SHA-256 mismatch; cached or upstream pixels changed."
        )
    print("WorldCover native window", landcover.shape, flush=True)
    mapping = {
        10: "vegetation",
        20: "vegetation",
        30: "vegetation",
        40: "cropland",
        50: "built",
        60: "bare",
        70: "snow",
        80: "water",
        90: "vegetation",
        95: "vegetation",
        100: "vegetation",
    }
    labels, purities, valid_fracs = [], [], []
    for row in table.itertuples():
        geom = {
            "type": "Polygon",
            "coordinates": [
                [[getattr(row, f"lon{i}"), getattr(row, f"lat{i}")] for i in [0, 1, 2, 3, 0]]
            ],
        }
        win = from_bounds(row.minlon, row.minlat, row.maxlon, row.maxlat, wc_transform)
        c0, r0 = int(np.floor(win.col_off)), int(np.floor(win.row_off))
        c1, r1 = int(np.ceil(win.col_off + win.width)), int(np.ceil(win.row_off + win.height))
        block = landcover[r0:r1, c0:c1]
        mask = geometry_mask(
            [geom],
            out_shape=block.shape,
            transform=wc_transform * rasterio.Affine.translation(c0, r0),
            invert=True,
        )
        values = block[mask]
        valid = values[values > 0]
        valid_fracs.append(len(valid) / len(values))
        if not len(valid):
            labels.append("nodata")
            purities.append(0)
            continue
        unique, counts = np.unique(valid, return_counts=True)
        grouped = {}
        for code, count in zip(unique, counts, strict=True):
            key = mapping[int(code)]
            grouped[key] = grouped.get(key, 0) + int(count)
        label = max(sorted(grouped), key=grouped.get)
        labels.append(label)
        purities.append(grouped[label] / len(valid))
    table["class_name"] = labels
    table["dominant_fraction"] = purities
    table["reference_valid_fraction"] = valid_fracs
    table["demo_split"] = np.where(
        table.maxlat <= 37.88, "train", np.where(table.minlat >= 37.93, "test", "buffer")
    )
    keep = table.aef_valid & table.reference_valid_fraction.ge(0.95)
    missing = table.loc[~keep].copy()
    table = table.loc[keep].reset_index(drop=True)
    x = x[keep]
    # Verify the public sampling route against complete overview reads, including south-up COGs.
    probe = np.linspace(0, len(table) - 1, 64, dtype=int)
    with rasterio.Env(**env):
        sampled = sample_aef(
            table.loc[probe, ["center_lon", "center_lat"]].to_numpy(), tiles=tiles, overview_level=6
        ).data
    np.testing.assert_array_equal(sampled, x[probe])
    out = ROOT / "src/rs_embed/data/demos/bayarea"
    out.mkdir(parents=True, exist_ok=True)
    if hashlib.sha256(x.tobytes()).hexdigest() != pinned["array_sha256"]:
        raise ValueError("Rebuilt features differ from the pinned regional sample.")
    for name, frame in [("samples.csv", table), ("excluded.csv", missing)]:
        canonical = frame.to_csv(index=False, lineterminator="\n", float_format="%.12g").encode()
        if hashlib.sha256(canonical).hexdigest() != pinned["files"][name]["sha256"]:
            raise ValueError(f"Rebuilt coordinates/labels differ from pinned {name}.")
    table.to_csv(out / "samples.csv", index=False, lineterminator="\n", float_format="%.12g")
    missing.to_csv(out / "excluded.csv", index=False, lineterminator="\n", float_format="%.12g")
    np.savez_compressed(out / "features.npz", tile_id=table.tile_id.to_numpy(dtype="U"), features=x)
    meta = dict(
        name="San Francisco Bay Area and surroundings",
        year=2021,
        bounds=BOUNDS,
        nominal_size_km=[88, 111],
        scope="Regional software demonstration, not a paper benchmark reproduction",
        license="CC-BY-4.0",
        tiles=tiles,
        overview_level=6,
        features="Official 1280m AEF overview cells: normalized sums of native vectors, decoded from int8; not 10m point vectors",
        labels="WorldCover 2021 v200 grouped majority of native 10m pixel centers inside each AEF cell polygon; minimum 95% valid reference support",
        attribution="The AlphaEarth Foundations Satellite Embedding dataset is produced by Google and Google DeepMind. © ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium.",
        source="https://developers.google.com/earth-engine/guides/aef_on_gcs_readme",
        worldcover_source=WC,
        selection="All 1280m AEF cells with center inside bounds, complete AEF vector and >=95% reference coverage; no score-based selection",
        split="South maxlat<=37.88 train; north minlat>=37.93 test; intervening cells buffer. Four-class built/vegetation/cropland/water task; other labels excluded.",
        candidates=len(keep),
        retained=len(table),
        excluded=len(missing),
        aef_sources=receipts,
        worldcover_window=dict(
            shape=list(landcover.shape),
            sha256=hashlib.sha256(landcover.tobytes()).hexdigest(),
            bytes=landcover.nbytes,
        ),
        array_sha256=hashlib.sha256(x.tobytes()).hexdigest(),
        seconds=round(time.perf_counter() - start, 2),
    )
    meta["files"] = {
        p.name: dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest(), bytes=p.stat().st_size)
        for p in out.iterdir()
        if p.name != "manifest.json"
    }
    (out / "manifest.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(pd.crosstab(table.demo_split, table.class_name).to_string(), flush=True)
    print(
        "seconds",
        meta["seconds"],
        "payload bytes",
        sum(p.stat().st_size for p in out.iterdir()),
        flush=True,
    )


if __name__ == "__main__":
    main()
