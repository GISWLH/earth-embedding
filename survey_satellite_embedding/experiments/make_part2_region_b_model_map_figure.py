from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

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
DEFAULT_OUT_DIR = ROOT / "results" / "part2_region_b_model_map_figure"

REGION_B_MODELS = ["copernicus", "tessera", "satvision"]
CLASS_COLORS = {
    "water": "#2c7fb8",
    "cropland": "#fec44f",
    "forest_green": "#238443",
    "built": "#de2d26",
    "anchor": "#6a3d9a",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a Region-B coarse-grid embedding map figure."
    )
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--smoke-dir", type=Path, default=DEFAULT_SMOKE_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--models", nargs="+", default=REGION_B_MODELS)
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
    if x.shape[0] < 2:
        return np.tile(np.array([[0.42, 0.24, 0.66]], dtype=np.float32), (x.shape[0], 1))

    x = x - x.mean(axis=0, keepdims=True)
    x = np.nan_to_num(x, nan=0.0, posinf=0.0, neginf=0.0)
    _, _, vt = np.linalg.svd(x, full_matrices=False)
    comps = vt[: min(3, vt.shape[0])].T
    y = x @ comps
    if y.shape[1] < 3:
        pad = np.zeros((y.shape[0], 3 - y.shape[1]), dtype=y.dtype)
        y = np.concatenate([y, pad], axis=1)
    return np.stack([robust_scale01(y[:, idx]) for idx in range(3)], axis=-1)


def format_embedding_shape(embeddings: Any) -> str:
    return "*".join(str(int(dim)) for dim in np.asarray(embeddings).shape)


def load_region_b_bounds(data_dir: Path) -> tuple[float, float, float, float]:
    summary = json.loads((data_dir / "prepare_part2_data_summary.json").read_text())
    return tuple(float(v) for v in summary["region_b_bounds"])


def configure_map_axis(ax: plt.Axes, bounds: tuple[float, float, float, float]) -> None:
    ax.set_xlim(bounds[0], bounds[2])
    ax.set_ylim(bounds[1], bounds[3])
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")


def draw_cell_rect(
    ax: plt.Axes,
    row: Any,
    *,
    facecolor: str | tuple[float, float, float] | np.ndarray,
    edgecolor: str = "none",
    linewidth: float = 0.0,
    alpha: float = 1.0,
) -> None:
    ax.add_patch(
        Rectangle(
            (float(row.minlon), float(row.minlat)),
            float(row.maxlon) - float(row.minlon),
            float(row.maxlat) - float(row.minlat),
            facecolor=facecolor,
            edgecolor=edgecolor,
            linewidth=linewidth,
            alpha=alpha,
        )
    )


def draw_region_b_reference(
    ax: plt.Axes,
    manifest: pd.DataFrame,
    bounds: tuple[float, float, float, float],
) -> None:
    for row in manifest.itertuples(index=False):
        draw_cell_rect(
            ax,
            row,
            facecolor=CLASS_COLORS.get(str(row.regional_dominant_class), "#bbbbbb"),
            edgecolor="white",
            linewidth=0.08,
            alpha=0.9,
        )
    configure_map_axis(ax, bounds)
    ax.set_title("Region B coarse manifest\n1056 cells, 0.25 deg", fontsize=11)


