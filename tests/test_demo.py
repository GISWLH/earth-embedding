"""Offline behavior tests; real COG and GLE inference have separate receipts."""

import hashlib
from types import SimpleNamespace

import numpy as np
import pytest

from earth_embedding.demo import (
    DemoData,
    align_samples,
    classify_demo,
    fetch_aef_demo,
    load_demo,
    pca_colors,
    plot_map,
)


def test_bundled_payload_integrity_and_id_alignment():
    data = load_demo()
    assert data.features.shape == (5933, 64)
    x = align_samples(data.samples, data.samples.tile_id.to_numpy()[::-1], data.features[::-1])
    np.testing.assert_array_equal(x, data.features)


@pytest.mark.parametrize("problem", ["duplicate", "missing", "nan"])
def test_invalid_feature_join_rejected(problem):
    data = load_demo()
    ids, x = data.samples.tile_id.to_numpy().copy(), data.features.copy()
    if problem == "duplicate":
        ids[0] = ids[1]
    elif problem == "missing":
        ids[0] = "missing"
    else:
        x[0, 0] = np.nan
    with pytest.raises(ValueError):
        align_samples(data.samples, ids, x)


def test_aef_download_cache_offline_and_corruption(tmp_path, monkeypatch):
    from rs_embed import aef

    data = load_demo("aef")
    calls = []

    def sample(points, *, tiles, overview_level):
        assert overview_level == 6
        calls.append(len(points))
        return SimpleNamespace(data=data.features)

    monkeypatch.setattr(aef, "sample_aef", sample)
    with pytest.raises(FileNotFoundError, match="online once"):
        fetch_aef_demo(tmp_path, offline=True)
    fetch_aef_demo(tmp_path)
    fetch_aef_demo(tmp_path, offline=True)
    assert calls == [5933]
    np.save(tmp_path / "aef-bayarea-2021.npy", data.features + 1)
    with pytest.raises(ValueError, match="SHA-256"):
        fetch_aef_demo(tmp_path)


def test_network_failure_does_not_create_cache(tmp_path, monkeypatch):
    from rs_embed import aef

    def fail(*args, **kwargs):
        raise OSError("network unavailable")

    monkeypatch.setattr(aef, "sample_aef", fail)
    with pytest.raises(RuntimeError, match="Official AEF download failed"):
        fetch_aef_demo(tmp_path)
    assert not list(tmp_path.glob("*.npy"))


def test_changed_remote_payload_is_not_cached(tmp_path, monkeypatch):
    from rs_embed import aef

    monkeypatch.setattr(
        aef, "sample_aef", lambda *a, **k: SimpleNamespace(data=load_demo("aef").features + 1)
    )
    with pytest.raises(ValueError, match="changed"):
        fetch_aef_demo(tmp_path)
    assert not list(tmp_path.glob("*.npy"))


def test_map_geometry_is_north_up_independent_of_row_order():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    data = load_demo("aef")
    samples = data.samples.loc[[data.samples.center_lat.idxmax(), data.samples.center_lat.idxmin()]]
    fig = plot_map(samples, ["red", "blue"])
    ax = fig.axes[0]
    paths = ax.collections[0].get_paths()
    assert paths[0].vertices[:, 1].mean() > paths[1].vertices[:, 1].mean()
    assert ax.get_ylim()[0] < ax.get_ylim()[1]
    plt.close(fig)


def test_spatial_holdout_and_no_test_fitting():
    data = load_demo()
    original = classify_demo(data)
    table = original["samples"]
    train = table.demo_split.eq("train")
    test = table.demo_split.eq("test")
    assert table.loc[test, "minlat"].min() - table.loc[train, "maxlat"].max() >= 0.05
    assert table.loc[~test, "prediction"].isna().all()
    changed = data.features.copy()
    changed[test] += 100
    other = classify_demo(DemoData(data.samples, changed, data.metadata))
    for step, attr in [("standardscaler", "mean_"), ("logisticregression", "coef_")]:
        np.testing.assert_array_equal(
            getattr(original["estimator"].named_steps[step], attr),
            getattr(other["estimator"].named_steps[step], attr),
        )
    assert sum(map(sum, original["metrics"]["confusion_matrix"])) == 2173


def test_public_errors_and_pca():
    with pytest.raises(ValueError, match="Unknown demo"):
        load_demo("not-real")
    with pytest.raises(ValueError, match="finite"):
        pca_colors(np.full((3, 3), np.nan))
    colors = pca_colors(load_demo().features)
    assert colors.shape == (5933, 3)
    assert ((colors >= 0) & (colors <= 1)).all()
    data = load_demo("aef")
    assert hashlib.sha256(data.features.tobytes()).hexdigest() == data.metadata["array_sha256"]


def test_spatial_columns_cannot_hide_overlapping_geography():
    data = load_demo()
    data.samples.loc[data.samples.demo_split.eq("train"), "maxlat"] = 38.0
    with pytest.raises(ValueError, match="Spatial leakage"):
        classify_demo(data)
