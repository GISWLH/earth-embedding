# Wuhan Pilot Benchmark

- ROI: `roi_wuhan_east_lake.geojson`
- Grid: `10 x 10` candidates with `500 m` square buffers
- Selected tiles: `6`
- Selected class balance: `{'water': 2, 'green': 2, 'built': 2}`
- Models: `gse, remoteclip`

| model      | status   |   elapsed_s |   per_tile_s |   peak_gpu_mb |   dim | errors   |   n_tiles_total |   n_tiles_valid |   cls_macro_f1 |   cls_balanced_acc |   built_mae |   built_rmse |   built_spearman |   green_mae |   green_rmse |   green_spearman |   water_mae |   water_rmse |   water_spearman |
|:-----------|:---------|------------:|-------------:|--------------:|------:|:---------|----------------:|----------------:|---------------:|-------------------:|------------:|-------------:|-----------------:|------------:|-------------:|-----------------:|------------:|-------------:|-----------------:|
| remoteclip | ok       |      32.948 |        5.491 |        600.82 |   512 | []       |               6 |               6 |              1 |                  1 |    0.232892 |     0.282141 |                1 |    0.253523 |     0.282365 |                1 |    0.281597 |     0.345868 |         0.333333 |
| gse        | ok       |      19.558 |        3.26  |          0    |    64 | []       |               6 |               5 |            nan |                nan |    0.133017 |     0.173181 |                1 |    0.279446 |     0.317354 |                0 |    0.268279 |     0.296667 |         0        |