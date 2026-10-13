# Esri Global Location Encoder (Sentinel-2)

`esri_gle` provides a coordinate-only adapter for Esri's Global Location Encoder.
It uses `arcgis.learn.Embeddings(dataset_type="location",
backbone="satclip/sentinel-2_trained")`. This is Esri's pretrained model, with
separate weights from Microsoft's SatCLIP. It produces 256-dimensional vectors.

**Status:** the adapter contract has been checked against the official ArcGIS API
for Python 2.4.3 source and tested with a deterministic runtime substitute.
Pretrained Esri inference still requires a compatible Esri environment and model
access. A mocked contract test is not evidence that the pretrained model has run.

On 2026-10-13 we attempted a real three-coordinate CPU call with the official
ArcGIS 2.4.3 and fastai 1.0.61 distributions in an isolated package directory on
Linux/Python 3.12. Two checks identified separate blockers in that environment:

1. `fastai.text` could not import because `spacy` was missing. ArcGIS's
   image-captioning import chain masked that dependency error and then raised
   `NameError: name 'torch' is not defined`. PyTorch itself imported successfully.
2. The official weights loader uses `GIS("home")`. A direct check of this call
   failed because `arcpy` was unavailable and an authorized ArcGIS host connection
   was not available through that path. The checked local Windows Python also
   had no `arcpy` installation.

Model loading and inference were not reached. This integration is therefore
**blocked in the tested environment**, not validated as a working pretrained
inference run. These results do not imply that the adapter fails in a properly
configured, authorized ArcGIS environment.

## Environment

Use an [Esri-supported deep-learning environment](https://developers.arcgis.com/python/latest/guide/install-and-set-up/)
with ArcGIS API for Python **2.4.3** and the corresponding `arcgis.learn`
dependencies. Installing the `arcgis` wheel alone does not install every required
deep-learning component. ArcGIS is deliberately optional and is not installed by
the ordinary library installation.

The official runtime manages checkpoint download and its local cache. The Esri
model and its downloads remain subject to Esri's access and license terms; the
library neither redistributes these weights nor replaces them with Microsoft
SatCLIP weights. For ArcGIS Pro's `.dlpk` workflow, follow the official model page
linked below. A `.dlpk` is not accepted as a PyTorch checkpoint by this adapter.
The checked ArcGIS loader calls `GIS("home")` for model access: run it in an
Esri environment where that connection is configured and authorized. An ordinary
standalone Python installation may not supply that connection.

## Query

```python
from earth_embedding import get_location_embeddings

embedding = get_location_embeddings(
    "esri_gle",  # aliases: "esri", "global_location_encoder"
    [[114.4, 30.5], [-117.1956, 34.0564]],  # longitude, latitude
    device="cpu",
    batch_size=1024,
)
print(embedding.data.shape)  # (2, 256)
print(embedding.meta["runtime_version"])
```

The adapter writes each bounded coordinate batch to a temporary CSV with `lon`
and `lat` columns. It calls the official `get(..., return_embeddings=True,
location_column=["lon", "lat"], spatial_reference=4326)` API and removes temporary
files even when inference fails. The returned array preserves input order. No
Earth Engine initialization or imagery fetch occurs.

`get_embedding("esri_gle", spatial=..., device="cpu")` supports the same centre
query interface as the other location encoders. `OutputSpec.grid()` samples
coordinates on a north-up grid, with `grid_step_m=1000` and
`max_grid_points=100000` defaults. These are sampling controls, not an assertion of
model resolution. Requested dates are ignored.

ArcGIS 2.4.3 internally fixes location inference batches at 1024; this adapter
splits the input files to honor smaller user batch sizes. It overrides the checked
runtime's `_get_device` hook so a CPU request does not first load onto a GPU,
without changing global ArcGIS environment settings. The adapter rejects other
ArcGIS versions until this private compatibility hook has been checked against
them. Metadata records the actual
runtime version, backbone and ArcGIS weights item ID.

## Scope and limitations

The official model is intended primarily for land locations and summarizes
conditions captured by its training imagery. A coordinate query does not provide
time-specific observations, arbitrary current imagery or guaranteed
generalization over open ocean. This additional integration is not part of the
paper's frozen 20-system benchmark.

## Official references

- [Model details and download workflow](https://doc.arcgis.com/en/pretrained-models/latest/vector/introduction-to-global-location-encoder-sentinel-2-.htm)
- [Use the model in ArcGIS Pro](https://doc.arcgis.com/en/pretrained-models/latest/vector/using-global-location-encoder-sentinel-2-.htm)
- [ArcGIS Embeddings Python API](https://developers.arcgis.com/python/latest/api-reference/arcgis.learn.toc.html#embeddings)
- [Esri explanation and model limitations](https://www.esri.com/arcgis-blog/products/arcgis-pro/geoai/beyond-latitude-and-longitude-giving-geographic-context-to-coordinates)
