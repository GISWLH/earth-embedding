from __future__ import annotations

import argparse
import json
import os
import re
import time
from pathlib import Path
from typing import Any

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from rs_embed import OutputSpec, TemporalSpec, get_embedding
from rs_embed.core.specs import BBox

ROOT = Path(__file__).resolve().parent
DEFAULT_DATA_DIR = ROOT.parent / "data" / "part2_20260507_2x_ne"
DEFAULT_OUT_DIR = ROOT / "results" / "wuhan_east_lake_2x_ne_public19_model_map"
EMBED_DIMS = (64, 128, 256, 384, 512, 768, 1024, 1536, 2048, 4096)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download and render dense 10 m GSE grids for the Wuhan East Lake 2x NE ROI."
    )
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--max-sample-pixels", type=int, default=200_000)
    parser.add_argument("--seed", type=int, default=7)
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
    for path in sorted(imagery_dir.glob("block_r*_c*.npz")):
        match = re.match(r"block_r(\d+)_c(\d+)\.npz", path.name)
        if match is None:
            continue
        row = int(match.group(1))
        col = int(match.group(2))
        with np.load(path, allow_pickle=True) as data:
            bbox = np.asarray(data["bbox"], dtype=float)
            input_shape = list(np.asarray(data["array"]).shape)
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
                "input_shape": input_shape,
            }
        )
    if not specs:
        raise FileNotFoundError(f"No block NPZ files found under {imagery_dir}")
    return specs


def load_dense_checkpoint(path: Path) -> np.ndarray | None:
    if not path.exists() or path.stat().st_size <= 0:
        return None
    try:
        with np.load(path, allow_pickle=True) as data:
            grid = np.asarray(data["embedding"], dtype=np.float32)
    except Exception:
        return None
    if grid.ndim != 3 or grid.shape[0] != 64 or not np.isfinite(grid).any():
        return None
    return grid


def download_dense_blocks(
    *,
    block_specs: list[dict[str, Any]],
    dense_dir: Path,
    device: str,
) -> dict[str, Any]:
    dense_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = dense_dir / "manifest.json"
    records: list[dict[str, Any]] = []
    n_ok = 0
    n_failed = 0
    t0 = time.perf_counter()

    def write_manifest(complete: bool = False) -> None:
        write_json_atomic(
            manifest_path,
            {
                "dense_dir": str(dense_dir),
                "model": "gse",
                "output": "grid",
                "temporal": {"mode": "year", "year": 2021},
                "n_blocks": len(block_specs),
                "n_ok": int(n_ok),
                "n_failed": int(n_failed),
                "n_done": int(n_ok + n_failed),
                "complete": bool(complete),
                "elapsed_s": round(time.perf_counter() - t0, 3),
                "blocks": records,
            },
        )

    for idx, item in enumerate(block_specs, start=1):
        block_id = str(item["block_id"])
        npz_path = dense_dir / f"{block_id}.npz"
        json_path = dense_dir / f"{block_id}.json"
        cached = load_dense_checkpoint(npz_path)
        if cached is not None:
            n_ok += 1
            records.append(
                {
                    "block_id": block_id,
                    "status": "ok",
                    "source": "checkpoint",
                    "shape": list(cached.shape),
                    "output_npz": str(npz_path),
                    "output_json": str(json_path),
                }
            )
            write_manifest()
            print(f"[gse-dense {idx}/{len(block_specs)}] reuse {block_id}", flush=True)
            continue

        print(f"[gse-dense {idx}/{len(block_specs)}] download {block_id}", flush=True)
        block_t0 = time.perf_counter()
        bbox = item["bbox"]
        try:
            emb = get_embedding(
                "gse",
                spatial=bbox,
                temporal=TemporalSpec.year(2021),
                output=OutputSpec.grid(),
                backend="auto",
                device=device,
            )
            grid = to_dhw(emb.data)
            if grid.shape[0] != 64:
                raise RuntimeError(f"Expected dense GSE grid with 64 channels, got {grid.shape}")
            finite_pixels = np.isfinite(grid).any(axis=0)
            if int(finite_pixels.sum()) == 0:
                raise RuntimeError(f"Dense GSE grid has no finite pixels for {block_id}")
            meta = dict(emb.meta or {})
            elapsed = round(time.perf_counter() - block_t0, 3)
            save_npz_atomic(
                npz_path,
                embedding=grid.astype(np.float16),
                block_id=np.asarray(block_id, dtype=object),
                row=np.asarray(int(item["row"]), dtype=np.int32),
                col=np.asarray(int(item["col"]), dtype=np.int32),
                bbox=np.asarray(item["bbox_values"], dtype=np.float64),
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
                    "output": "grid",
                    "row": int(item["row"]),
                    "col": int(item["col"]),
                    "bbox": item["bbox_values"],
                    "shape": list(grid.shape),
                    "finite_pixels": int(finite_pixels.sum()),
                    "valid_pixel_fraction": meta.get("valid_pixel_fraction"),
                    "elapsed_s": elapsed,
                    "output_npz": str(npz_path),
                },
            )
            n_ok += 1
            records.append(
                {
                    "block_id": block_id,
                    "status": "ok",
                    "source": "download",
                    "shape": list(grid.shape),
                    "elapsed_s": elapsed,
                    "output_npz": str(npz_path),
                    "output_json": str(json_path),
                }
            )
            write_manifest()
            print(f"[gse-dense {idx}/{len(block_specs)}] wrote {npz_path}", flush=True)
        except Exception as exc:  # noqa: BLE001
            n_failed += 1
            elapsed = round(time.perf_counter() - block_t0, 3)
            records.append(
                {
                    "block_id": block_id,
                    "status": "failed",
                    "reason": repr(exc),
                    "elapsed_s": elapsed,
                    "output_json": str(json_path),
                }
            )
            write_json_atomic(
                json_path,
                {
                    "block_id": block_id,
                    "status": "failed",
                    "model": "gse",
                    "output": "grid",
                    "row": int(item["row"]),
                    "col": int(item["col"]),
                    "bbox": item["bbox_values"],
                    "reason": repr(exc),
                    "elapsed_s": elapsed,
                },
            )
            write_manifest()
            print(f"[gse-dense {idx}/{len(block_specs)}] failed {block_id}: {exc!r}", flush=True)

    write_manifest(complete=(n_ok + n_failed) == len(block_specs))
    return json.loads(manifest_path.read_text())


