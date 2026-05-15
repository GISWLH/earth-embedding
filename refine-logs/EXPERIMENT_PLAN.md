# Experiment Plan

**Problem**: The survey already has a model inventory and a first Wuhan pilot, but the experimental section is still too narrow. Right now it overweights a small local classification setup and under-covers the mainstream remote sensing downstream task families.
**Method Thesis**: A paper-ready benchmark for satellite embeddings should combine **cross-scale comparison** with **task-family coverage**. The benchmark should therefore use exactly **two spatial regions**: one fine-scale local ROI and one regional scale-fair ROI. Temporal tasks such as change detection should be implemented as an additional **time slice** within the fine-scale ROI rather than as a third geographic region.
**Date**: 2026-04-19

## Claim Map
| Claim | Why It Matters | Minimum Convincing Evidence | Linked Blocks |
|-------|-----------------|-----------------------------|---------------|
| C1. Different embedding families are useful at different spatial supports and task types; there is no single universally best family once evaluation respects native scale. | This is the main paper message. Without evidence, the review is only a taxonomy. | One fine-scale benchmark and one coarse-scale benchmark that visibly change the family ordering, plus runtime / deployment evidence. | B1, B4 |
| C2. A credible satellite-embedding review should cover the mainstream EO downstream families, not only easy local classification tasks. | This makes the evaluation look like a real remote sensing paper rather than a convenience benchmark. | The final benchmark must include classification, dense segmentation, change detection, and regression, with retrieval as a family-specific extension. | B1, B2, B3, B4, B5 |
| C3. Frozen lightweight probes are sufficient for the review; the paper does not need a large fine-tuning study to make its point. | This keeps the benchmark compact and reproducible. | Linear / ridge probes should stay close to small stronger heads on representative models. | B5 |

## What the Recent EO Literature Repeats Most Often

From the local paper library and recent survey abstracts, the mainstream downstream families are:

| Task family | Typical examples in recent EO / FM papers | Why it is mainstream | Fit for an embedding-centered review | Planned role here |
|-------------|--------------------------------------------|----------------------|--------------------------------------|-------------------|
| Classification / mapping | scene classification, land-cover mapping, crop type, climate zone | Most common transfer baseline across SatMAE, TerraFM, AnySat, Copernicus-style benchmarks | Very high | **Core** |
| Semantic segmentation / dense prediction | land-cover segmentation, water / flood / burn scar / deforestation mapping | Standard dense downstream family in EO papers | High for grid outputs, moderate for pooled-only models | **Core** |
| Change detection | bi-temporal land-cover change, flood expansion, deforestation, urban change | One of the most common temporal EO tasks | High for temporal or annual embeddings | **Core** |
| Regression / continuous estimation | biomass, canopy height, built fraction, vegetation fraction, yield proxies | EO frequently predicts continuous quantities rather than only classes | Very high | **Core** |
| Object / instance detection | buildings, ships, vehicles, aircraft | Very mainstream in high-resolution EO, but strongly detector-head-dependent | Medium | **Appendix / future extension** |
| Retrieval / cross-modal alignment | text-to-image retrieval, image retrieval, zero-shot matching | Increasingly important for vision-language EO models | High, but only for some families | **Family-specific appendix** |
| Temporal sequence tasks | crop type time series, phenology, seasonal monitoring, forecasting | Common in multi-temporal EO and agriculture papers | High, but overlaps with change detection and regression in practice | **Covered through change + regression** |

This task taxonomy is the key design update. The paper should no longer stop at local land-cover classification plus one water task. The final benchmark should explicitly map **all 7 task families** into the paper structure, even if they do not all carry the same weight in the main text.

## Paper Storyline
- Main paper must prove:
  - fine-scale transfer and coarse-scale transfer are different evaluation regimes
  - precomputed products should be evaluated at their operating scale, not forced into tiny local tiles
  - the benchmark covers the mainstream EO downstream families rather than only "easy" tasks
  - simple frozen probes are enough to compare representation quality for this survey
- Appendix can support:
  - full 19-model coarse benchmark once the main paper cohort is stable
  - family-specific multimodal retrieval
  - detector-style or object-centric case studies
