# Wuhan Pilot Benchmark

- ROI: `roi_wuhan_east_lake.geojson`
- Grid: `10 x 10` candidates with `500 m` square buffers
- Selected tiles: `15`
- Selected class balance: `{'water': 5, 'green': 5, 'built': 5}`
- Models: `galileo`

| model   | status   |   elapsed_s |   per_tile_s |   peak_gpu_mb |   dim | errors   |   n_tiles_total |   n_tiles_valid |   cls_macro_f1 |   cls_balanced_acc |   built_mae |   built_rmse |   built_spearman |   green_mae |   green_rmse |   green_spearman |   water_mae |   water_rmse |   water_spearman |
|:--------|:---------|------------:|-------------:|--------------:|------:|:---------|----------------:|----------------:|---------------:|-------------------:|------------:|-------------:|-----------------:|------------:|-------------:|-----------------:|------------:|-------------:|-----------------:|
| galileo | ok       |      87.626 |        5.842 |        277.27 |   128 | []       |              15 |              15 |              1 |                  1 |     0.13016 |     0.160791 |         0.688096 |   0.0918515 |     0.110346 |              0.7 |    0.237565 |     0.305039 |         0.341993 |