"""Wuhan T2 fraction regression runner."""

# ruff: noqa: E402, I001

from __future__ import annotations

import argparse
import json
import math
import sys
import time
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

from rs_embed import OutputSpec, TemporalSpec, get_embeddings_batch, list_models

from survey_satellite_embedding.experiments.run_wuhan_t1_classification import (
    as_pooled_vector,
    assign_spatial_splits,
    chunked,
    embedding_path_for_model,
    load_embeddings,
    load_manifest,
    set_local_asset_env,
    spatial_rows,
)

ROOT = Path(__file__).resolve().parent
DEFAULT_DATA_DIR = ROOT.parent / "data" / "part2_20260502_full" / "region_a"
DEFAULT_OUT_DIR = ROOT / "results" / "downstream_fraction"
DEFAULT_EMBEDDING_DIR = DEFAULT_OUT_DIR / "embeddings_full_roi"

TARGETS = [
    ("built", "local_built_frac"),
    ("vegetation", "local_vegetation_frac"),
    ("cropland", "local_cropland_frac"),
    ("water", "local_water_frac"),
]
ALPHA_GRID = [0.01, 0.1, 1.0, 10.0, 100.0]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run Wuhan T2 tile-level land-cover fraction regression over the single-ROI "
            "500 m benchmark manifest."
        )
    )
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--embedding-dir", type=Path, default=DEFAULT_EMBEDDING_DIR)
    parser.add_argument("--models", nargs="+", default=["gse"])
    parser.add_argument("--all-models", action="store_true")
    parser.add_argument("--export-missing", action="store_true")
    parser.add_argument("--export-chunk-size", type=int, default=8)
    parser.add_argument("--inference-device", default="cuda")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def build_fraction_labels(df: pd.DataFrame) -> pd.DataFrame:
    labels = df.copy()
    labels["split"] = assign_spatial_splits(labels)
    labels["use_for_t2"] = np.all(
        np.isfinite(
            labels[[target_col for _, target_col in TARGETS]].to_numpy(dtype=np.float32)
        ),
        axis=1,
    )
    return labels


def write_label_artifacts(labels: pd.DataFrame, out_dir: Path) -> None:
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
        "use_for_t2",
        "local_dominant_class",
        "local_dominant_frac",
        "local_built_frac",
        "local_vegetation_frac",
        "local_cropland_frac",
        "local_water_frac",
        "jrc_occurrence_mean",
        "jrc_water_binary_frac",
    ]
    labels[cols].to_csv(out_dir / "downstream_labels_500m_fraction.csv", index=False)
    labels[["tile_id", "row", "col", "split", "use_for_t2"]].to_csv(
        out_dir / "downstream_splits_500m_fraction.csv", index=False
    )
    summary = {
        "n_tiles": int(len(labels)),
        "n_usable_t2": int(labels["use_for_t2"].sum()),
        "split_counts": {
            split: int((labels["split"] == split).sum()) for split in ["train", "val", "test"]
        },
        "target_means": {
            name: float(labels[col].mean()) for name, col in TARGETS if col in labels.columns
        },
    }
    (out_dir / "downstream_labels_summary_fraction.json").write_text(
        json.dumps(summary, indent=2)
    )


def temporal_for_model(model: str) -> TemporalSpec:
    if model in {"gse", "copernicus", "tessera"}:
        return TemporalSpec.year(2021 if model != "tessera" else 2024)
    return TemporalSpec.range("2021-05-01", "2021-10-31")


