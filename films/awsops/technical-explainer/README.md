# Inside AWSOps: what was approved, what ran, what the evidence proves

**Watch:** [awsops-technical-explainer.mp4](https://github.com/amitkarpe/video-demo/releases/download/film-awsops-technical-explainer/awsops-technical-explainer.mp4) (sha256 `dae56a170a89…`) — video files live on the film's [GitHub Release](https://github.com/amitkarpe/video-demo/releases/tag/film-awsops-technical-explainer), not in git. Paths such as `out/*.mp4` below are where a local build writes them.


A visually revised 10:49 engineering film for AWS CloudOps, security and DevOps peers. One public S3 canary alias connects eight chapters, while animated mechanisms expose the boundaries between imported assertions, private identity binding, frozen scope, human decisions, operation attempts and independent verification.

The owner-requested visual refinement is documented in `REVISION.md`, with before/after encoded evidence under `review/`. `architecture.svg` is the editable master map; `visuals.py` supplies the shared SVG vocabulary and `mechanisms.py` the focused mechanisms. Official icon origins, terms and unmodified-asset hashes are under `assets/icons/`.

The entire walkthrough is labelled **SYNTHETIC WALKTHROUGH**. It is a source-grounded SVG reconstruction, not AWS console footage or evidence that this worker changed a resource. Source `amitkarpe/awsops` was read only at `15c12fb5362dd05fc4d8aaf10ebd31d3ce2935d9`; current main matched that reviewed baseline at intake. Earlier pentest productions and PRs #7/#11 remain unchanged.

## Watch and review

- `awsops-technical-explainer.mp4`: standalone 1920×1080 H.264/AAC film.
- `captions.srt`, `transcript.txt`, `chapters.txt`: synchronized subtitles and asynchronous review aids.
- `evidence.md`: pinned claim-to-source and source-to-scene map, historical observations and pending acceptance.
- `QUALITY.md`: actual verification, creative/listening limits and paid usage.

`Batch A` and `Run A` are visual aliases. The complete public-safe example lives in `synthetic-batch.json`. Reject and Approve Once are **alternative scenarios**, not two decisions committed to the same batch or a replay after Reject. The import planner and canary preparation are separate implementations; the diagram does not invent a live wire between them. Provider and approval sequences are illustrative, never a real authenticated owner action. Source-test assertions and accepted historical results are identified separately from checks performed for this film.

## Edit and reproduce

The parent project pins HyperFrames 0.9.20 and GSAP 3.15.0. Reuse its installed dependencies, or use its lockfile with `npm ci` to restore the same versions. The parent's postinstall restores the local GSAP asset. No paid generator or API is required.

From `benchmarks/hyperframes`:

```sh
python3 awsops-technical-explainer/compose.py
./node_modules/.bin/hyperframes check awsops-technical-explainer
./node_modules/.bin/hyperframes render awsops-technical-explainer \
  -o awsops-technical-explainer/awsops-technical-explainer.mp4 --fps 30 --quality looks
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height \
  -of json awsops-technical-explainer/awsops-technical-explainer.mp4
ffmpeg -v error -i awsops-technical-explainer/awsops-technical-explainer.mp4 -f null -
```

`compose.py` builds the editable HTML/SVG/GSAP composition. A seekable spatial camera returns to the same master architecture, then enters source-grounded mechanisms: field assembly, a revision mismatch, atomic decision competition, fixed SDK steps, TLS-only policy branching, lost acknowledgement, same-run reconciliation, conditional cleanup and four independent evidence sources. Document entries use restrained layered perspective; code and captions settle front-facing. The top navigation/legend has been replaced by a compact identity and contextual trust note. `review/visual-beats.json` lists the cue-linked explanatory beats. Speech is timed first; visual events reference sentence cues by text. `script.json` is the narration input. Cached sentence WAVs, `speech-cache.json`, `cues.json` and `storyboard.json` preserve the exact voice and timing through visual revisions.

Narration uses the existing local Kokoro ONNX setup and `am_michael`, normal speed 1.0, without music. For narration edits, run `build.py --model /path/to/kokoro-v1.0.onnx --voices /path/to/voices-v1.0.bin` inside the existing Kokoro environment documented by the repository's voice work. Unchanged content hashes reuse audio. `--reuse-audio` refuses changed/uncached sentences rather than silently mismatching words and WAVs. No narration was trimmed, accelerated or regenerated to satisfy a runtime target.

The offline public-fixture checks used only the byte-verified pure `intake.cjs` and `scope.cjs` helpers in a scratch evidence directory. `fixture-check.json` records imported provenance, zero real writes, extra-field rejection, digest match and revision-drift mismatch. No application/executor path, boto3 client, AWS CLI, authentication flow or operational approval was invoked.

For visual-only changes, do not run TTS: all 100 original WAVs, narration, SRT and cue/storyboard files are preserved by `narration-preservation.json`. To reproduce the representative test, generate `proof.html` with `python3 compose.py --proof`, render 395–423s with `--composition proof.html --start 395 --end 423`, then remove that generated proof HTML before the normal check so there is only one root composition. This is an engineering/creative revision, not live runtime acceptance.
