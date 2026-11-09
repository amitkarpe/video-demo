"""Offline captions, original procedural score, and seekable scene composition."""
from pathlib import Path
import array,difflib,html,json,math,re,sys,wave
P=Path(__file__).resolve().parent
timing=json.loads((P/'timing.json').read_text());asr=json.loads((P/'transcription.json').read_text())
def norm(w):return re.sub(r'[^a-z0-9]','',w.lower())
captions=[];review=[]
for cue in timing['cues']:
    lo=cue['start'];hi=lo+cue['duration'];expected=cue['text'].split()
    words=[w for w in asr['words'] if lo-.3 <= (w['start']+w['end'])/2 < hi+.25]
    # ASR timestamps are evidence, not editorial authority. Align to approved wording.
    match=difflib.SequenceMatcher(None,[norm(w) for w in expected],[norm(w['word']) for w in words],autojunk=False)
    anchors={}
    for tag,a,b,c,d in match.get_opcodes():
        if tag=='equal':
            for k in range(b-a):anchors[a+k]=max(lo,min(hi-.02,words[c+k]['start']))
        else:review.append(dict(cue=cue['index'],operation=tag,script=' '.join(expected[a:b]),asr=' '.join(w['word'] for w in words[c:d])))
    anchors.setdefault(0,lo+.05);anchors[len(expected)]=hi
    for k in range(len(expected)):
        if k not in anchors:
            before=max(j for j in anchors if j<k);after=min(j for j in anchors if j>k)
            anchors[k]=anchors[before]+(anchors[after]-anchors[before])*(k-before)/(after-before)
    # Ensure monotonic placement even when ASR emits a zero-length word.
    for k in range(1,len(expected)+1):anchors[k]=max(anchors[k],anchors[k-1]+.015)
    i=0
    while i<len(expected):
        j=i+1
        while j<len(expected) and j-i<9 and len(' '.join(expected[i:j+1]))<=79:
            if j-i>=4 and expected[j-1][-1] in '.?!:':break
            j+=1
        if 0<len(expected)-j<3:
            j=max(i+1,len(expected)-3)
        text=' '.join(expected[i:j]);tokens=text.split();lines=[text]
        if len(text)>45:
            split=min(range(1,len(tokens)),key=lambda n:abs(len(' '.join(tokens[:n]))-len(' '.join(tokens[n:]))))
            lines=[' '.join(tokens[:split]),' '.join(tokens[split:])]
        start=round(max(lo,anchors[i]),3);end=round(min(hi,anchors[j]-.025 if j<len(expected) else hi),3)
        captions.append(dict(start=start,end=max(start+.1,end),text=text,lines=lines,cue=cue['index']))
        i=j
for a,b in zip(captions,captions[1:]):assert a['end']<=b['start']+.001
assert all(c['end']>c['start'] for c in captions)
(P/'captions.json').write_text(json.dumps(captions,indent=2)+'\n')
(P/'caption-alignment-review.json').write_text(json.dumps(review,indent=2)+'\n')
def stamp(t):
    n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'
(P/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n"+'\n'.join(c['lines']) for i,c in enumerate(captions))+'\n')
caphtml='\n'.join(f'<div class="caption" id="cap{i}"><span>'+ '<br>'.join(html.escape(x) for x in c['lines'])+'</span></div>' for i,c in enumerate(captions))
s=(P/'scene.html.template').read_text().replace('__DURATION__',str(timing['duration'])).replace('__CAPTIONS__',caphtml).replace('__TIMING__',json.dumps(timing)).replace('__CAPTION_TIMING__',json.dumps(captions))
(P/'index.html').write_text(s)
# Original deterministic D-minor / B-flat / F / C pulse. No licensed sample assets.
sr=24000;duration=timing['duration'];pcm=array.array('h');chords=[(146.832,174.614,220),(116.541,146.832,174.614),(130.813,174.614,220),(130.813,164.814,195.998)]
starts=[s['start'] for s in timing['scenes']];changes=iter(starts);next_change=next(changes);last_change=-10
for n in range(duration*sr):
    t=n/sr
    if next_change is not None and t>=next_change:last_change=next_change;next_change=next(changes,None)
    chord=chords[int(t/8)%4];beat=t%(.75);arp=chord[int(t/.75)%3]*2
    pad=sum(math.sin(2*math.pi*f*t)+.23*math.sin(2*math.pi*f*2.002*t) for f in chord)/3
    pulse=math.sin(2*math.pi*arp*t)*math.exp(-beat*6)*.22
    delta=t-last_change;chime=(math.sin(2*math.pi*880*delta)+.3*math.sin(2*math.pi*1320*delta))*math.exp(-delta*3)*.15 if 0<=delta<2 else 0
    fade=min(1,t/3,(duration-t)/4);sample=(pad*.56+pulse+chime)*.032*max(0,fade)
    pcm.append(round(max(-1,min(1,sample))*32767))
if sys.byteorder!='little':pcm.byteswap()
with wave.open(str(P/'assets/score.wav'),'wb') as w:w.setparams((1,2,sr,len(pcm),'NONE','not compressed'));w.writeframes(pcm.tobytes())
print(json.dumps(dict(duration=duration,captions=len(captions),alignment_edits=len(review),max_caption_chars=max(len(c['text']) for c in captions))))
