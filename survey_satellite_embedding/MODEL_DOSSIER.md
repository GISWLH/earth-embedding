# Satellite Embedding Model Dossier

This dossier consolidates the 19 canonical `rs-embed` models into a review-ready reference. It combines local adapter docs, local processed paper text, and first-pass survey taxonomy fields.

## Survey precedents used for the article structure

| Survey | Year | Why it matters for this review | Link |
|---|---:|---|---|
| AI Foundation Models in Remote Sensing: A Survey | 2024 | use a full-stack survey pattern but narrow the core object from general foundation models to satellite embeddings | https://arxiv.org/abs/2408.03464 |
| Advances on Multimodal Remote Sensing Foundation Models for Earth Observation Downstream Tasks: A Survey | 2025 | the application section should be task-centric rather than model-centric | https://www.mdpi.com/2072-4292/17/21/3532 |
| When Remote Sensing Meets Foundation Models: Concepts, Data, and Applications | 2025 | put concepts and taxonomy before individual models, and separate representation formation from application deployment | https://www.mdpi.com/2072-4292/17/2/179 |
| A Survey on Remote Sensing Foundation Models: From Vision to Multimodality | 2025 | classify satellite embeddings by both model design axis and data/modality axis | https://arxiv.org/abs/2503.22081 |

## Unified taxonomy table

| Model | Year | Venue | Type | Family | Modality | Backbone | Resolution | Temporal modeling | Embedding dim |
|---|---:|---|---|---|---|---|---|---|---:|
| tessera | 2026 | CVPR | precomputed | Precomputed temporal embedding field | single-modality spectral-temporal product | field model over surface spectra embeddings | 10 m precomputed embedding tiles | annual lookup over product years | 128 |
| gse | 2025 | arXiv | precomputed | Precomputed annual embedding product | single product | embedding field model | 10 m annual embedding product | strict yearly product | 64 |
| copernicus | 2025 | ICCV | precomputed | Precomputed foundation map | multisource product collapsed into a 2021 embedding map | Copernicus foundation model product | 0.25° precomputed grid | static in current adapter (2021 only) | 768 |
| remoteclip | 2024 | IEEE TGRS | on-the-fly | Vision-language satellite embedding | vision-language | CLIP / ViT-B-32 | 10 m provider default (`SensorSpec.scale_m=10`) on Sentinel-2 RGB | single composited observation window at inference | 768 |
| satmae | 2022 | NeurIPS | on-the-fly | Masked autoencoder for temporal or multispectral EO | multispectral and temporal optical imagery | ViT-MAE | 10 m provider default on Sentinel-2 RGB | explicit temporal embeddings in the original paper; rs-embed adapter currently uses RGB composite path | 1024 |
| satmaepp | 2024 | CVPR | on-the-fly | Improved masked autoencoder for EO | optical multispectral imagery | ViT-L / SatMAE++ | 10 m provider default on Sentinel-2 RGB | single composited observation window in adapter | 1024 |
| satmaepp_s2_10b | 2024 | CVPR | on-the-fly | Grouped-channel multispectral masked autoencoder | multispectral optical imagery | ViT-L / grouped-channel SatMAE++ | 10 m provider default on Sentinel-2 SR 10-band input | single composited observation window in adapter | 1024 |
| scalemae | 2023 | ICCV | on-the-fly | Scale-aware masked autoencoder | optical imagery across resolutions | ViT-L / MAE | 10 m provider default on Sentinel-2 RGB, plus explicit semantic scale input | single composited observation window | 1024 |
| anysat | 2025 | CVPR | on-the-fly | Generalist multi-resolution multimodal EO encoder | multimodal, multiresolution, temporal | versatile JEPA-style EO encoder | 10 m Sentinel-2 time-series input; default per-frame resize 24 px | multi-frame optical sequence with date tokens | 768 |
| galileo | 2025 | ICML | on-the-fly | Global-local multimodal time-series encoder | multimodal time series | transformer with global/local branches | 10 m Sentinel-2 time-series input; default frame size 64 px, patch size 8 | explicit month tokens and frame masks | 128 |
| wildsat | 2025 | ICCV | on-the-fly | Remote sensing representation learning from weak labels | optical imagery with biodiversity side labels | ViT-B-16 | 10 m provider default on Sentinel-2 RGB | single composited optical patch | 256 |
| prithvi | 2023 | arXiv | on-the-fly | Generalist geospatial foundation model | optical imagery with temporal and geolocation side information | ViT / masked autoencoder lineage | 30 m provider default in current adapter (`DEFAULT_IMAGE_SCALE_M=30`) on Sentinel-2 6-band input | explicit temporal coordinates in adapter and paper family | 768 |
| terrafm | 2026 | ICLR | on-the-fly | Unified multisensor foundation model | optical + SAR | multisensor transformer | 10 m provider default for both S2 and S1 paths; image resized to 224 px | single observation window in current adapter; paper focuses on multisensor unification | 768 |
| terramind | 2025 | ICCV | on-the-fly | Generative multimodal EO foundation model | multimodal generative EO modeling | large-scale generative multimodal transformer | 10 m provider default on Sentinel-2 SR 12-band input; image resized to 224 px | single composited optical path in adapter | 384 |
| dofa | 2024 | arXiv | on-the-fly | Wavelength-aware multimodal foundation model | multispectral / hyperspectral / multimodal | transformer with neural plasticity / dynamic wavelength handling | 10 m provider default for S2 path; fixed resize to 224 px | single observation window in adapter | 768 |
| fomo | 2025 | AAAI | on-the-fly | Forest-oriented multimodal and multiscale foundation model | multimodal, multiscale, multitask | multimodal transformer / representation learner | 10 m provider default on Sentinel-2 SR 12-band input; default image size 64 px | single optical composite in adapter | 768 |
| thor | 2026 | arXiv | on-the-fly | Versatile EO foundation model for climate and society | optical EO with broad application scope | versatile transformer | 10 m provider default on Sentinel-2 SR 10-band input; default image size 288 px | single optical composite in adapter | 768 |
| agrifm | 2026 | Remote Sensing of Environment | on-the-fly | Agriculture-specific multi-source temporal foundation model | multisource temporal optical imagery | Video Swin Transformer | 10 m Sentinel-2 time-series input; default image size 224 px with fixed T-frame packaging | fixed-length multi-frame temporal stack | 1024 |
| satvision | 2024 | arXiv | on-the-fly | Coarse-resolution all-sky foundation model | coarse-resolution all-sky optical/thermal imagery | SwinV2-style encoder | 1000 m provider default (`SensorSpec.scale_m=1000`) on 14-channel TOA input | single coarse-resolution observation window in adapter | 4096 |

## Per-model notes

### tessera

