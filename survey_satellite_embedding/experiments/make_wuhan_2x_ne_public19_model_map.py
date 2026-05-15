from __future__ import annotations

import argparse
import json
import math
import os
import re
import time
from pathlib import Path
from typing import Any

import pandas as pd

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from rs_embed import OutputSpec, TemporalSpec, get_embedding, get_embeddings_batch
from rs_embed.core.registry import get_embedder_cls
from rs_embed.core.specs import BBox, PointBuffer
from rs_embed.tools.model_defaults import default_sensor_for_model

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
DEFAULT_DATA_DIR = ROOT.parent / "data" / "part2_20260507_2x_ne"
DEFAULT_OUT_DIR = ROOT / "results" / "wuhan_east_lake_2x_ne_public19_model_map"
DEFAULT_ORIGINAL = (
    ROOT / "results" / "wuhan_east_lake_2x_ne_original_rgb" / "wuhan_east_lake_2x_ne_original_rgb.png"
)

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
CHUNK_SIZE_BY_MODEL = {
    "satmae": 1,
    "satmaepp": 1,
    "satmaepp_s2_10b": 1,
    "scalemae": 1,
    "satvision": 1,
    "terramind": 1,
    "terrafm": 1,
    "dofa": 1,
    "thor": 1,
    "agrifm": 1,
}
EMBED_DIMS = (64, 128, 256, 384, 512, 768, 1024, 1536, 2048, 4096)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render Wuhan East Lake 2x NE ROI original map plus 19 model pooled block maps."
    )
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--original-png", type=Path, default=DEFAULT_ORIGINAL)
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


def embedding_rgb(embeddings: np.ndarray) -> np.ndarray:
    x = np.asarray(embeddings, dtype=np.float32)
    if x.ndim != 2:
        raise ValueError(f"Expected a 2D pooled embedding matrix, got {x.shape}")
    valid_rows = np.isfinite(x).any(axis=1)
    if int(valid_rows.sum()) < 2:
        return np.tile(np.array([[0.42, 0.24, 0.66]], dtype=np.float32), (x.shape[0], 1))
    with np.errstate(invalid="ignore"):
        col_mean = np.nanmean(x[valid_rows], axis=0, keepdims=True)
    col_mean = np.nan_to_num(col_mean, nan=0.0, posinf=0.0, neginf=0.0)
    x = np.where(np.isfinite(x), x, col_mean)
    x = x - x[valid_rows].mean(axis=0, keepdims=True)
    x = np.nan_to_num(x, nan=0.0, posinf=0.0, neginf=0.0)
    _, _, vt = np.linalg.svd(x[valid_rows], full_matrices=False)
    comps = vt[: min(3, vt.shape[0])].T
    y = x @ comps
    if y.shape[1] < 3:
        y = np.concatenate([y, np.zeros((y.shape[0], 3 - y.shape[1]), dtype=y.dtype)], axis=1)
    return np.stack([robust_scale01(y[:, i]) for i in range(3)], axis=-1)


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
        y = np.concatenate([y, np.zeros((y.shape[0], 3 - y.shape[1]), dtype=y.dtype)], axis=1)
    rgb = np.stack([robust_scale01(y[:, i]) for i in range(3)], axis=-1)
    return rgb.reshape(h, w, 3)


def format_shape(shape: list[int] | tuple[int, ...] | np.ndarray) -> str:
    return "*".join(str(int(dim)) for dim in shape)


def temporal_for_model(model: str) -> TemporalSpec:
    if model in YEAR_MODELS:
        return TemporalSpec.year(YEAR_MODELS[model])
    return TemporalSpec.range("2021-05-01", "2021-10-31")


def spatial_for_precomputed(model: str, bbox: BBox) -> BBox | PointBuffer:
    if model == "copernicus":
        return PointBuffer(
            lon=float((bbox.minlon + bbox.maxlon) / 2.0),
            lat=float((bbox.minlat + bbox.maxlat) / 2.0),
            buffer_m=15000.0,
        )
    return bbox


def set_local_asset_env(model: str) -> None:
    if model == "satmaepp_s2_10b":
        os.environ["RS_EMBED_SATMAEPP_S2_CKPT_FILE"] = str(
            REPO_ROOT / "research_outputs" / "model_cache" / "checkpoint_ViT-L_pretrain_fmow_sentinel.pth"
        )
    elif model == "agrifm":
        os.environ["RS_EMBED_AGRIFM_CKPT"] = str(REPO_ROOT / "research_outputs" / "model_cache" / "AgriFM.pth")
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


