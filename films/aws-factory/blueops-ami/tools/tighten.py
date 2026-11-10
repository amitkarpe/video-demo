#!/usr/bin/env python3
"""Copy assets/voice-raw/<id>.wav -> assets/voice/<id>.wav with internal silences longer than
MAX_GAP shortened to MAX_GAP (speech untouched). Writes timing.json. Deterministic."""
import json, pathlib
import numpy as np, soundfile as sf
HERE = pathlib.Path(__file__).resolve().parent.parent
MAX_GAP, WIN, THR = 0.42, 0.02, 0.012
timing = {}
for p in sorted((HERE / "assets" / "voice-raw").glob("s*.wav")):
    x, sr = sf.read(p); w = int(WIN * sr); n = len(x) // w
    loud = np.array([np.abs(x[i*w:(i+1)*w]).max() > THR for i in range(n)])
    keep, run = [], 0
    for i in range(n):
        run = 0 if loud[i] else run + 1
        if run * WIN <= MAX_GAP: keep.append(x[i*w:(i+1)*w])
    keep.append(x[n*w:]); y = np.concatenate(keep)
    sf.write(HERE / "assets" / "voice" / p.name, y, sr); timing[p.stem] = round(len(y) / sr, 3)
(HERE / "timing.json").write_text(json.dumps(timing, indent=2) + "\n")
print("speech", round(sum(timing.values()), 2), "s")
