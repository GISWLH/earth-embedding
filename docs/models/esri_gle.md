# Esri Global Location Encoder (Sentinel-2)

`esri_gle` turns WGS84 longitude/latitude coordinates into 256-dimensional
embeddings using Esri's official pretrained weights. The adapter runs the location
encoder directly in PyTorch with the bundled MIT-licensed SatCLIP architecture.
ArcGIS, ArcPy, fastai, imagery downloads and Earth Engine initialization are not
required.

The model is lightweight: the official download is **3,741,098 bytes (about
3.7 MB)**, containing a **2,168,415-byte** `satclip.pth` checkpoint. Esri's weights
are distinct from Microsoft's SatCLIP checkpoints; this adapter uses the Esri
checkpoint.

## Query

The base installation provides the required runtime. On first use, the adapter
downloads the official model package and caches its extracted checkpoint locally.

```python
from earth_embedding import get_location_embeddings

embedding = get_location_embeddings(
    "esri_gle",  # aliases: "esri", "global_location_encoder"
    [[114.4, 30.5], [-117.1956, 34.0564]],  # longitude, latitude
    device="cpu",
    batch_size=1024,
)
print(embedding.data.shape)  # (2, 256)
print(embedding.meta)
```

Input rows are preserved. The result is a finite float32 array with shape
`(N, 256)`. `batch_size` bounds the number of coordinates in each forward pass.

## Downloads, caching and offline use

The default download is the model package published through Esri's
[Global Location Encoder catalog item](https://www.arcgis.com/home/item.html?id=b0664ef297c04d4aaa44191cf21e07f3).
The adapter verifies the extracted checkpoint against its pinned SHA-256 digest.
It reads the checkpoint with PyTorch's `weights_only=True` loader and
checks the parameter structure before inference. No Esri weights are bundled in
this repository, and the package's bundled Python files are never executed.
The outer package digest below records the checked download for reference.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Official catalog `.dlpk` | 3,741,098 | `8bb10ad29bf9e538c7724f118dfa12ceb052b61a603ef3ca8a8819c7f1ef42fe` |
| `satclip.pth` | 2,168,415 | `2d5b8ac88b4a7f210a00f7fbe145f5216987f373062ec71f3065f9ba13b15452` |

The default checkpoint cache is `~/.cache/earth_embedding/esri_gle/satclip.pth`.
Set `cache_dir` to choose its directory. Once populated, the same cache supports
an explicitly offline call:

```python
locations = [[114.4, 30.5], [139.76, 35.68]]

# Download the official package and cache its verified weights if needed.
get_location_embeddings(
    "esri_gle", locations, device="cpu", cache_dir="./model-cache/esri"
)

# Reuse only local files; fail clearly if the required weights are absent.
offline = get_location_embeddings(
    "esri_gle",
    locations,
    device="cpu",
    cache_dir="./model-cache/esri",
    local_files_only=True,
)
```

An existing official `.dlpk` or its extracted `satclip.pth` can be supplied
directly. The checkpoint must match the pinned Esri weights:

```python
offline = get_location_embeddings(
    "esri_gle",
    locations,
    checkpoint="/path/to/satclip.pth",  # or the official .dlpk
    device="cpu",
    local_files_only=True,
)
```

`RS_EMBED_ESRI_GLE_CKPT` also accepts a local checkpoint path; the explicit
`checkpoint` argument takes precedence. Both official catalog and ArcGIS-runtime
packages contain the same verified `satclip.pth` and are accepted.

Downloads and use remain subject to Esri's model terms. A checksum establishes
artifact identity, not a different license.

## Runtime and spatial queries

The location branch uses `L=40` spherical-harmonic features and a SIREN
network. Inference uses float64 internally to follow the reference model's
numerical path, then returns float32 features. Metadata records the backend,
device, checkpoint provenance and coordinate order.
The network has **541,440 parameters**. CPU inference is supported; an explicit
MPS request is rejected because MPS does not support float64. `device="auto"`
selects CUDA when available and CPU otherwise.

On 2026-10-13, seven real coordinate queries produced finite `(7, 256)` vectors
on CPU with ArcGIS and ArcPy imports disabled. Outputs matched the official
package's mathematical implementation exactly after float32 conversion.
The [execution receipt](../validation/esri-gle-20261013.json) also records first
download, offline cache/package use, batch consistency, pooled and grid checks.

`get_embedding("esri_gle", spatial=..., device="cpu")` supports the same centre
query interface as the other location encoders. `OutputSpec.grid()` samples
coordinates on a north-up grid, with `grid_step_m=1000` and
`max_grid_points=100000` defaults. These are sampling controls, not an assertion of
model resolution. Requested dates are ignored.

See the [validation report](../validation.md) for dated execution evidence and
the tested environments.

## Scope and limitations

The official model is intended primarily for land locations and summarizes
conditions captured by its training imagery. A coordinate query does not provide
time-specific observations, arbitrary current imagery or guaranteed
generalization over open ocean. This additional integration is not part of the
paper's frozen 20-system benchmark.

## Official references

- [Model details and download workflow](https://doc.arcgis.com/en/pretrained-models/latest/vector/introduction-to-global-location-encoder-sentinel-2-.htm)
- [Official model catalog and download](https://www.arcgis.com/home/item.html?id=b0664ef297c04d4aaa44191cf21e07f3)
- [Use the model in ArcGIS Pro](https://doc.arcgis.com/en/pretrained-models/latest/vector/using-global-location-encoder-sentinel-2-.htm)
- [ArcGIS Embeddings Python API](https://developers.arcgis.com/python/latest/api-reference/arcgis.learn.toc.html#embeddings)
- [Esri explanation and model limitations](https://www.esri.com/arcgis-blog/products/arcgis-pro/geoai/beyond-latitude-and-longitude-giving-geographic-context-to-coordinates)
