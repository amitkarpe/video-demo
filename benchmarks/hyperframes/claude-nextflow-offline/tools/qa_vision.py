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
RULES = """Film: an animated explainer, "Nextflow Offline — Prepare Once, Run with Confidence", for managers and engineers.
Takeaway: prepare once, verify everything, run with confidence.
Owner rules for this film (deliberate, not defects):
- High-level, generic language. No code, scripts, file names, commands, IDs, hashes or dates anywhere on screen.
- GitLab is the only repository service named or shown; no other code-hosting service may appear.
- The flow is presented as one working solution with no "proposed" or status badges. The only tag allowed is "ILLUSTRATION", used on two reconstructed moments (a missing piece stopping a run; a release rejected for a fingerprint mismatch).
Accuracy rules (the film must not break these):
- Example: a germline variant-calling test from nf-core Sarek on a small public test dataset.
- GitLab hosts the workflow code repository, container registry and datasets; content is security-scanned and the operations team reviews findings. A GitLab Runner prepares the release: code to AWS CodeCommit, container images to private Amazon ECR (exact identity), and one bundle (workflow, plugins, references, data, a fingerprint per file) to Amazon S3.
- Every file and image is read back and compared before the release is registered; a mismatch stops it.
- An approved run request in GitLab starts a uniquely identified run. AWS CodePipeline has ten gated stages; AWS CodeBuild does each stage's work; AWS Systems Manager sends commands to a private EC2 host with no internet route; private endpoints connect it only to S3 and ECR.
- On the host: the bundle is checked again, exact images are loaded into an isolated store, Nextflow runs offline, plugin downloads are off, tasks have no network, no image can be pulled.
- The pipeline confirms success, offline controls and expected outputs; the answer is PASS or FAIL with an evidence report.
- Service tiles are drawn in code with names (no logos). Artwork is AI-generated and labels are code. Frames are intentionally dark and cinematic."""
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