def export_model_embeddings_fraction(
    *,
    model: str,
    labels: pd.DataFrame,
    out_path: Path,
    chunk_size: int,
    device: str,
) -> dict[str, Any]:
    set_local_asset_env(model)
    spatials = spatial_rows(labels)
    temporal = temporal_for_model(model)
    embeddings: list[np.ndarray] = []
    peak_gpu_mb = 0.0
    t0 = time.perf_counter()

    import torch

    for spatial_chunk in chunked(spatials, chunk_size):
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.reset_peak_memory_stats()
        batch = get_embeddings_batch(
            model,
            spatials=spatial_chunk,
            temporal=temporal,
            output=OutputSpec.pooled(),
            backend="auto",
            device=device,
        )
        if torch.cuda.is_available():
            peak_gpu_mb = max(peak_gpu_mb, torch.cuda.max_memory_allocated() / (1024**2))
        embeddings.extend(as_pooled_vector(emb.data) for emb in batch)

    matrix = np.stack(embeddings, axis=0).astype(np.float32)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        out_path,
        embeddings=matrix,
        tile_id=labels["tile_id"].astype(str).to_numpy(dtype="U"),
        model=np.asarray(model),
    )
    elapsed_s = time.perf_counter() - t0
    return {
        "model": model,
        "embedding_path": str(out_path),
        "elapsed_s": round(elapsed_s, 3),
        "per_tile_s": round(elapsed_s / len(labels), 4),
        "peak_gpu_mb": round(peak_gpu_mb, 2),
        "dim": int(matrix.shape[1]),
    }


def select_alpha(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_val: np.ndarray,
    y_val: np.ndarray,
) -> tuple[float, dict[str, float]]:
    best_alpha = ALPHA_GRID[0]
    best_rmse = math.inf
    best_metrics = {
        "mae": math.nan,
        "rmse": math.nan,
        "r2": math.nan,
        "spearman": math.nan,
    }
    for alpha in ALPHA_GRID:
        reg = Ridge(alpha=alpha)
        reg.fit(x_train, y_train)
        pred = reg.predict(x_val)
        metrics = compute_regression_metrics(y_val, pred)
        if metrics["rmse"] < best_rmse:
            best_alpha = alpha
            best_rmse = metrics["rmse"]
            best_metrics = metrics
    return best_alpha, best_metrics


def compute_regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    y_true = np.asarray(y_true, dtype=np.float32)
    y_pred = np.asarray(y_pred, dtype=np.float32)
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "r2": float(r2_score(y_true, y_pred)),
        "spearman": float(spearmanr(y_true, y_pred).statistic),
    }


