# Nextflow Offline — Prepare Once, Run with Confidence

**Watch:** [offline-validation-r1.mp4](https://github.com/amitkarpe/video-demo/releases/download/film-nextflow-offline-offline-validation/offline-validation-r1.mp4) (sha256 `4bc740294c9a…`) — video files live on the film's [GitHub Release](https://github.com/amitkarpe/video-demo/releases/tag/film-nextflow-offline-offline-validation), not in git. Paths such as `out/*.mp4` below are where a local build writes them.


A 3 min 32 s narrated, animated explainer for managers and engineers, made by Claude as the sole video implementer, from the owner's brief in `amitkarpe/nextflow-offline` Issue #765 and the owner's direction of 9 Nov 2026.

**Story.** One release case carries a real example, a germline variant-calling test from nf-core Sarek on a small public test dataset, through one working flow:
1. **The problem:** one missing piece stops an offline run.
2. **GitLab:** the single trusted home for code, container images and datasets, scanned for security.
3. **Prepare:** a GitLab Runner prepares the release into AWS CodeCommit, private Amazon ECR and one fingerprinted bundle in Amazon S3.
4. **Verify:** everything is read back and compared before the release is registered.
5. **Run:** an approved run request starts a controlled run through ten gated stages in AWS CodePipeline, on a private EC2 host with no internet route.
6. **Offline:** exact images in an isolated store; Nextflow in offline mode; no network and no downloads.
7. **Proof:** a clear PASS or FAIL with an evidence report.

It closes on: *Prepare once. Verify everything. Run with confidence.*

The language is deliberately high-level (owner direction). The film shows no code, scripts, file names, IDs or dates, and GitLab is the only repository service named. `CLAIMS.md` maps every statement to the source revision and marks the owner-direction statements for reviewers.

## Files

| Path | What it is |
|---|---|
| `out/offline-validation-r1.mp4` | Final film: H.264 High 1920×1080 30 fps, AAC-LC 48 kHz stereo, 3 min 32 s, 80.9 MB, −16.0 LUFS |
| `captions.srt`, `transcript.txt`, `cues.json` | Captions and transcript timed from the measured post-edit narration |
| `keyframes/*.png` | Frames taken from the final MP4 |
| `CLAIMS.md` | Evidence map: each statement, its state and its source at the pinned revision |
| `review/VERIFICATION.md` | QA record: decode, playback, motion, 720p, captions, audio, OpenAI QA dispositions, spend, usage |
| `review/qa/*.jpg`, `review/qa-*.json` | 1280×720 frames from the final file and the OpenAI vision/transcription outputs |
| `storyboard.md` | Shot list and design rationale |
| `src/index.template.html` | Editable composition (HyperFrames + GSAP). Every label, service name and check is code |
| `build.py` | Writes cues, SRT, transcript, `index.html` and `assets/mix.wav` (voice + synthesized score and effects, loudness-normalised). No network |
| `script.json` | Narration, chapters and voice settings |
| `prompts/images.json`, `prompts/image-provenance.json` | Exact image prompts and settings; usage, cost, request ID and prompt/output SHA-256 per image |
| `media/original/**` | **Immutable provider originals**, bytes exactly as returned. Re-takes are new files, never overwrites |
| `media/derived/**`, `media/manifest.json` | Crops, JPEGs and trimmed narration rebuilt from the selected originals; hashes and derivation steps |
| `voice-takes.json`, `spend-ledger.json` | Per-take provider transcript, usage and cost; every paid OpenAI request |
| `../../../toolkit/` | Shared `ledger.py`, `media.py`, `gen_images.py` (generations and reference edits), `narrate_realtime.py`, `derive.py`, `qa_vision.py` (this film's rules: `review/qa-rules.md`), `qa_transcribe.py`. The film-specific frame list that the original `qa_frames.sh` used is in Git history (PR #31) |

## Rebuild (no paid API)
From the repository root (one shared toolchain; see the root README):
```bash
npm ci                                   # HyperFrames + GSAP, pinned; copies gsap.min.js into every film
python3 -m venv .venv && .venv/bin/pip install numpy==2.5.4 soundfile==0.14.0 pillow==13.0.0
cd films/nextflow-offline/offline-validation
../../../.venv/bin/python ../../../toolkit/derive.py && ../../../.venv/bin/python build.py
cd ../../.. && npx hyperframes check films/nextflow-offline/offline-validation
npx hyperframes render films/nextflow-offline/offline-validation -o films/nextflow-offline/offline-validation/out/master-delivery.mp4 -f 30 -q delivery
cd films/nextflow-offline/offline-validation && ../../../toolkit/finalize.sh && ../../../toolkit/qa_frames.sh
```
Toolkit commands (`toolkit/*.py`) run from this folder; paid ones (`narrate_realtime.py`, `gen_images.py`, `qa_transcribe.py`, `qa_vision.py`) take `--env-file` and stop at 90% of this film's cap (`spend-ledger.json`).

`out/master-delivery.mp4` (above GitHub's 100 MB file limit), `assets/mix.wav` and `assets/gsap.min.js` are build outputs and are gitignored.

**Optional, paid:** regenerate media with `OPENAI_API_KEY` in the environment (or `--env-file <ignored .env>`). Each call reserves its cost in `spend-ledger.json` first, and a rerun adds a new take instead of overwriting.

## Pins and provenance

- **Technical source:** `amitkarpe/nextflow-offline` @ `356ed30f322a109788ca68f352961a33a7bba046` (private, read-only), plus the owner's direction. Nothing was run against it: no pipeline, cloud, scan or worker action.
- **Base:** `feat/10-engineering-deep-dive` @ `995e8287847b77f81707e485f9767700bc98c162`, the production base used by earlier films. This folder is self-contained.
- **Toolchain (executed):** macOS, Node v26.12.1, HyperFrames 0.9.20, GSAP 3.15.0, FFmpeg 9.0.2, Python 3.12 (venv), numpy 2.5.4, soundfile 0.14.0, websockets 15.0.1, Pillow 13.0.0.
- **Images:** OpenAI `gpt-image-2.6-sunburst`, quality `high`.
  - Seven 2048×1152 plates: corridor, GitLab workshop, workbench, inspection bay, ten-arch bridge, sealed lab, dawn.
  - Three transparent sprites: the release case, the open case and a container. The open case is a reference edit of the closed case, so the object stays the same.
  - The prompts forbid text, logos and symbols. Service names and tiles are drawn in code; no logos are used.
- **Voice:** OpenAI `gpt-realtime-2.1` (Realtime API over WebSocket), voice `marin`, PCM 24 kHz, one session per line, with verbatim-reading and pronunciation instructions. Disclosed on screen and in the credits.
- **Score and effects:** synthesized in `build.py` with numpy from a fixed seed. No samples or third-party audio.
- **Fonts:** system fonts with fallbacks. No font files are committed.

## Spend (OpenAI, this film)

USD **1.03** committed over 42 requests, all ACK, with no retries and no uncertain charges. The owner set no budget limit; see `review/VERIFICATION.md` §7.
