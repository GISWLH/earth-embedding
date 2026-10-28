# Real regional embeddings, maps and a CPU classifier

The San Francisco Bay Area and surroundings span approximately **92 × 113 km**
(about 122.54–121.48° W, 37.30–38.32° N). The checked 2.3 MB bundle is a **complete
72 × 88 grid of 6,336 real AEF 2021 cells** on the official 1,280 m overview grid,
with matching WorldCover 2021 reference labels and cell polygons. Every cell inside
the frame is present, so maps have no clipped edges or no-data holes. This is a
regional software demonstration, not a reproduction or extension of the paper's
frozen 20-system global benchmark.

## Install and draw your first map

Python 3.12+, CPU. Install from the repository; no PyPI release is assumed.

```bash
git clone https://github.com/GISWLH/earth-embedding.git
cd earth-embedding
python -m pip install -e ".[demo,aef]"
```

```python
from earth_embedding.demo import load_demo, pca_colors, plot_map
data = load_demo("aef")
colors = pca_colors(data.features)
fig = plot_map(data.samples, colors, title="San Francisco Bay Area · AEF 2021 · PCA RGB")
fig.savefig("aef-pca.png", dpi=160)
```

![AEF overview PCA](../assets/demos/aef-pca.png)

`load_demo("aef")` and `load_demo("bayarea")` load the same data without network
access. Each payload is verified against SHA-256 in its bundled manifest; vectors
are joined to metadata by `tile_id`, never an assumed file row order.

These are **1,280 m official AEF overview cells**, not native 10 m point samples.
Google's overviews encode normalized sums of native vectors. We decode signed
int8 values using `sign(x) * (x / 127.5)**2`, with -128 treated as missing.
RGB shows PCA components stretched at their 2nd/98th percentiles.
**PCA colors are not land-cover classes** and cannot be compared between separately
fitted maps. PCA is descriptive and is not used by the classifier. Because the
sample is a complete grid (`grid_row`, `grid_col`), `plot_map` draws it as one
seamless curvilinear mesh with exact cell geometry, cropped to the inner frame.

To reproduce official GCS reads (first call needs network access):

```python
from earth_embedding.demo import fetch_aef_demo
fresh = fetch_aef_demo(cache_dir="cache/aef")
cached = fetch_aef_demo(cache_dir="cache/aef", offline=True)
```

Four bounded overview reads avoid downloading entire native COGs or a global
index. The decoded array is pinned to SHA-256, then cached atomically. Raw
overview payload totals 1 MiB; actual HTTP transfer includes headers and range
overhead and was not metered. Network failures and corrupted caches raise clear
errors without substitute data. Advanced callers can use
`sample_aef(points, tiles=urls, overview_level=6)` directly. Omitting
`overview_level` retains existing native 10 m behavior.

## Encode 6,336 locations with Esri GLE

```python
from earth_embedding import get_location_embeddings
from earth_embedding.demo import load_demo, pca_colors, plot_map
data = load_demo("bayarea")
points = data.samples[["center_lon", "center_lat"]].to_numpy()
gle = get_location_embeddings("esri_gle", points, device="cpu", batch_size=128)
fig = plot_map(data.samples, pca_colors(gle.data), title="San Francisco Bay Area · Esri GLE · PCA RGB")
fig.savefig("esri-gle-pca.png", dpi=160)
```

![Location encoder PCA](../assets/demos/esri-gle-pca.png)

