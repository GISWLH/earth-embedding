from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from rs_embed import (
    OutputSpec,
    TemporalSpec,
    describe_model,
    get_embedding,
    get_embeddings_batch,
    list_models,
)
from rs_embed.core.specs import BBox, PointBuffer

ROOT = Path(__file__).resolve().parent
DEFAULT_DATA_DIR = ROOT.parent / "data" / "part2_20260502_full"
DEFAULT_OUT = ROOT / "results" / "all_models_smoke"

LOCAL_CLASSES = ["water", "vegetation", "cropland", "built"]
REGIONAL_CLASSES = ["water", "cropland", "forest_green", "built"]
REGION_B_MODELS = {"copernicus", "satvision", "tessera"}
YEAR_MODELS = {
    "copernicus": 2021,
    "gse": 2021,
    "tessera": 2024,
}
TESSERA_ANCHOR = {
    "anchor_id": "tessera_anchor_2024",
    "center_lon": 121.45,
    "center_lat": 31.15,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a two-region, all-model smoke extraction for the part-2 benchmark."
    )
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--models", nargs="+", default=list_models())
    parser.add_argument("--local-per-class", type=int, default=4)
    parser.add_argument("--regional-per-class", type=int, default=4)
    parser.add_argument("--local-min-dominance", type=float, default=0.6)
    parser.add_argument("--regional-min-dominance", type=float, default=0.5)
    parser.add_argument("--chunk-size", type=int, default=4)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--resume", action="store_true")
    return parser.parse_args()


def sample_balanced(
    df: pd.DataFrame,
    *,
    label_col: str,
    frac_col: str,
    classes: list[str],
    per_class: int,
    min_frac: float,
) -> pd.DataFrame:
    parts: list[pd.DataFrame] = []
    for label in classes:
        part = df[(df[label_col] == label) & (df[frac_col] >= min_frac)].copy()
        if part.empty:
            continue
        part = part.sort_values([frac_col], ascending=False).head(per_class)
        parts.append(part)
    if not parts:
        raise RuntimeError(f"No samples satisfied {label_col=} with threshold {min_frac}.")
    return pd.concat(parts, ignore_index=True)


def bbox_rows(df: pd.DataFrame) -> list[BBox]:
    return [
        BBox(
            minlon=float(row.minlon),
            minlat=float(row.minlat),
            maxlon=float(row.maxlon),
            maxlat=float(row.maxlat),
        )
        for row in df.itertuples()
    ]


def spatial_rows_for_model(model: str, df: pd.DataFrame) -> list[BBox | PointBuffer]:
    if model == "tessera":
        return [
            PointBuffer(
                lon=float(row.center_lon),
                lat=float(row.center_lat),
                buffer_m=6000,
            )
            for row in df.itertuples()
        ]
    return bbox_rows(df)


def chunked(seq: list[Any], size: int) -> list[Any]:
    for i in range(0, len(seq), size):
        yield seq[i : i + size]


def pooled_numpy(x: Any) -> np.ndarray:
    if hasattr(x, "values"):
        return np.asarray(x.values)
    return np.asarray(x)


def temporal_for_model(model: str) -> TemporalSpec:
    if model in YEAR_MODELS:
        return TemporalSpec.year(YEAR_MODELS[model])
    return TemporalSpec.range("2021-05-01", "2021-10-31")