def fit_regression_heads(
    embeddings: np.ndarray,
    labels: pd.DataFrame,
    *,
    seed: int,
) -> tuple[dict[str, Any], dict[str, np.ndarray]]:
    np.random.seed(seed)
    usable = labels["use_for_t2"].to_numpy(dtype=bool) & np.all(np.isfinite(embeddings), axis=1)
    split = labels["split"].to_numpy()
    if not usable.any():
        raise ValueError("No usable samples available for T2.")

    masks = {name: usable & (split == name) for name in ["train", "val", "test"]}
    if not masks["train"].any() or not masks["val"].any() or not masks["test"].any():
        raise ValueError("Train/val/test split must all contain usable T2 samples.")

    scaler = StandardScaler().fit(embeddings[masks["train"]])
    x_train = scaler.transform(embeddings[masks["train"]]).astype(np.float32)
    x_val = scaler.transform(embeddings[masks["val"]]).astype(np.float32)
    x_test = scaler.transform(embeddings[masks["test"]]).astype(np.float32)

    metrics: dict[str, Any] = {
        "split_counts": {
            name: int(masks[name].sum()) for name in ["train", "val", "test"]
        }
    }
    predictions: dict[str, np.ndarray] = {}

    for target_name, target_col in TARGETS:
        y_train = labels.loc[masks["train"], target_col].to_numpy(dtype=np.float32)
        y_val = labels.loc[masks["val"], target_col].to_numpy(dtype=np.float32)
        y_test = labels.loc[masks["test"], target_col].to_numpy(dtype=np.float32)

        best_alpha, val_metrics = select_alpha(x_train, y_train, x_val, y_val)
        x_trainval = np.concatenate([x_train, x_val], axis=0)
        y_trainval = np.concatenate([y_train, y_val], axis=0)
        reg = Ridge(alpha=best_alpha)
        reg.fit(x_trainval, y_trainval)

        train_pred = reg.predict(x_train)
        val_pred = reg.predict(x_val)
        test_pred = reg.predict(x_test)

        train_metrics = compute_regression_metrics(y_train, train_pred)
        test_metrics = compute_regression_metrics(y_test, test_pred)

        metrics[f"{target_name}_best_alpha"] = float(best_alpha)
        metrics[f"{target_name}_val_mae"] = val_metrics["mae"]
        metrics[f"{target_name}_val_rmse"] = val_metrics["rmse"]
        metrics[f"{target_name}_val_r2"] = val_metrics["r2"]
        metrics[f"{target_name}_val_spearman"] = val_metrics["spearman"]
        metrics[f"{target_name}_train_mae"] = train_metrics["mae"]
        metrics[f"{target_name}_train_rmse"] = train_metrics["rmse"]
        metrics[f"{target_name}_train_r2"] = train_metrics["r2"]
        metrics[f"{target_name}_train_spearman"] = train_metrics["spearman"]
        metrics[f"{target_name}_test_mae"] = test_metrics["mae"]
        metrics[f"{target_name}_test_rmse"] = test_metrics["rmse"]
        metrics[f"{target_name}_test_r2"] = test_metrics["r2"]
        metrics[f"{target_name}_test_spearman"] = test_metrics["spearman"]

        predictions[f"{target_name}_train_pred"] = train_pred
        predictions[f"{target_name}_val_pred"] = val_pred
        predictions[f"{target_name}_test_pred"] = test_pred
        predictions[f"{target_name}_train_true"] = y_train
        predictions[f"{target_name}_val_true"] = y_val
        predictions[f"{target_name}_test_true"] = y_test

    predictions["train_tile_id"] = labels.loc[masks["train"], "tile_id"].astype(str).to_numpy()
    predictions["val_tile_id"] = labels.loc[masks["val"], "tile_id"].astype(str).to_numpy()
    predictions["test_tile_id"] = labels.loc[masks["test"], "tile_id"].astype(str).to_numpy()
    return metrics, predictions


def write_predictions(out_dir: Path, *, model: str, predictions: dict[str, np.ndarray]) -> None:
    rows: list[dict[str, Any]] = []
    for split in ["train", "val", "test"]:
        tile_ids = predictions[f"{split}_tile_id"]
        row_count = len(tile_ids)
        for i in range(row_count):
            row: dict[str, Any] = {
                "model": model,
                "split": split,
                "tile_id": str(tile_ids[i]),
            }
            for target_name, _ in TARGETS:
                row[f"true_{target_name}"] = float(predictions[f"{target_name}_{split}_true"][i])
                row[f"pred_{target_name}"] = float(predictions[f"{target_name}_{split}_pred"][i])
            rows.append(row)
    pd.DataFrame(rows).to_csv(out_dir / f"regression_predictions_{model}.csv", index=False)


def write_scatter_figure(out_dir: Path, *, model: str, predictions: dict[str, np.ndarray]) -> None:
    figures_dir = out_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(10, 9), constrained_layout=True)
    axes_flat = list(np.asarray(axes).reshape(-1))
    for ax, (target_name, _) in zip(axes_flat, TARGETS, strict=True):
        y_true = predictions[f"{target_name}_test_true"]
        y_pred = predictions[f"{target_name}_test_pred"]
        metrics = compute_regression_metrics(y_true, y_pred)
        ax.scatter(y_true, y_pred, s=12, alpha=0.7, color="#4472c4")
        lo = float(min(np.min(y_true), np.min(y_pred)))
        hi = float(max(np.max(y_true), np.max(y_pred)))
        pad = max(0.01, 0.05 * max(hi - lo, 1e-6))
        lo -= pad
        hi += pad
        ax.plot([lo, hi], [lo, hi], color="#444444", linewidth=1.1)
        ax.set_title(
            f"{target_name}\nRMSE {metrics['rmse']:.3f} | Spearman {metrics['spearman']:.3f}",
            fontsize=10,
        )
        ax.set_xlabel("True")
        ax.set_ylabel("Pred")
        ax.set_xlim(lo, hi)
        ax.set_ylim(lo, hi)
        ax.grid(alpha=0.25)
    fig.suptitle(f"{model} Wuhan T2 test-set parity plots", fontsize=13)
    fig.savefig(figures_dir / f"regression_scatter_{model}.png", dpi=200)
    plt.close(fig)


