# Patching Running Servers in AWS Factory — Scanned Is Not Patched

A 2 min 37 s public explainer for engineers and managers (Issue #35). It shows how AWS Factory keeps running servers patched with AWS Systems Manager Patch Manager. The look is a **3D toy-block world built with Three.js**, rendered by HyperFrames through its native `hf-seek` runtime: one continuous island, with no slide cuts.

**Story:**
1. New fixes arrive every week. How do running servers keep up, safely?
2. Two roads: build fresh images, or patch in place with Patch Manager.
3. Patch groups: a tag on each server.
4. The rules: security at once, other updates after 7 days, database and container engine never in place.
5. Scan on the weekend night, install at dawn, no automatic reboot.
6. The trap: a tag that matches no group means scanned, never installed. **Scanned is not patched.**
7. The check: reports flag any server with no patch data; one server first, then every group; the owner approves.
8. *Fresh images for new servers. Patch Manager for running ones.*

**Public-safe and generic:** groups only. No account, host names, IDs, schedule times, dates or patch counts. `CLAIMS.md` maps each statement to the private source.

## Files
| Path | What it is |
|---|---|
| `out/ssm-patch.mp4` | Final film: H.264 1080p30, AAC, 157.2 s, 30.2 MB, −16.0 LUFS |
| `captions.srt`, `transcript.txt`, `cues.json` | 36 caption cues from the measured narration |
| `keyframes/*.png` | One frame per chapter from the final file |
| `CLAIMS.md`, `review/VERIFICATION.md` | Evidence map; QA record with dispositions and spend |
| `src/world.js` | The 3D world: three looks; every object is a pure function of time |
| `src/index.template.html`, `build.py` | Composition (Three.js canvas, GSAP overlays, captions) and build (cues, captions, synthesized score and effects, loudness-normalised mix) |
| `lib/three/` | Three.js 0.187.0 (MIT), a pinned local copy; package sha256 `ff540832ded0cfe919764d24a3d88f3e2a05f23303f876423e4f893841e90728` |
| `script.json` | Narration and voice settings |
| `media/original/**`, `media/manifest.json` | Immutable provider voice originals and their derivations |
| `phase1/` | Phase 1 review pack: 3 looks, the 8-slide storyboard, the voice sample |
| `tools/` | Ledger, media, voice, derive, QA tools, `finalize.sh` |

## Rebuild (no paid API)
```bash
cd benchmarks/hyperframes && npm ci && cd ssm-patch
python3 -m venv .venv && .venv/bin/pip install numpy==2.5.4 soundfile==0.14.0 pillow==13.0.0
.venv/bin/python tools/derive.py && .venv/bin/python build.py
cd .. && npx hyperframes check ssm-patch
npx hyperframes render ssm-patch -o ssm-patch/out/master-delivery.mp4 -f 30 -q delivery   # about 50 s with a hardware GPU
ssm-patch/tools/finalize.sh
```

## Spend
USD **0.46** over 25 OpenAI requests, all ACK: 23 voice lines and 2 QA passes. No images were generated. See `review/VERIFICATION.md` §6.
