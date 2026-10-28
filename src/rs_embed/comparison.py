"""Run and visualize several models through the same public embedding interface.

Inference is sequential and retains each model's native output and provenance.
Plotting is optional and imports matplotlib only when called.
"""

from __future__ import annotations

import gc
import math
import textwrap
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import numpy as np

from .api import get_embedding, list_models, reset_runtime
from .core.embedding import Embedding
from .core.specs import OutputSpec, SpatialSpec, TemporalSpec
from .embedders.catalog import canonical_model_id


@dataclass
class EmbeddingComparison:
    """Ordered model requests, successful native embeddings, and explicit failures.

    ``errors`` contains ``"ExceptionType: message"`` strings, never substitutes
    for embeddings. Original metadata remains on every successful ``Embedding``.
    Instances can also wrap previously saved embeddings without running models.
    """

    models: tuple[str, ...]
    embeddings: dict[str, Embedding] = field(default_factory=dict)
    errors: dict[str, str] = field(default_factory=dict)

    def summary(self) -> dict[str, dict[str, Any]]:
        """Return a JSON-compatible status/shape summary in request order."""
        return {
            model: (
                {"status": "ok", "shape": list(self.embeddings[model].data.shape)}
                if model in self.embeddings
                else {"status": "error", "error": self.errors.get(model, "Missing result")}
            )
            for model in self.models
        }


def compare_embeddings(
    models: Iterable[str] | None = None,
    *,
    spatial: SpatialSpec,
    temporal: TemporalSpec | None = None,
    output: OutputSpec = OutputSpec.grid(),
    model_options: Mapping[str, Mapping[str, Any]] | None = None,
    on_error: Literal["raise", "record"] = "raise",
    release_models: bool = True,
    **shared_kwargs: Any,
) -> EmbeddingComparison:
    """Request multiple models with the same ``get_embedding`` arguments.

    ``models=None`` selects the full catalog. Aliases are canonicalized and
    duplicates removed in first-occurrence order. ``model_options`` overrides
    shared arguments for individual models, including ``temporal``, ``backend``
    and model settings. For example, annual products can use ``TemporalSpec.year``
    while image encoders share a seasonal ``TemporalSpec.range``.

    Errors raise by default; explicitly select ``on_error='record'`` to continue
    and retain their type/message in the returned report. Nothing is silently
    skipped or replaced with synthetic data. With ``release_models=True``
    (default), global model runtime caches are cleared after each request to
    prevent all model weights accumulating in memory. Disable it to reuse loaded
    weights across calls. Embedding arrays themselves remain in memory.

    This function does not align grids, harmonize sensors, change dates, or
    imply that different models' feature dimensions are interchangeable.
    Location models interpret grid spacing as coordinate sampling distance.
    Downloads and provider authentication follow each model's usual behavior.
    """
    if on_error not in {"raise", "record"}:
        raise ValueError("on_error must be 'raise' or 'record'.")
    if isinstance(models, str):
        raise TypeError("models must be a sequence of model IDs, e.g. ['prithvi', 'esri'].")
    requested = list_models() if models is None else models
    names = tuple(dict.fromkeys(canonical_model_id(m) for m in requested))
    if not names:
        raise ValueError("Select at least one model.")
    unknown = set(names) - set(list_models())
    if unknown:
        raise ValueError(f"Unknown models: {sorted(unknown)}. Use list_models() for valid IDs.")
    options: dict[str, dict[str, Any]] = {}
    for model, overrides in (model_options or {}).items():
        name = canonical_model_id(model)
        if name not in names:
            raise ValueError(f"model_options contains unselected model {model!r}.")
        if name in options:
            raise ValueError(f"model_options contains duplicate aliases for {name!r}.")
        if "model" in overrides:
            raise ValueError("model_options cannot override the model ID.")
        options[name] = dict(overrides)
    shared = dict(spatial=spatial, temporal=temporal, output=output, **shared_kwargs)
    report = EmbeddingComparison(models=names)
    for name in names:
        try:
            report.embeddings[name] = get_embedding(name, **(shared | options.get(name, {})))
        except Exception as exc:
            if on_error == "raise":
                raise
            report.errors[name] = f"{type(exc).__name__}: {exc}"
        finally:
            if release_models:
                reset_runtime()
                gc.collect()
    return report


