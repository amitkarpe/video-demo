# Ten-second cloud security teaser

**Watch:** Release removed (10 Nov 2026, owner decision). It held `cloud-security-teaser.mp4` (sha256 `90149f7c7756…`). Paths such as `out/*.mp4` below are where a local build writes them.


A fictional cloud security sequence: detect, investigate, human approval, and verification. It is labeled **SIMULATION / AI VOICE** and makes no AWS calls.

The visual is a generated still illustration animated with a slow camera push, traveling light particles, sliding text cards, and timed subtitles. This is motion graphics, not a fully generated 3D animation or a talking avatar. The narration uses OpenAI Realtime `gpt-realtime-2.1-mini` with the Cedar voice. The one generation request reported 162 input and 193 output tokens; actual dollar usage was not independently checked. The image was made with the built-in image generation tool; its billing is separate from this recorded API request.

## Files

- `background.png`: generated background.
- `narration-cedar.wav`: recorded synthetic speech; no key is stored here.
- `render.swift`: editable titles, captions, and visual overlays.
- `build.py`: local rendering and encoding.
- `captions.srt`: timings for the recorded speech.
- `cloud-security-teaser.mp4`: finished 10-second 1080p video.

## Rebuild

On macOS with Swift and FFmpeg available:

```sh
/usr/bin/python3 demo/teaser/build.py demo/output/cloud-security-teaser.mp4
```

The saved narration and illustration mean a rebuild uses no API or account. Edit text in `render.swift` and caption timing in `build.py` and `captions.srt`; a change to the spoken words requires a newly generated narration clip and timing adjustments. A human should review the narration and caption timing before publication.