- Experiments intentionally cut:
  - full end-to-end fine-tuning
  - a giant multi-dataset benchmark wishlist
  - forcing every model into every task when the output form is clearly incompatible

## Region Design

### Region A: Local mixed-landscape ROI
- **Name**: Wuhan East Lake - Tangxun Lake corridor
- **Extent**: about `20 km x 20 km`
- **Why keep it**:
  - mixed water / vegetation / cropland / built structure in one compact area
  - natural fit for 10 m to 30 m embeddings
  - already exists in the workspace
- **Sampling unit**: `500 m x 500 m` tiles on a regular grid
- **Labels**:
  - ESA WorldCover 2021 for dominant class and class fractions
  - JRC Global Surface Water or Dynamic World for dense water masks
  - pre / post seasonal water masks for local change detection

### Region B: Regional scale-fair ROI
- **Name**: Middle-Lower Yangtze macro-region
- **Suggested box**: roughly `28.0-33.5 N, 110.0-122.0 E`
- **Why add it**:
  - the Wuhan-only setup unfairly collapses coarse products such as Copernicus and SatVision
  - this box still matches the survey narrative while including plains, lakes, cropland, forest, and major urban areas
  - it is large enough to support `0.25 degree` products
- **Sampling unit**: `0.25 degree` cells
- **Labels**:
  - aggregate ESA WorldCover 2021 to cell-level fractions
  - use JRC water fraction as a second continuous target

There is **no third spatial region** in the final design. Change detection is folded back into **Region A** as a temporal task. This keeps the benchmark aligned with your original concept: one precise local region plus one coarse large region.

## Model Cohorts

### Main paper cohort
Use one or two strong representatives per family, chosen for reliability and tractable runtime.

- **Precomputed fine-scale**: `gse`
- **Precomputed coarse-scale**: `copernicus`
- **Masked autoencoder family**: `satmaepp_s2_10b`
- **Vision-language family**: `remoteclip`
- **Multimodal generalist family**: `galileo`
- **Domain-specialized family**: `agrifm`
- **Optional appendix model**: `tessera`
- **Optional coarse all-sky appendix model**: `satvision`

This representative cohort is the paper-safe default. A full 19-model sweep is appendix-only after the representative benchmark is stable.

### Appendix extension cohort
- all 19 canonical models
- only after Region A and Region B pipelines are validated
- only required for the coarse benchmark and capability / runtime summary

## Final Task Portfolio for the Paper

- **T1. Fine-scale land-cover classification**
  - Region A
  - 4 dominant classes: `water`, `vegetation`, `cropland`, `built`
- **T2. Fine-scale fraction regression**
  - Region A
  - continuous targets: `water`, `green`, `built`
- **T3. Fine-scale dense segmentation**
  - Region A
  - binary `water` first; optional dense land-cover extension later
- **T4. Temporal change detection**
  - Region A
  - binary water expansion / contraction first, using paired dates or seasonal windows
- **T5. Fine-scale object / instance detection**
  - Region A
  - building or large-manmade-object detection on a local annotated subset
- **T6. Fine-scale temporal sequence task**
  - Region A
  - crop type time-series classification or phenology-stage prediction on cropland subset
- **T7. Regional scale-fair classification**
  - Region B
  - dominant macro-class classification at `0.25 degree`
- **T8. Regional scale-fair regression**
  - Region B
  - cell-level `water` and `green` fractions
- **T9. Family-specific retrieval**
  - Region A + Region B tile bank
  - only for language-aligned models

## Seven-Task Coverage Map

