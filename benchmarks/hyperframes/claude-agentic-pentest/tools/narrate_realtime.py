#!/usr/bin/env python3
"""Narrate script.json lines with the OpenAI Realtime API (WebSocket), metered.
One short session per line; usage from response.done is settled into spend-ledger.json.
  .venv/bin/python tools/narrate_realtime.py --env-file <.env> [--only s01 s02]
The returned PCM (s16le, 24 kHz, mono) is saved UNCHANGED (WAV container only) to
media/original/voice/<id>.t<N>.wav before anything else. A rerun adds a new take and never
overwrites an earlier one. Trimming happens later in tools/derive.py.
voice-takes.json keeps the per-take provider transcript, verbatim flag, usage and cost."""
import argparse, asyncio, base64, io, json, pathlib, re, sys, wave
import websockets
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import ledger, media
HERE = pathlib.Path(__file__).resolve().parent.parent
# gpt-realtime-2.1 published USD/token rates (reviewed 2026-11-08)
PRICE = {"text_in": 4/1e6, "audio_in": 32/1e6, "cached_in": 0.4/1e6, "text_out": 24/1e6, "audio_out": 64/1e6}
ap = argparse.ArgumentParser(); ap.add_argument("--env-file"); ap.add_argument("--only", nargs="*")
a = ap.parse_args()
script = json.loads((HERE / "script.json").read_text()); V = script["voice"]
key = ledger.api_key(a.env_file)
tf = HERE / "voice-takes.json"; takes = json.loads(tf.read_text()) if tf.exists() else {}
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", re.sub(r"[-–—]", " ", s.lower())).split()

def cost_of(u):
    i = u.get("input_token_details", {}) or {}; o = u.get("output_token_details", {}) or {}
    return ((i.get("text_tokens", 0) or 0) * PRICE["text_in"] + (i.get("audio_tokens", 0) or 0) * PRICE["audio_in"]
            + (i.get("cached_tokens", 0) or 0) * PRICE["cached_in"] + (o.get("text_tokens", 0) or 0) * PRICE["text_out"]
            + (o.get("audio_tokens", 0) or 0) * PRICE["audio_out"])

def wav_bytes(pcm: bytes) -> bytes:
    b = io.BytesIO()
    with wave.open(b, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
    return b.getvalue()

async def speak(line):
    text = line.get("say", line["caption"])
    # reserve: instructions + text in, transcript text out, ~1 s of audio per 2.3 words at ~10 audio tokens/s, x2 headroom
    est = 700 * PRICE["text_in"] + 300 * PRICE["text_out"] + max(10, len(text.split())) * 0.45 * 2 * 10 * PRICE["audio_out"] * 4
    idx = ledger.reserve("realtime (wss)", V["model"], est, "voice:" + line["id"])
    pcm, transcript, usage, status, rid = bytearray(), "", None, None, None
    try:
        async with asyncio.timeout(180), websockets.connect(f"wss://api.openai.com/v1/realtime?model={V['model']}",
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
                elif t == "error": raise RuntimeError(json.dumps(ev.get("error"))[:300])
                elif t == "response.done":
                    r = ev["response"]; usage = r.get("usage"); status = r.get("status"); rid = r.get("id"); break
    except Exception as ex:
        ledger.settle(idx, "UNKNOWN", extra={"error": f"{type(ex).__name__}: {str(ex)[:200]}", "partial_audio_bytes": len(pcm)})
        raise SystemExit(f"{line['id']}: {type(ex).__name__} {str(ex)[:200]} — stopped, not retried")
    c = cost_of(usage) if usage else None
    if not pcm:
        ledger.settle(idx, "NO_AUDIO", cost=c, usage=usage, extra={"response_status": status, "response_id": rid})
        raise SystemExit(f"{line['id']}: no audio returned (status {status})")
    path, take = media.write_original("voice", line["id"], "wav", wav_bytes(bytes(pcm)),
                                      {"model": V["model"], "voice": V["voice"], "response_id": rid,
                                       "format": "pcm s16le 24000 Hz mono as returned; WAV header only"})
    ledger.settle(idx, "ACK" if usage else "NO_USAGE", cost=c, usage=usage,
                  extra={"response_status": status, "response_id": rid, "output": str(path.relative_to(HERE))})
    match = norm(transcript) == norm(text)
    takes[f"{line['id']}.{take}"] = {"seconds_raw": round(len(pcm) / 2 / 24000, 3), "provider_transcript": transcript,
                                     "provider_verbatim_match": match, "usage": usage, "cost_usd": c,
                                     "model": V["model"], "voice": V["voice"], "response_status": status}
    tf.write_text(json.dumps(takes, indent=2, ensure_ascii=False) + "\n")
    print(line["id"], take, takes[f"{line['id']}.{take}"]["seconds_raw"], "s", "MATCH" if match else "MISMATCH: " + transcript, "cost", round(c or 0, 5))

async def main():
    for line in script["lines"]:
        if a.only and line["id"] not in a.only: continue
        await speak(line)
asyncio.run(main())
