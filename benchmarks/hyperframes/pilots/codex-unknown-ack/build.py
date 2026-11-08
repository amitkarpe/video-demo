"""Generate new, local narration and an editable deterministic SVG/GSAP film."""
import hashlib, json, math, pathlib, sys, wave
P=pathlib.Path(__file__).resolve().parent
rows=[
('This is a simulation. An approved S3 policy request leaves the backend.','This is a simulation. An approved S three policy request leaves the backend.'),
('But the reply disappears.',None),
('Did the change fail? Or just the reply?',None),
('Before the call, the durable ledger already records CALLING.','Before the call, the durable ledger already records calling.'),
('AWSOps keeps that uncertainty. It does not blindly send another write.','A W S Ops keeps that uncertainty. It does not blindly send another write.'),
('It reconciles the same run, using read-only provider checks.','It reconciles the same run, using read only provider checks.'),
('Here, the observed policy matches.',None),
('But a matching policy is not fresh Config compliance.',None),
('Execution stays UNKNOWN. Compliance stays UNKNOWN.','Execution stays unknown. Compliance stays unknown.'),
('Freshness stays NOT_VERIFIED.','Freshness stays not verified.'),
('The outcome: NEEDS_REVIEW.','The outcome: needs review.'),
('The missing evidence stays visible. This demonstrates control logic, not live acceptance.',None)]
k=None
if '--voice' in sys.argv or any(not (P/f'assets/voice-{i:02}.wav').exists() for i in range(len(rows))):
 import soundfile as sf
 from kokoro_onnx import Kokoro
 for name,digest in [('kokoro-v1.0.onnx','beb0d1848dee9a49da392cc3df26958d46cfa35d321edf434f52949153f0df3a'),('voices-v1.0.bin','bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d')]:
  assert hashlib.sha256((P/'.build'/name).read_bytes()).hexdigest()==digest, name+' integrity mismatch'
 k=Kokoro(str(P/'.build/kokoro-v1.0.onnx'),str(P/'.build/voices-v1.0.bin'))
t=.65; cues=[]
for i,(caption,spoken) in enumerate(rows):
 f=P/f'assets/voice-{i:02}.wav'
 if '--voice' in sys.argv or not f.exists():
  samples,sr=k.create(spoken or caption,voice='am_michael',speed=.98,lang='en-us'); sf.write(f,samples,sr)
 with wave.open(str(f)) as w: dur=w.getnframes()/w.getframerate()
 cues.append(dict(text=caption,start=round(t,3),duration=round(dur,3)))
 t+=dur+(.65 if i in (1,2,6,10) else .32)
duration=math.ceil(t+.8)
(P/'timing.json').write_text(json.dumps(dict(duration=duration,cues=cues),indent=2)+'\n')
def stamp(t):
 ms=round(t*1000); return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["start"]+c["duration"])}\n{c["text"]}' for i,c in enumerate(cues))+'\n')
(P/'transcript.txt').write_text('\n'.join(c['text'] for c in cues)+'\n')
html=(P/'scene.html.template').read_text().replace('__DURATION__',str(duration))
audio=''.join(f'<audio id="voice{i}" class="clip" data-start="{c["start"]}" data-duration="{c["duration"]}" data-track-index="20" src="assets/voice-{i:02}.wav"></audio>' for i,c in enumerate(cues))
caps=''.join(f'<div id="cap{i}" class="caption clip" data-start="{c["start"]}" data-duration="{c["duration"]}" data-track-index="30">{c["text"]}</div>' for i,c in enumerate(cues))
html=html.replace('__MEDIA__',audio+caps).replace('__TIMING__',json.dumps(cues))
(P/'index.html').write_text(html)
print(json.dumps(dict(seconds=duration,cues=len(cues),starts=[c['start'] for c in cues])))