def load_block_specs(data_dir: Path) -> list[dict[str, Any]]:
    imagery_dir_10b = data_dir / "region_a" / "imagery_s2_20210501_20211031"
    imagery_dir_12b = data_dir / "region_a" / "imagery_s2_12b_20210501_20211031"
    specs: list[dict[str, Any]] = []
    for path in sorted(imagery_dir_10b.glob("block_r*_c*.npz")):
        match = re.match(r"block_r(\d+)_c(\d+)\.npz", path.name)
        if match is None:
            continue
        row = int(match.group(1))
        col = int(match.group(2))
        data = np.load(path, allow_pickle=True)
        bbox = np.asarray(data["bbox"], dtype=float)
        bands = [str(x) for x in data["bands"].tolist()]
        item = {
            "block_id": path.stem,
            "row": row,
            "col": col,
            "bbox": BBox(
                minlon=float(bbox[0]),
                minlat=float(bbox[1]),
                maxlon=float(bbox[2]),
                maxlat=float(bbox[3]),
            ),
            "input_chw": np.asarray(data["array"], dtype=np.float32),
            "bands": bands,
        }
        path_12b = imagery_dir_12b / path.name
        if path_12b.exists():
            data_12b = np.load(path_12b, allow_pickle=True)
            item["input_chw_12b"] = np.asarray(data_12b["array"], dtype=np.float32)
            item["bands_12b"] = [str(x) for x in data_12b["bands"].tolist()]
        specs.append(item)
    if not specs:
        raise FileNotFoundError(f"No block NPZ files found under {imagery_dir_10b}")
    return specs


def chunked(seq: list[Any], size: int):
    for i in range(0, len(seq), size):
        yield seq[i : i + size]


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(payload, indent=2))
    os.replace(tmp_path, path)


def save_npz_atomic(path: Path, **arrays: Any) -> None:
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("wb") as f:
        np.savez_compressed(f, **arrays)
    os.replace(tmp_path, path)


def pooled_numpy(x: Any) -> np.ndarray:
    if hasattr(x, "values"):
        return np.asarray(x.values)
    return np.asarray(x)


def adapt_input_chw(model: str, block_spec: dict[str, Any]) -> np.ndarray:
    input_chw = np.asarray(block_spec["input_chw"], dtype=np.float32)
    bands = list(block_spec["bands"])
    band_to_idx = {name: i for i, name in enumerate(bands)}

    if model in {"remoteclip", "satmae", "satmaepp", "scalemae", "wildsat"}:
        order = ["B4", "B3", "B2"]
        return np.stack([input_chw[band_to_idx[b]] for b in order], axis=0).astype(np.float32)
    if model in {"satmaepp_s2_10b", "anysat", "galileo", "thor", "agrifm"}:
        order = ["B2", "B3", "B4", "B5", "B6", "B7", "B8", "B8A", "B11", "B12"]
        return np.stack([input_chw[band_to_idx[b]] for b in order], axis=0).astype(np.float32)
    if model == "dofa":
        order = ["B4", "B3", "B2", "B5", "B6", "B7", "B8", "B11", "B12"]
        return np.stack([input_chw[band_to_idx[b]] for b in order], axis=0).astype(np.float32)
    if model == "prithvi":
        mapping = {
            "BLUE": "B2",
            "GREEN": "B3",
            "RED": "B4",
            "NIR_NARROW": "B8A",
            "SWIR_1": "B11",
            "SWIR_2": "B12",
        }
        return np.stack(
            [input_chw[band_to_idx[mapping[b]]] for b in ["BLUE", "GREEN", "RED", "NIR_NARROW", "SWIR_1", "SWIR_2"]],
            axis=0,
        ).astype(np.float32)
    if model in {"terrafm", "terramind", "fomo"}:
        input_chw_12b = block_spec.get("input_chw_12b")
        bands_12b = block_spec.get("bands_12b")
        if input_chw_12b is None or bands_12b is None:
            raise RuntimeError(f"{model} requires the 12-band Sentinel-2 block product, but it is not available yet")
        input_chw_12b = np.asarray(input_chw_12b, dtype=np.float32)
        band_to_idx_12b = {name: i for i, name in enumerate(list(bands_12b))}
        order = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B8A", "B9", "B11", "B12"]
        return np.stack([input_chw_12b[band_to_idx_12b[b]] for b in order], axis=0).astype(np.float32)
    if model == "satvision":
        raise RuntimeError("satvision uses provider-fetched MODIS TOA inputs in this workflow")
    return input_chw.astype(np.float32)


