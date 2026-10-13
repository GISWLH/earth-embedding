# DOFA (`dofa`)

> DOFA adapter for multispectral inputs with explicit per-channel wavelengths, supporting provider and tensor backends.

## Quick Facts

| Field                             | Value                                                         |
| --------------------------------- | ------------------------------------------------------------- |
| Model ID                          | `dofa`                                                        |
| Family / Backbone                 | DOFA ViT (`base` / `large`, official checkpoints)             |
| Adapter type                      | `on-the-fly`                                                  |
| Typical backend                   | provider backend (`gee`), also supports `backend="tensor"`    |
| Primary input                     | Raw Sentinel-2 SR CHW + wavelengths (µm)                      |
| Default resolution                | 10m default provider fetch (`sensor.scale_m`)                 |
| Temporal mode                     | provider path requires `TemporalSpec.range(...)`              |
| Output modes                      | `pooled`, `grid`                                              |
| Model config keys                 | `variant` (default: `base`; choices: `base`, `large`)         |
| Extra side inputs                 | **required** wavelength vector (`wavelengths_um`)             |
| Training alignment (adapter path) | Medium-High (when wavelengths and band semantics are correct) |

---

## When To Use This Model

DOFA is the right choice when wavelength-aware multispectral modeling matters, when you need custom band combinations with matching wavelengths, or when you want to compare spectral models against more S2-specific adapters. The main failure mode is semantic mismatch: missing wavelengths, wrong wavelength-to-channel alignment, or unlogged changes to `variant` and wavelength configuration will all make results hard to trust.

---

## Input Contract (Current Adapter Path)

### Spatial / temporal

The provider path requires `TemporalSpec.range(start, end)`. The tensor path bypasses provider fetch entirely, so temporal semantics only matter insofar as they shaped the tensor you prepared.

### Sensor / channels (provider path)

If `sensor` is omitted, the provider path uses `COPERNICUS/S2_SR_HARMONIZED` with the official DOFA S2 9-band order `B4,B3,B2,B5,B6,B7,B8,B11,B12`, plus `scale_m=10`, `cloudy_pct=30`, `composite="median"`, and `fill_value=0.0`.

Wavelengths:

The adapter requires one wavelength in micrometers per channel. If `sensor.wavelengths` is not provided, it tries to infer wavelengths from `sensor.bands`, but only known schemas such as the supported Sentinel-2 subsets are inferable. `len(wavelengths_um)` must always match the channel count `C`.

`input_chw` contract (provider override path):

If you override fetch with `input_chw`, it must be `CHW` with `C == len(bands)` and raw SR values in `0..10000`.

### Tensor backend contract

For `backend="tensor"`, `input_chw` must be `CHW`, and batch tensor usage should go through `get_embeddings_batch_from_inputs(...)`. `sensor.bands` is required so the official preprocessing path can be applied, and `sensor.wavelengths` should either be provided directly or be inferable from the bands. The tensor is expected to hold raw SR values in `0..10000`, not pre-normalized `[0,1]`.

---

## Preprocessing Pipeline (Current rs-embed Path)

### Provider path

<pre class="pipeline-flow"><code><span class="pipeline-root">PROVIDER</span>  fetch raw multiband Sentinel-2 SR patch
  <span class="pipeline-arrow">-&gt;</span> optional raw-value inspection
     <span class="pipeline-detail">expected_channels=len(bands), value range [0,10000]</span>
  <span class="pipeline-arrow">-&gt;</span> raw SR 0..10000 -&gt; 0..255-like scale
  <span class="pipeline-arrow">-&gt;</span> official DOFA S2 per-band mean/std normalization
  <span class="pipeline-arrow">-&gt;</span> resize to fixed 224x224
     <span class="pipeline-detail">bilinear; no crop / pad</span>
  <span class="pipeline-arrow">-&gt;</span> load DOFA model variant
     <span class="pipeline-branch">variant:</span> base | large
  <span class="pipeline-arrow">-&gt;</span> forward(image, wavelengths)
  <span class="pipeline-arrow">-&gt;</span> output projection
     <span class="pipeline-branch">pooled:</span> embedding vector
     <span class="pipeline-branch">grid:</span>   patch-token grid</code></pre>

### Tensor path

<pre class="pipeline-flow"><code><span class="pipeline-root">TENSOR</span>  read raw SR input_chw
  <span class="pipeline-arrow">-&gt;</span> reject already-normalized [0,1]-like inputs
  <span class="pipeline-arrow">-&gt;</span> apply provider-equivalent DOFA preprocessing
     <span class="pipeline-detail">raw SR 0..10000 -&gt; [0,1]</span>
     <span class="pipeline-detail">rescale to 0..255-like values</span>
     <span class="pipeline-detail">official per-band mean/std normalization</span>
  <span class="pipeline-arrow">-&gt;</span> resize to fixed 224x224
  <span class="pipeline-arrow">-&gt;</span> resolve wavelengths
     <span class="pipeline-branch">preferred:</span> sensor.wavelengths
     <span class="pipeline-branch">fallback:</span>  infer from sensor.bands
  <span class="pipeline-arrow">-&gt;</span> forward(image, wavelengths)
  <span class="pipeline-arrow">-&gt;</span> output projection
     <span class="pipeline-branch">pooled:</span> embedding vector
     <span class="pipeline-branch">grid:</span>   patch-token grid</code></pre>

