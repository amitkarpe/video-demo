#!/usr/bin/env python3
"""Generate one local Kokoro WAV per script line. No network, no API, no account.

Usage (inside a venv with kokoro-onnx==0.6.1 and soundfile==0.14.0):
  python tts.py --model kokoro-v1.0.onnx --voices voices-v1.0.bin
Writes assets/kokoro/voice-<id>.wav and timing.kokoro.json (offline FALLBACK; copy to assets/ + timing.json to use) (durations in seconds).
"""
import argparse, hashlib, json, pathlib, sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

HERE = pathlib.Path(__file__).resolve().parent
EXPECTED = {  # model-files-v1.1 release assets, sha256 recorded in README.md
    "kokoro-v1.0.onnx": "beb0d1848dee9a49da392cc3df26958d46cfa35d321edf434f52949153f0df3a",
    "voices-v1.0.bin": "bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d",
}

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

ap = argparse.ArgumentParser()
ap.add_argument("--model", required=True)
ap.add_argument("--voices", required=True)
ap.add_argument("--only", nargs="*", help="regenerate only these line ids")
a = ap.parse_args()
for p in (a.model, a.voices):
    name = pathlib.Path(p).name
    if EXPECTED.get(name) != sha(p):
        sys.exit(f"SHA-256 mismatch for {name}; refusing to run")

script = json.loads((HERE / "script.json").read_text())
voice, speed = script["voice"], script["speed"]
lang = "en-us" if voice.startswith("a") else "en-gb"
k = Kokoro(a.model, a.voices)
out = HERE / "assets" / "kokoro"
out.mkdir(parents=True, exist_ok=True)
tfile = HERE / "timing.kokoro.json"
timing = json.loads(tfile.read_text()) if tfile.exists() else {}
for line in script["lines"]:
    if a.only and line["id"] not in a.only:
        continue
    samples, sr = k.create(line["speak"], voice=voice, speed=speed, lang=lang)
    # trim leading/trailing near-silence (keep 60 ms head, 140 ms tail); pauses are set by gap_after
    loud = np.where(np.abs(samples) > 0.01)[0]
    if len(loud):
        samples = samples[max(0, loud[0] - int(0.06 * sr)): loud[-1] + int(0.14 * sr)]
    sf.write(out / f"voice-{line['id']}.wav", samples, sr)
    timing[line["id"]] = round(len(samples) / sr, 3)
    print(line["id"], timing[line["id"]], "s")
tfile.write_text(json.dumps(timing, indent=2) + "\n")