def sample_pixels_for_pca(
    *,
    block_specs: list[dict[str, Any]],
    dense_dir: Path,
    max_sample_pixels: int,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    per_block = max(512, int(np.ceil(max_sample_pixels / max(len(block_specs), 1))))
    samples: list[np.ndarray] = []
    for item in block_specs:
        grid = load_dense_checkpoint(dense_dir / f"{item['block_id']}.npz")
        if grid is None:
            continue
        d, h, w = grid.shape
        x = grid.reshape(d, h * w).T
        valid = np.isfinite(x).all(axis=1)
        valid_idx = np.flatnonzero(valid)
        if valid_idx.size == 0:
            continue
        take = min(per_block, valid_idx.size)
        chosen = rng.choice(valid_idx, size=take, replace=False)
        samples.append(x[chosen].astype(np.float32))
    if not samples:
        raise RuntimeError("No dense GSE pixels available for PCA sampling.")
    sample = np.concatenate(samples, axis=0)
    if sample.shape[0] > max_sample_pixels:
        chosen = rng.choice(sample.shape[0], size=max_sample_pixels, replace=False)
        sample = sample[chosen]
    mean = np.nanmean(sample, axis=0, keepdims=True).astype(np.float32)
    centered = np.nan_to_num(sample - mean, nan=0.0, posinf=0.0, neginf=0.0)
    _, _, vt = np.linalg.svd(centered, full_matrices=False)
    comps = vt[:3].astype(np.float32)
    return mean.reshape(-1), comps


def build_dense_rgb_canvas(
    *,
    block_specs: list[dict[str, Any]],
    dense_dir: Path,
    mean: np.ndarray,
    comps: np.ndarray,
) -> np.ndarray:
    rows = sorted({int(item["row"]) for item in block_specs})
    cols = sorted({int(item["col"]) for item in block_specs})
    row_heights: dict[int, int] = {}
    col_widths: dict[int, int] = {}
    for item in block_specs:
        grid = load_dense_checkpoint(dense_dir / f"{item['block_id']}.npz")
        if grid is None:
            continue
        row_heights[int(item["row"])] = max(row_heights.get(int(item["row"]), 0), int(grid.shape[1]))
        col_widths[int(item["col"])] = max(col_widths.get(int(item["col"]), 0), int(grid.shape[2]))

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
    for item in block_specs:
        grid = load_dense_checkpoint(dense_dir / f"{item['block_id']}.npz")
        if grid is None:
            continue
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

    rgb = np.stack([robust_scale01(score_canvas[..., i]) for i in range(3)], axis=-1)
    return rgb.astype(np.float32)


def save_extent_figure(
    *,
    original_canvas_path: Path,
    gse_rgb: np.ndarray,
    coverage: list[float],
    out_path: Path,
) -> None:
    with np.load(original_canvas_path) as z:
        original = np.asarray(z["rgb"], dtype=np.float32)
    extent = [coverage[0], coverage[2], coverage[1], coverage[3]]
    fig, axes = plt.subplots(1, 2, figsize=(15.5, 6.1), constrained_layout=True)
    for ax, img, title in [
        (axes[0], original, "Original RGB\nWuhan East Lake 2x NE"),
        (axes[1], gse_rgb, "GSE dense 10 m grid PCA\nSame 2x NE extent"),
    ]:
        ax.imshow(img, extent=extent, origin="upper", interpolation="nearest")
        ax.set_title(title, fontsize=13)
        ax.set_xlabel("longitude")
        ax.set_ylabel("latitude")
        ax.set_xlim(coverage[0], coverage[2])
        ax.set_ylim(coverage[1], coverage[3])
        for c in range(1, 8):
            x = coverage[0] + (coverage[2] - coverage[0]) * c / 8.0
            ax.axvline(x, color="white", linewidth=0.35, alpha=0.65)
        for r in range(1, 8):
            y = coverage[1] + (coverage[3] - coverage[1]) * r / 8.0
            ax.axhline(y, color="white", linewidth=0.35, alpha=0.65)
        ax.text(
            coverage[0] + 0.006,
            coverage[3] - 0.012,
            f"extent [{coverage[0]:.2f}, {coverage[1]:.2f}, {coverage[2]:.2f}, {coverage[3]:.2f}]",
            color="white",
            fontsize=8.5,
            va="top",
            bbox={"facecolor": "#111111", "alpha": 0.72, "edgecolor": "none", "pad": 3},
        )
    fig.suptitle("Dense GSE Check: 10 m Grid Rendered at the Same 2x NE Range as Original RGB", fontsize=15)
    fig.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    dense_dir = args.out_dir / "gse_dense_blocks"
    block_specs = load_block_specs(args.data_dir)

    summary = download_dense_blocks(block_specs=block_specs, dense_dir=dense_dir, device=args.device)
    if int(summary["n_failed"]) > 0:
        raise RuntimeError(f"{summary['n_failed']} dense GSE blocks failed; see {dense_dir / 'manifest.json'}")

    mean, comps = sample_pixels_for_pca(
        block_specs=block_specs,
        dense_dir=dense_dir,
        max_sample_pixels=args.max_sample_pixels,
        seed=args.seed,
    )
    rgb = build_dense_rgb_canvas(block_specs=block_specs, dense_dir=dense_dir, mean=mean, comps=comps)
    out_npz = args.out_dir / "gse_dense_10m.npz"
    out_png = args.out_dir / "gse_dense_10m.png"
    extent_png = args.out_dir / "wuhan_east_lake_2x_ne_original_vs_gse_dense_10m_extent_check.png"
    original_canvas_path = (
        ROOT
        / "results"
        / "wuhan_east_lake_2x_ne_original_rgb"
        / "wuhan_east_lake_2x_ne_original_rgb_canvas.npz"
    )

    bboxes = [np.asarray(item["bbox_values"], dtype=float) for item in block_specs]
    coverage = np.min([b[:2] for b in bboxes], axis=0).tolist() + np.max([b[2:] for b in bboxes], axis=0).tolist()
    save_npz_atomic(out_npz, rgb_canvas=rgb, pca_mean=mean, pca_components=comps, coverage=np.asarray(coverage))
    plt.imsave(out_png, rgb)
    save_extent_figure(
        original_canvas_path=original_canvas_path,
        gse_rgb=rgb,
        coverage=coverage,
        out_path=extent_png,
    )
    write_json_atomic(
        args.out_dir / "gse_dense_10m.json",
        {
            "model": "gse",
            "output": "grid",
            "status": "ok",
            "dense_block_dir": str(dense_dir),
            "n_blocks": len(block_specs),
            "coverage": coverage,
            "rgb_canvas_shape": list(rgb.shape),
            "output_npz": str(out_npz),
            "output_png": str(out_png),
            "extent_check_png": str(extent_png),
            "pca_sample_pixels": int(args.max_sample_pixels),
            "notes": [
                "This is a dense 10 m GSE grid rendering, not pooled block colors.",
                "Each block checkpoint stores a 64-channel GSE grid as float16 to reduce disk usage.",
            ],
        },
    )
    print(f"wrote {out_png}", flush=True)
    print(f"wrote {extent_png}", flush=True)


if __name__ == "__main__":
    main()
