#!/usr/bin/env python3
"""Build cues.json, captions.srt, transcript.txt and index.html from script.json + timing.json."""
import json, pathlib, shutil

HERE = pathlib.Path(__file__).resolve().parent
script = json.loads((HERE / "script.json").read_text())
timing = json.loads((HERE / "timing.json").read_text())

t = script["lead_in"]
cues, srt, words = {}, [], []
def ts(x):
    h, r = divmod(x, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}".replace(".", ",")
for i, line in enumerate(script["lines"], 1):
    d = timing[line["id"]]
    cues[line["id"]] = {"s": round(t, 3), "e": round(t + d, 3), "d": d}
    srt.append(f"{i}\n{ts(t)} --> {ts(t + d)}\n{line['caption']}\n")
    words.append(line["caption"])
    t += d + line["gap_after"]
total = round(t, 3)
(HERE / "cues.json").write_text(json.dumps({"total": total, "cues": cues}, indent=2) + "\n")
(HERE / "captions.srt").write_text("\n".join(srt))
(HERE / "transcript.txt").write_text(" ".join(words) + "\n")

caps, auds = [], []
for line in script["lines"]:
    c = cues[line["id"]]
    caps.append(f'<div id="cap-{line["id"]}" class="clip caption" data-start="{c["s"]-0.05:.3f}" data-duration="{c["d"]+0.2:.3f}" data-track-index="10">{line["caption"]}</div>')
    auds.append(f'<audio id="aud-{line["id"]}" class="clip" data-start="{c["s"]:.3f}" data-duration="{c["d"]:.3f}" data-track-index="20" src="assets/voice-{line["id"]}.wav"></audio>')

html = (HERE / "src" / "index.template.html").read_text()
html = (html.replace("__TOTAL__", str(total))
            .replace("__CUES__", json.dumps(cues))
            .replace("<!--__CAPTIONS__-->", "\n".join(caps))
            .replace("<!--__AUDIO__-->", "\n".join(auds)))
(HERE / "index.html").write_text(html)

gs = HERE.parent.parent / "node_modules" / "gsap" / "dist" / "gsap.min.js"
(HERE / "assets").mkdir(exist_ok=True)
shutil.copyfile(gs, HERE / "assets" / "gsap.min.js")
print("total", total, "s")