- Publication: Temporal Embeddings of Surface Spectra for Earth Representation and Analysis (CVPR 2026)
- Authors: Zhengpeng Feng, Clement Atzberger, Sadiq Jaffer, Jovana Knezevic, Silja Sormunen, Robin Young, Madeline C. Lisaius, Markus Immitzer, James Ball, David A. Coomes, Anil Madhavapeddy, Andrew Blake, Srinivasan Keshav
- Review family: Precomputed temporal embedding field
- Adapter type in rs-embed: precomputed via `precomputed_tessera.TesseraEmbedder`
- Spatial resolution / scale: 10 m precomputed embedding tiles
- Time coverage / semantics: 2017-2025; Year-like lookup. `TemporalSpec.year(...)` selects that year; `TemporalSpec.range(start, end)` falls back to the start year; not scene-level temporal filtering.
- Supported sensors / modalities: surface spectra product
- Backbone / architecture: field model over surface spectra embeddings
- Pretraining / learning signal: embedding field regression / product training
- Training data summary: global Earth observation spectra aggregated into tessellated embedding tiles
- Representation mode: precomputed dense embedding tiles
- Output modes in rs-embed: pooled, grid
- Typical downstream tasks: representation lookup, regional embedding analysis, retrieval, downstream transfer
- Verified rs-embed output: shape=[128], elapsed=1025.79 s, peak GPU=0.0 MB
- Code: https://github.com/ucam-eo/geotessera
- Paper: https://arxiv.org/abs/2506.20380v4
- Local paper note: `research_outputs/papers/processed/tessera/temporal-embeddings-of-surface-spectra-for-earth-representation-and-analysis.md`
- Architecture note: not an on-the-fly neural encoder inside rs-embed; uses GeoTessera runtime for tile lookup and crop
- Adapter note: Adapter expects `backend="auto"` (legacy `local` accepted).
- Adapter note: Strict tile mosaic/crop compatibility is required.

### gse

- Publication: An embedding field model for accurate and efficient global mapping from sparse label data (arXiv 2025)
- Authors: Christopher F. Brown, Michal R. Kazmierski, Valerie J. Pasquarella, William J. Rucklidge, Masha Samsikova, Chenhui Zhang, Evan Shelhamer, Estefania Lahera, Olivia Wiles, Simon Ilyushchenko, Noel Gorelick, Lihui Lydia Zhang, Sophia Alj, Emily Schechter, Sean Askay, Oliver Guinan, Rebecca Moore, Alexis Boukouvalas, Pushmeet Kohli
- Review family: Precomputed annual embedding product
- Adapter type in rs-embed: precomputed via `precomputed_gse_annual.GSEAnnualEmbedder`
- Spatial resolution / scale: 10 m annual embedding product
- Time coverage / semantics: 2017-2024; Strict annual product. Adapter requires `TemporalSpec.year(...)`; `range(...)` is not supported in v0.1.
- Supported sensors / modalities: Google Satellite Embedding annual product
- Backbone / architecture: embedding field model
- Pretraining / learning signal: global embedding field learning from sparse labels
- Training data summary: global annual satellite embedding product served through Earth Engine
- Representation mode: precomputed annual field
- Output modes in rs-embed: pooled, grid
- Typical downstream tasks: global mapping, rapid transfer, feature sampling
- Verified rs-embed output: shape=[64], elapsed=4.46 s, peak GPU=0.0 MB
- Code: n/a
- Paper: https://arxiv.org/abs/2507.22291
- Model / artifact hub: https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL
- Local paper note: `research_outputs/papers/processed/gse/an-embedding-field-model-for-accurate-and-efficient-global-mapping-from-sparse-label-data.md`
- Architecture note: adapter samples from an external yearly embedding product rather than running a neural encoder locally
- Adapter note: `OutputSpec.scale_m` controls provider sampling scale.

### copernicus

- Publication: Towards a Unified Copernicus Foundation Model for Earth Vision (ICCV 2025)
- Authors: Yi Wang, Zhitong Xiong, Chenying Liu, Adam J. Stewart, Thomas Dujardin, Nikolaos Ioannis Bountos, Angelos Zavras, Franziska Gerken, Ioannis Papoutsis, Laura Leal-Taixe, Xiao Xiang Zhu
- Review family: Precomputed foundation map
- Adapter type in rs-embed: precomputed via `precomputed_copernicus_embed.CopernicusEmbedder`
- Spatial resolution / scale: 0.25° precomputed grid
- Time coverage / semantics: 2021 only; Strict 2021-only precomputed product in current adapter; effectively a year gate rather than dynamic temporal retrieval.
- Supported sensors / modalities: Copernicus product stack
- Backbone / architecture: Copernicus foundation model product
- Pretraining / learning signal: foundation model pretraining followed by product distillation
- Training data summary: global Copernicus-scale EO data compiled into a unified feature raster
- Representation mode: precomputed GeoTIFF feature map
- Output modes in rs-embed: pooled, grid
- Typical downstream tasks: broad-area retrieval, feature extraction, downstream transfer
- Verified rs-embed output: shape=[768], elapsed=11.52 s, peak GPU=0.0 MB
- Code: n/a
- Paper: https://arxiv.org/abs/2503.11849
- Model / artifact hub: https://huggingface.co/datasets/torchgeo/copernicus_embed
- Local paper note: `research_outputs/papers/processed/copernicus/towards-a-unified-copernicus-foundation-model-for-earth-vision.md`
- Architecture note: rs-embed reads local slices from a precomputed embedding GeoTIFF
- Abstract snapshot: Advances in Earth observation (EO) foundation models have unlocked the potential of big satellite data to learn generic representations from space, benefiting a wide range of downstream applications crucial to our planet. However, most existing efforts remain limited to fixed spectral sensors, focus solely on the Earth’s surface, and overlook valuable metadata beyond imagery. In this work, we take a step towards next-generation EO foundation models with three key components: 1) Copernicus-Pretrain, a massivescale pretraining dataset that integrates 18.7M aligned images from all major Copernicus Sentinel missions, spanning from the Earth’s surface to its atmosphere; 2) CopernicusFM, a unified foundation model capable of processing any spectral or non-spectral sensor modality using extended ...
- Adapter note: Adapter expects `backend="auto"`.
- Adapter note: ROIs smaller than a single Copernicus pixel raise an error.

### remoteclip

