#!/bin/bash
# usage: sheet.sh name t1,t2,...  (up to 8 per row)
cd "$(dirname "$0")"; rm -rf snaps_$1; node snap.js $2 snaps_$1 >/dev/null 2>snaps_err.txt; cat snaps_err.txt | head -3
n=$(ls snaps_$1/*.jpg | wc -l); cols=$(( n<5 ? n : 5 )); rows=$(( (n+cols-1)/cols ))
ffmpeg -loglevel error -y -pattern_type glob -i "snaps_$1/*.jpg" -vf "scale=324:576,tile=${cols}x${rows}:padding=6:color=black" -frames:v 1 ../sheet_$1.jpg
