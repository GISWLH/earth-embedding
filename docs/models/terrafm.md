# TerraFM-B (`terrafm`)

> TerraFM-B adapter supporting both provider and tensor backends, with two input modalities (`s2` 12-band Sentinel-2 SR or `s1` VV/VH Sentinel-1) and model-native feature-map grids.

## Quick Facts

| Field                             | Value                                                                                                   |
| --------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Model ID                          | `terrafm`                                                                                               |
| Aliases                           | `terrafm_b`                                                                                             |
| Family / Backbone                 | TerraFM-B from Hugging Face (`MBZUAI/TerraFM`)                                                          |
| Adapter type                      | `on-the-fly`                                                                                            |
| Typical backend                   | provider backend (`gee`), also supports `backend="tensor"`                                              |
| Primary input                     | S2 SR 12-band or S1 VV/VH (selected by `sensor.modality`)                                               |
| Default resolution                | 10m default provider fetch (`sensor.scale_m`)                                                           |
| Temporal mode                     | provider path requires `TemporalSpec.range(...)` (v0.1 behavior)                                        |
| Output modes                      | `pooled`, `grid`                                                                                        |
| Extra side inputs                 | modality settings on `sensor` (`modality`, `use_float_linear`, `s1_require_iw`, `s1_relax_iw_on_empty`) |
| Training alignment (adapter path) | Medium-High when modality-specific preprocessing matches the intended TerraFM path                      |

---

## When To Use This Model

TerraFM is most useful when you want to compare S2 and S1 representations within one backbone family, switch between provider fetch and direct tensor inputs, or work with model-native feature-map grids instead of token-only grids. The main things to watch are modality drift between S1 and S2 runs, wrong tensor channel counts, and the mistaken assumption that `backend="auto"` selects something other than the provider-backed path.

---

## Input Contract (Current Adapter Path)

### Backend modes

`backend="tensor"` requires `input_chw` as `CHW`, batch tensor usage should go through `get_embeddings_batch_from_inputs(...)`, and the adapter resizes inputs to `224`. The provider-backed path, including `backend="auto"`, requires `TemporalSpec.range(...)` in v0.1 and fetches either S2 or S1 according to `modality` or `sensor.modality`.

### Modality selection (`modality` or `sensor.modality`)

For `s2`, which is the default, TerraFM expects 12-band Sentinel-2 SR input `B1,B2,B3,B4,B5,B6,B7,B8,B8A,B9,B11,B12`. Provider fetch normalizes that path to `[0,1]`, while an `input_chw` override should still carry raw SR values in `0..10000` so the adapter can apply the same scaling.

For `s1`, TerraFM expects two-band Sentinel-1 `VV` and `VH`. The provider path fetches raw VV/VH and normalizes it with the shared S1 helper. An `input_chw` override is expected to carry raw VV/VH so the adapter can apply the same `log1p` plus percentile scaling path.

### Sensor fields used by adapter (provider path)

The common provider-side sensor fields are `scale_m`, `cloudy_pct`, and `composite`. On the S1 path, TerraFM also uses `use_float_linear`, `s1_require_iw`, and `s1_relax_iw_on_empty`.

Channel sanity:

TerraFM is strict about channel count: `C` must be `12` for S2 or `2` for S1.

---

## Preprocessing Pipeline (Current rs-embed Path)

### What the original TerraFM model assumes for S1

TerraFM treats Sentinel-1 as a 2-channel input branch (`VV`, `VH`). The official model code routes the S1 path by channel count (`C == 2`). The TerraFM paper describes S1 pretraining data as Sentinel-1 RTC patches, so the strongest original assumption is dual-pol `VV/VH` plus an analysis-ready S1 product, not a hard-coded `IW` rule.

### Why rs-embed prefers `IW` on GEE

Earth Engine Sentinel-1 collections are heterogeneous: different instrument modes, coverage patterns, and product characteristics can appear in the same collection. rs-embed therefore prefers `IW` by default as a conservative proxy for a more homogeneous land-observation subset when approximating TerraFM's S1 training distribution from `COPERNICUS/S1_GRD_FLOAT` / `COPERNICUS/S1_GRD`. This `IW` preference is an adapter policy, not a TerraFM paper requirement.