def build_block_rgb_map(block_specs: list[dict[str, Any]], embeddings: np.ndarray) -> np.ndarray:
    rows = sorted({int(item["row"]) for item in block_specs})
    cols = sorted({int(item["col"]) for item in block_specs})
    row_to_idx = {row: i for i, row in enumerate(rows)}
    col_to_idx = {col: i for i, col in enumerate(cols)}
    rgb = embedding_rgb(embeddings)
    canvas = np.zeros((len(rows), len(cols), 3), dtype=np.float32)
    for item, color in zip(block_specs, rgb, strict=True):
        canvas[row_to_idx[int(item["row"])] , col_to_idx[int(item["col"])] ] = color
    return canvas


def build_block_rgb_canvas(block_specs: list[dict[str, Any]], rgb_map: np.ndarray) -> np.ndarray:
    rows = sorted({int(item["row"]) for item in block_specs})
    cols = sorted({int(item["col"]) for item in block_specs})
    heights = {
        row: max(int(np.asarray(item["input_chw"]).shape[-2]) for item in block_specs if int(item["row"]) == row)
        for row in rows
    }
    widths = {
        col: max(int(np.asarray(item["input_chw"]).shape[-1]) for item in block_specs if int(item["col"]) == col)
        for col in cols
    }
    row_offsets: dict[int, int] = {}
    col_offsets: dict[int, int] = {}
    y = 0
    for row in sorted(rows, reverse=True):
        row_offsets[row] = y
        y += heights[row]
    x = 0
    for col in cols:
        col_offsets[col] = x
        x += widths[col]

    row_to_idx = {row: i for i, row in enumerate(rows)}
    col_to_idx = {col: i for i, col in enumerate(cols)}
    canvas = np.zeros((sum(heights.values()), sum(widths.values()), 3), dtype=np.float32)
    for item in block_specs:
        row = int(item["row"])
        col = int(item["col"])
        y0 = row_offsets[row]
        x0 = col_offsets[col]
        h = heights[row]
        w = widths[col]
        canvas[y0 : y0 + h, x0 : x0 + w, :] = rgb_map[row_to_idx[row], col_to_idx[col], :]
    return canvas


def build_block_grid_rgb_mosaic(block_specs: list[dict[str, Any]], block_rgbs: list[np.ndarray]) -> np.ndarray:
    rows = sorted({int(item["row"]) for item in block_specs})
    cols = sorted({int(item["col"]) for item in block_specs})
    row_to_idx = {row: i for i, row in enumerate(rows)}
    col_to_idx = {col: i for i, col in enumerate(cols)}
    heights = {row: 0 for row in rows}
    widths = {col: 0 for col in cols}
    for item, rgb in zip(block_specs, block_rgbs, strict=True):
        heights[int(item["row"])] = max(heights[int(item["row"])] , int(rgb.shape[0]))
        widths[int(item["col"])] = max(widths[int(item["col"])] , int(rgb.shape[1]))
    row_offsets = {}
    col_offsets = {}
    y = 0
    for row in sorted(rows, reverse=True):
        row_offsets[row] = y
        y += heights[row]
    x = 0
    for col in cols:
        col_offsets[col] = x
        x += widths[col]
    canvas = np.zeros((sum(heights.values()), sum(widths.values()), 3), dtype=np.float32)
    for item, rgb in zip(block_specs, block_rgbs, strict=True):
        row = int(item["row"])
        col = int(item["col"])
        y0 = row_offsets[row]
        x0 = col_offsets[col]
        canvas[y0 : y0 + rgb.shape[0], x0 : x0 + rgb.shape[1], :] = rgb
    return canvas


