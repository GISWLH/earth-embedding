"""Esri GLE's official small checkpoint on the MIT SatCLIP location runtime."""

from __future__ import annotations

import hashlib
import io
import os
import tempfile
import urllib.request
import zipfile
from functools import lru_cache
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

_BACKBONE = "satclip/sentinel-2_trained"
_MODEL_ITEM = "b0664ef297c04d4aaa44191cf21e07f3"
_WEIGHTS_URL = f"https://www.arcgis.com/sharing/rest/content/items/{_MODEL_ITEM}/data"
_WEIGHTS_SHA256 = "2d5b8ac88b4a7f210a00f7fbe145f5216987f373062ec71f3065f9ba13b15452"
_WEIGHTS_BYTES = 2168415
_MAX_DOWNLOAD_BYTES = 16 * 1024 * 1024


def _verified_weights(raw: bytes) -> bytes:
    """Read only tensors from the package; never execute its bundled Python code."""
    if zipfile.is_zipfile(io.BytesIO(raw)):
        with zipfile.ZipFile(io.BytesIO(raw)) as package:
            # PyTorch .pth files are also ZIP archives, but have no satclip.pth member.
            if "satclip.pth" in package.namelist():
                if package.getinfo("satclip.pth").file_size != _WEIGHTS_BYTES:
                    raise ModelError("Esri GLE package contains an unexpected checkpoint size.")
                raw = package.read("satclip.pth")
    digest = hashlib.sha256(raw).hexdigest()
    if digest != _WEIGHTS_SHA256:
        raise ModelError(
            "Esri GLE checkpoint SHA-256 mismatch. Use the official Sentinel-2 "
            "satclip.pth or .dlpk; Microsoft SatCLIP and modified weights are not interchangeable. "
            f"Expected {_WEIGHTS_SHA256}, received {digest}."
        )
    return raw


def _resolve_checkpoint(config: dict[str, Any]) -> tuple[bytes, dict[str, Any]]:
    checkpoint = config.get("checkpoint") or os.environ.get("RS_EMBED_ESRI_GLE_CKPT")
    local_only = config.get("local_files_only", False)
    if not isinstance(local_only, bool):
        raise ModelError("local_files_only must be a boolean.")
    cache = Path(config.get("cache_dir") or Path.home() / ".cache/earth_embedding/esri_gle")
    path = Path(checkpoint).expanduser() if checkpoint else cache.expanduser() / "satclip.pth"
    if path.is_file():
        if path.stat().st_size > _MAX_DOWNLOAD_BYTES:
            raise ModelError("Esri GLE checkpoint exceeds the expected small package size.")
        raw = _verified_weights(path.read_bytes())
    elif checkpoint:
        raise ModelError(f"Esri GLE checkpoint does not exist: {path}")
    elif local_only:
        raise ModelError(
            f"Esri GLE checkpoint not found in cache: {path}. "
            "Set checkpoint= to an official .dlpk/.pth or allow its first download "
            "with local_files_only=False."
        )
    else:
        try:
            request = urllib.request.Request(
                _WEIGHTS_URL, headers={"User-Agent": "earth-embedding"}
            )
            with urllib.request.urlopen(request, timeout=60) as response:
                package = response.read(_MAX_DOWNLOAD_BYTES + 1)
            if len(package) > _MAX_DOWNLOAD_BYTES:
                raise ModelError("Esri GLE download exceeds the expected small package size.")
            raw = _verified_weights(package)
        except ModelError:
            raise
        except Exception as exc:
            raise ModelError(
                "Could not download Esri GLE's official model package. "
                "Supply a downloaded .dlpk/.pth via checkpoint= for offline use. "
                f"{type(exc).__name__}: {exc}"
            ) from exc
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                dir=path.parent, suffix=".tmp", delete=False
            ) as stream:
                temporary = Path(stream.name)
                stream.write(raw)
            os.replace(temporary, path)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    return raw, {
        "source": "local_override" if checkpoint else "esri_official_cache",
        "item_id": _MODEL_ITEM,
        "url": _WEIGHTS_URL,
        "path": str(path.resolve()),
        "sha256": _WEIGHTS_SHA256,
        "bytes": len(raw),
    }


@lru_cache(maxsize=4)
def _load_esri_gle(device: str, weights: bytes) -> Any:
    import torch

    from ._vendor.satclip import LocationEncoder, get_neural_network, get_positional_encoding

    # Matches the official DLPK: L40 analytic harmonics, two 256-wide SIREN
    # hidden layers, w0_initial=30, w0=1, float64 inference, raw 256-D output.
    posenc = get_positional_encoding("sphericalharmonics", 40, "analytic")
    nnet = get_neural_network("siren", posenc.embedding_dim, 256, 256, 2)
    model = LocationEncoder(posenc, nnet).double()
    try:
        state = torch.load(io.BytesIO(weights), map_location="cpu", weights_only=True)
        model.load_state_dict(state, strict=True)
    except Exception as exc:
        raise ModelError(f"Could not load the official Esri GLE state dictionary: {exc}") from exc
    return model.to(device).eval()


@register("esri_gle")
class EsriGLEEmbedder(LocationEmbedderBase):
    source = "https://doc.arcgis.com/en/pretrained-models/latest/vector/introduction-to-global-location-encoder-sentinel-2-.htm"
    runtime = "vendored_satclip"
    embedding_dim = 256

    def describe(self) -> dict[str, Any]:
        desc = super().describe()
        desc["backbone"] = _BACKBONE
        desc["model_config"].update(
            checkpoint={"type": "string", "default": None},
            cache_dir={"type": "string", "default": "~/.cache/earth_embedding/esri_gle"},
            local_files_only={"type": "boolean", "default": False},
        )
        desc["notes"].extend(
            [
                "Official Esri weights (2.17 MB), direct PyTorch inference; no ArcGIS/ArcPy required.",
                "Downloads the official public model package on first use and caches its weights.",
                "Esri model terms apply separately; weights are not redistributed by this library.",
                "Float64 inference matches the official architecture; returns raw float32 vectors.",
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
        unknown = set(config) - {
            "checkpoint",
            "cache_dir",
            "local_files_only",
            "batch_size",
            "grid_step_m",
            "max_grid_points",
        }
        if unknown:
            raise ModelError(f"Unknown Esri GLE settings: {sorted(unknown)}.")
        dev = resolve_torch_device(device)
        if dev.split(":", 1)[0] == "mps":
            raise ModelError(
                "Esri GLE uses float64 inference, which MPS does not support. Use device='cpu'."
            )
        weights, provenance = _resolve_checkpoint(config)
        model = _load_esri_gle(dev, weights)
        import torch

        outputs = []
        with torch.inference_mode():
            for start in range(0, len(arr), chunk):
                coords = torch.from_numpy(arr[start : start + chunk]).to(dev)
                outputs.append(model(coords).float().cpu().numpy())
        features = validate_features(
            np.concatenate(outputs), count=len(arr), model=self.model_name, expected_dim=256
        )
        return features, {
            "device": dev,
            "runtime_version": str(torch.__version__),
            "backbone": _BACKBONE,
            "native_coordinate_order": "longitude_latitude",
            "inference_dtype": "float64",
            "normalization": "none",
            "checkpoint": provenance,
        }
