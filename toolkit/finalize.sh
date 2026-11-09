#!/bin/sh
# Final web deliverable from the HyperFrames master: H.264 CRF 20 video + AAC 192k from the normalised assets/mix.wav.
# Run from the film folder. Writes out/<film-folder-name>.mp4. MP4s are not committed: attach them to the film's
# GitHub Release (see docs/AGENT_VIDEO_PLAYBOOK.md, "Delivery").
set -eu
[ -f script.json ] || { echo "run from a film folder (no script.json here)"; exit 1; }
NAME=$(basename "$PWD")
ffmpeg -v error -y -i out/master-delivery.mp4 -i assets/mix.wav -map 0:v:0 -map 1:a:0 \
  -c:v libx264 -preset slow -crf 20 -profile:v high -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart \
  "out/$NAME.mp4"
echo "out/$NAME.mp4"
