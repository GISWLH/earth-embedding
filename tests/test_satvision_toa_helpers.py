import numpy as np
import pytest

from rs_embed.core.errors import ModelError
from rs_embed.core.specs import OutputSpec, PointBuffer, SensorSpec, TemporalSpec
from rs_embed.embedders.onthefly_satvision_toa import (
    SatVisionTOAEmbedder,
    _coerce_fetch_result,
    _fetch_toa_chw_from_gee,
    _normalize_indices,
    _normalize_satvision_toa_input,
    _satvision_forward_batch,
)
from rs_embed.tools.model_defaults import default_sensor_for_model


def test_normalize_indices_supports_negative():
    assert _normalize_indices((12, 13, -1, -2, 99), 14) == (12, 13)


def test_normalize_satvision_raw_reflectance_and_thermal():
    raw = np.full((14, 4, 4), 5000.0, dtype=np.float32)
    raw[12] = 275.0
    raw[13] = 275.0

    y = _normalize_satvision_toa_input(
        raw,
        mode="raw",
        reflectance_indices=(0, 1, 2, 3, 4, 6),
        emissive_indices=(5, 7, 8, 9, 10, 11, 12, 13),
        reflectance_divisor=10000.0,
        emissive_mins=(175.0, 175.0, 175.0, 175.0, 175.0, 175.0, 175.0, 175.0),
        emissive_maxs=(375.0, 375.0, 375.0, 375.0, 375.0, 375.0, 375.0, 375.0),
    )

    # 5000/10000 => 0.5 for reflectance
    assert np.allclose(y[0], 0.5)
    assert np.allclose(y[6], 0.5)
    # (275-175)/(375-175) => 0.5 for thermal
    assert np.allclose(y[12], 0.5)
    assert np.allclose(y[13], 0.5)


def test_satvision_runtime_requires_14_bands(monkeypatch):
    emb = SatVisionTOAEmbedder()

    class _FakeSensor:
        collection = "TEST/COLL"
        bands = tuple("B" + str(i) for i in range(10))
        scale_m = 500
        cloudy_pct = 30
        fill_value = 0.0
        composite = "median"

    with pytest.raises(ModelError, match="requires exactly"):
        emb._resolve_runtime(sensor=_FakeSensor(), device="cpu")


def test_satvision_default_sensor_has_14_bands():
    emb = SatVisionTOAEmbedder()
    ss = emb._default_sensor()
    assert len(ss.bands) == 14


def test_satvision_model_defaults_matches_embedder_default_sensor():
    emb = SatVisionTOAEmbedder()
    direct = emb._default_sensor()
    resolved = default_sensor_for_model("satvision")
    assert resolved is not None
    assert resolved.collection == direct.collection
    assert resolved.bands == direct.bands
    assert resolved.scale_m == direct.scale_m
    assert resolved.cloudy_pct == direct.cloudy_pct
    assert resolved.fill_value == direct.fill_value
    assert resolved.composite == direct.composite


def test_coerce_fetch_result_supports_array_and_tuple():
    raw = np.ones((14, 4, 4), dtype=np.float32)
    arr0, meta0 = _coerce_fetch_result(raw)
    assert arr0.shape == (14, 4, 4)
    assert meta0["fallback_used"] is False
    assert meta0["already_unit_scaled"] is False

    arr1, meta1 = _coerce_fetch_result((raw, {"fallback_used": True, "already_unit_scaled": True}))
    assert arr1.shape == (14, 4, 4)
    assert meta1["fallback_used"] is True
    assert meta1["already_unit_scaled"] is True


def test_satvision_default_modis_fetch_prefers_proxy(monkeypatch):
    import rs_embed.embedders.onthefly_satvision_toa as sv

    calls = []

    def _fake_fetch(provider, *, spatial, temporal, sensor, to_float_image=False):
        calls.append((str(sensor.collection), tuple(sensor.bands), bool(to_float_image)))
        if str(sensor.collection) == sv._FALLBACK_MOD09_COLLECTION:
            return np.full((6, 4, 4), 5000.0, dtype=np.float32)
        if str(sensor.collection) == sv._FALLBACK_MOD21_COLLECTION:
            return np.full((1, 4, 4), 15000.0, dtype=np.float32)
        raise AssertionError(f"Unexpected collection: {sensor.collection}")

    monkeypatch.setattr(sv, "_fetch_sensor_patch_chw", _fake_fetch)

    sensor = SensorSpec(
        collection=sv._DEFAULT_MODIS_COLLECTION,
        bands=sv._DEFAULT_MODIS_BANDS,
        scale_m=1000,
    )
    arr, meta = _fetch_toa_chw_from_gee(
        object(),
        PointBuffer(lon=0.0, lat=0.0, buffer_m=1000),
        TemporalSpec.range("2020-01-01", "2020-01-31"),
        sensor,
    )

    assert arr.shape == (14, 4, 4)
    assert np.allclose(arr[0], 0.5)
    assert meta["gee_fetch_mode"] == "proxy"
    assert meta["already_unit_scaled"] is True
    assert meta["official_preprocess_alignment"] == "proxy_reflectance_lst"
    assert [c[0] for c in calls] == [sv._FALLBACK_MOD09_COLLECTION, sv._FALLBACK_MOD21_COLLECTION]


