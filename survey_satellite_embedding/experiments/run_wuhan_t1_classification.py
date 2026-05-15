from __future__ import annotations

import argparse
import json
import math
import os
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from rs_embed import OutputSpec, TemporalSpec, get_embeddings_batch, list_models
from rs_embed.core.specs import BBox

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
DEFAULT_DATA_DIR = ROOT.parent / "data" / "part2_20260502_full" / "region_a"
DEFAULT_OUT_DIR = ROOT / "results" / "downstream_core"
DEFAULT_EMBEDDING_DIR = DEFAULT_OUT_DIR / "embeddings_full_roi"

CLASSES = ["built", "vegetation", "cropland", "water"]
CLASS_TO_INDEX = {name: idx for idx, name in enumerate(CLASSES)}
YEAR_MODELS = {"gse": 2021, "copernicus": 2021, "tessera": 2024}


@dataclass(frozen=True)
class TrainConfig:
    head: str
    epochs: int
    batch_size: int
    lr: float
    weight_decay: float
    patience: int
    hidden_dim: int
    dropout: float
    seed: int
    device: str


class Standardizer:
    def __init__(self) -> None:
        self.mean: np.ndarray | None = None
        self.std: np.ndarray | None = None

    def fit(self, x: np.ndarray) -> Standardizer:
        self.mean = np.nanmean(x, axis=0, keepdims=True).astype(np.float32)
        std = np.nanstd(x, axis=0, keepdims=True).astype(np.float32)
        self.std = np.where(std < 1e-6, 1.0, std).astype(np.float32)
        return self

    def transform(self, x: np.ndarray) -> np.ndarray:
        if self.mean is None or self.std is None:
            raise RuntimeError("Standardizer must be fit before transform.")
        return ((x - self.mean) / self.std).astype(np.float32)