Fixed adapter behavior:

The current implementation fixes image size at `224`, and the official preprocessing path is defined for Sentinel-2 subsets of `B4,B3,B2,B5,B6,B7,B8,B11,B12`.

---

## Environment Variables / Tuning Knobs

| Env var                       | Default            | Effect                                              |
| ----------------------------- | ------------------ | --------------------------------------------------- |
| `RS_EMBED_DOFA_FETCH_WORKERS` | `8`                | Provider prefetch workers for batch APIs            |
| `RS_EMBED_DOFA_BATCH_SIZE`    | CPU:`8`, CUDA:`64` | Inference batch size for batch APIs                 |
| `RS_EMBED_DOFA_BASE_WEIGHTS`  | unset              | Local override for the base checkpoint file         |
| `RS_EMBED_DOFA_LARGE_WEIGHTS` | unset              | Local override for the large checkpoint file        |
| `RS_EMBED_DOFA_WEIGHTS_DIR`   | unset              | Directory override containing DOFA checkpoint files |
| `RS_EMBED_DOFA_HF_REPO_ID`    | `earthflow/DOFA`   | Hugging Face repo used for checkpoint download      |
| `RS_EMBED_DOFA_HF_REVISION`   | `main`             | Hugging Face revision used for checkpoint download  |

Non-env model selection knobs:

The main non-env knobs are `variant` (`base` or `large`), `sensor.bands` for channel semantics and wavelength inference, and `sensor.wavelengths` for an explicit wavelength vector in micrometers.

If `variant` is omitted, rs-embed uses the `base` DOFA checkpoint by default. Pass `variant="large"` to switch to the larger model.

Quick reminder:

Pass `variant` directly to `get_embedding("dofa", ..., variant="base")`. For export jobs, use `ExportModelRequest.configure("dofa", variant="large")`.

---

## Output Semantics

DOFA mostly follows the standard pooled and token-grid pattern. `pooled` returns a vector `(D,)`, while `grid` reshapes patch tokens to `(D,H,W)` in model token space rather than georeferenced raster space. The model-specific part is mainly in metadata, which records wavelengths, variant choice, and preprocessing details.

---

## Examples

### Minimal provider-backed example (S2 wavelengths inferred automatically)

```python
from rs_embed import get_embedding, PointBuffer, TemporalSpec, OutputSpec

emb = get_embedding(
    "dofa",
    spatial=PointBuffer(lon=121.5, lat=31.2, buffer_m=2048),
    temporal=TemporalSpec.range("2022-06-01", "2022-09-01"),
    output=OutputSpec.pooled(),
    backend="gee",
)
```

### Switch to the large checkpoint

```python
from rs_embed import get_embedding, PointBuffer, TemporalSpec, OutputSpec

emb = get_embedding(
    "dofa",
    spatial=PointBuffer(lon=121.5, lat=31.2, buffer_m=2048),
    temporal=TemporalSpec.range("2022-06-01", "2022-09-01"),
    output=OutputSpec.pooled(),
    backend="gee",
    variant="large",
)
```

### Custom bands / wavelengths example (conceptual)

```python
from rs_embed import SensorSpec

sensor = SensorSpec(
    collection="COPERNICUS/S2_SR_HARMONIZED",
    bands=("B2", "B3", "B4", "B8"),
    scale_m=10,
)
# If bands are non-standard, provide wavelengths explicitly via an extended sensor object/field used by your code path.
```

---

## Common Failure Modes / Debugging

- provider path called with non-`range` temporal spec
- wavelength vector missing or wrong length for channel count
- unsupported bands for the official S2 preprocessing path
- tensor backend called with already-normalized `[0,1]` inputs
- tensor backend called without `input_chw`
- unknown `variant` (must be `base` or `large`)

Recommended first checks:

Print or log the exact `bands` and `wavelengths_um` used by the adapter, then verify that the provider or tensor input is scaled and ordered the way you intended before blaming the model.

---

## Reproducibility Notes

Keep the `variant`, exact `bands`, exact `wavelengths_um`, temporal window and compositing policy, output mode, and backend choice fixed and recorded. Those settings materially change what DOFA sees.

---

## Source of Truth (Code Pointers)

The main code paths are `src/rs_embed/embedders/catalog.py` for registration and `src/rs_embed/embedders/onthefly_dofa.py` for both adapter logic and wavelength inference.
