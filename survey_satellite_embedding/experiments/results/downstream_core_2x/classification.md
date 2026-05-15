# Wuhan 2x T1 Land-Cover Classification

- Dataset: current Wuhan 2x public-19 window from `manifest_2x.json`
- Tiles: `567` 500 m tiles from the WorldCover-derived manifest
- Ground truth: `local_dominant_class` aggregated from ESA WorldCover 2021
- Classes: `built`, `vegetation`, `cropland`, `water`
- Split: fixed stratified random split shared by all models; this keeps the rare cropland class in train/val/test
- Caveat: cropland has only 5 tiles in this 2x window, so macro F1 is intentionally strict but has high variance for that class

## Class Balance

| split   |   built |   cropland |   vegetation |   water |
|:--------|--------:|-----------:|-------------:|--------:|
| test    |      48 |          1 |           40 |      24 |
| train   |     145 |          3 |          120 |      73 |
| val     |      48 |          1 |           40 |      24 |

## Ranked Test Results

| model           | status   | head   |   dim |   best_epoch |   train_macro_f1 |   val_macro_f1 |   test_macro_f1 |   test_balanced_accuracy |   test_accuracy |   knn5_test_macro_f1 |   knn5_test_balanced_accuracy |
|:----------------|:---------|:-------|------:|-------------:|-----------------:|---------------:|----------------:|-------------------------:|----------------:|---------------------:|------------------------------:|
| gse             | ok       | linear |    64 |          136 |         0.804844 |       0.875951 |        0.890427 |                 0.970833 |        0.955752 |             0.713735 |                      0.716667 |
| anysat          | ok       | linear |  1536 |           16 |         0.855995 |       0.677142 |        0.83582  |                 0.917708 |        0.884956 |             0.640479 |                      0.634375 |
| tessera         | ok       | linear |   128 |           39 |         0.754299 |       0.824084 |        0.830245 |                 0.951042 |        0.929204 |             0.69263  |                      0.691667 |
| thor            | ok       | linear |   768 |           20 |         0.916275 |       0.902031 |        0.6815   |                 0.677083 |        0.893805 |             0.653687 |                      0.647917 |
| terramind       | ok       | linear |   384 |           17 |         0.90511  |       0.887958 |        0.671386 |                 0.667708 |        0.884956 |             0.68793  |                      0.688542 |
| prithvi         | ok       | linear |   768 |           42 |         0.998098 |       0.790231 |        0.666392 |                 0.664583 |        0.884956 |             0.647894 |                      0.647917 |
| terrafm         | ok       | linear |   768 |           68 |         1        |       0.929397 |        0.666352 |                 0.667708 |        0.884956 |             0.660461 |                      0.661458 |
| wildsat         | ok       | linear |   768 |           12 |         0.825782 |       0.767235 |        0.640778 |                 0.635417 |        0.840708 |             0.622724 |                      0.620833 |
| dofa            | ok       | linear |   768 |           21 |         0.843718 |       0.78369  |        0.640453 |                 0.638542 |        0.840708 |             0.632164 |                      0.629167 |
| agrifm          | ok       | linear |  1024 |           56 |         0.865037 |       0.84245  |        0.639678 |                 0.6375   |        0.840708 |             0.627357 |                      0.623958 |
| galileo         | ok       | linear |   128 |           91 |         0.598214 |       0.575402 |        0.531895 |                 0.517708 |        0.672566 |             0.500906 |                      0.496875 |
| satvision       | ok       | linear |  4096 |           41 |         0.64315  |       0.730426 |        0.481986 |                 0.5      |        0.637168 |             0.513254 |                      0.520833 |
| remoteclip      | ok       | linear |   768 |            9 |         0.629936 |       0.592214 |        0.47921  |                 0.457292 |        0.60177  |             0.55374  |                      0.55625  |
| scalemae        | ok       | linear |  1024 |          183 |         0.660222 |       0.584133 |        0.474665 |                 0.479167 |        0.619469 |             0.474394 |                      0.479167 |
| fomo            | ok       | linear |   768 |           28 |         0.651862 |       0.703711 |        0.415455 |                 0.457292 |        0.566372 |             0.496997 |                      0.501042 |
| satmaepp_s2_10b | ok       | linear |  1024 |           24 |         0.748317 |       0.38439  |        0.336889 |                 0.35     |        0.451327 |             0.328356 |                      0.332292 |
| satmaepp        | ok       | linear |  1024 |           75 |         0.962397 |       0.330526 |        0.305374 |                 0.313542 |        0.40708  |             0.325586 |                      0.340625 |
| copernicus      | ok       | linear |   768 |            9 |         0.306986 |       0.334971 |        0.293257 |                 0.2625   |        0.362832 |             0.228384 |                      0.2375   |
| satmae          | ok       | linear |  1024 |            3 |         0.227776 |       0.180052 |        0.159444 |                 0.358333 |        0.150442 |             0.239131 |                      0.251042 |

