#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p .build
if [[ ! -x ../../node_modules/.bin/hyperframes ]]; then
  npm ci --ignore-scripts --no-audit --no-fund --prefix ../..
fi
../../node_modules/.bin/hyperframes browser ensure
cp ../../node_modules/gsap/dist/gsap.min.js assets/gsap.min.js
python3 prepare_audio.py
python3 build.py
../../node_modules/.bin/hyperframes lint . --json > .build/lint.json
../../node_modules/.bin/hyperframes render . --output .build/render.mp4 --fps 30 --resolution 1080p --workers "${WORKERS:-4}" --crf 20 --strict
ffmpeg -y -v warning -i .build/render.mp4 -c:v copy -af 'loudnorm=I=-16:TP=-1.5:LRA=9' -ar 48000 -ac 2 -c:a aac -b:a 192k -movflags +faststart blueops-trust-factory.mp4
ffmpeg -v error -i blueops-trust-factory.mp4 -f null -
