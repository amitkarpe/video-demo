#!/usr/bin/env python3
"""Build cues.json, captions.srt, transcript.txt, assets/mix.wav and index.html (no network, no paid API).

Inputs: script.json, timing.json, media/derived/voice/<id>.v1.wav (from tools/derive.py), src/index.template.html.
Captions: one cue per sentence group (<= 2 lines), timed from the measured post-edit clip lengths, split
proportionally to characters inside a line. The score and sound effects are synthesized here with numpy from a
fixed seed: no samples, no third-party audio. Run inside the venv (numpy + soundfile).
"""
import json, pathlib, re, shutil
import numpy as np, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
SR = 48000
script = json.loads((HERE / "script.json").read_text())
timing = json.loads((HERE / "timing.json").read_text())
MAXC = 84   # characters per caption cue (two lines of ~42 at 38 px)

# ---------------- cues / captions / transcript ----------------
def ts(x):
    h, r = divmod(x, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}".replace(".", ",")
def chunks(text):
    """Split a caption into sentence groups of <= MAXC chars (split long sentences at commas/dashes/colons)."""
    sents = re.findall(r"[^.?!;]+[.?!;]?[”\"]?\s*", text)
    parts = []
    for s in (x.strip() for x in sents if x.strip()):
        while len(s) > MAXC:
            cut = max((m.end() for m in re.finditer(r"[,:—]\s", s[:MAXC])), default=0) or s[:MAXC].rfind(" ")
            parts.append(s[:cut].strip()); s = s[cut:].strip()
        parts.append(s)
    out = []
    for p in parts:
        if out and len(out[-1]) + 1 + len(p) <= MAXC: out[-1] += " " + p
        else: out.append(p)
    # rebalance: never leave a stranded short tail (< 24 chars) after a long cue
    for k in range(1, len(out)):
        while len(out[k]) < 24 and len(out[k - 1]) > 40:
            head, _, last = out[k - 1].rpartition(" ")
            out[k - 1], out[k] = head, last + " " + out[k]
    # merge a very short chunk into its neighbour when the pair still fits two caption lines
    k = 0
    while k < len(out) - 1:
        if (len(out[k]) < 24 or len(out[k + 1]) < 24) and len(out[k]) + 1 + len(out[k + 1]) <= 100:
            out[k] = out[k] + " " + out.pop(k + 1)
        else: k += 1
    return out
t = script["lead_in"]; cues, srt, words, n = {}, [], [], 0
capcues = []
for line in script["lines"]:
    d = timing[line["id"]]
    cues[line["id"]] = {"s": round(t, 3), "e": round(t + d, 3), "d": d}
    parts = chunks(line["caption"]); tot = sum(len(p) for p in parts); u = t
    for p in parts:
        dd = d * len(p) / tot; n += 1
        srt.append(f"{n}\n{ts(u)} --> {ts(u + dd)}\n{p}\n"); capcues.append((line["id"], u, dd, p)); u += dd
    words.append(line["caption"])
    t += d + line["gap_after"]
total = round(t + script["tail"], 3)
(HERE / "cues.json").write_text(json.dumps({"total": total, "cues": cues}, indent=2) + "\n")
(HERE / "captions.srt").write_text("\n".join(srt))
(HERE / "transcript.txt").write_text("\n".join(words) + "\n")
S = lambda k: cues[k]["s"]; E = lambda k: cues[k]["e"]; Dd = lambda k: cues[k]["d"]; F = lambda k, f: cues[k]["s"] + cues[k]["d"] * f
chapters = [{"id": c["id"], "label": c["label"], "t": S(c["start"])} for c in script["chapters"]]

