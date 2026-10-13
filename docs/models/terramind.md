# TerraMind (`terramind`)

> TerraTorch-backed TerraMind adapter for Sentinel-2 SR 12-band inputs, supporting provider and tensor backends with TerraMind-specific z-score normalization.

## Quick Facts

| Field                             | Value                                                          |
| --------------------------------- | -------------------------------------------------------------- |
| Model ID                          | `terramind`                                                    |
| Family / Backbone                 | TerraMind via TerraTorch `BACKBONE_REGISTRY`                   |
| Adapter type                      | `on-the-fly`                                                   |
| Typical backend                   | provider backend (`gee`), also supports `backend="tensor"`     |
| Primary input                     | S2 SR 12-band (`B1..B12` subset used by adapter order)         |
| Default resolution                | 10m default provider fetch (`sensor.scale_m`)                  |
| Temporal mode                     | `range` (provider path normalized via shared helper)           |
| Output modes                      | `pooled`, `grid`                                               |
| Extra side inputs                 | none required in current adapter                               |
| Training alignment (adapter path) | High when default TerraMind z-score normalization is preserved |

---

## When To Use This Model

TerraMind is a good fit for strict multispectral Sentinel-2 experiments with TerraMind checkpoints, for comparisons that need a strong 12-band S2 encoder, and for workflows that want both provider-backed and direct tensor input paths.

Treat normalization mode as part of the model definition. Moving away from TerraMind's default `zscore` path changes the semantics of the input, and `grid` should still be read as a patch-token grid rather than georeferenced raster space. The tensor backend is useful, but only if the supplied channel order and preprocessing assumptions match the adapter contract.

---

## Input Contract (Current Adapter Path)

### Spatial / temporal

On the provider path, `SpatialSpec` is paired with temporal input normalized to a range via the shared helper. On the tensor path, there is no provider fetch, and the adapter reads `input_chw` directly as `CHW`.

### Sensor / channels (provider path)

Default `SensorSpec` if omitted:

The default sensor is `COPERNICUS/S2_SR_HARMONIZED` with adapter fetch order `_S2_SR_12_BANDS = B1,B2,B3,B4,B5,B6,B7,B8,B8A,B9,B11,B12`, `scale_m=10`, `cloudy_pct=30`, `composite="median"`, and `fill_value=0.0`.

TerraMind internal semantic mapping is also tracked in metadata (`bands_terramind`).

`input_chw` contract (provider override path):

For provider overrides, `input_chw` must be `CHW` with 12 bands in the adapter fetch order, and raw SR values are expected in `0..10000`.

### Tensor backend contract

`backend="tensor"` requires `input_chw` in `CHW` format, with `C=12`. Batch tensor inputs should go through `get_embeddings_batch_from_inputs(...)`. Before the forward pass, the adapter resizes to `224` and applies the same TerraMind normalization used on the provider path.

---

## Preprocessing Pipeline (Current rs-embed Path)

### Provider path

<pre class="pipeline-flow"><code><span class="pipeline-root">PROVIDER</span>  fetch raw 12-band S2 SR patch
  <span class="pipeline-arrow">-&gt;</span> composite over temporal window
  <span class="pipeline-arrow">-&gt;</span> optional raw-value inspection
     <span class="pipeline-detail">value_range=(0,10000)</span>
  <span class="pipeline-arrow">-&gt;</span> resize to fixed 224x224
  <span class="pipeline-arrow">-&gt;</span> TerraMind normalization
     <span class="pipeline-branch">zscore:</span> TerraMind v1 / v01 stats by model key prefix
     <span class="pipeline-branch">raw / none:</span> nan_to_num only
  <span class="pipeline-arrow">-&gt;</span> forward TerraMind backbone
  <span class="pipeline-arrow">-&gt;</span> token tensor
  <span class="pipeline-arrow">-&gt;</span> output projection
     <span class="pipeline-branch">pooled:</span> token pooling
     <span class="pipeline-branch">grid:</span>   patch-token grid</code></pre>

