from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

import numpy as np

from ..core.embedding import Embedding
from ..core.errors import ModelError
from ..core.registry import register
from ..core.specs import OutputSpec, SensorSpec, SpatialSpec, TemporalSpec
from .base import EmbedderBase
from .meta_utils import build_meta
from .runtime_utils import (
    fetch_collection_patch_all_bands_chw as _fetch_collection_patch_all_bands_chw,
)
from .runtime_utils import (
    is_provider_backend,
)


@register("gse")
class GSEAnnualEmbedder(EmbedderBase):
    """
    Precomputed embeddings on Provider:
      ImageCollection("GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL")
    """

    DEFAULT_BATCH_WORKERS = 4
    _allow_auto_backend = True

    def describe(self) -> dict[str, Any]:
        return {
            "type": "precomputed",
            "backend": ["provider"],
            "temporal": {"mode": "year"},
            "output": ["grid", "pooled"],
            "source": "GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL",
            "defaults": {
                "scale_m": 10,
                "fill_value": -9999.0,
                "composite": "mosaic",
            },
            "notes": "Uses sampleRectangle in EPSG:3857; returns [C,H,W] or pooled [C].",
        }

    @staticmethod
    def _resolve_batch_workers(n_items: int) -> int:
        v = int(
            os.environ.get(
                "RS_EMBED_GSE_BATCH_WORKERS",
                str(GSEAnnualEmbedder.DEFAULT_BATCH_WORKERS),
            )
        )
        return max(1, min(int(n_items), v))

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
    ) -> Embedding:
        if not is_provider_backend(backend, allow_auto=True):
            raise ModelError("gse_annual expects a provider backend (or 'auto').")
        if temporal is None:
            raise ModelError("gse_annual requires TemporalSpec.year(year=...).")
        temporal.validate()
        if temporal.mode != "year":
            raise ModelError("gse_annual only supports TemporalSpec.year in v0.1.")

        scale_m = int(getattr(sensor, "scale_m", 10) if sensor is not None else 10)

        provider = self._get_provider(backend)
        emb_chw, band_names = _fetch_collection_patch_all_bands_chw(
            provider,
            spatial=spatial,
            temporal=temporal,
            collection="GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL",
            scale_m=scale_m,
            fill_value=-9999.0,
            composite="mosaic",
        )
        emb_chw = np.asarray(emb_chw, dtype=np.float32)
        emb_chw[emb_chw == -9999] = np.nan
        valid_pixel_fraction = float(np.isfinite(emb_chw).mean()) if emb_chw.size else 0.0

        meta = build_meta(
            model=self.model_name,
            kind="precomputed",
            backend=str(backend).lower(),
            source="GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL",
            sensor=None,
            temporal=temporal,
            image_size=None,
            extra={
                "year": temporal.year,
                "scale_m": scale_m,
                "bands": band_names,
                "valid_pixel_fraction": valid_pixel_fraction,
            },
        )

        if output.mode == "pooled":
            if output.pooling == "mean":
                valid = np.isfinite(emb_chw)
                sums = np.where(valid, emb_chw, 0.0).sum(axis=(-2, -1), dtype=np.float64)
                counts = valid.sum(axis=(-2, -1))
                vec = np.divide(
                    sums,
                    counts,
                    out=np.full_like(sums, np.nan, dtype=np.float64),
                    where=counts > 0,
                ).astype(np.float32)
            elif output.pooling == "max":
                valid = np.isfinite(emb_chw)
                masked = np.where(valid, emb_chw, -np.inf)
                vec = masked.max(axis=(-2, -1)).astype(np.float32)
                vec[~valid.any(axis=(-2, -1))] = np.nan
            else:
                raise ModelError(f"Unknown pooling='{output.pooling}' (expected 'mean' or 'max').")
            return Embedding(data=vec, meta={**meta, "pooling": output.pooling})

        # grid: return xarray with dims (band,y,x)
        try:
            import xarray as xr
        except Exception as e:
            raise ModelError("grid output requires xarray. Install: pip install xarray") from e
        da = xr.DataArray(
            emb_chw,
            dims=("d", "y", "x"),
            coords={"d": list(band_names)},
            name="embedding",
            attrs=meta,
        )
        return Embedding(data=da, meta=meta)

    def get_embeddings_batch(
        self,
        *,
        spatials: list[SpatialSpec],
        temporal: TemporalSpec | None = None,
        sensor: SensorSpec | None = None,
        output: OutputSpec = OutputSpec.pooled(),
        backend: str = "auto",
        device: str = "auto",
    ) -> list[Embedding]:
        if not spatials:
            return []
        if not is_provider_backend(backend, allow_auto=True):
            raise ModelError("gse_annual expects a provider backend (or 'auto').")

        n = len(spatials)
        out: list[Embedding | None] = [None] * n

        def _one(i: int, sp: SpatialSpec) -> tuple[int, Embedding]:
            emb = self.get_embedding(
                spatial=sp,
                temporal=temporal,
                sensor=sensor,
                output=output,
                backend=backend,
                device=device,
            )
            return i, emb

        mw = self._resolve_batch_workers(n)
        if mw == 1:
            for i, sp in enumerate(spatials):
                _, emb = _one(i, sp)
                out[i] = emb
        else:
            with ThreadPoolExecutor(max_workers=mw) as ex:
                futs = [ex.submit(_one, i, sp) for i, sp in enumerate(spatials)]
                for fut in as_completed(futs):
                    i, emb = fut.result()
                    out[i] = emb

        if any(e is None for e in out):
            raise ModelError("gse_annual batch failed to produce all outputs.")
        return [e for e in out if e is not None]
