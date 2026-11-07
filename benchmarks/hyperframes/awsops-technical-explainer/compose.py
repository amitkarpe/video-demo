#!/usr/bin/env python3
"""Editable, seekable SVG mechanisms; all motion is timed to measured local speech."""
from pathlib import Path
import json, html
r=Path(__file__).resolve().parent
story=json.loads((r/'storyboard.json').read_text());cues=json.loads((r/'cues.json').read_text())
batch=json.loads((r/'synthetic-batch.json').read_text())['record']
C={'input':'#f6bd66','backend':'#72bfff','human':'#c2a4fa','provider':'#69d9d4','observed':'#a4df99','red':'#ff9f9f','muted':'#b3c7d7','white':'#edf6ff'}
def text(x,y,s,size=30,fill='#edf6ff',weight=400,anchor='start',id=''):
 lines=s.split('\n');attrs=f' id="{id}"' if id else ''
 return f'<text{attrs} x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">'+''.join(f'<tspan x="{x}" dy="{0 if i==0 else size*1.35}">{html.escape(v)}</tspan>' for i,v in enumerate(lines))+'</text>'
def box(x,y,w,h,color='#72bfff',fill='#102638',id='',radius=16):
 return f'<rect id="{id}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{color}" stroke-width="2"/>'
def line(x,y,xx,yy,color='#72bfff',id='',dash=False):
 return f'<path id="{id}" d="M{x},{y} L{xx},{yy}" stroke="{color}" stroke-width="3" fill="none" marker-end="url(#arrow)"'+(' stroke-dasharray="12 9"' if dash else '')+'/>'
def node(id,x,y,w,h,title,body='',color='backend'):
 c=C.get(color,color)
 return f'<g id="{id}">'+box(x,y,w,h,c)+text(x+24,y+44,title,30,c,700)+text(x+24,y+92,body,29)+'</g>'
def group(id,s):return f'<g id="{id}">{s}</g>'
def badge(x,y,w,label,color='backend',id=''):
 return group(id,box(x,y,w,50,C.get(color,color),'#0c1d2d',radius=10)+text(x+w/2,y+34,label,28,C.get(color,color),700,'middle'))
def bucket(x,y):
 return f'<g transform="translate({x},{y})"><path d="M0,22 L15,142 Q80,178 145,142 L160,22" stroke="#69d9d4" stroke-width="4" fill="#14394b"/><ellipse cx="80" cy="22" rx="80" ry="22" stroke="#69d9d4" stroke-width="4" fill="#235167"/>'+text(80,93,'S3',42,C['provider'],700,'middle')+'</g>'
def heading(x,y,label,color='muted'):return text(x,y,label,28,C.get(color,color),700)
# 1. Unfold the evidence lanes, withholding the badge.
p0=bucket(90,130)+badge(40,345,300,'FIXED?',id='fixed')+line(270,235,535,235)
for j,(label,val) in enumerate([('execution','UNKNOWN'),('providerReadback','NOT_ACQUIRED'),('compliance','UNKNOWN'),('freshness','NOT_VERIFIED')]):
 y=16+j*110
 p0+=group(f'openlane{j}',box(570,y,1115,91,C['input'])+text(600,y+57,label,33)+text(1645,y+57,val,34,C['input'],700,'end'))
