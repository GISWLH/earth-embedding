"""Location API tests use deterministic runtimes; no imagery, EE or downloads."""

import hashlib
import io
import sys
import zipfile

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


@pytest.fixture
def esri_weights(monkeypatch):
    """A pinned tiny stand-in exercises I/O without distributing Esri weights."""
    import rs_embed.embedders.location_esri_gle as mod

    raw = b"test-only Esri checkpoint bytes"
    monkeypatch.setattr(mod, "_WEIGHTS_BYTES", len(raw))
    monkeypatch.setattr(mod, "_WEIGHTS_SHA256", hashlib.sha256(raw).hexdigest())
    monkeypatch.delenv("RS_EMBED_ESRI_GLE_CKPT", raising=False)
    return raw


def _esri_dlpk(weights, **extra_members):
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as package:
        package.writestr("satclip.pth", weights)
        for name, value in extra_members.items():
            package.writestr(name, value)
    return archive.getvalue()


@pytest.mark.parametrize("as_archive", [False, True])
def test_esri_local_checkpoint_is_verified_without_network(
    esri_weights, as_archive, tmp_path, monkeypatch
):
    import rs_embed.embedders.location_esri_gle as mod

    checkpoint = tmp_path / ("model.dlpk" if as_archive else "model.pth")
    checkpoint.write_bytes(_esri_dlpk(esri_weights) if as_archive else esri_weights)

    def unexpected(*args, **kwargs):
        pytest.fail("Explicit local checkpoints must never access the network")

    monkeypatch.setattr(mod.urllib.request, "urlopen", unexpected)
    weights, provenance = mod._resolve_checkpoint(
        {"checkpoint": str(checkpoint), "local_files_only": True}
    )
    assert weights == esri_weights
    assert provenance["sha256"] == hashlib.sha256(esri_weights).hexdigest()


def test_esri_dlpk_ignores_python_and_never_extracts_members(esri_weights, tmp_path):
    import rs_embed.embedders.location_esri_gle as mod

    sentinel = tmp_path / "must-not-exist"
    dangerous = f"from pathlib import Path\nPath({str(sentinel)!r}).touch()"
    package = _esri_dlpk(
        esri_weights, **{"LocationEncoder.py": dangerous, "../outside.txt": "ignored"}
    )
    assert mod._verified_weights(package) == esri_weights
    assert not sentinel.exists()
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("as_archive", [False, True])
def test_esri_rejects_different_weights_even_when_size_matches(esri_weights, as_archive):
    import rs_embed.embedders.location_esri_gle as mod

    different = b"X" + esri_weights[1:]
    raw = _esri_dlpk(different) if as_archive else different
    with pytest.raises(ModelError, match="(?i)(sha|checksum|match)"):
        mod._verified_weights(raw)


def test_esri_rejects_wrong_size_and_archive_without_weights(esri_weights):
    import rs_embed.embedders.location_esri_gle as mod

    with pytest.raises(ModelError):
        mod._verified_weights(esri_weights[:-1])
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w") as package:
        package.writestr("LocationEncoder.py", "raise RuntimeError('do not run')")
    with pytest.raises(ModelError, match="satclip.pth"):
        mod._verified_weights(archive.getvalue())


def test_esri_checkpoint_env_and_explicit_path_precedence(esri_weights, tmp_path, monkeypatch):
    import rs_embed.embedders.location_esri_gle as mod

    explicit = tmp_path / "explicit.pth"
    explicit.write_bytes(esri_weights)
    monkeypatch.setenv("RS_EMBED_ESRI_GLE_CKPT", str(tmp_path / "missing.pth"))
    weights, _ = mod._resolve_checkpoint({"checkpoint": str(explicit), "local_files_only": True})
    assert weights == esri_weights
    monkeypatch.setenv("RS_EMBED_ESRI_GLE_CKPT", str(explicit))
    weights, _ = mod._resolve_checkpoint({"local_files_only": True})
    assert weights == esri_weights


def test_esri_offline_missing_cache_never_downloads(esri_weights, tmp_path, monkeypatch):
    import rs_embed.embedders.location_esri_gle as mod

    def unexpected(*args, **kwargs):
        pytest.fail("local_files_only=True must never access the network")

    monkeypatch.setattr(mod.urllib.request, "urlopen", unexpected)
    with pytest.raises(ModelError, match="(?i)(offline|local_files_only|cache)"):
        mod._resolve_checkpoint({"cache_dir": str(tmp_path), "local_files_only": True})


