# FoMo (`fomo`)

> Multispectral Sentinel-2 adapter for FoMo-Bench (MultiSpectralViT), with explicit S2 modality-key mapping and token/grid outputs averaged across spectral modalities.

## Quick Facts

| Field                             | Value                                                                                    |
| --------------------------------- | ---------------------------------------------------------------------------------------- |
| Model ID                          | `fomo`                                                                                   |
| Family / Backbone                 | FoMo-Bench `MultiSpectralViT` (vendored local code + checkpoint loader)                  |
| Adapter type                      | `on-the-fly`                                                                             |
| Typical backend                   | provider backend (`gee`)                                                                 |
| Primary input                     | S2 SR 12-band (`B1,B2,B3,B4,B5,B6,B7,B8,B8A,B9,B11,B12`)                                 |
| Default resolution                | 10m default provider fetch (`sensor.scale_m`)                                            |
| Temporal mode                     | `range` in practice (normalized via shared helper)                                       |
| Output modes                      | `pooled`, `grid`                                                                         |
| Extra side inputs                 | **required modality keys** (adapter provides S2 defaults, configurable via env)          |
| Training alignment (adapter path) | Medium-High when `S2_KEYS`, normalization, and model config match checkpoint assumptions |

---

## When To Use This Model

FoMo is a good fit for strict multispectral S2 experiments with spectral-token modeling, for testing modality-aware token layouts beyond plain RGB ViT pipelines, and for analyses where averaging spectral tokens into one spatial grid is acceptable. The main pitfalls are changing `RS_EMBED_FOMO_S2_KEYS` without understanding FoMo modality indexing, treating the FoMo grid as georeferenced pixels, or modifying architecture envs while keeping an incompatible checkpoint.

---

## Input Contract (Current Adapter Path)

### Spatial / temporal

FoMo is provider-backed, so use `backend="gee"` or another provider-compatible backend. `TemporalSpec` is normalized through the shared helper, and `TemporalSpec.range(...)` is the clearest option.

### Sensor / channels

If `sensor` is omitted, FoMo uses `COPERNICUS/S2_SR_HARMONIZED` with bands `B1,B2,B3,B4,B5,B6,B7,B8,B8A,B9,B11,B12`, `scale_m=10`, `cloudy_pct=30`, `composite="median"`, and `fill_value=0.0`. If you pass `input_chw`, it must be `CHW` with `C=12` in that adapter band order and raw S2 SR values in `0..10000`.

### Modality keys

The FoMo forward path requires one modality key per channel. The default S2 mapping is encoded in `_DEFAULT_S2_MODALITY_KEYS`, and you can override it with `RS_EMBED_FOMO_S2_KEYS`, which must provide exactly 12 comma-separated integers.

---

## Preprocessing Pipeline (Current rs-embed Path)

<pre class="pipeline-flow"><code><span class="pipeline-root">INPUT</span>  provider fetch / input_chw
  <span class="pipeline-arrow">-&gt;</span> S2 SR 12-band patch
  <span class="pipeline-arrow">-&gt;</span> normalize with RS_EMBED_FOMO_NORM
     <span class="pipeline-branch">unit_scale:</span> /10000
     <span class="pipeline-branch">per_tile_minmax:</span> per-channel min-max after unit scaling
     <span class="pipeline-branch">none / raw:</span> keep clipped raw values
  <span class="pipeline-arrow">-&gt;</span> resize to RS_EMBED_FOMO_IMG=64
  <span class="pipeline-arrow">-&gt;</span> load FoMo runtime + checkpoint
     <span class="pipeline-detail">vendored local runtime with local / auto-downloaded weights</span>
  <span class="pipeline-arrow">-&gt;</span> forward(x, spectral_keys, pool=False)
  <span class="pipeline-arrow">-&gt;</span> token output [N,D]
  <span class="pipeline-arrow">-&gt;</span> output projection
     <span class="pipeline-branch">pooled:</span> mean / max over all tokens
     <span class="pipeline-branch">grid:</span>   modality-averaged patch grid when available
     <span class="pipeline-branch">fallback:</span> 1x1 vector grid</code></pre>

---

## Environment Variables / Tuning Knobs

### Core model / preprocessing

