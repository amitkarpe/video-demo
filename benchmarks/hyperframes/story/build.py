#!/usr/bin/env python3
"""Build a fictional, locally voiced cybersecurity story with seekable shots."""
import argparse, html, json, math
from pathlib import Path
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro
p=argparse.ArgumentParser();p.add_argument('--model',required=True);p.add_argument('--voices',required=True);a=p.parse_args()
r=Path(__file__).resolve().parent;d=r/'assets';d.mkdir(exist_ok=True)
# Dialogue is fictional, and does not claim the project prevented the incident.
script=[
('NARRATOR','am_michael','Monday morning. A company discovers an intrusion.','boardroom.png','50%'),
('CEO','am_adam','How did we miss this?','boardroom.png','18%'),
('CISO','af_heart','We had alerts. Too many to investigate in time.','ciso.png','50%'),
('NARRATOR','am_michael','Attackers can use AI to move faster. Defenders need help connecting the clues.','threat.png','50%'),
('ENGINEER','am_michael','Give me evidence I can trust, not another mountain of alerts.','engineer.png','40%'),
('NARRATOR','am_michael','In an isolated training lab, the agentic pentest proof of concept groups scanner findings and uses AI to propose the next action.','engineer.png','65%'),
('CISO','af_heart','And who controls the tools?','ciso.png','50%'),
('ENGINEER','am_michael','A fixed policy gate. The model never gets them.','engineer.png','40%'),
('NARRATOR','am_michael','People review the findings. The audit keeps the trail.','boardroom.png','65%')]
k=Kokoro(a.model,a.voices);clips=[];t=.45
for i,(speaker,voice,words,pic,focus) in enumerate(script):
    wav,sr=k.create(words,voice=voice,speed=1.02,lang='en-us');sf.write(d/f'line-{i+1}.wav',wav,sr,subtype='PCM_16');dur=len(wav)/sr
    clips.append(dict(start=round(t,3),duration=dur,caption_duration=max(dur,2.1),speaker=speaker,text=words,image=pic,focus=focus));t+=max(dur,2.1)+.55
end=math.ceil(t+1)
sr=24000;times=np.arange(end*sr)/sr;env=np.minimum(times/2,1)*np.minimum((end-times)/2,1);bed=(.025*np.sin(2*np.pi*55*times)+.015*np.sin(2*np.pi*82.5*times)+.01*np.sin(2*np.pi*110*times))*env
for c in clips:
    if c['speaker']=='NARRATOR':
        q=np.maximum(times-c['start'],0);bed+=.065*np.sin(2*np.pi*49*q)*np.exp(-q*3)*(times>=c['start'])
sf.write(d/'underscore.wav',bed,sr,subtype='PCM_16')
def ts(x):
    n=round(x*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'
(r/'captions.srt').write_text('\n'.join(f'{i+1}\n{ts(c["start"])} --> {ts(c["start"]+c["caption_duration"])}\n{c["speaker"]}: {c["text"]}\n' for i,c in enumerate(clips)))
(r/'storyboard.json').write_text(json.dumps({'fictional':True,'duration':end,'segments':clips},indent=2)+'\n')
shots=[];voices=[];caps=[];anims=[]
for i,c in enumerate(clips):
    start=0 if i==0 else c['start']-.25;stop=clips[i+1]['start']-.25 if i+1<len(clips) else end;duration=stop-start
    shots.append(f'<div id="shot{i}" class="clip shot" data-start="{start:.3f}" data-duration="{duration:.3f}" data-track-index="{i}"><div class="image" style="background-image:url(assets/{c["image"]});background-position:{c["focus"]} center"></div></div>')
    voices.append(f'<audio id="voice{i}" class="clip" data-start="{c["start"]}" data-duration="{c["duration"]:.3f}" data-track-index="20" src="assets/line-{i+1}.wav"></audio>')
    caps.append(f'<div class="clip subtitle" data-start="{c["start"]}" data-duration="{c["caption_duration"]:.3f}" data-track-index="15"><span>{html.escape(c["speaker"])}</span> {html.escape(c["text"])}</div>')
    anims.append(f'tl.fromTo("#shot{i} .image",{{scale:1.04,x:0}},{{scale:1.14,x:{25 if i%2 else -25},duration:{duration:.3f},ease:"none"}},{start:.3f});')
    if i: anims.append(f'tl.fromTo("#shot{i} .image",{{opacity:.3}},{{opacity:1,duration:.45,ease:"power2.out"}},{start:.3f});')
page=f'''<!doctype html><html><head><meta charset="utf-8"><script src="assets/gsap.min.js"></script><style>
*{{box-sizing:border-box}}html,body{{margin:0;width:1920px;height:1080px;overflow:hidden;background:#05090f;color:#fff;font-family:Arial,sans-serif}}#root{{width:1920px;height:1080px;position:relative;overflow:hidden}}.shot{{position:absolute;inset:0;overflow:hidden;background:#02080e}}.image{{position:absolute;inset:-35px;background-size:cover;background-repeat:no-repeat;transform-origin:center center}}.grade{{position:absolute;inset:0;background:linear-gradient(0deg,#02060df5,transparent 33%,transparent 76%,#02060d99);pointer-events:none}}.label{{position:absolute;top:54px;right:70px;color:#edf4f8;font-size:28px;letter-spacing:3px;background:#03080aba;padding:12px 16px}}.subtitle{{position:absolute;bottom:100px;left:205px;width:1510px;text-align:center;font-size:38px;line-height:1.25;font-weight:600;text-shadow:0 2px 5px #000;padding:18px 30px;background:#03070cc9;border-radius:8px}}.subtitle span{{font-size:28px;letter-spacing:2px;color:#80e6e1;margin-right:13px}}
</style></head><body><div id="root" data-composition-id="story" data-start="0" data-duration="{end}" data-width="1920" data-height="1080">{''.join(shots)}<div class="grade"></div><div class="label">FICTIONAL DRAMATIZATION · LAB POC</div>{''.join(caps)}{''.join(voices)}<audio id="music" class="clip" data-start="0" data-duration="{end}" data-track-index="21" src="assets/underscore.wav"></audio></div><script>window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});{''.join(anims)}window.__timelines.story=tl;</script></body></html>'''
(r/'index.html').write_text(page);print(json.dumps({'duration':end,'segments':clips},indent=2))
