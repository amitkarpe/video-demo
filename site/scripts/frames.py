#!/usr/bin/env python3
"""Make the small JPG frames the site shows: 4 per public film, taken from the public release MP4 (no download of the whole
file; ffmpeg seeks with HTTP range requests). Frame 2 is the card poster.
  python3 scripts/frames.py            # only missing frames
  python3 scripts/frames.py --force    # all again
  python3 scripts/frames.py <slug>...  # some films
Output: public/frames/<slug>-<1..4>.jpg (640 px wide, about 30-60 KB each). Needs ffmpeg and ffprobe."""
import json, pathlib, subprocess, sys

SITE = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((SITE / "src/data/videos.json").read_text())
OUT = SITE / "public/frames"
OUT.mkdir(parents=True, exist_ok=True)
force = "--force" in sys.argv
only = [a for a in sys.argv[1:] if not a.startswith("--")]
SPOTS = (0.12, 0.37, 0.63, 0.88)

for v in DATA["videos"]:
    if not v.get("public") or not v.get("mp4") or (only and v["slug"] not in only):
        continue
    want = [OUT / f"{v['slug']}-{i}.jpg" for i in range(1, 5)]
    if not force and all(p.exists() for p in want):
        continue
    dur = v.get("durationSec") or float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", v["mp4"]],
        check=True, capture_output=True, text=True).stdout)
    for p, f in zip(want, SPOTS):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{dur * f:.2f}", "-i", v["mp4"], "-frames:v", "1",
                        "-vf", "scale=640:-2", "-q:v", "5", str(p)], check=True)
    print(f"{v['slug']}: {sum(p.stat().st_size for p in want) // 1024} KB")
