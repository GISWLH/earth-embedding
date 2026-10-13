import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

spec = importlib.util.spec_from_file_location(
    "evaluate_embeddings", Path(__file__).parents[1] / "examples/evaluate_embeddings.py"
)
evaluation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluation)


def metadata():
    return pd.DataFrame(
        {
            "sample_id": ["a", "b", "c", "d"],
            "target": [0, 1, 0, 1],
            "split": ["train", "train", "test", "test"],
            "spatial_group": ["west", "west", "east", "east"],
        }
    )


def test_alignment_uses_sample_ids_and_common_finite_cohort():
    ids = np.array(["d", "c", "b", "a"])
    x = np.array([[4.0], [3.0], [2.0], [1.0]])
    y = np.array([[np.nan], [3.0], [2.0], [1.0]])
    cohort, arrays = evaluation.align_cohort(metadata(), {"first": (ids, x), "second": (ids, y)})
    assert cohort.sample_id.tolist() == ["a", "b", "c"]
    np.testing.assert_array_equal(arrays["first"].ravel(), [1, 2, 3])


def test_spatial_leakage_rejected():
    frame = metadata()
    frame.loc[3, "spatial_group"] = "west"
    with pytest.raises(ValueError, match="Spatial leakage"):
        evaluation.align_cohort(frame, {"model": (frame.sample_id, np.ones((4, 2)))})


def test_fixed_classification_probe():
    pytest.importorskip("sklearn")
    frame = metadata()
    report = evaluation.evaluate(
        frame, {"model": (frame.sample_id, np.array([[0], [1], [0], [1]]))}, task="classification"
    )
    assert report["results"][0]["accuracy"] == 1
    assert report["matched_rows"] == 4
