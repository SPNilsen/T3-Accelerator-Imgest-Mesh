"""One-shot helper: generate *.thumb.png for every *.bmp in a directory.

Run from the repo root:
    python resources/camera/scripts/generate-thumbnails.py            # sample-data/ (default)
    python resources/camera/scripts/generate-thumbnails.py .data/bmp-input  # live source BMPs

Requires Pillow (already in resources/camera/requirements.txt).
This script is NOT invoked at build time — it is a developer utility for
regenerating thumbnails when new BMPs are added to any input directory.
"""
import sys
from pathlib import Path

from PIL import Image

DEFAULT_DIR = Path(__file__).parent.parent / "sample-data"
MAX_EDGE = 200


def main() -> None:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DIR

    if not target.exists():
        print(f"Directory not found: {target}")
        sys.exit(1)

    bmps = sorted(target.glob("*.bmp"))
    if not bmps:
        print(f"No .bmp files found in {target}")
        return

    print(f"Generating thumbnails in {target} ...")
    for bmp in bmps:
        thumb = bmp.parent / f"{bmp.stem}.thumb.png"
        with Image.open(bmp) as img:
            img.thumbnail((MAX_EDGE, MAX_EDGE))
            img.save(thumb, "PNG")
        print(f"  wrote {thumb.name}  ({thumb.stat().st_size} bytes)")

    print(f"Done — {len(bmps)} thumbnail(s) written.")


if __name__ == "__main__":
    main()
