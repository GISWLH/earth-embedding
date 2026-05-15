from __future__ import annotations

import argparse
import json
import math
import time
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path

import ee
import numpy as np
import pandas as pd
from pyproj import Transformer

from rs_embed.core.specs import BBox, SensorSpec, TemporalSpec
from rs_embed.providers.gee import GEEProvider
from rs_embed.providers.gee_utils import _fetch_provider_array_chw_with_bbox_fallback


ROOT = Path(__file__).resolve().parent
DEFAULT_OUT = ROOT.parent / "data" / "part2"
REGION_A_ROI = ROOT / "roi_wuhan_east_lake.geojson"

REGION_B_BBOX = (110.0, 28.0, 122.0, 33.5)
REGION_B_CELL_DEG = 0.25

WC_CODES = {
    "trees": (10,),
    "shrubland": (20,),
    "grassland": (30,),
    "cropland": (40,),
    "built": (50,),
    "bare_sparse": (60,),
    "snow_ice": (70,),
    "water": (80,),
    "wetland": (90,),
    "mangroves": (95,),
    "moss_lichen": (100,),
}

LOCAL_4CLASS = {
    "water": ("water",),
    "vegetation": ("trees", "shrubland", "grassland", "wetland", "mangroves", "moss_lichen"),
    "cropland": ("cropland",),
    "built": ("built", "bare_sparse"),
}

REGIONAL_4CLASS = {
    "water": ("water",),
    "cropland": ("cropland",),
    "forest_green": ("trees", "shrubland", "grassland", "wetland", "mangroves", "moss_lichen"),
    "built": ("built", "bare_sparse"),
}


@dataclass(frozen=True)
class RegionBlock:
    block_id: str
    row: int
    col: int
    minlon: float
    minlat: float
    maxlon: float
    maxlat: float

    def to_bbox(self) -> BBox:
        return BBox(self.minlon, self.minlat, self.maxlon, self.maxlat)


@dataclass(frozen=True)
class TileRecord:
    tile_id: str
    row: int
    col: int
    center_lon: float
    center_lat: float
    minlon: float
    minlat: float
    maxlon: float
    maxlat: float
    tile_size_m: int


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Prepare two-region data for the part-2 benchmark.")
    p.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    p.add_argument("--region-a-roi", type=Path, default=REGION_A_ROI)
    p.add_argument("--region-a-blocks-x", type=int, default=4)
    p.add_argument("--region-a-blocks-y", type=int, default=4)
    p.add_argument("--region-a-max-blocks", type=int, default=None)
    p.add_argument("--region-a-tile-size-m", type=int, default=500)
    p.add_argument("--region-a-tile-chunk-size", type=int, default=64)
    p.add_argument("--region-b-cell-chunk-size", type=int, default=64)
    p.add_argument("--region-b-max-cells", type=int, default=None)
    p.add_argument("--skip-region-a-imagery", action="store_true")
    p.add_argument("--skip-region-a-label-blocks", action="store_true")
    p.add_argument("--skip-region-a-manifest", action="store_true")
    p.add_argument("--skip-region-b-manifest", action="store_true")
    p.add_argument("--overwrite", action="store_true")
    return p.parse_args()


def load_roi_bounds(path: Path) -> tuple[float, float, float, float]:
    data = json.loads(path.read_text())
    coords = data["features"][0]["geometry"]["coordinates"][0]
    xs = [float(p[0]) for p in coords]
    ys = [float(p[1]) for p in coords]
    return min(xs), min(ys), max(xs), max(ys)


def split_bbox(bounds: tuple[float, float, float, float], nx: int, ny: int) -> list[RegionBlock]:
    minlon, minlat, maxlon, maxlat = bounds
    blocks: list[RegionBlock] = []
    for row in range(ny):
        for col in range(nx):
            x0 = minlon + (maxlon - minlon) * col / nx
            x1 = minlon + (maxlon - minlon) * (col + 1) / nx
            y0 = minlat + (maxlat - minlat) * row / ny
            y1 = minlat + (maxlat - minlat) * (row + 1) / ny
            blocks.append(
                RegionBlock(
                    block_id=f"block_r{row:02d}_c{col:02d}",
                    row=row,
                    col=col,
                    minlon=x0,
                    minlat=y0,
                    maxlon=x1,
                    maxlat=y1,
                )
            )
    return blocks


