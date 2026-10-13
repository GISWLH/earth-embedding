"""Minimal vendored SatVision SwinV2 runtime.

Adapted from `pytorch-caney` to keep only the inference path used by rs-embed.
The upstream project ships under Apache-2.0; see `LICENSE.satvision_caney`.
"""

from __future__ import annotations

import math
from collections.abc import Iterable

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.checkpoint as checkpoint


def to_2tuple(x: int | tuple[int, int]) -> tuple[int, int]:
    if isinstance(x, tuple):
        return x
    return (int(x), int(x))


def trunc_normal_(tensor: torch.Tensor, std: float = 0.02, mean: float = 0.0) -> torch.Tensor:
    return nn.init.trunc_normal_(tensor, mean=mean, std=std)


def drop_path(
    x: torch.Tensor,
    drop_prob: float = 0.0,
    training: bool = False,
) -> torch.Tensor:
    if drop_prob == 0.0 or not training:
        return x
    keep_prob = 1.0 - drop_prob
    shape = (x.shape[0],) + (1,) * (x.ndim - 1)
    random_tensor = x.new_empty(shape).bernoulli_(keep_prob)
    return x.div(keep_prob) * random_tensor


class DropPath(nn.Module):
    def __init__(self, drop_prob: float = 0.0) -> None:
        super().__init__()
        self.drop_prob = float(drop_prob)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return drop_path(x, self.drop_prob, self.training)