- Publication: A Vision Language Foundation Model for Remote Sensing (IEEE TGRS 2024)
- Authors: Fan Liu, Delong Chen, Zhangqingyun Guan, Xiaocong Zhou, Jiale Zhu, Qiaolin Ye, Liyong Fu, Jun Zhou
- Review family: Vision-language satellite embedding
- Adapter type in rs-embed: on-the-fly via `onthefly_remoteclip.RemoteCLIPS2RGBEmbedder`
- Spatial resolution / scale: 10 m provider default (`SensorSpec.scale_m=10`) on Sentinel-2 RGB
- Time coverage / semantics: No fixed product window in rs-embed; user-specified range over `COPERNICUS/S2_SR_HARMONIZED`; Requires `TemporalSpec.range(...)`. Range defines imagery filter/composite window (default `median`), not a single-scene acquisition selector.
- Supported sensors / modalities: Sentinel-2 RGB, remote sensing captions, UAV imagery in pretraining
- Backbone / architecture: CLIP / ViT-B-32
- Pretraining / learning signal: contrastive image-text alignment (InfoNCE)
- Training data summary: large image-caption corpus built via box-to-caption and mask-to-caption conversion plus UAV imagery
- Representation mode: joint image-text embedding
- Output modes in rs-embed: pooled, grid
- Typical downstream tasks: zero-shot classification, retrieval, few-shot classification, counting, open-vocabulary transfer
- Verified rs-embed output: shape=[768], elapsed=13.87 s, peak GPU=600.8 MB
- Code: https://github.com/ChenDelong1999/RemoteCLIP
- Paper: https://arxiv.org/abs/2306.11029
- Model / artifact hub: https://huggingface.co/MVRL/remote-clip-vit-base-patch32
- Local paper note: `research_outputs/papers/processed/remoteclip/a-vision-language-foundation-model-for-remote-sensing.md`
- Architecture note: CLIP-style dual encoder specialized for remote sensing semantics and zero-shot transfer
- Abstract snapshot: General-purpose foundation models have led to recent breakthroughs in artificial intelligence. In remote sensing, self-supervised learning (SSL) and Masked Image Modeling (MIM) have been adopted to build foundation models. However, these models primarily learn low-level features and require annotated data for fine-tuning. Moreover, they are inapplicable for retrieval and zero-shot applications due to the lack of language understanding. To address these limitations, we propose RemoteCLIP, the first vision-language foundation model for remote sensing that aims to learn robust visual features with rich semantics and aligned text embeddings for seamless downstream application. To address the scarcity of pre-training data, we leverage data scaling which converts heterogeneous annotations into a...
- Adapter note: `grid` is a ViT patch-token grid, not a georeferenced raster.

### satmae

- Publication: Pre-training Transformers for Temporal and Multi-Spectral Satellite Imagery (NeurIPS 2022)
- Authors: Yezhen Cong, Samar Khanna, Chenlin Meng, Patrick Liu, Erik Rozi, Yutong He, Marshall Burke, David B. Lobell, Stefano Ermon
- Review family: Masked autoencoder for temporal or multispectral EO
- Adapter type in rs-embed: on-the-fly via `onthefly_satmae.SatMAERGBEmbedder`
- Spatial resolution / scale: 10 m provider default on Sentinel-2 RGB
- Time coverage / semantics: No fixed product window in rs-embed; user-specified range over `COPERNICUS/S2_SR_HARMONIZED`; Range window is normalized through shared helpers and used for compositing/filtering; adapter produces one composite image, not a temporal stack.
- Supported sensors / modalities: Sentinel-2 RGB or multispectral/time-series variants in original paper
- Backbone / architecture: ViT-MAE
- Pretraining / learning signal: masked autoencoding with temporal/spectral positional encoding
- Training data summary: fMoW-Sentinel and satellite imagery with temporal and spectral structure
- Representation mode: ViT patch tokens
- Output modes in rs-embed: pooled, grid
- Typical downstream tasks: classification, segmentation, transfer learning, representation learning
- Verified rs-embed output: shape=[1024], elapsed=2061.66 s, peak GPU=1276.6 MB
- Code: https://github.com/sustainlab-group/SatMAE
- Paper: https://arxiv.org/abs/2207.08051
- Model / artifact hub: https://huggingface.co/MVRL/satmae-vitlarge-fmow-pretrain-800
- Local paper note: `research_outputs/papers/processed/satmae/pre-training-transformers-for-temporal-and-multi-spectral-satellite-imagery.md`
- Architecture note: extends MAE with spectral/temporal positional encodings and masking across temporal or spectral dimensions
- Abstract snapshot: Unsupervised pre-training methods for large vision models have shown to enhance performance on downstream supervised tasks. Developing similar techniques for satellite imagery presents signiﬁcant opportunities as unlabelled data is plentiful and the inherent temporal and multi-spectral structure provides avenues to further improve existing pre-training strategies. In this paper, we present SatMAE, a pre-training framework for temporal or multi-spectral satellite imagery based on Masked Autoencoder (MAE). To leverage temporal information, we include a temporal embedding along with independently masking image patches across time. In addition, we demonstrate that encoding multi-spectral data as groups of bands with distinct spectral positional encodings is beneﬁcial. Our approach yields stron...
- Adapter note: Current adapter path targets token output from `forward_encoder(mask_ratio=0.0)`.

### satmaepp

- Publication: Rethinking Transformers Pre-training for Multi-Spectral Satellite Imagery (CVPR 2024)
- Authors: Mubashir Noman, Muzammal Naseer, Hisham Cholakkal, Rao Muhammad Anwer, Salman Khan, Fahad Shahbaz Khan
- Review family: Improved masked autoencoder for EO
- Adapter type in rs-embed: on-the-fly via `onthefly_satmaepp.SatMAEPPEmbedder`
- Spatial resolution / scale: 10 m provider default on Sentinel-2 RGB
- Time coverage / semantics: No fixed product window in rs-embed; user-specified range over `COPERNICUS/S2_SR_HARMONIZED`; Single-composite range window. Uses SatMAE++ fMoW-style eval preprocessing; temporal range selects the image composite window only.
- Supported sensors / modalities: Sentinel-2 RGB in adapter, multispectral Sentinel-2 in paper
- Backbone / architecture: ViT-L / SatMAE++
- Pretraining / learning signal: revised MAE pretraining for multispectral satellite imagery
- Training data summary: fMoW RGB / multispectral and remote sensing pretraining corpora
- Representation mode: ViT patch tokens
- Output modes in rs-embed: pooled, grid
- Typical downstream tasks: classification, segmentation, representation transfer
- Verified rs-embed output: shape=[1024], elapsed=2052.08 s, peak GPU=1276.7 MB
- Code: https://github.com/techmn/satmae_pp
- Paper: https://arxiv.org/abs/2403.05419
- Model / artifact hub: https://huggingface.co/MVRL/satmaepp_ViT-L_pretrain_fmow_rgb
- Local paper note: `research_outputs/papers/processed/satmaepp/rethinking-transformers-pre-training-for-multi-spectral-satellite-imagery.md`
- Architecture note: rethinks channel handling and pretraining settings for multispectral transformer pretraining
- Abstract snapshot: Recent advances in unsupervised learning have demonstrated the ability of large vision models to achieve promising results on downstream tasks by pre-training on large amount of unlabelled data. Such pre-training techniques have also been explored recently in the remote sensing domain due to the availability of large amount of unlabelled data. Different from standard natural image datasets, remote sensing data is acquired from various sensor technologies and exhibit diverse range of scale variations as well as modalities. Existing satellite image pre-training methods either ignore the scale information present in the remote sensing imagery or restrict themselves to use only a single type of data modality. In this paper, we re-visit transformers pre-training and leverage multi-scale informa...
- Adapter note: `grid` is a standard ViT patch-token grid.

### satmaepp_s2_10b

