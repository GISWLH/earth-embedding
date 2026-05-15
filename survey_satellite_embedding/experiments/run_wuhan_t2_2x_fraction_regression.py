"""Run T2 fraction regression from existing 2x tile embeddings only."""

# ruff: noqa: E402, I001

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
for candidate in [REPO_ROOT, REPO_ROOT / "src"]:
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent
DEFAULT_CORE_2X_DIR = ROOT / "results" / "downstream_core_2x"
DEFAULT_LABELS = DEFAULT_CORE_2X_DIR / "downstream_labels_500m_2x.csv"
DEFAULT_EMBEDDING_DIR = DEFAULT_CORE_2X_DIR / "embeddings_2x_tile"
DEFAULT_OUT_DIR = ROOT / "results" / "downstream_fraction_2x"

TARGETS = [
    ("built", "local_built_frac"),
    ("vegetation", "local_vegetation_frac"),
    ("cropland", "local_cropland_frac"),
    ("water", "local_water_frac"),
]
ALPHA_GRID = [0.01, 0.1, 1.0, 10.0, 100.0]
MODEL_GROUPS = [
    ("Precomputed\nproducts", ["gse", "tessera", "copernicus"], "#f3edf5"),
    (
        "Masked\nautoencoder\n/ vision",
        ["satmae", "satmaepp", "satmaepp_s2_10b", "scalemae"],
        "#f7eef0",
    ),
    (
        "Vision-language\n/ cross-modal",
        ["remoteclip", "wildsat"],
        "#eef3f8",
    ),
    (
        "Multimodal\ngeneralists",
        ["anysat", "galileo", "prithvi", "terrafm", "terramind", "dofa"],
        "#eef5ef",
    ),
    (
        "Domain-specialized\nencoders",
        ["agrifm", "fomo", "thor", "satvision"],
        "#f7f1e8",
    ),
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
FRACTION_FIGURE_TARGETS = [
    ("built", "Built-up"),
    ("vegetation", "Vegetation"),
    ("water", "Water"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run Wuhan T2 fraction regression using existing local 2x tile embeddings. "
            "This script never exports embeddings or fetches GEE imagery."
        )
    )
    parser.add_argument("--labels", type=Path, default=DEFAULT_LABELS)
    parser.add_argument("--embedding-dir", type=Path, default=DEFAULT_EMBEDDING_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--models", nargs="+", default=None)
    return parser.parse_args()


def load_labels(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing 2x label file: {path}")
    labels = pd.read_csv(path)
    required = {
        "tile_id",
        "split",
        "local_built_frac",
        "local_vegetation_frac",
        "local_cropland_frac",
        "local_water_frac",
    }
    missing = sorted(required - set(labels.columns))
    if missing:
        raise ValueError(f"Label file is missing required columns: {missing}")
    labels["use_for_t2"] = np.all(
        np.isfinite(labels[[col for _, col in TARGETS]].to_numpy(dtype=np.float32)),
        axis=1,
    )
    return labels


def available_models(embedding_dir: Path, requested: list[str] | None) -> list[str]:
    if not embedding_dir.exists():
        raise FileNotFoundError(f"Missing local 2x embedding directory: {embedding_dir}")
    found = sorted(path.stem for path in embedding_dir.glob("*.npz"))
    if requested is None:
        return found
    missing = sorted(set(requested) - set(found))
    if missing:
        raise ValueError(f"Requested models are missing local 2x embeddings: {missing}")
    return requested


def load_embeddings(path: Path, labels: pd.DataFrame) -> np.ndarray:
    payload = np.load(path, allow_pickle=True)
    if "embeddings" in payload:
        embeddings = np.asarray(payload["embeddings"], dtype=np.float32)
    else:
        keys = [key for key in payload.files if key.startswith("embeddings")]
        if len(keys) != 1:
            raise ValueError(f"Could not identify embedding array in {path}; keys={payload.files}")
        embeddings = np.asarray(payload[keys[0]], dtype=np.float32)

    if "tile_id" in payload:
        tile_ids = payload["tile_id"].astype(str)
        expected = labels["tile_id"].astype(str).to_numpy()
        if list(tile_ids) != list(expected):
            order = {tile_id: idx for idx, tile_id in enumerate(tile_ids)}
            embeddings = embeddings[[order[tile_id] for tile_id in expected]]

    if embeddings.shape[0] != len(labels):
        raise ValueError(f"Embedding row mismatch for {path}: {embeddings.shape[0]} != {len(labels)}")
    if embeddings.ndim > 2:
        embeddings = embeddings.reshape(embeddings.shape[0], embeddings.shape[1], -1).mean(axis=2)
    return embeddings.astype(np.float32)


def regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    rho = spearmanr(y_true, y_pred).statistic
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "r2": float(r2_score(y_true, y_pred)),
        "spearman": float(rho) if np.isfinite(rho) else math.nan,
    }


def choose_alpha(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_val: np.ndarray,
    y_val: np.ndarray,
) -> tuple[float, dict[str, float]]:
    best_alpha = ALPHA_GRID[0]
    best_metrics = {"mae": math.nan, "rmse": math.inf, "r2": math.nan, "spearman": math.nan}
    for alpha in ALPHA_GRID:
        model = Ridge(alpha=alpha, solver="svd")
        model.fit(x_train, y_train)
        metrics = regression_metrics(y_val, model.predict(x_val))
        if metrics["rmse"] < best_metrics["rmse"]:
            best_alpha = alpha
            best_metrics = metrics
    return best_alpha, best_metrics


def fit_model(
    embeddings: np.ndarray,
    labels: pd.DataFrame,
) -> tuple[dict[str, Any], pd.DataFrame]:
    usable = labels["use_for_t2"].to_numpy(dtype=bool) & np.all(np.isfinite(embeddings), axis=1)
    split = labels["split"].astype(str).to_numpy()
    masks = {name: usable & (split == name) for name in ["train", "val", "test"]}
    if not all(masks[name].any() for name in ["train", "val", "test"]):
        raise ValueError("T2 requires non-empty train/val/test splits.")

    scaler = StandardScaler().fit(embeddings[masks["train"]])
    x_train = scaler.transform(embeddings[masks["train"]])
    x_val = scaler.transform(embeddings[masks["val"]])
    x_test = scaler.transform(embeddings[masks["test"]])
    x_trainval = np.concatenate([x_train, x_val], axis=0)

    metrics: dict[str, Any] = {
        "split_train": int(masks["train"].sum()),
        "split_val": int(masks["val"].sum()),
        "split_test": int(masks["test"].sum()),
    }
    pred_rows = pd.DataFrame(
        {
            "split": labels.loc[masks["test"], "split"].astype(str).to_numpy(),
            "tile_id": labels.loc[masks["test"], "tile_id"].astype(str).to_numpy(),
        }
    )

    for target_name, target_col in TARGETS:
        y_train = labels.loc[masks["train"], target_col].to_numpy(dtype=np.float32)
        y_val = labels.loc[masks["val"], target_col].to_numpy(dtype=np.float32)
        y_test = labels.loc[masks["test"], target_col].to_numpy(dtype=np.float32)
        y_trainval = np.concatenate([y_train, y_val], axis=0)

        alpha, val_metrics = choose_alpha(x_train, y_train, x_val, y_val)
        reg = Ridge(alpha=alpha, solver="svd")
        reg.fit(x_trainval, y_trainval)
        y_pred = reg.predict(x_test)
        test_metrics = regression_metrics(y_test, y_pred)

        metrics[f"{target_name}_alpha"] = float(alpha)
        for key, value in val_metrics.items():
            metrics[f"{target_name}_val_{key}"] = value
        for key, value in test_metrics.items():
            metrics[f"{target_name}_test_{key}"] = value
        pred_rows[f"true_{target_name}"] = y_test
        pred_rows[f"pred_{target_name}"] = y_pred

    return metrics, pred_rows


def write_scatter(out_dir: Path, model: str, preds: pd.DataFrame) -> None:
    fig_dir = out_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(9, 8), constrained_layout=True)
    for ax, (target_name, _) in zip(axes.flat, TARGETS, strict=True):
        y_true = preds[f"true_{target_name}"].to_numpy(dtype=float)
        y_pred = preds[f"pred_{target_name}"].to_numpy(dtype=float)
        metrics = regression_metrics(y_true, y_pred)
        lo = float(np.nanmin([y_true.min(), y_pred.min()]))
        hi = float(np.nanmax([y_true.max(), y_pred.max()]))
        pad = max(0.02, 0.05 * (hi - lo))
        lo -= pad
        hi += pad
        ax.scatter(y_true, y_pred, s=13, alpha=0.72, color="#4776b4")
        ax.plot([lo, hi], [lo, hi], color="#444444", linewidth=1)
        ax.set_xlim(lo, hi)
        ax.set_ylim(lo, hi)
        ax.set_title(
            f"{target_name}: RMSE {metrics['rmse']:.3f}, rho {metrics['spearman']:.3f}",
            fontsize=10,
        )
        ax.set_xlabel("WorldCover fraction")
        ax.set_ylabel("Predicted fraction")
        ax.grid(alpha=0.25)
    fig.suptitle(f"{model} T2 fraction regression, 2x Wuhan test split", fontsize=13)
    fig.savefig(fig_dir / f"fraction_regression_scatter_{model}.png", dpi=200)
    plt.close(fig)


def write_metric_figure(out_dir: Path, results: pd.DataFrame) -> None:
    fig_dir = out_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    ok = results[results["status"] == "ok"].copy()
    if ok.empty:
        return
    ok["mean_test_spearman"] = ok[[f"{name}_test_spearman" for name, _ in TARGETS]].mean(axis=1)
    model_order: list[str] = []
    positions: list[float] = []
    spans: list[tuple[float, float, str, str, str]] = []
    cursor = 0.0
    group_index = 1
    for group_name, group_models, color in MODEL_GROUPS:
        present = [model for model in group_models if model in set(ok["model"])]
        if not present:
            continue
        start = cursor
        for model in present:
            model_order.append(model)
            positions.append(cursor)
            cursor += 1.0
        spans.append((start - 0.5, cursor - 0.5, color, group_name, roman_numeral(group_index)))
        group_index += 1
        cursor += 0.8

    ordered = ok.set_index("model").loc[model_order]
    fig, ax = plt.subplots(figsize=(19, 8.8))
    fig.subplots_adjust(left=0.07, right=0.995, bottom=0.18, top=0.62)
    for start, end, color, _, _ in spans:
        ax.axvspan(start, end, color=color, alpha=0.65, zorder=0)
    x = np.asarray(positions)
    width = 0.22
    colors = ["#FFB6B9", "#FAE3D9", "#BBDED6"]
    hatches = ["", "||", "\\\\"]
    for idx, (target_name, target_label) in enumerate(FRACTION_FIGURE_TARGETS):
        ax.bar(
            x + (idx - 1.0) * width,
            ordered[f"{target_name}_test_spearman"].to_numpy(dtype=float),
            width=width,
            label=target_label,
            color=colors[idx],
            hatch=hatches[idx],
            edgecolor="black",
            linewidth=1.8,
            zorder=3,
        )
    ax.set_ylim(0, 1)
    ax.set_ylabel("Fraction regression Spearman", fontsize=22, labelpad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(
        [MODEL_DISPLAY_NAMES.get(model, model) for model in model_order],
        rotation=90,
        fontsize=15,
    )
    ax.xaxis.tick_top()
    ax.tick_params(axis="x", labeltop=True, labelbottom=False, pad=4)
    ax.tick_params(axis="x", length=0)
    ax.tick_params(axis="y", labelsize=16, width=1.8, length=7, color="#555555")
    ax.grid(axis="y", color="#d8d2d2", linewidth=1.0, alpha=0.75, zorder=1)
    ax.grid(axis="x", color="#d8d2d2", linewidth=0.8, alpha=0.45, zorder=1)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#4a4a4a")
    ax.spines["bottom"].set_color("#4a4a4a")
    ax.spines["left"].set_linewidth(1.8)
    ax.spines["bottom"].set_linewidth(1.8)
    ax.legend(
        frameon=False,
        ncol=3,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.12),
        fontsize=18,
        handlelength=1.8,
        columnspacing=2.8,
    )

    transform = ax.get_xaxis_transform()
    for start, end, _, group_name, roman in spans:
        center = (start + end) / 2
        ax.plot(
            [start + 0.18, end - 0.18],
            [1.42, 1.42],
            transform=transform,
            color="#6f6f6f",
            linewidth=1.2,
            clip_on=False,
        )
        ax.text(
            center,
            1.48,
            group_name,
            transform=transform,
            ha="center",
            va="bottom",
            fontsize=17,
            fontweight="bold",
            linespacing=0.9,
            clip_on=False,
        )
        ax.text(
            center,
            1.68,
            roman,
            transform=transform,
            ha="center",
            va="center",
            fontsize=15,
            fontweight="bold",
            bbox={
                "boxstyle": "circle,pad=0.35",
                "facecolor": "white",
                "edgecolor": "#777777",
                "linewidth": 1.2,
            },
            clip_on=False,
        )
    fig.savefig(fig_dir / "fraction_regression_spearman_public19_2x.png", dpi=220)
    plt.close(fig)


def roman_numeral(value: int) -> str:
    numerals = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
    return numerals[value]


def write_summary(out_dir: Path, labels: pd.DataFrame, results: pd.DataFrame) -> None:
    ranked = results[results["status"] == "ok"].copy()
    metric_cols = [f"{name}_test_spearman" for name, _ in TARGETS]
    if not ranked.empty:
        ranked["mean_test_spearman"] = ranked[metric_cols].mean(axis=1)
        ranked = ranked.sort_values("mean_test_spearman", ascending=False)
    lines = [
        "# Wuhan 2x T2 Fraction Regression",
        "",
        "- Scope: current 2x public-19 Wuhan window",
        "- Embeddings: existing local `downstream_core_2x/embeddings_2x_tile/*.npz`",
        "- No GEE fetch, no model re-export, no encoder inference",
        f"- Tiles: `{len(labels)}` total; split counts `{labels['split'].value_counts().to_dict()}`",
        "- Targets: built, vegetation, cropland, water fractions from ESA WorldCover 2021",
        "- Head: ridge regression with alpha selected on the validation split",
        "",
        "## Ranked Results",
        "",
        ranked.to_markdown(index=False) if not ranked.empty else "No successful model rows.",
        "",
        "## Artifacts",
        "",
        "- Metrics CSV: `fraction_regression.csv`",
        "- Ranked CSV: `fraction_regression_ranked.csv`",
        "- Per-model predictions: `fraction_regression_predictions_{model}.csv`",
        "- Per-model parity plots: `figures/fraction_regression_scatter_{model}.png`",
        "- Accuracy figure: `figures/fraction_regression_spearman_public19_2x.png`",
    ]
    (out_dir / "fraction_regression.md").write_text("\n".join(lines))


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    labels = load_labels(args.labels)
    labels.to_csv(args.out_dir / "downstream_labels_500m_2x_fraction.csv", index=False)
    labels[["tile_id", "row", "col", "split", "use_for_t2"]].to_csv(
        args.out_dir / "downstream_splits_500m_2x_fraction.csv",
        index=False,
    )
    models = available_models(args.embedding_dir, args.models)
    rows: list[dict[str, Any]] = []
    for model in models:
        try:
            embeddings = load_embeddings(args.embedding_dir / f"{model}.npz", labels)
            metrics, preds = fit_model(embeddings, labels)
            preds.insert(0, "model", model)
            preds.to_csv(args.out_dir / f"fraction_regression_predictions_{model}.csv", index=False)
            write_scatter(args.out_dir, model, preds)
            rows.append({"model": model, "status": "ok", "dim": int(embeddings.shape[1]), **metrics})
            print(
                f"[{model}] mean_rho="
                f"{np.mean([metrics[f'{name}_test_spearman'] for name, _ in TARGETS]):.3f}"
            )
        except Exception as exc:
            rows.append({"model": model, "status": "failed", "error": repr(exc)})
            print(f"[{model}] failed: {exc!r}")

    results = pd.DataFrame(rows)
    results.to_csv(args.out_dir / "fraction_regression.csv", index=False)
    (args.out_dir / "fraction_regression.json").write_text(
        results.to_json(orient="records", indent=2)
    )
    ranked = results[results["status"] == "ok"].copy()
    if not ranked.empty:
        ranked["mean_test_spearman"] = ranked[[f"{name}_test_spearman" for name, _ in TARGETS]].mean(axis=1)
        ranked = ranked.sort_values("mean_test_spearman", ascending=False)
    ranked.to_csv(args.out_dir / "fraction_regression_ranked.csv", index=False)
    write_metric_figure(args.out_dir, results)
    write_summary(args.out_dir, labels, results)


if __name__ == "__main__":
    main()
