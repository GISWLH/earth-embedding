# Initial Experiment Results

**Date**: 2026-05-02  
**Plan**: `refine-logs/EXPERIMENT_PLAN.md`

## M0: Data preparation — PASSED

- Full two-region GEE preparation completed at `survey_satellite_embedding/data/part2_20260502_full`.
- Region A artifacts:
  - 16 Sentinel-2 blocks
  - 16 WorldCover blocks
  - 16 JRC occurrence blocks
  - `tile_manifest_500m.csv` with **2173** tiles
- Region B artifacts:
  - `cell_manifest_025deg.csv` with **1056** cells

## M1: All-model smoke extraction — PASSED

- Fresh smoke outputs were written to `survey_satellite_embedding/experiments/results/all_models_smoke_20260502`.
- A new runner, `survey_satellite_embedding/experiments/run_part2_all_models_smoke.py`, now performs two-region pooled embedding extraction with:
  - Region A balanced local samples for fine-scale families
  - Region B coarse cells for coarse-scale families
  - local checkpoint wiring for `satmaepp_s2_10b` and `agrifm`

### Fresh current-run passes (19 models)

| Model | Split | Dim | Elapsed s | Status |
|-------|-------|----:|----------:|--------|
| agrifm | region_a | 1024 | 94.560 | ok |
| anysat | region_a | 768 | 75.656 | ok |
| dofa | region_a | 768 | 36.322 | ok |
| fomo | region_a | 768 | 25.080 | ok |
| galileo | region_a | 128 | 59.969 | ok |
| gse | region_a | 64 | 23.070 | ok |
| prithvi | region_a | 768 | 27.984 | ok |
| remoteclip | region_a | 512 | 49.005 | ok |
| satmae | region_a | 1024 | 37.962 | ok |
| satmaepp | region_a | 1024 | 39.306 | ok |
| satmaepp_s2_10b | region_a | 1024 | 29.667 | ok |
| scalemae | region_a | 1024 | 36.188 | ok |
| terrafm | region_a | 768 | 32.121 | ok |
| terramind | region_a | 384 | 61.263 | ok |
| tessera | region_b | 128 | 5.048 | ok |
| thor | region_a | 768 | 41.053 | ok |
| wildsat | region_a | 256 | 31.977 | ok |
| copernicus | region_b | 768 | 11.115 | ok |
| satvision | region_b | 4096 | 98.751 | ok |

### Tessera status

- `tessera` is a **precomputed** model with no meaningful GPU compute.
- The repository already contains a **local successful run** in `research_outputs/gpu_benchmark_full_summary.{md,json}`:
  - status: `pass`
  - elapsed: `1025.79 s`
  - shape: `[128]`
  - config: `6000m` buffer, year `2024`, cache `research_outputs/model_cache/geotessera_cache`
- The fresh current-session rerun is now also completed:
  - status: `ok`
  - elapsed: `5.048 s`
  - shape: `[128]`
  - method: direct pooling from local `global_0.1_degree_representation/2024/...` files selected by the cached `registry.parquet`

## Summary

- Must-run data-prep runs completed: **2 / 2**
- Must-run smoke runs completed: **2 / 2**
- Fresh current-session model outputs: **19 / 19**
- All representative and appendix smoke models are now locally available for downstream task runs
- Ready for next milestone: **YES**

## Next task setup

### Immediate run order

1. **M2 / Block 1 — Local classification + regression**
   - cohort: `gse`, `satmaepp_s2_10b`, `remoteclip`, `galileo`, `agrifm`
   - baseline: mean spectral features
   - split: Region A `60 / 20 / 20`
   - tasks: T1 + T2

2. **M2 / Block 2 — Local dense water segmentation**
   - start with grid-capable subset: `satmaepp_s2_10b`, `galileo`, `anysat`, `terrafm`
   - compare against pooled-broadcast baseline
   - use Region A water mask first

3. **M3 / Block 5 — Regional scale-fair benchmark**
   - cohort: `copernicus`, `satvision`, `gse`, `satmaepp_s2_10b`, `galileo`, `agrifm`
   - tasks: T7 + T8
   - `tessera` can now be included as a coarse precomputed add-back immediately

4. **M3 / Block 3 — Temporal change detection**
   - first cohort: `galileo`, `agrifm`, `gse`, `copernicus`
   - `tessera` can participate through the local cached precomputed path

### Concrete files already ready for those runs

- Region A labels: `survey_satellite_embedding/data/part2_20260502_full/region_a/tile_manifest_500m.csv`
- Region B labels: `survey_satellite_embedding/data/part2_20260502_full/region_b/cell_manifest_025deg.csv`
- Smoke embeddings / metadata: `survey_satellite_embedding/experiments/results/all_models_smoke_20260502`

## Recommendation

Proceed directly to **M2 Block 1** on the representative cohort, then **M3 Block 5** for the cross-scale claim. Those two blocks now have the cleanest path to a paper-usable main table.
