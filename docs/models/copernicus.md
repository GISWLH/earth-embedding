# Copernicus Embed (`copernicus`)

> Precomputed embedding adapter using a vendored local GeoTIFF reader over the published `torchgeo/copernicus_embed` Hugging Face dataset, with strict bbox slicing.

## Quick Facts

| Field                             | Value                                                                          |
| --------------------------------- | ------------------------------------------------------------------------------ |
| Model ID                          | `copernicus`                                                                   |
| Aliases                           | `copernicus_embed`                                                             |
| Family / Source                   | `torchgeo/copernicus_embed` GeoTIFF redistribution on Hugging Face             |
| Adapter type                      | `precomputed`                                                                  |
| Typical backend                   | `auto`                                                                         |
| Primary input                     | `BBox` / `PointBuffer` in EPSG:4326, sliced via vendored GeoTIFF bbox indexing |
| Product grid CRS                  | fixed `EPSG:4326` grid (not the common provider-backed EPSG:3857 default)      |
| Default resolution                | 0.25° source product resolution                                                |
| Temporal mode                     | **strict** `TemporalSpec.year(2021)` in v0.1                                   |
| Output modes                      | `pooled`, `grid`                                                               |
| Extra side inputs                 | none                                                                           |
| Training alignment (adapter path) | N/A (precomputed product)                                                      |

---

## When To Use This Model

Copernicus Embed is a good fit for precomputed embedding workflows via local GeoTIFF access, quick spatial baselines without provider requests, and experiments where coarse precomputed coverage is acceptable. It is easy to misuse if you request years other than `2021`, pass ROIs smaller than one 0.25° pixel, or use non-`auto` backends.

---

## Input Contract (Current Adapter Path)

### Spatial

The adapter accepts `BBox` directly and `PointBuffer`, which it converts to an EPSG:4326 bbox. Internally it slices the local GeoTIFF with bbox indexing via `ds[minlon:maxlon, minlat:maxlat]`.

!!! warning
Copernicus keeps the product's fixed `EPSG:4326` grid with 0.25 degree pixels. That differs from the more common provider-backed EPSG:3857 sampling default used elsewhere in `rs-embed`, even though the public spatial input is still `EPSG:4326`.

### Temporal

Copernicus Embed requires `TemporalSpec.year(...)`, currently supports only `2021`, and validates the year before dataset access.

### Backend / data directory

The backend should be `auto`, although legacy `local` is still accepted for compatibility. Data directory resolution comes from `RS_EMBED_COP_DIR` by default, or from a per-call override such as `sensor.collection="dir:/path/to/copernicus_embed"`.

---

## Retrieval Pipeline (Current rs-embed Path)

<pre class="pipeline-flow"><code><span class="pipeline-root">INPUT</span>  TemporalSpec.year(...) + SpatialSpec
  <span class="pipeline-arrow">-&gt;</span> validate supported year
     <span class="pipeline-detail">current adapter supports 2021</span>
  <span class="pipeline-arrow">-&gt;</span> resolve data_dir
     <span class="pipeline-branch">default:</span> RS_EMBED_COP_DIR
     <span class="pipeline-branch">override:</span> sensor.collection
  <span class="pipeline-arrow">-&gt;</span> load / cache CopernicusEmbedGeoTiff dataset
     <span class="pipeline-detail">download=True in current adapter</span>
  <span class="pipeline-arrow">-&gt;</span> convert SpatialSpec to EPSG:4326 bbox
  <span class="pipeline-arrow">-&gt;</span> validate ROI covers at least one full Copernicus pixel
  <span class="pipeline-arrow">-&gt;</span> bbox slice -&gt; sample["image"] as CHW
  <span class="pipeline-arrow">-&gt;</span> output projection
     <span class="pipeline-branch">pooled:</span> vector
     <span class="pipeline-branch">grid:</span>   embedding grid</code></pre>

Notes:

`temporal` is validated, but metadata in the current adapter is built with `temporal=None`, so record the requested year externally if strict provenance matters.

---

## Environment Variables / Tuning Knobs

| Env var                             | Default                 | Effect                                             |
| ----------------------------------- | ----------------------- | -------------------------------------------------- |
| `RS_EMBED_COP_DIR`                  | `data/copernicus_embed` | Local Copernicus embed GeoTIFF directory           |
| `RS_EMBED_COPERNICUS_BATCH_WORKERS` | `4`                     | Batch worker count for `get_embeddings_batch(...)` |

Non-env override:

`sensor.collection="dir:/path/to/copernicus_embed"` overrides the data directory per call.

Current fixed adapter behavior (not env-configurable in v0.1):

The current adapter keeps `download=True`, and that is not env-configurable in v0.1.

---

## Output Semantics

Copernicus follows the same precomputed-product pattern as the other local or provider-sampled embedding products. `pooled` applies spatial pooling over the sampled `CHW` embedding grid, and `grid` returns `(D,H,W)` in product space rather than raw imagery pixel space.

The current adapter exposes this explicitly in metadata: `input_crs` is `EPSG:4326`, `output_crs` is the fixed product CRS `EPSG:4326`, and `product_resolution_deg` records the 0.25 degree grid spacing.

---

## Examples

### Minimal example

```python
from rs_embed import get_embedding, PointBuffer, TemporalSpec, OutputSpec

emb = get_embedding(
    "copernicus",
    spatial=PointBuffer(lon=121.5, lat=31.2, buffer_m=5000),
    temporal=TemporalSpec.year(2021),
    output=OutputSpec.pooled(),
    backend="auto",
)
```

### Local dataset directory override

```python
# Example (shell):
# export RS_EMBED_COP_DIR=/data/copernicus_embed
```

---

## Common Failure Modes / Debugging

- year not supported (`2021` only in current adapter)
- backend is not `auto`
- broken local install missing the GeoTIFF stack (`tifffile` / `imagecodecs`)
- dataset files missing/corrupt under `RS_EMBED_COP_DIR`
- ROI is smaller than one Copernicus pixel (raises immediately)

Recommended first checks:

Confirm `TemporalSpec.year(2021)` first, then inspect metadata such as `data_dir`, `chw_shape`, and `bbox_4326`. If coverage seems empty, test a larger ROI before assuming the dataset is broken.

---

## Reproducibility Notes

Keep the dataset path or version snapshot, requested year, ROI geometry, and output mode fixed and recorded.

---

## Source of Truth (Code Pointers)

The main code paths are `src/rs_embed/embedders/catalog.py` for registration, `src/rs_embed/embedders/precomputed_copernicus_embed.py` for the adapter, and `src/rs_embed/embedders/_vendor/copernicus_embed.py` for the vendored GeoTIFF reader.