def build_region_a_tiles(
    bounds: tuple[float, float, float, float],
    *,
    tile_size_m: int,
) -> list[TileRecord]:
    tx = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    inv = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)
    minlon, minlat, maxlon, maxlat = bounds
    minx, miny = tx.transform(minlon, minlat)
    maxx, maxy = tx.transform(maxlon, maxlat)
    size = float(tile_size_m)
    ncols = int(math.floor((maxx - minx) / size))
    nrows = int(math.floor((maxy - miny) / size))
    tiles: list[TileRecord] = []
    for row in range(nrows):
        for col in range(ncols):
            x0 = minx + col * size
            x1 = x0 + size
            y0 = miny + row * size
            y1 = y0 + size
            c_lon, c_lat = inv.transform((x0 + x1) / 2.0, (y0 + y1) / 2.0)
            lon0, lat0 = inv.transform(x0, y0)
            lon1, lat1 = inv.transform(x1, y1)
            tiles.append(
                TileRecord(
                    tile_id=f"tile_r{row:03d}_c{col:03d}",
                    row=row,
                    col=col,
                    center_lon=c_lon,
                    center_lat=c_lat,
                    minlon=min(lon0, lon1),
                    minlat=min(lat0, lat1),
                    maxlon=max(lon0, lon1),
                    maxlat=max(lat0, lat1),
                    tile_size_m=tile_size_m,
                )
            )
    return tiles


def build_region_b_cells(
    bounds: tuple[float, float, float, float],
    *,
    step_deg: float,
    max_cells: int | None = None,
) -> list[dict[str, float | str | int]]:
    minlon, minlat, maxlon, maxlat = bounds
    rows = int(round((maxlat - minlat) / step_deg))
    cols = int(round((maxlon - minlon) / step_deg))
    cells: list[dict[str, float | str | int]] = []
    for row in range(rows):
        for col in range(cols):
            x0 = minlon + col * step_deg
            x1 = x0 + step_deg
            y0 = minlat + row * step_deg
            y1 = y0 + step_deg
            cells.append(
                {
                    "cell_id": f"cell_r{row:02d}_c{col:02d}",
                    "row": row,
                    "col": col,
                    "minlon": x0,
                    "minlat": y0,
                    "maxlon": x1,
                    "maxlat": y1,
                    "center_lon": (x0 + x1) / 2.0,
                    "center_lat": (y0 + y1) / 2.0,
                    "cell_deg": step_deg,
                }
            )
            if max_cells is not None and len(cells) >= max_cells:
                return cells
    return cells


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def json_dump(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2))


def iter_chunks(items: list, size: int) -> Iterable[list]:
    for i in range(0, len(items), size):
        yield items[i : i + size]


def hist_to_fraction_features(hist: dict[str, float] | None) -> dict[str, float]:
    hist = hist or {}
    total = float(sum(float(v) for v in hist.values()) or 1.0)
    frac_by_name = {
        name: sum(float(hist.get(str(code), 0.0)) for code in codes) / total
        for name, codes in WC_CODES.items()
    }
    return frac_by_name


def collapse_fraction_groups(
    frac_by_name: dict[str, float],
    groups: dict[str, tuple[str, ...]],
) -> dict[str, float]:
    return {name: sum(float(frac_by_name.get(src, 0.0)) for src in members) for name, members in groups.items()}


def dominant_label(fracs: dict[str, float]) -> tuple[str, float]:
    label = max(fracs, key=fracs.get)
    return label, float(fracs[label])


def temporal_to_dict(temporal: TemporalSpec | None) -> dict[str, object] | None:
    if temporal is None:
        return None
    return {
        "mode": temporal.mode,
        "year": temporal.year if isinstance(temporal.year, int) else None,
        "start": temporal.start,
        "end": temporal.end,
    }


