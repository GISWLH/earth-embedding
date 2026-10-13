# AnySat (`anysat`)

> Multi-frame Sentinel-2 time-series adapter that builds AnySat inputs (`s2` + `s2_dates`) from a temporal window and returns dense sub-patch grids by default or pooled vectors.

## Quick Facts

| Field                             | Value                                                               |
| --------------------------------- | ------------------------------------------------------------------- |
| Model ID                          | `anysat`                                                            |
| Family / Backbone                 | AnySat (vendored local runtime)                                     |
| Adapter type                      | `on-the-fly`                                                        |
| Typical backend                   | provider-backed; prefer `backend="auto"` in public API              |
| Primary input                     | S2 10-band time series (`T,C,H,W`)                                  |
| Default resolution                | 10m default provider fetch (`sensor.scale_m`)                       |
| Temporal mode                     | `range` in practice (adapter normalizes `year`/`None` to range)     |
| Output modes                      | `pooled`, `grid`                                                    |
| Model config keys                 | `variant` (default: `base`; choices: `base`)                        |
| Extra side inputs                 | **required** `s2_dates` (per-frame DOY values)                      |
| Training alignment (adapter path) | Medium (depends on frame count, normalization mode, and image size) |

---

## When To Use This Model

AnySat is a good fit when you want actual temporal S2 sequence modeling rather than a single composite, when day-of-year context matters, or when you are explicitly comparing multi-frame adapters such as `anysat`, `galileo`, and `agrifm`. It becomes easy to misuse if you compare it against single-composite models without matching temporal assumptions, if you change frame count or normalization without recording it, or if you read `grid` output as a georeferenced raster instead of model patch output.

---

## Input Contract (Current Adapter Path)

### Spatial / temporal

The adapter accepts `BBox` and `PointBuffer`, and normalizes `TemporalSpec` to a range internally; using `TemporalSpec.range(...)` directly is still the clearest and most reproducible choice. The requested window is split into `T` sub-windows, one composite is built per bin, and the midpoint of each bin is converted into AnySat-style day-of-year values in `s2_dates`.

### Sensor / channels

If `sensor` is omitted, AnySat uses `COPERNICUS/S2_SR_HARMONIZED` with bands `("B2","B3","B4","B5","B6","B7","B8","B8A","B11","B12")`, `scale_m=10`, `cloudy_pct=30`, `composite="median"`, and `fill_value=0.0`.

For `input_chw`, the adapter accepts either `CHW` or `TCHW` with `C=10`. A `CHW` tensor is repeated to `T` frames, while `TCHW` is padded or truncated to the exact configured frame count. Values are clipped to the raw-SR range `0..10000`.

---

## Preprocessing Pipeline (Current rs-embed Path)

<pre class="pipeline-flow"><code><span class="pipeline-root">INPUT</span>  provider fetch / input_chw
  <span class="pipeline-arrow">-&gt;</span> S2 10-band time series in TCHW
     <span class="pipeline-detail">input_chw path: coerce CHW / TCHW to exact T</span>
  <span class="pipeline-arrow">-&gt;</span> optional resize to RS_EMBED_ANYSAT_IMG=24
  <span class="pipeline-arrow">-&gt;</span> normalize series with RS_EMBED_ANYSAT_NORM
     <span class="pipeline-branch">per_tile_zscore:</span> default
     <span class="pipeline-branch">unit_scale / reflectance:</span> /10000 -&gt; [0,1]
     <span class="pipeline-branch">raw / none:</span> keep raw values
  <span class="pipeline-arrow">-&gt;</span> build AnySat side inputs
     <span class="pipeline-branch">s2:</span> [1,T,10,H,W]
     <span class="pipeline-branch">s2_dates:</span> [1,T] from frame-bin DOY midpoints
  <span class="pipeline-arrow">-&gt;</span> forward with AnySat spatial output
     <span class="pipeline-branch">grid path:</span> default `output="dense"` (`grid_feature_mode="dense"`)
     <span class="pipeline-branch">pooled path:</span> default compatibility path keeps `output="patch"`; optional `pooled_source="tile"` uses native AnySat tile output
  <span class="pipeline-arrow">-&gt;</span> map [B,H,W,D] -&gt; rs-embed grid [D,H,W]
  <span class="pipeline-arrow">-&gt;</span> output projection
     <span class="pipeline-branch">pooled:</span> spatial mean / max over patch grid
     <span class="pipeline-branch">grid:</span>   dense sub-patch grid by default (or patch grid when overridden)</code></pre>

Important constraint:

`sensor.scale_m` or `fetch.scale_m` must be a positive multiple of 10 meters.

---

## Environment Variables / Tuning Knobs

