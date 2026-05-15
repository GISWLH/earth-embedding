from __future__ import annotations

import argparse
import json
import math
import os
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
SLOW_MODELS = {"satmae", "satmaepp", "scalemae", "satvision"}
EMBED_DIMS = (64, 128, 256, 384, 512, 768, 1024, 1536, 4096)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a map-style figure for the part-2 original ROI and 19 models."
    )
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--models", nargs="+", default=PUBLIC_MODELS)
    parser.add_argument("--resume", action="store_true")
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


def pca_rgb(arr: Any) -> np.ndarray:
    dhw = to_dhw(arr)
    d, h, w = dhw.shape
    x = dhw.reshape(d, h * w).T
    x = np.nan_to_num(x, nan=0.0, posinf=0.0, neginf=0.0)
    x = x - x.mean(axis=0, keepdims=True)
    if x.shape[0] < 2:
        return np.zeros((h, w, 3), dtype=np.float32)
    _, _, vt = np.linalg.svd(x, full_matrices=False)
    comps = vt[:3].T
    y = x @ comps
    if y.shape[1] < 3:
        pad = np.zeros((y.shape[0], 3 - y.shape[1]), dtype=y.dtype)
        y = np.concatenate([y, pad], axis=1)
    rgb = np.stack([robust_scale01(y[:, i]) for i in range(3)], axis=-1)
    return rgb.reshape(h, w, 3)


def load_reference_block(data_dir: Path) -> tuple[np.ndarray, BBox, PointBuffer]:
    path = data_dir / "region_a" / "imagery_s2_20210501_20211031" / "block_r01_c01.npz"
    data = np.load(path, allow_pickle=True)
    arr = np.asarray(data["array"], dtype=np.float32)
    bands = [str(x) for x in data["bands"].tolist()]
    bbox = np.asarray(data["bbox"], dtype=float)
    band_index = {name: idx for idx, name in enumerate(bands)}
    rgb = np.stack(
        [
            robust_scale01(arr[band_index["B4"]]),
            robust_scale01(arr[band_index["B3"]]),
            robust_scale01(arr[band_index["B2"]]),
        ],
        axis=-1,
    )
    spatial_bbox = BBox(
        minlon=float(bbox[0]),
        minlat=float(bbox[1]),
        maxlon=float(bbox[2]),
        maxlat=float(bbox[3]),
    )
    center = PointBuffer(
        lon=float((bbox[0] + bbox[2]) / 2.0),
        lat=float((bbox[1] + bbox[3]) / 2.0),
        buffer_m=15_000.0,
    )
    return rgb, spatial_bbox, center


def temporal_for_model(model: str) -> TemporalSpec:
    if model in YEAR_MODELS:
        return TemporalSpec.year(YEAR_MODELS[model])
    return TemporalSpec.range("2021-05-01", "2021-10-31")


def spatial_for_model(model: str, bbox: BBox, coarse_center: PointBuffer) -> BBox | PointBuffer:
    if model in COARSE_BUFFER_MODELS:
        return PointBuffer(
            lon=coarse_center.lon,
            lat=coarse_center.lat,
            buffer_m=float(COARSE_BUFFER_MODELS[model]),
        )
    return bbox


def tessera_has_local_tiles(spatial: BBox | PointBuffer, year: int) -> bool:
    if isinstance(spatial, BBox):
        bounds = (spatial.minlon, spatial.minlat, spatial.maxlon, spatial.maxlat)
    else:
        m_per_deg_lat = 111_320.0
        dlat = spatial.buffer_m / m_per_deg_lat
        dlon = spatial.buffer_m / (m_per_deg_lat * max(1e-6, math.cos(math.radians(spatial.lat))))
        bounds = (spatial.lon - dlon, spatial.lat - dlat, spatial.lon + dlon, spatial.lat + dlat)
    registry = pd.read_parquet(
        REPO_ROOT / "research_outputs" / "model_cache" / "geotessera_cache" / "registry.parquet",
        columns=["lat", "lon", "year"],
    )
    hits = registry[
        (registry["year"] == int(year))
        & (registry["lon"] >= bounds[0])
        & (registry["lon"] <= bounds[2])
        & (registry["lat"] >= bounds[1])
        & (registry["lat"] <= bounds[3])
    ]
    return not hits.empty


def save_panel_png(rgb: np.ndarray, title: str, out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(3.2, 3.2))
    ax.imshow(rgb)
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