def fetch_image_array(
    provider: GEEProvider,
    *,
    image: ee.Image,
    bbox: BBox,
    bands: tuple[str, ...],
    scale_m: int,
    fill_value: float,
    collection_name: str,
) -> np.ndarray:
    return _fetch_provider_array_chw_with_bbox_fallback(
        provider,
        image=image,
        spatial=bbox,
        bands=bands,
        scale_m=scale_m,
        fill_value=fill_value,
        collection=collection_name,
    )


def build_s2_image(
    provider: GEEProvider,
    *,
    bbox: BBox,
    temporal: TemporalSpec,
    sensor: SensorSpec,
) -> ee.Image:
    region = provider.get_region(bbox)
    return provider.build_image(sensor=sensor, temporal=temporal, region=region)


def save_block_array(
    out_path: Path,
    *,
    array: np.ndarray,
    block: RegionBlock,
    bands: tuple[str, ...],
    temporal: dict | None,
    source: str,
) -> None:
    ensure_dir(out_path.parent)
    np.savez_compressed(
        out_path,
        array=array.astype(np.float32),
        bands=np.asarray(bands, dtype=object),
        bbox=np.asarray([block.minlon, block.minlat, block.maxlon, block.maxlat], dtype=np.float64),
    )
    meta = {
        "block": asdict(block),
        "bands": list(bands),
        "shape": list(array.shape),
        "dtype": str(array.dtype),
        "source": source,
        "temporal": temporal,
    }
    json_dump(out_path.with_suffix(".json"), meta)


