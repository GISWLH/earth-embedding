# Prithvi-EO v2 (`prithvi`)

> Vendored Prithvi runtime for Sentinel-2 6-band inputs, with required temporal/location coordinate side inputs derived by rs-embed and `variant` keyword support for TL checkpoints.

## Quick Facts

| Field                             | Value                                                               |
| --------------------------------- | ------------------------------------------------------------------- |
| Model ID                          | `prithvi`                                                           |
| Aliases                           | `prithvi_eo_v2_s2_6b`                                               |
| Family / Backbone                 | Prithvi-EO v2 via vendored `PrithviMAE` runtime                     |
| Adapter type                      | `on-the-fly`                                                        |
| Typical backend                   | provider backend (`gee` via public API)                             |
| Primary input                     | S2 6-band (`BLUE,GREEN,RED,NIR_NARROW,SWIR_1,SWIR_2`)               |
| Default resolution                | 30m default provider fetch (`sensor.scale_m`)                       |
| Temporal mode                     | `range` preferred; adapter normalizes `year`/`None` to a range      |
| Output modes                      | `pooled`, `grid`                                                    |
| Model config keys                 | `variant` (default: `prithvi_eo_v2_100_tl`)                         |
| Extra side inputs                 | **required** temporal coords + location coords (derived by adapter) |
| Training alignment (adapter path) | Medium (depends on preprocessing mode and resize/pad choices)       |

---

## When To Use This Model

Prithvi is a good fit for multispectral Sentinel-2 experiments that need more than RGB, token or grid-level feature inspection with a ViT-style backbone, or comparisons where explicit time and location conditioning are part of the model path.

Use carefully when comparing Prithvi against models without side inputs, because the derived time and location signals can affect behavior. It is also worth treating preprocessing mode (`resize` vs `pad`) as part of the experiment definition.

---

## Input Contract (Current Adapter Path)

### Spatial / temporal

`SpatialSpec` may be either `BBox` or `PointBuffer`. `TemporalSpec.range(...)` is used directly, while `TemporalSpec.year(...)` is normalized to the half-open interval `[YYYY-01-01, (YYYY+1)-01-01)`. When temporal input is omitted, the adapter falls back to a shared default-range helper, which is usually a poor choice for reproducible experiments.

The adapter also derives the required side inputs for the vendored runtime: temporal coordinates are encoded as `(year, day_of_year)` from the midpoint date of the effective window, and location coordinates are encoded as `(lat, lon)` from the ROI center.

### Sensor / channels

Default `SensorSpec` if omitted:

The default sensor is `COPERNICUS/S2_SR_HARMONIZED` with bands `("BLUE", "GREEN", "RED", "NIR_NARROW", "SWIR_1", "SWIR_2")`, `scale_m=30`, `cloudy_pct=30`, `composite="median"`, and `fill_value=0.0`.

`input_chw` contract:

`input_chw` must be `CHW` with exactly 6 bands. The adapter expects raw Sentinel-2 SR values in `0..10000`, normalizes them to `[0,1]`, clips out-of-range values, and replaces non-finite entries.

---

## Preprocessing Pipeline (Current rs-embed Path)

<pre class="pipeline-flow"><code><span class="pipeline-root">INPUT</span>  provider fetch / input_chw
  <span class="pipeline-arrow">-&gt;</span> 6-band S2 patch
  <span class="pipeline-arrow">-&gt;</span> normalize raw SR to [0,1]
     <span class="pipeline-detail">/10000 -&gt; clip -&gt; nan_to_num</span>
  <span class="pipeline-arrow">-&gt;</span> optional checks + quicklook RGB
  <span class="pipeline-arrow">-&gt;</span> _prepare_prithvi_chw
     <span class="pipeline-branch">resize:</span> RS_EMBED_PRITHVI_IMG=224
     <span class="pipeline-branch">pad:</span>    H/W -&gt; multiple of RS_EMBED_PRITHVI_PATCH_MULT=16
  <span class="pipeline-arrow">-&gt;</span> derive side inputs
     <span class="pipeline-detail">temporal coords from window midpoint</span>
     <span class="pipeline-detail">location coords from ROI center</span>
  <span class="pipeline-arrow">-&gt;</span> encoder forward pass
  <span class="pipeline-arrow">-&gt;</span> output projection
     <span class="pipeline-branch">pooled:</span> vector
     <span class="pipeline-branch">grid:</span>   patch-token grid</code></pre>

---

## Environment Variables / Tuning Knobs

