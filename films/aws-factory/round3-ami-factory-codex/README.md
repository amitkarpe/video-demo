# BlueOps — The Trust Factory

**Watch:** [blueops-trust-factory.mp4](https://github.com/amitkarpe/video-demo/releases/download/film-aws-factory-round3-ami-factory-codex/blueops-trust-factory.mp4) (sha256 `3e01ae8dd0e6…`) — video files live on the film's [GitHub Release](https://github.com/amitkarpe/video-demo/releases/tag/film-aws-factory-round3-ami-factory-codex), not in git. Paths such as `out/*.mp4` below are where a local build writes them.


A 4:28 illustrated factory film for [Round 3 / issue #24](https://github.com/amitkarpe/video-demo/issues/24). It follows a golden AL2023 image through a package-only shared base, three workload families, DEV proof, separate PROD acceptance, human approval, a proposed future release policy, and recovery.

[Play or download the MP4](https://raw.githubusercontent.com/amitkarpe/video-demo/feat/round3-codex-blueops-ami/benchmarks/hyperframes/pilots/round3-codex-blueops-ami/blueops-trust-factory.mp4)

The film is an original visual simulation. It performs no AWS operations and claims no live deployment evidence. OpenAI-generated Cedar narration and generated artwork are disclosed in the film. **AUDIBLE_REVIEW=NOT_VERIFIED**: automated transcription and playback checks do not replace human listening or creative acceptance.

## Deliverables

- `blueops-trust-factory.mp4`: 1920×1080, 30 fps, H.264/AAC, burned-in captions.
- `player.html`: local review player; `captions.srt` and `transcript.txt`: accessible companion files.
- `scene.html.template`, `index.html`, `script.json`, `timing.json`, `build.py`: editable, seekable composition and original sound synthesis.
- `assets/factory-day.png`, `assets/factory-night.png`: original Images API output and continuity edit; `prompts/`: exact image prompts.
- `assets/voice-00.wav` through `voice-25.wav`: the original cached Speech API output, before mixing.
- `keyframes/`: five actual final-film frames. `evidence/`: technical measurements and reviewed draft frames.
- `STORYBOARD.md`, `SOURCES.md`, `EVIDENCE.md`, `PROVENANCE.md`: rationale, claim boundaries, review and asset rights.
- `api-spend.json`, `run-metrics.json`: request-level receipts and separate agent inference counters. No credentials are included.

## Rebuild with no paid API

Requirements: Python 3, Node/npm, FFmpeg/FFprobe, the repository's pinned HyperFrames/GSAP dependencies, and HyperFrames-managed Chrome. Tested with Node 26.12.1, FFmpeg 9.0.2, HyperFrames 0.9.20 and GSAP 3.15.0. Run from this directory:

```sh
bash render.sh
```

`render.sh` installs the pinned npm dependencies only if absent, ensures the renderer browser (a first run may download Chrome), copies the local GSAP runtime, reconstructs narration from cached WAVs, rebuilds captions and the original score, renders, normalizes audio, and fully decodes the result. It does not read an API key or invoke any media API. Set `WORKERS=2` on a smaller machine. Cached synthesis is deterministic; encoded bytes can differ across browser, font and codec builds.

For local review:

```sh
python3 -m http.server 8774 --bind 127.0.0.1
```

Open `http://127.0.0.1:8774/player.html`. The server is local only; no hosting service is created. The direct MP4 also plays in a normal media player.

`python3 verify.py` checks the final container, complete decoding, caption bounds, cached-asset hashes, ledger completion and budget. It saves measurements and five keyframes. `python3 check_budget.py` exercises near-cap and uncertain-request admission without network calls.

## Optional API regeneration

Ordinary rebuilds must use the cache. API tools require explicit `--approved-issue-24`, an existing `OPENAI_API_KEY` in the process environment, and the isolated dependencies in `requirements-api.lock`. Do not commit an environment file. `generate_image.py` uses the unchanged Codex imagegen CLI from the operator's installed skill; `generate_voice.py`, `transcribe.py`, `check_pronunciation.py` and `vision_review.py` record their own request receipts.

Run paid commands serially. The production ledger is append-only by convention; it is not a concurrent billing service. Existing completed names and uncertain/reserved calls stop new admissions. Do not erase receipts, overwrite cached outputs or replay uncertain requests to regenerate this deliverable. A future revision needs its own explicitly approved accounting scope.

All 31 paid requests completed. Usage-priced incremental media/QA cost: **$0.2083537**, with **$9.7916463** of the $10 lane allowance unused. These are returned-usage calculations, not a provider invoice. Agent subscription inference is separate and its cost is unavailable. See the detailed report for limitations and counter capture time.
