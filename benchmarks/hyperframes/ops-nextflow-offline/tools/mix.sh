#!/usr/bin/env bash
# Build assets/mix.wav: narration lines at fixed starts over a ducked music bed.
# Starts must match timing.json (read by index.html via build.py).
set -euo pipefail
cd "$(dirname "$0")/.."
DUR=$(python3 -c "import json;print(json.load(open('timing.json'))['duration'])")
read -r -a ST < <(python3 -c "import json;print(' '.join(str(int(l['start']*1000)) for l in json.load(open('timing.json'))['lines']))")
in=(); f=""
for i in 0 1 2 3 4 5; do in+=(-i "assets/l$((i+1)).wav"); f+="[$i:a]aresample=48000,adelay=${ST[$i]}|${ST[$i]}[v$i];"; done
f+="[v0][v1][v2][v3][v4][v5]amix=inputs=6:normalize=0,pan=stereo|c0=c0|c1=c0,volume=1.6,apad=whole_dur=${DUR}[voice];"
f+="[voice]asplit=2[vo][sc];"
# music: dips during the failure drill (t 32-40.5), returns for the payoff
f+="[6:a]atrim=start=80:duration=${DUR},asetpts=PTS-STARTPTS,aresample=48000,volume='if(between(t,32,40.5),0.10,0.30)':eval=frame,afade=t=in:d=1.2,afade=t=out:st=$(python3 -c "print(${DUR}-3)"):d=3[mu];"
f+="[mu][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[duck];"
f+="[vo][duck]amix=inputs=2:normalize=0,alimiter=limit=0.95[out]"
ffmpeg -v error -y "${in[@]}" -i assets/m_Inspired.mp3 -filter_complex "$f" -map "[out]" -t "$DUR" -ar 48000 assets/mix.wav
echo "mix.wav $(ffprobe -v error -show_entries format=duration -of csv=p=0 assets/mix.wav)s"
