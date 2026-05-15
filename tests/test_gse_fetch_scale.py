import importlib
import sys
import types

import numpy as np

from rs_embed.core.specs import OutputSpec, PointBuffer, SensorSpec, TemporalSpec


def test_gse_get_embedding_uses_sensor_scale_m(monkeypatch):
    fake_xarray = types.ModuleType("xarray")
    fake_xarray.DataArray = object
    monkeypatch.setitem(sys.modules, "xarray", fake_xarray)

    gse_mod = importlib.import_module("rs_embed.embedders.precomputed_gse_annual")
    embedder = gse_mod.GSEAnnualEmbedder()
    embedder.model_name = "gse"
    embedder._get_provider = lambda _backend: object()
    seen = {}

    def _fake_fetch(provider, **kw):
        seen["scale_m"] = kw["scale_m"]
        return np.ones((2, 2, 2), dtype=np.float32), ["b0", "b1"]

    monkeypatch.setattr(gse_mod, "_fetch_collection_patch_all_bands_chw", _fake_fetch)

    emb = embedder.get_embedding(
        spatial=PointBuffer(lon=0.0, lat=0.0, buffer_m=256),
        temporal=TemporalSpec.year(2020),
        sensor=SensorSpec(collection="GSE", bands=tuple(), scale_m=60),
        output=OutputSpec.pooled(),
        backend="auto",
    )

    assert seen["scale_m"] == 60
    np.testing.assert_allclose(emb.data, np.array([1.0, 1.0], dtype=np.float32))


def test_gse_pooled_mean_ignores_fill_value_pixels(monkeypatch):
    fake_xarray = types.ModuleType("xarray")
    fake_xarray.DataArray = object
    monkeypatch.setitem(sys.modules, "xarray", fake_xarray)

    gse_mod = importlib.import_module("rs_embed.embedders.precomputed_gse_annual")
    embedder = gse_mod.GSEAnnualEmbedder()
    embedder.model_name = "gse"
    embedder._get_provider = lambda _backend: object()

    def _fake_fetch(provider, **kw):
        return (
            np.array(
                [
                    [[1.0, -9999.0], [3.0, 5.0]],
                    [[-9999.0, -9999.0], [-9999.0, -9999.0]],
                ],
                dtype=np.float32,
            ),
            ["A00", "A01"],
        )

    monkeypatch.setattr(gse_mod, "_fetch_collection_patch_all_bands_chw", _fake_fetch)

    emb = embedder.get_embedding(
        spatial=PointBuffer(lon=0.0, lat=0.0, buffer_m=256),
        temporal=TemporalSpec.year(2021),
        sensor=None,
        output=OutputSpec.pooled(),
        backend="auto",
    )

    assert emb.meta["valid_pixel_fraction"] == 0.375
    np.testing.assert_allclose(emb.data[0], np.float32(3.0))
    assert np.isnan(emb.data[1])