def _meshgrid_ij(a: torch.Tensor, b: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    try:
        return torch.meshgrid(a, b, indexing="ij")
    except TypeError:
        return torch.meshgrid(a, b)


def window_partition(x: torch.Tensor, window_size: int) -> torch.Tensor:
    b, h, w, c = x.shape
    x = x.view(b, h // window_size, window_size, w // window_size, window_size, c)
    return x.permute(0, 1, 3, 2, 4, 5).contiguous().view(-1, window_size, window_size, c)


def window_reverse(windows: torch.Tensor, window_size: int, h: int, w: int) -> torch.Tensor:
    b = int(windows.shape[0] / (h * w / window_size / window_size))
    x = windows.view(b, h // window_size, w // window_size, window_size, window_size, -1)
    return x.permute(0, 1, 3, 2, 4, 5).contiguous().view(b, h, w, -1)


class Mlp(nn.Module):
    def __init__(
        self,
        in_features: int,
        hidden_features: int | None = None,
        out_features: int | None = None,
        act_layer: type[nn.Module] = nn.GELU,
        drop: float = 0.0,
    ) -> None:
        super().__init__()
        out_features = out_features or in_features
        hidden_features = hidden_features or in_features
        self.fc1 = nn.Linear(in_features, hidden_features)
        self.act = act_layer()
        self.fc2 = nn.Linear(hidden_features, out_features)
        self.drop = nn.Dropout(drop)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.fc1(x)
        x = self.act(x)
        x = self.drop(x)
        x = self.fc2(x)
        x = self.drop(x)
        return x


class WindowAttention(nn.Module):
    def __init__(
        self,
        dim: int,
        window_size: tuple[int, int],
        num_heads: int,
        qkv_bias: bool = True,
        attn_drop: float = 0.0,
        proj_drop: float = 0.0,
        pretrained_window_size: Iterable[int] = (0, 0),
    ) -> None:
        super().__init__()
        self.dim = int(dim)
        self.window_size = tuple(int(v) for v in window_size)
        self.pretrained_window_size = tuple(int(v) for v in pretrained_window_size)
        self.num_heads = int(num_heads)
        self.logit_scale = nn.Parameter(
            torch.log(10 * torch.ones((self.num_heads, 1, 1))), requires_grad=True
        )
        self.cpb_mlp = nn.Sequential(
            nn.Linear(2, 512, bias=True),
            nn.ReLU(inplace=True),
            nn.Linear(512, self.num_heads, bias=False),
        )

        relative_coords_h = torch.arange(
            -(self.window_size[0] - 1), self.window_size[0], dtype=torch.float32
        )
        relative_coords_w = torch.arange(
            -(self.window_size[1] - 1), self.window_size[1], dtype=torch.float32
        )
        grid_h, grid_w = _meshgrid_ij(relative_coords_h, relative_coords_w)
        relative_coords_table = (
            torch.stack([grid_h, grid_w]).permute(1, 2, 0).contiguous().unsqueeze(0)
        )

        if self.pretrained_window_size[0] > 0:
            relative_coords_table[:, :, :, 0] /= self.pretrained_window_size[0] - 1
            relative_coords_table[:, :, :, 1] /= self.pretrained_window_size[1] - 1
        else:
            relative_coords_table[:, :, :, 0] /= self.window_size[0] - 1
            relative_coords_table[:, :, :, 1] /= self.window_size[1] - 1
        relative_coords_table *= 8
        relative_coords_table = torch.sign(relative_coords_table) * torch.log2(
            torch.abs(relative_coords_table) + 1.0
        ) / math.log2(8)
        self.register_buffer("relative_coords_table", relative_coords_table)

        coords_h = torch.arange(self.window_size[0])
        coords_w = torch.arange(self.window_size[1])
        grid_h, grid_w = _meshgrid_ij(coords_h, coords_w)
        coords = torch.stack([grid_h, grid_w])
        coords_flatten = torch.flatten(coords, 1)
        relative_coords = coords_flatten[:, :, None] - coords_flatten[:, None, :]
        relative_coords = relative_coords.permute(1, 2, 0).contiguous()
        relative_coords[:, :, 0] += self.window_size[0] - 1
        relative_coords[:, :, 1] += self.window_size[1] - 1
        relative_coords[:, :, 0] *= 2 * self.window_size[1] - 1
        relative_position_index = relative_coords.sum(-1)
        self.register_buffer("relative_position_index", relative_position_index)

        self.qkv = nn.Linear(self.dim, self.dim * 3, bias=False)
        if qkv_bias:
            self.q_bias = nn.Parameter(torch.zeros(self.dim))
            self.v_bias = nn.Parameter(torch.zeros(self.dim))
        else:
            self.q_bias = None
            self.v_bias = None
        self.attn_drop = nn.Dropout(attn_drop)
        self.proj = nn.Linear(self.dim, self.dim)
        self.proj_drop = nn.Dropout(proj_drop)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        b_, n, c = x.shape
        qkv_bias = None
        if self.q_bias is not None:
            qkv_bias = torch.cat(
                (
                    self.q_bias,
                    torch.zeros_like(self.v_bias, requires_grad=False),
                    self.v_bias,
                )
            )
        qkv = F.linear(input=x, weight=self.qkv.weight, bias=qkv_bias)
        qkv = qkv.reshape(b_, n, 3, self.num_heads, -1).permute(2, 0, 3, 1, 4)
        q, k, v = qkv[0], qkv[1], qkv[2]

        attn = F.normalize(q, dim=-1) @ F.normalize(k, dim=-1).transpose(-2, -1)
        max_scale = torch.log(torch.tensor(1.0 / 0.01, device=self.logit_scale.device))
        logit_scale = torch.clamp(self.logit_scale, max=max_scale).exp()
        attn = attn * logit_scale

        relative_position_bias_table = self.cpb_mlp(self.relative_coords_table).view(
            -1, self.num_heads
        )
        relative_position_bias = relative_position_bias_table[
            self.relative_position_index.view(-1)
        ].view(
            self.window_size[0] * self.window_size[1],
            self.window_size[0] * self.window_size[1],
            -1,
        )
        relative_position_bias = relative_position_bias.permute(2, 0, 1).contiguous()
        relative_position_bias = 16 * torch.sigmoid(relative_position_bias)
        attn = attn + relative_position_bias.unsqueeze(0)

        if mask is not None:
            nw = mask.shape[0]
            attn = attn.view(b_ // nw, nw, self.num_heads, n, n) + mask.unsqueeze(1).unsqueeze(0)
            attn = attn.view(-1, self.num_heads, n, n)
        attn = self.softmax(attn)
        attn = self.attn_drop(attn)

        x = (attn @ v).transpose(1, 2).reshape(b_, n, c)
        x = self.proj(x)
        x = self.proj_drop(x)
        return x


class SwinTransformerBlock(nn.Module):
    def __init__(
        self,
        dim: int,
        input_resolution: tuple[int, int],
        num_heads: int,
        window_size: int = 7,
        shift_size: int = 0,
        mlp_ratio: float = 4.0,
        qkv_bias: bool = True,
        drop: float = 0.0,
        attn_drop: float = 0.0,
        drop_path: float = 0.0,
        act_layer: type[nn.Module] = nn.GELU,
        norm_layer: type[nn.Module] = nn.LayerNorm,
        pretrained_window_size: int = 0,
        extra_norm: bool = False,
    ) -> None:
        super().__init__()
        self.dim = int(dim)
        self.input_resolution = tuple(int(v) for v in input_resolution)
        self.num_heads = int(num_heads)
        self.window_size = int(window_size)
        self.shift_size = int(shift_size)
        self.mlp_ratio = float(mlp_ratio)
        if min(self.input_resolution) <= self.window_size:
            self.shift_size = 0
            self.window_size = min(self.input_resolution)
        if not (0 <= self.shift_size < self.window_size):
            raise ValueError("shift_size must be in [0, window_size)")

        self.norm1 = norm_layer(self.dim)
        self.attn = WindowAttention(
            self.dim,
            window_size=to_2tuple(self.window_size),
            num_heads=self.num_heads,
            qkv_bias=qkv_bias,
            attn_drop=attn_drop,
            proj_drop=drop,
            pretrained_window_size=to_2tuple(pretrained_window_size),
        )
        self.drop_path = DropPath(drop_path) if drop_path > 0 else nn.Identity()
        self.norm2 = norm_layer(self.dim)
        self.norm3 = norm_layer(self.dim) if extra_norm else nn.Identity()
        mlp_hidden_dim = int(self.dim * self.mlp_ratio)
        self.mlp = Mlp(self.dim, hidden_features=mlp_hidden_dim, act_layer=act_layer, drop=drop)

        if self.shift_size > 0:
            h, w = self.input_resolution
            img_mask = torch.zeros((1, h, w, 1))
            h_slices = (
                slice(0, -self.window_size),
                slice(-self.window_size, -self.shift_size),
                slice(-self.shift_size, None),
            )
            w_slices = (
                slice(0, -self.window_size),
                slice(-self.window_size, -self.shift_size),
                slice(-self.shift_size, None),
            )
            cnt = 0
            for hs in h_slices:
                for ws in w_slices:
                    img_mask[:, hs, ws, :] = cnt
                    cnt += 1
            mask_windows = window_partition(img_mask, self.window_size)
            mask_windows = mask_windows.view(-1, self.window_size * self.window_size)
            attn_mask = mask_windows.unsqueeze(1) - mask_windows.unsqueeze(2)
            attn_mask = attn_mask.masked_fill(attn_mask != 0, float(-100.0)).masked_fill(
                attn_mask == 0, float(0.0)
            )
        else:
            attn_mask = None
        self.register_buffer("attn_mask", attn_mask)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h, w = self.input_resolution
        b, l, c = x.shape
        if l != h * w:
            raise ValueError("input feature has wrong size")
        shortcut = x
        x = x.view(b, h, w, c)
        if self.shift_size > 0:
            shifted_x = torch.roll(x, shifts=(-self.shift_size, -self.shift_size), dims=(1, 2))
        else:
            shifted_x = x

        x_windows = window_partition(shifted_x, self.window_size)
        x_windows = x_windows.view(-1, self.window_size * self.window_size, c)
        attn_windows = self.attn(x_windows, mask=self.attn_mask)
        attn_windows = attn_windows.view(-1, self.window_size, self.window_size, c)
        shifted_x = window_reverse(attn_windows, self.window_size, h, w)

        if self.shift_size > 0:
            x = torch.roll(shifted_x, shifts=(self.shift_size, self.shift_size), dims=(1, 2))
        else:
            x = shifted_x
        x = x.view(b, h * w, c)
        x = shortcut + self.drop_path(self.norm1(x))
        x = x + self.drop_path(self.norm2(self.mlp(x)))
        x = self.norm3(x)
        return x


class PatchMerging(nn.Module):
    def __init__(
        self,
        input_resolution: tuple[int, int],
        dim: int,
        norm_layer: type[nn.Module] = nn.LayerNorm,
    ) -> None:
        super().__init__()
        self.input_resolution = tuple(int(v) for v in input_resolution)
        self.dim = int(dim)
        self.reduction = nn.Linear(4 * self.dim, 2 * self.dim, bias=False)
        self.norm = norm_layer(2 * self.dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h, w = self.input_resolution
        b, l, c = x.shape
        if l != h * w:
            raise ValueError("input feature has wrong size")
        if h % 2 != 0 or w % 2 != 0:
            raise ValueError(f"x size ({h}*{w}) are not even.")
        x = x.view(b, h, w, c)
        x0 = x[:, 0::2, 0::2, :]
        x1 = x[:, 1::2, 0::2, :]
        x2 = x[:, 0::2, 1::2, :]
        x3 = x[:, 1::2, 1::2, :]
        x = torch.cat([x0, x1, x2, x3], -1)
        x = x.view(b, -1, 4 * c)
        x = self.reduction(x)
        x = self.norm(x)
        return x


class BasicLayer(nn.Module):
    def __init__(
        self,
        dim: int,
        input_resolution: tuple[int, int],
        depth: int,
        num_heads: int,
        window_size: int,
        mlp_ratio: float = 4.0,
        qkv_bias: bool = True,
        drop: float = 0.0,
        attn_drop: float = 0.0,
        drop_path: float | list[float] = 0.0,
        norm_layer: type[nn.Module] = nn.LayerNorm,
        downsample: type[nn.Module] | None = None,
        use_checkpoint: bool = False,
        pretrained_window_size: int = 0,
        extra_norm_period: int = 0,
        extra_norm_stage: bool = False,
    ) -> None:
        super().__init__()
        self.dim = int(dim)
        self.input_resolution = tuple(int(v) for v in input_resolution)
        self.depth = int(depth)
        self.use_checkpoint = bool(use_checkpoint)

        def _extra_norm(index: int) -> bool:
            i = index + 1
            if extra_norm_period and i % extra_norm_period == 0:
                return True
            return i == self.depth if extra_norm_stage else False

        self.blocks = nn.ModuleList(
            [
                SwinTransformerBlock(
                    dim=self.dim,
                    input_resolution=self.input_resolution,
                    num_heads=num_heads,
                    window_size=window_size,
                    shift_size=0 if i % 2 == 0 else window_size // 2,
                    mlp_ratio=mlp_ratio,
                    qkv_bias=qkv_bias,
                    drop=drop,
                    attn_drop=attn_drop,
                    drop_path=drop_path[i] if isinstance(drop_path, list) else drop_path,
                    norm_layer=norm_layer,
                    pretrained_window_size=pretrained_window_size,
                    extra_norm=_extra_norm(i),
                )
                for i in range(self.depth)
            ]
        )
        self.downsample = (
            downsample(self.input_resolution, dim=self.dim, norm_layer=norm_layer)
            if downsample is not None
            else None
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        for blk in self.blocks:
            if self.use_checkpoint:
                x = checkpoint.checkpoint(blk, x, use_reentrant=False)
            else:
                x = blk(x)
        if self.downsample is not None:
            x = self.downsample(x)
        return x

    def _init_respostnorm(self) -> None:
        for blk in self.blocks:
            nn.init.constant_(blk.norm1.bias, 0)
            nn.init.constant_(blk.norm1.weight, 0)
            nn.init.constant_(blk.norm2.bias, 0)
            nn.init.constant_(blk.norm2.weight, 0)


class PatchEmbed(nn.Module):
    def __init__(
        self,
        img_size: int | tuple[int, int] = 224,
        patch_size: int | tuple[int, int] = 4,
        in_chans: int = 3,
        embed_dim: int = 96,
        norm_layer: type[nn.Module] | None = None,
    ) -> None:
        super().__init__()
        img_size = to_2tuple(img_size)
        patch_size = to_2tuple(patch_size)
        patches_resolution = [img_size[0] // patch_size[0], img_size[1] // patch_size[1]]
        self.img_size = img_size
        self.patch_size = patch_size
        self.patches_resolution = patches_resolution
        self.num_patches = patches_resolution[0] * patches_resolution[1]
        self.in_chans = int(in_chans)
        self.embed_dim = int(embed_dim)
        self.proj = nn.Conv2d(
            self.in_chans,
            self.embed_dim,
            kernel_size=self.patch_size,
            stride=self.patch_size,
        )
        self.norm = norm_layer(self.embed_dim) if norm_layer is not None else None

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        b, c, h, w = x.shape
        if h != self.img_size[0] or w != self.img_size[1]:
            raise ValueError(
                f"Input image size ({h}*{w}) doesn't match model ({self.img_size[0]}*{self.img_size[1]})."
            )
        x = self.proj(x).flatten(2).transpose(1, 2)
        if self.norm is not None:
            x = self.norm(x)
        return x


class SwinTransformerV2(nn.Module):
    def __init__(
        self,
        img_size: int = 224,
        patch_size: int = 4,
        in_chans: int = 3,
        num_classes: int = 1000,
        embed_dim: int = 96,
        depths: Iterable[int] = (2, 2, 6, 2),
        num_heads: Iterable[int] = (3, 6, 12, 24),
        window_size: int = 7,
        mlp_ratio: float = 4.0,
        qkv_bias: bool = True,
        drop_rate: float = 0.0,
        attn_drop_rate: float = 0.0,
        drop_path_rate: float = 0.1,
        norm_layer: type[nn.Module] = nn.LayerNorm,
        ape: bool = False,
        patch_norm: bool = True,
        use_checkpoint: bool = False,
        pretrained_window_sizes: Iterable[int] = (0, 0, 0, 0),
        extra_norm_period: int = 0,
        extra_norm_stage: bool = False,
        **kwargs,
    ) -> None:
        super().__init__()
        depths = [int(v) for v in depths]
        num_heads = [int(v) for v in num_heads]
        pretrained_window_sizes = [int(v) for v in pretrained_window_sizes]

        self.num_classes = int(num_classes)
        self.num_layers = len(depths)
        self.embed_dim = int(embed_dim)
        self.ape = bool(ape)
        self.patch_norm = bool(patch_norm)
        self.num_features = int(self.embed_dim * 2 ** (self.num_layers - 1))
        self.mlp_ratio = float(mlp_ratio)

        self.patch_embed = PatchEmbed(
            img_size=img_size,
            patch_size=patch_size,
            in_chans=in_chans,
            embed_dim=self.embed_dim,
            norm_layer=norm_layer if self.patch_norm else None,
        )
        num_patches = self.patch_embed.num_patches
        patches_resolution = self.patch_embed.patches_resolution
        self.patches_resolution = patches_resolution

        if self.ape:
            self.absolute_pos_embed = nn.Parameter(torch.zeros(1, num_patches, self.embed_dim))
            trunc_normal_(self.absolute_pos_embed, std=0.02)

        self.pos_drop = nn.Dropout(p=drop_rate)
        dpr = [x.item() for x in torch.linspace(0, drop_path_rate, sum(depths))]

        self.layers = nn.ModuleList()
        for i_layer in range(self.num_layers):
            layer = BasicLayer(
                dim=int(self.embed_dim * 2**i_layer),
                input_resolution=(
                    patches_resolution[0] // (2**i_layer),
                    patches_resolution[1] // (2**i_layer),
                ),
                depth=depths[i_layer],
                num_heads=num_heads[i_layer],
                window_size=window_size,
                mlp_ratio=self.mlp_ratio,
                qkv_bias=qkv_bias,
                drop=drop_rate,
                attn_drop=attn_drop_rate,
                drop_path=dpr[sum(depths[:i_layer]) : sum(depths[: i_layer + 1])],
                norm_layer=norm_layer,
                downsample=PatchMerging if i_layer < self.num_layers - 1 else None,
                use_checkpoint=use_checkpoint,
                pretrained_window_size=pretrained_window_sizes[i_layer],
                extra_norm_period=extra_norm_period,
                extra_norm_stage=extra_norm_stage,
            )
            self.layers.append(layer)

        self.norm = norm_layer(self.num_features)
        self.avgpool = nn.AdaptiveAvgPool1d(1)
        self.head = nn.Linear(self.num_features, self.num_classes) if self.num_classes > 0 else nn.Identity()

        self.apply(self._init_weights)
        for layer in self.layers:
            layer._init_respostnorm()

    def _init_weights(self, m: nn.Module) -> None:
        if isinstance(m, nn.Linear):
            trunc_normal_(m.weight, std=0.02)
            if m.bias is not None:
                nn.init.constant_(m.bias, 0)
        elif isinstance(m, nn.LayerNorm):
            nn.init.constant_(m.bias, 0)
            nn.init.constant_(m.weight, 1.0)

    @torch.jit.ignore
    def no_weight_decay(self) -> set[str]:
        return {"absolute_pos_embed"}

    @torch.jit.ignore
    def no_weight_decay_keywords(self) -> set[str]:
        return {"cpb_mlp", "logit_scale", "relative_position_bias_table"}

    def _forward_tokens(self, x: torch.Tensor) -> torch.Tensor:
        x = self.patch_embed(x)
        if self.ape:
            x = x + self.absolute_pos_embed
        x = self.pos_drop(x)
        for layer in self.layers:
            x = layer(x)
        return x

    def forward_features(self, x: torch.Tensor) -> torch.Tensor:
        x = self._forward_tokens(x)
        x = self.norm(x)
        x = self.avgpool(x.transpose(1, 2))
        x = torch.flatten(x, 1)
        return x

    def extra_features(self, x: torch.Tensor) -> list[torch.Tensor]:
        x = self.patch_embed(x)
        if self.ape:
            x = x + self.absolute_pos_embed
        x = self.pos_drop(x)
        feature: list[torch.Tensor] = []
        for layer in self.layers:
            x = layer(x)
            bs, n, f = x.shape
            h = int(n**0.5)
            feature.append(x.view(-1, h, h, f).permute(0, 3, 1, 2).contiguous())
        return feature

    def get_unet_feature(self, x: torch.Tensor) -> list[torch.Tensor]:
        x = self.patch_embed(x)
        if self.ape:
            x = x + self.absolute_pos_embed
        x = self.pos_drop(x)
        bs, n, f = x.shape
        h = int(n**0.5)
        feature = [x.view(-1, h, h, f).permute(0, 3, 1, 2).contiguous()]
        for layer in self.layers:
            x = layer(x)
            bs, n, f = x.shape
            h = int(n**0.5)
            feature.append(x.view(-1, h, h, f).permute(0, 3, 1, 2).contiguous())
        return feature

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.extra_features(x)[-1]


class SwinTransformerV2ForSimMIM(SwinTransformerV2):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        if self.num_classes != 0:
            raise ValueError("SwinTransformerV2ForSimMIM requires num_classes=0.")
        self.mask_token = nn.Parameter(torch.zeros(1, 1, self.embed_dim))
        trunc_normal_(self.mask_token, mean=0.0, std=0.02)

    def forward(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        x = self.patch_embed(x)
        if mask is None:
            raise ValueError("mask is required for SimMIM forward()")
        b, l, _ = x.shape
        mask_tokens = self.mask_token.expand(b, l, -1)
        w = mask.flatten(1).unsqueeze(-1).type_as(mask_tokens)
        x = x * (1.0 - w) + mask_tokens * w
        if self.ape:
            x = x + self.absolute_pos_embed
        x = self.pos_drop(x)
        for layer in self.layers:
            x = layer(x)
        x = self.norm(x)
        x = x.transpose(1, 2)
        b, c, l = x.shape
        h = w = int(l**0.5)
        return x.reshape(b, c, h, w)

    @torch.jit.ignore
    def no_weight_decay(self) -> set[str]:
        return super().no_weight_decay() | {"mask_token"}


__all__ = ["SwinTransformerV2", "SwinTransformerV2ForSimMIM"]
