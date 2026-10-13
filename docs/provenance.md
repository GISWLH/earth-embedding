# Provenance and attribution

Earth Embedding is an independent derivative of **[rs-embed](https://github.com/cybergis/rs-embed)**, created by Dingqi Ye and contributors in the CyberGIS community. The project was developed under the GISWLH/rs-embed repository name and has been renamed **[GISWLH/earth-embedding](https://github.com/GISWLH/earth-embedding)**. The original framework and its authors remain credited; renaming the repository does not change authorship of inherited work.

## Relationship to the upstream project

The upstream project established a geographic request interface for remote sensing embeddings, reusable spatial/temporal/output specifications, model adapters, data-provider integration, and batch/export workflows. This extension retains that foundation and the compatible `rs_embed` import path. The new `earth_embedding` import and `earth-embedding` command identify the maintained extension.

The upstream publication is:

> Ye, D., Kiv, D., Hu, W., Shi, J., and Wang, S. (2026). *Any Model, Any Place, Any Time: Get Remote Sensing Foundation Model Embeddings On Demand*. arXiv:2602.23678.

[Read the original paper](https://arxiv.org/abs/2602.23678). This is the original project's publication, not the Earth Embedding manuscript. No endorsement by the upstream authors is implied.

## Additions in this extension

| Area | Extension |
| --- | --- |
| Release taxonomy | Image encoders, location encoders, and precomputed products, with input-contract subclasses |
| Location access | SatCLIP integration and a shared batch coordinate API; additional GeoCLIP and lightweight Esri GLE adapters |
| Local imagery | A public image-array route with explicit spatial/temporal context and model-specific preprocessing |
| AlphaEarth access | Official GCS footprint discovery and COG point sampling, including decoding and nodata handling |
| Research documentation | Distinct global/local evaluation scopes, frozen benchmark set, and evidence boundaries |
| Release presentation | English, Chinese, and Japanese homepages; original editable Excalidraw artwork |
| Validation | Dated test and runtime receipts, with optional dependencies and access failures kept explicit |

The 16 image configurations and established precomputed routes build on inherited adapters and subsequent project work. The entire model roster should not be represented as newly invented by this extension. See the changelog, source history, and individual model pages for component-level detail.

## Software, model, and data licenses

The repository's [Apache-2.0 license](https://github.com/GISWLH/earth-embedding/blob/main/LICENSE) and [NOTICE](https://github.com/GISWLH/earth-embedding/blob/main/NOTICE) preserve upstream attribution. They do not grant rights to every external model or dataset accessed by the package.

| Component | Source / terms |
| --- | --- |
| Inherited rs-embed framework | [CyberGIS rs-embed](https://github.com/cybergis/rs-embed); Apache-2.0 |
| Bundled model code | Original notices and licenses in `src/rs_embed/embedders/_vendor/` |
| GeoCLIP | [Official implementation](https://github.com/VicenteVivan/geo-clip); retain its MIT notice and cite its authors |
| SatCLIP | [Microsoft SatCLIP](https://github.com/microsoft/satclip); source/checkpoint terms apply |
| Esri Global Location Encoder | [Official model documentation](https://doc.arcgis.com/en/pretrained-models/latest/vector/introduction-to-global-location-encoder-sentinel-2-.htm); Esri software and model terms apply separately |
| Google Satellite Embedding | [Official GCS guide](https://developers.google.com/earth-engine/guides/aef_on_gcs_readme); CC-BY-4.0 with required attribution |
| Original artwork | Repository Apache-2.0; embedded fonts retain separate licenses listed in the [artwork guide](assets/earth-embedding-brand.md) |

The Esri adapter downloads Esri's official model package on demand and runs its location encoder with the bundled MIT-licensed SatCLIP architecture. The repository does not redistribute Esri checkpoints or claim that their license is Apache-2.0. The package and checkpoint hashes are pinned in the adapter and documented on the [Esri model page](models/esri_gle.md). Public download access does not replace the model's usage terms.

For AlphaEarth data, retain Google's required acknowledgement:

> The AlphaEarth Foundations Satellite Embedding dataset is produced by Google and Google DeepMind.

## How to cite

Cite **Earth Embedding** as software using the repository URL and the commit or release used. [CITATION.cff](https://github.com/GISWLH/earth-embedding/blob/main/CITATION.cff) provides metadata for this extension and references the original framework. Until a release DOI or public manuscript record exists, do not invent one.

Also cite the original rs-embed publication and each model or data publication used in the analysis. This separates framework authorship, integration work, and the scientific contribution embodied in pretrained weights or embedding products.

## Reporting lineage problems

If an attribution, source link, or license boundary is incomplete, [open an issue](https://github.com/GISWLH/earth-embedding/issues) with the affected file and primary source. Contributions should preserve author notices, document substantial modifications, and keep checkpoint/data licensing separate from package licensing.
