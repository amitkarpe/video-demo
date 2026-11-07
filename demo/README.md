# Free Mac video demo

The [MP4](video-demo.mp4) is a fictional, clearly labeled simulation: no AWS APIs are called, no commands are executed on a server, and no real incident data is used. It covers detection, AI investigation, an approve-once human decision, simulated Systems Manager patching, and verification/audit evidence.

## Files

- `storyboard.json` — editable scene content and narration; each `captions` entry is spoken and displayed.
- `render-scenes.swift` — local AppKit scene and caption renderer.
- `build.py` — synthesizes speech, generates scene images and SRT timing, and assembles the MP4.
- `captions.srt` — captions generated for the committed MP4. Captions are also burned into the video.
- `video-demo.mp4` — original macOS-voice revision, committed because it is approximately 2 MB.
- `kokoro-video.mp4` — local neural-voice candidate, with its own `kokoro-captions.srt`.

## Rebuild or revise

On macOS, install Apple's Command Line Tools (Swift/AppKit), ensure Python 3 and the `Samantha` system voice are available, and install the free Homebrew `ffmpeg` formula if needed. These requirements are local; no cloud account or paid service is used. An installed voice can be checked with `say -v '?'`.

From the repository root:

```sh
/usr/bin/python3 demo/build.py --output-dir demo/output
open demo/output/video-demo.mp4
```

To revise, edit a scene or caption in `demo/storyboard.json`, then rerun the command. The caption text is also the speech input. Replace `demo/captions.srt` and the committed MP4 with the newly generated versions if the revision is intended for the repository. `demo/output/` is ignored; the script overwrites its generated MP4 and SRT in the specified output directory. Speech duration may vary by macOS voice version, so regenerated SRT timings can differ. The builder rejects output outside 60–90 seconds.

## Verification on 2026-11-07

- Local Mac host profile check passed. Computer Use could enumerate applications, but selecting QuickTime timed out; the local Codex/CLI fallback was used. There was no ChatGPT Desktop Work playback verification.
- Final export: 65.13 seconds, 1920 × 1080, H.264 video and 48 kHz mono AAC audio, 1,985,588 bytes. FFmpeg decoded the whole file without errors; the audio track measured mean −16.5 dB and peak −1.9 dB. Extracted frames from all five scenes show readable captions and the simulation label.
- Revision: initial narration said “potential risk”; it was changed to “security risk” in scene 2, and the full video was re-exported. The SRT confirms the wording change. Initial MP4 SHA-256: `cf4543d9035cb790e9abacaa4c1131c98e4e695a720f6e9f01c30e38aa167442`; final: `8c3bd1a8ed01e6db475cfced28d3b4741493f3c11adc8f0dc60bc8bfe682b412`.
- No paid credits or watermark were used. The macOS voice and local FFmpeg were used; the user authorized Homebrew installation of FFmpeg and its dependencies.

The local `ffplay -autoexit` run completed the full video with audio enabled and exited successfully. Computer Use could not inspect the player, and the agent could not independently hear or judge the narration; review the MP4 with speakers enabled for that final subjective check.

## Local neural voice candidate

`kokoro-video.mp4` is an alternate narration using the Kokoro 82M `af_heart` voice, rendered locally through ONNX Runtime. `kokoro-captions.srt` has timings regenerated from those speech clips. The original `video-demo.mp4` remains available for comparison. A person should choose a voice and listen to the complete candidate before final acceptance.

Reproduce on an Apple Silicon Mac with Python 3.12, `uv`, Swift, and FFmpeg. These commands download free software and model files, and then run speech generation locally without an account or API key:

```sh
uv venv --python 3.12 demo/output/venv
uv pip install --python demo/output/venv/bin/python 'kokoro-onnx==0.6.1' 'soundfile==0.14.0'
mkdir -p demo/output/models
curl -fL -o demo/output/models/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/kokoro-v1.0.onnx
curl -fL -o demo/output/models/voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/voices-v1.0.bin
shasum -a 256 demo/output/models/*
demo/output/venv/bin/python demo/generate_kokoro_onnx.py \
  --model demo/output/models/kokoro-v1.0.onnx \
  --voices demo/output/models/voices-v1.0.bin \
  --voice af_heart --output-dir demo/output/speech
/usr/bin/python3 demo/build.py --speech-dir demo/output/speech --audio-gain-db 4 --output-dir demo/output/kokoro
```

Expected SHA-256 values for the downloaded model and voice files are `beb0d1848dee9a49da392cc3df26958d46cfa35d321edf434f52949153f0df3a` and `bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d`, respectively. These are the model-files-v1.1 release assets. Kokoro weights are Apache-2.0 and the [ONNX runtime wrapper](https://github.com/thewh1teagle/kokoro-onnx) is MIT. Downloading the files requires network access; inference is local. Do not commit the generated model, environment, or intermediate audio files.

The candidate is 65.64 seconds at 1920 × 1080, SHA-256 `f08faa669bfd91acb9e0bc3c4fe402f33cf9cb2ec4b1681353ddbed3bcc6a94f`. A second Kokoro export changed “security risk” to “potential risk”; its regenerated captions and full decode verified the edit and export without paid services. FFmpeg decoded it without errors. Local Whisper transcription of the complete initial Kokoro export matched all storyboard words after normalization of capitalization and punctuation. The final export uses the same speech and captions with 4 dB gain; measured peak is −2.7 dBFS. Transcription is an automated check, not a substitute for a human listening review. The current M5/macOS 26.1 combination rejected MLX GPU kernels; ONNX Runtime on CPU provided a working, fast alternative without an OS change.