p0+=text(580,488,'One badge cannot replace four independent answers.',31,C['muted'])
# 2. Inert import and the private authority boundary.
p1=node('raw',15,30,470,225,'SYNTHETIC INPUT','schemaVersion\nfindings[0]\nresourceAlias',color='input')
p1+=line(490,135,715,135,C['input'])
p1+=node('intake',725,30,425,225,'BOUNDED INTAKE','262,144 bytes · 500 rows\nExact fields · unique IDs\nNo imported authority',color='backend')
p1+=line(1155,135,1245,135)
p1+=node('finding',1260,30,455,225,'Finding ENVELOPE','schemaVersion · kind\nrecord · revision: 1\nIMPORTED_ASSERTION',color='input')
p1+=badge(410,264,410,'extraField → REJECT','red','extra')
p1+=node('private',935,320,780,153,'PRIVATE BACKEND BINDING','Alias ≠ credential · registration ≠ IAM trust',color='backend')
p1+=node('companion',15,320,860,153,'COMPANION UI / OFFLINE PLAN','Same public alias · separate preparation path',color='input')
p1+=f'<circle id="importpacket" cx="510" cy="135" r="11" fill="{C["input"]}"/>'
# 3. An actual-shaped complete batch with field-level digest drift.
p2=heading(15,28,'BATCH A · ACTUAL CONTRACT FIELDS / SYNTHETIC VALUES')
fields=[('batchId','batch-canary-aaaa…'),('datasetId','dataset-canary'),('registryVersion / mode','1 / MOCK'),('frozenAt / expiresAt','00:00Z / 00:05Z'),('targets[0].revision','1'),('targets[0].evidenceDigest','synthetic observation digest'),('capabilityId','s3-require-tls'),('expectedChange','DENY_INSECURE_TRANSPORT')]
for i,(k,v) in enumerate(fields):
 col=i//4;row=i%4;x=15+col*645;y=58+row*83
 p2+=group(f'field{i}',box(x,y,620,73,'#385973')+text(x+18,y+29,k,28,C['muted'])+text(x+18,y+59,v,28,C['white'],700,id='revisionValue' if i==4 else ''))
p2+=node('seal',1320,60,395,235,'scopeDigest',batch['scopeDigest'][:16]+'…\nSHA-256\nComplete payload',color='observed')
p2+=badge(1320,315,395,'DIGEST MISMATCH','red','drift')
p2+=group('expiry',badge(15,414,370,'EXPIRED → BLOCKED','input')+text(415,447,'Canonical keys · retain array order · omit scopeDigest',29))
p2+=text(18,490,'Legacy FrozenScope ≠ Batch     |     Integrity binding ≠ authenticated principal',28,C['muted'])
# 4. Two requests race toward a single terminal decision.
p3=node('approveRequest',20,25,425,115,'APPROVE_ONCE','',color='human')+node('rejectRequest',20,190,425,115,'REJECT','',color='human')
p3+=line(450,82,700,175,C['human'])+line(450,247,700,175,C['human'])
p3+=node('sqlite',720,55,550,245,'SQLite · BEGIN IMMEDIATE','Check saved scope + principal\nCommit decision + initial Run\nREJECTED · writes: 0',color='backend')
p3+=line(1280,175,1460,175,C['backend'],id='dispatchline',dash=True)
p3+=node('providerGate',1470,85,250,200,'PROVIDER','No dispatch\non Reject',color='provider')
p3+=badge(20,333,560,'COUNTERFACTUAL REJECT BRANCH','human')
p3+=badge(605,333,570,'COMPETING CHOICE → CONSUMED','red','consumed')
p3+=group('failclosed',box(20,407,1700,83,C['input'])+text(45,441,'CURRENT LIVE ROUTE: TRUSTED_HUMAN_APPROVAL_BINDING_REQUIRED',29,C['input'],700)+text(45,476,'Legacy native: APPROVE_BLOCKED · dispatch_allowed=false',29))
# 5. An alternative approved mock branch, never replay of the rejected batch.
p4=heading(15,29,'APPROVE_ONCE ALTERNATIVE · FAKE PROVIDER · NOT A REPLAY OF REJECT','human')
for i,(name,code) in enumerate([('CREATE','create_bucket'),('TASK TAGS','put_bucket_tagging'),('PUBLIC BLOCK','put_public_access_block'),('TLS POLICY','put_bucket_policy')]):
 x=15+i*435
 p4+=node(f'step{i}',x,60,395,132,name,code,color='provider')
 if i<3:p4+=line(x+398,125,x+430,125,C['provider'])
