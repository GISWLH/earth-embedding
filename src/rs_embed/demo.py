"""Small, real, checksummed datasets and CPU teaching workflows.

Install ``.[demo]`` for plotting, linear probes, and the guided notebooks.
These helpers complement the extraction API; they are not a benchmark framework.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass
class DemoData:
    """Features aligned to ``samples.tile_id``; coordinates use WGS84 lon/lat."""

    samples: pd.DataFrame
    features: np.ndarray
    metadata: dict


def align_samples(samples, ids, features):
    """Strict one-to-one ID join. Reject duplicates, missing IDs and nonfinite data."""
    ids = np.asarray(ids).astype(str)
    x = np.asarray(features)
    if "tile_id" not in samples or samples.tile_id.isna().any():
        raise ValueError("samples requires nonmissing tile_id values.")
    keys = samples.tile_id.astype(str)
    if ids.ndim != 1 or x.ndim != 2 or len(ids) != len(x) or x.shape[1] == 0:
        raise ValueError("Expected feature IDs (N,) and features (N,D).")
    if keys.duplicated().any() or len(set(ids)) != len(ids):
        raise ValueError("Duplicate tile_id; a one-to-one join is required.")
    if set(keys) != set(ids):
        raise ValueError("Sample and feature tile_id sets differ; no silent row dropping.")
    if not np.isfinite(x).all():
        raise ValueError("Features contain nonfinite values.")
    positions = pd.Series(np.arange(len(ids)), index=ids)
    return x[positions.loc[keys].to_numpy()].copy()


def load_demo(name="wuhan"):
    """Load bundled real AEF or Wuhan data, verifying every payload SHA-256.

    No credentials, network, model download or private paths are required.
    ``aef`` is a 64 x 64 point sample; ``wuhan`` is 567 historical pooled tiles.
    """
    if name not in {"wuhan", "aef"}:
        raise ValueError("Unknown demo. Choose 'wuhan' or 'aef'.")
    root = files("rs_embed").joinpath("data", "demos", name)
    meta = json.loads(root.joinpath("manifest.json").read_text(encoding="utf-8"))
    import io

    payloads = {}
    for filename, expected in meta["files"].items():
        raw = root.joinpath(filename).read_bytes()
        if hashlib.sha256(raw).hexdigest() != expected["sha256"]:
            raise ValueError(f"SHA-256 mismatch for demo {name}/{filename}; reinstall the package.")
        payloads[filename] = raw
    samples = pd.read_csv(io.BytesIO(payloads["samples.csv"]), dtype={"tile_id": str})
    with np.load(io.BytesIO(payloads["features.npz"]), allow_pickle=False) as archive:
        x = align_samples(samples, archive["tile_id"], archive["features"])
    return DemoData(samples, x, meta)


def fetch_aef_demo(cache_dir=".earth-embedding-cache", *, offline=False):
    """Re-sample the bundled AEF coordinates from the official COG, once.

    The resulting NPZ is pinned to the bundled sample SHA-256. HTTP range reads
    avoid downloading a global index or whole COG. Requires ``.[aef]`` and
    network on the first call; failures never fall back to synthetic data.
    """
    from .aef import sample_aef

    data = load_demo("aef")
    folder = Path(cache_dir)
    target = folder / "aef-wuhan-2021.npy"
    expected = data.metadata["array_sha256"]
    if target.exists():
        x = np.load(target, allow_pickle=False)
        if x.shape != data.features.shape or hashlib.sha256(x.tobytes()).hexdigest() != expected:
            raise ValueError("AEF cache SHA-256 mismatch; remove the corrupt cache and retry.")
    else:
        if offline:
            raise FileNotFoundError(
                "AEF cache missing. Run fetch_aef_demo online once or load_demo('aef')."
            )
        try:
            x = sample_aef(
                data.samples[["center_lon", "center_lat"]].to_numpy(),
                tiles=data.metadata["tiles"],
            ).data
        except Exception as exc:
            raise RuntimeError(
                "Official AEF download failed. Check network; load_demo('aef') works offline."
            ) from exc
        if hashlib.sha256(x.tobytes()).hexdigest() != expected:
            raise ValueError(
                "Official AEF sample changed; expected pinned 2021 values. Cache not written."
            )
        folder.mkdir(parents=True, exist_ok=True)
        import tempfile

        with tempfile.NamedTemporaryFile(dir=folder, suffix=".npy", delete=False) as stream:
            staging = Path(stream.name)
            np.save(stream, x, allow_pickle=False)
        try:
            staging.replace(target)
        finally:
            staging.unlink(missing_ok=True)
    data.features = x
    return data


def pca_colors(features):
    """RGB from three descriptive PCs, each stretched between its 2/98 percentiles.

    Fitted to the displayed area only. Colors are not classes and must not be
    compared across separately fitted maps. Not used by the classification path.
    """
    from sklearn.decomposition import PCA

    x = np.asarray(features)
    if x.ndim != 2 or min(x.shape) < 3 or not np.isfinite(x).all():
        raise ValueError("PCA colors need finite (N,D) features with N,D >= 3.")
    scores = PCA(n_components=3, svd_solver="full").fit_transform(x)
    low, high = np.percentile(scores, [2, 98], axis=0)
    return np.clip((scores - low) / np.maximum(high - low, 1e-12), 0, 1)


def plot_map(samples, colors, *, title="Embedding PCA (not land-cover classes)", ax=None):
    """Draw real WGS84 cell bounds, north up; return a Matplotlib Figure."""
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection
    from matplotlib.ticker import MaxNLocator

    required = ["minlon", "minlat", "maxlon", "maxlat"]
    if not set(required).issubset(samples):
        raise ValueError(f"Map samples require {required}.")
    bounds = samples[required].to_numpy(float)
    if not len(bounds) or not np.isfinite(bounds).all() or (bounds[:, 2:] <= bounds[:, :2]).any():
        raise ValueError("Map bounds must be finite with west < east and south < north.")
    if len(colors) != len(samples):
        raise ValueError("One color is required per sample, in aligned tile_id order.")
    if ax is None:
        _, ax = plt.subplots(figsize=(6.2, 5.6), layout="constrained")
    polygons = [[(w, s), (e, s), (e, n), (w, n)] for w, s, e, n in bounds]
    ax.add_collection(PolyCollection(polygons, facecolors=colors, edgecolors="none"))
    ax.set_xlim(bounds[:, 0].min(), bounds[:, 2].max())
    ax.set_ylim(bounds[:, 1].min(), bounds[:, 3].max())
    ax.set_aspect(1 / np.cos(np.deg2rad(bounds[:, [1, 3]].mean())))
    ax.set(xlabel="Longitude (E)", ylabel="Latitude (N)", title=title)
    ax.ticklabel_format(useOffset=False)
    ax.xaxis.set_major_locator(MaxNLocator(5))
    ax.yaxis.set_major_locator(MaxNLocator(5))
    return ax.figure


CLASS_COLORS = {
    "built": "#d95f02",
    "vegetation": "#1b9e77",
    "cropland": "#e6ab02",
    "water": "#1f78b4",
}


def classify_demo(data=None):
    """Fixed east-train / west-test Wuhan probe with a two-column buffer.

    Excludes five rare cropland tiles (three-class teaching scope). No tuning,
    random splits, test fitting or train predictions masquerading as evaluation.
    """
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix, f1_score
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    data = load_demo("wuhan") if data is None else data
    table = data.samples.copy()
    needed = {"tile_id", "col", "row", "class_name", "minlon", "maxlon"}
    if not needed.issubset(table) or len(table) != len(data.features):
        raise ValueError("Wuhan classification requires aligned tile_id, row, col and class_name.")
    if table[list(needed)].isna().any().any() or table.tile_id.duplicated().any():
        raise ValueError("Classification metadata has missing values or duplicate IDs.")
    if table[["row", "col"]].duplicated().any():
        raise ValueError("Duplicate spatial cells are not allowed.")
    classes = ["built", "vegetation", "water"]
    eligible = table.class_name.isin(classes)
    table["demo_split"] = np.where(
        table.col <= 22, "test", np.where(table.col >= 25, "train", "buffer")
    )
    table.loc[~eligible, "demo_split"] = "excluded_rare_class"
    train = table.demo_split.eq("train").to_numpy()
    test = table.demo_split.eq("test").to_numpy()
    if not train.any() or not test.any() or set(table.loc[train, "class_name"]) != set(classes):
        raise ValueError(
            "Fixed Wuhan split needs nonempty train/test and all three training classes."
        )
    if table.loc[train, "minlon"].min() <= table.loc[test, "maxlon"].max():
        raise ValueError(
            "Spatial leakage: east training bounds must be separated from west test bounds."
        )
    x = np.asarray(data.features)
    if x.ndim != 2 or not np.isfinite(x).all():
        raise ValueError("Classification features must be a finite (N,D) array.")
    model = make_pipeline(
        StandardScaler(), LogisticRegression(C=1.0, max_iter=2000, random_state=42)
    )
    model.fit(x[train], table.loc[train, "class_name"])
    predicted = model.predict(x[test])
    truth = table.loc[test, "class_name"]
    table["prediction"] = pd.Series(pd.NA, index=table.index, dtype="string")
    table.loc[test, "prediction"] = predicted
    metrics = {
        "scope": "Historical Wuhan software demonstration, three classes; not global benchmark reproduction",
        "seed": 42,
        "model": "AEF 2021 historical mean-pooled features",
        "total": len(table),
        "split_counts": table.demo_split.value_counts().to_dict(),
        "class_counts": pd.crosstab(table.demo_split, table.class_name).to_dict(orient="index"),
        "split": "East col >=25 train; west col <=22 test; cols 23,24 buffer; exclude 5 cropland tiles",
        "classes": classes,
        "oa": float(accuracy_score(truth, predicted)),
        "macro_f1": float(
            f1_score(truth, predicted, labels=classes, average="macro", zero_division=0)
        ),
        "balanced_accuracy": float(balanced_accuracy_score(truth, predicted)),
        "confusion_matrix": confusion_matrix(truth, predicted, labels=classes).tolist(),
    }
    return {"metrics": metrics, "samples": table, "estimator": model}


def plot_classification(result):
    """Reference, held-out predictions, errors and confusion matrix; no train scores."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    from sklearn.metrics import ConfusionMatrixDisplay

    table = result["samples"]
    test = table.demo_split.eq("test")
    fig, axes = plt.subplots(2, 2, figsize=(11, 9), layout="constrained")
    plot_map(
        table,
        table.class_name.map(CLASS_COLORS),
        title="WorldCover 2021 reference (567 tiles)",
        ax=axes[0, 0],
    )
    plot_map(
        table,
        table.prediction.map(CLASS_COLORS).fillna("#e8e8e8"),
        title="AEF + logistic regression: west test only",
        ax=axes[0, 1],
    )
    error_colors = np.full(len(table), "#e8e8e8", dtype=object)
    error_colors[test] = np.where(
        table.loc[test, "class_name"].to_numpy() == table.loc[test, "prediction"].to_numpy(),
        "#267b72",
        "#bd3d45",
    )
    plot_map(table, error_colors, title="Held-out errors (red); correct (teal)", ax=axes[1, 0])
    for ax in axes.flat[:3]:
        for col in [23, 25]:
            ax.axvline(table.loc[table.col == col, "minlon"].min(), color="#173f40", ls="--", lw=1)
    axes[0, 0].legend(
        handles=[Patch(color=v, label=k) for k, v in CLASS_COLORS.items()],
        fontsize=8,
        loc="upper left",
    )
    axes[0, 1].legend(
        handles=[Patch(color="#e8e8e8", label="Train / buffer / excluded (unscored)")], fontsize=8
    )
    metrics = result["metrics"]
    ConfusionMatrixDisplay(
        np.array(metrics["confusion_matrix"]), display_labels=metrics["classes"]
    ).plot(ax=axes[1, 1], colorbar=False, cmap="Blues")
    axes[1, 1].set_title(
        f"Test n={int(test.sum())} | OA {metrics['oa']:.3f} | Macro-F1 {metrics['macro_f1']:.3f}"
    )
    return fig
