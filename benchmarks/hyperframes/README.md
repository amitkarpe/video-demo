# HyperFrames pentest benchmark

A 43-second, 1920×1080 animated explainer from the recorded OWASP Juice Shop lab. [`pentest.mp4`](pentest.mp4) includes male Kokoro narration and burned-in captions; [`captions.srt`](captions.srt) is available separately for players or SharePoint. [`storyboard.json`](storyboard.json), [`index.html`](index.html) and [`make.py`](make.py) are editable. The flow diagram illustrates AI triage and a human policy gate; it is an explanatory design, not a recording of a live autonomous action.

## Evidence and boundaries

The [private recorded report](https://github.com/kcloud1/agentic-pentest-poc/blob/main/docs/sample/out/juice-shop/report/report.json) group `grp-d382cb1578` contains six findings from Nikto and ZAP, sample `Access-Control-Allow-Origin: *` headers, a model-scored CVSS 4.3 and an origin-allowlist recommendation. The score and model verdict are from the report, not a proof of exploitation. No scan, AWS call, remediation, OpenAI or HeyGen API call was made. The recorded example is a lab; the animation does not show a live system.

## Reproduce

Requires Node 22+, FFmpeg and a compatible Chrome/Chromium browser; tested on Apple Silicon macOS, Node 26.12.1 and FFmpeg 9.0.2. Install dependencies once (network needed for npm and, if absent, the renderer's first Chrome download):

```sh
cd benchmarks/hyperframes
npm ci
npx hyperframes render -o pentest.mp4 --fps 30 --quality looks
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height -of json pentest.mp4
ffmpeg -v error -i pentest.mp4 -f null -
```

The six WAV clips are included; npm installs the GSAP runtime, so changing only HTML animation does not require voice generation or an API. To revise narration, install the local Kokoro ONNX prerequisites and verified model files documented in `demo/README.md`, then run `python make.py --model /path/to/kokoro-v1.0.onnx --voices /path/to/voices-v1.0.bin` inside the Kokoro environment and re-render. `make.py` regenerates the HTML, six voice clips, storyboard and synchronized SRT. Edits made only to generated `index.html` will be overwritten by `make.py`; edit its source template for durable changes. Assets are local for playback; the HyperFrames CLI may fetch its browser/fonts during initial setup. HyperFrames is Apache-2.0; the GSAP runtime is under the [standard no-charge license](https://gsap.com/standard-license/), with its own use restrictions; it is not claimed to be Apache-licensed. Kokoro model weights are Apache-2.0, ONNX wrapper MIT.

## Observed benchmark scorecard

| Criterion | Result / limitation |
|---|---|
| First 10 seconds | Six alerts to one potential issue; lab context visible. |
| Motion | Lines draw through the diagram and the evidence view zooms/pans. Motion is deliberately simple; commercial polish is subjective. |
| Fidelity | Recorded report values checked directly; workflow is an illustration, not a live exploit or remediation. |
| Editable / revision | HTML and generator source retained. Initial 46-second render was revised by shortening two narration lines and re-rendered to 43 seconds. |
| Local render | 43 seconds, 1080p H.264/AAC; full FFmpeg decode passed. Final local render took 19.9 seconds after browser setup on this Mac. `hyperframes check` passed with zero craft, audio, motion, or contrast warnings; lint reported six warnings because scenes are not split into sub-compositions, limiting Studio timeline editing. |
| Voice | Local male Kokoro `am_michael`; clips aligned to caption start/end times. No human listening assessment by the agent; quality and pronunciation require listener review. |
| Scalability | Chapters and media can be composed, but 20–30-minute throughput, footage integration and resulting file sizes were not tested. |
| Cost | $0 in paid API/software use. npm/browser/font downloads used the network; model inference and final render were local. |

**Decision: HYPERFRAMES_ACCEPTED for an initial technical benchmark**, conditional on the viewer's voice and creative review. This is not proof of long-form production readiness. Six lint warnings and untested long-form scaling should be addressed before a larger production. No second framework was implemented.
