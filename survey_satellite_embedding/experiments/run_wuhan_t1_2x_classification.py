from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from run_wuhan_t1_classification import (
    CLASS_TO_INDEX,
    CLASSES,
    TrainConfig,
    evaluate_knn,
    train_probe_head,
    write_predictions,
)

ROOT = Path(__file__).resolve().parent
DEFAULT_DATA_DIR = ROOT.parent / "data" / "part2_20260502_full" / "region_a"
DEFAULT_MAP_DIR = ROOT / "results" / "part2_model_map_figure"
DEFAULT_OUT_DIR = ROOT / "results" / "downstream_core_2x"

CLASS_COLORS = {
    "built": "#d95f02",
    "vegetation": "#1b9e77",
    "cropland": "#e6ab02",
    "water": "#1f78b4",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run T1 land-cover classification on the current Wuhan 2x public-19 window."
    )
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--map-dir", type=Path, default=DEFAULT_MAP_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--models", nargs="+", default=None)
    parser.add_argument("--head", choices=["linear", "mlp"], default="linear")
    parser.add_argument("--epochs", type=int, default=200)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--patience", type=int, default=30)
    parser.add_argument("--hidden-dim", type=int, default=128)
    parser.add_argument("--dropout", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--train-device", default="cuda")
    parser.add_argument(
        "--plots-only",
        action="store_true",
        help="Regenerate acceptance plots from existing predictions/metrics without retraining.",
    )
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_2x_manifest(map_dir: Path) -> dict[str, Any]:
    manifest_path = map_dir / "manifest_2x.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing 2x manifest: {manifest_path}")
    return read_json(manifest_path)


def available_models(manifest: dict[str, Any], requested: list[str] | None) -> list[str]:
    models = [m["model"] for m in manifest.get("models", []) if m.get("status") == "ok"]
    if requested is None:
        return models
    missing = sorted(set(requested) - set(models))
    if missing:
        raise ValueError(f"Requested models not present in successful 2x manifest: {missing}")
    return requested


def load_labels(data_dir: Path, coverage: list[float], seed: int) -> pd.DataFrame:
    manifest_path = data_dir / "tile_manifest_500m.csv"
    df = pd.read_csv(manifest_path).sort_values(["row", "col"]).reset_index(drop=True)
    minlon, minlat, maxlon, maxlat = [float(v) for v in coverage]
    subset = df[
        (df["center_lon"].between(minlon, maxlon))
        & (df["center_lat"].between(minlat, maxlat))
    ].copy()
    if subset.empty:
        raise ValueError("No 500 m manifest tiles fall inside the 2x coverage.")
    subset["class_name"] = subset["local_dominant_class"].astype(str)
    subset["class_index"] = subset["class_name"].map(CLASS_TO_INDEX).astype(int)
    subset["use_for_t1"] = True
    subset["split"] = stratified_split(subset, seed=seed)
    return subset.reset_index(drop=True)


def stratified_split(labels: pd.DataFrame, *, seed: int) -> pd.Series:
    rng = np.random.default_rng(seed)
    split = pd.Series("train", index=labels.index, dtype=object)
    for class_name in CLASSES:
        idx = labels.index[labels["class_name"] == class_name].to_numpy()
        rng.shuffle(idx)
        n = len(idx)
        if n == 0:
            continue
        if n >= 5:
            n_test = max(1, int(round(0.2 * n)))
            n_val = max(1, int(round(0.2 * n)))
        elif n >= 3:
            n_test = 1
            n_val = 1
        elif n == 2:
            n_test = 1
            n_val = 0
        else:
            n_test = 0
            n_val = 0
        split.loc[idx[:n_test]] = "test"
        split.loc[idx[n_test : n_test + n_val]] = "val"
    return split


