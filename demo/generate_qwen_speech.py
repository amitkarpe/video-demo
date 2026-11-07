#!/usr/bin/env python3
"""Generate local Qwen3-TTS clips for the video storyboard on Apple Silicon."""
import argparse
import json
from pathlib import Path

import mlx.core as mx
from mlx_audio.audio_io import write
from mlx_audio.tts.utils import load_model

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, required=True, help="Local Qwen3-TTS CustomVoice model directory")
    parser.add_argument("--voice", default="Ryan", help="English presets include Ryan and Aiden")
    parser.add_argument("--storyboard", type=Path, default=ROOT / "storyboard.json")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--style", default="Speak clearly and naturally, with warmth and engaging, measured documentary narration.")
    args = parser.parse_args()
    story = json.loads(args.storyboard.read_text())
    args.output_dir.mkdir(parents=True, exist_ok=True)
    model = load_model(str(args.model))
    for i, scene in enumerate(story["scenes"], 1):
        for j, caption in enumerate(scene["captions"], 1):
            results = list(model.generate_custom_voice(text=caption, speaker=args.voice, language="English", instruct=args.style))
            if not results or any(r.sample_rate != results[0].sample_rate for r in results):
                raise RuntimeError(f"No audio or mismatched sample rates for scene {i}, caption {j}")
            audio = mx.concatenate([r.audio for r in results], axis=0) if len(results) > 1 else results[0].audio
            path = args.output_dir / f"speech-{i}-{j}.wav"
            write(str(path), audio, results[0].sample_rate)
            print(f"Generated {path}", flush=True)


if __name__ == "__main__":
    main()