- Publication: Rethinking Transformers Pre-training for Multi-Spectral Satellite Imagery (CVPR 2024)
- Authors: Mubashir Noman, Muzammal Naseer, Hisham Cholakkal, Rao Muhammad Anwer, Salman Khan, Fahad Shahbaz Khan
- Review family: Grouped-channel multispectral masked autoencoder
- Adapter type in rs-embed: on-the-fly via `onthefly_satmaepp_s2.SatMAEPPSentinel10Embedder`
- Spatial resolution / scale: 10 m provider default on Sentinel-2 SR 10-band input
- Time coverage / semantics: No fixed product window in rs-embed; user-specified range over `COPERNICUS/S2_SR_HARMONIZED`; Single-composite range window. Adapter applies strict 10-band order and grouped-token handling; temporal range only determines the composite.
- Supported sensors / modalities: Sentinel-2 SR 10-band
- Backbone / architecture: ViT-L / grouped-channel SatMAE++
- Pretraining / learning signal: grouped-channel masked autoencoding
- Training data summary: Sentinel/fMoW-style multispectral pretraining checkpoint
- Representation mode: ViT group-channel tokens
- Output modes in rs-embed: pooled, grid
- Typical downstream tasks: classification, transfer learning, representation extraction
- Verified rs-embed output: shape=[1024], elapsed=17.52 s, peak GPU=1288.5 MB
- Code: https://github.com/techmn/satmae_pp
- Paper: https://arxiv.org/abs/2403.05419
- Model / artifact hub: https://huggingface.co/mubashir04/checkpoint_ViT-L_pretrain_fmow_sentinel
- Local paper note: `research_outputs/papers/processed/satmaepp/rethinking-transformers-pre-training-for-multi-spectral-satellite-imagery.md`
- Architecture note: uses three grouped channel branches to accommodate 10-band Sentinel-2 input
- Abstract snapshot: Recent advances in unsupervised learning have demonstrated the ability of large vision models to achieve promising results on downstream tasks by pre-training on large amount of unlabelled data. Such pre-training techniques have also been explored recently in the remote sensing domain due to the availability of large amount of unlabelled data. Different from standard natural image datasets, remote sensing data is acquired from various sensor technologies and exhibit diverse range of scale variations as well as modalities. Existing satellite image pre-training methods either ignore the scale information present in the remote sensing imagery or restrict themselves to use only a single type of data modality. In this paper, we re-visit transformers pre-training and leverage multi-scale informa...
- Adapter note: Current rs-embed path exposes only the `large` grouped-channel variant.

### scalemae

- Publication: A Scale-Aware Masked Autoencoder for Multiscale Geospatial Representation Learning (ICCV 2023)
- Authors: Colorado J. Reed, Ritwik Gupta, Shufan Li, Sarah Brockman, Christopher Funk, Brian Clipp, Kurt Keutzer, Salvatore Candido, Matt Uyttendaele, Trevor Darrell
- Review family: Scale-aware masked autoencoder
- Adapter type in rs-embed: on-the-fly via `onthefly_scalemae.ScaleMAERGBEmbedder`
- Spatial resolution / scale: 10 m provider default on Sentinel-2 RGB, plus explicit semantic scale input
- Time coverage / semantics: No fixed product window in rs-embed; user-specified range over `COPERNICUS/S2_SR_HARMONIZED`; Single-composite range window. Temporal range defines provider compositing; scale semantics come from `sensor.scale_m` and materially affect the embedding.
- Supported sensors / modalities: Sentinel-2 RGB in adapter, multiscale EO imagery in paper
- Backbone / architecture: ViT-L / MAE
- Pretraining / learning signal: masked autoencoding with explicit resolution conditioning
- Training data summary: multiscale geospatial imagery with explicit resolution metadata
- Representation mode: ViT patch tokens with scale token
- Output modes in rs-embed: pooled, grid
- Typical downstream tasks: cross-resolution transfer, classification, segmentation
- Verified rs-embed output: shape=[1024], elapsed=1874.83 s, peak GPU=1175.0 MB
- Code: https://github.com/bair-climate-initiative/scale-mae
- Paper: https://arxiv.org/abs/2212.14532
- Model / artifact hub: https://huggingface.co/MVRL/scalemae-vitlarge-800
- Local paper note: `research_outputs/papers/processed/scalemae/a-scale-aware-masked-autoencoder-for-multiscale-geospatial-representation-learning.md`
- Architecture note: injects semantic scale/resolution into the encoder to reduce scale mismatch
- Abstract snapshot: Large, pretrained models are commonly finetuned with imagery that is heavily augmented to mimic different conditions and scales, with the resulting models used for various tasks with imagery from a range of spatial scales. Such models overlook scale-specific information in the data for scale-dependent domains, such as remote sensing. In this paper, we present Scale-MAE, a pretraining method that explicitly learns relationships between data at different, known scales throughout the pretraining process. Scale-MAE pretrains a network by masking an input image at a known input scale, where the area of the Earth covered by the image determines the scale of the ViT positional encoding, not the image resolution. Scale-MAE encodes the masked image with a standard ViT backbone, and then decodes the...
- Adapter note: `sensor.scale_m` is a hard semantic input, not just fetch metadata.

### anysat

- Publication: One Earth Observation Model for Many Resolutions, Scales, and Modalities (CVPR 2025)
- Authors: Guillaume Astruc, Nicolas Gonthier, Clement Mallet, Loic Landrieu
- Review family: Generalist multi-resolution multimodal EO encoder
- Adapter type in rs-embed: on-the-fly via `onthefly_anysat.AnySatEmbedder`
- Spatial resolution / scale: 10 m Sentinel-2 time-series input; default per-frame resize 24 px
- Time coverage / semantics: No fixed product window in rs-embed; user-specified range over `COPERNICUS/S2_SR_HARMONIZED`, split into T frames; Multi-frame adapter. `TemporalSpec.range(...)` is split into `T` equal sub-windows, one composite frame per bin; midpoint day-of-year values become required `s2_dates` side inputs.
- Supported sensors / modalities: Sentinel-2, Sentinel-1, aerial/VHR and other modalities in original paper
- Backbone / architecture: versatile JEPA-style EO encoder
- Pretraining / learning signal: self-supervised representation learning across many configurations
- Training data summary: GeoPlex-like multi-resolution multi-modality corpora
- Representation mode: dense / pooled feature grid
- Output modes in rs-embed: pooled, grid
- Typical downstream tasks: classification, segmentation, cross-modal transfer, few-shot transfer
- Verified rs-embed output: shape=[768], elapsed=789.78 s, peak GPU=550.3 MB
- Code: https://github.com/gastruc/AnySat
- Paper: https://arxiv.org/abs/2412.14123
- Model / artifact hub: https://huggingface.co/g-astruc/AnySat
- Local paper note: `research_outputs/papers/processed/anysat/one-earth-observation-model-for-many-resolutions-scales-and-modalities.md`
- Architecture note: designed to accept many resolutions, scales, and modalities within one encoder
- Abstract snapshot: PASTIS-HD S2NAIP TSAI-TS FLAIR PLANTED 1280m 640m 60m 102.4m 120m Geospatial models must adapt to the diversity of Earth observation data in terms of resolutions, scales, and modalities. However, existing approaches expect fixed input configurations, which limits their practical applicability. We propose AnySat, a multimodal model based on joint embedding predictive architecture (JEPA) and scale-adaptive spatial encoders, allowing us to train a single model on highly heterogeneous data in a self-supervised manner. To demonstrate the advantages of this unified approach, we compile GeoPlex, a collection of 5 multimodal datasets with varying characteristics and 11 distinct sensors. We then train a single powerful model on these diverse datasets simultaneously. Once finetuned or probed, we rea...
- Adapter note: `output.scale_m` / patch size must be a positive multiple of 10 m.

