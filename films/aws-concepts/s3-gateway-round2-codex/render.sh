#!/bin/sh
set -eu
pilot_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$pilot_dir/../.."
mkdir -p "$pilot_dir/.build"
cp node_modules/gsap/dist/gsap.min.js "$pilot_dir/assets/gsap.min.js"
python3 "$pilot_dir/build.py"
./node_modules/.bin/hyperframes lint "$pilot_dir"
./node_modules/.bin/hyperframes render "$pilot_dir" --fps 30 --workers 2 --strict -o "$pilot_dir/.build/render.mp4"
ffmpeg -y -v error -i "$pilot_dir/.build/render.mp4" -map 0:v:0 -map 0:a:0 -c:v copy -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 192k -movflags +faststart "$pilot_dir/pilot.mp4"