| Env var                          | Default                    | Effect                                                              |
| -------------------------------- | -------------------------- | ------------------------------------------------------------------- |
| `RS_EMBED_ANYSAT_FRAMES`         | `8`                        | Number of temporal frames `T`                                       |
| `RS_EMBED_ANYSAT_IMG`            | `24`                       | Per-frame resize target (square)                                    |
| `RS_EMBED_ANYSAT_NORM`           | `per_tile_zscore`          | Series normalization mode                                           |
| `RS_EMBED_ANYSAT_MODEL_SIZE`     | `base`                     | AnySat model size                                                   |
| `RS_EMBED_ANYSAT_GRID_MODE`      | `dense`                    | Grid path native AnySat spatial output (`dense` or `patch`)         |
| `RS_EMBED_ANYSAT_POOLED_SOURCE`  | `patch`                    | Pooled path source (`patch` compatibility pooling or native `tile`) |
| `RS_EMBED_ANYSAT_FLASH_ATTN`     | `0`                        | Enable flash attention path if supported                            |
| `RS_EMBED_ANYSAT_PRETRAINED`     | `1`                        | Load pretrained checkpoint weights                                  |
| `RS_EMBED_ANYSAT_CKPT`           | unset                      | Local checkpoint override                                           |
| `RS_EMBED_ANYSAT_HF_REPO`        | `g-astruc/AnySat`          | Hugging Face repo used for checkpoint download                      |
| `RS_EMBED_ANYSAT_HF_FILE`        | `models/AnySat.pth`        | Checkpoint file inside the Hugging Face repo                        |
| `RS_EMBED_ANYSAT_CACHE_DIR`      | `~/.cache/rs_embed/anysat` | Checkpoint cache dir                                                |
| `RS_EMBED_ANYSAT_CKPT_MIN_BYTES` | adapter threshold          | Download size sanity check                                          |
| `RS_EMBED_ANYSAT_FETCH_WORKERS`  | `8`                        | Provider prefetch workers for batch APIs                            |

## Output Semantics

AnySat now uses two spatial output paths inside the adapter. `pooled` defaults to the historical rs-embed behavior and applies spatial pooling over the AnySat `patch` grid, which preserves the previous pooled vector dimensionality; pass `pooled_source="tile"` (or set `RS_EMBED_ANYSAT_POOLED_SOURCE=tile`) to use the native AnySat tile embedding instead. `grid` defaults to AnySat `dense`, so the returned `(D,H,W)` is a denser sub-patch feature map by default; pass `grid_feature_mode="patch"` to the public API (or set `RS_EMBED_ANYSAT_GRID_MODE=patch`) to recover the older patch-grid behavior. As with other on-the-fly models, this grid is model space rather than guaranteed georeferenced raster pixels.

---

## Examples

### Minimal example

```python
from rs_embed import get_embedding, PointBuffer, TemporalSpec, OutputSpec

emb = get_embedding(
    "anysat",
    spatial=PointBuffer(lon=121.5, lat=31.2, buffer_m=2048),
    temporal=TemporalSpec.range("2022-01-01", "2023-01-01"),
    output=OutputSpec.pooled(),
    backend="auto",
)
```

### Example with temporal/frame tuning (env-controlled)

```python
# Example (shell):
# export RS_EMBED_ANYSAT_FRAMES=8
# export RS_EMBED_ANYSAT_NORM=per_tile_zscore
# export RS_EMBED_ANYSAT_IMG=24
```

---

## Common Failure Modes / Debugging

- backend is not provider-compatible
- wrong channel count for `input_chw` (must be 10 channels)
- `fetch.scale_m` / `sensor.scale_m` is not a positive multiple of 10
- missing `torch` / `einops` / `huggingface_hub` dependency for vendored runtime + checkpoint path
- local checkpoint missing / too small / invalid format
- inconsistent results from untracked changes to `FRAMES`, `NORM`, or image size

Recommended first check:

Inspect the input patches first and confirm that the temporal window and frame construction match the experiment you think you are running.

---

## Reproducibility Notes

For fair comparisons and stable reruns, record the temporal window, `RS_EMBED_ANYSAT_FRAMES`, `RS_EMBED_ANYSAT_NORM`, `RS_EMBED_ANYSAT_IMG`, the effective provider resolution from `fetch.scale_m` or `sensor.scale_m`, and the exact checkpoint source.

---

## Source of Truth (Code Pointers)

The main code paths are `src/rs_embed/embedders/catalog.py` for registration, `src/rs_embed/embedders/onthefly_anysat.py` for the adapter, and `src/rs_embed/embedders/runtime_utils.py` for TCHW coercion helpers.
