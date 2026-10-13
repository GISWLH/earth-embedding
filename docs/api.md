# API Reference

This section is the exact reference for the public API.
If you want installation and first-run examples, start with [Quickstart](quickstart.md) instead.

---

## Core Entry Points

The preferred package name is `earth_embedding`. All existing public
`rs_embed` imports remain available for compatibility.

### Locations and public AEF data

- `get_image_embedding(model, pixels, *, spatial, temporal, sensor=None, output=None, device="auto", model_config=None)`
  runs a model on caller-supplied finite CHW/TCHW arrays without fetching imagery.
  Use raw sensor units and the model's exact band ordering; `spatial` and
  `temporal` retain geolocation/date semantics. Checkpoints may download on first use.

- `get_location_embeddings(model, lonlat, *, device="auto", batch_size=1024, **model_kwargs)`
  accepts a nonempty `(N, 2)` WGS84 array in longitude/latitude order and returns
  `Embedding` with `(N, D)` data. Supports `satclip`, `geoclip`, `esri_gle`.
- `find_aef_tiles(index, *, spatial, year)` selects candidate COG URLs from a
  local official CSV/Parquet index or DataFrame; `spatial` is a WGS84 `BBox`.
- `sample_aef(lonlat, *, tiles, strict=True, overview_level=None)` reads and decodes
  raw AEF COG vectors into `(N, 64)` data, with masks and per-point provenance.
  The default samples native 10 m data. Select an official zero-based overview
  explicitly (0 = 20 m, 6 = 1280 m) for normalized area-sum vectors.
- `dequantize_aef(values)` decodes signed integer data and replaces nodata by NaN.

See [data access](data-access.md) and [location models](models.md#location-encoders).

Most users only need five public entry points: `get_embedding(...)`, `get_embeddings_batch(...)`, `export_batch(...)`, `load_export(...)`, and `inspect_provider_patch(...)`.

### Multi-model comparison and discovery

- `compare_embeddings(models=None, *, spatial, temporal=None, output=OutputSpec.grid(), model_options=None, on_error="raise", release_models=True, **shared_kwargs)`
  calls the geographic API for each selected model. `models=None` selects the
  complete catalog; `model_options` maps model IDs to per-model keyword overrides.
  The returned `EmbeddingComparison` keeps canonical model order, successful
  `embeddings`, and explicit `errors`. `on_error="record"` retains partial runs.
  Cached model runtimes are cleared between requests by default.
- `plot_embedding_comparison(comparison_or_mapping, *, columns=5, reference=None, reference_title="Reference image", title=None, lonlat=None, save_path=None, dpi=160)`
  returns a Matplotlib figure. Spatial grids use independent PCA RGB; pooled
  vectors are shown as feature profiles; point matrices need `lonlat` for a map.
  Error panels retain failed model IDs. Requires the `plot` extra.
- `get_model_resources(model)` and `list_model_resources()` expose lightweight
  upstream code, checkpoint, dataset, and documentation links without inference.

See the [comparison tutorial](tutorials/model-comparison.md) and
[resource directory](model-resources.md).

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

The current version is still early stage (`0.2.x`):

`BBox` and `PointBuffer` currently require `crs="EPSG:4326"`. Precomputed models should usually use `backend="auto"`, while on-the-fly models mainly use provider backends such as `"gee"` or other explicit provider names. `ExportConfig(format=...)` is the recommended way to choose export format; today that means `"npz"` or `"netcdf"`, with room for additional formats later.