p4+=group('policy',box(15,230,825,258,C['provider'])+text(40,272,'FIXED POLICY CONDITION',30,C['provider'],700)+text(40,324,'Effect: Deny\nBool: {aws:SecureTransport: false}\nExisting policy → do not overwrite',30))
p4+=group('ledger',box(880,230,840,258,C['backend'])+text(905,273,'DURABLE OPERATION LEDGER',30,C['backend'],700))
for i,(step,state) in enumerate([('create','ACK'),('tags','ACK'),('public_block','ACK'),('policy','INTENT')]):
 p4+=text(915,321+i*46,step,29)+text(1655,321+i*46,state,29,C['observed'] if i<3 else C['input'],700,'end',f'op{i}')
p4+=badge(920,421,370,'SDK ATTEMPTS: 4','provider','attempt4')
# 6. Lost acknowledgement, no write replay; independent reconciliation.
p5=node('caller',15,35,365,125,'SAME RUN A','policy operation',color='backend')
p5+=line(390,95,610,95,C['provider'],id='outbound')
p5+=node('calling',625,35,450,125,'CALLING','execution = UNKNOWN',color='input')
p5+=line(1080,95,1335,95,C['provider'])+node('cloud',1350,35,370,125,'FAKE PROVIDER','Change may exist',color='provider')
p5+=group('lost',line(1340,199,1080,199,C['input'],dash=True)+text(1195,245,'RESPONSE LOST',29,C['input'],700,'middle')+text(1200,212,'×',62,C['red'],700,'middle'))
p5+=group('retryblocked',line(390,285,1350,285,C['red'],dash=True)+text(865,278,'NO AUTOMATIC WRITE RETRY',31,C['red'],700,'middle'))
p5+=group('reconcile',line(1380,355,385,355,C['observed'])+text(885,395,'READ-ONLY RECONCILIATION → SAME RUN A',30,C['observed'],700,'middle'))
p5+=group('counts',badge(15,432,530,'4 SIMULATED ATTEMPTS · 0 REAL','provider')+badge(570,432,440,'CONFIRMED CHANGES: ?','input')+badge(1035,432,680,'REFUSED BEFORE CALL: +0 ATTEMPTS','backend'))
p5+=group('cleanup',box(15,255,1705,232,C['input'])+text(45,300,'CONDITIONAL CLEANUP ≠ AUTOMATIC ROLLBACK',31,C['input'],700)+text(45,349,'Exact authority + fresh owner / Region + empty state + expiry',31)+text(45,399,'CALLING / uncertain creation → destructive cleanup blocked',31,C['red'])+text(45,450,'TTL tag does not schedule deletion.',31))
p5+=f'<circle id="callpacket" cx="405" cy="95" r="11" fill="{C["provider"]}"/>'
# 7. The four independent evidence lanes pay off.
p6=''
for j,(label,val,col) in enumerate([('execution','SUCCEEDED','observed'),('providerReadback','MATCH','observed'),('compliance','UNKNOWN','input'),('freshness','NOT_VERIFIED','input')]):
 y=j*97
 p6+=group(f'lane{j}',box(15,y,1115,82,C[col])+text(40,y+53,label,33)+text(1095,y+53,val,35,C[col],700,'end'))
p6+=node('review',1170,35,550,170,'OVERALL RUN STATUS','NEEDS_REVIEW',color='input')
p6+=node('verified',1170,235,550,130,'VERIFIED?','Gate remains closed',color='red')
p6+=group('versions',box(15,407,1705,84,C['backend'])+text(42,442,'sourceRevision: 15c12fb5362d…     hostedVersion: null',30)+text(42,478,'SYNTHETIC evidence · source version suffix is not deployment proof',28,C['muted']))
# 8. Dated evidence, no unearned deployment badge.
p7=''
board=[('SOURCE IMPLEMENTED','Bounded records · frozen scope · durable states','backend'),('SOURCE TESTS / FAKE SDK','Approval · Reject · drift · expiry · uncertainty','provider'),('HISTORICAL LIVE READ','11 Oct 2026: bounded Config acquisition','observed'),('PENDING LIVE ACCEPTANCE','Ledger provenance · deployed pins · genuine Reject','input')]
for i,(label,detail,col) in enumerate(board):
 y=i*103
 p7+=group(f'proofrow{i}',box(15,y,1705,88,C[col])+text(40,y+54,label,28,C[col],700)+text(630,y+54,detail,30))
