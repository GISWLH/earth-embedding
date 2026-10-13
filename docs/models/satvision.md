# SatVision-TOA (`satvision`)

> Provider-backed SatVision-TOA adapter for 14-channel TOA inputs (default MODIS band order), with channel-aware reflectance/emissive normalization and token/grid outputs.

## Quick Facts

| Field                             | Value                                                                    |
| --------------------------------- | ------------------------------------------------------------------------ |
| Model ID                          | `satvision`                                                              |
| Aliases                           | `satvision_toa`                                                          |
| Family / Backbone                 | SatVision-TOA checkpoint (HF/local checkpoint loader)                    |
| Adapter type                      | `on-the-fly`                                                             |
| Typical backend                   | provider backend (`gee`)                                                 |
| Primary input                     | 14-channel TOA `CHW` (default MODIS/061/MOD021KM band order)             |
| Default resolution                | 1000m default provider fetch (`sensor.scale_m`)                          |
| Temporal mode                     | `range` in practice (normalized via shared helper)                       |
| Output modes                      | `pooled`, `grid`                                                         |
| Extra side inputs                 | none (but channel calibration settings matter)                           |
| Training alignment (adapter path) | High only when channel order + calibration match checkpoint expectations |

---

## When To Use This Model

SatVision is a better fit for TOA-based experiments where you want SatVision checkpoints rather than Sentinel-2 SR-specific encoders, for MODIS-style provider workflows with explicit normalization and calibration control, and for cases where you want to compare pooled versus patch-token outputs from the same model path.

Be careful when changing `SensorSpec.bands` order without updating the matching `RS_EMBED_SATVISION_TOA_*` channel settings. The page also assumes you will log whether the effective normalization path was raw, auto, or unit-scaled, because mixing those modes makes results hard to compare. Arbitrary 14-channel tensors are not enough on their own if they do not match the checkpoint's training semantics.

---

## Input Contract (Current Adapter Path)

### Spatial / temporal

`SpatialSpec` may be either `BBox` or `PointBuffer`. `TemporalSpec` is normalized to a range through the shared helper, and `TemporalSpec.range(...)` is the recommended path for reproducible requests. The current adapter path is provider-only, so use `backend="gee"` or another provider-compatible backend.

### Sensor / channels

Default `SensorSpec` if omitted:

The default sensor is `MODIS/061/MOD021KM` with the strict band order `1,2,3,26,6,20,7,27,28,29,31,32,33,34`, `scale_m=1000`, `cloudy_pct=100`, `composite="mosaic"`, and `fill_value=0.0`.

`input_chw` contract:

`input_chw` must be `CHW`, and `C` must match `RS_EMBED_SATVISION_TOA_IN_CHANS`, which defaults to `14`. The adapter also checks that `len(sensor.bands) == in_chans`. Values may be raw TOA-like inputs or already unit-scaled data, depending on the active normalization mode.

Important:

The adapter does not infer semantic channel order from the values themselves, so `sensor.bands` must match the checkpoint's expected order exactly.

---

## Preprocessing Pipeline (Current rs-embed Path)

<pre class="pipeline-flow"><code><span class="pipeline-root">SETUP</span>  runtime settings
  <span class="pipeline-arrow">-&gt;</span> checkpoint / model ID
  <span class="pipeline-arrow">-&gt;</span> in_chans + normalization + calibration arrays
<span class="pipeline-root">INPUT</span>  provider fetch / input_chw
  <span class="pipeline-arrow">-&gt;</span> CHW patch
  <span class="pipeline-arrow">-&gt;</span> provider unit-scale override
     <span class="pipeline-detail">if metadata says unit-scaled, effective norm mode becomes unit</span>
  <span class="pipeline-arrow">-&gt;</span> normalize with RS_EMBED_SATVISION_TOA_NORM
     <span class="pipeline-branch">auto:</span> use [0,1] if values look unit-scaled, else raw scaling
     <span class="pipeline-branch">raw:</span>  channel-wise scaling
     <span class="pipeline-detail">reflectance: divide by RS_EMBED_SATVISION_TOA_REF_DIV=100</span>
     <span class="pipeline-detail">emissive: min-max with RS_EMBED_SATVISION_TOA_EMISSIVE_MINS/MAXS</span>
     <span class="pipeline-branch">unit:</span> clip to [0,1]
  <span class="pipeline-arrow">-&gt;</span> resize to RS_EMBED_SATVISION_TOA_IMG=128
  <span class="pipeline-arrow">-&gt;</span> forward model + decode output tensor
  <span class="pipeline-arrow">-&gt;</span> output projection
     <span class="pipeline-branch">pooled:</span> token pooling or model-pooled vector
     <span class="pipeline-branch">grid:</span>   token reshape when output is [N,D]</code></pre>

---

## Environment Variables / Tuning Knobs

### Model / weights

