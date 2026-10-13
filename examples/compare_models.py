"""Extract several models for one region, save their features, and plot one figure.

    python examples/compare_models.py --models satclip geoclip esri_gle --device cpu
    python examples/compare_models.py --models all --out outputs/comparison

Install the project first. The all-model run requires model-specific runtimes,
weights, and data-provider access; its failures are recorded, never substituted.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--models", nargs="+", default=["satclip", "geoclip", "esri_gle"])
    parser.add_argument(
        "--bbox",
        type=float,
        nargs=4,
        default=[114.35, 30.46, 114.43, 30.54],
        metavar=("WEST", "SOUTH", "EAST", "NORTH"),
    )
    parser.add_argument("--year", type=int, default=2021)
    parser.add_argument("--start", default=None, help="Image window start, default YEAR-05-01")
    parser.add_argument("--end", default=None, help="Image window end, default YEAR-10-31")
    parser.add_argument("--grid-step-m", type=float, default=320, help="Location sampling only")
    parser.add_argument("--device", default="auto")
    parser.add_argument("--columns", type=int, default=5)
    parser.add_argument("--out", type=Path, default=Path("outputs/comparison"))
    parser.add_argument(
        "--allow-errors", action="store_true", help="Exit zero with partial results"
    )
    args = parser.parse_args(argv)
    if args.grid_step_m <= 0 or not np.isfinite(args.grid_step_m):
        parser.error("--grid-step-m must be finite and positive")
    if args.columns < 1:
        parser.error("--columns must be positive")
    if "all" in args.models and args.models != ["all"]:
        parser.error("Use --models all alone, or provide a list of model IDs")

    from earth_embedding import (
        BBox,
        OutputSpec,
        TemporalSpec,
        compare_embeddings,
        list_models,
        plot_embedding_comparison,
    )
    from rs_embed.embedders.catalog import canonical_model_id

    models = (
        list_models()
        if args.models == ["all"]
        else [canonical_model_id(model) for model in args.models]
    )
    options = {}
    for model in models:
        if model in {"satclip", "geoclip", "esri_gle"}:
            options[model] = {"temporal": None, "grid_step_m": args.grid_step_m}
        elif model in {"gse", "tessera", "copernicus"}:
            options[model] = {"temporal": TemporalSpec.year(args.year)}

    spatial = BBox(*args.bbox)
    temporal = TemporalSpec.range(
        args.start or f"{args.year}-05-01", args.end or f"{args.year}-10-31"
    )
    spatial.validate()
    temporal.validate()
    comparison = compare_embeddings(
        models,
        spatial=spatial,
        temporal=temporal,
        output=OutputSpec.grid(),
        model_options=options,
        device=args.device,
        on_error="record",
    )
    args.out.mkdir(parents=True, exist_ok=True)
    report = {
        "request": {
            "models": models,
            "bbox": args.bbox,
            "year": args.year,
            "image_window": [temporal.start, temporal.end],
            "location_grid_step_m": args.grid_step_m,
            "device": args.device,
        },
        "successful": {},
        "errors": comparison.errors,
        "interpretation": "Independent PCA colors; native support differs; not a ranking.",
    }
    for model, embedding in comparison.embeddings.items():
        values = embedding.data
        if hasattr(values, "detach"):
            values = values.detach().cpu().numpy()
        data = np.asarray(values)
        np.savez_compressed(args.out / f"{model}.npz", data=data)
        report["successful"][model] = {
            "shape": list(data.shape),
            "features": f"{model}.npz",
            "meta": embedding.meta,
        }
    (args.out / "report.json").write_text(
        json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8"
    )
    figure = plot_embedding_comparison(comparison, columns=args.columns)
    figure.savefig(args.out / "comparison.png", dpi=180, bbox_inches="tight")
    import matplotlib.pyplot as plt

    plt.close(figure)
    print(f"Saved {len(comparison.embeddings)}/{len(comparison.models)} models to {args.out}")
    for model, error in comparison.errors.items():
        print(f"  {model}: {error}")
    return int(bool(comparison.errors) and not args.allow_errors)


if __name__ == "__main__":
    raise SystemExit(main())
