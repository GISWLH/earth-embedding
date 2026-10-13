"""Resource discovery must stay complete, alias compatible and offline."""

import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest

from rs_embed.core.errors import ModelError
from rs_embed.embedders.catalog import MODEL_SPECS
from rs_embed.resources import get_model_resources, list_model_resources


def test_directory_covers_registered_adapters_and_existing_guides():
    entries = list_model_resources()
    assert len(entries) == len(MODEL_SPECS)
    assert {entry["model_id"] for entry in entries} == set(MODEL_SPECS)
    assert Counter(entry["category"] for entry in entries) == {
        "image": 16,
        "location": 3,
        "precomputed": 3,
    }
    docs = Path(__file__).resolve().parents[1] / "docs"
    directory = (docs / "model-resources.md").read_text(encoding="utf-8")
    for entry in entries:
        slug = entry["docs_url"].rstrip("/").rsplit("/", 1)[1]
        assert (docs / "models" / f"{slug}.md").is_file()
        assert f"[`{entry['model_id']}`]" in directory
        assert entry["source_url"] in directory
        assert entry["weights_url"] in directory


def test_alias_and_category_discovery_without_mutating_the_directory():
    esri = get_model_resources(" ESRI ")
    assert esri["model_id"] == "esri_gle"
    esri["weights_url"] = "changed locally"
    assert get_model_resources("esri")["weights_url"] != "changed locally"
    entries = list_model_resources(" LOCATION ")
    assert {entry["model_id"] for entry in entries} == {"satclip", "geoclip", "esri_gle"}
    entries[0]["model_id"] = "changed locally"
    assert list_model_resources("location")[0]["model_id"] == "satclip"


def test_bad_model_or_category_is_actionable():
    with pytest.raises(ModelError, match="Unknown model 'missing'.*Available models"):
        get_model_resources("missing")
    with pytest.raises(
        ValueError, match="Unknown category 'missing'.*image.*location.*precomputed"
    ):
        list_model_resources("missing")


def test_artifact_types_distinguish_checkpoints_from_data():
    checkpoint = get_model_resources("prithvi")
    assert checkpoint["weights_kind"] == "Hugging Face model"
    assert checkpoint["weights_url"].endswith("Prithvi-EO-2.0-100M-TL")
    dataset = get_model_resources("copernicus")
    assert dataset["weights_kind"] == "Hugging Face dataset"
    assert "/datasets/" in dataset["weights_url"]
    assert get_model_resources("alphaearth")["weights_kind"] == "official product"
    assert get_model_resources("esri")["weights_kind"] == "official download"


def test_discovery_does_not_load_inference_dependencies_or_open_network():
    # A fresh interpreter catches accidental eager imports even when other
    # tests in this process already imported an optional model dependency.
    script = """
import importlib.abc
import json
import socket
import sys

class RejectInferenceImports(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'torch', 'ee', 'huggingface_hub', 'terratorch', 'geoclip'}:
            raise AssertionError(f'Discovery imported inference dependency: {fullname}')

def reject_network(*args, **kwargs):
    raise AssertionError('Discovery attempted a network connection')

sys.meta_path.insert(0, RejectInferenceImports())
socket.create_connection = reject_network
socket.socket.connect = reject_network
from rs_embed.resources import get_model_resources, list_model_resources
print(json.dumps([get_model_resources('esri')['model_id'], len(list_model_resources())]))
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src")},
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == ["esri_gle", len(MODEL_SPECS)]
