# Wuhan Pilot Benchmark

- ROI: `roi_wuhan_east_lake.geojson`
- Grid: `10 x 10` candidates with `500 m` square buffers
- Selected tiles: `15`
- Selected class balance: `{'water': 5, 'green': 5, 'built': 5}`
- Models: `remoteclip`

| model      | status   |   elapsed_s |   per_tile_s |   peak_gpu_mb |   dim | errors   |   n_tiles_total |   n_tiles_valid |   cls_macro_f1 |   cls_balanced_acc |   built_mae |   built_rmse |   built_spearman |   green_mae |   green_rmse |   green_spearman |   water_mae |   water_rmse |   water_spearman |
|:-----------|:---------|------------:|-------------:|--------------:|------:|:---------|----------------:|----------------:|---------------:|-------------------:|------------:|-------------:|-----------------:|------------:|-------------:|-----------------:|------------:|-------------:|-----------------:|
| remoteclip | ok       |      44.591 |        2.973 |         602.6 |   512 | []       |              15 |              15 |       0.851852 |           0.888889 |    0.154605 |     0.186982 |         0.958226 |    0.192776 |     0.260487 |         0.866667 |    0.243193 |     0.299933 |         0.666886 |