from __future__ import annotations

import argparse
import json
import math
import time
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import balanced_accuracy_score, f1_score, mean_absolute_error, root_mean_squared_error
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import ee

from rs_embed import (
    FetchSpec,
    OutputSpec,
    PointBuffer,
    TemporalSpec,
    describe_model,
    get_embedding,
    get_embeddings_batch,
)


ROOT = Path(__file__).resolve().parent
DEFAULT_OUT = ROOT / "results" / "wuhan_pilot_fast"
ROI_PATH = ROOT / "roi_wuhan_east_lake.geojson"

DEFAULT_MODELS = [
    "gse",
    "copernicus",
    "remoteclip",
    "satmaepp_s2_10b",
    "galileo",
    "agrifm",
]

COARSE6 = {
    "water": [80],
    "trees": [10],
    "cropland": [40],
    "built": [50],
    "bare_sparse": [60],
    "grass_shrub": [20, 30, 90, 95, 100],
}

COARSE3 = {
    "water": ["water"],
    "green": ["trees", "cropland", "grass_shrub"],
    "built": ["built", "bare_sparse"],
}

ON_THE_FLY_FETCH = FetchSpec(scale_m=10, cloudy_pct=30, composite="median")


@dataclass
class TileRecord:
    tile_id: str
    lon: float
    lat: float
    buffer_m: int
    frac_water: float
    frac_trees: float
    frac_cropland: float
    frac_built: float
    frac_bare_sparse: float
    frac_grass_shrub: float
    frac_green: float
    frac_built3: float
    frac_water3: float
    dominant_3class: str
    dominant_3frac: float
    jrc_water_fraction: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Wuhan East Lake satellite embedding pilot benchmark.")
    parser.add_argument("--roi", type=Path, default=ROI_PATH)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--models", nargs="+", default=DEFAULT_MODELS)
    parser.add_argument("--nx", type=int, default=10)
    parser.add_argument("--ny", type=int, default=10)
    parser.add_argument("--buffer-m", type=int, default=500)
    parser.add_argument("--dominance-threshold", type=float, default=0.50)
    parser.add_argument("--max-per-class", type=int, default=8)
    parser.add_argument("--chunk-size", type=int, default=4)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--label-cache", type=Path, default=None)
    parser.add_argument("--resume-embeddings", action="store_true")
    return parser.parse_args()


def load_roi_bounds(path: Path) -> tuple[float, float, float, float]:
    data = json.loads(path.read_text())
    coords = data["features"][0]["geometry"]["coordinates"][0]
    xs = [p[0] for p in coords]
    ys = [p[1] for p in coords]
    return min(xs), min(ys), max(xs), max(ys)


def iter_grid_centers(bounds: tuple[float, float, float, float], nx: int, ny: int):
    minx, miny, maxx, maxy = bounds
    lons = [minx + (i + 0.5) * (maxx - minx) / nx for i in range(nx)]
    lats = [miny + (j + 0.5) * (maxy - miny) / ny for j in range(ny)]
    for j, lat in enumerate(lats):
        for i, lon in enumerate(lons):
            yield i, j, lon, lat


def _hist_get(hist: dict[Any, Any], code: int) -> float:
    return float(hist.get(str(code), hist.get(code, 0.0)))


