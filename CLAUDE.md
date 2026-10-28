# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment

Default runtime for this machine: **project `.venv`**. It has the most complete dependency set for this repo, including GPU-enabled PyTorch and the geospatial/model extras used by the survey experiments.

Use **GPU by default** for model inference and experiment runs on this machine. Prefer `device="cuda"` or `--device cuda` unless the user explicitly asks for CPU or a specific model must fall back due to an environment/runtime issue.

Legacy note: `.vscode/settings.json` still references conda env **pynew** (Python 3.13), but if `pynew` is unavailable or incomplete, prefer the project `.venv` instead.

```bash
# Preferred interpreter on this machine
./.venv/bin/python

# If you need the legacy conda environment and it exists
conda activate pynew
```

## Survey Experiment Status

The active survey benchmark is the **single high-resolution Wuhan ROI** under
`survey_satellite_embedding/data/part2_20260502_full/region_a/`. Do not use the
old two-region design as the default experiment plan.

Current anchor assets:

- ROI bounds: `[114.29, 30.44, 114.53, 30.60]`
- 500 m task manifest:
  `survey_satellite_embedding/data/part2_20260502_full/region_a/tile_manifest_500m.csv`
  with 2173 tiles
- Final public-19 visual sanity case:
  `survey_satellite_embedding/experiments/results/part2_model_map_figure/part2_original_map_with_public19_models_2x.png`
- 2x manifest:
  `survey_satellite_embedding/experiments/results/part2_model_map_figure/manifest_2x.json`

The 2x figure expands the original reference block in both width and height,
so it covers 4x the previous single-block area. Treat
`part2_original_map_with_public19_models.png` as historical only.

Downstream planning lives in:

- `survey_satellite_embedding/notes/part2_experiments_plan.md`
- `survey_satellite_embedding/experiments/DOWNSTREAM_TASK_PLAN.md`

The first implementation priority is classification and fraction/water
regression from the 500 m manifest, followed by dense water / land-cover
segmentation for models with grid outputs.

## Commands

```bash
# Install for development (run once, in pynew)
pip install -e ".[dev,full]"

# Run all tests
python -m pytest -v

# Run a single test file
python -m pytest tests/test_api.py -v

# Run a single test by name
python -m pytest tests/test_api.py::test_function_name -v

# Lint
ruff check src/

# Build docs
mkdocs build --strict
```

## Architecture

**rs-embed** is a unified Python library that abstracts away data fetching, preprocessing, and model inference to provide embeddings from any Remote Sensing Foundation Model (RSFM) for any geographic location and time period.

### Layers (top to bottom)

**Public API** (`api.py`, `model.py`, `cli.py`)
- `get_embedding()` — single embedding for one location
- `get_embeddings_batch()` — batch reusing the same model instance
- `export_batch()` — batch export with prefetch, retry, and resume support
- `Model` — stateful wrapper (TorchGeo-style) around the above

**Normalization & Validation** (`tools/normalization.py`, `tools/model_defaults.py`, `core/validation.py`)
- Resolves user-facing strings (model names, backend names, device strings) to canonical forms before execution
- Per-model sensor defaults live in `tools/model_defaults.py`

**Runtime Context & Pipelines** (`tools/runtime.py`, `pipelines/`)
- `_EmbeddingRequestContext` encapsulates the resolved model, backend, device, specs, and cached embedder instance — avoids repeated model loading in batch operations
- `BatchExporter` orchestrates `PrefetchManager` → `InferenceEngine` → writers → `CheckpointManager`
- Supports `COMBINED` (single `.npz` + manifest) and `PER_ITEM` (one file per location) output layouts

**Embedders** (`embedders/`)
- All implementations inherit from `EmbedderBase` (`embedders/base.py`)
- `embedders/catalog.py` maps 19 model IDs to `(module, class)` tuples — models are loaded lazily
- Two categories:
  - **On-the-fly** (16 models): fetch imagery and run inference live;
    `remoteclip`, `satmae`, `satmaepp`, `satmaepp_s2_10b`, `scalemae`, `wildsat`,
    `prithvi`, `terrafm`, `terramind`, `dofa`, `anysat`, `galileo`, `agrifm`,
    `satvision`, `fomo`, `thor`
  - **Precomputed** (3 models): download pre-computed embeddings (`tessera`, `gse`, `copernicus`)
- Vendored third-party code lives in `embedders/_vendor/`

**Providers** (`providers/`)
- `ProviderBase` defines the data fetch interface; `GEEProvider` is the current implementation via Google Earth Engine
- `providers/prefetch_plan.py` handles pre-download planning for batch jobs

**Core Specs** (`core/specs.py`)
- `BBox` / `PointBuffer` — spatial inputs
- `TemporalSpec` — year or ISO date range
- `SensorSpec` — GEE collection, band names, scale, cloud filtering
- `OutputSpec` — `pooled` (single vector) or `grid` (spatial grid)
- `InputPrepSpec` — `resize`, `tile`, or `auto` tiling strategy

**Output** (`core/embedding.py`, `writers.py`)
- `Embedding` dataclass: `data` (ndarray or xr.DataArray) + `meta` dict (provenance, diagnostics, orientation)

### Adding a new model

1. Add a class inheriting `EmbedderBase` in a new `embedders/onthefly_<name>.py`
2. Implement `describe()`, `fetch_input()` (optional), and `get_embedding()`
3. Register it in `embedders/catalog.py` under `MODEL_SPECS`
4. Add sensor defaults to `tools/model_defaults.py`

See `docs/extending.md` for the full guide.

### Key constraints

- Python 3.12+ required
- `terratorch` is pinned to `==1.2.1` — do not upgrade without testing all on-the-fly embedders
- `timm` is bounded `>=1.0.3,<=1.0.15` for the same reason
- Line length is 100 characters (`ruff` enforces this)
