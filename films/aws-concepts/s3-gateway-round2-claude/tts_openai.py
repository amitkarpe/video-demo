#!/usr/bin/env python3
"""Generate narration with OpenAI TTS (metered). The key is read from an env file
or the environment and is NEVER printed or written. The API returns audio bytes
with no usage counts, so spend is bounded by a deliberately high pre-call estimate
recorded in spend-ledger.json; the run aborts before any call that could pass the ceiling.

  python3 tts_openai.py --env-file ~/git/video-demo/.env [--only s05 s07] [--ceiling 0.50]
Writes assets/voice-<id>.wav, timing.json, spend-ledger.json.
"""
import argparse, io, json, os, pathlib, sys, time, urllib.request, urllib.error, wave
HERE = pathlib.Path(__file__).resolve().parent
PRICE_TEXT, PRICE_AUDIO = 0.60 / 1e6, 12.0 / 1e6   # USD per token (published gpt-4o-mini-tts rates)
AUDIO_TOK_PER_SEC = 100      # conservative upper bound (real rate is lower, ~50)
ap = argparse.ArgumentParser()
ap.add_argument("--env-file"); ap.add_argument("--only", nargs="*")
ap.add_argument("--ceiling", type=float, default=1.00, help="self-imposed spend stop (USD); owner cap is 5.00")
a = ap.parse_args()
key = os.environ.get("OPENAI_API_KEY")
if not key and a.env_file:
    for ln in pathlib.Path(a.env_file).expanduser().read_text().splitlines():
        if ln.startswith("OPENAI_API_KEY="):
            key = ln.split("=", 1)[1].strip().strip('"').strip("'")
if not key:
    sys.exit("OPENAI_API_KEY missing; no call made")
script = json.loads((HERE / "script.json").read_text())
cfg = script["openai"]
lf = HERE / "spend-ledger.json"
ledger = json.loads(lf.read_text()) if lf.exists() else {"model": cfg["model"], "calls": [], "estimated_usd": 0.0}
def est(text):
    words = len(text.split())
    secs = max(3.0, 1.0 * words)                         # generous: 1 s per word
    tin = (len(text) + len(cfg["instructions"])) / 3     # generous token count
    return tin * PRICE_TEXT + secs * AUDIO_TOK_PER_SEC * PRICE_AUDIO
out = HERE / "assets"; tfile = HERE / "timing.json"
timing = json.loads(tfile.read_text()) if tfile.exists() else {}
for line in script["lines"]:
    if a.only and line["id"] not in a.only: continue
    text = line.get("speak", line["caption"])
    e = est(text)
    if ledger["estimated_usd"] + e > a.ceiling:
        sys.exit(f"STOP before {line['id']}: estimate {ledger['estimated_usd']+e:.4f} > ceiling {a.ceiling}")
    body = json.dumps({"model": cfg["model"], "voice": cfg["voice"], "input": text,
                       "instructions": cfg["instructions"], "response_format": cfg["response_format"]}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/audio/speech", body,
          {"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    # count the attempt BEFORE the call (an unacknowledged call may still bill)
    ledger["estimated_usd"] = round(ledger["estimated_usd"] + e, 6)
    rec = {"id": line["id"], "est_usd": round(e, 6), "chars": len(text), "status": "CALLING", "t": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    ledger["calls"].append(rec); lf.write_text(json.dumps(ledger, indent=2) + "\n")
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            audio = r.read()
        rec["status"] = "ACK"
    except urllib.error.HTTPError as ex:
        rec["status"] = f"HTTP_{ex.code}"; lf.write_text(json.dumps(ledger, indent=2) + "\n"); sys.exit(f"{line['id']}: HTTP {ex.code}; stopped")
    except Exception as ex:
        rec["status"] = "UNKNOWN"; lf.write_text(json.dumps(ledger, indent=2) + "\n"); sys.exit(f"{line['id']}: {type(ex).__name__}; stopped (unmetered/unknown)")
    import numpy as np, soundfile as sf
    x, sr = sf.read(io.BytesIO(audio))
    if x.ndim > 1: x = x.mean(axis=1)
    loud = np.where(np.abs(x) > 0.01)[0]
    if len(loud): x = x[max(0, loud[0] - int(0.06 * sr)): loud[-1] + int(0.14 * sr)]
    sf.write(out / f"voice-{line['id']}.wav", x, sr)
    timing[line["id"]] = round(len(x) / sr, 3); rec["seconds"] = timing[line["id"]]
    lf.write_text(json.dumps(ledger, indent=2) + "\n"); print(line["id"], timing[line["id"]], "s", "est", round(e, 4))
tfile.write_text(json.dumps(timing, indent=2) + "\n")
print("estimated upper-bound spend USD", ledger["estimated_usd"])