class ProbeHead(nn.Module):
    def __init__(
        self,
        input_dim: int,
        num_classes: int,
        *,
        head: str,
        hidden_dim: int,
        dropout: float,
    ) -> None:
        super().__init__()
        if head == "linear":
            self.net = nn.Linear(input_dim, num_classes)
        elif head == "mlp":
            self.net = nn.Sequential(
                nn.Linear(input_dim, hidden_dim),
                nn.GELU(),
                nn.Dropout(dropout),
                nn.Linear(hidden_dim, num_classes),
            )
        else:
            raise ValueError(f"Unsupported head: {head!r}")

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run Wuhan T1 tile-level land-cover classification over the single-ROI "
            "500 m benchmark manifest."
        )
    )
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--embedding-dir", type=Path, default=DEFAULT_EMBEDDING_DIR)
    parser.add_argument("--models", nargs="+", default=["gse"])
    parser.add_argument("--all-models", action="store_true")
    parser.add_argument("--head", choices=["linear", "mlp"], default="linear")
    parser.add_argument("--confidence-threshold", type=float, default=0.0)
    parser.add_argument("--export-missing", action="store_true")
    parser.add_argument("--export-chunk-size", type=int, default=8)
    parser.add_argument("--inference-device", default="cuda")
    parser.add_argument("--train-device", default="cuda")
    parser.add_argument("--epochs", type=int, default=200)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--patience", type=int, default=30)
    parser.add_argument("--hidden-dim", type=int, default=128)
    parser.add_argument("--dropout", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--resume", action="store_true")
    return parser.parse_args()


def load_manifest(data_dir: Path) -> pd.DataFrame:
    manifest_path = data_dir / "tile_manifest_500m.csv"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing Wuhan tile manifest: {manifest_path}")
    df = pd.read_csv(manifest_path)
    required = {
        "tile_id",
        "row",
        "col",
        "minlon",
        "minlat",
        "maxlon",
        "maxlat",
        "center_lon",
        "center_lat",
        "local_dominant_class",
        "local_dominant_frac",
        "local_built_frac",
        "local_vegetation_frac",
        "local_cropland_frac",
        "local_water_frac",
        "jrc_occurrence_mean",
        "jrc_water_binary_frac",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Manifest is missing required columns: {missing}")
    return df.sort_values(["row", "col"]).reset_index(drop=True)


def assign_spatial_splits(df: pd.DataFrame) -> pd.Series:
    """Freeze a row-contiguous spatial split for the 41x53 Wuhan 500 m grid."""
    split = pd.Series("train", index=df.index, dtype=object)
    split[df["row"].between(24, 31)] = "val"
    split[df["row"].ge(32)] = "test"
    return split


def build_labels_and_splits(df: pd.DataFrame, confidence_threshold: float) -> pd.DataFrame:
    labels = df.copy()
    labels["split"] = assign_spatial_splits(labels)
    labels["class_name"] = labels["local_dominant_class"].astype(str)
    labels["class_index"] = labels["class_name"].map(CLASS_TO_INDEX)
    labels["use_for_t1"] = labels["class_index"].notna() & (
        labels["local_dominant_frac"].astype(float) >= confidence_threshold
    )
    if labels["class_index"].isna().any():
        unknown = sorted(labels.loc[labels["class_index"].isna(), "class_name"].unique())
        raise ValueError(f"Unknown local dominant classes: {unknown}")
    labels["class_index"] = labels["class_index"].astype(int)
    return labels


def validate_split_table(labels: pd.DataFrame) -> None:
    usable = labels[labels["use_for_t1"]]
    for split in ["train", "val", "test"]:
        counts = usable.loc[usable["split"] == split, "class_name"].value_counts().to_dict()
        missing = [cls for cls in CLASSES if counts.get(cls, 0) == 0]
        if missing:
            raise ValueError(f"{split} split has no samples for classes: {missing}")


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
    labels[cols].to_csv(out_dir / "downstream_labels_500m.csv", index=False)
    labels[["tile_id", "row", "col", "split", "use_for_t1"]].to_csv(
        out_dir / "downstream_splits_500m.csv", index=False
    )
    summary = {
        "n_tiles": int(len(labels)),
        "n_usable_t1": int(labels["use_for_t1"].sum()),
        "classes": CLASSES,
        "split_counts": {
            split: labels.loc[labels["split"] == split, "class_name"].value_counts().to_dict()
            for split in ["train", "val", "test"]
        },
        "usable_split_counts": {
            split: labels.loc[
                (labels["split"] == split) & labels["use_for_t1"], "class_name"
            ]
            .value_counts()
            .to_dict()
            for split in ["train", "val", "test"]
        },
    }
    (out_dir / "downstream_labels_summary.json").write_text(json.dumps(summary, indent=2))


def temporal_for_model(model: str) -> TemporalSpec:
    if model in YEAR_MODELS:
        return TemporalSpec.year(YEAR_MODELS[model])
    return TemporalSpec.range("2021-05-01", "2021-10-31")


def spatial_rows(df: pd.DataFrame) -> list[BBox]:
    return [
        BBox(
            minlon=float(row.minlon),
            minlat=float(row.minlat),
            maxlon=float(row.maxlon),
            maxlat=float(row.maxlat),
        )
        for row in df.itertuples()
    ]


def chunked(seq: list[Any], size: int):
    for start in range(0, len(seq), size):
        yield seq[start : start + size]


def as_pooled_vector(x: Any) -> np.ndarray:
    if hasattr(x, "values"):
        x = x.values
    arr = np.asarray(x, dtype=np.float32)
    if arr.ndim == 1:
        return arr
    if arr.ndim == 3:
        return arr.reshape(arr.shape[0], -1).mean(axis=1).astype(np.float32)
    return arr.reshape(-1).astype(np.float32)


def set_local_asset_env(model: str) -> None:
    if model == "satmaepp_s2_10b":
        os.environ.setdefault(
            "RS_EMBED_SATMAEPP_S2_CKPT_FILE",
            str(
                REPO_ROOT
                / "research_outputs"
                / "model_cache"
                / "checkpoint_ViT-L_pretrain_fmow_sentinel.pth"
            ),
        )
    elif model == "agrifm":
        os.environ.setdefault(
            "RS_EMBED_AGRIFM_CKPT", str(REPO_ROOT / "research_outputs" / "model_cache" / "AgriFM.pth")
        )
    elif model == "copernicus":
        os.environ.setdefault("RS_EMBED_COP_DIR", str(REPO_ROOT / "data" / "copernicus_embed"))
    elif model == "tessera":
        os.environ.setdefault(
            "RS_EMBED_TESSERA_CACHE",
            str(REPO_ROOT / "research_outputs" / "model_cache" / "geotessera_cache"),
        )


def embedding_path_for_model(embedding_dir: Path, model: str) -> Path:
    direct = embedding_dir / f"{model}.npz"
    prefixed = embedding_dir / f"embeddings_{model}.npz"
    if direct.exists():
        return direct
    return prefixed


def save_embeddings(path: Path, model: str, labels: pd.DataFrame, embeddings: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        path,
        embeddings=embeddings.astype(np.float32),
        tile_id=labels["tile_id"].astype(str).to_numpy(dtype="U"),
        model=np.asarray(model),
    )


def load_embeddings(path: Path, labels: pd.DataFrame) -> np.ndarray:
    payload = np.load(path, allow_pickle=True)
    if "embeddings" in payload:
        embeddings = np.asarray(payload["embeddings"], dtype=np.float32)
    else:
        keys = [k for k in payload.files if k.startswith("embeddings__")]
        if len(keys) != 1:
            raise ValueError(f"Could not identify embedding array in {path}; keys={payload.files}")
        embeddings = np.asarray(payload[keys[0]], dtype=np.float32)

    if "tile_id" in payload:
        tile_ids = payload["tile_id"].astype(str)
        expected = labels["tile_id"].astype(str).to_numpy()
        if list(tile_ids) != list(expected):
            order = {tile_id: idx for idx, tile_id in enumerate(tile_ids)}
            try:
                embeddings = embeddings[[order[tile_id] for tile_id in expected]]
            except KeyError as exc:
                raise ValueError(f"Embedding file {path} does not cover all manifest tile_ids.") from exc

    if embeddings.shape[0] != len(labels):
        raise ValueError(
            f"Embedding row count mismatch for {path}: {embeddings.shape[0]} != {len(labels)}"
        )
    if embeddings.ndim > 2:
        embeddings = embeddings.reshape(embeddings.shape[0], embeddings.shape[1], -1).mean(axis=2)
    return embeddings.astype(np.float32)


def export_model_embeddings(
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
    t0 = time.perf_counter()
    peak_gpu_mb = 0.0

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
    save_embeddings(out_path, model, labels, matrix)
    elapsed_s = time.perf_counter() - t0
    return {
        "model": model,
        "embedding_path": str(out_path),
        "elapsed_s": round(elapsed_s, 3),
        "per_tile_s": round(elapsed_s / len(labels), 4),
        "peak_gpu_mb": round(peak_gpu_mb, 2),
        "dim": int(matrix.shape[1]),
    }


def compute_classification_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    classes: list[str] = CLASSES,
) -> dict[str, Any]:
    y_true = np.asarray(y_true, dtype=int)
    y_pred = np.asarray(y_pred, dtype=int)
    num_classes = len(classes)
    confusion = np.zeros((num_classes, num_classes), dtype=int)
    for true_idx, pred_idx in zip(y_true, y_pred, strict=False):
        if 0 <= true_idx < num_classes and 0 <= pred_idx < num_classes:
            confusion[true_idx, pred_idx] += 1

    per_class: dict[str, dict[str, float]] = {}
    f1s: list[float] = []
    recalls: list[float] = []
    for idx, name in enumerate(classes):
        tp = float(confusion[idx, idx])
        fp = float(confusion[:, idx].sum() - confusion[idx, idx])
        fn = float(confusion[idx, :].sum() - confusion[idx, idx])
        support = int(confusion[idx, :].sum())
        precision = tp / (tp + fp) if tp + fp > 0 else 0.0
        recall = tp / (tp + fn) if tp + fn > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0.0
        per_class[name] = {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "support": support,
        }
        f1s.append(f1)
        recalls.append(recall)

    return {
        "accuracy": float(np.mean(y_true == y_pred)) if len(y_true) else math.nan,
        "macro_f1": float(np.mean(f1s)) if f1s else math.nan,
        "balanced_accuracy": float(np.mean(recalls)) if recalls else math.nan,
        "per_class": per_class,
        "confusion_matrix": confusion.tolist(),
    }


def make_loaders(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_val: np.ndarray,
    y_val: np.ndarray,
    *,
    batch_size: int,
) -> tuple[DataLoader, DataLoader]:
    train_ds = TensorDataset(torch.from_numpy(x_train), torch.from_numpy(y_train.astype(np.int64)))
    val_ds = TensorDataset(torch.from_numpy(x_val), torch.from_numpy(y_val.astype(np.int64)))
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)
    return train_loader, val_loader


def predict(model: nn.Module, x: np.ndarray, device: torch.device, batch_size: int) -> np.ndarray:
    model.eval()
    preds: list[np.ndarray] = []
    loader = DataLoader(TensorDataset(torch.from_numpy(x)), batch_size=batch_size, shuffle=False)
    with torch.no_grad():
        for (xb,) in loader:
            logits = model(xb.to(device))
            preds.append(logits.argmax(dim=1).cpu().numpy())
    return np.concatenate(preds, axis=0)


def train_probe_head(
    embeddings: np.ndarray,
    labels: pd.DataFrame,
    config: TrainConfig,
) -> tuple[dict[str, Any], dict[str, np.ndarray]]:
    torch.manual_seed(config.seed)
    np.random.seed(config.seed)

    usable = labels["use_for_t1"].to_numpy(dtype=bool) & np.all(np.isfinite(embeddings), axis=1)
    split = labels["split"].to_numpy()
    y_all = labels["class_index"].to_numpy(dtype=np.int64)

    masks = {
        name: usable & (split == name)
        for name in ["train", "val", "test"]
    }
    if not masks["train"].any() or not masks["val"].any() or not masks["test"].any():
        raise ValueError("Train/val/test split must all have usable samples.")

    scaler = Standardizer().fit(embeddings[masks["train"]])
    x_train = scaler.transform(embeddings[masks["train"]])
    x_val = scaler.transform(embeddings[masks["val"]])
    x_test = scaler.transform(embeddings[masks["test"]])
    y_train = y_all[masks["train"]]
    y_val = y_all[masks["val"]]
    y_test = y_all[masks["test"]]

    device = torch.device(config.device if torch.cuda.is_available() else "cpu")
    model = ProbeHead(
        input_dim=x_train.shape[1],
        num_classes=len(CLASSES),
        head=config.head,
        hidden_dim=config.hidden_dim,
        dropout=config.dropout,
    ).to(device)

    weights = class_weights(y_train).to(device)
    criterion = nn.CrossEntropyLoss(weight=weights)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.lr, weight_decay=config.weight_decay)
    train_loader, _ = make_loaders(
        x_train, y_train, x_val, y_val, batch_size=config.batch_size
    )

    best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
    best_val_macro_f1 = -1.0
    best_epoch = 0
    bad_epochs = 0
    history: list[dict[str, float | int]] = []

    for epoch in range(1, config.epochs + 1):
        model.train()
        losses: list[float] = []
        for xb, yb in train_loader:
            xb = xb.to(device)
            yb = yb.to(device)
            optimizer.zero_grad(set_to_none=True)
            loss = criterion(model(xb), yb)
            loss.backward()
            optimizer.step()
            losses.append(float(loss.detach().cpu()))

        val_pred = predict(model, x_val, device, config.batch_size)
        val_metrics = compute_classification_metrics(y_val, val_pred)
        val_macro_f1 = float(val_metrics["macro_f1"])
        history.append(
            {
                "epoch": epoch,
                "train_loss": float(np.mean(losses)) if losses else math.nan,
                "val_macro_f1": val_macro_f1,
                "val_balanced_accuracy": float(val_metrics["balanced_accuracy"]),
            }
        )
        if val_macro_f1 > best_val_macro_f1:
            best_val_macro_f1 = val_macro_f1
            best_epoch = epoch
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
            bad_epochs = 0
        else:
            bad_epochs += 1
            if bad_epochs >= config.patience:
                break

    model.load_state_dict(best_state)
    train_pred = predict(model, x_train, device, config.batch_size)
    val_pred = predict(model, x_val, device, config.batch_size)
    test_pred = predict(model, x_test, device, config.batch_size)

    metrics = {
        "head": config.head,
        "device": str(device),
        "input_dim": int(x_train.shape[1]),
        "best_epoch": int(best_epoch),
        "train": compute_classification_metrics(y_train, train_pred),
        "val": compute_classification_metrics(y_val, val_pred),
        "test": compute_classification_metrics(y_test, test_pred),
        "split_counts": {
            name: dict(Counter(labels.loc[masks[name], "class_name"]))
            for name in ["train", "val", "test"]
        },
        "history": history,
    }
    predictions = {
        "train": train_pred,
        "val": val_pred,
        "test": test_pred,
        "train_tile_id": labels.loc[masks["train"], "tile_id"].astype(str).to_numpy(),
        "val_tile_id": labels.loc[masks["val"], "tile_id"].astype(str).to_numpy(),
        "test_tile_id": labels.loc[masks["test"], "tile_id"].astype(str).to_numpy(),
        "train_true": y_train,
        "val_true": y_val,
        "test_true": y_test,
    }
    return metrics, predictions