def prepare_region_a_blocks(
    provider: GEEProvider,
    *,
    bounds: tuple[float, float, float, float],
    out_dir: Path,
    blocks_x: int,
    blocks_y: int,
    max_blocks: int | None,
    overwrite: bool,
    include_imagery: bool,
    include_label_blocks: bool,
) -> dict[str, object]:
    blocks = split_bbox(bounds, blocks_x, blocks_y)
    if max_blocks is not None:
        blocks = blocks[:max_blocks]

    s2_sensor = SensorSpec(
        collection="COPERNICUS/S2_SR_HARMONIZED",
        bands=("B2", "B3", "B4", "B5", "B6", "B7", "B8", "B8A", "B11", "B12"),
        scale_m=10,
        cloudy_pct=30,
        composite="median",
        fill_value=0.0,
    )
    s2_sensor_12b = SensorSpec(
        collection="COPERNICUS/S2_SR_HARMONIZED",
        bands=("B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B8A", "B9", "B11", "B12"),
        scale_m=10,
        cloudy_pct=30,
        composite="median",
        fill_value=0.0,
    )
    s2_temporal = TemporalSpec.range("2021-05-01", "2021-10-31")
    wc_img = ee.ImageCollection("ESA/WorldCover/v200").first().select("Map").toFloat()
    jrc_img = ee.Image("JRC/GSW1_4/GlobalSurfaceWater").select("occurrence").toFloat()

    s2_out = out_dir / "region_a" / "imagery_s2_20210501_20211031"
    s2_out_12b = out_dir / "region_a" / "imagery_s2_12b_20210501_20211031"
    wc_out = out_dir / "region_a" / "worldcover_2021_blocks"
    jrc_out = out_dir / "region_a" / "jrc_occurrence_blocks"
    ensure_dir(s2_out)
    ensure_dir(s2_out_12b)
    ensure_dir(wc_out)
    ensure_dir(jrc_out)

    records: list[dict[str, object]] = []
    for idx, block in enumerate(blocks, start=1):
        bbox = block.to_bbox()
        block_rec: dict[str, object] = {"block_id": block.block_id}
        if include_imagery:
            out_path = s2_out / f"{block.block_id}.npz"
            if overwrite or not out_path.exists():
                t0 = time.perf_counter()
                s2_img = build_s2_image(provider, bbox=bbox, temporal=s2_temporal, sensor=s2_sensor)
                arr = fetch_image_array(
                    provider,
                    image=s2_img,
                    bbox=bbox,
                    bands=s2_sensor.bands,
                    scale_m=s2_sensor.scale_m,
                    fill_value=s2_sensor.fill_value,
                    collection_name=s2_sensor.collection,
                )
                save_block_array(
                    out_path,
                    array=arr,
                    block=block,
                    bands=s2_sensor.bands,
                    temporal=temporal_to_dict(s2_temporal),
                    source=s2_sensor.collection,
                )
                block_rec["s2_sec"] = round(time.perf_counter() - t0, 2)
                block_rec["s2_shape"] = list(arr.shape)
                block_rec["s2_mb"] = round(arr.nbytes / 1e6, 2)
            else:
                block_rec["s2_skipped"] = True

            out_path_12b = s2_out_12b / f"{block.block_id}.npz"
            if overwrite or not out_path_12b.exists():
                t0 = time.perf_counter()
                s2_img_12b = build_s2_image(provider, bbox=bbox, temporal=s2_temporal, sensor=s2_sensor_12b)
                arr_12b = fetch_image_array(
                    provider,
                    image=s2_img_12b,
                    bbox=bbox,
                    bands=s2_sensor_12b.bands,
                    scale_m=s2_sensor_12b.scale_m,
                    fill_value=s2_sensor_12b.fill_value,
                    collection_name=s2_sensor_12b.collection,
                )
                save_block_array(
                    out_path_12b,
                    array=arr_12b,
                    block=block,
                    bands=s2_sensor_12b.bands,
                    temporal=temporal_to_dict(s2_temporal),
                    source=s2_sensor_12b.collection,
                )
                block_rec["s2_12b_sec"] = round(time.perf_counter() - t0, 2)
                block_rec["s2_12b_shape"] = list(arr_12b.shape)
                block_rec["s2_12b_mb"] = round(arr_12b.nbytes / 1e6, 2)
            else:
                block_rec["s2_12b_skipped"] = True
        if include_label_blocks:
            for name, image, bands, scale_m in (
                ("worldcover", wc_img, ("Map",), 10),
                ("jrc_occurrence", jrc_img, ("occurrence",), 30),
            ):
                base = wc_out if name == "worldcover" else jrc_out
                out_path = base / f"{block.block_id}.npz"
                if overwrite or not out_path.exists():
                    t0 = time.perf_counter()
                    arr = fetch_image_array(
                        provider,
                        image=image,
                        bbox=bbox,
                        bands=bands,
                        scale_m=scale_m,
                        fill_value=0.0,
                        collection_name=name,
                    )
                    save_block_array(
                        out_path,
                        array=arr,
                        block=block,
                        bands=bands,
                        temporal=None,
                        source=name,
                    )
                    block_rec[f"{name}_sec"] = round(time.perf_counter() - t0, 2)
                    block_rec[f"{name}_shape"] = list(arr.shape)
                else:
                    block_rec[f"{name}_skipped"] = True
        records.append(block_rec)
        print(f"[Region A] {idx}/{len(blocks)} done: {block.block_id}")

    summary = {
        "bounds": list(bounds),
        "blocks_x": blocks_x,
        "blocks_y": blocks_y,
        "n_blocks": len(blocks),
        "records": records,
    }
    json_dump(out_dir / "region_a" / "download_summary.json", summary)
    return summary


def reduce_regions_chunk(
    *,
    image: ee.Image,
    features: list[ee.Feature],
    reducer: ee.Reducer,
    scale: int,
    tile_scale: int = 4,
) -> list[dict]:
    fc = ee.FeatureCollection(features)
    out = image.reduceRegions(collection=fc, reducer=reducer, scale=scale, tileScale=tile_scale).getInfo()
    return out["features"]


