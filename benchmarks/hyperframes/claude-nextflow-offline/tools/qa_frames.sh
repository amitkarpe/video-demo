#!/bin/sh
# QA frames from the FINAL web MP4: 1280x720 JPEGs named by film time and narration line (review/qa/),
# and 1080p keyframes (keyframes/). No network.
set -eu
cd "$(dirname "$0")/.."
F=out/claude-nextflow-offline.mp4
mkdir -p review/qa keyframes
rm -f review/qa/*.jpg
for spec in 16.9:s03 24.0:s04 36.5:s05 47.5:s07 59.0:s09 66.5:s10 81.0:s12 86.0:s13 96.5:s14 101.5:s15 106.5:s16 112.0:s17 124.0:s18 137.5:s19 142.0:s20 150.5:s21 161.5:s23 184.5:s27 193.0:s28 204.5:s30 109.4:wipe 61.0:wipe; do
  t=${spec%%:*}; id=${spec##*:}
  ffmpeg -v error -y -ss "$t" -i "$F" -frames:v 1 -vf scale=1280:720 -q:v 3 "review/qa/t$(printf '%06.1f' "$t")-$id.jpg"
done
for spec in 16.9:01-missing-piece 59.0:02-gitlab-home 86.0:03-one-release 101.5:04-registered 142.0:05-architecture 161.5:06-offline-run 184.5:07-pass 204.5:08-confidence; do
  t=${spec%%:*}; n=${spec##*:}
  ffmpeg -v error -y -ss "$t" -i "$F" -frames:v 1 "keyframes/$n.png"
done
ls review/qa keyframes
