import pytest

from rs_embed.core.errors import ModelError
from rs_embed.embedders import onthefly_terramind as tm


class _FakeTerratorchRegistry:
    def __init__(self, keys):
        self._keys = tuple(keys)

    def __iter__(self):
        return iter(self._keys)


class _FakeBackboneRegistry:
    def __init__(self, *, has_key=False, terratorch_keys=()):
        self.has_key = has_key
        self.terratorch_keys = tuple(terratorch_keys)

    def __contains__(self, name):
        return bool(self.has_key and name == "terramind_v1_small")

    def __iter__(self):
        return iter(())

    def __getitem__(self, key):
        if key != "terratorch":
            raise KeyError(key)
        return _FakeTerratorchRegistry(self.terratorch_keys)


def test_ensure_terramind_backbone_registered_retries_explicit_imports(monkeypatch):
    registry = _FakeBackboneRegistry(has_key=False)
    seen = []

    def _fake_import(name):
        seen.append(name)
        if name == "terratorch.models.backbones.terramind":
            registry.has_key = True
        return object()

    monkeypatch.setattr(tm.importlib, "import_module", _fake_import)

    tm._ensure_terramind_backbone_registered(registry, model_key="terramind_v1_small")

    assert seen[:2] == [
        "terratorch",
        "terratorch.models.backbones.terramind",
    ]


def test_ensure_terramind_backbone_registered_lists_available_keys(monkeypatch):
    registry = _FakeBackboneRegistry(
        has_key=False,
        terratorch_keys=("terramind_v1_base", "terramind_v1_large"),
    )

    monkeypatch.setattr(tm.importlib, "import_module", lambda name: object())

    with pytest.raises(
        ModelError, match="Available TerraMind backbones: terramind_v1_base, terramind_v1_large"
    ):
        tm._ensure_terramind_backbone_registered(registry, model_key="terramind_v1_small")


def test_import_terramind_backbone_registry_missing_terratorch_points_to_optional(monkeypatch):
    """Missing terratorch must suggest the optional-dep install command."""
    err = ModuleNotFoundError("No module named 'terratorch'")
    err.name = "terratorch"
    monkeypatch.setattr(tm.importlib, "import_module", lambda _name: (_ for _ in ()).throw(err))

    with pytest.raises(ModelError, match=r'pip install -e "\.\[terramind\]"'):
        tm._import_terramind_backbone_registry()
