#!/usr/bin/env python3
"""Build cues.json, captions.srt, transcript.txt, assets/mix.wav and index.html (no network, no paid API).

Inputs: script.json, timing.json, assets/voice/<id>.wav (cached OpenAI narration), src/index.template.html.
The score and sound effects are synthesized here with numpy from a fixed seed: no samples, no libraries.
Run inside a venv with numpy + soundfile.
"""
import json, pathlib, shutil
import numpy as np, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
SR = 48000
script = json.loads((HERE / "script.json").read_text())
timing = json.loads((HERE / "timing.json").read_text())

# ---------------- cues / captions / transcript ----------------
t = script["lead_in"]; cues, srt, words = {}, [], []
def ts(x):
    h, r = divmod(x, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}".replace(".", ",")
for i, line in enumerate(script["lines"], 1):
    d = timing[line["id"]]
    cues[line["id"]] = {"s": round(t, 3), "e": round(t + d, 3), "d": d}
    srt.append(f"{i}\n{ts(t)} --> {ts(t + d)}\n{line['caption']}\n"); words.append(line["caption"])
    t += d + line["gap_after"]
total = round(t + script["tail"], 3)
(HERE / "cues.json").write_text(json.dumps({"total": total, "cues": cues}, indent=2) + "\n")
(HERE / "captions.srt").write_text("\n".join(srt))
(HERE / "transcript.txt").write_text("\n".join(words) + "\n")
S = lambda k: cues[k]["s"]; E = lambda k: cues[k]["e"]
chapters = [{"id": c["id"], "label": c["label"], "t": S(c["start"])} for c in script["chapters"]]

# ---------------- synthesis helpers ----------------
rng = np.random.default_rng(20261108)
N = int(total * SR) + SR
music = np.zeros((N, 2)); sfx = np.zeros((N, 2))
def put(buf, sig, at, gain=1.0, pan=0.0):
    i = int(max(0, at) * SR); sig = sig[: max(0, N - i)]
    l, r = np.cos((pan + 1) * np.pi / 4) * 1.414, np.sin((pan + 1) * np.pi / 4) * 1.414
    buf[i:i + len(sig), 0] += sig * gain * l; buf[i:i + len(sig), 1] += sig * gain * r
def bandnoise(n, lo, hi):
    X = np.fft.rfft(rng.standard_normal(n)); f = np.fft.rfftfreq(n, 1 / SR); X[(f < lo) | (f > hi)] = 0
    y = np.fft.irfft(X, n); return y / (np.abs(y).max() + 1e-9)
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def whoosh(d=1.0, lo=250, hi=3500): n = int(d*SR); return bandnoise(n, lo, hi) * np.sin(np.linspace(0, np.pi, n)) ** 2
def blip(f=880, d=.14): x = tt(d); return (np.sin(2*np.pi*f*x) + .3*np.sin(4*np.pi*f*x)) * np.exp(-x*26)
def thunk(f=70, d=.5): x = tt(d); return np.sin(2*np.pi*(f*x + 28*(1-np.exp(-x*18))/18))*np.exp(-x*8) + .25*bandnoise(len(x), 700, 4000)*np.exp(-x*60)
def clank(d=.7): x = tt(d); return norm(sum(np.sin(2*np.pi*f*x)*np.exp(-x*k) for f, k in [(523, 9), (1187, 12), (1731, 16), (2690, 22)]) + .4*bandnoise(len(x), 2000, 8000)*np.exp(-x*40))
def chime(fs, d=2.2): x = tt(d); return sum(np.sin(2*np.pi*f*x)*np.exp(-x*(1.8+k*.6)) for k, f in enumerate(fs)) / len(fs)
def riser(d=1.2): x = tt(d); return np.sin(2*np.pi*(160*x + 380*x**2/d))*(x/d)**2 + .35*bandnoise(len(x), 2500, 9000)*(x/d)**3
def boom(d=2.0): x = tt(d); return np.sin(2*np.pi*46*x)*np.exp(-x*2.3) + .15*bandnoise(len(x), 30, 220)*np.exp(-x*7)
def ping(d=1.2): x = tt(d); return np.sin(2*np.pi*1480*x)*np.exp(-x*4) + .5*np.sin(2*np.pi*740*x)*np.exp(-x*3)
def alarm(d=.9): x = tt(d); f = np.where((x*4).astype(int) % 2 == 0, 660, 520); return np.sign(np.sin(2*np.pi*f*x))*.25*np.exp(-x*1.5)
def shimmer(d=2.0): x = tt(d); return sum(np.sin(2*np.pi*f*x + k)*np.exp(-x*2)*(1+np.sin(2*np.pi*(5+k)*x))*.5 for k, f in enumerate([2093, 2637, 3136, 3951]))
NOTE = lambda n: 440.0 * 2 ** ((n - 69) / 12)
def pad(notes, start, dur, gain=1.0):
    x = tt(dur); a = min(1.5, dur / 3); env = np.minimum(1, x / a) * np.minimum(1, (dur - x) / 1.2).clip(0, 1)
    sig = sum(np.sin(2*np.pi*NOTE(n)*x*(1+det)) for n in notes for det in (-0.0025, 0.0025))
    sig += .35 * sum(np.sin(2*np.pi*NOTE(n-12)*x) for n in notes[:1])
    put(music, norm(sig) * env * gain, start, 1.0, 0)