def save_panel_png(rgb_map: np.ndarray, title: str, out_path: Path, *, upscale_blocks: bool = True) -> None:
    vis = np.kron(rgb_map, np.ones((64, 64, 1), dtype=np.float32)) if upscale_blocks else rgb_map
    h, w = vis.shape[:2]
    aspect = max(w / max(h, 1), 1e-6)
    fig_w = 3.4
    fig_h = max(2.0, fig_w / aspect)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.imshow(vis, interpolation="nearest")
    ax.set_title(title, fontsize=10)
    ax.axis("off")
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def run_gse_block_grid_mosaic(
    *,
    block_specs: list[dict[str, Any]],
    device: str,
) -> tuple[np.ndarray, list[int]]:
    block_rgbs: list[np.ndarray] = []
    last_shape: list[int] = []
    for item in block_specs:
        emb = get_embedding(
            'gse',
            spatial=item['bbox'],
            temporal=temporal_for_model('gse'),
            output=OutputSpec.grid(),
            backend='auto',
            device=device,
        )
        arr = np.asarray(getattr(emb.data, 'values', emb.data), dtype=np.float32)
        block_rgbs.append(pca_rgb(arr))
        last_shape = list(arr.shape)
    return build_block_grid_rgb_mosaic(block_specs, block_rgbs), last_shape


def load_gse_block_checkpoint(npz_path: Path) -> np.ndarray | None:
    if not npz_path.exists():
        return None
    try:
        with np.load(npz_path, allow_pickle=True) as data:
            embedding = np.asarray(data["embedding"], dtype=np.float32).reshape(-1)
    except Exception:
        return None
    return embedding if embedding.shape == (64,) else None


def run_gse_pooled_by_block(
    *,
    block_specs: list[dict[str, Any]],
    out_dir: Path,
    device: str,
) -> tuple[np.ndarray, dict[str, Any]]:
    block_dir = out_dir / "gse_blocks"
    block_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = block_dir / "manifest.json"
    matrix = np.full((len(block_specs), 64), np.nan, dtype=np.float32)
    block_records: list[dict[str, Any]] = []
    n_ok = 0
    n_failed = 0
    t0 = time.perf_counter()

    def _write_progress_manifest() -> None:
        write_json_atomic(
            manifest_path,
            {
                "block_dir": str(block_dir),
                "n_blocks": len(block_specs),
                "n_ok": int(n_ok),
                "n_failed": int(n_failed),
                "n_done": int(n_ok + n_failed),
                "elapsed_s": round(time.perf_counter() - t0, 3),
                "complete": bool((n_ok + n_failed) == len(block_specs)),
                "blocks": block_records,
            },
        )

    for idx, item in enumerate(block_specs, start=1):
        block_id = str(item["block_id"])
        npz_path = block_dir / f"{block_id}.npz"
        json_path = block_dir / f"{block_id}.json"
        cached = load_gse_block_checkpoint(npz_path)
        if cached is not None:
            matrix[idx - 1] = cached
            n_ok += 1
            block_records.append(
                {
                    "block_id": block_id,
                    "status": "ok",
                    "source": "checkpoint",
                    "output_npz": str(npz_path),
                    "output_json": str(json_path),
                }
            )
            _write_progress_manifest()
            print(f"[gse {idx}/{len(block_specs)}] reuse {block_id}", flush=True)
            continue

        print(f"[gse {idx}/{len(block_specs)}] download {block_id}", flush=True)
        block_t0 = time.perf_counter()
        bbox = item["bbox"]
        try:
            emb = get_embedding(
                "gse",
                spatial=bbox,
                temporal=temporal_for_model("gse"),
                output=OutputSpec.pooled(),
                backend="auto",
                device=device,
            )
            vector = pooled_numpy(emb.data).astype(np.float32).reshape(-1)
            if vector.shape != (64,):
                raise RuntimeError(f"Expected GSE pooled vector shape=(64,), got {vector.shape}")
            matrix[idx - 1] = vector
            elapsed = round(time.perf_counter() - block_t0, 3)
            bbox_values = [float(bbox.minlon), float(bbox.minlat), float(bbox.maxlon), float(bbox.maxlat)]
            meta = dict(emb.meta or {})
            save_npz_atomic(
                npz_path,
                embedding=vector,
                block_id=np.asarray(block_id, dtype=object),
                row=np.asarray(int(item["row"]), dtype=np.int32),
                col=np.asarray(int(item["col"]), dtype=np.int32),
                bbox=np.asarray(bbox_values, dtype=np.float64),
                valid_pixel_fraction=np.asarray(
                    float(meta.get("valid_pixel_fraction", np.nan)), dtype=np.float32
                ),
            )
            write_json_atomic(
                json_path,
                {
                    "block_id": block_id,
                    "status": "ok",
                    "source": "download",
                    "model": "gse",
                    "row": int(item["row"]),
                    "col": int(item["col"]),
                    "bbox": bbox_values,
                    "shape": list(vector.shape),
                    "finite_dims": int(np.isfinite(vector).sum()),
                    "valid_pixel_fraction": meta.get("valid_pixel_fraction"),
                    "elapsed_s": elapsed,
                    "output_npz": str(npz_path),
                },
            )
            n_ok += 1
            block_records.append(
                {
                    "block_id": block_id,
                    "status": "ok",
                    "source": "download",
                    "elapsed_s": elapsed,
                    "output_npz": str(npz_path),
                    "output_json": str(json_path),
                }
            )
            _write_progress_manifest()
            print(f"[gse {idx}/{len(block_specs)}] wrote {npz_path}", flush=True)
        except Exception as exc:  # noqa: BLE001
            n_failed += 1
            elapsed = round(time.perf_counter() - block_t0, 3)
            fail_payload = {
                "block_id": block_id,
                "status": "failed",
                "model": "gse",
                "row": int(item["row"]),
                "col": int(item["col"]),
                "reason": repr(exc),
                "elapsed_s": elapsed,
            }
            write_json_atomic(json_path, fail_payload)
            block_records.append(
                {
                    "block_id": block_id,
                    "status": "failed",
                    "reason": repr(exc),
                    "elapsed_s": elapsed,
                    "output_json": str(json_path),
                }
            )
            _write_progress_manifest()
            print(f"[gse {idx}/{len(block_specs)}] failed {block_id}: {exc!r}", flush=True)

    summary = {
        "block_dir": str(block_dir),
        "n_blocks": len(block_specs),
        "n_ok": int(n_ok),
        "n_failed": int(n_failed),
        "n_done": int(n_ok + n_failed),
        "elapsed_s": round(time.perf_counter() - t0, 3),
        "complete": True,
        "blocks": block_records,
    }
    write_json_atomic(manifest_path, summary)
    return matrix, summary


