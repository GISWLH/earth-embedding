from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DEFAULT_DATA_DIR = ROOT.parent / "data" / "part2_20260502_full"
DEFAULT_SMOKE_DIR = ROOT / "results" / "all_models_smoke_20260502"
DEFAULT_OUT_DIR = DEFAULT_SMOKE_DIR / "figures"

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
REGION_B_MODELS = {"copernicus", "satvision", "tessera"}
CLASS_COLORS = {
    "water": "#2c7fb8",
    "vegetation": "#41ab5d",
    "forest_green": "#238443",
    "cropland": "#fec44f",
    "built": "#de2d26",
    "anchor": "#6a3d9a",
}
CLASS_LABELS = ["water", "vegetation", "forest_green", "cropland", "built", "anchor"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate part-2 survey benchmark overview figures."
    )
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--smoke-dir", type=Path, default=DEFAULT_SMOKE_DIR)
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


def load_region_a_mosaic(region_a_dir: Path) -> tuple[np.ndarray, tuple[float, float, float, float]]:
    block_dir = region_a_dir / "imagery_s2_20210501_20211031"
    block_paths = sorted(block_dir.glob("block_r*_c*.npz"))
    if not block_paths:
        raise FileNotFoundError(f"No Region A Sentinel-2 blocks found in {block_dir}")

    blocks: dict[tuple[int, int], np.ndarray] = {}
    bbox_minlon = math.inf
    bbox_minlat = math.inf
    bbox_maxlon = -math.inf
    bbox_maxlat = -math.inf
    for path in block_paths:
        match = re.match(r"block_r(\d+)_c(\d+)\.npz", path.name)
        if match is None:
            continue
        row = int(match.group(1))
        col = int(match.group(2))
        data = np.load(path, allow_pickle=True)
        array = np.asarray(data["array"], dtype=np.float32)
        bands = [str(b) for b in data["bands"].tolist()]
        bbox = np.asarray(data["bbox"], dtype=float)
        band_index = {name: idx for idx, name in enumerate(bands)}
        rgb = np.stack(
            [
                array[band_index["B4"]],
                array[band_index["B3"]],
                array[band_index["B2"]],
            ],
            axis=-1,
        )
        blocks[(row, col)] = rgb
        bbox_minlon = min(bbox_minlon, float(bbox[0]))
        bbox_minlat = min(bbox_minlat, float(bbox[1]))
        bbox_maxlon = max(bbox_maxlon, float(bbox[2]))
        bbox_maxlat = max(bbox_maxlat, float(bbox[3]))

    n_rows = max(row for row, _ in blocks) + 1
    n_cols = max(col for _, col in blocks) + 1
    row_images: list[np.ndarray] = []
    for row in range(n_rows):
        row_images.append(np.concatenate([blocks[(row, col)] for col in range(n_cols)], axis=1))
    mosaic = np.concatenate(row_images, axis=0)
    rgb = np.stack([robust_scale01(mosaic[..., idx]) for idx in range(3)], axis=-1)
    return rgb, (bbox_minlon, bbox_minlat, bbox_maxlon, bbox_maxlat)


def load_region_bounds(data_dir: Path) -> tuple[tuple[float, float, float, float], tuple[float, float, float, float]]:
    summary = json.loads((data_dir / "prepare_part2_data_summary.json").read_text())
    region_a = tuple(float(v) for v in summary["region_a_bounds"])
    region_b = tuple(float(v) for v in summary["region_b_bounds"])
    return region_a, region_b


