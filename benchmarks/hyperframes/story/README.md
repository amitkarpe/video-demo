# The morning after — fictional short

A fictional company discovers an intrusion; its leaders and engineer discuss alert overload and an isolated agentic pentest proof of concept. The film uses AI-generated character artwork, locally synthesized Kokoro dialogue (CEO, CISO, engineer and narrator), an original synthesized underscore, HyperFrames camera moves, and timed captions. One CISO close-up is an audio-driven SadTalker facial-animation experiment; the other characters remain still images with camera movement. This is not a fully animated or commercially polished avatar film. See `docs/VIDEO_STORYTELLING.md` for the evidence and creative lessons.

The incident is invented. The pentest project tests isolated vulnerable training targets, not the company in this story; it does not claim to block intrusions or detect every issue. The model has no direct tools, and a deterministic executor and policy gate control permitted actions. The characters' concerns and dialogue are dramatization. The local voices and AI images require viewer review for quality and continuity.

Re-render after `npm ci` in `benchmarks/hyperframes`:

```sh
npx hyperframes render story -o story/security-story.mp4 --fps 30 --quality looks
```

The committed footage, images, WAV audio and editable HTML require no inference or paid service to re-render. To alter dialogue and regenerate voices/captions, edit `build.py` and run it in the local Kokoro ONNX environment using the model and voice paths documented in the parent README. Changes made only to generated `index.html` are overwritten when `build.py` is rerun.

The CISO clip was generated locally with [SadTalker](https://github.com/OpenTalker/SadTalker) from the generated CISO image and her Kokoro speech. On this Mac, Python 3.10 and downloaded model files required compatibility patches for NumPy, torchvision and Apple MPS; rendering the approximately three-second clip took several minutes plus one-time setup. The generated clip is included, but the patched experimental setup is not a turnkey dependency. Inspect lip synchronization and visual artifacts before production use; evaluate all model and dependency licenses for intended use.
