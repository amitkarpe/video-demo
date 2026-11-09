#!/usr/bin/env python3
"""Create a local mock video with macOS speech, AppKit scenes and FFmpeg."""
import argparse
import json
import shutil
import subprocess
import tempfile
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(command):
    subprocess.run([str(item) for item in command], check=True)


def duration(path):
    output = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)], text=True)
    return float(output.strip())


def srt_time(seconds):
    ms = round(seconds * 1000)
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


def concat_line(path):
    # ffconcat escapes apostrophes by closing the quote, escaping and reopening.
    return "file '" + str(path).replace("'", "'\\''") + "'\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=ROOT / "output")
    parser.add_argument("--storyboard", type=Path, default=ROOT / "storyboard.json")
    parser.add_argument("--speech-dir", type=Path, help="Directory containing speech-<scene>-<caption>.wav files")
    parser.add_argument("--audio-gain-db", type=float, default=0.0, help="Optional output gain in decibels")
    args = parser.parse_args()
    for tool in (("swiftc", "ffmpeg", "ffprobe") if args.speech_dir else ("say", "swiftc", "ffmpeg", "ffprobe")):
        if not shutil.which(tool):
            raise SystemExit(f"Missing required tool: {tool}")
    story = json.loads(args.storyboard.read_text())
    if len(story["scenes"]) != 5 or any(len(s["captions"]) != 2 for s in story["scenes"]):
        raise SystemExit("Storyboard must contain five scenes with two captions each")
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="video-demo-") as scratch:
        temp = Path(scratch)
        renderer = temp / "render-scenes"
        run(["swiftc", ROOT / "render-scenes.swift", "-o", renderer])
        run([renderer, args.storyboard.resolve(), temp])
        segments = []
        for i, scene in enumerate(story["scenes"], 1):
            clips = []
            for j, caption in enumerate(scene["captions"], 1):
                if args.speech_dir:
                    sound = args.speech_dir / f"speech-{i}-{j}.wav"
                    if not sound.is_file():
                        raise SystemExit(f"Missing speech clip: {sound}")
                else:
                    sound = temp / f"speech-{i}-{j}.aiff"
                    run(["say", "-v", story["voice"], "-r", str(story["rate"]), "-o", sound, caption])
                clips.append((j, caption, sound, duration(sound)))
            padding = max(0.7, (13.0 - sum(c[3] for c in clips)) / 2)
            for j, caption, sound, _ in clips:
                wave = temp / f"audio-{i}-{j}.wav"
                run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", sound, "-af", f"apad=pad_dur={padding:.3f}", "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", wave])
                segments.append((caption, wave, temp / f"scene-{i:02}-caption-{j:02}.png", duration(wave)))
        audio_list = temp / "audio.ffconcat"
        image_list = temp / "images.ffconcat"
        audio_list.write_text("ffconcat version 1.0\n" + "".join(concat_line(x[1]) for x in segments))
        image_list.write_text("ffconcat version 1.0\n" + "".join(concat_line(x[2]) + f"duration {x[3]:.6f}\n" for x in segments) + concat_line(segments[-1][2]))
        audio = temp / "narration.wav"
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", audio_list, "-c", "copy", audio])
        position = 0.0
        blocks = []
        for n, (caption, _, _, seconds) in enumerate(segments, 1):
            blocks.append(f"{n}\n{srt_time(position)} --> {srt_time(position + seconds)}\n{textwrap.fill(caption, width=55)}\n")
            position += seconds
        (out / "captions.srt").write_text("\n".join(blocks))
        if not 60 <= position <= 90:
            raise SystemExit(f"Narration duration {position:.1f}s is outside the 60–90 second acceptance range")
        movie = out / "video-demo.mp4"
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", image_list, "-i", audio, "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-af", f"volume={args.audio_gain_db}dB", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-t", f"{position:.3f}", movie])
        print(f"Created {movie} ({duration(movie):.2f} seconds); captions: {out / 'captions.srt'}")


if __name__ == "__main__":
    main()
