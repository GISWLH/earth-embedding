# Research scope and evidence

Earth Embedding connects manuscript work to reusable software through a release-object taxonomy, explicit input contracts, and documented extraction provenance. The repository's implementation scope and the manuscript's evaluated system set are tracked separately.

The manuscript is being developed for submission to Remote Sensing of Environment. This page is not a claim of acceptance, publication, completed review, or final comparative rankings. The [rs-embed paper](https://arxiv.org/abs/2602.23678) belongs to the original CyberGIS project and must not be presented as our manuscript.

## Taxonomy based on the delivered object

| Class | What the user receives | Query input | Subclasses |
| --- | --- | --- | --- |
| A · Image encoders | Weights and preprocessing contract | Satellite pixels | A1 RGB; A2 fixed-schema multispectral; A3 channel-adaptive; A4 multitemporal sequence |
| B · Location encoders | A learned location-mapping network | Longitude and latitude | SatCLIP, GeoCLIP, Esri Global Location Encoder are examples |
| C · Precomputed embedding products | Spatially indexed embedding vectors | A point or bounding box | C1 gridded fields; C2 sampled collections |

Class assignment follows the specific release and evaluated configuration. An image model and a derived precomputed product can belong to different classes. Temporal input takes precedence over spectral flexibility when assigning an A subclass. Architecture, training objective, output geometry, spatial support, and temporal coverage are facets, rather than competing top-level categories. Eligibility for a controlled comparison is a separate status.

The manuscript taxonomy was frozen on **2026-10-09**. Changes to the software catalog do not silently revise that decision.

## Evaluated systems and integrations

The frozen benchmark set contains **20 systems**:

- **A1, five:** RemoteCLIP, SatMAE, SatMAE++ RGB, Scale-MAE, WildSAT.
- **A2, five:** SatMAE++ Sentinel-2 10-band, Prithvi-EO-2.0, TerraMind, TerraFM, SatVision-TOA.
- **A3, three:** DOFA, FoMo, THOR.
- **A4, three:** Galileo, AnySat, AgriFM.
- **B, one:** SatCLIP, with the configured checkpoint/variant recorded in each run.
- **C1, three:** GSE (AlphaEarth Foundations v2.1 annual), TESSERA v1.1, Copernicus-Embed-025deg.

The software catalog adds **GeoCLIP** and **Esri GLE**, bringing it to **22 adapters**. They are not automatically included in the frozen benchmark. C2 is part of the taxonomy; this release does not claim an implemented C2 adapter or a benchmarked C2 system.

SatVision-TOA and Copernicus-Embed keep their A2 and C1 assignments even when they are ineligible for a particular controlled comparison because spatial support is unmatched. A raster resampling operation does not remove this mismatch.

## Global and local evaluation

The revised main design uses **globally distributed 640 m spatial units**. It is intended to support comparisons across geographic contexts with documented label joins, matched support, and spatial holdouts. Model availability, task eligibility, and the completeness of extracted data must be recorded before reporting comparative results.

Wuhan provides local and historical diagnostic materials, including a **567-tile** subset and a **2,173-tile** ROI design. These scopes have different extents and completion states. The existence of a manifest does not establish that all embeddings were extracted; results for the 567-tile subset do not establish results for the full ROI. Local results do not substitute for evidence from the revised global design.

| Evaluation dimension | Intended question | Required evidence |
| --- | --- | --- |
| Land-cover classification | Are pooled features useful for semantic discrimination? | Label provenance, spatial split, fixed estimator/protocol |
| Fraction regression | Do features capture built-up, vegetation, and water composition? | Support-matched fractions, held-out predictions, metric definition |
| Water masks / segmentation | Do available dense features retain spatial structure? | Dense-output eligibility, geometry alignment, task-specific evaluation |
| Retrieval and map inspection | Which similarities or geographic patterns are represented? | Defined query/gallery scope and documented qualitative selection |
| Access and computation | What does a reproducible extraction require? | Checkpoints, data source, bytes, cache state, runtime, hardware, failures |

These dimensions describe the evaluation framework. This page does not assert that every model has completed every task.

## What is reusable in the library?

The [model catalog](models.md) exposes input differences rather than hiding them. `get_image_embedding` supports user-provided imagery; `get_location_embeddings` provides a common location query; geographic and precomputed routes preserve source metadata. Direct AEF COG access enables workflows outside Earth Engine while retaining the official quantization and masking conventions.

For a reproducible experiment, save the repository commit, exact model/checkpoint revision, input bands and units, temporal window, spatial support, query geometry, provider/data version, output metadata, spatial split, and downstream estimator settings. Record failures and exclusions explicitly. A model that cannot access its data in one environment should not be silently converted into a scientific exclusion.

### Run a small evaluation on your own features

The repository's [evaluation script](https://github.com/GISWLH/earth-embedding/blob/main/examples/evaluate_embeddings.py) compares saved NPZ feature matrices against a metadata CSV. Each NPZ contains `X` and `sample_id`; metadata contains `sample_id,target,split,spatial_group`. Supply an externally defined spatial holdout with `train` and `test` rows and disjoint spatial groups.

```bash
python -m pip install -e ".[benchmark]"
python examples/evaluate_embeddings.py --metadata metadata.csv --features satclip=satclip.npz geoclip=geoclip.npz --task classification --out evaluation.json
```

The script retains a common finite cohort across models, aligns rows by ID, checks group separation, fits scaling and a linear estimator on training rows only, and records input/cohort hashes. Regression is available through `--task regression`. Users provide task labels, features, and a meaningful split. This executable example is not a reproduction of manuscript scores.

## Reading validation correctly

The [validation report](validation.md) distinguishes software regression tests, actual model inference, and live provider queries. A mocked dependency test checks error handling or interface behavior. A successful inference checks that one configuration produces a valid output. A live GCS query checks one data path. None of these by itself establishes downstream accuracy, fairness of a comparison, or a final scientific claim.

When citing the project, cite this software version, the upstream framework, and the individual model/data sources actually used. A separate manuscript citation will be added when a public bibliographic record is available. See [provenance](provenance.md).
