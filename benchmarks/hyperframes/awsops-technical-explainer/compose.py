#!/usr/bin/env python3
"""Source-faithful spatial journey; cached speech and timing are immutable inputs."""
from pathlib import Path
import json,html,argparse
from visuals import *
from mechanisms import lost_response, evidence_wheel, imported, frozen, decision, execution, cleanup, provenance
r=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--proof',action='store_true');a=p.parse_args()
S=json.loads((r/'storyboard.json').read_text());Q=json.loads((r/'cues.json').read_text())
def at(s):
 x=[q['start'] for q in Q if s.lower() in q['words'].lower()]
 if len(x)!=1:raise ValueError((s,len(x)))
 return x[0]
js=[];init=[]
def set_(sel,props,t):js.append(f'tl.set({json.dumps(sel)},{json.dumps(props)},{t:.3f});')
def to(sel,props,t):js.append(f'tl.to({json.dumps(sel)},{json.dumps(props)},{t:.3f});')
def hide(sel):init.append(f'gsap.set({json.dumps(sel)},{{autoAlpha:0}});')
def reveal(sel,t,d=.8):hide(sel);to(sel,{'autoAlpha':1,'duration':d},t)
def camera(x,y,scale,t,d=1.7):to('#camera',{'x':960-x*scale,'y':360-y*scale,'scale':scale,'duration':d,'ease':'power2.inOut'},t)
# All lenses share the same spatial world, with front-facing readable SVG.
anchors=[(4500,1880),(1120,480),(1840,1120),(2600,1120),(4040,1120),(4500,1250),(4000,1930),(2800,1930)]
world=master()
(r/'architecture.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="5600" height="2400" viewBox="0 0 5600 2400" style="background:#06131f;font-family:Arial">'+defs()+world.replace('href="assets/','href="assets/')+'</svg>')
digest=json.loads((r/'synthetic-batch.json').read_text())['record']['scopeDigest']
lenses={0:evidence_wheel('o'),1:imported(),2:frozen(digest),3:decision(),4:execution(),5:g('u-mechanism',lost_response())+g('u-cleanup',cleanup()),6:g('v-wheel',evidence_wheel('v'))+g('v-version',code('v-source-code',250,180,1200,'SOURCE / HOSTED PROVENANCE','sourceRevision: 15c12fb5362d…\nhostedVersion: null\nVersion suffix ≠ deployed release',240)),7:provenance()}
body='<svg width="1" height="1" style="position:absolute">'+defs()+'</svg><svg id="worldmap" width="5600" height="2400" viewBox="0 0 5600 2400">'+world+'</svg>'
for i,svg in lenses.items():
 x,y=anchors[i]
 body+=f'<div class="lens" id="lens{i}" style="left:{x-840}px;top:{y-330}px"><svg width="1680" height="660" viewBox="0 0 1680 660">{rect(0,0,1680,660,"line","ink",28)}{svg}</svg></div>'
hide('.lens');hide('#mapNote')
init.append("gsap.set('#lens1,#lens2',{rotationY:-3,z:-24,transformOrigin:'50% 50%'});")
# Source map is exposed during travel and context beats; it is never a grey text backdrop.
def overview(t,d=1.7,note='DOTTED = UNPROVEN · LIVE APPROVAL BLOCKED · NO ACCEPTED CANARY WRITE'):
 to('.lens',{'autoAlpha':0,'duration':.5},t)
 to('#worldmap',{'autoAlpha':1,'duration':.5},t)
 to('#camera',{'x':148,'y':0,'scale':.285,'duration':d,'ease':'power2.inOut'},t)
 set_('#mapNote',{'textContent':note},t);to('#mapNote',{'autoAlpha':1,'duration':.5},t)
 to('.provenance',{'autoAlpha':0,'duration':.4},t)
def focus(i,t,d=1.7):
 x,y=anchors[i]
 if i in (1,2):to(f'#lens{i}',{'rotationY':0,'z':0,'duration':1.2,'ease':'power2.out'},t+d-.7)
 to('.lens',{'autoAlpha':0,'duration':.35},t)
 to('#worldmap',{'autoAlpha':1,'duration':.3},t)
 camera(x,y,1,t,d)
 to(f'#lens{i}',{'autoAlpha':1,'duration':.6},t+d-.5)
 to('#worldmap',{'autoAlpha':0,'duration':.4},t+d-.25)
 to('#mapNote',{'autoAlpha':0,'duration':.35},t)
 to('.provenance',{'autoAlpha':1,'duration':.5},t+d-.5)
