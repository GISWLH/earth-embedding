import numpy as np

from rs_embed.core.specs import OutputSpec, PointBuffer, TemporalSpec
from rs_embed.embedders.onthefly_satmaepp_s2 import (
    SatMAEPPSentinel10Embedder,
    _ensure_satmaepp_s2_assets,
    _fetch_s2_sr_10_raw_chw,
)


def test_fetch_s2_sr_10_raw_chw_preserves_source_values(monkeypatch):
    import rs_embed.embedders.onthefly_satmaepp_s2 as satpp_s2

    raw = np.zeros((10, 2, 2), dtype=np.float32)
    raw[0, 0, 0] = -3.0
    raw[1, 0, 0] = 20001.0
    raw[2, 0, 0] = np.nan
    raw[3, 0, 0] = np.inf
    raw[4, 0, 0] = -np.inf

    monkeypatch.setattr(satpp_s2, "_fetch_collection_patch_chw", lambda *args, **kwargs: raw)

    out = _fetch_s2_sr_10_raw_chw(
        provider=object(),
        spatial=PointBuffer(lon=0.0, lat=0.0, buffer_m=256),
        temporal=TemporalSpec.year(2020),
        scale_m=10,
        cloudy_pct=30,
        composite="median",
        fill_value=0.0,
    )

    assert float(out[0, 0, 0]) == -3.0
    assert float(out[1, 0, 0]) == 20001.0
    assert np.isnan(out[2, 0, 0])
    assert np.isposinf(out[3, 0, 0])
    assert np.isneginf(out[4, 0, 0])


def test_satmaepp_s2_input_override_preserves_raw_values(monkeypatch):
    import rs_embed.embedders.onthefly_satmaepp_s2 as satpp_s2

    emb = SatMAEPPSentinel10Embedder()
    seen = {}

    def _fake_load(**kwargs):
        return object(), {"device": "cpu"}

    def _fake_forward_batch(model, raw_chw_batch, *, image_size, device):
        seen["raw"] = np.array(raw_chw_batch[0], copy=True)
        return [np.full((13, 2), 1.0, dtype=np.float32)]

    monkeypatch.setattr(satpp_s2, "_load_satmaepp_s2", _fake_load)
    monkeypatch.setattr(satpp_s2, "_satmaepp_s2_forward_tokens_batch", _fake_forward_batch)

    raw = np.zeros((10, 2, 2), dtype=np.float32)
    raw[0, 0, 0] = -7.0
    raw[1, 0, 0] = 12345.0
    raw[2, 0, 0] = np.nan

    emb.get_embedding(
        spatial=PointBuffer(lon=0.0, lat=0.0, buffer_m=256),
        temporal=TemporalSpec.year(2020),
        sensor=None,
        output=OutputSpec.pooled(),
        backend="gee",
        device="cpu",
        input_chw=raw,
    )

    assert float(seen["raw"][0, 0, 0]) == -7.0
    assert float(seen["raw"][1, 0, 0]) == 12345.0
    assert np.isnan(seen["raw"][2, 0, 0])


def test_satmaepp_s2_batch_input_override_preserves_raw_values(monkeypatch):
    import rs_embed.embedders.onthefly_satmaepp_s2 as satpp_s2

    emb = SatMAEPPSentinel10Embedder()
    seen = {}

    def _fake_load(**kwargs):
        return object(), {"device": "cpu"}

    def _fake_forward_batch(model, raw_chw_batch, *, image_size, device):
        seen["raw_batch"] = [np.array(x, copy=True) for x in raw_chw_batch]
        return [np.full((13, 2), 1.0, dtype=np.float32) for _ in raw_chw_batch]

    monkeypatch.setattr(satpp_s2, "_load_satmaepp_s2", _fake_load)
    monkeypatch.setattr(satpp_s2, "_satmaepp_s2_forward_tokens_batch", _fake_forward_batch)

    raw0 = np.zeros((10, 2, 2), dtype=np.float32)
    raw0[0, 0, 0] = -5.0
    raw1 = np.zeros((10, 2, 2), dtype=np.float32)
    raw1[1, 0, 0] = np.nan

    emb.get_embeddings_batch_from_inputs(
        spatials=[
            PointBuffer(lon=0.0, lat=0.0, buffer_m=256),
            PointBuffer(lon=1.0, lat=0.0, buffer_m=256),
        ],
        input_chws=[raw0, raw1],
        temporal=TemporalSpec.year(2020),
        sensor=None,
        output=OutputSpec.pooled(),
        backend="gee",
        device="cpu",
    )

    assert float(seen["raw_batch"][0][0, 0, 0]) == -5.0
    assert np.isnan(seen["raw_batch"][1][1, 0, 0])


def test_satmaepp_s2_assets_accept_local_checkpoint_file(tmp_path):
    ckpt = tmp_path / "checkpoint.pth"
    ckpt.write_bytes(b"ok")

    out = _ensure_satmaepp_s2_assets(
        ckpt_repo="unused/repo",
        ckpt_file=str(ckpt),
        cache_dir=None,
    )

    assert out == str(ckpt)
