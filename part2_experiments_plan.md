# Part 2: Single-ROI Downstream Experiment Plan

## 1. Current Position

本部分实验不是做一个“19 个模型总排行榜”，而是为综述论文提供一个可复现、
可解释的下游任务比较：在同一个高分辨率武汉 ROI 上，用统一网格、统一标签、
统一 train / validation / test split，观察不同 satellite embedding family 在主流遥感
下游任务上的能力边界。

当前实验锚点以 2x 图为准：

- 数据根目录：`survey_satellite_embedding/data/part2_20260502_full/region_a/`
- ROI bounds：`[114.29, 30.44, 114.53, 30.60]`
- 500 m tile manifest：`tile_manifest_500m.csv`，共 2173 个 tiles
- 最终 public-19 sanity figure：
  `survey_satellite_embedding/experiments/results/part2_model_map_figure/part2_original_map_with_public19_models_2x.png`
- 2x manifest：
  `survey_satellite_embedding/experiments/results/part2_model_map_figure/manifest_2x.json`

`part2_original_map_with_public19_models_2x.png` 是原 reference block 在宽和高方向各
扩展 2 倍后的版本，因此覆盖面积是旧单块图的 4 倍。旧图
`part2_original_map_with_public19_models.png` 只作为历史 sanity check，不再作为当前
实验设计依据。

Region B 的 `cell_manifest_025deg.csv` 只保留为历史兼容资产。除非专门要求历史对比，
不再围绕“small Region A + coarse Region B”设计新的实验主线。

---

## 2. Available Data and Labels

| Local source | Path | What it supports |
| --- | --- | --- |
| Sentinel-2 SR 2021 growing-season composite | `imagery_s2_20210501_20211031/` | visual QA, spectral baselines, model input consistency |
| ESA WorldCover 2021 | `worldcover_2021_blocks/` and columns in `tile_manifest_500m.csv` | land-cover classification, land-cover fraction regression, dense land-cover masks |
| JRC Global Surface Water occurrence | `jrc_occurrence_blocks/` and JRC columns in `tile_manifest_500m.csv` | water fraction regression, water occurrence regression, dense water masks |
| Public-19 2x embedding maps | `experiments/results/part2_model_map_figure/*_2x.npz` | visual sanity check before full-ROI downstream runs |
| Future full-ROI pooled embeddings | planned `embeddings_full_roi/{model}.npz` | T1-T3 all-model downstream tasks over all 2173 tiles |

Current tile class balance from the manifest:

| Class | Count |
| --- | ---: |
| built | 1078 |
| vegetation | 625 |
| water | 409 |
| cropland | 61 |

Cropland is rare, so first results should report both the full four-class setting and a
confidence-filtered or merged-class sensitivity setting.

---

## 3. Downstream Task Plan

| ID | Priority | Task family | Wuhan benchmark | Local truth / data | Open benchmark or dataset to cite / compare | Metrics | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | Must | Classification / mapping | 4-class tile-level land-cover classification: built, vegetation, cropland, water | `local_dominant_class` and `local_dominant_frac` from `tile_manifest_500m.csv` | EuroSAT, BigEarthNet, SEN12MS, Dynamic World / WorldCover land-cover mapping | Macro F1, balanced accuracy, per-class F1, confusion matrix | Ready |
| T2 | Must | Land-cover fraction regression | Built-up, vegetation, cropland, and water fraction regression per 500 m tile | `local_built_frac`, `local_vegetation_frac`, `local_cropland_frac`, `local_water_frac` | land-cover fraction mapping, urban fraction estimation, vegetation cover estimation; WorldCover-derived weak labels | MAE, RMSE, R2, Spearman rho | Ready |
| T3 | Must | Water regression | JRC water occurrence mean and binary water fraction regression | `jrc_occurrence_mean`, `jrc_water_binary_frac` | JRC Global Surface Water, surface-water mapping and flood/water extent benchmarks | MAE, RMSE, Spearman rho, calibration plot | Ready |
| T4 | Should | Dense water segmentation / mask reconstruction | Predict water mask inside each block or tile | `jrc_occurrence_blocks/*.npz`, thresholded or soft occurrence | JRC Global Surface Water, flood extent mapping datasets, Sen1Floods11-style water mapping | IoU, F1, precision, recall, boundary F1 if resolution supports it | Needs dense-output alignment |
| T5 | Should | Dense land-cover segmentation | Predict collapsed WorldCover mask: built / vegetation / cropland / water / other | `worldcover_2021_blocks/*.npz` | LoveDA, DeepGlobe Land Cover, DFC2020, Dynamic World / WorldCover segmentation-style mapping | mIoU, macro F1, per-class IoU | Needs dense-output alignment |
| T6 | Should | Retrieval / cross-modal | Retrieve Wuhan tiles by text query or label prototypes | pseudo relevance from manifest fractions; optional manual top-k QA | RemoteCLIP-style retrieval, RSICD, RSITMD, UCM-Captions, Million-AID captions if needed | Recall@K, mAP, median rank, qualitative panels | Needs query set |
| T7 | Could | Change detection | Seasonal water expansion / contraction or land-cover-change proxy | needs second temporal truth export from JRC monthly water or Dynamic World windows | OSCD, LEVIR-CD, xView2/xBD for disaster change, flood-change datasets | F1, IoU, precision, recall, change-area MAE | Not ready |
| T8 | Could | Temporal sequence task | Phenology or seasonal vegetation signal prediction | needs monthly Sentinel-2 / Dynamic World / NDVI trajectory labels | PASTIS, crop type time-series benchmarks, phenology monitoring datasets | MAE / RMSE for continuous targets, Macro F1 for phase classes | Not ready |
| T9 | Could | Object / instance detection | Building or large man-made object subset | needs external building footprints or manual labels; Sentinel-2 resolution limits small objects | SpaceNet buildings, xView, DOTA, FAIR1M for object detection context | AP50, AP, recall; fallback building-presence F1 | Appendix only |

The main paper should prioritize T1-T5 because they are closest to the current prepared
Wuhan data. T6 is useful for multimodal models but should be marked family-specific. T7-T9
are coverage extensions and should not block the first result table.

---

## 4. First Implementation Order

1. Freeze a spatial split file: `downstream_splits_500m.csv`.
2. Materialize core labels: `downstream_labels_500m.csv`.
3. Export pooled embeddings for all 19 models over the 2173 tiles.
4. Run T1 with linear probe and k-NN baseline.
5. Run T2-T3 with ridge regression and a shallow MLP sensitivity check.
6. Build dense truth alignment utilities for JRC and WorldCover masks.
7. Run T4-T5 for models with dense token grids, plus pooled-broadcast weak baselines.
8. Add T6 retrieval only after the core tables are stable.

---

## 5. Paper Tables and Figures

| Output | Content |
| --- | --- |
| Dataset / task table | ROI bounds, tile count, class balance, label sources, task list |
| Core all-model table | T1 classification plus T2-T3 regression quality for 19 models |
| Dense prediction table | T4 water and T5 land-cover segmentation for dense-capable models |
| Quality-runtime figure | downstream quality versus extraction/runtime cost |
| Qualitative figure | 2x public-19 map figure plus selected dense/retrieval panels |

The qualitative anchor is always the 2x public-19 figure, not the old single-block figure.
