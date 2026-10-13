# Google Satellite Embedding Annual (`gse`)

> Provider-backed precomputed annual embedding adapter for `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL`, supporting pooled vectors or provider-sampled embedding grids.

## Quick Facts

| Field                             | Value                                                                              |
| --------------------------------- | ---------------------------------------------------------------------------------- |
| Model ID                          | `gse`                                                                              |
| Aliases                           | `gse_annual`                                                                       |
| Family / Source                   | Google Satellite Embedding annual product (`GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL`) |
| Adapter type                      | `precomputed`                                                                      |
| Typical backend                   | provider-backed; prefer `backend="auto"` in public API                             |
| Primary input                     | Provider-sampled annual embedding image collection                                 |
| Default resolution                | 10m default provider sampling (`fetch.scale_m` / `sensor.scale_m`)                 |
| Temporal mode                     | **strict** `TemporalSpec.year(...)`                                                |
| Output modes                      | `pooled`, `grid`                                                                   |
| Extra side inputs                 | none                                                                               |
| Training alignment (adapter path) | N/A (precomputed product)                                                          |

---

## When To Use This Model

GSE is a good fit for quick annual baselines, low-friction comparisons with `OutputSpec.pooled()`, and workflows that prefer provider-based sampling over local tile cache management. The main caveats are that `TemporalSpec.range(...)` is not supported in v0.1, the product is an embedding image rather than native imagery, and `fetch.scale_m` still affects provider sampling resolution.

---

## Input Contract (Current Adapter Path)

### Backend / temporal

This is a provider-backed path, and the public API should usually use `backend="auto"`. It requires `TemporalSpec.year(year=...)`, and the adapter validates `temporal.mode == "year"`.

### Spatial / sampling

The adapter accepts the normal `SpatialSpec` provider sampling path, fetches all embedding bands from the annual collection through the provider helper, and uses `fetch.scale_m` or `sensor.scale_m` as the provider sampling scale.

Fixed provider fetch settings in current adapter:

The provider fetch settings are fixed to collection `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL`, `fill_value=-9999.0`, and `composite="mosaic"`.

---

## Retrieval Pipeline (Current rs-embed Path)

<pre class="pipeline-flow"><code><span class="pipeline-root">INPUT</span>  provider-compatible backend + TemporalSpec.year(...)
  <span class="pipeline-arrow">-&gt;</span> fetch annual embedding product as CHW
  <span class="pipeline-arrow">-&gt;</span> replace fill value -9999 with NaN
  <span class="pipeline-arrow">-&gt;</span> build metadata
     <span class="pipeline-detail">year + scale + band names</span>
  <span class="pipeline-arrow">-&gt;</span> output projection
     <span class="pipeline-branch">pooled:</span> pool_chw_to_vec(...)
     <span class="pipeline-branch">grid:</span>   xarray.DataArray (D,H,W) with d coords = band names</code></pre>

---

## Environment Variables / Tuning Knobs

| Env var                      | Default | Effect                                             |
| ---------------------------- | ------- | -------------------------------------------------- |
| `RS_EMBED_GSE_BATCH_WORKERS` | `4`     | Batch worker count for `get_embeddings_batch(...)` |

Primary non-env sampling knob:

The main non-env sampling knob is `fetch.scale_m`, or the more explicit `sensor.scale_m`.

---

## Output Semantics

GSE also follows the standard precomputed-product pattern. `pooled` applies spatial pooling over the sampled embedding grid, and `grid` returns `(D,H,W)` in embedding-product space rather than raw imagery space. The main GSE-specific detail is that the `d` coordinate uses product band names.

---

## Examples

### Minimal annual example

```python
from rs_embed import get_embedding, PointBuffer, TemporalSpec, OutputSpec

emb = get_embedding(
    "gse",
    spatial=PointBuffer(lon=121.5, lat=31.2, buffer_m=2048),
    temporal=TemporalSpec.year(2021),
    output=OutputSpec.pooled(),
    backend="auto",
)
```

### Sampling resolution example

```python
from rs_embed import FetchSpec

fetch = FetchSpec(scale_m=30)
```

---

## Common Failure Modes / Debugging

- backend is not provider-compatible
- missing `TemporalSpec.year(...)`
- `TemporalSpec.range(...)` used instead of `year`
- provider sampling issues / permissions (GEE auth or provider config)
- unexpected NaNs due to fill regions (`-9999` -> `NaN`)

Recommended first checks:

Inspect metadata such as `year`, `scale_m`, and `bands` first. If access itself is in doubt, try `OutputSpec.pooled()` before debugging the grid path. If the result looks too coarse or too fine, adjust `fetch.scale_m`.

---

## Reproducibility Notes

Keep the requested year, provider auth context, `fetch.scale_m`, and output mode fixed and recorded.

---

## Source of Truth (Code Pointers)

The main code paths are `src/rs_embed/embedders/catalog.py` for registration and `src/rs_embed/embedders/precomputed_gse_annual.py` for the adapter implementation.
