"""Budget/receipt adapter around the unchanged bundled image-generation CLI.

The owner requires request metering and no uncertain retries. This adapter only
injects a no-retry client and records the response; the skill CLI owns generation.
Cached PNGs are sufficient for every ordinary video rebuild.
"""
from pathlib import Path
from decimal import Decimal
import hashlib,importlib.util,json,sys
from openai import OpenAI
from budget import P,reserve,finish

name=sys.argv[1] if len(sys.argv)>1 else ''
if name not in ['factory-day','factory-night']:raise SystemExit('Choose factory-day or factory-night')
if '--approved-issue-24' not in sys.argv:raise SystemExit('Explicit issue-24 API opt-in required')
target=P/'assets'/f'{name}.png'
if target.exists():raise SystemExit('Cached image exists; no call needed')
prompt=(P/'prompts'/f'{name}.txt').read_text()
cli=Path.home()/'.codex/skills/.system/imagegen/scripts/image_gen.py'
spec=importlib.util.spec_from_file_location('bundled_imagegen',cli);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
model='gpt-image-2.6-sunburst';editing=name.endswith('night')
inputs=dict(model=model,prompt=prompt,n=1,size='1536x1024',quality='high',output_format='png')
if editing:inputs['image_sha256']=hashlib.sha256((P/'assets/factory-day.png').read_bytes()).hexdigest()
reserve(name,'/v1/images/edits' if editing else '/v1/images/generations',model,'3.00',inputs)
client=OpenAI(max_retries=0,timeout=240)
real_generate=client.images.generate;real_edit=client.images.edit
receipt={}
def record(method,**kwargs):
    result=method(**kwargs)
    receipt.update(request_id=result._request_id,usage=result.usage.model_dump() if result.usage else None,returned_model=getattr(result,'model',None))
    return result
client.images.generate=lambda **kw:record(real_generate,**kw)
client.images.edit=lambda **kw:record(real_edit,**kw)
mod._create_client=lambda:client
args=['image_gen.py','edit' if editing else 'generate','--model',model,'--prompt-file',str(P/'prompts'/f'{name}.txt'),'--no-augment','--size','1536x1024','--quality','high','--out',str(target)]
if editing:args+=['--image',str(P/'assets/factory-day.png')]
sys.argv=args
try:
    mod.main()
    u=receipt.get('usage');cost=None
    if u:
        detail=u.get('input_tokens_details') or {}; image=detail.get('image_tokens',0);text=detail.get('text_tokens',u.get('input_tokens',0)-image)
        cost=(Decimal(text)*5+Decimal(image)*8+Decimal(u['output_tokens'])*30)/Decimal(1000000)
    finish(name,status='completed',**receipt,output_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),output_path=str(target.relative_to(P)),charged_or_reserved_usd=str(cost) if cost is not None else '3.00',cost_basis='Provider usage at published text 5 / image input 8 / image output 30 USD per million; full reservation retained if usage absent.',cli_sha256=hashlib.sha256(cli.read_bytes()).hexdigest())
    print(json.dumps(dict(name=name,usage=u,metered_usd=str(cost),output=str(target))))
except BaseException as exc:
    finish(name,status='uncertain',error_type=type(exc).__name__,**receipt)
    raise SystemExit('Image request uncertain; reservation retained; no retry. Reconcile the saved receipt.') from None