def plot_region_overview(data_dir: Path, smoke_dir: Path, out_path: Path) -> None:
    region_a_dir = data_dir / "region_a"
    region_b_dir = data_dir / "region_b"
    mosaic_rgb, region_a_mosaic_bounds = load_region_a_mosaic(region_a_dir)
    region_a_bounds, region_b_bounds = load_region_bounds(data_dir)
    region_b = pd.read_csv(region_b_dir / "cell_manifest_025deg.csv")
    region_a_samples = pd.read_csv(smoke_dir / "region_a_samples.csv")
    region_b_samples = pd.read_csv(smoke_dir / "region_b_samples.csv")

    fig, axes = plt.subplots(1, 2, figsize=(15, 6), constrained_layout=True)

    ax = axes[0]
    ax.imshow(
        mosaic_rgb,
        extent=region_a_mosaic_bounds,
        origin="upper",
    )
    ax.set_title("Region A: small high-resolution ROI", fontsize=12)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.scatter(
        region_a_samples["center_lon"],
        region_a_samples["center_lat"],
        c=[CLASS_COLORS.get(x, "#444444") for x in region_a_samples["local_dominant_class"]],
        s=14,
        edgecolors="white",
        linewidths=0.3,
        alpha=0.9,
    )
    ax.text(
        0.02,
        0.02,
        "Sentinel-2 RGB mosaic\n16 blocks, 2173 candidate tiles",
        transform=ax.transAxes,
        fontsize=9,
        color="white",
        bbox={"facecolor": "black", "alpha": 0.55, "pad": 4},
    )

    ax = axes[1]
    for label, part in region_b.groupby("regional_dominant_class"):
        ax.scatter(
            part["center_lon"],
            part["center_lat"],
            label=label,
            s=38,
            marker="s",
            color=CLASS_COLORS.get(label, "#777777"),
            alpha=0.75,
            linewidths=0,
        )
    rect = Rectangle(
        (region_a_bounds[0], region_a_bounds[1]),
        region_a_bounds[2] - region_a_bounds[0],
        region_a_bounds[3] - region_a_bounds[1],
        fill=False,
        edgecolor="black",
        linewidth=1.5,
        linestyle="--",
    )
    ax.add_patch(rect)
    ax.scatter(
        region_b_samples["center_lon"],
        region_b_samples["center_lat"],
        c=[CLASS_COLORS.get(x, "#444444") for x in region_b_samples["regional_dominant_class"]],
        s=48,
        marker="o",
        edgecolors="black",
        linewidths=0.3,
        alpha=0.9,
    )
    ax.set_xlim(region_b_bounds[0], region_b_bounds[2])
    ax.set_ylim(region_b_bounds[1], region_b_bounds[3])
    ax.set_title("Region B: large coarse regional grid", fontsize=12)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.text(
        0.02,
        0.02,
        "Manifest-only regional benchmark\n1056 cells, 15 sampled cells shown as circles",
        transform=ax.transAxes,
        fontsize=9,
        bbox={"facecolor": "white", "alpha": 0.85, "pad": 4},
    )
    ax.legend(loc="upper left", fontsize=8, frameon=True)

    fig.suptitle("Part-2 benchmark regions", fontsize=15, y=1.02)
    fig.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def pca_2d(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=np.float32)
    if x.ndim != 2:
        raise ValueError(f"Expected 2D embedding matrix, got shape {x.shape}")
    if x.shape[0] == 1:
        return np.zeros((1, 2), dtype=np.float32)
    mean = x.mean(axis=0, keepdims=True)
    std = x.std(axis=0, keepdims=True)
    x = (x - mean) / np.where(std > 1e-6, std, 1.0)
    x = np.nan_to_num(x, nan=0.0, posinf=0.0, neginf=0.0)
    _, _, vt = np.linalg.svd(x, full_matrices=False)
    comps = vt[:2].T
    proj = x @ comps
    if proj.shape[1] == 1:
        proj = np.concatenate([proj, np.zeros((proj.shape[0], 1), dtype=proj.dtype)], axis=1)
    return proj[:, :2]


def load_labels(smoke_dir: Path) -> tuple[dict[str, str], dict[str, str]]:
    region_a = pd.read_csv(smoke_dir / "region_a_samples.csv")
    region_b = pd.read_csv(smoke_dir / "region_b_samples.csv")
    region_a_labels = dict(zip(region_a["tile_id"], region_a["local_dominant_class"], strict=True))
    region_b_labels = dict(zip(region_b["cell_id"], region_b["regional_dominant_class"], strict=True))
    return region_a_labels, region_b_labels


