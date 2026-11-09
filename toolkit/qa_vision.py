#!/usr/bin/env python3
"""QA only: ask an OpenAI vision model (gpt-5.5, Responses API) to review 720p frames for
legibility, overlap/framing and claim accuracy against the film's accuracy rules. Metered.
  python3 tools/qa_vision.py --env-file <.env> --frames review/qa/*.jpg --out review/qa-vision.json"""
import argparse, base64, json, pathlib, sys, urllib.request, urllib.error
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import ledger
from film import film_dir
HERE = film_dir()
MODEL, P_IN, P_OUT = "gpt-5.5", 5/1e6, 30/1e6
ap = argparse.ArgumentParser(); ap.add_argument("--env-file"); ap.add_argument("--frames", nargs="+", required=True); ap.add_argument("--out", required=True)
a = ap.parse_args(); key = ledger.api_key(a.env_file)
RULES_FILE = HERE / "review" / "qa-rules.md"   # the film's style, public-output and accuracy rules for the reviewer
if not RULES_FILE.exists(): sys.exit(f"missing {RULES_FILE}: write the film's QA rules first (see toolkit/README.md)")
RULES = RULES_FILE.read_text().strip()
content = [{"type": "input_text", "text": RULES + "\n\nYou are a strict broadcast QA reviewer. The frames are 1280x720 downscales of a 1080p film. "
            "For each frame report concrete problems only: text too small or low-contrast to read at 720p, overlapping/clipped elements, awkward framing, "
            "visual clutter, or any claim that breaks the rules. Return JSON: {\"frames\":[{\"file\":...,\"issues\":[{\"severity\":\"high|medium|low\",\"issue\":...,\"fix\":...}]}],\"overall\":...}. Empty issue lists are fine."}]
for f in a.frames:
    content.append({"type": "input_text", "text": "FRAME " + pathlib.Path(f).name + " (name gives the film time in seconds and the narration line it belongs to)"})
    content.append({"type": "input_image", "image_url": "data:image/jpeg;base64," + base64.b64encode(pathlib.Path(f).read_bytes()).decode(), "detail": "high"})
est = len(a.frames) * 2500 * P_IN + 2000 * P_IN + 32000 * P_OUT
idx = ledger.reserve("responses", MODEL, est, f"qa-vision:{len(a.frames)} frames")
body = {"model": MODEL, "input": [{"role": "user", "content": content}], "text": {"format": {"type": "json_object"}}, "max_output_tokens": 32000}
req = urllib.request.Request("https://api.openai.com/v1/responses", json.dumps(body).encode(), {"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=600) as r: res = json.loads(r.read())
except urllib.error.HTTPError as ex:
    m = ex.read().decode()[:400]; ledger.settle(idx, f"HTTP_{ex.code}", extra={"error": m}); sys.exit(m)
except Exception as ex:
    ledger.settle(idx, "UNKNOWN", extra={"error": type(ex).__name__}); sys.exit("stopped, not retried")
u = res.get("usage", {}); cost = u.get("input_tokens", 0) * P_IN + u.get("output_tokens", 0) * P_OUT
ledger.settle(idx, "ACK", cost=cost, usage=u)
txt = "".join(c.get("text", "") for o in res.get("output", []) if o.get("type") == "message" for c in o.get("content", []))
pathlib.Path(a.out).with_suffix(".raw.txt").write_text(txt + "\n\nstatus: " + str(res.get("status")) + " " + json.dumps(res.get("incomplete_details")))
pathlib.Path(a.out).write_text(json.dumps({"model": MODEL, "usage": u, "cost_usd": cost, "review": json.loads(txt)}, indent=2) + "\n")
print("cost", round(cost, 4)); print(txt[:6000])
