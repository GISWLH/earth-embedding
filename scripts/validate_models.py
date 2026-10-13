#!/usr/bin/env python3
"""Bounded, honest pretrained-inference smoke checks; never a scientific benchmark.

Run from a source checkout or an installed environment:
    python scripts/validate_models.py --model satmae --model satclip --timeout 180

Image models receive deterministic synthetic raw sensor values in their declared
band order. Multitemporal models receive independently generated TCHW frames.
One subprocess per model isolates runtime imports and releases model memory.
Cached Hugging Face assets are used by default; --allow-network permits downloads.
Precomputed products require --include-products and use a real geographic query.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import inspect
import json
import os
import platform
import subprocess
import sys
import time
import traceback
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
PRODUCTS = {"gse", "copernicus", "tessera"}
LOCATIONS = {"satclip", "geoclip", "esri_gle"}
MULTITEMPORAL = {"anysat", "galileo", "agrifm"}
MARKER = "EARTH_EMBEDDING_RECEIPT="


def clean(value):
    """Serialize useful metadata without leaking home paths or credential fields."""
    if isinstance(value, dict):
        return {
            str(k): clean(v)
            for k, v in value.items()
            if not any(t in str(k).lower() for t in ("password", "secret", "authorization"))
        }
    if isinstance(value, (tuple, list)):
        return [clean(v) for v in value]
    if isinstance(value, str):
        return value.replace(str(Path.home()), "~").replace(str(ROOT), "<repository>")
    if value is None or isinstance(value, (bool, int, float)):
        return value
    return clean(str(value))


def classify_error(exc: Exception) -> str:
    messages = []
    current = exc
    while current is not None:
        messages.append(str(current).lower())
        current = current.__cause__
    message = " ".join(messages)
    blocked_terms = (
        "no module named",
        "install:",
        "install ",
        "not installed",
        "not found",
        "localentrynotfound",
        "offline mode",
        "couldn't connect",
        "connection error",
        "connectionerror",
        "connection refused",
        "network is unreachable",
        "401",
        "403",
        "authentication",
        "authenticate",
        "credentials",
        "project is required",
        "cannot access gated",
        "not in the cached",
        "could not locate",
        "out of memory",
        "libcud",
        "undefined symbol",
        "flash_attn",
        "no tessera tiles",
    )
    return (
        "blocked"
        if isinstance(exc, (ImportError, FileNotFoundError))
        or any(term in message for term in blocked_terms)
        else "fail"
    )


def child(args) -> int:
    start = time.perf_counter()
    receipt = {
        "model": args.child,
        "status": "fail",
        "device": args.device,
        "threads": args.threads,
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "scope": "product_access" if args.child in PRODUCTS else "pretrained_inference",
        "huggingface_downloads_allowed": args.allow_network,
    }
    try:
        import numpy as np

        from rs_embed.core.registry import get_embedder_cls
        from rs_embed.core.specs import BBox, OutputSpec, PointBuffer, TemporalSpec
        from rs_embed.tools.model_defaults import default_sensor_for_model

        if args.child in PRODUCTS and not args.include_products:
            receipt.update(
                status="blocked",
                reason="Real product access not requested; synthetic pixels cannot validate precomputed products.",
            )
        else:
            import torch

            torch.set_num_threads(args.threads)
            torch.set_num_interop_threads(1)
            torch.manual_seed(args.seed)
            model = get_embedder_cls(args.child)()
            receipt["adapter_sha256"] = hashlib.sha256(
                Path(inspect.getfile(type(model))).read_bytes()
            ).hexdigest()
            sensor = default_sensor_for_model(args.child)
            desc = model.describe()
            receipt["model_descriptor"] = clean(desc)
            receipt["environment"] = {
                "python": platform.python_version(),
                "torch": torch.__version__,
            }
            for dependency in (
                "numpy",
                "transformers",
                "timm",
                "huggingface-hub",
                "terratorch",
                "torchvision",
            ):
                try:
                    receipt["environment"][dependency] = importlib.metadata.version(dependency)
                except importlib.metadata.PackageNotFoundError:
                    pass
            kwargs = dict(
                spatial=PointBuffer(lon=args.lon, lat=args.lat, buffer_m=320),
                temporal=TemporalSpec.range("2021-01-01", "2022-01-01"),
                sensor=sensor,
                output=OutputSpec.pooled(),
                backend="auto",
                device=args.device,
            )
            if args.child not in PRODUCTS | LOCATIONS:
                channels = len(sensor.bands) if sensor else 3
                shape = (channels, 64, 64)
                if args.child in MULTITEMPORAL:
                    frames = int(
                        os.environ.get(
                            f"RS_EMBED_{args.child.upper()}_FRAMES",
                            getattr(model, "DEFAULT_FRAMES", 8),
                        )
                    )
                    shape = (frames, *shape)
                pixels = (
                    np.random.default_rng(args.seed)
                    .uniform(500, 4500, size=shape)
                    .astype(np.float32)
                )
                kwargs["input_chw"] = pixels
                receipt["input"] = {
                    "kind": "synthetic_raw_sensor_values",
                    "seed": args.seed,
                    "shape": list(shape),
                    "bands": list(sensor.bands) if sensor else None,
                    "range": [500, 4500],
                    "sha256": hashlib.sha256(pixels.tobytes()).hexdigest(),
                    "independent_temporal_frames": args.child in MULTITEMPORAL,
                }
            elif args.child in PRODUCTS:
                kwargs["temporal"] = TemporalSpec.year(2021)
                receipt["input"] = {
                    "kind": "real_product_query",
                    "lon": args.lon,
                    "lat": args.lat,
                    "year": 2021,
                }
                if args.child == "copernicus":
                    # This product's native grid is 0.25 degrees, so a 640 m ROI
                    # cannot select a valid pixel under its explicit ROI contract.
                    kwargs["spatial"] = BBox(
                        args.lon - 0.25, args.lat - 0.25, args.lon + 0.25, args.lat + 0.25
                    )
                    receipt["input"]["bbox_lonlat"] = [
                        args.lon - 0.25,
                        args.lat - 0.25,
                        args.lon + 0.25,
                        args.lat + 0.25,
                    ]
            else:
                receipt["input"] = {"kind": "coordinates", "lon": args.lon, "lat": args.lat}
            inference_start = time.perf_counter()
            if args.child not in PRODUCTS | LOCATIONS:
                from rs_embed.image import get_image_embedding

                pixels = kwargs.pop("input_chw")
                kwargs.pop("backend")
                embedding = get_image_embedding(args.child, pixels, **kwargs)
                receipt["entrypoint"] = "get_image_embedding"
            else:
                embedding = model.get_embedding(**kwargs)
                receipt["entrypoint"] = "Embedder.get_embedding"
            receipt["load_and_forward_seconds"] = round(time.perf_counter() - inference_start, 3)
            values = np.asarray(embedding.data)
            if values.ndim != 1 or values.size == 0 or not np.isfinite(values).all():
                raise ValueError(
                    f"Expected a nonempty finite pooled vector, got shape={values.shape}"
                )
            if float(np.linalg.norm(values)) == 0:
                raise ValueError("Output is an all-zero vector")
            receipt.update(
                status="pass",
                output={
                    "shape": list(values.shape),
                    "dtype": str(values.dtype),
                    "finite": True,
                    "l2_norm": float(np.linalg.norm(values)),
                    "std": float(np.std(values)),
                    "sha256": hashlib.sha256(values.tobytes()).hexdigest(),
                },
                embedding_metadata=clean(embedding.meta),
            )
    except Exception as exc:
        receipt.update(
            status=classify_error(exc),
            error_type=type(exc).__name__,
            reason=clean(str(exc)),
            traceback=clean(traceback.format_exc()),
        )
    receipt["total_seconds"] = round(time.perf_counter() - start, 3)
    print(MARKER + json.dumps(clean(receipt), ensure_ascii=False), flush=True)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model", action="append", help="Repeat to select canonical IDs; default: all"
    )
    parser.add_argument("--output", type=Path, default=ROOT / "docs/validation/model-smoke.json")
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--seed", type=int, default=20261013)
    parser.add_argument("--lon", type=float, default=114.35)
    parser.add_argument("--lat", type=float, default=30.50)
    parser.add_argument("--allow-network", action="store_true")
    parser.add_argument("--include-products", action="store_true")
    parser.add_argument("--child", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.threads < 1 or args.timeout <= 0:
        parser.error("threads and timeout must be positive")
    if args.child:
        return child(args)
    from rs_embed.embedders.catalog import MODEL_SPECS, canonical_model_id

    models = [canonical_model_id(m) for m in (args.model or MODEL_SPECS)]
    unknown = sorted(set(models) - MODEL_SPECS.keys())
    if unknown:
        parser.error(f"Unknown canonical models: {unknown}")
    env = os.environ.copy()
    env.update(
        OMP_NUM_THREADS=str(args.threads),
        MKL_NUM_THREADS=str(args.threads),
        OPENBLAS_NUM_THREADS=str(args.threads),
        TOKENIZERS_PARALLELISM="false",
        PYTHONUNBUFFERED="1",
        PYTHONPATH=str(ROOT / "src") + os.pathsep + env.get("PYTHONPATH", ""),
    )
    if args.device == "cpu":
        env["CUDA_VISIBLE_DEVICES"] = ""
    if not args.allow_network:
        env.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    log_dir = args.output.parent / (args.output.stem + "-logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "schema_version": 1,
        "scope": "synthetic smoke checks, not benchmark evidence",
        "created_utc": datetime.now(UTC).isoformat(),
        "timeout_seconds": args.timeout,
        "huggingface_downloads_allowed": args.allow_network,
        "product_access_requested": args.include_products,
        "results": [],
    }
    report["validation_script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    report["explicit_model_environment"] = clean(
        {k: v for k, v in env.items() if k.startswith("RS_EMBED_")}
    )
    for model_id in models:
        command = [
            sys.executable,
            str(Path(__file__).resolve()),
            "--child",
            model_id,
            "--threads",
            str(args.threads),
            "--device",
            args.device,
            "--seed",
            str(args.seed),
            "--lon",
            str(args.lon),
            "--lat",
            str(args.lat),
        ]
        if args.allow_network:
            command.append("--allow-network")
        if args.include_products:
            command.append("--include-products")
        print(f"Running {model_id} (timeout {args.timeout:g}s)...", flush=True)
        start = time.perf_counter()
        try:
            proc = subprocess.run(
                command,
                env=env,
                capture_output=True,
                text=True,
                errors="replace",
                timeout=args.timeout,
                cwd=ROOT,
            )
            records = [
                line[len(MARKER) :] for line in proc.stdout.splitlines() if line.startswith(MARKER)
            ]
            if records:
                result = json.loads(records[-1])
            else:
                result = {
                    "model": model_id,
                    "status": "fail",
                    "reason": "Child exited without a receipt",
                    "returncode": proc.returncode,
                    "total_seconds": round(time.perf_counter() - start, 3),
                }
            logs = proc.stdout + "\nSTDERR:\n" + proc.stderr
        except subprocess.TimeoutExpired as exc:
            result = {
                "model": model_id,
                "status": "blocked",
                "reason": f"Exceeded bounded {args.timeout:g}s CPU/runtime budget",
                "total_seconds": args.timeout,
            }

            def decode(value):
                return value.decode(errors="replace") if isinstance(value, bytes) else value or ""

            logs = decode(exc.stdout) + "\nSTDERR:\n" + decode(exc.stderr)
        result["log"] = str((log_dir / f"{model_id}.log").relative_to(args.output.parent))
        (log_dir / f"{model_id}.log").write_text(clean(logs), encoding="utf-8")
        report["results"].append(result)
        report["counts"] = {
            status: sum(r["status"] == status for r in report["results"])
            for status in ("pass", "blocked", "fail")
        }
        args.output.write_text(
            json.dumps(clean(report), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(
            f"  {result['status']}: {result.get('output', {}).get('shape', result.get('reason', ''))}",
            flush=True,
        )
    print(json.dumps(report["counts"]), flush=True)
    return int(report["counts"]["fail"] > 0)


if __name__ == "__main__":
    raise SystemExit(main())
