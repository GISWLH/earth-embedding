from __future__ import annotations

import argparse
import json
import textwrap
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from make_part2_model_map_figure_2x import (
    DEFAULT_DATA_DIR,
    DEFAULT_OUT_DIR,
    build_original_rgb_canvas,
    load_block_specs,
)

FONT_SCALE = 2.2
ICON_DIR_NAME = "concept_icons"
GROUP_ICON_FILES = {
    "I": "01_precomputed_products.png",
    "II": "02_masked_autoencoder_vision.png",
    "III": "03_vision_language_cross_modal.png",
    "IV": "04_multimodal_generalists.png",
    "V": "05_domain_specialized_encoders.png",
}


def scaled_font(size: float) -> float:
    return size * FONT_SCALE


MODEL_GROUPS = [
    (
        "I",
        "Precomputed products",
        ["gse", "tessera", "copernicus"],
        "#f5eef5",
    ),
    (
        "II",
        "Masked autoencoder / vision",
        ["satmae", "satmaepp", "satmaepp_s2_10b", "scalemae"],
        "#f8eff1",
    ),
    (
        "III",
        "Vision-language / cross-modal",
        ["remoteclip", "wildsat"],
        "#edf3f7",
    ),
    (
        "IV",
        "Multimodal generalists",
        ["anysat", "galileo", "prithvi", "terrafm", "terramind", "dofa"],
        "#eef6f1",
    ),
    (
        "V",
        "Domain-specialized encoders",
        ["agrifm", "fomo", "thor", "satvision"],
        "#f8f3ec",
    ),
]

MODEL_LABELS = {
    "gse": "GSE",
    "tessera": "TESSERA",
    "copernicus": "Copernicus",
    "satmae": "SatMAE",
    "satmaepp": "SatMAE++",
    "satmaepp_s2_10b": "S2-10B",
    "scalemae": "ScaleMAE",
    "remoteclip": "RemoteCLIP",
    "wildsat": "WildSAT",
    "anysat": "AnySat",
    "galileo": "Galileo",
    "prithvi": "Prithvi",
    "terrafm": "TerraFM",
    "terramind": "TerraMind",
    "dofa": "DOFA",
    "agrifm": "AgriFM",
    "fomo": "FoMo",
    "thor": "THOR",
    "satvision": "SatVision",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Redraw the part-2 public19 2x map figure with model-family grouping."
    )
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_OUT_DIR / "manifest_2x.json")
    parser.add_argument(
        "--png-name",
        default="part2_original_map_with_public19_models_2x_grouped.png",
    )
    parser.add_argument(
        "--pdf-name",
        default="part2_original_map_with_public19_models_2x_grouped.pdf",
    )
    return parser.parse_args()


def load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing manifest: {path}")
    return json.loads(path.read_text())


def model_result_by_name(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item["model"]): item for item in manifest.get("models", [])}


def load_model_rgb(result: dict[str, Any]) -> np.ndarray | None:
    npz_path = Path(str(result.get("output_npz", "")))
    if npz_path.exists():
        with np.load(npz_path, allow_pickle=True) as data:
            if "rgb_canvas" in data:
                return np.asarray(data["rgb_canvas"], dtype=np.float32)
    png_path = Path(str(result.get("output_png", "")))
    if png_path.exists():
        return np.asarray(plt.imread(png_path)[..., :3], dtype=np.float32)
    return None


def format_shape(result: dict[str, Any]) -> str:
    shape = result.get("shape")
    if isinstance(shape, list) and shape:
        return "x".join(str(int(dim)) for dim in shape)
    grid_hw = result.get("grid_hw")
    if isinstance(grid_hw, list) and len(grid_hw) == 2:
        return f"{int(grid_hw[0])}x{int(grid_hw[1])}"
    return ""


def show_panel(ax: plt.Axes, rgb: np.ndarray | None, title: str, subtitle: str = "") -> None:
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_linewidth(0.45)
        spine.set_color("#d8d8d8")
    if rgb is None:
        ax.set_facecolor("#f2f2f2")
        ax.text(
            0.5,
            0.54,
            title,
            ha="center",
            va="center",
            fontsize=scaled_font(8.5),
            fontweight="bold",
        )
        ax.text(
            0.5,
            0.43,
            "not available",
            ha="center",
            va="center",
            fontsize=scaled_font(7.5),
            color="#666666",
        )
        return
    ax.imshow(rgb, interpolation="nearest")
    ax.set_title(title, fontsize=scaled_font(9.2), pad=8.0, fontweight="bold")