def run_model_map(
    *,
    model: str,
    bbox: BBox,
    coarse_center: PointBuffer,
    device: str,
    out_dir: Path,
    resume: bool,
) -> dict[str, Any]:
    json_path = out_dir / f"{model}.json"
    npz_path = out_dir / f"{model}.npz"
    png_path = out_dir / f"{model}.png"
    if resume and json_path.exists() and png_path.exists():
        return json.loads(json_path.read_text())

    temporal = temporal_for_model(model)
    spatial = spatial_for_model(model, bbox, coarse_center)
    set_local_asset_env(model)
    result: dict[str, Any] = {
        "model": model,
        "status": "ok",
        "reason": None,
        "output_json": str(json_path),
        "output_npz": str(npz_path),
        "output_png": str(png_path),
        "temporal": temporal.mode,
        "spatial_type": type(spatial).__name__,
    }

    if model == "tessera" and not tessera_has_local_tiles(spatial, YEAR_MODELS["tessera"]):
        result["reason"] = "No local tessera tiles were pre-cached for the Wuhan ROI."

    try:
        try:
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
                result["reason"] = "Retried on CPU after CUDA OOM."
            else:
                raise
        arr = np.asarray(getattr(emb.data, "values", emb.data), dtype=np.float32)
        rgb = pca_rgb(arr)
        np.savez_compressed(npz_path, embedding=arr)
        save_panel_png(rgb, title=model, out_path=png_path)
        result["shape"] = list(arr.shape)
        result["grid_hw"] = list(np.asarray(rgb).shape[:2])
        result["meta"] = {k: str(v) for k, v in getattr(emb, "meta", {}).items()}
    except Exception as exc:  # noqa: BLE001
        result["status"] = "failed"
        result["reason"] = repr(exc)

    json_path.write_text(json.dumps(result, indent=2))
    return result


def load_existing_or_pending(model: str, out_dir: Path) -> dict[str, Any]:
    json_path = out_dir / f"{model}.json"
    if json_path.exists():
        return json.loads(json_path.read_text())
    return {
        "model": model,
        "status": "pending",
        "reason": "Not rendered in this run yet.",
        "output_png": str(out_dir / f"{model}.png"),
    }


def draw_summary_figure(
    *,
    original_rgb: np.ndarray,
    model_results: list[dict[str, Any]],
    out_path: Path,
) -> None:
    fig, axes = plt.subplots(4, 5, figsize=(18, 14), constrained_layout=True)
    axes_flat = list(axes.flat)

    axes_flat[0].imshow(original_rgb)
    axes_flat[0].set_title("original RGB\nRegion A block_r01_c01", fontsize=11)
    axes_flat[0].axis("off")

    for ax, result in zip(axes_flat[1:], model_results, strict=True):
        status = result["status"]
        if status == "ok":
            rgb = plt.imread(result["output_png"])
            ax.imshow(rgb)
            ax.set_title(format_model_panel_title(result), fontsize=9)
        else:
            ax.axis("off")
            reason = result.get("reason") or status
            ax.text(
                0.03,
                0.92,
                result["model"],
                fontsize=11,
                fontweight="bold",
                va="top",
            )
            ax.text(0.03, 0.72, f"status: {status}", fontsize=10, va="top")
            ax.text(0.03, 0.55, reason[:180], fontsize=9, va="top", wrap=True)
            continue
        ax.axis("off")

    fig.suptitle(
        "Original map + 19 model spatial embedding maps\n"
        "Each model panel is a PCA pseudocolor rendering of its grid embedding.",
        fontsize=15,
        y=1.06,
    )
    fig.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    original_rgb, bbox, coarse_center = load_reference_block(args.data_dir)
    original_path = args.out_dir / "original_region_a_block_r01_c01.png"
    save_panel_png(original_rgb, "original RGB", original_path)

    requested_models = [str(model) for model in args.models]
    for idx, model in enumerate(requested_models, start=1):
        print(f"[{idx}/{len(requested_models)}] rendering {model}", flush=True)
        result = run_model_map(
            model=model,
            bbox=bbox,
            coarse_center=coarse_center,
            device=args.device,
            out_dir=args.out_dir,
            resume=args.resume,
        )
        print(f"[{idx}/{len(requested_models)}] {model} -> {result['status']}", flush=True)

    model_results = [load_existing_or_pending(model, args.out_dir) for model in PUBLIC_MODELS]

    summary_path = args.out_dir / "part2_original_map_with_public19_models.png"
    draw_summary_figure(
        original_rgb=original_rgb,
        model_results=model_results,
        out_path=summary_path,
    )

    manifest = {
        "reference_block": "region_a/block_r01_c01",
        "original_rgb": str(original_path),
        "summary_figure": str(summary_path),
        "models": model_results,
        "notes": [
            "Each model panel is the first three PCA components of the model grid embedding.",
            "gse is included as a precomputed product model.",
            "copernicus uses a larger buffer so that the ROI exceeds one 0.25 degree cell.",
            "tessera is marked unavailable when no local tiles exist for the Wuhan ROI.",
        ],
    }
    (args.out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
