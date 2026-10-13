# Galileo (`galileo`)

> Multi-frame Sentinel-2 adapter that constructs Galileo encoder inputs (including `months`) from a temporal window and returns pooled vectors or patch-token grids.

## Quick Facts

| Field                             | Value                                                                                       |
| --------------------------------- | ------------------------------------------------------------------------------------------- |
| Model ID                          | `galileo`                                                                                   |
| Family / Backbone                 | Galileo `Encoder` from vendored local runtime                                               |
| Adapter type                      | `on-the-fly`                                                                                |
| Typical backend                   | provider-backed; prefer `backend="auto"` in public API                                      |
| Primary input                     | S2 10-band time series (`T,C,H,W`)                                                          |
| Default resolution                | 10m default provider fetch (`sensor.scale_m`)                                               |
| Temporal mode                     | `range` in practice (adapter normalizes via shared helper)                                  |
| Output modes                      | `pooled`, `grid`                                                                            |
| Extra side inputs                 | **required** `months` (per-frame month tokens), plus Galileo masks/tensors built by adapter |
| Training alignment (adapter path) | Medium (depends on `FRAMES`, `IMG`, `PATCH`, normalization)                                 |

---

## When To Use This Model

Galileo is a good fit for temporal S2 sequence modeling with explicit month tokens, comparisons against other multi-frame adapters such as `anysat` and `agrifm`, and feature-grid analysis over Galileo's S2-related token groups. The main pitfalls are comparing it to single-composite models without matching temporal assumptions, changing `image_size` and `patch_size` inconsistently, or changing month handling without documenting it.

---

## Input Contract (Current Adapter Path)

### Spatial / temporal

The adapter accepts `BBox` and `PointBuffer`, and normalizes `TemporalSpec` to a range through the shared helper; `TemporalSpec.range(...)` is still the clearest choice for reproducibility. Galileo builds `T` frames by splitting the requested window into equal sub-windows and compositing one frame per bin. The `months` side input is derived from frame-bin midpoints unless you force a constant month with `RS_EMBED_GALILEO_MONTH`.

### Sensor / channels

If `sensor` is omitted, Galileo uses `COPERNICUS/S2_SR_HARMONIZED` with bands `B2,B3,B4,B5,B6,B7,B8,B8A,B11,B12`, `scale_m=10`, `cloudy_pct=30`, `composite="median"`, and `fill_value=0.0`.

For `input_chw`, the adapter accepts `CHW` or `TCHW` with `C=10` through the shared coercion helper. `CHW` repeats to `T`, `TCHW` pads or truncates to exact `T`, and values are clipped to the raw-SR range `0..10000`.

---

## Preprocessing Pipeline (Current rs-embed Path)

<pre class="pipeline-flow"><code><span class="pipeline-root">INPUT</span>  provider fetch / input_chw
  <span class="pipeline-arrow">-&gt;</span> S2 10-band raw_tchw
     <span class="pipeline-detail">input_chw path: coerce to exact TCHW</span>
  <span class="pipeline-arrow">-&gt;</span> resolve months sequence
     <span class="pipeline-detail">frame-bin midpoints or RS_EMBED_GALILEO_MONTH override</span>
  <span class="pipeline-arrow">-&gt;</span> resize frames to RS_EMBED_GALILEO_IMG=64 if needed
  <span class="pipeline-arrow">-&gt;</span> normalize series with RS_EMBED_GALILEO_NORM
     <span class="pipeline-branch">default:</span> none
     <span class="pipeline-detail">use `official_stats` to match Galileo pretraining normalization</span>
  <span class="pipeline-arrow">-&gt;</span> build encoder tensors + masks
     <span class="pipeline-branch">inputs:</span> s_t_x, sp_x, t_x, st_x
     <span class="pipeline-branch">masks:</span>  s_t_m, sp_m, t_m, st_m
     <span class="pipeline-branch">side input:</span> months
  <span class="pipeline-arrow">-&gt;</span> Galileo encoder forward
     <span class="pipeline-detail">patch_size=RS_EMBED_GALILEO_PATCH=8</span>
  <span class="pipeline-arrow">-&gt;</span> output projection
     <span class="pipeline-branch">pooled:</span> visible-token average
     <span class="pipeline-branch">grid:</span>   official-style patch mean over visible tokens</code></pre>