# ---------------- synthesis helpers ----------------
rng = np.random.default_rng(20261110)
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
def tick(f=2400, d=.05): x = tt(d); return np.sin(2*np.pi*f*x) * np.exp(-x*120) + .3*bandnoise(len(x), 3000, 9000)*np.exp(-x*200)
def thunk(f=70, d=.5): x = tt(d); return np.sin(2*np.pi*(f*x + 28*(1-np.exp(-x*18))/18))*np.exp(-x*8) + .25*bandnoise(len(x), 700, 4000)*np.exp(-x*60)
def stamp(d=.45): x = tt(d); return .9*np.sin(2*np.pi*(58*x + 30*(1-np.exp(-x*30))/30))*np.exp(-x*14) + .6*bandnoise(len(x), 400, 3000)*np.exp(-x*45)
def paper(d=.35): n = int(d*SR); return bandnoise(n, 1800, 9000) * np.exp(-np.linspace(0, 6, n)) * (1 + .5*np.sin(np.linspace(0, 40, n)))
def printer(d=1.2): x = tt(d); return bandnoise(len(x), 600, 5000) * (.55 + .45*np.sign(np.sin(2*np.pi*18*x))) * np.minimum(1, (d-x)*6) * .6
def chime(fs, d=2.2): x = tt(d); return sum(np.sin(2*np.pi*f*x)*np.exp(-x*(1.8+k*.6)) for k, f in enumerate(fs)) / len(fs)
def deny(d=.5): x = tt(d); return (np.sin(2*np.pi*196*x) + np.sin(2*np.pi*208*x)) * np.exp(-x*7) * .6
def boom(d=2.0): x = tt(d); return np.sin(2*np.pi*46*x)*np.exp(-x*2.3) + .15*bandnoise(len(x), 30, 220)*np.exp(-x*7)
def shimmer(d=2.0): x = tt(d); return sum(np.sin(2*np.pi*f*x + k)*np.exp(-x*2)*(1+np.sin(2*np.pi*(5+k)*x))*.5 for k, f in enumerate([1760, 2217, 2637, 3322]))
NOTE = lambda n: 440.0 * 2 ** ((n - 69) / 12)
def pad(notes, start, dur, gain=1.0):
    x = tt(dur); a = min(1.8, dur / 3); env = np.minimum(1, x / a) * np.minimum(1, (dur - x) / 1.4).clip(0, 1)
    sig = sum(np.sin(2*np.pi*NOTE(n)*x*(1+det)) for n in notes for det in (-0.002, 0.002))
    sig += .4 * np.sin(2*np.pi*NOTE(notes[0]-12)*x)
    put(music, norm(sig) * env * gain, start, 1.0, 0)
def pluck(n, at, gain=.5, pan=0.0):
    x = tt(1.2); f = NOTE(n); s = (np.sin(2*np.pi*f*x) + .4*np.sin(4*np.pi*f*x)) * np.exp(-x*6)
    put(music, s, at, gain, pan)
# a light, steady, modern palette (MIDI) for the Swiss Grid look
C, G, Am, Fa, Dm, Em, Gsus = [48, 55, 60, 64], [43, 55, 59, 62], [45, 57, 60, 64], [41, 57, 60, 65], [50, 57, 62, 65], [40, 55, 59, 64], [43, 55, 60, 62]
def seq(chords, start, end, gain=.7):
    n = len(chords); step = (end - start) / n
    for k, ch in enumerate(chords): pad(ch, start + k*step, step + 1.4, gain)
def arp(start, end, chords, bpm=108, gain=.16):
    beat = 60 / bpm / 2; k = 0; t0 = start
    while t0 < end:
        ch = chords[int((t0 - start) / ((end - start) / len(chords))) % len(chords)]
        pluck(ch[k % len(ch)] + 12, t0, gain * (1.0 if k % 4 == 0 else .6), [-.3, .3][k % 2]); t0 += beat; k += 1
seq([Am, Fa, C, G], 0.0, S("s04"), .65)
seq([C, G, Am, Fa], S("s04") - .4, S("s07"), .65)
seq([Fa, C, G, Am, Fa, Gsus], S("s07") - .4, S("s10"), .7)
arp(S("s08"), E("s09"), [Fa, C, G, Am])
seq([C, G, Am, Fa, C, G], S("s10") - .4, S("s14"), .7)
arp(S("s11"), E("s13"), [C, G, Am, Fa], bpm=112, gain=.14)
seq([Am, Dm, Em, Am, Fa, Gsus], S("s14") - .4, S("s18"), .6)
seq([C, G, Am, Fa, C, G], S("s18") - .4, S("s22"), .7)
arp(S("s19"), E("s20"), [C, G, Am, Fa], bpm=120, gain=.15)
seq([Fa, G, C, C], S("s22") - .4, total, .85)

