# Pilot B (Claude lane) — "The reply disappeared" (SYNTHETIC / MOCK)

One independent ~54 s narrated, animated explainer for [Issue #16](https://github.com/amitkarpe/video-demo/issues/16).
Story: an approved fixed S3 canary policy request crosses the SDK boundary, the acknowledgement is lost,
the ledger already holds `CALLING`, AWSOps does **not** resend, the **same Run A** is reconciled read-only,
a provider `MATCH` is not fresh AWS Config compliance, freshness stays `NOT_VERIFIED`, and the film ends at `NEEDS_REVIEW`.
It never asserts `execution=SUCCEEDED` for the unresolved branch. Everything shown is a SYNTHETIC / MOCK recreation;
live acceptance is still pending ([manager#19](https://github.com/amitkarpe/manager/issues/19)).

## Files

| File | What it is |
|---|---|
| `out/claude-unknown-ack.mp4` | Final film, H.264 High 1920×1080 30 fps + AAC 48 kHz stereo, 53.73 s |
| `out/claude-unknown-ack-preview.mp4` | 20 s, 960×540 preview of the first half |
| `captions.srt`, `transcript.txt` | Generated from `script.json` + measured clip durations |
| `keyframes/01-problem.png`, `02-mechanism.png`, `03-payoff.png` | Frames extracted from the final MP4 |
| `storyboard.md`, `treatments.md` | Shot list; two reference treatments |
| `review/VERIFICATION.md` | Verification report and honest limits |
| `script.json`, `tts_openai.py`, `timing.json`, `spend-ledger.json` | Narration source, OpenAI TTS generator (metered), measured clip lengths, redacted spend ledger |
| `tts.py`, `timing.kokoro.json`, `assets/kokoro/` | Offline Kokoro fallback narration (first version; copy back to `assets/` + `timing.json` to use) |
| `src/index.template.html`, `build.py` | Editable composition source; builder (writes `index.html`, `cues.json`, SRT, transcript) |
| `assets/voice-s01..s15.wav` | Final narration clips (OpenAI `gpt-4o-mini-tts`, voice `cedar`) |
| `assets/aws-icons/*.svg` | Two unmodified official AWS Architecture Icons (S3, AWS Config) |

Edit `src/index.template.html` (not the generated `index.html`).

## Rebuild (new machine)

```bash
cd benchmarks/hyperframes && npm ci                       # hyperframes 0.9.20, gsap 3.15.0 (lockfile)
cd pilots/claude-unknown-ack
# optional: regenerate narration. PAID: OpenAI TTS needs OPENAI_API_KEY (env or --env-file), numpy, soundfile; ledger stops at --ceiling (default USD 0.50)
python3 tts_openai.py --env-file <path-to-.env>
# or free/offline fallback: python tts.py --model <kokoro-v1.0.onnx> --voices <voices-v1.0.bin>  (writes assets/kokoro/)
python3 build.py                                           # copies gsap into assets/ (gitignored), fills the template
cd ../.. && npx hyperframes check pilots/claude-unknown-ack
npx hyperframes render pilots/claude-unknown-ack -o pilots/claude-unknown-ack/out/claude-unknown-ack.mp4 -f 30 -q delivery
```

The HyperFrames compiler fetches Inter and JetBrains Mono (SIL OFL) from Google Fonts on first render and caches them.
Rendering offline needs that cache.

## Pins and provenance

- Baseline commit `995e8287847b77f81707e485f9767700bc98c162` (`feat/10-engineering-deep-dive`).
- Node v26.12.1 / npm 11.20.0 (Issue asks 22+), FFmpeg/ffprobe 9.0.2, headless Chrome from `~/.cache/hyperframes/chrome`.
- **Final narration:** OpenAI `gpt-4o-mini-tts`, voice `cedar`, WAV, via `POST /v1/audio/speech` (`tts_openai.py`; stdlib `urllib`, no SDK). **The voice is AI-generated and is disclosed on screen** (`AI-GENERATED VOICE` tag and end credit). OpenAI lists `gpt-4o-mini-tts` for shutdown on 2027-01-06; re-voice before then.
- Fallback narration: Python 3.15.2, `kokoro-onnx 0.6.1`, `soundfile 0.14.0`; voice `bm_george` (en-gb), speed 0.95.
  Model files: `kokoro-v1.0.onnx` SHA-256 `beb0d1848dee9a49da392cc3df26958d46cfa35d321edf434f52949153f0df3a`,
  `voices-v1.0.bin` SHA-256 `bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d`; `tts.py` refuses to run on a mismatch.
  Weights Apache-2.0; ONNX wrapper MIT. The weights are not committed.
- AWS Architecture Icons, package `Icon-package_07312026` (13,988,918-byte zip from `d1.awsstatic.com`), used unmodified under the
  [AWS icon terms](https://aws.amazon.com/architecture/icons/):
  `Arch_Amazon-Simple-Storage-Service_64.svg` SHA-256 `b92c5101cc6565dd12df37655802279f8fba0c719279f62f93106d26750b36c6`,
  `Arch_AWS-Config_64.svg` SHA-256 `6e6ee0b691d7ef2f71d81b508daa21dd154512a4e101ecc8113e161870bdb9a4`.
  The SQLite-style database, gate, clock, stamp and ladder shapes are custom SVG/CSS. No STS icon is used.
- Licences: HyperFrames Apache-2.0; GSAP under its [standard no-charge licence](https://gsap.com/standard-license/) (not Apache; not committed, copied from `node_modules` by `build.py`).
- Source facts verified read-only at `amitkarpe/awsops` commit `15c12fb5362dd05fc4d8aaf10ebd31d3ce2935d9`: see `review/VERIFICATION.md`.

## Effort and spend

Claude Code (model `claude-sonnet-5-5`), one fresh session. Phase 1 (read-only, no spend) produced a free Kokoro version; Phase 2 (approved by Amit in Issue #16) re-voiced it with OpenAI TTS.
Four renders in total; the last is the delivered file. One OpenAI TTS generation of 15 lines (15 calls, no retries), nothing else paid.
**`OPENAI_API_SPEND_USD` ≤ 0.12** (conservative pre-call upper bound 0.1184 from `spend-ledger.json`: 1 s/word at 100 audio tokens/s × USD 12/1M, plus generous text tokens × USD 0.60/1M). The API returns no usage counts, so this is an estimate, not an invoice;
the owner's OpenAI dashboard is authoritative (NOT_VERIFIED by Claude). Cap for this pilot: USD 5. No Claude API, other paid service, AWS call, cloud render or hosting.
The API key value was read only inside the generator process and never printed, logged or committed.
