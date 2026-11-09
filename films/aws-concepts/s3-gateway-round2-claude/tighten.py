#!/usr/bin/env python3
"""Shorten long internal pauses inside each narration clip (any silent run > MAX_GAP s
becomes MAX_GAP s) and rewrite timing.json. Speech itself is untouched. Idempotent."""
import json, pathlib
import numpy as np, soundfile as sf
HERE = pathlib.Path(__file__).resolve().parent
MAX_GAP, WIN, THR = 0.30, 0.02, 0.012
timing = json.loads((HERE / "timing.json").read_text())
for cid in timing:
    p = HERE / "assets" / f"voice-{cid}.wav"
    x, sr = sf.read(p)
    w = int(WIN * sr); n = len(x) // w
    loud = np.array([np.abs(x[i*w:(i+1)*w]).max() > THR for i in range(n)])
    keep, run = [], 0
    for i in range(n):
        run = 0 if loud[i] else run + 1
        if run * WIN <= MAX_GAP:
            keep.append(x[i*w:(i+1)*w])
    keep.append(x[n*w:])
    y = np.concatenate(keep)
    sf.write(p, y, sr)
    old, timing[cid] = timing[cid], round(len(y) / sr, 3)
    print(cid, old, "->", timing[cid])
(HERE / "timing.json").write_text(json.dumps(timing, indent=2) + "\n")
