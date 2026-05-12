"""One-shot helper: generate *.thumb.png for every *.bmp in sample-data/.

Run from the repo root:
    python resources/camera/scripts/generate-thumbnails.py

Requires Pillow (already in resources/camera/requirements.txt).
This script is NOT invoked at build time — it is a developer utility for
regenerating thumbnails when new sample BMPs are added to sample-data/.
"""
from pathlib import Path

from PIL import Image

SAMPLE = Path(__file__).parent.parent / "sample-data"
MAX_EDGE = 200


def main() -> None:
    bmps = sorted(SAMPLE.glob("*.bmp"))
    if not bmps:
        print(f"No .bmp files found in {SAMPLE}")
        return

    for bmp in bmps:
        thumb = bmp.parent / f"{bmp.stem}.thumb.png"
        with Image.open(bmp) as img:
            img.thumbnail((MAX_EDGE, MAX_EDGE))
            img.save(thumb, "PNG")
        print(f"  wrote {thumb.name}  ({thumb.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