p7+=text(22,473,'Controlled change. Inspectable evidence. Explicit unknowns.',36,C['white'],700)
scenes=[p0,p1,p2,p3,p4,p5,p6,p7]
# Every event targets a sentence; no independent stopwatch-driven edit decisions.
def at(fragment):
 m=[c['start'] for c in cues if fragment.lower() in c['words'].lower()]
 if len(m)!=1:raise ValueError(f'Need one timing cue: {fragment} ({len(m)})')
 return m[0]
a=[];initial=[]
def set_(sel,props,t):a.append(f'tl.set({json.dumps(sel)},{json.dumps(props)},{t:.3f});')
def to(sel,props,t):a.append(f'tl.to({json.dumps(sel)},{json.dumps(props)},{t:.3f});')
def frm(sel,props,t):
 start={k:v for k,v in props.items() if k not in ('duration','ease')}
 end={k:(1 if k in ('opacity','scale') else 0 if k in ('x','y') else v) for k,v in start.items()}
 end.update({k:v for k,v in props.items() if k in ('duration','ease')})
 initial.append(f'gsap.set({json.dumps(sel)},{json.dumps(start)});')
 a.append(f'tl.to({json.dumps(sel)},{json.dumps(end)},{t:.3f});')
# Scene initial visibility is set immediately outside the paused timeline.
for i,s in enumerate(story['scenes']):
 st=s['start'];dur=s['duration']
 if i:to(f'#scene{i-1}',{'autoAlpha':0,'duration':.4},max(0,st-.3))
 to(f'#scene{i}',{'autoAlpha':1,'duration':.5},st)
 to(f'#nav{i}',{'color':C['white'],'borderColor':C['provider'],'backgroundColor':'#183b4c','duration':.4},st)
 set_('#chapterTitle',{'textContent':f'{i+1:02} / '+s['title']},st)
 frm(f'#scene{i} svg',{'y':18,'scale':.985,'transformOrigin':'50% 50%','duration':1.2,'ease':'power2.out'},st)