### galileo

- Publication: Learning Global & Local Features of Many Remote Sensing Modalities (ICML 2025)
- Authors: Gabriel Tseng, Anthony Fuller, Marlena Reil, Henry Herzog, Patrick Beukema, Favyen Bastani, James R. Green, Evan Shelhamer, Hannah Kerner, David Rolnick
- Review family: Global-local multimodal time-series encoder
- Adapter type in rs-embed: on-the-fly via `onthefly_galileo.GalileoEmbedder`
- Spatial resolution / scale: 10 m Sentinel-2 time-series input; default frame size 64 px, patch size 8
- Time coverage / semantics: No fixed product window in rs-embed; user-specified range over `COPERNICUS/S2_SR_HARMONIZED`, split into T frames; Multi-frame adapter. `TemporalSpec.range(...)` is partitioned into `T` equal sub-windows; midpoint months become required `months` side inputs (or can be forced constant via env).
- Supported sensors / modalities: Sentinel-2 time series, multiple remote sensing modalities in original work
- Backbone / architecture: transformer with global/local branches
- Pretraining / learning signal: self-supervised multimodal representation learning
- Training data summary: many remote sensing modalities with temporal alignment
- Representation mode: pooled and token embeddings
- Output modes in rs-embed: pooled, grid
- Typical downstream tasks: classification, segmentation, retrieval, time-series transfer
- Verified rs-embed output: shape=[128], elapsed=24.12 s, peak GPU=281.3 MB
- Code: https://github.com/nasaharvest/galileo
- Paper: https://arxiv.org/abs/2502.09356
- Model / artifact hub: https://huggingface.co/nasaharvest/galileo
- Local paper note: `research_outputs/papers/processed/galileo/learning-global-local-features-of-many-remote-sensing-modalities.md`
- Architecture note: jointly learns local patch-level and global scene-level features
- Abstract snapshot: We introduce a highly multimodal transformer to represent many remote sensing modalities— multispectral optical, synthetic aperture radar, elevation, weather, pseudo-labels, and more—across space and time. These inputs are useful for diverse remote sensing tasks, such as crop mapping and flood detection. However, learning shared representations of remote sensing data is challenging, given the diversity of relevant data modalities, and because objects of interest vary massively in scale, from small boats (1−2 pixels and fast) to glaciers (thousands of pixels and slow). We present a novel self-supervised learning algorithm that extracts multi-scale features across a flexible set of input modalities through masked modeling. Our dual global and local contrastive losses differ in their targets ...
- Adapter note: Grid output averages S2-related space-time/group tokens to `(D,H,W)`.

### wildsat

- Publication: Learning Satellite Image Representations from Wildlife Observations (ICCV 2025)
- Authors: Rangel Daroya, Elijah Cole, Oisin Mac Aodha, Grant Van Horn, Subhransu Maji
- Review family: Remote sensing representation learning from weak labels
- Adapter type in rs-embed: on-the-fly via `onthefly_wildsat.WildSATEmbedder`
- Spatial resolution / scale: 10 m provider default on Sentinel-2 RGB
- Time coverage / semantics: No fixed product window in rs-embed; user-specified range over `COPERNICUS/S2_SR_HARMONIZED`; Single-composite range window. Adapter uses one composite image and can expose token grids for ViT checkpoints, or a 1x1 grid fallback for non-token paths.
- Supported sensors / modalities: Sentinel-2 RGB, wildlife observations as supervision
- Backbone / architecture: ViT-B-16
- Pretraining / learning signal: supervised / weakly supervised representation learning from wildlife observations
- Training data summary: satellite imagery aligned with wildlife observations and biodiversity labels
- Representation mode: image-head features / token grid
- Output modes in rs-embed: pooled, grid
- Typical downstream tasks: ecology transfer, classification, retrieval, representation learning
- Verified rs-embed output: shape=[256], elapsed=666.26 s, peak GPU=348.0 MB
- Code: https://github.com/mdchuc/HRSFM
- Paper: https://arxiv.org/abs/2412.14428
- Local paper note: `research_outputs/papers/processed/wildsat/learning-satellite-image-representations-from-wildlife-observations.md`
- Architecture note: learns satellite features from ecological observation signals rather than standard EO pretext tasks
- Abstract snapshot: The growth in the number of satellites with imaging capabilities deployed over the past 50 years has provided an unprecedented ability to monitor the surface of the earth [37, 80, 83]. The image data derived from these remote sensors has been shown to be highly effective for diverse tasks such as estimating global tree canopy height [39, 68], detecting illegal fishing activity [22, 36, 56], crop monitoring [19, 33, 75], disaster management [57, 66, 73], among others. Central to building computer vision models for these tasks is the need for mechanisms for learning effective representations from image data. As a result of the distribution shift between remote sensing imagery and web-sourced images, a large body of work has emerged exploring the merits and trade-offs between different source...
- Adapter note: Current adapter can return a `1x1` vector grid when token extraction is unavailable.

### prithvi

