"""Encode supplied pixels without fetching imagery or authenticating a provider."""

from __future__ import annotations

import inspect
from typing import Any

import numpy as np

from .core.embedding import Embedding
from .core.errors import ModelError
from .core.registry import get_embedder_cls
from .core.specs import OutputSpec, SensorSpec, SpatialSpec, TemporalSpec
from .embedders.catalog import MODEL_SPECS, canonical_model_id
from .tools.model_defaults import default_sensor_for_model

_TEMPORAL_MODELS = frozenset({"anysat", "galileo", "agrifm"})


def get_image_embedding(
    model: str,
    pixels: np.ndarray,
    *,
    spatial: SpatialSpec,
    temporal: TemporalSpec,
    sensor: SensorSpec | None = None,
    output: OutputSpec | None = None,
    device: str = "auto",
    model_config: dict[str, Any] | None = None,
) -> Embedding:
    """Run an image encoder on a caller-supplied CHW or multitemporal TCHW array.

    ``pixels`` uses the model's declared sensor band order and raw sensor units:
    Sentinel-2 reflectance is ordinarily scaled by 10000, rather than RGB uint8
    or an already normalized tensor. Model-specific preprocessing remains inside
    the adapter. Supply ``sensor`` when overriding the model's default modality.
    Check ``describe_model(model)`` and its model guide before preparing input.

    ``spatial`` and ``temporal`` describe these pixels, and are required because
    some encoders use geographic, resolution, or time metadata. TCHW inputs are
    accepted for AnySat, Galileo, and AgriFM; use independent temporal frames for
    meaningful temporal embeddings. No imagery is fetched. Pretrained weights
    may be downloaded on the first call according to the adapter's cache policy.

    This helper is for class-A image encoders. Use ``get_location_embedding`` for
    coordinates and ``get_embedding`` for precomputed products.
    """
    model_id = canonical_model_id(model)
    spec = MODEL_SPECS.get(model_id)
    if spec is None:
        raise ModelError(f"Unknown image model {model!r}.")
    if not spec[0].startswith("onthefly_"):
        raise ModelError(f"{model_id!r} is not an image encoder; it cannot encode supplied pixels.")
    spatial.validate()
    temporal.validate()
    array = np.asarray(pixels)
    if array.dtype.kind not in "uif":
        raise ModelError("pixels must be a real numeric array in raw sensor units.")
    accepted_ndims = (3, 4) if model_id in _TEMPORAL_MODELS else (3,)
    if array.ndim not in accepted_ndims or any(size == 0 for size in array.shape):
        layout = "CHW or TCHW" if model_id in _TEMPORAL_MODELS else "CHW"
        raise ModelError(f"{model_id} requires a nonempty {layout} array; got {array.shape}.")
    if not np.isfinite(array).all():
        raise ModelError("pixels contains NaN or infinity; resolve missing values before encoding.")
    resolved_sensor = sensor if sensor is not None else default_sensor_for_model(model_id)
    if resolved_sensor is not None and resolved_sensor.bands:
        channels = array.shape[-3]
        if channels != len(resolved_sensor.bands):
            raise ModelError(
                f"{model_id} expects {len(resolved_sensor.bands)} channels in sensor.bands order; "
                f"received {channels}."
            )
    # Copy only when required; adapters own any model-specific normalization.
    array = np.ascontiguousarray(array, dtype=np.float32)
    if not np.isfinite(array).all():
        raise ModelError("pixels cannot be represented as finite float32 values.")
    embedder = get_embedder_cls(model_id)()
    kwargs: dict[str, Any] = {
        "spatial": spatial,
        "temporal": temporal,
        "sensor": resolved_sensor,
        "output": output if output is not None else OutputSpec.pooled(),
        "device": device,
        "backend": "auto",
        "input_chw": array,
    }
    if model_config:
        parameters = inspect.signature(embedder.get_embedding).parameters.values()
        if not any(p.name == "model_config" or p.kind == p.VAR_KEYWORD for p in parameters):
            raise ModelError(
                f"{model_id} does not accept model_config; see its documented settings."
            )
        kwargs["model_config"] = model_config
    embedding = embedder.get_embedding(**kwargs)
    return Embedding(
        data=embedding.data,
        meta={**embedding.meta, "input_source": "user_array", "supplied_input_shape": array.shape},
    )
