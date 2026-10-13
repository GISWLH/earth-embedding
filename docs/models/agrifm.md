# AgriFM (`agrifm`)

> Multi-frame Sentinel-2 adapter for AgriFM (Video Swin-style backbone), with fixed-frame temporal packaging and provider-backed S2 sequence fetching.

## Quick Facts

| Field                             | Value                                                                 |
| --------------------------------- | --------------------------------------------------------------------- |
| Model ID                          | `agrifm`                                                              |
| Family / Backbone                 | AgriFM (vendored Video Swin runtime + checkpoint loader)              |
| Adapter type                      | `on-the-fly`                                                          |
| Typical backend                   | provider backend (`gee`)                                              |
| Primary input                     | S2 SR 10-band time series (`T,10,H,W`)                                |
| Default resolution                | 10m default provider fetch (`sensor.scale_m`)                         |
| Temporal mode                     | `range` in practice (window split into `T` frames)                    |
| Output modes                      | `pooled`, `grid`                                                      |
| Extra side inputs                 | none required (adapter builds fixed frame stack)                      |
| Training alignment (adapter path) | High when `n_frames`, normalization, and checkpoint version are fixed |

---

## When To Use This Model

AgriFM is a good fit for crop-oriented temporal S2 experiments, comparisons against other multi-frame adapters such as `anysat` and `galileo`, and workflows where a fixed-length frame stack is useful. The main pitfalls are changing `RS_EMBED_AGRIFM_FRAMES` between runs, forgetting that `CHW` inputs are repeated to `T` frames, and comparing it to single-window models without documenting the temporal packaging.

---

## Input Contract (Current Adapter Path)

### Spatial / temporal

AgriFM is provider-backed, so use `backend="gee"` or another provider-compatible backend. `TemporalSpec` is normalized to a range through the shared helper, and `TemporalSpec.range(...)` is the clearest choice. The provider path fetches a multi-frame S2 sequence over that range and composes it into a fixed `T`-frame stack.

### Sensor / channels

If `sensor` is omitted, AgriFM uses `COPERNICUS/S2_SR_HARMONIZED` with bands `B2,B3,B4,B5,B6,B7,B8,B8A,B11,B12`, `scale_m=10`, `cloudy_pct=30`, `composite="median"`, and `fill_value=0.0`.

For `input_chw`, the adapter accepts `CHW` with `C=10` and repeats that frame to `T = RS_EMBED_AGRIFM_FRAMES`, or `TCHW` with `C=10` and pads or truncates to the exact configured frame count. Values are clipped to the raw S2 SR range `0..10000`.

---

## Preprocessing Pipeline (Current rs-embed Path)

<pre class="pipeline-flow"><code><span class="pipeline-root">SETUP</span>  runtime settings
  <span class="pipeline-arrow">-&gt;</span> n_frames + image_size + normalization mode
  <span class="pipeline-arrow">-&gt;</span> checkpoint path (local or auto-download)
<span class="pipeline-root">INPUT</span>  provider fetch / input_chw
  <span class="pipeline-arrow">-&gt;</span> multi-frame raw TCHW
     <span class="pipeline-detail">input_chw path: coerce CHW / TCHW to exact T</span>
  <span class="pipeline-arrow">-&gt;</span> optional inspection on frame 0
  <span class="pipeline-arrow">-&gt;</span> normalize with RS_EMBED_AGRIFM_NORM
     <span class="pipeline-branch">agrifm_stats:</span> z-score with AgriFM S2 statistics
     <span class="pipeline-branch">unit_scale:</span> /10000 -&gt; clip [0,1]
     <span class="pipeline-branch">none / raw:</span> keep clipped raw values
  <span class="pipeline-arrow">-&gt;</span> resize all frames to RS_EMBED_AGRIFM_IMG=224
  <span class="pipeline-arrow">-&gt;</span> load checkpoint + vendored runtime
  <span class="pipeline-arrow">-&gt;</span> forward to embedding grid (D,H,W)
  <span class="pipeline-arrow">-&gt;</span> output projection
     <span class="pipeline-branch">pooled:</span> spatial mean / max over grid
     <span class="pipeline-branch">grid:</span>   xarray.DataArray</code></pre>

