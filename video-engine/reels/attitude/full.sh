#!/bin/bash
# full render: 4 workers -> concat -> mux voice + sfx
cd "$(dirname "$0")"; O=../out; mkdir -p $O; N=2038; W=4; step=$(( (N+W-1)/W ))
for i in $(seq 0 $((W-1))); do a=$((i*step)); b=$(( (i+1)*step < N ? (i+1)*step : N )); node render.js $a $b $O/seg$i.mp4 > $O/log$i.txt 2>&1 & done; wait
printf "file 'seg%d.mp4'\n" 0 1 2 3 > $O/list.txt
ffmpeg -loglevel error -y -f concat -safe 0 -i $O/list.txt -c copy $O/video.mp4
ffmpeg -loglevel error -y -i $O/video.mp4 -i ../src.mp4 -i sfx.wav \
  -filter_complex "[1:a]aresample=48000[v];[2:a]aresample=48000,pan=stereo|c0=c0|c1=c0[s];[v][s]amix=inputs=2:duration=first:normalize=0[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart -shortest $O/reels.mp4
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of compact $O/reels.mp4
cat $O/log*.txt | grep -i err
