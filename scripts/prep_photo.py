#!/usr/bin/env python3
"""Prepare source-photo.png for the animated ASCII portrait.

The supplied cutout has a light checkerboard baked into the image. This script
turns those light background tiles into white, boosts contrast, and pads the
portrait to a square grayscale canvas for make_ascii_svg.py.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageEnhance, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

# Flood-fill only the light background connected to the top-left edge. This keeps
# highlights and skin tones intact while replacing the flat backdrop with white.
BACKGROUND_TOLERANCE = 28

image = Image.open(INP).convert("RGB")
gray = ImageOps.grayscale(image)
ImageDraw.floodfill(gray, (0, 0), 255, thresh=BACKGROUND_TOLERANCE)
gray = ImageEnhance.Contrast(gray).enhance(1.12)

side = max(gray.size)
square = Image.new("L", (side, side), 255)
square.paste(gray, ((side - gray.width) // 2, (side - gray.height) // 2))
square = ImageEnhance.Sharpness(square).enhance(1.15)
square.save(OUT)
print(f"wrote {OUT}: {side} x {side}")
