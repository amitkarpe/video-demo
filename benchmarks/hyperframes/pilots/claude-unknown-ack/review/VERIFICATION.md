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
- `out/claude-unknown-ack.mp4`: 14,393,806 bytes (13.7 MiB), SHA-256 `e96384b9c60bba01d5ab2ad73646889ba037007e142caeac33f511cba309e9a6`.
- ffprobe: H.264 High, yuv420p, **1920×1080**, 30 fps, 53.733 s; AAC LC 48 kHz stereo, 53.733 s. Audio levels: mean −23.5 dB, peak −2.9 dB (`volumedetect`).
- `out/claude-unknown-ack-preview.mp4`: 751,263 bytes, 960×540, 20.0 s (4–24 s of the film), SHA-256 `ac02ce4dff15f205786dc18b5b7be6aa7b03d225fe2b49b05508e77dbcf8b31e`.
- **Full decode:** `ffmpeg -v error -i <file> -f null -` → no errors, exit 0 (both files).
- **Changing frames:** `mpdecimate` keeps 730 of 1,612 frames (the rest are exact repeats, i.e. deliberate holds between steps). Visual changes land on each narration line (contact sheet reviewed at 3, 14, 22, 30, 37, 46 s).
- **Playback:** the final file opened in QuickTime Player (AppleScript), reported duration 53.73 s and advanced during playback (0 → 2.75 s). Picture/sound output itself is not observable by Claude; see §6.
- Audio/video sync: `silencedetect` speech onsets are within ~0.06 s of planned cues (s01 1.31 s vs 1.30 s, s02 5.43 s vs 5.39 s, s09 26.98 s vs 26.97 s).

## 4. HyperFrames checks (VERIFIED)
`npx hyperframes check` on the final composition: **0 errors**. Remaining warnings: `escaped_container` notes on the scaled evidence ladder (coordinates look correct in rendered frames), and a type-floor note on secondary mono labels (smallest in-scene text 21 px; credit line marked texture).
All 151 text/contrast checks pass WCAG AA. Lint ran clean after moving to transform-based motion.

## 5. Captions at 1280×720 (VERIFIED by viewing)
Frames scaled to 1280×720 (`review/frame-720p-s06.jpg`, `-s09.jpg`, `-s09b.jpg`, `-s14.jpg`) show the 41 px caption (≈27 px at 720p) on a dark box, one line for every caption except the two-line `NEEDS_REVIEW` caption. All essential values (`UNKNOWN`, `MATCH`, `NOT_VERIFIED`, `NEEDS_REVIEW`) are ≥ 27 px at 720p. Small mono labels (SDK BOUNDARY, ledger sub-title) are context only, not required to follow the story. Judge legibility yourself on a laptop screen: that is part of the scorecard.

## 6. Narration — **NOT_VERIFIED by a human ear**
Claude cannot hear audio. A human has not yet listened to the final file.
Machine diagnostic only (faster-whisper `base.en` on the final MP4 audio): all 15 lines are transcribed correctly, including `SQLite`, `AWS Ops`, `S3` and `AWS Config`; the only miss is the homophone "write" → "right" in line 7.
Voice: OpenAI `gpt-4o-mini-tts`, `cedar`, with a calm-engineer style instruction; spoken forms use `speak_openai` in `script.json` (`SQLite`, `AWS Ops`, `S3`, `CALLING`, `NEEDS REVIEW`). Captions use the written forms.
**The voice is AI-generated; the film says so on screen (pill-style tag top right, plus end credit).**
**Please listen once for pronunciation and naturalness, especially AWS Ops, SQLite, S3, CALLING and NEEDS_REVIEW, and compare with the Kokoro fallback if you prefer an offline voice.**

## 7. Dependencies (VERIFIED) — see README "Pins"
hyperframes 0.9.20, gsap 3.15.0, FFmpeg 9.0.2, Node v26.12.1, Python 3.15.2 (build), OpenAI `gpt-4o-mini-tts` (final voice; shutdown listed 2027-01-06). Fallback: kokoro-onnx 0.6.1, soundfile 0.14.0; model SHA-256 checked by `tts.py`.

## 8. Factual limits
- SYNTHETIC / MOCK walkthrough only; real acceptance is pending (manager#19). The film says so on screen and in the last line.
- Narration ≈ 44.2 s of speech in a 53.7 s film; the Issue asks ≈ 45–60 s.
- Icons: only unmodified S3 and AWS Config icons from the AWS Architecture Icons package; custom shapes elsewhere.

## 9. Spend and effort
`OPENAI_API_SPEND_USD` **≤ 0.12** (estimated upper bound 0.1184, itemized per call in `spend-ledger.json`; 15 `gpt-4o-mini-tts` calls, all ACK, no retries). The API returns no usage counts, so this is a conservative estimate; the owner's dashboard is authoritative and was not checked by Claude (NOT_VERIFIED). Pilot cap USD 5 (shared cap USD 10): not approached.
No Claude API, other paid service, AWS operation, cloud render or external hosting. Key never printed or committed.
Local effort: Phase 1 free Kokoro build (≈4 narration generations, 3 snapshot rounds, 2 renders), Phase 2 one OpenAI narration, 2 renders. Agent: Claude Code, `claude-sonnet-5-5`.
