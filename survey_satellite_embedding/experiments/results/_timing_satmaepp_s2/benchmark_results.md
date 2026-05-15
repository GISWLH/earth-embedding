# Wuhan Pilot Benchmark

- ROI: `roi_wuhan_east_lake.geojson`
- Grid: `10 x 10` candidates with `500 m` square buffers
- Selected tiles: `15`
- Selected class balance: `{'water': 5, 'green': 5, 'built': 5}`
- Models: `satmaepp_s2_10b`

| model           | status   |   elapsed_s |   per_tile_s |   peak_gpu_mb |   dim | errors   |   n_tiles_total |   n_tiles_valid |   cls_macro_f1 |   cls_balanced_acc |   built_mae |   built_rmse |   built_spearman |   green_mae |   green_rmse |   green_spearman |   water_mae |   water_rmse |   water_spearman |
|:----------------|:---------|------------:|-------------:|--------------:|------:|:---------|----------------:|----------------:|---------------:|-------------------:|------------:|-------------:|-----------------:|------------:|-------------:|-----------------:|------------:|-------------:|-----------------:|
| satmaepp_s2_10b | ok       |      36.925 |        2.462 |       1353.75 |  1024 | []       |              15 |              15 |              1 |                  1 |    0.066981 |    0.0828552 |         0.622295 |   0.0545261 |    0.0705852 |         0.933333 |     0.19976 |     0.263717 |         0.769484 |