def pluck(n, at, gain=.5, pan=0.0):
    x = tt(1.4); f = NOTE(n); s = (np.sin(2*np.pi*f*x) + .45*np.sin(4*np.pi*f*x) + .2*np.sin(6*np.pi*f*x)) * np.exp(-x*5)
    put(music, s, at, gain, pan)

# chord colours per section (MIDI note numbers)
Dm, Bb, F, C, Gm, Am, Asus = [62, 65, 69, 74], [58, 62, 65, 69], [53, 57, 60, 65], [55, 60, 64, 67], [55, 58, 62, 67], [57, 60, 64, 69], [57, 62, 64, 69]
def seq(chords, start, end, gain=.8):
    n = len(chords); step = (end - start) / n
    for k, ch in enumerate(chords): pad(ch, start + k*step, step + 1.2, gain)
pad(Dm + [76], 0.0, S("s04") + 0.5, .9)
seq([Bb, F], S("s04") - 0.5, S("s07"))
seq([F, Gm, Bb, C], S("s07") - 0.5, S("s13"))
seq([Dm, Bb, F, C], S("s13") - 0.5, S("s18"))
seq([Dm, Bb, F, C, Dm, Bb, F, Asus], S("s18") - 0.5, S("s26"), .7)
seq([Asus], S("s26") - 0.5, S("s27"))
seq([F, C, Dm, Bb], S("s27") - 0.5, S("s31"))
seq([Dm, Gm, Dm, Asus, Dm, Bb], S("s31") - 0.5, S("s38"), .7)
seq([Bb, C, F + [77]], S("s38") - 0.5, total, 1.0)
# arpeggio pulse under the DEV proving grounds and Phase B
def arp(start, end, chords, bpm=100, gain=.32):
    beat = 60 / bpm / 2; k = 0; t0 = start
    while t0 < end:
        ch = chords[int((t0 - start) / ((end - start) / len(chords))) % len(chords)]
        pluck(ch[k % len(ch)] + 12, t0, gain * (1.0 if k % 4 == 0 else .7), [-.4, .4][k % 2]); t0 += beat; k += 1
arp(S("s18"), E("s25"), [Dm, Bb, F, C, Dm, Bb, F, Asus])
arp(S("s32"), E("s37"), [Dm, Gm, Dm, Asus, Dm, Bb], bpm=84, gain=.24)

