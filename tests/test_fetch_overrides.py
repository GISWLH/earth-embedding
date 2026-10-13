import pytest

from rs_embed.core import registry
from rs_embed.core.errors import ModelError
from rs_embed.core.specs import FetchSpec, SensorSpec
from rs_embed.tools.model_defaults import resolve_sensor_for_model


@pytest.fixture(autouse=True)
def clean_registry():
    registry._REGISTRY.clear()
    yield
    registry._REGISTRY.clear()


def test_resolve_sensor_for_model_applies_fetch_to_default_sensor():
    @registry.register("fetchable_model")
    class DummyFetchable:
        def describe(self):
            return {
                "type": "on_the_fly",
                "inputs": {
                    "collection": "COPERNICUS/S2_SR_HARMONIZED",
                    "bands": ["B4", "B3", "B2"],
                },
                "defaults": {"scale_m": 10, "cloudy_pct": 30, "composite": "median"},
            }

    out = resolve_sensor_for_model(
        "fetchable_model",
        sensor=None,
        fetch=FetchSpec(scale_m=30, cloudy_pct=5, fill_value=-1.0),
    )
    assert out is not None
    assert out.collection == "COPERNICUS/S2_SR_HARMONIZED"
    assert out.bands == ("B4", "B3", "B2")
    assert out.scale_m == 30
    assert out.cloudy_pct == 5
    assert out.fill_value == -1.0
    assert out.composite == "median"


def test_resolve_sensor_for_model_rejects_sensor_and_fetch_together():
    with pytest.raises(ModelError, match="Use either sensor=... or fetch=..., not both"):
        resolve_sensor_for_model(
            "mock",
            sensor=SensorSpec(collection="A", bands=("B1",)),
            fetch=FetchSpec(scale_m=20),
        )


def test_resolve_sensor_for_gse_fetch_override():
    out = resolve_sensor_for_model(
        "gse",
        sensor=None,
        fetch=FetchSpec(scale_m=60),
    )
    assert out is not None
    assert out.collection == "GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL"
    assert out.scale_m == 60
