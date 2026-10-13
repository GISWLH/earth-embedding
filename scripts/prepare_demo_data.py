"""Maintainer: package historical inputs and sample a tiny official AEF area.

python scripts/prepare_demo_data.py --labels labels.csv --features gse.npz --index aef_index.parquet
The input CSV/NPZ are the unmodified historical downstream_core_2x artifacts.
End users use the bundled checksummed data; no manuscript workspace is needed.
"""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from earth_embedding import BBox, find_aef_tiles, sample_aef
from earth_embedding.demo import align_samples


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(root, samples, features, meta):
    root.mkdir(parents=True, exist_ok=True)
    samples.to_csv(root / "samples.csv", index=False)
    np.savez_compressed(
        root / "features.npz", tile_id=samples.tile_id.to_numpy(dtype="U"), features=features
    )
    meta["files"] = {
        name: {"sha256": digest(root / name), "bytes": (root / name).stat().st_size}
        for name in ["samples.csv", "features.npz"]
    }
    meta["array_sha256"] = hashlib.sha256(features.tobytes()).hexdigest()
    (root / "manifest.json").write_text(json.dumps(meta, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--labels", type=Path, required=True)
    parser.add_argument("--features", type=Path, required=True)
    parser.add_argument("--index", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1] / "src/rs_embed/data/demos"
    labels = pd.read_csv(args.labels)
    labels = labels.drop(columns=[c for c in labels if c.startswith("jrc_")])
    with np.load(args.features, allow_pickle=False) as z:
        x = align_samples(labels, z["tile_id"], z["embeddings"])
    assert len(labels) == 567 and x.shape == (567, 64)
    save(
        root / "wuhan",
        labels,
        x,
        {
            "name": "Wuhan historical 567-tile software demo",
            "year": 2021,
            "scope": "Historical local diagnostics, not the current global manuscript benchmark",
            "license": "CC-BY-4.0 (AEF and WorldCover derived data)",
            "attribution": "The AlphaEarth Foundations Satellite Embedding dataset is produced by Google and Google DeepMind. Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium.",
            "sources": [
                "https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL",
                "https://doi.org/10.5281/zenodo.7254221",
            ],
            "source_artifacts": {
                "paper/experiments/results/downstream_core_2x/downstream_labels_500m_2x.csv": digest(
                    args.labels
                ),
                "paper/experiments/results/downstream_core_2x/embeddings_2x_tile/gse.npz": digest(
                    args.features
                ),
            },
            "selection": "All 567 centers in [114.35,30.48,114.47,30.56]; no quality or score selection",
            "features": "64 float32 channels, historical arithmetic mean of valid EE float pixels per tile; not GCS int8 and not renormalized",
            "labels": "Dominant grouped ESA WorldCover v200 (2021) class; vegetation combines trees, shrubland, grassland, wetland, mangroves, moss/lichen; built, cropland and water separate",
            "historical_split": "Original seed-42 stratified random train/val/test retained in split column; not used in this spatial demo",
            "geometry": "Original projected nominal-500m grid converted to WGS84 bounds; physical widths differ from 500m at this latitude",
        },
    )
    bbox = BBox(114.40, 30.51, 114.42, 30.53)
    tiles = find_aef_tiles(args.index, spatial=bbox, year=2021)
    nx = ny = 64
    lon = np.linspace(bbox.minlon, bbox.maxlon, nx + 1)
    lat = np.linspace(bbox.minlat, bbox.maxlat, ny + 1)
    rows = []
    for r in range(ny):
        for c in range(nx):
            rows.append(
                dict(
                    tile_id=f"aef_r{r:03d}_c{c:03d}",
                    row=r,
                    col=c,
                    center_lon=(lon[c] + lon[c + 1]) / 2,
                    center_lat=(lat[r] + lat[r + 1]) / 2,
                    minlon=lon[c],
                    minlat=lat[r],
                    maxlon=lon[c + 1],
                    maxlat=lat[r + 1],
                )
            )
    samples = pd.DataFrame(rows)
    x = sample_aef(samples[["center_lon", "center_lat"]].to_numpy(), tiles=tiles).data
    save(
        root / "aef",
        samples,
        x,
        {
            "name": "Wuhan 64x64 AEF point sample",
            "year": 2021,
            "tiles": tiles,
            "license": "CC-BY-4.0",
            "source": "https://developers.google.com/earth-engine/guides/aef_on_gcs_readme",
            "attribution": "The AlphaEarth Foundations Satellite Embedding dataset is produced by Google and Google DeepMind.",
            "selection": "Uniform 64x64 WGS84 cell centers in [114.40,30.51,114.42,30.53]; nearest native 10m COG pixel, not area means. Display cells approximately 30m apart.",
            "features": "64 float32 channels decoded sign(x)*(x/127.5)^2 from official signed int8 pixels; no interpolation",
            "index_sha256": digest(args.index),
            "access": "Anonymous HTTPS range reads; no EE credentials; entire COG and global index not bundled",
        },
    )
    print(
        json.dumps(
            {
                "tiles": tiles,
                "shape": list(x.shape),
                "bytes": sum(p.stat().st_size for p in root.rglob("*") if p.is_file()),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
