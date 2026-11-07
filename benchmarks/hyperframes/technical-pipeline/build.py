#!/usr/bin/env python3
"""Build a local, seekable narrated technical film from verified lab facts."""
import argparse, json, math, html
from pathlib import Path
import soundfile as sf
from kokoro_onnx import Kokoro
p=argparse.ArgumentParser();p.add_argument('--model',required=True);p.add_argument('--voices',required=True);p.add_argument('--reuse-audio',action='store_true');a=p.parse_args()
r=Path(__file__).resolve().parent;assets=r/'assets';assets.mkdir(exist_ok=True)
scenes=[
('01','THE SIGNAL PROBLEM','FIVE SCANNERS → DISCONNECTED ALERTS','Five scanners can produce hundreds of disconnected alerts. Duplicates obscure what matters. This proof of concept turns raw signals into reviewable findings.'),
('02','ISOLATED TRAINING LAB','IDENTITY  ·  LABELS  ·  PINNED IMAGES  ·  ISOLATION','It begins inside deliberately vulnerable Docker labs. Preflight checks target identity, container labels, pinned images and network isolation. Unknown targets fail closed. No corporate systems are in scope.'),
('03','THE TRUST BOUNDARY','MODEL SELECTS  ·  PYTHON VALIDATES','A deterministic baseline is planned first. Then tool-less OpenCode sees sanitized findings and chooses only a fixed action ID and profile. Python validates the choice, budgets and timeouts. Model-written commands never execute.'),
('04','RECORDED DEMO REALITY','MAKE DEMO  =  RECORDED INPUT  ·  NO LIVE SCAN','The repeatable demo replays recorded ZAP, Nuclei, Nikto, Trivy and npm audit output. It runs no new scans. Agent follow-up choices are logged, not executed by the default runner. Normalizers produce a common finding schema.'),
('05','FROM ALERTS TO EVIDENCE','480 ALERTS  →  69 DISTINCT GROUPS','The Juice Shop sample groups 480 alerts into 69 findings. Six ZAP and Nikto alerts become one CORS finding with retained evidence. Code maps OWASP categories, computes CVSS from proposed vectors, and adds remediation.'),
('06','OUTPUTS AND CHAIN OF CUSTODY','VERDICT  ·  EVIDENCE  ·  AUDIT','For web findings, the model classifies probable issues, noise, or items needing human review. Model exchanges are recorded in a hash-chained audit trail. The output is HTML, JSON and optional deduplicated private GitHub issues.'),
('07','HONEST LAB MEASUREMENT','PROVISIONAL GROUND TRUTH  ·  HUMAN REVIEW','The sample shows 92 percent precision and 64 percent overall recall against provisional ground truth. Triage time was mostly model latency, not verified analyst time saved. Human review remains necessary.'),
('08','PHASED DELIVERY','CONTROLLED  ·  MEASURED  ·  AUDITABLE','Phase one built the lab pipeline. Phase two added accuracy measurement and more scanners. Phase three extended coverage to lab networks and Terraform code. This is a controlled, auditable scanner-to-report pipeline, not an autonomous hacker.')]
import re
k=None if a.reuse_audio else Kokoro(a.model,a.voices); clips=[]; cues=[];t=.6
for i,(num,title,tag,words) in enumerate(scenes):
 scene_start=t; sentences=re.split(r'(?<=[.!?])\s+',words)
 for j,sentence in enumerate(sentences):
  path=assets/f'voice-{i+1}-{j+1}.wav'
  if a.reuse_audio: audio,sr=sf.read(path)
  else:
   audio,sr=k.create(sentence,voice='am_michael',speed=1.0,lang='en-us');sf.write(path,audio,sr,subtype='PCM_16')
  duration=len(audio)/sr;cues.append(dict(start=round(t,3),duration=round(duration,3),words=sentence,path=f'assets/{path.name}'));t+=duration+.16
 clips.append(dict(number=num,title=title,tag=tag,words=words,start=round(scene_start,3),duration=round(t-scene_start,3)));t+=.45
 print(num,round(t-scene_start,2),flush=True)
end=math.ceil(t+0.4); print('TOTAL',end,flush=True)
if not 125<=end<=145: raise SystemExit('Duration outside 125–145 s: adjust narration or voice pace deliberately')
def stamp(x):
 ms=round(x*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(r/'captions.srt').write_text('\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["start"]+c["duration"])}\n{c["words"]}\n' for i,c in enumerate(cues)))
(r/'cues.json').write_text(json.dumps(cues,indent=2)+'\n')
(r/'storyboard.json').write_text(json.dumps({'duration':end,'scenes':clips},indent=2)+'\n')
(r/'transcript.txt').write_text('\n\n'.join(f"{c['number']} — {c['title']}\n{c['words']}" for c in clips)+'\n')
