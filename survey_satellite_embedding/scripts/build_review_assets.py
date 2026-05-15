from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[2]
SURVEY_DIR = ROOT / "survey_satellite_embedding"
DATA_DIR = SURVEY_DIR / "data"
PAPER_DIR = SURVEY_DIR / "paper"
TABLES_DIR = PAPER_DIR / "tables"
DATA_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)

INVENTORY_PATH = ROOT / "research_outputs" / "rs_embed_model_inventory.json"
BENCHMARK_PATH = ROOT / "research_outputs" / "gpu_benchmark_full_summary.json"
PAPERS_DIR = ROOT / "research_outputs" / "papers" / "processed"


PROCESSED_PATHS = {
    "agrifm": PAPERS_DIR / "agrifm" / "agrifm.md",
    "anysat": PAPERS_DIR
    / "anysat"
    / "one-earth-observation-model-for-many-resolutions-scales-and-modalities.md",
    "copernicus": PAPERS_DIR
    / "copernicus"
    / "towards-a-unified-copernicus-foundation-model-for-earth-vision.md",
    "dofa": PAPERS_DIR
    / "dofa"
    / "neural-plasticity-inspired-multimodal-foundation-model-for-earth-observation.md",
    "fomo": PAPERS_DIR
    / "fomo"
    / "multi-modal-multi-scale-and-multi-task-remote-sensing-foundation-models-for-forest-monitoring.md",
    "galileo": PAPERS_DIR
    / "galileo"
    / "learning-global-local-features-of-many-remote-sensing-modalities.md",
    "gse": PAPERS_DIR
    / "gse"
    / "an-embedding-field-model-for-accurate-and-efficient-global-mapping-from-sparse-label-data.md",
    "prithvi": PAPERS_DIR
    / "prithvi"
    / "foundation-models-for-generalist-geospatial-artificial-intelligence.md",
    "remoteclip": PAPERS_DIR
    / "remoteclip"
    / "a-vision-language-foundation-model-for-remote-sensing.md",
    "satmae": PAPERS_DIR
    / "satmae"
    / "pre-training-transformers-for-temporal-and-multi-spectral-satellite-imagery.md",
    "satmaepp": PAPERS_DIR
    / "satmaepp"
    / "rethinking-transformers-pre-training-for-multi-spectral-satellite-imagery.md",
    "satmaepp_s2_10b": PAPERS_DIR
    / "satmaepp"
    / "rethinking-transformers-pre-training-for-multi-spectral-satellite-imagery.md",
    "satvision": PAPERS_DIR
    / "satvision"
    / "a-geospatial-foundation-model-for-coarse-resolution-all-sky-remote-sensing-imagery.md",
    "scalemae": PAPERS_DIR
    / "scalemae"
    / "a-scale-aware-masked-autoencoder-for-multiscale-geospatial-representation-learning.md",
    "terrafm": PAPERS_DIR
    / "terrafm"
    / "a-scalable-foundation-model-for-unified-multisensor-earth-observation.md",
    "terramind": PAPERS_DIR
    / "terramind"
    / "large-scale-generative-multimodality-for-earth-observation.md",
    "tessera": PAPERS_DIR
    / "tessera"
    / "temporal-embeddings-of-surface-spectra-for-earth-representation-and-analysis.md",
    "thor": PAPERS_DIR
    / "thor"
    / "a-versatile-foundation-model-for-earth-observation-climate-and-society-applications.md",
    "wildsat": PAPERS_DIR
    / "wildsat"
    / "learning-satellite-image-representations-from-wildlife-observations.md",
}


