"""Generate the real README figures and spatial-probe metrics on CPU.

Run from the repository root: python examples/real_demos.py
"""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
from earth_embedding import get_location_embeddings
from earth_embedding.demo import classify_demo, load_demo, pca_colors, plot_classification, plot_map


def main():
    out = Path("docs/assets/demos")
    out.mkdir(parents=True, exist_ok=True)
    aef = load_demo("aef")
    fig = plot_map(
        aef.samples,
        pca_colors(aef.features),
        title="San Francisco Bay Area | AEF 2021 | PCA RGB (not classes)",
    )
    fig.savefig(out / "aef-pca.png", dpi=160)
    bayarea = load_demo("bayarea")
    gle = get_location_embeddings(
        "esri_gle",
        bayarea.samples[["center_lon", "center_lat"]].to_numpy(),
        device="cpu",
        batch_size=128,
    )
    fig = plot_map(
        bayarea.samples,
        pca_colors(gle.data),
        title="San Francisco Bay Area | Esri GLE | PCA RGB (no observation year)",
    )
    fig.savefig(out / "esri-gle-pca.png", dpi=160)
    result = classify_demo(bayarea)
    plot_classification(result).savefig(out / "bayarea-classification.png", dpi=160)
    (out / "classification-metrics.json").write_text(json.dumps(result["metrics"], indent=2) + "\n")
    result["samples"].to_csv(out / "classification-predictions.csv", index=False)
    print(json.dumps(result["metrics"], indent=2))


if __name__ == "__main__":
    main()
