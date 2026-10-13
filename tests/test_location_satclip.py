import numpy as np
import pytest

torch = pytest.importorskip("torch")

from rs_embed.core.errors import ModelError  # noqa: E402
from rs_embed.core.specs import BBox, OutputSpec, PointBuffer, TemporalSpec  # noqa: E402
from rs_embed.embedders._vendor.satclip import (  # noqa: E402
    LocationEncoder,
    get_neural_network,
    get_positional_encoding,
)
from rs_embed.embedders.catalog import MODEL_SPECS, canonical_model_id  # noqa: E402


@pytest.fixture
def tiny_ckpt(tmp_path, monkeypatch):
    """A small SatCLIP-format Lightning checkpoint (L=3, 8-d) with random weights."""
    import rs_embed.embedders.location_satclip as mod

    torch.manual_seed(0)
    hp = {
        "le_type": "sphericalharmonics",
        "pe_type": "siren",
        "legendre_polys": 3,
        "harmonics_calculation": "analytic",
        "min_radius": 1,
        "max_radius": 360,
        "frequency_num": 16,
        "embed_dim": 8,
        "capacity": 16,
        "num_hidden_layers": 2,
        "vision_layers": "test",
    }
    posenc = get_positional_encoding("sphericalharmonics", 3, "analytic")
    nnet = get_neural_network("siren", posenc.embedding_dim, 8, 16, 2)
    state = {
        f"model.location.{k}": v for k, v in LocationEncoder(posenc, nnet).state_dict().items()
    }
    state["model.visual.weight"] = torch.zeros(2)
    path = tmp_path / "tiny_satclip.ckpt"
    torch.save({"hyper_parameters": hp, "state_dict": state}, path)
    monkeypatch.setenv("RS_EMBED_SATCLIP_CKPT", str(path))
    mod._load_location_encoder.cache_clear()
    yield path
    mod._load_location_encoder.cache_clear()


def test_catalog_registers_satclip_as_location_encoder():
    from rs_embed.embedders.location_satclip import SatCLIPEmbedder

    assert MODEL_SPECS["satclip"] == ("location_satclip", "SatCLIPEmbedder")
    assert canonical_model_id("SatCLIP_ViT16_L40") == "satclip"
    desc = SatCLIPEmbedder().describe()
    assert desc["type"] == "location"
    assert "precomputed" not in desc["type"]
    assert desc["model_config"]["variant"]["default"] == "vit16-l40"


def test_pooled_output_queries_centre_and_ignores_temporal(tiny_ckpt):
    from rs_embed.embedders.location_satclip import SatCLIPEmbedder, encode_lonlat

    emb = SatCLIPEmbedder().get_embedding(
        spatial=PointBuffer(lon=114.4, lat=30.5, buffer_m=320),
        temporal=TemporalSpec.year(2021),
        sensor=None,
        output=OutputSpec.pooled(),
        backend="auto",
        device="cpu",
    )
    direct, _ = encode_lonlat(np.array([[114.4, 30.5]]), variant="vit16-l40", device="cpu")
    assert emb.data.shape == (8,)
    np.testing.assert_allclose(emb.data, direct[0])
    assert emb.meta["pooling"] == "centre_coordinate_query"
    assert emb.meta["query_input"] == "longitude_latitude_only"
    assert emb.meta["requested_temporal_ignored"] is True
    assert emb.meta["checkpoint"]["source"] == "local_override"


def test_batch_matches_single_queries(tiny_ckpt):
    from rs_embed.embedders.location_satclip import SatCLIPEmbedder

    e = SatCLIPEmbedder()
    sps = [PointBuffer(lon=float(x), lat=float(y), buffer_m=100) for x, y in [(0, 0), (-70, -30)]]
    batch = e.get_embeddings_batch(spatials=sps, device="cpu")
    for sp, b in zip(sps, batch, strict=False):
        one = e.get_embedding(
            spatial=sp,
            temporal=None,
            sensor=None,
            output=OutputSpec.pooled(),
            backend="auto",
            device="cpu",
        )
        np.testing.assert_allclose(b.data, one.data, rtol=1e-6)


def test_grid_output_is_north_up_cell_centres(tiny_ckpt, monkeypatch):
    from rs_embed.embedders.location_satclip import SatCLIPEmbedder

    monkeypatch.setenv("RS_EMBED_SATCLIP_GRID_STEP_M", "100")
    bbox = BBox(minlon=10.0, minlat=45.0, maxlon=10.01, maxlat=45.005)
    emb = SatCLIPEmbedder().get_embedding(
        spatial=bbox,
        temporal=None,
        sensor=None,
        output=OutputSpec.grid(),
        backend="auto",
        device="cpu",
    )
    da = emb.data
    assert da.dims == ("d", "y", "x") and da.shape[0] == 8
    assert np.all(np.diff(da["y"].values) < 0)
    assert np.all(np.diff(da["x"].values) > 0)
    assert bbox.minlat < da["y"].values.min() and da["y"].values.max() < bbox.maxlat


def test_rejects_imagery_unknown_variant_and_bad_coordinates(tiny_ckpt):
    from rs_embed.embedders.location_satclip import SatCLIPEmbedder, encode_lonlat

    e = SatCLIPEmbedder()
    sp = PointBuffer(lon=0.0, lat=0.0, buffer_m=10)
    with pytest.raises(ModelError, match="does not accept imagery"):
        e.get_embedding(
            spatial=sp,
            temporal=None,
            sensor=None,
            output=OutputSpec.pooled(),
            backend="auto",
            input_chw=np.zeros((3, 2, 2), np.float32),
        )
    with pytest.raises(ModelError, match="Unknown SatCLIP variant"):
        e.get_embedding(
            spatial=sp,
            temporal=None,
            sensor=None,
            output=OutputSpec.pooled(),
            backend="auto",
            model_config={"variant": "vit99"},
        )
    with pytest.raises(ModelError, match="out of range"):
        encode_lonlat(np.array([[200.0, 0.0]]), variant="vit16-l40", device="cpu")


def test_vendored_analytic_harmonics_cover_degree_39():
    from rs_embed.embedders._vendor.satclip.positional_encoding import spherical_harmonics_ylm

    assert hasattr(spherical_harmonics_ylm, "Yl39_m39")
    assert not hasattr(spherical_harmonics_ylm, "Yl40_m0")
    with pytest.raises(ValueError, match="legendre_polys <= 40"):
        get_positional_encoding("sphericalharmonics", 41, "analytic")


def test_encode_accepts_non_contiguous_columns(tiny_ckpt):
    from rs_embed.embedders.location_satclip import encode_lonlat

    latlon = np.array([[30.5, 114.4], [-30.0, -70.0]])
    reversed_view = latlon[:, ::-1]
    feats, _ = encode_lonlat(reversed_view, variant="vit16-l40", device="cpu")
    ref, _ = encode_lonlat(reversed_view.copy(), variant="vit16-l40", device="cpu")
    np.testing.assert_array_equal(feats, ref)