def prepare_region_a_manifest(
    *,
    tiles: list[TileRecord],
    out_dir: Path,
    chunk_size: int,
    overwrite: bool,
) -> dict[str, object]:
    out_path = out_dir / "region_a" / "tile_manifest_500m.csv"
    if out_path.exists() and not overwrite:
        df = pd.read_csv(out_path)
        return {"path": str(out_path), "n_rows": int(len(df)), "skipped": True}

    worldcover = ee.ImageCollection("ESA/WorldCover/v200").first().select("Map")
    jrc = ee.Image("JRC/GSW1_4/GlobalSurfaceWater").select("occurrence")

    rows: list[dict[str, object]] = []
    total_chunks = int(math.ceil(len(tiles) / chunk_size))
    for chunk_idx, chunk in enumerate(iter_chunks(tiles, chunk_size), start=1):
        features = []
        for tile in chunk:
            geom = ee.Geometry.Rectangle(
                [tile.minlon, tile.minlat, tile.maxlon, tile.maxlat],
                geodesic=False,
            )
            features.append(ee.Feature(geom, {"tile_id": tile.tile_id}))

        wc_info = reduce_regions_chunk(
            image=worldcover,
            features=features,
            reducer=ee.Reducer.frequencyHistogram(),
            scale=10,
            tile_scale=4,
        )
        jrc_info = reduce_regions_chunk(
            image=jrc,
            features=features,
            reducer=ee.Reducer.mean(),
            scale=30,
            tile_scale=4,
        )
        jrc_by_id = {f["properties"]["tile_id"]: f["properties"].get("mean", 0.0) for f in jrc_info}
        for tile, wc_feat in zip(chunk, wc_info, strict=True):
            props = wc_feat["properties"]
            hist = props.get("histogram") or {}
            frac_names = hist_to_fraction_features(hist)
            frac_local = collapse_fraction_groups(frac_names, LOCAL_4CLASS)
            dominant_local, dominant_frac = dominant_label(frac_local)
            row = asdict(tile)
            for k, v in frac_names.items():
                row[f"wc_{k}_frac"] = round(float(v), 6)
            for k, v in frac_local.items():
                row[f"local_{k}_frac"] = round(float(v), 6)
            row["local_dominant_class"] = dominant_local
            row["local_dominant_frac"] = round(float(dominant_frac), 6)
            row["jrc_occurrence_mean"] = round(float(jrc_by_id.get(tile.tile_id, 0.0) or 0.0), 6)
            row["jrc_water_binary_frac"] = round(row["jrc_occurrence_mean"] / 100.0, 6)
            rows.append(row)
        print(f"[Region A manifest] chunk {chunk_idx}/{total_chunks} done")

    df = pd.DataFrame(rows).sort_values("tile_id").reset_index(drop=True)
    ensure_dir(out_path.parent)
    df.to_csv(out_path, index=False)
    summary = {
        "path": str(out_path),
        "n_rows": int(len(df)),
        "class_counts": df["local_dominant_class"].value_counts().to_dict(),
    }
    json_dump(out_dir / "region_a" / "tile_manifest_summary.json", summary)
    return summary


