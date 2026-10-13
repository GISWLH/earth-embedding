import numpy as np
import pytest

from rs_embed.core import registry
from rs_embed.core.embedding import Embedding
from rs_embed.core.specs import (
    FetchSpec,
    InputPrepSpec,
    ModelInputSpec,
    OutputSpec,
    PointBuffer,
    SensorSpec,
    TemporalSpec,
)
from rs_embed.embedders.base import EmbedderBase
from rs_embed.tools.runtime import get_embedder_bundle_cached


@pytest.fixture(autouse=True)
def clean_registry():
    registry._REGISTRY.clear()
    get_embedder_bundle_cached.cache_clear()
    yield
    registry._REGISTRY.clear()
    get_embedder_bundle_cached.cache_clear()


def test_base_fetch_input_honors_sensor_overrides(monkeypatch):
    captured = {}

    class DummySpecEmbedder(EmbedderBase):
        model_name = "dummy_spec_fetch"
        input_spec = ModelInputSpec(
            collection="SPEC/COLL",
            bands=("B1", "B2"),
            scale_m=30,
            cloudy_pct=30,
            composite="median",
            fill_value=0.0,
        )

        def describe(self):
            return {"type": "onthefly"}

    def _fake_fetch_collection_patch_chw(
        provider,
        *,
        spatial,
        temporal,
        collection,
        bands,
        scale_m,
        cloudy_pct,
        composite,
        fill_value,
    ):
        captured.update(
            {
                "collection": collection,
                "bands": bands,
                "scale_m": scale_m,
                "cloudy_pct": cloudy_pct,
                "composite": composite,
                "fill_value": fill_value,
            }
        )
        return np.ones((2, 4, 4), dtype=np.float32)

    monkeypatch.setattr(
        "rs_embed.embedders.runtime_utils.fetch_collection_patch_chw",
        _fake_fetch_collection_patch_chw,
    )

    out = DummySpecEmbedder().fetch_input(
        object(),
        spatial=PointBuffer(lon=0.0, lat=0.0, buffer_m=10.0),
        temporal=None,
        sensor=SensorSpec(
            collection="OVERRIDE/COLL",
            bands=("X", "Y"),
            scale_m=77,
            cloudy_pct=5,
            composite="mosaic",
            fill_value=-1.0,
        ),
    )

    assert out is not None
    assert out.data.shape == (2, 4, 4)
    assert captured == {
        "collection": "OVERRIDE/COLL",
        "bands": ("X", "Y"),
        "scale_m": 77,
        "cloudy_pct": 5,
        "composite": "mosaic",
        "fill_value": -1.0,
    }


def test_tile_input_prep_honors_fetch_scale_override(monkeypatch):
    import rs_embed.api as api

    captured = {"scale_m": []}

    class DummyProvider:
        def ensure_ready(self):
            return None

    @registry.register("mock_spec_fetch")
    class DummySpecFetchEmbedder(EmbedderBase):
        model_name = "mock_spec_fetch"
        input_spec = ModelInputSpec(
            collection="SPEC/COLL",
            bands=("B1",),
            scale_m=30,
            cloudy_pct=30,
            composite="median",
            fill_value=0.0,
            image_size=4,
        )

        def describe(self):
            return {
                "type": "onthefly",
                "backend": ["provider"],
                "output": ["pooled"],
                "inputs": {"collection": "SPEC/COLL", "bands": ["B1"]},
                "defaults": {
                    "scale_m": 30,
                    "cloudy_pct": 30,
                    "composite": "median",
                    "fill_value": 0.0,
                    "image_size": 4,
                },
            }

        def get_embedding(
            self,
            *,
            spatial,
            temporal,
            sensor,
            output,
            backend,
            device="auto",
            input_chw=None,
        ):
            x = np.asarray(input_chw, dtype=np.float32)
            return Embedding(
                data=np.array([float(x.mean())], dtype=np.float32),
                meta={"seen_hw": list(x.shape[-2:])},
            )

    def _fake_fetch_collection_patch_chw(
        provider,
        *,
        spatial,
        temporal,
        collection,
        bands,
        scale_m,
        cloudy_pct,
        composite,
        fill_value,
    ):
        captured["scale_m"].append(int(scale_m))
        return np.ones((1, 8, 8), dtype=np.float32)

    monkeypatch.setattr(
        "rs_embed.tools.runtime._create_default_gee_provider",
        lambda: DummyProvider(),
    )
    monkeypatch.setattr(
        "rs_embed.embedders.runtime_utils.fetch_collection_patch_chw",
        _fake_fetch_collection_patch_chw,
    )

    emb = api.get_embedding(
        "mock_spec_fetch",
        spatial=PointBuffer(lon=0.0, lat=0.0, buffer_m=100.0),
        temporal=TemporalSpec.range("2020-01-01", "2020-02-01"),
        output=OutputSpec.pooled(),
        backend="gee",
        input_prep=InputPrepSpec.tile(tile_size=4, max_tiles=9),
        fetch=FetchSpec(scale_m=77),
    )

    assert captured["scale_m"] == [77]
    assert emb.meta["input_prep"]["resolved_mode"] == "tile"
    assert emb.meta["input_prep"]["tile_count"] == 4
