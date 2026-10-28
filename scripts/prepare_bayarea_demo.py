"""Package a complete SF Bay Area regional demo from public official COGs.

python scripts/prepare_bayarea_demo.py           # rebuild and verify against the pins
python scripts/prepare_bayarea_demo.py --repin   # deliberately replace the pins

The demo is a whole-cell rectangle of the official 1280 m AEF overview grid
(UTM 10N), so every cell inside the frame is present: no lon/lat clipping
staircase and no ocean no-data holes. Optionally supply
--index path/to/aef_index.parquet to rediscover the four source tiles.
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

CELL = 1280
# Whole-cell rectangle on the AEF overview grid, EPSG:32610 metres: 72 x 88 cells.
GRID = dict(crs="EPSG:32610", west=540960, east=633120, south=4129280, north=4241920)
# Columns counted from the west edge. Six buffer columns (7.68 km) separate the two folds.
WEST_COLS, BUFFER_COLS = 33, 6
WC = "https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_N36W123_Map.tif"
ROOT = Path(__file__).resolve().parents[1]
MAPPING = {
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


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def read_overviews(tiles, cache, env):
    """Return {url: (raw int8 CxHxW, Affine)} from cache or official COG overviews."""
    out = {}
    for url in tiles:
        filename = cache / (sha256(url.encode())[:16] + ".npz")
        if filename.exists():
            with np.load(filename) as z:
                raw, transform = z["raw"], rasterio.Affine(*z["transform"][:6])
        else:
            with rasterio.Env(**env), rasterio.open(url, overview_level=6) as src:
                assert src.crs.to_epsg() == 32610 and abs(src.transform.a) == CELL
                raw, transform = src.read(), src.transform
            np.savez_compressed(filename, raw=raw, transform=np.array(transform))
        out[url] = (raw, transform)
    return out


def mosaic(overviews, rows, cols):
    """North-up int8 mosaic of the GRID rectangle; works for south-up COGs too."""
    raw_grid = np.full((64, rows, cols), -128, dtype=np.int8)
    filled = np.zeros((rows, cols), dtype=bool)
    for raw, transform in overviews.values():
        for r in range(raw.shape[1]):
            for c in range(raw.shape[2]):
                x, y = transform * (c + 0.5, r + 0.5)
                col = int(np.floor((x - GRID["west"]) / CELL))
                row = int(np.floor((GRID["north"] - y) / CELL))
                if 0 <= row < rows and 0 <= col < cols:
                    raw_grid[:, row, col] = raw[:, r, c]
                    filled[row, col] = True
    if not filled.all():
        raise ValueError("The four source tiles do not cover the demo rectangle.")
    return raw_grid


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path)
    parser.add_argument("--repin", action="store_true", help="write new pinned checksums")
    args = parser.parse_args()
    start = time.perf_counter()
    out = ROOT / "src/rs_embed/data/demos/bayarea"
    pinned = json.loads((out / "manifest.json").read_text())
    rows = (GRID["north"] - GRID["south"]) // CELL
    cols = (GRID["east"] - GRID["west"]) // CELL
    to_geo = Transformer.from_crs(32610, 4326, always_xy=True)
    lon_w, lat_s = to_geo.transform(GRID["west"], GRID["south"])
    lon_e, lat_n = to_geo.transform(GRID["east"], GRID["north"])
    tiles = (
        find_aef_tiles(args.index, spatial=BBox(lon_w, lat_s, lon_e, lat_n), year=2021)
        if args.index
        else pinned["tiles"]
    )
    if set(tiles) != set(pinned["tiles"]):
        raise ValueError("Regional AEF source URLs differ from the pinned manifest.")
    cache = ROOT / "work/bayarea-source-cache"
    cache.mkdir(parents=True, exist_ok=True)
    env = dict(
        GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_TIMEOUT=45, GDAL_HTTP_MAX_RETRY=1
    )
    overviews = read_overviews(tiles, cache, env)
    expected_aef = {r["url"]: r["raw_sha256"] for r in pinned["aef_sources"]}
    receipts = []
    for url, (raw, _) in overviews.items():
        if sha256(raw.tobytes()) != expected_aef[url]:
            raise ValueError(f"AEF source/cache SHA-256 mismatch: {url}")
        receipts.append(
            dict(url=url, overview_level=6, raw_sha256=expected_aef[url], raw_bytes=raw.nbytes)
        )
    decoded = dequantize_aef(mosaic(overviews, rows, cols))
    if not np.isfinite(decoded).all():
        raise ValueError("AEF no-data inside the demo rectangle; choose a fully valid grid.")

    records, vectors = [], []
    for row in range(rows):
        for col in range(cols):
            x = GRID["west"] + (col + 0.5) * CELL
            y = GRID["north"] - (row + 0.5) * CELL
            lon, lat = to_geo.transform(x, y)
            corners = [
                to_geo.transform(x + dx * CELL / 2, y + dy * CELL / 2)
                for dx, dy in [(-1, -1), (1, -1), (1, 1), (-1, 1)]
            ]
            record = dict(
                tile_id=f"bay_x{int(x)}_y{int(y)}",
                grid_row=row,
                grid_col=col,
                center_lon=lon,
                center_lat=lat,
                minlon=min(p[0] for p in corners),
                minlat=min(p[1] for p in corners),
                maxlon=max(p[0] for p in corners),
                maxlat=max(p[1] for p in corners),
                utm_easting=x,
                utm_northing=y,
            )
            for i, (lo, la) in enumerate(corners):
                record[f"lon{i}"], record[f"lat{i}"] = lo, la
            records.append(record)
            vectors.append(decoded[:, row, col])
    table = pd.DataFrame(records)
    x = np.asarray(vectors, dtype=np.float32)
    assert not table.tile_id.duplicated().any()
    print("AEF cells", len(table), f"({rows} rows x {cols} cols)", flush=True)

    wc_cache = cache / "worldcover-window-grid.npz"
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
    wc_hash = sha256(landcover.tobytes())
    if not args.repin and wc_hash != pinned["worldcover_window"]["sha256"]:
        raise ValueError(
            "WorldCover source/cache SHA-256 mismatch; cached or upstream pixels changed."
        )
    print("WorldCover native window", landcover.shape, flush=True)

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
            key = MAPPING[int(code)]
            grouped[key] = grouped.get(key, 0) + int(count)
        label = max(sorted(grouped), key=grouped.get)
        labels.append(label)
        purities.append(grouped[label] / len(valid))
    table["class_name"] = labels
    table["dominant_fraction"] = purities
    table["reference_valid_fraction"] = valid_fracs
    if table.reference_valid_fraction.lt(0.95).any():
        raise ValueError("Every demo cell needs >=95% valid WorldCover support.")
    table["demo_split"] = np.where(
        table.grid_col < WEST_COLS,
        "west",
        np.where(table.grid_col < WEST_COLS + BUFFER_COLS, "buffer", "east"),
    )

    # Verify the public sampling route against complete overview reads, including south-up COGs.
    probe = np.linspace(0, len(table) - 1, 64, dtype=int)
    with rasterio.Env(**env):
        sampled = sample_aef(
            table.loc[probe, ["center_lon", "center_lat"]].to_numpy(), tiles=tiles, overview_level=6
        ).data
    np.testing.assert_array_equal(sampled, x[probe])

    canonical = table.to_csv(index=False, lineterminator="\n", float_format="%.12g").encode()
    if not args.repin:
        if sha256(x.tobytes()) != pinned["array_sha256"]:
            raise ValueError("Rebuilt features differ from the pinned regional sample.")
        if sha256(canonical) != pinned["files"]["samples.csv"]["sha256"]:
            raise ValueError("Rebuilt coordinates/labels differ from pinned samples.csv.")
    out.mkdir(parents=True, exist_ok=True)
    (out / "excluded.csv").unlink(missing_ok=True)
    (out / "samples.csv").write_bytes(canonical)
    np.savez_compressed(out / "features.npz", tile_id=table.tile_id.to_numpy(dtype="U"), features=x)
    meta = dict(
        name="San Francisco Bay Area and surroundings",
        year=2021,
        bounds=[
            round(float(table[c].agg(f)), 4)
            for c, f in [("minlon", "min"), ("minlat", "min"), ("maxlon", "max"), ("maxlat", "max")]
        ],
        grid=dict(GRID, cell_m=CELL, rows=int(rows), cols=int(cols)),
        nominal_size_km=[cols * CELL / 1000, rows * CELL / 1000],
        scope="Regional software demonstration, not a paper benchmark reproduction",
        license="CC-BY-4.0",
        tiles=tiles,
        overview_level=6,
        features="Official 1280m AEF overview cells: normalized sums of native vectors, decoded from int8; not 10m point vectors",
        labels="WorldCover 2021 v200 grouped majority of native 10m pixel centers inside each AEF cell polygon; minimum 95% valid reference support",
        attribution="The AlphaEarth Foundations Satellite Embedding dataset is produced by Google and Google DeepMind. © ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium.",
        source="https://developers.google.com/earth-engine/guides/aef_on_gcs_readme",
        worldcover_source=WC,
        selection="Every cell of a whole-cell 72 x 88 rectangle on the official 1280m AEF overview grid (UTM 10N); all cells have complete AEF vectors and >=95% reference support; no score-based selection",
        split=f"Two spatial folds by grid column: west columns 0-{WEST_COLS - 1}, buffer columns {WEST_COLS}-{WEST_COLS + BUFFER_COLS - 1} ({BUFFER_COLS * CELL / 1000:g} km), east columns {WEST_COLS + BUFFER_COLS}-{cols - 1}. Each fold is predicted by a model fitted only on the other. Four-class built/vegetation/cropland/water task; other labels are not scored.",
        cells=len(table),
        aef_sources=receipts,
        worldcover_window=dict(shape=list(landcover.shape), sha256=wc_hash, bytes=landcover.nbytes),
        array_sha256=sha256(x.tobytes()),
        seconds=round(time.perf_counter() - start, 2),
    )
    meta["files"] = {
        p.name: dict(sha256=sha256(p.read_bytes()), bytes=p.stat().st_size)
        for p in sorted(out.iterdir())
        if p.name != "manifest.json"
    }
    (out / "manifest.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
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
