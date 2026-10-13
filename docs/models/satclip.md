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

- `PointBuffer`: the point is queried directly.
- `BBox`: `pooled` queries the box centre; `grid` evaluates cell centres on a north-up grid with
  `RS_EMBED_SATCLIP_GRID_STEP_M` spacing (default 10 m).
- `input_chw` is rejected: SatCLIP is a location encoder.
- `OutputSpec.pooling` is not applied; metadata records `pooling="centre_coordinate_query"`.

## Environment Variables

| Env var                          | Default     | Effect                                                      |
| -------------------------------- | ----------- | ----------------------------------------------------------- |
| `RS_EMBED_SATCLIP_VARIANT`       | `vit16-l40` | Variant when `variant=` is not passed                       |
| `RS_EMBED_SATCLIP_CKPT`          | unset       | Local checkpoint path (skips the Hugging Face download)     |
| `RS_EMBED_SATCLIP_GRID_STEP_M`   | `10`        | Grid spacing for `OutputSpec.grid()`                        |
| `RS_EMBED_SATCLIP_CHUNK`         | `65536`     | Coordinates per forward pass                                |
| `RS_EMBED_SATCLIP_WEIGHTS_ONLY`  | `1`         | `torch.load(weights_only=...)`; keep `1` for released files |

Set `HF_ENDPOINT` when Hugging Face must be reached through a mirror.

## Example

```python
from rs_embed import get_embedding
from rs_embed.core.specs import PointBuffer

emb = get_embedding("satclip", spatial=PointBuffer(lon=114.41, lat=30.52, buffer_m=320))
print(emb.data.shape)  # (256,)
```

## Provenance

The vendored runtime reproduces the upstream `load_lightweight.py` location branch exactly
(maximum absolute difference 0.0 on 503 test coordinates for L10 and L40). Only the
spherical-harmonic functions up to degree 39 are vendored. SatCLIP code and weights are MIT
licensed (Klemmer et al., AAAI 2025).