| User-level task family | Concrete benchmark task | Region | Paper role | Notes |
|------------------------|-------------------------|--------|------------|-------|
| 1. Classification / mapping | T1 local land-cover classification + T7 regional macro-class classification | A + B | **Core** | Covers both fine and coarse scale |
| 2. Semantic segmentation / dense prediction | T3 local dense water / land-cover segmentation | A | **Core** | Dense benchmark for grid-capable models |
| 3. Change detection | T4 local bi-temporal water / land-cover change | A | **Core** | Time dimension inside the local ROI |
| 4. Regression / continuous estimation | T2 local fraction regression + T8 regional fraction regression | A + B | **Core** | Covers continuous EO targets |
| 5. Object / instance detection | T5 local building / large-object detection subset | A | **Appendix / extension** | Important to cover explicitly, but likely resolution-limited for some models |
| 6. Retrieval / cross-modal | T9 retrieval on fixed tile bank | A + B | **Appendix / family-specific** | For language-aligned models only |
| 7. Temporal sequence tasks | T6 crop-type or phenology time-series task | A | **Appendix / temporal extension** | Separate from change detection so that long-range temporal reasoning is still represented |

So the corrected statement is: **the benchmark now covers all 7 task families**, but it does so with different priority levels:

- **Main paper core**: classification, segmentation, change detection, regression, cross-scale comparison
- **Appendix / extension**: object detection, retrieval, temporal sequence tasks

## Experiment Blocks

### Block 1: Local classification and regression benchmark
- **Claim tested**: Fine-scale embeddings from major families can be compared fairly on a shared local ROI using frozen features and lightweight heads.
- **Why this block exists**: This is the anchor result for city-scale or watershed-scale transfer.
- **Dataset / split / task**:
  - Region A
  - T1 + T2
  - stratified `60 / 20 / 20`
- **Compared systems**:
  - main paper cohort except clearly incompatible coarse-only models
  - one non-neural baseline: per-tile mean spectral features + linear / ridge head
- **Metrics**:
  - T1: macro F1, balanced accuracy, per-class F1
  - T2: RMSE, MAE, Spearman
  - both: extraction time per tile, peak GPU memory, failure rate
- **Setup details**:
  - frozen encoder only
  - on-the-fly models use `2021-05-01` to `2021-10-31`
  - annual products use `2021`
  - 3 probe seeds
  - linear probe for T1, ridge regression for T2
- **Success criterion**:
  - at least three families beat the spectral baseline clearly
  - family differences are visible without everyone saturating
- **Failure interpretation**:
  - if nearly all models saturate, the task is too easy; tighten the dominance threshold or enlarge the class set
- **Table / figure target**:
  - Main paper Table 1
  - Main paper Figure 1
- **Priority**: MUST-RUN

### Block 2: Local dense segmentation benchmark
- **Claim tested**: Models that preserve spatial structure provide added value beyond pooled classification.
- **Why this block exists**: Semantic segmentation and dense prediction are part of the standard EO task set and should appear in the main paper.
- **Dataset / split / task**:
  - Region A
  - T3
- **Compared systems**:
  - models with practical dense outputs or spatial product grids
  - compare against a pooled-feature broadcast baseline
- **Metrics**:
  - IoU, F1, boundary F1
  - inference time per patch
- **Setup details**:
  - fixed patch size
  - lightweight decoder or linear pixel head only
- **Success criterion**:
  - dense-capable models beat pooled-broadcast baselines
- **Failure interpretation**:
  - if the gap is weak, keep the task as a compact complement rather than the center of the paper
- **Table / figure target**:
  - Main paper Table 2 or a compact figure
- **Priority**: MUST-RUN

### Block 3: Temporal change detection benchmark
- **Claim tested**: Temporal and annual embeddings should be judged on a mainstream EO temporal task, not only on single-date transfer.
- **Why this block exists**: Change detection is one of the most standard downstream families in EO foundation-model papers.
- **Dataset / split / task**:
  - Region A
  - T4
- **Compared systems**:
  - temporal-capable representatives first: `galileo`, `agrifm`, `gse`, `tessera`, `copernicus`
  - single-date models can participate through paired-feature differencing if operationally stable
- **Metrics**:
  - F1, IoU, precision / recall
  - optional AUROC if applicable
- **Setup details**:
  - simplest baseline: absolute embedding difference + linear classifier
  - same temporal gap for all compatible models
- **Success criterion**:
  - temporal-aware or annual-product models show a meaningful advantage over pure single-date baselines
