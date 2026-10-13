"""GeoCLIP's official pretrained GPS branch (no image model instantiated)."""

from __future__ import annotations

import os
from functools import lru_cache
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

import numpy as np

from ..core.errors import ModelError
from ..core.registry import register
from .location_common import (
    LocationEmbedderBase,
    positive_int,
    resolve_torch_device,
    validate_features,
    validate_lonlat,
)


@lru_cache(maxsize=4)
def _load_geoclip(device: str, checkpoint: str | None) -> Any:
    try:
        from geoclip import LocationEncoder
    except ImportError as exc:
        raise ModelError(
            "GeoCLIP requires its official optional package: pip install 'geoclip==1.2.3'. "
            "See docs/models/geoclip.md for setup."
        ) from exc
    try:
        model = LocationEncoder(from_pretrained=checkpoint is None)
        if checkpoint is not None:
            import torch

            # Official GeoCLIP checkpoint is a plain location-encoder state_dict.
            state = torch.load(checkpoint, map_location="cpu", weights_only=True)
            model.load_state_dict(state, strict=True)
        return model.to(device).eval()
    except Exception as exc:
        raise ModelError(
            f"Could not load GeoCLIP's pretrained location encoder: {type(exc).__name__}: {exc}. "
            "Use the official location_encoder_weights.pth state dictionary for checkpoint=."
        ) from exc


@register("geoclip")
class GeoCLIPEmbedder(LocationEmbedderBase):
    source = "https://github.com/VicenteVivan/geo-clip"
    runtime = "geoclip"
    embedding_dim = 512

    def describe(self) -> dict[str, Any]:
        desc = super().describe()
        desc["model_config"]["checkpoint"] = {"type": "string", "default": None}
        desc["notes"].extend(
            [
                "Official GeoCLIP location branch, trained with geotagged ground-level photographs.",
                "The adapter converts longitude/latitude to GeoCLIP's native latitude/longitude.",
                "Requires optional geoclip package; packaged pretrained weights are used by default.",
                "Raw pretrained features are returned without L2 normalization.",
            ]
        )
        return desc

    def encode_locations(
        self,
        lonlat: np.ndarray,
        *,
        device: str = "auto",
        batch_size: int = 1024,
        model_config: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        arr = validate_lonlat(lonlat)
        chunk = positive_int(batch_size, "batch_size")
        config = model_config or {}
        unknown = set(config) - {"checkpoint", "batch_size", "grid_step_m", "max_grid_points"}
        if unknown:
            raise ModelError(f"Unknown GeoCLIP settings: {sorted(unknown)}.")
        checkpoint = config.get("checkpoint") or os.environ.get("RS_EMBED_GEOCLIP_CKPT")
        if checkpoint is not None:
            checkpoint = str(Path(checkpoint).expanduser().resolve())
            if not Path(checkpoint).is_file():
                raise ModelError(f"GeoCLIP checkpoint does not exist: {checkpoint}")
        dev = resolve_torch_device(device)
        model = _load_geoclip(dev, checkpoint)
        import torch

        outputs = []
        with torch.inference_mode():
            for start in range(0, len(arr), chunk):
                # Public API is GIS order; upstream explicitly requires latitude first.
                latlon = np.ascontiguousarray(arr[start : start + chunk, ::-1], dtype=np.float32)
                tensor = torch.from_numpy(latlon).to(dev)
                outputs.append(model(tensor).float().cpu().numpy())
        features = validate_features(
            np.concatenate(outputs),
            count=len(arr),
            model=self.model_name,
            expected_dim=self.embedding_dim,
        )
        try:
            runtime_version = version("geoclip")
        except PackageNotFoundError:
            runtime_version = "unknown"
        return features, {
            "device": dev,
            "runtime_version": runtime_version,
            "native_coordinate_order": "latitude_longitude",
            "normalization": "none",
            "checkpoint": {
                "source": "local_override" if checkpoint else "geoclip_package",
                "path": checkpoint or "geoclip/model/weights/location_encoder_weights.pth",
            },
        }
