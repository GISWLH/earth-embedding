"""The public ROI API samples identical bounded coordinates for all location encoders."""

import numpy as np
import pytest

from rs_embed import (
    BBox,
    OutputSpec,
    PointBuffer,
    get_embedding,
    get_embeddings_batch,
    reset_runtime,
)
from rs_embed.core.errors import ModelError
from rs_embed.embedders.location_common import location_grid
from rs_embed.embedders.location_esri_gle import EsriGLEEmbedder
from rs_embed.embedders.location_geoclip import GeoCLIPEmbedder

MODELS = ("satclip", "geoclip", "esri_gle")
ROI = BBox(114.35, 30.46, 114.43, 30.54)


@pytest.fixture
def coordinate_runtimes(monkeypatch):
    import rs_embed.embedders.location_satclip as satclip

    reset_runtime()
    calls = []

    def features(model, points, batch_size):
        calls.append((model, np.array(points), batch_size))
        return np.column_stack((points, points.sum(axis=1))).astype(np.float32), {}

    def satclip_encode(points, *, variant, device, batch_size=None):
        return features("satclip", points, batch_size)

    def other_encode(self, points, *, device, batch_size, model_config=None):
        return features(self.model_name, points, batch_size)

    monkeypatch.setattr(satclip, "encode_lonlat", satclip_encode)
    monkeypatch.setattr(GeoCLIPEmbedder, "encode_locations", other_encode)
    monkeypatch.setattr(EsriGLEEmbedder, "encode_locations", other_encode)
    yield calls
    reset_runtime()


def test_all_three_public_models_use_same_320m_grid_and_batch_size(
    coordinate_runtimes, monkeypatch
):
    pytest.importorskip("xarray")
    # An explicit setting must win over legacy SatCLIP environment settings.
    monkeypatch.setenv("RS_EMBED_SATCLIP_GRID_STEP_M", "10")
    outputs = [
        get_embedding(
            model,
            spatial=ROI,
            output=OutputSpec.grid(),
            grid_step_m=320,
            max_grid_points=1000,
            batch_size=37,
        )
        for model in MODELS
    ]
    for output in outputs:
        assert output.data.shape == (3, 28, 24)
        assert output.meta["grid_step_m"] == 320
        assert output.meta["grid_semantics"] == "coordinate_queries_not_image_pixels"
        assert output.meta["y_axis_direction"] == "north_to_south"
        assert np.all(np.diff(output.data.x) > 0)
        assert np.all(np.diff(output.data.y) < 0)
        np.testing.assert_array_equal(output.data, outputs[0].data)
    assert [call[0] for call in coordinate_runtimes] == list(MODELS)
    assert all(points.shape == (672, 2) for _, points, _ in coordinate_runtimes)
    assert all(size == 37 for _, _, size in coordinate_runtimes)
    for _, points, _ in coordinate_runtimes[1:]:
        np.testing.assert_array_equal(points, coordinate_runtimes[0][1])


def test_location_default_grid_spacing_is_consistent(coordinate_runtimes, monkeypatch):
    pytest.importorskip("xarray")
    monkeypatch.delenv("RS_EMBED_SATCLIP_GRID_STEP_M", raising=False)
    for model in MODELS:
        result = get_embedding(model, spatial=ROI, output=OutputSpec.grid())
        assert result.meta["grid_step_m"] == 1000
        assert result.data.shape == (3, 9, 8)


@pytest.mark.parametrize("model", MODELS)
@pytest.mark.parametrize("step", [0, -1, np.nan, np.inf, True, "invalid"])
def test_invalid_spacing_never_calls_encoder(model, step, coordinate_runtimes):
    with pytest.raises(ModelError, match="grid_step_m"):
        get_embedding(model, spatial=ROI, output=OutputSpec.grid(), grid_step_m=step)
    assert not coordinate_runtimes


@pytest.mark.parametrize("model", MODELS)
@pytest.mark.parametrize("step", [1, 5e-324])
def test_oversized_or_underflow_grid_is_rejected_before_encoding(model, step, coordinate_runtimes):
    with pytest.raises(ModelError, match="max_grid_points"):
        get_embedding(
            model, spatial=ROI, output=OutputSpec.grid(), grid_step_m=step, max_grid_points=1000
        )
    assert not coordinate_runtimes


@pytest.mark.parametrize("limit", [0, -1, True, 1.5, np.inf])
def test_grid_point_limit_must_be_positive_integer(limit):
    with pytest.raises(ModelError, match="max_grid_points"):
        location_grid(ROI, step_m=320, max_grid_points=limit)


def test_satclip_legacy_spacing_environment_is_still_supported(coordinate_runtimes, monkeypatch):
    monkeypatch.setenv("RS_EMBED_SATCLIP_GRID_STEP_M", "320")
    result = get_embedding("satclip", spatial=ROI, output=OutputSpec.grid())
    assert result.data.shape == (3, 28, 24)
    assert result.meta["grid_step_m"] == 320


def test_satclip_pooled_batch_honors_chunk_and_rejects_invalid_config(coordinate_runtimes):
    results = get_embeddings_batch(
        "satclip", spatials=[ROI, ROI], output=OutputSpec.pooled(), batch_size=7
    )
    assert len(results) == 2
    assert coordinate_runtimes[-1][2] == 7
    with pytest.raises(ModelError, match="Unknown SatCLIP settings"):
        get_embedding("satclip", spatial=ROI, grid_step_typo=320)
    assert len(coordinate_runtimes) == 1


@pytest.mark.parametrize("model", MODELS)
def test_nonfinite_point_buffer_is_rejected_before_encoding(model, coordinate_runtimes):
    with pytest.raises(ModelError, match="finite"):
        get_embedding(model, spatial=PointBuffer(114.4, 30.5, float("inf")))
    assert not coordinate_runtimes
