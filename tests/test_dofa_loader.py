from __future__ import annotations

from types import SimpleNamespace

import numpy as np
import pytest
import torch
import torch.nn as nn

import rs_embed.embedders.onthefly_dofa as dofa


class _FakeDOFAModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.fc_norm = nn.LayerNorm(4)
        self.img_size = 224
        self.patch_size = 16
        self.embed_dim = 4
        self.global_pool = True
        self.loaded_state_dict = None

    def load_state_dict(self, state_dict, strict: bool = False):
        self.loaded_state_dict = dict(state_dict)
        return SimpleNamespace(missing_keys=["head.weight"], unexpected_keys=["mask_token"])


def test_unwrap_dofa_state_dict_strips_nested_prefixes():
    payload = {
        "state_dict": {
            "module.norm.weight": torch.ones(4),
            "module.norm.bias": torch.zeros(4),
        }
    }

    state_dict = dofa._unwrap_dofa_state_dict(payload)

    assert sorted(state_dict) == ["norm.bias", "norm.weight"]


def test_prepare_dofa_state_dict_copies_norm_to_fc_norm_and_drops_mismatch():
    model = _FakeDOFAModel()
    state_dict = {
        "norm.weight": torch.arange(4, dtype=torch.float32),
        "norm.bias": torch.arange(4, dtype=torch.float32) + 10,
        "fc_norm.weight": torch.ones(5, dtype=torch.float32),
    }

    filtered, missing, unexpected = dofa._prepare_dofa_state_dict_for_model(model, state_dict)

    assert torch.equal(filtered["fc_norm.weight"], state_dict["norm.weight"])
    assert torch.equal(filtered["fc_norm.bias"], state_dict["norm.bias"])
    assert missing == ["head.weight"]
    assert unexpected == ["mask_token"]


def test_load_dofa_model_cached_uses_hf_weight_path(monkeypatch):
    fake_model = _FakeDOFAModel()

    monkeypatch.setattr(dofa, "_build_dofa_model", lambda variant: fake_model)
    monkeypatch.setattr(
        dofa,
        "_resolve_dofa_weights_path",
        lambda spec: ("/tmp/dofa-base.pth", "https://example.invalid/dofa-base.pth"),
    )
    monkeypatch.setattr(
        torch,
        "load",
        lambda path, map_location=None: {
            "model": {
                "norm.weight": torch.ones(4, dtype=torch.float32),
                "norm.bias": torch.zeros(4, dtype=torch.float32),
            }
        },
    )

    dofa._load_dofa_model_cached.cache_clear()
    model, meta = dofa._load_dofa_model_cached("base", "cpu")

    assert model is fake_model
    assert meta["variant"] == "base"
    assert meta["weights_meta"]["filename"] == "DOFA_ViT_base_e100.pth"
    assert meta["weights_meta"]["path"] == "/tmp/dofa-base.pth"
    assert torch.equal(fake_model.loaded_state_dict["fc_norm.weight"], torch.ones(4))


def test_resolve_dofa_variant_prefers_model_config():
    variant = dofa._resolve_dofa_variant(
        model_config={"variant": "large"},
    )

    assert variant == "large"


def test_resolve_dofa_variant_defaults_to_base():
    variant = dofa._resolve_dofa_variant(model_config=None)

    assert variant == "base"


def test_normalize_dofa_input_chw_uses_official_s2_stats_by_band():
    raw = np.full((2, 1, 1), 5000.0, dtype=np.float32)

    x, meta = dofa._normalize_dofa_input_chw(
        raw,
        bands=["B4", "B12"],
        input_name="input_chw",
    )

    expected_b4 = (
        (5000.0 / 10000.0) * 255.0 - dofa._DOFA_S2_STATS_BY_BAND["B4"][0]
    ) / dofa._DOFA_S2_STATS_BY_BAND["B4"][1]
    expected_b12 = (
        (5000.0 / 10000.0) * 255.0 - dofa._DOFA_S2_STATS_BY_BAND["B12"][0]
    ) / dofa._DOFA_S2_STATS_BY_BAND["B12"][1]

    assert x.shape == (2, 1, 1)
    assert np.isclose(float(x[0, 0, 0]), expected_b4)
    assert np.isclose(float(x[1, 0, 0]), expected_b12)
    assert meta["normalization"] == "official_dofa_s2_stats"


def test_normalize_dofa_input_chw_rejects_already_normalized_inputs():
    raw = np.full((1, 2, 2), 1.0, dtype=np.float32)

    with pytest.raises(dofa.ModelError, match="expects raw Sentinel-2 SR values"):
        dofa._normalize_dofa_input_chw(
            raw,
            bands=["B4"],
            input_name="input_chw",
        )
