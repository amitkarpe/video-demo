#!/bin/sh
# QA frames from the FINAL web MP4: one 1280x720 JPEG at 70% of every narration line (review/qa/),
# and one 1080p keyframe per chapter (keyframes/). Times come from cues.json. No network.
set -eu
cd "$(dirname "$0")/.."
F=out/ssm-patch.mp4
mkdir -p review/qa keyframes
rm -f review/qa/*.jpg keyframes/*.png
python3 -c '
import json; c=json.load(open("cues.json"))["cues"]
for k,v in c.items(): print("%.1f:%s" % (v["s"]+0.7*v["d"], k))' > review/tmp/qa-times.txt
while IFS= read -r spec; do
  t=${spec%%:*}; id=${spec##*:}
  ffmpeg -v error -y -ss "$t" -i "$F" -frames:v 1 -vf scale=1280:720 -q:v 3 "review/qa/t$(printf '%06.1f' "$t")-$id.jpg"
done < review/tmp/qa-times.txt
python3 -c '
import json; s=json.load(open("script.json")); c=json.load(open("cues.json"))["cues"]
for n,ch in enumerate(s["chapters"],1):
    v=c[ch["start"]]; print("%.1f:%02d-%s" % (v["s"]+0.8*v["d"], n, ch["shot"]))' > review/tmp/kf-times.txt
while IFS= read -r spec; do
  t=${spec%%:*}; n=${spec##*:}
  ffmpeg -v error -y -ss "$t" -i "$F" -frames:v 1 "keyframes/$n.png"
done < review/tmp/kf-times.txt
ls review/qa keyframes
