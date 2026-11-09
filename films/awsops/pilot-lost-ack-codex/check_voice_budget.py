"""No-network checks of the actual paid-call admission boundary."""
import contextlib
import io
import json
from pathlib import Path
import runpy
import shutil
import sys
import tempfile
from unittest.mock import patch

P = Path(__file__).resolve().parent

def check_case(name, change, expected):
    with tempfile.TemporaryDirectory(prefix='pilot15-budget-') as folder:
        root = Path(folder)
        for filename in ('generate_openai_voice.py', 'build.py'):
            shutil.copyfile(P / filename, root / filename)
        ledger = json.loads((P / 'openai-spend.json').read_text())
        change(ledger)
        original = json.dumps(ledger)
        (root / 'openai-spend.json').write_text(original)
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-placeholder'}), \
             patch.object(sys, 'argv', ['generate_openai_voice.py', '--approved-phase-2']), \
             patch('urllib.request.urlopen', side_effect=AssertionError('NETWORK MUST NOT RUN')) as network, \
             contextlib.redirect_stdout(io.StringIO()):
            try:
                runpy.run_path(str(root / 'generate_openai_voice.py'), run_name='__main__')
            except SystemExit as exc:
                assert expected in str(exc), str(exc)
            else:
                raise AssertionError('Expected stop did not occur')
            network.assert_not_called()
        assert (root / 'openai-spend.json').read_text() == original
    print(name + ': PASS (zero network calls; ledger unchanged)')

def near_cap(ledger):
    ledger['calls'] = ledger['calls'][:-1]
    for call in ledger['calls']:
        call['reserved_usd'] = '0'
    ledger['calls'][0]['reserved_usd'] = '4.999'

def uncertain(ledger):
    ledger['calls'][0]['status'] = 'uncertain'

check_case('Next call would exceed USD 5', near_cap, 'CAP STOP')
check_case('Prior call uncertain', uncertain, 'Uncertain prior call')
