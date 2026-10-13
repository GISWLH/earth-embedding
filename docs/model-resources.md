# Model resources and Hugging Face

Find the source code, default checkpoint or embedding product, and usage guide
for all **22 canonical adapters**. The links below were checked on **2026-10-13**.
They point to upstream resources; Earth Embedding does not republish the weights.

## Browse from Python

```python
from earth_embedding import get_model_resources, list_model_resources

prithvi = get_model_resources("prithvi")
print(prithvi["weights_url"])  # Hugging Face model card for the default 100M-TL model

for model in list_model_resources(category="location"):
    print(model["model_id"], model["weights_kind"], model["weights_url"])
```

These helpers read bundled metadata only. They do not download weights, initialize
providers, or run inference. Aliases such as `alphaearth` and `esri` work too.
Call `list_model_resources()` without a category for all 22 adapters; categories
are `image`, `location`, and `precomputed`. Each entry includes `model_id`, `name`,
`category`, `input`, `docs_url`, `source_url`, `weights_url`, `weights_kind`, and `notes`.

## Full resource directory

**A** means an image encoder, **B** a location encoder, and **C** a precomputed
embedding product. Inputs describe the current adapter path, which can be narrower
than the upstream model's capabilities. All adapters expose `pooled` and `grid`
outputs; the meaning of a grid differs by model (tokens, coordinates, or product
pixels). Read the linked guide before comparing them.

