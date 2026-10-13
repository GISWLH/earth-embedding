"""Compare saved embeddings on one matched cohort with a fixed spatial holdout.

NPZ files contain X (N,D) and sample_id (N,) without pickled objects.
Metadata CSV contains sample_id,target,split,spatial_group. Both train and test
must be present and their spatial groups must be disjoint. An externally
specified split can represent global regions or separated blocks within Wuhan.
This example does not reproduce manuscript scores or choose a winning model.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


def align_cohort(metadata: pd.DataFrame, features: dict[str, tuple[np.ndarray, np.ndarray]]):
    """Align every model by sample ID and retain exactly the same finite cohort."""
    required = {"sample_id", "target", "split", "spatial_group"}
    if not required.issubset(metadata):
        raise ValueError(f"Metadata requires columns: {sorted(required)}")
    table = metadata.copy()
    if table[list(required)].isna().any().any():
        raise ValueError("Metadata IDs, targets, splits and groups cannot be missing.")
    table["sample_id"] = table["sample_id"].astype(str)
    if table.sample_id.duplicated().any():
        raise ValueError("Metadata sample_id values must be unique.")
    if not features:
        raise ValueError("Supply at least one feature file.")
    common = set(table.sample_id)
    indexed = {}
    for name, (ids, array) in features.items():
        ids, array = np.asarray(ids).astype(str), np.asarray(array)
        if ids.ndim != 1 or array.ndim != 2 or len(ids) != len(array) or array.shape[1] == 0:
            raise ValueError(f"{name}: expected sample_id (N,) and X (N,D).")
        if len(set(ids)) != len(ids):
            raise ValueError(f"{name}: duplicate sample IDs.")
        valid = np.isfinite(array).all(axis=1)
        indexed[name] = pd.DataFrame(array[valid], index=ids[valid])
        common &= set(ids[valid])
    cohort = table[table.sample_id.isin(common)].reset_index(drop=True)
    if set(cohort.split) != {"train", "test"}:
        raise ValueError("The matched cohort must contain train and test rows only.")
    train = cohort.split.eq("train").to_numpy()
    overlap = set(cohort.loc[train, "spatial_group"]) & set(cohort.loc[~train, "spatial_group"])
    if overlap:
        raise ValueError(
            f"Spatial leakage: groups appear in train and test: {sorted(overlap, key=str)[:5]}"
        )
    arrays = {name: frame.loc[cohort.sample_id].to_numpy() for name, frame in indexed.items()}
    return cohort, arrays


def evaluate(metadata, features, *, task):
    from sklearn.linear_model import LogisticRegression, Ridge
    from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, mean_squared_error
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    cohort, arrays = align_cohort(metadata, features)
    train = cohort.split.eq("train").to_numpy()
    target = cohort.target.to_numpy()
    if task == "regression":
        target = target.astype(float)
        if not np.isfinite(target).all():
            raise ValueError("Regression targets must be finite.")
    elif task == "classification":
        if len(set(target[train])) < 2:
            raise ValueError("Classification training data requires at least two classes.")
        unknown = set(target[~train]) - set(target[train])
        if unknown:
            raise ValueError(f"Test-only classes cannot be learned: {unknown}")
    else:
        raise ValueError("task must be classification or regression.")
    rows = []
    for name, array in arrays.items():
        estimator = (
            LogisticRegression(max_iter=2000, random_state=42)
            if task == "classification"
            else Ridge(alpha=1.0)
        )
        # Both scaling and fitting see training rows only.
        model = make_pipeline(StandardScaler(), estimator)
        model.fit(array[train], target[train])
        predictions = model.predict(array[~train])
        metrics = (
            {
                "accuracy": accuracy_score(target[~train], predictions),
                "macro_f1": f1_score(target[~train], predictions, average="macro", zero_division=0),
            }
            if task == "classification"
            else {
                "mae": mean_absolute_error(target[~train], predictions),
                "rmse": float(np.sqrt(mean_squared_error(target[~train], predictions))),
            }
        )
        rows.append({"model": name, "dimensions": array.shape[1], **metrics})
    return {
        "task": task,
        "metadata_rows": len(metadata),
        "matched_rows": len(cohort),
        "excluded_rows": len(metadata) - len(cohort),
        "train_rows": int(train.sum()),
        "test_rows": int((~train).sum()),
        "sample_ids": cohort.sample_id.tolist(),
        "cohort_sha256": hashlib.sha256(cohort.to_csv(index=False).encode()).hexdigest(),
        "results": rows,
        "scope": "Example fixed-split linear probe; not manuscript benchmark reproduction.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", required=True, type=Path)
    parser.add_argument("--features", nargs="+", required=True, help="model_name=features.npz")
    parser.add_argument("--task", choices=["classification", "regression"], required=True)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    features, sources = {}, {}
    for item in args.features:
        name, path = item.split("=", 1)
        if name in features:
            parser.error(f"Duplicate model name: {name}")
        with np.load(path, allow_pickle=False) as data:
            features[name] = (data["sample_id"].copy(), data["X"].copy())
        sources[name] = {
            "file": Path(path).name,
            "sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest(),
        }
    metadata = pd.read_csv(args.metadata, dtype={"sample_id": str})
    report = evaluate(metadata, features, task=args.task)
    report["sources"] = sources
    report["metadata_sha256"] = hashlib.sha256(args.metadata.read_bytes()).hexdigest()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "sample_ids"}, indent=2))


if __name__ == "__main__":
    main()