def _pca_rgb(samples: np.ndarray, *, max_fit_samples: int = 2048) -> np.ndarray:
    """Independent deterministic PCA; invalid rows gray, flat channels neutral."""
    samples = np.asarray(samples)
    if samples.ndim != 2 or min(samples.shape) == 0:
        raise ValueError("PCA requires a nonempty (samples, features) array.")
    if not np.issubdtype(samples.dtype, np.number) or np.iscomplexobj(samples):
        raise ValueError("PCA requires real numeric feature values.")
    # Large precomputed products can have millions of vectors. Keep their
    # source dtype, and only allocate float64 for bounded chunks and PCA fit.
    chunk_size = max(1, 1_000_000 // samples.shape[1])
    valid = np.zeros(len(samples), dtype=bool)
    scale = 0.0
    for start in range(0, len(samples), chunk_size):
        block = np.asarray(samples[start : start + chunk_size], dtype=np.float64)
        finite = np.isfinite(block).all(axis=1)
        valid[start : start + len(block)] = finite
        if finite.any():
            scale = max(scale, float(np.max(np.abs(block[finite]))))
    rgb = np.full((len(samples), 3), 0.5, dtype=np.float32)
    if not valid.any():
        raise ValueError("Embedding contains no finite feature vectors.")
    if scale == 0:
        return rgb
    indices = np.flatnonzero(valid)
    count = min(len(indices), max_fit_samples)
    selected = indices[np.linspace(0, len(indices) - 1, count, dtype=int)]
    # Scale first to avoid overflow from large finite source values.
    fit = np.asarray(samples[selected], dtype=np.float64) / scale
    mean = fit.mean(axis=0)
    centered = fit - mean
    if not np.any(centered):
        return rgb
    _, singular, components = np.linalg.svd(centered, full_matrices=False)
    k = min(3, len(singular))
    components = components[:k].copy()
    # Eigenvectors' signs are arbitrary; lock them by their largest loading.
    pivots = np.argmax(np.abs(components), axis=1)
    signs = np.sign(components[np.arange(k), pivots])
    components *= np.where(signs == 0, 1, signs)[:, None]
    scores = np.empty((len(indices), k), dtype=np.float64)
    for start in range(0, len(indices), chunk_size):
        rows = indices[start : start + chunk_size]
        block = np.asarray(samples[rows], dtype=np.float64)
        scores[start : start + len(rows)] = (block / scale - mean) @ components.T
    # Suppress numerical noise in rank-deficient/constant feature fields.
    tolerance = singular[0] * max(centered.shape) * np.finfo(np.float64).eps
    for channel in range(k):
        if singular[channel] <= tolerance:
            continue
        low, high = np.percentile(scores[:, channel], [2, 98])
        if high > low:
            rgb[valid, channel] = np.clip((scores[:, channel] - low) / (high - low), 0, 1)
    return rgb


def _grid_array(embedding: Embedding) -> np.ndarray:
    """Read CHW grids, honoring named axes and explicit orientation metadata."""
    data = embedding.data
    dims = tuple(getattr(data, "dims", ()))
    if len(dims) == 3 and "y" in dims and "x" in dims:
        feature_dim = next(d for d in dims if d not in {"y", "x"})
        data = data.transpose(feature_dim, "y", "x")
        array = np.asarray(data.values)
    else:
        array = np.asarray(data)
    # Most encoders use ascending pixel indices for y, not latitude. Do not
    # infer geographic orientation from these indices and flip a valid image.
    if embedding.meta.get("y_axis_direction") == "south_to_north":
        array = array[:, ::-1, :]
    return array


def _panel_kind(model: str, embedding: Embedding) -> str:
    kind = embedding.meta.get("type", embedding.meta.get("kind", ""))
    if kind == "location" or canonical_model_id(model) in {"esri_gle", "satclip", "geoclip"}:
        return "coordinate samples (not image pixels)"
    if kind == "precomputed" or canonical_model_id(model) in {"gse", "tessera", "copernicus"}:
        return "precomputed product"
    return "image encoder"


def _plot_embedding(ax: Any, model: str, embedding: Embedding, lonlat: Any) -> None:
    data = np.asarray(embedding.data)
    if data.size == 0:
        raise ValueError(f"{model}: embedding is empty.")
    label = _panel_kind(model, embedding)
    if data.ndim == 3:
        chw = _grid_array(embedding)
        dim, height, width = chw.shape
        rgb = _pca_rgb(chw.reshape(dim, -1).T).reshape(height, width, 3)
        ax.imshow(rgb, interpolation="nearest")
        grid_kind = "query grid" if label.startswith("coordinate") else "native grid"
        ax.set_title(f"{model} | {dim}-D\n{height} x {width} {grid_kind}", fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
    elif data.ndim == 2:
        rgb = _pca_rgb(data)
        if lonlat is not None:
            points = np.asarray(lonlat, dtype=float)
            if points.shape != (len(data), 2) or not np.isfinite(points).all():
                raise ValueError(f"{model}: lonlat must be finite with shape ({len(data)}, 2).")
            ax.scatter(points[:, 0], points[:, 1], c=rgb, s=9, linewidths=0)
            ax.set_xlabel("Longitude", fontsize=8)
            ax.set_ylabel("Latitude", fontsize=8)
            midlat = np.mean(points[:, 1])
            ax.set_aspect(1 / max(np.cos(np.deg2rad(midlat)), 0.01))
            ax.tick_params(labelsize=7)
            label = "coordinate samples; input row order retained"
        else:
            ax.imshow(rgb[None], aspect="auto", interpolation="nearest")
            ax.set_xlabel("Sample index (not a spatial map)", fontsize=8)
            ax.set_yticks([])
            label = "sample colors; coordinates not provided"
        ax.set_title(f"{model} | {data.shape[1]}-D\n{len(data)} samples", fontsize=10)
    elif data.ndim == 1:
        if not np.isfinite(data).any():
            raise ValueError(f"{model}: embedding contains no finite values.")
        ax.plot(data, color="#2563a6", linewidth=0.8)
        ax.set_title(f"{model} | {data.size}-D\nPooled vector (not a spatial map)", fontsize=10)
        ax.set_xlabel("Feature index", fontsize=8)
        ax.tick_params(labelsize=7)
    else:
        raise ValueError(f"{model}: expected a vector, (N, D) samples, or (D, H, W) grid.")
    # Directly under bare image panels; below tick labels and axis labels elsewhere.
    decorated = bool(ax.get_xlabel()) or len(ax.get_xticks()) > 0
    ax.text(
        0.5,
        -0.2 if decorated else -0.025,
        label,
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=7,
        color="#526071",
    )


def _box_ratio(ax: Any) -> float:
    """Height/width of a panel's drawn box, so each figure row can fit its panels."""
    aspect = ax.get_aspect()
    if aspect == "auto":
        return 0.62
    return float(np.clip(float(aspect) * ax.get_data_ratio(), 0.3, 1.2))


def plot_embedding_comparison(
    comparison: EmbeddingComparison | Mapping[str, Embedding],
    *,
    columns: int = 5,
    reference: Any | None = None,
    reference_title: str = "Reference image",
    title: str | None = None,
    lonlat: Any | Mapping[str, Any] | None = None,
    save_path: str | Path | None = None,
    dpi: int = 160,
) -> Any:
    """Create one figure from native grids, coordinate samples, or pooled vectors.

    Accepts a comparison report or an ordered mapping of model IDs to previously
    computed ``Embedding`` objects. Grid arrays are channel-first ``(D, H, W)``;
    xarray ``y``/``x`` dimensions and orientation metadata are respected. For ``(N, D)`` point
    samples pass ``lonlat`` (shared or a model-to-coordinate mapping), otherwise
    display a labeled sample strip. Pooled vectors are explicitly line plots.

    Colors use three independent PCA components per model, fitted to at most
    2048 deterministically sampled finite vectors, with 2nd/98th percentile
    stretching. They show within-model structure, not comparable feature axes,
    quantitative accuracy, land-cover labels or equal spatial resolution.
    Invalid pixels and constant components are gray. Nothing is interpolated.

    Failed inference requests in a report remain visible as error panels.
    Invalid plotting inputs raise rather than silently hiding corrupted data.
    ``reference`` optionally adds an HWC RGB/RGBA array. Requires the ``plot``
    extra. Returns a matplotlib Figure; call ``plt.show()`` or save it yourself,
    or supply ``save_path`` for a convenience export.
    """
    if isinstance(columns, bool) or not isinstance(columns, int) or columns < 1:
        raise ValueError("columns must be a positive integer.")
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ImportError('Plotting requires: pip install "earth-embedding[plot]"') from exc
    if isinstance(comparison, EmbeddingComparison):
        names = comparison.models
        embeddings, errors = comparison.embeddings, comparison.errors
    else:
        names = tuple(comparison)
        embeddings, errors = comparison, {}
    if not names:
        raise ValueError("A comparison must contain at least one model.")
    conflicts = set(embeddings) & set(errors)
    if conflicts:
        raise ValueError(f"Models cannot have both embeddings and errors: {sorted(conflicts)}.")
    count = len(names) + (reference is not None)
    columns = min(columns, count)
    rows = math.ceil(count / columns)
    fig, axes = plt.subplots(
        rows, columns, figsize=(3.6 * columns, 3.7 * rows), squeeze=False, layout="constrained"
    )
    flat = axes.ravel()
    offset = 0
    try:
        if reference is not None:
            ref = np.asarray(reference)
            if ref.ndim != 3 or ref.shape[-1] not in {3, 4}:
                raise ValueError("reference must be an HWC RGB or RGBA image.")
            flat[0].imshow(ref, interpolation="nearest")
            flat[0].set_title(reference_title, fontsize=10)
            flat[0].set_axis_off()
            offset = 1
        for ax, name in zip(flat[offset:], names, strict=False):
            if name in embeddings:
                coordinates = lonlat.get(name) if isinstance(lonlat, Mapping) else lonlat
                _plot_embedding(ax, name, embeddings[name], coordinates)
            else:
                ax.set_facecolor("#fef2f2")
                ax.set_title(f"{name}\nFAILED / UNAVAILABLE", fontsize=10, color="#9b2424")
                message = errors.get(name, "No embedding or error was supplied for this model.")
                ax.text(
                    0.04,
                    0.9,
                    textwrap.fill(message, width=38)[:600],
                    transform=ax.transAxes,
                    va="top",
                    fontsize=8,
                    color="#7c3030",
                    clip_on=True,
                )
                ax.set_xticks([])
                ax.set_yticks([])
        for ax in flat[count:]:
            ax.set_visible(False)
        successes = sum(name in embeddings for name in names)
        heading = title or f"Embedding comparison | {successes}/{len(names)} models available"
        # Size each row to its widest-aspect panel: global maps no longer leave empty bands.
        heights = [
            3.3 * max((_box_ratio(ax) for ax in row if ax.get_visible()), default=0.62) + 0.8
            for row in axes
        ]
        axes[0, 0].get_gridspec().set_height_ratios(heights)
        fig.set_size_inches(3.6 * columns, sum(heights) + 0.4 * (heading.count("\n") + 2))
        fig.get_layout_engine().set(w_pad=0.08, h_pad=0.08, hspace=0.04, wspace=0.03)
        fig.suptitle(heading, fontsize=15, fontweight="bold")
        fig.supxlabel(
            "Independent PCA colors per model; colors are not comparable across models. "
            "Native grids are not resampled.\n"
            "Coordinate sampling is not image resolution. Gray denotes invalid vectors "
            "or constant components; panels are qualitative, not accuracy scores.",
            fontsize=8,
            color="#526071",
        )
        if save_path is not None:
            path = Path(save_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(path, dpi=dpi, bbox_inches="tight")
    except Exception:
        plt.close(fig)
        raise
    return fig