AUTHOR_OVERRIDES = {
    "anysat": "Guillaume Astruc, Nicolas Gonthier, Clement Mallet, Loic Landrieu",
    "copernicus": (
        "Yi Wang, Zhitong Xiong, Chenying Liu, Adam J. Stewart, Thomas Dujardin, "
        "Nikolaos Ioannis Bountos, Angelos Zavras, Franziska Gerken, Ioannis Papoutsis, "
        "Laura Leal-Taixe, Xiao Xiang Zhu"
    ),
    "dofa": (
        "Zhitong Xiong, Yi Wang, Fahong Zhang, Adam J. Stewart, Joelle Hanna, "
        "Damian Borth, Ioannis Papoutsis, Bertrand Le Saux, Gustau Camps-Valls, Xiao Xiang Zhu"
    ),
    "fomo": "Nikolaos Ioannis Bountos, Arthur Ouaknine, Ioannis Papoutsis, David Rolnick",
    "galileo": (
        "Gabriel Tseng, Anthony Fuller, Marlena Reil, Henry Herzog, Patrick Beukema, "
        "Favyen Bastani, James R. Green, Evan Shelhamer, Hannah Kerner, David Rolnick"
    ),
    "prithvi": (
        "Johannes Jakubik, Sujit Roy, C. E. Phillips, Paolo Fraccaro, Denys Godwin, "
        "Bianca Zadrozny, Daniela Szwarcman, Carlos Gomes, Gabby Nyirjesy, Blair Edwards, "
        "Daiki Kimura, Naomi Simumba, Linsong Chu, S. Karthik Mukkavilli, Devyani Lambhate, "
        "Kamal Das, Ranjini Bangalore, Dario Oliveira, Michal Muszynski, Kumar Ankur, "
        "Muthukumaran Ramasubramanian, Iksha Gurung, Sam Khallaghi, Hanxi Li, Michael Cecil, "
        "Maryam Ahmadi, Fatemeh Kordi, Hamed Alemohammad, Manil Maskey, Raghu Ganti, "
        "Kommy Weldemariam, Rahul Ramachandran"
    ),
    "satmae": (
        "Yezhen Cong, Samar Khanna, Chenlin Meng, Patrick Liu, Erik Rozi, "
        "Yutong He, Marshall Burke, David B. Lobell, Stefano Ermon"
    ),
    "satmaepp": (
        "Mubashir Noman, Muzammal Naseer, Hisham Cholakkal, "
        "Rao Muhammad Anwer, Salman Khan, Fahad Shahbaz Khan"
    ),
    "satmaepp_s2_10b": (
        "Mubashir Noman, Muzammal Naseer, Hisham Cholakkal, "
        "Rao Muhammad Anwer, Salman Khan, Fahad Shahbaz Khan"
    ),
    "scalemae": (
        "Colorado J. Reed, Ritwik Gupta, Shufan Li, Sarah Brockman, Christopher Funk, "
        "Brian Clipp, Kurt Keutzer, Salvatore Candido, Matt Uyttendaele, Trevor Darrell"
    ),
    "terrafm": (
        "Muhammad Sohail Danish, Muhammad Akhtar Munir, Syed Roshaan Ali Shah, "
        "Muhammad Haris Khan, Rao Muhammad Anwer, Jorma Laaksonen, "
        "Fahad Shahbaz Khan, Salman Khan"
    ),
    "terramind": (
        "Johannes Jakubik, Felix Yang, Benedikt Blumenstiel, Erik Scheurer, Rocco Sedona, "
        "Stefano Maurogiovanni, Jente Bosmans, Nikolaos Dionelis, Valerio Marsocci, "
        "Niklas Kopp, Rahul Ramachandran, Paolo Fraccaro, Thomas Brunschwiler, "
        "Gabriele Cavallaro, Juan Bernabe-Moreno, Nicolas Longepe"
    ),
    "thor": (
        "Theodor Forgaard, Jarle Reksten, Anders Waldeland, Valerio Marsocci, "
        "Nicolas Longepe, Michael Kampffmeyer, Arnt-Borre Salberg"
    ),
    "wildsat": "Rangel Daroya, Elijah Cole, Oisin Mac Aodha, Grant Van Horn, Subhransu Maji",
    "agrifm": (
        "Wenyuan Li, Shunlin Liang, Keyan Chen, Yongzhe Chen, Han Ma, Jianglei Xu, "
        "Yichuan Ma, Yuxiang Zhang, Shikang Guan, Husheng Fang, Zhenwei Shi"
    ),
}


