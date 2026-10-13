from __future__ import annotations

from collections import OrderedDict
from typing import Any


def extract_model_state_dict_from_ckpt(ckpt: dict[str, Any]):
    """Extract per-model state dicts from a THOR checkpoint."""
    if "state_dict" in ckpt:
        state_dict = ckpt["state_dict"]
    else:
        state_dict = ckpt

    model_state_dict = {}
    for key, state in state_dict.items():
        key_parts = key.split(".")
        model = key_parts[0]
        layer = ".".join(key_parts[1:])
        if model not in model_state_dict:
            model_state_dict[model] = OrderedDict()
        model_state_dict[model][layer] = state.clone()
    return model_state_dict

