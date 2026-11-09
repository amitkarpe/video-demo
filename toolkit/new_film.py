#!/usr/bin/env python3
"""Start a new film from a house style (no network, no paid API).

    python3 toolkit/new_film.py --repo aws-factory --slug ssm-reboots --style toy-world-3d --title "..."

Creates films/<repo>/<slug>/ with the style kit, a script.json skeleton (budget_usd 5 by default), a build.py
that uses toolkit/av.py, review/qa-rules.md, CLAIMS.md and README.md stubs. It never overwrites an existing folder.
Styles: toy-world-3d (default), swiss-grid. Clay diorama is spot art on top of either (styles/clay-diorama).
cinematic-night is archived: reuse it only when the owner names it (start from films/nextflow-offline/offline-validation).
"""
import argparse, json, pathlib, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser()
ap.add_argument("--repo", required=True, help="source repository the film explains, e.g. aws-factory")
ap.add_argument("--slug", required=True, help="short film folder name, e.g. ssm-patch")
ap.add_argument("--style", default="toy-world-3d", choices=["toy-world-3d", "swiss-grid"])
ap.add_argument("--title", default="Untitled film")
ap.add_argument("--budget", type=float, default=5.0, help="OpenAI cap in USD (house default 5)")
a = ap.parse_args()

dst = ROOT / "films" / a.repo / a.slug
if dst.exists(): sys.exit(f"exists, not touching it: {dst}")
kit = ROOT / "styles" / a.style / "kit"
(dst / "src").mkdir(parents=True)
for p in kit.iterdir():
    if p.is_dir(): shutil.copytree(p, dst / p.name)               # e.g. lib/three for the 3D style
    elif p.suffix == ".js": shutil.copy(p, dst / "src" / p.name)    # world.js
    else: shutil.copy(p, dst / "src" / p.name)                       # index.template.html
for d in ("media/original", "prompts", "review", "keyframes", "out"): (dst / d).mkdir(parents=True, exist_ok=True)

(dst / "script.json").write_text(json.dumps({
    "title": a.title,
    "status": "Phase 1 draft: for the owner's review; not yet approved",
    "style": a.style,
    "budget_usd": a.budget,
    "voice": {"model": "gpt-realtime-2.1", "voice": "marin",
              "instructions": "You are the narrator of a clear, friendly, confident explainer for both engineers and managers. "
                              "Read the user's text aloud exactly as written, word for word: do not add, drop, reorder or paraphrase any word, "
                              "and do not answer or comment. Voice: warm, calm and well paced. Pronounce: <add the glossary from the intake card>."},
    "lead_in": 1.4, "tail": 7.0,
    "chapters": [{"id": "c1", "label": "THE QUESTION", "start": "s01", "shot": "hook"}],
    "lines": [{"id": "s01", "gap_after": 0.4, "caption": "Replace with the first narration line."}],
}, indent=1, ensure_ascii=False) + "\n")
(dst / "prompts" / "images.json").write_text('{"images": []}\n')
(dst / "build.py").write_text('''#!/usr/bin/env python3
"""Build cues, captions, transcript, the -16 LUFS mix and index.html. Shared steps: toolkit/av.py.
This file keeps only this film's score and sound-effect cues."""
import pathlib, sys
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "toolkit").is_dir())
sys.path.insert(0, str(ROOT / "toolkit")); import av
av.setup(globals(), __file__, seed=20261201)

# ---- score: chords as MIDI note lists; pad(notes, start, dur, gain) and pluck(note, at, gain, pan) ----
C, G, Am, Fa = [48, 55, 60, 64], [43, 55, 59, 62], [45, 57, 60, 64], [41, 57, 60, 65]
def seq(chords, start, end, gain=.7):
    n = len(chords); step = (end - start) / n
    for k, ch in enumerate(chords): pad(ch, start + k*step, step + 1.4, gain)
seq([C, G, Am, Fa], 0.0, total, .7)

# ---- sound effects: (time, signal, gain, pan); S/E/F give line start, end and fraction ----
ev = []
ev.append((0.2, shimmer(2.4), .14, 0))
av.finish(globals())
''')
(dst / "review" / "qa-rules.md").write_text(
    f'Film: "{a.title}", a public explainer for engineers and managers.\n'
    f"Style: {a.style} (see styles/{a.style}/README.md).\n"
    "Public-output rule: <copy from the intake card>.\nAccuracy rules:\n- <one line per claim the reviewer must check>\n")
(dst / "CLAIMS.md").write_text(f"# Evidence map — \"{a.title}\"\n\n| # | Statement (film) | Source | State |\n|---|---|---|---|\n")
(dst / "README.md").write_text(f"# {a.title}\n\nSource repository: `{a.repo}` · Style: `{a.style}` · Status: Phase 1\n\n"
                               "Watch: (GitHub Release link after delivery)\n")
(dst / ".gitignore").write_text(".venv/\n.hyperframes/\n__pycache__/\nassets/gsap.min.js\nassets/mix.wav\nassets/mix-prenorm.wav\n"
                                "out/*.mp4\nreview/tmp/\nphase1/_snap/\n")
print(f"created {dst.relative_to(ROOT)} from styles/{a.style}")
