# Wuhan Pilot Benchmark

- ROI: `roi_wuhan_east_lake.geojson`
- Grid: `10 x 10` candidates with `500 m` square buffers
- Selected tiles: `15`
- Selected class balance: `{'water': 5, 'green': 5, 'built': 5}`
- Models: `agrifm`

| model   | status   |   elapsed_s |   per_tile_s |   peak_gpu_mb |   dim | errors   |   n_tiles_total |   n_tiles_valid |   cls_macro_f1 |   cls_balanced_acc |   built_mae |   built_rmse |   built_spearman |   green_mae |   green_rmse |   green_spearman |   water_mae |   water_rmse |   water_spearman |
|:--------|:---------|------------:|-------------:|--------------:|------:|:---------|----------------:|----------------:|---------------:|-------------------:|------------:|-------------:|-----------------:|------------:|-------------:|-----------------:|------------:|-------------:|-----------------:|
| agrifm  | ok       |       88.68 |        5.912 |        591.05 |  1024 | []       |              15 |              15 |              1 |                  1 |     0.18507 |     0.238268 |          0.79156 |   0.0764346 |    0.0916576 |              0.3 |    0.579381 |     0.836085 |         0.119697 |