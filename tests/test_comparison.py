"""No-network contracts for multi-model requests and honest comparison plots."""

from __future__ import annotations

import json

import numpy as np
import pytest

import rs_embed.comparison as comparison
from rs_embed import BBox, OutputSpec, TemporalSpec
from rs_embed.core.embedding import Embedding

ROI = BBox(114.3, 30.4, 114.4, 30.5)


@pytest.fixture
def fake_api(monkeypatch):
    calls = []
    resets = []

    def get_embedding(model, **kwargs):
        calls.append((model, kwargs))
        return Embedding(np.arange(24).reshape(3, 2, 4), {"model": model})

    monkeypatch.setattr(comparison, "get_embedding", get_embedding)
    monkeypatch.setattr(comparison, "reset_runtime", lambda: resets.append(True))
    monkeypatch.setattr(comparison.gc, "collect", lambda: None)
    return calls, resets


def test_all_catalog_models_share_public_request_and_release_weights(fake_api):
    calls, resets = fake_api
    report = comparison.compare_embeddings(spatial=ROI)
    assert report.models == tuple(comparison.list_models())
    assert len(report.embeddings) == len(report.models) == 22
    assert not report.errors
    assert len(resets) == 22
    assert all(kwargs["spatial"] is ROI for _, kwargs in calls)
    assert all(kwargs["output"] == OutputSpec.grid() for _, kwargs in calls)


def test_aliases_and_per_model_options_preserve_order_and_inputs(fake_api):
    calls, resets = fake_api
    annual = TemporalSpec.year(2021)
    seasonal = TemporalSpec.range("2021-05-01", "2021-10-31")
    options = {"aef": {"temporal": annual}, "esri": {"grid_step_m": 500}}
    report = comparison.compare_embeddings(
        ["prithvi", "esri", "esri_gle", "aef"],
        spatial=ROI,
        temporal=seasonal,
        device="cpu",
        model_options=options,
        release_models=False,
    )
    assert report.models == ("prithvi", "esri_gle", "gse")
    assert calls[0][1]["temporal"] is seasonal
    assert calls[1][1]["grid_step_m"] == 500
    assert calls[2][1]["temporal"] is annual
    assert all(kwargs["device"] == "cpu" for _, kwargs in calls)
    assert options == {"aef": {"temporal": annual}, "esri": {"grid_step_m": 500}}
    assert not resets


def test_recorded_failure_is_not_an_embedding_and_later_models_run(fake_api, monkeypatch):
    calls, resets = fake_api
    original = comparison.get_embedding

    def get_embedding(model, **kwargs):
        if model == "prithvi":
            raise RuntimeError("checkpoint unavailable")
        return original(model, **kwargs)

    monkeypatch.setattr(comparison, "get_embedding", get_embedding)
    report = comparison.compare_embeddings(["prithvi", "esri"], spatial=ROI, on_error="record")
    assert report.errors == {"prithvi": "RuntimeError: checkpoint unavailable"}
    assert list(report.embeddings) == ["esri_gle"]
    assert calls[0][0] == "esri_gle"
    assert len(resets) == 2
    summary = json.loads(json.dumps(report.summary()))
    assert summary["prithvi"]["status"] == "error"
    assert summary["esri_gle"] == {"status": "ok", "shape": [3, 2, 4]}


def test_default_fail_fast_still_releases_weights(fake_api, monkeypatch):
    _, resets = fake_api

    def fail(*args, **kwargs):
        raise RuntimeError("no checkpoint")

    monkeypatch.setattr(comparison, "get_embedding", fail)
    with pytest.raises(RuntimeError, match="no checkpoint"):
        comparison.compare_embeddings(["prithvi", "esri"], spatial=ROI)
    assert len(resets) == 1


