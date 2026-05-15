# Part-2 All-Model Smoke Extraction

- Data dir: `survey_satellite_embedding/data/part2_20260502_full`
- Models: `tessera`
- Region A samples: `16`
- Region B samples: `15`

## Region A sample balance

| local_dominant_class   |   count |
|:-----------------------|--------:|
| built                  |       4 |
| vegetation             |       4 |
| cropland               |       4 |
| water                  |       4 |

## Region B sample balance

| regional_dominant_class   |   count |
|:--------------------------|--------:|
| water                     |       4 |
| forest_green              |       4 |
| cropland                  |       4 |
| built                     |       3 |

## Extraction summary

| model           | split    | status   | type        |   elapsed_s |   per_item_s |   peak_gpu_mb |   dim |   n_items | errors   | sample_id_col   | notes                                          |
|:----------------|:---------|:---------|:------------|------------:|-------------:|--------------:|------:|----------:|:---------|:----------------|:-----------------------------------------------|
| gse             | region_a | ok       | precomputed |      23.07  |        1.442 |       1570.94 |    64 |        16 | []       | tile_id         | nan                                            |
| fomo            | region_a | ok       | on_the_fly  |      25.08  |        1.567 |       1577.03 |   768 |        16 | []       | tile_id         | nan                                            |
| prithvi         | region_a | ok       | onthefly    |      27.984 |        1.749 |       2061.03 |   768 |        16 | []       | tile_id         | nan                                            |
| satmaepp_s2_10b | region_a | ok       | onthefly    |      29.667 |        1.854 |       6446.29 |  1024 |        16 | []       | tile_id         | nan                                            |
| wildsat         | region_a | ok       | on_the_fly  |      31.977 |        1.999 |        707.43 |   256 |        16 | []       | tile_id         | nan                                            |
| terrafm         | region_a | ok       | on_the_fly  |      32.121 |        2.008 |      17910.3  |   768 |        16 | []       | tile_id         | nan                                            |
| scalemae        | region_a | ok       | onthefly    |      36.188 |        2.262 |      17456.6  |  1024 |        16 | []       | tile_id         | nan                                            |
| dofa            | region_a | ok       | on_the_fly  |      36.322 |        2.27  |       1353.81 |   768 |        16 | []       | tile_id         | nan                                            |
| satmae          | region_a | ok       | onthefly    |      37.962 |        2.373 |       3877.21 |  1024 |        16 | []       | tile_id         | nan                                            |
| satmaepp        | region_a | ok       | onthefly    |      39.306 |        2.457 |       5135.84 |  1024 |        16 | []       | tile_id         | nan                                            |
| thor            | region_a | ok       | on_the_fly  |      41.053 |        2.566 |        404.36 |   768 |        16 | []       | tile_id         | nan                                            |
| remoteclip      | region_a | ok       | on_the_fly  |      49.005 |        3.063 |       2597.81 |   512 |        16 | []       | tile_id         | nan                                            |
| galileo         | region_a | ok       | on_the_fly  |      59.969 |        3.748 |       1836.64 |   128 |        16 | []       | tile_id         | nan                                            |
| terramind       | region_a | ok       | on_the_fly  |      61.263 |        3.829 |      17992.8  |   384 |        16 | []       | tile_id         | nan                                            |
| anysat          | region_a | ok       | on_the_fly  |      75.656 |        4.729 |        939.67 |   768 |        16 | []       | tile_id         | nan                                            |
| agrifm          | region_a | ok       | on_the_fly  |      94.56  |        5.91  |        591.05 |  1024 |        16 | []       | tile_id         | nan                                            |
| tessera         | region_b | ok       | precomputed |       5.048 |        5.048 |          0    |   128 |         1 | []       | anchor_id       | ['direct geotessera cache pooling workaround'] |
| copernicus      | region_b | ok       | precomputed |      11.115 |        0.741 |        883.18 |   768 |        15 | []       | cell_id         | nan                                            |
| satvision       | region_b | ok       | on_the_fly  |      98.751 |        6.583 |      16376.2  |  4096 |        15 | []       | cell_id         | nan                                            |