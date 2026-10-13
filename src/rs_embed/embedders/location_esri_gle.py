"""Esri Global Location Encoder using the official ArcGIS optional runtime.

The public CSV interface and the loaded runtime's device fields were checked
against the official ArcGIS API for Python 2.4.3 distribution. Model weights are
managed by Esri; this package does not redistribute them.
"""

from __future__ import annotations

from functools import lru_cache
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from tempfile import TemporaryDirectory
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

_BACKBONE = "satclip/sentinel-2_trained"
_WEIGHTS_ITEM = "716bec23b9d346e485311523107629c0"


@lru_cache(maxsize=4)
def _load_esri_gle(device: str) -> Any:
    try:
        from arcgis.learn import Embeddings
    except Exception as exc:
        raise ModelError(
            "esri_gle requires ArcGIS API for Python 2.4.3 with its compatible deep-learning "
            "dependencies. Use an Esri-supported environment; installing the arcgis wheel alone "
            f"is insufficient. Import failed with {type(exc).__name__}: {exc}. "
            "See docs/models/esri_gle.md."
        ) from exc
    try:
        runtime_version = version("arcgis")
        if runtime_version != "2.4.3":
            raise ModelError(
                f"Esri GLE currently supports the checked ArcGIS 2.4.3 runtime; found {runtime_version}. "
                "Use ArcGIS 2.4.3 with its compatible deep-learning environment."
            )
        # ArcGIS 2.4.3 chooses its device at construction and does not offer a
        # public device argument. Override its checked device hook so a CPU
        # request never allocates the checkpoint on a GPU during construction.
        # Do not change the user's process-wide arcgis.env settings.
        import torch

        class DeviceEmbeddings(Embeddings):
            def _get_device(self):
                return torch.device(device)

        encoder = DeviceEmbeddings(dataset_type="location", backbone=_BACKBONE)
        if not hasattr(encoder, "model") or not hasattr(encoder, "_device"):
            raise ModelError("Unsupported ArcGIS Embeddings runtime: missing model/device fields.")
        encoder.model.to(device).eval()
        encoder._device = torch.device(device)
        return encoder
    except ModelError:
        raise
    except Exception as exc:
        raise ModelError(
            f"Could not initialize Esri Global Location Encoder: {type(exc).__name__}: {exc}. "
            "Check ArcGIS deep-learning dependencies, model access and the Esri model terms."
        ) from exc


@register("esri_gle")
class EsriGLEEmbedder(LocationEmbedderBase):
    source = (
        "https://doc.arcgis.com/en/pretrained-models/latest/vector/"
        "introduction-to-global-location-encoder-sentinel-2-.htm"
    )
    runtime = "arcgis.learn.Embeddings"
    embedding_dim = 256

    def describe(self) -> dict[str, Any]:
        desc = super().describe()
        desc["defaults"]["backbone"] = _BACKBONE
        desc["notes"].extend(
            [
                "Esri Global Location Encoder (Sentinel-2), separate from Microsoft's SatCLIP weights.",
                "Requires the official ArcGIS API for Python and matching deep-learning environment.",
                "ArcGIS manages model downloads; Esri's own model license and access terms apply.",
                "ArcGIS 2.4.3 interface verified; actual inference requires that optional runtime.",
                "No Earth Engine or imagery request is made by this adapter.",
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
        unknown = set(config) - {"batch_size", "grid_step_m", "max_grid_points"}
        if unknown:
            raise ModelError(f"Unknown Esri GLE settings: {sorted(unknown)}.")
        dev = resolve_torch_device(device)
        encoder = _load_esri_gle(dev)
        outputs = []
        # ArcGIS get() uses file input for locations and overrides its internal
        # location batch size to 1024 in 2.4.3. Chunk files here to honor callers.
        with TemporaryDirectory(prefix="earth-embedding-esri-") as directory:
            csv_path = Path(directory) / "locations.csv"
            for start in range(0, len(arr), chunk):
                block = arr[start : start + chunk]
                np.savetxt(
                    csv_path, block, delimiter=",", header="lon,lat", comments="", fmt="%.17g"
                )
                try:
                    result = encoder.get(
                        str(csv_path),
                        batch_size=chunk,
                        show_progress=False,
                        return_embeddings=True,
                        location_column=["lon", "lat"],
                        spatial_reference=4326,
                    )
                except Exception as exc:
                    raise ModelError(
                        f"Esri GLE inference failed: {type(exc).__name__}: {exc}. "
                        "Check that this ArcGIS runtime supports location embeddings."
                    ) from exc
                outputs.append(
                    validate_features(
                        result,
                        count=len(block),
                        model=self.model_name,
                        expected_dim=self.embedding_dim,
                    )
                )
        try:
            runtime_version = version("arcgis")
        except PackageNotFoundError:
            runtime_version = "unknown"
        return np.concatenate(outputs), {
            "device": dev,
            "runtime_version": runtime_version,
            "backbone": _BACKBONE,
            "native_coordinate_order": "longitude_latitude",
            "checkpoint": {"source": "arcgis_runtime", "item_id": _WEIGHTS_ITEM},
        }
