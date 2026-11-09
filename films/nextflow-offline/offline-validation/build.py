#!/usr/bin/env python3
"""Build cues.json, captions.srt, transcript.txt, assets/mix.wav and index.html (no network, no paid API).
The shared steps live in toolkit/av.py; this file keeps only this film's score and sound-effect cues.
Run with a Python that has numpy and soundfile (see the repository README)."""
import pathlib, sys
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "toolkit").is_dir())
sys.path.insert(0, str(ROOT / "toolkit")); import av
av.setup(globals(), __file__, seed=20261109, merge_short=False)
# a warm, confident major palette (MIDI)
C, G, Am, Fa, Dm, Em, Esus, Fmaj7, Gsus = [48, 55, 60, 64], [43, 55, 59, 62], [45, 57, 60, 64], [41, 57, 60, 65], [50, 57, 62, 65], [40, 55, 59, 64], [52, 57, 59, 64], [41, 57, 60, 64], [43, 55, 60, 62]
def seq(chords, start, end, gain=.8):
    n = len(chords); step = (end - start) / n
    for k, ch in enumerate(chords): pad(ch, start + k*step, step + 1.4, gain)
def arp(start, end, chords, bpm=96, gain=.2):
    beat = 60 / bpm / 2; k = 0; t0 = start
    while t0 < end:
        ch = chords[int((t0 - start) / ((end - start) / len(chords))) % len(chords)]
        pluck(ch[k % len(ch)] + 12, t0, gain * (1.0 if k % 4 == 0 else .65), [-.35, .35][k % 2]); t0 += beat; k += 1
seq([Am, Fa], 0.0, S("s03"), .7)
seq([Dm, Esus], S("s03") - .3, S("s04"), .75)
seq([C, G, Am, Fa], S("s04") - .3, S("s06"), .85)
seq([C, G, Am, Fa, C, G, Fa, Gsus], S("s06") - .5, S("s10"), .8)
arp(S("s07"), E("s09"), [C, G, Am, Fa], bpm=92, gain=.16)
seq([Fa, C, G, Am, Fa, C, Gsus, G], S("s10") - .5, S("s14"), .8)
arp(S("s10"), E("s13"), [Fa, C, G, Am], bpm=104, gain=.2)
seq([Am, Fa, C, G, Dm, Esus], S("s14") - .5, S("s17"), .75)
seq([C, G, Am, Fa, C, G, Fa, G], S("s17") - .5, S("s21"), .8)
arp(S("s18"), E("s20"), [C, G, Am, Fa], bpm=112, gain=.18)
seq([Am, Em, Fa, G, Am, Fmaj7], S("s21") - .5, S("s25"), .7)
seq([Fa, G, C, Am, Fa, Gsus], S("s25") - .5, S("s28"), .8)
seq([C, G, Am, Fa, C, G, Fa, C], S("s28") - .5, total, .95)

ev = []  # (time, signal, gain, pan)
add = lambda *e: ev.append(e)
add(0.1, boom(2.6), .45, 0); add(0.4, shimmer(3.0), .16, -.4)
add(F("s01", .45), blip(660), .28, -.5)
for k, f in enumerate([.14, .34, .46, .66]): add(F("s02", f), blip(740 + 90*k), .26, -.3 + .2*k)
add(S("s03"), whoosh(1.4, 150, 2500), .32, 0); add(F("s03", .62), deny(.7), .42, 0)
add(S("s04"), whoosh(1.2, 300, 4000), .3, 0)
add(F("s04", .62), chime([523.25, 783.99, 1046.5], 3.2), .42, 0); add(F("s04", .62), boom(2.2), .35, 0)
add(S("s05") - .2, paper(.5), .3, .2)
add(S("s06") - .6, whoosh(1.4, 150, 2500), .35, 0)
add(S("s07") - .2, whoosh(1.0, 200, 3000), .22, -.4); add(F("s07", .5) - .3, whoosh(1.0, 200, 3000), .22, 0); add(S("s08") - .2, whoosh(1.0, 200, 3000), .22, .4)
add(S("s09") + .3, shimmer(2.6), .2, 0)
for k, dt in enumerate([.35, .95, 1.65]): add(S("s09") + dt, blip(880 + 110*k, .2), .26, -.5 + .5*k)
for k in range(3): add(F("s09", .55) + k*.25 + .3, tick(1900), .22, .5)
add(S("s10") - 1.0, whoosh(1.3, 200, 4000), .38, 0); add(S("s10") + .35, thunk(70, .5), .45, 0)
add(F("s10", .6) + .2, whoosh(1.0, 300, 3500), .25, -.4)
for k in range(5): add(S("s11") + .4 + k*.22, whoosh(.6, 400, 4000), .14, -.1 + .02*k)
add(F("s12", .35) + .2, whoosh(1.1, 300, 3500), .25, .4)
add(S("s13") + .3, chime([659.25, 987.77]), .32, 0)
add(S("s14") - 1.0, whoosh(1.3, 200, 4000), .38, 0)
add(F("s14", .4), shimmer(3.0), .16, 0)
for f in (.5, .58, .66, .74): add(F("s14", f), tick(2200), .32, -.3)
for i in range(10): add(F("s14", .8) + i*.09, tick(1700 + 40*i), .2, .2)
add(F("s14", .8) + 1.0, tick(2400), .32, -.3)
add(F("s15", .55) + .3, stamp(), .6, .3)
add(S("s16") + .2, deny(.6), .4, -.3)
add(S("s17") - 1.0, whoosh(1.3, 200, 4000), .38, 0); add(S("s17") + .2, paper(.45), .3, -.4)
for i, f in enumerate([.32, .37, .42, .47, .53, .58, .63, .7, .82, .9]): add(F("s18", f), tick(1500 + 70*i), .3, -.6 + .13*i)
for t0 in (S("s19") - .3, S("s19"), S("s19") + .5, F("s19", .4), F("s19", .62)): add(t0, thunk(95, .35), .3, 0)
add(F("s19", .82), deny(.5), .3, .5)
add(S("s20") + .1, blip(784), .24, -.2); add(S("s20") + .4, blip(659), .24, -.4)
add(S("s21") - 1.0, whoosh(1.3, 200, 4000), .38, 0); add(S("s21") + .3, thunk(65, .5), .4, 0)
for k in range(6): add(F("s21", .58) + k*.2 + .3, whoosh(.5, 500, 5000), .12, -.6)
for f in (.05, .38, .7): add(F("s23", f), deny(.45), .34, .5)
add(S("s24"), shimmer(2.4), .2, 0)
add(S("s25") - .5, whoosh(1.2, 150, 2500), .3, 0)
for f in (.32, .62, .88): add(F("s26", f), tick(2300), .32, 0)
add(F("s27", .3), stamp(.4), .45, 0); add(F("s27", .3), chime([783.99, 1046.5, 1318.5], 2.6), .38, 0)
add(S("s28") - 1.0, whoosh(1.6, 100, 1800), .35, 0)
for k, f in enumerate([.06, .3, .46, .64, .82]): add(F("s28", f), blip(523.25 * 2 ** (k / 6), .25), .26, -.6 + .3*k)
add(S("s30") - .1, chime([523.25, 659.25, 783.99, 1046.5], 3.8), .42, 0); add(S("s30") - .1, boom(2.4), .32, 0)
add(E("s30") + .8, shimmer(3.0), .18, 0)
av.finish(globals())