def build_label_table(args: argparse.Namespace) -> pd.DataFrame:
    cache_path = args.label_cache or (args.out_dir / "tiles_labels_all.csv")
    if cache_path.exists():
        return pd.read_csv(cache_path)

    ee.Initialize()
    worldcover = ee.ImageCollection("ESA/WorldCover/v200").first().select("Map")
    jrc_water = ee.Image("JRC/GSW1_4/GlobalSurfaceWater").select("occurrence").gt(50)
    bounds = load_roi_bounds(args.roi)
    rows: list[TileRecord] = []

    for i, j, lon, lat in iter_grid_centers(bounds, args.nx, args.ny):
        geom = ee.Geometry.Point([lon, lat]).buffer(args.buffer_m).bounds()
        hist = (
            worldcover.reduceRegion(
                reducer=ee.Reducer.frequencyHistogram(),
                geometry=geom,
                scale=10,
                maxPixels=1e8,
            )
            .get("Map")
            .getInfo()
            or {}
        )
        total = float(sum(hist.values()) or 1.0)
        fractions6 = {
            key: sum(_hist_get(hist, c) for c in codes) / total for key, codes in COARSE6.items()
        }
        frac_green = fractions6["trees"] + fractions6["cropland"] + fractions6["grass_shrub"]
        frac_built3 = fractions6["built"] + fractions6["bare_sparse"]
        fractions3 = {
            "water": fractions6["water"],
            "green": frac_green,
            "built": frac_built3,
        }
        dominant_3class = max(fractions3, key=fractions3.get)
        dominant_3frac = fractions3[dominant_3class]
        jrc_frac = (
            jrc_water.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=geom,
                scale=30,
                maxPixels=1e8,
            )
            .get("occurrence")
            .getInfo()
            or 0.0
        )
        rows.append(
            TileRecord(
                tile_id=f"tile_{j:02d}_{i:02d}",
                lon=lon,
                lat=lat,
                buffer_m=args.buffer_m,
                frac_water=fractions6["water"],
                frac_trees=fractions6["trees"],
                frac_cropland=fractions6["cropland"],
                frac_built=fractions6["built"],
                frac_bare_sparse=fractions6["bare_sparse"],
                frac_grass_shrub=fractions6["grass_shrub"],
                frac_green=frac_green,
                frac_built3=frac_built3,
                frac_water3=fractions3["water"],
                dominant_3class=dominant_3class,
                dominant_3frac=dominant_3frac,
                jrc_water_fraction=float(jrc_frac),
            )
        )

    df = pd.DataFrame(asdict(r) for r in rows).sort_values("tile_id").reset_index(drop=True)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(cache_path, index=False)
    return df


def select_balanced_tiles(df: pd.DataFrame, threshold: float, max_per_class: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    selected_parts = []
    for label in ["built", "green", "water"]:
        part = df[(df["dominant_3class"] == label) & (df["dominant_3frac"] >= threshold)].copy()
        if part.empty:
            continue
        order = rng.permutation(len(part))
        part = part.iloc[order].sort_values("dominant_3frac", ascending=False).head(max_per_class)
        selected_parts.append(part)
    if not selected_parts:
        raise RuntimeError("No tiles passed the dominance threshold.")
    return pd.concat(selected_parts, ignore_index=True).sort_values("tile_id").reset_index(drop=True)


def temporal_for_model(model: str) -> TemporalSpec:
    if model in {"gse", "copernicus"}:
        return TemporalSpec.year(2021)
    return TemporalSpec.range("2021-05-01", "2021-10-31")


def _as_numpy(x: Any) -> np.ndarray:
    if hasattr(x, "values"):
        return np.asarray(x.values)
    return np.asarray(x)


def chunked(seq: list[Any], n: int):
    for i in range(0, len(seq), n):
        yield seq[i : i + n]


def run_model_embeddings(
    model: str,
    tiles: pd.DataFrame,
    chunk_size: int,
    device: str,
) -> tuple[np.ndarray, dict[str, Any]]:
    import torch

    info = describe_model(model)
    model_type = str(info.get("type", "")).lower()
    spatial_specs = [
        PointBuffer(lon=float(row.lon), lat=float(row.lat), buffer_m=int(row.buffer_m))
        for row in tiles.itertuples()
    ]
    temporal = temporal_for_model(model)
    fetch = None if "precomputed" in model_type else ON_THE_FLY_FETCH

    embeddings: list[np.ndarray] = []
    status = "ok"
    errors: list[str] = []
    t0 = time.perf_counter()
    peak_gpu_mb = 0.0

    for spatial_chunk in chunked(spatial_specs, chunk_size):
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
                fetch=fetch,
            )
            if torch.cuda.is_available():
                peak_gpu_mb = max(
                    peak_gpu_mb,
                    torch.cuda.max_memory_allocated() / (1024**2),
                )
            embeddings.extend(_as_numpy(emb.data).astype(np.float32).reshape(-1) for emb in batch)
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
                        fetch=fetch,
                    )
                    if torch.cuda.is_available():
                        peak_gpu_mb = max(
                            peak_gpu_mb,
                            torch.cuda.max_memory_allocated() / (1024**2),
                        )
                    embeddings.append(_as_numpy(emb.data).astype(np.float32).reshape(-1))
                except Exception as item_exc:  # noqa: BLE001
                    status = "failed"
                    errors.append(f"single fail: {item_exc!r}")
                    raise RuntimeError(
                        f"{model} failed during single-item fallback for {spatial!r}: {item_exc!r}"
                    ) from item_exc

    elapsed = time.perf_counter() - t0
    matrix = np.stack(embeddings, axis=0)
    meta = {
        "model": model,
        "status": status,
        "elapsed_s": round(elapsed, 3),
        "per_tile_s": round(elapsed / len(tiles), 3),
        "peak_gpu_mb": round(peak_gpu_mb, 2),
        "dim": int(matrix.shape[1]),
        "errors": errors,
    }
    return matrix, meta


