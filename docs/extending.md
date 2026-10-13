# Extending rs-embed

This page documents the extension contract for adding a new embedder.

For repository workflow, issue expectations, and pull request requirements, see [Contributing Guide](contributing.md).

In most cases, adding a model means:

1. Create an embedder class in `src/rs_embed/embedders/`.
2. Register it with `@register("your_model_name")`.
3. Add it to `src/rs_embed/embedders/catalog.py` (`MODEL_SPECS`).
4. Implement `describe()` and `get_embedding(...)`.
5. Override batch methods when the model supports true batched inference.

For on-the-fly models, also choose one fetch path:

- declarative fetch via `input_spec = ModelInputSpec(...)`
- custom fetch via `fetch_input(...)`

Useful source-of-truth locations:

- catalog: `src/rs_embed/embedders/catalog.py`
- base contract: `src/rs_embed/embedders/base.py`
- on-the-fly examples: `src/rs_embed/embedders/onthefly_*.py`
- precomputed examples: `src/rs_embed/embedders/precomputed_*.py`

---

## Registration

Models are discovered through `rs_embed.core.registry`.

- `@register("name")` registers an embedder class.
- `get_embedder_cls("name")` resolves the class.
- `list_models()` lists models that have already been loaded in the current process.
- `rs_embed.list_models()` returns the stable public model catalog from `MODEL_SPECS`.

Model loading is lazy:

- `get_embedder_cls("name")` looks up `name` in `MODEL_SPECS`.
- Then it imports the mapped module and reads the mapped class.
- The class is inserted into the runtime registry.

!!! tip
Put your embedder in `rs_embed/embedders/` and add it to `src/rs_embed/embedders/catalog.py`.
If it's not in `MODEL_SPECS`, string-based lookup (`get_embedding("...")`) will not find it.

---

## Embedder Interface

All models implement `EmbedderBase`:

```python
from rs_embed.embedders.base import EmbedderBase

class EmbedderBase:
    def describe(self) -> dict: ...
    def fetch_input(self, provider, *, spatial, temporal, sensor): ...
    def get_embedding(
        self,
        *,
        spatial,
        temporal,
        sensor,
        output,
        backend,
        device="auto",
        input_chw=None,
        model_config=None,
    ): ...
    def get_embeddings_batch(..., model_config=None): ...
    def get_embeddings_batch_from_inputs(..., model_config=None): ...
```

The stable extension points are:

- `describe()` for capability metadata
- `fetch_input(...)` for model-specific provider fetch behavior
- `get_embedding(...)` for single-item inference
- `get_embeddings_batch(...)` and `get_embeddings_batch_from_inputs(...)` for true batched inference

### `describe()`

`describe()` should return a small JSON-serializable capability dictionary. A typical shape is:

```python
{
  "type": "on_the_fly" | "precomputed",
  "backend": ["provider" | "gee" | "auto" | "tensor", ...],
  "inputs": {
    "collection": "COPERNICUS/S2_SR_HARMONIZED",
    "bands": ["B4", "B3", "B2"],
    # or, for models with a more specific provider-facing default:
    "provider_default": {
      "collection": "...",
      "bands": [...]
    }
  },
  "temporal": {"mode": "year" | "range"} | null,
  "output": ["pooled", "grid"],
  "defaults": {
    "scale_m": 10,
    "cloudy_pct": 30,
    "composite": "median",
    "image_size": 224
  },
  "model_config": {
    "variant": {
      "type": "string",
      "default": "base",
      "choices": ["base", "large"]
    }
  }
}
```

!!! note
`describe()` must stay fast. It should not trigger checkpoint downloads, provider setup, or heavy model loading.

Important fields currently consumed by rs-embed:

- `backend`, `output`, and `temporal` for capability checks
- `inputs`, `defaults`, `modalities`, or `_default_sensor()` for default-sensor resolution
- `model_config` for public model-specific keyword settings such as `variant`

---

## Minimal Skeleton

This is the smallest useful embedder pattern. It returns a deterministic vector and supports the current public contract.

Create `src/rs_embed/embedders/toy_model.py`:

