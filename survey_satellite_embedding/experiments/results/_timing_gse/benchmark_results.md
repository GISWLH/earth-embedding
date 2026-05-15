# Wuhan Pilot Benchmark

- ROI: `roi_wuhan_east_lake.geojson`
- Grid: `10 x 10` candidates with `500 m` square buffers
- Selected tiles: `15`
- Selected class balance: `{'water': 5, 'green': 5, 'built': 5}`
- Models: `gse`

| model   | status   |   elapsed_s |   per_tile_s |   peak_gpu_mb |   dim | errors   |   n_tiles_total |   n_tiles_valid |   cls_macro_f1 |   cls_balanced_acc |   built_mae |   built_rmse |   built_spearman |   green_mae |   green_rmse |   green_spearman |   water_mae |   water_rmse |   water_spearman |
|:--------|:---------|------------:|-------------:|--------------:|------:|:---------|----------------:|----------------:|---------------:|-------------------:|------------:|-------------:|-----------------:|------------:|-------------:|-----------------:|------------:|-------------:|-----------------:|
| gse     | ok       |      35.628 |        2.375 |             0 |    64 | []       |              15 |              12 |              1 |                  1 |   0.0514598 |    0.0609418 |         0.849561 |   0.0898927 |     0.104118 |              0.6 |    0.297155 |     0.347721 |         0.316228 |