- Publication: Foundation Models for Generalist Geospatial Artificial Intelligence (arXiv 2023)
- Authors: Johannes Jakubik, Sujit Roy, C. E. Phillips, Paolo Fraccaro, Denys Godwin, Bianca Zadrozny, Daniela Szwarcman, Carlos Gomes, Gabby Nyirjesy, Blair Edwards, Daiki Kimura, Naomi Simumba, Linsong Chu, S. Karthik Mukkavilli, Devyani Lambhate, Kamal Das, Ranjini Bangalore, Dario Oliveira, Michal Muszynski, Kumar Ankur, Muthukumaran Ramasubramanian, Iksha Gurung, Sam Khallaghi, Hanxi Li, Michael Cecil, Maryam Ahmadi, Fatemeh Kordi, Hamed Alemohammad, Manil Maskey, Raghu Ganti, Kommy Weldemariam, Rahul Ramachandran
- Review family: Generalist geospatial foundation model
- Adapter type in rs-embed: on-the-fly via `onthefly_prithvi.PrithviEOV2S2_6B_Embedder`
- Spatial resolution / scale: 30 m provider default in current adapter (`DEFAULT_IMAGE_SCALE_M=30`) on Sentinel-2 6-band input
- Time coverage / semantics: No fixed product window in rs-embed; range preferred over `COPERNICUS/S2_SR_HARMONIZED`; `year` is normalized to a full-year range; Adapter normalizes `year` to `[YYYY-01-01, (YYYY+1)-01-01)` and derives temporal midpoint coordinates; location coordinates come from the ROI center.
- Supported sensors / modalities: HLS / Sentinel-Landsat style 6-band optical imagery
- Backbone / architecture: ViT / masked autoencoder lineage
- Pretraining / learning signal: self-supervised geospatial pretraining
- Training data summary: NASA/IBM geospatial corpora designed for generalist GeoAI
- Representation mode: ViT tokens with time/location side inputs
- Output modes in rs-embed: pooled, grid
- Typical downstream tasks: classification, segmentation, mapping, generalist transfer
- Verified rs-embed output: shape=[768], elapsed=719.82 s, peak GPU=455.1 MB
- Code: n/a
- Paper: https://arxiv.org/abs/2310.18660
- Model / artifact hub: https://huggingface.co/ibm-nasa-geospatial
- Local paper note: `research_outputs/papers/processed/prithvi/foundation-models-for-generalist-geospatial-artificial-intelligence.md`
- Architecture note: time and geolocation are first-class side inputs in the encoder family
- Abstract snapshot: Significant progress in the development of highly adaptable and reusable Artificial Intelligence (AI) models is expected to have a significant impact on Earth science and remote sensing. Foundation models are pre-trained on large unlabeled datasets through self-supervision, and then fine-tuned for various downstream tasks with small labeled datasets. There is an increasing interest within the scientific community to investigate whether this approach can be successfully applied to domains beyond natural language processing to effectively build generalist AI models that exploit multi-sensor data. This paper introduces a first-of-its-kind framework for the efficient pre-training and fine-tuning of foundational models on extensive geospatial data. We have utilized this framework to create Prit...
- Adapter note: This is the one canonical rs-embed model with a 30 m default fetch scale.
- Adapter note: Current adapter exposes `100_tl`, `300_tl`, and `600_tl` variants through `model_config`.

### terrafm

- Publication: A Scalable Foundation Model for Unified Multisensor Earth Observation (ICLR 2026)
- Authors: Muhammad Sohail Danish, Muhammad Akhtar Munir, Syed Roshaan Ali Shah, Muhammad Haris Khan, Rao Muhammad Anwer, Jorma Laaksonen, Fahad Shahbaz Khan, Salman Khan
- Review family: Unified multisensor foundation model
- Adapter type in rs-embed: on-the-fly via `onthefly_terrafm.TerraFMBEmbedder`
- Spatial resolution / scale: 10 m provider default for both S2 and S1 paths; image resized to 224 px
- Time coverage / semantics: No fixed product window in rs-embed; provider path requires `TemporalSpec.range(...)` over either Sentinel-2 or Sentinel-1 collections; Single-composite range window. Provider path composites either S2 or S1 imagery; S1 path adds adapter policy around IW filtering and fallback behavior.
- Supported sensors / modalities: Sentinel-2, Sentinel-1
- Backbone / architecture: multisensor transformer
- Pretraining / learning signal: scalable unified multisensor pretraining
- Training data summary: large multisensor Earth observation corpus spanning S1 and S2
- Representation mode: shared encoder features
- Output modes in rs-embed: pooled, grid
- Typical downstream tasks: classification, segmentation, cross-sensor transfer, representation learning
- Verified rs-embed output: shape=[768], elapsed=671.25 s, peak GPU=477.7 MB
- Code: https://github.com/mbzuai-oryx/TerraFM
- Paper: https://arxiv.org/abs/2506.06281
- Model / artifact hub: https://huggingface.co/MBZUAI/TerraFM
- Local paper note: `research_outputs/papers/processed/terrafm/a-scalable-foundation-model-for-unified-multisensor-earth-observation.md`
- Architecture note: one foundation model for both optical and SAR inputs with modality routing
- Abstract snapshot: Modern Earth observation (EO) increasingly leverages deep learning to harness the scale and diversity of satellite imagery across sensors and regions. While recent foundation models have demonstrated promising generalization across EO tasks, many remain limited by the scale, geographical coverage, and spectral diversity of their training data, factors critical for learning globally transferable representations. In this work, we introduce TerraFM, a scalable self-supervised learning model that leverages globally distributed Sentinel-1 and Sentinel-2 imagery, combined with large spatial tiles and land-cover aware sampling to enrich spatial and semantic coverage. By treating sensing modalities as natural augmentations in our self-supervised approach, we unify radar and optical inputs via moda...
- Adapter note: Current adapter only wires up the TerraFM-B path.
- Adapter note: The S1 `IW` preference is an rs-embed adapter policy, not a TerraFM paper requirement.

### terramind

- Publication: Large-Scale Generative Multimodality for Earth Observation (ICCV 2025)
- Authors: Johannes Jakubik, Felix Yang, Benedikt Blumenstiel, Erik Scheurer, Rocco Sedona, Stefano Maurogiovanni, Jente Bosmans, Nikolaos Dionelis, Valerio Marsocci, Niklas Kopp, Rahul Ramachandran, Paolo Fraccaro, Thomas Brunschwiler, Gabriele Cavallaro, Juan Bernabe-Moreno, Nicolas Longepe
- Review family: Generative multimodal EO foundation model
- Adapter type in rs-embed: on-the-fly via `onthefly_terramind.TerraMindEmbedder`
- Spatial resolution / scale: 10 m provider default on Sentinel-2 SR 12-band input; image resized to 224 px
- Time coverage / semantics: No fixed product window in rs-embed; user-specified range over `COPERNICUS/S2_SR_HARMONIZED`; Single-composite range window for provider path; tensor path bypasses provider/temporal fetching.
- Supported sensors / modalities: Sentinel-2 in adapter, wider multimodal EO stack in paper
- Backbone / architecture: large-scale generative multimodal transformer
- Pretraining / learning signal: large-scale generative multimodal learning
- Training data summary: large multimodal Earth observation data for generation and representation learning
- Representation mode: multimodal latent features
- Output modes in rs-embed: pooled, grid
- Typical downstream tasks: representation learning, generation, multimodal transfer
- Verified rs-embed output: shape=[384], elapsed=725.17 s, peak GPU=104.2 MB
- Code: https://github.com/IBM/terramind
- Paper: https://arxiv.org/abs/2504.11171
- Local paper note: `research_outputs/papers/processed/terramind/large-scale-generative-multimodality-for-earth-observation.md`
- Architecture note: generative multimodality is central; rs-embed currently exposes the Sentinel-2 encoder path
- Abstract snapshot: We present TerraMind, the first any-to-any generative, multimodal deep learning model for Earth observation (EO). Unlike other approaches, TerraMind is pretrained on dualscale representations combining both token-level and pixellevel data across modalities. On a token level, TerraMind encodes high-level contextual information to learn crossmodal relationships, while on a pixel level, TerraMind lever- ages fine-grained representations to capture critical spatial nuances. In this paper, we demonstrate that (i) TerraMind achieves beyond state-of-the-art performance in communitystandard benchmarks, (ii) TerraMind can leverage “thinking in modalities” (TiM)—the capability of generating additional artificial data during finetuning and inference to improve the model output—and (iii) TerraMind’s d...
- Adapter note: Default normalization is TerraMind z-score; changing it changes representation semantics.

