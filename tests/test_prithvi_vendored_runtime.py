import json
import sys
from datetime import datetime
from types import SimpleNamespace

import numpy as np


class _FakeTensor:
    def __init__(self, data):
        self.data = np.asarray(data, dtype=np.float32)

    @property
    def shape(self):
        return self.data.shape

    @property
    def ndim(self):
        return self.data.ndim

    def __getitem__(self, item):
        return _FakeTensor(self.data[item])

    def unsqueeze(self, dim):
        return _FakeTensor(np.expand_dims(self.data, axis=dim))

    def to(self, _device):
        return self

    def detach(self):
        return self

    def float(self):
        return self

    def cpu(self):
        return self

    def clone(self):
        return _FakeTensor(self.data.copy())

    def numpy(self):
        return self.data.copy()

    def tolist(self):
        return self.data.tolist()


class _FakeTorchModule:
    float32 = np.float32

    @staticmethod
    def from_numpy(arr):
        return _FakeTensor(arr)

    @staticmethod
    def tensor(data, dtype=None, device=None):
        return _FakeTensor(data)

    class no_grad:
        def __enter__(self):
            return None

        def __exit__(self, exc_type, exc, tb):
            return False


class _FakePandasModule:
    @staticmethod
    def to_datetime(value):
        dt = datetime.fromisoformat(str(value))
        return SimpleNamespace(
            year=dt.year,
            dayofyear=float(dt.timetuple().tm_yday),
        )


class _FakePrithviModel:
    def __init__(self, **kwargs):
        self.init_kwargs = kwargs
        self.encoder = type("Encoder", (), {"pos_embed": object()})()
        self.decoder = type("Decoder", (), {"decoder_pos_embed": object()})()
        self.loaded_state = None
        self.forward_seen = None

    def load_state_dict(self, state_dict, strict=True):
        self.loaded_state = dict(state_dict)
        self.loaded_state["strict"] = strict

    def eval(self):
        return self

    def to(self, _device):
        return self

    def forward_features(self, x, temporal_coords=None, location_coords=None):
        self.forward_seen = {
            "x_shape": tuple(x.shape),
            "temporal_coords": temporal_coords.clone(),
            "location_coords": location_coords.clone(),
        }
        return [_FakeTensor(np.arange(12, dtype=np.float32).reshape(1, 3, 4))]


def test_load_prithvi_cached_uses_vendored_runtime(monkeypatch, tmp_path):
    import rs_embed.embedders.onthefly_prithvi as pr

    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(
        json.dumps(
            {
                "pretrained_cfg": {
                    "img_size": 224,
                    "num_frames": 4,
                    "patch_size": [1, 16, 16],
                    "in_chans": 6,
                    "embed_dim": 768,
                    "depth": 12,
                    "num_heads": 12,
                    "decoder_embed_dim": 512,
                    "decoder_depth": 8,
                    "decoder_num_heads": 16,
                    "mlp_ratio": 4,
                    "coords_encoding": ["time", "location"],
                    "coords_scale_learn": True,
                    "mask_ratio": 0.75,
                    "norm_pix_loss": False,
                    "bands": ["B02", "B03", "B04", "B05", "B06", "B07"],
                }
            }
        ),
        encoding="utf-8",
    )
    ckpt_path = tmp_path / "weights.pt"
    encoder_pos_embed = object()
    decoder_pos_embed = object()

    pr._load_prithvi_cached.cache_clear()
    monkeypatch.setattr(pr, "ensure_torch", lambda: None)
    monkeypatch.setattr(
        pr,
        "_download_prithvi_file",
        lambda repo_id, filename, cache_dir: str(
            cfg_path if filename == "config.json" else ckpt_path
        ),
    )

    def _fake_loader():
        model = _FakePrithviModel
        return model

    monkeypatch.setattr(pr, "_load_prithvi_module", _fake_loader)
    monkeypatch.setattr(
        pr,
        "_torch_load_checkpoint_compat",
        lambda _path: {
            "encoder.pos_embed": encoder_pos_embed,
            "decoder.decoder_pos_embed": decoder_pos_embed,
            "some.weight": "value",
        },
    )

    model, meta = pr._load_prithvi_cached(
        model_key="prithvi_eo_v2_100_tl",
        pretrained=True,
        bands=tuple(pr.PRITHVI_S2_BANDS_DST),
        num_frames=1,
        coords_encoding=("time", "location"),
        dev="cpu",
    )

    assert isinstance(model, _FakePrithviModel)
    assert model.init_kwargs["num_frames"] == 1
    assert model.init_kwargs["in_chans"] == 6
    assert tuple(model.init_kwargs["coords_encoding"]) == ("time", "location")
    assert meta["repo_id"] == "ibm-nasa-geospatial/Prithvi-EO-2.0-100M-TL"
    assert meta["checkpoint"] == "Prithvi_EO_V2_100M_TL.pt"
    assert meta["checkpoint_path"] == str(ckpt_path)
    assert model.loaded_state["encoder.pos_embed"] is model.encoder.pos_embed
    assert model.loaded_state["decoder.decoder_pos_embed"] is model.decoder.decoder_pos_embed
    assert model.loaded_state["strict"] is True


def test_prithvi_forward_tokens_uses_hf_coord_convention(monkeypatch):
    import rs_embed.embedders.onthefly_prithvi as pr

    monkeypatch.setitem(sys.modules, "torch", _FakeTorchModule())
    monkeypatch.setitem(sys.modules, "pandas", _FakePandasModule())

    model = _FakePrithviModel()
    tokens = pr._prithvi_forward_tokens(
        model,
        np.zeros((6, 8, 8), dtype=np.float32),
        lon=10.0,
        lat=20.0,
        date_str="2022-06-01",
        device="cpu",
    )

    assert tokens.shape == (3, 4)
    assert model.forward_seen is not None
    assert model.forward_seen["x_shape"] == (1, 6, 8, 8)
    assert model.forward_seen["temporal_coords"].tolist() == [[[2022.0, 152.0]]]
    assert model.forward_seen["location_coords"].tolist() == [[20.0, 10.0]]
