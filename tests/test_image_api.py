from __future__ import annotations

import numpy as np
import pytest

from rs_embed import image as image_api
from rs_embed.core.embedding import Embedding
from rs_embed.core.errors import ModelError
from rs_embed.core.specs import PointBuffer, SensorSpec, TemporalSpec


@pytest.fixture
def context():
    return {
        "spatial": PointBuffer(114.35, 30.5, 320),
        "temporal": TemporalSpec.range("2021-01-01", "2022-01-01"),
    }


def test_supplied_image_forwards_raw_values_and_context_without_fetch(monkeypatch, context):
    seen = {}
    sensor = SensorSpec(collection="synthetic", bands=("B4", "B3", "B2"))

    class FakeEncoder:
        def get_embedding(self, **kwargs):
            seen.update(kwargs)
            return Embedding(np.ones(4, dtype=np.float32), {"checkpoint": "test-double"})

    monkeypatch.setattr(image_api, "get_embedder_cls", lambda model: FakeEncoder)
    monkeypatch.setattr(image_api, "default_sensor_for_model", lambda model: sensor)
    pixels = np.full((3, 8, 8), 1000, dtype=np.uint16)
    result = image_api.get_image_embedding("satmae_rgb", pixels, **context, device="cpu")
    assert seen["sensor"] is sensor
    assert seen["spatial"] is context["spatial"]
    assert seen["temporal"] is context["temporal"]
    assert seen["input_chw"].dtype == np.float32
    np.testing.assert_array_equal(seen["input_chw"], pixels)
    assert seen["backend"] == "auto"
    assert result.meta["input_source"] == "user_array"
    assert result.meta["checkpoint"] == "test-double"


@pytest.mark.parametrize(
    "model", ["satclip", "geoclip", "esri_gle", "gse", "tessera", "copernicus"]
)
def test_non_image_models_fail_before_runtime_loading(model, context):
    with pytest.raises(ModelError, match="not an image encoder"):
        image_api.get_image_embedding(model, np.ones((3, 4, 4)), **context)


@pytest.mark.parametrize(
    "pixels",
    [
        np.ones((3, 0, 4)),
        np.ones((1, 3, 4, 4)),
        np.ones((4, 4)),
        np.full((3, 4, 4), np.nan),
        np.full((3, 4, 4), np.inf),
        np.ones((3, 4, 4), complex),
    ],
)
def test_invalid_image_fails_before_runtime_loading(pixels, context):
    with pytest.raises(ModelError):
        image_api.get_image_embedding("satmae", pixels, **context)


def test_band_mismatch_is_explicit(monkeypatch, context):
    monkeypatch.setattr(
        image_api,
        "default_sensor_for_model",
        lambda model: SensorSpec(collection="synthetic", bands=("B4", "B3", "B2")),
    )
    with pytest.raises(ModelError, match="expects 3 channels"):
        image_api.get_image_embedding("satmae", np.ones((4, 4, 4)), **context)


def test_multitemporal_frames_are_preserved_and_config_forwarded(monkeypatch, context):
    seen = {}

    class FakeEncoder:
        def get_embedding(self, **kwargs):
            seen.update(kwargs)
            return Embedding(np.ones(4), {})

    monkeypatch.setattr(image_api, "get_embedder_cls", lambda model: FakeEncoder)
    monkeypatch.setattr(image_api, "default_sensor_for_model", lambda model: None)
    pixels = np.arange(2 * 10 * 4 * 4).reshape(2, 10, 4, 4)
    image_api.get_image_embedding("anysat", pixels, **context, model_config={"n_frames": 2})
    np.testing.assert_array_equal(seen["input_chw"], pixels)
    assert seen["model_config"] == {"n_frames": 2}


def test_model_config_is_not_silently_ignored(monkeypatch, context):
    class LegacyEncoder:
        def get_embedding(self, input_chw):
            pytest.fail("Unsupported configuration reached inference")

    monkeypatch.setattr(image_api, "get_embedder_cls", lambda model: LegacyEncoder)
    monkeypatch.setattr(image_api, "default_sensor_for_model", lambda model: None)
    with pytest.raises(ModelError, match="does not accept model_config"):
        image_api.get_image_embedding(
            "satmae", np.ones((3, 4, 4)), **context, model_config={"variant": "invalid"}
        )