| Env var                       | Default                    | Effect                                                 |
| ----------------------------- | -------------------------- | ------------------------------------------------------ |
| `RS_EMBED_FOMO_IMG`           | `64`                       | Resize target image size                               |
| `RS_EMBED_FOMO_PATCH`         | `16`                       | Patch size (used for model config + grid expectations) |
| `RS_EMBED_FOMO_NORM`          | `unit_scale`               | `unit_scale`, `per_tile_minmax`, or `none`             |
| `RS_EMBED_FOMO_S2_KEYS`       | adapter S2 default mapping | 12 comma-separated modality keys                       |
| `RS_EMBED_FOMO_FETCH_WORKERS` | `8`                        | Provider prefetch workers for batch APIs               |

### FoMo model config (advanced; keep aligned with checkpoint)

| Env var                     | Default | Effect                                 |
| --------------------------- | ------- | -------------------------------------- |
| `RS_EMBED_FOMO_DIM`         | `768`   | Model dim                              |
| `RS_EMBED_FOMO_DEPTH`       | `12`    | Transformer depth                      |
| `RS_EMBED_FOMO_HEADS`       | `12`    | Attention heads                        |
| `RS_EMBED_FOMO_MLP_DIM`     | `2048`  | MLP dim                                |
| `RS_EMBED_FOMO_NUM_CLASSES` | `1000`  | Class head size (config compatibility) |

### Checkpoint loading

| Env var                        | Default                          | Effect                         |
| ------------------------------ | -------------------------------- | ------------------------------ |
| `RS_EMBED_FOMO_CKPT`           | unset                            | Local checkpoint path          |
| `RS_EMBED_FOMO_AUTO_DOWNLOAD`  | `1`                              | Allow checkpoint auto-download |
| `RS_EMBED_FOMO_CACHE_DIR`      | `~/.cache/rs_embed/fomo`         | Checkpoint cache dir           |
| `RS_EMBED_FOMO_CKPT_FILE`      | default FoMo checkpoint filename | Cached ckpt filename           |
| `RS_EMBED_FOMO_CKPT_URL`       | default Dropbox URL              | Checkpoint download URL        |
| `RS_EMBED_FOMO_CKPT_MIN_BYTES` | adapter threshold                | Download size sanity check     |

---

## Output Semantics

### `OutputSpec.pooled()`

`OutputSpec.pooled()` pools the FoMo token sequence across tokens. `mean` becomes `token_mean`, `max` becomes `token_max`, and metadata records `token_count`, `token_dim`, and pooling mode.

### `OutputSpec.grid()`

The preferred path interprets tokens as `[modalities, H, W, D]`, averages over modalities, and returns `(D,H,W)` with `grid_kind="spectral_mean_patch_tokens"`. If token layout is incompatible with the expected modality or grid structure, the adapter falls back to a `1x1` vector grid with `grid_kind="vector_as_1x1"`. In either case, this remains model token structure rather than georeferenced raster space.

---

## Examples

### Minimal provider-backed example

```python
from rs_embed import get_embedding, PointBuffer, TemporalSpec, OutputSpec

emb = get_embedding(
    "fomo",
    spatial=PointBuffer(lon=121.5, lat=31.2, buffer_m=2048),
    temporal=TemporalSpec.range("2022-06-01", "2022-09-01"),
    output=OutputSpec.pooled(),
    backend="gee",
)
```

### Example FoMo tuning (env-controlled)

```python
# Example (shell):
# export RS_EMBED_FOMO_IMG=64
# export RS_EMBED_FOMO_PATCH=16
# export RS_EMBED_FOMO_NORM=unit_scale
# export RS_EMBED_FOMO_S2_KEYS=6,7,8,9,10,11,12,13,14,15,17,18
```

---

## Common Failure Modes / Debugging

- backend mismatch (`fomo` is provider-only)
- wrong `input_chw` shape (`C` must be `12`)
- `RS_EMBED_FOMO_S2_KEYS` length mismatch (must be 12 values)
- missing `torch` / `einops` dependency or checkpoint/import failures
- changed model config envs incompatible with checkpoint architecture
- grid returns `1x1` fallback because token layout is not modality-grid compatible

Recommended first checks:

Inspect metadata such as `spectral_keys`, `token_count`, `grid_kind`, and `grid_expected_tokens` first. Revert architecture envs to defaults before benchmarking, and verify normalization mode together with image and patch sizes.

---

## Reproducibility Notes

Keep the checkpoint source or path, vendored FoMo runtime version, `IMG`, `PATCH`, normalization mode, `S2_KEYS` mapping, model config envs, and temporal plus compositing settings fixed and recorded.

---

## Source of Truth (Code Pointers)

The main code paths are `src/rs_embed/embedders/catalog.py` for registration and `src/rs_embed/embedders/onthefly_fomo.py` for the adapter implementation.