ENRICHMENTS = {
    "tessera": {
        "review_family": "Precomputed temporal embedding field",
        "representation_mode": "precomputed dense embedding tiles",
        "backbone_family": "field model over surface spectra embeddings",
        "sensor_support": ["surface spectra product"],
        "modality_scope": "single-modality spectral-temporal product",
        "pretraining_signal": "embedding field regression / product training",
        "temporal_modeling": "annual lookup over product years",
        "training_data_summary": "global Earth observation spectra aggregated into tessellated embedding tiles",
        "architecture_notes": "not an on-the-fly neural encoder inside rs-embed; uses GeoTessera runtime for tile lookup and crop",
        "typical_tasks": ["representation lookup", "regional embedding analysis", "retrieval", "downstream transfer"],
    },
    "gse": {
        "review_family": "Precomputed annual embedding product",
        "representation_mode": "precomputed annual field",
        "backbone_family": "embedding field model",
        "sensor_support": ["Google Satellite Embedding annual product"],
        "modality_scope": "single product",
        "pretraining_signal": "global embedding field learning from sparse labels",
        "temporal_modeling": "strict yearly product",
        "training_data_summary": "global annual satellite embedding product served through Earth Engine",
        "architecture_notes": "adapter samples from an external yearly embedding product rather than running a neural encoder locally",
        "typical_tasks": ["global mapping", "rapid transfer", "feature sampling"],
    },
    "copernicus": {
        "review_family": "Precomputed foundation map",
        "representation_mode": "precomputed GeoTIFF feature map",
        "backbone_family": "Copernicus foundation model product",
        "sensor_support": ["Copernicus product stack"],
        "modality_scope": "multisource product collapsed into a 2021 embedding map",
        "pretraining_signal": "foundation model pretraining followed by product distillation",
        "temporal_modeling": "static in current adapter (2021 only)",
        "training_data_summary": "global Copernicus-scale EO data compiled into a unified feature raster",
        "architecture_notes": "rs-embed reads local slices from a precomputed embedding GeoTIFF",
        "typical_tasks": ["broad-area retrieval", "feature extraction", "downstream transfer"],
    },
    "remoteclip": {
        "review_family": "Vision-language satellite embedding",
        "representation_mode": "joint image-text embedding",
        "backbone_family": "CLIP / ViT-B-32",
        "sensor_support": ["Sentinel-2 RGB", "remote sensing captions", "UAV imagery in pretraining"],
        "modality_scope": "vision-language",
        "pretraining_signal": "contrastive image-text alignment (InfoNCE)",
        "temporal_modeling": "single composited observation window at inference",
        "training_data_summary": "large image-caption corpus built via box-to-caption and mask-to-caption conversion plus UAV imagery",
        "architecture_notes": "CLIP-style dual encoder specialized for remote sensing semantics and zero-shot transfer",
        "typical_tasks": ["zero-shot classification", "retrieval", "few-shot classification", "counting", "open-vocabulary transfer"],
    },
    "satmae": {
        "review_family": "Masked autoencoder for temporal or multispectral EO",
        "representation_mode": "ViT patch tokens",
        "backbone_family": "ViT-MAE",
        "sensor_support": ["Sentinel-2 RGB or multispectral/time-series variants in original paper"],
        "modality_scope": "multispectral and temporal optical imagery",
        "pretraining_signal": "masked autoencoding with temporal/spectral positional encoding",
        "temporal_modeling": "explicit temporal embeddings in the original paper; rs-embed adapter currently uses RGB composite path",
        "training_data_summary": "fMoW-Sentinel and satellite imagery with temporal and spectral structure",
        "architecture_notes": "extends MAE with spectral/temporal positional encodings and masking across temporal or spectral dimensions",
        "typical_tasks": ["classification", "segmentation", "transfer learning", "representation learning"],
    },
    "satmaepp": {
        "review_family": "Improved masked autoencoder for EO",
        "representation_mode": "ViT patch tokens",
        "backbone_family": "ViT-L / SatMAE++",
        "sensor_support": ["Sentinel-2 RGB in adapter", "multispectral Sentinel-2 in paper"],
        "modality_scope": "optical multispectral imagery",
        "pretraining_signal": "revised MAE pretraining for multispectral satellite imagery",
        "temporal_modeling": "single composited observation window in adapter",
        "training_data_summary": "fMoW RGB / multispectral and remote sensing pretraining corpora",
        "architecture_notes": "rethinks channel handling and pretraining settings for multispectral transformer pretraining",
        "typical_tasks": ["classification", "segmentation", "representation transfer"],
    },
    "satmaepp_s2_10b": {
        "review_family": "Grouped-channel multispectral masked autoencoder",
        "representation_mode": "ViT group-channel tokens",
        "backbone_family": "ViT-L / grouped-channel SatMAE++",
        "sensor_support": ["Sentinel-2 SR 10-band"],
        "modality_scope": "multispectral optical imagery",
        "pretraining_signal": "grouped-channel masked autoencoding",
        "temporal_modeling": "single composited observation window in adapter",
        "training_data_summary": "Sentinel/fMoW-style multispectral pretraining checkpoint",
        "architecture_notes": "uses three grouped channel branches to accommodate 10-band Sentinel-2 input",
        "typical_tasks": ["classification", "transfer learning", "representation extraction"],
    },
    "scalemae": {
        "review_family": "Scale-aware masked autoencoder",
        "representation_mode": "ViT patch tokens with scale token",
        "backbone_family": "ViT-L / MAE",
        "sensor_support": ["Sentinel-2 RGB in adapter", "multiscale EO imagery in paper"],
        "modality_scope": "optical imagery across resolutions",
        "pretraining_signal": "masked autoencoding with explicit resolution conditioning",
        "temporal_modeling": "single composited observation window",
        "training_data_summary": "multiscale geospatial imagery with explicit resolution metadata",
        "architecture_notes": "injects semantic scale/resolution into the encoder to reduce scale mismatch",
        "typical_tasks": ["cross-resolution transfer", "classification", "segmentation"],
    },
    "anysat": {
        "review_family": "Generalist multi-resolution multimodal EO encoder",
        "representation_mode": "dense / pooled feature grid",
        "backbone_family": "versatile JEPA-style EO encoder",
        "sensor_support": ["Sentinel-2", "Sentinel-1", "aerial/VHR and other modalities in original paper"],
        "modality_scope": "multimodal, multiresolution, temporal",
        "pretraining_signal": "self-supervised representation learning across many configurations",
        "temporal_modeling": "multi-frame optical sequence with date tokens",
        "training_data_summary": "GeoPlex-like multi-resolution multi-modality corpora",
        "architecture_notes": "designed to accept many resolutions, scales, and modalities within one encoder",
        "typical_tasks": ["classification", "segmentation", "cross-modal transfer", "few-shot transfer"],
    },
    "galileo": {
        "review_family": "Global-local multimodal time-series encoder",
        "representation_mode": "pooled and token embeddings",
        "backbone_family": "transformer with global/local branches",
        "sensor_support": ["Sentinel-2 time series", "multiple remote sensing modalities in original work"],
        "modality_scope": "multimodal time series",
        "pretraining_signal": "self-supervised multimodal representation learning",
        "temporal_modeling": "explicit month tokens and frame masks",
        "training_data_summary": "many remote sensing modalities with temporal alignment",
        "architecture_notes": "jointly learns local patch-level and global scene-level features",
        "typical_tasks": ["classification", "segmentation", "retrieval", "time-series transfer"],
    },
    "wildsat": {
        "review_family": "Remote sensing representation learning from weak labels",
        "representation_mode": "image-head features / token grid",
        "backbone_family": "ViT-B-16",
        "sensor_support": ["Sentinel-2 RGB", "wildlife observations as supervision"],
        "modality_scope": "optical imagery with biodiversity side labels",
        "pretraining_signal": "supervised / weakly supervised representation learning from wildlife observations",
        "temporal_modeling": "single composited optical patch",
        "training_data_summary": "satellite imagery aligned with wildlife observations and biodiversity labels",
        "architecture_notes": "learns satellite features from ecological observation signals rather than standard EO pretext tasks",
        "typical_tasks": ["ecology transfer", "classification", "retrieval", "representation learning"],
    },
    "prithvi": {
        "review_family": "Generalist geospatial foundation model",
        "representation_mode": "ViT tokens with time/location side inputs",
        "backbone_family": "ViT / masked autoencoder lineage",
        "sensor_support": ["HLS / Sentinel-Landsat style 6-band optical imagery"],
        "modality_scope": "optical imagery with temporal and geolocation side information",
        "pretraining_signal": "self-supervised geospatial pretraining",
        "temporal_modeling": "explicit temporal coordinates in adapter and paper family",
        "training_data_summary": "NASA/IBM geospatial corpora designed for generalist GeoAI",
        "architecture_notes": "time and geolocation are first-class side inputs in the encoder family",
        "typical_tasks": ["classification", "segmentation", "mapping", "generalist transfer"],
    },
    "terrafm": {
        "review_family": "Unified multisensor foundation model",
        "representation_mode": "shared encoder features",
        "backbone_family": "multisensor transformer",
        "sensor_support": ["Sentinel-2", "Sentinel-1"],
        "modality_scope": "optical + SAR",
        "pretraining_signal": "scalable unified multisensor pretraining",
        "temporal_modeling": "single observation window in current adapter; paper focuses on multisensor unification",
        "training_data_summary": "large multisensor Earth observation corpus spanning S1 and S2",
        "architecture_notes": "one foundation model for both optical and SAR inputs with modality routing",
        "typical_tasks": ["classification", "segmentation", "cross-sensor transfer", "representation learning"],
    },
    "terramind": {
        "review_family": "Generative multimodal EO foundation model",
        "representation_mode": "multimodal latent features",
        "backbone_family": "large-scale generative multimodal transformer",
        "sensor_support": ["Sentinel-2 in adapter", "wider multimodal EO stack in paper"],
        "modality_scope": "multimodal generative EO modeling",
        "pretraining_signal": "large-scale generative multimodal learning",
        "temporal_modeling": "single composited optical path in adapter",
        "training_data_summary": "large multimodal Earth observation data for generation and representation learning",
        "architecture_notes": "generative multimodality is central; rs-embed currently exposes the Sentinel-2 encoder path",
        "typical_tasks": ["representation learning", "generation", "multimodal transfer"],
    },
    "dofa": {
        "review_family": "Wavelength-aware multimodal foundation model",
        "representation_mode": "token embedding with wavelength side vector",
        "backbone_family": "transformer with neural plasticity / dynamic wavelength handling",
        "sensor_support": ["multispectral and hyperspectral style inputs", "Sentinel-2 in adapter"],
        "modality_scope": "multispectral / hyperspectral / multimodal",
        "pretraining_signal": "self-supervised multimodal EO foundation modeling",
        "temporal_modeling": "single observation window in adapter",
        "training_data_summary": "multimodal EO corpora with wavelength metadata",
        "architecture_notes": "explicitly consumes wavelength vectors, making it sensor-flexible",
        "typical_tasks": ["classification", "cross-sensor transfer", "hyperspectral transfer"],
    },
    "fomo": {
        "review_family": "Forest-oriented multimodal and multiscale foundation model",
        "representation_mode": "pooled or token embeddings",
        "backbone_family": "multimodal transformer / representation learner",
        "sensor_support": ["Sentinel-2 SR in adapter", "multiple scales and tasks in original work"],
        "modality_scope": "multimodal, multiscale, multitask",
        "pretraining_signal": "multi-task forest monitoring pretraining",
        "temporal_modeling": "single optical composite in adapter",
        "training_data_summary": "forest monitoring corpora across multiple modalities and scales",
        "architecture_notes": "injects modality keys for each channel and focuses on forest monitoring use cases",
        "typical_tasks": ["forest type mapping", "biomass-related transfer", "classification", "segmentation"],
    },
    "thor": {
        "review_family": "Versatile EO foundation model for climate and society",
        "representation_mode": "ViT embeddings",
        "backbone_family": "versatile transformer",
        "sensor_support": ["Sentinel-2 SR 10-band"],
        "modality_scope": "optical EO with broad application scope",
        "pretraining_signal": "foundation pretraining for climate and society applications",
        "temporal_modeling": "single optical composite in adapter",
        "training_data_summary": "large EO corpus oriented toward broad societal and climate tasks",
        "architecture_notes": "designed as a versatile base model rather than a task-specific agriculture or vision-language model",
        "typical_tasks": ["classification", "regression", "mapping", "broad transfer"],
    },
    "agrifm": {
        "review_family": "Agriculture-specific multi-source temporal foundation model",
        "representation_mode": "video Swin features",
        "backbone_family": "Video Swin Transformer",
        "sensor_support": ["Sentinel-2 in adapter", "Sentinel-2, Landsat-8/9, MODIS in original paper"],
        "modality_scope": "multisource temporal optical imagery",
        "pretraining_signal": "supervised land-cover fraction pretraining with EMA teacher",
        "temporal_modeling": "fixed-length multi-frame temporal stack",
        "training_data_summary": "25M+ globally sampled multi-source temporal patches from MODIS, Landsat, and Sentinel-2",
        "architecture_notes": "synchronized spatiotemporal downsampling is the core design idea for agriculture mapping",
        "typical_tasks": ["cropland mapping", "field boundary delineation", "crop type mapping", "agricultural land-use mapping"],
    },
    "satvision": {
        "review_family": "Coarse-resolution all-sky foundation model",
        "representation_mode": "Swin-based coarse-resolution features",
        "backbone_family": "SwinV2-style encoder",
        "sensor_support": ["MODIS 14-band TOA"],
        "modality_scope": "coarse-resolution all-sky optical/thermal imagery",
        "pretraining_signal": "foundation pretraining on all-sky MODIS TOA data",
        "temporal_modeling": "single coarse-resolution observation window in adapter",
        "training_data_summary": "14-band MODIS TOA imagery capturing visible, NIR, and thermal bands under all-sky conditions",
        "architecture_notes": "extends remote sensing foundation modeling beyond cloud-free, fine-resolution optical imagery",
        "typical_tasks": ["atmospheric science", "environmental monitoring", "coarse-resolution transfer"],
    },
}


