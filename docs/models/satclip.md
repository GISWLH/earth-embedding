# SatCLIP (`satclip`)

> Location-encoder adapter for SatCLIP: longitude/latitude in, embedding out. No imagery is fetched or accepted.

## Quick Facts

| Field                             | Value                                                                              |
| --------------------------------- | ---------------------------------------------------------------------------------- |
| Model ID                          | `satclip`                                                                          |
| Aliases                           | `satclip_vit16_l40`                                                                |
| Release class                     | B, location encoder (frozen rs-embed taxonomy)                                     |
| Family / Backbone                 | SatCLIP spherical-harmonic encoding + SIREN (vendored, microsoft/satclip@1ead1067) |
| Adapter type                      | `location`                                                                         |
| Typical backend                   | `auto`                                                                             |
| Primary input                     | `PointBuffer` or `BBox` in EPSG:4326; only the coordinates are used                |
| Default variant                   | `vit16-l40` (`microsoft/SatCLIP-ViT16-L40`, pinned revision)                       |
| Other variants                    | `vit16-l10`, `resnet50-l40`                                                        |
| Temporal mode                     | ignored (accepted for interface compatibility)                                     |
| Output modes                      | `pooled` (centre query), `grid` (cell-centre coordinate grid)                      |
| Embedding dimension               | 256                                                                                |
| Default grid spacing              | 1,000 m coordinate sampling; not learned spatial resolution                        |

---

## When To Use This Model

Use `satclip` when a task needs a learned location prior without acquiring imagery, or as a
coordinate-only comparison against image encoders and precomputed products. The vector encodes what
the model learned from its pretraining images about a place; it is not an observation of current
surface conditions and cannot change between years at the same location.

Spatial detail is limited by the spherical-harmonic degree: `L=40` resolves broad regional
structure and `L=10` only continental-scale structure. Within a few kilometres the embedding is
nearly constant, so dense `grid` outputs are useful mainly as a diagnostic.

---

## Input Contract

- `PointBuffer`: `pooled` queries the point; `grid` samples the surrounding bounding box.
- `BBox`: `pooled` queries the box centre; `grid` evaluates cell centres on a north-up grid.
- `grid_step_m` sets approximate coordinate sampling spacing (default 1,000 m). Grid dimensions
  use ceiling division and span the requested bounds. SatCLIP, GeoCLIP, and Esri GLE use the
  same cell centres for the same region and spacing.
- Grid size is checked against `max_grid_points` before allocating coordinates or running
  inference. Increase spacing to stay under the limit, or raise the limit explicitly.
- `input_chw` is rejected: SatCLIP is a location encoder.
- `OutputSpec.pooling` is not applied; metadata records `pooling="centre_coordinate_query"`.

## Model Settings

Pass these keywords directly to `get_embedding(...)` or `get_embeddings_batch(...)`.
Unknown settings raise an error. Explicit values take precedence over environment variables.

| Keyword | Default | Effect |
| --- | --- | --- |
| `variant` | `vit16-l40` | Select `vit16-l40`, `vit16-l10`, or `resnet50-l40` |
| `grid_step_m` | `1000` | Approximate cell spacing for grid queries; finite and positive |
| `max_grid_points` | `100000` | Maximum number of coordinate queries in one grid |
| `batch_size` | `1024` | Coordinates processed in each forward pass; positive integer |

The default grid spacing changed from 10 m to 1,000 m to keep geographic previews bounded.
Set `grid_step_m=10` explicitly when reproducing an older dense query, and increase
`max_grid_points` if the region requires it. Sampling more densely does not increase the
model's learned spatial resolution.

## Environment Variables

| Env var                          | Default     | Effect                                                      |
| -------------------------------- | ----------- | ----------------------------------------------------------- |
| `RS_EMBED_SATCLIP_VARIANT`       | `vit16-l40` | Variant when `variant=` is not passed                       |
| `RS_EMBED_SATCLIP_CKPT`          | unset       | Local checkpoint path (skips the Hugging Face download)     |
| `RS_EMBED_SATCLIP_GRID_STEP_M`   | `1000`      | Grid spacing when `grid_step_m=` is not passed             |
| `RS_EMBED_SATCLIP_CHUNK`         | `1024`      | Geographic API batch size when `batch_size=` is not passed |
| `RS_EMBED_SATCLIP_WEIGHTS_ONLY`  | `1`         | `torch.load(weights_only=...)`; keep `1` for released files |

Set `HF_ENDPOINT` when Hugging Face must be reached through a mirror.
The point-list API `get_location_embeddings(...)` uses its explicit `batch_size` parameter
(default 1,024), independently of `RS_EMBED_SATCLIP_CHUNK`.

## Example

```python
from earth_embedding import BBox, OutputSpec, PointBuffer, get_embedding

emb = get_embedding("satclip", spatial=PointBuffer(lon=114.41, lat=30.52, buffer_m=320))
print(emb.data.shape)  # (256,)

grid = get_embedding(
    "satclip",
    spatial=BBox(114.35, 30.46, 114.43, 30.54),
    output=OutputSpec.grid(),
    grid_step_m=320,
    max_grid_points=100000,
    batch_size=1024,
    device="cpu",
)
print(grid.data.shape)  # (256, 28, 24)
```

## Provenance

The vendored runtime reproduces the upstream `load_lightweight.py` location branch exactly
(maximum absolute difference 0.0 on 503 test coordinates for L10 and L40). Only the
spherical-harmonic functions up to degree 39 are vendored. SatCLIP code and weights are MIT
licensed (Klemmer et al., AAAI 2025).
