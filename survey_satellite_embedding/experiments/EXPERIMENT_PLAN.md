# Small-Area Benchmark Plan

## Goal

Build a reproducible, embedding-centered benchmark that compares all 19 canonical `rs-embed` models under the same ROI, label sources, and lightweight downstream heads.

## Study Area

- **Pilot ROI**: Wuhan East Lake and Tangxun Lake urban-water-vegetation corridor
- **Center**: `30.52 N, 114.41 E`
- **Nominal extent**: `20 km x 20 km`
- **Why this ROI**:
  - mixed urban, cropland, forest, and water classes
  - strong spatial texture at Sentinel-2 scale
  - enough heterogeneity for classification, segmentation, and regression in one compact area
  - compatible with annual precomputed products and on-the-fly Sentinel-based models

The draft ROI polygon is stored in `experiments/roi_wuhan_east_lake.geojson`.

## Data and Labels

- **Base imagery**: Sentinel-2 SR composite for 2021 growing season
- **Precomputed annual models**: use the nearest available annual layer for 2021
- **Land-cover labels**: ESA WorldCover 2021
- **Water mask**: JRC Global Surface Water occurrence or Dynamic World water class
- **Regression target**: tile-level built-up fraction or vegetation fraction aggregated from WorldCover

## Benchmark Tasks

### Task A. Tile Classification

- Predict 6 coarse classes: water, trees, cropland, built-up, bare/sparse, grass/shrub
- Use pooled embeddings only
- Train linear probe and `k`-NN baseline
- Report macro F1, balanced accuracy, and per-class F1

### Task B. Water Segmentation

- Predict binary water mask on a regular grid
- Start with dense token grids when available; otherwise broadcast pooled embeddings to tile level
- Report IoU, F1, and boundary F1 when feasible

### Task C. Fraction Regression

- Predict built-up fraction or vegetation fraction for each tile
- Use ridge regression on pooled embeddings
- Report MAE, RMSE, and Spearman correlation

### Optional Task D. Text-to-Region Retrieval

- RemoteCLIP and other multimodal-capable models only
- Query examples: `dense urban area`, `small inland lake`, `cropland mosaic`
- Report Recall@K qualitatively and quantitatively if annotation budget permits

## Fairness Rules

- Use the same tile centroids for all models.
- Keep the same train/validation/test split across models.
- Use the same year or nearest annual product for precomputed layers.
- Do not fine-tune encoder weights in the first benchmark pass.
- Report both predictive quality and extraction runtime.

## Extraction Protocol

- Default tile size: `224 x 224` pixels for models that require image resizing internally
- Standard temporal window: `2021-05-01` to `2021-10-31`
- Standard optical source: `COPERNICUS/S2_SR_HARMONIZED`
- Save both pooled vectors and dense outputs when the adapter exposes them
- Record:
  - embedding dimension
  - elapsed inference time per tile
  - peak GPU memory
  - failed models or unsupported task/output modes

## Result Tables for the Paper

- **Table 1**: dataset and task summary
- **Table 2**: all-model benchmark table with quality + runtime
- **Figure 1**: task transfer matrix by model family
- **Figure 2**: quality vs. latency scatter
- **Figure 3**: family-level radar or grouped bar summary

## Execution Order

1. Generate the tile grid and labels for the Wuhan ROI.
2. Extract embeddings for all 19 models.
3. Train linear and ridge heads.
4. Aggregate results by task and by family.
5. Produce paper-ready CSV tables and plots.

## Risks and Mitigations

- **Precomputed products may be coarse**: report native resolution explicitly and evaluate at a coarser tile aggregation when needed.
- **Temporal mismatch across models**: use annual tags where required and document the mismatch.
- **Dense output availability differs**: keep pooled-embedding tasks as the mandatory baseline, dense segmentation as a secondary analysis.
