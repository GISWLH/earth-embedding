# Part-2 All-Model Smoke Extraction

- Data dir: `survey_satellite_embedding/data/part2_20260502_full`
- Models: `gse, satmaepp_s2_10b, copernicus`
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

| model           | split    | status   | type        |   elapsed_s |   per_item_s |   peak_gpu_mb |   dim |   n_items | errors   | sample_id_col   |
|:----------------|:---------|:---------|:------------|------------:|-------------:|--------------:|------:|----------:|:---------|:----------------|
| gse             | region_a | ok       | precomputed |      30.107 |        1.882 |          0    |    64 |        16 | []       | tile_id         |
| satmaepp_s2_10b | region_a | ok       | onthefly    |      64.139 |        4.009 |       1353.75 |  1024 |        16 | []       | tile_id         |
| copernicus      | region_b | ok       | precomputed |      19.422 |        1.295 |       1265.43 |   768 |        15 | []       | cell_id         |