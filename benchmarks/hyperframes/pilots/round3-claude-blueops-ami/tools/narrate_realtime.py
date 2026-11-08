#!/usr/bin/env python3
"""Narrate script.json lines with the OpenAI Realtime API (gpt-realtime-2.1, WebSocket), metered.
One short session per line; usage from response.done is settled into spend-ledger.json.
  python tools/narrate_realtime.py --env-file <.env> [--only s01 s02]
Writes assets/voice/<id>.wav (24 kHz mono, edges trimmed), voice-takes.json (transcript, match, usage)."""
import argparse, asyncio, base64, json, pathlib, re, sys
import numpy as np, soundfile as sf, websockets
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import ledger
HERE = pathlib.Path(__file__).resolve().parent.parent
PRICE = {"text_in": 4/1e6, "audio_in": 32/1e6, "cached_in": 0.4/1e6, "text_out": 24/1e6, "audio_out": 64/1e6}
ap = argparse.ArgumentParser(); ap.add_argument("--env-file"); ap.add_argument("--only", nargs="*")
a = ap.parse_args()
script = json.loads((HERE / "script.json").read_text()); V = script["voice"]
key = ledger.api_key(a.env_file)
tf = HERE / "voice-takes.json"; takes = json.loads(tf.read_text()) if tf.exists() else {}
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", re.sub(r"[-–—]", " ", s.lower())).split()

def cost_of(u):
    i = u.get("input_token_details", {}) or {}; o = u.get("output_token_details", {}) or {}
    cached = i.get("cached_tokens", 0) or 0
    return ((i.get("text_tokens", 0) or 0) * PRICE["text_in"] + (i.get("audio_tokens", 0) or 0) * PRICE["audio_in"]
            + cached * PRICE["cached_in"] + (o.get("text_tokens", 0) or 0) * PRICE["text_out"]
            + (o.get("audio_tokens", 0) or 0) * PRICE["audio_out"])

async def speak(line):
    text = line["caption"]
    est = 400 * PRICE["text_in"] + 200 * PRICE["text_out"] + max(8, len(text.split())) * 1.0 * 40 * PRICE["audio_out"]
    idx = ledger.reserve("realtime (wss)", V["model"], est, "voice:" + line["id"])
    pcm, transcript, usage = bytearray(), "", None
    try:
        async with websockets.connect(f"wss://api.openai.com/v1/realtime?model={V['model']}",
                                      additional_headers={"Authorization": f"Bearer {key}"}, max_size=None,
                                      open_timeout=30) as ws:
            await ws.send(json.dumps({"type": "session.update", "session": {
                "type": "realtime", "output_modalities": ["audio"], "instructions": V["instructions"],
                "audio": {"output": {"format": {"type": "audio/pcm", "rate": 24000}, "voice": V["voice"]}}}}))
            await ws.send(json.dumps({"type": "conversation.item.create", "item": {
                "type": "message", "role": "user", "content": [{"type": "input_text", "text": text}]}}))
            await ws.send(json.dumps({"type": "response.create"}))
            async for raw in ws:
                ev = json.loads(raw); t = ev.get("type", "")
                if t == "response.output_audio.delta": pcm += base64.b64decode(ev["delta"])
                elif t == "response.output_audio_transcript.done": transcript = ev.get("transcript", "")
                elif t == "error":
                    raise RuntimeError(json.dumps(ev.get("error"))[:300])
                elif t == "response.done":
                    usage = ev["response"].get("usage"); status = ev["response"].get("status"); break
    except Exception as ex:
        ledger.settle(idx, "UNKNOWN", extra={"error": f"{type(ex).__name__}: {str(ex)[:200]}"})
        raise SystemExit(f"{line['id']}: {type(ex).__name__} {str(ex)[:200]} — stopped, not retried")
    c = cost_of(usage) if usage else None
    ledger.settle(idx, "ACK" if usage else "NO_USAGE", cost=c, usage=usage, extra={"response_status": status})
    x = np.frombuffer(bytes(pcm), dtype="<i2").astype(np.float32) / 32768
    loud = np.where(np.abs(x) > 0.01)[0]
    if len(loud): x = x[max(0, loud[0] - int(0.06 * 24000)): loud[-1] + int(0.16 * 24000)]
    (HERE / "assets" / "voice").mkdir(parents=True, exist_ok=True)
    sf.write(HERE / "assets" / "voice" / f"{line['id']}.wav", x, 24000)
    match = norm(transcript) == norm(text)
    takes[line["id"]] = {"seconds": round(len(x) / 24000, 3), "transcript": transcript, "verbatim_match": match,
                         "usage": usage, "cost_usd": c, "model": V["model"], "voice": V["voice"]}
    tf.write_text(json.dumps(takes, indent=2) + "\n")
    print(line["id"], takes[line["id"]]["seconds"], "s", "MATCH" if match else "MISMATCH: " + transcript, "cost", round(c or 0, 5))

async def main():
    for line in script["lines"]:
        if a.only and line["id"] not in a.only: continue
        await speak(line)
asyncio.run(main())
