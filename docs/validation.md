# Validation and current limits

On **2026-10-13**, all **16 image encoders** and **SatCLIP** completed a real
pretrained forward pass on CPU. **GeoCLIP and Esri GLE** passed real-checkpoint tests,
and **AlphaEarth / GSE** passed a live Google Cloud Storage point query.
This gives **20 PASS / 2 BLOCKED** across the 22-entry software catalog.
Tessera and Copernicus remain **blocked in the checked environments**;
they are not advertised as having passed pretrained inference or product access.

These are software smoke checks, **not scientific benchmark results**. Synthetic
imagery is suitable for checking checkpoint loading, tensor handling, and finite
outputs; it says nothing about representation quality, accuracy, or generalization.
Additional integrations do not change the paper's frozen 20-system benchmark.

## Comparison gallery and unified API checks

The [22-model gallery](tutorials/model-comparison.md) adds a different evidence
layer: 19 retained historical Wuhan image/product outputs, plus fresh SatCLIP,
GeoCLIP and Esri GLE coordinate inference. It does **not** turn the blocked live
Tessera/Copernicus access checks below into passes. Dates and spatial support
differ; the historical SatVision proxy input is labeled, and the coarse Copernicus
window is displayed without duplicating overlapping product cells.

The new `compare_embeddings` CLI was also [executed with real weights](validation/comparison-api.json) for all
three location encoders on CPU, with identical 320 m query settings. It returned
672 coordinate samples per model and saved real feature arrays, a combined PNG,
and a run report. The [comparison notebook receipt](validation/comparison-notebook.json)
records its separate 5 km, three-model execution; full 22-model extraction in
that notebook remains an optional, unexecuted cell.

Regression checks for this change passed on Windows/Python 3.13
(774 passed, 1 skipped) and Linux/Python 3.12 (773 passed, 2 skipped).
Tests cover shared location sampling, finite spacing and size limits, explicit
failure reports, per-model dates, visualization shapes, and offline resource
discovery. [Gallery source hashes and provenance](assets/comparison/provenance.json)
document the displayed data independently of those interface tests.

## Per-model evidence

PASS means a real pretrained output or real product array was returned and checked
for shape, nonempty values, and finiteness. BLOCKED means an external dependency,
data access, or bounded runtime prevented that check. Interface tests and mocks do
not qualify as a real inference PASS.

| Canonical ID | Family | Result | Observed output | Checked path / remaining limitation |
| --- | --- | --- | --- | --- |
| `remoteclip` | A1 | **PASS** | `(768,)` | Cached official weights; supplied-pixel helper; patch-mean output |
| `satmae` | A1 | **PASS** | `(1024,)` | Cached official weights; synthetic 3-band input |
| `satmaepp` | A1 | **PASS** | `(1024,)` | Cached official weights; synthetic 3-band input |
| `scalemae` | A1 | **PASS** | `(1024,)` | Official binary checkpoint; strict loading with modern Hub compatibility fallback |
| `wildsat` | A1 | **PASS** | `(256,)` | Cached published checkpoint; synthetic 3-band input |
| `satmaepp_s2_10b` | A2 | **PASS** | `(1024,)` | Explicit locally cached official Sentinel checkpoint; supplied-pixel helper |
| `prithvi` | A2 | **PASS** | `(768,)` | Default EO v2 100M TL weights; synthetic 6-band input |
| `terramind` | A2 | **PASS** | `(384,)` | Default small checkpoint; synthetic 12-band input |
| `terrafm` | A2 | **PASS** | `(768,)` | Default base checkpoint; synthetic S2 input |
| `satvision` | A2 | **PASS** | `(4096,)` | Published giant checkpoint; adapter preprocessing and pooled output |
| `dofa` | A3 | **PASS** | `(768,)` | Official checkpoint; default multispectral schema |
| `fomo` | A3 | **PASS** | `(768,)` | Cached published checkpoint; default band schema |
| `thor` | A3 | **PASS** | `(768,)` | THOR 1.0 base checkpoint; default band schema |
| `galileo` | A4 | **PASS** | `(128,)` | Cached checkpoint; independent synthetic temporal frames |
| `anysat` | A4 | **PASS** | `(768,)` | Cached checkpoint; independent synthetic temporal frames |
| `agrifm` | A4 | **PASS** | `(1024,)` | Cached AgriFM checkpoint; independent synthetic temporal frames |
| `satclip` | B | **PASS** | `(256,)` | Default ViT16-L40 location branch; coordinate query |
| `geoclip` | B, added integration | **PASS** | `(3, 512)` | Official GeoCLIP 1.2.3 bundled weights; numerical comparison to upstream |
| `esri_gle` | B, added integration | **PASS** | `(7, 256)` | Official 2.17 MB Esri weights; direct CPU inference; exact numerical match to official mathematical implementation |
| `gse` / AEF | C1 | **PASS — GCS** | `(1, 64)` | Live official 2021 Wuhan pixel; legacy Earth Engine path not validated here |
| `tessera` | C1 | **BLOCKED** | — | Cached registry present; official service reported no route to host; 60 s bound reached before an array returned |
| `copernicus` | C1 | **BLOCKED** | — | Local product GeoTIFF absent; see the product access receipt for the bounded download attempt |

The output widths above are **the observed configured outputs**, not universal
dimensions for every variant or pooling choice. For example, RemoteCLIP's patch
features differ from its projected image embedding.

