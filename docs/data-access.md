# AlphaEarth Foundations: two access routes

`gse` is the precomputed Google Satellite Embedding product derived from
AlphaEarth Foundations. This repository does not distribute AEF model weights.

## Direct Cloud Storage

The official bucket is [`gs://alphaearth_foundations`](https://console.cloud.google.com/storage/browser/alphaearth_foundations).
Google documents provider-paid access as of July 2026. The current annual
release covers 2017–2025. Check the [official data guide](https://developers.google.com/earth-engine/guides/aef_on_gcs_readme)
for subsequent changes.

| Resource | Direct HTTPS link |
| --- | --- |
| CSV footprint index | [aef_index.csv](https://storage.googleapis.com/alphaearth_foundations/satellite_embedding/v1/annual/aef_index.csv) |
| GeoParquet index | [aef_index.parquet](https://storage.googleapis.com/alphaearth_foundations/satellite_embedding/v1/annual/aef_index.parquet) |
| GeoPackage index | [aef_index.gpkg](https://storage.googleapis.com/alphaearth_foundations/satellite_embedding/v1/annual/aef_index.gpkg) |
| Full object manifest | [manifest.txt](https://storage.googleapis.com/alphaearth_foundations/satellite_embedding/v1/annual/manifest.txt) |

Download an index once. These are global indexes, so check their size first.
`find_aef_tiles` accepts a local CSV/Parquet file or a pandas DataFrame; it does
not silently download the global index. The COG sampler uses byte-range reads
and needs neither a Google account nor Earth Engine initialization.

```bash
pip install -e ".[aef]"
curl -I https://storage.googleapis.com/alphaearth_foundations/satellite_embedding/v1/annual/aef_index.csv
curl -L -o aef_index.csv https://storage.googleapis.com/alphaearth_foundations/satellite_embedding/v1/annual/aef_index.csv
```

```python
from earth_embedding import BBox, find_aef_tiles, sample_aef

tiles = find_aef_tiles(
    "aef_index.csv",
    spatial=BBox(114.40, 30.51, 114.42, 30.53),
    year=2021,
)
result = sample_aef([[114.41, 30.52]], tiles=tiles)
print(result.data.shape)  # (1, 64)
print(result.meta["source_for_point"])
```

Input coordinates are WGS84 **[longitude, latitude]**. Supply candidate tiles
from one year only. The helper transforms points into each COG's native CRS,
selects the first fully valid vector in overlaps, and raises for uncovered or
masked points. Use `strict=False` to retain those rows as NaN. Network errors
remain errors, rather than being mistaken for missing observations.

## Decode before analyzing

GCS COGs store signed int8 values; -128 is nodata. `sample_aef` applies the
official conversion `sign(x) * (x / 127.5) ** 2`, then marks nodata as NaN.
Earth Engine already returns floating-point embeddings: **do not decode those
again**. Use `dequantize_aef` only on raw signed integer arrays. For spatial
aggregation decode first, sum valid vectors, then normalize the sum if a
unit-length descriptor is desired. An average of encoded integers is incorrect.

## Earth Engine

```python
from earth_embedding import PointBuffer, TemporalSpec, get_embedding

result = get_embedding(
    "gse",
    spatial=PointBuffer(lon=114.41, lat=30.52, buffer_m=320),
    temporal=TemporalSpec.year(2021),
    backend="gee",
)
```

This route requires an authorized Earth Engine account/project and uses the
[`GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL`](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL)
collection. Run `earthengine authenticate` once; set `EE_PROJECT` if needed.
See [GSE model details](models/gse.md).

## Attribution

Data license: CC-BY-4.0. Retain the attribution required by Google:

> The AlphaEarth Foundations Satellite Embedding dataset is produced by Google and Google DeepMind.

The library's Apache-2.0 license does not replace the data license.

## Environment troubleshooting

When Rasterio reports incompatible `proj.db` versions, a Conda `PROJ_LIB` or
`PROJ_DATA` setting may point to another GDAL installation. Use the same
environment for Rasterio and PROJ, or unset those inherited variables for the
command. The validation environment used `env -u PROJ_LIB -u PROJ_DATA` on Linux.
