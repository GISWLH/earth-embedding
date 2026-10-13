import os
import sys
import types

import numpy as np
import pytest

from rs_embed.core.errors import ModelError
from rs_embed.embedders._vendor import copernicus_embed as cop_mod


class _FakeTag:
    def __init__(self, value):
        self.value = value


class _FakeTiffFile:
    def __init__(self, path: str, shape: tuple[int, int, int]):
        self.path = path
        self.series = [types.SimpleNamespace(shape=shape)]
        self.pages = [
            types.SimpleNamespace(
                tags={
                    "ModelPixelScaleTag": _FakeTag((0.25, 0.25, 0.0)),
                    "ModelTiepointTag": _FakeTag((0.0, 0.0, 0.0, -180.0, 90.125, 0.0)),
                }
            )
        ]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_resolve_embed_tif_path_downloads_when_missing(monkeypatch, tmp_path):
    fake_hf = types.ModuleType("huggingface_hub")

    def _fake_download(**kwargs):
        path = tmp_path / kwargs["filename"]
        path.write_bytes(b"x" * 16)
        return str(path)

    fake_hf.hf_hub_download = _fake_download
    monkeypatch.setitem(sys.modules, "huggingface_hub", fake_hf)
    monkeypatch.setattr(cop_mod, "_validate_large_file", lambda path, min_bytes=0: path)

    out = cop_mod.resolve_embed_tif_path(data_dir=str(tmp_path), auto_download=True)

    assert out.endswith(cop_mod.HF_FILENAME)
    assert os.path.exists(out)


def test_load_geotiff_meta_reads_tags(monkeypatch, tmp_path):
    fake_path = tmp_path / cop_mod.HF_FILENAME
    fake_path.write_bytes(b"x")

    fake_tifffile = types.ModuleType("tifffile")
    fake_tifffile.TiffFile = lambda path: _FakeTiffFile(path, (768, 721, 1440))
    monkeypatch.setitem(sys.modules, "tifffile", fake_tifffile)
    monkeypatch.setattr(cop_mod, "_validate_large_file", lambda path, min_bytes=0: path)

    meta = cop_mod.load_geotiff_meta(str(fake_path))

    assert meta.axis_order == "chw"
    assert meta.bands == 768
    assert meta.height == 721
    assert meta.width == 1440
    assert meta.left == -180.0
    assert meta.top == 90.125
    assert meta.right == 180.0
    assert meta.bottom == -90.125


def test_copernicus_geotiff_dataset_slices_bbox(monkeypatch, tmp_path):
    fake_path = tmp_path / cop_mod.HF_FILENAME
    fake_path.write_bytes(b"x")
    fake_arr = np.arange(2 * 721 * 1440, dtype=np.float32).reshape(2, 721, 1440)

    fake_tifffile = types.ModuleType("tifffile")
    fake_tifffile.TiffFile = lambda path: _FakeTiffFile(path, fake_arr.shape)
    fake_tifffile.memmap = lambda path: fake_arr

    monkeypatch.setitem(sys.modules, "tifffile", fake_tifffile)
    monkeypatch.setattr(cop_mod, "_validate_large_file", lambda path, min_bytes=0: path)

    ds = cop_mod.CopernicusEmbedGeoTiff(paths=str(tmp_path), download=False)
    sample = ds[-180.0:-179.5, 89.625:90.125]

    assert sample["image"].shape == (2, 2, 2)
    np.testing.assert_array_equal(sample["window"], np.array([0, 2, 0, 2], dtype=np.int64))
    np.testing.assert_array_equal(sample["image"], fake_arr[:, 0:2, 0:2])


