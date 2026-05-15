from __future__ import annotations

import argparse
import json
import math
import os
import re
import time
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from rs_embed import OutputSpec, TemporalSpec, get_embedding
from rs_embed.core.specs import BBox, PointBuffer

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
DEFAULT_DATA_DIR = ROOT.parent / "data" / "part2_20260502_full"
DEFAULT_OUT_DIR = ROOT / "results" / "part2_model_map_figure"

PUBLIC_MODELS = [
    "gse",
    "remoteclip",
    "copernicus",
    "tessera",
    "satmae",
    "satmaepp",
    "satmaepp_s2_10b",
    "scalemae",
    "anysat",
    "galileo",
    "wildsat",
    "prithvi",
    "terrafm",
    "terramind",
    "dofa",
    "fomo",
    "thor",
    "agrifm",
    "satvision",
]
YEAR_MODELS = {"gse": 2021, "copernicus": 2021, "tessera": 2024}
COARSE_BUFFER_MODELS = {"copernicus": 15_000.0, "satvision": 3_000.0}
EMBED_DIMS = (64, 128, 256, 384, 512, 768, 1024, 1536, 2048, 4096)
REFERENCE_ROW = 1
REFERENCE_COL = 1
GRID_SIZE = 2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the part-2 public19 figure over a 2x2 expansion of block_r01_c01."
    )
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--models", nargs="+", default=PUBLIC_MODELS)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--max-sample-pixels", type=int, default=120_000)
    parser.add_argument("--seed", type=int, default=11)
    return parser.parse_args()


def robust_scale01(x: np.ndarray, lo: float = 2.0, hi: float = 98.0) -> np.ndarray:
    x = np.asarray(x, dtype=np.float32)
    if not np.isfinite(x).any():
        return np.zeros_like(x, dtype=np.float32)
    low = float(np.nanpercentile(x, lo))
    high = float(np.nanpercentile(x, hi))
    scale = max(high - low, 1e-6)
    return np.clip((x - low) / scale, 0.0, 1.0)


def to_dhw(arr: Any) -> np.ndarray:
    if hasattr(arr, "values"):
        arr = arr.values
    x = np.asarray(arr, dtype=np.float32)
    if x.ndim != 3:
        raise ValueError(f"Expected 3D embedding grid, got {x.shape}")
    if x.shape[0] in EMBED_DIMS:
        return x
    if x.shape[-1] in EMBED_DIMS:
        return np.moveaxis(x, -1, 0)
    raise ValueError(f"Could not infer embedding layout for shape {x.shape}")


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(payload, indent=2))
    os.replace(tmp_path, path)


def save_npz_atomic(path: Path, **arrays: Any) -> None:
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("wb") as f:
        np.savez_compressed(f, **arrays)
    os.replace(tmp_path, path)


def load_block_specs(data_dir: Path) -> list[dict[str, Any]]:
    imagery_dir = data_dir / "region_a" / "imagery_s2_20210501_20211031"
    specs: list[dict[str, Any]] = []
    wanted = {
        (REFERENCE_ROW + row_offset, REFERENCE_COL + col_offset)
        for row_offset in range(GRID_SIZE)
        for col_offset in range(GRID_SIZE)
    }
    for path in sorted(imagery_dir.glob("block_r*_c*.npz")):
        match = re.match(r"block_r(\d+)_c(\d+)\.npz", path.name)
        if match is None:
            continue
        row = int(match.group(1))
        col = int(match.group(2))
        if (row, col) not in wanted:
            continue
        with np.load(path, allow_pickle=True) as data:
            arr = np.asarray(data["array"], dtype=np.float32)
            bbox = np.asarray(data["bbox"], dtype=float)
            bands = [str(x) for x in data["bands"].tolist()]
        specs.append(
            {
                "block_id": path.stem,
                "row": row,
                "col": col,
                "bbox": BBox(
                    minlon=float(bbox[0]),
                    minlat=float(bbox[1]),
                    maxlon=float(bbox[2]),
                    maxlat=float(bbox[3]),
                ),
                "bbox_values": [float(v) for v in bbox.tolist()],
                "input_chw": arr,
                "bands": bands,
            }
        )
    found = {(int(item["row"]), int(item["col"])) for item in specs}
    missing = sorted(wanted - found)
    if missing:
        raise FileNotFoundError(f"Missing required 2x2 reference blocks: {missing}")
    return sorted(specs, key=lambda item: (int(item["row"]), int(item["col"])))