def write_metric_barplot(out_dir: Path, result_df: pd.DataFrame) -> None:
    figures_dir = out_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    ok = result_df[result_df["status"] == "ok"].copy()
    if ok.empty:
        return

    family_groups = [
        ("I", "Precomputed", ["gse", "tessera", "copernicus"], "#f3edf5"),
        ("II", "MAE / vision", ["satmae", "satmaepp", "satmaepp_s2_10b", "scalemae"], "#f7eef0"),
        ("III", "Vision-language", ["remoteclip", "wildsat"], "#eef3f8"),
        (
            "IV",
            "Multimodal",
            ["anysat", "galileo", "prithvi", "terrafm", "terramind", "dofa"],
            "#eef5ef",
        ),
        ("V", "Domain", ["agrifm", "fomo", "thor", "satvision"], "#f7f1e8"),
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
    target_metric_cols = [f"{target}_test_spearman" for target, _ in TARGETS]
    ordered = ok.assign(mean_spearman=ok[target_metric_cols].mean(axis=1)).sort_values(
        "mean_spearman",
        ascending=False,
    )
    models = ordered["model"].tolist()

    plot_params = {
        "font.family": "Arial",
        "font.size": 12,
        "axes.spines.left": True,
        "axes.spines.bottom": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "savefig.bbox": "tight",
    }
    old_params = plt.rcParams.copy()
    plt.rcParams.update(plot_params)
    try:
        fig, ax = plt.subplots(figsize=(19.2, 8.0))
        positions: list[float] = []
        ordered_models: list[str] = []
        family_spans: list[tuple[str, str, float, float, str]] = []
        cursor = 0.0
        family_gap = 0.9
        for family_id, family_name, family_models, shade in family_groups:
            present = [model for model in family_models if model in models]
            if not present:
                continue
            start = cursor
            for model in present:
                positions.append(cursor)
                ordered_models.append(model)
                cursor += 1.0
            family_spans.append((family_id, family_name, start, cursor - 1.0, shade))
            cursor += family_gap

        x = np.asarray(positions, dtype=float)
        ordered_df = ordered.set_index("model").loc[ordered_models]
        width = 0.16
        colors = ["#73A5CA", "#FEFDDF", "#FFC81E", "#8ecae6"]

        for _, _, start, end, shade in family_spans:
            ax.axvspan(start - 0.5, end + 0.5, color=shade, alpha=0.65, zorder=0)
        for xpos in x:
            ax.vlines(xpos, 0, 1.0, color="#d7d0d0", linewidth=0.8, zorder=1)
        for _, _, start, _, _ in family_spans[1:]:
            ax.vlines(start - 0.5, 0, 1.0, color="#bfb7b7", linewidth=1.2, zorder=2)

        for idx, (target_name, _) in enumerate(TARGETS):
            ax.bar(
                x + (idx - 1.5) * width,
                ordered_df[f"{target_name}_test_spearman"].to_numpy(dtype=float),
                width=width,
                color=colors[idx],
                edgecolor="black",
                linewidth=1.4,
                label=f"{target_name} spearman",
                zorder=4,
            )

        ax.set_ylim(0, 1.0)
        ax.set_ylabel("Test Spearman rho", fontsize=14)
        ax.set_xticks([])
        ax.grid(axis="y", color="#d9d1d1", linewidth=0.8, alpha=0.9, zorder=1)

        transform = ax.get_xaxis_transform()
        for xpos, model in zip(x, ordered_models, strict=True):
            ax.text(
                xpos,
                1.01,
                display_names.get(model, model),
                rotation=90,
                ha="center",
                va="bottom",
                fontsize=8.2,
                clip_on=False,
                transform=transform,
            )
        for family_id, _family_name, start, end, _ in family_spans:
            center = (start + end) / 2
            ax.text(
                center,
                1.12,
                family_id,
                ha="center",
                va="center",
                fontsize=9.5,
                fontweight="bold",
                bbox={
                    "boxstyle": "circle,pad=0.3",
                    "facecolor": "white",
                    "edgecolor": "#676767",
                    "linewidth": 1.0,
                },
                clip_on=False,
                transform=transform,
            )
        ax.legend(frameon=False, ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.18))
        fig.savefig(figures_dir / "regression_spearman_barplot_public19.png", dpi=220)
        plt.close(fig)
    finally:
        plt.rcParams.update(old_params)


