# SatMAE RGB (`satmae`)

> Sentinel-2 RGB on-the-fly adapter for SatMAE (`rshf.satmae.SatMAE`), returning pooled vectors or ViT patch-token grids from `forward_encoder(mask_ratio=0.0)`.

## Quick Facts

| Field                             | Value                                                                          |
| --------------------------------- | ------------------------------------------------------------------------------ |
| Model ID                          | `satmae`                                                                       |
| Aliases                           | `satmae_rgb`                                                                   |
| Family / Backbone                 | SatMAE via `rshf.satmae.SatMAE`                                                |
| Adapter type                      | `on-the-fly`                                                                   |
| Typical backend                   | provider backend (`gee`)                                                       |
| Primary input                     | S2 RGB (`B4,B3,B2`)                                                            |
| Default resolution                | 10m default provider fetch (`sensor.scale_m`)                                  |
| Temporal mode                     | range window in practice (normalized via shared helper)                        |
| Output modes                      | `pooled`, `grid`                                                               |
| Extra side inputs                 | none                                                                           |
| Training alignment (adapter path) | Medium-High (higher when wrapper `model.transform(...)` is available and used) |

---

## When To Use This Model

SatMAE is a strong RGB-only Sentinel-2 baseline when you want MAE-style token features, `OutputSpec.grid()` inspection, or direct comparisons with other RGB ViT adapters such as `remoteclip`, `scalemae`, and `wildsat`.

It is a weaker fit when multispectral semantics matter, and its `grid` output should still be read as a patch-token grid rather than georeferenced pixels. For cross-environment comparisons, keep in mind that `rshf` wrapper preprocessing behavior can influence outputs.

---

## Input Contract (Current Adapter Path)

### Spatial / temporal

The current adapter path is provider-only, so use `backend="gee"` or another provider-compatible backend. `TemporalSpec` is normalized with the shared helper, and `TemporalSpec.range(...)` remains the safest choice for reproducibility. The temporal window is used for compositing and filtering rather than locking the request to a single source scene.

### Sensor / channels

Default `SensorSpec` if omitted:

The default sensor is `COPERNICUS/S2_SR_HARMONIZED` with bands `("B4", "B3", "B2")`, `scale_m=10`, `cloudy_pct=30`, and `composite="median"`.

`input_chw` contract:

`input_chw` must be `CHW` with exactly 3 bands in `(B4,B3,B2)` order. The adapter expects raw Sentinel-2 SR values in `0..10000`, converts them to `[0,1]`, and then converts them to `uint8` RGB before model preprocessing.

---

## Preprocessing Pipeline (Current rs-embed Path)

<pre class="pipeline-flow"><code><span class="pipeline-root">INPUT</span>  provider fetch / input_chw
  <span class="pipeline-arrow">-&gt;</span> S2 RGB uint8 patch
     <span class="pipeline-detail">input_chw path: raw SR -&gt; [0,1] -&gt; uint8</span>
  <span class="pipeline-arrow">-&gt;</span> resize to RS_EMBED_SATMAE_IMG=224
  <span class="pipeline-arrow">-&gt;</span> model preprocess
     <span class="pipeline-branch">preferred:</span> model.transform(rgb_u8, image_size)
     <span class="pipeline-branch">fallback:</span>  rgb_u8_to_tensor_clipnorm
  <span class="pipeline-arrow">-&gt;</span> forward_encoder(mask_ratio=0.0)
  <span class="pipeline-arrow">-&gt;</span> output projection
     <span class="pipeline-branch">pooled:</span> patch-token mean / max
     <span class="pipeline-branch">grid:</span>   patch-token reshape</code></pre>

Notes:

The current adapter path always targets token output rather than pre-pooled wrapper outputs. If a CLS token is present, the pooling and grid helpers remove it automatically.

---

## Environment Variables / Tuning Knobs

| Env var                         | Default                                  | Effect                                            |
| ------------------------------- | ---------------------------------------- | ------------------------------------------------- |
| `RS_EMBED_SATMAE_ID`            | `MVRL/satmae-vitlarge-fmow-pretrain-800` | HF model ID used by `SatMAE.from_pretrained(...)` |
| `RS_EMBED_SATMAE_IMG`           | `224`                                    | Resize / preprocess image size                    |
| `RS_EMBED_SATMAE_FETCH_WORKERS` | `8`                                      | Provider prefetch workers for batch APIs          |
| `RS_EMBED_SATMAE_BATCH_SIZE`    | CPU:`8`, CUDA:`32`                       | Inference batch size for batch APIs               |

---

## Output Semantics

SatMAE also follows the standard pooled and patch-token grid behavior. `pooled` uses token pooling according to `OutputSpec.pooling`, and `grid` reshapes the token sequence to `(D,H,W)` in ViT patch-token space rather than georeferenced raster pixels.

---

## Examples

### Minimal provider-backed example

```python
from rs_embed import get_embedding, PointBuffer, TemporalSpec, OutputSpec

emb = get_embedding(
    "satmae",
    spatial=PointBuffer(lon=121.5, lat=31.2, buffer_m=2048),
    temporal=TemporalSpec.range("2022-06-01", "2022-09-01"),
    output=OutputSpec.pooled(),
    backend="gee",
)
```

### Example model/image-size tuning (env-controlled)

```python
# Example (shell):
# export RS_EMBED_SATMAE_ID=MVRL/satmae-vitlarge-fmow-pretrain-800
# export RS_EMBED_SATMAE_IMG=224
```

---

## Common Failure Modes / Debugging

- backend mismatch (`satmae` is provider-only)
- wrong `input_chw` shape or band order (must be `CHW`, `C=3`, `(B4,B3,B2)`)
- missing `rshf` / incompatible `rshf` version (no `SatMAE` wrapper or `forward_encoder`)
- `grid` requests failing if token output shape is unexpected

Recommended first checks:

Start by checking metadata such as `tokens_shape` and `grid_hw`, then confirm `RS_EMBED_SATMAE_ID` and `RS_EMBED_SATMAE_IMG`. If you pass a custom `input_chw`, verify that it is still raw SR rather than already scaled to `0..1`, unless that conversion was intentional.

---

## Reproducibility Notes

For reproducibility, keep `RS_EMBED_SATMAE_ID`, `RS_EMBED_SATMAE_IMG`, the temporal window, compositing settings, output mode, and pooling choice fixed. It is also worth recording the `rshf` version, because wrapper preprocessing behavior can matter.

---

## Source of Truth (Code Pointers)

The code paths to check are `src/rs_embed/embedders/catalog.py`, `src/rs_embed/embedders/onthefly_satmae.py`, and the shared helpers in `src/rs_embed/embedders/_vit_mae_utils.py`.
