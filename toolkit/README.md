# Toolkit — one shared copy of the film scripts

Run every command **from inside a film folder** (`films/<source-repo>/<film>/`, the one with `script.json`), or set `FILM=<path>`. `T=../../../toolkit` and `PY=../../../.venv/bin/python` below.

| Step | Command | Paid? | What it does |
|---|---|---|---|
| Start a film | `python3 toolkit/new_film.py --repo <repo> --slug <film> --style toy-world-3d` (from the repo root) | no | Copies a house look's kit and writes the skeleton files |
| Voice | `$PY $T/narrate_realtime.py --env-file <.env> [--only s01 s02]` | yes | OpenAI Realtime narration, one take per line; the original is saved untouched and the provider transcript must match the script |
| Images | `$PY $T/gen_images.py --env-file <.env> [--only id]` | yes | Generations and reference edits from `prompts/images.json`; originals immutable |
| Derive | `$PY $T/derive.py` | no | Trims voice, crops sprites, writes `timing.json` and the manifest derivations |
| Build | `$PY build.py` | no | The film's score and effects plus `av.py`: cues, captions, transcript, −16 LUFS mix, `index.html` |
| Render | `npx hyperframes render <film-dir> -o <film-dir>/out/master-delivery.mp4 -f 30 -q delivery` (from the repo root) | no | About 60 s for 3 minutes of 3D on a hardware GPU |
| Finalize | `$T/finalize.sh` | no | Web MP4 `out/<film>.mp4` (H.264 CRF 20, AAC 192k) |
| QA frames | `$T/qa_frames.sh` | no | One 720p frame per line (`review/qa/`), one keyframe per chapter |
| Transcribe QA | `$PY $T/qa_transcribe.py --env-file <.env> --audio assets/mix.wav --minutes <m> --out review/qa-transcribe.json` | yes | WER of the final mix against the script |
| Vision QA | `$PY $T/qa_vision.py --env-file <.env> --frames review/qa/*.jpg --out review/qa-vision.json` | yes | Reviewer findings using this film's `review/qa-rules.md`; the raw reply is saved first |

**Spend ledger (`ledger.py`):** every paid call reserves an estimate first and settles from the returned usage, in `spend-ledger.json`.
- The cap is the existing ledger's `cap_usd`, else `script.json` `budget_usd`, else USD 5.
- Calls stop at 90% of the cap.
- A timeout stays reserved; it is never replayed blindly.

**Media (`media.py`):** provider bytes go to `media/original/<kind>/<id>.t<N>.<ext>` before any processing, with their sha256 in `media/manifest.json`. A new generation is a new take; nothing is overwritten.

**Proof:** moving the three newest films onto `av.py` reproduced their `mix.wav`, `index.html`, captions, cues and transcript byte for byte (2026-11-10).

Films made before this toolkit (`agentic-pentest-poc/*`, `awsops/*`, `aws-concepts/*`, the round-3 films and `demos/*`) keep their own frozen scripts. Do not "upgrade" them unless a revision is requested.
