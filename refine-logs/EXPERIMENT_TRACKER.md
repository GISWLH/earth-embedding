# Experiment Tracker

| Run ID | Milestone | Purpose | System / Variant | Split | Metrics | Priority | Status | Notes |
|--------|-----------|---------|------------------|-------|---------|----------|--------|-------|
| R001 | M0 | Build Region A manifest | Wuhan `500 m` grid + dominant-label filtering | candidate grid | class balance, label purity | MUST | DONE | Built at `survey_satellite_embedding/data/part2_20260502_full/region_a/tile_manifest_500m.csv` with 2173 tiles; class counts built 1078 / vegetation 625 / water 409 / cropland 61 |
| R002 | M0 | Build Region B manifest | Yangtze `0.25 degree` cells + aggregated labels | candidate grid | class balance, coverage | MUST | DONE | Built at `survey_satellite_embedding/data/part2_20260502_full/region_b/cell_manifest_025deg.csv` with 1056 cells; compatible with `copernicus` smoke extraction |
| R003 | M0 | Build Region A temporal manifest | pre / post pairs inside Wuhan ROI for water-change task | candidate pairs | pair count, label quality | MUST | TODO | Start with seasonal water change |
| R004 | M0 | Sanity-check metrics | spectral baseline on Region A | train / val / test | macro F1, RMSE | MUST | TODO | Confirms labels are non-trivial |
| R005 | M1 | Smoke-test local extraction | `gse`, `satmaepp_s2_10b`, `remoteclip`, `galileo`, `agrifm` | 8 sample tiles | pass / fail, time, GPU MB | MUST | DONE | Generalized to `run_part2_all_models_smoke.py`; current run produced fresh Region A embeddings for 16 local-scale models under `survey_satellite_embedding/experiments/results/all_models_smoke_20260502` |
| R006 | M1 | Smoke-test coarse extraction | `copernicus`, `satvision`, `gse`, `tessera` | 8 sample cells | pass / fail, time, coverage | MUST | DONE | Fresh Region B smoke passed for `copernicus`, `satvision`, and `tessera`; `tessera` was completed by directly pooling local `global_0.1_degree_representation` files from the cached 2024 anchor tile set |
| R007 | M2 | Main local classification | representative cohort + spectral baseline | Region A split | macro F1, balanced accuracy | MUST | TODO | First core table |
| R008 | M2 | Main local regression | representative cohort + spectral baseline | Region A split | RMSE, MAE, Spearman | MUST | TODO | Built / green / water fractions |
| R009 | M2 | Main dense segmentation | dense-capable subset vs pooled broadcast | Region A dense split | IoU, F1, boundary F1 | MUST | TODO | Keeps segmentation in the core story |
| R010 | M3 | Temporal change detection | temporal-capable cohort + paired-feature baseline | Region A temporal split | F1, IoU, precision / recall | MUST | TODO | First temporal task |
| R011 | M3 | Main regional classification | representative cohort, then all 19 if stable | Region B split | macro F1, balanced accuracy | MUST | TODO | Critical for scale-fair claim |
| R012 | M3 | Main regional regression | representative cohort, then all 19 if stable | Region B split | RMSE, MAE, Spearman | MUST | TODO | Include runtime and failure rate |
| R013 | M4 | Object detection extension | local annotated building / large-object subset | Region A detection split | AP, AP50, recall | NICE | TODO | Needed for explicit task-family coverage |
| R014 | M4 | Temporal sequence extension | crop-type or phenology subset | Region A temporal-sequence split | macro F1 or MAE | NICE | TODO | Separate from binary change detection |
| R015 | M4 | Probe simplicity ablation | linear vs MLP vs k-NN | same splits as R007 and R011 | macro F1, train time | MUST | TODO | Decide whether linear-only story is safe |
| R016 | M5 | Family-specific retrieval | `remoteclip`, `wildsat` on fixed tile bank | retrieval set | Recall@K, median rank | NICE | TODO | Appendix by default |
| R017 | M5 | Full 19-model regional extension | all remaining models | Region B split | same as R011 / R012 | NICE | TODO | Run only after core tables are stable |