| Env var                          | Default                | Effect                                                          |
| -------------------------------- | ---------------------- | --------------------------------------------------------------- |
| `RS_EMBED_PRITHVI_KEY`           | `prithvi_eo_v2_100_tl` | Prithvi variant selector                                        |
| `RS_EMBED_PRITHVI_PRETRAINED`    | `1`                    | Use pretrained weights vs random init                           |
| `RS_EMBED_PRITHVI_CACHE_DIR`     | unset                  | Optional Hugging Face cache dir for config/checkpoint downloads |
| `RS_EMBED_PRITHVI_WEIGHTS_ONLY`  | `1`                    | `torch.load(..., weights_only=...)` compatibility toggle        |
| `RS_EMBED_PRITHVI_PREP`          | `resize`               | Input prep mode: `resize` or `pad`                              |
| `RS_EMBED_PRITHVI_IMG`           | `224`                  | Target square size for `resize` mode                            |
| `RS_EMBED_PRITHVI_PATCH_MULT`    | `16`                   | Pad multiple for `pad` mode                                     |
| `RS_EMBED_PRITHVI_FETCH_WORKERS` | `8`                    | Provider prefetch workers for batch APIs                        |
| `RS_EMBED_PRITHVI_BATCH_SIZE`    | CPU:`4`, CUDA:`16`     | Inference batch size for batch APIs                             |

---

## Model-specific Settings

| Key       | Type     | Default                | Choices                                                                |
| --------- | -------- | ---------------------- | ---------------------------------------------------------------------- |
| `variant` | `string` | `prithvi_eo_v2_100_tl` | `prithvi_eo_v2_100_tl`, `prithvi_eo_v2_300_tl`, `prithvi_eo_v2_600_tl` |

Notes:

`variant` overrides `RS_EMBED_PRITHVI_KEY`, and the short aliases `100_tl`, `300_tl`, and `600_tl` are also accepted in code.

---

## Output Semantics

Prithvi follows the standard pooled and patch-token grid behavior once the required temporal and location side inputs have been prepared. `pooled` applies token pooling with optional CLS removal, and `grid` returns `(D,H,W)` in model token space rather than georeferenced raster pixels.

---

## Examples

### Minimal example (explicit temporal window)

```python
from rs_embed import get_embedding, PointBuffer, TemporalSpec, OutputSpec

emb = get_embedding(
    "prithvi",
    spatial=PointBuffer(lon=121.5, lat=31.2, buffer_m=2048),
    temporal=TemporalSpec.range("2022-06-01", "2022-09-01"),
    output=OutputSpec.pooled(),
    backend="gee",
)
```

### With custom preprocessing mode (env-controlled)

```python
# Example (shell):
# export RS_EMBED_PRITHVI_PREP=pad
# export RS_EMBED_PRITHVI_PATCH_MULT=16
# export RS_EMBED_PRITHVI_PRETRAINED=1
```

### With variant selection

```python
from rs_embed import get_embedding, PointBuffer, TemporalSpec, OutputSpec

emb = get_embedding(
    "prithvi",
    spatial=PointBuffer(lon=121.5, lat=31.2, buffer_m=2048),
    temporal=TemporalSpec.range("2022-06-01", "2022-09-01"),
    output=OutputSpec.pooled(),
    backend="gee",
    variant="prithvi_eo_v2_300_tl",
)
```

---

## Common Failure Modes / Debugging

- non-provider backend passed to adapter path
- wrong `input_chw` channel count (must be 6)
- missing torch / huggingface_hub dependencies
- inconsistent comparisons due to hidden changes in `RS_EMBED_PRITHVI_PREP` / `RS_EMBED_PRITHVI_IMG`
- confusion about `year` input semantics (adapter converts to full-year range)

Recommended first check:

Inspect the raw fetched patch first and confirm the 6-band order plus value range before debugging embedding quality.

---

## Reproducibility Notes

For reproducible runs, keep the temporal specification fixed, preferably with explicit `TemporalSpec.range(...)`, and record `sensor.scale_m`, which defaults to `30` here rather than the more common Sentinel-2 value of `10`. You should also keep the preprocessing mode (`resize` vs `pad`) and its related environment variables fixed, along with the output mode, pooling method, and selected model key or pretrained flag.

---

## Source of Truth (Code Pointers)

The implementation details live in `src/rs_embed/embedders/catalog.py`, `src/rs_embed/embedders/onthefly_prithvi.py`, and the shared temporal helper `src/rs_embed/embedders/meta_utils.py`.
