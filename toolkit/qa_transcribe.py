#!/usr/bin/env python3
"""QA only: transcribe the final film audio with OpenAI gpt-transcribe and compare to the spoken script text (WER). Metered.
  python3 tools/qa_transcribe.py --env-file <.env> --audio <file.mp3> --minutes <float> --out review/qa-transcribe.json"""
import argparse, json, pathlib, re, sys, urllib.request, urllib.error, uuid
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import ledger
from film import film_dir
HERE = film_dir()
ap = argparse.ArgumentParser(); ap.add_argument("--env-file"); ap.add_argument("--audio", required=True); ap.add_argument("--minutes", type=float, required=True); ap.add_argument("--out", required=True)
a = ap.parse_args(); key = ledger.api_key(a.env_file)
MODEL, PER_MIN = "gpt-transcribe", 0.0045
idx = ledger.reserve("audio/transcriptions", MODEL, (a.minutes + 1) * PER_MIN * 2, "qa-transcribe")
b = uuid.uuid4().hex; data = pathlib.Path(a.audio).read_bytes()
body = (f'--{b}\r\nContent-Disposition: form-data; name="model"\r\n\r\n{MODEL}\r\n'
        f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="{pathlib.Path(a.audio).name}"\r\nContent-Type: audio/mpeg\r\n\r\n').encode() + data + f"\r\n--{b}--\r\n".encode()
req = urllib.request.Request("https://api.openai.com/v1/audio/transcriptions", body, {"Authorization": f"Bearer {key}", "Content-Type": f"multipart/form-data; boundary={b}"})
try:
    with urllib.request.urlopen(req, timeout=600) as r: res = json.loads(r.read())
except urllib.error.HTTPError as ex:
    m = ex.read().decode()[:400]; ledger.settle(idx, f"HTTP_{ex.code}", extra={"error": m}); sys.exit(m)
except Exception as ex:
    ledger.settle(idx, "UNKNOWN", extra={"error": type(ex).__name__}); sys.exit("stopped, not retried")
u = res.get("usage"); cost = a.minutes * PER_MIN
if u and u.get("type") == "duration": cost = u.get("seconds", a.minutes * 60) / 60 * PER_MIN
ledger.settle(idx, "ACK", cost=cost, usage=u)
w = lambda s: re.sub(r"[^a-z0-9 ]", " ", re.sub(r"[-–—]", " ", s.lower())).split()
S = json.loads((HERE / "script.json").read_text())
ref, hyp = w(" ".join(l.get("say", l["caption"]) for l in S["lines"])), w(res.get("text", ""))
import difflib
sm = difflib.SequenceMatcher(None, ref, hyp); errs = sum(max(i2 - i1, j2 - j1) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal")
diffs = [(op, " ".join(ref[i1:i2]), " ".join(hyp[j1:j2])) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
out = {"model": MODEL, "usage": u, "cost_usd": cost, "ref_words": len(ref), "word_errors": errs, "wer": round(errs / max(1, len(ref)), 4), "diffs": diffs, "text": res.get("text")}
pathlib.Path(a.out).write_text(json.dumps(out, indent=2) + "\n"); print(json.dumps({k: out[k] for k in ("wer", "word_errors", "ref_words", "cost_usd")}), diffs[:40])
