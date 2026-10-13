"""Coordinate-only embeddings; run with --model geoclip, satclip, or esri_gle.

Requires the selected model's optional runtime and weights. No Earth Engine,
imagery or timestamp is required. Use --device cpu for a small CPU smoke run.
"""

import argparse

from earth_embedding import get_location_embeddings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", choices=["satclip", "geoclip", "esri_gle"], default="geoclip")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--batch-size", type=int, default=32)
    args = parser.parse_args()
    result = get_location_embeddings(
        args.model,
        [[114.3055, 30.5928], [139.6917, 35.6895], [-74.0060, 40.7128]],
        device=args.device,
        batch_size=args.batch_size,
    )
    print(f"{result.meta['model']}: {result.data.shape}, {result.data.dtype}")
    print(result.meta)


if __name__ == "__main__":
    main()
