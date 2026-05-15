# Satellite Embedding: A Review

## Positioning

This paper should read like a remote sensing review, not like a computer vision taxonomy memo. The narrative should therefore follow a **total-sub-total** logic:

1. first explain the overall evolution of satellite embeddings as a field;
2. then split the landscape into a few major model families;
3. within each family, discuss data, architecture, representation form, and deployment characteristics;
4. finally return to cross-family comparison, downstream use, and future outlook.

The key shift is that internal scaffolding headings such as `Why a dossier is necessary` or `Implications for the rest of the review` should not appear as top-level paper sections. Those are author-facing notes, not reader-facing survey structure.

## Recommended Survey Logic

### 1. Introduction

- Motivate why satellite embeddings have become a practical interface for Earth observation.
- State the gap: current surveys focus on foundation models broadly, but practitioners consume embeddings.
- Summarize contributions: a unified taxonomy, a model inventory, a benchmark plan, and an interactive access layer.

### 2. Overall Landscape of Satellite Embeddings

- Briefly define what a satellite embedding is.
- Show the overall field evolution with a timeline figure.
- Introduce the main design axes:
  - spatial scale and resolution
  - modality and sensor support
  - temporal semantics
  - deployment form: on-the-fly encoder vs. precomputed product

This section should be concise and synthetic. It is the “总” part.

### 3. Model Families of Satellite Embeddings

This is the main “分” part of the paper. Split models into a few broad families and discuss each family in the same order:

- representative models
- data sources and sensor assumptions
- architecture and pretraining signal
- representation form
- strengths, limits, and typical use cases

Recommended family split:

1. precomputed embedding products and annual fields
2. masked autoencoder and pure vision encoders
3. vision-language and cross-modal embedding models
4. multimodal generalist EO encoders
5. domain-specialized embedding models

### 4. Cross-Family Comparison

- Present the main summary table.
- Compare models along common dimensions:
  - data scale
  - modality breadth
  - temporal modeling
  - embedding form
  - inference cost and deployment style
- Add the resolution-modality matrix here.

This section is where the reader should quickly understand the whole landscape without reading every model paper.

### 5. Data Resources and Application Space

- Summarize the main pretraining data regimes and sensor resources used in the field.
- Organize downstream tasks by application family:
  - classification and mapping
  - segmentation and dense prediction
  - regression and continuous estimation
  - retrieval and multimodal interaction
- Emphasize which families of embeddings are naturally better suited to which tasks.

### 6. Comparative Evaluation Protocol

- Introduce the study area and benchmark protocol.
- Explain why a compact mixed-landscape ROI is useful.
- Define the first-pass evaluation tasks and metrics.
- Keep this section practical and reproducible.

### 7. Interactive Access Platform

- Describe the Leaflet-based explorer as the software layer of the review.
- Explain how model metadata, ROI selection, embedding extraction, and task launching connect.

### 8. Challenges and Future Directions

- temporal ambiguity
- scale mismatch
- modality alignment and metadata integration
- benchmark realism
- embedding products versus checkpoints

### 9. Conclusion

- Return to the central argument: satellite embeddings are a representation layer, not just a by-product of foundation models.

## Figure Logic

- **Fig. 1**: concept map of the field
- **Fig. 2**: model timeline
- **Fig. 3**: resolution-modality matrix
- **Fig. 4**: application / benchmark pipeline
- **Fig. 5**: interactive system overview

## Table Logic

- **Table 1**: main-text cross-family model summary
- **Table 2**: appendix-level implementation-oriented long table

## Writing Principle

The paper should feel like:

- one overall story about the rise of satellite embeddings;
- several family-level subsections that readers can skim independently;
- one synthesis section that compares families;
- one application and benchmarking section that connects the literature to practice.

That structure is much closer to how remote sensing review papers usually read than a flat taxonomy-first outline with many meta-headings.