Machine-readable evidence: [22-model matrix](validation/model-validation-20261013.json)
and [live AEF GCS receipt](validation/aef-gcs-20261013.json), plus the
[Esri real-weight receipt](validation/esri-gle-20261013.json). The public matrix records
the latest completed result, bounded failures, input/output hashes, runtime versions,
and reproducible settings without publishing local host paths or raw runtime logs.
Earlier failures were retained privately and superseded only after successful real
reruns. Product SDKs control their own network connections independently of the
runner's Hugging Face offline switch.

## Reproduce a real-weight smoke check

Use an environment containing the relevant model dependencies and official cached
weights. The checked Linux environment used Python 3.12.2, PyTorch 2.12.0+cu130,
Transformers 5.9.0, timm 1.0.15, and four CPU threads. GPU visibility was disabled
for these runs. This records an environment that passed; it is not a claim that
every optional model works with every possible dependency combination.

```bash
python scripts/validate_models.py --model remoteclip --model satclip --timeout 180
```

The runner uses a deterministic seed (`20261013`), raw input values in `[500, 4500]`,
the declared band order, and 64 × 64 supplied pixels before the model's own
preprocessing. A4 models receive distinct frames, rather than a repeated static
image. The geographic metadata is a 320 m radius around `(114.35, 30.50)`, with
the 2021 calendar year. Full input hashes, shapes, metadata, versions, durations,
and output hashes are retained in the receipts. Each model runs in a fresh process
with a 180 s default bound, releasing its model memory when it exits.

Hugging Face and Esri GLE runs are cache-only by default. Add `--allow-network` to
allow their checkpoint downloads. Real product queries require `--include-products`; their SDKs may contact
their official endpoints. Product checks are not synthetic inference:

```bash
python scripts/validate_models.py --model tessera --model copernicus \
  --include-products --allow-network --timeout 60
```

Copernicus uses a 0.5° bounding box in the current runner, because its native grid
is 0.25° and a 640 m ROI cannot satisfy its pixel-selection contract. For an already
downloaded file, set `RS_EMBED_COP_DIR`; for a retained GeoTessera cache, set
`RS_EMBED_TESSERA_CACHE`. No cache was fabricated from scientific result vectors.
For the verified AEF path, see [direct Google Cloud Storage access](data-access.md).

The SatMAE++ Sentinel smoke used the existing downloaded checkpoint through
`RS_EMBED_SATMAEPP_S2_CKPT_FILE`. Supply your own local official checkpoint path when
the default Hub reference cannot be resolved; no randomly initialized model is
substituted. The final ScaleMAE pass used its canonical Hub ID and cached
`pytorch_model.bin`, with strict parameter matching.

## GeoCLIP and Esri details

GeoCLIP used official `geoclip==1.2.3` on local CPU / Python 3.13.12. Three points
(Wuhan, Tokyo, New York) produced distinct finite vectors. The maximum absolute
difference from the upstream `LocationEncoder` was `2.60770320892334e-08`, within
`rtol=atol=1e-5`. The official bundled checkpoint SHA-256 was
`94b80ae3af89fca78539e129dd2929d321247f5ceeeb0a31bc2c31041a253394`.

Esri GLE now loads the official `satclip.pth` directly with PyTorch and the
MIT-licensed SatCLIP architecture. The checkpoint has 541,440 parameters and
occupies 2,168,415 bytes. Its SHA-256 is
`2d5b8ac88b4a7f210a00f7fbe145f5216987f373062ec71f3065f9ba13b15452`.
Seven coordinates, including Wuhan, Tokyo, New York, Sydney, the equator and
both poles, produced finite vectors on Linux CPU. The output matched the official
package's mathematical classes with maximum absolute difference **0.0** after
float32 conversion. This reference check covers the location model, not ArcGIS
feature-class conversion or ArcGIS Pro integration.

The run explicitly blocked ArcGIS and ArcPy imports. It verified a fresh official
download, cached `.pth` and explicit `.dlpk` use with network calls blocked,
batch sizes 1/3/1024, a pooled point and a north-up `(256, 3, 2)` query grid.
The earlier ArcGIS SDK import failure was an unnecessary integration dependency;
the lightweight path supersedes that attempt. See the
[Esri setup guide](models/esri_gle.md) for offline and cache options.

```bash
python scripts/validate_models.py --model esri_gle --allow-network --timeout 60
```

## Regression and compatibility checks

The full Linux release suite passed; the [unit-test receipt](validation/unit-tests-20261013.json)
records the exact final count, skipped tests, versions, and elapsed time. Targeted
checks for the ScaleMAE binary fallback also passed 2 tests. Tests using substitutes
verify contracts only and are kept separate from the real-weight results above.

This work also fixed five adapters that previously initialized an imagery provider
even when pixels were supplied: RemoteCLIP, Prithvi, DOFA, TerraMind, and TerraFM.
The no-provider regression reproduced five failures before the fix and passed
afterward. The new `get_image_embedding` helper has 16 contract tests, with real
pretrained helper calls additionally verified for RemoteCLIP, ScaleMAE, and
SatMAE++ Sentinel. The helper requires the spatial/time context and preserves
raw sensor preprocessing inside each model adapter.

Remaining scope: authenticated Earth Engine data access, Esri GPU inference,
Tessera/Copernicus product access in a connected data environment, additional
checkpoint variants, all grid/batch combinations, and downstream scientific
performance have not all been validated by this smoke pass.
