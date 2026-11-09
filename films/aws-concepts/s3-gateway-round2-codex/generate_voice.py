"""Explicit opt-in speech generation. Reserve before each call; never retry uncertainty."""
import ast
import hashlib
import json
import io
import os
from pathlib import Path
import sys
import urllib.request
import urllib.error
import wave
from decimal import Decimal
from datetime import datetime, timezone

P = Path(__file__).resolve().parent
CAP = Decimal('5')
RATE = Decimal('30') / Decimal('1000000')
LEDGER = P / 'openai-spend.json'
MODEL, VOICE = 'tts-1-hd', 'nova'

def save(data):
    tmp = LEDGER.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, indent=2) + '\n')
    tmp.replace(LEDGER)

if '--approved-issue-19' not in sys.argv:
    raise SystemExit('Requires explicit --approved-issue-19. Cached assets need no API.')
key = os.environ.get('OPENAI_API_KEY')
if not key:
    raise SystemExit('OPENAI_API_KEY missing; no request sent')
rows = [(r['caption'], r['spoken']) for r in json.loads((P / 'script.json').read_text())]
ledger = json.loads(LEDGER.read_text()) if LEDGER.exists() else dict(
    model=MODEL, voice=VOICE, cap_usd=str(CAP), price_usd_per_million_input_characters='30',
    pricing_source='https://developers.openai.com/api/docs/models/tts-1-hd',
    authority='Issue 19 authorizes Round 2 execution; narration only, incremental media cap USD 5.',
    billing_note='Character-metered billable amount at published list rate; invoice reconciliation not independently available. Credits do not reduce recorded usage cost.',
    calls=[])
if ledger['model'] != MODEL or ledger['voice'] != VOICE:
    raise SystemExit('Ledger model/voice mismatch')
if any(c['status'] != 'completed' for c in ledger['calls']):
    raise SystemExit('Uncertain prior call: stop for reconciliation, never resend')
for i, (caption, spoken) in enumerate(rows):
    text = spoken or caption
    old = next((c for c in ledger['calls'] if c['cue'] == i), None)
    if old:
        if old['input_sha256'] != hashlib.sha256(text.encode()).hexdigest():
            raise SystemExit('Cached narration changed: explicit new budget decision required')
        continue
    chars = len(text)
    reserve = Decimal(chars) * RATE
    used = sum(Decimal(c['reserved_usd']) for c in ledger['calls'])
    if used + reserve > CAP:
        raise SystemExit('CAP STOP: no call sent')
    row = dict(cue=i, input_characters=chars, input_sha256=hashlib.sha256(text.encode()).hexdigest(),
               reserved_usd=str(reserve), status='reserved', timestamp=datetime.now(timezone.utc).isoformat())
    ledger['calls'].append(row)
    save(ledger)
    payload = json.dumps(dict(model=MODEL, voice=VOICE, input=text, response_format='wav', speed=1.0)).encode()
    request = urllib.request.Request('https://api.openai.com/v1/audio/speech', data=payload,
        headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            audio = response.read()
            row['request_id'] = response.headers.get('x-request-id')
            row['http_status'] = response.status
        target = P / f'assets/voice-{i:02}.wav'
        staged = target.with_suffix('.pending.wav')
        # Finalize unknown-length streaming WAV headers without changing PCM.
        row['transport_wav_sha256'] = hashlib.sha256(audio).hexdigest()
        with wave.open(io.BytesIO(audio)) as w:
            params = w.getparams()
            frames = w.readframes(w.getnframes())
        if not frames:
            raise ValueError('Empty speech')
        with wave.open(str(staged), 'wb') as out:
            out.setparams(params._replace(nframes=len(frames) // (params.sampwidth * params.nchannels)))
            out.writeframes(frames)
        row['audio_seconds'] = round(len(frames) / (params.sampwidth * params.nchannels * params.framerate), 4)
        audio = staged.read_bytes()
        staged.replace(target)
        row.update(status='completed', metered_usd=str(reserve), output_sha256=hashlib.sha256(audio).hexdigest())
        ledger['metered_total_usd'] = str(sum(Decimal(c.get('metered_usd', '0')) for c in ledger['calls']))
        save(ledger)
        print(json.dumps(dict(cue=i, characters=chars, cost_usd=str(reserve), cumulative_usd=ledger['metered_total_usd'], seconds=row['audio_seconds'])), flush=True)
    except Exception as exc:
        row['status'] = 'uncertain'
        row['error_type'] = type(exc).__name__
        if isinstance(exc, urllib.error.HTTPError):
            row['http_status'] = exc.code
        save(ledger)
        raise SystemExit('Speech call failed or uncertain; reserved amount retained; NO automatic retry') from None
print('Speech complete; all calls metered; no more requests needed')
