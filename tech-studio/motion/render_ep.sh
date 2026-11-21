#!/bin/bash
# Render one exported episode: ./render_ep.sh <timeline-id> [vertical]
set -e
cd "$(dirname "$0")"
E=$PWD/episodes/$1
SIZE=""; [ "$2" = "vertical" ] && SIZE="--w 1080 --h 1920"
CHROME_PATH=${CHROME_PATH:-/opt/pw-browsers/chromium} bun scripts/render.ts video --ep "$E" $SIZE --fps 30 --samples 2 --shutter 0.5 --crf 18 --out "$E/out/$1.mp4"
ffmpeg -y -loglevel error -i "$E/out/$1.mp4" -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 192k "$E/out/$1-final.mp4"
echo "$E/out/$1-final.mp4"
