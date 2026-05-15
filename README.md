<div align="center">

# <img src="https://raw.githubusercontent.com/cybergis/rs-embed/main/docs/assets/icon.png" width="35" alt="icon" /> rs-embed

**One line code to get Any Remote Sensing Foundation Model (RSFM) embeddings for Any Place and Any Time**

[![arXiv](https://img.shields.io/badge/arXiv-2602.23678-b31b1b.svg)](https://arxiv.org/abs/2602.23678)
[![Docs](https://img.shields.io/badge/docs-online-brightgreen)](https://cybergis.github.io/rs-embed/)
![Python](https://img.shields.io/badge/python-3.12-blue?logo=python)
[![PyTorch 2.2](https://img.shields.io/badge/torch-2.2-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)

![Visitors](https://visitor-badge.laobi.icu/badge?page_id=cybergis.rs-embed)
![Last Commit](https://img.shields.io/github/last-commit/cybergis/rs-embed)
![License](https://img.shields.io/github/license/cybergis/rs-embed)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/rs-embed?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/rs-embed)

[Docs](https://cybergis.github.io/rs-embed/) · [Releases](https://github.com/cybergis/rs-embed/releases) · [Changelog](https://github.com/cybergis/rs-embed/blob/main/CHANGELOG.md) · [StartNow](https://github.com/cybergis/rs-embed/blob/main/examples/playground.ipynb) · [UseCase](https://github.com/cybergis/rs-embed/blob/main/examples/demo.ipynb) · [Paper](https://arxiv.org/abs/2602.23678)

</div>

> Get Start on [I-GUIDE](https://platform.i-guide.io/notebooks/a013ce97-d963-4262-9f21-edd09976181a) Today!

<img src="https://raw.githubusercontent.com/cybergis/rs-embed/main/docs/assets/background.png" />

## TL;DR

```python
emb = get_embedding("prithvi", spatial=..., temporal=..., output=...)
```

## Install

```bash
# base install
pip install rs-embed

# add [terratorch] only if you use terramind
pip install "rs-embed[terratorch]"
```

For local development:

```bash
git clone https://github.com/cybergis/rs-embed.git
cd rs-embed
pip install -e .  # use -e ".[terratorch]" if you need terramind
```

If this is your first time using Google Earth Engine, authenticate once:

```bash
earthengine authenticate
```

## Quick Example

```python
from rs_embed import PointBuffer, TemporalSpec, OutputSpec, get_embedding

spatial = PointBuffer(lon=121.5, lat=31.2, buffer_m=2048)
temporal = TemporalSpec.range(
    "2022-06-01",
    "2022-09-01",
)

emb = get_embedding(
    "prithvi",
    spatial=spatial,
    temporal=temporal,
    output=OutputSpec.pooled(),
)

```

See the visualization helper and end-to-end notebook in the repository:

- [`examples/plot_utils.py`](https://github.com/cybergis/rs-embed/blob/main/examples/plot_utils.py)
- [`examples/playground.ipynb`](https://github.com/cybergis/rs-embed/blob/main/examples/playground.ipynb)

<img src="https://raw.githubusercontent.com/cybergis/rs-embed/main/docs/assets/vis.png" width=750 />

## Main API

For new users, start with these primary APIs:

- `get_embedding(...)`: one ROI -> one embedding
- `get_embeddings_batch(...)`: many ROIs, same model
- `export_batch(...)`: export datasets / experiments (single or multiple ROIs)
- `inspect_provider_patch(...)`: inspect raw provider patches before inference

## Supported Models

rs-embed supports **19 canonical public models** in two categories:
- **16 open-source inference models** — fetch imagery from GEE and run the model locally; weights are downloaded from HuggingFace or GitHub on first use.
- **3 precomputed embedding products** — return embeddings by coordinate lookup with no local inference (`tessera`, `gse`, `copernicus`).

This is a convenience index with basic model info only (for quick scanning / links). For detailed I/O behavior and preprocessing notes, see [Supported Models](https://cybergis.github.io/rs-embed/models/).

| Model ID          | Institution | Embedding Source | Input Data                | Bands | Resolution | Embed Dim | Params  | Architecture  | Publication                                                                     | Link                                                         |
| ----------------- | ----------- | ---------------- | ------------------------- | ----- | ---------- | --------- | ------- | ------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| `tessera`         | U of Cambridge, dClimate | Pre-computed | —                    | —     | 10m        | 128       | —       | —             | [CVPR 2026](https://arxiv.org/abs/2506.20380v4)                                | [link](https://github.com/ucam-eo/geotessera)                |
| `gse` (Alpha Earth) | Google DeepMind | Pre-computed | —                    | —     | 10m        | 64        | —       | —             | [arXiv 2025](https://arxiv.org/abs/2507.22291)                                 | [link](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL) |
| `copernicus`      | TU Munich, NVIDIA | Pre-computed | —                      | —     | 0.25°      | 768       | —       | —             | [ICCV 2025](https://arxiv.org/abs/2503.11849)                                  | [link](https://huggingface.co/datasets/torchgeo/copernicus_embed) |
| `galileo`         | Mila, McGill, AI2 | Inference  | Sentinel-2 SR            | 10    | 10m        | 128       | ~25M    | ViT (nano)    | [ICML 2025](https://arxiv.org/abs/2502.09356)                                  | [link](https://github.com/nasaharvest/galileo)               |
| `remoteclip`      | Hohai U, HKUST | Inference   | Sentinel-2 RGB            | 3     | 10m        | 512       | ~49M    | CLIP ViT-B/32 | [TGRS 2024](https://arxiv.org/abs/2306.11029)                                  | [link](https://github.com/ChenDelong1999/RemoteCLIP)         |
| `agrifm`          | HKU, Beihang U, Wuhan U | Inference | Sentinel-2 SR          | 10    | 10m        | 1024      | ~60M    | Swin-3D       | [RSE 2026](https://www.sciencedirect.com/science/article/pii/S0034425726000040) | [link](https://github.com/flyakon/AgriFM)                    |
| `wildsat`         | UMass Amherst, U of Edinburgh | Inference | Sentinel-2 RGB      | 3     | 10m        | 256       | ~86M    | ViT-B/16      | [ICCV 2025](https://arxiv.org/abs/2412.14428)                                  | [link](https://github.com/mdchuc/HRSFM)                      |
| `dofa`            | TU Munich, ESA | Inference    | Sentinel-2 SR              | 9     | 10m        | 768       | ~86M    | ViT-B         | [arXiv 2024](https://arxiv.org/abs/2403.15356)                                 | [link](https://github.com/zhu-xlab/DOFA)                     |
| `fomo`            | Mila, McGill U | Inference    | Sentinel-2 SR              | 12    | 10m        | 768       | ~86M    | ViT-B MAE     | [AAAI 2025](https://arxiv.org/abs/2312.10114)                                  | [link](https://github.com/RolnickLab/FoMo-Bench)             |
| `terrafm`         | MBZUAI, Aalto U | Inference   | Sentinel-2 SR / Sentinel-1 | 12/2  | 10m        | 768       | ~86M    | ViT-B         | [ICLR 2026](https://arxiv.org/abs/2506.06281)                                  | [link](https://github.com/mbzuai-oryx/TerraFM)               |
| `anysat`          | IGN France, CNES | Inference  | Sentinel-2 SR              | 10    | 10m        | 768       | ~86M    | ViT-B         | [CVPR 2025](https://arxiv.org/abs/2412.14123)                                  | [link](https://github.com/gastruc/AnySat)                    |
| `thor`            | Norwegian Computing Center, ESA | Inference | Sentinel-2 SR      | 10    | 10m        | 768       | ~86M    | ViT-B         | [arXiv 2026](https://arxiv.org/abs/2601.16011)                                 | [link](https://github.com/FM4CS/THOR)                        |
| `satvision`       | NASA Goddard | Inference      | MODIS TOA                  | 14    | 1000m      | 4096      | ~87M    | Swin-B (GIANT)| [arXiv 2024](https://arxiv.org/abs/2411.17000)                                 | [link](https://github.com/nasa-nccs-hpda/pytorch-caney)      |
| `prithvi`         | IBM Research, NASA | Inference | Sentinel-2 SR              | 6     | 30m        | 768       | ~100M   | PrithviMAE    | [arXiv 2023](https://arxiv.org/abs/2310.18660)                                 | [link](https://huggingface.co/ibm-nasa-geospatial)           |
| `terramind`       | IBM Research, ESA, ETH Zurich | Inference | Sentinel-2 SR      | 12    | 10m        | 384       | ~25M    | ViT-S         | [ICCV 2025](https://arxiv.org/abs/2504.11171)                                  | [link](https://github.com/IBM/terramind)                     |
| `satmae`          | Stanford U | Inference        | Sentinel-2 RGB              | 3     | 10m        | 1024      | ~304M   | ViT-L MAE     | [NeurIPS 2022](https://arxiv.org/abs/2207.08051)                               | [link](https://github.com/sustainlab-group/SatMAE)           |
| `satmaepp`        | MBZUAI | Inference            | Sentinel-2 RGB              | 3     | 10m        | 1024      | ~304M   | ViT-L MAE     | [CVPR 2024](https://arxiv.org/abs/2403.05419)                                  | [link](https://github.com/techmn/satmae_pp)                  |
| `satmaepp_s2_10b` | MBZUAI | Inference            | Sentinel-2 SR               | 10    | 10m        | 1024      | ~304M   | ViT-L MAE     | [CVPR 2024](https://arxiv.org/abs/2403.05419)                                  | [link](https://github.com/techmn/satmae_pp)                  |
| `scalemae`        | UC Berkeley, Meta AI | Inference | Sentinel-2 RGB            | 3     | 10m        | 1024      | ~304M   | ViT-L MAE     | [ICCV 2023](https://arxiv.org/abs/2212.14532)                                  | [link](https://github.com/bair-climate-initiative/scale-mae) |

- **Embedding Source**: *Pre-computed* = embeddings already computed globally, query by coordinates; *Inference* = fetch imagery then run model locally
- **Bands**: number of input spectral bands required by inference models; pre-computed models have no input requirement
- **Embed Dim**: output embedding vector dimensionality (number of features)
- **Resolution**: default provider fetch resolution, not the model's internal tensor size
- **Params**: approximate parameter count for the default variant used in rs-embed

> **Why do inference times vary so much (2 s ~ 1800 s)?** Three factors dominate:
> 1. **Pre-computed vs. inference** — Pre-computed models (tessera, gse, copernicus) only look up coordinates, finishing in seconds. Inference models must fetch imagery from GEE and then run a forward pass.
> 2. **Model size** — ViT-Large models (~304M params: satmae, satmaepp, scalemae) take 3-5x longer per forward pass than ViT-Base models (~86M params: dofa, fomo, terrafm). The satvision GIANT checkpoint (87M but deep Swin with 42-layer stage) is similarly heavy.
> 3. **Input complexity** — Multi-temporal models (anysat, galileo, agrifm) fetch multiple time frames from GEE, multiplying both network I/O and compute. First-run latency also includes one-time weight downloads (100 MB ~ 2.5 GB).

## Local survey benchmark assets

The survey experiment assets live under `survey_satellite_embedding/` and are
prepared around a **single high-resolution Wuhan ROI**, not a two-region
benchmark or a simple all-model leaderboard. The experiment section should use
this one area to compare the 19 canonical public models on common
remote-sensing downstream tasks under shared tiles, labels, temporal windows,
and evaluation splits.

### Active experiment data

- **Primary benchmark ROI**:
  Wuhan East Lake / Tangxun Lake urban-water-vegetation corridor
- **Prepared data folder**:
  `survey_satellite_embedding/data/part2_20260502_full/region_a/`
- **Bounds**:
  `[114.29, 30.44, 114.53, 30.60]`
- **Prepared assets**:
  - Sentinel-2 2021 growing-season blocks:
    `imagery_s2_20210501_20211031/`
  - ESA WorldCover 2021 blocks:
    `worldcover_2021_blocks/`
  - JRC water occurrence blocks:
    `jrc_occurrence_blocks/`
  - 500 m downstream-task manifest:
    `tile_manifest_500m.csv` (**2173** tiles)
- **Full prep summary**:
  `survey_satellite_embedding/data/part2_20260502_full/prepare_part2_data_summary.json`

### Benchmark task scope

The active survey benchmark should keep one ROI and cover several task families:

- tile-level land-cover classification from pooled embeddings
- built-up, vegetation, and water fraction regression
- water segmentation or mask reconstruction when dense token grids are exposed
- optional retrieval and qualitative map panels for compatible model families

This design keeps the data source, label source, temporal window, and spatial
split fixed while still covering the common downstream task types discussed in
the survey.

### Current experiment status

- **All-model smoke outputs**:
  `survey_satellite_embedding/experiments/results/all_models_smoke_20260502/`
- This directory contains fresh pooled embeddings and runtime metadata for the
  current public models over sampled Wuhan ROI tiles.
- **Final single-area public-19 map test case**:
  `survey_satellite_embedding/experiments/results/part2_model_map_figure/`
  - summary figure:
    `part2_original_map_with_public19_models_2x.png`
  - manifest:
    `manifest_2x.json`
  - coverage:
    `region_a/block_r01_c01`, `block_r01_c02`, `block_r02_c01`, and
    `block_r02_c02`
  - scale:
    this is the 2x-by-2x expansion of the original reference block, so the
    displayed geographic area is 4x the old single-block figure
  - status:
    all 19 canonical public models have map outputs for this 2x Wuhan case
- **Current 2x downstream-cache status**:
  `survey_satellite_embedding/experiments/results/downstream_core_2x/`
  - T1 classification has already been completed for the current 2x public-19
    Wuhan window.
  - `classification.csv`, `classification_ranked.csv`, per-model prediction
    CSVs, and classification figures are present.
  - `embeddings_2x_tile/` contains the reusable local pooled tile embeddings
    for all 19 canonical public models over the 567 500 m tiles in this 2x
    window.
  - Use these local `.npz` files for the next T2 fraction-regression acceptance
    run. Do not re-export embeddings or fetch Sentinel-2 inputs from GEE for
    this acceptance scope.
- **Current T2 2x fraction-regression status**:
  `survey_satellite_embedding/experiments/results/downstream_fraction_2x/`
  - T2 fraction regression has been completed for all 19 canonical public
    models on the current 567-tile 2x Wuhan window.
  - The run used only the existing local embeddings in
    `downstream_core_2x/embeddings_2x_tile/`; it did not fetch imagery from GEE,
    export embeddings, or rerun model encoders.
  - Main outputs:
    `fraction_regression.csv`, `fraction_regression_ranked.csv`,
    `fraction_regression_predictions_{model}.csv`,
    `figures/fraction_regression_scatter_{model}.png`, and
    `figures/fraction_regression_spearman_public19_2x.png`.
  - Local-cache-only runner:
    `survey_satellite_embedding/experiments/run_wuhan_t2_2x_fraction_regression.py`
  - Current top mean test Spearman models:
    `gse`, `tessera`, `thor`, `dofa`, and `terramind`.
- **Current T2 full-ROI status**:
  `survey_satellite_embedding/experiments/results/downstream_fraction/`
  - only the full-ROI T2 label/split artifacts have been materialized so far:
    `downstream_labels_500m_fraction.csv`,
    `downstream_splits_500m_fraction.csv`, and
    `downstream_labels_summary_fraction.json`.
  - full-ROI pooled embeddings for all 2173 tiles are not present in
    `downstream_fraction/embeddings_full_roi/`.
  - A full-ROI `--export-missing` run was stopped because it would recompute
    embeddings. Restart full-ROI extraction only after explicit approval.
- **Historical single-block figure**:
  `part2_original_map_with_public19_models.png`
  - keep this as the previous reference-block sanity check only; it is not the
    active downstream benchmark case.

The immediate experiment priority is to run downstream tasks on the same
single-area Wuhan setup rather than revive the old small-block or two-region
plans. The active planning table is
`survey_satellite_embedding/experiments/DOWNSTREAM_TASK_PLAN.md`. The next
tables should be built from the 500 m tile grid and shared label sources above:
land-cover classification, built-up / vegetation / water fraction regression,
water mask reconstruction or segmentation for dense models, and optional
retrieval / qualitative panels where the model family supports it.

The immediate T2 acceptance task has already been run from the materialized 2x
downstream cache:

```text
survey_satellite_embedding/experiments/results/downstream_core_2x/embeddings_2x_tile/
```

Treat missing files under `downstream_fraction/embeddings_full_roi/` as
"full-ROI embeddings not prepared yet", not as permission to regenerate them.

The older `survey_satellite_embedding/data/part2_20260502_full/region_b/`
folder contains a coarse `cell_manifest_025deg.csv` with **1056** cells. It is
manifest-only and should be treated as a historical compatibility asset, not the
default design for new survey benchmark experiments.

### Local model weight / asset locations

The benchmark now also provides a **single consolidated local asset folder** for
the 19 canonical public models:

- `research_outputs/model_assets_public19/`
  - one subdirectory per model
  - symlinks to the actual local checkpoints / cache snapshots / precomputed products
  - root manifest at `research_outputs/model_assets_public19/manifest.json`

The underlying assets are still physically stored across the following paths:

- **Repository-managed checkpoints**:
  `research_outputs/model_cache/`
  - `checkpoint_ViT-L_pretrain_fmow_sentinel.pth` (`satmaepp_s2_10b`)
  - `AgriFM.pth` (`agrifm`)
- **Hugging Face local cache**:
  `~/.cache/huggingface/hub/`
  - used by models such as `thor`, `terrafm`, `remoteclip`, `satmae`,
    `satmaepp`, `scalemae`, `dofa`, `terramind`, `prithvi`, and `satvision`
- **`rs-embed` runtime cache**:
  `~/.cache/rs_embed/`
  - used by models such as `anysat`, `wildsat`, `fomo`, and `galileo`
- **Precomputed / local product assets**:
  - `global_0.1_degree_representation/` (`tessera`)
  - `research_outputs/model_cache/geotessera_cache/` (`tessera` registry/cache)
  - Google Earth Engine product access for `gse`
  - local Copernicus product slices cached through the adapter / Hugging Face dataset path

The canonical public model inventory remains the 19 entries listed in
`src/rs_embed/embedders/catalog.py`. The current repository does **not** track any
additional verified private-model embedding outputs alongside those 19 public runs.

## Learn More

📚 [Full documentation](https://cybergis.github.io/rs-embed/)

🪄 [Get Started: Try `rs-embed` Now](https://github.com/cybergis/rs-embed/blob/main/examples/playground.ipynb)

🪀 [Use case: Maize yield mapping Illinois](https://github.com/cybergis/rs-embed/blob/main/examples/demo.ipynb)

📢 [Disscusion](https://github.com/cybergis/rs-embed/discussions)

🧾 [Release policy and versioning](https://cybergis.github.io/rs-embed/releases/)

📌 [Project changelog](https://github.com/cybergis/rs-embed/blob/main/CHANGELOG.md)

## Extending & Contributing

We welcome issues for new model integrations, extension ideas, bugs, and documentation gaps. If you have your own work, or a model or paper that you think would be valuable to include in `rs-embed`, please open an [Issue](https://github.com/cybergis/rs-embed/issues) and share the relevant links, context, and examples.

We also warmly welcome community contributions, including new model support, bug fixes, documentation improvements, and example notebooks. If you would like to contribute directly, please start with the [`extending`](https://cybergis.github.io/rs-embed/extending/) guide and the [contributing guide](https://cybergis.github.io/rs-embed/contributing/).

## 🎖 Acknowledgements

We would like to thank the following organizations and projects that make rs-embed possible: [Google Earth Engine](https://earthengine.google.com), [TorchGeo](https://github.com/torchgeo/torchgeo), [GeoTessera](https://github.com/ucam-eo/geotessera), [TerraTorch](https://github.com/terrastackai/terratorch), [rshf](https://github.com/mvrl/rshf), and the [Copernicus-Embed](https://huggingface.co/datasets/torchgeo/copernicus_embed).

This library also builds upon the incredible work of the Remote Sensing community!(Full list and citations available in our Documentation)

## Citation

```
@article{ye2026modelplacetimeremote,
      title={Any Model, Any Place, Any Time: Get Remote Sensing Foundation Model Embeddings On Demand},
      author={Dingqi Ye and Daniel Kiv and Wei Hu and Jimeng Shi and Shaowen Wang},
      year={2026},
      eprint={2602.23678},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2602.23678},
}
```

## License

This project is released under the [Apache-2.0](https://github.com/cybergis/rs-embed/blob/main/LICENSE)

## Contributors

<a href="https://github.com/cybergis/rs-embed/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=cybergis/rs-embed" />
</a>
