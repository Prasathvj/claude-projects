#!/bin/bash
# Loudness-normalise a render for YouTube (-14 LUFS, -1.5 dBTP); video stream is copied untouched.
# Usage: tools/finish.sh out/<name>.mp4  -> out/<name>-final.mp4
set -e
in="$1"; out="${in%.mp4}-final.mp4"
ffmpeg -y -loglevel error -i "$in" -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 192k "$out"
echo "$out"
