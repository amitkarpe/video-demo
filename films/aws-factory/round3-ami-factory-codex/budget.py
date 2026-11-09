"""Shared pre-call reservations for every incremental media/QA endpoint."""
from pathlib import Path
from decimal import Decimal
from datetime import datetime,timezone
import hashlib,json
P=Path(__file__).resolve().parent
FILE=P/'api-spend.json'; CAP=Decimal('10')
def read():
    return json.loads(FILE.read_text()) if FILE.exists() else dict(cap_usd='10.00',authority='video-demo issue 24',calls=[])
def save(d):
    q=FILE.with_suffix('.tmp');q.write_text(json.dumps(d,indent=2)+'\n');q.replace(FILE)
def reserve(name,endpoint,model,amount,inputs):
    d=read()
    if any(c['status'] in ['reserved','uncertain'] for c in d['calls']):raise RuntimeError('STOP: prior uncertain/reserved call; reconcile, never replay')
    if any(c['name']==name for c in d['calls']):raise RuntimeError('STOP: call name already exists; use cached output')
    used=sum(Decimal(c.get('charged_or_reserved_usd',c['reservation_usd'])) for c in d['calls'])
    if used+Decimal(amount)>CAP:raise RuntimeError('STOP: next reservation exceeds USD 10')
    row=dict(name=name,endpoint=endpoint,model=model,reservation_usd=str(amount),status='reserved',at=datetime.now(timezone.utc).isoformat(),input_sha256=hashlib.sha256(json.dumps(inputs,sort_keys=True).encode()).hexdigest())
    d['calls'].append(row);save(d);return row
def finish(name,**fields):
    d=read();r=next(c for c in d['calls'] if c['name']==name);r.update(fields)
    if 'charged_or_reserved_usd' not in r:r['charged_or_reserved_usd']=r['reservation_usd']
    d['accounted_total_usd']=str(sum(Decimal(c.get('charged_or_reserved_usd',c['reservation_usd'])) for c in d['calls']))
    d['remaining_usd']=str(CAP-Decimal(d['accounted_total_usd']));save(d)
    if Decimal(d['accounted_total_usd'])>CAP:raise RuntimeError('STOP: unexpected provider usage above cap')
