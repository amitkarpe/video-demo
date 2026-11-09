#!/usr/bin/env python3
"""Build a cinematic, seekable HyperFrames teaser; speech is generated offline."""
import argparse, html, math, json, wave
from pathlib import Path
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

p=argparse.ArgumentParser();p.add_argument('--model',required=True);p.add_argument('--voices',required=True);a=p.parse_args()
r=Path(__file__).resolve().parent; d=r/'assets'; d.mkdir(exist_ok=True)
lines=["What if an attack leaves a trail of noise?", "Six scanner alerts. One hidden weakness. AI connects the evidence.", "Policy controls the tools. A human gets a finding, ready to review."]
k=Kokoro(a.model,a.voices); clips=[]; starts=[0.6,5.1,11.0]
for i,text in enumerate(lines):
    wav,sr=k.create(text,voice='am_michael',speed=1.05,lang='en-us'); sf.write(d/f'cinema-voice-{i+1}.wav',wav,sr,subtype='PCM_16'); clips.append(dict(start=starts[i],duration=len(wav)/sr,text=text))
end=max(18,math.ceil(clips[-1]['start']+clips[-1]['duration']+1.2));sr=24000;t=np.arange(end*sr)/sr
# Original synthesized tension bed and impacts; no licensed music or external assets.
env=np.minimum(t/1.3,1)*np.minimum((end-t)/1.5,1); bed=(.042*np.sin(2*np.pi*55*t)+.023*np.sin(2*np.pi*83*t)+.015*np.sin(2*np.pi*110*t))*env
for hit in (0,4.8,10.7,15.8):
    q=np.maximum(t-hit,0); bed+=.14*np.sin(2*np.pi*(52*q-8*q*q))*np.exp(-q*4)*(t>=hit)