for i in lenses:
 st=S['scenes'][i]['start']
 if i:focus(i,max(0,st-1.7))
 title=[
 'When SUCCEEDED + MATCH still does not mean fixed',
 'Import the finding. Keep authority outside it.',
 'Freeze the exact bytes. Authenticate the person separately.',
 'One durable decision, before any SDK mutation',
 'A fixed canary lifecycle — never an arbitrary AWS agent',
 'UNKNOWN: preserve uncertainty, never invent success',
 'Four independent sources. One defensible outcome.',
 'What is implemented, simulated, historical or still pending?'][i]
 set_('#chapterTitle',{'textContent':f'{i+1:02} / '+title},max(0,st-.4))
 # A brief map return makes continuity explicit between focused mechanisms.
 if i and i<7:overview(st-3.1,1.1)
# Cold open: positive operation/readback facts coexist with missing Config evidence.
for j,frag in enumerate(['An AWS compliance finding','It does not tell us who','AWSOps, the backend']):
 sel=['#o-execution','#o-readback','#o-config,#o-fresh'][j]
 reveal(sel,[.6,1.8,3.2][j],.9)
reveal('#o-review',at('It does not tell us who'),1)
reveal('#o-equation',7.4,.7)
reveal('#o-gate',7.4,.7)
overview(at('The interesting part'),1.8)
focus(0,at('A finding is not authority'),1.5)
# Import: fields cross shape admission, but the assertion badge never changes trust class.
for sel in ['#i-envelope','#i-extra','#i-private','#i-separation']:hide(sel)
for j in range(3):
 reveal(f'#i-field{j}',at('An envelope has')+j*.7,.6)
 to(f'#i-field{j}',{'x':260,'duration':1.4,'ease':'power2.inOut'},at('An envelope has')+j*.7)
 to(f'#i-field{j}',{'autoAlpha':0,'duration':.4},at('An envelope has')+j*.7+1.5)
reveal('#i-envelope',at('An envelope has')+2.1,.8)
reveal('#i-extra',at('Unknown fields'),.6)
to('#i-extra',{'x':-55,'duration':.55,'yoyo':True,'repeat':1},at('Unknown fields')+.5)
reveal('#i-assertion',at('Even a structurally valid'),.8)
reveal('#i-private',at('A private backend'),.8)
for sel in ['#i-extra','#i-raw','#i-envelope','#i-assertion','#i-boundary']:to(sel,{'autoAlpha':0,'duration':.4},at('A private backend'))
to('#i-private',{'autoAlpha':0,'duration':.5},at('The companion'))
for sel in ['#i-raw','#i-envelope','#i-assertion','#i-boundary']:to(sel,{'autoAlpha':1,'duration':.6},at('The companion'))
reveal('#i-separation',at('The offline planner'),.8)
# Batch: assemble complete field families, break the seal on exact revision drift.
for sel in ['#b-break','#b-auth','#b-expiry']:hide(sel)
for j in range(8):
 init.append(f'gsap.set("#b-field{j}",{{x:{-80 if j<4 else 80},y:-12}});')
 reveal(f'#b-field{j}',at('The batch binds')+j*.5,.7)
 to(f'#b-field{j}',{'x':0,'y':0,'duration':.8},at('The batch binds')+j*.5)
reveal('#b-seal',at('The scope digest'),.8)
to('#b-seal',{'rotation':7,'svgOrigin':'1430 268','duration':.5,'yoyo':True,'repeat':1},at('The scope digest'))
set_('#b-revision',{'textContent':'2  ← illustrative change','fill':C['red']},at('Change the target'))
reveal('#b-break',at('Change the target')+.3,.6)
to('#b-seal',{'autoAlpha':0,'duration':.4},at('Change the target')+.3)
reveal('#b-expiry',at('Expired preparation'),.7)
to('#b-break',{'autoAlpha':0,'duration':.4},at('Expired preparation'))
to('#b-expiry',{'autoAlpha':0,'duration':.4},at('These limits do not turn'))
reveal('#b-auth',at('These limits do not turn'),.8)
# Atomic decision race is a labelled counterfactual, not an actual owner action.
for sel in ['#d-winning','#d-consumed','#d-branch','#d-atomic']:hide(sel)
reveal('#d-principal',at('The decision must come'),.8)
to('#d-reject',{'x':190,'y':-150,'duration':1.3,'ease':'power2.inOut'},at('In this illustrative race'))
reveal('#d-winning',at('In this illustrative race')+1.1,.6)
reveal('#d-atomic',at('It commits the winning'),.7)
to('#d-reject',{'autoAlpha':0,'duration':.3},at('In this illustrative race')+1.4)
to('#d-db',{'y':-8,'duration':.4,'yoyo':True,'repeat':1},at('It commits the winning'))
reveal('#d-consumed',at('A competing choice'),.7)
to('#d-approve',{'x':80,'duration':.8,'yoyo':True,'repeat':1},at('A competing choice'))
reveal('#d-branch',at('The application also claims'),.7)
to('#d-live',{'y':-8,'duration':.5,'yoyo':True,'repeat':1},at('Now the important current boundary'))
# Fixed provider: identity, operation order, TLS semantics, preconditions, durable boundary.
for sel in ['#x-calls','#x-policy','#x-preconditions','#x-journal']+[f'#x-check{j}' for j in range(5)]:hide(sel)
to('#x-identity',{'autoAlpha':0,'duration':.5},at('The fixed setup sequence'))
reveal('#x-calls',at('The fixed setup sequence'),.6)
for j in range(4):
 set_(f'#x-state{j} text',{'textContent':'CALLING','fill':C['amber']},at('The fixed setup sequence')+j*1.3+.4)
 set_(f'#x-state{j} text',{'textContent':'ACK','fill':C['green']},at('The fixed setup sequence')+j*1.3+1.1)
