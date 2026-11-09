#!/usr/bin/env python3
"""QA only: ask an OpenAI vision model (gpt-5.5, Responses API) to review 720p frames for
legibility, overlap/framing and claim accuracy against the film's accuracy rules. Metered.
  python3 tools/qa_vision.py --env-file <.env> --frames review/qa/*.jpg --out review/qa-vision.json"""
import argparse, base64, json, pathlib, sys, urllib.request, urllib.error
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import ledger
HERE = pathlib.Path(__file__).resolve().parent.parent
MODEL, P_IN, P_OUT = "gpt-5.5", 5/1e6, 30/1e6
ap = argparse.ArgumentParser(); ap.add_argument("--env-file"); ap.add_argument("--frames", nargs="+", required=True); ap.add_argument("--out", required=True)
a = ap.parse_args(); key = ledger.api_key(a.env_file)
RULES = """Film: "CIS Hardening in AWS Factory — Fix What We Can, Accept What We Must", a public explainer for engineers and managers (about 50% technical).
Style: the native HyperFrames Swiss Grid look (grey grid paper, navy and gold, Helvetica, hard offset shadows) with three small AI clay illustrations. Labels and diagrams are code.
Public-output rule (deliberate): no CIS control numbers, no account/instance/image IDs, no dates, no credential details.
Accuracy rules:
- CIS = Center for Internet Security; the Amazon Linux 2023 benchmark has 243 checks across Level 1 (essential) and Level 2 (stricter).
- AWS Factory line: GovTech parent image -> base image (CIS fixes, security agents, latest patches) -> ECS, MongoDB and GitLab images -> test and share; reruns on a new parent image or new patches.
- Every check the scanner can test lands in one of three buckets: hardened upstream by GovTech; fixed by us in the base image (login lockout and password rules, file and log permissions, audit rules, unused networking off, signed package sources); accepted risk approved by the owner (separate disk partitions x5 and one user start-up file permission check: 6 controls, named in code). Square counts in the first two buckets are illustrative and labelled so; the accepted bucket is exactly 6.
- Accepted exceptions are approved by the owner, not by a security authority; the film must not imply otherwise.
- Each release reboots a test host and scans it against CIS Level 2 plus HCR checks; a failure not on the approved list stops the release; scanner FAILED labels are never relabelled.
- AI disclosure shown top right; chapter counter 01/06..06/06."""
content = [{"type": "input_text", "text": RULES + "\n\nYou are a strict broadcast QA reviewer. The frames are 1280x720 downscales of a 1080p film. "
            "For each frame report concrete problems only: text too small or low-contrast to read at 720p, overlapping/clipped elements, awkward framing, "
            "visual clutter, or any claim that breaks the rules. Return JSON: {\"frames\":[{\"file\":...,\"issues\":[{\"severity\":\"high|medium|low\",\"issue\":...,\"fix\":...}]}],\"overall\":...}. Empty issue lists are fine."}]
for f in a.frames:
    content.append({"type": "input_text", "text": "FRAME " + pathlib.Path(f).name + " (name gives the film time in seconds and the narration line it belongs to)"})
    content.append({"type": "input_image", "image_url": "data:image/jpeg;base64," + base64.b64encode(pathlib.Path(f).read_bytes()).decode(), "detail": "high"})
est = len(a.frames) * 2500 * P_IN + 2000 * P_IN + 12000 * P_OUT
idx = ledger.reserve("responses", MODEL, est, f"qa-vision:{len(a.frames)} frames")
body = {"model": MODEL, "input": [{"role": "user", "content": content}], "text": {"format": {"type": "json_object"}}, "max_output_tokens": 12000}
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
pathlib.Path(a.out).write_text(json.dumps({"model": MODEL, "usage": u, "cost_usd": cost, "review": json.loads(txt)}, indent=2) + "\n")
print("cost", round(cost, 4)); print(txt[:6000])
