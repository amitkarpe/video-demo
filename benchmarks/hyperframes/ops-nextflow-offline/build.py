#!/usr/bin/env python3
"""Build index.html from src/index.template.html, script.json, timing.json and transcript.json.

Captions use the script's words, timed by the transcript words of each line
(matched by position, scaled when counts differ). Run tools/mix.sh after a
timing change to rebuild assets/mix.wav.
"""
import json, re, html, pathlib

ROOT = pathlib.Path(__file__).parent
timing = json.loads((ROOT / "timing.json").read_text())
words = json.loads((ROOT / "transcript.json").read_text())
if isinstance(words, dict):
    words = words.get("words", [])
DUR = timing["duration"]


LINES = timing["lines"]


def line_words(line):
    i = LINES.index(line)
    a = (LINES[i-1]["start"] + LINES[i-1]["dur"] + line["start"]) / 2 if i else -1
    b = (line["start"] + line["dur"] + LINES[i+1]["start"]) / 2 if i + 1 < len(LINES) else 1e9
    return [w for w in words if a <= w["start"] < b]


caps, qtimes = [], []
for li, line in enumerate(timing["lines"]):
    sw = line["text"].split()
    tw = line_words(line)
    n, m = len(sw), len(tw)
    timed = []
    for i, w in enumerate(sw):
        j0 = min(m - 1, round(i * m / n)) if m else 0
        j1 = min(m - 1, max(j0, round((i + 1) * m / n) - 1)) if m else 0
        s = tw[j0]["start"] if m else line["start"] + line["dur"] * i / n
        e = tw[j1]["end"] if m else line["start"] + line["dur"] * (i + 1) / n
        timed.append((w, s, e))
    if li == 0:  # the question typed into the chat card
        qi = sw.index("Was")
        qtimes = [round(s, 3) for _, s, _ in timed[qi:]]
        qwords = [w for w, _, _ in timed[qi:]]
    group = []
    for k, (w, s, e) in enumerate(timed):
        group.append((w, s, e))
        nxt = timed[k + 1] if k + 1 < len(timed) else None
        brk = re.search(r"[.?!:]$", w) or len(group) >= 6 or (nxt and nxt[1] - e > 0.15 and len(group) >= 3)
        if brk or nxt is None:
            caps.append({"s": round(group[0][1] - 0.05, 3), "e": round(group[-1][2] + 0.12, 3), "t": " ".join(x[0] for x in group)})
            group = []
for a, b in zip(caps, caps[1:]):  # one group visible at a time
    a["e"] = min(a["e"], b["s"] - 0.02)

stages = ["source", "verify-source", "validate-intake", "check-bundle", "check-data", "check-images",
          "runtime-preflight", "offline-execute", "validate-results", "publish-report"]
st_html = "".join(f'<div class="st"><b>{i+1:02d}</b><span>{html.escape(s)}</span></div>' for i, s in enumerate(stages))
cap_html = "\n".join(f'<div class="cg" id="cg{i}"><span>{html.escape(c["t"])}</span></div>' for i, c in enumerate(caps))
q_html = " ".join(f"<span>{html.escape(w)}</span>" for w in qwords)

out = (ROOT / "src/index.template.html").read_text()
for k, v in {"__DUR__": str(DUR), "__CAPJSON__": json.dumps(caps), "__QJSON__": json.dumps(qtimes),
             "__STAGES__": st_html, "__CAPTIONS__": cap_html, "__QWORDS__": q_html}.items():
    out = out.replace(k, v)
(ROOT / "index.html").write_text(out)
srt = []
fmt = lambda x: f"{int(x//3600):02d}:{int(x%3600//60):02d}:{int(x%60):02d},{int(round(x%1*1000)):03d}"
for i, c in enumerate(caps, 1):
    srt.append(f"{i}\n{fmt(c['s'])} --> {fmt(c['e'])}\n{c['t']}\n")
(ROOT / "captions.srt").write_text("\n".join(srt))
print(f"index.html built: {len(caps)} caption groups, duration {DUR}s")