### dofa

- Publication: Neural Plasticity-Inspired Multimodal Foundation Model for Earth Observation (arXiv 2024)
- Authors: Zhitong Xiong, Yi Wang, Fahong Zhang, Adam J. Stewart, Joelle Hanna, Damian Borth, Ioannis Papoutsis, Bertrand Le Saux, Gustau Camps-Valls, Xiao Xiang Zhu
- Review family: Wavelength-aware multimodal foundation model
- Adapter type in rs-embed: on-the-fly via `onthefly_dofa.DOFAEmbedder`
- Spatial resolution / scale: 10 m provider default for S2 path; fixed resize to 224 px
- Time coverage / semantics: No fixed product window in rs-embed; provider path uses user-specified range over `COPERNICUS/S2_SR_HARMONIZED`; Provider path requires `TemporalSpec.range(...)` and builds one composite patch; tensor path bypasses temporal/provider retrieval. Wavelengths are required and may be inferred for recognized band sets such as Sentinel-2.
- Supported sensors / modalities: multispectral and hyperspectral style inputs, Sentinel-2 in adapter
- Backbone / architecture: transformer with neural plasticity / dynamic wavelength handling
- Pretraining / learning signal: self-supervised multimodal EO foundation modeling
- Training data summary: multimodal EO corpora with wavelength metadata
- Representation mode: token embedding with wavelength side vector
- Output modes in rs-embed: pooled, grid
- Typical downstream tasks: classification, cross-sensor transfer, hyperspectral transfer
- Verified rs-embed output: shape=[768], elapsed=104.99 s, peak GPU=464.6 MB
- Code: https://github.com/zhu-xlab/DOFA
- Paper: https://arxiv.org/abs/2403.15356
- Model / artifact hub: https://huggingface.co/earthflow/DOFA
- Local paper note: `research_outputs/papers/processed/dofa/neural-plasticity-inspired-multimodal-foundation-model-for-earth-observation.md`
- Architecture note: explicitly consumes wavelength vectors, making it sensor-flexible
- Abstract snapshot: Earth observation (EO) in open-world settings presents a unique challenge: different applications rely on diverse sensor modalities, each with varying ground sampling distances, spectral ranges, and numbers of spectral bands. However, existing EO foundation models are typically tailored to specific sensor types, making them inflexible when generalizing across the heterogeneous landscape of EO data. To address this, we propose the Dynamic One-For-All (DOFA) model, a unified, multimodal foundation framework designed for diverse vision tasks in EO. Inspired by neural plasticity, DOFA utilizes a wavelength-conditioned dynamic hypernetwork to process inputs from five distinct satellite sensors flexibly. By continually pretraining on five EO modalities, DOFA achieves state-of-the-art perfor-...
- Adapter note: Current adapter exposes `base` and `large` variants.

### fomo

- Publication: Multi-Modal, Multi-Scale and Multi-Task Remote Sensing Foundation Models for Forest Monitoring (AAAI 2025)
- Authors: Nikolaos Ioannis Bountos, Arthur Ouaknine, Ioannis Papoutsis, David Rolnick
- Review family: Forest-oriented multimodal and multiscale foundation model
- Adapter type in rs-embed: on-the-fly via `onthefly_fomo.FoMoEmbedder`
- Spatial resolution / scale: 10 m provider default on Sentinel-2 SR 12-band input; default image size 64 px
- Time coverage / semantics: No fixed product window in rs-embed; user-specified range over `COPERNICUS/S2_SR_HARMONIZED`; Single-composite range window. Adapter normalizes a single provider composite and forwards `(x, spectral_keys)` through the FoMo model.
- Supported sensors / modalities: Sentinel-2 SR in adapter, multiple scales and tasks in original work
- Backbone / architecture: multimodal transformer / representation learner
- Pretraining / learning signal: multi-task forest monitoring pretraining
- Training data summary: forest monitoring corpora across multiple modalities and scales
- Representation mode: pooled or token embeddings
- Output modes in rs-embed: pooled, grid
- Typical downstream tasks: forest type mapping, biomass-related transfer, classification, segmentation
- Verified rs-embed output: shape=[768], elapsed=418.65 s, peak GPU=361.3 MB
- Code: https://github.com/RolnickLab/FoMo-Bench
- Paper: https://arxiv.org/abs/2312.10114
- Local paper note: `research_outputs/papers/processed/fomo/multi-modal-multi-scale-and-multi-task-remote-sensing-foundation-models-for-forest-monitoring.md`
- Architecture note: injects modality keys for each channel and focuses on forest monitoring use cases
- Abstract snapshot: balance. However, forests are rapidly changing as a result of land use decisions, climate change and invasive species (Bonan 2008; Curtis et al. 2018; Hartmann et al. 2022) leading to significant biodiversity decline and economic losses. However, effective forest management and conservation are hampered by a lack of information, highlighting the need for scalable forest monitoring. This gap encompasses multiple specific problems, such as tree species identification, tree size assessment, land cover classification, etc., which also vary considerably across geographies, climatic zones and landscapes. Forests are vital to ecosystems, supporting biodiversity and essential services, but are rapidly changing due to land use and climate change. Understanding and mitigating negative effects requir...
- Adapter note: Grid output averages spectral modalities into a spatial token grid when possible.

### thor

- Publication: A Versatile Foundation Model for Earth Observation Climate and Society Applications (arXiv 2026)
- Authors: Theodor Forgaard, Jarle Reksten, Anders Waldeland, Valerio Marsocci, Nicolas Longepe, Michael Kampffmeyer, Arnt-Borre Salberg
- Review family: Versatile EO foundation model for climate and society
- Adapter type in rs-embed: on-the-fly via `onthefly_thor.THORBaseEmbedder`
- Spatial resolution / scale: 10 m provider default on Sentinel-2 SR 10-band input; default image size 288 px
- Time coverage / semantics: No fixed product window in rs-embed; user-specified range over `COPERNICUS/S2_SR_HARMONIZED`; Single-composite range window. Adapter uses temporal range only for provider compositing; no separate temporal tokens in the current path.
- Supported sensors / modalities: Sentinel-2 SR 10-band
- Backbone / architecture: versatile transformer
- Pretraining / learning signal: foundation pretraining for climate and society applications
- Training data summary: large EO corpus oriented toward broad societal and climate tasks
- Representation mode: ViT embeddings
- Output modes in rs-embed: pooled, grid
- Typical downstream tasks: classification, regression, mapping, broad transfer
- Verified rs-embed output: shape=[768], elapsed=555.73 s, peak GPU=489.3 MB
- Code: https://github.com/FM4CS/THOR
- Paper: https://arxiv.org/abs/2601.16011
- Model / artifact hub: https://huggingface.co/FM4CS/THOR-1.0-base
- Local paper note: `research_outputs/papers/processed/thor/a-versatile-foundation-model-for-earth-observation-climate-and-society-applications.md`
- Architecture note: designed as a versatile base model rather than a task-specific agriculture or vision-language model
- Abstract snapshot: els (FM) promise to solve EO [16], but simply applying models pre-trained on standard natural images is often suboptimal [24] as one must ingest a vast, heterogeneous data stream from diverse sensors (e.g., optical, SAR) at scales from meters to kilometers ground sampling distance (GSD). Most current EO-specific FMs (e.g., [8, 13, 26, 30, 31]), often built on Vision Transformers (ViT), are architecturally rigid. They are trained using a fixed input image size and a fixed patch size (e.g., 16 × 16), which creates a critical bottleneck for data-efficient adaptation: coarse patching produces a low-resolution token sequence. Consequently, dense pixel-level tasks like segmentation require large, complex decoders (e.g., UperNet [25]) to upsample the features. These decoders often demand signific...
- Adapter note: Current adapter exposes `tiny`, `small`, `base`, and `large` through `model_config["variant"]`.

