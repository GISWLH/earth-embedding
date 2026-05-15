from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parent
DEFAULT_DATA_DIR = ROOT.parent / "data" / "part2_20260507_2x_ne"
DEFAULT_ROI = ROOT / "roi_wuhan_east_lake_2x_ne.geojson"
DEFAULT_OUT_DIR = ROOT / "results" / "wuhan_east_lake_2x_ne_original_rgb"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Draw the Wuhan East Lake 2x NE ROI original RGB reference map."
    )
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--roi", type=Path, default=DEFAULT_ROI)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args()


def robust_scale01(x: np.ndarray, lo: float = 2.0, hi: float = 98.0) -> np.ndarray:
    x = np.asarray(x, dtype=np.float32)
    if not np.isfinite(x).any():
        return np.zeros_like(x, dtype=np.float32)
    low = float(np.nanpercentile(x, lo))
    high = float(np.nanpercentile(x, hi))
    scale = max(high - low, 1e-6)
    return np.clip((x - low) / scale, 0.0, 1.0)


def load_roi(path: Path) -> tuple[tuple[float, float, float, float], dict[str, Any]]:
    data = json.loads(path.read_text())
    feature = data["features"][0]
    coords = feature["geometry"]["coordinates"][0]
    xs = [float(p[0]) for p in coords]
    ys = [float(p[1]) for p in coords]
    return (min(xs), min(ys), max(xs), max(ys)), feature.get("properties", {})


def load_block_rgb(path: Path) -> tuple[np.ndarray, tuple[float, float, float, float]]:
    data = np.load(path, allow_pickle=True)
    arr = np.asarray(data["array"], dtype=np.float32)
    bands = [str(x) for x in data["bands"].tolist()]
    band_index = {name: idx for idx, name in enumerate(bands)}
    rgb = np.stack(
        [
            robust_scale01(arr[band_index["B4"]]),
            robust_scale01(arr[band_index["B3"]]),
            robust_scale01(arr[band_index["B2"]]),
        ],
        axis=-1,
    )
    bbox = tuple(float(v) for v in np.asarray(data["bbox"], dtype=float).tolist())
    return rgb, bbox


def block_id_parts(path: Path) -> tuple[int, int]:
    stem = path.stem
    row_s, col_s = stem.split("_")[1:]
    return int(row_s[1:]), int(col_s[1:])


def load_available_mosaic(
    imagery_dir: Path,
) -> tuple[np.ndarray, tuple[float, float, float, float], list[dict[str, Any]]]:
    paths = sorted(imagery_dir.glob("block_r*_c*.npz"))
    if not paths:
        raise FileNotFoundError(f"No Sentinel-2 block NPZ files found under {imagery_dir}")

    loaded: list[tuple[Path, np.ndarray, tuple[float, float, float, float], int, int]] = []
    for path in paths:
        rgb, bbox = load_block_rgb(path)
        row, col = block_id_parts(path)
        loaded.append((path, rgb, bbox, row, col))

    row_lat = {
        row: max(bbox[3] for _, _, bbox, r, _ in loaded if r == row)
        for row in {row for _, _, _, row, _ in loaded}
    }
    col_lon = {
        col: min(bbox[0] for _, _, bbox, _, c in loaded if c == col)
        for col in {col for _, _, _, _, col in loaded}
    }
    rows = sorted(row_lat, key=lambda row: row_lat[row], reverse=True)
    cols = sorted(col_lon, key=lambda col: col_lon[col])
    row_heights = {row: max(rgb.shape[0] for _, rgb, _, r, _ in loaded if r == row) for row in rows}
    col_widths = {col: max(rgb.shape[1] for _, rgb, _, _, c in loaded if c == col) for col in cols}
    row_offsets: dict[int, int] = {}
    col_offsets: dict[int, int] = {}
    y = 0
    for row in rows:
        row_offsets[row] = y
        y += row_heights[row]
    x = 0
    for col in cols:
        col_offsets[col] = x
        x += col_widths[col]

    mosaic = np.zeros((sum(row_heights.values()), sum(col_widths.values()), 3), dtype=np.float32)
    blocks: list[dict[str, Any]] = []
    for path, rgb, bbox, row, col in loaded:
        y0 = row_offsets[row]
        x0 = col_offsets[col]
        mosaic[y0 : y0 + rgb.shape[0], x0 : x0 + rgb.shape[1], :] = rgb
        blocks.append({"path": str(path), "bbox": list(bbox), "shape": list(rgb.shape), "row": row, "col": col})

    coverage = (
        min(bbox[0] for _, _, bbox, _, _ in loaded),
        min(bbox[1] for _, _, bbox, _, _ in loaded),
        max(bbox[2] for _, _, bbox, _, _ in loaded),
        max(bbox[3] for _, _, bbox, _, _ in loaded),
    )
    return mosaic, coverage, blocks