# Opening evidence rows are progressively unfolded.
for j in range(4):frm(f'#openlane{j}',{'opacity':0,'x':-80,'duration':1.1},at('AWSOps, the backend')+j*1.05)
frm('#fixed',{'y':10,'duration':1.5},.6)
to('#fixed',{'opacity':.35,'duration':1.2},at('A successful operation'))
# Import boundary: data moves, authority does not.
to('#importpacket',{'x':650,'duration':3,'ease':'power1.inOut'},at('An envelope has'))
frm('#finding',{'opacity':.2,'x':-25,'duration':1},at('Even a structurally valid'))
frm('#extra',{'opacity':0,'y':-18,'duration':.6},at('Unknown fields'))
to('#extra',{'opacity':.25,'duration':1},at('The bounded synthetic'))
frm('#private',{'opacity':0,'y':20,'duration':1},at('A private backend'))
frm('#companion',{'opacity':0,'duration':1},at('The companion'))
# Scope assembly and illustrative revision drift.
for j in range(8):frm(f'#field{j}',{'opacity':0,'y':12,'duration':.7},at('The batch binds')+j*.55)
frm('#seal',{'opacity':0,'scale':.85,'transformOrigin':'50% 50%','duration':1},at('The scope digest'))
set_('#drift',{'autoAlpha':0},0)
set_('#revisionValue',{'textContent':'2  ← illustrative change','fill':C['red']},at('Change the target'))
to('#seal',{'opacity':.35,'duration':.8},at('Change the target'))
to('#drift',{'autoAlpha':1,'duration':.7},at('Change the target')+.9)
frm('#expiry',{'opacity':0,'duration':1},at('Expired preparation'))
# A transaction commits once; counterfactual branch is labelled.
to('#rejectRequest',{'x':210,'duration':1.4,'ease':'power2.in'},at('In this illustrative race'))
to('#approveRequest',{'x':95,'opacity':.3,'duration':1},at('A competing choice'))
frm('#consumed',{'opacity':0,'duration':1},at('A competing choice'))
frm('#sqlite',{'opacity':.3,'duration':1},at('It commits the winning'))
frm('#failclosed',{'opacity':0,'duration':1},at('Now the important current boundary'))
# Fixed setup steps highlight in order, then policy and journal states reveal.
for j in range(4):frm(f'#step{j}',{'opacity':.15,'y':15,'duration':1},at('The fixed setup sequence')+j*1.5)
frm('#policy',{'opacity':0,'duration':1.2},at('Public access blocking'))
frm('#ledger',{'opacity':0,'duration':1},at('Each mutation has'))
for j in range(4):frm(f'#op{j}',{'opacity':0,'duration':.6},at('Each mutation has')+j*.5)
set_('#attempt4',{'autoAlpha':0},0)
set_('#op3',{'textContent':'CALLING','fill':C['input']},at('Intent becomes calling'))
set_('#op3',{'textContent':'ACK','fill':C['observed']},at('Intent becomes calling')+5.2)
# Counts stay out of ledger until the independent uncertainty explanation.
# Unknown: request crosses a boundary; the acknowledgement never arrives.
set_('#cleanup',{'autoAlpha':0},0)
to('#callpacket',{'x':1080,'duration':3,'ease':'power1.in'},at('Suppose the policy request'))
frm('#lost',{'opacity':0,'duration':.7},at('but its response disappears'))
frm('#retryblocked',{'opacity':0,'duration':1},at('Automatically replaying'))
frm('#reconcile',{'opacity':0,'duration':1},at('The provider disables'))
frm('#counts',{'opacity':0,'duration':1},at('The exported write count'))
for sel in ['#lost','#retryblocked','#reconcile','#counts']:
 to(sel,{'autoAlpha':0,'duration':.5},at('Cleanup is not'))
to('#cleanup',{'autoAlpha':1,'duration':.6},at('Cleanup is not'))
# Evidence lanes retain distinct states; green never propagates to missing evidence.
for j in range(4):frm(f'#lane{j}',{'opacity':.12,'x':-18,'duration':1},at('Our synthetic successful branch')+j*.9)
frm('#review',{'opacity':0,'duration':1},at('The run remains needs review'))
frm('#verified',{'opacity':0,'duration':1},at('The shared contract requires'))
frm('#versions',{'opacity':0,'duration':1},at('The evidence also separates'))
for j,fragment in enumerate(['The repository contains concrete','The source tests assert','There is also accepted historical','The later transfer record']):
 frm(f'#proofrow{j}',{'opacity':.15,'x':-20,'duration':1},at(fragment))
