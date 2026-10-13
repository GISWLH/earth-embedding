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


def load_demo(name="bayarea"):
    """Load the real Bay Area sample, verifying every payload SHA-256.

    No credentials, network, model download or private paths are required.
    ``aef`` is an alias for ``bayarea``: 5933 official 1280 m AEF overview cells.
    """
    if name not in {"bayarea", "aef"}:
        raise ValueError("Unknown demo. Choose 'bayarea' (or alias 'aef').")
    root = files("rs_embed").joinpath("data", "demos", "bayarea")
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

    The resulting array is pinned to the bundled sample SHA-256. HTTP range reads
    avoid downloading a global index or whole COG. Requires ``.[aef]`` and
    network on the first call; failures never fall back to synthetic data.
    """
    from .aef import sample_aef

    data = load_demo("aef")
    folder = Path(cache_dir)
    target = folder / "aef-bayarea-2021.npy"
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
                overview_level=data.metadata["overview_level"],
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
    vertices = [item for i in range(4) for item in (f"lon{i}", f"lat{i}")]
    if set(vertices).intersection(samples):
        if not set(vertices).issubset(samples):
            raise ValueError("Cell polygons require all four lon0/lat0 through lon3/lat3 vertices.")
        polygons = samples[vertices].to_numpy(float).reshape(-1, 4, 2)
        if not np.isfinite(polygons).all():
            raise ValueError("Cell polygon vertices must be finite.")
    ax.add_collection(PolyCollection(polygons, facecolors=colors, edgecolors="none"))
    ax.set_xlim(bounds[:, 0].min(), bounds[:, 2].max())
    ax.set_ylim(bounds[:, 1].min(), bounds[:, 3].max())
    ax.set_aspect(1 / np.cos(np.deg2rad(bounds[:, [1, 3]].mean())))
    ax.set(xlabel="Longitude (degrees)", ylabel="Latitude (degrees)", title=title)
    ax.ticklabel_format(useOffset=False)
    ax.xaxis.set_major_locator(MaxNLocator(5))
    ax.yaxis.set_major_locator(MaxNLocator(5))
    return ax.figure


CLASS_COLORS = {
    "built": "#d95f02",
    "vegetation": "#1b9e77",
    "cropland": "#e6ab02",
    "water": "#1f78b4",
    "bare": "#969696",
}


def classify_demo(data=None):
    """Fixed south-train / north-test Bay Area probe, with a >=0.05 degree gap.

    Four classes; two bare cells are excluded. No tuning,
    random splits, test fitting or train predictions masquerading as evaluation.
    """
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix, f1_score
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    data = load_demo("bayarea") if data is None else data
    table = data.samples.copy()
    needed = {"tile_id", "demo_split", "class_name", "minlat", "maxlat", "center_lon", "center_lat"}
    if not needed.issubset(table) or len(table) != len(data.features):
        raise ValueError(
            "Bay Area classification requires aligned IDs, coordinates, labels and demo_split."
        )
    if table[list(needed)].isna().any().any() or table.tile_id.duplicated().any():
        raise ValueError("Classification metadata has missing values or duplicate IDs.")
    if table[["center_lon", "center_lat"]].duplicated().any():
        raise ValueError("Duplicate spatial cells are not allowed.")
    classes = ["built", "vegetation", "cropland", "water"]
    eligible = table.class_name.isin(classes)
    expected = np.where(
        table.maxlat <= 37.88, "train", np.where(table.minlat >= 37.93, "test", "buffer")
    )
    if not np.array_equal(table.demo_split.to_numpy(), expected):
        raise ValueError(
            "Spatial leakage or changed split: saved split must match the fixed geographic holdout."
        )
    table.loc[~eligible, "demo_split"] = "excluded_other_class"
    train = table.demo_split.eq("train").to_numpy()
    test = table.demo_split.eq("test").to_numpy()
    if not train.any() or not test.any() or set(table.loc[train, "class_name"]) != set(classes):
        raise ValueError(
            "Fixed Bay Area split needs nonempty train/test and all four training classes."
        )
    if table.loc[test, "minlat"].min() - table.loc[train, "maxlat"].max() < 0.05:
        raise ValueError(
            "Spatial leakage: north test bounds must be separated from south training bounds."
        )
    # Explicit float64 avoids version-dependent float32 solver paths.
    x = np.asarray(data.features, dtype=np.float64)
    if x.ndim != 2 or not np.isfinite(x).all():
        raise ValueError("Classification features must be a finite (N,D) array.")
    model = make_pipeline(
        StandardScaler(), LogisticRegression(C=1.0, tol=1e-8, max_iter=2000, random_state=42)
    )
    model.fit(x[train], table.loc[train, "class_name"])
    predicted = model.predict(x[test])
    truth = table.loc[test, "class_name"]
    table["prediction"] = pd.Series(pd.NA, index=table.index, dtype="string")
    table.loc[test, "prediction"] = predicted
    metrics = {
        "scope": "San Francisco Bay Area regional software demonstration; not a paper benchmark reproduction",
        "seed": 42,
        "estimator": {
            "name": "StandardScaler + LogisticRegression",
            "C": 1.0,
            "tol": 1e-8,
            "max_iter": 2000,
            "dtype": "float64",
            "solver": "lbfgs",
        },
        "model": "AEF 2021 official 1280m overview features",
        "total": len(table),
        "split_counts": table.demo_split.value_counts().to_dict(),
        "class_counts": pd.crosstab(table.demo_split, table.class_name).to_dict(orient="index"),
        "split": "South maxlat<=37.88 train; north minlat>=37.93 test; intervening cells buffer; exclude 2 bare cells",
        "minimum_latitude_gap": float(
            table.loc[test, "minlat"].min() - table.loc[train, "maxlat"].max()
        ),
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
        title=f"Bay Area | WorldCover 2021 reference ({len(table)} cells)",
        ax=axes[0, 0],
    )
    plot_map(
        table,
        table.prediction.map(CLASS_COLORS).fillna("#e8e8e8"),
        title="AEF + logistic regression: north test only",
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
        for latitude in [37.88, 37.93]:
            ax.axhline(latitude, color="#173f40", ls="--", lw=1)
    axes[0, 0].legend(
        handles=[Patch(color=v, label=k) for k, v in CLASS_COLORS.items()],
        fontsize=8,
        loc="upper left",
    )
    axes[0, 1].legend(
        handles=[Patch(color="#e8e8e8", label="Train / buffer / excluded (unscored)")],
        fontsize=8,
        loc="lower left",
    )
    metrics = result["metrics"]
    ConfusionMatrixDisplay(
        np.array(metrics["confusion_matrix"]), display_labels=metrics["classes"]
    ).plot(ax=axes[1, 1], colorbar=False, cmap="Blues")
    axes[1, 1].set_title(
        f"Test n={int(test.sum())} | OA {metrics['oa']:.3f} | Macro-F1 {metrics['macro_f1']:.3f}"
    )
    return fig