### S1 fetch options in rs-embed

With `s1_require_iw=True`, rs-embed first tries `instrumentMode == "IW"` together with dual-pol `VV/VH`. If `s1_relax_iw_on_empty=True`, a strict `IW` miss triggers one retry without the `IW` filter. With `s1_require_iw=False`, the adapter queries dual-pol `VV/VH` directly and does not enforce `IW`.

Metadata behavior:

When provider-backed S1 fetch succeeds, metadata records `s1_iw_requested`, `s1_iw_applied`, `s1_iw_relaxed_on_empty`, and `s1_relax_iw_on_empty`, so you can tell whether a sample came from strict `IW` filtering or from the relaxed fallback path.

### Provider path

<pre class="pipeline-flow"><code><span class="pipeline-root">PROVIDER</span>  validate TemporalSpec.range(...)
  <span class="pipeline-arrow">-&gt;</span> select modality
     <span class="pipeline-branch">s2:</span> 12-band Sentinel-2 SR
     <span class="pipeline-branch">s1:</span> dual-pol Sentinel-1 VV/VH
  <span class="pipeline-arrow">-&gt;</span> provider fetch + modality-specific normalization
     <span class="pipeline-branch">s2:</span> raw SR -&gt; [0,1]
     <span class="pipeline-branch">s1:</span> prefer IW -&gt; optional relaxed retry -&gt; shared S1 normalization -&gt; [0,1]
  <span class="pipeline-arrow">-&gt;</span> optional inspection on normalized input
  <span class="pipeline-arrow">-&gt;</span> resize to fixed 224x224
  <span class="pipeline-arrow">-&gt;</span> load TerraFM-B runtime + HF weights
  <span class="pipeline-arrow">-&gt;</span> forward / feature extraction
     <span class="pipeline-branch">pooled:</span> TerraFM CLS embedding (D,)
     <span class="pipeline-branch">grid:</span>   extract_feature(...) last-layer map (D,H,W)</code></pre>

### Tensor backend path

<pre class="pipeline-flow"><code><span class="pipeline-root">TENSOR</span>  read input_chw
  <span class="pipeline-arrow">-&gt;</span> validate channel count
     <span class="pipeline-branch">s2:</span> 12 channels
     <span class="pipeline-branch">s1:</span> 2 channels
  <span class="pipeline-arrow">-&gt;</span> apply provider-equivalent modality normalization
     <span class="pipeline-branch">s2:</span> raw SR 0..10000 -&gt; /10000 -&gt; clip [0,1]
     <span class="pipeline-branch">s1:</span> shared VV/VH normalization helper
     <span class="pipeline-detail">log1p + percentile scaling</span>
  <span class="pipeline-arrow">-&gt;</span> resize to fixed 224x224
  <span class="pipeline-arrow">-&gt;</span> load TerraFM-B
  <span class="pipeline-arrow">-&gt;</span> run same forward / grid extraction path
     <span class="pipeline-branch">pooled:</span> TerraFM CLS embedding
     <span class="pipeline-branch">grid:</span>   extract_feature(...) last-layer map</code></pre>

Notes:

The tensor backend does apply the adapter's modality-specific normalization. In practice, `input_chw` should still be raw S2 SR values for `s2`, or raw Sentinel-1 `VV/VH` values for `s1`, so that the tensor path matches the provider path semantics.

---

## Environment Variables / Tuning Knobs

| Env var                          | Default            | Effect                                   |
| -------------------------------- | ------------------ | ---------------------------------------- |
| `RS_EMBED_TERRAFM_FETCH_WORKERS` | `8`                | Provider prefetch workers for batch APIs |
| `RS_EMBED_TERRAFM_BATCH_SIZE`    | CPU:`8`, CUDA:`64` | Inference batch size for batch APIs      |

Related cache envs (used by HF asset download path):