ev = [  # (time, signal, gain, pan)
    (0.1, boom(2.4), .6, 0), (0.5, shimmer(2.5), .25, -.5),
    (S("s02") + .4, whoosh(1.4, 150, 1800), .3, .2),
    (S("s03") - .1, chime([587.33, 880, 1174.66], 3.0), .55, 0), (S("s03") - .1, boom(2.0), .4, 0),
    (S("s04") - .9, whoosh(1.2, 300, 6000), .45, -.6),
    (S("s05") + .1, ping(), .45, -.4), (S("s05") + .6, ping(), .3, -.2), (S("s06") + .1, riser(1.6), .2, .3),
    (S("s07") - .6, whoosh(1.4, 120, 2000), .4, 0), (E("s07") - .05, boom(2.0), .7, 0), (E("s07") - .05, clank(), .35, .2),
    (S("s08") + .1, thunk(80), .45, 0), (S("s08") + 2.6, clank(), .3, .3), (S("s10") + .1, clank(), .3, -.3),
    (E("s10") - .6, chime([783.99, 1174.66]), .35, 0),
    *[(S("s11") + .6 + k*.55, blip(988 + 60*k), .3, -.5 + k*.25) for k in range(5)],
    (S("s12") + .2, thunk(60, .7), .55, -.4),
    (S("s13") - .5, whoosh(1.2, 200, 3000), .35, 0), (S("s13") + 1.2, riser(.9), .25, 0),
    (S("s14"), thunk(90, .4), .4, -.6), (S("s15"), thunk(80, .4), .4, 0), (S("s16"), thunk(100, .4), .4, .6),
    (S("s17") + .4, blip(660, .25), .3, -.7),
    (S("s18") - .9, whoosh(1.2, 300, 6000), .45, .6), (S("s18") - .5, boom(1.6), .4, 0),
    (S("s25") + .2, thunk(55, .8), .8, 0), (S("s25") + .3, alarm(), .35, 0),
    (S("s26") - .6, whoosh(1.0, 200, 2500), .3, 0),
    (S("s27") - .9, whoosh(1.4, 120, 3000), .45, -.4),
    (S("s28") + 2.0, shimmer(1.6), .2, .5), (S("s29") - .2, whoosh(.8, 400, 3000), .25, .6),
    (S("s29") + cues["s29"]["d"] * .72, thunk(70, .6), .7, 0), (S("s29") + cues["s29"]["d"] * .72 + .05, chime([659.25, 987.77]), .3, 0),
    (S("s30") + cues["s30"]["d"] * .3, whoosh(.8, 600, 5000), .25, .3), (S("s30") + cues["s30"]["d"] * .42, blip(1318.5, .3), .35, .3),
    (S("s31") - .4, whoosh(2.0, 100, 1500), .3, 0),
    (S("s33") + .4, chime([1046.5, 1567.98, 2093], 2.5), .35, .5),
    (S("s34") + .3, blip(740), .3, -.6), (S("s34") + .7, blip(880), .3, -.3), (S("s34") + 1.1, blip(988), .3, 0),
    *[(S("s35") + cues["s35"]["d"] * f, thunk(110, .3), .35, -.3) for f in (.05, .28, .5, .78)],
    (E("s35") - .2, thunk(55, .8), .8, 0),
    (S("s36"), riser(.5), .3, 0), (S("s36") + .1, thunk(90, .3), .4, 0),
    (S("s37") + .2, whoosh(1.2, 200, 2500), .25, -.3),
    (S("s38") - 1.0, whoosh(1.4, 300, 7000), .45, 0), (S("s38"), boom(2.0), .55, 0),
    (S("s38"), chime([587.33, 880]), .4, -.3), (S("s39"), chime([698.46, 1046.5]), .4, .3), (S("s40"), chime([698.46, 880, 1396.9], 3.5), .5, 0),
    (E("s40") + .4, shimmer(3.0), .25, 0),
]
for at, sig, g, p in ev: put(sfx, norm(sig), at, g, p)

voice = np.zeros(N); vmask = np.zeros(N)
for line in script["lines"]:
    x, sr = sf.read(HERE / "assets" / "voice" / f"{line['id']}.wav")
    if x.ndim > 1: x = x.mean(axis=1)
    if sr != SR: x = np.interp(np.arange(int(len(x) * SR / sr)) * sr / SR, np.arange(len(x)), x)
    i = int(S(line["id"]) * SR); voice[i:i + len(x)] += x; vmask[i:i + len(x)] = 1
voice = norm(voice)
k = int(0.3 * SR); duck = np.convolve(vmask, np.ones(k) / k, mode="same")
music = music / (np.abs(music).max() + 1e-9); sfx = sfx / (np.abs(sfx).max() + 1e-9)
fade = np.clip(np.arange(N) / SR / 1.5, 0, 1) * np.clip((total - np.arange(N) / SR) / 3.0, 0, 1)
mix = np.zeros((N, 2))
for c in range(2):
    mix[:, c] = voice * .82 + music[:, c] * .16 * (1 - .5 * duck) * fade + sfx[:, c] * .42 * (1 - .3 * duck)
mix = mix[: int(total * SR)]; mix *= 0.89 / (np.abs(mix).max() + 1e-9)
sf.write(HERE / "assets" / "mix.wav", mix, SR, subtype="PCM_16")

# ---------------- html ----------------
caps = []
for line in script["lines"]:
    c = cues[line["id"]]
    caps.append(f'<div id="cap-{line["id"]}" class="clip caption" data-start="{c["s"]-0.03:.3f}" '
                f'data-duration="{c["d"]+max(0.0, min(0.3, line["gap_after"]-0.08)):.3f}" data-track-index="10">{line["caption"]}</div>')
chap_html = "\n    ".join(f'<div id="chap-{c["id"]}" class="chap">{c["label"]}</div>' for c in chapters if c["label"])
audio = f'<audio id="mix" class="clip" data-start="0" data-duration="{total:.3f}" data-track-index="20" src="assets/mix.wav"></audio>'
html = (HERE / "src" / "index.template.html").read_text()
html = (html.replace("__TOTAL__", str(total)).replace("__CUES__", json.dumps(cues))
            .replace("__CHAPTER_TIMES__", json.dumps(chapters)).replace("__CHAPTERS__", chap_html)
            .replace("<!--__CAPTIONS__-->", "\n".join(caps)).replace("<!--__AUDIO__-->", audio))
(HERE / "index.html").write_text(html)
shutil.copyfile(HERE.parent.parent / "node_modules" / "gsap" / "dist" / "gsap.min.js", HERE / "assets" / "gsap.min.js")
print("total", total, "s")
