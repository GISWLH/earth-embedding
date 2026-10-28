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
    ``aef`` is an alias for ``bayarea``: a complete 72 x 88 grid of 6336 official
    1280 m AEF overview cells.
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


def _degree_formatter(axis):
    from matplotlib.ticker import FuncFormatter

    hemispheres = ("E", "W") if axis == "x" else ("N", "S")

    def label(value, _):
        digits = f"{abs(value):.4f}".rstrip("0").rstrip(".")
        return f"{digits}°{hemispheres[int(value < 0)]}"

    return FuncFormatter(label)


def _complete_grid(samples):
    """Return (rows, cols) index arrays when samples form a complete grid, else None."""
    if not {"grid_row", "grid_col"}.issubset(samples):
        return None
    rows, cols = samples.grid_row.to_numpy(int), samples.grid_col.to_numpy(int)
    if rows.min() != 0 or cols.min() != 0:
        return None
    if len(set(zip(rows, cols, strict=True))) != len(rows) or len(rows) != (rows.max() + 1) * (
        cols.max() + 1
    ):
        return None
    return rows, cols


def _grid_mesh(rows, cols, polygons):
    """Corner lon/lat arrays (H+1, W+1) of a complete grid; vertices are SW, SE, NE, NW."""
    height, width = rows.max() + 1, cols.max() + 1
    cell = np.empty((height, width, 4, 2))
    cell[rows, cols] = polygons
    mesh = np.empty((height + 1, width + 1, 2))
    mesh[:-1, :-1] = cell[:, :, 3]
    mesh[:-1, -1] = cell[:, -1, 2]
    mesh[-1, :-1] = cell[-1, :, 0]
    mesh[-1, -1] = cell[-1, -1, 1]
    return mesh


def _map_extent(mesh):
    """Inner lon/lat frame of a projected grid, which is slightly rotated against lon/lat."""
    return (
        mesh[:, 0, 0].max(),
        mesh[:, -1, 0].min(),
        mesh[-1, :, 1].max(),
        mesh[0, :, 1].min(),
    )


def plot_map(samples, colors, *, title="Embedding PCA (not land-cover classes)", ax=None):
    """Draw real WGS84 cell polygons, north up; return a Matplotlib Figure.

    A complete grid with ``grid_row``/``grid_col`` columns is drawn as one seamless
    mesh and cropped to its inner frame; other samples are drawn cell by cell.
    """
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection
    from matplotlib.colors import to_rgba_array
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
        _, ax = plt.subplots(figsize=(5.0, 5.9), layout="constrained")
    polygons = np.array([[(w, s), (e, s), (e, n), (w, n)] for w, s, e, n in bounds])
    vertices = [item for i in range(4) for item in (f"lon{i}", f"lat{i}")]
    if set(vertices).intersection(samples):
        if not set(vertices).issubset(samples):
            raise ValueError("Cell polygons require all four lon0/lat0 through lon3/lat3 vertices.")
        polygons = samples[vertices].to_numpy(float).reshape(-1, 4, 2)
        if not np.isfinite(polygons).all():
            raise ValueError("Cell polygon vertices must be finite.")
    grid = _complete_grid(samples)
    if grid is None:
        ax.add_collection(
            PolyCollection(polygons, facecolors=colors, edgecolors="face", linewidths=0.35)
        )
        west, east = polygons[..., 0].min(), polygons[..., 0].max()
        south, north = polygons[..., 1].min(), polygons[..., 1].max()
    else:
        # A whole-cell grid is drawn as one curvilinear mesh: exact cell geometry, no seams.
        rows, cols = grid
        mesh = _grid_mesh(rows, cols, polygons)
        rgba = np.zeros((rows.max() + 1, cols.max() + 1, 4))
        rgba[rows, cols] = to_rgba_array(colors)
        ax.pcolormesh(mesh[..., 0], mesh[..., 1], rgba, shading="flat", rasterized=True)
        west, east, south, north = _map_extent(mesh)
    ax.set_xlim(west, east)
    ax.set_ylim(south, north)
    ax.set_aspect(1 / np.cos(np.deg2rad((south + north) / 2)))
    ax.set_title(title, loc="left", fontsize=10.5)
    # 1/2/5 steps keep tick values exact at one or two decimals.
    ax.xaxis.set_major_locator(MaxNLocator(4, steps=[1, 2, 5, 10]))
    ax.yaxis.set_major_locator(MaxNLocator(6, steps=[1, 2, 5, 10]))
    ax.xaxis.set_major_formatter(_degree_formatter("x"))
    ax.yaxis.set_major_formatter(_degree_formatter("y"))
    ax.tick_params(labelsize=8, length=3, color="#9aa5a2", labelcolor="#4a5a57")
    for spine in ax.spines.values():
        spine.set_color("#9aa5a2")
    return ax.figure


