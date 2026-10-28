# Repository Guidelines

## Project Structure & Module Organization
`rs-embed` uses a `src/` layout. Core package code lives in `src/rs_embed/`: public entry points such as `api.py`, `cli.py`, `load.py`, and `export.py` sit at the top level, while reusable internals are grouped under `core/`, `pipelines/`, and `providers/`. Tests live in `tests/` and generally mirror the module or behavior they cover. Documentation is built from `docs/` with MkDocs, and runnable examples live in `examples/`. Large generated research artifacts are kept in `research_outputs/`; avoid touching them unless your change is specifically about those outputs.

### Survey benchmark assets

The current survey benchmark lives under `survey_satellite_embedding/` and should
be treated as a **single-area, high-resolution Wuhan ROI benchmark** for common
remote-sensing downstream tasks. Do not design new survey experiments around the
old two-region "small Region A + coarse Region B" split unless the user
explicitly asks for a historical comparison.

Use these paths when working on the experiment pipeline or preparing figures:

- **Prepared data root**:
  `survey_satellite_embedding/data/part2_20260502_full/`
- **Primary benchmark ROI (Wuhan East Lake / Tangxun Lake corridor)**:
  `survey_satellite_embedding/data/part2_20260502_full/region_a/`
  - Sentinel-2 blocks in `imagery_s2_20210501_20211031/`
  - WorldCover blocks in `worldcover_2021_blocks/`
  - JRC water blocks in `jrc_occurrence_blocks/`
  - task manifest in `tile_manifest_500m.csv` (2173 rows)
- **Historical coarse manifest only, not the active benchmark design**:
  `survey_satellite_embedding/data/part2_20260502_full/region_b/`
  - task manifest in `cell_manifest_025deg.csv` (1056 rows)
  - current prep is manifest-only for Region B, not a full imagery mosaic
  - keep it as an archived compatibility asset unless a task specifically needs it
- **Smoke embeddings / metadata**:
  `survey_satellite_embedding/experiments/results/all_models_smoke_20260502/`
- **Current final public-19 map test case**:
  `survey_satellite_embedding/experiments/results/part2_model_map_figure/`
  - final 2x single-area figure:
    `part2_original_map_with_public19_models_2x.png`
  - manifest:
    `manifest_2x.json`
  - expands the original reference block to
    `block_r01_c01`, `block_r01_c02`, `block_r02_c01`, and `block_r02_c02`
  - geographic width and height are each 2x the old single block; area is 4x
  - the older single-block figure
    `part2_original_map_with_public19_models.png` is a historical reference only
- **Current downstream 2x task artifacts**:
  `survey_satellite_embedding/experiments/results/downstream_core_2x/`
  - T1 classification is completed for the current 2x public-19 Wuhan window.
  - `classification.csv`, `classification_ranked.csv`, per-model prediction CSVs,
    and classification figures already exist.
  - `embeddings_2x_tile/` contains one local pooled tile embedding file per
    canonical public model: 19 `.npz` files for the 567 500 m tiles in the
    current 2x window.
  - For the next T2 fraction-regression acceptance pass, reuse these local
    `embeddings_2x_tile/*.npz` files first. Do **not** default to re-exporting
    embeddings from GEE or rerunning model inference.
- **Current T2 2x fraction-regression artifacts**:
  `survey_satellite_embedding/experiments/results/downstream_fraction_2x/`
  - T2 fraction regression is completed for all 19 public models on the current
    567-tile 2x Wuhan window.
  - The run used only local cached embeddings from
    `downstream_core_2x/embeddings_2x_tile/`; no GEE fetch, embedding export, or
    encoder inference was performed.
  - Main outputs are `fraction_regression.csv`,
    `fraction_regression_ranked.csv`, per-model
    `fraction_regression_predictions_{model}.csv`, per-model scatter plots, and
    `figures/fraction_regression_spearman_public19_2x.png`.
  - The script for this local-cache-only pass is
    `survey_satellite_embedding/experiments/run_wuhan_t2_2x_fraction_regression.py`.
  - As of this checkpoint, the top mean test Spearman models are `gse`,
    `tessera`, `thor`, `dofa`, and `terramind`.
- **T2 full-ROI status**:
  `survey_satellite_embedding/experiments/results/downstream_fraction/`
  - currently contains only generated label/split artifacts:
    `downstream_labels_500m_fraction.csv`,
    `downstream_splits_500m_fraction.csv`, and
    `downstream_labels_summary_fraction.json`.
  - `embeddings_full_roi/` is intentionally empty at this checkpoint; there are
    no verified full-ROI pooled embeddings for all 2173 tiles in this folder.
  - A previously started full-ROI `--export-missing` run was stopped because it
    would recompute/fetch embeddings. Do not restart it unless the user
    explicitly asks for full-ROI embedding extraction.
- **Unified public-model asset folder**:
  `research_outputs/model_assets_public19/`
  - contains one subdirectory per canonical public model
  - uses symlinks plus `manifest.json` instead of duplicating large checkpoints

