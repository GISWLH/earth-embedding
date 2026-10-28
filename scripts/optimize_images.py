"""Shrink committed PNG figures without visible quality loss.

python -m pip install imagequant pyoxipng pillow
python scripts/optimize_images.py docs/assets examples   # PNG files and notebook outputs

Each PNG is palette-quantized (libimagequant, dithered, quality floor 80; lower it
with --min-quality for photographic images) and then losslessly recompressed with
oxipng. A result is kept only when it is at least 10% smaller, so rerunning the
script is safe. Executed notebooks are handled the same way for their embedded
image/png outputs.
"""

import argparse
import base64
import io
import json
from pathlib import Path

import imagequant
import oxipng
from PIL import Image


def shrink(raw: bytes, min_quality: int = 80) -> bytes:
    """Return optimized PNG bytes, or the input when optimization does not pay off."""
    image = Image.open(io.BytesIO(raw))
    image.load()
    try:
        quantized = imagequant.quantize_pil_image(
            image.convert("RGBA"), dithering_level=1.0, max_colors=256, min_quality=min_quality
        )
        buffer = io.BytesIO()
        quantized.save(buffer, format="PNG")
        candidate = buffer.getvalue()
    except RuntimeError:  # Quality floor not reachable with 256 colors; stay lossless.
        candidate = raw
    candidate = oxipng.optimize_from_memory(candidate, level=4, strip=oxipng.StripChunks.safe())
    return candidate if len(candidate) < 0.9 * len(raw) else raw


def optimize_png(path: Path, min_quality: int = 80) -> tuple[int, int]:
    raw = path.read_bytes()
    result = shrink(raw, min_quality)
    if result is not raw:
        path.write_bytes(result)
    return len(raw), len(result)


def optimize_notebook(path: Path, min_quality: int = 80) -> tuple[int, int]:
    before = path.stat().st_size
    notebook = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for cell in notebook.get("cells", []):
        for output in cell.get("outputs", []):
            data = output.get("data", {})
            if "image/png" not in data:
                continue
            encoded = data["image/png"]
            encoded = "".join(encoded) if isinstance(encoded, list) else encoded
            raw = base64.b64decode(encoded)
            result = shrink(raw, min_quality)
            if result is not raw:
                data["image/png"] = base64.b64encode(result).decode("ascii")
                changed = True
    if changed:
        # Same layout as nbformat.write, so optimization adds no formatting churn.
        text = json.dumps(notebook, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
        path.write_text(text, encoding="utf-8", newline="\n")
    return before, path.stat().st_size


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument(
        "--min-quality", type=int, default=80, help="lower for photographic images (0-100)"
    )
    args = parser.parse_args()
    total_before = total_after = 0
    for root in args.paths:
        files = [root] if root.is_file() else sorted(root.rglob("*"))
        for path in files:
            if path.suffix == ".png":
                before, after = optimize_png(path, args.min_quality)
            elif path.suffix == ".ipynb":
                before, after = optimize_notebook(path, args.min_quality)
            else:
                continue
            total_before += before
            total_after += after
            if after < before:
                print(f"{before / 1024:8.0f} KB -> {after / 1024:6.0f} KB  {path}")
    print(f"total {total_before / 1048576:.2f} MB -> {total_after / 1048576:.2f} MB")


if __name__ == "__main__":
    main()