def class_weights(y: np.ndarray) -> torch.Tensor:
    counts = np.bincount(y, minlength=len(CLASSES)).astype(np.float32)
    weights = counts.sum() / np.maximum(counts, 1.0)
    weights = weights / weights.mean()
    return torch.from_numpy(weights.astype(np.float32))


def knn_predict(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_eval: np.ndarray,
    *,
    k: int = 5,
) -> np.ndarray:
    k_eff = max(1, min(k, len(x_train)))
    preds: list[int] = []
    for x in x_eval:
        distances = np.sum((x_train - x) ** 2, axis=1)
        idx = np.argpartition(distances, k_eff - 1)[:k_eff]
        votes = np.bincount(y_train[idx], minlength=len(CLASSES))
        preds.append(int(np.argmax(votes)))
    return np.asarray(preds, dtype=np.int64)


def evaluate_knn(embeddings: np.ndarray, labels: pd.DataFrame, *, k: int = 5) -> dict[str, Any]:
    usable = labels["use_for_t1"].to_numpy(dtype=bool) & np.all(np.isfinite(embeddings), axis=1)
    split = labels["split"].to_numpy()
    y_all = labels["class_index"].to_numpy(dtype=np.int64)
    train_mask = usable & (split == "train")
    test_mask = usable & (split == "test")
    scaler = Standardizer().fit(embeddings[train_mask])
    x_train = scaler.transform(embeddings[train_mask])
    x_test = scaler.transform(embeddings[test_mask])
    y_train = y_all[train_mask]
    y_test = y_all[test_mask]
    pred = knn_predict(x_train, y_train, x_test, k=k)
    return {"k": k, "test": compute_classification_metrics(y_test, pred)}


