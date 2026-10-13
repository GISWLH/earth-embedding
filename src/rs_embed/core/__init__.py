"""
Domain Definitions and Data Contracts.

This module defines the immutable "Nouns" of the system:

- **Specs**: Data contracts (``SpatialSpec``, ``SensorSpec``, ``OutputSpec``,
  ``TemporalSpec``, ``InputPrepSpec``).
- **Types**: Return types (``Embedding``) and configuration hints
  (``ExportConfig``, ``ExportTarget``, ``ExportModelRequest``, ``ModelConfig``).
- **Errors**: Custom exception hierarchy (``SpecError``, ``ProviderError``).

Rules
-----
- **Pure data only** — no processing logic, no heavy imports.
- **Zero cross-package dependencies** — this module must *never* import from
  ``pipelines``, ``providers``, ``embedders``, or ``tools``.
"""
