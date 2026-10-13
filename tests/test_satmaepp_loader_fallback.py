import json
import sys
import types

from rs_embed.embedders.onthefly_satmaepp import (
    _canonicalize_satmaepp_config,
    _load_satmaepp_cached,
)


def test_canonicalize_satmaepp_config_accepts_input_channel_aliases():
    cfg = _canonicalize_satmaepp_config(
        {
            "num_channels": 3,
            "image_size": 224,
            "patch_size": 16,
            "hidden_size": 1024,
            "num_hidden_layers": 24,
            "num_attention_heads": 16,
        }
    )

    assert cfg["in_chans"] == 3
    assert cfg["img_size"] == 224
    assert cfg["embed_dim"] == 1024
    assert cfg["depth"] == 24
    assert cfg["num_heads"] == 16
    assert cfg["decoder_embed_dim"] == 512


def test_load_satmaepp_cached_falls_back_when_from_pretrained_needs_in_chans(monkeypatch, tmp_path):
    import rs_embed.embedders.onthefly_satmaepp as satpp

    satpp._load_satmaepp_cached.cache_clear()
    monkeypatch.setattr(satpp, "ensure_torch", lambda: None)

    snapshot_dir = tmp_path / "snapshot"
    snapshot_dir.mkdir()
    (snapshot_dir / "config.json").write_text(
        json.dumps(
            {
                "in_chans": 3,
                "img_size": 224,
                "patch_size": 16,
                "embed_dim": 1024,
                "depth": 24,
                "num_heads": 16,
                "decoder_embed_dim": 512,
                "decoder_depth": 8,
                "decoder_num_heads": 16,
                "mlp_ratio": 4.0,
                "proj_ratio": 4,
                "norm_pix_loss": False,
            }
        ),
        encoding="utf-8",
    )
    (snapshot_dir / "pytorch_model.bin").write_text("placeholder", encoding="utf-8")

    class FakeSatMAEPP:
        def __init__(self, config):
            self.config = types.SimpleNamespace(**config)
            self.loaded_state_dict = None

        @classmethod
        def from_pretrained(cls, _model_id):
            raise AttributeError("'PreTrainedConfig' object has no attribute 'in_chans'")

        def load_state_dict(self, state_dict, strict=True):
            self.loaded_state_dict = (state_dict, strict)

        def to(self, _dev):
            return self

        def eval(self):
            return self

    monkeypatch.setitem(sys.modules, "rshf", types.ModuleType("rshf"))
    monkeypatch.setitem(sys.modules, "rshf.satmaepp", types.SimpleNamespace(SatMAEPP=FakeSatMAEPP))
    monkeypatch.setitem(
        sys.modules,
        "huggingface_hub",
        types.SimpleNamespace(snapshot_download=lambda **kwargs: str(snapshot_dir)),
    )
    monkeypatch.setitem(
        sys.modules,
        "torch",
        types.SimpleNamespace(load=lambda *args, **kwargs: {"state_dict": {"weight": 1}}),
    )

    model, meta = _load_satmaepp_cached("fake/satmaepp", "cpu")

    assert isinstance(model, FakeSatMAEPP)
    assert model.config.in_chans == 3
    assert model.loaded_state_dict == ({"weight": 1}, True)
    assert meta["load_mode"] == "manual_snapshot"
    assert meta["in_chans"] == 3
