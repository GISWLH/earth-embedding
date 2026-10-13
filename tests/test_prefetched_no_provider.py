"""Supplied pixels must never initialize an imagery provider or authenticate."""

import importlib

import numpy as np
import pytest

from rs_embed.core.errors import ModelError
from rs_embed.core.specs import OutputSpec, PointBuffer, TemporalSpec
from rs_embed.embedders.catalog import MODEL_SPECS


@pytest.mark.parametrize("model_id", ["remoteclip", "prithvi", "dofa", "terramind", "terrafm"])
def test_bad_local_pixels_are_rejected_without_initializing_provider(monkeypatch, model_id):
    module_name, class_name = MODEL_SPECS[model_id]
    module = importlib.import_module("rs_embed.embedders." + module_name)
    embedder = getattr(module, class_name)()

    def unexpected_provider(_backend):
        pytest.fail("Local pixels unexpectedly initialized an imagery provider")

    monkeypatch.setattr(embedder, "_get_provider", unexpected_provider)
    if model_id == "prithvi":
        monkeypatch.setattr(module, "_load_prithvi", lambda *a, **k: (object(), {}, "cpu"))
    with pytest.raises(ModelError, match="input_chw must be CHW"):
        embedder.get_embedding(
            spatial=PointBuffer(lon=114.35, lat=30.5, buffer_m=320),
            temporal=TemporalSpec.range("2021-01-01", "2022-01-01"),
            sensor=None,
            output=OutputSpec.pooled(),
            backend="auto",
            device="cpu",
            input_chw=np.ones((1, 4, 4), dtype=np.float32),
        )
