from __future__ import annotations

import math
import os
from functools import lru_cache
from typing import Any

import numpy as np

from ..core.embedding import Embedding
from ..core.errors import ModelError
from ..core.registry import register
from ..core.specs import BBox, OutputSpec, PointBuffer, SensorSpec, SpatialSpec, TemporalSpec
from .base import EmbedderBase
from .location_common import (
    centre_lonlat,
    location_grid,
    positive_int,
    resolve_torch_device,
    validate_features,
    validate_lonlat,
)
from .meta_utils import build_meta

# Released location-encoder checkpoints (MIT License), pinned to the Hugging Face revisions
# verified on 2026-10-09.
_SATCLIP_VARIANTS: dict[str, dict[str, str]] = {
    "vit16-l40": {
        "repo_id": "microsoft/SatCLIP-ViT16-L40",
        "filename": "satclip-vit16-l40.ckpt",
        "revision": "0ef2acc0b91d3c8cfdf4a0cc03207095989287ab",
    },
    "vit16-l10": {
        "repo_id": "microsoft/SatCLIP-ViT16-L10",
        "filename": "satclip-vit16-l10.ckpt",
        "revision": "829a79064fade0233c68bf01b7a3155be1b8778b",
    },
    "resnet50-l40": {
        "repo_id": "microsoft/SatCLIP-ResNet50-L40",
        "filename": "satclip-resnet50-l40.ckpt",
        "revision": "b66714c7308a55d12849d1ea43f892440d78e41a",
    },
}
_DEFAULT_VARIANT = "vit16-l40"
_M_PER_DEG_LAT = 111_320.0


def _model_config_value(model_config: dict[str, Any] | None, key: str) -> Any | None:
    if model_config is None:
        return None
    if isinstance(model_config, dict):
        return model_config.get(key)
    return getattr(model_config, key, None)


def _resolve_variant(model_config: dict[str, Any] | None) -> str:
    raw = _model_config_value(model_config, "variant")
    if raw is None:
        raw = os.environ.get("RS_EMBED_SATCLIP_VARIANT", _DEFAULT_VARIANT)
    variant = str(raw).strip().lower().replace("_", "-")
    if variant not in _SATCLIP_VARIANTS:
        raise ModelError(
            f"Unknown SatCLIP variant={raw!r}; expected one of {sorted(_SATCLIP_VARIANTS)}."
        )
    return variant


def _resolve_checkpoint(variant: str) -> tuple[str, dict[str, Any]]:
    """Return a local checkpoint path and its provenance record."""
    override = os.environ.get("RS_EMBED_SATCLIP_CKPT")
    if override:
        path = os.path.expanduser(override)
        if not os.path.isfile(path):
            raise ModelError(f"RS_EMBED_SATCLIP_CKPT does not exist: {path}")
        return path, {"source": "local_override", "path": path}
    spec = _SATCLIP_VARIANTS[variant]
    try:
        from huggingface_hub import hf_hub_download
    except Exception as e:  # pragma: no cover - dependency guard
        raise ModelError("SatCLIP checkpoint download requires huggingface_hub.") from e
    path = hf_hub_download(spec["repo_id"], spec["filename"], revision=spec["revision"])
    return path, {"source": "huggingface", **spec, "path": path}


@lru_cache(maxsize=4)
def _load_location_encoder(ckpt_path: str, device: str) -> tuple[Any, dict[str, Any]]:
    try:
        from ._vendor.satclip import load_satclip_location_encoder
    except Exception as e:
        raise ModelError(
            f"Failed to import vendored SatCLIP runtime: {type(e).__name__}: {e}"
        ) from e
    weights_only = os.environ.get("RS_EMBED_SATCLIP_WEIGHTS_ONLY", "1") != "0"
    return load_satclip_location_encoder(ckpt_path, device=device, weights_only=weights_only)


def _resolve_device(device: str) -> str:
    return resolve_torch_device(device)


def _bbox_of(spatial: SpatialSpec) -> BBox:
    if isinstance(spatial, BBox):
        spatial.validate()
        return spatial
    if isinstance(spatial, PointBuffer):
        spatial.validate()
        dlat = spatial.buffer_m / _M_PER_DEG_LAT
        dlon = spatial.buffer_m / (_M_PER_DEG_LAT * max(1e-6, math.cos(math.radians(spatial.lat))))
        return BBox(
            minlon=spatial.lon - dlon,
            minlat=spatial.lat - dlat,
            maxlon=spatial.lon + dlon,
            maxlat=spatial.lat + dlat,
            crs="EPSG:4326",
        )
    raise ModelError(f"Unsupported SpatialSpec type: {type(spatial)}")


def _centre_lonlat(spatial: SpatialSpec) -> tuple[float, float]:
    return centre_lonlat(spatial)


