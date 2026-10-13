"""Minimal DOFA dynamic wavelength layers.

Derived from `wave_dynamic_layer.py` in `zhu-xlab/DOFA` (MIT License).
Only the pieces required by rs-embed's inference path are vendored here.
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.init as init

_RANDOM_SEED = 1234
torch.manual_seed(_RANDOM_SEED)


def get_1d_sincos_pos_embed_from_grid_torch(embed_dim: int, pos: torch.Tensor) -> torch.Tensor:
    """Build 1D sin/cos wavelength embeddings."""
    if embed_dim % 2 != 0:
        raise ValueError(f"embed_dim must be even, got {embed_dim}")

    omega = torch.arange(embed_dim // 2, dtype=torch.float32, device=pos.device)
    omega /= embed_dim / 2.0
    omega = 1.0 / (10000**omega)

    pos = pos.reshape(-1)
    out = torch.einsum("m,d->md", pos, omega)
    emb_sin = torch.sin(out)
    emb_cos = torch.cos(out)
    return torch.cat([emb_sin, emb_cos], dim=1)


class TransformerWeightGenerator(nn.Module):
    def __init__(
        self,
        input_dim: int,
        output_dim: int,
        embed_dim: int,
        num_heads: int = 4,
        num_layers: int = 1,
    ) -> None:
        super().__init__()
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=input_dim,
            nhead=num_heads,
            activation="gelu",
            norm_first=False,
            batch_first=False,
            dropout=0.0,
        )
        self.transformer_encoder = nn.TransformerEncoder(
            encoder_layer,
            num_layers=num_layers,
            enable_nested_tensor=False,
        )
        self.fc_weight = nn.Linear(input_dim, output_dim)
        self.fc_bias = nn.Linear(input_dim, embed_dim)

        self.wt_num = 128
        self.weight_tokens = nn.Parameter(torch.empty([self.wt_num, input_dim]))
        self.bias_token = nn.Parameter(torch.empty([1, input_dim]))
        nn.init.normal_(self.weight_tokens, std=0.02)
        nn.init.normal_(self.bias_token, std=0.02)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        pos_wave = x
        x = torch.cat([self.weight_tokens, pos_wave], dim=0)
        x = torch.cat([x, self.bias_token], dim=0)
        transformer_output = self.transformer_encoder(x)
        weights = self.fc_weight(transformer_output[self.wt_num : -1] + pos_wave)
        bias = self.fc_bias(transformer_output[-1])
        return weights, bias


class FCResLayer(nn.Module):
    def __init__(self, linear_size: int = 128) -> None:
        super().__init__()
        self.l_size = linear_size
        self.nonlin1 = nn.ReLU(inplace=True)
        self.nonlin2 = nn.ReLU(inplace=True)
        self.w1 = nn.Linear(self.l_size, self.l_size)
        self.w2 = nn.Linear(self.l_size, self.l_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        y = self.w1(x)
        y = self.nonlin1(y)
        y = self.w2(y)
        y = self.nonlin2(y)
        return x + y


class DynamicMLPOFA(nn.Module):
    """Dynamic wavelength-aware patch embedding used by DOFA."""

    def __init__(
        self,
        wv_planes: int,
        inter_dim: int = 128,
        kernel_size: int = 3,
        embed_dim: int = 1024,
    ) -> None:
        super().__init__()
        self.kernel_size = kernel_size
        self.wv_planes = wv_planes
        self.embed_dim = embed_dim
        self._num_kernel = self.kernel_size * self.kernel_size * self.embed_dim
        self.inter_dim = inter_dim
        self.patch_size = (kernel_size, kernel_size)
        self.num_patches = -1
        self.weight_generator = TransformerWeightGenerator(
            wv_planes,
            self._num_kernel,
            embed_dim,
        )
        self.scaler = 0.01
        self.fclayer = FCResLayer(wv_planes)
        self._init_weights()

    def _get_weights(self, waves: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        return self.weight_generator(waves)

    @staticmethod
    def _weight_init(module: nn.Module) -> None:
        if isinstance(module, nn.Linear):
            init.xavier_uniform_(module.weight)
            if module.bias is not None:
                module.bias.data.fill_(0.01)

    def _init_weights(self) -> None:
        self.weight_generator.apply(self._weight_init)
        self.fclayer.apply(self._weight_init)

    def forward(
        self,
        img_feat: torch.Tensor,
        wvs: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        inplanes = int(wvs.size(0))
        waves = get_1d_sincos_pos_embed_from_grid_torch(self.wv_planes, wvs * 1000)
        waves = self.fclayer(waves)
        weight, bias = self._get_weights(waves)

        dynamic_weight = weight.view(
            inplanes,
            self.kernel_size,
            self.kernel_size,
            self.embed_dim,
        )
        dynamic_weight = dynamic_weight.permute([3, 0, 1, 2])

        if bias is not None:
            bias = bias.view([self.embed_dim]) * self.scaler

        weights = dynamic_weight * self.scaler
        dynamic_out = F.conv2d(
            img_feat,
            weights,
            bias=bias,
            stride=self.kernel_size,
            padding=1,
            dilation=1,
        )
        x = dynamic_out.flatten(2).transpose(1, 2)
        return x, waves
