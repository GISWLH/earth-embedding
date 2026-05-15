# Wuhan Single-ROI Downstream Task Plan

## Current Anchor

The active benchmark is the single high-resolution Wuhan ROI, not the old
two-region design. All downstream tasks should start from:

- Data root: `survey_satellite_embedding/data/part2_20260502_full/region_a/`
- ROI bounds: `[114.29, 30.44, 114.53, 30.60]`
- Tile manifest: `tile_manifest_500m.csv` with 2173 tiles
- Final map sanity case:
  `survey_satellite_embedding/experiments/results/part2_model_map_figure/part2_original_map_with_public19_models_2x.png`
- Final map manifest:
  `survey_satellite_embedding/experiments/results/part2_model_map_figure/manifest_2x.json`

The main principle is: one ROI, one 500 m tile grid, one train/validation/test
split, many downstream heads. The 2x public-19 map is the visual sanity case;
the actual downstream tables should scale to the full 2173-tile manifest where
the task uses pooled embeddings.

## Available Ground Truth Sources

| Source | Local path | Native target | How it is used |
| --- | --- | --- | --- |
| ESA WorldCover 2021 | `worldcover_2021_blocks/*.npz` and aggregated columns in `tile_manifest_500m.csv` | 10 m land-cover classes | dominant land-cover class, land-cover fractions, dense land-cover masks |
| JRC Global Surface Water occurrence | `jrc_occurrence_blocks/*.npz` and `jrc_*` columns in `tile_manifest_500m.csv` | 0-100 water occurrence | binary/soft water mask, water fraction, water-occurrence regression |
| Sentinel-2 SR composite | `imagery_s2_20210501_20211031/*.npz` | 10-band image input | spectral baseline, NDVI/NDBI/MNDWI baselines, visual QA |
| Public-19 embeddings | `experiments/results/part2_model_map_figure/*_2x.npz` and future full-ROI exports | pooled or dense model features | downstream predictors; current 2x output is the sanity case before full ROI runs |
| Optional manual labels | future `annotations/` folder | object boxes, retrieval relevance, change QA | only for appendix tasks that cannot get reliable automatic truth |

## Task Plan Table

| ID | Priority | Downstream family | Concrete Wuhan benchmark | Prediction unit | Ground truth construction | Model input | Metrics | Existing benchmark / open data to cite or extend | Implementation status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | MUST | Classification / mapping | 4-class land-cover classification: `built`, `vegetation`, `cropland`, `water` | 500 m tile | Use `local_dominant_class` from `tile_manifest_500m.csv`; optionally filter low-confidence tiles by `local_dominant_frac >= 0.5` or report both filtered and full results | pooled embedding per tile | macro F1, balanced accuracy, per-class F1, confusion matrix | EuroSAT, BigEarthNet, SEN12MS, Dynamic World / WorldCover land-cover mapping | Ready; truth already exists |
| T2 | MUST | Regression / continuous estimation | Built-up, vegetation, cropland, water fraction regression | 500 m tile | Use `local_built_frac`, `local_vegetation_frac`, `local_cropland_frac`, `local_water_frac`; these are WorldCover-derived fractions collapsed into local classes | pooled embedding per tile | MAE, RMSE, R2, Spearman rho | WorldCover-derived fraction mapping, urban fraction estimation, vegetation cover estimation | 2x acceptance completed in `results/downstream_fraction_2x/`; full-ROI embeddings not prepared |
| T3 | MUST | Water regression | JRC water occurrence / binary-water fraction regression | 500 m tile | Use `jrc_occurrence_mean` and `jrc_water_binary_frac`; treat occurrence as soft persistence and binary fraction as water area target | pooled embedding per tile | MAE, RMSE, Spearman rho, calibration plot | JRC Global Surface Water, surface-water mapping, flood/water extent benchmarks | Ready; truth already exists |
| T4 | SHOULD | Dense water segmentation / mask reconstruction | Predict water mask inside each block or tile | dense grid or per-pixel mask | Use `jrc_occurrence_blocks/*.npz`; threshold occurrence, e.g. `>= 50`, for binary water, and keep raw 0-100 occurrence for soft target | dense token grid when available; pooled embedding broadcast as weak baseline | IoU, F1, precision, recall, boundary F1 if resolution permits | JRC Global Surface Water, Sen1Floods11-style water mapping, flood extent datasets | Needs dense-output alignment script |
| T5 | SHOULD | Dense land-cover segmentation | Predict collapsed WorldCover mask: built / vegetation / cropland / water / other | dense grid or per-pixel mask | Use `worldcover_2021_blocks/*.npz`; collapse ESA WorldCover codes to benchmark classes; ignore no-data and rare classes if needed | dense token grid when available; pooled broadcast baseline | mean IoU, macro F1, per-class IoU | LoveDA, DeepGlobe Land Cover, DFC2020, Dynamic World / WorldCover segmentation-style mapping | Needs dense-output alignment script |
| T6 | SHOULD | Retrieval / cross-modal | Text or prototype retrieval over fixed Wuhan tile bank | 500 m tile | Build pseudo-relevance from manifest classes and fractions: e.g. `large lake` = high `local_water_frac`, `dense urban` = high `local_built_frac`, `green corridor` = high `local_vegetation_frac`; optionally manually screen top-k | image/text embeddings for language models; image embeddings for prototype search | Recall@K, mAP, median rank, qualitative panel | RemoteCLIP-style retrieval, RSICD, RSITMD, UCM-Captions, Million-AID captions if needed | Needs query set and relevance thresholds |
| T7 | COULD | Change detection | Seasonal water-change or land-cover-change proxy within Wuhan ROI | 500 m tile or dense mask | Need a second temporal label layer. Preferred: query JRC monthly water history or Dynamic World by two windows and compare water probability/mask; avoid claiming urban change from single-year WorldCover | paired embeddings or feature difference | F1, IoU, precision, recall, change-area MAE | OSCD, LEVIR-CD, xView2/xBD, flood-change datasets | Not ready; needs new temporal truth export |
| T8 | COULD | Temporal sequence task | Phenology / seasonal vegetation signal prediction | cropland/vegetation tiles | Need multi-month Sentinel-2 or Dynamic World vegetation series; derive NDVI seasonal amplitude, peak month, or vegetation fraction trajectory as target | temporal-capable embeddings or monthly pooled embeddings | MAE/RMSE for continuous phenology, macro F1 for phase class | PASTIS, crop type time-series benchmarks, phenology monitoring datasets | Not ready; needs monthly data prep |
| T9 | COULD | Object / instance detection | Building or large man-made object detection subset | object box / instance | Need external building footprint or manual annotation. Possible sources: OSM building footprints, Microsoft/Google building footprints if available, or manual boxes on Sentinel-2/HR imagery. Sentinel-2 resolution makes small objects weak | dense embeddings plus lightweight detector, or tile-level proxy first | AP50, AP, recall; fallback tile-level building-presence F1 | SpaceNet buildings, xView, DOTA, FAIR1M for object detection context | Appendix only; requires new labels |