def block_coverage(block_specs: list[dict[str, Any]]) -> list[float]:
    bboxes = [np.asarray(item["bbox_values"], dtype=float) for item in block_specs]
    return np.min([b[:2] for b in bboxes], axis=0).tolist() + np.max(
        [b[2:] for b in bboxes], axis=0
    ).tolist()


def build_original_rgb_canvas(block_specs: list[dict[str, Any]]) -> np.ndarray:
    rows = sorted({int(item["row"]) for item in block_specs})
    cols = sorted({int(item["col"]) for item in block_specs})
    row_heights = {
        row: max(int(item["input_chw"].shape[-2]) for item in block_specs if int(item["row"]) == row)
        for row in rows
    }
    col_widths = {
        col: max(int(item["input_chw"].shape[-1]) for item in block_specs if int(item["col"]) == col)
        for col in cols
    }
    row_offsets: dict[int, int] = {}
    col_offsets: dict[int, int] = {}
    y = 0
    for row in sorted(rows, reverse=True):
        row_offsets[row] = y
        y += row_heights[row]
    x = 0
    for col in cols:
        col_offsets[col] = x
        x += col_widths[col]
    canvas = np.zeros((sum(row_heights.values()), sum(col_widths.values()), 3), dtype=np.float32)
    for item in block_specs:
        arr = np.asarray(item["input_chw"], dtype=np.float32)
        band_index = {name: idx for idx, name in enumerate(item["bands"])}
        rgb = np.stack(
            [
                robust_scale01(arr[band_index["B4"]]),
                robust_scale01(arr[band_index["B3"]]),
                robust_scale01(arr[band_index["B2"]]),
            ],
            axis=-1,
        )
        row = int(item["row"])
        col = int(item["col"])
        y0 = row_offsets[row]
        x0 = col_offsets[col]
        canvas[y0 : y0 + rgb.shape[0], x0 : x0 + rgb.shape[1], :] = rgb
    return canvas


def save_panel_png(rgb: np.ndarray, title: str, out_path: Path) -> None:
    h, w = rgb.shape[:2]
    fig_w = 3.2
    fig_h = max(2.0, fig_w / max(w / max(h, 1), 1e-6))
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.imshow(rgb, interpolation="nearest")
    ax.set_title(title, fontsize=10)
    ax.axis("off")
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def format_model_panel_title(result: dict[str, Any]) -> str:
    model = str(result["model"])
    shape = result.get("shape")
    if isinstance(shape, list) and shape:
        dims = "*".join(str(int(dim)) for dim in shape)
        return f"{model} [{dims}]"
    return model


def set_local_asset_env(model: str) -> None:
    if model == "satmaepp_s2_10b":
        os.environ["RS_EMBED_SATMAEPP_S2_CKPT_FILE"] = str(
            REPO_ROOT
            / "research_outputs"
            / "model_cache"
            / "checkpoint_ViT-L_pretrain_fmow_sentinel.pth"
        )
    elif model == "agrifm":
        os.environ["RS_EMBED_AGRIFM_CKPT"] = str(
            REPO_ROOT / "research_outputs" / "model_cache" / "AgriFM.pth"
        )
    elif model == "copernicus":
        os.environ["RS_EMBED_COP_DIR"] = str(REPO_ROOT / "data" / "copernicus_embed")
    elif model == "tessera":
        os.environ["RS_EMBED_TESSERA_CACHE"] = str(
            REPO_ROOT / "research_outputs" / "model_cache" / "geotessera_cache"
        )
    elif model == "satvision":
        os.environ["RS_EMBED_SATVISION_TOA_CKPT"] = str(
            REPO_ROOT / "research_outputs" / "model_assets_public19" / "satvision" / "snapshot"
        )
        os.environ["RS_EMBED_SATVISION_TOA_BATCH_SIZE"] = "1"
        os.environ["RS_EMBED_SATVISION_TOA_IMG"] = "128"


