#!/usr/bin/env python3
"""Labelled review sheets from the HyperFrames snapshots (needs Pillow).
  python phase1/make_sheets.py  -> phase1/style-options.jpg, phase1/storyboard.jpg"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
SNAP = HERE / "_snap"
W, H = 960, 540  # each frame at half size
try:
    F = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 34)
    f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 26)
except OSError:
    F = f = ImageFont.load_default()

def frames(d):
    return sorted((SNAP / d).glob("frame-*.png"))

def sheet(paths, cols, labels, head, out, rowlabels=None):
    rows = (len(paths) + cols - 1) // cols
    lw = 330 if rowlabels else 0
    img = Image.new("RGB", (lw + cols * (W + 16) + 16, 90 + rows * (H + 60)), "#1c1a24")
    d = ImageDraw.Draw(img)
    d.text((24, 24), head, font=F, fill="#ffffff")
    for i, p in enumerate(paths):
        r, c = divmod(i, cols)
        x, y = lw + 16 + c * (W + 16), 90 + r * (H + 60)
        img.paste(Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS), (x, y))
        d.text((x, y + H + 12), labels[i], font=f, fill="#d9d4e8")
    for r, t in enumerate(rowlabels or []):
        d.multiline_text((24, 90 + r * (H + 60) + H // 2 - 40), t, font=F, fill="#ffffff", spacing=8)
    img.save(out, quality=88)
    print(out, img.size)

sheet(frames("styles"), 2, ["two roads", "the rules gate"] * 3, "Patching film · 3 looks in Three.js (same scene, same frames)",
      HERE / "style-options.jpg", ["A · Pastel\ndiorama\n(recommended)", "B · Blueprint\nisometric", "C · Bold toy\nblocks"])
names = ["1 · The question", "2 · Two roads", "3 · Patch groups", "4 · The rules", "5 · The weekend window", "6 · The trap", "7 · The check", "8 · Close"]
sheet(frames("storyboard"), 2, names, "Patching film · storyboard in look A (8 slides)", HERE / "storyboard.jpg")