```python
from __future__ import annotations

import hashlib
from dataclasses import asdict
from typing import Any, Dict, Optional
import numpy as np

from rs_embed.core.registry import register
from rs_embed.core.embedding import Embedding
from rs_embed.core.errors import ModelError
from rs_embed.core.specs import SpatialSpec, TemporalSpec, SensorSpec, OutputSpec
from rs_embed.embedders.base import EmbedderBase


@register("toy_model_v1")
class ToyModelV1(EmbedderBase):
    def describe(self) -> Dict[str, Any]:
        return {
            "type": "precomputed",
            "backend": ["auto"],  # use "provider"/"gee" for on-the-fly fetchers
            "output": ["pooled"],
        }

    def get_embedding(
        self,
        *,
        spatial: SpatialSpec,
        temporal: Optional[TemporalSpec],
        sensor: Optional[SensorSpec],
        output: OutputSpec,
        backend: str = "auto",
        device: str = "auto",
        input_chw: Optional[np.ndarray] = None,
        model_config: Optional[Dict[str, Any]] = None,
    ) -> Embedding:
        # Use a stable hash so results are reproducible across processes.
        seed_bytes = hashlib.blake2s(
            f"{spatial!r}|{temporal!r}|{self.model_name}".encode("utf-8"),
            digest_size=4,
        ).digest()
        seed = int.from_bytes(seed_bytes, "little")
        rng = np.random.default_rng(seed)

        if output.mode != "pooled":
            raise ModelError("toy_model_v1 only supports pooled output")

        vec = rng.standard_normal(512).astype("float32")
        meta = {
            "model": self.model_name,
            "backend": backend,
            "device": device,
            "model_config": model_config,
            "spatial": asdict(spatial),
            "temporal": asdict(temporal) if temporal else None,
        }
        return Embedding(data=vec, meta=meta)
```

Then register it in `src/rs_embed/embedders/catalog.py`:

```python
MODEL_SPECS["toy_model_v1"] = ("toy_model", "ToyModelV1")
```

---

## On-the-fly Models

Most on-the-fly embedders follow this flow:

1. Use a provider (e.g., Earth Engine) to fetch an **input patch** (CHW numpy).
2. Preprocess it (normalize/resample).
3. Run inference.
4. Return `Embedding(data=..., meta=...)`.

Recommended extension pattern:

- If generic provider fetching is enough, prefer declaring
  `input_spec = ModelInputSpec(...)` on the embedder. That lets the base
  `fetch_input()` implementation handle provider fetch + normalization.
- If your model needs custom fetch logic, fallback chains, multi-sensor routing,
  or fetch-time metadata, override `fetch_input(...)`.
- Use `SensorSpec` and model defaults so API-level `fetch=...`, `sensor=...`,
  and `modality=...` resolution can reuse your model cleanly.

You can follow existing implementations in:

- `rs_embed/embedders/onthefly_*.py`

!!! tip
Keep provider IO separate from model inference whenever possible. That makes batching, caching, and export reuse simpler.

---

## Vendored Runtime Code

If a model depends on upstream runtime code that is easier to vendor than to wrap as an external package dependency, place that code under `src/rs_embed/embedders/_vendor/`.

Typical patterns:

- a single vendored module such as `_vendor/prithvi_mae.py`
- a small vendored package such as `_vendor/anysat/` or `_vendor/thor/`

Recommended layout:

- keep the adapter itself in `onthefly_<model>.py` or `precomputed_<model>.py`
- keep vendored upstream runtime code in `_vendor/`
- keep vendored code minimally patched and document any rs-embed-specific changes in comments or a short local note

License and dependency notes may live alongside the vendored runtime:

- add the upstream license text under `_vendor/`, for example `LICENSE.<model>` or a package-local `LICENSE`
- include `NOTICE` or attribution material when the upstream project requires it
- if the vendored runtime still needs third-party Python packages at import or runtime, document those requirements close to the vendored code and surface the user-facing install error from the adapter with `ModelError`

`_vendor/` is an implementation area, not a public API surface. Public behavior should remain defined by the adapter, `describe()`, and the stable rs-embed APIs.

---

## Input Reuse

`export_batch` can prefetch the input patch once and reuse it for both:

- saving `inputs`
- computing `embeddings`

Contract:

> If `input_chw` is provided, **do not fetch inputs again**. Use `input_chw` as the model input.

Example snippet:

```python
if input_chw is None:
    # fetch from backend/provider, or via your custom fetch_input(...)
    input_chw = provider.fetch_array_chw(...)
# now preprocess + infer using input_chw
```

!!! important
This is the key to avoiding “download twice” when `save_inputs=True` and `save_embeddings=True`.