Constraint:

`image_size % patch_size == 0` is required.

---

## Environment Variables / Tuning Knobs

| Env var                          | Default                     | Effect                                                                            |
| -------------------------------- | --------------------------- | --------------------------------------------------------------------------------- |
| `RS_EMBED_GALILEO_MODEL_SIZE`    | `nano`                      | Galileo model size selector (`models/<size>/`)                                    |
| `RS_EMBED_GALILEO_MODEL_PATH`    | unset                       | Local model folder override containing `config.json` + `encoder.pt`               |
| `RS_EMBED_GALILEO_HF_REPO`       | `nasaharvest/galileo`       | Hugging Face repo used for snapshot download                                      |
| `RS_EMBED_GALILEO_CACHE_DIR`     | `~/.cache/rs_embed/galileo` | Download cache dir for model snapshots                                            |
| `RS_EMBED_GALILEO_AUTO_DOWNLOAD` | `1`                         | Auto-download model folder from Hugging Face when `MODEL_PATH` is unset           |
| `RS_EMBED_GALILEO_IMG`           | `64`                        | Frame resize target                                                               |
| `RS_EMBED_GALILEO_PATCH`         | `8`                         | Encoder patch size                                                                |
| `RS_EMBED_GALILEO_FRAMES`        | `8`                         | Number of temporal frames `T`                                                     |
| `RS_EMBED_GALILEO_NORM`          | `none`                      | S2 normalization mode (`none`, `unit_scale`, `per_tile_minmax`, `official_stats`) |
| `RS_EMBED_GALILEO_ADD_LN`        | `1`                         | Add layer norm on encoder exit                                                    |
| `RS_EMBED_GALILEO_MONTH`         | unset                       | Force a constant month (1..12) for all frames                                     |
| `RS_EMBED_GALILEO_FETCH_WORKERS` | `8`                         | Prefetch workers for batch APIs                                                   |

---

## Output Semantics

### `OutputSpec.pooled()`

The default pooled path uses Galileo's pooled token output, recorded with `token_mean` semantics in metadata. If `OutputSpec.pooling="max"`, the adapter max-pools the produced grid instead and records `grid_max`.

### `OutputSpec.grid()`

`OutputSpec.grid()` returns a Galileo patch-token grid as `xarray.DataArray` `(D,H,W)`. The adapter now follows Galileo's own patch-level token averaging path when available, so each spatial position is the mean of visible tokens assigned to that patch. This is model token structure rather than georeferenced raster space.

---

## Examples

### Minimal example

```python
from rs_embed import get_embedding, PointBuffer, TemporalSpec, OutputSpec

emb = get_embedding(
    "galileo",
    spatial=PointBuffer(lon=121.5, lat=31.2, buffer_m=2048),
    temporal=TemporalSpec.range("2022-01-01", "2023-01-01"),
    output=OutputSpec.pooled(),
    backend="auto",
)
```

### Example tuning temporal packaging (env-controlled)

```python
# Example (shell):
# export RS_EMBED_GALILEO_FRAMES=8
# export RS_EMBED_GALILEO_IMG=64
# export RS_EMBED_GALILEO_PATCH=8
# export RS_EMBED_GALILEO_NORM=official_stats
```

---

## Common Failure Modes / Debugging

- backend is not provider-compatible
- `image_size` not divisible by `patch_size`
- wrong `input_chw` channel count (must be 10)
- unexpected effects from `RS_EMBED_GALILEO_MONTH` forcing a constant month
- missing `huggingface_hub` / `einops` dependency
- missing local model folder when auto-download is disabled

Recommended first checks:

Verify temporal window, frame count, and month sequence in metadata first. Inspect raw inputs before changing normalization or model settings.

---

## Reproducibility Notes

Keep the temporal window, `RS_EMBED_GALILEO_FRAMES`, `RS_EMBED_GALILEO_IMG`, `RS_EMBED_GALILEO_PATCH`, normalization mode, month override, and model source fixed and recorded.

---

## Source of Truth (Code Pointers)

The main code paths are `src/rs_embed/embedders/catalog.py` for registration, `src/rs_embed/embedders/onthefly_galileo.py` for the adapter, and `src/rs_embed/embedders/runtime_utils.py` for shared TCHW coercion.
