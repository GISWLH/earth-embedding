from __future__ import annotations

import numpy as np
import pandas as pd

from survey_satellite_embedding.experiments.run_wuhan_t1_classification import (
    CLASSES,
    build_labels_and_splits,
    compute_classification_metrics,
    validate_split_table,
)


def _manifest_like() -> pd.DataFrame:
    rows = []
    for row in range(41):
        for cls in CLASSES:
            rows.append(
                {
                    "tile_id": f"tile_r{row:03d}_{cls}",
                    "row": row,
                    "col": len(rows) % 4,
                    "center_lon": 114.3,
                    "center_lat": 30.5,
                    "minlon": 114.3,
                    "minlat": 30.5,
                    "maxlon": 114.31,
                    "maxlat": 30.51,
                    "local_dominant_class": cls,
                    "local_dominant_frac": 0.75,
                    "local_built_frac": 0.0,
                    "local_vegetation_frac": 0.0,
                    "local_cropland_frac": 0.0,
                    "local_water_frac": 0.0,
                    "jrc_occurrence_mean": 0.0,
                    "jrc_water_binary_frac": 0.0,
                }
            )
    return pd.DataFrame(rows)


def test_build_labels_and_splits_uses_row_contiguous_spatial_split() -> None:
    labels = build_labels_and_splits(_manifest_like(), confidence_threshold=0.5)

    assert set(labels.loc[labels["row"] <= 23, "split"]) == {"train"}
    assert set(labels.loc[labels["row"].between(24, 31), "split"]) == {"val"}
    assert set(labels.loc[labels["row"] >= 32, "split"]) == {"test"}
    assert labels["use_for_t1"].all()
    validate_split_table(labels)


def test_confidence_threshold_marks_low_confidence_tiles_unused() -> None:
    df = _manifest_like()
    df.loc[0, "local_dominant_frac"] = 0.25

    labels = build_labels_and_splits(df, confidence_threshold=0.5)

    assert not bool(labels.loc[0, "use_for_t1"])
    assert labels.loc[1:, "use_for_t1"].all()


def test_compute_classification_metrics_reports_macro_f1_and_confusion() -> None:
    y_true = np.array([0, 0, 1, 1, 2, 2, 3, 3])
    y_pred = np.array([0, 1, 1, 1, 2, 0, 3, 2])

    metrics = compute_classification_metrics(y_true, y_pred)

    assert metrics["confusion_matrix"] == [
        [1, 1, 0, 0],
        [0, 2, 0, 0],
        [1, 0, 1, 0],
        [0, 0, 1, 1],
    ]
    assert 0.0 <= metrics["macro_f1"] <= 1.0
    assert 0.0 <= metrics["balanced_accuracy"] <= 1.0
    assert metrics["per_class"]["built"]["support"] == 2
