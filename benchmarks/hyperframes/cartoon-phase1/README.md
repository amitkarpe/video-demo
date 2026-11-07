# Tiny Security Robots: Phase 1

A 10-second, 1080p cartoon built from editable SVG and a seekable HyperFrames/GSAP timeline. The smiling scanner bot, AI helper arm, gate, four clue bubbles, grouping machine, report, human head and arm are separate animated elements. The visuals are a simplified illustration of a recorded Juice Shop training-lab replay, not a live scan or incident.

## Storyboard and narration

| Seconds | Action and emotion | Spoken words |
|---|---|---|
| 0–1.8 | A safe bubble and toy lab pop up; the scanner rolls in and waves. | “A safe lab!” |
| 1.8–4.1 | The friendly AI points at an approved choice; the policy gate opens green while the rejected choice stays outside. | “AI picks an approved step.” |
| 4.1–6.8 | Four colorful alert bubbles travel independently into a squash-and-stretch grouping machine. | “Clues join up.” |
| 6.8–10 | One report appears for a smiling person to inspect: evidence, severity, and fix. | “A person checks the report!” |

The real model has no scanner or shell tools: it selects from fixed action IDs; deterministic code and a policy gate control execution. The current demo can replay recorded results. The actual report, OWASP/CVSS mapping and remediation are explained in the private [pentest README](https://github.com/kcloud1/agentic-pentest-poc/blob/main/README.md) and [demo guide](https://github.com/kcloud1/agentic-pentest-poc/blob/main/docs/DEMO.md). The cartoon omits implementation details rather than portraying a real attack.

## Re-render and edit

From `benchmarks/hyperframes` on the Mac with the already-installed dependencies:

```sh
npm ci                 # one-time dependency restore; uses the existing lockfile
./node_modules/.bin/hyperframes render cartoon-phase1 -o cartoon-phase1/cartoon-phase1.mp4 --fps 30 --quality looks
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height -of json cartoon-phase1/cartoon-phase1.mp4
ffmpeg -v error -i cartoon-phase1/cartoon-phase1.mp4 -f null -
```

`index.html` contains the SVG artwork, separate body parts and seekable timeline. `captions.srt`, `voice.json` and the four WAVs provide the voice timing. To change the narration, install/use the Kokoro ONNX environment and model files documented in `demo/README.md`, run `make_voice.py --model ... --voices ...`, then update the matching timed caption/audio attributes in `index.html` from `voice.json`. Re-render after edits. The included WAV files are locally generated with Kokoro `am_michael`; the project uses no paid service. GSAP's no-charge license has its own restrictions; see the parent README.

## Scorecard

**HYPERFRAMES_CARTOON_PASS for the technical/creative prototype**, pending the viewer's listening and creative review. Four independent bubbles travel and shrink; the bot arm and wheels, AI arm, gate, grouping machine, report, human arm/head and clouds animate separately. The single continuous scene communicates lab → permitted choice → grouped clues → report without depicting live exploitation. SVG and motion remain editable; the corrected report placement was re-rendered. Ten seconds limits how much policy and technical detail a young viewer can absorb. Audio was played through the Mac but not heard by the agent; voice quality remains unverified. No software installation, paid API credits, AWS calls or scan were used for this cartoon.

Validation on this Mac: HyperFrames check passed; contrast 45/45, motion and audio checks passed. It flagged small report text during the report’s entry animation and layout overlap/pivot warnings for deliberately moving artwork; the final report was inspected at full size. FFmpeg decoded the complete 10-second H.264/AAC file, and `ffplay` exited successfully after playback.
