"""Regenerate the four guided notebook sources; execute with run_demo_notebooks.py."""

from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "examples/notebooks"


def write(name, cells):
    nb = nbf.v4.new_notebook(
        cells=[
            nbf.v4.new_markdown_cell(text) if kind == "md" else nbf.v4.new_code_cell(text)
            for kind, text in cells
        ]
    )
    nb.metadata.kernelspec = {"display_name": "Python 3", "language": "python", "name": "python3"}
    OUT.mkdir(parents=True, exist_ok=True)
    nbf.write(nb, OUT / name)


setup = """%matplotlib inline
from pathlib import Path
from IPython.display import display
import matplotlib.pyplot as plt
import numpy as np
from earth_embedding.demo import load_demo, pca_colors, plot_map
out = Path("outputs")
out.mkdir(exist_ok=True)
print("CPU demo; outputs are saved in ./outputs")"""
intro = """\n\nInstall from the repository: `python -m pip install -e ".[demo,aef]"`.
Python 3.12+, CPU. Run all cells in order. All paths below are relative.
The small real data are bundled and SHA-256 checked by `load_demo`; corruption
raises an error. No Earth Engine login or manuscript workspace is needed.
[Full tutorial](https://github.com/GISWLH/earth-embedding/blob/main/docs/tutorials/real-demos.md)."""

