#!/bin/sh
set -eu
pilot_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$pilot_dir/../.."
cp node_modules/gsap/dist/gsap.min.js "$pilot_dir/assets/gsap.min.js"
mkdir -p "$pilot_dir/.build"
python3 "$pilot_dir/build.py"
npx hyperframes lint "$pilot_dir"
npx hyperframes render "$pilot_dir" --fps 30 --workers 2 --strict -o "$pilot_dir/.build/render.mp4"
ffmpeg -y -v error -i "$pilot_dir/.build/render.mp4" -map 0:v:0 -map 0:a:0 -c:v copy -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 192k -movflags +faststart "$pilot_dir/pilot.mp4"