CLASS_COLORS = {
    "built": "#d95f02",
    "vegetation": "#1b9e77",
    "cropland": "#e6ab02",
    "water": "#1f78b4",
    "bare": "#969696",
}
CLASSES = ["built", "vegetation", "cropland", "water"]
# Two spatial folds by grid column; six buffer columns (7.68 km) are never fitted or scored.
FOLDS = {"west": "east", "east": "west"}
SPLIT_COLUMNS = {"west": (0, 33), "buffer": (33, 39), "east": (39, 72)}
_UNSCORED = "#ebebe6"


def classify_demo(data=None):
    """Two-fold spatial holdout: west predicts east, east predicts west.

    Each half is labelled by a model fitted only on the other half; a 7.68 km
    buffer is never fitted or scored, so every scored cell has an out-of-fold
    prediction. Four classes (the two bare cells are not scored). No tuning,
    random splits, test fitting or train predictions masquerading as evaluation.
    """
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix, f1_score
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    data = load_demo("bayarea") if data is None else data
    table = data.samples.copy()
    needed = {"tile_id", "demo_split", "class_name", "grid_col", "minlon", "maxlon"}
    if not needed.issubset(table) or len(table) != len(data.features):
        raise ValueError(
            "Bay Area classification requires aligned IDs, grid columns, labels and demo_split."
        )
    if table[list(needed)].isna().any().any() or table.tile_id.duplicated().any():
        raise ValueError("Classification metadata has missing values or duplicate IDs.")
    if table[["grid_row", "grid_col"]].duplicated().any():
        raise ValueError("Duplicate spatial cells are not allowed.")
    expected = np.full(len(table), "", dtype=object)
    for name, (start, stop) in SPLIT_COLUMNS.items():
        expected[table.grid_col.between(start, stop - 1).to_numpy()] = name
    if not np.array_equal(table.demo_split.to_numpy(dtype=object), expected):
        raise ValueError(
            "Spatial leakage or changed split: saved split must match the fixed column folds."
        )
    # Explicit float64 avoids version-dependent float32 solver paths.
    x = np.asarray(data.features, dtype=np.float64)
    if x.ndim != 2 or not np.isfinite(x).all():
        raise ValueError("Classification features must be a finite (N,D) array.")
    eligible = table.class_name.isin(CLASSES).to_numpy()
    table["prediction"] = pd.Series(pd.NA, index=table.index, dtype="string")
    table["predicted_by"] = pd.Series(pd.NA, index=table.index, dtype="string")
    estimators, folds = {}, {}
    for fit_on, predict in FOLDS.items():
        train = table.demo_split.eq(fit_on).to_numpy() & eligible
        test = table.demo_split.eq(predict).to_numpy() & eligible
        if not test.any() or set(table.loc[train, "class_name"]) != set(CLASSES):
            raise ValueError("Each fold needs nonempty test cells and all four training classes.")
        west, east = (train, test) if fit_on == "west" else (test, train)
        gap = table.loc[east, "minlon"].min() - table.loc[west, "maxlon"].max()
        if gap < 0.05:
            raise ValueError(
                "Spatial leakage: fitted and predicted cells must be separated by the buffer."
            )
        model = make_pipeline(
            StandardScaler(),
            LogisticRegression(
                C=1.0, class_weight="balanced", tol=1e-8, max_iter=4000, random_state=42
            ),
        )
        model.fit(x[train], table.loc[train, "class_name"])
        predicted = model.predict(x[test])
        table.loc[test, "prediction"] = predicted
        table.loc[test, "predicted_by"] = f"fit_{fit_on}"
        truth = table.loc[test, "class_name"]
        estimators[f"{fit_on}_to_{predict}"] = model
        folds[f"{fit_on}_to_{predict}"] = {
            "train": int(train.sum()),
            "test": int(test.sum()),
            "longitude_gap_degrees": float(gap),
            "oa": float(accuracy_score(truth, predicted)),
            "macro_f1": float(
                f1_score(truth, predicted, labels=CLASSES, average="macro", zero_division=0)
            ),
        }
    scored = table.prediction.notna().to_numpy()
    truth, predicted = table.loc[scored, "class_name"], table.loc[scored, "prediction"].astype(str)
    metrics = {
        "scope": "San Francisco Bay Area regional software demonstration; not a paper benchmark reproduction",
        "seed": 42,
        "estimator": {
            "name": "StandardScaler + LogisticRegression",
            "C": 1.0,
            "class_weight": "balanced",
            "tol": 1e-8,
            "max_iter": 4000,
            "dtype": "float64",
            "solver": "lbfgs",
        },
        "model": "AEF 2021 official 1280m overview features",
        "total": len(table),
        "scored": int(scored.sum()),
        "split_counts": table.demo_split.value_counts().to_dict(),
        "class_counts": pd.crosstab(table.demo_split, table.class_name).to_dict(orient="index"),
        "split": "Two spatial folds: west columns 0-32 and east columns 39-71 each predicted by a model fitted only on the other; buffer columns 33-38 (7.68 km) never fitted or scored; 2 bare cells not scored",
        "folds": folds,
        "classes": CLASSES,
        "oa": float(accuracy_score(truth, predicted)),
        "macro_f1": float(
            f1_score(truth, predicted, labels=CLASSES, average="macro", zero_division=0)
        ),
        "balanced_accuracy": float(balanced_accuracy_score(truth, predicted)),
        "confusion_matrix": confusion_matrix(truth, predicted, labels=CLASSES).tolist(),
    }
    return {"metrics": metrics, "samples": table, "estimators": estimators}


