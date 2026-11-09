# Your shift with Nextflow Offline (ops film)

Audience: the operations team (knows Linux and AWS, not hands-on with the pipeline). Goal: they finish proud and confident.
Story: one question from a researcher ("was last night's run really offline?"), answered with one picture of three islands:
the connected mainland (internet, GitLab), the vault (private S3 and ECR), and the sealed island (runtime host, no route out, joined only by a private pipe).

This folder is the **52 s sample**: hook, the whole picture, a failure drill and what PASS means. The full film follows after review.

## Build

```bash
cd benchmarks/hyperframes/ops-nextflow-offline
# voice (local Kokoro; needs kokoro-onnx in HYPERFRAMES_PYTHON)
python3 -c "import json,subprocess;[subprocess.run(['npx','hyperframes','tts',l['text'],'-v','af_heart','-o',f'assets/{l[\"id\"]}.wav'],check=True) for l in json.load(open('script.json'))['lines']]"
curl -sSo assets/m_Inspired.mp3 https://incompetech.com/music/royalty-free/mp3-royaltyfree/Inspired.mp3
bash tools/mix.sh            # assets/mix.wav: voice at timing.json starts + ducked music bed
npx hyperframes transcribe review/voice.wav -e parakeet   # word times -> transcript.json
python3 build.py             # index.html + captions.srt
npx hyperframes check
npx hyperframes render -o out/ops-sample.mp4 -f 30 -q delivery
```

Parts: three.js r147 world drawn from `hf-seek` time (deterministic, seeded), GSAP overlays and captions, real AWS architecture icons, Inter font.
Music: "Inspired" by Kevin MacLeod (incompetech.com). Claims and labels: `CLAIMS.md`.