### agrifm

- Publication: AgriFM: A multi-source temporal remote sensing foundation model for Agriculture mapping (Remote Sensing of Environment 2026)
- Authors: Wenyuan Li, Shunlin Liang, Keyan Chen, Yongzhe Chen, Han Ma, Jianglei Xu, Yichuan Ma, Yuxiang Zhang, Shikang Guan, Husheng Fang, Zhenwei Shi
- Review family: Agriculture-specific multi-source temporal foundation model
- Adapter type in rs-embed: on-the-fly via `onthefly_agrifm.AgriFMEmbedder`
- Spatial resolution / scale: 10 m Sentinel-2 time-series input; default image size 224 px with fixed T-frame packaging
- Time coverage / semantics: No fixed product window in rs-embed; user-specified range over `COPERNICUS/S2_SR_HARMONIZED`, split into T frames; Multi-frame adapter. `TemporalSpec.range(...)` is partitioned into `T` equal sub-windows; one composite frame per bin is stacked directly into the model input with no separate temporal token tensor.
- Supported sensors / modalities: Sentinel-2 in adapter, Sentinel-2, Landsat-8/9, MODIS in original paper
- Backbone / architecture: Video Swin Transformer
- Pretraining / learning signal: supervised land-cover fraction pretraining with EMA teacher
- Training data summary: 25M+ globally sampled multi-source temporal patches from MODIS, Landsat, and Sentinel-2
- Representation mode: video Swin features
- Output modes in rs-embed: pooled, grid
- Typical downstream tasks: cropland mapping, field boundary delineation, crop type mapping, agricultural land-use mapping
- Verified rs-embed output: shape=[1024], elapsed=21.3 s, peak GPU=590.3 MB
- Code: https://github.com/flyakon/AgriFM
- Paper: https://www.sciencedirect.com/science/article/pii/S0034425726000040
- Model / artifact hub: https://glass.hku.hk/casual/AgriFM/AgriFM.pth
- Local paper note: `research_outputs/papers/processed/agrifm/agrifm.md`
- Architecture note: synchronized spatiotemporal downsampling is the core design idea for agriculture mapping
- Abstract snapshot: arXiv:2505.21357v3 [cs.CV] 15 Jan 2026 Climate change and population growth intensify the demand for precise agriculture mapping to enhance food security. Such mapping tasks require robust modeling of multi-scale spatiotemporal patterns from fine field textures to landscape context, and from short-term phenology to full growing-season dynamics. Existing methods often process spatial and temporal features separately, limiting their ability to capture essential agricultural dynamics. While transformer-based remote sensing foundation models (RSFMs) offer unified spatiotemporal modeling ability, most of them remain suboptimal: they either use fixed windows that ignore multi-scale crop characteristics or neglect temporal information entirely. To address these gaps, we propose AgriFM, a multi-so...
- Adapter note: Paper uses multi-source pretraining, but the current rs-embed adapter path is Sentinel-2 10-band only.

### satvision

- Publication: A Geospatial Foundation Model for Coarse-Resolution All-Sky Remote Sensing Imagery (arXiv 2024)
- Authors: Caleb S. Spradlin, Jordan A. Caraballo-Vega, Jian Li, Mark L. Carroll, Jie Gong, Paul M. Montesano
- Review family: Coarse-resolution all-sky foundation model
- Adapter type in rs-embed: on-the-fly via `onthefly_satvision_toa.SatVisionTOAEmbedder`
- Spatial resolution / scale: 1000 m provider default (`SensorSpec.scale_m=1000`) on 14-channel TOA input
- Time coverage / semantics: No fixed product window in rs-embed; user-specified range over default `MODIS/061/MOD021KM` unless overridden; Single-composite range window normalized via shared helpers. Default provider path mosaics MODIS TOA imagery over the requested range; no extra temporal tokenization.
- Supported sensors / modalities: MODIS 14-band TOA
- Backbone / architecture: SwinV2-style encoder
- Pretraining / learning signal: foundation pretraining on all-sky MODIS TOA data
- Training data summary: 14-band MODIS TOA imagery capturing visible, NIR, and thermal bands under all-sky conditions
- Representation mode: Swin-based coarse-resolution features
- Output modes in rs-embed: pooled, grid
- Typical downstream tasks: atmospheric science, environmental monitoring, coarse-resolution transfer
- Verified rs-embed output: shape=[4096], elapsed=7179.36 s, peak GPU=9938.2 MB
- Code: https://github.com/nasa-nccs-hpda/pytorch-caney
- Paper: https://arxiv.org/abs/2411.17000
- Model / artifact hub: https://huggingface.co/nasa-cisto-data-science-group/satvision-toa-giant-patch8-window8-128
- Local paper note: `research_outputs/papers/processed/satvision/a-geospatial-foundation-model-for-coarse-resolution-all-sky-remote-sensing-imagery.md`
- Architecture note: extends remote sensing foundation modeling beyond cloud-free, fine-resolution optical imagery
- Abstract snapshot: Foundation models have the potential to transform the landscape of remote sensing (RS) data analysis by enabling large computer vision models to be pre-trained on vast amounts of remote sensing data. These models can then be fine-tuned with small amounts of labeled training and applied to a variety of mapping and monitoring applications. Most existing foundation models are designed for high spatial resolution, cloud-free satellite imagery or photos, limiting their applicability in scenarios that require frequent temporal monitoring or broad spectral profiles. As a result, foundation models trained solely on cloud-free images have limited utility for applications that involve atmospheric variables (e.g., cloud or aerosol) or require atmospheric corrections. We introduce SatVision-TOA, a nov...
- Adapter note: Important repo-level nuance: the current adapter defaults to MODIS TOA at 1000 m, which is more specific than the README shorthand 'TOA 14-channel'.
