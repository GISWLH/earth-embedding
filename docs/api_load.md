# API: Load

This page covers the export reader API for loading files produced by [`export_batch`](api_export.md).

Related pages: [API: Specs and Data Structures](api_specs.md), [API: Embedding](api_embedding.md), and [API: Export](api_export.md).

---

## load_export (primary / recommended) { #load_export }

### Signature

```python
load_export(
    path: Union[str, os.PathLike],
) -> ExportResult
```

Use `load_export(...)` to read any export produced by [`export_batch`](api_export.md) — both **combined** (single file) and **per-item** (directory) layouts are supported. The layout is detected automatically.

### Mental Model

`load_export(...)` answers one question: _where is the export?_

- Pass a **file** (`.npz`, `.nc`, or `.json`) to load a **combined** export.
- Pass a **directory** to load a **per-item** export.

Everything else — layout detection, key parsing, NaN-fill for partial failures — is handled automatically.

### Default Pattern

```python
from rs_embed import load_export

# Combined export (single file)
result = load_export("exports/run.npz")

# Per-item export (directory of p00000.npz, p00001.npz, ...)
result = load_export("exports/per_item_run/")
```

---

## Parameters

| Parameter | Meaning                                                                          |
| --------- | -------------------------------------------------------------------------------- |
| `path`    | Path to a `.npz`/`.nc`/`.json` file (combined) or a directory (per-item export). |

### Raises

| Exception           | When                                                         |
| ------------------- | ------------------------------------------------------------ |
| `FileNotFoundError` | Path does not exist.                                         |
| `ValueError`        | Path exists but cannot be interpreted as an rs-embed export. |
| `ImportError`       | NetCDF export requested but `xarray` is not installed.       |

---

## Return Value: ExportResult { #ExportResult }

`load_export(...)` always returns an `ExportResult`.

```python
@dataclass
class ExportResult:
    layout: str                        # "combined" or "per_item"
    spatials: list[dict]               # one dict per spatial point
    temporal: dict | None              # temporal spec used at export time
    n_items: int                       # number of spatial points
    status: str                        # "ok" | "partial" | "failed"
    models: dict[str, ModelResult]     # keyed by model name
    manifest: dict                     # raw manifest for advanced use
```

### Convenience Methods

```python
result.embedding("remoteclip")   # → np.ndarray, shape (n_items, dim)
result.ok_models                 # → list[str]  — models with status "ok"
result.failed_models             # → list[str]  — models with status "failed"
```

`embedding(model)` raises `KeyError` if the model was not part of the export and `ValueError` if the model failed for every point.

---

## ModelResult { #ModelResult }

Each entry in `result.models` is a `ModelResult`:

```python
@dataclass
class ModelResult:
    name: str                          # canonical model identifier
    status: str                        # "ok" | "partial" | "failed"
    embeddings: np.ndarray | None      # (n_items, dim) or (n_items, C, H, W)
    inputs: np.ndarray | None          # (n_items, C, H, W) — None if not saved
    meta: list[dict]                   # per-point embedding metadata
    error: str | None                  # error string for fully-failed models
```

**Status values:**

| Status      | Meaning                                                              |
| ----------- | -------------------------------------------------------------------- |
| `"ok"`      | All points succeeded.                                                |
| `"partial"` | Some points succeeded; failed points are NaN-filled in `embeddings`. |
| `"failed"`  | All points failed; `embeddings` is `None`.                           |

---

## Common Patterns

### Load and inspect a combined export

```python
from rs_embed import load_export

result = load_export("exports/combined_run.npz")

print(result.n_items)           # number of spatial points
print(result.ok_models)         # models that succeeded
print(result.temporal)          # {'start': '2022-06-01', 'end': '2022-09-01'}

emb = result.embedding("remoteclip")   # shape (n_items, dim)
```

### Access inputs when save_inputs=True

```python
result = load_export("exports/combined_run.npz")
mr = result.models["prithvi"]
if mr.inputs is not None:
    print(mr.inputs.shape)   # (n_items, C, H, W)
```

### Load a per-item export directory

```python
result = load_export("exports/per_item_run/")
print(result.layout)        # "per_item"
print(result.n_items)       # number of files found

emb = result.embedding("remoteclip")   # (n_items, dim) — stacked from per-file arrays
```

### Handle partial failures

```python
result = load_export("exports/combined_run.npz")

if result.failed_models:
    print("Failed:", result.failed_models)

for name in result.ok_models:
    emb = result.embedding(name)
    print(f"{name}: {emb.shape}")
```

### Load via the manifest JSON

Pass the `.json` manifest path if that is what you have — `load_export` finds the paired array file automatically:

```python
result = load_export("exports/combined_run.json")
```

---

## Relationship to export_batch

`load_export` is the read-side counterpart to `export_batch`. Every file produced by `export_batch` can be read back with `load_export` without manually parsing NPZ keys or manifest JSON.

```python
from rs_embed import export_batch, load_export, ExportTarget, ExportConfig, PointBuffer, TemporalSpec

# Write
export_batch(
    spatials=[PointBuffer(121.5, 31.2, 2048)],
    temporal=TemporalSpec.range("2022-06-01", "2022-09-01"),
    models=["remoteclip"],
    target=ExportTarget.combined("exports/run"),
    config=ExportConfig(save_inputs=True),
)

# Read back
result = load_export("exports/run.npz")
emb = result.embedding("remoteclip")   # shape (1, dim)
```

!!! tip "Simple rule"
Pass a file path for combined exports, a directory path for per-item exports.
Everything else is automatic.