write(
    "01_first_embedding_map.ipynb",
    [
        (
            "md",
            "# 01 · Your first real embedding map"
            + intro
            + """
Expected time: under one minute after installation. Download during this notebook: 0 bytes.
Source: Google / Google DeepMind AlphaEarth Foundations annual **2021**, CC-BY-4.0.
The bundled 5933-cell sample spans the San Francisco Bay Area and surroundings,
[-122.6,37.3,-121.6,38.3], approximately 88 × 111 km. It contains official
1280 m overview vectors (normalized sums of native AEF vectors), not 10 m
point samples or optical RGB. The complete checked bundle is about 2.1 MB.""",
        ),
        ("code", setup),
        (
            "code",
            """aef = load_demo("aef")
print(aef.features.shape)
print(aef.metadata["attribution"])
display(aef.samples.head())""",
        ),
        (
            "code",
            """fig = plot_map(aef.samples, pca_colors(aef.features), title="San Francisco Bay Area | AEF 2021 | PCA RGB")
fig.savefig(out / "aef-pca.png", dpi=160)
plt.show()""",
        ),
        (
            "md",
            """Red/green/blue show the first three principal components, stretched at the
2nd/98th percentiles. PCA is fitted only for this descriptive map. Colors are
**not land-cover labels** and cannot be compared to separately fitted PCA maps.
North is up; map placement uses the stored bounds, never implicit array order.

To fetch these same points yourself, install `.[aef]`, then run
`from earth_embedding.demo import fetch_aef_demo; fresh = fetch_aef_demo()`.
This reads official COG ranges (network transfer depends on COG block layout,
potentially tens of MB), checks the expected sample SHA-256, and caches the array.
Subsequent `fetch_aef_demo(offline=True)` calls use only the checked cache.
Network errors raise a clear error; the bundled `load_demo("aef")` remains usable offline.""",
        ),
    ],
)
write(
    "02_esri_locations.ipynb",
    [
        (
            "md",
            "# 02 · Esri GLE: batch, cache, offline"
            + intro
            + """
Expected time: 1–2 minutes on CPU. First download: official ~3.7 MB package;
subsequent runs: 0 bytes. Weights are not included in the repository.
Source: [Esri Global Location Encoder](https://www.arcgis.com/home/item.html?id=b0664ef297c04d4aaa44191cf21e07f3),
subject to Esri's model terms. The adapter validates the pinned checkpoint.
The 5933 query locations cover the San Francisco Bay Area, about 88 × 111 km. A location encoder has
no requested observation year; these are geographic priors, not 2021 imagery.
If the first download fails, restore connectivity and rerun; no synthetic fallback.""",
        ),
        ("code", setup + "\nfrom earth_embedding import get_location_embeddings"),
        (
            "code",
            """bayarea = load_demo("bayarea")
points = bayarea.samples[["center_lon", "center_lat"]].to_numpy()
gle = get_location_embeddings("esri_gle", points, device="cpu", batch_size=128, cache_dir="model-cache/esri")
print("Longitude, latitude:", points.shape, "→ embeddings:", gle.data.shape)
assert np.isfinite(gle.data).all()""",
        ),
        (
            "code",
            """offline = get_location_embeddings("esri_gle", points, device="cpu", batch_size=37, cache_dir="model-cache/esri", local_files_only=True)
np.testing.assert_allclose(gle.data, offline.data, rtol=1e-5, atol=1e-6)
np.savez_compressed(out / "esri-bayarea.npz", tile_id=bayarea.samples.tile_id.to_numpy(dtype="U"), features=offline.data)
print("Offline cache and batch consistency passed; exported IDs + 256-dimensional features.")""",
        ),
        (
            "code",
            """fig = plot_map(bayarea.samples, pca_colors(gle.data), title="San Francisco Bay Area | Esri GLE | PCA RGB (not classes)")
fig.savefig(out / "esri-gle-pca.png", dpi=160)
plt.show()""",
        ),
    ],
)
write(
    "03_regional_classification.ipynb",
    [
        (
            "md",
            "# 03 · Embeddings to a held-out classification map"
            + intro
            + """
Expected time: under one minute. Download: 0 bytes. Source: San Francisco Bay
Area, 5933 official 1280 m AEF **2021** overview cells and ESA WorldCover
**2021 v200** grouped dominant labels (both CC-BY-4.0; see bundled provenance).
Reference labels aggregate native 10 m pixel centers inside each AEF polygon.
This is a software teaching example, **not reproduction of the current global
paper benchmark**. It does not add any model to the frozen 20-system study.

The split was fixed before evaluation: south (maxlat <=37.88) trains, north
(minlat >=37.93) tests, with at least about 5.5 km between footprints.
3383 train / 2173 test / 375 buffer cells; two bare cells are excluded.
The four classes are built, vegetation, cropland and water. Only nine training
cells are cropland: this geographic class imbalance is retained, not resampled.
No parameter selection or test-label tuning: StandardScaler + LogisticRegression(C=1, tol=1e-8, seed=42).
Training uses float64 and a strict convergence tolerance for numerical reproducibility.""",
        ),
        (
            "code",
            setup
            + "\nimport json\nfrom earth_embedding.demo import classify_demo, plot_classification",
        ),
        (
            "code",
            """bayarea = load_demo("bayarea")
result = classify_demo(bayarea)
display(__import__("pandas").crosstab(result["samples"].demo_split, result["samples"].class_name))
print(json.dumps(result["metrics"], indent=2))""",
        ),
        (
            "code",
            """train = result["samples"].demo_split.eq("train").to_numpy()
np.testing.assert_allclose(result["estimator"].named_steps["standardscaler"].mean_, bayarea.features[train].mean(axis=0, dtype=np.float64))
assert result["samples"].loc[~result["samples"].demo_split.eq("test"), "prediction"].isna().all()
print("Scaler fitted on train only; predictions and metrics restricted to held-out north.")""",
        ),
        (
            "code",
            """fig = plot_classification(result)
fig.savefig(out / "bayarea-classification.png", dpi=160)
result["samples"].to_csv(out / "predictions.csv", index=False)
(out / "metrics.json").write_text(json.dumps(result["metrics"], indent=2))
plt.show()""",
        ),
        (
            "md",
            """Gray areas have no held-out prediction. Red errors and confusion-matrix
rows compare predictions to WorldCover reference labels, not field-survey truth.
OA is overall accuracy; Macro-F1 gives each of the four classes equal weight;
Balanced Accuracy is mean per-class recall. One regional holdout has no uncertainty
estimate or global generalization claim. Same-year input and reference products
may share satellite signals; the buffer reduces immediate adjacency leakage,
but does not remove all spatial autocorrelation.""",
        ),
    ],
)
write(
    "04_export_and_reuse.ipynb",
    [
        (
            "md",
            "# 04 · Batch export and safe feature reuse"
            + intro
            + """
Expected time: under one minute. Download: 0 bytes. Uses the same real AEF 2021
Bay Area 5933-cell data and WorldCover labels (CC-BY-4.0) as notebook 03.
AEF overview vectors and GLE geographic priors have different spatial support
and input semantics. This notebook teaches
portable exports and ID alignment instead of claiming a fair model comparison.""",
        ),
        (
            "code",
            setup + "\nfrom earth_embedding.demo import align_samples, classify_demo, DemoData",
        ),
        (
            "code",
            """bayarea = load_demo("bayarea")
parts = []
for start in range(0, len(bayarea.samples), 128):
    ids = bayarea.samples.tile_id.iloc[start:start+128].to_numpy(dtype="U")
    x = bayarea.features[start:start+128]
    path = out / f"batch-{start:04d}.npz"
    np.savez_compressed(path, tile_id=ids, features=x)
    parts.append(path)
print(f"Exported {len(parts)} ID-bearing batches; no model inference needed.")""",
        ),
        (
            "code",
            """ids, arrays = [], []
for path in reversed(parts):  # Deliberately read in a different order.
    with np.load(path, allow_pickle=False) as z:
        ids.extend(z["tile_id"].tolist())
        arrays.append(z["features"])
aligned = align_samples(bayarea.samples, np.array(ids), np.vstack(arrays))
np.testing.assert_array_equal(aligned, bayarea.features)
reused = classify_demo(DemoData(bayarea.samples, aligned, bayarea.metadata))
print("Shuffled-batch round trip: exact feature equality.")
print({key: reused["metrics"][key] for key in ["oa", "macro_f1", "balanced_accuracy"]})""",
        ),
        (
            "code",
            """fig = plot_map(bayarea.samples, pca_colors(aligned), title="Reused AEF 2021 1280 m overview cells | PCA RGB")
fig.savefig(out / "reused-pca.png", dpi=160)
plt.show()""",
        ),
        (
            "md",
            """Every export includes stable IDs. `align_samples` rejects duplicate IDs,
unequal ID sets and nonfinite features. It never joins by an implicit row order.
When bringing your own data, preserve source/year/license and spatial support,
document exclusions, and design a geographic holdout before looking at scores.""",
        ),
    ],
)
print("Generated four notebook sources; execution is a separate mandatory step.")
