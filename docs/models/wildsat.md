# WildSAT (`wildsat`)

> Sentinel-2 RGB on-the-fly adapter for WildSAT checkpoints, supporting multiple backbone architectures (ViT/ResNet/Swin), optional decoder image-head features, and token-grid fallback behavior.

## Quick Facts

| Field                             | Value                                                                                         |
| --------------------------------- | --------------------------------------------------------------------------------------------- |
| Model ID                          | `wildsat`                                                                                     |
| Family / Backbone                 | WildSAT checkpoint loader + torchvision backbones (`vitb16`, `vitl16`, `resnet50`, `swint`)   |
| Adapter type                      | `on-the-fly`                                                                                  |
| Typical backend                   | provider backend (`gee`)                                                                      |
| Primary input                     | S2 RGB (`B4,B3,B2`)                                                                           |
| Default resolution                | 10m default provider fetch (`sensor.scale_m`)                                                 |
| Temporal mode                     | `range` in practice (normalized via shared helper)                                            |
| Output modes                      | `pooled`, `grid`                                                                              |
| Extra side inputs                 | none (but checkpoint/arch/image-head settings matter)                                         |
| Training alignment (adapter path) | Medium (depends on checkpoint source, arch inference, normalization mode, and feature source) |

---

## When To Use This Model

WildSAT is useful when you want to experiment with different checkpoints and feature targets in one adapter, compare backbone features against image-head features through `RS_EMBED_WILDSAT_FEATURE`, or keep RGB workflows unified across ViT, ResNet, and Swin-style backbones. It is especially relevant for ecological and environmental downstream tasks, because the original WildSAT training objective jointly used satellite images, species occurrence maps, and habitat text to encode biodiversity-related and habitat-level signals rather than only generic visual similarity.

Its flexibility also makes configuration drift easier. If architecture inference is ambiguous, set `RS_EMBED_WILDSAT_ARCH` explicitly. Normalization mode changes such as `minmax` versus `unit_scale` should be logged, and `grid` should not be assumed to mean a ViT patch grid because some paths intentionally return a `1x1` vector grid instead.

---

## Input Contract (Current Adapter Path)

### Spatial / temporal

The current adapter path is provider-only, so use `backend="gee"` or another provider-compatible backend. `TemporalSpec` is normalized via the shared helper, and `TemporalSpec.range(...)` is still the safest path for reproducible runs.

### Sensor / channels

Default `SensorSpec` if omitted:

The default sensor is `COPERNICUS/S2_SR_HARMONIZED` with bands `("B4", "B3", "B2")`, `scale_m=10`, `cloudy_pct=30`, and `composite="median"`.

`input_chw` contract:

`input_chw` must be `CHW` with `C=3` in `(B4,B3,B2)` order. The adapter expects raw values in `0..10000`, clips NaN and Inf values, and converts the normalized result to `uint8` RGB.

---

## Preprocessing Pipeline (Current rs-embed Path)

<pre class="pipeline-flow"><code><span class="pipeline-root">SETUP</span>  resolve checkpoint path
  <span class="pipeline-arrow">-&gt;</span> local checkpoint or auto-download
<span class="pipeline-root">INPUT</span>  provider fetch / input_chw
  <span class="pipeline-arrow">-&gt;</span> S2 RGB patch
  <span class="pipeline-arrow">-&gt;</span> normalize raw_chw with RS_EMBED_WILDSAT_NORM
     <span class="pipeline-branch">minmax:</span> per-tile min-max after unit scaling
     <span class="pipeline-branch">unit_scale / none:</span> keep unit-scaled values
  <span class="pipeline-arrow">-&gt;</span> uint8 HWC + resize to RS_EMBED_WILDSAT_IMG=224
  <span class="pipeline-arrow">-&gt;</span> load backbone + optional decoder image head
  <span class="pipeline-arrow">-&gt;</span> forward pass
     <span class="pipeline-branch">feature source:</span> image_head | backbone | auto
     <span class="pipeline-detail">optional ViT token extraction for token pooling / grid</span>
  <span class="pipeline-arrow">-&gt;</span> output projection
     <span class="pipeline-branch">pooled:</span> vector
     <span class="pipeline-branch">grid:</span>   token grid or 1x1 fallback</code></pre>

Important behavior:

If `grid` is requested but ViT tokens are unavailable, for example with a non-ViT architecture or when token extraction is disabled, the adapter returns a `1x1` grid with `grid_kind="vector_as_1x1"` instead of failing.

---

## Environment Variables / Tuning Knobs

### Runtime / feature extraction

