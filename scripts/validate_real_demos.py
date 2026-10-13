"""Network integration + exact README snippets; separate from offline unit tests."""

import argparse
import hashlib
import json
import os
import platform
import re
import tempfile
import time
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")

from earth_embedding.demo import fetch_aef_demo, load_demo

root = Path(__file__).resolve().parents[1]
workspace = root / "work/demo-live-check"
workspace.mkdir(parents=True, exist_ok=True)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--fresh", action="store_true", help="Read official COGs into a new cache.")
args = parser.parse_args()
cache = (
    Path(tempfile.mkdtemp(prefix="fresh-", dir=workspace))
    if args.fresh
    else workspace / "fresh-cache"
)
receipt = {"scope": "Actual official COG reads and README snippet execution; not unit substitutes"}
receipt["python"] = platform.python_version()
receipt["platform"] = platform.system()
start = time.perf_counter()
cache_existed = (cache / "aef-bayarea-2021.npy").exists()
fresh = fetch_aef_demo(cache)
cached = fetch_aef_demo(cache, offline=True)
np.testing.assert_array_equal(fresh.features, cached.features)
np.testing.assert_array_equal(fresh.features, load_demo("aef").features)
receipt["aef"] = {
    "status": "passed",
    "shape": list(fresh.features.shape),
    "seconds": round(time.perf_counter() - start, 2),
    "array_sha256": hashlib.sha256(fresh.features.tobytes()).hexdigest(),
    "sources": fresh.metadata["tiles"],
    "cache_existed_before_run": cache_existed,
}
blocks = []
for name in ["README.md", "README.zh-CN.md", "README.ja.md"]:
    text = (
        (root / name)
        .read_text(encoding="utf-8")
        .split("<!-- REAL_DEMOS_START -->")[1]
        .split("<!-- REAL_DEMOS_END -->")[0]
    )
    snippets = re.findall(r"```python\n(.*?)```", text, re.S)
    blocks.append(snippets)
assert blocks[0] == blocks[1] == blocks[2] and len(blocks[0]) == 3
os.chdir(workspace)
start = time.perf_counter()
for code in blocks[0]:
    exec(compile(code, "README quickstart", "exec"), {})
receipt["readme"] = {
    "status": "passed",
    "identical_languages": 3,
    "executed_snippets": 3,
    "seconds": round(time.perf_counter() - start, 2),
}
(root / "docs/validation/demo-live.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