---

## Batch Methods

`EmbedderBase.get_embeddings_batch` defaults to a Python loop calling `get_embedding`.
`EmbedderBase.get_embeddings_batch_from_inputs` defaults to a Python loop calling
`get_embedding(..., input_chw=...)`.

Override one or both when the model supports true vectorized inference:

```python
def get_embeddings_batch(
    self,
    *,
    spatials,
    temporal=None,
    sensor=None,
    model_config=None,
    output=OutputSpec.pooled(),
    backend="gee",
    device="auto",
):
    # 1) fetch/preprocess inputs for all spatials
    # 2) stack into a batch tensor
    # 3) run a single forward pass
    # 4) split outputs back into Embedding objects
```

If your model supports prefetched inputs, also consider:

```python
def get_embeddings_batch_from_inputs(
    self,
    *,
    spatials,
    input_chws,
    temporal=None,
    sensor=None,
    model_config=None,
    output=OutputSpec.pooled(),
    backend="auto",
    device="auto",
):
    # 1) preprocess/stack prefetched CHW inputs
    # 2) run a single batched forward pass
    # 3) split outputs back into Embedding objects
```

`export_batch(...)` prefers `get_embeddings_batch_from_inputs(...)` when it has prefetched
provider inputs available, so overriding this method usually gives the biggest speedup for
on-the-fly models.

General guidance:

- Batch **inference** (GPU-friendly).
- Parallelize **IO** (provider fetch) with threads if needed.
- Keep memory stable by using chunking (see `ExportConfig(chunk_size=...)` in `export_batch(...)`).

---

## Output Modes

`OutputSpec` controls output shape:

- `OutputSpec.pooled()` → `(D,)`
- `OutputSpec.grid(...)` → `(D, H, W)`

If your model does not support a mode, raise a clear error:

```python
if output.mode == "grid" and not supported:
    raise ModelError("model_x does not support grid output")
```

---

## Optional Dependencies

Many embedders rely on optional packages (e.g., `torch`, `ee`).

Recommended pattern:

- Import heavy dependencies **inside** methods or within a `try/except` at module import.
- If the dependency is missing, raise a **helpful** error (`ModelError`) explaining what to install.

Example:

```python
from rs_embed.core.errors import ModelError

try:
    import torch
except Exception as e:
    torch = None
    _torch_err = e

def _require_torch():
    if torch is None:
        raise ModelError("Torch is required. Install this repository with: pip install -e .")
```

---

## Testing

Minimum test coverage:

### Registry

Add a small test ensuring registration works:

```python
from rs_embed.core.registry import get_embedder_cls

def test_toy_model_registered():
    cls = get_embedder_cls("toy_model_v1")
    assert cls is not None
```

### API-level

```python
from rs_embed import PointBuffer, TemporalSpec, OutputSpec, get_embedding

def test_toy_model_get_embedding():
    emb = get_embedding(
        "toy_model_v1",
        spatial=PointBuffer(0, 0, 1000),
        temporal=TemporalSpec.year(2022),
        output=OutputSpec.pooled(),
        backend="auto",
    )
    assert emb.data.shape == (512,)
```

### Export integration

If your model supports input reuse and batch export, add a small `export_batch` test using `monkeypatch` to avoid real network calls.
See existing patterns in:

- `tests/test_export_batch.py`
- `tests/test_gee_provider.py`

Run tests:

```bash
pytest -q
```

---

## Documentation

Update docs in these places as needed:

- `docs/models.md` for the overview table / entry point
- `docs/models/<model>.md` for the detailed model page
- `docs/models_reference.md` if the model adds important preprocessing or comparison caveats

Use [Model Detail Template](model_detail_template.md) for the detailed page structure.

---

## Checklist

Before opening a PR:

- [ ] `@register("...")` added and entry added in `src/rs_embed/embedders/catalog.py`
- [ ] `describe()` is fast and accurate
- [ ] on-the-fly fetch path is defined through `input_spec` or `fetch_input(...)`
- [ ] `get_embedding()` supports `input_chw` reuse (if on-the-fly)
- [ ] override `get_embeddings_batch_from_inputs()` if your model can batch prefetched inputs
- [ ] clear errors for missing optional dependencies
- [ ] unit tests added (`pytest -q` passes)
- [ ] docs updated (`models.md`, model detail page, and reference pages if needed)