The related Hugging Face cache environment variables are `HUGGINGFACE_HUB_CACHE`, `HF_HOME`, and `HUGGINGFACE_HOME`.

Adapter behavior notes:

Image size is fixed at `224` in the current implementation, the runtime code is vendored inside `rs-embed`, and weights are fetched from `MBZUAI/TerraFM` as `TerraFM-B.pth`. Although the vendored runtime also exposes a `large` factory, the current adapter only wires up the TerraFM-B weight path, so variant switching is not exposed yet.

---

## Output Semantics

### `OutputSpec.pooled()`

`OutputSpec.pooled()` returns TerraFM's own pooled forward output `(D,)`. This is not token pooling; it is the model's pooled embedding path.

### `OutputSpec.grid()`

`OutputSpec.grid()` returns the last-layer TerraFM feature map via `extract_feature(...)` as `xarray.DataArray` `(D,H,W)`. Metadata includes `grid_type="feature_map"`. This is model feature-map layout, not georeferenced raster pixels.

---

## Examples

### Minimal provider-backed S2 example

```python
from rs_embed import get_embedding, PointBuffer, TemporalSpec, OutputSpec

emb = get_embedding(
    "terrafm",
    spatial=PointBuffer(lon=121.5, lat=31.2, buffer_m=2048),
    temporal=TemporalSpec.range("2022-06-01", "2022-09-01"),
    modality="s2",
    output=OutputSpec.pooled(),
    backend="gee",
)
```

### Minimal provider-backed S1 example

```python
from rs_embed import get_embedding, PointBuffer, TemporalSpec, OutputSpec, SensorSpec

sensor = SensorSpec(
    collection="COPERNICUS/S1_GRD_FLOAT",
    bands=("VV", "VH"),
    scale_m=10,
    composite="median",
    use_float_linear=True,
    s1_require_iw=True,
    s1_relax_iw_on_empty=True,
)

emb = get_embedding(
    "terrafm",
    spatial=PointBuffer(lon=121.5, lat=31.2, buffer_m=2048),
    temporal=TemporalSpec.range("2022-06-01", "2022-09-01"),
    sensor=sensor,
    modality="s1",
    output=OutputSpec.pooled(),
    backend="gee",
)
```

Notes:

Prefer passing `modality="s1"` or `modality="s2"` directly at the public API layer. Setting `modality="s1"` is what actually switches TerraFM onto the S1 path; changing only `collection` or `bands` is not enough. `use_float_linear=True` matches `COPERNICUS/S1_GRD_FLOAT`, while `False` matches `COPERNICUS/S1_GRD`. The conservative default is `s1_require_iw=True`, and `s1_relax_iw_on_empty=True` keeps that strict path but retries without `IW` if the strict query is empty. For maximum reproducibility, keep `s1_require_iw=True` and set `s1_relax_iw_on_empty=False`.

---

## Common Failure Modes / Debugging

- using an unsupported backend; use `backend="auto"`, an explicit provider backend, or `tensor`
- provider path with non-`range` temporal spec
- tensor backend without `input_chw`
- wrong channel count (`C` must be `2` or `12`)
- S1/S2 modality mismatch between data and `modality`
- strict S1 `IW` filtering returning an empty collection for the chosen AOI / time window
- HF weight download issues (`.pth` weights)

Recommended first checks:

Inspect metadata such as `modality`, `source`, `grid_type`, and weight file info first. On the S1 path, also inspect `s1_iw_requested`, `s1_iw_applied`, and `s1_iw_relaxed_on_empty`. If you are using `backend="tensor"`, verify input scale and normalization before debugging anything else. For a clean baseline, start with the default S2 path before adding S1 overrides.

---

## Reproducibility Notes

Keep the backend mode, modality, S1-specific options, temporal window, compositing settings, output mode, and TerraFM asset snapshot fixed and recorded. Those settings change both the data path and the model path.

---

## Source of Truth (Code Pointers)

The main code paths are `src/rs_embed/embedders/catalog.py` for registration and `src/rs_embed/embedders/onthefly_terrafm.py` for the adapter implementation.