def lonlat_to_pixel(
    lon: float,
    lat: float,
    bounds: tuple[float, float, float, float],
    width: int,
    height: int,
) -> tuple[float, float]:
    minlon, minlat, maxlon, maxlat = bounds
    x = (float(lon) - minlon) / (maxlon - minlon) * width
    y = (maxlat - float(lat)) / (maxlat - minlat) * height
    return x, y


def bbox_to_rect(
    bounds: tuple[float, float, float, float],
    canvas_bounds: tuple[float, float, float, float],
    width: int,
    height: int,
) -> tuple[float, float, float, float]:
    minlon, minlat, maxlon, maxlat = bounds
    x0, y0 = lonlat_to_pixel(minlon, maxlat, canvas_bounds, width, height)
    x1, y1 = lonlat_to_pixel(maxlon, minlat, canvas_bounds, width, height)
    return x0, y0, x1 - x0, y1 - y0


def paste_mosaic_into_roi_canvas(
    mosaic: np.ndarray,
    coverage: tuple[float, float, float, float],
    roi_bounds: tuple[float, float, float, float],
) -> np.ndarray:
    minlon, minlat, maxlon, maxlat = roi_bounds
    cov_minlon, cov_minlat, cov_maxlon, cov_maxlat = coverage
    h_m, w_m = mosaic.shape[:2]
    px_per_lon = w_m / (cov_maxlon - cov_minlon)
    px_per_lat = h_m / (cov_maxlat - cov_minlat)
    width = int(round((maxlon - minlon) * px_per_lon))
    height = int(round((maxlat - minlat) * px_per_lat))
    canvas = np.full((height, width, 3), 0.88, dtype=np.float32)

    x0 = int(round((cov_minlon - minlon) * px_per_lon))
    y0 = int(round((maxlat - cov_maxlat) * px_per_lat))
    canvas[y0 : y0 + h_m, x0 : x0 + w_m, :] = mosaic
    return canvas


def validate_block_grid(blocks: list[dict[str, Any]], roi_bounds: tuple[float, float, float, float]) -> dict[str, Any]:
    by_row: dict[int, list[dict[str, Any]]] = {}
    by_col: dict[int, list[dict[str, Any]]] = {}
    for block in blocks:
        by_row.setdefault(int(block["row"]), []).append(block)
        by_col.setdefault(int(block["col"]), []).append(block)

    row_ranges = []
    for row in sorted(by_row):
        row_blocks = sorted(by_row[row], key=lambda item: item["bbox"][0])
        lats = {(round(item["bbox"][1], 12), round(item["bbox"][3], 12)) for item in row_blocks}
        lon_edges = [row_blocks[0]["bbox"][0], *[item["bbox"][2] for item in row_blocks]]
        row_ranges.append(
            {
                "row": row,
                "lat_range": list(next(iter(lats))) if len(lats) == 1 else sorted(list(lats)),
                "lon_edges": lon_edges,
                "continuous_west_to_east": all(
                    np.isclose(row_blocks[i]["bbox"][2], row_blocks[i + 1]["bbox"][0], atol=1e-9)
                    for i in range(len(row_blocks) - 1)
                ),
            }
        )

    col_ranges = []
    for col in sorted(by_col):
        col_blocks = sorted(by_col[col], key=lambda item: item["bbox"][1])
        lons = {(round(item["bbox"][0], 12), round(item["bbox"][2], 12)) for item in col_blocks}
        lat_edges = [col_blocks[0]["bbox"][1], *[item["bbox"][3] for item in col_blocks]]
        col_ranges.append(
            {
                "col": col,
                "lon_range": list(next(iter(lons))) if len(lons) == 1 else sorted(list(lons)),
                "lat_edges": lat_edges,
                "continuous_south_to_north": all(
                    np.isclose(col_blocks[i]["bbox"][3], col_blocks[i + 1]["bbox"][1], atol=1e-9)
                    for i in range(len(col_blocks) - 1)
                ),
            }
        )

    coverage = (
        min(block["bbox"][0] for block in blocks),
        min(block["bbox"][1] for block in blocks),
        max(block["bbox"][2] for block in blocks),
        max(block["bbox"][3] for block in blocks),
    )
    row_lats = {
        row: max(float(item["bbox"][3]) for item in row_blocks) for row, row_blocks in by_row.items()
    }
    col_lons = {
        col: min(float(item["bbox"][0]) for item in col_blocks) for col, col_blocks in by_col.items()
    }
    return {
        "n_blocks": len(blocks),
        "n_rows": len(by_row),
        "n_cols": len(by_col),
        "coverage": list(coverage),
        "coverage_matches_roi": bool(np.allclose(np.asarray(coverage), np.asarray(roi_bounds), atol=1e-9)),
        "rows_continuous": all(item["continuous_west_to_east"] for item in row_ranges),
        "cols_continuous": all(item["continuous_south_to_north"] for item in col_ranges),
        "row_order_for_mosaic": sorted(row_lats, key=lambda row: row_lats[row], reverse=True),
        "col_order_for_mosaic": sorted(col_lons, key=lambda col: col_lons[col]),
        "row_ranges": row_ranges,
        "col_ranges": col_ranges,
    }


