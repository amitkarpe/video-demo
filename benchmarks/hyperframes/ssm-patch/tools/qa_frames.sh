#!/bin/sh
# QA frames from the FINAL web MP4: 1280x720 JPEGs named by film time and narration line (review/qa/),
# and 1080p keyframes (keyframes/). No network.
set -eu
cd "$(dirname "$0")/.."
F=out/ssm-patch.mp4
mkdir -p review/qa keyframes
rm -f review/qa/*.jpg
for spec in 4.0:s01 12.5:s02 17.0:s03 24.0:s04 34.0:s05 39.0:s06 44.0:s07 58.0:s08 64.0:s09 69.0:s10 74.0:s11 85.0:s12 91.0:s13 97.0:s14 105.0:s15 111.0:s16 117.0:s17 128.0:s19 139.0:s20 143.0:s21 150.0:s22 66.6:wipe; do
  t=${spec%%:*}; id=${spec##*:}
  ffmpeg -v error -y -ss "$t" -i "$F" -frames:v 1 -vf scale=1280:720 -q:v 3 "review/qa/t$(printf '%06.1f' "$t")-$id.jpg"
done
for spec in 17.0:01-the-question 39.0:02-what-is-cis 64.0:03-factory-line 91.0:04-three-buckets 117.0:05-accepted-in-code 139.0:06-release-gate 150.0:07-close; do
  t=${spec%%:*}; n=${spec##*:}
  ffmpeg -v error -y -ss "$t" -i "$F" -frames:v 1 "keyframes/$n.png"
done
ls review/qa keyframes
