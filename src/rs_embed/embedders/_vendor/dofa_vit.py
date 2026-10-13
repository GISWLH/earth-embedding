"""Minimal DOFA ViT model.

Derived from `dofa_v1.py` in `zhu-xlab/DOFA` (MIT License).
Only the inference path used by rs-embed is vendored here.
"""

from __future__ import annotations

from functools import partial

import torch
import torch.nn as nn
from timm.models.vision_transformer import Block

from .dofa_wave_dynamic_layer import DynamicMLPOFA


class OFAViT(nn.Module):
    """DOFA Vision Transformer backbone."""

    def __init__(
        self,
        *,
        img_size: int = 224,
        patch_size: int = 16,
        drop_rate: float = 0.0,
        embed_dim: int = 1024,
        depth: int = 24,
        num_heads: int = 16,
        wv_planes: int = 128,
        num_classes: int = 0,
        global_pool: bool = True,
        mlp_ratio: float = 4.0,
        norm_layer: type[nn.Module] | None = None,
    ) -> None:
        super().__init__()
        if norm_layer is None:
            norm_layer = partial(nn.LayerNorm, eps=1e-6)

        self.img_size = img_size
        self.patch_size = patch_size
        self.embed_dim = embed_dim
        self.wv_planes = wv_planes
        self.global_pool = global_pool

        if self.global_pool:
            self.fc_norm = norm_layer(embed_dim)
        else:
            self.norm = norm_layer(embed_dim)

        self.patch_embed = DynamicMLPOFA(
            wv_planes=wv_planes,
            inter_dim=128,
            kernel_size=patch_size,
            embed_dim=embed_dim,
        )
        self.num_patches = (img_size // patch_size) ** 2
        self.cls_token = nn.Parameter(torch.zeros(1, 1, embed_dim))
        self.pos_embed = nn.Parameter(
            torch.zeros(1, self.num_patches + 1, embed_dim),
            requires_grad=False,
        )
        self.blocks = nn.ModuleList(
            [
                Block(
                    embed_dim,
                    num_heads,
                    mlp_ratio,
                    qkv_bias=True,
                    norm_layer=norm_layer,
                )
                for _ in range(depth)
            ]
        )
        self.head_drop = nn.Dropout(drop_rate)
        self.head = nn.Linear(embed_dim, num_classes) if num_classes > 0 else nn.Identity()

    def forward_features(self, x: torch.Tensor, wave_list: list[float] | torch.Tensor) -> torch.Tensor:
        if torch.is_tensor(wave_list):
            wavelist = wave_list.to(device=x.device, dtype=torch.float32)
        else:
            wavelist = torch.tensor(wave_list, device=x.device, dtype=torch.float32)
        self.waves = wavelist

        x, _ = self.patch_embed(x, self.waves)
        x = x + self.pos_embed[:, 1:, :]

        cls_token = self.cls_token + self.pos_embed[:, :1, :]
        cls_tokens = cls_token.expand(x.shape[0], -1, -1)
        x = torch.cat((cls_tokens, x), dim=1)

        for block in self.blocks:
            x = block(x)

        if self.global_pool:
            x = x[:, 1:, :].mean(dim=1)
            return self.fc_norm(x)

        x = self.norm(x)
        return x[:, 0]

    def forward_head(self, x: torch.Tensor, pre_logits: bool = False) -> torch.Tensor:
        x = self.head_drop(x)
        return x if pre_logits else self.head(x)

    def forward(self, x: torch.Tensor, wave_list: list[float] | torch.Tensor) -> torch.Tensor:
        x = self.forward_features(x, wave_list)
        return self.forward_head(x)


def vit_base_patch16(**kwargs) -> OFAViT:
    return OFAViT(
        patch_size=16,
        embed_dim=768,
        depth=12,
        num_heads=12,
        mlp_ratio=4,
        norm_layer=partial(nn.LayerNorm, eps=1e-6),
        **kwargs,
    )


def vit_large_patch16(**kwargs) -> OFAViT:
    return OFAViT(
        patch_size=16,
        embed_dim=1024,
        depth=24,
        num_heads=16,
        mlp_ratio=4,
        norm_layer=partial(nn.LayerNorm, eps=1e-6),
        **kwargs,
    )