def temporal_for_model(model: str) -> TemporalSpec:
    if model in YEAR_MODELS:
        return TemporalSpec.year(YEAR_MODELS[model])
    return TemporalSpec.range("2021-05-01", "2021-10-31")


def spatial_for_model(model: str, bbox: BBox) -> BBox | PointBuffer:
    if model not in COARSE_BUFFER_MODELS:
        return bbox
    buffer_m = float(COARSE_BUFFER_MODELS[model])
    return PointBuffer(
        lon=float((bbox.minlon + bbox.maxlon) / 2.0),
        lat=float((bbox.minlat + bbox.maxlat) / 2.0),
        buffer_m=buffer_m,
    )


def tessera_has_local_tiles(spatial: BBox | PointBuffer, year: int) -> bool:
    if isinstance(spatial, BBox):
        bounds = (spatial.minlon, spatial.minlat, spatial.maxlon, spatial.maxlat)
    else:
        m_per_deg_lat = 111_320.0
        dlat = spatial.buffer_m / m_per_deg_lat
        dlon = spatial.buffer_m / (m_per_deg_lat * max(1e-6, math.cos(math.radians(spatial.lat))))
        bounds = (spatial.lon - dlon, spatial.lat - dlat, spatial.lon + dlon, spatial.lat + dlat)
    try:
        from geotessera import GeoTessera

        gt = GeoTessera(cache_dir=str(REPO_ROOT / "research_outputs" / "model_cache" / "geotessera_cache"))
        return bool(gt.registry.load_blocks_for_region(bounds=bounds, year=int(year)))
    except Exception:
        registry = pd.read_parquet(
            REPO_ROOT / "research_outputs" / "model_cache" / "geotessera_cache" / "registry.parquet",
            columns=["lat", "lon", "year"],
        )
        tile_min_lon = registry["lon"] - 0.05
        tile_max_lon = registry["lon"] + 0.05
        tile_min_lat = registry["lat"] - 0.05
        tile_max_lat = registry["lat"] + 0.05
        hits = registry[
            (registry["year"] == int(year))
            & (tile_max_lon >= bounds[0])
            & (tile_min_lon <= bounds[2])
            & (tile_max_lat >= bounds[1])
            & (tile_min_lat <= bounds[3])
        ]
        return not hits.empty


def load_grid_checkpoint(path: Path) -> np.ndarray | None:
    if not path.exists() or path.stat().st_size <= 0:
        return None
    try:
        with np.load(path, allow_pickle=True) as data:
            grid = np.asarray(data["embedding"], dtype=np.float32)
    except Exception:
        return None
    if grid.ndim != 3 or not np.isfinite(grid).any():
        return None
    return grid