### Tensor path

<pre class="pipeline-flow"><code><span class="pipeline-root">TENSOR</span>  read input_chw
  <span class="pipeline-arrow">-&gt;</span> resize to fixed 224x224
  <span class="pipeline-arrow">-&gt;</span> apply the same TerraMind normalization
     <span class="pipeline-branch">zscore:</span> TerraMind v1 / v01 stats by model key prefix
     <span class="pipeline-branch">raw / none:</span> nan_to_num only
  <span class="pipeline-arrow">-&gt;</span> forward TerraMind backbone
  <span class="pipeline-arrow">-&gt;</span> output projection
     <span class="pipeline-branch">pooled:</span> token pooling
     <span class="pipeline-branch">grid:</span>   patch-token grid</code></pre>

---

## Environment Variables / Tuning Knobs

| Env var                            | Default              | Effect                                                               |
| ---------------------------------- | -------------------- | -------------------------------------------------------------------- |
| `RS_EMBED_TERRAMIND_MODEL_KEY`     | `terramind_v1_small` | TerraMind backbone key                                               |
| `RS_EMBED_TERRAMIND_MODALITY`      | `S2L2A`              | Modality passed to TerraMind/TerraTorch                              |
| `RS_EMBED_TERRAMIND_NORMALIZE`     | `zscore`             | Input normalization mode (`zscore` vs raw/none)                      |
| `RS_EMBED_TERRAMIND_LAYER_INDEX`   | `-1`                 | Which layer output to select when sequence-like outputs are returned |
| `RS_EMBED_TERRAMIND_PRETRAINED`    | `1`                  | Use pretrained weights                                               |
| `RS_EMBED_TERRAMIND_FETCH_WORKERS` | `8`                  | Provider prefetch workers for batch APIs                             |

Fixed adapter behavior:

In the current implementation, image size is fixed to `224`.

---

## Output Semantics

TerraMind behaves like a standard token model at output time: `pooled` applies token pooling according to `OutputSpec.pooling`, and `grid` returns a ViT-style token grid `(D,H,W)` in model space rather than georeferenced raster pixels. Metadata still records the key details such as pooling mode, `grid_hw`, and CLS removal.

---

## Examples

### Minimal provider-backed example

```python
from rs_embed import get_embedding, PointBuffer, TemporalSpec, OutputSpec

emb = get_embedding(
    "terramind",
    spatial=PointBuffer(lon=121.5, lat=31.2, buffer_m=2048),
    temporal=TemporalSpec.range("2022-06-01", "2022-09-01"),
    output=OutputSpec.pooled(),
    backend="gee",
)
```

### Example normalization/model tuning (env-controlled)

```python
# Example (shell):
# export RS_EMBED_TERRAMIND_MODEL_KEY=terramind_v1_small
# export RS_EMBED_TERRAMIND_NORMALIZE=zscore
# export RS_EMBED_TERRAMIND_MODALITY=S2L2A
```

---

## Common Failure Modes / Debugging

- wrong channel count for `input_chw` / tensor backend (`C` must be 12)
- backend mismatch (`tensor` path requires `input_chw`; provider path requires provider backend)
- hidden normalization changes via `RS_EMBED_TERRAMIND_NORMALIZE`
- TerraTorch import/build issues for selected model key or optional deps

Recommended first checks:

Verify provider raw input channel order and value range before normalization, then inspect metadata for the model key, modality, normalization mode, and selected layer index.

---

## Reproducibility Notes

For reproducibility, keep the model key fixed, because `v1` versus `v01` changes which z-score statistics are used. It is also worth keeping normalization mode, modality, output mode, pooling choice, and provider-side temporal and compositing settings fixed across runs.

---

## Source of Truth (Code Pointers)

The implementation details are in `src/rs_embed/embedders/catalog.py`, `src/rs_embed/embedders/onthefly_terramind.py`, and `src/rs_embed/embedders/_vit_mae_utils.py`.
