#!/usr/bin/env python3
"""Rebuild every derived file from the SELECTED immutable originals (no network, deterministic).
  .venv/bin/python tools/derive.py
Images: opaque plates -> media/derived/images/<id>.jpg (q90); transparent sprites -> cropped to alpha bbox, PNG.
Voice:  edges trimmed (60 ms lead, 160 ms tail) and internal silences longer than MAX_GAP shortened to
        MAX_GAP (speech untouched) -> media/derived/voice/<id>.v1.wav; durations -> timing.json.
Never writes into media/original/."""
import hashlib, json, pathlib, sys
import numpy as np, soundfile as sf
from PIL import Image
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import media
from film import film_dir
HERE = film_dir()
MAX_GAP, WIN, THR, LEAD, TAIL = 0.42, 0.02, 0.012, 0.06, 0.16
m = media.load(); der = {}
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
spec = json.loads((HERE / "prompts" / "images.json").read_text())
outd = HERE / "media" / "derived" / "images"; outd.mkdir(parents=True, exist_ok=True)
for item in spec["images"]:
    k = f"images/{item['id']}"
    if k not in m["selected"]: continue
    src = media.selected_path("images", item["id"]); im = Image.open(src)
    if item.get("background") == "transparent":
        im = im.convert("RGBA"); bbox = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox(); im = im.crop(bbox)
        dst = outd / f"{item['id']}.png"; im.save(dst, optimize=True); step = f"crop to alpha bbox {bbox}; PNG"
    else:
        dst = outd / f"{item['id']}.jpg"; im.convert("RGB").save(dst, quality=90, optimize=True); step = "RGB JPEG q90"
    der[str(dst.relative_to(HERE))] = {"from": f"{k}.{m['selected'][k]}", "step": step, "sha256": sha(dst)}

timing = {}
script = json.loads((HERE / "script.json").read_text())
vout = HERE / "media" / "derived" / "voice"; vout.mkdir(parents=True, exist_ok=True)
for line in script["lines"]:
    k = f"voice/{line['id']}"
    if k not in m["selected"]: continue
    x, sr = sf.read(media.selected_path("voice", line["id"]))
    loud = np.where(np.abs(x) > 0.01)[0]
    if len(loud): x = x[max(0, loud[0] - int(LEAD * sr)): loud[-1] + int(TAIL * sr)]
    w = int(WIN * sr); n = len(x) // w
    lw = np.array([np.abs(x[i*w:(i+1)*w]).max() > THR for i in range(n)])
    keep, run = [], 0
    for i in range(n):
        run = 0 if lw[i] else run + 1
        if run * WIN <= MAX_GAP: keep.append(x[i*w:(i+1)*w])
    keep.append(x[n*w:]); y = np.concatenate(keep)
    dst = vout / f"{line['id']}.v1.wav"; sf.write(dst, y, sr, subtype="PCM_16"); timing[line["id"]] = round(len(y) / sr, 3)
    der[str(dst.relative_to(HERE))] = {"from": f"{k}.{m['selected'][k]}", "step": f"trim edges (lead {LEAD}s, tail {TAIL}s); cap silences > {MAX_GAP}s", "sha256": sha(dst)}
m = media.load(); m["derivations"] = der; media.save(m)
(HERE / "timing.json").write_text(json.dumps(timing, indent=2) + "\n")
print(len(der), "derived files;", "speech", round(sum(timing.values()), 2), "s" if timing else "")
