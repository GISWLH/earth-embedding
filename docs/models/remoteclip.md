# RemoteCLIP (`remoteclip`)

> Sentinel-2 RGB on-the-fly embedding via `rshf.remoteclip.RemoteCLIP`, with pooled vector or ViT token-grid outputs.

## Quick Facts

| Field                             | Value                                                                                                            |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Model ID                          | `remoteclip`                                                                                                     |
| Aliases                           | `remoteclip_s2rgb`                                                                                               |
| Family / Backbone                 | RemoteCLIP (CLIP-style ViT via `rshf.remoteclip.RemoteCLIP`)                                                     |
| Adapter type                      | `on-the-fly`                                                                                                     |
| Typical backend                   | provider-backed; prefer `backend="auto"` in public API                                                           |
| Primary input                     | S2 RGB (`B4,B3,B2`)                                                                                              |
| Default resolution                | 10m default provider fetch (`sensor.scale_m`)                                                                    |
| Temporal mode                     | `TemporalSpec.range(...)` required                                                                               |
| Output modes                      | `pooled`, `grid`                                                                                                 |
| Extra side inputs                 | none                                                                                                             |
| Training alignment (adapter path) | Medium (higher if wrapper `model.transform(...)` matches training pipeline; fallback is generic CLIP preprocess) |

---

## When To Use This Model

RemoteCLIP is a good fit for fast Sentinel-2 RGB baselines, CLIP-style retrieval experiments, and simple cross-model comparisons where `OutputSpec.pooled()` is enough. Be more careful if you need strict multispectral semantics, if you plan to treat `grid` output as georeferenced pixels, or if your wrapper build only exposes pooled outputs and therefore cannot serve a token grid.

---

## Input Contract (Current Adapter Path)

### Spatial / temporal

The adapter accepts `BBox` and `PointBuffer`. `TemporalSpec` must be `TemporalSpec.range(start, end)`, and that range is treated as a filter-and-composite window, not as a guarantee of one exact acquisition.

### Sensor / channels

If `sensor` is omitted, the default path uses `COPERNICUS/S2_SR_HARMONIZED` with bands `("B4", "B3", "B2")`, `scale_m=10`, `cloudy_pct=30`, and `composite="median"`. `sensor.collection` can also be used as a checkpoint override in the form `hf:<repo_or_path>`, for example `hf:MVRL/remote-clip-vit-base-patch32`. If you bypass provider fetch with `input_chw`, it must be `CHW` with exactly three bands in `(B4,B3,B2)` order.

---

## Preprocessing Pipeline (Current rs-embed Path)

<pre class="pipeline-flow"><code><span class="pipeline-root">INPUT</span>  provider fetch / input_chw
  <span class="pipeline-arrow">-&gt;</span> S2 RGB patch
  <span class="pipeline-arrow">-&gt;</span> normalize raw SR to [0,1]
     <span class="pipeline-detail">input_chw path: /10000 -&gt; clip</span>
  <span class="pipeline-arrow">-&gt;</span> optional checks + quicklook export
  <span class="pipeline-arrow">-&gt;</span> CHW [0,1] -&gt; uint8 HWC
  <span class="pipeline-arrow">-&gt;</span> model preprocess
     <span class="pipeline-branch">preferred:</span> model.transform(rgb_u8, image_size)
     <span class="pipeline-branch">fallback:</span>  Resize(224) -&gt; CenterCrop(224) -&gt; ToTensor -&gt; CLIP normalization
  <span class="pipeline-arrow">-&gt;</span> forward pass
     <span class="pipeline-branch">preferred:</span> token sequence
     <span class="pipeline-branch">fallback:</span>  pooled vector</code></pre>

Current adapter image size:

The image size is fixed at `224` in this adapter path.

---

## Environment Variables / Tuning Knobs

| Env var                                                  | Default            | Effect                                                   |
| -------------------------------------------------------- | ------------------ | -------------------------------------------------------- |
| `RS_EMBED_REMOTECLIP_FETCH_WORKERS`                      | `8`                | Provider prefetch worker count for batch APIs            |
| `RS_EMBED_REMOTECLIP_BATCH_SIZE`                         | CPU:`8`, CUDA:`64` | Inference batch size for batch APIs                      |
| `HUGGINGFACE_HUB_CACHE` / `HF_HOME` / `HUGGINGFACE_HOME` | unset              | Controls HF cache path used for model snapshot downloads |

Checkpoint override (not env-based in this adapter):

Set `sensor.collection="hf:<repo_or_local_path>"`.

---

## Output Semantics

RemoteCLIP mostly follows the standard pooled and patch-token grid behavior. `pooled` returns a vector `(D,)`, usually via token mean pooling when tokens are available, while `grid` returns a ViT token grid `(D,H,W)` in model token space rather than georeferenced raster pixels.

---

## Examples

### Minimal example

```python
from rs_embed import get_embedding, PointBuffer, TemporalSpec, OutputSpec

emb = get_embedding(
    "remoteclip",
    spatial=PointBuffer(lon=121.5, lat=31.2, buffer_m=2048),
    temporal=TemporalSpec.range("2022-06-01", "2022-09-01"),
    output=OutputSpec.pooled(),
    backend="auto",
)
```

### Custom checkpoint via `sensor.collection="hf:..."`

```python
from rs_embed import get_embedding, PointBuffer, TemporalSpec, OutputSpec, SensorSpec

emb = get_embedding(
    "remoteclip",
    spatial=PointBuffer(lon=121.5, lat=31.2, buffer_m=2048),
    temporal=TemporalSpec.range("2022-06-01", "2022-09-01"),
    sensor=SensorSpec(
        collection="hf:MVRL/remote-clip-vit-base-patch32",
        bands=("B4", "B3", "B2"),
        scale_m=10,
        cloudy_pct=30,
        composite="median",
    ),
    output=OutputSpec.grid(),
    backend="auto",
)
```

---

## Common Failure Modes / Debugging

- `backend` is not provider-compatible (`backend="auto"` is the recommended public default)
- `TemporalSpec` is missing or not `range`
- `input_chw` shape is not `CHW` with 3 channels
- missing optional dependencies (`rshf`, `huggingface_hub`, torch stack)
- `grid` requested but wrapper only exposes pooled outputs / no token path

Recommended first check:

Use `inspect_provider_patch(...)` or `inspect_gee_patch(...)` to verify raw RGB inputs and temporal composite quality before debugging the model path.

---

## Reproducibility Notes

For fair comparisons, keep the ROI, temporal window, `SensorSpec.composite`, `OutputSpec` mode, checkpoint choice, and preprocessing path fixed. In particular, log whether the run used the wrapper transform or the CLIP-style fallback, because those paths are not identical.

---

## Source of Truth (Code Pointers)

The main code paths are `src/rs_embed/embedders/catalog.py` for registration and `src/rs_embed/embedders/onthefly_remoteclip.py` for the adapter itself, including the token reshape helpers.