def draw_embedding_panel(
    ax: plt.Axes,
    *,
    model: str,
    manifest: pd.DataFrame,
    bounds: tuple[float, float, float, float],
    smoke_dir: Path,
) -> dict[str, Any]:
    data = np.load(smoke_dir / f"embeddings_{model}.npz", allow_pickle=True)
    ids = [str(item) for item in np.asarray(data["ids"]).tolist()]
    embeddings = np.asarray(data["embeddings"], dtype=np.float32)
    colors = embedding_rgb(embeddings)

    for row in manifest.itertuples(index=False):
        draw_cell_rect(ax, row, facecolor="#f1f1f1", edgecolor="white", linewidth=0.08)

    cell_lookup = {str(row.cell_id): row for row in manifest.itertuples(index=False)}
    plotted = 0
    for item_id, color in zip(ids, colors, strict=True):
        if item_id in cell_lookup:
            draw_cell_rect(
                ax,
                cell_lookup[item_id],
                facecolor=color,
                edgecolor="black",
                linewidth=0.45,
                alpha=0.95,
            )
            plotted += 1

    if model == "tessera":
        ax.scatter(
            [121.45],
            [31.15],
            s=80,
            marker="*",
            color=colors[0],
            edgecolors="black",
            linewidths=0.5,
            zorder=5,
        )
        plotted = len(ids)

    configure_map_axis(ax, bounds)
    ax.set_title(f"{model} [{format_embedding_shape(embeddings)}]", fontsize=11)
    ax.text(
        0.02,
        0.02,
        "Pooled embedding PCA RGB\non sampled Region B cells",
        transform=ax.transAxes,
        fontsize=8,
        bbox={"facecolor": "white", "alpha": 0.82, "pad": 3},
    )
    return {
        "model": model,
        "ids": ids,
        "shape": list(embeddings.shape),
        "plotted_items": plotted,
        "output_npz": str(smoke_dir / f"embeddings_{model}.npz"),
        "output_json": str(smoke_dir / f"embeddings_{model}.json"),
    }


def draw_summary_figure(
    *,
    data_dir: Path,
    smoke_dir: Path,
    out_path: Path,
    models: list[str],
) -> list[dict[str, Any]]:
    manifest = pd.read_csv(data_dir / "region_b" / "cell_manifest_025deg.csv")
    bounds = load_region_b_bounds(data_dir)
    n_panels = len(models) + 1
    n_cols = min(4, n_panels)
    n_rows = int(np.ceil(n_panels / n_cols))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5.1 * n_cols, 4.4 * n_rows))
    axes_flat = np.atleast_1d(axes).ravel().tolist()

    draw_region_b_reference(axes_flat[0], manifest, bounds)
    results = [
        draw_embedding_panel(
            axes_flat[idx],
            model=model,
            manifest=manifest,
            bounds=bounds,
            smoke_dir=smoke_dir,
        )
        for idx, model in enumerate(models, start=1)
    ]

    for ax in axes_flat[n_panels:]:
        ax.axis("off")

    legend_handles = [
        Line2D(
            [0],
            [0],
            marker="s",
            color="w",
            label=label,
            markerfacecolor=color,
            markeredgecolor="black",
            markersize=8,
        )
        for label, color in CLASS_COLORS.items()
    ]
    fig.legend(
        handles=legend_handles,
        loc="lower center",
        ncol=len(legend_handles),
        frameon=False,
        bbox_to_anchor=(0.5, -0.02),
    )
    fig.suptitle(
        "Region B coarse-grid embedding maps",
        fontsize=16,
        y=0.96,
    )
    fig.subplots_adjust(
        left=0.045,
        right=0.995,
        top=0.86,
        bottom=0.16,
        wspace=0.18,
        hspace=0.3,
    )
    fig.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close(fig)
    return results


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    models = [str(model) for model in args.models]
    summary_path = args.out_dir / "part2_region_b_coarse_embedding_maps.png"
    model_results = draw_summary_figure(
        data_dir=args.data_dir,
        smoke_dir=args.smoke_dir,
        out_path=summary_path,
        models=models,
    )

    manifest = {
        "region": "region_b",
        "data_dir": str(args.data_dir),
        "smoke_dir": str(args.smoke_dir),
        "summary_figure": str(summary_path),
        "models": model_results,
        "notes": [
            "Region B preparation is manifest-only: 1056 coarse 0.25 degree cells.",
            "Current Region B smoke embeddings exist for copernicus, tessera, and satvision.",
            "Panels render pooled embedding matrices as PCA RGB colors on sampled cells.",
        ],
    }
    (args.out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
