#!/usr/bin/env python3
"""Generate/edit images with OpenAI gpt-image-2.6-sunburst (metered). Reads prompts/images.json.
  python3 tools/gen_images.py --env-file <.env> --only hero_factory
Writes assets/gen/<id>.png and prompts/image-provenance.json (prompt sha256, usage, output sha256)."""
import argparse, base64, hashlib, json, pathlib, sys, urllib.request, urllib.error, uuid
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import ledger
HERE = pathlib.Path(__file__).resolve().parent.parent
MODEL = "gpt-image-2.6-sunburst"
P_TXT_IN, P_IMG_IN, P_IMG_OUT = 5/1e6, 8/1e6, 30/1e6   # published USD/token rates
ap = argparse.ArgumentParser(); ap.add_argument("--env-file"); ap.add_argument("--only", nargs="*")
ap.add_argument("--reserve-out-tokens", type=int, default=40000, help="conservative output-token reservation per image")
a = ap.parse_args()
spec = json.loads((HERE / "prompts" / "images.json").read_text())
prov_f = HERE / "prompts" / "image-provenance.json"
prov = json.loads(prov_f.read_text()) if prov_f.exists() else {}
key = ledger.api_key(a.env_file)
style = spec["style"]
def multipart(fields, files):
    b = uuid.uuid4().hex; out = b""
    for k, v in fields.items():
        out += f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    for k, (fn, data, ct) in files.items():
        out += f'--{b}\r\nContent-Disposition: form-data; name="{k}"; filename="{fn}"\r\nContent-Type: {ct}\r\n\r\n'.encode() + data + b"\r\n"
    return out + f"--{b}--\r\n".encode(), f"multipart/form-data; boundary={b}"
for item in spec["images"]:
    if a.only and item["id"] not in a.only: continue
    prompt = style + " " + item["prompt"]
    est = len(prompt) / 3 * P_TXT_IN + a.reserve_out_tokens * P_IMG_OUT + (8000 * P_IMG_IN if item.get("edit_from") else 0)
    idx = ledger.reserve("images/" + ("edits" if item.get("edit_from") else "generations"), MODEL, est, "image:" + item["id"])
    params = {"model": MODEL, "prompt": prompt, "size": item["size"], "quality": item.get("quality", "high"),
              "n": 1, "output_format": "png", "background": item.get("background", "opaque")}
    if item.get("complexity"): params["complexity"] = item["complexity"]
    try:
        if item.get("edit_from"):
            src = HERE / "assets" / "gen" / f"{item['edit_from']}.png"
            body, ct = multipart({k: str(v) for k, v in params.items()}, {"image": (src.name, src.read_bytes(), "image/png")})
            req = urllib.request.Request("https://api.openai.com/v1/images/edits", body, {"Authorization": f"Bearer {key}", "Content-Type": ct})
        else:
            req = urllib.request.Request("https://api.openai.com/v1/images/generations", json.dumps(params).encode(),
                                         {"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=600) as r:
            res = json.loads(r.read())
    except urllib.error.HTTPError as ex:
        msg = ex.read().decode()[:400]
        ledger.settle(idx, f"HTTP_{ex.code}", extra={"error": msg}); sys.exit(f"{item['id']}: HTTP {ex.code} {msg}")
    except Exception as ex:
        ledger.settle(idx, "UNKNOWN", extra={"error": type(ex).__name__}); sys.exit(f"{item['id']}: {type(ex).__name__}; stopped, not retried")
    u = res.get("usage") or {}
    det = u.get("input_tokens_details") or {}
    cost = None
    if u:
        cost = det.get("text_tokens", 0) * P_TXT_IN + det.get("image_tokens", 0) * P_IMG_IN + u.get("output_tokens", 0) * P_IMG_OUT
    img = base64.b64decode(res["data"][0]["b64_json"])
    out = HERE / "assets" / "gen" / f"{item['id']}.png"; out.write_bytes(img)
    ledger.settle(idx, "ACK", cost=cost, usage=u)
    prov[item["id"]] = {"model": MODEL, "endpoint": "edits" if item.get("edit_from") else "generations",
        "edit_from": item.get("edit_from"), "params": {k: v for k, v in params.items() if k != "prompt"},
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(), "usage": u, "cost_usd": cost,
        "output_sha256": hashlib.sha256(img).hexdigest(), "revised_prompt": res["data"][0].get("revised_prompt"),
        "created": res.get("created")}
    prov_f.write_text(json.dumps(prov, indent=2) + "\n")
    print(item["id"], "usage", u, "cost", cost)