## Ground Truth Recipe By Task

### T1 Classification

1. Read `tile_manifest_500m.csv`.
2. Use `local_dominant_class` as the label.
3. Main setting: keep classes with enough support: built, vegetation, water,
   cropland.
4. Recommended first table:
   - strict split: `local_dominant_frac >= 0.5`
   - full split: all 2173 tiles
5. Use a fixed spatial split so nearby tiles do not leak across train/val/test.
   A simple first pass is block- or row/column-based splitting, then freeze the
   split file.

### T2-T3 Fraction Regression

1. Read the same manifest.
2. Targets:
   - WorldCover fractions: `local_built_frac`, `local_vegetation_frac`,
     `local_cropland_frac`, `local_water_frac`
   - JRC water targets: `jrc_occurrence_mean`, `jrc_water_binary_frac`
3. Train ridge regression or a shallow MLP with frozen embeddings.
4. Report one table with one row per model and one metric group per target.

### T4-T5 Dense Prediction

1. Load the block-level truth arrays:
   - JRC water occurrence from `jrc_occurrence_blocks/`
   - WorldCover map from `worldcover_2021_blocks/`
2. Load each model's dense map output when available.
3. Reproject/resize the truth mask onto the model grid using nearest-neighbor for
   categorical labels and area/linear aggregation for soft water occurrence.
4. Evaluate dense-capable models directly.
5. Add a pooled-broadcast baseline to show the value of spatial token grids, but
   keep it clearly marked as a weak baseline.

### T6 Retrieval

1. Build a tile bank from the 2173 manifest rows.
2. Define query concepts from label columns:
   - `large inland lake`: high `local_water_frac`
   - `dense urban block`: high `local_built_frac`
   - `green corridor`: high `local_vegetation_frac`
   - `cropland mosaic`: high `local_cropland_frac`
3. Construct pseudo-relevance labels by thresholds, for example top 10-20% by
   target fraction or absolute fraction `>= 0.6`.
4. Run text-to-image retrieval for RemoteCLIP-like models and prototype retrieval
   for image-only models.
5. Use this as a family-specific appendix unless the relevance labels are clean.

### T7-T9 Extensions

These should not block the main table. They only enter after T1-T5 are stable:

- T7 change detection needs a second temporal truth export, preferably water
  change from JRC monthly history or Dynamic World windows.
- T8 temporal sequence needs monthly Sentinel-2/Dynamic World labels and should
  be limited to vegetation/cropland tiles.
- T9 object detection needs external or manual object labels; with Sentinel-2 it
  is safer to start as a tile-level building-presence proxy before attempting AP.

## Execution Order

| Step | Output | Purpose |
| --- | --- | --- |
| 1 | `downstream_splits_500m.csv` | Freeze train/val/test split for all tasks |
| 2 | `downstream_labels_500m.csv` | Materialize classification and regression labels from the manifest |
| 3 | `embeddings_full_roi/{model}.npz` | Export pooled embeddings for all 19 models over the 2173 tiles |
| 4 | `results/downstream_core/classification.csv` | T1 metrics |
| 5 | `results/downstream_fraction_2x/fraction_regression.csv` | T2 2x acceptance metrics from cached local embeddings |
| 6 | `results/downstream_dense/water_segmentation.csv` | T4 metrics for dense-capable models |
| 7 | `results/downstream_dense/landcover_segmentation.csv` | T5 metrics for dense-capable models |
| 8 | `results/downstream_retrieval/retrieval.csv` | T6 optional retrieval metrics |

## Main-Paper vs Appendix Split

| Paper location | Tasks | Reason |
| --- | --- | --- |
| Main table | T1 classification, T2 fraction regression, T3 JRC water regression | Works for all or nearly all 19 models using pooled embeddings |
| Main dense table or figure | T4 water segmentation, T5 land-cover segmentation | Tests whether dense token grids preserve spatial structure |
| Appendix / qualitative | T6 retrieval | Family-specific; strongest for language-aligned models |
| Appendix / future work | T7 change, T8 temporal sequence, T9 object detection | Needs extra truth sources beyond the current single-year prepared assets |

## Immediate Next Implementation Target

Start with T1-T3 because their truth already exists in
`tile_manifest_500m.csv`. The first runnable script should:

1. create a frozen spatial split,
2. build the label table,
3. export or load pooled embeddings for each model,
4. run linear classification and ridge regression,
5. write CSV/Markdown summaries for the paper.
