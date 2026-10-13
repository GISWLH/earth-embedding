# Earth Embedding

```python
emb = get_embedding("prithvi", spatial=spatial, temporal=temporal, output=output)
```

**One geographic API, 22 model configurations, and a shared comparison figure.**
Use `get_embedding` for one model, `compare_embeddings` for several models,
and `plot_embedding_comparison` to display their results together.

![Sentinel-2 reference and 22 real model outputs](assets/comparison/all-models.png)

[Run the comparison tutorial](tutorials/model-comparison.md) ·
[Hugging Face weights and official resources](model-resources.md) ·
[Quickstart](quickstart.md)

The gallery contains real image/product features and location inference over
the same Wuhan extent. Each panel uses its own PCA colors and spatial support;
this qualitative view is not a model ranking.

<picture>
  <source media="(max-width: 760px)" srcset="assets/earth-embedding-hero-mobile.svg">
  <img src="assets/earth-embedding-hero.svg" width="100%" alt="Earth Embedding: images, locations and precomputed products through a shared Python interface.">
</picture>

Earth Embedding provides a shared Python interface for image encoders, location encoders, and precomputed geospatial embedding products. Its catalog contains 22 adapters across these three release classes. Choose the input you have, check the model's contract, and retain both embedding values and provenance for downstream analysis.

This project is an independent extension of [CyberGIS rs-embed](https://github.com/cybergis/rs-embed), by Dingqi Ye and contributors. Its Apache-2.0 foundation and upstream attribution are retained. Read [provenance](provenance.md) for the relationship between the original project, this extension, and our manuscript.

## Choose a starting point

**Start with real results:** [five-line AEF map, Esri GLE, spatial classification,
and four executed notebooks](tutorials/real-demos.md). Small real samples are
bundled; the first map and downstream probe run on CPU without credentials.

![Bay Area spatial classification demo](assets/demos/bayarea-classification.png)

| Your input | Entry point | Guide |
| --- | --- | --- |
| One region, several models | `compare_embeddings(...)`, `plot_embedding_comparison(...)` | [Multi-model tutorial](tutorials/model-comparison.md) |
| WGS84 longitude/latitude | `get_location_embeddings(...)` | [SatCLIP](models/satclip.md), [GeoCLIP](models/geoclip.md), [Esri GLE](models/esri_gle.md) |
| Place and observation window | `get_embedding(...)` | [Quickstart](quickstart.md) |
| An existing image array | `get_image_embedding(...)` | [API reference](api.md) |
| Annual AlphaEarth COGs | `find_aef_tiles(...)`, `sample_aef(...)` | [Data access](data-access.md) |
| A collection of regions | `get_embeddings_batch(...)`, `export_batch(...)` | [Workflows](workflows.md) |

## Install from source

```bash
git clone https://github.com/GISWLH/earth-embedding.git
cd earth-embedding
python -m pip install -e ".[location,aef]"
earth-embedding models --json
```

Use Python 3.12 or later. Additional model runtimes, data-provider credentials, and checkpoints depend on the model. Esri GLE runs directly in PyTorch with its official lightweight weights; it needs no ArcGIS installation. Current installation instructions do not assume publication on PyPI.

## A first location query

```python
from earth_embedding import get_location_embeddings

result = get_location_embeddings("satclip", [[114.41, 30.52]], device="cpu")
print(result.data.shape)  # (1, 256)
print(result.meta)
```

Coordinates are **[longitude, latitude]** in WGS84 degrees. Model weights may download on first use. This query does not acquire imagery or initialize Earth Engine. The original `rs_embed` import remains available for compatibility.

## Explore the documentation

- [Model catalog](models.md): each adapter's input requirements, output support, and optional dependencies.
- [Hugging Face & official resources](model-resources.md): linked checkpoints, datasets, upstream code, and model terms for all 22 entries.
- [API reference](api.md): geographic extraction, local images, locations, batch export, and metadata.
- [AlphaEarth access](data-access.md): official GCS indexes, point sampling, decoding, Earth Engine, and attribution.
- [Validation report](validation.md): real execution evidence, environments, and unresolved limitations.
- [Research scope](research.md): release taxonomy, global design, Wuhan diagnostics, and evidence boundaries.
- [Limitations](limitations.md): practical and scientific constraints to consider before use.
- [Extending the package](extending.md) and [contributing](contributing.md): model integrations and development workflow.

Full project introductions are available in [English](https://github.com/GISWLH/earth-embedding/blob/main/README.md), [简体中文](https://github.com/GISWLH/earth-embedding/blob/main/README.zh-CN.md), and [日本語](https://github.com/GISWLH/earth-embedding/blob/main/README.ja.md).

## Software and research are different scopes

The software catalog has 22 entries. The frozen manuscript benchmark has 20 systems: 16 image encoders, SatCLIP, and 3 precomputed products. GeoCLIP and Esri GLE are additional software integrations. A passing interface test or a successful smoke query does not establish a new scientific result or a complete benchmark ranking.
