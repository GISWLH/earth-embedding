from __future__ import annotations

from numbers import Integral
from typing import Any

from ..core.errors import ModelError


def model_config_value(
    model_config: dict[str, Any] | None,
    key: str,
) -> Any | None:
    if model_config is None:
        return None
    if isinstance(model_config, dict):
        return model_config.get(key)
    return getattr(model_config, key, None)


def coerce_config_bool(value: Any, *, key: str) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, Integral):
        return bool(value)
    if isinstance(value, str):
        raw = value.strip().lower()
        if raw in {"1", "true", "yes", "y", "on"}:
            return True
        if raw in {"0", "false", "no", "n", "off"}:
            return False
    raise ModelError(f"model_config['{key}'] must be a boolean-like value, got {value!r}.")
