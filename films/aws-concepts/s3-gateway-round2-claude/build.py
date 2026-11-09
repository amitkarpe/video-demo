#!/usr/bin/env python3
"""Build cues.json, captions.srt, transcript.txt, assets/mix.wav and index.html.

Inputs: script.json (lines, gaps), timing.json (measured clip lengths), assets/voice-*.wav.
Sound design is synthesized here (numpy, seeded): no sample libraries, no network.
Needs numpy + soundfile (the same venv as tts_openai.py). Deterministic for the same inputs.
"""
import json, pathlib, shutil
import numpy as np, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
SR = 48000
script = json.loads((HERE / "script.json").read_text())
timing = json.loads((HERE / "timing.json").read_text())

# ---------- cues / captions / transcript ----------
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
total = round(t + script["tail"], 3)
(HERE / "cues.json").write_text(json.dumps({"total": total, "cues": cues}, indent=2) + "\n")
(HERE / "captions.srt").write_text("\n".join(srt))
(HERE / "transcript.txt").write_text(" ".join(words) + "\n")
S = lambda k: cues[k]["s"]; E = lambda k: cues[k]["e"]

# ---------- sound design ----------
rng = np.random.default_rng(20261108)
N = int(total * SR) + SR
mix = np.zeros((N, 2))
def env(n, a, r):
    e = np.ones(n); ai = int(a * SR); ri = int(r * SR)
    if ai: e[:ai] = np.linspace(0, 1, ai)
    if ri: e[-ri:] *= np.exp(-np.linspace(0, 6, ri))
    return e
def bandnoise(n, lo, hi):
    X = np.fft.rfft(rng.standard_normal(n)); f = np.fft.rfftfreq(n, 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    y = np.fft.irfft(X, n); return y / (np.abs(y).max() + 1e-9)
def put(sig, at, gain=1.0, pan=0.0):
    i = int(at * SR); sig = sig[: max(0, N - i)]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    mix[i:i + len(sig), 0] += sig * gain * l * 1.414
    mix[i:i + len(sig), 1] += sig * gain * r * 1.414
def whoosh(d=0.9, lo=250, hi=3500):
    n = int(d * SR); x = bandnoise(n, lo, hi)
    w = np.sin(np.linspace(0, np.pi, n)) ** 2; return x * w
def blip(f=880, d=0.12):
    n = int(d * SR); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * tt) + .35 * np.sin(2 * np.pi * 2 * f * tt)) * np.exp(-tt * 28)
def thunk(f=72, d=0.45):
    n = int(d * SR); tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * (f * tt + 30 * (1 - np.exp(-tt * 18)) / 18)) * np.exp(-tt * 9)
    return s + 0.25 * bandnoise(n, 800, 4000) * np.exp(-tt * 60)
def chime(fs=(659.25, 987.77, 1318.5), d=1.6):
    n = int(d * SR); tt = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt * (2.2 + k)) for k, f in enumerate(fs)) / len(fs)
def riser(d=1.0):
    n = int(d * SR); tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * (180 * tt + 420 * tt ** 2 / d)) * (tt / d) ** 2
    return s + 0.4 * bandnoise(n, 2000, 9000) * (tt / d) ** 3
def boom(d=1.6):
    n = int(d * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * 48 * tt) * np.exp(-tt * 2.6) + 0.15 * bandnoise(n, 30, 200) * np.exp(-tt * 8)
def rewind(d=0.8):
    n = int(d * SR); tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * (1600 * tt - 700 * tt ** 2 / d)) * 0.35
    return (s + 0.5 * bandnoise(n, 1500, 7000)) * np.sin(np.linspace(0, np.pi, n))

# ambient pad (A minor colour), slow LFO, ducked under the voice later
tt = np.arange(N) / SR
pad = sum(a * np.sin(2 * np.pi * f * tt + p) for a, f, p in
          [(1, 55, 0), (.6, 82.41, 1), (.45, 110, 2), (.25, 164.81, .5), (.18, 220, 1.7), (.10, 329.63, .3)])
pad *= 0.55 + 0.45 * np.sin(2 * np.pi * tt / 9.0) ** 2
pad *= np.clip(tt / 2.0, 0, 1) * np.clip((total - tt) / 2.5, 0, 1)
pad = pad / np.abs(pad).max()

