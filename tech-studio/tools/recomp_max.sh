#!/bin/bash
# Re-render Max's overlay frames for finished projects and re-composite over the existing scene renders.
# Usage: tools/recomp_max.sh <project> <final-name> [crf]
set -e
cd "$(dirname "$0")/../hf/$1"
rm -rf maxframes && node max_render.cjs > maxrender.log 2>&1
ffmpeg -y -loglevel error -i out/scenes.mp4 -framerate 30 -i maxframes/m%04d.png -filter_complex "[0:v][1:v]overlay=0:0:eof_action=pass[v];[0:a]loudnorm=I=-14:TP=-1.5:LRA=11[a]" -map "[v]" -map "[a]" -c:v libx264 -crf ${3:-18} -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart out/final-legs.mp4
cp out/final-legs.mp4 "../../out/$2"
echo "done $1 -> $2"
