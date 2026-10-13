import numpy as np

from rs_embed.core.specs import OutputSpec, PointBuffer, TemporalSpec
from rs_embed.embedders._vit_mae_utils import fetch_s2_rgb_u8_from_provider
from rs_embed.embedders.onthefly_satmaepp import SatMAEPPEmbedder


def test_fetch_s2_rgb_u8_from_provider_allows_unresized_output(monkeypatch):
    class _P:
        def ensure_ready(self):
            return None

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
        return np.full((3, 11, 13), 5000.0, dtype=np.float32)

    monkeypatch.setattr(
        "rs_embed.embedders._vit_mae_utils.fetch_collection_patch_chw",
        _fake_fetch_collection_patch_chw,
    )
    monkeypatch.setattr(
        "rs_embed.embedders._vit_mae_utils.maybe_inspect_chw",
        lambda *args, **kwargs: None,
        raising=False,
    )

    sensor = SatMAEPPEmbedder.input_spec.to_sensor_spec()
    spatial = PointBuffer(lon=0.0, lat=0.0, buffer_m=256)
    temporal = TemporalSpec.year(2020)

    rgb_u8 = fetch_s2_rgb_u8_from_provider(
        spatial=spatial,
        temporal=temporal,
        sensor=sensor,
        out_size=None,
        provider=_P(),
    )

    assert rgb_u8.shape == (11, 13, 3)
    assert rgb_u8.dtype == np.uint8


def test_satmaepp_input_override_skips_pre_resize(monkeypatch):
    import rs_embed.embedders.onthefly_satmaepp as satpp

    emb = SatMAEPPEmbedder()
    seen = {}

    def _fake_load(*, model_id, device):
        return object(), {"device": "cpu"}

    def _fake_forward(model, rgb_u8, *, image_size, device, model_id):
        seen["shape"] = tuple(rgb_u8.shape)
        return np.full((4, 2), 1.0, dtype=np.float32)

    monkeypatch.setattr(satpp, "_load_satmaepp", _fake_load)
    monkeypatch.setattr(satpp, "_satmaepp_forward_tokens", _fake_forward)

    input_chw = np.full((3, 11, 13), 5000.0, dtype=np.float32)
    emb.get_embedding(
        spatial=PointBuffer(lon=0.0, lat=0.0, buffer_m=256),
        temporal=TemporalSpec.year(2020),
        sensor=None,
        output=OutputSpec.pooled(),
        backend="gee",
        device="cpu",
        input_chw=input_chw,
    )

    assert seen["shape"] == (11, 13, 3)
