"""Legacy official binary weights remain loadable with recent Hub mixins."""

import json
import sys
from types import SimpleNamespace

import pytest

from rs_embed.embedders import onthefly_scalemae as scale


def test_binary_fallback_loads_real_state_strictly(monkeypatch, tmp_path):
    torch = pytest.importorskip("torch")

    class TinyModel(torch.nn.Linear):
        def __init__(self, config=None):
            super().__init__(2, (config or {}).get("output_features", 3))

        @classmethod
        def from_pretrained(cls, model_id):
            raise FileNotFoundError("model.safetensors")

    expected = TinyModel()
    with torch.no_grad():
        expected.weight.fill_(0.25)
    torch.save(expected.state_dict(), tmp_path / "pytorch_model.bin")
    monkeypatch.setitem(sys.modules, "rshf.scalemae", SimpleNamespace(ScaleMAE=TinyModel))
    scale._load_scalemae_cached.cache_clear()
    try:
        model, meta = scale._load_scalemae_cached(str(tmp_path), "cpu")
        torch.testing.assert_close(model.weight, expected.weight)
        assert not model.training
        assert meta["load_mode"] == "strict_binary_checkpoint"
        assert meta["checkpoint_path"] == str(tmp_path / "pytorch_model.bin")
    finally:
        scale._load_scalemae_cached.cache_clear()


def test_binary_fallback_honors_config_and_rejects_partial_weights(tmp_path):
    torch = pytest.importorskip("torch")

    class TinyModel(torch.nn.Linear):
        def __init__(self, config=None):
            super().__init__(2, (config or {}).get("output_features", 3))

    (tmp_path / "config.json").write_text(json.dumps({"output_features": 4}))
    expected = TinyModel({"output_features": 4})
    torch.save({"model": expected.state_dict()}, tmp_path / "pytorch_model.bin")
    loaded, _ = scale._load_scalemae_binary_checkpoint(TinyModel, str(tmp_path))
    assert loaded.out_features == 4
    torch.save({"weight": expected.weight}, tmp_path / "pytorch_model.bin")
    with pytest.raises(RuntimeError, match="Missing key"):
        scale._load_scalemae_binary_checkpoint(TinyModel, str(tmp_path))