def test_user_interrupt_is_not_recorded(fake_api, monkeypatch):
    _, resets = fake_api

    def interrupt(*args, **kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(comparison, "get_embedding", interrupt)
    with pytest.raises(KeyboardInterrupt):
        comparison.compare_embeddings(["prithvi"], spatial=ROI, on_error="record")
    assert len(resets) == 1


@pytest.mark.parametrize(
    "models,options,error",
    [
        ([], {}, "at least one"),
        (["typo"], {}, "Unknown models"),
        (["prithvi"], {"esri": {}}, "unselected"),
        (["esri"], {"esri": {}, "esri_gle": {}}, "duplicate aliases"),
        (["prithvi"], {"prithvi": {"model": "esri"}}, "override the model"),
    ],
)
def test_invalid_catalog_requests_do_not_run_models(fake_api, models, options, error):
    calls, resets = fake_api
    with pytest.raises(ValueError, match=error):
        comparison.compare_embeddings(models, spatial=ROI, model_options=options)
    assert not calls and not resets


def test_single_model_string_and_invalid_error_mode_fail_early(fake_api):
    with pytest.raises(TypeError, match="sequence"):
        comparison.compare_embeddings("prithvi", spatial=ROI)
    with pytest.raises(ValueError, match="on_error"):
        comparison.compare_embeddings(["prithvi"], spatial=ROI, on_error="silent")


def test_pca_is_deterministic_ignores_invalid_vectors_and_does_not_mutate():
    values = np.random.default_rng(23).normal(size=(40, 7))
    values[3, 2] = np.nan
    before = values.copy()
    rgb = comparison._pca_rgb(values)
    np.testing.assert_array_equal(rgb, comparison._pca_rgb(values))
    np.testing.assert_array_equal(values, before)
    np.testing.assert_array_equal(rgb[3], [0.5, 0.5, 0.5])
    assert rgb.shape == (40, 3)
    assert np.isfinite(rgb).all()
    assert 0 <= rgb.min() <= rgb.max() <= 1


@pytest.mark.parametrize("values", [np.zeros((1, 8)), np.ones((5, 2)), np.full((3, 4), 1e300)])
def test_constant_or_single_sample_vectors_have_neutral_color(values):
    np.testing.assert_array_equal(comparison._pca_rgb(values), np.full((len(values), 3), 0.5))


def test_rank_deficient_pca_does_not_color_numerical_noise():
    values = np.arange(10)[:, None] * np.array([[1, 2, 3, 4]])
    rgb = comparison._pca_rgb(values)
    assert np.ptp(rgb[:, 0]) == 1
    np.testing.assert_array_equal(rgb[:, 1:], np.full((10, 2), 0.5))


def test_sampled_pca_projects_every_vector_in_wide_feature_blocks():
    values = np.random.default_rng(4).normal(size=(1200, 1024)).astype(np.float16)
    values[1100] = np.nan
    rgb = comparison._pca_rgb(values, max_fit_samples=12)
    assert rgb.shape == (1200, 3)
    assert np.ptp(rgb[1000:1100]) > 0
    np.testing.assert_array_equal(rgb[1100], [0.5, 0.5, 0.5])
    assert np.isfinite(rgb).all()


def test_pca_rejects_all_invalid_values():
    with pytest.raises(ValueError, match="no finite"):
        comparison._pca_rgb(np.full((4, 2), np.nan))


def test_named_axes_are_transposed_without_flipping_pixel_indices():
    xr = pytest.importorskip("xarray")
    chw = np.arange(24).reshape(3, 2, 4)
    da = xr.DataArray(
        chw.transpose(1, 2, 0), dims=("y", "x", "d"), coords={"y": [0, 1], "x": [0, 1, 2, 3]}
    )
    np.testing.assert_array_equal(comparison._grid_array(Embedding(da, {})), chw)
    np.testing.assert_array_equal(
        comparison._grid_array(Embedding(da, {"y_axis_direction": "south_to_north"})),
        chw[:, ::-1],
    )


@pytest.fixture
def plt():
    matplotlib = pytest.importorskip("matplotlib")
    matplotlib.use("Agg")
    import matplotlib.pyplot as pyplot

    yield pyplot
    pyplot.close("all")


def test_plot_native_grids_reference_and_failures_in_one_saved_figure(plt, tmp_path):
    report = comparison.EmbeddingComparison(
        models=("prithvi", "esri_gle", "gse"),
        embeddings={
            "prithvi": Embedding(np.arange(24).reshape(3, 2, 4), {}),
            "esri_gle": Embedding(np.arange(30).reshape(5, 2, 3), {"type": "location"}),
        },
        errors={"gse": "RuntimeError: Earth Engine authentication required"},
    )
    target = tmp_path / "nested" / "comparison.png"
    fig = comparison.plot_embedding_comparison(
        report, reference=np.zeros((8, 8, 3)), columns=2, save_path=target
    )
    assert target.is_file()
    assert len(fig.axes) == 4
    assert fig.axes[1].images[0].get_array().shape == (2, 4, 3)
    assert fig.axes[2].images[0].get_array().shape == (2, 3, 3)
    assert "coordinate samples" in fig.axes[2].texts[0].get_text()
    assert "query grid" in fig.axes[2].get_title()
    assert "FAILED" in fig.axes[3].get_title()
    assert "authentication required" in fig.axes[3].texts[0].get_text()
    assert "2/3 models" in fig._suptitle.get_text()


def test_point_samples_render_as_points_and_preserve_coordinates(plt):
    coords = np.array([[114.3, 30.4], [114.4, 30.5], [114.5, 30.6]])
    fig = comparison.plot_embedding_comparison(
        {"esri_gle": Embedding(np.arange(15).reshape(3, 5), {"type": "location"})},
        lonlat=coords,
    )
    np.testing.assert_array_equal(fig.axes[0].collections[0].get_offsets(), coords)
    assert "3 samples" in fig.axes[0].get_title()


def test_samples_without_coordinates_and_pooled_vector_are_not_maps(plt):
    fig = comparison.plot_embedding_comparison(
        {
            "esri_gle": Embedding(np.arange(15).reshape(3, 5), {}),
            "prithvi": Embedding(np.arange(8), {}),
        }
    )
    assert "not a spatial map" in fig.axes[0].get_xlabel()
    assert "not a spatial map" in fig.axes[1].get_title()
    assert len(fig.axes[1].lines) == 1
    assert not fig.axes[1].images


def test_plot_closes_incomplete_figure_when_input_is_invalid(plt):
    with pytest.raises(ValueError, match="lonlat"):
        comparison.plot_embedding_comparison(
            {"esri": Embedding(np.ones((3, 4)), {})}, lonlat=np.zeros((4, 2))
        )
    assert not plt.get_fignums()


@pytest.mark.parametrize("columns", [0, -1, 1.5, True])
def test_invalid_column_counts_are_rejected(plt, columns):
    with pytest.raises(ValueError, match="columns"):
        comparison.plot_embedding_comparison(
            {"prithvi": Embedding(np.ones(3), {})}, columns=columns
        )


def test_exports_are_available_from_both_package_names():
    import earth_embedding
    import rs_embed

    assert earth_embedding.compare_embeddings is rs_embed.compare_embeddings
    assert earth_embedding.plot_embedding_comparison is rs_embed.plot_embedding_comparison
    assert earth_embedding.EmbeddingComparison is rs_embed.EmbeddingComparison