def _fold_guides(ax, table):
    """Shade the unscored buffer and label which model predicted each half."""
    buffer = table.demo_split.eq("buffer")
    west = table.loc[buffer, ["lon0", "lon3"]].to_numpy().min()
    east = table.loc[buffer, ["lon1", "lon2"]].to_numpy().max()
    ax.axvspan(west, east, facecolor="none", edgecolor="#5b6b68", hatch="////", lw=0)
    for edge in (west, east):
        ax.axvline(edge, color="#173f40", ls=(0, (4, 3)), lw=0.9)


def plot_classification(result):
    """Reference, out-of-fold predictions, errors and confusion matrix in one row."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch

    table = result["samples"]
    metrics = result["metrics"]
    scored = table.prediction.notna().to_numpy()
    fig = plt.figure(figsize=(15.2, 5.0), layout="constrained")
    grid = fig.add_gridspec(1, 4, width_ratios=[1, 1, 1, 1.12])
    axes = [fig.add_subplot(grid[0, i]) for i in range(4)]
    plot_map(
        table,
        table.class_name.map(CLASS_COLORS).to_numpy(dtype=object),
        title="a  WorldCover 2021 reference",
        ax=axes[0],
    )
    plot_map(
        table,
        table.prediction.map(CLASS_COLORS).fillna(_UNSCORED).to_numpy(dtype=object),
        title="b  AEF + logistic regression, held out",
        ax=axes[1],
    )
    correct = table.class_name.to_numpy() == table.prediction.astype(str).to_numpy()
    agreement = np.full(len(table), _UNSCORED, dtype=object)
    agreement[scored] = np.where(correct[scored], "#cfe3dc", "#c43c39")
    plot_map(table, agreement, title="c  Where the prediction is wrong", ax=axes[2])
    for ax in axes[:3]:
        _fold_guides(ax, table)
    top = axes[1].get_ylim()[1]
    middle = np.mean(axes[1].get_xlim())
    for ax in axes[1:3]:
        for x, text, align in [
            (middle - 0.07, "← fit east, predict west", "right"),
            (middle + 0.07, "fit west, predict east →", "left"),
        ]:
            ax.annotate(
                text,
                (x, top),
                xytext=(0, -5),
                textcoords="offset points",
                ha=align,
                va="top",
                fontsize=7.5,
                color="#173f40",
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.85),
            )

    matrix = np.array(metrics["confusion_matrix"], dtype=float)
    recall = matrix / np.maximum(matrix.sum(axis=1, keepdims=True), 1)
    ax = axes[3]
    ax.imshow(recall, cmap="GnBu", vmin=0, vmax=1)
    for (i, j), count in np.ndenumerate(matrix.astype(int)):
        ax.text(
            j,
            i,
            f"{count:,}\n{recall[i, j]:.0%}",
            ha="center",
            va="center",
            fontsize=8.5,
            color="white" if recall[i, j] > 0.55 else "#173f40",
        )
    ticks = range(len(metrics["classes"]))
    ax.set_xticks(ticks, metrics["classes"], fontsize=8.5)
    ax.set_yticks(ticks, metrics["classes"], fontsize=8.5, rotation=90, va="center")
    ax.set_xlabel(f"Predicted class · {metrics['scored']:,} held-out cells", fontsize=9)
    ax.set_ylabel("WorldCover reference", fontsize=9)
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title(
        f"d  OA {metrics['oa']:.1%} · macro-F1 {metrics['macro_f1']:.1%}",
        loc="left",
        fontsize=10.5,
    )
    handles = [Patch(color=CLASS_COLORS[name], label=name) for name in metrics["classes"]]
    handles += [
        Patch(facecolor=_UNSCORED, edgecolor="#5b6b68", hatch="////", label="buffer, not scored"),
        Patch(color="#cfe3dc", label="correct"),
        Patch(color="#c43c39", label="wrong"),
    ]
    fig.legend(
        handles=handles,
        loc="outside lower center",
        ncol=len(handles),
        frameon=False,
        fontsize=9,
        handlelength=1.4,
    )
    return fig
