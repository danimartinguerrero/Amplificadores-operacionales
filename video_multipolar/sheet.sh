#!/bin/bash
# sheet.sh video.mp4 out.png N  -> contact sheet de N fotogramas
v=$1; out=$2; n=${3:-12}
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v")
fps=$(python3 -c "print($n/$d)")
ffmpeg -loglevel error -y -i "$v" -vf "fps=$fps,scale=480:-1,tile=4x$(( (n+3)/4 ))" -frames:v 1 "$out"
echo "$d s"
