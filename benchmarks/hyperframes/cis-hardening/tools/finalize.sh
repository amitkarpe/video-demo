#!/bin/sh
# Final web deliverable from the HyperFrames master: H.264 CRF 20 video + AAC 192k from the normalised assets/mix.wav.
# The master (out/master-delivery.mp4, ~180 MB) is above GitHub's 100 MB file limit and is not committed.
set -eu
cd "$(dirname "$0")/.."
ffmpeg -v error -y -i out/master-delivery.mp4 -i assets/mix.wav -map 0:v:0 -map 1:a:0 \
  -c:v libx264 -preset slow -crf 20 -profile:v high -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart \
  out/cis-hardening.mp4
