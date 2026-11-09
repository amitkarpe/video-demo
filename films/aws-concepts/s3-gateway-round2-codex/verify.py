"""Check the real encoded artifact; generate review frames and machine receipts."""
from pathlib import Path
import hashlib,json,re,subprocess

P=Path(__file__).resolve().parent
def run(args):
    return subprocess.run(args,cwd=P,check=True,capture_output=True)
probe=json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json','pilot.mp4']).stdout)
v=next(s for s in probe['streams'] if s['codec_type']=='video')
a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert (v['codec_name'],v['width'],v['height'],v['r_frame_rate'])==('h264',1920,1080,'30/1')
assert a['codec_name']=='aac'
assert 45<=float(probe['format']['duration'])<=60
run(['ffmpeg','-v','error','-i','pilot.mp4','-f','null','-'])
timing=json.loads((P/'timing.json').read_text())
cues=timing['cues']
assert all(cues[i]['start']+cues[i]['duration'] <= cues[i+1]['start'] for i in range(len(cues)-1))
assert cues[-1]['start']+cues[-1]['duration']<=timing['duration']
levels=run(['ffmpeg','-hide_banner','-i','pilot.mp4','-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-']).stderr.decode()
loudness=json.loads(re.findall(r'\{[^{}]+\}',levels)[-1])
assert float(loudness['input_tp'])<=-1.0
assert -18<=float(loudness['input_i'])<=-14
selected={'hook':3,'mechanism':20.5,'payoff':43}
diagnostics={'dns':10,'packet':24.5,'endpoint':28,'network-access':34,'policies':38.5,'transition':41.4}
for name,t in {**selected,**diagnostics}.items():
    dest='keyframes' if name in selected else '.build'
    run(['ffmpeg','-y','-v','error','-ss',str(t),'-i','pilot.mp4','-frames:v','1',f'{dest}/{name}.png'])
    run(['ffmpeg','-y','-v','error','-ss',str(t),'-i','pilot.mp4','-frames:v','1','-vf','scale=1280:720',f'.build/{name}-720.png'])
def pixels(t):
    return run(['ffmpeg','-v','error','-ss',str(t),'-i','pilot.mp4','-frames:v','1','-vf','crop=1740:300:90:450,scale=580:100,format=gray','-f','rawvideo','-']).stdout
motion=[]
for begin,finish in [(19.5,20.5),(24,25),(42,43)]:
    x,y=pixels(begin),pixels(finish);assert len(x)==len(y)>0
    changed=sum(abs(a-b)>8 for a,b in zip(x,y))
    assert changed>100, (begin,finish,changed)
    motion.append(dict(seconds=[begin,finish],changed_pixels=changed,total_pixels=len(x),threshold=8))
run(['ffmpeg','-y','-v','error','-ss','14','-i','pilot.mp4','-t','12','-c:v','libx264','-preset','fast','-crf','22','-c:a','aac','-b:a','128k','-movflags','+faststart','preview.mp4'])
receipt=dict(duration_seconds=float(probe['format']['duration']),video_codec=v['codec_name'],width=v['width'],height=v['height'],fps=v['r_frame_rate'],audio_codec=a['codec_name'],audio_sample_rate=a['sample_rate'],bytes=(P/'pilot.mp4').stat().st_size,sha256=hashlib.sha256((P/'pilot.mp4').read_bytes()).hexdigest(),full_decode='PASS',captions={'cues':len(cues),'overlaps':0,'max_characters_per_second':round(max(len(c['text'])/c['duration'] for c in cues),2)},loudness_lufs=loudness['input_i'],true_peak_dbtp=loudness['input_tp'],encoded_motion=motion,keyframe_times=selected,AUDIBLE_REVIEW='NOT_VERIFIED',owner_acceptance='PENDING')
(P/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
