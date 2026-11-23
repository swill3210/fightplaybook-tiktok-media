#!/usr/bin/env bash
# Mux the voice track, run QC, and build a side by side comparison.
# usage: finish.sh <render_dir> <voice_source(mp4 or audio)> [reference_video_for_side_by_side]
set -euo pipefail
R="$1"; VOICE="$2"; REF="${3:-}"
HERE="$(cd "$(dirname "$0")" && pwd)"
FONT="$HERE/node_modules/@fontsource/bebas-neue/files/bebas-neue-latin-400-normal.woff"
ffmpeg -v error -y -i "$R/video_silent.mp4" -i "$VOICE" -map 0:v -map 1:a:0 -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest "$R/final.mp4"
python3 "$HERE/qc.py" "$R" "$R/final.mp4" --audio "$VOICE" || echo "QC reported blocking issues"
if [ -n "$REF" ]; then
  ffmpeg -v error -y -i "$REF" -i "$R/final.mp4" -filter_complex \
    "[0:v]scale=540:960,setsar=1,drawtext=fontfile=$FONT:text='BEFORE':x=(w-tw)/2:y=24:fontsize=56:fontcolor=white:borderw=5:bordercolor=black[a];\
     [1:v]scale=540:960,setsar=1,drawtext=fontfile=$FONT:text='AFTER':x=(w-tw)/2:y=24:fontsize=56:fontcolor=white:borderw=5:bordercolor=black[b];\
     [a][b]hstack=2[v]" -map "[v]" -map 1:a -c:v libx264 -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k "$R/side_by_side.mp4"
fi
ls -la "$R"