| Model ID / guide | Class | Current adapter input | Upstream source | Weights or product |
| --- | --- | --- | --- | --- |
| [`remoteclip`](models/remoteclip.md) | A · image | Sentinel-2 RGB | [Source](https://github.com/ChenDelong1999/RemoteCLIP) | [Hugging Face model](https://huggingface.co/MVRL/remote-clip-vit-base-patch32) |
| [`satmae`](models/satmae.md) | A · image | Sentinel-2 RGB | [Source](https://github.com/sustainlab-group/SatMAE) | [Hugging Face model](https://huggingface.co/MVRL/satmae-vitlarge-fmow-pretrain-800) |
| [`satmaepp`](models/satmaepp.md) | A · image | Sentinel-2 RGB | [Source](https://github.com/techmn/satmae_pp) | [Hugging Face model](https://huggingface.co/MVRL/satmaepp_ViT-L_pretrain_fmow_rgb) |
| [`satmaepp_s2_10b`](models/satmaepp.md) | A · image | Sentinel-2 10 bands | [Source](https://github.com/techmn/satmae_pp) | [Hugging Face model](https://huggingface.co/mubashir04/checkpoint_ViT-L_pretrain_fmow_sentinel) |
| [`scalemae`](models/scalemae.md) | A · image | Sentinel-2 RGB + ground resolution | [Source](https://github.com/bair-climate-initiative/scale-mae) | [Hugging Face model](https://huggingface.co/MVRL/scalemae-vitlarge-800) |
| [`wildsat`](models/wildsat.md) | A · image | Sentinel-2 RGB | [Source](https://github.com/cvl-umass/wildsat) | [official download](https://github.com/cvl-umass/wildsat#quickstart) |
| [`prithvi`](models/prithvi.md) | A · image | Sentinel-2 6 bands + time/location | [Source](https://github.com/NASA-IMPACT/Prithvi-EO-2.0) | [Hugging Face model](https://huggingface.co/ibm-nasa-geospatial/Prithvi-EO-2.0-100M-TL) |
| [`terrafm`](models/terrafm.md) | A · image | Sentinel-2 12 bands or Sentinel-1 VV/VH | [Source](https://github.com/mbzuai-oryx/TerraFM) | [Hugging Face model](https://huggingface.co/MBZUAI/TerraFM) |
| [`terramind`](models/terramind.md) | A · image | Sentinel-2 12 bands | [Source](https://github.com/IBM/terramind) | [Hugging Face model](https://huggingface.co/ibm-esa-geospatial/TerraMind-1.0-small) |
| [`dofa`](models/dofa.md) | A · image | Multispectral imagery + wavelengths | [Source](https://github.com/zhu-xlab/DOFA) | [Hugging Face model](https://huggingface.co/earthflow/DOFA) |
| [`fomo`](models/fomo.md) | A · image | Sentinel-2 12 bands | [Source](https://github.com/RolnickLab/FoMo-Bench) | [official download](https://github.com/RolnickLab/FoMo-Bench#loading-pretrained-fomo-net) |
| [`thor`](models/thor.md) | A · image | Sentinel-2 10 bands | [Source](https://github.com/FM4CS/THOR) | [Hugging Face model](https://huggingface.co/FM4CS/THOR-1.0-base) |
| [`satvision`](models/satvision.md) | A · image | 14 calibrated TOA channels | [Source](https://github.com/nasa-nccs-hpda/pytorch-caney) | [Hugging Face model](https://huggingface.co/nasa-cisto-data-science-group/satvision-toa-giant-patch8-window8-128) |
| [`anysat`](models/anysat.md) | A · image | Sentinel-2 10-band time series | [Source](https://github.com/gastruc/anysat) | [Hugging Face model](https://huggingface.co/g-astruc/AnySat) |
| [`galileo`](models/galileo.md) | A · image | Sentinel-2 10-band time series | [Source](https://github.com/nasaharvest/galileo) | [Hugging Face model](https://huggingface.co/nasaharvest/galileo) |
| [`agrifm`](models/agrifm.md) | A · image | Sentinel-2 10-band time series | [Source](https://github.com/flyakon/AgriFM) | [official download](https://github.com/flyakon/AgriFM#model-training) |
| [`satclip`](models/satclip.md) | B · location | Longitude/latitude only | [Source](https://github.com/microsoft/satclip) | [Hugging Face model](https://huggingface.co/microsoft/SatCLIP-ViT16-L40) |
| [`geoclip`](models/geoclip.md) | B · location | Longitude/latitude only | [Source](https://github.com/VicenteVivan/geo-clip) | [official download](https://github.com/VicenteVivan/geo-clip#usage-pre-trained-location-encoder) |
| [`esri_gle`](models/esri_gle.md) | B · location | Longitude/latitude only | [Source](https://doc.arcgis.com/en/pretrained-models/latest/vector/introduction-to-global-location-encoder-sentinel-2-.htm) | [official download](https://www.arcgis.com/home/item.html?id=b0664ef297c04d4aaa44191cf21e07f3) |
| [`tessera`](models/tessera.md) | C · product | Published GeoTessera embedding tiles | [Source](https://github.com/ucam-eo/geotessera) | [official product](https://github.com/ucam-eo/geotessera#dataset-versions-and-variants) |
| [`gse`](models/gse.md) | C · product | Annual Google Satellite Embedding product | [Source](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL) | [official product](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL) |
| [`copernicus`](models/copernicus.md) | C · product | 0.25-degree embedding product | [Source](https://huggingface.co/datasets/wangyi111/Copernicus-Embed-025deg) | [Hugging Face dataset](https://huggingface.co/datasets/torchgeo/copernicus_embed) |

## Which artifact am I opening?

- **Hugging Face model** links identify the checkpoint repository selected by the
  current adapter default. The Prithvi default is **100M-TL** and the TerraMind
  default is **1.0 small**. Environment overrides can select a different source;
  see the model guide and `describe_model(...)`.
- **MVRL checkpoints** are the `rshf`-compatible packages used for RemoteCLIP,
  SatMAE RGB, SatMAE++ RGB, and Scale-MAE. Their upstream author repositories are
  linked separately; these are not Earth Embedding publications.
- **Hugging Face dataset** is already-computed data. The Copernicus adapter reads
  TorchGeo's GeoTIFF redistribution; the source link leads to the author's
  Copernicus-Embed dataset. It is not an inference-model checkpoint.
- **Official download** links lead to the authors' release instructions. WildSAT
  uses Google Drive, FoMo uses Dropbox, and AgriFM provides GLASS/OneDrive links.
  GeoCLIP uses its author's Python package; Esri GLE uses the ArcGIS Living Atlas
  model item. A Hugging Face account is not a universal requirement.
- **Official product** links describe published embeddings. `gse` retrieves
  Google Satellite Embedding/AlphaEarth output; it does not load an AlphaEarth
  encoder. `tessera` queries GeoTessera tiles; retain the dataset version and
  variant when reusing embeddings.

Each upstream model or dataset keeps its own license, citation, access terms,
and preprocessing requirements. Follow its model card or release documentation.
The directory is a discovery aid, not a lockfile or a claim that all sources
have the same license.

## Location encoders, including Esri

`satclip`, `geoclip`, and `esri_gle` encode coordinates without fetching an image.
Earth Embedding accepts **longitude, latitude** consistently and converts to the
underlying model's coordinate order. Their outputs are time invariant, so changing
`temporal` does not create new observations. A coordinate grid is a sampled
location prior, not satellite imagery at that date.

The Esri adapter downloads the official Global Location Encoder package and runs
its location weights directly with PyTorch. See the [Esri guide](models/esri_gle.md)
for cache controls and model limits. The [GeoCLIP guide](models/geoclip.md) covers
its optional `location` extra; the [SatCLIP guide](models/satclip.md) covers its
checkpoint variants.

The library's **22 adapters** include the two software extensions GeoCLIP and
Esri GLE. The manuscript benchmark remains the frozen **20 systems** (A: 16,
B: SatCLIP only, C: 3); listing an adapter does not add a benchmark result.
See [validation status](validation.md) for the evidence behind each integration,
and [model selection](models.md) for input and output choices.
