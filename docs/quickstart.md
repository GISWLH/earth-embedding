# Quickstart

This page is the shortest path from installation to a first successful run.
It focuses on the three core APIs most users need: `get_embedding(...)`, `get_embeddings_batch(...)`, and `export_batch(...)`.

Use this page top-to-bottom once. After that, go to [Models](models.md) to choose model IDs, [API](api.md) for exact signatures and edge cases, and [Extending](extending.md) only if you want to add a model.

Canonical model IDs use short names such as `tessera`, `remoteclip`, and `prithvi`.
Legacy aliases such as `remoteclip_s2rgb` still work, but new code should use the short names.

---

## Install

Use Python 3.12. Install this fork from source; `pip install rs-embed` installs
the separate upstream distribution. `earth-embedding` has not yet been
published to PyPI by this project.

```bash
# base install
pip install "earth-embedding @ git+https://github.com/GISWLH/earth-embedding.git"

# add [terratorch] only if you use terramind
pip install "earth-embedding[terratorch] @ git+https://github.com/GISWLH/earth-embedding.git"
```

For local development:

```bash
git clone https://github.com/GISWLH/earth-embedding.git
cd earth-embedding
pip install -e .  # use -e ".[terratorch]" if you need terramind
```

Repository examples are available in `examples/playground.ipynb` and `examples/quickstart.py`.

If this is your first time using Google Earth Engine, authenticate once:

```bash
earthengine authenticate
```

Earth Engine is needed only for provider-backed imagery and GSE access.
Location encoders and [direct AEF COG sampling](data-access.md) work without it.

```python
from earth_embedding import get_location_embeddings

result = get_location_embeddings("satclip", [[114.41, 30.52]], device="cpu")
print(result.data.shape)  # (1, 256), downloads weights on first use
```

---

## One place, several models

The same spatial and output specs work for image encoders, location encoders,
and products. Use the comparison helper to collect and plot several models:

```python
from earth_embedding import (
    BBox, OutputSpec, compare_embeddings, plot_embedding_comparison,
)

models = ["satclip", "geoclip", "esri_gle"]
comparison = compare_embeddings(
    models,
    spatial=BBox(113.9, 30.2, 114.7, 30.9),
    output=OutputSpec.grid(),
    model_options={model: {"grid_step_m": 2000} for model in models},
    device="cpu",
)
fig = plot_embedding_comparison(comparison, columns=3)
fig.savefig("location-comparison.png", dpi=180)
```

Install `.[plot,location]` for this example. It downloads location-model weights
on first use and needs no Earth Engine account. See the
[22-model tutorial](tutorials/model-comparison.md) for imagery/product models,
per-model dates, failure reports, and native-resolution interpretation.

## Core extraction APIs

### 1. One ROI: `get_embedding(...)`

Use this when you want one embedding now.

```python
from rs_embed import PointBuffer, TemporalSpec, OutputSpec, get_embedding

emb = get_embedding(
    "tessera",
    spatial=PointBuffer(lon=121.5, lat=31.2, buffer_m=1024),
    temporal=TemporalSpec.year(2024),
    output=OutputSpec.pooled(pooling="mean"),
    backend="auto",
)

vec = emb.data
meta = emb.meta
```

Use `backend="auto"` unless you need to force a provider path such as `backend="gee"`.

### 2. Many ROIs, one model: `get_embeddings_batch(...)`

Use this when the model is fixed and you have multiple ROIs.

```python
from rs_embed import PointBuffer, TemporalSpec, OutputSpec, get_embeddings_batch

spatials = [
    PointBuffer(121.5, 31.2, 1024),
    PointBuffer(120.5, 30.2, 1024),
]

embs = get_embeddings_batch(
    "tessera",
    spatials=spatials,
    temporal=TemporalSpec.year(2024),
    output=OutputSpec.pooled(),
    backend="auto",
)
```

### 3. Dataset export: `export_batch(...)`

Use this when you are building a dataset or benchmark and want files plus manifests.

```python
from rs_embed import (
    ExportConfig,
    ExportTarget,
    PointBuffer,
    TemporalSpec,
    export_batch,
)

spatials = [
    PointBuffer(121.5, 31.2, 1024),
    PointBuffer(120.5, 30.2, 1024),
]

export_batch(
    spatials=spatials,
    temporal=TemporalSpec.year(2024),
    models=["tessera"],
    target=ExportTarget.per_item("exports", names=["p1", "p2"]),
    backend="auto",
    config=ExportConfig(
        save_inputs=False,
        save_embeddings=True,
        resume=True,
        show_progress=True,
    ),
)
```

For new code, `target=ExportTarget(...)` plus `config=ExportConfig(...)` is the recommended style.

---

## Repository Examples

The repository also includes optional runnable examples:

- `examples/quickstart.py` for a small end-to-end script
- `examples/playground.ipynb` for notebook-style exploration

These are examples, not the primary usage path. For normal library use, start from the API snippets above.

---

## When You Need GEE or Model Debugging

Use GEE-backed on-the-fly models when you want to fetch imagery and run model inference directly.
Typical examples include `remoteclip`, `prithvi`, `terrafm`, and `terramind`.

If the model output looks wrong, inspect the fetched patch before changing model settings:

[`inspect_provider_patch(...)`](api_inspect.md#inspect_provider_patch) is the recommended inspection API, while [`inspect_gee_patch(...)`](api_inspect.md#inspect_gee_patch) remains available as a compatibility alias.

---

## What To Read Next

From here, use [Models](models.md) to choose the right model and verify its input assumptions, [API](api.md) for exact signatures and edge cases, [Concepts](concepts.md) for temporal and output semantics, and [Workflows](workflows.md) for extra recipes around tiling, inspection, and fair comparison.