ev = []
add = lambda *e: ev.append(e)
add(0.2, shimmer(2.4), .14, 0)
for k in range(10): add(S("s01") + 0.4 + k * .12, tick(1800 + 60*k), .12, -.6 + .12*k)
add(F("s02", .62), blip(784), .26, .3)
add(F("s03", .45), chime([659.25, 987.77]), .22, 0)
add(S("s04") - .5, whoosh(1.0, 300, 4000), .26, 0)
add(S("s05") + .2, paper(.4), .22, -.4); add(F("s05", .45), paper(.4), .22, -.4)
add(S("s06") - .2, blip(523.25, .25), .26, .4)
add(S("s07") - .5, whoosh(1.0, 300, 4000), .26, 0)
for f in (.04, .24, .58, .64, .7, .9): add(F("s08", f), thunk(110, .3), .3, 0)
add(S("s09") + .1, whoosh(1.4, 400, 3000), .18, 0)
add(S("s10") - .5, whoosh(1.0, 300, 4000), .26, 0)
add(S("s11") + .1, whoosh(1.2, 600, 5000), .2, -.5); add(F("s12", .2), whoosh(1.2, 600, 5000), .2, 0)
add(S("s13") + .2, chime([880, 1318.5]), .24, .5)
add(S("s14") - .5, whoosh(1.0, 300, 4000), .26, 0)
add(S("s15") + .1, paper(.4), .2, -.3); add(F("s15", .35), thunk(80, .45), .26, 0)
add(S("s16") + .1, paper(.4), .2, -.3); add(S("s17") + .1, stamp(.4), .32, .3)
add(S("s18") - .5, whoosh(1.0, 300, 4000), .26, 0)
for f in (.0, .25, .5, .84): add(F("s19", f) + .1, tick(2100), .26, 0)
add(F("s20", .45), deny(.6), .36, .5); add(F("s20", .8), chime([783.99, 1046.5]), .3, .5)
add(S("s21") + .1, stamp(.4), .3, -.3)
add(S("s22") - .1, chime([523.25, 659.25, 783.99, 1046.5], 3.6), .38, 0); add(S("s22") - .1, boom(2.2), .24, 0)
for at, sig, g, p in ev: put(sfx, norm(sig), at, g, p)

voice = np.zeros(N); vmask = np.zeros(N)
for line in script["lines"]:
    x, sr = sf.read(HERE / "media" / "derived" / "voice" / f"{line['id']}.v1.wav")
    if x.ndim > 1: x = x.mean(axis=1)
    if sr != SR: x = np.interp(np.arange(int(len(x) * SR / sr)) * sr / SR, np.arange(len(x)), x)
    i = int(S(line["id"]) * SR); voice[i:i + len(x)] += x; vmask[i:i + len(x)] = 1
voice = norm(voice)
k = int(0.3 * SR); duck = np.convolve(vmask, np.ones(k) / k, mode="same")
music = music / (np.abs(music).max() + 1e-9); sfx = sfx / (np.abs(sfx).max() + 1e-9)
fade = np.clip(np.arange(N) / SR / 1.5, 0, 1) * np.clip((total - np.arange(N) / SR) / 3.0, 0, 1)
mix = np.zeros((N, 2))
for c in range(2):
    mix[:, c] = voice * .82 + music[:, c] * .15 * (1 - .5 * duck) * fade + sfx[:, c] * .40 * (1 - .35 * duck)
mix = mix[: int(total * SR)]; mix *= 0.89 / (np.abs(mix).max() + 1e-9)
(HERE / "assets").mkdir(exist_ok=True)
raw = HERE / "assets" / "mix-prenorm.wav"; sf.write(raw, mix, SR, subtype="PCM_24")
# two-pass EBU R128 loudness normalisation to the web house default (-16 LUFS, true peak <= -1.5 dBTP)
import subprocess
m = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(raw), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
                    "-f", "null", "-"], capture_output=True, text=True).stderr
ms = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af",
                f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={ms['input_i']}:measured_TP={ms['input_tp']}:measured_LRA={ms['input_lra']}:"
                f"measured_thresh={ms['input_thresh']}:offset={ms['target_offset']}:linear=true", "-ar", str(SR), "-c:a", "pcm_s16le",
                str(HERE / "assets" / "mix.wav")], check=True)
raw.unlink()

# ---------------- html ----------------
caps = []
for i, (lid, u, dd, p) in enumerate(capcues):
    nxt = capcues[i + 1][1] if i + 1 < len(capcues) else u + dd + 0.5
    dur = min(dd + 0.35, nxt - u - 0.04)
    caps.append(f'<div id="cap{i:03d}" class="clip caption" data-start="{u - 0.03:.3f}" data-duration="{dur:.3f}" data-track-index="10">{p}</div>')
chap_html = "\n    ".join(f'<div id="chap-{c["id"]}" class="chap">{c["label"]}</div>' for c in chapters if c["label"])
audio = f'<audio id="mix" class="clip" data-start="0" data-duration="{total:.3f}" data-track-index="20" src="assets/mix.wav"></audio>'
html = (HERE / "src" / "index.template.html").read_text()
html = (html.replace("__TOTAL__", str(total)).replace("__CUES__", json.dumps(cues))
            .replace("__CHAPTER_TIMES__", json.dumps(chapters)).replace("__CHAPTERS__", chap_html)
            .replace("<!--__CAPTIONS__-->", "\n".join(caps)).replace("<!--__AUDIO__-->", audio))
(HERE / "index.html").write_text(html)
shutil.copyfile(HERE.parent / "node_modules" / "gsap" / "dist" / "gsap.min.js", HERE / "assets" / "gsap.min.js")
print("total", total, "s;", len(capcues), "caption cues")
