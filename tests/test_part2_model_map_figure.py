from survey_satellite_embedding.experiments.make_part2_model_map_figure import (
    format_model_panel_title,
)
from survey_satellite_embedding.experiments.make_part2_region_b_model_map_figure import (
    embedding_rgb,
    format_embedding_shape,
)


def test_format_model_panel_title_includes_shape() -> None:
    result = {"model": "thor", "shape": [768, 18, 18]}

    assert format_model_panel_title(result) == "thor [768*18*18]"


def test_format_model_panel_title_falls_back_to_model_name() -> None:
    result = {"model": "tessera", "status": "failed"}

    assert format_model_panel_title(result) == "tessera"


def test_format_embedding_shape_uses_matrix_dimensions() -> None:
    assert format_embedding_shape([[0.0] * 768] * 15) == "15*768"


def test_embedding_rgb_handles_single_embedding() -> None:
    colors = embedding_rgb([[1.0, 2.0, 3.0]])

    assert colors.shape == (1, 3)
