# CIS Hardening in AWS Factory — Fix What We Can, Accept What We Must

**Watch:** [cis-hardening.mp4](https://github.com/amitkarpe/video-demo/releases/download/film-aws-factory-cis-hardening/cis-hardening.mp4) (sha256 `46830a9487c7…`) — video files live on the film's [GitHub Release](https://github.com/amitkarpe/video-demo/releases/tag/film-aws-factory-cis-hardening), not in git. Paths such as `out/*.mp4` below are where a local build writes them.


A 2 min 36 s public explainer for engineers and managers (Issue #32). It follows the two-phase workflow: Phase 1 storyboard in `phase1/`, then this film after the owner's "Go". The look is the native **HyperFrames Swiss Grid** style, with three small AI clay illustrations.

**Story:**
1. 243 CIS checks: do we fix them all?
2. What CIS is.
3. The AWS Factory line.
4. Three buckets: hardened upstream, fixed by us, accepted risk with owner approval. The 243 squares sort themselves into the buckets.
5. Why accept a risk.
6. The release gate: a new failure stops the release, and labels are never relabelled.
7. *Fix what we can. Accept what we must.*

**Public-safe by rule:** no CIS control numbers, IDs, dates or credential details. `CLAIMS.md` maps each statement to the private source at a pinned revision.

## Files
| Path | What it is |
|---|---|
| `out/cis-hardening.mp4` | Final film: H.264 1080p30, AAC 48 kHz, 156.3 s, 25.3 MB, −16.0 LUFS |
| `captions.srt`, `transcript.txt`, `cues.json` | 36 caption cues from the measured narration |
| `keyframes/*.png` | 7 frames from the final file |
| `CLAIMS.md`, `review/VERIFICATION.md` | Evidence map; QA record with dispositions, spend and usage |
| `src/index.template.html`, `build.py` | Editable composition (HyperFrames + GSAP) and the build (cues, captions, synthesized score and effects, loudness-normalised mix) |
| `script.json`, `prompts/` | Narration and voice settings; image prompts and provenance |
| `media/original/**`, `media/manifest.json` | Immutable provider originals and their derivations |
| `phase1/` | The Phase 1 review pack: 3 native styles, a 7-slide storyboard, a voice sample |
| `../../../toolkit/` | Shared ledger, media, voice, image, derive, QA and finalize tools (this film's QA rules: `review/qa-rules.md`) |

## Rebuild (no paid API)
From the repository root (one shared toolchain; see the root README):
```bash
npm ci                                   # HyperFrames + GSAP, pinned; copies gsap.min.js into every film
python3 -m venv .venv && .venv/bin/pip install numpy==2.5.4 soundfile==0.14.0 pillow==13.0.0
cd films/aws-factory/cis-hardening
../../../.venv/bin/python ../../../toolkit/derive.py && ../../../.venv/bin/python build.py
cd ../../.. && npx hyperframes check films/aws-factory/cis-hardening
npx hyperframes render films/aws-factory/cis-hardening -o films/aws-factory/cis-hardening/out/master-delivery.mp4 -f 30 -q delivery
cd films/aws-factory/cis-hardening && ../../../toolkit/finalize.sh && ../../../toolkit/qa_frames.sh
```
Toolkit commands (`toolkit/*.py`) run from this folder; paid ones (`narrate_realtime.py`, `gen_images.py`, `qa_transcribe.py`, `qa_vision.py`) take `--env-file` and stop at 90% of this film's cap (`spend-ledger.json`).

## Spend
USD **0.61** over 27 OpenAI requests, all ACK: 22 voice lines, 3 illustrations and 2 QA passes. See `review/VERIFICATION.md` §7.