| Env var                               | Default      | Effect                                                                  |
| ------------------------------------- | ------------ | ----------------------------------------------------------------------- |
| `RS_EMBED_WILDSAT_ARCH`               | `auto`       | Backbone arch hint (`vitb16`, `vitl16`, `resnet50`, `swint`, or `auto`) |
| `RS_EMBED_WILDSAT_IMG`                | `224`        | Resize target image size                                                |
| `RS_EMBED_WILDSAT_NORM`               | `minmax`     | `minmax`, `unit_scale`, or `none`                                       |
| `RS_EMBED_WILDSAT_FEATURE`            | `image_head` | Feature source: `auto`, `image_head`, `backbone`                        |
| `RS_EMBED_WILDSAT_IMAGE_BRANCH`       | `3`          | Preferred decoder branch for image head extraction                      |
| `RS_EMBED_WILDSAT_POOLED_FROM_TOKENS` | `0`          | If true and ViT tokens available, pooled output uses token pooling      |
| `RS_EMBED_WILDSAT_GRID_FROM_TOKENS`   | `1`          | Enable ViT token extraction for grid/token-based pooling                |
| `RS_EMBED_WILDSAT_FETCH_WORKERS`      | `8`          | Provider prefetch workers for batch APIs                                |

### Checkpoint path / download

| Env var                           | Default                     | Effect                                               |
| --------------------------------- | --------------------------- | ---------------------------------------------------- |
| `RS_EMBED_WILDSAT_CKPT`           | unset                       | Local checkpoint path                                |
| `RS_EMBED_WILDSAT_AUTO_DOWNLOAD`  | `1`                         | Allow auto-download if `CKPT` not set                |
| `RS_EMBED_WILDSAT_CACHE_DIR`      | `~/.cache/rs_embed/wildsat` | Checkpoint cache dir                                 |
| `RS_EMBED_WILDSAT_CKPT_MIN_BYTES` | adapter threshold           | Download size sanity check                           |
| `RS_EMBED_WILDSAT_GDRIVE_ID`      | official sample file id     | Google Drive source (default auto-download path)     |
| `RS_EMBED_WILDSAT_CKPT_FILE`      | `vitb16-imagenet-bnfc.pth`  | Local cached filename for GDrive path                |
| `RS_EMBED_WILDSAT_HF_REPO`        | unset                       | Optional HF repo override (must pair with `HF_FILE`) |
| `RS_EMBED_WILDSAT_HF_FILE`        | unset                       | Optional HF file override (must pair with `HF_REPO`) |

---

## Output Semantics

### `OutputSpec.pooled()`

By default, `OutputSpec.pooled()` usually returns the selected feature-source vector, with `image_head` preferred unless configuration says otherwise. If `RS_EMBED_WILDSAT_POOLED_FROM_TOKENS=1` and ViT tokens are available, the adapter instead pools tokens with `mean` or `max`. Metadata records `feature_source`, `tokens_available`, and `pooled_from_tokens`.

### `OutputSpec.grid()`

If ViT tokens are available and token-grid extraction is enabled, `OutputSpec.grid()` returns a ViT patch-token grid with `grid_kind="vit_patch_tokens"`. Otherwise it returns a `1x1` vector grid with `grid_kind="vector_as_1x1"`. In either case, the result is model feature layout rather than georeferenced raster pixels.

---

## Examples

### Minimal provider-backed example

```python
from rs_embed import get_embedding, PointBuffer, TemporalSpec, OutputSpec

emb = get_embedding(
    "wildsat",
    spatial=PointBuffer(lon=121.5, lat=31.2, buffer_m=2048),
    temporal=TemporalSpec.range("2022-06-01", "2022-09-01"),
    output=OutputSpec.pooled(),
    backend="gee",
)
```

### Example feature/arch tuning (env-controlled)

```python
# Example (shell):
# export RS_EMBED_WILDSAT_ARCH=vitb16
# export RS_EMBED_WILDSAT_FEATURE=image_head
# export RS_EMBED_WILDSAT_NORM=minmax
# export RS_EMBED_WILDSAT_GRID_FROM_TOKENS=1
```

---

## Common Failure Modes / Debugging

- backend mismatch (`wildsat` is provider-only)
- missing/invalid checkpoint path or auto-download failure
- unsupported / mis-inferred architecture (`RS_EMBED_WILDSAT_ARCH`)
- invalid `RS_EMBED_WILDSAT_FEATURE` value
- misunderstanding `grid` fallback (`1x1` vector grid is expected in some configs)
- token-based pooling requested but tokens unavailable (adapter silently falls back to vector path and records metadata)

Recommended first checks:

Inspect metadata for `arch`, `feature_source`, `tokens_available`, and `grid_kind` first. If checkpoint inference is ambiguous, set `RS_EMBED_WILDSAT_ARCH` explicitly, and stabilize the checkpoint source before tuning feature branch or normalization details.

---

## Reproducibility Notes

For reproducibility, keep the checkpoint path or source fixed and record a file hash when possible. It is also worth fixing `RS_EMBED_WILDSAT_ARCH`, normalization mode, feature source, image branch, token-grid toggles, temporal window, and provider compositing settings.

---

## Source of Truth (Code Pointers)

The implementation details are in `src/rs_embed/embedders/catalog.py`, `src/rs_embed/embedders/onthefly_wildsat.py`, and the shared helpers in `src/rs_embed/embedders/_vit_mae_utils.py`.
