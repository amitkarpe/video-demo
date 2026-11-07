#!/usr/bin/env python3
"""Build the editable HyperFrames composition and timed narration locally."""
import argparse, html, json, math
from pathlib import Path
import soundfile as sf
from kokoro_onnx import Kokoro

p=argparse.ArgumentParser(); p.add_argument('--model',required=True); p.add_argument('--voices',required=True); args=p.parse_args()
root=Path(__file__).resolve().parent; assets=root/'assets'; assets.mkdir(exist_ok=True)
segments=[
('THE SIGNAL IN THE NOISE','Six scanner alerts. One finding.','In a Juice Shop lab, six scanner alerts reveal one potential issue.'),
('NORMALIZE THE EVIDENCE','NIKTO + ZAP  →  ONE GROUP','Nikto and ZAP results are grouped, bringing the evidence together for review.'),
('FOLLOW THE HEADER','Access-Control-Allow-Origin: *','The common evidence is a wildcard cross origin header, returned on multiple paths.'),
('AI TRIAGE · POLICY GATE','MODEL PROPOSES  →  RULES CHECK','AI assists the triage. Fixed policy gates constrain actions, and a human reviews the finding.'),
('ONE REVIEWABLE FINDING','CORS MISCONFIGURATION  ·  CVSS 4.3','The recorded report scores the proposed finding at four point three. This is not proof of exploitation.'),
('REDUCE THE EXPOSURE','RESTRICT ORIGINS  →  VERIFY','The recommended fix: allow only trusted origins, then test that untrusted origins receive no approval.')]
k=Kokoro(args.model,args.voices); clips=[]; t=0.5
for i,(heading,sub,words) in enumerate(segments):
    wav,sr=k.create(words,voice='am_michael',speed=1.0,lang='en-us'); path=assets/f'voice-{i+1}.wav'; sf.write(path,wav,sr,subtype='PCM_16'); duration=len(wav)/sr
    clips.append(dict(start=t,duration=duration,heading=heading,sub=sub,words=words)); t+=duration+0.55
end=math.ceil(t+0.2)
def fmt(x):
    ms=round(x*1000); h=ms//3600000; m=ms//60000%60; s=ms//1000%60; return f'{h:02}:{m:02}:{s:02},{ms%1000:03}'
(root/'captions.srt').write_text('\n'.join(f'{i+1}\n{fmt(c["start"])} --> {fmt(c["start"]+c["duration"])}\n{c["words"]}\n' for i,c in enumerate(clips)))
(root/'storyboard.json').write_text(json.dumps({'source':'Recorded Juice Shop lab, report group grp-d382cb1578','scenes':clips,'duration':end},indent=2)+'\n')
scene_markup=[]; audio=[]; anim=[]
for i,c in enumerate(clips):
    start=0 if i==0 else c['start']-0.25; stop=clips[i+1]['start']-0.25 if i+1<len(clips) else end; dur=stop-start
    title=html.escape(c['heading']); sub=html.escape(c['sub']); words=html.escape(c['words'])
    scene_markup.append(f'''<section id="scene{i}" class="clip scene" data-start="{start:.3f}" data-duration="{dur:.3f}" data-track-index="{i}"><div class="inner"><div class="eyebrow">FIELD NOTES <span> / </span> {i+1:02} — 06</div><div class="content"><h1>{title}</h1><p class="subtitle">{sub}</p><div class="rule"></div><div class="diagram"><span class="node">SCANNERS</span><span class="wire"></span><span class="node focus">EVIDENCE</span><span class="wire"></span><span class="node">AI + POLICY</span><span class="wire"></span><span class="node">HUMAN REVIEW</span></div><div class="hint">RECORDED LAB · NO LIVE SCAN · NO EXPLOIT CLAIM</div></div></div></section><div id="cap{i}" class="clip caption" data-start="{c['start']:.3f}" data-duration="{c['duration']:.3f}" data-track-index="10">{words}</div>''')
    audio.append(f'<audio id="voice{i}" class="clip" data-start="{c["start"]:.3f}" data-duration="{c["duration"]:.3f}" data-track-index="20" src="assets/voice-{i+1}.wav"></audio>')
    if i: anim.append(f'tl.fromTo("#scene{i} .inner",{{opacity:0,y:34}},{{opacity:1,y:0,duration:.7,ease:"power3.out"}},{start:.3f});')
    anim.append(f'tl.to("#scene{i} .content",{{x:28,duration:{max(1,dur-0.5):.3f},ease:"none"}},{start+0.2:.3f});')
    if i==2: anim.append(f'tl.to("#scene{i} .diagram",{{scale:1.13,x:-55,duration:2.2,ease:"power2.inOut"}},{start+1:.3f});')
    anim.append(f'tl.fromTo("#scene{i} .wire",{{scaleX:0}},{{scaleX:1,duration:1.1,stagger:.18,ease:"power2.out"}},{start+.35:.3f});')
page=f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920,height=1080"><script src="assets/gsap.min.js"></script><style>
*{{box-sizing:border-box}} html,body{{margin:0;width:1920px;height:1080px;overflow:hidden;background:#07111f;color:#f4f7fc;font-family:Arial,sans-serif}} #root{{width:1920px;height:1080px;position:relative;background:radial-gradient(ellipse at 78% 15%,#142b3d,#07111f 65%)}} #root:before{{content:"";position:absolute;inset:0;background-image:linear-gradient(#ffffff08 1px,transparent 1px),linear-gradient(90deg,#ffffff08 1px,transparent 1px);background-size:80px 80px}} .scene{{position:absolute;inset:0}} .inner{{padding:112px 145px}} .eyebrow{{font-size:28px;font-weight:bold;letter-spacing:5px;color:#74e5d0}} .eyebrow span{{color:#5b7082}} .content{{margin-top:108px}} h1{{font-size:76px;letter-spacing:-2px;max-width:1450px;margin:0;line-height:1.08}} .subtitle{{font-size:36px;color:#b7c7d6;margin:30px 0 0;letter-spacing:1px}} .rule{{width:180px;height:5px;background:#6ee4c9;margin:55px 0 75px}} .diagram{{display:flex;align-items:center;transform-origin:left center}} .node{{border:2px solid #435e70;background:#102434;border-radius:12px;padding:24px 23px;font-size:28px;font-weight:bold;letter-spacing:1px;white-space:nowrap}} .node.focus{{border-color:#6ee4c9;color:#82f0d3;background:#103532}} .wire{{height:3px;width:78px;background:#6ee4c9;transform-origin:left center}} .hint{{font-size:28px;letter-spacing:2px;color:#7e95a7;margin-top:62px}} .caption{{position:absolute;bottom:90px;left:230px;width:1460px;text-align:center;padding:20px 30px;border-radius:12px;background:#030a12ed;color:white;font-size:33px;line-height:1.3;font-weight:600}} </style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="{end}" data-width="1920" data-height="1080">{''.join(scene_markup)}{''.join(audio)}</div><script>window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});{''.join(anim)}window.__timelines.main=tl;</script></body></html>'''
(root/'index.html').write_text(page); print(f'duration={end}s; speech={sum(c["duration"] for c in clips):.1f}s')
