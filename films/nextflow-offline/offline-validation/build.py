#!/usr/bin/env python3
"""Revision 2 build: index.html, captions.srt and transcript.txt from
script.json, cues.json (tools/voice.py) and transcript.json (word times from
`npx hyperframes transcribe review/voice.wav -e parakeet`). No network.

Captions show the script's words, timed by the transcript words of each line,
matched by position and scaled when the counts differ."""
import html, json, pathlib, re

D = pathlib.Path(__file__).resolve().parent
s = json.loads((D / "script.json").read_text())
cj = json.loads((D / "cues.json").read_text())
cues, total = cj["cues"], cj["total"]
words = json.loads((D / "transcript.json").read_text())
words = words["words"] if isinstance(words, dict) else words
L = s["lines"]

word_times, caps = {}, []
for i, l in enumerate(L):
    q = cues[l["id"]]
    a = (cues[L[i-1]["id"]]["e"] + q["s"]) / 2 if i else -1
    b = (q["e"] + cues[L[i+1]["id"]]["s"]) / 2 if i + 1 < len(L) else 1e9
    tw = [w for w in words if a <= w["start"] < b]
    sw = l["caption"].replace("—", " ").split()
    n, m = len(sw), len(tw)
    timed = []
    for k, w in enumerate(sw):
        if m:
            j0 = min(m - 1, round(k * m / n)); j1 = min(m - 1, max(j0, round((k + 1) * m / n) - 1))
            st, en = tw[j0]["start"], tw[j1]["end"]
        else:
            st, en = q["s"] + q["d"] * k / n, q["s"] + q["d"] * (k + 1) / n
        timed.append((w, round(st, 3), round(en, 3)))
    word_times[l["id"]] = [list(x) for x in timed]
    group = []
    for k, (w, st, en) in enumerate(timed):
        group.append((w, st, en)); nxt = timed[k + 1] if k + 1 < n else None
        if re.search(r"[.?!:]$", w) or len(group) >= 6 or nxt is None or (nxt[1] - en > 0.15 and len(group) >= 3):
            caps.append({"s": round(group[0][1] - 0.05, 3), "e": round(group[-1][2] + 0.15, 3), "t": " ".join(x[0] for x in group)}); group = []
for x, y in zip(caps, caps[1:]):
    x["e"] = min(x["e"], y["s"] - 0.02)

chapters = [{"label": c["label"], "t": round(cues[c["start"]]["s"] - 0.3, 3)} for c in s["chapters"]]
stages = ["source", "verify-source", "validate-intake", "check-bundle", "check-data", "check-images",
          "runtime-preflight", "offline-execute", "validate-results", "publish-report"]
rep = {
    "__DUR__": str(total),
    "__CUES__": json.dumps(cues),
    "__WORDS__": json.dumps(word_times),
    "__CAPJSON__": json.dumps(caps),
    "__CHAPTERS__": json.dumps(chapters),
    "__STAGES__": "".join(f'<div class="st"><b>{i+1:02d}</b><span>{html.escape(x)}</span></div>' for i, x in enumerate(stages)),
    "__CAPTIONS__": "\n".join(f'<div class="cg" id="cg{i}"><span>{html.escape(c["t"])}</span></div>' for i, c in enumerate(caps)),
}
out = (D / "src/index.template.html").read_text()
for k, v in rep.items():
    out = out.replace(k, v)
(D / "index.html").write_text(out)
fmt = lambda x: f"{int(x//3600):02d}:{int(x%3600//60):02d}:{int(x%60):02d},{int(round(x%1*1000)) % 1000:03d}"
(D / "captions.srt").write_text("\n".join(f"{i}\n{fmt(c['s'])} --> {fmt(c['e'])}\n{c['t']}\n" for i, c in enumerate(caps, 1)))
(D / "transcript.txt").write_text("\n".join(l["caption"] for l in L) + "\n")
print(f"index.html: {total}s, {len(caps)} caption groups")