def run_tessera_from_local_cache(block_specs: list[dict[str, Any]]) -> np.ndarray:
    registry_path = REPO_ROOT / "research_outputs" / "model_cache" / "geotessera_cache" / "registry.parquet"
    repr_root = REPO_ROOT / "global_0.1_degree_representation"
    registry = pd.read_parquet(registry_path, columns=["lat", "lon", "year"])
    vectors: list[np.ndarray] = []
    for item in block_specs:
        bbox = item["bbox"]
        bounds = (bbox.minlon, bbox.minlat, bbox.maxlon, bbox.maxlat)
        tiles = registry[
            (registry["year"] == 2024)
            & (registry["lon"] >= bounds[0])
            & (registry["lon"] <= bounds[2])
            & (registry["lat"] >= bounds[1])
            & (registry["lat"] <= bounds[3])
        ][["lon", "lat"]].drop_duplicates()
        if tiles.empty:
            center_lon_raw = (bbox.minlon + bbox.maxlon) / 2.0
            center_lat_raw = (bbox.minlat + bbox.maxlat) / 2.0
            center_lon = math.floor(center_lon_raw * 10.0) / 10.0 + 0.05
            center_lat = math.floor(center_lat_raw * 10.0) / 10.0 + 0.05
            tiles = registry[
                (registry["year"] == 2024)
                & np.isclose(registry["lon"], center_lon, atol=1e-6)
                & np.isclose(registry["lat"], center_lat, atol=1e-6)
            ][["lon", "lat"]].drop_duplicates()
        tile_vectors: list[np.ndarray] = []
        for tile in tiles.itertuples(index=False):
            grid_name = f"grid_{float(tile.lon):.2f}_{float(tile.lat):.2f}"
            emb_path = repr_root / "2024" / grid_name / f"{grid_name}.npy"
            scale_path = repr_root / "2024" / grid_name / f"{grid_name}_scales.npy"
            if not emb_path.exists() or not scale_path.exists():
                continue
            quantized = np.load(emb_path, mmap_mode="r")
            scales = np.load(scale_path, mmap_mode="r")
            if scales.ndim == 2 and quantized.ndim == 3:
                scales = scales[..., np.newaxis]
            hwc = quantized.astype(np.float32) * scales
            tile_vectors.append(hwc.mean(axis=(0, 1)).astype(np.float32))
        if not tile_vectors:
            raise RuntimeError(f"tessera local cache has no usable tile arrays for bounds={bounds}")
        vectors.append(np.stack(tile_vectors, axis=0).mean(axis=0).astype(np.float32))
    return np.stack(vectors, axis=0)


