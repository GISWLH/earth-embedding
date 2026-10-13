"""Sample official AEF Cloud Optimized GeoTIFFs without Earth Engine.

Download the index once (see docs/data-access.md), then:
    python examples/aef_gcs.py --index /path/to/aef_index.csv
"""

import argparse

from earth_embedding import BBox, find_aef_tiles, sample_aef


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", required=True)
    parser.add_argument("--lon", type=float, default=114.41)
    parser.add_argument("--lat", type=float, default=30.52)
    parser.add_argument("--year", type=int, default=2021)
    args = parser.parse_args()
    eps = 0.00001
    tiles = find_aef_tiles(
        args.index,
        spatial=BBox(args.lon - eps, args.lat - eps, args.lon + eps, args.lat + eps),
        year=args.year,
    )
    embedding = sample_aef([[args.lon, args.lat]], tiles=tiles)
    print(embedding.data.shape)
    print(embedding.meta)


if __name__ == "__main__":
    main()
