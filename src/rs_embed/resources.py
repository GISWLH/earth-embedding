"""Download-free discovery of model documentation and upstream artifacts.

These are landing pages, not download instructions or a claim that every
checkpoint is hosted by its original authors. Adapter overrides are described
on the individual model pages. URLs were reviewed on 2026-10-13.
"""

from __future__ import annotations

from .core.errors import ModelError
from .embedders.catalog import canonical_model_id

_DOCS = "https://giswlh.github.io/earth-embedding/latest/models/"
_HF = "https://huggingface.co/"


def _resource(
    model_id: str,
    name: str,
    category: str,
    input_description: str,
    source_url: str,
    weights_url: str,
    weights_kind: str,
    notes: str = "",
    *,
    docs_slug: str | None = None,
) -> dict[str, str]:
    return {
        "model_id": model_id,
        "name": name,
        "category": category,
        "input": input_description,
        "docs_url": f"{_DOCS}{docs_slug or model_id}/",
        "source_url": source_url,
        "weights_url": weights_url,
        "weights_kind": weights_kind,
        "notes": notes,
    }


_RESOURCES = [
    _resource(
        "remoteclip",
        "RemoteCLIP",
        "image",
        "Sentinel-2 RGB",
        "https://github.com/ChenDelong1999/RemoteCLIP",
        _HF + "MVRL/remote-clip-vit-base-patch32",
        "Hugging Face model",
        "Default adapter checkpoint: MVRL/rshf packaging of RemoteCLIP ViT-B/32.",
    ),
    _resource(
        "satmae",
        "SatMAE",
        "image",
        "Sentinel-2 RGB",
        "https://github.com/sustainlab-group/SatMAE",
        _HF + "MVRL/satmae-vitlarge-fmow-pretrain-800",
        "Hugging Face model",
        "Default adapter checkpoint: MVRL/rshf packaging of the RGB model.",
    ),
    _resource(
        "satmaepp",
        "SatMAE++ RGB",
        "image",
        "Sentinel-2 RGB",
        "https://github.com/techmn/satmae_pp",
        _HF + "MVRL/satmaepp_ViT-L_pretrain_fmow_rgb",
        "Hugging Face model",
        "Default adapter checkpoint: MVRL/rshf packaging of the RGB model.",
    ),
    _resource(
        "satmaepp_s2_10b",
        "SatMAE++ multispectral",
        "image",
        "Sentinel-2 10 bands",
        "https://github.com/techmn/satmae_pp",
        _HF + "mubashir04/checkpoint_ViT-L_pretrain_fmow_sentinel",
        "Hugging Face model",
        "Separate multispectral checkpoint; not interchangeable with the RGB adapter.",
        docs_slug="satmaepp",
    ),
    _resource(
        "scalemae",
        "Scale-MAE",
        "image",
        "Sentinel-2 RGB + ground resolution",
        "https://github.com/bair-climate-initiative/scale-mae",
        _HF + "MVRL/scalemae-vitlarge-800",
        "Hugging Face model",
        "Default adapter checkpoint: MVRL/rshf packaging.",
    ),
    _resource(
        "wildsat",
        "WildSAT",
        "image",
        "Sentinel-2 RGB",
        "https://github.com/cvl-umass/wildsat",
        "https://github.com/cvl-umass/wildsat#quickstart",
        "official download",
        "Author repository links to Google Drive checkpoints; no default HF repository.",
    ),
    _resource(
        "prithvi",
        "Prithvi-EO 2.0",
        "image",
        "Sentinel-2 6 bands + time/location",
        "https://github.com/NASA-IMPACT/Prithvi-EO-2.0",
        _HF + "ibm-nasa-geospatial/Prithvi-EO-2.0-100M-TL",
        "Hugging Face model",
        "Default: 100M-TL. The adapter also supports 300M-TL and 600M-TL.",
    ),
    _resource(
        "terrafm",
        "TerraFM",
        "image",
        "Sentinel-2 12 bands or Sentinel-1 VV/VH",
        "https://github.com/mbzuai-oryx/TerraFM",
        _HF + "MBZUAI/TerraFM",
        "Hugging Face model",
        "Base checkpoint; select one sensor modality per call.",
    ),
    _resource(
        "terramind",
        "TerraMind",
        "image",
        "Sentinel-2 12 bands",
        "https://github.com/IBM/terramind",
        _HF + "ibm-esa-geospatial/TerraMind-1.0-small",
        "Hugging Face model",
        "Default: TerraMind 1.0 small; requires the TerraTorch extra.",
    ),
    _resource(
        "dofa",
        "DOFA",
        "image",
        "Multispectral imagery + wavelengths",
        "https://github.com/zhu-xlab/DOFA",
        _HF + "earthflow/DOFA",
        "Hugging Face model",
    ),
    _resource(
        "fomo",
        "FoMo-Net",
        "image",
        "Sentinel-2 12 bands",
        "https://github.com/RolnickLab/FoMo-Bench",
        "https://github.com/RolnickLab/FoMo-Bench#loading-pretrained-fomo-net",
        "official download",
        "Author repository links to the FoMo-Net checkpoint on Dropbox.",
    ),
    _resource(
        "thor",
        "THOR",
        "image",
        "Sentinel-2 10 bands",
        "https://github.com/FM4CS/THOR",
        _HF + "FM4CS/THOR-1.0-base",
        "Hugging Face model",
    ),
    _resource(
        "satvision",
        "SatVision-TOA",
        "image",
        "14 calibrated TOA channels",
        "https://github.com/nasa-nccs-hpda/pytorch-caney",
        _HF + "nasa-cisto-data-science-group/satvision-toa-giant-patch8-window8-128",
        "Hugging Face model",
        "Requires the model-specific TOA channel/calibration contract.",
    ),
    _resource(
        "anysat",
        "AnySat",
        "image",
        "Sentinel-2 10-band time series",
        "https://github.com/gastruc/anysat",
        _HF + "g-astruc/AnySat",
        "Hugging Face model",
    ),
    _resource(
        "galileo",
        "Galileo",
        "image",
        "Sentinel-2 10-band time series",
        "https://github.com/nasaharvest/galileo",
        _HF + "nasaharvest/galileo",
        "Hugging Face model",
    ),
    _resource(
        "agrifm",
        "AgriFM",
        "image",
        "Sentinel-2 10-band time series",
        "https://github.com/flyakon/AgriFM",
        "https://github.com/flyakon/AgriFM#model-training",
        "official download",
        "Author repository links to GLASS/OneDrive; adapter downloads AgriFM.pth from GLASS.",
    ),
    _resource(
        "satclip",
        "SatCLIP",
        "location",
        "Longitude/latitude only",
        "https://github.com/microsoft/satclip",
        _HF + "microsoft/SatCLIP-ViT16-L40",
        "Hugging Face model",
        "Default: ViT16-L40 location encoder; no imagery fetch, time invariant.",
    ),
    _resource(
        "geoclip",
        "GeoCLIP",
        "location",
        "Longitude/latitude only",
        "https://github.com/VicenteVivan/geo-clip",
        "https://github.com/VicenteVivan/geo-clip#usage-pre-trained-location-encoder",
        "official download",
        "Author's geoclip package supplies the location weights; requires the location extra.",
    ),
    _resource(
        "esri_gle",
        "Esri Global Location Encoder",
        "location",
        "Longitude/latitude only",
        "https://doc.arcgis.com/en/pretrained-models/latest/vector/"
        "introduction-to-global-location-encoder-sentinel-2-.htm",
        "https://www.arcgis.com/home/item.html?id=b0664ef297c04d4aaa44191cf21e07f3",
        "official download",
        "Official ArcGIS Living Atlas model; direct PyTorch adapter, no ArcGIS install needed.",
    ),
    _resource(
        "tessera",
        "Tessera",
        "precomputed",
        "Published GeoTessera embedding tiles",
        "https://github.com/ucam-eo/geotessera",
        "https://github.com/ucam-eo/geotessera#dataset-versions-and-variants",
        "official product",
        "Queries precomputed tiles; preserve dataset version and variant.",
    ),
    _resource(
        "gse",
        "Google Satellite Embedding / AlphaEarth",
        "precomputed",
        "Annual Google Satellite Embedding product",
        "https://developers.google.com/earth-engine/datasets/catalog/"
        "GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL",
        "https://developers.google.com/earth-engine/datasets/catalog/"
        "GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL",
        "official product",
        "Published embedding product, not downloadable encoder weights.",
    ),
    _resource(
        "copernicus",
        "Copernicus-Embed",
        "precomputed",
        "0.25-degree embedding product",
        _HF + "datasets/wangyi111/Copernicus-Embed-025deg",
        _HF + "datasets/torchgeo/copernicus_embed",
        "Hugging Face dataset",
        "Adapter uses TorchGeo's GeoTIFF redistribution of the author's embedding dataset.",
    ),
]
_BY_ID = {entry["model_id"]: entry for entry in _RESOURCES}
_CATEGORIES = ("image", "location", "precomputed")


def get_model_resources(model: str) -> dict[str, str]:
    """Return documentation, source and artifact URLs without loading a model.

    Canonical IDs and aliases accepted by :func:`get_embedding` work here too.
    The returned dictionary is an independent copy. ``weights_url`` points to
    a model, dataset or product landing page according to ``weights_kind``.
    It records the adapter's default source, not an environment override.
    """
    model_id = canonical_model_id(model)
    try:
        return dict(_BY_ID[model_id])
    except KeyError:
        raise ModelError(
            f"Unknown model '{model}'. Available models: {', '.join(_BY_ID)}"
        ) from None


def list_model_resources(category: str | None = None) -> list[dict[str, str]]:
    """List resources for all adapters or one of image/location/precomputed.

    Uses bundled metadata only: no network request, provider authentication,
    checkpoint loading or inference. Returns fresh dictionaries in catalog
    presentation order (image encoders, location encoders, products).
    """
    if category is not None:
        category = str(category).strip().lower()
        if category not in _CATEGORIES:
            raise ValueError(f"Unknown category '{category}'; choose from {_CATEGORIES}.")
    return [
        dict(entry) for entry in _RESOURCES if category is None or entry["category"] == category
    ]