def run_model_from_local_inputs(
    *,
    model: str,
    block_specs: list[dict[str, Any]],
    device: str,
) -> np.ndarray:
    embedder = get_embedder_cls(model)()
    sensor = default_sensor_for_model(model)
    if sensor is None:
        raise RuntimeError(f"{model} has no default sensor for local input inference")
    temporal = temporal_for_model(model)
    spatials = [item["bbox"] for item in block_specs]
    input_chws = [adapt_input_chw(model, item) for item in block_specs]
    batch_fn = getattr(embedder, "get_embeddings_batch_from_inputs", None)
    if not callable(batch_fn):
        raise RuntimeError(f"{model} does not expose get_embeddings_batch_from_inputs")
    outputs = batch_fn(
        spatials=spatials,
        input_chws=input_chws,
        temporal=temporal,
        sensor=sensor,
        output=OutputSpec.pooled(),
        backend="auto",
        device=device,
    )
    return np.stack([pooled_numpy(emb.data).astype(np.float32).reshape(-1) for emb in outputs], axis=0)


def run_model(
    *,
    model: str,
    block_specs: list[dict[str, Any]],
    device: str,
    out_dir: Path,
    resume: bool,
) -> dict[str, Any]:
    json_path = out_dir / f"{model}.json"
    npz_path = out_dir / f"{model}.npz"
    png_path = out_dir / f"{model}.png"
    if resume and json_path.exists() and png_path.exists() and npz_path.exists():
        return json.loads(json_path.read_text())

    set_local_asset_env(model)
    temporal = temporal_for_model(model)
    spatials = [item["bbox"] for item in block_specs]
    chunk_size = CHUNK_SIZE_BY_MODEL.get(model, 4)
    result: dict[str, Any] = {
        "model": model,
        "status": "ok",
        "reason": None,
        "output_json": str(json_path),
        "output_npz": str(npz_path),
        "output_png": str(png_path),
        "n_blocks": len(block_specs),
        "chunk_size": chunk_size,
        "temporal": temporal.mode,
    }
    vectors: list[np.ndarray] = []
    t0 = time.perf_counter()

    try:
        if model == "gse":
            matrix, gse_summary = run_gse_pooled_by_block(
                block_specs=block_specs,
                out_dir=out_dir,
                device=device,
            )
            result["block_checkpoint_dir"] = gse_summary["block_dir"]
            result["block_checkpoint_n_ok"] = gse_summary["n_ok"]
            result["block_checkpoint_n_failed"] = gse_summary["n_failed"]
            if int(gse_summary["n_failed"]) > 0:
                result["status"] = "partial" if int(gse_summary["n_ok"]) > 0 else "failed"
                result["reason"] = f"{gse_summary['n_failed']} GSE block downloads failed"
        elif model == "tessera":
            matrix = run_tessera_from_local_cache(block_specs)
        elif model in {"copernicus", "satvision"}:
            provider_spatials = [
                spatial_for_precomputed(model, item["bbox"]) if model in {"gse", "copernicus"} else item["bbox"]
                for item in block_specs
            ]
            for spatial_chunk in chunked(provider_spatials, chunk_size):
                try:
                    batch = get_embeddings_batch(
                        model,
                        spatials=spatial_chunk,
                        temporal=temporal,
                        output=OutputSpec.pooled(),
                        backend="auto",
                        device=device,
                    )
                    vectors.extend(pooled_numpy(emb.data).astype(np.float32).reshape(-1) for emb in batch)
                except Exception as exc:
                    result["status"] = "partial"
                    result["reason"] = f"batch fallback: {exc!r}"
                    for spatial in spatial_chunk:
                        emb = get_embedding(
                            model,
                            spatial=spatial,
                            temporal=temporal,
                            output=OutputSpec.pooled(),
                            backend="auto",
                            device=device,
                        )
                        vectors.append(pooled_numpy(emb.data).astype(np.float32).reshape(-1))
            matrix = np.stack(vectors, axis=0)
        else:
            matrix = run_model_from_local_inputs(
                model=model,
                block_specs=block_specs,
                device=device,
            )

        rgb_map = build_block_rgb_map(block_specs, matrix)
        rgb_canvas = build_block_rgb_canvas(block_specs, rgb_map)
        save_npz_atomic(
            npz_path,
            block_ids=np.asarray([item["block_id"] for item in block_specs], dtype=object),
            embeddings=matrix,
            rgb_map=rgb_map,
            rgb_canvas=rgb_canvas,
        )
        save_panel_png(rgb_canvas, model, png_path, upscale_blocks=False)
        result["shape"] = list(matrix.shape)
        result["grid_hw"] = list(rgb_map.shape[:2])
        result["elapsed_s"] = round(time.perf_counter() - t0, 3)
    except Exception as exc:  # noqa: BLE001
        result["status"] = "failed"
        result["reason"] = repr(exc)

    json_path.write_text(json.dumps(result, indent=2))
    return result


