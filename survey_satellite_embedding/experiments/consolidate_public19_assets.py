from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "research_outputs" / "model_assets_public19"

HF_HUB = Path.home() / ".cache" / "huggingface" / "hub"
RS_EMBED_CACHE = Path.home() / ".cache" / "rs_embed"

MODEL_ASSETS: dict[str, dict[str, object]] = {
    "agrifm": {
        "type": "repo_checkpoint",
        "paths": [REPO_ROOT / "research_outputs" / "model_cache" / "AgriFM.pth"],
    },
    "anysat": {
        "type": "rs_embed_cache",
        "paths": [RS_EMBED_CACHE / "anysat"],
    },
    "copernicus": {
        "type": "precomputed_local_product",
        "paths": [REPO_ROOT / "data" / "copernicus_embed" / "embed_map_310k.tif"],
    },
    "dofa": {
        "type": "hf_snapshot",
        "paths": [HF_HUB / "models--earthflow--DOFA"],
    },
    "fomo": {
        "type": "rs_embed_cache",
        "paths": [RS_EMBED_CACHE / "fomo"],
    },
    "galileo": {
        "type": "rs_embed_cache",
        "paths": [RS_EMBED_CACHE / "galileo"],
    },
    "gse": {
        "type": "remote_product",
        "paths": [],
        "source": "Google Earth Engine: GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL",
    },
    "prithvi": {
        "type": "hf_snapshot",
        "paths": [HF_HUB / "models--ibm-nasa-geospatial--Prithvi-EO-2.0-100M-TL"],
    },
    "remoteclip": {
        "type": "hf_snapshot",
        "paths": [HF_HUB / "models--MVRL--remote-clip-vit-base-patch32"],
    },
    "satmae": {
        "type": "hf_snapshot",
        "paths": [HF_HUB / "models--MVRL--satmae-vitlarge-fmow-pretrain-800"],
    },
    "satmaepp": {
        "type": "hf_snapshot",
        "paths": [HF_HUB / "models--MVRL--satmaepp_ViT-L_pretrain_fmow_rgb"],
    },
    "satmaepp_s2_10b": {
        "type": "repo_checkpoint",
        "paths": [
            REPO_ROOT / "research_outputs" / "model_cache" / "checkpoint_ViT-L_pretrain_fmow_sentinel.pth"
        ],
    },
    "satvision": {
        "type": "hf_snapshot",
        "paths": [
            HF_HUB / "models--nasa-cisto-data-science-group--satvision-toa-giant-patch8-window8-128"
        ],
    },
    "scalemae": {
        "type": "hf_snapshot",
        "paths": [HF_HUB / "models--MVRL--scalemae-vitlarge-800"],
    },
    "terrafm": {
        "type": "hf_snapshot",
        "paths": [HF_HUB / "models--MBZUAI--TerraFM"],
    },
    "terramind": {
        "type": "hf_snapshot",
        "paths": [HF_HUB / "models--ibm-esa-geospatial--TerraMind-1.0-small"],
    },
    "tessera": {
        "type": "precomputed_local_product",
        "paths": [
            REPO_ROOT / "global_0.1_degree_representation",
            REPO_ROOT / "global_0.1_degree_tiff_all",
            REPO_ROOT / "research_outputs" / "model_cache" / "geotessera_cache",
        ],
    },
    "thor": {
        "type": "hf_snapshot",
        "paths": [HF_HUB / "models--FM4CS--THOR-1.0-base"],
    },
    "wildsat": {
        "type": "rs_embed_cache",
        "paths": [RS_EMBED_CACHE / "wildsat"],
    },
}


def latest_snapshot_dir(root: Path) -> Path | None:
    snapshots = root / "snapshots"
    if not snapshots.exists():
        return None
    candidates = sorted([p for p in snapshots.iterdir() if p.is_dir()])
    return candidates[-1] if candidates else None


def safe_unlink(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def make_symlink(target: Path, link_path: Path) -> None:
    if link_path.exists() or link_path.is_symlink():
        safe_unlink(link_path)
    os.symlink(target, link_path)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, object] = {
        "root": str(OUT_DIR),
        "notes": [
            "This folder consolidates local assets for the 19 canonical public models.",
            "Symlinks are used instead of copies to avoid duplicating large checkpoints.",
            "gse is a remote annual product and therefore has no local weight file to symlink.",
        ],
        "models": {},
    }

    for model, spec in sorted(MODEL_ASSETS.items()):
        model_dir = OUT_DIR / model
        model_dir.mkdir(parents=True, exist_ok=True)
        resolved_paths: list[str] = []
        link_names: list[str] = []
        for idx, raw_path in enumerate(spec.get("paths", [])):
            source = Path(raw_path)
            if not source.exists():
                continue
            target = latest_snapshot_dir(source) if spec["type"] == "hf_snapshot" else source
            if target is None or not target.exists():
                continue
            link_name = "snapshot" if spec["type"] == "hf_snapshot" else f"asset_{idx + 1}"
            if target.is_file():
                suffix = target.suffix
                link_name = f"{link_name}{suffix}"
            link_path = model_dir / link_name
            make_symlink(target, link_path)
            resolved_paths.append(str(target))
            link_names.append(str(link_path))

        manifest["models"][model] = {
            "asset_type": spec["type"],
            "resolved_paths": resolved_paths,
            "symlinks": link_names,
            "source": spec.get("source"),
        }

    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
