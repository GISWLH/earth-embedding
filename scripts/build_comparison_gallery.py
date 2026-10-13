"""Build the documented gallery from genuine cached grids and location inference.

The optional archive is the historical Wuhan four-block diagnostic cache, not a
benchmark shipped with this package. No image encoder is rerun by this script.
Without --archive, the coordinate-only figure is fully reproducible from public
weights and needs neither imagery nor Google Earth Engine.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.metadata
import json
import platform
import time
from datetime import UTC, datetime
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")

from earth_embedding import (  # noqa: E402
    get_location_embeddings,
    plot_embedding_comparison,
)
from rs_embed.core.embedding import Embedding  # noqa: E402

WUHAN_BBOX = [114.35, 30.48, 114.47, 30.56]
GLOBAL_BBOX = [-180.0, -80.0, 180.0, 80.0]
LOCATION_MODELS = ("satclip", "geoclip", "esri_gle")
IMAGE_MODELS = (
    "remoteclip",
    "satmae",
    "satmaepp",
    "scalemae",
    "wildsat",
    "satmaepp_s2_10b",
    "prithvi",
    "terrafm",
    "terramind",
    "satvision",
    "dofa",
    "fomo",
    "thor",
    "galileo",
    "anysat",
    "agrifm",
)
PRODUCT_MODELS = ("gse", "tessera", "copernicus")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def array_hash(data: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(data).tobytes()).hexdigest()


def public_metadata(value):
    """Retain provenance while omitting machine-specific home directories."""
    if isinstance(value, dict):
        return {key: public_metadata(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [public_metadata(item) for item in value]
    if isinstance(value, Path):
        value = str(value)
    if isinstance(value, str) and value.startswith(("/home/", "/tmp/")):
        return Path(value).name
    return value


def sample_coordinates(bbox, height: int, width: int) -> np.ndarray:
    west, south, east, north = bbox
    lons = west + (np.arange(width) + 0.5) * (east - west) / width
    lats = north - (np.arange(height) + 0.5) * (north - south) / height
    lon, lat = np.meshgrid(lons, lats)
    return np.column_stack([lon.ravel(), lat.ravel()])


def location_grids(device: str, cache_dir: Path):
    """Evaluate exactly the same WGS84 cell centers for all three encoders."""
    grids, records = {}, []
    cache_dir.mkdir(parents=True, exist_ok=True)
    for area, bbox, height, width in (
        ("global", GLOBAL_BBOX, 80, 180),
        ("wuhan", WUHAN_BBOX, 48, 64),
    ):
        points = sample_coordinates(bbox, height, width)
        for model in LOCATION_MODELS:
            start = time.perf_counter()
            key = f"{model}_{area}"
            cache = cache_dir / f"{key}.npz"
            receipt = cache_dir / f"{key}.json"
            if cache.exists() and receipt.exists():
                record = json.loads(receipt.read_text())
                if record["coordinate_sha256"] != array_hash(points):
                    raise ValueError(f"Coordinate mismatch in {cache}")
                with np.load(cache, allow_pickle=False) as loaded:
                    features = loaded["embedding"]
                if record["embedding_sha256"] != array_hash(features):
                    raise ValueError(f"Embedding hash mismatch in {cache}")
                metadata = record["metadata"]
                record["reused_run_cache"] = True
            else:
                result = get_location_embeddings(model, points, device=device, batch_size=1024)
                features, metadata = result.data, result.meta
                checkpoint = metadata.get("checkpoint", {}).get("path")
                if (
                    model == "geoclip"
                    and metadata.get("checkpoint", {}).get("source") == "geoclip_package"
                ):
                    import geoclip

                    checkpoint = (
                        Path(geoclip.__file__).parent / "model/weights/location_encoder_weights.pth"
                    )
                checkpoint_hash = sha256(Path(checkpoint)) if checkpoint else None
                record = {
                    "model": model,
                    "area": area,
                    "source": "actual_coordinate_encoder_inference",
                    "run_utc": datetime.now(UTC).isoformat(),
                    "elapsed_seconds": round(time.perf_counter() - start, 3),
                    "bbox_4326": bbox,
                    "query_grid_hw": [height, width],
                    "coordinate_order": "longitude_latitude",
                    "coordinate_dtype": str(points.dtype),
                    "coordinate_sha256": array_hash(points),
                    "embedding_shape": list(features.shape),
                    "embedding_dtype": str(features.dtype),
                    "embedding_sha256": array_hash(features),
                    "checkpoint_sha256": checkpoint_hash,
                    "metadata": public_metadata(metadata),
                    "reused_run_cache": False,
                }
                np.savez_compressed(cache, embedding=features, lonlat=points)
                receipt.write_text(json.dumps(record, indent=2) + "\n")
            data = features.reshape(height, width, -1).transpose(2, 0, 1)
            grids[key] = Embedding(
                data=data,
                meta={
                    **metadata,
                    "type": "location",
                    "bbox_4326": bbox,
                    "grid_semantics": "coordinate_queries_not_image_pixels",
                    "y_axis_direction": "north_to_south",
                },
            )
            records.append(record)
            print(f"{key}: {features.shape}; {record['elapsed_seconds']:.2f}s", flush=True)
    return grids, records


def archive_grid(archive: Path, model: str):
    """Mosaic four genuine blocks, retaining their samples and edge padding.

    Rows in the historical cache increase northward. Within each block the
    stored sample orientation is retained, matching its original diagnostic.
    Unequal edge sizes are padded with NaN, never interpolated or duplicated.
    """
    blocks = []
    for row in (1, 2):
        for col in (1, 2):
            name = f"block_r{row:02d}_c{col:02d}"
            source = archive / "blocks_2x" / model / f"{name}.npz"
            metadata_path = source.with_suffix(".json")
            metadata = json.loads(metadata_path.read_text())
            with np.load(source, allow_pickle=False) as loaded:
                data = loaded["embedding"]
                bbox = loaded["bbox"].tolist()
            blocks.append(
                (
                    row,
                    col,
                    data,
                    {
                        "file": str(source.relative_to(archive)).replace("\\", "/"),
                        "sha256": sha256(source),
                        "metadata_file": str(metadata_path.relative_to(archive)).replace("\\", "/"),
                        "metadata_sha256": sha256(metadata_path),
                        "shape": list(data.shape),
                        "dtype": str(data.dtype),
                        "bbox_4326": bbox,
                        "run_metadata": public_metadata(metadata.get("meta", {})),
                    },
                )
            )
    if model == "copernicus":
        # These queries used 15 km buffers on a 0.25-degree product. Their
        # returned samples overlap, so retain one complete expanded query.
        data, record = blocks[0][2:]
        effective_bbox = ast.literal_eval(record["run_metadata"]["bbox_4326"])
        returned = np.concatenate([item[2].reshape(item[2].shape[0], -1).T for item in blocks])
        return Embedding(
            data=data,
            meta={
                "model": model,
                "type": "precomputed",
                "bbox_4326": effective_bbox,
                "source": "historical_wuhan_expanded_product_query",
                "display_note": "One 15 km buffered query; 0.25-degree product cells",
            },
        ), {
            "model": model,
            "source": "historical_wuhan_expanded_product_query",
            "output_shape": list(data.shape),
            "output_dtype": str(data.dtype),
            "effective_bbox_4326": list(effective_bbox),
            "mosaic_policy": "not mosaicked: expanded adjacent queries overlap",
            "overlap_diagnostic": {
                "returned_vectors": len(returned),
                "distinct_vectors": len(np.unique(returned, axis=0)),
            },
            "blocks": [record],
        }
    heights = {row: max(data.shape[1] for r, _, data, _ in blocks if r == row) for row in (1, 2)}
    widths = {col: max(data.shape[2] for _, c, data, _ in blocks if c == col) for col in (1, 2)}
    dim = blocks[0][2].shape[0]
    # Retain source precision; all 18 current mosaics use float16 caches.
    dtype = np.result_type(*[data.dtype for _, _, data, _ in blocks])
    mosaic = np.full((dim, sum(heights.values()), sum(widths.values())), np.nan, dtype=dtype)
    for row, col, data, _ in blocks:
        if data.shape[0] != dim:
            raise ValueError(f"Inconsistent dimensions in {model} blocks")
        top = 0 if row == 2 else heights[2]
        left = 0 if col == 1 else widths[1]
        mosaic[:, top : top + data.shape[1], left : left + data.shape[2]] = data
    return Embedding(
        data=mosaic,
        meta={
            "model": model,
            "type": "precomputed" if model in PRODUCT_MODELS else "on_the_fly",
            "bbox_4326": WUHAN_BBOX,
            "source": "historical_wuhan_four_block_diagnostic",
            "display_note": "native cached samples; NaN padding at uneven block edges",
        },
    ), {
        "model": model,
        "source": "historical_wuhan_four_block_diagnostic",
        "output_shape": list(mosaic.shape),
        "output_dtype": str(mosaic.dtype),
        "mosaic_policy": "north rows first; preserve native samples; NaN edge padding",
        "blocks": [record for _, _, _, record in blocks],
    }


def build(args):
    import matplotlib.image as mpimg
    import matplotlib.pyplot as plt
    import torch

    torch.set_num_threads(args.threads)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    location, location_records = location_grids(args.device, args.cache_dir)
    panels = {
        f"{model} / {area}": location[f"{model}_{area}"]
        for area in ("global", "wuhan")
        for model in LOCATION_MODELS
    }
    location_png = args.output_dir / "location-encoders.png"
    figure = plot_embedding_comparison(
        panels,
        columns=3,
        title="Three location encoders, two spatial scales\n"
        "Global: 180 x 80 queries, 80 S to 80 N | Wuhan: 64 x 48 queries",
        save_path=location_png,
        dpi=160,
    )
    plt.close(figure)
    provenance = {
        "schema": "earth-embedding-comparison-gallery-v1",
        "created_utc": datetime.now(UTC).isoformat(),
        "purpose": "qualitative_library_demonstration_not_new_benchmark",
        "script_sha256": sha256(Path(__file__)),
        "environment": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "numpy": np.__version__,
            "matplotlib": matplotlib.__version__,
            "geoclip": importlib.metadata.version("geoclip"),
            "device": args.device,
        },
        "visualization": {
            "function": "earth_embedding.plot_embedding_comparison",
            "pca": "independent per panel; first 3 PCs; 2048 deterministic fit samples maximum",
            "stretch": "2nd to 98th percentile, per component and panel",
            "interpolation": "nearest (no feature grid resampling)",
            "caveats": [
                "Colors cannot be compared numerically between models or scales.",
                "Coordinate sampling density is not learned spatial resolution.",
                "Different encoders, products, sensors and dates have different support.",
                "Historical Wuhan grids are supplementary diagnostics, not a new evaluation.",
            ],
        },
        "location_runs": location_records,
        "images": {"location-encoders.png": sha256(location_png)},
    }
    if args.archive is not None:
        archived, records = {}, []
        for model in IMAGE_MODELS + PRODUCT_MODELS:
            archived[model], record = archive_grid(args.archive, model)
            records.append(record)
            print(f"cached {model}: {archived[model].data.shape}", flush=True)
        archived.update({model: location[f"{model}_wuhan"] for model in LOCATION_MODELS})
        reference = args.archive / "original_region_a_block_r01_c01_2x.png"
        # The archived PNG is a Matplotlib panel with a white margin and black
        # title. Retain its colored raster bounds, excluding that duplicate title.
        reference_rgb = mpimg.imread(reference)
        colored = np.ptp(reference_rgb[..., :3], axis=-1) > 0.02
        ys, xs = np.nonzero(colored)
        crop = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
        reference_rgb = reference_rgb[crop[1] : crop[3], crop[0] : crop[2]]
        figure = plot_embedding_comparison(
            archived,
            columns=5,
            reference=reference_rgb,
            reference_title="Sentinel-2 reference\nWuhan | May-Oct 2021",
            title="22 models in the Wuhan region\n16 image encoders + 3 products + 3 location encoders",
            dpi=170,
        )
        for index, model in enumerate(archived):
            ax = figure.axes[index + 1]
            if model == "copernicus":
                ax.set_title("copernicus | 768-D\n3 x 2 expanded product window", fontsize=10)
                ax.texts[0].set_text("0.25-degree cells; larger buffered support")
            elif model == "satvision":
                ax.texts[0].set_text("historical MODIS proxy input / 2021")
            elif model == "tessera":
                ax.texts[0].set_text("precomputed product / 2024")
            elif model == "gse":
                ax.texts[0].set_text("precomputed product / 2021")
            elif model in IMAGE_MODELS:
                ax.texts[0].set_text("image encoder / 2021 imagery")
        figure.text(
            0.5,
            0.951,
            "Historical image/product outputs + newly sampled coordinates; support and dates differ.",
            ha="center",
            fontsize=10,
            color="#526071",
        )
        figure.savefig(args.output_dir / "all-models.png", dpi=170, bbox_inches="tight")
        plt.close(figure)
        provenance.update(
            {
                "historical_archive_name": args.archive.name,
                "historical_manifest_sha256": sha256(args.archive / "manifest_2x.json"),
                "historical_reference_sha256": sha256(reference),
                "historical_reference_crop_ltrb_pixels": crop,
                "wuhan_bbox_4326": WUHAN_BBOX,
                "historical_models": records,
            }
        )
        provenance["images"]["all-models.png"] = sha256(args.output_dir / "all-models.png")
    (args.output_dir / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, help="Historical part2_model_map_figure cache")
    parser.add_argument("--output-dir", type=Path, default=Path("docs/assets/comparison"))
    parser.add_argument("--cache-dir", type=Path, default=Path("work/gallery-cache"))
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--threads", type=int, default=4)
    build(parser.parse_args())