- **Failure interpretation**:
  - if all models are weak, the temporal label source or date pair is likely too noisy
- **Table / figure target**:
  - Main paper temporal task table or appendix, depending on result strength
- **Priority**: MUST-RUN

### Block 4: Object detection and temporal sequence extensions
- **Claim tested**: The review's task coverage is broad enough to reflect mainstream EO downstream practice, including object-centric and long-horizon temporal tasks.
- **Why this block exists**: Without this block, the 7-task taxonomy is only partially instantiated.
- **Dataset / split / task**:
  - Region A
  - T5: building or large-object detection on an annotated subset
  - T6: crop type time-series classification or phenology-stage prediction on cropland subset
- **Compared systems**:
  - detection: only models whose resolution and output form make the task meaningful
  - temporal sequence: temporal-capable models first, plus simple pooled baselines
- **Metrics**:
  - detection: AP, AP50, recall
  - temporal sequence: macro F1 or MAE, depending on label type
- **Setup details**:
  - keep this block as a controlled extension, not the main benchmark center
  - if detection is too mismatched to model resolution, explicitly report that and keep the block as a documented limitation / appendix experiment
- **Success criterion**:
  - at least one usable object-centric task and one usable long-horizon temporal task are represented in the final benchmark package
- **Failure interpretation**:
  - if detection remains fundamentally mismatched, keep it as a clearly documented appendix limitation rather than pretending it is a fair main-table task
- **Table / figure target**:
  - Appendix tables
  - optional qualitative figure
- **Priority**: NICE-TO-HAVE but REQUIRED for full 7-task coverage

### Block 5: Regional scale-fair benchmark
- **Claim tested**: Coarse precomputed products become competitive when evaluated at the scale they were designed for, and model ranking changes across spatial support.
- **Why this block exists**: This block defends the paper's most important methodological point: a survey benchmark must respect native operating scale.
- **Dataset / split / task**:
  - Region B
  - T7 + T8
  - stratified `60 / 20 / 20`
- **Compared systems**:
  - full main paper cohort
  - appendix extension cohort after validation
- **Metrics**:
  - T5: macro F1, balanced accuracy
  - T6: RMSE, MAE, Spearman
  - runtime per cell, failure rate
- **Setup details**:
  - same geographic cell support for every model
  - on-the-fly models first try direct `BBox` extraction over the cell
  - if large-cell extraction is unstable, switch to a fixed 4-subtile average and report that explicitly
  - annual products use nearest valid year, documented per model
- **Success criterion**:
  - `copernicus` and `satvision` become evaluable rather than trivially failing
  - family ordering differs from Block 1 in a reviewer-visible way
- **Failure interpretation**:
  - if coarse products still fail, that is still a useful review result about deployment constraints
- **Table / figure target**:
  - Main paper cross-scale comparison table
  - Main paper Figure 2
- **Priority**: MUST-RUN

### Block 6: Probe simplicity and family-specific retrieval
- **Claim tested**: The survey's conclusions are about the embedding, not about a heavy downstream head; additionally, language-aligned families should be tested on at least one task that matches their design intent.
- **Why this block exists**: This keeps the main benchmark honest while also giving RemoteCLIP / WildSAT-style models an appropriate task family.
- **Dataset / split / task**:
  - simplicity: Region A classification and Region B classification
  - retrieval: Region A + Region B tile bank with text queries such as `large inland lake`, `dense urban block`, `cropland mosaic`, `forest hillside`
- **Compared systems**:
  - simplicity: `gse`, `copernicus`, `satmaepp_s2_10b`, `remoteclip`, `galileo`, `agrifm`
  - retrieval: `remoteclip`, `wildsat`, optionally future text-aligned models
- **Metrics**:
  - simplicity: macro F1, training time, variance
  - retrieval: Recall@K, median rank, qualitative retrieval panel
- **Setup details**:
  - simplicity compares linear vs 2-layer MLP vs k-NN
  - retrieval uses a fixed tile bank and frozen image / text embeddings
- **Success criterion**:
  - linear stays within about `2` macro-F1 points of stronger simple heads on most models
  - retrieval produces semantically sensible ranking for language-aligned models
