#!/bin/bash
v=$1; out=$2; n=${3:-12}
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v")
fps=$(python3 -c "print($n/$d)")
ffmpeg -nostdin -loglevel error -y -i "$v" -vf "fps=$fps,scale=240:-1,tile=${n}x1" -frames:v 1 "$out"
echo "$d s"