SURVEY_PAPERS = [
    {
        "title": "AI Foundation Models in Remote Sensing: A Survey",
        "year": 2024,
        "url": "https://arxiv.org/abs/2408.03464",
        "focus": "broad remote sensing foundation models overview with sections on data, methods, tasks, and open challenges",
        "takeaway_for_this_project": "use a full-stack survey pattern but narrow the core object from general foundation models to satellite embeddings",
    },
    {
        "title": "Advances on Multimodal Remote Sensing Foundation Models for Earth Observation Downstream Tasks: A Survey",
        "year": 2025,
        "url": "https://www.mdpi.com/2072-4292/17/21/3532",
        "focus": "downstream-task-centric survey that emphasizes multimodality, task grouping, and benchmarking",
        "takeaway_for_this_project": "the application section should be task-centric rather than model-centric",
    },
    {
        "title": "When Remote Sensing Meets Foundation Models: Concepts, Data, and Applications",
        "year": 2025,
        "url": "https://www.mdpi.com/2072-4292/17/2/179",
        "focus": "conceptual taxonomy plus data/method/application organization",
        "takeaway_for_this_project": "put concepts and taxonomy before individual models, and separate representation formation from application deployment",
    },
    {
        "title": "A Survey on Remote Sensing Foundation Models: From Vision to Multimodality",
        "year": 2025,
        "url": "https://arxiv.org/abs/2503.22081",
        "focus": "modality-aware organization from vision-only to multimodal generalist EO models",
        "takeaway_for_this_project": "classify satellite embeddings by both model design axis and data/modality axis",
    },
]