| Env var                                | Default                   | Effect                                          |
| -------------------------------------- | ------------------------- | ----------------------------------------------- |
| `RS_EMBED_SATVISION_TOA_ID`            | SatVision TOA HF model ID | HF model identifier                             |
| `RS_EMBED_SATVISION_TOA_CKPT`          | unset                     | Local checkpoint path override                  |
| `RS_EMBED_SATVISION_TOA_AUTO_DOWNLOAD` | `1`                       | Allow HF download when local checkpoint not set |
| `RS_EMBED_SATVISION_TOA_IMG`           | `128`                     | Resize target image size                        |
| `RS_EMBED_SATVISION_TOA_IN_CHANS`      | `14`                      | Expected channel count                          |
| `RS_EMBED_SATVISION_TOA_BATCH_SIZE`    | CPU:`2`, CUDA:`8`         | Inference batch size (batch APIs)               |
| `RS_EMBED_SATVISION_TOA_FETCH_WORKERS` | `8`                       | Provider prefetch workers (batch APIs)          |

### Normalization / calibration

| Env var                                   | Default          | Effect                          |
| ----------------------------------------- | ---------------- | ------------------------------- |
| `RS_EMBED_SATVISION_TOA_NORM`             | `auto`           | `auto`, `raw`, or `unit`        |
| `RS_EMBED_SATVISION_TOA_REFLECTANCE_IDXS` | adapter defaults | Reflectance channel indices     |
| `RS_EMBED_SATVISION_TOA_EMISSIVE_IDXS`    | adapter defaults | Emissive channel indices        |
| `RS_EMBED_SATVISION_TOA_REF_DIV`          | `100`            | Reflectance divisor             |
| `RS_EMBED_SATVISION_TOA_EMISSIVE_MINS`    | adapter defaults | Emissive min calibration values |
| `RS_EMBED_SATVISION_TOA_EMISSIVE_MAXS`    | adapter defaults | Emissive max calibration values |

### Default sensor overrides (if `sensor` omitted)

| Env var                             | Default                     | Effect                      |
| ----------------------------------- | --------------------------- | --------------------------- |
| `RS_EMBED_SATVISION_TOA_COLLECTION` | `MODIS/061/MOD021KM`        | Default provider collection |
| `RS_EMBED_SATVISION_TOA_BANDS`      | default 14-band MODIS order | Override default band list  |
| `RS_EMBED_SATVISION_TOA_SCALE_M`    | `1000`                      | Default fetch scale         |
| `RS_EMBED_SATVISION_TOA_CLOUDY_PCT` | `100`                       | Default cloud filter        |
| `RS_EMBED_SATVISION_TOA_FILL`       | `0`                         | Default fill value          |
| `RS_EMBED_SATVISION_TOA_COMPOSITE`  | `mosaic`                    | Default composite method    |

---

## Output Semantics

### `OutputSpec.pooled()`

If the model output is a token sequence `[N,D]`, `OutputSpec.pooled()` pools patch tokens with `mean` or `max`. If the model already returns a vector `(D,)`, the adapter returns it directly as `model_pooled`. Metadata records the pooling behavior together with whether a CLS token was removed.

### `OutputSpec.grid()`

`OutputSpec.grid()` requires token-sequence output `[N,D]` and reshapes patch tokens into an `xarray.DataArray` with shape `(D,H,W)`. The result is model patch-token layout rather than georeferenced raster pixels.

---

## Examples

### Minimal provider-backed example

```python
from rs_embed import get_embedding, PointBuffer, TemporalSpec, OutputSpec

emb = get_embedding(
    "satvision",
    spatial=PointBuffer(lon=121.5, lat=31.2, buffer_m=5000),
    temporal=TemporalSpec.range("2022-07-01", "2022-07-31"),
    output=OutputSpec.pooled(),
    backend="gee",
)
```

### Example normalization tuning (env-controlled)

```python
# Example (shell):
# export RS_EMBED_SATVISION_TOA_NORM=raw
# export RS_EMBED_SATVISION_TOA_IMG=128
# export RS_EMBED_SATVISION_TOA_REF_DIV=100
# export RS_EMBED_SATVISION_TOA_IN_CHANS=14
```

---

## Common Failure Modes / Debugging

- backend is not provider-compatible (`satvision` is provider-only)
- `sensor.bands` count does not match `RS_EMBED_SATVISION_TOA_IN_CHANS`
- calibration list lengths mismatch (`EMISSIVE_IDXS` vs `EMISSIVE_MINS/MAXS`)
- wrong channel order for the chosen checkpoint (results look unstable even if shapes pass)
- grid requested but model output is not a token sequence
- HF download/auth issues when using gated/private checkpoints

Recommended first checks:

Start by inspecting metadata for `norm_mode` and `norm_mode_effective`, then log the effective `sensor.collection`, `sensor.bands`, and calibration environment values. As with other token models, `OutputSpec.pooled()` is the simpler first check before debugging `grid`.

---

## Reproducibility Notes

For reproducibility, keep the checkpoint source fixed, whether that is `RS_EMBED_SATVISION_TOA_ID` or a local checkpoint path, and record the exact band order, `in_chans`, normalization mode, calibration arrays, divisor, temporal window, compositing settings, output mode, and pooling choice.

---

## Source of Truth (Code Pointers)

The implementation lives in `src/rs_embed/embedders/catalog.py`, `src/rs_embed/embedders/onthefly_satvision_toa.py`, and the shared token-grid helpers in `src/rs_embed/embedders/_vit_mae_utils.py`.
