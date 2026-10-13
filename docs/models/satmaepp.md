# SatMAE++ Family (`satmaepp`, `satmaepp_s2_10b`)

> `rs-embed` currently exposes two SatMAE++ adapter paths: RGB (`satmaepp`) and Sentinel-2 10-band (`satmaepp_s2_10b`). This page documents the shared behavior first, then the variant-specific details.

## Quick Facts

| Field              | `satmaepp` (RGB)                              | `satmaepp_s2_10b` (S2-10B)                         |
| ------------------ | --------------------------------------------- | -------------------------------------------------- |
| Canonical ID       | `satmaepp`                                    | `satmaepp_s2_10b`                                  |
| Aliases            | `satmaepp_rgb`, `satmae++`                    | `satmaepp_sentinel10`, `satmaepp_s2`               |
| Adapter type       | `on-the-fly`                                  | `on-the-fly`                                       |
| Typical backend    | provider backend (`gee`)                      | provider backend (`gee`)                           |
| Primary input      | S2 RGB (`B4,B3,B2`)                           | S2 SR 10-band (`B2,B3,B4,B5,B6,B7,B8,B8A,B11,B12`) |
| Default resolution | 10m default provider fetch (`sensor.scale_m`) | 10m default provider fetch (`sensor.scale_m`)      |
| Temporal mode      | range window + single composite               | range window + single composite                    |
| Output modes       | `pooled`, `grid`                              | `pooled`, `grid`                                   |
| Model config keys  | none                                          | `variant` (default: `large`; choices: `large`)     |
| Core extraction    | `forward_encoder(mask_ratio=0.0)`             | `forward_encoder(mask_ratio=0.0)`                  |

---

## When To Use This Family

The SatMAE++ family is useful when you want MAE-style patch-token features with a familiar encoder path, side-by-side comparisons between RGB and multispectral Sentinel-2 setups, or a single family that supports both pooled vectors and token-grid outputs.

The two variants are not interchangeable apart from channel count. Their preprocessing paths, runtime loading logic, and representation details differ enough that checkpoint and preprocessing settings should be treated as part of the experiment definition. As elsewhere in this docs set, `grid` refers to model token layout rather than georeferenced pixel space.

---

## Shared Output Semantics

### `OutputSpec.pooled()`

Both variants support token pooling with `mean` or `max`. The RGB path typically records `patch_mean` or `patch_max` in metadata, while `satmaepp_s2_10b` usually records `group_tokens_mean` or `group_tokens_max` to reflect its grouped-token runtime.

### `OutputSpec.grid()`

`satmaepp` returns a standard ViT patch-token grid `(D,H,W)`. `satmaepp_s2_10b` first reduces grouped tokens across channel groups and then reshapes the result to `(D,H,W)`. In both cases, the output is model token layout rather than a georeferenced raster grid.

---

## Variant A: `satmaepp` (RGB)

### Input Contract

Default `SensorSpec`:

The RGB variant defaults to `collection="COPERNICUS/S2_SR_HARMONIZED"`, `bands=("B4","B3","B2")`, `scale_m=10`, `cloudy_pct=30`, and `composite="median"`.

`input_chw` contract:

`input_chw` must be 3-channel `CHW` in `(B4,B3,B2)` order, and the adapter expects raw Sentinel-2 SR values in `0..10000`.

### Preprocessing Pipeline

<pre class="pipeline-flow"><code><span class="pipeline-root">INPUT</span>  provider fetch / input_chw
  <span class="pipeline-arrow">-&gt;</span> RGB uint8 patch
     <span class="pipeline-detail">input_chw path: raw SR -&gt; [0,1] -&gt; uint8</span>
  <span class="pipeline-arrow">-&gt;</span> SatMAE++ fMoW eval preprocess
     <span class="pipeline-branch">channel_order:</span> rgb | bgr
     <span class="pipeline-detail">ToTensor -&gt; Normalize(mean/std) -&gt; Resize(short side) -&gt; CenterCrop(image_size)</span>
  <span class="pipeline-arrow">-&gt;</span> forward_encoder(mask_ratio=0.0)
  <span class="pipeline-arrow">-&gt;</span> output projection
     <span class="pipeline-branch">pooled:</span> token pooling
     <span class="pipeline-branch">grid:</span>   patch-token reshape</code></pre>

### Key Environment Variables

| Env var                           | Effect                                   |
| --------------------------------- | ---------------------------------------- |
| `RS_EMBED_SATMAEPP_ID`            | HF model ID / checkpoint selector        |
| `RS_EMBED_SATMAEPP_IMG`           | Eval image size                          |
| `RS_EMBED_SATMAEPP_CHANNEL_ORDER` | `rgb` or `bgr` preprocessing order       |
| `RS_EMBED_SATMAEPP_BGR`           | Legacy BGR toggle                        |
| `RS_EMBED_SATMAEPP_FETCH_WORKERS` | Provider prefetch workers for batch APIs |
| `RS_EMBED_SATMAEPP_BATCH_SIZE`    | Inference batch size for batch APIs      |

### Common Failure Modes

- wrong `input_chw` shape or band order
- checkpoint preprocessing mismatch because `CHANNEL_ORDER` changed
- missing `rshf` / SatMAE++ wrapper dependencies
- unexpected token shape causing grid reshape failures

---

## Variant B: `satmaepp_s2_10b` (Sentinel-2 10-band)

