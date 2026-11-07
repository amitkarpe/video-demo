#!/usr/bin/env python3
"""Build a local, seekable narrated technical film from verified lab facts."""
import argparse, json, math, html, hashlib
from pathlib import Path
import soundfile as sf
from kokoro_onnx import Kokoro
p=argparse.ArgumentParser();p.add_argument('--model',required=True);p.add_argument('--voices',required=True);p.add_argument('--reuse-audio',action='store_true');a=p.parse_args()
r=Path(__file__).resolve().parent;assets=r/'assets';assets.mkdir(exist_ok=True)
scenes=[(f'{i+1:02}',c['title'].upper(),'EVIDENCE THREAD: grp-d382cb1578',c['words']) for i,c in enumerate(json.loads((r/'script.json').read_text()))]
import re
cache_path=r/"speech-cache.json"
cache=json.loads(cache_path.read_text()) if cache_path.exists() else {}
k=None if a.reuse_audio else Kokoro(a.model,a.voices); clips=[]; cues=[];t=.6
for i,(num,title,tag,words) in enumerate(scenes):
 scene_start=t; sentences=re.split(r'(?<=[.!?])\s+',words)
 for j,sentence in enumerate(sentences):
  path=assets/f'voice-{i+1}-{j+1}.wav'
  digest=hashlib.sha256(('am_michael|1.0|'+sentence).encode()).hexdigest()
  if a.reuse_audio or (path.exists() and cache.get(path.name)==digest): audio,sr=sf.read(path)
  else:
   audio,sr=k.create(sentence,voice='am_michael',speed=1.0,lang='en-us');sf.write(path,audio,sr,subtype='PCM_16')
  cache[path.name]=digest
  duration=len(audio)/sr;cues.append(dict(start=round(t,3),duration=round(duration,3),words=sentence,path=f'assets/{path.name}'));t+=duration+.16
 clips.append(dict(number=num,title=title,tag=tag,words=words,start=round(scene_start,3),duration=round(t-scene_start,3)));t+=.45
 print(num,round(t-scene_start,2),flush=True)
end=math.ceil(t+0.4); print('TOTAL',end,flush=True)
# Runtime follows the naturally spoken script; no duration gate.
def stamp(x):
 ms=round(x*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(r/'captions.srt').write_text('\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["start"]+c["duration"])}\n{c["words"]}\n' for i,c in enumerate(cues)))
(r/'cues.json').write_text(json.dumps(cues,indent=2)+'\n')
(r/'storyboard.json').write_text(json.dumps({'duration':end,'scenes':clips},indent=2)+'\n')
(r/'transcript.txt').write_text('\n\n'.join(f"{c['number']} — {c['title']}\n{c['words']}" for c in clips)+'\n')

cache_path.write_text(json.dumps(cache,indent=2)+"\n")