def _clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


AUTHOR_NAME_RE = re.compile(
    r"[A-Z][A-Za-z'`\-]+(?:\s+(?:[A-Z]\.|[A-Z][A-Za-z'`\-]+)){1,3}"
)

NON_AUTHOR_HINTS = (
    "foundation model",
    "remote sensing",
    "earth observation",
    "satellite imagery",
    "multispectral",
    "multi-spectral",
    "embedding",
    "representation",
    "analysis",
    "pre-training",
    "transformers",
    "learning",
    "imagery",
    "introduce",
    "present",
    "propose",
    "demonstrate",
    "however",
    "in this paper",
    "sample spectral hypernet",
    "dynamic patch embedding",
    "spectral variable",
)

AFFILIATION_HINTS = (
    "university",
    "institute",
    "school",
    "department",
    "laboratory",
    "lab",
    "research",
    "google deepmind",
    "google",
    "ibm",
    "nasa",
    "nvidia",
    "technical university",
    "center",
    "centre",
    "academy",
)


def _strip_md_prefix(line: str) -> str:
    s = line.strip()
    s = re.sub(r"^#+\s*", "", s)
    s = re.sub(r"^>\s*", "", s)
    if s.startswith("*") and s.endswith("*") and len(s) > 2:
        s = s[1:-1].strip()
    return s


def _normalize_author_text(text: str) -> str:
    text = _strip_md_prefix(text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"\b(Member|Senior Member),\s*IEEE\b", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"[†‡∗*©]", " ", text)
    text = re.sub(r"(?<=\D)\d+(?:,\d+)*", " ", text)
    text = re.sub(r"\bEqual contribution[s]?\b.*", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\bCorresponding author[s]?\b.*", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+(?:and|&)\s+", ", ", text)
    text = re.sub(r"[;|]+", ", ", text)
    text = re.sub(r"\s*,\s*", ", ", text)
    return _clean_text(text).strip(", ")


def _looks_like_affiliation(text: str) -> bool:
    lower = text.lower()
    return any(token in lower for token in AFFILIATION_HINTS)


def _looks_like_non_author_text(text: str) -> bool:
    lower = text.lower()
    return any(token in lower for token in NON_AUTHOR_HINTS)


def _extract_names(text: str) -> str:
    cleaned = _normalize_author_text(text)
    names = []
    seen = set()
    for match in AUTHOR_NAME_RE.finditer(cleaned):
        name = _clean_text(match.group(0)).strip(", ")
        if _looks_like_affiliation(name) or _looks_like_non_author_text(name):
            continue
        if len(name.split()) < 2:
            continue
        if name not in seen:
            seen.add(name)
            names.append(name)
    if names:
        return ", ".join(names)
    return cleaned


def _is_author_line(text: str) -> bool:
    candidate = _strip_md_prefix(text)
    lower = candidate.lower()
    if not candidate:
        return False
    if lower == "abstract":
        return False
    if re.fullmatch(r"\d{4}-\d{1,2}-\d{1,2}", candidate):
        return False
    if "arxiv:" in lower:
        return False
    if _looks_like_affiliation(candidate):
        return False
    if _looks_like_non_author_text(candidate):
        return False
    return len(AUTHOR_NAME_RE.findall(_normalize_author_text(candidate))) >= 1


