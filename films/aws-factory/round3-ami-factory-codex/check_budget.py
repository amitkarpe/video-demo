"""Exercise admission on synthetic ledgers. No network is involved."""
import json,tempfile
from pathlib import Path
import budget
with tempfile.TemporaryDirectory() as temp:
    budget.FILE=Path(temp)/'ledger.json'
    for status,cost,expect in [('completed','9.90','exceeds'),('uncertain','0.01','uncertain')]:
        original=json.dumps({'calls':[dict(name='prior',status=status,reservation_usd=cost,charged_or_reserved_usd=cost)]})
        budget.FILE.write_text(original)
        try:budget.reserve('new','test','test','0.25',{})
        except RuntimeError as e:assert expect in str(e)
        else:raise AssertionError('Admission should stop')
        assert budget.FILE.read_text()==original
        print(f'{status} guard: PASS; ledger unchanged')
