#!/bin/bash
# Renderiza los 12 clips verticales (1080x1920, 60 fps, sin audio) en 4 procesos paralelos.
cd "$(dirname "$0")"
MANIM=${MANIM:-manim}
R=${RES:-1080,1920}; F=${FPS:-60}
run() { # $1 = fichero, resto = escenas
  f=$1; shift
  for s in "$@"; do
    $MANIM -r $R --fps $F --disable_caching --media_dir build/m_$s -o $s $f $s > build/log_$s.txt 2>&1 || echo "FALLO $s"
  done
}
mkdir -p build clips
run clips_a.py C01_AnguloSolido C04_Delta C06_Circulacion &
run clips_a.py C02_AnguloTotal C05_DivDelta C03_Gauss &
run clips_b.py C07_Normal C10_Anillo C12_Lineas &
run clips_b.py C08_Tangencial C09_Potencial C11_Disco &
wait
for f in build/m_*/videos/*/*/C*.mp4; do
  n=$(basename $f)
  ffmpeg -nostdin -loglevel error -y -i "$f" -an -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p \
    -movflags +faststart "clips/$n"
done
ls -la clips
