# Contributing to Earth Embedding

Contributions are welcome: reproducible bug reports, model integrations, data-access fixes, examples, tests, and English/Chinese/Japanese documentation. This is an independent extension of [CyberGIS rs-embed](https://github.com/cybergis/rs-embed); preserve upstream attribution and all component licenses.

## Set up a development environment

Use Python 3.12. Create an isolated environment and install the dependencies needed for your change:

```bash
git clone https://github.com/GISWLH/earth-embedding.git
cd earth-embedding
python -m venv .venv
# Activate .venv with the command appropriate for your shell.
python -m pip install -e ".[dev,full,location,aef,benchmark]"
```

Esri GLE uses a separate official ArcGIS deep-learning environment. Installing all extras does not install or license that environment. Model inference and live data tests may need checkpoints, provider authorization, substantial memory, or network access. Keep these separate from small offline tests.

## Report a problem

Open an issue with the package commit/version, Python and platform, model ID, optional packages, a minimal example, actual error, and expected behavior. Include input shape, band order, temporal contract, and relevant metadata. State whether the failure occurred during import, weight download, imagery access, preprocessing, inference, or export. Remove credentials and personal data before sharing logs.

For scientific comparisons, also state the task, label source, spatial support, and train/test split. A performance difference is not automatically an adapter bug.

## Add or change an adapter

Read [the extension guide](docs/extending.md) and the closest existing adapter. Keep changes focused and provide:

1. The official implementation, publication, checkpoint source/revision, and license.
2. Its release class: A image encoder, B location encoder, or C precomputed product. Follow the existing taxonomy and document the actual input configuration.
3. An explicit input/output contract: bands and units, coordinate order, CRS, temporal requirements, feature dimension, grid support, and supported pooling.
4. Lazy loading for heavy optional runtimes, actionable missing-dependency errors, and predictable device handling.
5. Tests for relevant behavior and failure paths, plus a documented real smoke run when the required assets and runtime are available.
6. A model page, catalog entry, changelog entry, and updated multilingual README when user-facing behavior changes.

Use WGS84 `[longitude, latitude]` at public location interfaces. Preserve `.data` and `.meta` output conventions. Do not silently substitute a different checkpoint or data product when one is unavailable. Keep source code, model weights, and data licenses separate.

## Validate your change

Start with the tests relevant to the changed behavior, then run the release checks appropriate to its scope:

```bash
python -m pytest tests -q
ruff check src/ tests/
ruff format --check src/ tests/
mkdocs build --strict
```

Record which checks ran and which required unavailable resources. Fixtures and mocked dependencies verify software behavior; label real inference and live provider access separately. New runtime evidence should include date, environment, model/checkpoint, output shape, finite-value check, source, and a sanitized failure reason where relevant. See [validation](docs/validation.md).

## Documentation and artwork

Keep `README.md`, `README.zh-CN.md`, and `README.ja.md` aligned on supported APIs, counts, status, and scientific scope. All three should be useful starting points. Prefer executable examples with explicit prerequisites over claims that every model works everywhere.

The logo and hero have native editable Excalidraw sources under `docs/assets/`. Follow the [artwork guide](docs/assets/earth-embedding-brand.md) to rebuild exports, and check both desktop and narrow layouts.

## Submit a pull request

Describe the user-visible problem, resulting behavior, and validation. Include access/runtime limitations and relevant issue links. Preserve unrelated changes, upstream notices, and backwards-compatible imports unless a documented breaking change is intended. Use a short descriptive commit subject such as `feat: add location adapter` or `fix: validate channel order`.

The manuscript's frozen 20-system benchmark and the 22-entry software catalog are different scopes. Adding an adapter does not establish benchmark results or change the frozen manuscript taxonomy. Do not add rankings, completed scientific claims, or publication metadata without supporting evidence.