def run_tessera_smoke(sample_df: pd.DataFrame) -> tuple[np.ndarray, dict[str, Any]]:
    row = sample_df.iloc[0]
    lon = float(row.center_lon)
    lat = float(row.center_lat)
    buffer_m = 6000.0
    m_per_deg_lat = 111_320.0
    dlat = buffer_m / m_per_deg_lat
    dlon = buffer_m / (m_per_deg_lat * max(1e-6, math.cos(math.radians(lat))))
    bounds = (lon - dlon, lat - dlat, lon + dlon, lat + dlat)
    t0 = time.perf_counter()
    registry_path = ROOT.parent.parent / "research_outputs" / "model_cache" / "geotessera_cache" / "registry.parquet"
    repr_root = ROOT.parent.parent / "global_0.1_degree_representation"
    registry = pd.read_parquet(registry_path, columns=["lat", "lon", "year"])
    tiles = registry[
        (registry["year"] == 2024)
        & (registry["lon"] >= bounds[0])
        & (registry["lon"] <= bounds[2])
        & (registry["lat"] >= bounds[1])
        & (registry["lat"] <= bounds[3])
    ][["lon", "lat"]].drop_duplicates()
    if tiles.empty:
        raise RuntimeError(f"tessera cache has no tiles for bounds={bounds}, year=2024")

    tile_vectors: list[np.ndarray] = []
    for tile in tiles.itertuples(index=False):
        grid_name = f"grid_{float(tile.lon):.2f}_{float(tile.lat):.2f}"
        emb_path = repr_root / "2024" / grid_name / f"{grid_name}.npy"
        scale_path = repr_root / "2024" / grid_name / f"{grid_name}_scales.npy"
        if not emb_path.exists() or not scale_path.exists():
            continue
        quantized = np.load(emb_path, mmap_mode="r")
        scales = np.load(scale_path, mmap_mode="r")
        if scales.ndim == 2 and quantized.ndim == 3:
            scales = scales[..., np.newaxis]
        hwc = quantized.astype(np.float32) * scales
        tile_vectors.append(hwc.mean(axis=(0, 1)).astype(np.float32))
    if not tile_vectors:
        raise RuntimeError("tessera fetch_embeddings returned no arrays after tile lookup")

    vec = np.stack(tile_vectors, axis=0).mean(axis=0, keepdims=True)
    elapsed_s = time.perf_counter() - t0
    meta = {
        "model": "tessera",
        "split": "region_b",
        "status": "ok",
        "type": "precomputed",
        "elapsed_s": round(elapsed_s, 3),
        "per_item_s": round(elapsed_s / len(sample_df), 3),
        "peak_gpu_mb": 0.0,
        "dim": int(vec.shape[1]),
        "n_items": int(len(sample_df)),
        "errors": [],
        "notes": ["direct geotessera cache pooling workaround"],
    }
    return vec, meta


def split_for_model(model: str) -> str:
    return "region_b" if model in REGION_B_MODELS else "region_a"


def id_col_for_model(model: str, split: str) -> str:
    if model == "tessera":
        return "anchor_id"
    return "cell_id" if split == "region_b" else "tile_id"


def sample_df_for_model(model: str, sample_df: pd.DataFrame) -> pd.DataFrame:
    if model != "tessera":
        return sample_df
    return pd.DataFrame([TESSERA_ANCHOR])


def run_model_embeddings(
    *,
    model: str,
    sample_df: pd.DataFrame,
    chunk_size: int,
    device: str,
) -> tuple[np.ndarray, dict[str, Any]]:
    if model == "tessera":
        return run_tessera_smoke(sample_df)

    import torch

    temporal = temporal_for_model(model)
    model_info = describe_model(model)
    model_type = str(model_info.get("type", "")).lower()
    spatials = spatial_rows_for_model(model, sample_df)
    embeddings: list[np.ndarray] = []
    errors: list[str] = []
    peak_gpu_mb = 0.0
    status = "ok"
    t0 = time.perf_counter()

    for spatial_chunk in chunked(spatials, chunk_size):
        try:
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.reset_peak_memory_stats()
            batch = get_embeddings_batch(
                model,
                spatials=spatial_chunk,
                temporal=temporal,
                output=OutputSpec.pooled(),
                backend="auto",
                device=device,
            )
            if torch.cuda.is_available():
                peak_gpu_mb = max(peak_gpu_mb, torch.cuda.max_memory_allocated() / (1024**2))
            embeddings.extend(pooled_numpy(emb.data).astype(np.float32).reshape(-1) for emb in batch)
        except Exception as exc:  # noqa: BLE001
            status = "partial"
            errors.append(f"batch fallback: {exc!r}")
            for spatial in spatial_chunk:
                try:
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()
                        torch.cuda.reset_peak_memory_stats()
                    emb = get_embedding(
                        model,
                        spatial=spatial,
                        temporal=temporal,
                        output=OutputSpec.pooled(),
                        backend="auto",
                        device=device,
                    )
                    if torch.cuda.is_available():
                        peak_gpu_mb = max(peak_gpu_mb, torch.cuda.max_memory_allocated() / (1024**2))
                    embeddings.append(pooled_numpy(emb.data).astype(np.float32).reshape(-1))
                except Exception as item_exc:  # noqa: BLE001
                    status = "failed"
                    errors.append(f"single fail: {item_exc!r}")
                    raise RuntimeError(
                        f"{model} failed during single-item fallback for {spatial}: {item_exc!r}"
                    ) from item_exc

    matrix = np.stack(embeddings, axis=0)
    elapsed_s = time.perf_counter() - t0
    meta = {
        "model": model,
        "split": split_for_model(model),
        "status": status,
        "type": model_type,
        "elapsed_s": round(elapsed_s, 3),
        "per_item_s": round(elapsed_s / len(sample_df), 3),
        "peak_gpu_mb": round(peak_gpu_mb, 2),
        "dim": int(matrix.shape[1]),
        "n_items": int(len(sample_df)),
        "errors": errors,
    }
    return matrix, meta


