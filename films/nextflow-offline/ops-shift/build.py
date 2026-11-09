#!/usr/bin/env python3
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