def _extract_authors(model_id: str, md_text: str) -> str:
    if model_id in AUTHOR_OVERRIDES:
        return AUTHOR_OVERRIDES[model_id]

    author_match = re.search(r'^authors:\s*"(.+?)"\s*$', md_text, re.MULTILINE)
    if author_match and _is_author_line(author_match.group(1)):
        return _extract_names(author_match.group(1))

    lines = md_text.splitlines()
    title_seen = False
    author_lines: list[str] = []
    for raw in lines[:80]:
        s = _strip_md_prefix(raw)
        lower = s.lower()
        if not s or s == "---":
            continue
        if lower.startswith("title:"):
            continue
        if raw.startswith("# "):
            title_seen = True
            continue
        if not title_seen:
            continue
        if re.match(r"^(abstract|introduction|\d+\.?\s+introduction|\d+\.?\s*$)", lower):
            break
        if _is_author_line(s):
            author_lines.append(s)
            continue
        if author_lines:
            break
    if author_lines:
        return _extract_names(" ".join(author_lines))
    return ""


def _extract_abstract(md_text: str) -> str:
    lines = md_text.splitlines()
    in_abstract = False
    chunks: list[str] = []
    for raw in lines:
        s = _strip_md_prefix(raw)
        lower = s.lower()
        if not in_abstract:
            if lower == "abstract":
                in_abstract = True
            continue
        if re.match(r"^(introduction|\d+\.?\s+introduction|\d+\.?\s*$)", lower):
            break
        if not s:
            continue
        if s.lower().startswith(("figure ", "table ")):
            continue
        if len(s) < 40 and not s.endswith("."):
            continue
        chunks.append(s)
    if chunks:
        return _clean_text(" ".join(chunks))

    m = re.search(
        r"(?:## Abstract|> Abstract|Abstract[—-])\s*(.+?)(?=\n## |\n> \d+\.\s|\n## \d+ |\nI\. |\n1 Introduction|\n## 1 )",
        md_text,
        re.DOTALL,
    )
    if m:
        return _clean_text(m.group(1))
    return ""


def _extract_benchmark_meta() -> dict[str, dict]:
    benchmark = json.loads(BENCHMARK_PATH.read_text(encoding="utf-8"))
    out: dict[str, dict] = {}
    for row in benchmark["results"]:
        out[row["model"]] = {
            "shape": row.get("shape"),
            "elapsed_s": row.get("elapsed_s"),
            "peak_mem_mb": row.get("peak_mem_mb"),
            "benchmark_note": row.get("note"),
        }
    return out


def _build_records() -> list[dict]:
    inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))["models"]
    bench = _extract_benchmark_meta()
    records: list[dict] = []
    for m in inventory:
        model_id = m["model_id"]
        paper_path = PROCESSED_PATHS.get(model_id)
        md_text = paper_path.read_text(encoding="utf-8", errors="ignore") if paper_path and paper_path.exists() else ""
        authors = _extract_authors(model_id, md_text)
        abstract = _extract_abstract(md_text)
        pub = m["source_publication"]
        rec = {
            **m,
            **ENRICHMENTS.get(model_id, {}),
            "paper_authors": authors,
            "abstract_excerpt": abstract,
            "processed_paper_path": str(paper_path.relative_to(ROOT)) if paper_path and paper_path.exists() else None,
            "benchmark_summary": bench.get(model_id, {}),
        }
        # Stable short classification used in the review and UI.
        rec["taxonomy_labels"] = [
            rec.get("type", ""),
            rec.get("review_family", ""),
            rec.get("modality_scope", ""),
            rec.get("backbone_family", ""),
        ]
        pub["authors"] = authors
        records.append(rec)
    return records


def _write_json(records: list[dict]) -> None:
    out = {
        "title": "Satellite Embedding Model Dossier",
        "record_count": len(records),
        "records": records,
        "survey_precedents": SURVEY_PAPERS,
    }
    (DATA_DIR / "model_dossier.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _write_bib(records: list[dict]) -> None:
    lines = []
    for rec in records:
        pub = rec["source_publication"]
        key = rec["model_id"].replace("-", "")
        title = pub["title"].replace("{", "").replace("}", "").replace("&", r"\&")
        authors = rec["paper_authors"] or "Unknown"
        bib_authors = " and ".join(part.strip() for part in authors.split(",") if part.strip()) or "Unknown"
        year = pub["year"]
        url = pub["paper_url"]
        lines.append(
            "\n".join(
                [
                    f"@misc{{{key},",
                    f"  title = {{{title}}},",
                    f"  author = {{{bib_authors}}},",
                    f"  year = {{{year}}},",
                    f"  url = {{{url}}},",
                    "}",
                ]
            )
        )
    for i, survey in enumerate(SURVEY_PAPERS, start=1):
        key = f"survey{i}"
        title = survey["title"].replace("{", "").replace("}", "").replace("&", r"\&")
        lines.append(
            "\n".join(
                [
                    f"@misc{{{key},",
                    f"  title = {{{title}}},",
                    "  author = {{Unknown}},",
                    f"  year = {{{survey['year']}}},",
                    f"  url = {{{survey['url']}}},",
                    "}",
                ]
            )
        )
    (PAPER_DIR / "references.bib").write_text("\n\n".join(lines) + "\n", encoding="utf-8")


def _latex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "°": r"\textdegree{}",
    }
    out = text
    for old, new in replacements.items():
        out = out.replace(old, new)
    return out


def _format_table_value(value: object) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, list):
        value = ", ".join(str(v) for v in value)
    text = _clean_text(str(value)).replace("`", "")
    if not text:
        return "n/a"
    return _latex_escape(text)


def _compact_resolution(text: str) -> str:
    text = _clean_text(text).replace("`", "")
    text = re.sub(r"\([^)]*[=_][^)]*\)", "", text)
    text = text.replace("provider default", "")
    text = re.sub(r"\s+", " ", text)
    text = text.replace(" on ", "; ")
    return text.strip(" ;")