def _grid_lonlat(
    bbox: BBox, step_m: float, max_grid_points: int = 100000
) -> tuple[np.ndarray, np.ndarray]:
    """Cell-centre coordinates of a north-up grid with approximately ``step_m`` spacing."""
    lons, lats, _ = location_grid(bbox, step_m=step_m, max_grid_points=max_grid_points)
    return lons, lats


def _request_config(model_config: dict[str, Any] | None) -> tuple[dict[str, Any], str, int]:
    config = dict(model_config or {})
    unknown = set(config) - {"variant", "batch_size", "grid_step_m", "max_grid_points"}
    if unknown:
        raise ModelError(f"Unknown SatCLIP settings: {sorted(unknown)}.")
    variant = _resolve_variant(config)
    batch_size = positive_int(
        config.get("batch_size", os.environ.get("RS_EMBED_SATCLIP_CHUNK", 1024)), "batch_size"
    )
    return config, variant, batch_size


def encode_lonlat(
    lonlat: np.ndarray, *, variant: str, device: str, batch_size: int | None = None
) -> tuple[np.ndarray, dict]:
    """Encode an ``(N, 2)`` array of ``[lon, lat]`` degrees with SatCLIP."""
    import torch

    arr = validate_lonlat(lonlat)
    chunk = positive_int(
        batch_size if batch_size is not None else os.environ.get("RS_EMBED_SATCLIP_CHUNK", "65536"),
        "batch_size / RS_EMBED_SATCLIP_CHUNK",
    )
    variant = _resolve_variant({"variant": variant})
    ckpt_path, ckpt_meta = _resolve_checkpoint(variant)
    dev = _resolve_device(device)
    model, hp = _load_location_encoder(ckpt_path, dev)
    out = []
    with torch.no_grad():
        for start in range(0, len(arr), chunk):
            x = torch.from_numpy(arr[start : start + chunk]).to(device=dev, dtype=torch.float64)
            out.append(model(x).float().cpu().numpy())
    feats = np.concatenate(out, axis=0) if out else np.zeros((0, 0), np.float32)
    return feats, {"checkpoint": ckpt_meta, "hyper_parameters": hp, "device": dev}