ev = [  # (time, signal, gain, pan)
    (0.05, boom(), .55, 0), (0.1, whoosh(.7, 200, 2500), .35, 0),
    (S("s01") - .4, whoosh(1.0, 150, 1800), .3, .2),
    (S("s01") + 1.5, blip(700), .35, .3),
    (S("s02") - .1, whoosh(1.2, 200, 3000), .35, -.3),
    (S("s02") + .15, blip(620), .35, .2), (S("s02") + .3, thunk(90, .3), .3, .3),
    (S("s02") + .85, blip(560), .35, .2), (S("s02") + 1.0, thunk(90, .3), .3, -.1),
    (S("s03") - .2, whoosh(1.0, 300, 4000), .3, 0),
    (S("s03") + .55, whoosh(.9, 1500, 9000), .45, -.6), (S("s03") + 1.45, blip(1320, .2), .4, .7),
    (S("s03") + 1.6, whoosh(1.0, 1200, 7000), .3, .5),
    (S("s04") - .25, rewind(), .5, 0), (S("s04") + .45, blip(440, .25), .3, 0),
    (S("s05") - .15, whoosh(1.1, 200, 2500), .3, 0),
    (S("s05") + .4, blip(1046.5), .3, -.3), (S("s05") + 1.4, blip(1318.5), .3, .2),
    (S("s05") + 2.3, blip(1567.98), .3, -.2),
    (S("s06") - .1, whoosh(1.0, 300, 5000), .35, 0), (S("s06") + .6, riser(.7), .3, 0),
    (S("s06") + 1.3, blip(880), .25, -.4),
    (S("s07") + .25, thunk(120, .25), .25, .3), (S("s07") + 1.6, blip(988), .3, 0),
    (S("s07") + 3.4, chime(), .45, 0), (E("s07") - 1.7, blip(1318.5), .3, .3),
    (S("s08") - .2, riser(.8), .35, 0), (S("s08") + .6, boom(1.2), .45, 0),
    (S("s08") + .55, whoosh(1.4, 400, 6000), .35, -.4),
    (S("s08") + 1.85, blip(784), .3, .2), (S("s08") + 2.9, chime((783.99, 1174.66, 1567.98), 1.2), .35, .6),
    (S("s09") - .2, whoosh(1.1, 200, 3000), .3, 0), (S("s09") + 1.5, thunk(85, .35), .4, -.2),
    (S("s10") - .2, whoosh(.9, 300, 3000), .25, .3), (S("s10") + .2, blip(659.25, .2), .35, .2),
    (S("s11") - .2, whoosh(1.0, 200, 2500), .3, 0), (S("s11") + .1, whoosh(1.2, 1200, 7000), .3, -.5),
    (S("s11") + .9, thunk(60, .6), .7, .6), (S("s11") + 1.35, blip(330, .3), .3, .5),
    (S("s12") - .15, whoosh(1.0, 200, 2500), .3, -.3), (S("s12") + .5, blip(988), .28, -.4),
    (S("s12") + 1.8, blip(1174.66), .28, -.2),
    (S("s13") - .2, whoosh(1.1, 200, 2500), .3, .3), (S("s13") + .2, blip(988), .28, .4),
    (S("s13") + .9, blip(1174.66), .28, .1), (S("s13") + 1.9, blip(1318.5), .28, .5),
    (S("s13") + 2.8, whoosh(.6, 600, 5000), .3, .6), (S("s13") + 3.7, blip(1567.98, .2), .3, .6),
    (S("s14") - .4, whoosh(1.4, 120, 1500), .3, 0),
    (S("s14") + .05, chime((523.25, 659.25, 783.99), 2.0), .4, -.2),
    (S("s14") + 1.25, chime((587.33, 739.99, 880.0), 2.2), .4, .2),
    (E("s14") + .45, boom(1.8), .5, 0),
]
for at, sig, g, p in ev:          # put() renders into `mix`, used here as the SFX bus
    put(sig / (np.abs(sig).max() + 1e-9), at, g, p)
sfx, mix = mix, np.zeros((N, 2))

voice = np.zeros(N); vmask = np.zeros(N)
for line in script["lines"]:
    x, sr = sf.read(HERE / "assets" / f"voice-{line['id']}.wav")
    if x.ndim > 1: x = x.mean(axis=1)
    if sr != SR:  # linear resample to 48 kHz
        x = np.interp(np.arange(int(len(x) * SR / sr)) * sr / SR, np.arange(len(x)), x)
    i = int(S(line["id"]) * SR); voice[i:i + len(x)] += x; vmask[i:i + len(x)] = 1
voice /= np.abs(voice).max() + 1e-9
# smooth ducking envelope for pad + sfx while the narrator speaks
k = int(0.25 * SR); duck = np.convolve(vmask, np.ones(k) / k, mode="same")
pad_g = 0.075 * (1 - 0.55 * duck); sfx_g = 0.55 * (1 - 0.35 * duck)
mix[:, 0] = voice * 0.80 + pad * pad_g + sfx[:, 0] * sfx_g
mix[:, 1] = voice * 0.80 + pad * pad_g * 0.96 + sfx[:, 1] * sfx_g
mix = mix[: int(total * SR)]
mix *= 0.89 / (np.abs(mix).max() + 1e-9)   # peak -1 dBFS
sf.write(HERE / "assets" / "mix.wav", mix, SR, subtype="PCM_16")

# ---------- html ----------
caps = []
for line in script["lines"]:
    c = cues[line["id"]]
    caps.append(f'<div id="cap-{line["id"]}" class="clip caption" data-start="{c["s"]-0.03:.3f}" data-duration="{c["d"]+max(0.0, min(0.25, line["gap_after"]-0.08)):.3f}" data-track-index="10">{line["caption"]}</div>')
audio = f'<audio id="mix" class="clip" data-start="0" data-duration="{total:.3f}" data-track-index="20" src="assets/mix.wav"></audio>'
html = (HERE / "src" / "index.template.html").read_text()
html = (html.replace("__TOTAL__", str(total)).replace("__CUES__", json.dumps(cues))
            .replace("<!--__CAPTIONS__-->", "\n".join(caps)).replace("<!--__AUDIO__-->", audio))
(HERE / "index.html").write_text(html)
gs = HERE.parent.parent / "node_modules" / "gsap" / "dist" / "gsap.min.js"
shutil.copyfile(gs, HERE / "assets" / "gsap.min.js")
print("total", total, "s")
