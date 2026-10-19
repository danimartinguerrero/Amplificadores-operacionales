"""Corta los mejores momentos del vídeo en clips verticales (1080x1920, sin audio) para TikTok.

Uso: python clips.py   (necesita desarrollo_multipolar.mp4 ya montado)
"""
import os
import subprocess

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "desarrollo_multipolar.mp4")
OUT = os.path.join(ROOT, "clips")
TMP = os.path.join(ROOT, "build", "clips")
W, H = 1080, 1920
BG = (14, 17, 23)
F_BOLD = "/usr/share/fonts/truetype/cmu/cmunbx.ttf"
F_REG = "/usr/share/fonts/truetype/cmu/cmunrm.ttf"

# (nombre, título, subtítulo, [(inicio, fin, ancho de recorte[, recorte superior]) en px del original 1920x1080])
CLIPS = [
    ("01_nube_de_carga", "¿Cómo se calcula el potencial\nde una nube de carga?", "Una integral distinta para cada punto…",
     [(5.0, 38.0, 1500)]),
    ("02_legendre", "1/R como suma de\npolinomios de Legendre", "Con 4 términos ya es casi exacta",
     [(182.0, 214.0, 1920)]),
    ("03_dipolo", "Así es el campo\nde un dipolo", "Equipotenciales y líneas: siempre a 90°",
     [(357.0, 387.0, 970, 110)]),
    ("04_cuadrupolo", "El cuadrupolo:\ncuatro lóbulos y un cono", "Q = 0, p = 0… y aun así hay campo",
     [(467.0, 484.0, 1920), (484.0, 497.0, 970, 110)]),
    ("05_tres_terminos", "Monopolo, dipolo\ny cuadrupolo", "El potencial, capa a capa",
     [(517.0, 551.0, 1920)]),
    ("06_cuantos_terminos", "¿Cuántos términos\nnecesitas?", "A 10 veces el tamaño: con 3 basta (1 %)",
     [(580.0, 612.0, 1920)]),
]


def overlay(title, subtitle, idx, n, path):
    im = Image.new("RGBA", (W, H), BG + (255,))
    d = ImageDraw.Draw(im)
    kick = ImageFont.truetype(F_REG, 34)
    size = 80
    while True:  # ajusta el título al ancho
        ft = ImageFont.truetype(F_BOLD, size)
        if d.multiline_textbbox((0, 0), title, font=ft, spacing=14)[2] <= W - 110 or size <= 48:
            break
        size -= 2
    fs = ImageFont.truetype(F_REG, 44)
    k = f"DESARROLLO MULTIPOLAR  ·  {idx}/{n}"
    d.text((W / 2, 190), k, font=kick, fill=(139, 147, 161), anchor="mm")
    d.multiline_text((W / 2, 330), title, font=ft, fill=(255, 255, 255), anchor="mm", align="center", spacing=14)
    d.line([(W / 2 - 60, 455), (W / 2 + 60, 455)], fill=(255, 255, 0), width=4)
    d.text((W / 2, 530), subtitle, font=fs, fill=(255, 221, 85), anchor="mm")
    im.save(path)


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(TMP, exist_ok=True)
    n = len(CLIPS)
    for i, (name, title, sub, pieces) in enumerate(CLIPS, 1):
        ov = os.path.join(TMP, f"{name}.png")
        overlay(title, sub, i, n, ov)
        # cada tramo: recorte centrado, escalado a 1080 de ancho
        parts = []
        for j, (t0, t1, cw, *top) in enumerate(pieces):
            top = top[0] if top else 0
            ch = 1080 - top
            p = os.path.join(TMP, f"{name}_{j}.mp4")
            vh = round(1080 * ch / cw / 2) * 2
            run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", str(t0), "-t", str(t1 - t0), "-i", SRC,
                 "-an", "-vf", # tapa el rótulo de sección de la esquina superior izquierda
                 f"drawbox=x=0:y=0:w=780:h=115:color=0x0e1117:t=fill,crop={cw}:{ch}:(iw-{cw})/2:{top},scale=1080:{vh}:flags=lanczos,"
                 f"pad=1080:1080:0:(1080-{vh})/2:color=0x0e1117,setsar=1",
                 "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", p])
            parts.append(p)
        lst = os.path.join(TMP, f"{name}.txt")
        open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
        joined = os.path.join(TMP, f"{name}_joined.mp4")
        run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
             "-c", "copy", joined])
        dur = sum(p[1] - p[0] for p in pieces)
        out = os.path.join(OUT, f"{name}.mp4")
        # lienzo vertical: rótulos arriba/abajo y el vídeo (1080x1080) en el centro
        run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-loop", "1", "-i", ov, "-i", joined,
             "-filter_complex",
             f"[0:v][1:v]overlay=0:600:shortest=1,fade=t=in:st=0:d=0.5,fade=t=out:st={dur - 0.6:.2f}:d=0.6,format=yuv420p[v]",
             "-map", "[v]", "-an", "-r", "60", "-c:v", "libx264", "-crf", "18", "-preset", "slow",
             "-profile:v", "high", "-movflags", "+faststart", "-t", f"{dur:.2f}", out])
        print(out)


if __name__ == "__main__":
    main()
