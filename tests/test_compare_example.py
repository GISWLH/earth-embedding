"""The runnable comparison example preserves partial failures and temporal contracts."""

import importlib.util
import json
from pathlib import Path

import numpy as np

from rs_embed.core.embedding import Embedding


def _example():
    path = Path(__file__).parents[1] / "examples" / "compare_models.py"
    spec = importlib.util.spec_from_file_location("compare_models_example", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cli_keeps_failed_models_and_uses_annual_product_dates(monkeypatch, tmp_path):
    import earth_embedding

    observed = {}

    def compare(models, **kwargs):
        observed.update(kwargs)
        return earth_embedding.EmbeddingComparison(
            models=tuple(models),
            embeddings={"esri_gle": Embedding(np.ones((3, 2, 2)), {"type": "location"})},
            errors={"gse": "ModelError: Earth Engine authentication required"},
        )

    monkeypatch.setattr(earth_embedding, "compare_embeddings", compare)
    status = _example().main(
        ["--models", "esri", "alphaearth", "--year", "2021", "--out", str(tmp_path)]
    )
    assert status == 1
    assert observed["model_options"]["esri_gle"]["temporal"] is None
    assert observed["model_options"]["gse"]["temporal"].year == 2021
    assert observed["temporal"].start == "2021-05-01"
    report = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    assert report["request"]["models"] == ["esri_gle", "gse"]
    assert set(report["errors"]) == {"gse"}
    assert not (tmp_path / "gse.npz").exists()
    with np.load(tmp_path / "esri_gle.npz", allow_pickle=False) as saved:
        assert saved["data"].shape == (3, 2, 2)
    assert (tmp_path / "comparison.png").stat().st_size > 0