The official lightweight Esri package (~3.7 MB) downloads once. Inference runs
directly in PyTorch without ArcGIS/ArcPy. Coordinates are `[longitude, latitude]`.
GLE has no observation year: it encodes a geographic prior. Drawing point
features on this grid is a visualization choice, not matched area support.
Notebook 02 verifies batch consistency and `local_files_only=True`. Weights are
not committed and remain subject to the
[Esri model terms](https://www.arcgis.com/home/item.html?id=b0664ef297c04d4aaa44191cf21e07f3).

## Real spatial classification

```python
from earth_embedding.demo import classify_demo, plot_classification
result = classify_demo()
print({k: result["metrics"][k] for k in ("oa", "macro_f1", "balanced_accuracy")})
fig = plot_classification(result)
fig.savefig("bayarea-classification.png", dpi=160)
```

![Reference, out-of-fold prediction, errors and confusion matrix](../assets/demos/bayarea-classification.png)

The geographic split was fixed before scoring: **two spatial folds by grid column**.
A model fitted only on the west half (columns 0–32) predicts the east half
(columns 39–71), and a model fitted only on the east half predicts the west half.
Columns 33–38 form a 7.68 km buffer that is never fitted or scored; the minimum gap
between fitted and predicted footprints is 0.0737° longitude (about 6.5 km). Every
scored cell therefore has an out-of-fold prediction, and the maps are complete.
Two bare cells remain in the reference map but are outside the four-class task.

| Fold half | Built | Vegetation | Cropland | Water | Bare | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| West (columns 0–32) | 504 | 1433 | 51 | 914 | 2 | 2904 |
| East (columns 39–71) | 325 | 1936 | 512 | 131 | 0 | 2904 |
| Buffer (columns 33–38) | 158 | 299 | 1 | 70 | 0 | 528 |

Each fold fits `StandardScaler` and
`LogisticRegression(C=1, class_weight="balanced", tol=1e-8, max_iter=4000, random_state=42)`
on its own half only. Class weights compensate for the uneven cropland and water
split between halves; there is no tuning or random split. Explicit float64 training
and a strict convergence tolerance avoid version-dependent float32 solver paths.

| Scope | Scored cells | OA | Macro-F1 | Balanced Accuracy |
| --- | ---: | ---: | ---: | ---: |
| Pooled out-of-fold | 5806 | 93.64% | 91.64% | 92.63% |
| Fit west → predict east | 2904 | 92.46% | 90.99% | — |
| Fit east → predict west | 2902 | 94.83% | 87.85% | — |

These are this run's measurements, saved in
[metrics JSON](../assets/demos/classification-metrics.json) and
[ID-bearing predictions CSV](../assets/demos/classification-predictions.csv)
(`predicted_by` names the fold model). Confusion-matrix rows are reference labels;
columns are predictions, in the order built, vegetation, cropland, water. The hatched
buffer is unscored. Most errors are vegetation/cropland confusions along field
margins; pooled cropland recall is 470/563. Two regional folds give no uncertainty
estimate or global generalization claim. WorldCover is a satellite-derived reference,
not field-survey truth. Same-year products may share satellite signals, and the
buffer cannot remove all spatial autocorrelation. Coarse majority classes hide
within-cell mixtures.

## Sources, selection and independent rebuilding

The source inspection found the paper's existing global cache to be discrete
samples, unsuitable for a continuous regional map. This replacement reads a
bounded subset of official public products; it does not change paper data/results.

- [Google / Google DeepMind AEF GCS documentation](https://developers.google.com/earth-engine/guides/aef_on_gcs_readme): annual 2021, four UTM 10N COGs, official overview index 6. CC-BY-4.0.
- [ESA WorldCover data access](https://esa-worldcover.org/en/data-access): 2021 v200, `N36W123`, native 10 m labels from the official public AWS COG. CC-BY-4.0.
- Attribution: The AlphaEarth Foundations Satellite Embedding dataset is produced by Google and Google DeepMind. © ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium.

The sample is the whole-cell rectangle `x 540960–633120 m, y 4129280–4241920 m`
in EPSG:32610 on the official 1,280 m overview grid: 72 columns × 88 rows. It was
chosen so that every cell has a complete AEF vector (open-ocean overview cells are
no-data) and is checked again at build time; the earlier lon/lat-box selection
clipped the rotated UTM grid into a staircase and left ocean holes. Each cell has at
least 95% valid reference support. WorldCover native pixel **centers inside the
same AEF polygon** are counted, grouped, then the most frequent group is assigned
(alphabetic tie break). Codes 10/20/30/90/95/100 map to vegetation, 40 to cropland,
50 to built, 80 to water, 60 to bare and 70 to snow. Zero is nodata. Selection
does not use scores. Maps use transformed polygons, including south-up source
rasters; neither file order nor raster row number determines north.

The installed `rs_embed/data/demos/bayarea/manifest.json` records exact source
URLs, pixel hashes, decoded feature hash, payload sizes, selection and license.
Large source rasters are not committed. Rebuild from pinned public URLs with no
private paths or index file (`--repin` deliberately replaces the pins):

```bash
python scripts/prepare_bayarea_demo.py
python examples/real_demos.py
python scripts/run_demo_notebooks.py
python scripts/validate_real_demos.py
```

Preparation reads four overviews and a bounded 12,289 × 12,728 WorldCover window
(156 MB uncompressed; on-wire transfer varies). Allow a few minutes, network access
and about 1 GB free memory. Source cache pixels are checked against pinned SHA-256
values. Normal examples and notebooks use only the 2.3 MB bundled subset.

| Field | Meaning |
| --- | --- |
| `tile_id` | Stable UTM center identifier, shared with NPZ feature IDs |
| `grid_row`, `grid_col` | Position in the 88 × 72 grid; row 0 is the north edge |
| `center_lon`, `center_lat` | Cell center in WGS84 degrees |
| `minlon/minlat/maxlon/maxlat` | Geographic envelope for split checks |
| `lon0/lat0` … `lon3/lat3` | Four transformed corners of the UTM cell |
| `utm_easting`, `utm_northing` | EPSG:32610 center in meters |
| `class_name`, `dominant_fraction` | Grouped majority and its fraction |
| `reference_valid_fraction` | Share of valid WorldCover pixels in the cell |
| `demo_split` | Fixed `west` / `buffer` / `east` fold assignment |
| `features` | 64-dimensional float32 official overview vectors |

## Executed notebooks

| Notebook | Task | Expected CPU time | First download |
| --- | --- | --- | --- |
| [01](https://github.com/GISWLH/earth-embedding/blob/main/examples/notebooks/01_first_embedding_map.ipynb) | Regional AEF PCA map | <1 minute | None |
| [02](https://github.com/GISWLH/earth-embedding/blob/main/examples/notebooks/02_esri_locations.ipynb) | GLE batching, cache and offline inference | 1–2 minutes | ~3.7 MB weights |
| [03](https://github.com/GISWLH/earth-embedding/blob/main/examples/notebooks/03_regional_classification.ipynb) | Two-fold spatial holdout, metrics and maps | <1 minute | None |
| [04](https://github.com/GISWLH/earth-embedding/blob/main/examples/notebooks/04_export_and_reuse.ipynb) | ID-safe batch export and reuse | <1 minute | None |

Each is executed from a fresh kernel with real outputs and at least one embedded
map. Notebook 04 teaches reuse rather than ranking unequal spatial supports.
See separate receipts for [notebooks](../validation/demo-notebooks.json),
[actual AEF/GLE and README execution](../validation/demo-live.json), and
[repository checks](../validation/real-demos-20261013.json).
