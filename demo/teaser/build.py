#!/usr/bin/env python3
"""Build the ten-second local motion-graphics teaser from its saved assets."""
import subprocess
import tempfile
from pathlib import Path
import sys
R = Path(__file__).resolve().parent
out = Path(sys.argv[1]).resolve() if len(sys.argv)>1 else R / 'teaser.mp4'
out.parent.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix='cloud-teaser-') as tmp:
    t=Path(tmp); exe=t/'render'
    subprocess.run(['swiftc',str(R/'render.swift'),'-o',str(exe)],check=True)
    subprocess.run([str(exe),str(t)],check=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-loop','1','-framerate','30','-i',str(R/'background.png')]
    for i in range(6): cmd += ['-loop','1','-framerate','30','-i',str(t/f'overlay-{i}.png')]
    cmd += ['-i',str(R/'narration-cedar.wav')]
    fc="[0:v]scale=2160:1215,zoompan=z='min(1.04+on*0.00016,1.10)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=30,format=yuv420p[base];[base][6:v]overlay=x='mod(t*180,1380)-150':y=0[energy];[energy][1:v]overlay=0:0[badge]"
    last='badge'; start=[0.55,2.60,4.08,5.45]; end=[2.60,4.08,5.45,9.75]
    for i,(a,b) in enumerate(zip(start,end),2):
        fc+=f";[{i}:v]format=rgba,fade=t=in:st={a}:d=0.20:alpha=1,fade=t=out:st={b-0.20}:d=0.20:alpha=1[o{i}];[{last}][o{i}]overlay=x='if(lt(t,{a}+0.35),-80*(1-(t-{a})/0.35),0)':y=0:enable='between(t,{a},{b})'[v{i}]"
        last=f'v{i}'
    cmd += ['-filter_complex',fc,'-map',f'[{last}]','-map','7:a','-af','adelay=650|650,apad','-t','10','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)]
    subprocess.run(cmd,check=True)
print('Created',out)