def evaluate_classification(X: np.ndarray, y: np.ndarray) -> dict[str, float]:
    if len(X) < 4:
        return {"cls_macro_f1": math.nan, "cls_balanced_acc": math.nan}
    min_class_count = min(Counter(y).values())
    if min_class_count < 2:
        return {"cls_macro_f1": math.nan, "cls_balanced_acc": math.nan}
    n_splits = max(2, min(3, int(min_class_count)))
    splitter = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    macro_f1: list[float] = []
    bal_acc: list[float] = []
    for train_idx, test_idx in splitter.split(X, y):
        clf = make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=4000, class_weight="balanced", solver="lbfgs"),
        )
        clf.fit(X[train_idx], y[train_idx])
        pred = clf.predict(X[test_idx])
        macro_f1.append(f1_score(y[test_idx], pred, average="macro"))
        bal_acc.append(balanced_accuracy_score(y[test_idx], pred))
    return {
        "cls_macro_f1": float(np.mean(macro_f1)),
        "cls_balanced_acc": float(np.mean(bal_acc)),
    }


def evaluate_regression(X: np.ndarray, y: np.ndarray) -> dict[str, float]:
    if len(X) < 4:
        return {"mae": math.nan, "rmse": math.nan, "spearman": math.nan}
    n_splits = max(2, min(3, int(len(y))))
    splitter = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    maes: list[float] = []
    rmses: list[float] = []
    spearmans: list[float] = []
    for train_idx, test_idx in splitter.split(X):
        reg = make_pipeline(StandardScaler(), Ridge(alpha=1.0))
        reg.fit(X[train_idx], y[train_idx])
        pred = reg.predict(X[test_idx])
        maes.append(mean_absolute_error(y[test_idx], pred))
        rmses.append(root_mean_squared_error(y[test_idx], pred))
        spearmans.append(float(spearmanr(y[test_idx], pred).statistic))
    return {
        "mae": float(np.mean(maes)),
        "rmse": float(np.mean(rmses)),
        "spearman": float(np.nanmean(spearmans)),
    }


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    label_df = build_label_table(args)
    selected_df = select_balanced_tiles(
        label_df,
        threshold=args.dominance_threshold,
        max_per_class=args.max_per_class,
        seed=args.seed,
    )
    label_df.to_csv(args.out_dir / "tiles_labels_all.csv", index=False)
    selected_df.to_csv(args.out_dir / "tiles_selected.csv", index=False)

    label_summary = {
        "all_tiles": int(len(label_df)),
        "selected_tiles": int(len(selected_df)),
        "dominant_3class_all": dict(Counter(label_df["dominant_3class"])),
        "dominant_3class_selected": dict(Counter(selected_df["dominant_3class"])),
        "dominance_threshold": args.dominance_threshold,
        "max_per_class": args.max_per_class,
    }
    (args.out_dir / "label_summary.json").write_text(json.dumps(label_summary, indent=2))

    y_cls = selected_df["dominant_3class"].to_numpy()
    y_built = selected_df["frac_built"].to_numpy(dtype=np.float32)
    y_green = selected_df["frac_green"].to_numpy(dtype=np.float32)
    y_water = selected_df["jrc_water_fraction"].to_numpy(dtype=np.float32)

    model_rows = []
    for model in args.models:
        try:
            emb_path = args.out_dir / f"embeddings_{model}.npz"
            if args.resume_embeddings and emb_path.exists():
                matrix = np.load(emb_path)["embeddings"]
                meta = {
                    "model": model,
                    "status": "ok",
                    "elapsed_s": 0.0,
                    "per_tile_s": 0.0,
                    "peak_gpu_mb": 0.0,
                    "dim": int(matrix.shape[1]),
                    "errors": ["reused existing embeddings"],
                }
            else:
                matrix, meta = run_model_embeddings(
                    model=model,
                    tiles=selected_df,
                    chunk_size=args.chunk_size,
                    device=args.device,
                )
                np.savez_compressed(emb_path, embeddings=matrix)

            valid_mask = np.all(np.isfinite(matrix), axis=1)
            matrix_eval = matrix[valid_mask]
            y_cls_eval = y_cls[valid_mask]
            y_built_eval = y_built[valid_mask]
            y_green_eval = y_green[valid_mask]
            y_water_eval = y_water[valid_mask]

            cls_metrics = evaluate_classification(matrix_eval, y_cls_eval)
            built_metrics = evaluate_regression(matrix_eval, y_built_eval)
            green_metrics = evaluate_regression(matrix_eval, y_green_eval)
            water_metrics = evaluate_regression(matrix_eval, y_water_eval)

            row = {
                **meta,
                "n_tiles_total": int(len(matrix)),
                "n_tiles_valid": int(valid_mask.sum()),
                **cls_metrics,
                "built_mae": built_metrics["mae"],
                "built_rmse": built_metrics["rmse"],
                "built_spearman": built_metrics["spearman"],
                "green_mae": green_metrics["mae"],
                "green_rmse": green_metrics["rmse"],
                "green_spearman": green_metrics["spearman"],
                "water_mae": water_metrics["mae"],
                "water_rmse": water_metrics["rmse"],
                "water_spearman": water_metrics["spearman"],
            }
            print(
                f"[{model}] dim={row['dim']} time={row['elapsed_s']:.1f}s "
                f"macro_f1={row['cls_macro_f1']:.3f} built_rmse={row['built_rmse']:.3f}"
            )
        except Exception as exc:  # noqa: BLE001
            row = {
                "model": model,
                "status": "failed",
                "elapsed_s": math.nan,
                "per_tile_s": math.nan,
                "peak_gpu_mb": math.nan,
                "dim": math.nan,
                "n_tiles_total": int(len(selected_df)),
                "n_tiles_valid": 0,
                "errors": [repr(exc)],
                "cls_macro_f1": math.nan,
                "cls_balanced_acc": math.nan,
                "built_mae": math.nan,
                "built_rmse": math.nan,
                "built_spearman": math.nan,
                "green_mae": math.nan,
                "green_rmse": math.nan,
                "green_spearman": math.nan,
                "water_mae": math.nan,
                "water_rmse": math.nan,
                "water_spearman": math.nan,
            }
            print(f"[{model}] failed: {exc!r}")
        model_rows.append(row)

    result_df = pd.DataFrame(model_rows).sort_values(
        ["cls_macro_f1", "built_rmse"],
        ascending=[False, True],
    )
    result_df.to_csv(args.out_dir / "benchmark_results.csv", index=False)
    (args.out_dir / "benchmark_results.json").write_text(
        result_df.to_json(orient="records", indent=2)
    )

    lines = [
        "# Wuhan Pilot Benchmark",
        "",
        f"- ROI: `{args.roi.name}`",
        f"- Grid: `{args.nx} x {args.ny}` candidates with `{args.buffer_m} m` square buffers",
        f"- Selected tiles: `{len(selected_df)}`",
        f"- Selected class balance: `{dict(Counter(selected_df['dominant_3class']))}`",
        f"- Models: `{', '.join(args.models)}`",
        "",
        result_df.to_markdown(index=False),
    ]
    (args.out_dir / "benchmark_results.md").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
