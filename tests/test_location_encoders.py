"""Location API tests use deterministic runtimes; no imagery, EE or downloads."""

import sys
from types import SimpleNamespace

import numpy as np
import pytest

from rs_embed.core.errors import ModelError
from rs_embed.core.specs import BBox, OutputSpec, PointBuffer, TemporalSpec
from rs_embed.embedders.catalog import canonical_model_id
from rs_embed.embedders.location_api import get_location_embeddings
from rs_embed.embedders.location_common import positive_int, validate_lonlat
from rs_embed.embedders.location_esri_gle import EsriGLEEmbedder
from rs_embed.embedders.location_geoclip import GeoCLIPEmbedder


@pytest.fixture
def fake_geoclip(monkeypatch):
    torch = pytest.importorskip("torch")
    import rs_embed.embedders.location_geoclip as mod

    seen = []

    class CoordinateEncoder(torch.nn.Module):
        def forward(self, x):
            seen.append(x.cpu().numpy().copy())
            result = torch.zeros((len(x), 512))
            result[:, :3] = torch.column_stack((x[:, 0], x[:, 1], x[:, 0] + 2 * x[:, 1]))
            return result

    monkeypatch.setattr(mod, "_load_geoclip", lambda device, checkpoint: CoordinateEncoder())
    return seen


@pytest.mark.parametrize(
    "bad",
    [[], [10, 20], [[1, 2, 3]], [[np.nan, 0]], [[np.inf, 0]], [[181, 0]], [[0, -91]], [["x", 0]]],
)
def test_invalid_coordinates_fail_before_runtime_load(bad, monkeypatch):
    import rs_embed.embedders.location_api as mod

    def unexpected(*args):
        pytest.fail("Invalid coordinates must not load a runtime")

    monkeypatch.setattr(mod, "get_embedder_cls", unexpected)
    with pytest.raises(ModelError):
        get_location_embeddings("geoclip", bad)


@pytest.mark.parametrize("bad", [0, -1, 1.5, True, np.nan, "bad"])
def test_invalid_batch_size(bad):
    with pytest.raises(ModelError, match="positive integer"):
        positive_int(bad, "batch_size")


def test_wgs84_endpoints_and_noncontiguous_coordinates():
    arr = np.array([[-90, -180], [90, 180]])[:, ::-1]
    checked = validate_lonlat(arr)
    assert checked.flags.c_contiguous
    np.testing.assert_array_equal(checked, [[-180, -90], [180, 90]])


def test_geoclip_converts_order_batches_and_records_provenance(fake_geoclip):
    emb = get_location_embeddings(
        "geo_clip", [[114.4, 30.5], [-74, 40], [139, 35]], device="cpu", batch_size=2
    )
    np.testing.assert_allclose(np.concatenate(fake_geoclip), [[30.5, 114.4], [40, -74], [35, 139]])
    assert [len(x) for x in fake_geoclip] == [2, 1]
    assert emb.data.shape == (3, 512)
    assert emb.data.dtype == np.float32
    assert emb.meta["model"] == "geoclip"
    assert emb.meta["coordinate_order"] == "longitude_latitude"
    assert emb.meta["native_coordinate_order"] == "latitude_longitude"
    assert emb.meta["query_count"] == 3
    assert emb.meta["sensor"] is None
    assert emb.meta["checkpoint"]["source"] == "geoclip_package"


def test_pooled_batch_matches_single_and_marks_time_ignored(fake_geoclip):
    encoder = GeoCLIPEmbedder()
    spatials = [PointBuffer(114.4, 30.5, 10), BBox(10, 20, 12, 22)]
    kwargs = dict(temporal=TemporalSpec.year(2024), device="cpu")
    batch = encoder.get_embeddings_batch(spatials=spatials, **kwargs)
    for spatial, item in zip(spatials, batch, strict=True):
        single = encoder.get_embedding(
            spatial=spatial, sensor=None, output=OutputSpec.pooled(), backend="auto", **kwargs
        )
        np.testing.assert_allclose(item.data, single.data)
        assert item.meta["requested_temporal_ignored"] is True
        assert item.meta["pooling"] == "centre_coordinate_query"
    np.testing.assert_allclose(batch[1].meta["query_lonlat"], [11, 21])


