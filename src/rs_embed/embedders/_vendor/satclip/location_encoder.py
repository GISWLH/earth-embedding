"""SatCLIP location encoder (spherical harmonics + SIREN).

Adapted from microsoft/satclip@1ead1067 ``satclip/location_encoder.py`` and
``satclip/load_lightweight.py`` (MIT License). Network definitions are unchanged; imports are
package-relative, unused encoders/networks are removed and the loader accepts an explicit
``weights_only`` policy.
"""

from __future__ import annotations

import math
from typing import Any

import torch
import torch.nn.functional as F
from einops import rearrange
from torch import nn

from . import positional_encoding as PE


def exists(val):
    return val is not None


def cast_tuple(val, repeat=1):
    return val if isinstance(val, tuple) else ((val,) * repeat)


class SirenNet(nn.Module):
    """Sinusoidal Representation Network (SIREN)."""

    def __init__(
        self,
        dim_in,
        dim_hidden,
        dim_out,
        num_layers,
        w0=1.0,
        w0_initial=30.0,
        use_bias=True,
        final_activation=None,
        degreeinput=False,
        dropout=True,
    ):
        super().__init__()
        self.num_layers = num_layers
        self.dim_hidden = dim_hidden
        self.degreeinput = degreeinput

        self.layers = nn.ModuleList([])
        for ind in range(num_layers):
            is_first = ind == 0
            layer_w0 = w0_initial if is_first else w0
            layer_dim_in = dim_in if is_first else dim_hidden

            self.layers.append(
                Siren(
                    dim_in=layer_dim_in,
                    dim_out=dim_hidden,
                    w0=layer_w0,
                    use_bias=use_bias,
                    is_first=is_first,
                    dropout=dropout,
                )
            )

        final_activation = nn.Identity() if not exists(final_activation) else final_activation
        self.last_layer = Siren(
            dim_in=dim_hidden,
            dim_out=dim_out,
            w0=w0,
            use_bias=use_bias,
            activation=final_activation,
            dropout=False,
        )

    def forward(self, x, mods=None):
        if self.degreeinput:
            x = torch.deg2rad(x) - torch.pi

        mods = cast_tuple(mods, self.num_layers)

        for layer, mod in zip(self.layers, mods):
            x = layer(x)

            if exists(mod):
                x *= rearrange(mod, "d -> () d")

        return self.last_layer(x)


class Sine(nn.Module):
    def __init__(self, w0=1.0):
        super().__init__()
        self.w0 = w0

    def forward(self, x):
        return torch.sin(self.w0 * x)


class Siren(nn.Module):
    def __init__(
        self,
        dim_in,
        dim_out,
        w0=1.0,
        c=6.0,
        is_first=False,
        use_bias=True,
        activation=None,
        dropout=False,
    ):
        super().__init__()
        self.dim_in = dim_in
        self.is_first = is_first
        self.dim_out = dim_out
        self.dropout = dropout

        weight = torch.zeros(dim_out, dim_in)
        bias = torch.zeros(dim_out) if use_bias else None
        self.init_(weight, bias, c=c, w0=w0)

        self.weight = nn.Parameter(weight)
        self.bias = nn.Parameter(bias) if use_bias else None
        self.activation = Sine(w0) if activation is None else activation

    def init_(self, weight, bias, c, w0):
        dim = self.dim_in

        w_std = (1 / dim) if self.is_first else (math.sqrt(c / dim) / w0)
        weight.uniform_(-w_std, w_std)

        if exists(bias):
            bias.uniform_(-w_std, w_std)

    def forward(self, x):
        out = F.linear(x, self.weight, self.bias)
        if self.dropout:
            out = F.dropout(out, training=self.training)
        out = self.activation(out)
        return out


def get_positional_encoding(
    name,
    legendre_polys=10,
    harmonics_calculation="analytic",
    min_radius=1,
    max_radius=360,
    frequency_num=10,
):
    if name == "sphericalharmonics" and harmonics_calculation in {"analytic", "closed-form"}:
        if harmonics_calculation == "analytic" and int(legendre_polys) > 40:
            raise ValueError("Vendored analytic spherical harmonics support legendre_polys <= 40.")
        return PE.SphericalHarmonics(
            legendre_polys=legendre_polys, harmonics_calculation=harmonics_calculation
        )
    raise ValueError(
        f"Positional encoding {name!r}/{harmonics_calculation!r} is not vendored; "
        "released SatCLIP checkpoints use analytic spherical harmonics."
    )


def get_neural_network(name, input_dim, num_classes=256, dim_hidden=256, num_layers=2):
    if name == "linear":
        return nn.Linear(input_dim, num_classes)
    if name == "siren":
        return SirenNet(
            dim_in=input_dim,
            dim_hidden=dim_hidden,
            num_layers=num_layers,
            dim_out=num_classes,
        )
    raise ValueError(f"{name} is not a vendored SatCLIP location network.")


class LocationEncoder(nn.Module):
    def __init__(self, posenc, nnet):
        super().__init__()
        self.posenc = posenc
        self.nnet = nnet

    def forward(self, x):
        x = self.posenc(x)
        return self.nnet(x)


def load_satclip_location_encoder(
    ckpt_path: str, device: str = "cpu", *, weights_only: bool = True
) -> tuple[LocationEncoder, dict[str, Any]]:
    """Load only the location branch of a SatCLIP Lightning checkpoint.

    Mirrors ``satclip/load_lightweight.py``: hyperparameters select the positional encoding
    and network, and only ``nnet`` parameters are loaded. The model runs in float64 as upstream.
    Inputs are ``[lon, lat]`` in degrees.
    """
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=weights_only)
    hp = ckpt["hyper_parameters"]

    posenc = get_positional_encoding(
        hp["le_type"],
        hp["legendre_polys"],
        hp["harmonics_calculation"],
        hp["min_radius"],
        hp["max_radius"],
        hp["frequency_num"],
    )
    nnet = get_neural_network(
        hp["pe_type"],
        posenc.embedding_dim,
        hp["embed_dim"],
        hp["capacity"],
        hp["num_hidden_layers"],
    )

    state_dict = ckpt["state_dict"]
    state_dict = {k[k.index("nnet") :]: state_dict[k] for k in state_dict.keys() if "nnet" in k}

    loc_encoder = LocationEncoder(posenc, nnet).double()
    loc_encoder.load_state_dict(state_dict)
    loc_encoder.eval()
    keys = (
        "le_type",
        "pe_type",
        "legendre_polys",
        "harmonics_calculation",
        "embed_dim",
        "capacity",
        "num_hidden_layers",
        "vision_layers",
    )
    return loc_encoder.to(device), {k: hp.get(k) for k in keys}
