# GeoCLIP

GeoCLIP maps coordinates to 512-dimensional vectors. Its pretrained location branch
learns from geotagged ground-level photographs. Querying it requires no imagery and
no Earth Engine account. This library uses the authors' **actual pretrained
`LocationEncoder`**, without instantiating their image encoder.

**Verified:** on 2026-10-13, three real coordinate queries using GeoCLIP 1.2.3's
packaged pretrained checkpoint returned finite `(3, 512)` float32 features on CPU.
They agreed with a direct upstream `LocationEncoder` call to an absolute difference
of less than `3e-8`. Checkpoint SHA-256:
`94b80ae3af89fca78539e129dd2929d321247f5ceeeb0a31bc2c31041a253394`.

## Install and query

```bash
pip install "geoclip==1.2.3"
```

```python
from earth_embedding import get_location_embeddings

embedding = get_location_embeddings(
    "geoclip",
    [[114.4, 30.5], [139.6917, 35.6895]],  # longitude, latitude (WGS84)
    device="cpu",
    batch_size=1024,
)
print(embedding.data.shape)  # (2, 512)
print(embedding.meta)
```

The shared API always accepts **longitude first**. The adapter swaps the columns
for GeoCLIP's native `[latitude, longitude]` input. Passing coordinates in the wrong
order can produce plausible but incorrect results: range checks cannot detect all
swapped coordinates. Features are returned as float32, without L2 normalization,
in the original input row order.

## Region queries and grids

```python
from earth_embedding import BBox, OutputSpec, get_embedding

embedding = get_embedding(
    "geoclip",
    spatial=BBox(114.3, 30.4, 114.5, 30.6),
    output=OutputSpec.pooled(),
    device="cpu",
)
```

Pooled output queries the region's centre coordinate. A temporal argument is
accepted for compatibility and ignored. `OutputSpec.grid()` evaluates coordinate
queries on a north-up grid; set `grid_step_m=1000` and `max_grid_points=100000` as
model keyword arguments. Grid spacing controls query density, **not** the
information content or physical resolution of the pretrained model.

## Checkpoints and reproducibility

By default, the official GeoCLIP Python distribution supplies
`geoclip/model/weights/location_encoder_weights.pth`. To load a locally retained
official location checkpoint, pass `checkpoint="/path/location_encoder_weights.pth"`
or set `RS_EMBED_GEOCLIP_CKPT`. The adapter reads a plain PyTorch state dictionary
with `weights_only=True` and strict parameter matching. Whole GeoCLIP model
checkpoints and randomly initialized architectures are not substituted.

The runtime is cached by checkpoint path and device. Restart the Python process
after replacing checkpoint contents at the same path. Metadata includes runtime
version, device, checkpoint source, native/public coordinate order and output
dimension. The base library stays lightweight; GeoCLIP's own package declares its
PyTorch, torchvision, transformers and supporting dependencies.

## Sources and credit

- [Official repository and location-encoder example](https://github.com/VicenteVivan/geo-clip)
- [Official implementation](https://github.com/VicenteVivan/geo-clip/blob/main/geoclip/model/location_encoder.py)
- [GeoCLIP paper, NeurIPS 2023](https://arxiv.org/abs/2309.16020)

The upstream implementation is MIT licensed. GeoCLIP is an additional software
integration; adding it to the catalog does not add it to the paper's frozen
20-system benchmark.
