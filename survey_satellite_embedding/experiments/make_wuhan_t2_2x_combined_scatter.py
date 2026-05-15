"""Make a combined 19-model scatter figure for Wuhan T2 2x fraction regression."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import AutoMinorLocator
import numpy as np
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.stats import gaussian_kde, spearmanr

ROOT = Path(__file__).resolve().parent
DEFAULT_RESULT_DIR = ROOT / "results" / "downstream_fraction_2x"
DEFAULT_OUTPUT = DEFAULT_RESULT_DIR / "figures" / "fraction_regression_scatter_public19_2x.png"

TARGETS = [
    ("built", "Built-up", "#576A8F"),
    ("vegetation", "Vegetation", "#B7BDF7"),
    ("cropland", "Cropland", "#FFF8DE"),
    ("water", "Water", "#FEEAC9"),
]
BOLD_LINE_COLOR = "#F5AFAF"
AXIS_MIN = -0.1
AXIS_MAX = 1.05
FIGURE_SCALE = 1.6
FONT_SCALE = 2.0
MODEL_GROUPS = [
    ("Precomputed\nproducts", ["gse", "tessera", "copernicus"], "#f3edf5"),
    (
        "Masked\nautoencoder\n/ vision",
        ["satmae", "satmaepp", "satmaepp_s2_10b", "scalemae"],
        "#f7eef0",
    ),
    ("Vision-language\n/ cross-modal", ["remoteclip", "wildsat"], "#eef3f8"),
    (
        "Multimodal\ngeneralists",
        ["anysat", "galileo", "prithvi", "terrafm", "terramind", "dofa"],
        "#eef5ef",
    ),
    ("Domain-specialized\nencoders", ["agrifm", "fomo", "thor", "satvision"], "#f7f1e8"),
]
MODEL_DISPLAY_NAMES = {
    "agrifm": "AgriFM",
    "anysat": "AnySat",
    "copernicus": "Copernicus",
    "dofa": "DOFA",
    "fomo": "FoMo",
    "galileo": "Galileo",
    "gse": "GSE",
    "prithvi": "Prithvi",
    "remoteclip": "RemoteCLIP",
    "satmae": "SatMAE",
    "satmaepp": "SatMAE++",
    "satmaepp_s2_10b": "S2-10B",
    "satvision": "SatVision",
    "scalemae": "ScaleMAE",
    "terrafm": "TerraFM",
    "terramind": "TerraMind",
    "tessera": "TESSERA",
    "thor": "THOR",
    "wildsat": "WildSAT",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Combine all public-19 T2 fraction-regression scatter plots into one figure."
    )
    parser.add_argument("--result-dir", type=Path, default=DEFAULT_RESULT_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def roman_numeral(value: int) -> str:
    numerals = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
    return numerals[value]


def present_model_groups(result_dir: Path) -> list[tuple[str, list[str], str, str]]:
    groups: list[tuple[str, list[str], str, str]] = []
    for group_name, group_models, color in MODEL_GROUPS:
        present = [
            model
            for model in group_models
            if (result_dir / f"fraction_regression_predictions_{model}.csv").exists()
        ]
        if not present:
            continue
        groups.append((group_name, present, color, roman_numeral(len(groups) + 1)))
    return groups


def model_order_from_groups(result_dir: Path) -> list[str]:
    order: list[str] = []
    for _, present, _, _ in present_model_groups(result_dir):
        order.extend(present)
    return order


def clipped(values: np.ndarray) -> np.ndarray:
    return np.clip(values.astype(float), 0.0, 1.0)


def kde_curve(values: np.ndarray, grid: np.ndarray) -> np.ndarray | None:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if values.size < 2 or np.allclose(values.min(), values.max()):
        return None
    try:
        density = gaussian_kde(values, bw_method="scott")(grid)
        peak = float(np.nanmax(density))
        if not np.isfinite(peak) or peak <= 0:
            return None
        return density / peak
    except Exception:
        return None


def mean_spearman(preds: pd.DataFrame) -> float:
    scores = []
    for target, _, _ in TARGETS:
        rho = spearmanr(preds[f"true_{target}"], preds[f"pred_{target}"]).statistic
        if np.isfinite(rho):
            scores.append(float(rho))
    return float(np.mean(scores)) if scores else float("nan")


def draw_panel(ax: plt.Axes, result_dir: Path, model: str) -> None:
    preds = pd.read_csv(result_dir / f"fraction_regression_predictions_{model}.csv")
    ax.set_facecolor("white")
    divider = make_axes_locatable(ax)
    ax_top = divider.append_axes("top", size="22%", pad=0.08, sharex=ax)
    ax_right = divider.append_axes("right", size="22%", pad=0.08, sharey=ax)
    ax_top.set_facecolor("white")
    ax_right.set_facecolor("white")

    for target, label, color in TARGETS:
        ax.scatter(
            clipped(preds[f"true_{target}"].to_numpy()),
            clipped(preds[f"pred_{target}"].to_numpy()),
            s=16,
            alpha=0.72,
            color=color,
            edgecolors="white",
            linewidths=0.45,
            label=label,
            rasterized=True,
        )
    ax.plot(
        [AXIS_MIN, 1],
        [AXIS_MIN, 1],
        color=BOLD_LINE_COLOR,
        linewidth=1.5,
        linestyle="--",
        zorder=1,
    )
    ax.set_xlim(AXIS_MIN, AXIS_MAX)
    ax.set_ylim(AXIS_MIN, AXIS_MAX)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(color="#dddddd", linewidth=0.55, alpha=0.65)
    rho = mean_spearman(preds)
    ax.set_title(
        f"{MODEL_DISPLAY_NAMES.get(model, model)}\nmean rho={rho:.3f}",
        fontsize=14.2 * FONT_SCALE,
        pad=7,
    )
    ax.tick_params(
        axis="both",
        labelsize=12.2 * FONT_SCALE,
        width=1.0,
        length=8,
        direction="in",
        labelbottom=True,
        labelleft=True,
        colors="#454545",
    )
    ax.tick_params(axis="both", which="minor", width=1.0, length=4, direction="in", colors="#454545")
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.set_xlabel("True fraction", fontsize=15 * FONT_SCALE)
    ax.set_ylabel("Predicted fraction", fontsize=16 * FONT_SCALE)
    for spine in ["top", "right", "left", "bottom"]:
        ax.spines[spine].set_visible(True)
        ax.spines[spine].set_color("#454545")
        ax.spines[spine].set_linewidth(1.0)

    grid = np.linspace(AXIS_MIN, AXIS_MAX, 300)
    for target, _, color in TARGETS:
        true_vals = clipped(preds[f"true_{target}"].to_numpy())
        pred_vals = clipped(preds[f"pred_{target}"].to_numpy())
        true_kde = kde_curve(true_vals, grid)
        pred_kde = kde_curve(pred_vals, grid)
        if true_kde is not None:
            ax_top.plot(grid, true_kde, color=color, linewidth=1.9)
        if pred_kde is not None:
            ax_right.plot(pred_kde, grid, color=color, linewidth=1.9)

    overall_true = kde_curve(clipped(preds[[f"true_{t}" for t, _, _ in TARGETS]].to_numpy().ravel()), grid)
    overall_pred = kde_curve(clipped(preds[[f"pred_{t}" for t, _, _ in TARGETS]].to_numpy().ravel()), grid)
    if overall_true is not None:
        ax_top.plot(grid, overall_true, color=BOLD_LINE_COLOR, linewidth=3.4)
    if overall_pred is not None:
        ax_right.plot(overall_pred, grid, color=BOLD_LINE_COLOR, linewidth=3.4)

    for extra_ax in [ax_top, ax_right]:
        extra_ax.grid(False)
        extra_ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        extra_ax.spines["top"].set_visible(False)
        extra_ax.spines["right"].set_visible(False)
        extra_ax.spines["left"].set_visible(False)
        extra_ax.spines["bottom"].set_visible(False)

    ax_top.set_ylim(bottom=0)
    ax_top.set_xlim(AXIS_MIN, AXIS_MAX)
    ax_right.set_xlim(left=0)
    ax_right.set_ylim(AXIS_MIN, AXIS_MAX)


def main() -> None:
    args = parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    font_path = "/usr/share/fonts/arial/ARIAL.TTF"
    if Path(font_path).exists():
        font_manager.fontManager.addfont(font_path)
        font_name = font_manager.FontProperties(fname=font_path).get_name()
    else:
        font_name = "Arial"
    plt.style.use("seaborn-v0_8-talk")
    mpl.rcParams["svg.fonttype"] = "none"
    mpl.rcParams["svg.hashsalt"] = "hello"
    plt.rcParams.update(
        {
            "font.family": font_name,
            "font.size": 10 * FONT_SCALE,
            "axes.titlesize": 11 * FONT_SCALE,
            "axes.labelsize": 10 * FONT_SCALE,
            "xtick.labelsize": 9 * FONT_SCALE,
            "ytick.labelsize": 9 * FONT_SCALE,
            "legend.fontsize": 9 * FONT_SCALE,
            "figure.dpi": 600,
            "figure.figsize": (6, 4),
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
            "axes.facecolor": "white",
            "lines.linewidth": 1.0,
            "axes.linewidth": 1.0,
            "axes.spines.left": True,
            "axes.spines.bottom": True,
            "axes.spines.top": True,
            "axes.spines.right": True,
            "axes.edgecolor": "#454545",
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.major.size": 8,
            "ytick.major.size": 8,
            "xtick.minor.size": 4,
            "ytick.minor.size": 4,
            "xtick.major.width": 1.0,
            "ytick.major.width": 1.0,
            "xtick.minor.width": 1.0,
            "ytick.minor.width": 1.0,
            "xtick.color": "#454545",
            "ytick.color": "#454545",
            "savefig.bbox": "tight",
            "savefig.transparent": False,
        }
    )
    groups = present_model_groups(args.result_dir)
    model_order = model_order_from_groups(args.result_dir)
    if not model_order:
        raise FileNotFoundError(f"No prediction CSV files found under {args.result_dir}")

    max_cols = max(len(models) for _, models, _, _ in groups)
    fig, axes = plt.subplots(
        len(groups),
        max_cols,
        figsize=(34 * FIGURE_SCALE, 28 * FIGURE_SCALE),
        sharex=False,
        sharey=False,
        constrained_layout=False,
    )
    axes = np.asarray(axes).reshape(len(groups), max_cols)
    fig.subplots_adjust(left=0.075, right=0.995, bottom=0.065, top=0.955, hspace=0.38, wspace=0.18)

    for row_idx, (group_name, models, color, roman) in enumerate(groups):
        row_axes = axes[row_idx]
        for col_idx, ax in enumerate(row_axes):
            if col_idx < len(models):
                draw_panel(ax, args.result_dir, models[col_idx])
            else:
                ax.axis("off")

        row_pos = row_axes[0].get_position()
        fig.text(
            0.038,
            (row_pos.y0 + row_pos.y1) / 2,
            f"{roman}\n{group_name}",
            ha="center",
            va="center",
            fontsize=18 * FONT_SCALE,
            fontweight="bold",
            linespacing=0.95,
        )

    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        frameon=False,
        ncol=4,
        loc="lower center",
        bbox_to_anchor=(0.55, 0.012),
        fontsize=17 * FONT_SCALE,
        handletextpad=0.5,
        columnspacing=1.7,
    )

    fig.suptitle(
        "Wuhan 2x T2 fraction regression: public-19 scatter plots by model family",
        y=0.972,
        fontsize=21 * FONT_SCALE,
        fontweight="bold",
    )
    fig.savefig(args.output, dpi=300)
    plt.close(fig)
    print(args.output)


if __name__ == "__main__":
    main()
