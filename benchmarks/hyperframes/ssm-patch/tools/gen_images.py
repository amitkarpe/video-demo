#!/usr/bin/env python3
"""Generate images with OpenAI gpt-image-2.6-sunburst (metered). Reads prompts/images.json.
  python3 tools/gen_images.py --env-file <.env> --only hall
Provider bytes go to media/original/images/<id>.t<N>.png first (never overwritten; a rerun is a new take),
then prompts/image-provenance.json records prompt sha256, usage, cost and output sha256."""
import argparse, base64, hashlib, json, pathlib, sys, urllib.request, urllib.error, uuid
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import ledger, media
HERE = pathlib.Path(__file__).resolve().parent.parent
MODEL = "gpt-image-2.6-sunburst"
P_TXT_IN, P_IMG_IN, P_IMG_OUT = 5/1e6, 8/1e6, 30/1e6   # published USD/token rates (reviewed 2026-11-08)
ap = argparse.ArgumentParser(); ap.add_argument("--env-file"); ap.add_argument("--only", nargs="*")
ap.add_argument("--reserve-out-tokens", type=int, default=6000, help="conservative output-token reservation per image")
a = ap.parse_args()
spec = json.loads((HERE / "prompts" / "images.json").read_text())
prov_f = HERE / "prompts" / "image-provenance.json"
prov = json.loads(prov_f.read_text()) if prov_f.exists() else {}
key = ledger.api_key(a.env_file)
for item in spec["images"]:
    if a.only and item["id"] not in a.only: continue
    prompt = spec["style"] + " " + item["prompt"]
    est = len(prompt) / 3 * P_TXT_IN + a.reserve_out_tokens * P_IMG_OUT
    idx = ledger.reserve("images/" + ("edits" if item.get("edit_of") else "generations"), MODEL, est + (3000 * P_IMG_IN if item.get("edit_of") else 0), "image:" + item["id"])
    params = {"model": MODEL, "prompt": prompt, "size": item["size"], "quality": item.get("quality", "high"),
              "n": 1, "output_format": "png", "background": item.get("background", "opaque")}
    endpoint = "generations"
    if item.get("edit_of"):
        # reference edit: keeps the object identical across shots (playbook §3)
        endpoint = "edits"; ref = media.selected_path("images", item["edit_of"])
        bnd = uuid.uuid4().hex; body = bytearray()
        for k2, v2 in params.items():
            body += f"--{bnd}\r\nContent-Disposition: form-data; name=\"{k2}\"\r\n\r\n{v2}\r\n".encode()
        body += (f"--{bnd}\r\nContent-Disposition: form-data; name=\"image[]\"; filename=\"{ref.name}\"\r\n"
                 "Content-Type: image/png\r\n\r\n").encode() + ref.read_bytes() + f"\r\n--{bnd}--\r\n".encode()
        req = urllib.request.Request("https://api.openai.com/v1/images/edits", bytes(body),
                                     {"Authorization": f"Bearer {key}", "Content-Type": f"multipart/form-data; boundary={bnd}"})
    else:
        req = urllib.request.Request("https://api.openai.com/v1/images/generations", json.dumps(params).encode(),
                                     {"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            res = json.loads(r.read()); req_id = r.headers.get("x-request-id")
    except urllib.error.HTTPError as ex:
        msg = ex.read().decode()[:400]
        ledger.settle(idx, f"HTTP_{ex.code}", extra={"error": msg, "request_id": ex.headers.get("x-request-id")})
        sys.exit(f"{item['id']}: HTTP {ex.code} {msg}")
    except Exception as ex:
        ledger.settle(idx, "UNKNOWN", extra={"error": type(ex).__name__}); sys.exit(f"{item['id']}: {type(ex).__name__}; stopped, not retried")
    u = res.get("usage") or {}; det = u.get("input_tokens_details") or {}
    cost = (det.get("text_tokens", 0) * P_TXT_IN + det.get("image_tokens", 0) * P_IMG_IN + u.get("output_tokens", 0) * P_IMG_OUT) if u else None
    img = base64.b64decode(res["data"][0]["b64_json"])
    path, take = media.write_original("images", item["id"], "png", img, {"model": MODEL, "endpoint": "images/" + endpoint, "edit_of": item.get("edit_of"),
                                      "request_id": req_id, "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest()})
    ledger.settle(idx, "ACK", cost=cost, usage=u, extra={"request_id": req_id, "output": str(path.relative_to(HERE))})
    prov[f"{item['id']}.{take}"] = {"model": MODEL, "endpoint": endpoint, "edit_of": item.get("edit_of"),
        "params": {k: v for k, v in params.items() if k != "prompt"}, "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "usage": u, "cost_usd": cost, "output": str(path.relative_to(HERE)), "output_sha256": hashlib.sha256(img).hexdigest(),
        "revised_prompt": res["data"][0].get("revised_prompt"), "created": res.get("created"), "request_id": req_id}
    prov_f.write_text(json.dumps(prov, indent=2) + "\n")
    print(item["id"], take, "out_tokens", u.get("output_tokens"), "cost", round(cost or 0, 4))
