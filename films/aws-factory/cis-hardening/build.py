#!/usr/bin/env python3
"""Build cues.json, captions.srt, transcript.txt, assets/mix.wav and index.html (no network, no paid API).
The shared steps live in toolkit/av.py; this file keeps only this film's score and sound-effect cues.
Run with a Python that has numpy and soundfile (see the repository README)."""
import pathlib, sys
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "toolkit").is_dir())
sys.path.insert(0, str(ROOT / "toolkit")); import av
av.setup(globals(), __file__, seed=20261110)
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
av.finish(globals())