@pytest.mark.parametrize("bad", ["false", 0, 1, None])
def test_esri_offline_setting_requires_boolean(esri_weights, tmp_path, bad):
    import rs_embed.embedders.location_esri_gle as mod

    with pytest.raises(ModelError, match="local_files_only"):
        mod._resolve_checkpoint({"cache_dir": str(tmp_path), "local_files_only": bad})


def test_esri_download_verifies_then_reuses_cache_offline(esri_weights, tmp_path, monkeypatch):
    import rs_embed.embedders.location_esri_gle as mod

    requests = []

    def download(request, timeout):
        requests.append(request.full_url)
        assert timeout > 0
        assert not (tmp_path / "satclip.pth").exists()
        return io.BytesIO(_esri_dlpk(esri_weights))

    monkeypatch.setattr(mod.urllib.request, "urlopen", download)
    weights, metadata = mod._resolve_checkpoint({"cache_dir": str(tmp_path)})
    assert weights == esri_weights
    assert requests == [mod._WEIGHTS_URL]
    assert metadata["sha256"] == hashlib.sha256(esri_weights).hexdigest()
    assert (tmp_path / "satclip.pth").read_bytes() == esri_weights
    assert sorted(path.name for path in tmp_path.iterdir()) == ["satclip.pth"]

    def unexpected(*args, **kwargs):
        pytest.fail("A valid cache must work offline without another download")

    monkeypatch.setattr(mod.urllib.request, "urlopen", unexpected)
    cached, _ = mod._resolve_checkpoint({"cache_dir": str(tmp_path), "local_files_only": True})
    assert cached == weights


def test_esri_corrupt_cache_is_rejected_without_silent_redownload(
    esri_weights, tmp_path, monkeypatch
):
    import rs_embed.embedders.location_esri_gle as mod

    path = tmp_path / "satclip.pth"
    path.write_bytes(b"X" + esri_weights[1:])

    def unexpected(*args, **kwargs):
        pytest.fail("A corrupt cached checkpoint must not be silently replaced")

    monkeypatch.setattr(mod.urllib.request, "urlopen", unexpected)
    with pytest.raises(ModelError, match="SHA-256"):
        mod._resolve_checkpoint({"cache_dir": str(tmp_path)})
    assert path.read_bytes() != esri_weights


@pytest.mark.parametrize("failure", ["checksum", "size", "network"])
def test_esri_failed_download_does_not_leave_a_checkpoint(
    esri_weights, tmp_path, monkeypatch, failure
):
    import rs_embed.embedders.location_esri_gle as mod

    def download(*args, **kwargs):
        if failure == "network":
            raise OSError("connection interrupted")
        if failure == "size":
            return io.BytesIO(b"X" * 33)
        return io.BytesIO(_esri_dlpk(b"X" + esri_weights[1:]))

    if failure == "size":
        monkeypatch.setattr(mod, "_MAX_DOWNLOAD_BYTES", 32)
    monkeypatch.setattr(mod.urllib.request, "urlopen", download)
    with pytest.raises(ModelError):
        mod._resolve_checkpoint({"cache_dir": str(tmp_path)})
    assert list(tmp_path.iterdir()) == []


def test_esri_failed_cache_publish_cleans_temporary_file(esri_weights, tmp_path, monkeypatch):
    import rs_embed.embedders.location_esri_gle as mod

    monkeypatch.setattr(
        mod.urllib.request, "urlopen", lambda *args, **kwargs: io.BytesIO(_esri_dlpk(esri_weights))
    )

    def failed_replace(source, target):
        assert source.read_bytes() == esri_weights
        assert not target.exists()
        raise OSError("simulated interrupted cache publication")

    monkeypatch.setattr(mod.os, "replace", failed_replace)
    with pytest.raises(OSError, match="cache publication"):
        mod._resolve_checkpoint({"cache_dir": str(tmp_path)})
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("unexpected_key", [False, True])
def test_esri_loads_tensors_safely_on_cpu_and_requires_exact_state(monkeypatch, unexpected_key):
    torch = pytest.importorskip("torch")
    import rs_embed.embedders.location_esri_gle as mod

    state = {
        "nnet.layers.0.weight": torch.zeros((256, 1600)),
        "nnet.layers.0.bias": torch.zeros(256),
        "nnet.layers.1.weight": torch.zeros((256, 256)),
        "nnet.layers.1.bias": torch.zeros(256),
        "nnet.last_layer.weight": torch.zeros((256, 256)),
        "nnet.last_layer.bias": torch.zeros(256),
    }
    if unexpected_key:
        state["unexpected.weight"] = torch.zeros(1)
    buffer = io.BytesIO()
    torch.save(state, buffer)
    original_load = torch.load
    seen = []

    def safe_load(*args, **kwargs):
        seen.append(kwargs)
        return original_load(*args, **kwargs)

    monkeypatch.setattr(torch, "load", safe_load)
    mod._load_esri_gle.cache_clear()
    try:
        if unexpected_key:
            with pytest.raises(ModelError, match="state dictionary"):
                mod._load_esri_gle("cpu", buffer.getvalue())
        else:
            model = mod._load_esri_gle("cpu", buffer.getvalue())
            assert model.training is False
            assert all(
                p.device.type == "cpu" and p.dtype == torch.float64 for p in model.parameters()
            )
            for name, value in state.items():
                torch.testing.assert_close(model.state_dict()[name], value.double())
        assert len(seen) == 1
        assert seen[0]["weights_only"] is True
        assert seen[0]["map_location"] == "cpu"
    finally:
        mod._load_esri_gle.cache_clear()