def write_label_artifacts(labels: pd.DataFrame, out_dir: Path, coverage: list[float]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    cols = [
        "tile_id",
        "row",
        "col",
        "center_lon",
        "center_lat",
        "minlon",
        "minlat",
        "maxlon",
        "maxlat",
        "split",
        "class_name",
        "class_index",
        "use_for_t1",
        "local_dominant_frac",
        "local_built_frac",
        "local_vegetation_frac",
        "local_cropland_frac",
        "local_water_frac",
        "jrc_occurrence_mean",
        "jrc_water_binary_frac",
    ]
    labels[cols].to_csv(out_dir / "downstream_labels_500m_2x.csv", index=False)
    labels[["tile_id", "row", "col", "split", "use_for_t1"]].to_csv(
        out_dir / "downstream_splits_500m_2x.csv", index=False
    )
    summary = {
        "coverage": coverage,
        "n_tiles": int(len(labels)),
        "classes": CLASSES,
        "class_counts": labels["class_name"].value_counts().to_dict(),
        "split_counts": {
            split: labels.loc[labels["split"] == split, "class_name"].value_counts().to_dict()
            for split in ["train", "val", "test"]
        },
    }
    (out_dir / "downstream_labels_summary_2x.json").write_text(json.dumps(summary, indent=2))


def normalize_grid(embedding: np.ndarray) -> np.ndarray:
    arr = np.asarray(embedding, dtype=np.float32)
    if arr.ndim != 3:
        raise ValueError(f"Expected a 3D embedding grid, got {arr.shape}")
    if arr.shape[0] <= arr.shape[-1] or arr.shape[0] >= 16:
        return arr
    return np.moveaxis(arr, -1, 0)


def feature_at_tile(grid: np.ndarray, bbox: np.ndarray, tile: Any) -> np.ndarray:
    channels, height, width = grid.shape
    minlon, minlat, maxlon, maxlat = [float(v) for v in bbox]
    lon_values = minlon + (np.arange(width, dtype=np.float32) + 0.5) * (maxlon - minlon) / width
    lat_values = maxlat - (np.arange(height, dtype=np.float32) + 0.5) * (maxlat - minlat) / height
    col_mask = (lon_values >= float(tile.minlon)) & (lon_values <= float(tile.maxlon))
    row_mask = (lat_values >= float(tile.minlat)) & (lat_values <= float(tile.maxlat))
    if col_mask.any() and row_mask.any():
        patch = grid[:, row_mask, :][:, :, col_mask]
        return np.nanmean(patch.reshape(channels, -1), axis=1).astype(np.float32)

    lon = float(tile.center_lon)
    lat = float(tile.center_lat)
    col = int(np.clip(np.searchsorted(lon_values, lon), 0, width - 1))
    row = int(np.clip(np.searchsorted(-lat_values, -lat), 0, height - 1))
    return grid[:, row, col].astype(np.float32)


def load_model_tile_embeddings(map_dir: Path, model: str, labels: pd.DataFrame) -> np.ndarray:
    block_dir = map_dir / "blocks_2x" / model
    block_paths = sorted(block_dir.glob("block_*.npz"))
    if not block_paths:
        raise FileNotFoundError(f"No 2x block embeddings found for {model}: {block_dir}")

    blocks: list[dict[str, Any]] = []
    for path in block_paths:
        with np.load(path, allow_pickle=True) as payload:
            blocks.append(
                {
                    "path": path,
                    "bbox": np.asarray(payload["bbox"], dtype=np.float64),
                    "grid": normalize_grid(payload["embedding"]),
                }
            )

    features: list[np.ndarray] = []
    for tile in labels.itertuples():
        center_lon = float(tile.center_lon)
        center_lat = float(tile.center_lat)
        containing = [
            block
            for block in blocks
            if block["bbox"][0] <= center_lon <= block["bbox"][2]
            and block["bbox"][1] <= center_lat <= block["bbox"][3]
        ]
        if not containing:
            raise ValueError(f"No block covers tile {tile.tile_id} for model {model}")
        features.append(feature_at_tile(containing[0]["grid"], containing[0]["bbox"], tile))
    return np.stack(features, axis=0).astype(np.float32)


def prediction_table(labels: pd.DataFrame, model: str, predictions_csv: Path) -> pd.DataFrame:
    preds = pd.read_csv(predictions_csv)
    pred_by_tile = preds.set_index("tile_id")["pred_class"]
    out = labels.copy()
    out["model"] = model
    out["pred_class"] = out["tile_id"].map(pred_by_tile)
    return out


def class_to_rgba(values: pd.Series) -> np.ndarray:
    import matplotlib.colors as mcolors

    colors = [CLASS_COLORS.get(str(v), "#dddddd") for v in values]
    return np.asarray([mcolors.to_rgba(c) for c in colors], dtype=np.float32)


def render_tile_grid(ax: Any, labels: pd.DataFrame, column: str, title: str) -> None:
    rows = sorted(labels["row"].unique())
    cols = sorted(labels["col"].unique())
    row_to_idx = {row: idx for idx, row in enumerate(rows)}
    col_to_idx = {col: idx for idx, col in enumerate(cols)}
    image = np.ones((len(rows), len(cols), 4), dtype=np.float32)
    image[..., :3] = 0.94
    for item in labels.itertuples():
        value = getattr(item, column)
        image[row_to_idx[item.row], col_to_idx[item.col]] = class_to_rgba(pd.Series([value]))[0]
    ax.imshow(image, interpolation="nearest")
    ax.set_title(title, fontsize=9)
    ax.set_xticks([])
    ax.set_yticks([])


def add_class_legend(fig: Any, *, loc: str = "lower center", ncol: int | None = None) -> None:
    handles = [
        plt.Line2D(
            [0],
            [0],
            marker="s",
            color="w",
            label=class_name,
            markerfacecolor=color,
            markersize=9,
        )
        for class_name, color in CLASS_COLORS.items()
    ]
    fig.legend(handles=handles, loc=loc, ncol=ncol or len(CLASSES), frameon=False)


def write_classification_maps(out_dir: Path, labels: pd.DataFrame, models: list[str]) -> None:
    figures_dir = out_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    for model in models:
        pred_path = out_dir / f"classification_predictions_{model}.csv"
        if not pred_path.exists():
            continue
        table = prediction_table(labels, model, pred_path)
        fig, axes = plt.subplots(1, 2, figsize=(8, 4), constrained_layout=True)
        render_tile_grid(axes[0], table, "class_name", "WorldCover truth")
        render_tile_grid(axes[1], table, "pred_class", f"{model} prediction")
        fig.savefig(figures_dir / f"classification_map_{model}.png", dpi=180)
        plt.close(fig)

    ok_models = [m for m in models if (out_dir / f"classification_predictions_{m}.csv").exists()]
    panels = [("truth", labels, "class_name")] + [
        (model, prediction_table(labels, model, out_dir / f"classification_predictions_{model}.csv"), "pred_class")
        for model in ok_models
    ]
    ncols = 5
    nrows = int(math.ceil(len(panels) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(3.0 * ncols, 3.0 * nrows), constrained_layout=True)
    axes_arr = np.asarray(axes).reshape(-1)
    for ax, (title, table, column) in zip(axes_arr, panels, strict=False):
        render_tile_grid(ax, table, column, title)
    for ax in axes_arr[len(panels) :]:
        ax.axis("off")
    add_class_legend(fig)
    fig.savefig(figures_dir / "classification_maps_public19_2x.png", dpi=180)
    plt.close(fig)


def write_reference_style_classification_figure(
    out_dir: Path,
    labels: pd.DataFrame,
    models: list[str],
    result_df: pd.DataFrame,
) -> None:
    figures_dir = out_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    metrics = result_df.set_index("model")
    fig, axes = plt.subplots(4, 5, figsize=(18, 14), constrained_layout=True)
    axes_flat = list(axes.flat)

    render_tile_grid(axes_flat[0], labels, "class_name", "WorldCover truth\n500 m T1 labels")
    for ax, model in zip(axes_flat[1:], models, strict=True):
        pred_path = out_dir / f"classification_predictions_{model}.csv"
        if not pred_path.exists():
            ax.axis("off")
            ax.text(0.03, 0.92, model, fontsize=11, fontweight="bold", va="top")
            ax.text(0.03, 0.72, "missing predictions", fontsize=10, va="top")
            continue
        table = prediction_table(labels, model, pred_path)
        macro_f1 = float(metrics.loc[model, "test_macro_f1"])
        accuracy = float(metrics.loc[model, "test_accuracy"])
        title = f"{model}\nF1 {macro_f1:.3f} | Acc {accuracy:.3f}"
        render_tile_grid(ax, table, "pred_class", title)

    fig.suptitle(
        "WorldCover truth + 19 model T1 classification maps, 2x2 expansion of block_r01_c01\n"
        "Panels use the same Wuhan 2x window as part2_original_map_with_public19_models_2x.png.",
        fontsize=15,
        y=1.06,
    )
    add_class_legend(fig, loc="lower center")
    fig.savefig(figures_dir / "classification_public19_models_2x_reference_layout.png", dpi=220)
    plt.close(fig)


def write_accuracy_barplot(out_dir: Path, result_df: pd.DataFrame) -> None:
    figures_dir = out_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    ok = result_df[result_df["status"] == "ok"].set_index("model")
    family_groups = [
        (
            "I",
            "Precomputed\nproducts",
            ["gse", "tessera", "copernicus"],
            "#f3edf5",
        ),
        (
            "II",
            "Masked\nautoencoder\n/ vision",
            ["satmae", "satmaepp", "satmaepp_s2_10b", "scalemae"],
            "#f7eef0",
        ),
        (
            "III",
            "Vision-language\n/\ncross-modal",
            ["remoteclip", "wildsat"],
            "#eef3f8",
        ),
        (
            "IV",
            "Multimodal\ngeneralists",
            ["anysat", "galileo", "prithvi", "terrafm", "terramind", "dofa"],
            "#eef5ef",
        ),
        (
            "V",
            "Domain-specialized\nencoders",
            ["agrifm", "fomo", "thor", "satvision"],
            "#f7f1e8",
        ),
    ]
    display_names = {
        "gse": "GSE",
        "tessera": "TESSERA",
        "copernicus": "Copernicus",
        "remoteclip": "RemoteCLIP",
        "satmae": "SatMAE",
        "satmaepp": "SatMAE++",
        "satmaepp_s2_10b": "S2-10B",
        "scalemae": "ScaleMAE",
        "anysat": "AnySat",
        "galileo": "Galileo",
        "wildsat": "WildSAT",
        "prithvi": "Prithvi",
        "terrafm": "TerraFM",
        "terramind": "TerraMind",
        "dofa": "DOFA",
        "fomo": "FoMo",
        "thor": "THOR",
        "agrifm": "AgriFM",
        "satvision": "SatVision",
    }

    font_scale = 1.8
    extra_header_pt = 4.0
    scale_font = lambda pt: pt * font_scale
    plot_params = {
        "font.family": "Arial",
        "font.size": scale_font(13),
        "axes.spines.left": True,
        "axes.spines.bottom": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": "#454545",
        "axes.linewidth": 2.2,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.major.size": 8,
        "ytick.major.size": 8,
        "xtick.major.width": 2.0,
        "ytick.major.width": 2.0,
        "xtick.color": "#454545",
        "ytick.color": "#454545",
        "savefig.bbox": "tight",
        "savefig.transparent": False,
    }
    old_params = plt.rcParams.copy()
    plt.rcParams.update(plot_params)
    try:
        fig, ax = plt.subplots(figsize=(22.0, 14.0))
        positions: list[float] = []
        ordered_models: list[str] = []
        family_spans: list[tuple[str, str, float, float, str]] = []
        cursor = 0.0
        family_gap = 0.9
        for family_id, family_name, models, shade in family_groups:
            present = [model for model in models if model in ok.index]
            if not present:
                continue
            start = cursor
            for model in present:
                positions.append(cursor)
                ordered_models.append(model)
                cursor += 1.0
            end = cursor - 1.0
            family_spans.append((family_id, family_name, start, end, shade))
            cursor += family_gap

        if not ordered_models:
            raise ValueError("No successful classification rows available for plotting.")

        x = np.asarray(positions, dtype=float)
        ordered = ok.loc[ordered_models]
        width = 0.22
        metrics = [
            ("test_macro_f1", "Macro F1", "#FFB2B2", ""),
            ("test_balanced_accuracy", "Balanced Acc", "#FFF2D0", "|"),
            ("test_accuracy", "Accuracy", "#FFFBF1", "\\"),
        ]

        for _, _, start, end, shade in family_spans:
            ax.axvspan(start - 0.5, end + 0.5, color=shade, alpha=0.72, zorder=0)

        for xpos in x:
            ax.vlines(xpos, 0, 1.0, color="#d7d0d0", linewidth=0.8, zorder=1)
        for _, _, start, _, _ in family_spans[1:]:
            ax.vlines(start - 0.5, 0, 1.0, color="#bfb7b7", linewidth=1.4, zorder=2)

        for idx, (column, label, color, hatch) in enumerate(metrics):
            ax.bar(
                x + (idx - 1) * width * 1.08,
                ordered[column].to_numpy(dtype=float),
                width=width,
                label=label,
                color=color,
                edgecolor="black",
                linewidth=2,
                hatch=hatch,
                zorder=4,
            )

        ax.set_xlim(x.min() - 0.75, x.max() + 0.75)
        ax.set_ylim(0, 1.0)
        ax.set_yticks(np.linspace(0, 1.0, 6))
        ax.set_ylabel("Classification score", fontsize=scale_font(15), labelpad=12)
        ax.set_xticks([])
        ax.grid(axis="y", color="#d9d1d1", linewidth=0.8, alpha=0.9, zorder=1)

        transform = ax.get_xaxis_transform()
        for xpos, model in zip(x, ordered_models, strict=True):
            ax.text(
                xpos,
                1.012,
                display_names.get(model, model),
                rotation=90,
                ha="center",
                va="bottom",
                fontsize=scale_font(8.5) + extra_header_pt,
                clip_on=False,
                transform=transform,
            )

        for family_id, family_name, start, end, _ in family_spans:
            center = (start + end) / 2
            ax.plot(
                [start - 0.42, end + 0.42],
                [1.42, 1.42],
                color="#676767",
                linewidth=1.2,
                clip_on=False,
                transform=transform,
            )
            ax.text(
                center,
                1.68,
                family_id,
                ha="center",
                va="center",
                fontsize=scale_font(9.5) + extra_header_pt,
                fontweight="bold",
                bbox={
                    "boxstyle": "circle,pad=0.35",
                    "facecolor": "white",
                    "edgecolor": "#676767",
                    "linewidth": 1.2,
                },
                clip_on=False,
                transform=transform,
            )
            ax.text(
                center,
                1.52,
                family_name,
                ha="center",
                va="center",
                fontsize=scale_font(9.2) + extra_header_pt,
                fontweight="bold",
                linespacing=0.95,
                clip_on=False,
                transform=transform,
            )

        ax.legend(
            loc="lower center",
            bbox_to_anchor=(0.5, -0.27),
            ncol=3,
            fontsize=scale_font(13),
            frameon=False,
            handlelength=1.9,
            columnspacing=2.0,
        )
        fig.subplots_adjust(left=0.085, right=0.99, bottom=0.20, top=0.52)
        fig.savefig(figures_dir / "classification_accuracy_barplot_public19_2x.png", dpi=600)
        plt.close(fig)
    finally:
        plt.rcParams.update(old_params)


def write_acceptance_figures(out_dir: Path, labels: pd.DataFrame, models: list[str]) -> None:
    result_path = out_dir / "classification.csv"
    if not result_path.exists():
        raise FileNotFoundError(f"Missing metrics CSV for acceptance plots: {result_path}")
    result_df = pd.read_csv(result_path)
    ok_models = [
        model
        for model in models
        if model in set(result_df.loc[result_df["status"] == "ok", "model"])
        and (out_dir / f"classification_predictions_{model}.csv").exists()
    ]
    if len(ok_models) != 19:
        raise ValueError(f"Expected 19 models with predictions, found {len(ok_models)}")
    write_reference_style_classification_figure(out_dir, labels, ok_models, result_df)
    write_accuracy_barplot(out_dir, result_df)


def write_2x_summary_markdown(out_dir: Path, result_df: pd.DataFrame, labels: pd.DataFrame) -> None:
    ranked = result_df[result_df["status"] == "ok"].sort_values(
        "test_macro_f1", ascending=False
    )
    lines = [
        "# Wuhan 2x T1 Land-Cover Classification",
        "",
        "- Dataset: current Wuhan 2x public-19 window from `manifest_2x.json`",
        f"- Tiles: `{len(labels)}` 500 m tiles from the WorldCover-derived manifest",
        "- Ground truth: `local_dominant_class` aggregated from ESA WorldCover 2021",
        "- Classes: `built`, `vegetation`, `cropland`, `water`",
        "- Split: fixed stratified random split shared by all models; this keeps the rare cropland class in train/val/test",
        "- Caveat: cropland has only 5 tiles in this 2x window, so macro F1 is intentionally strict but has high variance for that class",
        "",
        "## Class Balance",
        "",
        labels.groupby(["split", "class_name"]).size().unstack(fill_value=0).to_markdown(),
        "",
        "## Ranked Test Results",
        "",
        ranked.to_markdown(index=False),
        "",
        "## All Rows",
        "",
        result_df.to_markdown(index=False),
        "",
        "## Main Artifacts",
        "",
        "- Metrics CSV: `classification.csv`",
        "- Per-model predictions: `classification_predictions_{model}.csv`",
        "- Combined map: `figures/classification_maps_public19_2x.png`",
        "- Reference-layout acceptance map: `figures/classification_public19_models_2x_reference_layout.png`",
        "- Accuracy barplot: `figures/classification_accuracy_barplot_public19_2x.png`",
        "- Per-model maps: `figures/classification_map_{model}.png`",
    ]
    (out_dir / "classification.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    manifest = load_2x_manifest(args.map_dir)
    coverage = [float(v) for v in manifest["coverage"]]
    models = available_models(manifest, args.models)
    labels = load_labels(args.data_dir, coverage, seed=args.seed)
    write_label_artifacts(labels, args.out_dir, coverage)

    if args.plots_only:
        write_acceptance_figures(args.out_dir, labels, models)
        return

    config = TrainConfig(
        head=args.head,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        weight_decay=args.weight_decay,
        patience=args.patience,
        hidden_dim=args.hidden_dim,
        dropout=args.dropout,
        seed=args.seed,
        device=args.train_device,
    )

    embedding_dir = args.out_dir / "embeddings_2x_tile"
    embedding_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    ok_models: list[str] = []
    for model in models:
        try:
            embeddings = load_model_tile_embeddings(args.map_dir, model, labels)
            np.savez_compressed(
                embedding_dir / f"{model}.npz",
                embeddings=embeddings,
                tile_id=labels["tile_id"].astype(str).to_numpy(dtype="U"),
                model=np.asarray(model),
            )
            metrics, predictions = train_probe_head(embeddings, labels, config)
            knn_metrics = evaluate_knn(embeddings, labels, k=5)
            write_predictions(args.out_dir, model=model, predictions=predictions)
            (args.out_dir / f"classification_{model}.json").write_text(
                json.dumps({"model": model, **metrics, "knn": knn_metrics}, indent=2)
            )
            rows.append(
                {
                    "model": model,
                    "status": "ok",
                    "head": args.head,
                    "dim": int(metrics["input_dim"]),
                    "best_epoch": int(metrics["best_epoch"]),
                    "train_macro_f1": metrics["train"]["macro_f1"],
                    "val_macro_f1": metrics["val"]["macro_f1"],
                    "test_macro_f1": metrics["test"]["macro_f1"],
                    "test_balanced_accuracy": metrics["test"]["balanced_accuracy"],
                    "test_accuracy": metrics["test"]["accuracy"],
                    "knn5_test_macro_f1": knn_metrics["test"]["macro_f1"],
                    "knn5_test_balanced_accuracy": knn_metrics["test"]["balanced_accuracy"],
                }
            )
            ok_models.append(model)
            print(f"[{model}] test_macro_f1={metrics['test']['macro_f1']:.3f}")
        except Exception as exc:
            rows.append({"model": model, "status": "failed", "error": repr(exc)})
            print(f"[{model}] failed: {exc!r}")

    result_df = pd.DataFrame(rows)
    result_df.to_csv(args.out_dir / "classification.csv", index=False)
    result_df[result_df["status"] == "ok"].sort_values("test_macro_f1", ascending=False).to_csv(
        args.out_dir / "classification_ranked.csv", index=False
    )
    (args.out_dir / "classification.json").write_text(result_df.to_json(orient="records", indent=2))
    write_2x_summary_markdown(args.out_dir, result_df, labels)
    write_classification_maps(args.out_dir, labels, ok_models)
    write_acceptance_figures(args.out_dir, labels, ok_models)


if __name__ == "__main__":
    main()
