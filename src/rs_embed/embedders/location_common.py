"""Shared coordinate-only inference, validation, and spatial output contracts."""

from __future__ import annotations

import math
from typing import Any

import numpy as np

from ..core.embedding import Embedding
from ..core.errors import ModelError
from ..core.specs import BBox, OutputSpec, PointBuffer, SensorSpec, SpatialSpec, TemporalSpec
from .base import EmbedderBase
from .meta_utils import build_meta


def validate_lonlat(lonlat: Any) -> np.ndarray:
    """Return a nonempty finite ``(N, 2)`` WGS84 array in **longitude, latitude** order."""
    try:
        arr = np.asarray(lonlat, dtype=np.float64)
    except (TypeError, ValueError) as exc:
        raise ModelError("Locations must be a numeric (N, 2) [longitude, latitude] array.") from exc
    if arr.ndim != 2 or arr.shape[1] != 2 or len(arr) == 0:
        raise ModelError("Locations must be a nonempty (N, 2) [longitude, latitude] array.")
    if not np.isfinite(arr).all():
        raise ModelError("Location coordinates must all be finite.")
    if (np.abs(arr[:, 0]) > 180).any() or (np.abs(arr[:, 1]) > 90).any():
        raise ModelError(
            "Coordinates out of range: longitude must be in [-180, 180] and latitude in [-90, 90]."
        )
    return np.ascontiguousarray(arr)


def positive_int(value: Any, name: str) -> int:
    try:
        result = int(value)
        valid = not isinstance(value, (bool, np.bool_)) and result == float(value) and result > 0
    except (TypeError, ValueError, OverflowError):
        valid = False
    if not valid:
        raise ModelError(f"{name} must be a positive integer.")
    return result


def validate_features(
    features: Any, *, count: int, model: str, expected_dim: int | None = None
) -> np.ndarray:
    try:
        arr = np.asarray(features, dtype=np.float32)
    except (TypeError, ValueError) as exc:
        raise ModelError(f"{model} returned nonnumeric embeddings.") from exc
    if arr.ndim != 2 or arr.shape[0] != count or arr.shape[1] == 0:
        raise ModelError(f"{model} returned {arr.shape}; expected ({count}, D) with D > 0.")
    if expected_dim is not None and arr.shape[1] != expected_dim:
        raise ModelError(f"{model} returned dimension {arr.shape[1]}; expected {expected_dim}.")
    if not np.isfinite(arr).all():
        raise ModelError(f"{model} returned nonfinite embeddings.")
    return arr


def resolve_torch_device(device: str) -> str:
    try:
        import torch
    except ImportError as exc:
        raise ModelError(
            "Location encoders require PyTorch. Install torch for your platform."
        ) from exc
    name = str(device or "auto").strip().lower()
    if name == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    try:
        resolved = torch.device(name)
    except (RuntimeError, ValueError) as exc:
        raise ModelError(f"Invalid PyTorch device: {device!r}.") from exc
    if resolved.type == "cuda" and not torch.cuda.is_available():
        raise ModelError(f"Requested device {name!r}, but CUDA is unavailable. Use device='cpu'.")
    return str(resolved)


def centre_lonlat(spatial: SpatialSpec) -> tuple[float, float]:
    spatial.validate()
    if isinstance(spatial, PointBuffer):
        arr = validate_lonlat([[spatial.lon, spatial.lat]])
        if not math.isfinite(spatial.buffer_m):
            raise ModelError("PointBuffer buffer_m must be finite.")
        return float(arr[0, 0]), float(arr[0, 1])
    if isinstance(spatial, BBox):
        return (spatial.minlon + spatial.maxlon) / 2, (spatial.minlat + spatial.maxlat) / 2
    raise ModelError("Location encoders accept BBox or PointBuffer spatial requests.")


def location_grid(
    bbox: BBox, *, step_m: Any, max_grid_points: Any = 100000
) -> tuple[np.ndarray, np.ndarray, float]:
    """Make a bounded north-up coordinate grid, validating before allocation.

    All location encoders use the same cell centres and ceiling convention.
    Spacing describes requested coordinate sampling, not model resolution.
    """
    bbox.validate()
    try:
        step = float(step_m)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ModelError("grid_step_m must be a finite positive number.") from exc
    if isinstance(step_m, (bool, np.bool_)) or not math.isfinite(step) or step <= 0:
        raise ModelError("grid_step_m must be a finite positive number.")
    limit = positive_int(max_grid_points, "max_grid_points")
    midlat = (bbox.minlat + bbox.maxlat) / 2
    height_m = (bbox.maxlat - bbox.minlat) * 111320.0
    width_m = (bbox.maxlon - bbox.minlon) * 111320.0 * math.cos(math.radians(midlat))
    # Check before division/ceil too: a finite subnormal step can overflow
    # dimension arithmetic, long before numpy gets a chance to reject allocation.
    if step < max(height_m, width_m) / limit:
        raise ModelError(
            f"Requested grid exceeds max_grid_points={limit}. "
            "Increase grid_step_m or explicitly raise max_grid_points."
        )
    ny = max(1, math.ceil(height_m / step))
    nx = max(1, math.ceil(width_m / step))
    if nx * ny > limit:
        raise ModelError(
            f"Requested grid has {nx * ny} points, exceeding max_grid_points={limit}. "
            "Increase grid_step_m or explicitly raise max_grid_points."
        )
    lons = bbox.minlon + (np.arange(nx) + 0.5) * (bbox.maxlon - bbox.minlon) / nx
    lats = bbox.maxlat - (np.arange(ny) + 0.5) * (bbox.maxlat - bbox.minlat) / ny
    return lons, lats, step