### Input Contract

Default `SensorSpec`:

The 10-band variant defaults to `collection="COPERNICUS/S2_SR_HARMONIZED"`, `bands=("B2","B3","B4","B5","B6","B7","B8","B8A","B11","B12")`, `scale_m=10`, `cloudy_pct=30`, `composite="median"`, and `fill_value=0.0`.

Strict requirements:

This path is stricter than the RGB path: `sensor.bands` must exactly match the 10-band order above, `input_chw` must be 10-channel `CHW`, and the adapter expects raw Sentinel-2 SR values in `0..10000`.

### Preprocessing + Runtime Loading

<pre class="pipeline-flow"><code><span class="pipeline-root">INPUT</span>  provider fetch / input_chw
  <span class="pipeline-arrow">-&gt;</span> 10-band CHW
  <span class="pipeline-arrow">-&gt;</span> source-style Sentinel stats mapping to uint8
     <span class="pipeline-detail">mean ± 2*std stretch</span>
  <span class="pipeline-arrow">-&gt;</span> eval transforms
     <span class="pipeline-detail">ToTensor -&gt; Resize(short side) -&gt; CenterCrop(image_size)</span>
  <span class="pipeline-arrow">-&gt;</span> load runtime weights + vendored grouped-channel runtime
  <span class="pipeline-arrow">-&gt;</span> construct grouped model
     <span class="pipeline-detail">channel groups: ((0,1,2,6),(3,4,5,7),(8,9))</span>
  <span class="pipeline-arrow">-&gt;</span> forward_encoder(mask_ratio=0.0)
  <span class="pipeline-arrow">-&gt;</span> grouped-token reduction
     <span class="pipeline-branch">pooled:</span> reduce grouped tokens to vector
     <span class="pipeline-branch">grid:</span>   reduce + reshape patch grid</code></pre>

### Key Environment Variables

| Env var                              | Effect                                   |
| ------------------------------------ | ---------------------------------------- |
| `RS_EMBED_SATMAEPP_S2_CKPT_REPO`     | Checkpoint repo/source                   |
| `RS_EMBED_SATMAEPP_S2_CKPT_FILE`     | Checkpoint filename                      |
| `RS_EMBED_SATMAEPP_S2_MODEL_FN`      | Model constructor name                   |
| `RS_EMBED_SATMAEPP_S2_IMG`           | Eval image size                          |
| `RS_EMBED_SATMAEPP_S2_PATCH`         | Patch size                               |
| `RS_EMBED_SATMAEPP_S2_GRID_REDUCE`   | Group reduction mode for grid output     |
| `RS_EMBED_SATMAEPP_S2_WEIGHTS_ONLY`  | Weights-only checkpoint loading toggle   |
| `RS_EMBED_SATMAEPP_S2_FETCH_WORKERS` | Provider prefetch workers for batch APIs |
| `RS_EMBED_SATMAEPP_S2_BATCH_SIZE`    | Inference batch size for batch APIs      |

### Common Failure Modes

- `sensor.bands` order differs from the strict expected 10-band layout
- vendored runtime import fails or checkpoint download is unavailable
- grouped-token reshape assumptions do not match the loaded checkpoint/config
- `GRID_REDUCE` changes representation semantics across experiments

---

## Examples

### Minimal pooled examples

```python
from rs_embed import get_embedding, PointBuffer, TemporalSpec, OutputSpec

spatial = PointBuffer(lon=121.5, lat=31.2, buffer_m=2048)
temporal = TemporalSpec.range("2022-06-01", "2022-09-01")

emb_rgb = get_embedding(
    "satmaepp",
    spatial=spatial,
    temporal=temporal,
    output=OutputSpec.pooled(),
    backend="gee",
)

emb_s2 = get_embedding(
    "satmaepp_s2_10b",
    spatial=spatial,
    temporal=temporal,
    output=OutputSpec.pooled(),
    backend="gee",
)
```

### Example tuning knobs (env-controlled)

```python
# RGB variant:
# export RS_EMBED_SATMAEPP_ID=...
# export RS_EMBED_SATMAEPP_CHANNEL_ORDER=rgb
#
# S2-10B variant:
# export RS_EMBED_SATMAEPP_S2_IMG=224
# export RS_EMBED_SATMAEPP_S2_GRID_REDUCE=mean
```

### Example with variant selection

```python
from rs_embed import get_embedding, PointBuffer, TemporalSpec, OutputSpec

spatial = PointBuffer(lon=121.5, lat=31.2, buffer_m=2048)
temporal = TemporalSpec.range("2022-06-01", "2022-09-01")

emb_s2 = get_embedding(
    "satmaepp_s2_10b",
    spatial=spatial,
    temporal=temporal,
    output=OutputSpec.grid(),
    backend="gee",
    variant="large",
)
```

For export jobs, the same setting goes through
`ExportModelRequest.configure("satmaepp_s2_10b", variant="large")`.

---

## Reproducibility Notes

For reproducibility, record which variant you used, the checkpoint source, image size, patch size, channel or group reduction settings, temporal window, provider compositing settings, output mode, and pooling choice.

---

## Source of Truth (Code Pointers)

The relevant code paths are `src/rs_embed/embedders/catalog.py`, `src/rs_embed/embedders/onthefly_satmaepp.py`, and `src/rs_embed/embedders/onthefly_satmaepp_s2.py`.