def test_copernicus_geotiff_dataset_rejects_subpixel_bbox(monkeypatch, tmp_path):
    fake_path = tmp_path / cop_mod.HF_FILENAME
    fake_path.write_bytes(b"x")
    fake_arr = np.arange(2 * 721 * 1440, dtype=np.float32).reshape(2, 721, 1440)

    fake_tifffile = types.ModuleType("tifffile")
    fake_tifffile.TiffFile = lambda path: _FakeTiffFile(path, fake_arr.shape)
    fake_tifffile.memmap = lambda path: fake_arr

    monkeypatch.setitem(sys.modules, "tifffile", fake_tifffile)
    monkeypatch.setattr(cop_mod, "_validate_large_file", lambda path, min_bytes=0: path)

    ds = cop_mod.CopernicusEmbedGeoTiff(paths=str(tmp_path), download=False)

    try:
        ds[-180.0:-179.9, 90.0:90.1]
    except Exception as e:
        assert "smaller than one dataset pixel" in str(e)
    else:
        raise AssertionError("Expected a subpixel bbox to raise an error.")


def test_copernicus_geotiff_falls_back_when_source_is_not_memmappable(monkeypatch, tmp_path):
    fake_path = tmp_path / cop_mod.HF_FILENAME
    fake_path.write_bytes(b"x")
    fake_arr = np.arange(2 * 721 * 1440, dtype=np.float32).reshape(2, 721, 1440)

    class _FallbackTiffFile(_FakeTiffFile):
        def asarray(self, *args, **kwargs):
            assert kwargs.get("series", 0) == 0
            assert kwargs.get("out") == "memmap"
            return fake_arr

    fake_tifffile = types.ModuleType("tifffile")
    fake_tifffile.TiffFile = lambda path: _FallbackTiffFile(path, fake_arr.shape)

    def _fake_memmap(path):
        raise ValueError("image data are not memory-mappable")

    fake_tifffile.memmap = _fake_memmap

    monkeypatch.setitem(sys.modules, "tifffile", fake_tifffile)
    monkeypatch.setattr(cop_mod, "_validate_large_file", lambda path, min_bytes=0: path)
    monkeypatch.setattr(cop_mod, "_COPERNICUS_MEMMAP_FALLBACK_WARNED", False)

    ds = cop_mod.CopernicusEmbedGeoTiff(paths=str(tmp_path), download=False)
    with pytest.warns(UserWarning, match="not directly memory-mappable"):
        sample = ds[-180.0:-179.5, 89.625:90.125]

    assert sample["image"].shape == (2, 2, 2)
    np.testing.assert_array_equal(sample["image"], fake_arr[:, 0:2, 0:2])


def test_copernicus_geotiff_reports_missing_imagecodecs(monkeypatch, tmp_path):
    fake_path = tmp_path / cop_mod.HF_FILENAME
    fake_path.write_bytes(b"x")
    fake_arr = np.arange(2 * 721 * 1440, dtype=np.float32).reshape(2, 721, 1440)

    class _ImagecodecsTiffFile(_FakeTiffFile):
        def asarray(self, *args, **kwargs):
            raise ValueError("<PREDICTOR.FLOATINGPOINT: 3> requires the 'imagecodecs' package")

    fake_tifffile = types.ModuleType("tifffile")
    fake_tifffile.TiffFile = lambda path: _ImagecodecsTiffFile(path, fake_arr.shape)

    def _fake_memmap(path):
        raise ValueError("image data are not memory-mappable")

    fake_tifffile.memmap = _fake_memmap

    monkeypatch.setitem(sys.modules, "tifffile", fake_tifffile)
    monkeypatch.setattr(cop_mod, "_validate_large_file", lambda path, min_bytes=0: path)
    monkeypatch.setattr(cop_mod, "_COPERNICUS_MEMMAP_FALLBACK_WARNED", False)

    ds = cop_mod.CopernicusEmbedGeoTiff(paths=str(tmp_path), download=False)
    with pytest.warns(UserWarning, match="not directly memory-mappable"):
        with pytest.raises(ModelError, match="requires 'imagecodecs'"):
            ds[-180.0:-179.5, 89.625:90.125]