For the survey experiment section, prefer one ROI with multiple downstream
tasks over two differently scaled regions. The active task families are:

- tile-level land-cover classification from pooled embeddings
- built-up / vegetation / water fraction regression
- water segmentation or mask reconstruction when dense token grids are available
- optional retrieval / qualitative map panels for multimodal or dense-grid models

Treat the current 2x public-19 map figure as the final visual sanity-check case
before downstream tasks. Do not revive the previous small-block-only test case or
the old small-Region-A / coarse-Region-B design unless the user explicitly asks
for a historical comparison. Downstream runs should now be organized around the
same Wuhan ROI, 500 m grid, label sources, and train/validation/test split rules.
Use `survey_satellite_embedding/experiments/DOWNSTREAM_TASK_PLAN.md` and the
`survey_satellite_embedding/notes/part2_experiments_plan.md` as the current downstream-task planning docs.

For immediate downstream-task work, distinguish these two scopes:

- **2x acceptance scope**: use
  `survey_satellite_embedding/experiments/results/downstream_core_2x/embeddings_2x_tile/`
  and its existing 567-tile labels/splits. T2 has already been run from this
  cache and the results are in `downstream_fraction_2x/`.
- **Full 2173-tile ROI scope**: only run after confirming that full-ROI
  embeddings already exist or after the user explicitly approves a long
  extraction job. Never infer that missing full-ROI files mean they should be
  regenerated automatically.

The current prepared Wuhan ROI bounds are `[114.29, 30.44, 114.53, 30.60]`.
It contains 16 downloaded Sentinel-2 / WorldCover / JRC blocks and 2173 500 m
tiles. If expanding the study area, scale this same ROI outward and keep the
500 m tile grid, label sources, temporal window, and train/validation/test split
rules consistent across all 19 public models.

Local model assets for the current 19 canonical public models are split across:

- `research_outputs/model_cache/` for repo-pinned checkpoints such as
  `AgriFM.pth` and `checkpoint_ViT-L_pretrain_fmow_sentinel.pth`
- `~/.cache/huggingface/hub/` for Hugging Face-backed checkpoints
- `~/.cache/rs_embed/` for runtime-managed caches such as `anysat`, `wildsat`,
  `fomo`, and `galileo`
- `global_0.1_degree_representation/` and
  `research_outputs/model_cache/geotessera_cache/` for local `tessera` assets

The canonical public model list is defined in `src/rs_embed/embedders/catalog.py`
and currently contains 19 entries. There are no additional verified private-model
embedding outputs tracked in the repository result folders at the moment.

The 19 models split into two categories:

- **16 open-source inference models** — fetch imagery and run model locally;
  weights from HuggingFace / GitHub:
  `remoteclip`, `satmae`, `satmaepp`, `satmaepp_s2_10b`, `scalemae`, `wildsat`,
  `prithvi`, `terrafm`, `terramind`, `dofa`, `anysat`, `galileo`, `agrifm`,
  `satvision`, `fomo`, `thor`
- **3 precomputed embedding products** — query by coordinates, no local inference:
  `tessera` (GeoTessera tile cache), `gse` (Google Earth Engine product), `copernicus` (HuggingFace dataset)

## Build, Test, and Development Commands
Use Python 3.12. For CI-parity setup, prefer:

- `uv sync --frozen --extra dev --extra full` installs the locked development environment.
- `uv run python -m pytest -v -n auto` runs the full test suite.
- `ruff check src/` runs lint checks used in CI.
- `ruff format --check src/` verifies formatting; use `ruff format src/ tests/` locally to rewrite files.
- `mkdocs build --strict` validates documentation builds.

If you are not using `uv`, `pip install -e ".[dev,full]"` is the supported local fallback.

## Coding Style & Naming Conventions
Follow 4-space indentation, Python 3.12 syntax, and Ruff’s 100-character line limit. Use `snake_case` for modules, functions, variables, and test files; keep public API names aligned with existing patterns such as `get_embedding` and `export_batch`. Prefer small, behavior-focused helpers over large monolithic functions. Run pre-commit hooks before opening a PR if you have them installed.

## Testing Guidelines
Tests use `pytest` with `pytest-xdist`. Name new files `test_<feature>.py` and keep one clear behavior per test when possible. Add or update tests for any Python behavior change, especially public API semantics, model defaults, export flows, or provider logic. For targeted work, run a narrow command like `uv run python -m pytest tests/test_api.py -v`.

## Commit & Pull Request Guidelines
Recent history uses short prefixed subjects such as `fix:pytest`, `feat:gee auto error`, and `release:prepare 0.1.2`. Keep commits focused and use the same `type:summary` style. PRs should fill out `.github/PULL_REQUEST_TEMPLATE.md`, link the related issue, describe verification steps, and update docs for user-facing changes. If a PR changes package-relevant behavior, update `CHANGELOG.md` or coordinate a `skip-changelog` label for internal-only work.