def test_satvision_fetch_rejects_custom_gee_sensor():
    sensor = SensorSpec(
        collection="TEST/COLL",
        bands=tuple(f"B{i}" for i in range(14)),
        scale_m=1000,
    )
    with pytest.raises(ModelError, match="only supports the default MODIS SatVision sensor"):
        _fetch_toa_chw_from_gee(
            object(),
            PointBuffer(lon=0.0, lat=0.0, buffer_m=1000),
            TemporalSpec.range("2020-01-01", "2020-01-31"),
            sensor,
        )


def test_satvision_grid_manual_fallback_accepts_4d_feature_map(monkeypatch):
    import rs_embed.embedders.onthefly_satvision_toa as sv

    class _Identity:
        def __call__(self, x):
            return x

    class _PatchEmbed:
        def __call__(self, x):
            return x

    class _LayerTo4D:
        def __call__(self, x):
            return x.reshape(1, 2, 2, 4)

    class _FakeModel:
        patch_embed = _PatchEmbed()
        layers = [_LayerTo4D()]
        norm = _Identity()
        ape = False

    class _FakeTensor:
        def __init__(self, arr):
            self.arr = np.asarray(arr, dtype=np.float32)

        @property
        def ndim(self):
            return self.arr.ndim

        @property
        def shape(self):
            return self.arr.shape

        def to(self, _dev):
            return self

        def reshape(self, *shape):
            return _FakeTensor(self.arr.reshape(*shape))

        def permute(self, *dims):
            return _FakeTensor(np.transpose(self.arr, dims))

        def contiguous(self):
            return self

        def detach(self):
            return self

        def float(self):
            return self

        def cpu(self):
            return self

        def numpy(self):
            return self.arr

    class _NoGrad:
        def __enter__(self):
            return None

        def __exit__(self, exc_type, exc, tb):
            return False

    class _FakeTorch:
        @staticmethod
        def from_numpy(arr):
            return _FakeTensor(arr)

        @staticmethod
        def is_tensor(obj):
            return isinstance(obj, _FakeTensor)

        @staticmethod
        def no_grad():
            return _NoGrad()

    monkeypatch.setattr(sv, "ensure_torch", lambda: None)
    import sys

    real_torch = sys.modules.get("torch")
    sys.modules["torch"] = _FakeTorch
    try:
        arrs, meta = _satvision_forward_batch(
            _FakeModel(),
            [np.arange(16, dtype=np.float32).reshape(4, 2, 2)],
            device="cpu",
            output_mode="grid",
        )
    finally:
        if real_torch is not None:
            sys.modules["torch"] = real_torch
        else:
            del sys.modules["torch"]

    assert len(arrs) == 1
    assert arrs[0].shape == (4, 4)
    assert meta["forward_path"] == "manual_last_stage"
    assert meta["tokens_kind"] == "tokens_feature_map_bhwc"


def test_satvision_single_forces_unit_norm_when_fetch_is_unit_scaled(monkeypatch):
    import rs_embed.embedders.onthefly_satvision_toa as sv

    emb = SatVisionTOAEmbedder()
    monkeypatch.setattr(emb, "_get_provider", lambda _backend: object())
    monkeypatch.setattr(
        emb,
        "_resolve_runtime",
        lambda **kw: {
            "model": object(),
            "model_meta": {},
            "device": "cpu",
            "model_id": "nasa-cisto-data-science-group/satvision-toa-giant-patch8-window8-128",
            "image_size": 8,
            "in_chans": 14,
            "norm_mode": "raw",
            "reflectance_indices": (0, 1, 2, 3, 4, 6),
            "emissive_indices": (5, 7, 8, 9, 10, 11, 12, 13),
            "reflectance_divisor": 10000.0,
            "emissive_mins": (175.0,) * 8,
            "emissive_maxs": (375.0,) * 8,
        },
    )
    monkeypatch.setattr(
        sv,
        "_fetch_toa_chw_from_gee",
        lambda provider, spatial, temporal, sensor: (
            np.full((14, 8, 8), 0.5, dtype=np.float32),
            {"fallback_used": True, "already_unit_scaled": True},
        ),
    )
    seen = {}

    def _fake_prepare(raw_chw, **kw):
        seen["norm_mode"] = kw["norm_mode"]
        return np.asarray(raw_chw, dtype=np.float32)

    monkeypatch.setattr(emb, "_prepare_input", _fake_prepare)
    monkeypatch.setattr(
        sv,
        "_satvision_forward_batch",
        lambda model, x_chw_batch, **kw: (
            [np.full((4,), 1.0, dtype=np.float32)],
            {"tokens_kind": "pooled"},
        ),
    )

    sensor = SensorSpec(
        collection="TEST/COLL",
        bands=tuple(f"B{i}" for i in range(14)),
        scale_m=500,
    )
    out = emb.get_embedding(
        spatial=PointBuffer(lon=0.0, lat=0.0, buffer_m=256),
        temporal=TemporalSpec.range("2020-01-01", "2020-01-31"),
        sensor=sensor,
        output=OutputSpec.pooled(),
        backend="gee",
    )
    assert seen["norm_mode"] == "unit"
    assert out.meta["fallback_used"] is True
    assert out.meta["norm_mode_effective"] == "unit"