def write_predictions(
    out_dir: Path,
    *,
    model: str,
    predictions: dict[str, np.ndarray],
) -> None:
    rows: list[dict[str, Any]] = []
    for split in ["train", "val", "test"]:
        for tile_id, y_true, y_pred in zip(
            predictions[f"{split}_tile_id"],
            predictions[f"{split}_true"],
            predictions[split],
            strict=True,
        ):
            rows.append(
                {
                    "model": model,
                    "split": split,
                    "tile_id": str(tile_id),
                    "true_class": CLASSES[int(y_true)],
                    "pred_class": CLASSES[int(y_pred)],
                    "true_index": int(y_true),
                    "pred_index": int(y_pred),
                }
            )
    pd.DataFrame(rows).to_csv(out_dir / f"classification_predictions_{model}.csv", index=False)


def write_summary_markdown(out_dir: Path, result_df: pd.DataFrame, labels: pd.DataFrame) -> None:
    lines = [
        "# Wuhan T1 Land-Cover Classification",
        "",
        "- Dataset: single high-resolution Wuhan ROI, 500 m tile grid",
        f"- Tiles: `{len(labels)}` total, `{int(labels['use_for_t1'].sum())}` used for T1",
        "- Classes: `built`, `vegetation`, `cropland`, `water`",
        "- Split: fixed row-contiguous spatial split; rows 0-23 train, 24-31 val, 32-40 test",
        "",
        "## Class Balance",
        "",
        labels.groupby(["split", "class_name"]).size().unstack(fill_value=0).to_markdown(),
        "",
        "## Results",
        "",
        result_df.to_markdown(index=False),
        "",
    ]
    (out_dir / "classification.md").write_text("\n".join(lines))


