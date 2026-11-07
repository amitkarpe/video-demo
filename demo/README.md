# Free Mac video demo

The [MP4](video-demo.mp4) is a fictional, clearly labeled simulation: no AWS APIs are called, no commands are executed on a server, and no real incident data is used. It covers detection, AI investigation, an approve-once human decision, simulated Systems Manager patching, and verification/audit evidence.

## Files

- `storyboard.json` — editable scene content and narration; each `captions` entry is spoken and displayed.
- `render-scenes.swift` — local AppKit scene and caption renderer.
- `build.py` — synthesizes speech, generates scene images and SRT timing, and assembles the MP4.
- `captions.srt` — captions generated for the committed MP4. Captions are also burned into the video.
- `video-demo.mp4` — final revision, committed because it is approximately 2 MB.

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