def draw_group_label_square(ax: plt.Axes, roman: str, title: str, color: str) -> None:
    ax.set_facecolor(color)
    ax.set_box_aspect(1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.plot([0.08, 0.92], [0.14, 0.14], transform=ax.transAxes, color="#555555", lw=0.8)
    ax.text(
        0.5,
        0.70,
        roman,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=scaled_font(13.0),
        fontweight="bold",
        bbox={
            "boxstyle": "circle,pad=0.22",
            "facecolor": "white",
            "edgecolor": "#666666",
            "linewidth": 1.0,
        },
    )
    ax.text(
        0.5,
        0.33,
        textwrap.fill(title, width=16),
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=scaled_font(8.8),
        fontweight="bold",
        linespacing=1.0,
    )


def draw_icon_square(ax: plt.Axes, icon_path: Path | None, color: str) -> None:
    ax.set_facecolor("white")
    ax.set_box_aspect(1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.65)
        spine.set_color("#d4d4d4")
    if icon_path is not None and icon_path.exists():
        ax.imshow(plt.imread(icon_path))
    else:
        ax.text(
            0.5,
            0.5,
            "icon\nmissing",
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=scaled_font(6.2),
            color="#666666",
        )


def draw_original_reference_box(ax: plt.Axes, original_rgb: np.ndarray) -> None:
    ax.set_facecolor("#fff1f4")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(1.6)
        spine.set_color("#222222")
    ax.text(
        0.5,
        0.94,
        "Original RGB Reference",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=scaled_font(9.2),
        fontweight="bold",
    )
    inner = ax.inset_axes([0.08, 0.08, 0.84, 0.78])
    show_panel(inner, original_rgb, "")
    inner.set_title("")
    for spine in inner.spines.values():
        spine.set_linewidth(0.7)
        spine.set_color("#808080")


def draw_grouped_figure(
    *,
    original_rgb: np.ndarray,
    results: dict[str, dict[str, Any]],
    out_png: Path,
    out_pdf: Path,
) -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "DejaVu Sans", "Liberation Sans"],
            "axes.titlesize": scaled_font(9),
            "font.size": scaled_font(8),
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )

    icon_dir = out_png.parent / ICON_DIR_NAME

    fig = plt.figure(figsize=(28.0, 16.2), constrained_layout=False)
    outer = fig.add_gridspec(
        nrows=5,
        ncols=8,
        width_ratios=[1.08, 1.08, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18],
        height_ratios=[1, 1, 1, 1, 1],
        hspace=0.30,
        wspace=0.13,
        top=0.975,
        bottom=0.03,
        left=0.018,
        right=0.992,
    )

    for row, (roman, group_title, models, color) in enumerate(MODEL_GROUPS):
        ax_header = fig.add_subplot(outer[row, 0])
        icon_path = icon_dir / GROUP_ICON_FILES[roman]
        draw_group_label_square(ax_header, roman, group_title, color)
        ax_icon = fig.add_subplot(outer[row, 1])
        draw_icon_square(ax_icon, icon_path, color)
        for idx, model in enumerate(models, start=1):
            ax = fig.add_subplot(outer[row, idx + 1])
            ax.set_facecolor(color)
            result = results.get(model, {"model": model, "status": "missing"})
            rgb = load_model_rgb(result) if result.get("status") == "ok" else None
            shape = format_shape(result)
            show_panel(ax, rgb, MODEL_LABELS.get(model, model))
        if row in {0, 1}:
            blank_stop = 6
        else:
            blank_stop = 8
        for idx in range(len(models) + 2, blank_stop):
            ax = fig.add_subplot(outer[row, idx])
            ax.set_facecolor(color)
            ax.axis("off")

    ax_original = fig.add_subplot(outer[0:2, 6:8])
    draw_original_reference_box(ax_original, original_rgb)

    for path in (out_png, out_pdf):
        path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    fig.savefig(out_pdf, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    args = parse_args()
    manifest = load_manifest(args.manifest)
    block_specs = load_block_specs(args.data_dir)
    original_rgb = build_original_rgb_canvas(block_specs)
    results = model_result_by_name(manifest)
    draw_grouped_figure(
        original_rgb=original_rgb,
        results=results,
        out_png=args.out_dir / args.png_name,
        out_pdf=args.out_dir / args.pdf_name,
    )


if __name__ == "__main__":
    main()