class LocationEmbedderBase(EmbedderBase):
    """Coordinate model contract with batched centre queries and bounded query grids."""

    source: str = ""
    runtime: str = ""
    embedding_dim: int = 0

    def describe(self) -> dict[str, Any]:
        return {
            "type": "location",
            "backend": ["auto"],
            "inputs": {"spatial": "BBox or PointBuffer (EPSG:4326); no imagery"},
            "temporal": {"mode": "ignored"},
            "output": ["pooled", "grid"],
            "embedding_dim": self.embedding_dim,
            "defaults": {"pooled": "centre_coordinate_query", "grid_step_m": 1000.0},
            "model_config": {
                "batch_size": {"type": "integer", "default": 1024},
                "grid_step_m": {"type": "number", "default": 1000.0},
                "max_grid_points": {"type": "integer", "default": 100000},
            },
            "notes": [
                "Coordinates are longitude, latitude in WGS84 degrees; no imagery or EE needed.",
                "Pooled output queries the ROI centre; pooling is not applied.",
                "TemporalSpec is ignored: these embeddings do not represent a requested date.",
                "Grid spacing is query sampling distance, not the model's physical resolution.",
            ],
        }

    def encode_locations(
        self,
        lonlat: np.ndarray,
        *,
        device: str,
        batch_size: int,
        model_config: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        raise NotImplementedError

    def _meta(self, run_meta: dict[str, Any], **extra: Any) -> dict[str, Any]:
        return build_meta(
            model=self.model_name,
            kind="location",
            backend=self.runtime,
            source=self.source,
            sensor=None,
            temporal=None,
            image_size=None,
            extra={
                "input_crs": "EPSG:4326",
                "coordinate_order": "longitude_latitude",
                "query_input": "longitude_latitude_only",
                **run_meta,
                **extra,
            },
        )

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
            raise ModelError(
                f"{self.model_name} is a location encoder and does not accept imagery."
            )
        if backend != "auto":
            raise ModelError(
                f"{self.model_name} uses a local location runtime; use backend='auto'."
            )
        centre = centre_lonlat(spatial)
        config = model_config or {}
        batch_size = positive_int(config.get("batch_size", 1024), "batch_size")
        if output.mode == "pooled":
            feats, run_meta = self.encode_locations(
                np.array([centre]), device=device, batch_size=batch_size, model_config=config
            )
            feats = validate_features(feats, count=1, model=self.model_name)
            meta = self._meta(
                run_meta,
                query_lonlat=centre,
                pooling="centre_coordinate_query",
                requested_temporal_ignored=temporal is not None,
            )
            return Embedding(data=feats[0], meta=meta)
        if output.mode != "grid":
            raise ModelError(f"Unsupported location output mode: {output.mode!r}.")
        try:
            import xarray as xr
        except ImportError as exc:
            raise ModelError("Grid output requires xarray: pip install xarray") from exc
        from .location_satclip import _bbox_of

        bbox = _bbox_of(spatial)
        lons, lats, step = location_grid(
            bbox,
            step_m=config.get("grid_step_m", 1000.0),
            max_grid_points=config.get("max_grid_points", 100000),
        )
        ny, nx = len(lats), len(lons)
        lon2, lat2 = np.meshgrid(lons, lats)
        points = np.column_stack((lon2.ravel(), lat2.ravel()))
        feats, run_meta = self.encode_locations(
            points, device=device, batch_size=batch_size, model_config=config
        )
        feats = validate_features(feats, count=len(points), model=self.model_name)
        chw = feats.reshape(ny, nx, -1).transpose(2, 0, 1)
        meta = self._meta(
            run_meta,
            requested_temporal_ignored=temporal is not None,
            grid_step_m=step,
            grid_semantics="coordinate_queries_not_image_pixels",
            y_axis_direction="north_to_south",
            bbox_4326=(bbox.minlon, bbox.minlat, bbox.maxlon, bbox.maxlat),
            chw_shape=tuple(chw.shape),
        )
        data = xr.DataArray(
            chw,
            dims=("d", "y", "x"),
            coords={"d": np.arange(chw.shape[0]), "y": lats, "x": lons},
            name="embedding",
            attrs=meta,
        )
        return Embedding(data=data, meta=meta)

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
            raise ModelError(
                f"{self.model_name} uses a local location runtime; use backend='auto'."
            )
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
        points = np.array([centre_lonlat(sp) for sp in spatials])
        config = model_config or {}
        feats, run_meta = self.encode_locations(
            points,
            device=device,
            batch_size=positive_int(config.get("batch_size", 1024), "batch_size"),
            model_config=config,
        )
        feats = validate_features(feats, count=len(points), model=self.model_name)
        return [
            Embedding(
                data=vec,
                meta=self._meta(
                    run_meta,
                    query_lonlat=tuple(point),
                    pooling="centre_coordinate_query",
                    requested_temporal_ignored=temporal is not None,
                ),
            )
            for point, vec in zip(points, feats, strict=True)
        ]
