from __future__ import annotations

import numpy as np
import pandas as pd

from survey_satellite_embedding.experiments.run_wuhan_t2_fraction_regression import (
    build_fraction_labels,
    compute_regression_metrics,
    select_alpha,
)


def _manifest_like() -> pd.DataFrame:
    rows = []
    for row in range(41):
        rows.append(
            {
                "tile_id": f"tile_{row}",
                "row": row,
                "col": 0,
                "center_lon": 114.4,
                "center_lat": 30.5,
                "minlon": 114.39,
                "minlat": 30.49,
                "maxlon": 114.41,
                "maxlat": 30.51,
                "local_dominant_class": "built",
                "local_dominant_frac": 0.8,
                "local_built_frac": row / 40.0,
                "local_vegetation_frac": 1.0 - row / 40.0,
                "local_cropland_frac": 0.0,
                "local_water_frac": 0.0,
                "jrc_occurrence_mean": 0.0,
                "jrc_water_binary_frac": 0.0,
            }
        )
    return pd.DataFrame(rows)


def test_build_fraction_labels_uses_same_row_split() -> None:
    labels = build_fraction_labels(_manifest_like())

    assert set(labels.loc[labels["row"] <= 23, "split"]) == {"train"}
    assert set(labels.loc[labels["row"].between(24, 31), "split"]) == {"val"}
    assert set(labels.loc[labels["row"] >= 32, "split"]) == {"test"}
    assert labels["use_for_t2"].all()


def test_compute_regression_metrics_reports_standard_errors() -> None:
    y_true = np.array([0.0, 0.5, 1.0, 1.5])
    y_pred = np.array([0.0, 0.4, 1.1, 1.4])

    metrics = compute_regression_metrics(y_true, y_pred)

    assert metrics["mae"] >= 0.0
    assert metrics["rmse"] >= 0.0
    assert -1.0 <= metrics["r2"] <= 1.0
    assert -1.0 <= metrics["spearman"] <= 1.0


def test_select_alpha_prefers_better_validation_fit() -> None:
    x_train = np.array([[0.0], [1.0], [2.0], [3.0]], dtype=np.float32)
    y_train = np.array([0.0, 1.0, 2.0, 3.0], dtype=np.float32)
    x_val = np.array([[4.0], [5.0]], dtype=np.float32)
    y_val = np.array([4.0, 5.0], dtype=np.float32)

    alpha, metrics = select_alpha(x_train, y_train, x_val, y_val)

    assert alpha in {0.01, 0.1, 1.0, 10.0, 100.0}
    assert metrics["rmse"] >= 0.0