def load_existing_or_pending(model: str, out_dir: Path) -> dict[str, Any]:
    path = out_dir / f"{model}.json"
    if path.exists():
        return json.loads(path.read_text())
    return {
        "model": model,
        "status": "pending",
        "reason": "Not rendered in this run yet.",
        "output_png": str(out_dir / f"{model}.png"),
    }


def draw_summary_figure(original_png: Path, model_results: list[dict[str, Any]], out_path: Path) -> None:
    fig, axes = plt.subplots(4, 5, figsize=(18, 14), constrained_layout=True)
    axes_flat = list(axes.flat)

    axes_flat[0].imshow(plt.imread(original_png))
    axes_flat[0].set_title("original RGB\nWuhan East Lake 2x NE ROI", fontsize=11)
    axes_flat[0].axis("off")

    for ax, result in zip(axes_flat[1:], model_results, strict=True):
        if result["status"] in {"ok", "partial"} and Path(result["output_png"]).exists():
            ax.imshow(plt.imread(result["output_png"]))
            shape = result.get("shape")
            title = result["model"] if not shape else f"{result['model']} [{format_shape(shape)}]"
            ax.set_title(title, fontsize=9)
            ax.axis("off")
            continue
        ax.axis("off")
        reason = str(result.get("reason") or result["status"])
        ax.text(0.03, 0.92, result["model"], fontsize=11, fontweight="bold", va="top")
        ax.text(0.03, 0.72, f"status: {result['status']}", fontsize=10, va="top")
        ax.text(0.03, 0.55, reason[:180], fontsize=9, va="top", wrap=True)

    fig.suptitle(
        "Original map + 19 model block embedding maps\n"
        "Each model panel is PCA pseudocolor over pooled embeddings for the 8x8 downloaded blocks.",
        fontsize=15,
        y=1.03,
    )
    fig.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    block_specs = load_block_specs(args.data_dir)

    requested_models = [str(model) for model in args.models]
    for idx, model in enumerate(requested_models, start=1):
        print(f"[{idx}/{len(requested_models)}] rendering {model}", flush=True)
        result = run_model(
            model=model,
            block_specs=block_specs,
            device=args.device,
            out_dir=args.out_dir,
            resume=args.resume,
        )
        print(f"[{idx}/{len(requested_models)}] {model} -> {result['status']}", flush=True)

    model_results = [load_existing_or_pending(model, args.out_dir) for model in PUBLIC_MODELS]
    summary_path = args.out_dir / "wuhan_east_lake_2x_ne_original_with_public19_models.png"
    draw_summary_figure(args.original_png, model_results, summary_path)

    manifest = {
        "data_dir": str(args.data_dir),
        "original_png": str(args.original_png),
        "summary_figure": str(summary_path),
        "grid_definition": "8x8 downloaded Sentinel-2 blocks for the 2x NE ROI",
        "models": model_results,
        "notes": [
            "Each model panel is built from pooled embeddings over all downloaded region-A blocks.",
            "Block colors are the first three PCA components of the 64 pooled block embeddings.",
            "Panels are intended as acceptance visuals aligned with the earlier public19 template.",
        ],
    }
    (args.out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