sf.write(d/'tension.wav',bed,sr,subtype='PCM_16')
def ts(x):
    m=round(x*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'
(r/'captions.srt').write_text('\n'.join(f'{i+1}\n{ts(c["start"])} --> {ts(c["start"]+c["duration"])}\n{c["text"]}\n' for i,c in enumerate(clips)))
(r/'storyboard.json').write_text(json.dumps({'duration':end,'segments':clips},indent=2)+'\n')
audio=''.join(f'<audio id="v{i}" class="clip" data-start="{c["start"]}" data-duration="{c["duration"]:.3f}" data-track-index="12" src="assets/cinema-voice-{i+1}.wav"></audio>' for i,c in enumerate(clips))
caps=''.join(f'<div id="c{i}" class="clip caption" data-start="{c["start"]}" data-duration="{c["duration"]:.3f}" data-track-index="10">{html.escape(c["text"])}</div>' for i,c in enumerate(clips))
page=f'''<!doctype html><html><head><meta charset="utf-8"><script src="assets/gsap.min.js"></script><style>
*{{box-sizing:border-box}}html,body{{margin:0;width:1920px;height:1080px;overflow:hidden;background:#020814;color:white;font-family:Arial,sans-serif}}#root{{width:1920px;height:1080px;position:relative;overflow:hidden;background:#020814}} .art{{position:absolute;inset:-55px;background:url('assets/cyber-keyart.png') center/cover;filter:brightness(.65) saturate(1.15)}}.wash{{position:absolute;inset:0;background:linear-gradient(90deg,#02060cc9 0%,#0209126b 42%,#0208147d 100%),linear-gradient(0deg,#01050cf0 0%,transparent 40%)}}.top{{position:absolute;top:70px;left:110px;font-size:28px;letter-spacing:5px;color:#a9d8e7;font-weight:bold}} .label{{position:absolute;top:70px;right:110px;border:2px solid #fd6b6b;padding:12px 18px;color:#ff9b9b;font-size:28px;letter-spacing:3px}} .beat{{position:absolute;top:260px;left:1040px;width:790px}} .kicker{{font-size:28px;letter-spacing:5px;font-weight:700;color:#79edee}} h1{{font-size:94px;line-height:.98;letter-spacing:-3px;margin:22px 0 30px}} .red{{color:#ff6674}} .cyan{{color:#6cf7ef}} .sub{{font-size:33px;color:#dcecf3;line-height:1.25}} .small{{font-size:28px;color:#acc8d6;letter-spacing:2px;margin-top:28px}} .number{{font-size:190px;color:#ff6c76;font-weight:900;letter-spacing:-12px;line-height:.9}} .divider{{display:inline-block;width:74px;height:5px;background:#69f5ee;vertical-align:middle;margin:0 14px}} .caption{{position:absolute;bottom:82px;left:235px;width:1450px;text-align:center;font-size:36px;font-weight:700;line-height:1.25;padding:18px 25px;background:#03070ddf;border-radius:9px}} .frame{{position:absolute;inset:32px;border:1px solid #8ceffb33;pointer-events:none}} .scanline{{position:absolute;left:-300px;top:180px;width:260px;height:620px;transform:skewX(-18deg);background:linear-gradient(90deg,transparent,#94fff530,transparent);pointer-events:none}}
</style></head><body><div id="root" data-composition-id="cinema" data-start="0" data-duration="{end}" data-width="1920" data-height="1080"><div class="art" id="art"></div><div class="wash"></div><div class="top">AGENTIC PENTEST / FIELD DEMO</div><div class="label">DRAMATIZED LAB</div><div class="frame"></div><div class="scanline" id="scanline"></div>
<div class="clip beat" id="beat0" data-start="0" data-duration="5" data-track-index="0"><div class="kicker">A QUESTION, NOT A LIVE ATTACK</div><h1>WHAT HIDES<br><span class="red">IN THE NOISE?</span></h1><div class="sub">An isolated lab. A flood of signals.<br>One problem worth investigating.</div></div>
<div class="clip beat" id="beat1" data-start="5" data-duration="5.9" data-track-index="1"><div class="kicker">NIKTO + ZAP / RECORDED LAB</div><div class="number">6 <span class="divider"></span> 1</div><h1>ALERTS <span class="cyan">BECOME</span><br>ONE FINDING</h1><div class="sub">Cross-origin policy: wildcard access</div></div>
<div class="clip beat" id="beat2" data-start="10.9" data-duration="{end-10.9}" data-track-index="2"><div class="kicker">THE MODEL HAS NO TOOLS</div><h1>AI FINDS SIGNAL.<br><span class="cyan">POLICY HOLDS</span><br>THE LINE.</h1><div class="sub">Fixed actions. Evidence. Human review.</div><div class="small">JUICE SHOP · REVIEWABLE CORS FINDING</div></div>
{caps}{audio}<audio id="bed" class="clip" data-start="0" data-duration="{end}" data-track-index="13" src="assets/tension.wav"></audio></div><script>window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});tl.fromTo('#art',{{scale:1.03,x:0}},{{scale:1.17,x:50,duration:{end},ease:'none'}},0);tl.fromTo('#scanline',{{x:0,opacity:0}},{{x:2450,opacity:.8,duration:2.4,ease:'power2.inOut'}},4.5);tl.fromTo('#scanline',{{x:0,opacity:0}},{{x:2450,opacity:.7,duration:2.0,ease:'power2.inOut'}},10.4);tl.fromTo('#beat0',{{y:18,opacity:.4}},{{y:0,opacity:1,duration:.6}},0);tl.fromTo('#beat1',{{x:100,opacity:0}},{{x:0,opacity:1,duration:.55,ease:'power4.out'}},5);tl.fromTo('#beat2',{{x:100,opacity:0}},{{x:0,opacity:1,duration:.55,ease:'power4.out'}},10.9);window.__timelines.cinema=tl;</script></body></html>'''
(r/'index.html').write_text(page);print(json.dumps({'duration':end,'clips':clips},indent=2))
