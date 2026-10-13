from rs_embed.core.specs import FetchSpec, PointBuffer
from rs_embed.core.types import ExportConfig, ExportTarget
from rs_embed.export import export_npz


def test_export_npz_delegates(monkeypatch, tmp_path):
    captured = {}

    def _fake_export_batch(**kwargs):
        captured.update(kwargs)
        return {"ok": True}

    monkeypatch.setattr("rs_embed.api.export_batch", _fake_export_batch)

    out = export_npz(
        spatial=PointBuffer(lon=0.0, lat=0.0, buffer_m=10),
        temporal=None,
        models=["mock_model"],
        out_path=str(tmp_path / "one"),
        config=ExportConfig(save_inputs=False, save_embeddings=False, save_manifest=False),
    )

    assert out == {"ok": True}
    assert captured["config"].format == "npz"
    assert captured["spatials"]
    assert isinstance(captured["target"], ExportTarget)
    assert captured["target"].out_file.endswith(".npz")


def test_export_npz_delegates_fetch(monkeypatch, tmp_path):
    captured = {}

    def _fake_export_batch(**kwargs):
        captured.update(kwargs)
        return {"ok": True}

    monkeypatch.setattr("rs_embed.api.export_batch", _fake_export_batch)

    out = export_npz(
        spatial=PointBuffer(lon=0.0, lat=0.0, buffer_m=10),
        temporal=None,
        models=["mock_model"],
        out_path=str(tmp_path / "one"),
        fetch=FetchSpec(scale_m=20),
    )

    assert out == {"ok": True}
    assert captured["fetch"] == FetchSpec(scale_m=20)
    assert captured["config"].format == "npz"


def test_export_npz_forces_npz_format_even_when_config_specifies_other(monkeypatch, tmp_path):
    """export_npz always forces format='npz', overriding any config.format value."""
    captured = {}

    def _fake_export_batch(**kwargs):
        captured.update(kwargs)
        return {"ok": True}

    monkeypatch.setattr("rs_embed.api.export_batch", _fake_export_batch)

    export_npz(
        spatial=PointBuffer(lon=0.0, lat=0.0, buffer_m=10),
        temporal=None,
        models=["mock_model"],
        out_path=str(tmp_path / "one"),
        config=ExportConfig(format="netcdf"),
    )

    assert captured["config"].format == "npz"
