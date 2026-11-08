"""Second ASR check of two words flagged by Whisper; no script prompt bias."""
from budget import P,reserve,finish
from openai import OpenAI
from decimal import Decimal
import hashlib,json,sys,wave
if '--approved-issue-24' not in sys.argv:raise SystemExit('Explicit API opt-in required')
if (P/'pronunciation-crosscheck.json').exists():raise SystemExit('Cached QA output exists; no call needed')
f=P/'.build/pronunciation.wav';pcm=b''
for i in (6,22):
    with wave.open(str(P/'assets'/f'voice-{i:02}.wav')) as w:pcm+=w.readframes(w.getnframes())+b'\0'*48000
with wave.open(str(f),'wb') as w:w.setparams((1,2,24000,len(pcm)//2,'NONE','not compressed'));w.writeframes(pcm)
name='pronunciation-crosscheck';model='gpt-4o-transcribe';inputs=dict(audio_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),language='en',response_format='json')
reserve(name,'/v1/audio/transcriptions',model,'.15',inputs)
try:
    with f.open('rb') as audio:
        result=OpenAI(max_retries=0,timeout=90).audio.transcriptions.create(model=model,file=audio,language='en',response_format='json')
    d=result.model_dump();(P/'pronunciation-crosscheck.json').write_text(json.dumps(d,indent=2)+'\n')
    u=d['usage'];cost=(Decimal(u['input_tokens'])*Decimal('2.5')+Decimal(u['output_tokens'])*10)/1000000
    finish(name,status='completed',request_id=result._request_id,usage=u,charged_or_reserved_usd=str(cost),pricing_source='https://developers.openai.com/api/docs/models/gpt-4o-transcribe',output_sha256=hashlib.sha256((P/'pronunciation-crosscheck.json').read_bytes()).hexdigest())
    print(d['text']);print('Metered USD',cost)
except BaseException as e:
    finish(name,status='uncertain',error_type=type(e).__name__);raise
