"""Vendored SatCLIP location-encoder runtime.

Source: https://github.com/microsoft/satclip at commit
1ead1067e9a00d44b132403b6bb2ce061e48d48e (MIT License, see LICENSE).

Kept: the spherical-harmonic positional encoding, the SIREN network and the lightweight
checkpoint loader (``satclip/load_lightweight.py``). The image tower, training code and
unused positional encodings are not vendored. Upstream SHA-256 of the adapted files:

- satclip/location_encoder.py   9ac312155977ec0dc88cc35670216815000e69540b868035b8110415d89cc373
- satclip/load_lightweight.py   92594e655517129240b5e7151df3a78e4a32b27cee19c325e422831d67118a75
- positional_encoding/spherical_harmonics.py
                                98ad17aaa647c812ce20462f4e9e46db256a6bd0c56305e0e12a50e42f01de7d
- positional_encoding/spherical_harmonics_ylm.py (truncated to l <= 39)
                                facf06de2c98b6cc9ec7f6cbc2f73b8c94ff6dd43076e6607bf99b6e75078097
- positional_encoding/spherical_harmonics_closed_form.py
                                fc8e705ddabd0a41f862929204985909575b64ee2c3534e4988a663a08e76291
"""

from .location_encoder import (
    LocationEncoder,
    get_neural_network,
    get_positional_encoding,
    load_satclip_location_encoder,
)

__all__ = [
    "LocationEncoder",
    "get_neural_network",
    "get_positional_encoding",
    "load_satclip_location_encoder",
]
