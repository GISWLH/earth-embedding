import os

import numpy as np
import pytest

import rs_embed.embedders.onthefly_agrifm as ag
from rs_embed.core.errors import ModelError
from rs_embed.core.specs import OutputSpec, PointBuffer, TemporalSpec

_ENV_KEYS = [
    "RS_EMBED_AGRIFM_CKPT",
    "RS_EMBED_AGRIFM_AUTO_DOWNLOAD",
    "RS_EMBED_AGRIFM_CKPT_URL",
    "RS_EMBED_AGRIFM_CACHE_DIR",
    "RS_EMBED_AGRIFM_CKPT_FILE",
    "RS_EMBED_AGRIFM_CKPT_MIN_BYTES",
]


def _clear_agrifm_env(monkeypatch):
    for k in _ENV_KEYS:
        monkeypatch.delenv(k, raising=False)


def test_resolve_agrifm_ckpt_uses_local_env_path(monkeypatch, tmp_path):
    _clear_agrifm_env(monkeypatch)
    p = tmp_path / "local_agrifm.pth"
    p.write_bytes(b"123")
    monkeypatch.setenv("RS_EMBED_AGRIFM_CKPT", str(p))

    def _should_not_be_called(**_kw):
        raise AssertionError("auto-download should not be called when RS_EMBED_AGRIFM_CKPT is set")

    monkeypatch.setattr(ag, "_download_agrifm_ckpt", _should_not_be_called)
    assert ag._resolve_ckpt_path() == os.path.expanduser(str(p))


def test_resolve_agrifm_ckpt_local_missing_raises(monkeypatch):
    _clear_agrifm_env(monkeypatch)
    monkeypatch.setenv("RS_EMBED_AGRIFM_CKPT", "/tmp/not_exist_agrifm_xxx.pth")

    with pytest.raises(ModelError, match="does not exist"):
        ag._resolve_ckpt_path()


def test_resolve_agrifm_ckpt_auto_download_disabled_raises(monkeypatch):
    _clear_agrifm_env(monkeypatch)
    monkeypatch.setenv("RS_EMBED_AGRIFM_AUTO_DOWNLOAD", "0")

    with pytest.raises(ModelError, match="checkpoint is required"):
        ag._resolve_ckpt_path()


def test_resolve_agrifm_ckpt_uses_default_auto_download(monkeypatch):
    _clear_agrifm_env(monkeypatch)
    seen = {}

    def _fake_download(*, url, cache_dir, filename, min_bytes):
        seen["url"] = url
        seen["cache_dir"] = cache_dir
        seen["filename"] = filename
        seen["min_bytes"] = min_bytes
        return "/tmp/agrifm_from_auto/AgriFM.pth"

    monkeypatch.setattr(ag, "_download_agrifm_ckpt", _fake_download)
    out = ag._resolve_ckpt_path()
    assert out == "/tmp/agrifm_from_auto/AgriFM.pth"
    assert seen["url"] == ag._AGRIFM_DEFAULT_CKPT_URL
    assert seen["filename"] == ag._AGRIFM_DEFAULT_CKPT_FILENAME
    assert seen["min_bytes"] == ag._AGRIFM_DEFAULT_MIN_BYTES


def test_agrifm_chw_repeat_to_t_warns_and_records_meta(monkeypatch):
    _clear_agrifm_env(monkeypatch)
    monkeypatch.setenv("RS_EMBED_AGRIFM_FRAMES", "4")
    monkeypatch.setattr(ag, "_resolve_ckpt_path", lambda: "/tmp/fake_agrifm.pth")
    monkeypatch.setattr(ag, "_load_agrifm", lambda *, ckpt_path, device: (object(), {}, "cpu"))
    monkeypatch.setattr(
        ag,
        "_agrifm_forward_grid",
        lambda model, x_tchw, *, device: (
            np.ones((2, 3, 3), dtype=np.float32),
            {"feature_shape": (1, 2, 3, 3)},
        ),
    )

    import rs_embed.tools.inspection as inspection

    monkeypatch.setattr(inspection, "maybe_inspect_chw", lambda *args, **kwargs: None)
    monkeypatch.setattr(inspection, "checks_should_raise", lambda sensor: False)

    with pytest.warns(UserWarning, match="repeating it to T=4"):
        emb = ag.AgriFMEmbedder().get_embedding(
            spatial=PointBuffer(lon=0.0, lat=0.0, buffer_m=128),
            temporal=TemporalSpec.range("2020-06-01", "2020-08-31"),
            sensor=None,
            output=OutputSpec.pooled(),
            backend="gee",
            input_chw=np.ones((10, 8, 8), dtype=np.float32),
        )

    assert emb.meta["input_mode"] == "chw_repeated_to_t"
    assert emb.meta["input_original_frames"] == 1
    assert emb.meta["input_repeated_to_t"] is True
    assert emb.meta["input_frames"] == 4
