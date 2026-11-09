"""Offline final-output checks and five real keyframes. No API calls."""
from pathlib import Path
from decimal import Decimal
import hashlib,json,re,subprocess
P=Path(__file__).resolve().parent;video=P/'blueops-trust-factory.mp4';out=P/'evidence';out.mkdir(exist_ok=True)
def run(args):return subprocess.run(args,check=True,capture_output=True,text=True)
probe=json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(video)]).stdout)
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],v['pix_fmt'])==('h264',1920,1080,'30/1','yuv420p')
assert a['codec_name']=='aac' and a['channels']==2
assert abs(float(probe['format']['duration'])-268)<.1
assert int(v['nb_frames'])==8040
r=run(['ffmpeg','-v','error','-i',str(video),'-f','null','-']);assert not r.stderr.strip()
cs=json.loads((P/'captions.json').read_text());assert len(cs)==79
assert all(0<=c['start']<c['end']<=268 and c['end']-c['start']>=.7 for c in cs)
assert all(x['end']<=y['start'] for x,y in zip(cs,cs[1:]));assert all(len(c['lines'])<=2 for c in cs)
ledger=json.loads((P/'api-spend.json').read_text());assert len(ledger['calls'])==31
assert all(c['status']=='completed' for c in ledger['calls'])
assert sum(Decimal(c['charged_or_reserved_usd']) for c in ledger['calls'])<=Decimal(10)
verified=[]
for c in ledger['calls']:
    f=None
    if c['name'].startswith('voice-'):f=P/'assets'/(c['name']+'.wav')
    elif c['name'].startswith('factory-'):f=P/c['output_path']
    elif c['name']=='narration-transcription':f=P/'transcription.json'
    elif c['name']=='pronunciation-crosscheck':f=P/'pronunciation-crosscheck.json'
    if f:assert hashlib.sha256(f.read_bytes()).hexdigest()==c['output_sha256'];verified.append(str(f.relative_to(P)))
levels=run(['ffmpeg','-hide_banner','-i',str(video),'-af','loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json','-f','null','-']).stderr
m=re.search(r'\{\s*"input_i".*?\}',levels,re.S);assert m
levels=json.loads(m.group());assert -16.5<=float(levels['input_i'])<=-15.5 and float(levels['input_tp'])<=-1.0
# Compare cropped encoded motion, excluding titles, captions and progress meter.
def pixels(t):
 return subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(video),'-frames:v','1','-vf','crop=1440:480:240:300,scale=240:80','-pix_fmt','rgb24','-f','rawvideo','-'],check=True,capture_output=True).stdout
motion=[]
for lo,hi in [(5,6),(141.5,143.5),(243,245)]:
 x,y=pixels(lo),pixels(hi);assert len(x)==len(y)==240*80*3
 diff=sum(abs(a-b) for a,b in zip(x,y))/len(x);assert diff>.1
 motion.append(dict(start=lo,end=hi,mean_absolute_rgb_difference=round(diff,4),crop='1440x480+240+300'))
keys=P/'keyframes';keys.mkdir(exist_ok=True)
for name,t in [('01-factory',5),('02-three-families',66),('03-ecs-gate',149),('04-future-policy',221),('05-recovery',247)]:
 run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(video),'-frames:v','1',str(keys/(name+'.png'))])
public_files=[p for p in P.rglob('*') if p.is_file() and not any(s in p.parts for s in ['.build','.hyperframes','__pycache__']) and p.suffix in ['.py','.json','.md','.html','.template','.txt','.sh','.srt']]
private_patterns=[r'sk-[A-Za-z0-9_-]{20,}',r'\b\d{12}\b',r'\b(?:ami|vpc|subnet|snap|sg)-[0-9a-f]{8,}\b',r'arn:aws(?:-us-gov|-cn)?:[a-z0-9-]+:']
findings=[]
for f in public_files:
 text=f.read_text()
 for pat in private_patterns:
  if re.search(pat,text):findings.append(str(f.relative_to(P)))
assert not findings,findings
summary=dict(video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),bytes=video.stat().st_size,duration_seconds=float(probe['format']['duration']),frames=int(v['nb_frames']),video_codec=v['codec_name'],audio_codec=a['codec_name'],width=v['width'],height=v['height'],fps=v['r_frame_rate'],pixel_format=v['pix_fmt'],full_decode='PASS',captions=dict(count=len(cs),overlaps=0,minimum_duration=min(round(c['end']-c['start'],3) for c in cs),maximum_lines=2),loudness=levels,encoded_motion=motion,cached_asset_hashes_verified=len(verified),paid_calls=len(ledger['calls']),api_usage_priced_usd=ledger['accounted_total_usd'],privacy_pattern_findings=findings,privacy_scope='Text artifact pattern scan plus manual source/content review; no claim of exhaustive secret detection.',audible_review='NOT_VERIFIED')
(out/'technical-checks.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