def test_esri_batches_preserve_lonlat_without_arcgis_or_earth_engine(monkeypatch):
    torch = pytest.importorskip("torch")
    import rs_embed.embedders.location_esri_gle as mod

    seen = []

    class CoordinateEncoder(torch.nn.Module):
        def forward(self, coords):
            assert coords.dtype == torch.float64
            assert coords.device.type == "cpu"
            assert not torch.is_grad_enabled()
            seen.append(coords.cpu().numpy().copy())
            result = torch.zeros((len(coords), 256), dtype=torch.float64)
            result[:, :3] = torch.column_stack((coords, coords[:, 0] + coords[:, 1]))
            return result

    monkeypatch.setitem(sys.modules, "arcgis", None)
    monkeypatch.setitem(sys.modules, "arcgis.learn", None)
    monkeypatch.setitem(sys.modules, "ee", None)
    monkeypatch.setattr(mod, "_resolve_checkpoint", lambda config: (b"fixture", {"source": "test"}))
    monkeypatch.setattr(mod, "_load_esri_gle", lambda device, weights: CoordinateEncoder())
    coords = [[114.4, 30.5], [-74, 40], [139, 35]]
    result = get_location_embeddings("esri", coords, device="cpu", batch_size=2)
    np.testing.assert_allclose(np.concatenate(seen), coords)
    np.testing.assert_allclose(result.data[:, :2], coords)
    assert [len(x) for x in seen] == [2, 1]
    assert result.data.shape == (3, 256)
    assert result.data.dtype == np.float32
    assert result.meta["model"] == "esri_gle"
    assert result.meta["backbone"] == "satclip/sentinel-2_trained"
    assert result.meta["native_coordinate_order"] == "longitude_latitude"
    assert result.meta["checkpoint"]["source"] == "test"


@pytest.mark.parametrize("shape", [(1, 256), (2, 512)])
def test_esri_rejects_incomplete_or_wrong_dimension_results(monkeypatch, shape):
    torch = pytest.importorskip("torch")
    import rs_embed.embedders.location_esri_gle as mod

    monkeypatch.setattr(mod, "_resolve_checkpoint", lambda config: (b"fixture", {}))
    monkeypatch.setattr(
        mod, "_load_esri_gle", lambda device, weights: lambda coords: torch.zeros(shape)
    )
    with pytest.raises(ModelError, match="expected"):
        get_location_embeddings("esri_gle", [[10, 20], [30, 40]], device="cpu")


def test_esri_rejects_mps_float64_before_downloading(monkeypatch):
    import rs_embed.embedders.location_esri_gle as mod

    def unexpected(*args, **kwargs):
        pytest.fail("Unsupported MPS inference must fail before loading/downloading weights")

    monkeypatch.setattr(mod, "resolve_torch_device", lambda device: "mps")
    monkeypatch.setattr(mod, "_resolve_checkpoint", unexpected)
    monkeypatch.setattr(mod, "_load_esri_gle", unexpected)
    with pytest.raises(ModelError, match="float64.*MPS"):
        get_location_embeddings("esri_gle", [[10, 20]], device="mps")


def test_missing_geoclip_runtime_error_is_actionable(monkeypatch):
    import rs_embed.embedders.location_geoclip as geoclip

    geoclip._load_geoclip.cache_clear()
    monkeypatch.setitem(sys.modules, "geoclip", None)
    with pytest.raises(ModelError, match="pip install.*geoclip"):
        geoclip._load_geoclip("cpu", None)


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
        get_location_embeddings("esri_gle", [[1, 2]], variant="invented")
