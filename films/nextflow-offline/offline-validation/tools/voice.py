#!/usr/bin/env python3
"""Revision 2 audio: lay out the Kokoro lines (voice/sNN.wav) from script.json gaps,
write timing.json and cues.json, then build assets/mix.wav (voice over a ducked music bed)
and review/voice.wav (voice only, for word timings). No network, no paid API.
Music bed: voice/m_Inspired.mp3 ("Inspired", Kevin MacLeod, incompetech.com)."""
import json, subprocess, pathlib
D = pathlib.Path(__file__).resolve().parent.parent
s = json.loads((D / "script.json").read_text())
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)]))
t, cues, timing = s["lead_in"], {}, {}
for l in s["lines"]:
    d = round(dur(D / "voice" / f"{l['id']}.wav"), 3)
    cues[l["id"]] = {"s": round(t, 3), "e": round(t + d, 3), "d": d}; timing[l["id"]] = d
    t += d + l["gap_after"]
total = round(t - s["lines"][-1]["gap_after"] + s["tail"], 3)
(D / "timing.json").write_text(json.dumps(timing, indent=2) + "\n")
(D / "cues.json").write_text(json.dumps({"total": total, "cues": cues}, indent=2) + "\n")
L = s["lines"]; drill = next(l["id"] for l in L if l["caption"].startswith("And if anything tries"))
nxt = L[[l["id"] for l in L].index(drill) + 1]["id"]
a, b = cues[drill]["s"] - 0.3, cues[nxt]["s"] - 0.2
ins = sum([["-i", str(D / "voice" / f"{l['id']}.wav")] for l in L], [])
f = "".join(f"[{i}:a]aresample=48000,adelay={int(cues[l['id']]['s']*1000)}|{int(cues[l['id']]['s']*1000)}[v{i}];" for i, l in enumerate(L))
vmix = "".join(f"[v{i}]" for i in range(len(L))) + f"amix=inputs={len(L)}:normalize=0,pan=stereo|c0=c0|c1=c0,volume=1.6,apad=whole_dur={total}[voice]"
mus = (f"[{len(L)}:a]atrim=start=80:duration={total},asetpts=PTS-STARTPTS,aresample=48000,"
       f"volume='if(between(t,{a},{b}),0.10,0.28)':eval=frame,afade=t=in:d=1.5,afade=t=out:st={total-4}:d=4[mu]")
full = f + vmix + ";[voice]asplit=2[vo][sc];" + mus + ";[mu][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[duck];[vo][duck]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[out]"
(D / "assets").mkdir(exist_ok=True); (D / "review").mkdir(exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-i", str(D / "voice/m_Inspired.mp3"), "-filter_complex", full, "-map", "[out]", "-t", str(total), "-ar", "48000", str(D / "assets/mix.wav")], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", f + vmix, "-map", "[voice]", "-t", str(total), "-ar", "16000", "-ac", "1", str(D / "review/voice.wav")], check=True)
print(f"total {total}s, drill music dip {a:.1f}-{b:.1f}s")
