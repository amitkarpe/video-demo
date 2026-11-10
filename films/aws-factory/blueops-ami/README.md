# Round 3 — "BlueOps: the AMI Factory" (ILLUSTRATIVE)

**Watch:** [blueops-ami-preview.mp4](https://github.com/amitkarpe/video-demo/releases/download/film-aws-factory-blueops-ami/blueops-ami-preview.mp4) (sha256 `2f2f4666f1aa…`) · [blueops-ami.mp4](https://github.com/amitkarpe/video-demo/releases/download/film-aws-factory-blueops-ami/blueops-ami.mp4) (sha256 `89f7551fdc11…`) — video files live on the film's [GitHub Release](https://github.com/amitkarpe/video-demo/releases/tag/film-aws-factory-blueops-ami), not in git. Paths such as `out/*.mp4` below are where a local build writes them.


A 3 min 56 s narrated, animated explainer for [Issue #23](https://github.com/amitkarpe/video-demo/issues/23).

The story runs from the GovTech/GCC Golden Amazon Linux 2023 image, through the **Hardened Base OS** and exactly three production families (GitLab, MongoDB, CloudOS ECS Worker), to DEV proving grounds and a human-approved Phase A rollout. It ends with a clearly labelled **proposed** Phase B monthly auto-promotion.

The payoff line is "Build once. Validate every workload. Promote only what is proven."

Everything is illustrative. There are no real IDs, no AWS call and no live run.

## Files

| Path | What it is |
|---|---|
| `out/blueops-ami.mp4` | Final film: H.264 High 1920×1080 30 fps, AAC 48 kHz stereo, 236.3 s, 60.2 MB (web encode, CRF 20) |
| `out/blueops-ami-preview.mp4` | 30 s preview at 960×540 (three families → DEV proving grounds) |
| `captions.srt`, `transcript.txt` | Built from `script.json` and the measured clip lengths |
| `keyframes/01..05-*.png` | Five frames taken from the final MP4: hook, families, DEV gates, Phase A approval, payoff |
| `storyboard.md`, `RATIONALE.md` | Shot list; creative decisions and the alternatives considered |
| `review/VERIFICATION.md` | Claims vs. source, encode/decode/playback, 720p frames, OpenAI QA, spend, timing, self-evaluation |
| `review/qa/*.jpg`, `review/qa-*.json` | 720p frames and the OpenAI vision/transcription QA outputs |
| `src/index.template.html` | Editable composition (HyperFrames + GSAP). All labels, gates, states and diagrams are code |
| `build.py` | Writes cues, SRT, transcript, `assets/mix.wav` (voice + synthesized score + SFX) and `index.html`. No network |
| `script.json` | Narration lines, chapters, and the voice settings and instructions |
| `prompts/images.json`, `prompts/image-provenance.json` | Exact image prompts and settings; usage, cost, prompt/output SHA-256 for each image |
| `assets/gen/*.png` | **Original OpenAI `gpt-image-2.6-sunburst` outputs**, unmodified (7 images) |
| `assets/sprites/*` | Derived crops/scales/JPEGs of those outputs, used in the film |
| `assets/voice-raw/*.wav` | Cached OpenAI Realtime narration takes (`gpt-realtime-2.1`, voice `marin`) |
| `assets/voice/*.wav`, `timing.json` | The same takes with long internal pauses capped at 0.42 s (`tools/tighten.py`) |
| `voice-takes.json` | Per-line transcript returned by Realtime, verbatim-match flag, usage, cost |
| `spend-ledger.json` | Every paid OpenAI request: reservation, settled cost from returned usage, status |
| `tools/` | `ledger.py`, `gen_images.py`, `narrate_realtime.py`, `tighten.py`, `qa_vision.py`, `qa_transcribe.py` |

## Rebuild from cached outputs (no paid API)

```bash
cd benchmarks/hyperframes && npm ci                    # hyperframes 0.9.20, gsap 3.15.0 (lockfile)
cd pilots/blueops-ami
python -m venv .venv && .venv/bin/pip install numpy==2.5.4 soundfile==0.14.0
.venv/bin/python build.py                              # cues, SRT, transcript, assets/mix.wav, index.html
cd ../.. && npx hyperframes check pilots/blueops-ami
npx hyperframes render pilots/blueops-ami -o pilots/blueops-ami/out/master-delivery.mp4 -f 30 -q delivery
cd pilots/blueops-ami
ffmpeg -i out/master-delivery.mp4 -c:v libx264 -preset slow -crf 20 -profile:v high -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart out/blueops-ami.mp4
```

`assets/mix.wav`, `assets/gsap.min.js` and `out/master-delivery.mp4` (≈150 MB, above GitHub's 100 MB file limit) are build outputs and are gitignored.

**Optional, paid:** regenerate assets with `OPENAI_API_KEY` set in the environment (or passed with `--env-file`). Every call reserves its cost in `spend-ledger.json` first, and the tools stop at USD 9.00.

```bash
python3 tools/gen_images.py --env-file <.env> [--only hero_factory]   # gpt-image-2.6-sunburst
.venv/bin/pip install websockets==15.0.1
.venv/bin/python tools/narrate_realtime.py --env-file <.env> [--only s01]  # gpt-realtime-2.1 over WebSocket
cp assets/voice/*.wav assets/voice-raw/ && .venv/bin/python tools/tighten.py
```

## Pins and provenance

- **Base:** `feat/10-engineering-deep-dive` @ `995e8287847b77f81707e485f9767700bc98c162` (verified).
- **Toolchain:** Node v26.12.1, FFmpeg 9.0.2, HyperFrames 0.9.20, GSAP 3.15.0, Python 3.12.16, numpy 2.5.4, soundfile 0.14.0, websockets 15.0.1.
- **Images:** OpenAI `gpt-image-2.6-sunburst` via `POST /v1/images/generations` (6 images) and `POST /v1/images/edits` (1 image, `hardened_core` edited from `golden_core`). Quality `high`. The prompts forbid text and logos.
  - Every precise label, AWS term, gate and diagram line in the film is deterministic HTML/SVG, not generated lettering.
  - Derived sprites are crops, scales or JPEG conversions only.
  - Licence: per OpenAI's terms, outputs belong to the user. The film discloses that the art is AI-generated.
- **Voice:** OpenAI `gpt-realtime-2.1` (Realtime API, `wss://api.openai.com/v1/realtime`), voice `marin`, PCM 24 kHz, one session per line, with instructions to read verbatim.
  - All 40 takes matched the script word for word, per the Realtime output transcript.
  - Realtime is OpenAI's documented replacement for the Speech API models deprecated for 2027-01-06.
  - The film discloses the synthetic voice on screen (`AI VOICE · AI ART` tag and end credit).
- **Score and SFX:** synthesized in `build.py` with numpy from a fixed seed. No samples.
- **Technical source:** read-only `amitkarpe/ami-factory` @ `2cfd64667a93b8183f574da30f86c39af7089dcb`, with paraphrased claims only. No private IDs, accounts, VPCs, AMIs, code or document text are reproduced.

## Spend (OpenAI, this lane)

USD **1.087** committed of the USD 10.00 cap, so **USD 8.91 remains**. Settled from returned usage, all 51 requests ACK:

- images: 7 requests, USD 0.319
- Realtime narration: 40 requests, USD 0.371
- `gpt-5.5` vision QA: 2 requests, USD 0.361
- `gpt-transcribe` QA: 2 requests, USD 0.036

Details are in `review/VERIFICATION.md` §6. Your OpenAI dashboard is authoritative. The API key was never printed, logged or committed.
