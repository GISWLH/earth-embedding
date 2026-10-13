from __future__ import annotations

import logging
import re
import warnings

import torch
from torch import nn

from rs_embed.embedders._vendor.thor.utils.helper import extract_model_state_dict_from_ckpt
from rs_embed.embedders._vendor.thor.utils.patch_embed import pi_resize_patch_embed
from rs_embed.embedders._vendor.thor.utils.pos_embed import interpolate_pos_embed_thor

logger = logging.getLogger(__name__)


class ModelRegistry:
    def __init__(self):
        self.models = {}

    def _register(self, model_name: str, model: nn.Module):
        if model_name is None:
            model_name = model.__name__

        if model_name in self.models:
            raise ValueError(f"Model {model_name} already registered")

        self.models[model_name] = model

    def register(self, model_name: str | None = None, model: nn.Module = None):
        def _register_wrapper(model):
            self._register(model_name, model)
            return model

        return _register_wrapper

    def get_model(self, model_name: str) -> nn.Module:
        return self.models[model_name]

    def build(self, model_cfgs) -> nn.Module:
        if model_cfgs.get("name", None) is not None:
            model_cfgs = {model_cfgs["name"]: model_cfgs}

        models = {}
        for model_name, model_cfg in model_cfgs.items():
            model_type = model_cfg.get("type")
            if model_type not in self.models:
                raise ValueError(
                    f"Model {model_name} not found in registry, available models: {self.models}"
                )

            input_params = model_cfg.get("input_params", {})
            model_kwargs = model_cfg.get("kwargs", {})
            model = self.get_model(model_type)(input_params, **model_kwargs)

            ckpt = model_cfg.get("ckpt", None)
            ckpt_ignore = model_cfg.get("ckpt_ignore", [])
            ckpt_copy = model_cfg.get("ckpt_copy", [])
            ckpt_remap = model_cfg.get("ckpt_remap", {})
            strict = model_cfg.get("strict", True)
            resize_patch_embed = model_cfg.get("resize_patch_embed", False)
            target_model = model_cfg.get("target_model", model_name)

            if ckpt is not None:
                logger.debug(f"Loading custom weight for {model_name} from {ckpt}")
                ckpt = torch.load(ckpt, map_location="cpu")
                model_state_dict = extract_model_state_dict_from_ckpt(ckpt)[target_model]

                new_keys = list(model_state_dict.keys())
                for rgx_item in ckpt_ignore:
                    re_expr = re.compile(rgx_item)
                    new_keys = [key for key in new_keys if not re_expr.match(key)]
                model_state_dict = {k: model_state_dict[k] for k in new_keys}

                for copy_key in ckpt_copy:
                    logger.debug(f"Skipping model load for: {copy_key}")
                    model_state_dict[copy_key] = model.state_dict()[copy_key]

                for key, cfg_map in ckpt_remap.items():
                    logger.debug(f"Remapping key for custom load: {key}")
                    old_val = model_state_dict.pop(key)
                    new_val = old_val
                    new_name = cfg_map.get("name", key)
                    params = cfg_map.get("params", {})
                    func = cfg_map.get("func", None)
                    if func == "index_select":
                        if isinstance(params["indices"], str):
                            start, stop = params["indices"].split(":")
                            params["indices"] = torch.arange(int(start), int(stop))
                        new_val = torch.index_select(old_val, params["dim"], torch.tensor(params["indices"]))
                    elif func == "concat_passthrough":
                        new_val = torch.cat(
                            (
                                new_val,
                                torch.index_select(
                                    model.state_dict()[new_name],
                                    params["dim"],
                                    torch.tensor(params["index"]),
                                ),
                            ),
                            dim=params["dim"],
                        )
                    model_state_dict[new_name] = new_val

                if resize_patch_embed:
                    channels = input_params.get("channels", None)
                    ground_cover = input_params.get("ground_cover", None)
                    if ground_cover is None:
                        ground_cover = input_params.get("ground_covers", None)
                        if isinstance(ground_cover, list):
                            ground_cover = max(ground_cover)

                    patch_embed_keys = [k for k in model_state_dict.keys() if "patch_embed" in k and "weight" in k]

                    def _get_patch_size(ground_cover: int, gsd: int, num_patch: int) -> tuple[int, int]:
                        patch_size = int(ground_cover / (gsd * num_patch))
                        assert patch_size * gsd * num_patch == ground_cover, (
                            f"Patch size {patch_size} does not divide ground cover {ground_cover} evenly"
                        )
                        return patch_size, patch_size

                    for patch_embed_key in patch_embed_keys:
                        channel_key = patch_embed_key.split(".")[-2]
                        if channel_key not in channels:
                            warnings.warn(
                                f"Channel {channel_key} not found in input params, skipping resizing of patch embed",
                                stacklevel=2,
                            )
                            continue
                        new_patch_size = _get_patch_size(ground_cover, **channels[channel_key])

                        if model_state_dict[patch_embed_key].shape[2:] != new_patch_size:
                            logger.debug(f"Resizing patch embed for {patch_embed_key}")
                            model_state_dict[patch_embed_key] = pi_resize_patch_embed(
                                model_state_dict[patch_embed_key], new_patch_size
                            )

                pos_embed_keys = [f"pos_embed.{k}" for k in model.pos_embed.keys()]
                pos_embeds_needs_reinit = False
                if len(pos_embed_keys) > 0:
                    ref_pos_embed_key = sorted(pos_embed_keys, key=lambda x: int(x.split(".")[-1]))[0]
                    if (
                        ref_pos_embed_key in model_state_dict
                        and model.state_dict()[ref_pos_embed_key].shape
                        != model_state_dict[ref_pos_embed_key].shape
                    ):
                        logger.debug("interpolating pos_embed")
                        interpolate_pos_embed_thor(model, model_state_dict, ref_pos_embed_key)
                        for key in pos_embed_keys:
                            if key in model_state_dict:
                                del model_state_dict[key]
                        pos_embeds_needs_reinit = True

                model.load_state_dict(model_state_dict, strict=strict)
                logger.debug(f"Custom weight loaded for {model_name}")

                if pos_embeds_needs_reinit:
                    model.init_embeds(pos_only=True)

            models[model_name] = model

        return models


MODELS = ModelRegistry()