@register("satclip")
class SatCLIPEmbedder(EmbedderBase):
    """SatCLIP location encoder: longitude/latitude only, no imagery at query time.

    Output:
      - OutputSpec.pooled(): (D,) embedding of the ROI centre coordinate
      - OutputSpec.grid():   xarray.DataArray (d, y, x) evaluated at grid-cell centres
    """

    DEFAULT_GRID_STEP_M = 1000.0

    def describe(self) -> dict[str, Any]:
        return {
            "type": "location",
            "backend": ["auto"],
            "inputs": {"spatial": "BBox or PointBuffer (EPSG:4326); no imagery"},
            "temporal": {"mode": "ignored"},
            "output": ["pooled", "grid"],
            "defaults": {
                "variant": _DEFAULT_VARIANT,
                "pooled": "centre_coordinate_query",
                "grid_step_m": self.DEFAULT_GRID_STEP_M,
            },
            "model_config": {
                "variant": {
                    "type": "string",
                    "default": _DEFAULT_VARIANT,
                    "choices": sorted(_SATCLIP_VARIANTS),
                },
                "grid_step_m": {"type": "number", "default": self.DEFAULT_GRID_STEP_M},
                "max_grid_points": {"type": "integer", "default": 100000},
                "batch_size": {"type": "integer", "default": 1024},
            },
            "notes": [
                "Class B location encoder: evaluates the location branch only; no imagery.",
                "Pooled output queries the ROI centre; OutputSpec.pooling is not applied.",
                "Spatial detail is bounded by the spherical-harmonic degree (L=10 or L=40).",
                "TemporalSpec is accepted for interface compatibility and ignored.",
                "Grid spacing is coordinate sampling distance, not image resolution.",
            ],
        }

    def get_embedding(
        self,
        *,
        spatial: SpatialSpec,
        temporal: TemporalSpec | None,
        sensor: SensorSpec | None,
        output: OutputSpec,
        backend: str,
        device: str = "auto",
        input_chw: np.ndarray | None = None,
        model_config: dict[str, Any] | None = None,
    ) -> Embedding:
        if input_chw is not None:
            raise ModelError("satclip is a location encoder and does not accept imagery input.")
        if backend != "auto":
            raise ModelError("satclip uses a local location runtime; use backend='auto'.")
        config, variant, batch_size = _request_config(model_config)
        centre = _centre_lonlat(spatial)
        bbox = _bbox_of(spatial)
        extra: dict[str, Any] = {
            "variant": variant,
            "bbox_4326": (bbox.minlon, bbox.minlat, bbox.maxlon, bbox.maxlat),
            "input_crs": "EPSG:4326",
            "coordinate_order": "longitude_latitude",
            "query_input": "longitude_latitude_only",
            "requested_temporal_ignored": temporal is not None,
        }
        if output.mode == "pooled":
            lon, lat = centre
            feats, run_meta = encode_lonlat(
                np.array([[lon, lat]]), variant=variant, device=device, batch_size=batch_size
            )
            feats = validate_features(feats, count=1, model="satclip")
            meta = build_meta(
                model=self.model_name,
                kind="location",
                backend="vendored_satclip",
                source=f"hf://{_SATCLIP_VARIANTS[variant]['repo_id']}",
                sensor=None,
                temporal=None,
                image_size=None,
                extra={**extra, **run_meta, "query_lonlat": (lon, lat)},
            )
            meta["pooling"] = "centre_coordinate_query"
            return Embedding(data=feats[0], meta=meta)
        if output.mode == "grid":
            try:
                import xarray as xr
            except Exception as e:
                raise ModelError("grid output requires xarray. Install: pip install xarray") from e
            lons, lats, step = location_grid(
                bbox,
                step_m=config.get(
                    "grid_step_m",
                    os.environ.get("RS_EMBED_SATCLIP_GRID_STEP_M", self.DEFAULT_GRID_STEP_M),
                ),
                max_grid_points=config.get("max_grid_points", 100000),
            )
            lon2, lat2 = np.meshgrid(lons, lats)
            pts = np.stack([lon2.ravel(), lat2.ravel()], axis=1)
            feats, run_meta = encode_lonlat(
                pts, variant=variant, device=device, batch_size=batch_size
            )
            feats = validate_features(feats, count=len(pts), model="satclip")
            chw = feats.reshape(len(lats), len(lons), -1).transpose(2, 0, 1)
            meta = build_meta(
                model=self.model_name,
                kind="location",
                backend="vendored_satclip",
                source=f"hf://{_SATCLIP_VARIANTS[variant]['repo_id']}",
                sensor=None,
                temporal=None,
                image_size=None,
                extra={
                    **extra,
                    **run_meta,
                    "grid_step_m": step,
                    "chw_shape": tuple(chw.shape),
                    "grid_semantics": "coordinate_queries_not_image_pixels",
                    "y_axis_direction": "north_to_south",
                },
            )
            da = xr.DataArray(
                chw,
                dims=("d", "y", "x"),
                coords={"d": np.arange(chw.shape[0]), "y": lats, "x": lons},
                name="embedding",
                attrs=meta,
            )
            return Embedding(data=da, meta=meta)
        raise ModelError(f"Unknown output mode: {output.mode}")

    def get_embeddings_batch(
        self,
        *,
        spatials: list[SpatialSpec],
        temporal: TemporalSpec | None = None,
        sensor: SensorSpec | None = None,
        output: OutputSpec = OutputSpec.pooled(),
        backend: str = "auto",
        device: str = "auto",
        model_config: dict[str, Any] | None = None,
    ) -> list[Embedding]:
        if backend != "auto":
            raise ModelError("satclip uses a local location runtime; use backend='auto'.")
        if not spatials:
            return []
        if output.mode != "pooled":
            return [
                self.get_embedding(
                    spatial=sp,
                    temporal=temporal,
                    sensor=sensor,
                    output=output,
                    backend=backend,
                    device=device,
                    model_config=model_config,
                )
                for sp in spatials
            ]
        _, variant, batch_size = _request_config(model_config)
        centres = np.array([_centre_lonlat(sp) for sp in spatials], dtype=np.float64)
        feats, run_meta = encode_lonlat(
            centres, variant=variant, device=device, batch_size=batch_size
        )
        feats = validate_features(feats, count=len(centres), model="satclip")
        out = []
        for sp, (lon, lat), vec in zip(spatials, centres, feats, strict=True):
            bbox = _bbox_of(sp)
            meta = build_meta(
                model=self.model_name,
                kind="location",
                backend="vendored_satclip",
                source=f"hf://{_SATCLIP_VARIANTS[variant]['repo_id']}",
                sensor=None,
                temporal=None,
                image_size=None,
                extra={
                    "variant": variant,
                    "bbox_4326": (bbox.minlon, bbox.minlat, bbox.maxlon, bbox.maxlat),
                    "input_crs": "EPSG:4326",
                    "coordinate_order": "longitude_latitude",
                    "query_input": "longitude_latitude_only",
                    "requested_temporal_ignored": temporal is not None,
                    "query_lonlat": (float(lon), float(lat)),
                    **run_meta,
                },
            )
            meta["pooling"] = "centre_coordinate_query"
            out.append(Embedding(data=vec, meta=meta))
        return out