to('#progress',{'scaleX':1,'duration':story['duration'],'ease':'none'},0)
# Text captions and audio are timed by HyperFrames to exact measured sentence clips.
caps=''.join(f'<div id="caption-{i+1}" class="caption clip" data-start="{c["start"]}" data-duration="{c["duration"]}" data-track-index="5">{html.escape(c["words"])}</div>' for i,c in enumerate(cues))
audio=''.join(f'<audio id="voice-{i+1}" class="clip" data-start="{c["start"]}" data-duration="{c["duration"]}" data-track-index="10" src="{c["path"]}"></audio>' for i,c in enumerate(cues))
navs=['EVIDENCE','IMPORT','FREEZE','DECIDE','EXECUTE','RECONCILE','VERIFY','LIMITS']
legend=[('UNTRUSTED INPUT','input'),('TRUSTED BACKEND','backend'),('HUMAN DECISION','human'),('SYNTHETIC PROVIDER','provider'),('OBSERVATION','observed')]
css='''*{box-sizing:border-box}html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#07131f;color:#edf6ff;font-family:Arial,sans-serif}#root{position:relative;width:1920px;height:1080px;overflow:hidden;background:radial-gradient(ellipse at 70% 30%,#142c40,#07131f 75%)}#root:before{content:"";position:absolute;inset:0;background-image:linear-gradient(#ffffff05 1px,transparent 1px),linear-gradient(90deg,#ffffff05 1px,transparent 1px);background-size:80px 80px}.eyebrow{position:absolute;left:90px;top:35px;color:#b3c7d7;font-size:28px;letter-spacing:2px}.synthetic{position:absolute;right:90px;top:35px;color:#f6bd66;font-size:28px;font-weight:700;letter-spacing:1px}#chapterTitle{position:absolute;left:90px;top:92px;font-size:48px;font-weight:700;letter-spacing:-.5px}.identity{position:absolute;left:90px;top:169px;font-size:28px;color:#69d9d4}.identity span{color:#b3c7d7;padding-left:55px}.map{position:absolute;left:90px;top:224px;display:flex;gap:10px}.map div{width:208px;height:49px;border:1px solid #405a70;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#b3c7d7;font-size:28px;letter-spacing:1px;font-weight:700}.legend{position:absolute;left:90px;top:295px;display:flex;gap:32px;font-size:28px;font-weight:700}.legend i{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:10px}.scene{position:absolute;left:90px;top:350px;width:1740px;height:500px;visibility:hidden}.scene svg{overflow:visible;width:1740px;height:500px;font-family:Arial,sans-serif}.provenance{position:absolute;left:90px;top:871px;font-size:28px;color:#b3c7d7}.provenance span{color:#69d9d4}.caption{position:absolute;left:120px;top:916px;width:1680px;padding:12px 24px;min-height:67px;border-radius:10px;text-align:center;font-size:32px;line-height:1.26;font-weight:600;background:#030c14ee}.track{position:absolute;left:90px;bottom:20px;width:1740px;height:4px;background:#2c4356}#progress{height:100%;background:#69d9d4;transform-origin:left}'''
page='<!doctype html><html lang="en"><head><meta charset="utf-8"><script src="assets/gsap.min.js"></script><style>'+css+'</style></head><body>'
page+=f'<div id="root" data-composition-id="awsops" data-start="0" data-duration="{story["duration"]}" data-width="1920" data-height="1080">'
page+='<div class="eyebrow">INSIDE AWSOPS · APPROVAL, EXECUTION &amp; PROOF</div><div class="synthetic">SYNTHETIC WALKTHROUGH</div><div id="chapterTitle"></div><div class="identity">CANARY A · resource-disposable-s3-canary<span>Batch A = illustrative public alias</span></div>'
page+='<div class="map">'+''.join(f'<div id="nav{i}">{name}</div>' for i,name in enumerate(navs))+'</div>'
page+='<div class="legend">'+''.join(f'<span style="color:{C[col]}"><i style="background:{C[col]}"></i>{label}</span>' for label,col in legend)+'</div>'
for i,s in enumerate(scenes):page+=f'<section class="scene" id="scene{i}"><svg viewBox="0 0 1740 500" aria-label="{html.escape(story["scenes"][i]["title"])}"><defs><marker id="arrow-{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10Z" fill="#72bfff"/></marker></defs>{s.replace("url(#arrow)",f"url(#arrow-{i})")}</svg></section>'
page+='<div class="provenance"><span>SOURCE 15c12fb5362d…</span> · No AWS calls · AI voice: Kokoro / Michael · Source &amp; limits included</div>'+caps+audio+'<div class="track"><div id="progress"></div></div></div>'
page+='<script>window.__timelines=window.__timelines||{};gsap.set(".scene",{autoAlpha:0});gsap.set("#progress",{scaleX:0});'+''.join(initial)+'const tl=gsap.timeline({paused:true});'+''.join(a)+'window.__timelines.awsops=tl;</script></body></html>'
(r/'index.html').write_text(page)
print('Composed',story['duration'],'seconds,',len(cues),'measured cues,',len(a),'state changes')
