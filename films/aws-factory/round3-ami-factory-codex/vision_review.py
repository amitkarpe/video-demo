"""Optional, explicitly authorized paid review of public-safe encoded frames."""
from budget import P,reserve,finish
from openai import OpenAI
from decimal import Decimal
import base64,hashlib,json,sys
if '--approved-issue-24' not in sys.argv:raise SystemExit('Explicit API opt-in required')
if (P/'vision-review.json').exists():raise SystemExit('Cached QA output exists; no call needed')
files=sorted((P/'.build/review-frames').glob('*.jpg'));assert 8<=len(files)<=16
prompt='Review these timestamped frames from an original 268-second factory explainer. Assess visible legibility, collisions/cropping, narrative clarity and honest distinctions between current evidence, required tests and proposed policy. Do not infer motion or listening from stills. No numeric score. Return JSON with blocking_findings (each timestamp, visible evidence, concrete fix), improvements, strengths, limitations. In the required story, Golden AL2023 feeds Hardened Base OS, with THREE DIRECT children GitLab, MongoDB, CloudOS ECS Worker; the base stays DEV. Phase A needs DEV proof, effective shareability, exact PROD image/configuration/canary and explicit Ops approval. Phase B is a proposed weekly candidate/monthly first-Saturday-night policy needing prior management/security/change approval; current unattended PROD is NOT established. Mongo standalone does not prove cluster; ECS zero placed tasks fails. Unknown or failed evidence/approval/access/canary blocks. The film is illustrative, no live operations. Prior known-good and data recovery are separate. Please flag only defects supported by the supplied images; distinguish suggestions from blockers.'
content=[dict(type='text',text=prompt)]
for f in files:
    content.extend([dict(type='text',text=f.stem),dict(type='image_url',image_url=dict(url='data:image/jpeg;base64,'+base64.b64encode(f.read_bytes()).decode(),detail='high'))])
inputs=dict(prompt=prompt,images={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files},max_completion_tokens=2000)
(P/'vision-review-input.json').write_text(json.dumps(inputs,indent=2)+'\n')
name='encoded-frame-review';model='gpt-4.1-mini';reserve(name,'/v1/chat/completions',model,'.30',inputs)
try:
    r=OpenAI(max_retries=0,timeout=120).chat.completions.create(model=model,messages=[dict(role='user',content=content)],max_completion_tokens=2000,response_format=dict(type='json_object'))
    d=r.model_dump();(P/'vision-review.json').write_text(json.dumps(d,indent=2)+'\n');u=d['usage'];cached=u.get('prompt_tokens_details',{}).get('cached_tokens',0)
    cost=(Decimal(u['prompt_tokens']-cached)*Decimal('.40')+Decimal(cached)*Decimal('.10')+Decimal(u['completion_tokens'])*Decimal('1.60'))/1000000
    finish(name,status='completed',request_id=r._request_id,usage=u,returned_model=r.model,charged_or_reserved_usd=str(cost),pricing_source='https://developers.openai.com/api/docs/models/gpt-4.1-mini')
    print(r.choices[0].message.content);print('Metered USD',cost)
except BaseException as e:finish(name,status='uncertain',error_type=type(e).__name__);raise