def test_grid_is_north_up_and_has_bounded_query_count(fake_geoclip):
    pytest.importorskip("xarray")
    encoder = GeoCLIPEmbedder()
    kwargs = dict(
        spatial=BBox(10, 45, 10.02, 45.02),
        temporal=None,
        sensor=None,
        output=OutputSpec.grid(),
        backend="auto",
        device="cpu",
    )
    emb = encoder.get_embedding(**kwargs, model_config={"grid_step_m": 1000})
    assert emb.data.dims == ("d", "y", "x")
    assert np.all(np.diff(emb.data.y) < 0)
    assert np.all(np.diff(emb.data.x) > 0)
    assert emb.meta["grid_semantics"] == "coordinate_queries_not_image_pixels"
    seen_count = len(fake_geoclip)
    with pytest.raises(ModelError, match="max_grid_points"):
        encoder.get_embedding(**kwargs, model_config={"grid_step_m": 1, "max_grid_points": 10})
    assert len(fake_geoclip) == seen_count
    for step in [0, -1, np.inf, np.nan, "invalid"]:
        with pytest.raises(ModelError, match="grid_step_m"):
            encoder.get_embedding(**kwargs, model_config={"grid_step_m": step})


def test_locations_do_not_accept_imagery_or_gee(fake_geoclip):
    encoder = GeoCLIPEmbedder()
    kwargs = dict(
        spatial=PointBuffer(10, 20, 1),
        temporal=None,
        sensor=None,
        output=OutputSpec.pooled(),
        device="cpu",
    )
    with pytest.raises(ModelError, match="does not accept imagery"):
        encoder.get_embedding(**kwargs, backend="auto", input_chw=np.zeros((3, 2, 2)))
    with pytest.raises(ModelError, match="backend='auto'"):
        encoder.get_embedding(**kwargs, backend="gee")
    with pytest.raises(ModelError, match="not a location encoder"):
        get_location_embeddings("remoteclip", [[10, 20]])


def test_public_roi_api_needs_no_earth_engine_or_imagery(fake_geoclip, monkeypatch):
    from rs_embed import get_embedding

    monkeypatch.setitem(sys.modules, "ee", None)
    result = get_embedding("geoclip", spatial=PointBuffer(114.4, 30.5, 10), device="cpu")
    assert result.data.shape == (512,)
    np.testing.assert_allclose(fake_geoclip[0], [[30.5, 114.4]])
    assert result.meta["sensor"] is None


def test_esri_uses_documented_csv_order_and_cleans_temporary_files(monkeypatch):
    from pathlib import Path

    import rs_embed.embedders.location_esri_gle as mod

    seen = []
    paths = []

    class FakeEsri:
        def get(self, path, **kwargs):
            paths.append(Path(path))
            assert Path(path).read_text().splitlines()[0] == "lon,lat"
            assert kwargs["location_column"] == ["lon", "lat"]
            assert kwargs["spatial_reference"] == 4326
            assert kwargs["return_embeddings"] is True
            assert kwargs["show_progress"] is False
            coords = np.loadtxt(path, delimiter=",", skiprows=1, ndmin=2)
            seen.append(coords)
            result = np.zeros((len(coords), 256))
            result[:, :3] = np.column_stack((coords, coords[:, 0] + coords[:, 1]))
            return result

    monkeypatch.setattr(mod, "_load_esri_gle", lambda device: FakeEsri())
    monkeypatch.setattr(mod, "resolve_torch_device", lambda device: "cpu")
    result = get_location_embeddings(
        "esri", [[114.4, 30.5], [-74, 40], [139, 35]], device="cpu", batch_size=2
    )
    np.testing.assert_allclose(np.concatenate(seen), [[114.4, 30.5], [-74, 40], [139, 35]])
    assert [len(x) for x in seen] == [2, 1]
    assert all(not p.exists() for p in paths)
    assert result.meta["model"] == "esri_gle"
    assert result.meta["backbone"] == "satclip/sentinel-2_trained"
    assert result.meta["checkpoint"]["source"] == "arcgis_runtime"


def test_esri_rejects_incomplete_results_and_cleans_files(monkeypatch):
    from pathlib import Path

    import rs_embed.embedders.location_esri_gle as mod

    paths = []

    def incomplete(path, **kwargs):
        paths.append(Path(path))
        return np.zeros((1, 256))

    monkeypatch.setattr(mod, "_load_esri_gle", lambda device: SimpleNamespace(get=incomplete))
    monkeypatch.setattr(mod, "resolve_torch_device", lambda device: "cpu")
    with pytest.raises(ModelError, match="expected"):
        get_location_embeddings("esri_gle", [[10, 20], [30, 40]])
    assert all(not p.exists() for p in paths)


