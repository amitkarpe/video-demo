#!/usr/bin/env python3
import argparse, json
from pathlib import Path
import soundfile as sf
from kokoro_onnx import Kokoro
p=argparse.ArgumentParser();p.add_argument('--model',required=True);p.add_argument('--voices',required=True);a=p.parse_args()
r=Path(__file__).resolve().parent;k=Kokoro(a.model,a.voices)
phrases=['A safe lab!','AI picks an approved step.','Clues join up.','A person checks the report!']
starts=[0.25,1.8,4.55,6.9]
items=[]
for i,(text,start) in enumerate(zip(phrases,starts)):
    samples,sr=k.create(text,voice='am_michael',speed=1.0,lang='en-us');sf.write(r/'assets'/f'voice-{i+1}.wav',samples,sr,subtype='PCM_16');duration=len(samples)/sr
    items.append({'text':text,'start':start,'duration':duration}); print(i+1,round(duration,3),text)
    if start+duration> ([1.8,4.55,6.9,10][i]): raise ValueError('Narration overlaps next cue or exceeds 10 seconds')
(r/'voice.json').write_text(json.dumps(items,indent=2)+'\n')
def ts(t):
    ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(r/'captions.srt').write_text('\n'.join(f'{i+1}\n{ts(x["start"])} --> {ts(x["start"]+x["duration"])}\n{x["text"]}\n' for i,x in enumerate(items)))
