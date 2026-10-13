"""Convenient coordinate-only public entry point for all registered location encoders."""

from __future__ import annotations

from typing import Any

from ..core.embedding import Embedding
from ..core.errors import ModelError
from ..core.registry import get_embedder_cls
from .catalog import canonical_model_id
from .location_common import positive_int, validate_features, validate_lonlat
from .meta_utils import build_meta


def get_location_embeddings(
    model: str,
    lonlat: Any,
    *,
    device: str = "auto",
    batch_size: int = 1024,
    **model_kwargs: Any,
) -> Embedding:
    """Encode WGS84 coordinates without imagery, dates or Earth Engine.

    Parameters
    ----------
    model : str
        ``satclip``, ``geoclip`` or ``esri_gle`` (aliases also accepted).
    lonlat : array-like
        Nonempty ``(N, 2)`` array in **longitude, latitude** order, in degrees.
        A single coordinate must be nested: ``[[114.4, 30.5]]``.
    device : str
        ``auto``, ``cpu`` or a PyTorch device such as ``cuda:0``.
    batch_size : int
        Maximum number of coordinates passed to the encoder per inference call.
    **model_kwargs
        Model settings, e.g. ``variant='vit16-l10'`` for SatCLIP or
        ``checkpoint='/path/location_encoder_weights.pth'`` for GeoCLIP.

    Returns
    -------
    Embedding
        ``data`` is a float32 ``(N, D)`` array, in input row order. ``meta``
        records model/checkpoint provenance and coordinate order. Pooled ROI
        requests remain available through ``get_embedding``.
    """
    arr = validate_lonlat(lonlat)
    chunk = positive_int(batch_size, "batch_size")
    model_id = canonical_model_id(model)
    embedder = get_embedder_cls(model_id)()
    desc = embedder.describe()
    if desc.get("type") != "location":
        raise ModelError(
            f"{model!r} is not a location encoder. Use get_embedding for imagery/products."
        )
    if model_id == "satclip":
        from .location_satclip import _SATCLIP_VARIANTS, _resolve_variant, encode_lonlat

        unknown = set(model_kwargs) - {"variant"}
        if unknown:
            raise ModelError(f"Unknown SatCLIP location settings: {sorted(unknown)}.")
        variant = _resolve_variant(model_kwargs)
        features, run_meta = encode_lonlat(arr, variant=variant, device=device, batch_size=chunk)
        run_meta["variant"] = variant
        source = f"hf://{_SATCLIP_VARIANTS[variant]['repo_id']}"
        runtime = "vendored_satclip"
    else:
        features, run_meta = embedder.encode_locations(
            arr, device=device, batch_size=chunk, model_config=model_kwargs
        )
        source, runtime = embedder.source, embedder.runtime
    features = validate_features(features, count=len(arr), model=model_id)
    meta = build_meta(
        model=model_id,
        kind="location",
        backend=runtime,
        source=source,
        sensor=None,
        temporal=None,
        image_size=None,
        extra={
            **run_meta,
            "input_crs": "EPSG:4326",
            "coordinate_order": "longitude_latitude",
            "query_input": "longitude_latitude_only",
            "query_count": len(arr),
            "embedding_dim": features.shape[1],
            "batch_size": chunk,
        },
    )
    return Embedding(data=features, meta=meta)