## All Rows

| model           | status   | head   |   dim |   best_epoch |   train_macro_f1 |   val_macro_f1 |   test_macro_f1 |   test_balanced_accuracy |   test_accuracy |   knn5_test_macro_f1 |   knn5_test_balanced_accuracy |
|:----------------|:---------|:-------|------:|-------------:|-----------------:|---------------:|----------------:|-------------------------:|----------------:|---------------------:|------------------------------:|
| gse             | ok       | linear |    64 |          136 |         0.804844 |       0.875951 |        0.890427 |                 0.970833 |        0.955752 |             0.713735 |                      0.716667 |
| remoteclip      | ok       | linear |   768 |            9 |         0.629936 |       0.592214 |        0.47921  |                 0.457292 |        0.60177  |             0.55374  |                      0.55625  |
| copernicus      | ok       | linear |   768 |            9 |         0.306986 |       0.334971 |        0.293257 |                 0.2625   |        0.362832 |             0.228384 |                      0.2375   |
| tessera         | ok       | linear |   128 |           39 |         0.754299 |       0.824084 |        0.830245 |                 0.951042 |        0.929204 |             0.69263  |                      0.691667 |
| satmae          | ok       | linear |  1024 |            3 |         0.227776 |       0.180052 |        0.159444 |                 0.358333 |        0.150442 |             0.239131 |                      0.251042 |
| satmaepp        | ok       | linear |  1024 |           75 |         0.962397 |       0.330526 |        0.305374 |                 0.313542 |        0.40708  |             0.325586 |                      0.340625 |
| satmaepp_s2_10b | ok       | linear |  1024 |           24 |         0.748317 |       0.38439  |        0.336889 |                 0.35     |        0.451327 |             0.328356 |                      0.332292 |
| scalemae        | ok       | linear |  1024 |          183 |         0.660222 |       0.584133 |        0.474665 |                 0.479167 |        0.619469 |             0.474394 |                      0.479167 |
| anysat          | ok       | linear |  1536 |           16 |         0.855995 |       0.677142 |        0.83582  |                 0.917708 |        0.884956 |             0.640479 |                      0.634375 |
| galileo         | ok       | linear |   128 |           91 |         0.598214 |       0.575402 |        0.531895 |                 0.517708 |        0.672566 |             0.500906 |                      0.496875 |
| wildsat         | ok       | linear |   768 |           12 |         0.825782 |       0.767235 |        0.640778 |                 0.635417 |        0.840708 |             0.622724 |                      0.620833 |
| prithvi         | ok       | linear |   768 |           42 |         0.998098 |       0.790231 |        0.666392 |                 0.664583 |        0.884956 |             0.647894 |                      0.647917 |
| terrafm         | ok       | linear |   768 |           68 |         1        |       0.929397 |        0.666352 |                 0.667708 |        0.884956 |             0.660461 |                      0.661458 |
| terramind       | ok       | linear |   384 |           17 |         0.90511  |       0.887958 |        0.671386 |                 0.667708 |        0.884956 |             0.68793  |                      0.688542 |
| dofa            | ok       | linear |   768 |           21 |         0.843718 |       0.78369  |        0.640453 |                 0.638542 |        0.840708 |             0.632164 |                      0.629167 |
| fomo            | ok       | linear |   768 |           28 |         0.651862 |       0.703711 |        0.415455 |                 0.457292 |        0.566372 |             0.496997 |                      0.501042 |
| thor            | ok       | linear |   768 |           20 |         0.916275 |       0.902031 |        0.6815   |                 0.677083 |        0.893805 |             0.653687 |                      0.647917 |
| agrifm          | ok       | linear |  1024 |           56 |         0.865037 |       0.84245  |        0.639678 |                 0.6375   |        0.840708 |             0.627357 |                      0.623958 |
| satvision       | ok       | linear |  4096 |           41 |         0.64315  |       0.730426 |        0.481986 |                 0.5      |        0.637168 |             0.513254 |                      0.520833 |

## Main Artifacts

- Metrics CSV: `classification.csv`
- Per-model predictions: `classification_predictions_{model}.csv`
- Combined map: `figures/classification_maps_public19_2x.png`
- Reference-layout acceptance map: `figures/classification_public19_models_2x_reference_layout.png`
- Accuracy barplot: `figures/classification_accuracy_barplot_public19_2x.png`
- Per-model maps: `figures/classification_map_{model}.png`