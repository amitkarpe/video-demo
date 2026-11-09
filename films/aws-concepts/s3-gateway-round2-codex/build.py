"""Offline rebuild: validate cached narration, compose timing, score and HTML."""
from pathlib import Path
import array, hashlib, html, json, math, textwrap, wave

P = Path(__file__).resolve().parent
rows = json.loads((P / 'script.json').read_text())
ledger = json.loads((P / 'openai-spend.json').read_text())
cues = []
t = 0.6
for i, row in enumerate(rows):
    asset = P / f'assets/voice-{i:02}.wav'
    receipt = next(c for c in ledger['calls'] if c['cue'] == i)
    assert receipt['status'] == 'completed'
    assert receipt['input_sha256'] == hashlib.sha256(row['spoken'].encode()).hexdigest()
    assert receipt['output_sha256'] == hashlib.sha256(asset.read_bytes()).hexdigest()
    with wave.open(str(asset)) as wav:
        duration = wav.getnframes() / wav.getframerate()
    cues.append(dict(start=round(t, 4), duration=duration, text=row['caption']))
    t += duration + (0.48 if i in (1, 5, 7, 10) else 0.25)
duration = max(45, math.ceil(t + 1.35))
assert 45 <= duration <= 60, f'Film duration {duration} requires editorial adjustment'
(P / 'timing.json').write_text(json.dumps(dict(duration=duration, cues=cues), indent=2)+'\n')

def timestamp(t):
    ms=round(t*1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'

srt=[]; media=[]; captions=[]
for i,c in enumerate(cues):
    wrapped='\n'.join(textwrap.wrap(c['text'], 47))
    srt.append(f'{i+1}\n{timestamp(c["start"])} --> {timestamp(c["start"]+c["duration"])}\n{wrapped}\n')
    media.append(f'<audio id="voice{i}" class="clip" data-start="{c["start"]}" data-duration="{c["duration"]}" data-track-index="20" src="assets/voice-{i:02}.wav"></audio>')
    captions.append(f'<div id="cap{i}" class="caption"><span>{html.escape(wrapped).replace(chr(10), "<br>")}</span></div>')
(P/'captions.srt').write_text('\n'.join(srt))
(P/'transcript.txt').write_text('\n\n'.join(r['caption'] for r in rows)+'\n')

# Original deterministic score. Quiet harmonic bed and event accents, no samples.
sr=24000; samples=array.array('f', [0.0])*int(duration*sr)
def tone(start, length, freq, gain, kind='pluck'):
    offset=int(start*sr); n=int(length*sr)
    for j in range(min(n, len(samples)-offset)):
        sec=j/sr
        env=(1-math.exp(-sec*45))*math.exp(-sec*(5 if kind=='pluck' else 1.2))
        env*=min(1, (length-sec)*12)
        value=math.sin(2*math.pi*freq*sec)+0.2*math.sin(4*math.pi*freq*sec)
        samples[offset+j] += gain*env*value
# A restrained D minor ninth pulse; the moving packet supplies the rhythm.
notes=[146.8324,220.0,261.6256,329.6276,293.6648,220.0,261.6256,164.8138]
beat=60/98
for k in range(int(duration/beat)):
    tone(k*beat, 1.5, notes[k%8], 0.011 if k%4==0 else 0.006)
for k in range(0,duration,5):
    tone(k, 4.8, 73.4162 if (k//5)%2==0 else 65.4064, 0.009, 'pad')
for i in (2,3,4,5,6,8,10,11):
    tone(cues[i]['start'], 0.7, [440,523.251,659.255][i%3], 0.021)
pcm=array.array('h')
for j,v in enumerate(samples):
    fade=min(1,j/sr/1.2,(duration-j/sr)/1.8)
    pcm.append(round(max(-1,min(1,v*max(0,fade)))*32767))
with wave.open(str(P/'assets/score.wav'),'wb') as w:
    w.setparams((1,2,sr,len(pcm),'NONE','not compressed'));w.writeframes(pcm.tobytes())
media.append(f'<audio id="score" class="clip" data-start="0" data-duration="{duration}" data-track-index="21" src="assets/score.wav"></audio>')
source=(P/'scene.html.template').read_text()
source=source.replace('__DURATION__',str(duration)).replace('__CUES__',json.dumps(cues)).replace('__MEDIA__','\n'.join(media)).replace('__CAPTIONS__','\n'.join(captions))
(P/'index.html').write_text(source)
print(json.dumps(dict(duration=duration,cue_starts=[c['start'] for c in cues],speech_seconds=sum(c['duration'] for c in cues))))
