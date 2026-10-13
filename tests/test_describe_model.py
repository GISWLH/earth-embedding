"""Tests for describe_model().

All tests use mock embedders registered into the core registry so that no
GEE connection, torch, or real model weights are required.
"""

import pytest

from rs_embed.api import describe_model, list_models
from rs_embed.core import registry
from rs_embed.core.errors import ModelError
from rs_embed.embedders.base import EmbedderBase
from rs_embed.embedders.catalog import MODEL_SPECS

# ── mock embedders ─────────────────────────────────────────────────────────────


class _FullMockEmbedder(EmbedderBase):
    """Embedder with a rich describe() payload."""

    def describe(self):
        return {
            "type": "onthefly",
            "backend": ["provider"],
            "input_bands": ["RED", "GREEN", "BLUE"],
            "output": ["pooled", "grid"],
            "defaults": {"image_size": 224, "scale_m": 10},
        }

    def get_embedding(self, **kwargs):  # pragma: no cover
        raise NotImplementedError


class _MinimalMockEmbedder(EmbedderBase):
    """Embedder that returns a minimal describe() payload."""

    def describe(self):
        return {"type": "precomputed", "output": ["pooled"]}

    def get_embedding(self, **kwargs):  # pragma: no cover
        raise NotImplementedError


# ── fixtures ───────────────────────────────────────────────────────────────────


@pytest.fixture(autouse=True)
def _clean_registry():
    """Isolate registry state between tests."""
    registry._REGISTRY.clear()
    yield
    registry._REGISTRY.clear()


@pytest.fixture()
def full_model(_clean_registry):
    registry.register("mock_full")(_FullMockEmbedder)
    return "mock_full"


@pytest.fixture()
def minimal_model(_clean_registry):
    registry.register("mock_minimal")(_MinimalMockEmbedder)
    return "mock_minimal"


# ── describe_model: happy path ─────────────────────────────────────────────────


def test_returns_dict(full_model):
    result = describe_model(full_model)
    assert isinstance(result, dict)


def test_full_describe_contents(full_model):
    result = describe_model(full_model)
    assert result["type"] == "onthefly"
    assert result["output"] == ["pooled", "grid"]
    assert result["input_bands"] == ["RED", "GREEN", "BLUE"]
    assert result["defaults"]["image_size"] == 224


def test_minimal_describe_contents(minimal_model):
    result = describe_model(minimal_model)
    assert result["type"] == "precomputed"
    assert result["output"] == ["pooled"]


def test_alias_resolves(full_model):
    """Aliases registered in the catalog should resolve to the same metadata."""
    # Register an alias pointing at the same model.
    from rs_embed.embedders import catalog as _cat

    _cat.MODEL_ALIASES["mock_full_alias"] = full_model
    try:
        result = describe_model("mock_full_alias")
        assert result["type"] == "onthefly"
    finally:
        del _cat.MODEL_ALIASES["mock_full_alias"]


def test_name_is_case_insensitive(full_model):
    result = describe_model(full_model.upper())
    assert isinstance(result, dict)


# ── describe_model: error cases ────────────────────────────────────────────────


def test_unknown_model_raises():
    with pytest.raises(ModelError, match="Unknown model"):
        describe_model("definitely_not_a_real_model")


def test_error_message_contains_model_name():
    with pytest.raises(ModelError, match="no_such_model"):
        describe_model("no_such_model")


# ── catalog coverage ───────────────────────────────────────────────────────────


def test_all_catalog_models_are_importable():
    """Every entry in MODEL_SPECS must be importable and instantiable.

    This guards against stale catalog entries pointing at renamed classes.
    No weights are loaded — only the module import and class instantiation
    are exercised.
    """
    import importlib

    errors = []
    for model_id, (module_name, class_name) in MODEL_SPECS.items():
        try:
            mod = importlib.import_module(f"rs_embed.embedders.{module_name}")
            cls = getattr(mod, class_name)
            instance = cls()
            desc = instance.describe()
            assert isinstance(desc, dict), f"{model_id}: describe() must return dict"
        except Exception as exc:
            errors.append(f"{model_id}: {exc}")

    if errors:
        pytest.fail("Catalog entries failed:\n" + "\n".join(errors))


def test_all_catalog_models_have_required_describe_keys():
    """Every model's describe() must include 'type' and 'output'."""
    import importlib

    for model_id, (module_name, class_name) in MODEL_SPECS.items():
        mod = importlib.import_module(f"rs_embed.embedders.{module_name}")
        cls = getattr(mod, class_name)
        desc = cls().describe()
        assert "type" in desc, f"{model_id}: describe() missing 'type' key"
        assert "output" in desc, f"{model_id}: describe() missing 'output' key"


# ── integration with list_models ──────────────────────────────────────────────


def test_describe_model_consistent_with_list_models():
    """Every model returned by list_models() must be describable."""
    for model_id in list_models():
        result = describe_model(model_id)
        assert isinstance(result, dict), f"{model_id}: expected dict, got {type(result)}"