def draw_figure(
    *,
    canvas: np.ndarray,
    roi_bounds: tuple[float, float, float, float],
    coverage: tuple[float, float, float, float],
    original_bounds: tuple[float, float, float, float] | None,
    out_path: Path,
) -> None:
    height, width = canvas.shape[:2]
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    ax.imshow(canvas)
    ax.set_title("original RGB\nWuhan East Lake 2x NE ROI", fontsize=11)
    ax.axis("off")

    cov_rect = bbox_to_rect(coverage, roi_bounds, width, height)
    ax.add_patch(
        Rectangle(
            (cov_rect[0], cov_rect[1]),
            cov_rect[2],
            cov_rect[3],
            fill=False,
            edgecolor="#ffffff",
            linewidth=1.7,
        )
    )
    ax.text(
        cov_rect[0] + 12,
        cov_rect[1] + 24,
        "available Sentinel-2 RGB",
        color="#ffffff",
        fontsize=8,
        weight="bold",
        bbox={"facecolor": "#111111", "alpha": 0.55, "edgecolor": "none", "pad": 2},
    )

    if original_bounds is not None:
        orig_rect = bbox_to_rect(original_bounds, roi_bounds, width, height)
        ax.add_patch(
            Rectangle(
                (orig_rect[0], orig_rect[1]),
                orig_rect[2],
                orig_rect[3],
                fill=False,
                edgecolor="#f5d547",
                linewidth=1.6,
                linestyle="--",
            )
        )
        ax.text(
            orig_rect[0] + 12,
            orig_rect[1] + orig_rect[3] - 18,
            "original ROI",
            color="#111111",
            fontsize=8,
            weight="bold",
            bbox={"facecolor": "#f5d547", "alpha": 0.82, "edgecolor": "none", "pad": 2},
        )

    ax.text(
        width - 12,
        24,
        "2x NE ROI",
        color="#111111",
        fontsize=9,
        weight="bold",
        ha="right",
        bbox={"facecolor": "#ffffff", "alpha": 0.78, "edgecolor": "none", "pad": 2},
    )
    fig.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    roi_bounds, props = load_roi(args.roi)
    imagery_dir = args.data_dir / "region_a" / "imagery_s2_20210501_20211031"
    mosaic, coverage, blocks = load_available_mosaic(imagery_dir)
    canvas = paste_mosaic_into_roi_canvas(mosaic, coverage, roi_bounds)

    original_bounds = props.get("original_bounds")
    original_bounds_tuple = tuple(float(v) for v in original_bounds) if original_bounds else None
    out_path = args.out_dir / "wuhan_east_lake_2x_ne_original_rgb.png"
    draw_figure(
        canvas=canvas,
        roi_bounds=roi_bounds,
        coverage=coverage,
        original_bounds=original_bounds_tuple,
        out_path=out_path,
    )
    np.savez_compressed(args.out_dir / "wuhan_east_lake_2x_ne_original_rgb_canvas.npz", rgb=canvas)
    coverage_matches_roi = np.allclose(np.asarray(coverage), np.asarray(roi_bounds), atol=1e-9)
    notes = [
        "RGB rendering uses the same per-band 2-98 percentile robust stretch as the public19 reference figure.",
    ]
    if coverage_matches_roi:
        notes.append("The requested 2x NE ROI is fully covered by downloaded Sentinel-2 blocks.")
    else:
        notes.append(
            "Gray area is inside the requested 2x NE ROI but outside the currently downloaded Sentinel-2 block coverage."
        )

    manifest = {
        "roi_geojson": str(args.roi),
        "roi_bounds": list(roi_bounds),
        "roi_properties": props,
        "available_s2_coverage": list(coverage),
        "coverage_matches_roi": bool(coverage_matches_roi),
        "grid_validation": validate_block_grid(blocks, roi_bounds),
        "output_png": str(out_path),
        "output_npz": str(args.out_dir / "wuhan_east_lake_2x_ne_original_rgb_canvas.npz"),
        "blocks": blocks,
        "notes": notes,
    }
    (args.out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
