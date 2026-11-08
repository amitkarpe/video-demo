"""OpenAI Speech API, SSE usage receipts, no retries, cached PCM narration."""
from budget import P,reserve,finish,read
import base64,hashlib,json,os,sys,urllib.request,wave
from decimal import Decimal

if '--approved-issue-24' not in sys.argv:raise SystemExit('Explicit issue-24 API opt-in required')
rows=json.loads((P/'script.json').read_text())
limit=int(sys.argv[sys.argv.index('--limit')+1]) if '--limit' in sys.argv else len(rows)
instructions='Warm, precise cinematic documentary narration. Clear international English, natural connected phrasing, measured pace around 145 words per minute. Curious opening; confident explanation; firm safety gates. Read exactly the provided text. Do not add words, music, or sound effects. Avoid exaggerated announcer delivery.'
for i,row in enumerate(rows[:limit]):
    name=f'voice-{i:02}';target=P/'assets'/f'{name}.wav'
    if target.exists():
        receipt=next(c for c in read()['calls'] if c['name']==name)
        assert receipt['status']=='completed' and receipt['output_sha256']==hashlib.sha256(target.read_bytes()).hexdigest()
        continue
    payload=dict(model='gpt-4o-mini-tts',voice='cedar',input=row['spoken'],instructions=instructions,response_format='pcm',stream_format='sse',speed=1.0)
    reserve(name,'/v1/audio/speech',payload['model'],'0.25',payload)
    request=urllib.request.Request('https://api.openai.com/v1/audio/speech',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+os.environ['OPENAI_API_KEY'],'Content-Type':'application/json'})
    receipt={}
    try:
        with urllib.request.urlopen(request,timeout=180) as response:
            receipt['request_id']=response.headers.get('x-request-id');raw=response.read()
        (P/'.build'/f'{name}.sse').write_bytes(raw)
        events=[];chunks=[];usage=None
        for line in raw.decode().splitlines():
            if not line.startswith('data:'):continue
            text=line[5:].strip()
            if text=='[DONE]':continue
            e=json.loads(text);events.append({k:v for k,v in e.items() if k not in ['audio','delta']})
            if e.get('type')=='speech.audio.delta':chunks.append(base64.b64decode(e.get('audio',e.get('delta',''))))
            if e.get('usage'):usage=e['usage']
        pcm=b''.join(chunks);assert pcm and len(pcm)%2==0, 'No complete PCM in cached SSE'
        with wave.open(str(target),'wb') as w:w.setparams((1,2,24000,len(pcm)//2,'NONE','not compressed'));w.writeframes(pcm)
        cost=None
        if usage and 'input_tokens' in usage and 'output_tokens' in usage:
            cost=(Decimal(usage['input_tokens'])*Decimal('0.6')+Decimal(usage['output_tokens'])*12)/1000000
        finish(name,status='completed',**receipt,voice='cedar',instructions=instructions,input=row['spoken'],usage=usage,event_metadata=events[-1:],audio_seconds=len(pcm)/48000,output_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),charged_or_reserved_usd=str(cost) if cost is not None else '0.25',cost_basis='SSE token usage: input 0.60 and output 12 USD per million. Full 0.25 reservation retained if usage missing.')
        print(json.dumps(dict(cue=i,seconds=len(pcm)/48000,usage=usage,metered_usd=str(cost))),flush=True)
    except BaseException as exc:
        finish(name,status='uncertain',error_type=type(exc).__name__,**receipt)
        raise SystemExit('Speech request uncertain; cached SSE/reservation retained; no retry') from None