---

## Environment Variables / Tuning Knobs

### Temporal / preprocessing

| Env var                         | Default        | Effect                                   |
| ------------------------------- | -------------- | ---------------------------------------- |
| `RS_EMBED_AGRIFM_FRAMES`        | `8`            | Fixed frame count `T`                    |
| `RS_EMBED_AGRIFM_IMG`           | `224`          | Resize target image size                 |
| `RS_EMBED_AGRIFM_NORM`          | `agrifm_stats` | `agrifm_stats`, `unit_scale`, or `none`  |
| `RS_EMBED_AGRIFM_FETCH_WORKERS` | `8`            | Provider prefetch workers for batch APIs |

### Checkpoint loading

| Env var                          | Default                    | Effect                         |
| -------------------------------- | -------------------------- | ------------------------------ |
| `RS_EMBED_AGRIFM_CKPT`           | unset                      | Local checkpoint path          |
| `RS_EMBED_AGRIFM_AUTO_DOWNLOAD`  | `1`                        | Allow checkpoint auto-download |
| `RS_EMBED_AGRIFM_CACHE_DIR`      | `~/.cache/rs_embed/agrifm` | Checkpoint cache dir           |
| `RS_EMBED_AGRIFM_CKPT_FILE`      | `AgriFM.pth`               | Cached checkpoint filename     |
| `RS_EMBED_AGRIFM_CKPT_URL`       | project default URL        | Checkpoint download URL        |
| `RS_EMBED_AGRIFM_CKPT_MIN_BYTES` | large-size threshold       | Download validation threshold  |

## Output Semantics

AgriFM uses the standard feature-grid pattern for multi-frame encoders. `pooled` applies spatial pooling over the model feature grid, and `grid` returns `(D,H,W)` in model feature-map space rather than georeferenced raster pixels. The useful model-specific details are mostly carried in metadata, including frame count and normalization settings.

---

## Examples

### Minimal provider-backed example

```python
from rs_embed import get_embedding, PointBuffer, TemporalSpec, OutputSpec

emb = get_embedding(
    "agrifm",
    spatial=PointBuffer(lon=121.5, lat=31.2, buffer_m=2048),
    temporal=TemporalSpec.range("2022-01-01", "2022-12-31"),
    output=OutputSpec.pooled(),
    backend="gee",
)
```

### Example temporal packaging and normalization tuning

```python
# Example (shell):
# export RS_EMBED_AGRIFM_FRAMES=8
# export RS_EMBED_AGRIFM_IMG=224
# export RS_EMBED_AGRIFM_NORM=agrifm_stats
```

---

## Common Failure Modes / Debugging

- backend mismatch (`agrifm` is provider-only)
- wrong `input_chw` shape (must be `CHW`/`TCHW` with `C=10`)
- silent temporal mismatch from `CHW` repeat-to-`T` behavior
- checkpoint download failure or invalid local checkpoint path
- missing lightweight import deps (`torch`, `timm`, `einops`) for vendored backbone import

Recommended first checks:

Inspect metadata for `n_frames`, `norm_mode`, `input_frames`, and `grid_hw` first. Verify whether the input came from provider fetch or from repeated `CHW`, and pin the checkpoint source or path before benchmarking.

---

## Reproducibility Notes

Keep `RS_EMBED_AGRIFM_FRAMES`, `RS_EMBED_AGRIFM_IMG`, normalization mode, checkpoint source or path, temporal window, compositing settings, and output mode fixed and recorded. Multi-frame models are very sensitive to frame count and frame construction, so changing `FRAMES` is a different experiment rather than a small tuning tweak.

---

## Source of Truth (Code Pointers)

The main code paths are `src/rs_embed/embedders/catalog.py` for registration, `src/rs_embed/embedders/onthefly_agrifm.py` for the adapter, and `src/rs_embed/embedders/runtime_utils.py` for shared temporal fetch and coercion helpers.
