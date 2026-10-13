<div align="center">
  <img src="docs/assets/earth-embedding-logo.svg" width="96" alt="Earth Embedding logo">

# Earth Embedding

**A shared Python interface for Earth observation images, locations, and embedding products.**

[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md)

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](pyproject.toml)
[![License](https://img.shields.io/badge/Code-Apache--2.0-267b72)](LICENSE)
[![Models](https://img.shields.io/badge/Catalog-22%20adapters-267b72)](docs/models.md)
[![Validation](https://img.shields.io/badge/Validation-evidence%20%26%20limits-d98950)](docs/validation.md)
[![Tests](https://github.com/GISWLH/earth-embedding/actions/workflows/tests.yml/badge.svg)](https://github.com/GISWLH/earth-embedding/actions/workflows/tests.yml)

[Get started](#installation) · [Model catalog](#model-catalog) · [Documentation](docs/index.md) · [Validation](docs/validation.md) · [Contribute](CONTRIBUTING.md)

</div>

> **Origin and attribution.** Earth Embedding is an independently maintained extension of [CyberGIS rs-embed](https://github.com/cybergis/rs-embed), created by Dingqi Ye and contributors. We retain its Apache-2.0 license and acknowledge its APIs, adapters, and engineering foundation. The [upstream paper](https://arxiv.org/abs/2602.23678) describes rs-embed; our manuscript and extensions are separate work. See [provenance](docs/provenance.md).

<picture>
  <source media="(max-width: 760px)" srcset="docs/assets/earth-embedding-hero-mobile.svg">
  <img src="docs/assets/earth-embedding-hero.svg" width="100%" alt="Images, longitude and latitude, and precomputed products connect through Earth Embedding to geospatial analysis workflows.">
</picture>

## Why Earth Embedding?

Remote sensing models expose different inputs, preprocessing rules, spatial supports, and access methods. Earth Embedding makes those differences explicit while providing reusable interfaces for obtaining features. Start with satellite imagery, a list of locations, or an existing embedding product; receive embedding values and provenance metadata for your own analysis.

- **Three entry points:** image encoders, location encoders, and precomputed embedding products, organized by the object a user actually receives.
- **22 catalog entries:** 16 image configurations, 3 location encoders, and 3 precomputed products. The catalog includes optional integrations; consult the validation report for actual execution status.
- **Location-only inference:** SatCLIP, GeoCLIP, and Esri Global Location Encoder share a `[longitude, latitude]` interface. Esri's lightweight weights run directly in PyTorch.
- **Direct AlphaEarth data access:** discover official Google Cloud Storage tiles and sample 64-dimensional vectors without Earth Engine authentication.
- **Reusable outputs:** pooled vectors, supported spatial grids, batch extraction, export helpers, and model/source metadata.
- **Research connections:** a release-object taxonomy, globally distributed evaluation design, and Wuhan diagnostics documented separately from integration tests.

The `earth_embedding` import and `earth-embedding` command are the new entry points. Existing `rs_embed` imports and `rs-embed` commands remain available for compatibility.

## Installation

Use Python 3.12 or later. Install this project from its Git repository; the instructions below do not assume an `earth-embedding` release on PyPI.

```bash
python -m pip install "earth-embedding @ git+https://github.com/GISWLH/earth-embedding.git"
```

For optional features or development:

```bash
git clone https://github.com/GISWLH/earth-embedding.git
cd earth-embedding
python -m pip install -e ".[location,aef]"
```

| Extra / environment | When you need it |
| --- | --- |
| Base installation | Core APIs and the dependencies declared in `pyproject.toml` |
| `.[location]` | GeoCLIP's official Python package; SatCLIP and Esri GLE use bundled runtimes |
| `.[aef]` | Rasterio and PyArrow for direct AlphaEarth COG sampling and Parquet indexes |
| `.[benchmark]` | Scikit-learn for the spatial-holdout evaluation example |
| `.[terratorch]` | TerraTorch-backed models, including TerraMind and the current Prithvi integration |
| `.[dev,full,location,aef,benchmark]` | Development checks and these optional integrations |

PyTorch must match your hardware. Model weights may download on first use; image encoders can require substantial memory. Neither the catalog command nor the describe command performs model inference:

```bash
earth-embedding models --json
earth-embedding describe satclip
```

For Earth Engine imagery/product routes, authorize your account with `earthengine authenticate` and configure an eligible Cloud project (`EE_PROJECT` when required). The direct location and GCS examples below do not initialize Earth Engine.

## Three quickstarts

### 1. Locations to embeddings

No image acquisition or date selection is needed. Inputs are WGS84 degrees in **longitude, latitude order**; even a single point is a two-dimensional array.

```python
from earth_embedding import get_location_embeddings

locations = [[114.41, 30.52], [139.76, 35.68], [-0.12, 51.51]]
result = get_location_embeddings("satclip", locations, device="cpu")
print(result.data.shape)  # (3, 256)
print(result.meta)

# Esri's official ~3.7 MB model package downloads and caches on first use.
esri = get_location_embeddings("esri_gle", locations, device="cpu")
print(esri.data.shape)  # (3, 256)

# Install .[location] first; GeoCLIP returns 512 features per location.
geoclip = get_location_embeddings("geoclip", locations, device="cpu")
```

Esri GLE uses its official pretrained weights with direct PyTorch inference; ArcGIS and ArcPy are not required. Downloads are pinned by SHA-256, and a local `.dlpk` or `satclip.pth` can be supplied for offline use. Esri's model terms apply separately. See [Esri GLE setup](docs/models/esri_gle.md) and the [validation report](docs/validation.md).

Location embeddings describe a learned geographic prior. Querying the same location with a different year does not produce an observation of land-cover change.

### 2. A place and time to image embeddings

Use the geographic API to fetch the configured imagery and run an image encoder. This example needs authorized Earth Engine access, model weights, and the model's runtime dependencies.

```python
from earth_embedding import PointBuffer, TemporalSpec, OutputSpec, get_embedding

result = get_embedding(
    "remoteclip",
    spatial=PointBuffer(lon=114.41, lat=30.52, buffer_m=320),
    temporal=TemporalSpec.range("2021-05-01", "2021-10-31"),
    output=OutputSpec.pooled(),
    device="cpu",
)
print(result.data.shape)
print(result.meta)
```

Already have imagery? `get_image_embedding(model, pixels, spatial=..., temporal=..., sensor=..., device=...)` accepts local CHW or TCHW arrays without fetching imagery. Supply the adapter's exact band order, sensor units, and time contract; an arbitrary RGB array is not valid input for every model. See [API reference](docs/api.md) and [model documentation](docs/models.md).

### 3. AlphaEarth embeddings directly from Google Cloud Storage

Download the official footprint index once, then select a year and area. The index is global; check its size before downloading.

```bash
curl -L -o aef_index.parquet https://storage.googleapis.com/alphaearth_foundations/satellite_embedding/v1/annual/aef_index.parquet
```

```python
from earth_embedding import BBox, find_aef_tiles, sample_aef

tiles = find_aef_tiles(
    "aef_index.parquet",
    spatial=BBox(114.40, 30.51, 114.42, 30.53),
    year=2021,
)
result = sample_aef([[114.41, 30.52]], tiles=tiles)
print(result.data.shape)  # (1, 64)
print(result.meta["source_for_point"])
```

The sampler performs CRS transformation, byte-range COG reads, signed-int8 dequantization, and nodata handling. Keep candidate tiles within one year. Missing coverage raises by default; `strict=False` preserves those rows as NaN. Network errors remain explicit errors.

Google's [official GCS guide](https://developers.google.com/earth-engine/guides/aef_on_gcs_readme) documents provider-paid access as of July 2026 and annual coverage from 2017 through 2025. See [data access](docs/data-access.md) for the CSV/GeoParquet/GeoPackage indexes, object manifest, Earth Engine alternative, and required attribution. AEF model weights are not distributed by this project.

## Model catalog

Classification follows the delivered object and evaluated input contract. Architecture, resolution, learning signal, and evaluation eligibility are separate properties. An adapter's presence is an integration statement; it is not a guarantee of current data access, checkpoint availability, or successful execution on your machine.

| Class | Model ID | Model / release | Input or access contract |
| --- | --- | --- | --- |
| A1 · RGB | `remoteclip` | [RemoteCLIP](docs/models/remoteclip.md) | Three-channel optical imagery |
| A1 · RGB | `satmae` | [SatMAE](docs/models/satmae.md) | RGB configuration |
| A1 · RGB | `satmaepp` | [SatMAE++](docs/models/satmaepp.md) | RGB configuration |
| A1 · RGB | `scalemae` | [Scale-MAE](docs/models/scalemae.md) | RGB and spatial scale |
| A1 · RGB | `wildsat` | [WildSAT](docs/models/wildsat.md) | RGB; backbone depends on configuration |
| A2 · Fixed-schema | `satmaepp_s2_10b` | [SatMAE++ Sentinel-2](docs/models/satmaepp.md) | Ordered 10-band input |
| A2 · Fixed-schema | `prithvi` | [Prithvi-EO-2.0](docs/models/prithvi.md) | Adapter's six-band input contract |
| A2 · Fixed-schema | `terramind` | [TerraMind](docs/models/terramind.md) | Sentinel-2 path in this configuration |
| A2 · Fixed-schema | `terrafm` | [TerraFM](docs/models/terrafm.md) | Sentinel-2 path in this configuration |
| A2 · Fixed-schema | `satvision` | [SatVision-TOA](docs/models/satvision.md) | 14-channel MODIS TOA; coarse support |
| A3 · Channel-adaptive | `dofa` | [DOFA](docs/models/dofa.md) | Spectral channels and wavelengths |
| A3 · Channel-adaptive | `fomo` | [FoMo](docs/models/fomo.md) | Model-specific channel identities |
| A3 · Channel-adaptive | `thor` | [THOR](docs/models/thor.md) | Model-specific band/schema metadata |
| A4 · Multitemporal | `galileo` | [Galileo](docs/models/galileo.md) | Dated Sentinel-2 sequence |
| A4 · Multitemporal | `anysat` | [AnySat](docs/models/anysat.md) | Dated Sentinel-2 sequence |
| A4 · Multitemporal | `agrifm` | [AgriFM](docs/models/agrifm.md) | Dated Sentinel-2 sequence |
| B · Location | `satclip` | [SatCLIP](docs/models/satclip.md) | Longitude/latitude; 256 dimensions |
| B · Location | `geoclip` | [GeoCLIP](docs/models/geoclip.md) | Longitude/latitude; 512 dimensions; optional package |
| B · Location | `esri_gle` | [Esri Global Location Encoder](docs/models/esri_gle.md) | Longitude/latitude; 256 dimensions; direct PyTorch, ~3.7 MB download |
| C1 · Gridded product | `gse` | [Google Satellite Embedding / AEF](docs/models/gse.md) | 10 m annual product; 64 dimensions; GEE or separate GCS helpers |
| C1 · Gridded product | `tessera` | [TESSERA](docs/models/tessera.md) | 10 m annual product; GeoTessera access/cache |
| C1 · Gridded product | `copernicus` | [Copernicus-Embed-025deg](docs/models/copernicus.md) | Precomputed 0.25° grid |

The taxonomy also includes **C2 sampled embedding collections**. No C2 adapter is claimed in this 22-entry catalog. Model-lineage names alone do not determine a class: published weights and a precomputed product can be separate releases.

## A workflow you can reuse

| Stage | Interface | What to check |
| --- | --- | --- |
| Discover | `earth-embedding models --json`, `describe MODEL` | Input requirements, supported output, optional dependencies |
| Inspect imagery | `inspect_provider_patch(...)` | Coverage, bands, pixel values, shape, acquisition window |
| Encode images | `get_embedding(...)`, `get_image_embedding(...)` | Provider or local input; correct preprocessing |
| Encode locations | `get_location_embeddings(...)` | WGS84 `[lon, lat]`, model/checkpoint, device |
| Read AEF data | `find_aef_tiles(...)`, `sample_aef(...)` | Year, coverage, CRS, nodata, source URL |
| Scale extraction | `get_embeddings_batch(...)`, `export_batch(...)` | Consistent configuration, cache, metadata, error handling |
| Analyze | Your downstream estimator and spatial splits | Task labels, leakage, matched support, uncertainty |

Results expose `.data` and `.meta`. Persist both: a feature matrix without its model revision, coordinates, dates, and preprocessing choices is difficult to reproduce. Feature dimensions and spatial grid support vary across models; the library does not make vectors from different encoders interchangeable.

## What can you build?

- **Land-cover classifiers** using pooled tile features and spatially separated training/test regions.
- **Built-up, vegetation, and water fraction regressors** with labels aggregated to matching spatial support.
- **Water masks or segmentation experiments** where the selected model exposes suitable dense features.
- **Similarity search and retrieval** within a model's embedding space, with geographic holdouts for evaluation.
- **Location-prior baselines** that help distinguish geographic regularities from information in imagery.
- **Repeated product queries** across available annual layers, with consistent geometry and explicit time coverage.

These are downstream workflows you can implement with the features; they are not universal pretrained prediction heads supplied by every adapter.

### Evaluate saved embeddings with a spatial holdout

The [evaluation example](examples/evaluate_embeddings.py) consumes saved features without fetching imagery. Supply a metadata CSV with `sample_id,target,split,spatial_group`, and one NPZ per model containing `X` and `sample_id`. Use `train` / `test` splits whose spatial groups are disjoint.

```bash
python -m pip install -e ".[benchmark]"
python examples/evaluate_embeddings.py --metadata metadata.csv --features satclip=satclip.npz geoclip=geoclip.npz --task classification --out evaluation.json
```

The script aligns all models to the same finite cohort, fits scaling and linear estimators on training rows only, and records cohort/input hashes. For regression use `--task regression`. Define a meaningful spatial split before running it; this example does not reproduce final manuscript scores.

## From manuscript to reusable software

Our manuscript work motivates three additions to the software: an explicit release taxonomy, comparable input/output contracts, and evaluation provenance. The frozen manuscript benchmark contains **20 systems: A16 + B1 (SatCLIP) + C3**. The software catalog now has **22 adapters** because GeoCLIP and Esri GLE are additional integrations; this does not expand the paper's evaluated set automatically.

The revised main evaluation uses a globally distributed **640 m** design. Wuhan **567/2,173-tile** materials provide local and historical diagnostics and retain their own scope. Evaluation covers classification, fraction regression, and supported dense-output tasks; matched spatial support and spatial holdouts matter more than a single aggregate ranking. SatVision and Copernicus-Embed retain their taxonomy classes even where their spatial support makes them ineligible for a controlled comparison.

See [research scope and evidence boundaries](docs/research.md). The manuscript is under development; this repository does not claim an accepted RSE paper, a final leaderboard, or that a smoke test establishes scientific superiority.

## Validation and current limits

The [validation report](docs/validation.md) records dated execution evidence, environments, output shapes, and unresolved dependencies. It separates unit/regression checks, real model inference, and live provider access. The new direct AEF route has a [live Wuhan 2021 sampling receipt](docs/validation/aef-gcs-20261013.json); successful sampling at one point does not establish global coverage or downstream accuracy.

Data providers can require authentication, quotas, or terms acceptance. Some models need specialized packages or large checkpoints. Esri GLE's weights retain Esri's model terms. A location encoder has no temporal observations. Coarse products cannot be made equivalent to a 10 m field by resampling. Read [limitations](docs/limitations.md) before designing a comparison.

## Documentation and examples

| Start here | Go deeper |
| --- | --- |
| [Quickstart](docs/quickstart.md) | [API reference](docs/api.md) |
| [Model reference](docs/models.md) | [Input/output concepts](docs/concepts.md) |
| [AlphaEarth data access](docs/data-access.md) | [Extraction workflows](docs/workflows.md) |
| [Research scope](docs/research.md) | [Validation evidence](docs/validation.md) |
| [Example notebooks](examples/) | [Adding an adapter](docs/extending.md) |
| [Project provenance](docs/provenance.md) | [Changelog](CHANGELOG.md) |

The hero and logo are editable hand-drawn Excalidraw assets. See the [artwork source and rendering instructions](docs/assets/earth-embedding-brand.md).

## Contribute

Useful contributions include adapters with explicit input contracts, reproducible failure reports, small executable examples, provider-access fixes, and improvements to English, Chinese, or Japanese documentation. Start with [CONTRIBUTING.md](CONTRIBUTING.md) and [open an issue](https://github.com/GISWLH/earth-embedding/issues) with a model's official source, license, checkpoint, and a concrete use case.

Priorities include broader environment validation, reproducible user-supplied imagery examples, more precomputed-product access routes, and carefully documented C2 integrations. These are development directions, not promises of currently implemented functionality.

## Cite and acknowledge

For this extension, cite the software repository and the commit or release you used; machine-readable metadata is in [CITATION.cff](CITATION.cff). Cite the original rs-embed paper when using its framework, and the original model/data publications for the artifacts used in your analysis. Our research manuscript will receive its own citation when a public bibliographic record is available.

```bibtex
@article{ye2026modelplacetimeremote,
  title={Any Model, Any Place, Any Time: Get Remote Sensing Foundation Model Embeddings On Demand},
  author={Ye, Dingqi and Kiv, Daniel and Hu, Wei and Shi, Jimeng and Wang, Shaowen},
  year={2026},
  eprint={2602.23678},
  archivePrefix={arXiv},
  url={https://arxiv.org/abs/2602.23678}
}
```

We thank the rs-embed contributors, model authors, Google Earth Engine, Google and Google DeepMind, TorchGeo, GeoTessera, TerraTorch, rshf, Microsoft SatCLIP, GeoCLIP, Esri, and the wider Earth observation community. Integration does not imply endorsement.

## License

Library code is distributed under [Apache-2.0](LICENSE), with inherited attribution retained in [NOTICE](NOTICE). Vendored components, model weights, data, and fonts retain their respective licenses. AlphaEarth data is CC-BY-4.0; Esri's software/model terms apply separately. See [provenance and licensing](docs/provenance.md).