to('#x-calls',{'autoAlpha':0,'duration':.5},at('Public access blocking'))
reveal('#x-policy',at('Public access blocking'),.7)
to('#x-policy',{'autoAlpha':0,'duration':.5},at('Before the policy write'))
reveal('#x-preconditions',at('Before the policy write'),.6)
for j in range(5):reveal(f'#x-check{j}',at('Before the policy write')+.7+j*.7,.5)
for sel in ['#x-preconditions']+[f'#x-check{j}' for j in range(5)]:to(sel,{'autoAlpha':0,'duration':.4},at('Each mutation has'))
reveal('#x-journal',at('Each mutation has'),.6)
to('#x-s3',{'autoAlpha':0,'duration':.4},at('Each mutation has'))
# Lost acknowledgement: the representative proof's tested mechanism.
for selector in ['#u-reply','#u-fracture','#u-state','#u-retry','#u-reconcile','#u-code','#u-cleanup','#u-recovery','#u-counts']:hide(selector)
to('#u-request',{'x':840,'duration':3.1,'ease':'power1.inOut'},at('Suppose the policy request')+.7)
reveal('#u-reply',at('Suppose the policy request')+3.9,.6)
to('#u-request',{'autoAlpha':0,'duration':.4},at('Suppose the policy request')+4)
reveal('#u-fracture',at('That is not proof'),.5)
to('#u-reply',{'y':25,'autoAlpha':0,'duration':.7},at('That is not proof')+.3)
reveal('#u-state',at('The operation stays calling'),.7)
camera(anchors[5][0]+15,anchors[5][1],1.04,at('The operation stays calling'),1.3)
reveal('#u-retry',at('Automatically replaying'),.6)
reveal('#u-reconcile',at('The provider disables'),1)
to('#u-retry',{'autoAlpha':0,'duration':.5},at('The provider disables'))
camera(*anchors[5],1,at('The provider disables'),1.4)
reveal('#u-recovery',at('If every setup row'),.7)
to('#u-recovery',{'autoAlpha':0,'duration':.4},at('A calling row remains uncertain'))
reveal('#u-code',at('A calling row remains uncertain'),.6)
to('#u-code',{'autoAlpha':0,'duration':.4},at('The exported write count'))
reveal('#u-counts',at('The exported write count'),.7)
to('#u-reconcile',{'autoAlpha':0,'duration':.5},at('If every setup row'))
for sel in ['#u-mechanism']:to(sel,{'autoAlpha':0,'duration':.4},at('Cleanup is not'))
reveal('#u-cleanup',at('Cleanup is not'),.7)
# The four evidence sources reveal independently and never unlock VERIFIED.
for sel in ['#v-review','#v-gate','#v-version']:hide(sel)
reveal('#v-execution',at('Even when the SDK sequence'),.7)
reveal('#v-readback',at('The adapter reads provider'),.8)
reveal('#v-config',at('It does not trigger'),.8)
reveal('#v-fresh',at('It does not trigger')+.8,.8)
reveal('#v-review',at('Even when the SDK sequence'),.8)
to('#v-review',{'scale':1.035,'svgOrigin':'850 330','duration':.5,'yoyo':True,'repeat':1},at('The run remains needs review'))
reveal('#v-gate',at('The shared contract requires'),.7)
for sel in ['#v-wheel']:to(sel,{'autoAlpha':0,'duration':.4},at('The evidence also separates'))
reveal('#v-version',at('The evidence also separates'),.8)
# Closing is provenance-specific, then returns to the architecture with gates intact.
for sel in ['#p-fake','#p-history','#p-pending']:hide(sel)
reveal('#p-source',at('The repository contains concrete'),.8)
reveal('#p-fake',at('The source tests assert'),.8)
reveal('#p-history',at('There is also accepted historical'),.8)
reveal('#p-pending',at('The later transfer record'),.8)
overview(at('The proposition is controlled'),2.2,'CONTROLLED CHANGE · INSPECTABLE EVIDENCE · EXPLICIT UNKNOWNS')
# Keep the original source/voice contract and the exact 649-second natural pacing.
css='''*{box-sizing:border-box}html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#06131f;color:#f2f7fc;font-family:Arial,sans-serif}#root{position:relative;width:1920px;height:1080px;overflow:hidden;background:radial-gradient(ellipse at 72% 30%,#163a50,#06131f 70%)}.masthead{position:absolute;left:72px;top:24px;font-size:28px;letter-spacing:2px;color:#b6cbd9}.synthetic{position:absolute;right:72px;top:24px;font-size:28px;letter-spacing:1px;color:#ffc66c;font-weight:750}#chapterTitle{position:absolute;left:72px;top:73px;font-size:42px;font-weight:750}#identity{position:absolute;left:75px;top:127px;font-size:28px;color:#62e0cf}.stage{position:absolute;left:0;top:184px;width:1920px;height:688px;overflow:hidden;perspective:1800px}#camera{position:absolute;width:5600px;height:2400px;transform-origin:0 0;transform-style:preserve-3d}#worldmap{position:absolute;left:0;top:0;font-family:Arial;filter:drop-shadow(0 25px 20px #0009)}.lens{position:absolute;width:1680px;height:660px;visibility:hidden;filter:drop-shadow(0 22px 25px #000a);transform-style:preserve-3d}.lens svg{font-family:Arial;overflow:visible}.caption{position:absolute;left:115px;top:918px;width:1690px;padding:12px 24px;border-radius:12px;text-align:center;font-size:32px;line-height:1.2;font-weight:600;background:#020b13f2}.provenance{position:absolute;left:75px;top:879px;font-size:28px;color:#b6cbd9}.track{position:absolute;left:75px;bottom:17px;width:1770px;height:4px;background:#28495d}#progress{height:100%;background:#62e0cf;transform-origin:left}.scene-marker{display:none}'''
cap=''.join(f'<div id="caption-{i}" class="caption clip" data-start="{c["start"]}" data-duration="{c["duration"]}" data-track-index="5">{html.escape(c["words"])}</div>' for i,c in enumerate(Q))
audio=''.join(f'<audio id="voice-{i}" class="clip" data-start="{c["start"]}" data-duration="{c["duration"]}" data-track-index="10" src="{c["path"]}"></audio>' for i,c in enumerate(Q))
to('#progress',{'scaleX':1,'duration':649,'ease':'none'},0)
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><script src="assets/gsap.min.js"></script><style>{css}</style></head><body><div id="root" data-composition-id="awsops" data-start="0" data-duration="649" data-width="1920" data-height="1080"><div class="masthead">INSIDE AWSOPS · WHAT THE EVIDENCE PROVES</div><div class="synthetic">SYNTHETIC WALKTHROUGH</div><div id="chapterTitle">AWSOps: architecture and trust boundaries</div><div id="identity">CANARY A / BATCH A / RUN A · controlled synthetic aliases</div><div class="stage"><div id="camera">{body}</div></div><div id="mapNote" style="position:absolute;left:75px;top:879px;font-size:29px;color:#ffc66c;visibility:hidden"></div><div class="provenance">SOURCE 15c12fb5362d… · MOCK ≠ LIVE ACCEPTANCE · AI voice: Kokoro / Michael</div>{cap}{audio}<div class="track"><div id="progress"></div></div></div><script>window.__timelines=window.__timelines||{{}};gsap.set('#progress',{{scaleX:0}});{''.join(init)}gsap.set('#camera',{{x:{960-anchors[0][0]},y:{360-anchors[0][1]},scale:1}});gsap.set('#worldmap',{{autoAlpha:0}});gsap.set('#lens0',{{autoAlpha:1}});const tl=gsap.timeline({{paused:true}});{''.join(js)}window.__timelines.awsops=tl;</script></body></html>'''
(r/('proof.html' if a.proof else 'index.html')).write_text(page)
print("Composed eight-chapter spatial revision; narration untouched")