def sample_pixels_for_pca(
    grids: list[np.ndarray],
    *,
    max_sample_pixels: int,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    per_grid = max(1024, int(np.ceil(max_sample_pixels / max(len(grids), 1))))
    samples: list[np.ndarray] = []
    for grid in grids:
        d, h, w = grid.shape
        x = grid.reshape(d, h * w).T.astype(np.float32)
        valid = np.isfinite(x).all(axis=1)
        valid_idx = np.flatnonzero(valid)
        if valid_idx.size == 0:
            continue
        take = min(per_grid, valid_idx.size)
        chosen = rng.choice(valid_idx, size=take, replace=False)
        samples.append(x[chosen])
    if not samples:
        raise RuntimeError("No finite pixels available for PCA.")
    sample = np.concatenate(samples, axis=0)
    if sample.shape[0] > max_sample_pixels:
        chosen = rng.choice(sample.shape[0], size=max_sample_pixels, replace=False)
        sample = sample[chosen]
    mean = np.nanmean(sample, axis=0, keepdims=True).astype(np.float32)
    centered = np.nan_to_num(sample - mean, nan=0.0, posinf=0.0, neginf=0.0)
    _, _, vt = np.linalg.svd(centered, full_matrices=False)
    return mean.reshape(-1), vt[:3].astype(np.float32)


def grids_to_rgb_canvas(
    block_specs: list[dict[str, Any]],
    grids: list[np.ndarray],
    *,
    mean: np.ndarray,
    comps: np.ndarray,
) -> np.ndarray:
    rows = sorted({int(item["row"]) for item in block_specs})
    cols = sorted({int(item["col"]) for item in block_specs})
    row_heights = {row: 0 for row in rows}
    col_widths = {col: 0 for col in cols}
    for item, grid in zip(block_specs, grids, strict=True):
        row = int(item["row"])
        col = int(item["col"])
        row_heights[row] = max(row_heights[row], int(grid.shape[1]))
        col_widths[col] = max(col_widths[col], int(grid.shape[2]))

    row_offsets: dict[int, int] = {}
    col_offsets: dict[int, int] = {}
    y = 0
    for row in sorted(rows, reverse=True):
        row_offsets[row] = y
        y += row_heights[row]
    x = 0
    for col in cols:
        col_offsets[col] = x
        x += col_widths[col]

    score_canvas = np.full((sum(row_heights.values()), sum(col_widths.values()), 3), np.nan, dtype=np.float32)
    for item, grid in zip(block_specs, grids, strict=True):
        d, h, w = grid.shape
        x_pixels = grid.reshape(d, h * w).T.astype(np.float32)
        valid = np.isfinite(x_pixels).all(axis=1)
        centered = np.nan_to_num(x_pixels - mean.reshape(1, -1), nan=0.0, posinf=0.0, neginf=0.0)
        scores = centered @ comps.T
        scores[~valid] = np.nan
        rgb_scores = scores.reshape(h, w, 3)
        y0 = row_offsets[int(item["row"])]
        x0 = col_offsets[int(item["col"])]
        score_canvas[y0 : y0 + h, x0 : x0 + w, :] = rgb_scores

    return np.stack([robust_scale01(score_canvas[..., i]) for i in range(3)], axis=-1).astype(np.float32)


def run_model_map_2x(
    *,
    model: str,
    block_specs: list[dict[str, Any]],
    device: str,
    out_dir: Path,
    resume: bool,
    max_sample_pixels: int,
    seed: int,
) -> dict[str, Any]:
    json_path = out_dir / f"{model}_2x.json"
    npz_path = out_dir / f"{model}_2x.npz"
    png_path = out_dir / f"{model}_2x.png"
    block_dir = out_dir / "blocks_2x" / model
    block_dir.mkdir(parents=True, exist_ok=True)
    if resume and json_path.exists() and png_path.exists() and npz_path.exists():
        return json.loads(json_path.read_text())

    set_local_asset_env(model)
    temporal = temporal_for_model(model)
    result: dict[str, Any] = {
        "model": model,
        "status": "ok",
        "reason": None,
        "output_json": str(json_path),
        "output_npz": str(npz_path),
        "output_png": str(png_path),
        "block_dir": str(block_dir),
        "n_blocks": len(block_specs),
        "temporal": temporal.mode,
    }
    t0 = time.perf_counter()
    grids: list[np.ndarray] = []
    block_records: list[dict[str, Any]] = []

    try:
        for idx, item in enumerate(block_specs, start=1):
            block_id = str(item["block_id"])
            block_npz = block_dir / f"{block_id}.npz"
            block_json = block_dir / f"{block_id}.json"
            cached = load_grid_checkpoint(block_npz)
            if cached is not None:
                grids.append(cached)
                block_records.append(
                    {
                        "block_id": block_id,
                        "status": "ok",
                        "source": "checkpoint",
                        "shape": list(cached.shape),
                        "output_npz": str(block_npz),
                    }
                )
                print(f"[{model} 2x {idx}/{len(block_specs)}] reuse {block_id}", flush=True)
                continue

            spatial = spatial_for_model(model, item["bbox"])
            print(f"[{model} 2x {idx}/{len(block_specs)}] run {block_id}", flush=True)
            block_t0 = time.perf_counter()
            try:
                if model == "tessera" and not tessera_has_local_tiles(spatial, YEAR_MODELS["tessera"]):
                    raise RuntimeError(f"No local tessera tiles were pre-cached for {block_id}.")
                emb = get_embedding(
                    model,
                    spatial=spatial,
                    temporal=temporal,
                    output=OutputSpec.grid(),
                    backend="auto",
                    device=device,
                )
            except Exception as exc:
                if model == "satvision" and "out of memory" in repr(exc).lower():
                    emb = get_embedding(
                        model,
                        spatial=spatial,
                        temporal=temporal,
                        output=OutputSpec.grid(),
                        backend="auto",
                        device="cpu",
                    )
                else:
                    raise
            grid = to_dhw(emb.data)
            if not np.isfinite(grid).any():
                raise RuntimeError(f"{model} produced no finite grid values for {block_id}")
            save_npz_atomic(
                block_npz,
                embedding=grid.astype(np.float16),
                block_id=np.asarray(block_id, dtype=object),
                row=np.asarray(int(item["row"]), dtype=np.int32),
                col=np.asarray(int(item["col"]), dtype=np.int32),
                bbox=np.asarray(item["bbox_values"], dtype=np.float64),
            )
            write_json_atomic(
                block_json,
                {
                    "model": model,
                    "block_id": block_id,
                    "status": "ok",
                    "source": "run",
                    "row": int(item["row"]),
                    "col": int(item["col"]),
                    "bbox": item["bbox_values"],
                    "shape": list(grid.shape),
                    "elapsed_s": round(time.perf_counter() - block_t0, 3),
                    "output_npz": str(block_npz),
                    "meta": {k: str(v) for k, v in getattr(emb, "meta", {}).items()},
                },
            )
            grids.append(grid)
            block_records.append(
                {
                    "block_id": block_id,
                    "status": "ok",
                    "source": "run",
                    "shape": list(grid.shape),
                    "output_npz": str(block_npz),
                    "output_json": str(block_json),
                }
            )

        mean, comps = sample_pixels_for_pca(
            grids,
            max_sample_pixels=max_sample_pixels,
            seed=seed,
        )
        rgb_canvas = grids_to_rgb_canvas(block_specs, grids, mean=mean, comps=comps)
        save_npz_atomic(
            npz_path,
            rgb_canvas=rgb_canvas,
            pca_mean=mean,
            pca_components=comps,
            block_ids=np.asarray([item["block_id"] for item in block_specs], dtype=object),
            block_shapes=np.asarray([list(grid.shape) for grid in grids], dtype=object),
            coverage=np.asarray(block_coverage(block_specs), dtype=np.float64),
        )
        save_panel_png(rgb_canvas, title=model, out_path=png_path)
        result["shape"] = [len(block_specs), *list(grids[0].shape)]
        result["grid_hw"] = list(rgb_canvas.shape[:2])
        result["blocks"] = block_records
        result["elapsed_s"] = round(time.perf_counter() - t0, 3)
    except Exception as exc:  # noqa: BLE001
        result["status"] = "failed"
        result["reason"] = repr(exc)
        result["blocks"] = block_records

    write_json_atomic(json_path, result)
    return result


def load_existing_or_pending(model: str, out_dir: Path) -> dict[str, Any]:
    json_path = out_dir / f"{model}_2x.json"
    if json_path.exists():
        return json.loads(json_path.read_text())
    return {
        "model": model,
        "status": "pending",
        "reason": "Not rendered in this run yet.",
        "output_png": str(out_dir / f"{model}_2x.png"),
    }


def draw_summary_figure(
    *,
    original_rgb: np.ndarray,
    model_results: list[dict[str, Any]],
    out_path: Path,
) -> None:
    fig, axes = plt.subplots(4, 5, figsize=(18, 14), constrained_layout=True)
    axes_flat = list(axes.flat)

    axes_flat[0].imshow(original_rgb, interpolation="nearest")
    axes_flat[0].set_title("original RGB\nRegion A block_r01_c01 2x2", fontsize=11)
    axes_flat[0].axis("off")

    for ax, result in zip(axes_flat[1:], model_results, strict=True):
        status = result["status"]
        if status == "ok" and Path(result["output_png"]).exists():
            rgb = plt.imread(result["output_png"])
            ax.imshow(rgb, interpolation="nearest")
            ax.set_title(format_model_panel_title(result), fontsize=9)
            ax.axis("off")
            continue
        ax.axis("off")
        reason = result.get("reason") or status
        ax.text(0.03, 0.92, result["model"], fontsize=11, fontweight="bold", va="top")
        ax.text(0.03, 0.72, f"status: {status}", fontsize=10, va="top")
        ax.text(0.03, 0.55, str(reason)[:180], fontsize=9, va="top", wrap=True)

    fig.suptitle(
        "Original map + 19 model spatial embedding maps, 2x2 expansion of block_r01_c01\n"
        "Each model panel is PCA pseudocolor over dense grid embeddings for the same 2x2 range.",
        fontsize=15,
        y=1.06,
    )
    fig.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    block_specs = load_block_specs(args.data_dir)
    original_rgb = build_original_rgb_canvas(block_specs)
    original_path = args.out_dir / "original_region_a_block_r01_c01_2x.png"
    save_panel_png(original_rgb, "original RGB 2x", original_path)

    requested_models = [str(model) for model in args.models]
    model_results: list[dict[str, Any]] = []
    for idx, model in enumerate(requested_models, start=1):
        print(f"[{idx}/{len(requested_models)}] rendering {model} 2x", flush=True)
        result = run_model_map_2x(
            model=model,
            block_specs=block_specs,
            device=args.device,
            out_dir=args.out_dir,
            resume=args.resume,
            max_sample_pixels=args.max_sample_pixels,
            seed=args.seed,
        )
        print(f"[{idx}/{len(requested_models)}] {model} 2x -> {result['status']}", flush=True)
        model_results.append(result)

    all_model_results = [load_existing_or_pending(model, args.out_dir) for model in PUBLIC_MODELS]
    summary_path = args.out_dir / "part2_original_map_with_public19_models_2x.png"
    draw_summary_figure(original_rgb=original_rgb, model_results=all_model_results, out_path=summary_path)

    coverage = block_coverage(block_specs)
    ref = next(item for item in block_specs if int(item["row"]) == REFERENCE_ROW and int(item["col"]) == REFERENCE_COL)
    ref_bbox = np.asarray(ref["bbox_values"], dtype=float)
    manifest = {
        "reference_source_figure": str(args.out_dir / "part2_original_map_with_public19_models.png"),
        "reference_block": "region_a/block_r01_c01",
        "reference_block_bbox": ref["bbox_values"],
        "expanded_blocks": [str(item["block_id"]) for item in block_specs],
        "coverage": coverage,
        "width_ratio_vs_reference_block": float((coverage[2] - coverage[0]) / (ref_bbox[2] - ref_bbox[0])),
        "height_ratio_vs_reference_block": float((coverage[3] - coverage[1]) / (ref_bbox[3] - ref_bbox[1])),
        "area_ratio_vs_reference_block": float(
            ((coverage[2] - coverage[0]) * (coverage[3] - coverage[1]))
            / ((ref_bbox[2] - ref_bbox[0]) * (ref_bbox[3] - ref_bbox[1]))
        ),
        "original_rgb": str(original_path),
        "summary_figure": str(summary_path),
        "models": all_model_results,
        "notes": [
            "This is the intended 2x2 expansion of the original part2 figure's left-top block_r01_c01 panel.",
            "The geographic width and height are each 2x the reference block; the area is 4x.",
            "Models are rendered from dense grid outputs over the same four blocks.",
        ],
    }
    write_json_atomic(args.out_dir / "manifest_2x.json", manifest)


if __name__ == "__main__":
    main()