def write_summary_markdown(out_dir: Path, result_df: pd.DataFrame, labels: pd.DataFrame) -> None:
    lines = [
        "# Wuhan T2 Fraction Regression",
        "",
        "- Dataset: single high-resolution Wuhan ROI, 500 m tile grid",
        f"- Tiles: `{len(labels)}` total, `{int(labels['use_for_t2'].sum())}` used for T2",
        "- Targets: built, vegetation, cropland, water fraction",
        "- Split: fixed row-contiguous spatial split; rows 0-23 train, 24-31 val, 32-40 test",
        "",
        "## Split Counts",
        "",
        labels.groupby(["split"]).size().to_frame("count").to_markdown(),
        "",
        "## Results",
        "",
        result_df.to_markdown(index=False),
        "",
    ]
    (out_dir / "fraction_regression.md").write_text("\n".join(lines))


def main() -> None:
    args = parse_args()
    models = list_models() if args.all_models else args.models
    args.out_dir.mkdir(parents=True, exist_ok=True)
    args.embedding_dir.mkdir(parents=True, exist_ok=True)

    manifest = load_manifest(args.data_dir)
    labels = build_fraction_labels(manifest)
    write_label_artifacts(labels, args.out_dir)

    rows: list[dict[str, Any]] = []
    export_records: list[dict[str, Any]] = []
    for model in models:
        emb_path = embedding_path_for_model(args.embedding_dir, model)
        if not emb_path.exists():
            if not args.export_missing:
                rows.append(
                    {
                        "model": model,
                        "status": "missing_embeddings",
                        "embedding_path": str(emb_path),
                    }
                )
                continue
            export_records.append(
                export_model_embeddings_fraction(
                    model=model,
                    labels=labels,
                    out_path=emb_path,
                    chunk_size=args.export_chunk_size,
                    device=args.inference_device,
                )
            )

        try:
            embeddings = load_embeddings(emb_path, labels)
            metrics, predictions = fit_regression_heads(embeddings, labels, seed=args.seed)
            write_predictions(args.out_dir, model=model, predictions=predictions)
            write_scatter_figure(args.out_dir, model=model, predictions=predictions)
            rows.append(
                {
                    "model": model,
                    "status": "ok",
                    "embedding_path": str(emb_path),
                    "dim": int(embeddings.shape[1]),
                    **metrics,
                }
            )
            print(
                f"[{model}] built_rmse={metrics['built_test_rmse']:.3f} "
                f"water_spearman={metrics['water_test_spearman']:.3f}"
            )
        except Exception as exc:
            rows.append(
                {
                    "model": model,
                    "status": "failed",
                    "embedding_path": str(emb_path),
                    "error": repr(exc),
                }
            )
            print(f"[{model}] failed: {exc!r}")

    result_df = pd.DataFrame(rows)
    result_df.to_csv(args.out_dir / "fraction_regression.csv", index=False)
    (args.out_dir / "fraction_regression.json").write_text(
        result_df.to_json(orient="records", indent=2)
    )
    if export_records:
        (args.out_dir / "embedding_export_summary.json").write_text(
            json.dumps(export_records, indent=2)
        )
    write_metric_barplot(args.out_dir, result_df)
    write_summary_markdown(args.out_dir, result_df, labels)


if __name__ == "__main__":
    main()