def test_missing_runtime_errors_are_actionable(monkeypatch):
    import rs_embed.embedders.location_esri_gle as esri
    import rs_embed.embedders.location_geoclip as geoclip

    esri._load_esri_gle.cache_clear()
    geoclip._load_geoclip.cache_clear()
    monkeypatch.setitem(sys.modules, "geoclip", None)
    monkeypatch.setitem(sys.modules, "arcgis.learn", None)
    with pytest.raises(ModelError, match="pip install.*geoclip"):
        geoclip._load_geoclip("cpu", None)
    with pytest.raises(ModelError, match="Esri-supported environment"):
        esri._load_esri_gle("cpu")


def test_broken_esri_import_is_reported_as_an_environment_error(monkeypatch):
    import builtins

    import rs_embed.embedders.location_esri_gle as mod

    original_import = builtins.__import__

    def broken_import(name, *args, **kwargs):
        if name == "arcgis.learn":
            raise NameError("name 'torch' is not defined")
        return original_import(name, *args, **kwargs)

    mod._load_esri_gle.cache_clear()
    monkeypatch.setattr(builtins, "__import__", broken_import)
    with pytest.raises(ModelError, match="Esri-supported environment.*NameError"):
        mod._load_esri_gle("cpu")


def test_esri_cpu_request_controls_initial_checkpoint_device(monkeypatch):
    torch = pytest.importorskip("torch")
    import rs_embed.embedders.location_esri_gle as mod

    class FakeEmbeddings:
        def __init__(self, dataset_type, backbone):
            assert dataset_type == "location"
            assert backbone == "satclip/sentinel-2_trained"
            self._device = self._get_device()
            assert self._device == torch.device("cpu")
            self.model = torch.nn.Linear(2, 256)

    mod._load_esri_gle.cache_clear()
    monkeypatch.setattr(mod, "version", lambda package: "2.4.3")
    monkeypatch.setitem(sys.modules, "arcgis.learn", SimpleNamespace(Embeddings=FakeEmbeddings))
    try:
        loaded = mod._load_esri_gle("cpu")
        assert loaded.model.training is False
        assert loaded._device == torch.device("cpu")
    finally:
        mod._load_esri_gle.cache_clear()


def test_esri_rejects_unchecked_runtime_versions(monkeypatch):
    import rs_embed.embedders.location_esri_gle as mod

    mod._load_esri_gle.cache_clear()
    monkeypatch.setitem(sys.modules, "arcgis.learn", SimpleNamespace(Embeddings=object))
    monkeypatch.setattr(mod, "version", lambda package: "9.0.0")
    with pytest.raises(ModelError, match="checked ArcGIS 2.4.3"):
        mod._load_esri_gle("cpu")


def test_esri_rejects_wrong_embedding_dimension(monkeypatch):
    import rs_embed.embedders.location_esri_gle as mod

    monkeypatch.setattr(mod, "resolve_torch_device", lambda device: "cpu")
    monkeypatch.setattr(
        mod,
        "_load_esri_gle",
        lambda device: SimpleNamespace(get=lambda *args, **kwargs: np.zeros((1, 512))),
    )
    with pytest.raises(ModelError, match="expected 256"):
        get_location_embeddings("esri_gle", [[10, 20]])


@pytest.mark.parametrize("cls", [GeoCLIPEmbedder, EsriGLEEmbedder])
def test_describe_is_lightweight_and_aliases_work(cls):
    desc = cls().describe()
    assert desc["type"] == "location"
    assert desc["backend"] == ["auto"]
    assert desc["output"] == ["pooled", "grid"]
    assert canonical_model_id("ESRI") == "esri_gle"
    assert canonical_model_id("Geo_Clip") == "geoclip"


def test_missing_checkpoint_and_unknown_config_fail_before_loading(fake_geoclip, tmp_path):
    with pytest.raises(ModelError, match="does not exist"):
        get_location_embeddings("geoclip", [[1, 2]], checkpoint=str(tmp_path / "missing.pth"))
    with pytest.raises(ModelError, match="Unknown GeoCLIP settings"):
        get_location_embeddings("geoclip", [[1, 2]], variant="invented")
    with pytest.raises(ModelError, match="Unknown Esri GLE settings"):
        get_location_embeddings("esri_gle", [[1, 2]], checkpoint="not_supported")
