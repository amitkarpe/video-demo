"""Paid OpenAI word timing and independent speech-content check, with reservation."""
from budget import P,reserve,finish
from decimal import Decimal
from openai import OpenAI
import hashlib,json,math,sys,wave
if '--approved-issue-24' not in sys.argv:raise SystemExit('Explicit API opt-in required')
target=P/'transcription.json'
if target.exists():raise SystemExit('Cached transcription exists; no call needed')
f=P/'assets/narration.wav'
with wave.open(str(f)) as w:duration=w.getnframes()/w.getframerate()
client=OpenAI(max_retries=0,timeout=180)
model=client.models.retrieve('whisper-1');assert model.id=='whisper-1'
reserve('narration-transcription','/v1/audio/transcriptions','whisper-1','0.15',dict(audio_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),language='en',timestamp_granularities=['word'],response_format='verbose_json'))
try:
    with f.open('rb') as audio:
        result=client.audio.transcriptions.create(model='whisper-1',file=audio,language='en',response_format='verbose_json',timestamp_granularities=['word'])
    data=result.model_dump();target.write_text(json.dumps(data,indent=2)+'\n')
    cost=Decimal(math.ceil(duration))*Decimal('0.006')/60
    finish('narration-transcription',status='completed',request_id=result._request_id,provider_duration=data.get('duration'),audio_seconds=duration,charged_or_reserved_usd=str(cost),cost_basis='0.006 USD/minute; conservatively round submitted duration up to one second.',output_sha256=hashlib.sha256(target.read_bytes()).hexdigest())
    print(json.dumps(dict(seconds=duration,words=len(data.get('words',[])),metered_usd=str(cost))))
except BaseException as e:
    finish('narration-transcription',status='uncertain',error_type=type(e).__name__)
    raise SystemExit('Transcription uncertain; reservation retained; no retry') from None
