"""Vendored from microsoft/satclip@1ead1067e9a00d44b132403b6bb2ce061e48d48e (MIT License).

Only the spherical-harmonic encoding used by the released SatCLIP checkpoints is kept.
"""

from .spherical_harmonics import SphericalHarmonics

__all__ = ["SphericalHarmonics"]