def main() -> None:
    args = parse_args()
    models = list_models() if args.all_models else args.models
    args.out_dir.mkdir(parents=True, exist_ok=True)
    args.embedding_dir.mkdir(parents=True, exist_ok=True)

    manifest = load_manifest(args.data_dir)
    labels = build_labels_and_splits(manifest, args.confidence_threshold)
    validate_split_table(labels)
    write_label_artifacts(labels, args.out_dir)

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
                        "head": args.head,
                    }
                )
                continue
            export_records.append(
                export_model_embeddings(
                    model=model,
                    labels=labels,
                    out_path=emb_path,
                    chunk_size=args.export_chunk_size,
                    device=args.inference_device,
                )
            )

        try:
            embeddings = load_embeddings(emb_path, labels)
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
                    "embedding_path": str(emb_path),
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
            print(
                f"[{model}] test_macro_f1={metrics['test']['macro_f1']:.3f} "
                f"test_bal_acc={metrics['test']['balanced_accuracy']:.3f}"
            )
        except Exception as exc:
            rows.append(
                {
                    "model": model,
                    "status": "failed",
                    "embedding_path": str(emb_path),
                    "head": args.head,
                    "error": repr(exc),
                }
            )
            print(f"[{model}] failed: {exc!r}")

    result_df = pd.DataFrame(rows)
    result_df.to_csv(args.out_dir / "classification.csv", index=False)
    (args.out_dir / "classification.json").write_text(
        result_df.to_json(orient="records", indent=2)
    )
    if export_records:
        (args.out_dir / "embedding_export_summary.json").write_text(
            json.dumps(export_records, indent=2)
        )
    write_summary_markdown(args.out_dir, result_df, labels)


if __name__ == "__main__":
    main()