def load_existing_rows(out_dir: Path, skip_models: set[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for meta_path in sorted(out_dir.glob("embeddings_*.json")):
        model = meta_path.stem.removeprefix("embeddings_")
        if model in skip_models:
            continue
        meta = json.loads(meta_path.read_text())
        emb_path = out_dir / f"embeddings_{model}.npz"
        ids: list[str] = []
        if emb_path.exists():
            with np.load(emb_path, allow_pickle=True) as data:
                ids = [str(x) for x in data["ids"].tolist()]
        rows.append(
            {
                **meta,
                "sample_id_col": id_col_for_model(model, str(meta.get("split"))),
                "sample_ids": ids,
            }
        )
    return rows


def load_samples(args: argparse.Namespace) -> tuple[pd.DataFrame, pd.DataFrame]:
    local_df = pd.read_csv(args.data_dir / "region_a" / "tile_manifest_500m.csv")
    regional_df = pd.read_csv(args.data_dir / "region_b" / "cell_manifest_025deg.csv")
    local_samples = sample_balanced(
        local_df,
        label_col="local_dominant_class",
        frac_col="local_dominant_frac",
        classes=LOCAL_CLASSES,
        per_class=args.local_per_class,
        min_frac=args.local_min_dominance,
    ).sort_values("tile_id")
    regional_samples = sample_balanced(
        regional_df,
        label_col="regional_dominant_class",
        frac_col="regional_dominant_frac",
        classes=REGIONAL_CLASSES,
        per_class=args.regional_per_class,
        min_frac=args.regional_min_dominance,
    ).sort_values("cell_id")
    return local_samples.reset_index(drop=True), regional_samples.reset_index(drop=True)


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    local_samples, regional_samples = load_samples(args)
    local_samples.to_csv(args.out_dir / "region_a_samples.csv", index=False)
    regional_samples.to_csv(args.out_dir / "region_b_samples.csv", index=False)

    rows: list[dict[str, Any]] = []
    for model in args.models:
        split = split_for_model(model)
        base_sample_df = regional_samples if split == "region_b" else local_samples
        sample_df = sample_df_for_model(model, base_sample_df)
        id_col = id_col_for_model(model, split)
        emb_path = args.out_dir / f"embeddings_{model}.npz"
        meta_path = args.out_dir / f"embeddings_{model}.json"
        if args.resume and emb_path.exists() and meta_path.exists():
            matrix = np.load(emb_path)["embeddings"]
            meta = json.loads(meta_path.read_text())
            meta["errors"] = list(meta.get("errors", [])) + ["reused existing embeddings"]
        else:
            matrix, meta = run_model_embeddings(
                model=model,
                sample_df=sample_df,
                chunk_size=args.chunk_size,
                device=args.device,
            )
            np.savez_compressed(
                emb_path,
                ids=np.asarray(sample_df[id_col].tolist(), dtype=object),
                embeddings=matrix,
            )
            meta_path.write_text(json.dumps(meta, indent=2))
        row = {
            **meta,
            "sample_id_col": id_col,
            "sample_ids": sample_df[id_col].tolist(),
        }
        rows.append(row)
        print(
            f"[{model}] split={split} status={row['status']} "
            f"dim={row['dim']} time={row['elapsed_s']:.1f}s"
        )

    existing_rows = load_existing_rows(args.out_dir, skip_models=set(args.models))
    all_rows = existing_rows + rows
    result_df = pd.DataFrame(all_rows).sort_values(["split", "status", "elapsed_s", "model"])
    result_df.to_csv(args.out_dir / "smoke_summary.csv", index=False)
    (args.out_dir / "smoke_summary.json").write_text(result_df.to_json(orient="records", indent=2))

    lines = [
        "# Part-2 All-Model Smoke Extraction",
        "",
        f"- Data dir: `{args.data_dir}`",
        f"- Models: `{', '.join(args.models)}`",
        f"- Region A samples: `{len(local_samples)}`",
        f"- Region B samples: `{len(regional_samples)}`",
        "",
        "## Region A sample balance",
        "",
        local_samples["local_dominant_class"].value_counts().to_markdown(),
        "",
        "## Region B sample balance",
        "",
        regional_samples["regional_dominant_class"].value_counts().to_markdown(),
        "",
        "## Extraction summary",
        "",
        result_df.drop(columns=["sample_ids"]).to_markdown(index=False),
    ]
    (args.out_dir / "smoke_summary.md").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
