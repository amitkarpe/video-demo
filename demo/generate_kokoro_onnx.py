#!/usr/bin/env python3
"""Generate local Kokoro speech clips for the video storyboard."""
import argparse
import json
from pathlib import Path

import soundfile as sf
from kokoro_onnx import Kokoro

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, type=Path, help="Path to kokoro-v1.0.onnx")
    parser.add_argument("--voices", required=True, type=Path, help="Path to voices-v1.0.bin")
    parser.add_argument("--voice", default="af_heart")
    parser.add_argument("--storyboard", type=Path, default=ROOT / "storyboard.json")
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    story = json.loads(args.storyboard.read_text())
    args.output_dir.mkdir(parents=True, exist_ok=True)
    synthesizer = Kokoro(str(args.model), str(args.voices))
    for i, scene in enumerate(story["scenes"], 1):
        for j, caption in enumerate(scene["captions"], 1):
            audio, sample_rate = synthesizer.create(caption, voice=args.voice, speed=1.0, lang="en-us")
            path = args.output_dir / f"speech-{i}-{j}.wav"
            sf.write(str(path), audio, sample_rate, subtype="PCM_16")
            print(f"Generated {path}", flush=True)


if __name__ == "__main__":
    main()
