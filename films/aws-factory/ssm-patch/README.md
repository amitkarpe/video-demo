# Patching Running Servers in AWS Factory — Scanned Is Not Patched

**Watch:** [ssm-patch.mp4](https://github.com/amitkarpe/video-demo/releases/download/film-aws-factory-ssm-patch/ssm-patch.mp4) (sha256 `d5c40f5ed612…`) — video files live on the film's [GitHub Release](https://github.com/amitkarpe/video-demo/releases/tag/film-aws-factory-ssm-patch), not in git. Paths such as `out/*.mp4` below are where a local build writes them.


A 3 min public explainer for engineers and managers (Issue #35). It shows how AWS Factory keeps running servers patched with AWS Systems Manager Patch Manager. The look is a **3D toy-block world built with Three.js**, rendered by HyperFrames through its native `hf-seek` runtime: one continuous island, with no slide cuts. Each family has its own building: GitLab (orange towers and a pipeline), MongoDB (green vault members in a replica ring) and the CloudOS workspace on ECS (blue worker nodes, containers and a crane).

**Story (revision 2, the owner's option 2):**
1. New fixes arrive every week. How do running servers keep up, safely?
2. Two roads: build fresh images, or patch in place with Patch Manager.
3. Three families: one base image → GitLab, MongoDB, the CloudOS workspace on ECS. Each server's tag = its patch group.
4. The rules: security at once, other updates after 7 days, database and container engine never in place.
5. The patch flow: scan at night → nothing missing means compliant (MongoDB) → missing updates install in the group's window (GitLab, then CloudOS) → most need no reboot → a new kernel's reboot waits for the downtime window (CloudOS) → green.
6. The trap: a tag that matches no group means scanned, never installed. **Scanned is not patched.**
7. The check: reports flag any server with no patch data; one server first, then every group; the owner approves.
8. *Fresh images for new servers. Patch Manager for running ones.*

**Public-safe and generic:** groups only. No account, host names, IDs, schedule times, dates or patch counts. `CLAIMS.md` maps each statement to the private source.

## Files
| Path | What it is |
|---|---|
| `out/ssm-patch.mp4` | Final film: H.264 1080p30, AAC, 180.3 s, 50.7 MB, −16.0 LUFS |
| `captions.srt`, `transcript.txt`, `cues.json` | 42 caption cues from the measured narration |
| `keyframes/*.png` | One frame per chapter from the final file |
| `CLAIMS.md`, `review/VERIFICATION.md` | Evidence map; QA record with dispositions and spend |
| `src/world.js` | The 3D world: the three families and the patch machinery; every object is a pure function of time |
| `src/index.template.html`, `build.py` | Composition (Three.js canvas, GSAP overlays, captions) and build (cues, captions, synthesized score and effects, loudness-normalised mix) |
| `lib/three/` | Three.js 0.187.0 (MIT), a pinned local copy; package sha256 `ff540832ded0cfe919764d24a3d88f3e2a05f23303f876423e4f893841e90728` |
| `script.json` | Narration and voice settings |
| `media/original/**`, `media/manifest.json` | Immutable provider voice originals and their derivations |
| `phase1/` | Phase 1 review pack: 3 looks, the 8-slide storyboard, the voice sample (its generator needs `src/world.js` from commit `254f6d3`) |
| `../../../toolkit/` | Shared ledger, media, voice, image, derive, QA and finalize tools (this film's QA rules: `review/qa-rules.md`) |

## Rebuild (no paid API)
From the repository root (one shared toolchain; see the root README):
```bash
npm ci                                   # HyperFrames + GSAP, pinned; copies gsap.min.js into every film
python3 -m venv .venv && .venv/bin/pip install numpy==2.5.4 soundfile==0.14.0 pillow==13.0.0
cd films/aws-factory/ssm-patch
../../../.venv/bin/python ../../../toolkit/derive.py && ../../../.venv/bin/python build.py
cd ../../.. && npx hyperframes check films/aws-factory/ssm-patch
npx hyperframes render films/aws-factory/ssm-patch -o films/aws-factory/ssm-patch/out/master-delivery.mp4 -f 30 -q delivery
cd films/aws-factory/ssm-patch && ../../../toolkit/finalize.sh && ../../../toolkit/qa_frames.sh
```
Toolkit commands (`toolkit/*.py`) run from this folder; paid ones (`narrate_realtime.py`, `gen_images.py`, `qa_transcribe.py`, `qa_vision.py`) take `--env-file` and stop at 90% of this film's cap (`spend-ledger.json`).

## Spend
USD **1.50** in total over 54 OpenAI requests, all ACK: voice for Phase 1, revision 1 and revision 2, plus the QA passes. Revision 2 alone cost USD 1.03. No images were generated. See `review/VERIFICATION.md` §7.
