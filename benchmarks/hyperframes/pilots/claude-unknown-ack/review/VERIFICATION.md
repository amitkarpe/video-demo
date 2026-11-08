# Verification report — Pilot B (Claude lane)

Status key: **VERIFIED** (measured here), **NOT_VERIFIED** (not done or not possible here).
A mechanical pass is not owner creative acceptance. The owner scores the A/B pair.

## 1. Revision
- Baseline: `feat/10-engineering-deep-dive` @ `995e8287847b77f81707e485f9767700bc98c162`. Pilot branch: `feat/pilot-claude-unknown-ack`; the pilot commit is the PR head (a file cannot name its own hash).
- Source repo read-only: `amitkarpe/awsops` @ `15c12fb5362dd05fc4d8aaf10ebd31d3ce2935d9`.

## 2. Claims checked against source (VERIFIED by reading code at the pinned commit)
| On-screen / spoken claim | Source |
|---|---|
| A one-time approval decision is consumed before any provider call | `docs/current/S3_CANARY_ADAPTER.md` ("SQLite commits the one-time decision before any provider call") |
| Ledger is a private SQLite file with `synchronous=FULL`; states INTENT → CALLING → ACK/REFUSED | `src/awsops/execution/s3_canary.py` (`CanaryAdapter` ledger, `PRAGMA synchronous=FULL`, `operations` table) |
| `CALLING` is committed *before* the SDK call; an exception after the claim leaves `CALLING` and is never replayed | `s3_canary.py` `_attempt()` / `before_call()`; adapter doc ("A CALLING state with uncertain acknowledgment is retained and never replayed") |
| Reconcile reads back the **same run** and never rewrites | `s3_canary.py` `reconcile()`; adapter doc ("`reconcile` … reads back the SAME run, never rewrites") |
| Provider `MATCH` does not imply Config compliance: compliance `UNKNOWN`, freshness `NOT_VERIFIED`, run `NEEDS_REVIEW`; no Config call occurs | adapter doc ("Provider MATCH does not imply Config compliance convergence …No Config call occurs") |
| Execution stays `UNKNOWN` while the operation is `CALLING` | `s3_canary.py` reconcile path (execution not upgraded without ACK) |
| Fixed policy: deny `s3:*` on the bucket and objects when `aws:SecureTransport` is false | fixed policy in `s3_canary.py`; SDK calls `put_bucket_policy` / `get_bucket_policy` in `boto3_s3_canary.py` |
| MOCK public alias `mock-a`, resource `resource-disposable-s3-canary`, region `ap-southeast-1`, provenance SYNTHETIC; writes are counted as attempts | adapter doc ("Fake providers use MOCK … `mock-a`"; "Write counts conservatively count attempted calls") |

Deliberate simplifications (not falsehoods): the animation draws a single policy step, not the four-step setup sequence; the run id `run-canary-3f9c…` is invented and labelled SYNTHETIC ID;
"NO RESEND" illustrates the rule that an uncertain `CALLING` row is never replayed, not a literal code path with that name.
Not claimed: live acceptance, a real AWS call, fresh Config compliance, `execution=SUCCEEDED` for the lost-reply branch, deployed AgentCore2 integration.

## 3. File / encoding (VERIFIED)
- `out/claude-unknown-ack.mp4`: 15,131,083 bytes (14.4 MiB), SHA-256 `ae62a0100421214da3a28a248cc1a239a86d77568af558d77103de3b714fa8b1`.
- ffprobe: H.264 High, yuv420p, **1920×1080**, 30 fps, 57.633 s; AAC LC 48 kHz stereo, 57.633 s. Audio levels: mean −23.1 dB, peak −5.4 dB (`volumedetect`).
- `out/claude-unknown-ack-preview.mp4`: 865,762 bytes, 960×540, 20.0 s, SHA-256 `d0d0991b18350aa342a279e5bc7f9aa5a39c9adcb9c01dce9ead3a23388f5070`.
- **Full decode:** `ffmpeg -v error -i out/claude-unknown-ack.mp4 -f null -` → no errors, exit 0 (both files).
- **Playback:** opened in QuickTime Player on macOS; it loaded, played and advanced (5.8 s → 14.7 s → seek 34.2 s) with picture and sound track present. VERIFIED for opening and playing; see §5 for audibility.
- **Changing frames:** the scene-score filter flagged 1,434 of 1,728 encoded frames as different from the previous frame (the rest are deliberate holds, e.g. the 1.1 s silent beat, final stamp). The film never freezes for more than a few seconds; the visual changes land on every narration line.
- Audio/video sync: `silencedetect` shows speech onsets within ~0.05 s of the planned cues (e.g. s01 1.34 s vs 1.30 s, s02 6.20 s vs 6.16 s, s15 52.26 s vs 52.22 s).

## 4. HyperFrames checks (VERIFIED)
`npx hyperframes check` on the final composition: **0 errors**. Remaining warnings: three `escaped_container` notes on the scaled evidence ladder (coordinates look correct in rendered frames), and a type-floor note on secondary labels (smallest in-scene text 21 px, mono technical labels, plus the 17 px AWS-icon credit marked texture).
All 151 text/contrast checks pass WCAG AA. Lint ran clean after moving to transform-based motion.

## 5. Captions at 1280×720 (VERIFIED by viewing)
Frames scaled to 1280×720 (`review/frame-720p-s06.jpg`, `-s09.jpg`, `-s09b.jpg`, `-s14.jpg`) show the 41 px caption (≈27 px at 720p) on a dark box, one line for every caption except the two-line `NEEDS_REVIEW` caption. All essential values (`UNKNOWN`, `MATCH`, `NOT_VERIFIED`, `NEEDS_REVIEW`) are ≥ 27 px at 720p. Small mono labels (SDK BOUNDARY, ledger sub-title) are context only, not required to follow the story. Judge legibility yourself on a laptop screen: that is part of the scorecard.

## 6. Narration — **NOT_VERIFIED by a human ear**
Claude cannot hear audio. A human has not yet listened to the final file.
Machine diagnostic only (faster-whisper `base.en` on the final MP4 audio): all 15 lines were transcribed correctly except the expected ASR confusions
"SQLite" → "SQ light", "AWSOps" → "a WS ops" and the homophone "write" → "right". Spoken forms were tuned with spelled-out text
(`S Q Lite`, `A W S Ops`, `S three`, `calling`, `needs review`) in `script.json` `speak`. Voice: Kokoro `bm_george`, speed 0.95.
**Please listen once for pronunciation and naturalness, especially AWSOps, SQLite, S3, Config, CALLING and NEEDS_REVIEW.**

## 7. Dependencies (VERIFIED) — see README "Pins"
hyperframes 0.9.20, gsap 3.15.0, FFmpeg 9.0.2, Node v26.12.1, Python 3.15.2, kokoro-onnx 0.6.1, soundfile 0.14.0; model SHA-256 checked by `tts.py`.

## 8. Factual limits
- SYNTHETIC / MOCK walkthrough only; real acceptance is pending (manager#19). The film says so on screen and in the last line.
- Narration length ≈ 48.1 s of speech in a 57.6 s film; the Issue asks ≈ 45–60 s.
- Icons: only unmodified S3 and AWS Config icons from the AWS Architecture Icons package; custom shapes elsewhere.

## 9. Spend and effort
Actual extra spend **USD 0**. No paid API, no OpenAI/Anthropic API call from the pipeline, no AWS operation, no cloud render, no external hosting.
Local effort: ~4 narration generations, 3 snapshot-review rounds, 2 full renders (~40 s each). Agent: Claude Code, `claude-sonnet-5-5`.