- **Failure interpretation**:
  - if MLP changes ranking materially, report both probe choices
  - if retrieval is weak, keep it as a family-specific appendix rather than force it into the core narrative
- **Table / figure target**:
  - simplicity: appendix table or short main-text note
  - retrieval: appendix qualitative figure
- **Priority**: MUST-RUN for simplicity; NICE-TO-HAVE for retrieval

## Run Order and Milestones
| Milestone | Goal | Runs | Decision Gate | Cost | Risk |
|-----------|------|------|---------------|------|------|
| M0 | Validate data and metric pipeline | Build Region A tiles, Region A temporal pairs, Region B cells, label aggregation, one toy probe | Stop if labels are too imbalanced or temporal masks are too noisy | Low CPU + very low GPU | Label leakage or trivial labels |
| M1 | Validate representative extraction | Smoke-test `gse`, `satmaepp_s2_10b`, `remoteclip`, `galileo`, `agrifm`, `copernicus` on all applicable tasks | Stop if more than two representative models are operationally unstable | Low to medium GPU | Adapter-specific failures |
| M2 | Run the local core tasks | Block 1 and Block 2 on representative cohort | Continue only if classification is not saturated and dense labels are credible | Medium GPU | Local task too easy |
| M3 | Run the temporal core and scale-fair core | Block 3 and Block 5 on representative cohort, then coarse-product additions | Continue only if temporal labels and coarse extraction are meaningful | Medium GPU | Large-cell instability or weak temporal labels |
| M4 | Run task-coverage extensions | Block 4 plus simplicity part of Block 6 | Continue only if extension tasks are meaningful and do not derail the main tables | Medium GPU | Resolution mismatch for detection |
| M5 | Polish and appendix | Retrieval, full 19-model regional extension, qualitative panels | Skip extras if they delay main tables | Medium to high GPU | Scope creep |

## Compute and Data Budget
- **Total estimated GPU-hours**:
  - main paper representative cohort: about `30-50` GPU-hours if caching and batch export behave normally
  - appendix full regional extension: add about `15-30` GPU-hours
- **Data preparation needs**:
  - WorldCover aggregation
  - JRC / Dynamic World water masks
  - temporal change masks inside Region A
  - cached tile / cell manifests for Regions A / B
- **Human evaluation needs**:
  - none for the core benchmark
  - optional manual screening for retrieval only
- **Biggest bottleneck**:
  - slow per-sample extraction for some models; the main paper should therefore use a representative cohort, not all 19 models everywhere

## Risks and Mitigations
- **Risk**: Region A classification is too easy.
- **Mitigation**: use 4 classes, tighten dominance threshold, and enlarge the balanced subset.

- **Risk**: Region B `BBox` extraction is unstable for some on-the-fly models.
- **Mitigation**: fall back to a fixed 4-subtile average and document the aggregation rule explicitly.

- **Risk**: Region A change labels are noisy or too sparse.
- **Mitigation**: start with water change rather than urban object change, and only then consider harder change-detection labels.

- **Risk**: Object detection may be fundamentally mismatched to the current model resolutions.
- **Mitigation**: keep it as an appendix / documented limitation if needed, but still represent the task family explicitly in the benchmark design.

- **Risk**: Reviewers ask why not evaluate all 19 models on every task.
- **Mitigation**: keep the main paper representative and claim-driven; put the full 19-model extension in the appendix with runtime / capability context.

- **Risk**: Copernicus or SatVision still look weak.
- **Mitigation**: keep them in the story anyway if the weakness is the result; scale mismatch is a core review finding, not an embarrassment.

- **Risk**: Probe choice changes the ranking.
- **Mitigation**: elevate the simplicity comparison into the main paper and report both probe choices.

## Final Checklist
- [ ] Main paper tables are covered
- [ ] Mainstream EO task families are covered
- [ ] Cross-scale comparison is covered
- [ ] Simplicity is defended
- [ ] Frontier contribution is explicitly not claimed for this review benchmark
- [ ] Nice-to-have runs are separated from must-run runs
