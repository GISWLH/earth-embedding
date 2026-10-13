import numpy as np
import pandas as pd
import pytest

from rs_embed.aef import aef_url, dequantize_aef, find_aef_tiles, sample_aef
from rs_embed.core.errors import ModelError, SpecError
from rs_embed.core.specs import BBox


def test_signed_dequantization_and_nodata():
    result = dequantize_aef(np.array([-128, -127, -64, 0, 64, 127], dtype=np.int8))
    assert np.isnan(result[0])
    np.testing.assert_allclose(
        result[1:],
        [-((127 / 127.5) ** 2), -((64 / 127.5) ** 2), 0, (64 / 127.5) ** 2, (127 / 127.5) ** 2],
        rtol=1e-6,
    )
    with pytest.raises(ValueError):
        dequantize_aef(np.array([255], dtype=np.uint8))


def test_index_filters_year_and_bounds(tmp_path):
    path = "gs://alphaearth_foundations/satellite_embedding/v1/annual/2021/50N/example.tiff"
    frame = pd.DataFrame(
        [
            dict(
                path=path, year=2021, wgs84_west=114, wgs84_east=115, wgs84_south=30, wgs84_north=31
            ),
            dict(
                path=path.replace("2021", "2022"),
                year=2022,
                wgs84_west=114,
                wgs84_east=115,
                wgs84_south=30,
                wgs84_north=31,
            ),
        ]
    )
    index = tmp_path / "index.csv"
    frame.to_csv(index, index=False)
    assert find_aef_tiles(index, spatial=BBox(114.4, 30.4, 114.5, 30.5), year=2021) == [
        aef_url(path)
    ]
    assert find_aef_tiles(frame, spatial=BBox(10, 20, 11, 21), year=2021) == []
    with pytest.raises(SpecError, match="Invalid bbox"):
        find_aef_tiles(frame, spatial=BBox(np.nan, 20, 11, 21), year=2021)


def test_real_geotiff_sampling_masks_and_lonlat(tmp_path):
    rasterio = pytest.importorskip("rasterio")
    from rasterio.transform import from_origin

    path = tmp_path / "fixture.tiff"
    raw = np.full((64, 2, 2), 64, dtype=np.int8)
    raw[:, 0, 1] = -128
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        height=2,
        width=2,
        count=64,
        dtype="int8",
        crs="EPSG:4326",
        transform=from_origin(114, 31, 0.5, 0.5),
        nodata=-128,
    ) as dst:
        dst.write(raw)
    points = [[114.25, 30.75], [114.75, 30.75], [113, 30]]
    result = sample_aef(points, tiles=[path], strict=False)
    assert result.data.shape == (3, 64)
    np.testing.assert_allclose(result.data[0], (64 / 127.5) ** 2, rtol=1e-6)
    assert np.isnan(result.data[1:]).all()
    assert result.meta["valid_points"] == 1
    with pytest.raises(ModelError, match="point indices"):
        sample_aef(points, tiles=[path])


@pytest.mark.parametrize("points", [[[91, 181]], [[np.nan, 20]], [114, 30]])
def test_bad_coordinates_rejected_before_io(points):
    with pytest.raises(ValueError):
        sample_aef(points, tiles=[])


def test_global_batch_preserves_points_outside_each_utm_projection(tmp_path):
    rasterio = pytest.importorskip("rasterio")
    from pyproj import Transformer
    from rasterio.transform import from_origin

    points = [[114.0, 30.0], [27.0, 0.0]]
    paths = []
    for i, (point, crs) in enumerate(zip(points, ["EPSG:32650", "EPSG:32635"], strict=True)):
        x, y = Transformer.from_crs("EPSG:4326", crs, always_xy=True).transform(*point)
        path = tmp_path / f"zone-{i}.tiff"
        with rasterio.open(
            path,
            "w",
            driver="GTiff",
            height=1,
            width=1,
            count=64,
            dtype="int8",
            crs=crs,
            transform=from_origin(x - 5, y + 5, 10, 10),
            nodata=-128,
        ) as dst:
            dst.write(np.full((64, 1, 1), 32 + i, dtype=np.int8))
        paths.append(path)

    partial = sample_aef(points, tiles=paths[:1], strict=False)
    assert np.isfinite(partial.data[0]).all()
    assert np.isnan(partial.data[1]).all()
    result = sample_aef(points, tiles=paths)
    np.testing.assert_allclose(result.data[:, 0], (np.array([32, 33]) / 127.5) ** 2, rtol=1e-6)
    assert result.meta["source_for_point"] == [str(p) for p in paths]


@pytest.mark.parametrize("level", [-1, 13, True, 1.5, "6"])
def test_invalid_overview_rejected_before_io(level):
    with pytest.raises(ValueError, match="overview_level"):
        sample_aef([[-122, 38]], tiles=[], overview_level=level)


def test_south_up_overview_preserves_geographic_orientation(tmp_path):
    rasterio = pytest.importorskip("rasterio")
    from affine import Affine
    from rasterio.enums import Resampling

    path = tmp_path / "south-up.tiff"
    raw = np.full((64, 4, 4), 32, dtype=np.int8)
    raw[:, 2:, :] = 64
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        height=4,
        width=4,
        count=64,
        dtype="int8",
        crs="EPSG:4326",
        transform=Affine(0.01, 0, -122, 0, 0.01, 37),
        nodata=-128,
    ) as dst:
        dst.write(raw)
        dst.build_overviews([2], Resampling.nearest)
    result = sample_aef([[-121.99, 37.01], [-121.99, 37.03]], tiles=[path], overview_level=0)
    np.testing.assert_allclose(result.data[:, 0], (np.array([32, 64]) / 127.5) ** 2, rtol=1e-6)
    assert result.meta["overview_level"] == 0
