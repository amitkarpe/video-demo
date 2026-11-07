# Voice Lab — local Mac test

Read [the API credit and authentication guide](../docs/OPENAI_API_VOICE_LAB.md) first.

**Prerequisites:** macOS, Node.js 22+, an OpenAI API key from the linked **Personal Platform organization**, set as the local process environment variable `OPENAI_API_KEY` through a secure local method (e.g. macOS Keychain). **Do not paste API keys in repository files, shell scripts, PRs or chat.**

To launch from repository root: `node voice-lab/server.mjs`. Open **http://127.0.0.1:8787** and click Connect then Speak. The server listens only on 127.0.0.1; browser gets an ephemeral client credential, never the project API key. One session is allowed per server start; voice disconnects at 60 seconds. The script is for a **MOCK** EC2 workflow; no real AWS access.

**Validation:** `node --check voice-lab/server.mjs` first. A successful syntax check does not verify WebRTC, playback, rate limits or billing. On Mac, connect once, listen to the narrated sample and check [API Usage](https://platform.openai.com/usage). If the browser/Realtime model rejects this session shape, compare with the current [WebRTC official guide](https://developers.openai.com/api/docs/guides/voice-webrtc) and make the smallest correction before another attempt.

**Billing:** OpenAI Realtime is metered. The 7 Nov $61 grant expires on 23 Nov 2026. Auto-reload should remain OFF. Never buy credits or change billing settings as part of this lab.

**Editing boundary:** This is separate from draft PR #2's local-video implementation; do not overwrite that work.
