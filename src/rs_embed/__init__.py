"""rs-embed — location embeddings from remote-sensing imagery.

This top-level package re-exports the public API surface so that users can
write ``from rs_embed import Model, BBox`` without reaching into subpackages.

See :mod:`rs_embed.api` for the function-based API and :class:`rs_embed.Model`
for the class-based (stateful) interface.
"""

from ._version import __version__
from .aef import AEF_INDEX_URL, dequantize_aef, find_aef_tiles, sample_aef
from .api import (
    describe_model,
    export_batch,
    get_embedding,
    get_embeddings_batch,
    list_models,
    reset_runtime,
)
from .comparison import EmbeddingComparison, compare_embeddings, plot_embedding_comparison
from .core.specs import (
    BBox,
    FetchSpec,
    InputPrepSpec,
    OutputSpec,
    PointBuffer,
    SensorSpec,
    TemporalSpec,
)
from .core.types import (
    ExportConfig,
    ExportLayout,
    ExportModelRequest,
    ExportTarget,
    ModelConfig,
)
from .embedders.location_api import get_location_embeddings
from .export import export_npz
from .image import get_image_embedding
from .inspect import inspect_gee_patch, inspect_provider_patch
from .load import ExportResult, ModelResult, load_export
from .model import Model
from .pipelines.exporter import BatchExporter
from .resources import get_model_resources, list_model_resources

__all__ = [
    # Specs
    "BBox",
    "PointBuffer",
    "TemporalSpec",
    "SensorSpec",
    "FetchSpec",
    "OutputSpec",
    "InputPrepSpec",
    # Types
    "ExportConfig",
    "ExportLayout",
    "ExportModelRequest",
    "ExportTarget",
    "ModelConfig",
    # Embedding API (class-based)
    "Model",
    "BatchExporter",
    # Embedding API (function-based, backward compat)
    "get_embedding",
    "get_embeddings_batch",
    "list_models",
    "describe_model",
    "reset_runtime",
    "EmbeddingComparison",
    "compare_embeddings",
    "plot_embedding_comparison",
    "get_model_resources",
    "list_model_resources",
    # Export API
    "export_batch",
    "export_npz",
    # Load API
    "load_export",
    "ExportResult",
    "ModelResult",
    # Inspection
    "inspect_provider_patch",
    # Backward-compatible alias for inspect_provider_patch
    "inspect_gee_patch",
    "__version__",
    "AEF_INDEX_URL",
    "dequantize_aef",
    "find_aef_tiles",
    "sample_aef",
    "get_location_embeddings",
    "get_image_embedding",
]
