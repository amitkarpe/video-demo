"""Shared OpenAI spend ledger. Reserve a conservative estimate BEFORE each paid call,
then settle it with the cost computed from the returned usage. Never stores the key."""
import json, os, pathlib, time
HERE = pathlib.Path(__file__).resolve().parent.parent
LF = HERE / "spend-ledger.json"
CAP = 50.00          # owner said budget is unlimited for this film; a working cap keeps the ledger a real stop
STOP_AT = 45.00      # self-imposed stop, leaves headroom for uncertainty

def load():
    return json.loads(LF.read_text()) if LF.exists() else {"cap_usd": CAP, "entries": []}

def committed(led):
    # settled cost when known, otherwise the reservation stays counted
    return sum(e.get("cost_usd", e["reserved_usd"]) for e in led["entries"])

def reserve(endpoint, model, est, label):
    led = load()
    if committed(led) + est > STOP_AT:
        raise SystemExit(f"STOP: {label} would push committed spend to {committed(led)+est:.3f} > {STOP_AT}")
    e = {"t": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "endpoint": endpoint, "model": model,
         "label": label, "reserved_usd": round(est, 6), "status": "CALLING"}
    led["entries"].append(e); LF.write_text(json.dumps(led, indent=2) + "\n")
    return len(led["entries"]) - 1

def settle(idx, status, cost=None, usage=None, extra=None):
    led = load(); e = led["entries"][idx]; e["status"] = status
    if cost is not None: e["cost_usd"] = round(cost, 6)
    if usage is not None: e["usage"] = usage
    if extra: e.update(extra)
    led["committed_usd"] = round(committed(led), 6)
    LF.write_text(json.dumps(led, indent=2) + "\n")

def api_key(env_file=None):
    k = os.environ.get("OPENAI_API_KEY")
    if not k and env_file:
        for ln in pathlib.Path(env_file).expanduser().read_text().splitlines():
            if ln.startswith("OPENAI_API_KEY="):
                k = ln.split("=", 1)[1].strip().strip('"').strip("'")
    if not k: raise SystemExit("OPENAI_API_KEY missing; no call made")
    return k