def labels_for_model(
    model: str,
    ids: np.ndarray,
    *,
    region_a_labels: dict[str, str],
    region_b_labels: dict[str, str],
) -> list[str]:
    labels: list[str] = []
    for item_id in ids.tolist():
        key = str(item_id)
        if model == "tessera":
            labels.append("anchor")
        elif model in REGION_B_MODELS:
            labels.append(region_b_labels.get(key, "anchor"))
        else:
            labels.append(region_a_labels.get(key, "anchor"))
    return labels


def plot_embedding_overview(smoke_dir: Path, out_path: Path) -> list[str]:
    fig, axes = plt.subplots(4, 5, figsize=(18, 13), constrained_layout=True)
    axes_flat = list(axes.flat)
    private_models: list[str] = []
    region_a_labels, region_b_labels = load_labels(smoke_dir)

    for ax, model in zip(axes_flat[: len(PUBLIC_MODELS)], PUBLIC_MODELS, strict=True):
        data = np.load(smoke_dir / f"embeddings_{model}.npz", allow_pickle=True)
        ids = np.asarray(data["ids"])
        embeddings = np.asarray(data["embeddings"], dtype=np.float32)
        coords = pca_2d(embeddings)
        labels = labels_for_model(
            model,
            ids,
            region_a_labels=region_a_labels,
            region_b_labels=region_b_labels,
        )
        for label in sorted(set(labels), key=CLASS_LABELS.index):
            idx = [i for i, item in enumerate(labels) if item == label]
            ax.scatter(
                coords[idx, 0],
                coords[idx, 1],
                s=48 if label == "anchor" else 34,
                color=CLASS_COLORS[label],
                edgecolors="black",
                linewidths=0.25,
                alpha=0.9,
            )
        ax.axhline(0.0, color="#cccccc", linewidth=0.6, zorder=0)
        ax.axvline(0.0, color="#cccccc", linewidth=0.6, zorder=0)
        split = "Region B" if model in REGION_B_MODELS else "Region A"
        ax.set_title(f"{model}\n{split} | n={len(ids)} | d={embeddings.shape[1]}", fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])

    note_ax = axes_flat[len(PUBLIC_MODELS)]
    note_ax.axis("off")
    note_ax.text(
        0.02,
        0.92,
        "Private / local-only models",
        fontsize=12,
        fontweight="bold",
        va="top",
    )
    note_ax.text(
        0.02,
        0.70,
        "No verified private-model embedding outputs\nwere found in the repository result folders.\n\n"
        "This overview therefore shows the 19\ncanonical public models only.",
        fontsize=10,
        va="top",
    )
    for ax in axes_flat[len(PUBLIC_MODELS) + 1 :]:
        ax.axis("off")

    legend_handles = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label=label,
            markerfacecolor=CLASS_COLORS[label],
            markeredgecolor="black",
            markersize=8,
        )
        for label in CLASS_LABELS
    ]
    fig.legend(
        handles=legend_handles,
        loc="lower center",
        ncol=len(CLASS_LABELS),
        frameon=False,
        bbox_to_anchor=(0.5, -0.01),
    )
    fig.suptitle(
        "Part-2 embedding overview (19 canonical public models)",
        fontsize=16,
        y=1.02,
    )
    fig.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close(fig)
    return private_models


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    region_figure = args.out_dir / "part2_region_overview.png"
    embedding_figure = args.out_dir / "part2_embedding_overview_public19.png"
    manifest_path = args.out_dir / "part2_overview_manifest.json"

    plot_region_overview(args.data_dir, args.smoke_dir, region_figure)
    private_models = plot_embedding_overview(args.smoke_dir, embedding_figure)

    manifest = {
        "data_dir": str(args.data_dir),
        "smoke_dir": str(args.smoke_dir),
        "generated_files": {
            "region_overview": str(region_figure),
            "embedding_overview": str(embedding_figure),
        },
        "public_model_count": len(PUBLIC_MODELS),
        "public_models": PUBLIC_MODELS,
        "private_models_found": private_models,
        "notes": [
            "Region A is rendered from the downloaded Sentinel-2 block mosaic.",
            "Region B is rendered from the prepared coarse manifest because current prep is manifest-only.",
            "No verified private-model embedding outputs were found in repository result folders.",
        ],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
