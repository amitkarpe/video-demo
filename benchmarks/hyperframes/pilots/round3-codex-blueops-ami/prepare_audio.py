"""Offline master narration and cue clock; source speech remains unchanged."""
from pathlib import Path
import hashlib,json,math,subprocess,wave
P=Path(__file__).resolve().parent
rows=json.loads((P/'script.json').read_text());ledger=json.loads((P/'api-spend.json').read_text())
sr=24000;pcm=bytearray(b'\0'*int(.8*sr)*2);cues=[]
for i,row in enumerate(rows):
    f=P/'assets'/f'voice-{i:02}.wav';r=next(c for c in ledger['calls'] if c['name']==f'voice-{i:02}')
    assert r['status']=='completed' and r['output_sha256']==hashlib.sha256(f.read_bytes()).hexdigest()
    with wave.open(str(f)) as w:
        assert w.getframerate()==sr and w.getnchannels()==1 and w.getsampwidth()==2
        frames=w.readframes(w.getnframes())
    start=len(pcm)/2/sr;length=len(frames)/2/sr
    cues.append(dict(index=i,scene=row['scene'],start=start,duration=length,text=row['text'],spoken=row['spoken']))
    pcm.extend(frames)
    gap=.48 if i+1<len(rows) and rows[i+1]['scene']==row['scene'] else 1.05
    pcm.extend(b'\0'*round(gap*sr)*2)
duration=math.ceil(len(pcm)/2/sr+2.2);pcm.extend(b'\0'*(duration*sr-len(pcm)//2)*2)
with wave.open(str(P/'assets/narration.wav'),'wb') as w:w.setparams((1,2,sr,len(pcm)//2,'NONE','not compressed'));w.writeframes(pcm)
scenes=[]
for c in cues:
    if not scenes or scenes[-1]['id']!=c['scene']:scenes.append(dict(id=c['scene'],start=max(0,c['start']-.45),first_cue=c['index']))
for i,s in enumerate(scenes):s['end']=scenes[i+1]['start'] if i+1<len(scenes) else duration
(P/'timing.json').write_text(json.dumps(dict(duration=duration,cues=cues,scenes=scenes),indent=2)+'\n')
(P/'transcript.txt').write_text('\n\n'.join(r['text'] for r in rows)+'\n')
subprocess.run(['ffmpeg','-y','-v','error','-i',str(P/'assets/narration.wav'),'-af','loudnorm=I=-18:TP=-2:LRA=9','-ar','24000',str(P/'assets/narration-mix.wav')],check=True)
print(json.dumps(dict(duration=duration,scenes=scenes)))
