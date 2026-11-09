#!/usr/bin/env python3
"""Build cues.json, captions.srt, transcript.txt, assets/mix.wav and index.html (no network, no paid API).
The shared steps live in toolkit/av.py; this file keeps only this film's score and sound-effect cues.
Run with a Python that has numpy and soundfile (see the repository README)."""
import pathlib, sys
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "toolkit").is_dir())
sys.path.insert(0, str(ROOT / "toolkit")); import av
av.setup(globals(), __file__, seed=20261109)
# a bright, bouncy toy-box palette (MIDI) for look C
C, G, Am, Fa, Dm, Em, Gsus = [48, 55, 60, 64], [43, 55, 59, 62], [45, 57, 60, 64], [41, 57, 60, 65], [50, 57, 62, 65], [40, 55, 59, 64], [43, 55, 60, 62]
def seq(chords, start, end, gain=.7):
    n = len(chords); step = (end - start) / n
    for k, ch in enumerate(chords): pad(ch, start + k*step, step + 1.4, gain)
def arp(start, end, chords, bpm=116, gain=.16):
    beat = 60 / bpm / 2; k = 0; t0 = start
    while t0 < end:
        ch = chords[int((t0 - start) / ((end - start) / len(chords))) % len(chords)]
        pluck(ch[k % len(ch)] + 12, t0, gain * (1.0 if k % 4 == 0 else .6), [-.3, .3][k % 2]); t0 += beat; k += 1
seq([C, Am, Fa, G], 0.0, S("s04"), .6)
arp(S("s02"), E("s03"), [C, Am, Fa, G], bpm=104, gain=.12)
seq([C, G, Am, Fa], S("s04") - .4, S("s08"), .65)
arp(S("s05"), E("s06"), [C, G, Am, Fa], bpm=116)
seq([Fa, C, G, Am, Fa, C], S("s08") - .4, S("s12"), .7)
arp(S("s09"), E("s10"), [Fa, C, G, Am], bpm=120, gain=.15)
seq([C, G, Am, Fa, Dm, Gsus], S("s12") - .4, S("s16"), .65)
arp(S("s13"), E("s14"), [C, G, Am, Fa], bpm=120, gain=.13)
seq([Am, Em, Fa, C], S("s16") - .4, S("s18"), .5)
seq([C, G, Fa, C, Am, G, Fa, C], S("s18") - .4, S("s21"), .7)
arp(S("s18"), E("s18"), [C, G, Fa, C], bpm=120, gain=.13)
seq([Am, Dm, Em, Am], S("s21") - .4, S("s24"), .55)
seq([C, G, Am, Fa], S("s24") - .4, S("s26"), .7)
arp(S("s24"), E("s25"), [C, G, Am, Fa], bpm=120, gain=.13)
seq([Fa, G, C, C], S("s26") - .4, total, .85)

ev = []
add = lambda *e: ev.append(e)
add(0.2, shimmer(2.4), .14, 0)
for k in range(3): add(S("s01") + 2.0 + k * .45, thunk(120 - 15*k, .35), .3, -.2 + .2*k)   # crates land
add(S("s04") - .5, whoosh(1.2, 300, 4000), .24, 0)
add(S("s05") + .4, whoosh(1.4, 300, 3000), .2, -.4)
for k in range(4): add(F("s05", .35) + k * .5, tick(1600 + 120*k), .14, -.5)
add(S("s06") + .4, whoosh(1.4, 300, 3000), .2, .4)
add(S("s08") + .3, whoosh(1.0, 500, 5000), .2, 0)
add(S("s08") + 3.3, chime([1046.5, 1318.5, 1568], 1.4), .24, -.3)      # the base image splits
for f, pan in ((.02, -.3), (.33, -.1), (.63, .4)): add(F("s09", f) + .1, blip(784, .2), .28, pan); add(F("s09", f) + .2, thunk(150, .3), .22, pan)
for k in range(3): add(S("s10") + .3 + k * .25, paper(.3), .14, -.4 + .4*k)
add(S("s12") + .1, whoosh(1.2, 400, 4000), .22, 0)
add(F("s13", .45), chime([880, 1318.5]), .26, .2)
add(F("s14", .35), thunk(140, .3), .26, -.4); add(F("s14", .5), tick(2200), .18, -.4)
add(F("s15", .14), deny(.5), .32, 0); add(F("s15", .28), thunk(70, .45), .34, 0)
add(S("s16") - .8, boom(2.0), .16, 0)
for k in range(8): add(S("s16") + 0.5 + k * .55, tick(2400), .14, -.5 + .14*k)
add(F("s17", .4), chime([1046.5, 1318.5], 1.4), .24, .2)
for f in (.3, .6): add(F("s18", f), whoosh(.6, 900, 5000), .14, 0); add(F("s18", f) + .35, thunk(160, .25), .22, 0)
add(F("s18", .58), chime([1046.5, 1318.5], 1.2), .2, -.3)
add(S("s19") + .2, blip(659.25, .2), .18, 0)
add(S("s20") + .25, blip(523.25, .3), .22, .3)
for k in range(5): add(F("s20", .12) + k * .28, tick(1800), .14, .3)
add(F("s20", .46), thunk(60, .6), .28, .3); add(F("s20", .74), chime([523.25, 783.99, 1046.5], 2.0), .3, .3)
add(S("s21") + .5, deny(.5), .18, .4)
for k in range(3): add(S("s22") + 0.2 + k * .4, tick(2400), .16, .4)
add(F("s22", .7), whoosh(.8, 900, 5000), .18, .4)
add(S("s23") - .05, stamp(.45), .38, 0)
add(S("s24") + .5, paper(.4), .22, .3)
for k in range(4): add(F("s24", .25 + k * .13), blip(784 + 98*k), .2, .3)
add(S("s25") + .1, blip(659.25), .2, -.3); add(F("s25", .62), stamp(.4), .28, -.3)
add(S("s26") - .1, chime([523.25, 659.25, 783.99, 1046.5], 3.6), .38, 0); add(S("s26") - .1, boom(2.2), .22, 0)
av.finish(globals())