def _compact_time_coverage(text: str) -> str:
    text = _clean_text(text).replace("`", "")
    text = text.replace("No fixed product window in rs-embed; ", "")
    text = text.replace("user-specified range over ", "")
    text = text.replace("provider path uses ", "")
    text = text.replace("provider path requires ", "")
    text = text.replace("range preferred over ", "")
    text = text.replace("unless overridden", "")
    text = text.replace("TemporalSpec.range(...)", "range(...)")
    text = text.replace("COPERNICUS/S2_SR_HARMONIZED", "S2_SR_HARMONIZED")
    text = re.sub(r"\s+", " ", text)
    return text.strip(" ;")


def _short_link_label(url: str) -> str:
    if not url:
        return "n/a"
    host = (urlparse(url).netloc or "").lower()
    if "github.com" in host:
        return "GitHub"
    if "huggingface.co" in host:
        return "Hugging Face"
    if "developers.google.com" in host:
        return "Earth Engine catalog"
    if host.startswith("www."):
        host = host[4:]
    return host or "link"


def _write_latex_model_table(records: list[dict]) -> None:
    lines = [
        r"\begin{landscape}",
        r"\scriptsize",
        r"\setlength{\LTleft}{0pt}",
        r"\setlength{\LTright}{0pt}",
        r"\setlength{\tabcolsep}{3pt}",
        r"\renewcommand{\arraystretch}{1.15}",
        r"\begin{longtable}{p{1.45cm}p{0.75cm}p{1.2cm}p{0.95cm}p{2.25cm}p{2.05cm}p{2.75cm}p{2.35cm}p{2.25cm}p{1.55cm}p{3.0cm}}",
        r"\caption{Comprehensive model summary for the \modelcount{} canonical satellite embedding models currently exposed in \texttt{rs-embed}. The table emphasizes deployment-relevant details rather than only benchmark scores.}\label{tab:model-catalog}\\",
        r"\toprule",
        r"Model & Year & Venue & Type & Family & Backbone & Sensors / data & Resolution & Temporal semantics & Emb. / output & Pretraining signal \\",
        r"\midrule",
        r"\endfirsthead",
        r"\caption[]{Comprehensive model summary for the canonical \texttt{rs-embed} model set (continued).}\\",
        r"\toprule",
        r"Model & Year & Venue & Type & Family & Backbone & Sensors / data & Resolution & Temporal semantics & Emb. / output & Pretraining signal \\",
        r"\midrule",
        r"\endhead",
        r"\bottomrule",
        r"\endfoot",
    ]

    for rec in records:
        pub = rec["source_publication"]
        shape = rec.get("benchmark_summary", {}).get("shape") or []
        emb_dim = shape[-1] if shape else "n/a"
        emb_output = f"{emb_dim}; {', '.join(rec.get('output_modes', [])) or 'n/a'}"
        resolution = _compact_resolution(rec.get("stated_resolution", ""))
        row = [
            _format_table_value(rec["model_id"]),
            _format_table_value(pub["year"]),
            _format_table_value(pub["venue"]),
            _format_table_value(rec.get("type")),
            _format_table_value(rec.get("review_family")),
            _format_table_value(rec.get("backbone_family")),
            _format_table_value(rec.get("sensor_support")),
            _format_table_value(resolution),
            _format_table_value(rec.get("temporal_modeling")),
            _format_table_value(emb_output),
            _format_table_value(rec.get("pretraining_signal")),
        ]
        lines.append(" & ".join(row) + r" \\")

    lines.extend(
        [
            r"\end{longtable}",
            r"\normalsize",
            r"\end{landscape}",
        ]
    )
    (TABLES_DIR / "model_catalog_longtable.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_latex_appendix_table(records: list[dict]) -> None:
    lines = [
        r"\begin{landscape}",
        r"\scriptsize",
        r"\setlength{\LTleft}{0pt}",
        r"\setlength{\LTright}{0pt}",
        r"\setlength{\tabcolsep}{3pt}",
        r"\renewcommand{\arraystretch}{1.12}",
        r"\begin{longtable}{p{1.35cm}p{2.9cm}p{2.25cm}p{1.95cm}p{1.65cm}p{2.3cm}p{1.45cm}p{1.35cm}p{2.7cm}p{1.95cm}}",
        r"\caption{Extended implementation-oriented inventory for the canonical \texttt{rs-embed} model set. This appendix table adds authorship, output modes, application hints, and runtime metadata beyond the main-text catalog.}\label{tab:model-appendix-catalog}\\",
        r"\toprule",
        r"Model & Authors & Inputs / modalities & Time coverage & Outputs & Typical tasks & Elapsed (s) & Peak GPU (MB) & Code / artifact & Training data summary \\",
        r"\midrule",
        r"\endfirsthead",
        r"\caption[]{Extended implementation-oriented inventory for the canonical \texttt{rs-embed} model set (continued).}\\",
        r"\toprule",
        r"Model & Authors & Inputs / modalities & Time coverage & Outputs & Typical tasks & Elapsed (s) & Peak GPU (MB) & Code / artifact & Training data summary \\",
        r"\midrule",
        r"\endhead",
        r"\bottomrule",
        r"\endfoot",
    ]

    for rec in records:
        bench = rec.get("benchmark_summary", {})
        code_or_artifact = rec.get("code_repo_url") or rec.get("artifact_or_model_hub_url") or "n/a"
        time_cov = rec.get("stated_time_coverage") or rec.get("temporal_semantics") or "n/a"
        elapsed = f"{bench.get('elapsed_s', 'n/a'):.2f}" if isinstance(bench.get("elapsed_s"), (int, float)) else "n/a"
        peak = f"{bench.get('peak_mem_mb', 'n/a'):.1f}" if isinstance(bench.get("peak_mem_mb"), (int, float)) else "n/a"
        link_label = _short_link_label(code_or_artifact)
        row = [
            _format_table_value(rec.get("model_id")),
            _format_table_value(rec.get("paper_authors")),
            _format_table_value(rec.get("sensor_support")),
            _format_table_value(_compact_time_coverage(time_cov)),
            _format_table_value(rec.get("output_modes")),
            _format_table_value(rec.get("typical_tasks")),
            _format_table_value(elapsed),
            _format_table_value(peak),
            _format_table_value(link_label),
            _format_table_value(rec.get("training_data_summary")),
        ]
        lines.append(" & ".join(row) + r" \\")

    lines.extend(
        [
            r"\end{longtable}",
            r"\normalsize",
            r"\end{landscape}",
        ]
    )
    (TABLES_DIR / "model_catalog_appendix_longtable.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_markdown(records: list[dict]) -> None:
    lines = []
    lines.append("# Satellite Embedding Model Dossier\n")
    lines.append(
        "This dossier consolidates the 19 canonical `rs-embed` models into a review-ready reference. "
        "It combines local adapter docs, local processed paper text, and first-pass survey taxonomy fields.\n"
    )
    lines.append("## Survey precedents used for the article structure\n")
    lines.append("| Survey | Year | Why it matters for this review | Link |")
    lines.append("|---|---:|---|---|")
    for s in SURVEY_PAPERS:
        lines.append(f"| {s['title']} | {s['year']} | {s['takeaway_for_this_project']} | {s['url']} |")

    lines.append("\n## Unified taxonomy table\n")
    lines.append(
        "| Model | Year | Venue | Type | Family | Modality | Backbone | Resolution | Temporal modeling | Embedding dim |"
    )
    lines.append("|---|---:|---|---|---|---|---|---|---|---:|")
    for rec in records:
        pub = rec["source_publication"]
        shape = rec.get("benchmark_summary", {}).get("shape") or []
        emb_dim = shape[0] if shape else "n/a"
        lines.append(
            "| {model} | {year} | {venue} | {typ} | {family} | {modality} | {backbone} | {resolution} | {temporal} | {dim} |".format(
                model=rec["model_id"],
                year=pub["year"],
                venue=pub["venue"],
                typ=rec["type"],
                family=rec.get("review_family", ""),
                modality=rec.get("modality_scope", ""),
                backbone=rec.get("backbone_family", ""),
                resolution=rec["stated_resolution"],
                temporal=rec.get("temporal_modeling", ""),
                dim=emb_dim,
            )
        )

    lines.append("\n## Per-model notes\n")
    for rec in records:
        pub = rec["source_publication"]
        bench = rec.get("benchmark_summary", {})
        lines.append(f"### {rec['model_id']}\n")
        lines.append(f"- Publication: {pub['title']} ({pub['venue']} {pub['year']})")
        if rec.get("paper_authors"):
            lines.append(f"- Authors: {rec['paper_authors']}")
        lines.append(f"- Review family: {rec.get('review_family', '')}")
        lines.append(f"- Adapter type in rs-embed: {rec['type']} via `{rec['adapter_module']}.{rec['adapter_class']}`")
        lines.append(f"- Spatial resolution / scale: {rec['stated_resolution']}")
        lines.append(f"- Time coverage / semantics: {rec['stated_time_coverage']}; {rec['temporal_semantics']}")
        lines.append(f"- Supported sensors / modalities: {', '.join(rec.get('sensor_support', []))}")
        lines.append(f"- Backbone / architecture: {rec.get('backbone_family', '')}")
        lines.append(f"- Pretraining / learning signal: {rec.get('pretraining_signal', '')}")
        lines.append(f"- Training data summary: {rec.get('training_data_summary', '')}")
        lines.append(f"- Representation mode: {rec.get('representation_mode', '')}")
        lines.append(f"- Output modes in rs-embed: {', '.join(rec['output_modes'])}")
        lines.append(f"- Typical downstream tasks: {', '.join(rec.get('typical_tasks', []))}")
        if bench.get("shape"):
            lines.append(
                f"- Verified rs-embed output: shape={bench['shape']}, elapsed={bench['elapsed_s']} s, peak GPU={bench['peak_mem_mb']} MB"
            )
        lines.append(f"- Code: {rec.get('code_repo_url') or 'n/a'}")
        lines.append(f"- Paper: {pub['paper_url']}")
        if rec.get("artifact_or_model_hub_url"):
            lines.append(f"- Model / artifact hub: {rec['artifact_or_model_hub_url']}")
        if rec.get("processed_paper_path"):
            lines.append(f"- Local paper note: `{rec['processed_paper_path']}`")
        if rec.get("architecture_notes"):
            lines.append(f"- Architecture note: {rec['architecture_notes']}")
        if rec.get("abstract_excerpt"):
            lines.append(f"- Abstract snapshot: {rec['abstract_excerpt'][:800]}...")
        if rec.get("notes"):
            for note in rec["notes"]:
                lines.append(f"- Adapter note: {note}")
        lines.append("")

    (SURVEY_DIR / "MODEL_DOSSIER.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    records = _build_records()
    _write_json(records)
    _write_bib(records)
    _write_markdown(records)
    _write_latex_model_table(records)
    _write_latex_appendix_table(records)
    print(f"Wrote {len(records)} records to {DATA_DIR}")


if __name__ == "__main__":
    main()
