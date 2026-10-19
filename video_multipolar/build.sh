#!/bin/bash
# Renderiza todas las escenas y las monta en un único vídeo.
#   ./build.sh            -> 1080p60 (calidad final)
#   QUALITY=l ./build.sh  -> 480p15 (borrador rápido)
set -euo pipefail
cd "$(dirname "$0")"
MANIM=${MANIM:-manim}
Q=${QUALITY:-h}
case $Q in l) RES=480p15;; m) RES=720p30;; h) RES=1080p60;; k) RES=2160p60;; esac
SCENES_A="S01_Intro S02_Geometria S03_Legendre"
SCENES_B="S04_Desarrollo S05_Monopolo S06_Dipolo S07_Cuadrupolo S08_Resumen S09_Error"

$MANIM -q$Q --disable_caching --media_dir build/media scenes_a.py $SCENES_A
$MANIM -q$Q --disable_caching --media_dir build/media scenes_b.py $SCENES_B

: > build/list.txt
for s in $SCENES_A; do echo "file 'media/videos/scenes_a/$RES/$s.mp4'" >> build/list.txt; done
for s in $SCENES_B; do echo "file 'media/videos/scenes_b/$RES/$s.mp4'" >> build/list.txt; done

# Une las escenas (re-codificando el audio para que no haya saltos entre clips;
# las escenas sin audio reciben una pista silenciosa)
parts=()
i=0
while read -r _ f; do
  f=${f//\'/}
  out=build/part_$i.mp4
  if ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "build/$f" | grep -q .; then
    ffmpeg -loglevel error -y -i "build/$f" -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 "$out"
  else
    ffmpeg -loglevel error -y -i "build/$f" -f lavfi -i anullsrc=r=48000:cl=stereo -shortest \
      -c:v copy -c:a aac -b:a 192k "$out"
  fi
  parts+=("$out"); i=$((i+1))
done < build/list.txt
printf "file '%s'\n" "${parts[@]#build/}" > build/parts.txt
ffmpeg -loglevel error -y -f concat -safe 0 -i build/parts.txt -c copy build/concat.mp4
# Normaliza el volumen de la voz
ffmpeg -loglevel error -y -i build/concat.mp4 -c:v copy -af loudnorm=I=-16:TP=-1.5:LRA=11 -c:a aac -b:a 192k \
  desarrollo_multipolar.mp4
python3 make_srt.py
echo "Listo: desarrollo_multipolar.mp4"
