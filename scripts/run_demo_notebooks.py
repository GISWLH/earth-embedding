"""Execute every guided notebook from a new kernel and retain real outputs."""

import hashlib
import importlib.metadata
import json
import platform
import sys
import time
from pathlib import Path

import nbformat
from jupyter_client import KernelManager
from nbclient import NotebookClient

root = Path(__file__).resolve().parents[1]
receipt = {
    "python": platform.python_version(),
    "platform": platform.system(),
    "packages": {
        p: importlib.metadata.version(p)
        for p in ["numpy", "scikit-learn", "torch", "matplotlib", "nbclient"]
    },
    "notebooks": [],
}
for path in sorted((root / "examples/notebooks").glob("0*.ipynb")):
    workspace = root / "work/notebook-runs" / path.stem
    workspace.mkdir(parents=True, exist_ok=True)
    nb = nbformat.read(path, as_version=4)
    start = time.perf_counter()
    manager = KernelManager(kernel_name="python3")
    # Use the invoking environment even if a user has another python3 kernelspec.
    manager.kernel_spec.argv = [
        sys.executable,
        "-m",
        "ipykernel_launcher",
        "-f",
        "{connection_file}",
    ]
    try:
        NotebookClient(
            nb, timeout=300, km=manager, resources={"metadata": {"path": str(workspace)}}
        ).execute(cleanup_kc=True)
    except Exception:
        # Keep failed evidence outside the published notebooks and fail the command.
        nbformat.write(nb, workspace / "failed.ipynb")
        raise
    nbformat.write(nb, path)
    row = {
        "name": path.name,
        "status": "passed",
        "seconds": round(time.perf_counter() - start, 2),
        "executed_cells": sum(
            c.cell_type == "code" and c.execution_count is not None for c in nb.cells
        ),
        "image_outputs": sum(
            "image/png" in o.get("data", {})
            for c in nb.cells
            if c.cell_type == "code"
            for o in c.outputs
        ),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }
    if row["image_outputs"] < 1:
        raise RuntimeError(f"{path.name}: execution produced no embedded image output.")
    receipt["notebooks"].append(row)
    print(json.dumps(row), flush=True)
out = root / "docs/validation/demo-notebooks.json"
out.write_text(json.dumps(receipt, indent=2) + "\n")
