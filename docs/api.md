# API Reference

This section is the exact reference for the public API.
If you want installation and first-run examples, start with [Quickstart](quickstart.md) instead.

---

## Core Entry Points

Most users only need five public entry points: `get_embedding(...)`, `get_embeddings_batch(...)`, `export_batch(...)`, `load_export(...)`, and `inspect_provider_patch(...)`.

---

## Choose by Task

| I want to...                                  | Read this page                                 |
| --------------------------------------------- | ---------------------------------------------- |
| understand spatial/temporal/output specs      | [API: Specs and Data Structures](api_specs.md) |
| get one embedding or batch embeddings         | [API: Embedding](api_embedding.md)             |
| build export pipelines and datasets           | [API: Export](api_export.md)                   |
| read back a saved export                      | [API: Load](api_load.md)                       |
| inspect raw provider patches before inference | [API: Inspect](api_inspect.md)                 |

---

## Useful Extras

`export_npz(...)` is a compatibility wrapper around `export_batch(...)` for single-ROI `.npz`, `inspect_gee_patch(...)` is the older GEE-focused name for `inspect_provider_patch(...)`, and `list_models()` is the stable public helper for inspecting the model catalog.

### Model-Specific Configuration

`get_embedding(...)` and `get_embeddings_batch(...)` accept model-specific settings as direct keyword arguments such as `variant="large"`. `export_batch(...)` handles the same kind of override per model through `ExportModelRequest.configure("model", variant="large")`. Variant-aware models are documented on their own detail pages, and unsupported keyword arguments raise `ModelError`.

### Sampling And Fetch Configuration

Public embedding and export APIs accept `fetch=FetchSpec(...)` for common overrides such as `scale_m`, `cloudy_pct`, `composite`, and `fill_value`. Reserve `sensor=SensorSpec(...)` for advanced source overrides like `collection`, `bands`, or modality-specific contracts. `fetch` and `sensor` are mutually exclusive.

If you need a stable model list in code:

```python
from rs_embed import list_models

print(list_models())
```

`rs_embed.core.registry.list_models()` only reports models currently loaded into the runtime registry.

---

## Errors

rs-embed raises several explicit exception types (all in `rs_embed.core.errors`):

`SpecError` covers spec validation failures such as invalid bounds or missing temporal fields, `ProviderError` covers backend and fetch failures such as GEE initialization problems, and `ModelError` covers unknown model IDs, unsupported parameters, and unsupported export formats.

---

## Versioning Notes

The current version is still early stage (`0.1.x`):

`BBox` and `PointBuffer` currently require `crs="EPSG:4326"`. Precomputed models should usually use `backend="auto"`, while on-the-fly models mainly use provider backends such as `"gee"` or other explicit provider names. `ExportConfig(format=...)` is the recommended way to choose export format; today that means `"npz"` or `"netcdf"`, with room for additional formats later.
