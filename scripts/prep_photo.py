"""
prep_photo.py  –  run once whenever you update your photo
  1. Remove background with rembg
  2. Boost local contrast with CLAHE (gives face real shadow/highlight)
  3. Composite on white so blank areas map to spaces in the ASCII ramp
  4. Save greyscale source-prepped.png

Usage:
  python scripts/prep_photo.py source-photo.jpg
"""

import sys, io
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import remove


def prep(src: str, out: str = "source-prepped.png") -> None:
    # ── 1. Remove background ─────────────────────────────────────────
    print("Removing background …")
    raw_bytes = Path(src).read_bytes()
    no_bg_bytes = remove(raw_bytes)          # returns PNG bytes with alpha
    img = Image.open(io.BytesIO(no_bg_bytes)).convert("RGBA")

    # ── 2. Composite on pure white ───────────────────────────────────
    white = Image.new("RGBA", img.size, (255, 255, 255, 255))
    white.paste(img, mask=img.split()[3])    # use alpha as mask
    grey = white.convert("L")               # greyscale

    # ── 3. CLAHE – boosts local contrast, rescues flat lighting ──────
    arr = np.array(grey, dtype=np.uint8)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(arr)

    # ── 4. Save ───────────────────────────────────────────────────────
    Image.fromarray(enhanced).save(out)
    print(f"  ✓  Saved → {out}")


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
    prep(src)