def prepare_region_b_manifest(
    *,
    cells: list[dict[str, float | str | int]],
    out_dir: Path,
    chunk_size: int,
    overwrite: bool,
) -> dict[str, object]:
    out_path = out_dir / "region_b" / "cell_manifest_025deg.csv"
    if out_path.exists() and not overwrite:
        df = pd.read_csv(out_path)
        return {"path": str(out_path), "n_rows": int(len(df)), "skipped": True}

    worldcover = ee.ImageCollection("ESA/WorldCover/v200").first().select("Map")
    jrc = ee.Image("JRC/GSW1_4/GlobalSurfaceWater").select("occurrence")

    rows: list[dict[str, object]] = []
    total_chunks = int(math.ceil(len(cells) / chunk_size))
    for chunk_idx, chunk in enumerate(iter_chunks(cells, chunk_size), start=1):
        features = []
        for cell in chunk:
            geom = ee.Geometry.Rectangle(
                [cell["minlon"], cell["minlat"], cell["maxlon"], cell["maxlat"]],
                geodesic=False,
            )
            features.append(ee.Feature(geom, {"cell_id": cell["cell_id"]}))

        wc_info = reduce_regions_chunk(
            image=worldcover,
            features=features,
            reducer=ee.Reducer.frequencyHistogram(),
            scale=10,
            tile_scale=4,
        )
        jrc_info = reduce_regions_chunk(
            image=jrc,
            features=features,
            reducer=ee.Reducer.mean(),
            scale=30,
            tile_scale=4,
        )
        jrc_by_id = {f["properties"]["cell_id"]: f["properties"].get("mean", 0.0) for f in jrc_info}
        for cell, wc_feat in zip(chunk, wc_info, strict=True):
            props = wc_feat["properties"]
            hist = props.get("histogram") or {}
            frac_names = hist_to_fraction_features(hist)
            frac_regional = collapse_fraction_groups(frac_names, REGIONAL_4CLASS)
            dominant_regional, dominant_frac = dominant_label(frac_regional)
            row = dict(cell)
            for k, v in frac_names.items():
                row[f"wc_{k}_frac"] = round(float(v), 6)
            for k, v in frac_regional.items():
                row[f"regional_{k}_frac"] = round(float(v), 6)
            row["regional_dominant_class"] = dominant_regional
            row["regional_dominant_frac"] = round(float(dominant_frac), 6)
            row["jrc_occurrence_mean"] = round(float(jrc_by_id.get(cell["cell_id"], 0.0) or 0.0), 6)
            row["jrc_water_binary_frac"] = round(row["jrc_occurrence_mean"] / 100.0, 6)
            rows.append(row)
        print(f"[Region B manifest] chunk {chunk_idx}/{total_chunks} done")

    df = pd.DataFrame(rows).sort_values("cell_id").reset_index(drop=True)
    ensure_dir(out_path.parent)
    df.to_csv(out_path, index=False)
    summary = {
        "path": str(out_path),
        "n_rows": int(len(df)),
        "class_counts": df["regional_dominant_class"].value_counts().to_dict(),
    }
    json_dump(out_dir / "region_b" / "cell_manifest_summary.json", summary)
    return summary


def main() -> None:
    args = parse_args()
    ensure_dir(args.out_dir)

    provider = GEEProvider()
    provider.ensure_ready()
    ee.Initialize()

    region_a_bounds = load_roi_bounds(args.region_a_roi)
    region_b_bounds = REGION_B_BBOX

    global_summary: dict[str, object] = {
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "region_a_bounds": list(region_a_bounds),
        "region_b_bounds": list(region_b_bounds),
    }

    if not args.skip_region_a_imagery or not args.skip_region_a_label_blocks:
        global_summary["region_a_blocks"] = prepare_region_a_blocks(
            provider,
            bounds=region_a_bounds,
            out_dir=args.out_dir,
            blocks_x=args.region_a_blocks_x,
            blocks_y=args.region_a_blocks_y,
            max_blocks=args.region_a_max_blocks,
            overwrite=args.overwrite,
            include_imagery=not args.skip_region_a_imagery,
            include_label_blocks=not args.skip_region_a_label_blocks,
        )

    if not args.skip_region_a_manifest:
        tiles = build_region_a_tiles(region_a_bounds, tile_size_m=args.region_a_tile_size_m)
        global_summary["region_a_manifest"] = prepare_region_a_manifest(
            tiles=tiles,
            out_dir=args.out_dir,
            chunk_size=args.region_a_tile_chunk_size,
            overwrite=args.overwrite,
        )

    if not args.skip_region_b_manifest:
        cells = build_region_b_cells(
            region_b_bounds,
            step_deg=REGION_B_CELL_DEG,
            max_cells=args.region_b_max_cells,
        )
        global_summary["region_b_manifest"] = prepare_region_b_manifest(
            cells=cells,
            out_dir=args.out_dir,
            chunk_size=args.region_b_cell_chunk_size,
            overwrite=args.overwrite,
        )

    json_dump(args.out_dir / "prepare_part2_data_summary.json", global_summary)
    print(json.dumps(global_summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
