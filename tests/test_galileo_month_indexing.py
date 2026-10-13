import importlib
import sys
import types

import numpy as np
import pytest

from rs_embed.core.specs import TemporalSpec

sys.modules.setdefault("xarray", types.SimpleNamespace(DataArray=object))
gal = importlib.import_module("rs_embed.embedders.onthefly_galileo")
_frame_month_sequence = gal._frame_month_sequence
_galileo_forward = gal._galileo_forward
_is_galileo_official_stats_mode = gal._is_galileo_official_stats_mode
_month_from_iso = gal._month_from_iso
_month_override_sequence = gal._month_override_sequence


def test_galileo_month_from_iso_is_zero_based():
    assert _month_from_iso("2022-01-15") == 0
    assert _month_from_iso("2022-06-15") == 5
    assert _month_from_iso("2022-12-15") == 11


def test_galileo_frame_month_sequence_stays_within_embedding_range():
    months = _frame_month_sequence(
        TemporalSpec.range("2022-01-01", "2023-01-01"),
        n_frames=8,
    )

    assert months.dtype == np.int64
    assert months.shape == (8,)
    assert int(months.min()) >= 0
    assert int(months.max()) <= 11
    assert 11 in months.tolist()


def test_galileo_month_override_sequence_converts_to_zero_based():
    jan = _month_override_sequence(1, n_frames=3)
    dec = _month_override_sequence(12, n_frames=2)

    assert jan.dtype == np.int64
    assert jan.tolist() == [0, 0, 0]
    assert dec.tolist() == [11, 11]


def test_galileo_official_stats_mode_aliases():
    assert _is_galileo_official_stats_mode("official_stats") is True
    assert _is_galileo_official_stats_mode("pretrain_stats") is True
    assert _is_galileo_official_stats_mode("pretraining_stats") is True
    assert _is_galileo_official_stats_mode("galileo_stats") is True
    assert _is_galileo_official_stats_mode("none") is False
    assert _is_galileo_official_stats_mode("unit_scale") is False


def test_galileo_grid_prefers_official_patch_mean():
    torch = pytest.importorskip("torch", exc_type=ImportError)

    class _FakeEncoder:
        def to(self, _dev):
            return self

        def eval(self):
            return self

        def __call__(
            self,
            s_t_x,
            sp_x,
            t_x,
            st_x,
            s_t_m,
            sp_m,
            t_m,
            st_m,
            months,
            **_kw,
        ):
            return (s_t_x, sp_x, t_x, st_x, s_t_m, sp_m, t_m, st_m, months)

        def average_tokens(self, *_args):
            return torch.tensor([[1.0, 2.0, 3.0]], dtype=torch.float32)

        def apply_mask_and_average_tokens_per_patch(self, *_args):
            # [B,S,D] where S == H*W == 2*3
            return torch.arange(1, 1 + (1 * 6 * 4), dtype=torch.float32).reshape(1, 6, 4)

    data = {
        "s_t_x": torch.zeros((1, 2, 3, 4, 5, 7), dtype=torch.float32),
        "sp_x": torch.zeros((1, 2, 3, 1, 7), dtype=torch.float32),
        "t_x": torch.zeros((1, 4, 1, 7), dtype=torch.float32),
        "st_x": torch.zeros((1, 1, 7), dtype=torch.float32),
        "s_t_m": torch.zeros((1, 2, 3, 4, 5), dtype=torch.float32),
        "sp_m": torch.ones((1, 2, 3, 1), dtype=torch.float32),
        "t_m": torch.ones((1, 4, 1), dtype=torch.float32),
        "st_m": torch.ones((1, 1), dtype=torch.float32),
        "months": torch.zeros((1, 4), dtype=torch.int64),
    }

    vec, grid, meta = _galileo_forward(
        _FakeEncoder(),
        data,
        mod=types.SimpleNamespace(SPACE_TIME_BANDS_GROUPS_IDX={"S2_RGB": [0]}),
        patch_size=8,
        add_layernorm_on_exit=True,
        device="cpu",
    )

    assert vec.tolist() == [1.0, 2.0, 3.0]
    assert grid.shape == (4, 2, 3)
    assert meta["grid_kind"] == "patch_tokens"
    assert meta["grid_source"] == "official_patch_mean"
    # First patch token [1,2,3,4] should map to spatial location (0,0).
    assert np.allclose(grid[:, 0, 0], np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float32))
    # Last patch token [21,22,23,24] should map to spatial location (1,2).
    assert np.allclose(grid[:, 1, 2], np.array([21.0, 22.0, 23.0, 24.0], dtype=np.float32))
