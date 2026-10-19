"""Construye los subtítulos (desarrollo_multipolar.srt) a partir de los tiempos de cada escena."""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
ORDER = ["S01_Intro", "S02_Geometria", "S03_Legendre", "S04_Desarrollo", "S05_Monopolo",
         "S06_Dipolo", "S07_Cuadrupolo", "S08_Resumen", "S09_Error"]


def ts(t):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int((s % 1) * 1000):03d}"


def split(text, maxlen=84):
    """Trocea en frases cortas (corta en puntos y, si hace falta, en comas o espacios)."""
    import re
    parts = re.split(r"(?<=[.:;?!])\s+", text)
    out = []
    for p in parts:
        while len(p) > maxlen:
            cut = max(p.rfind(", ", 0, maxlen), p.rfind(": ", 0, maxlen))
            if cut < maxlen // 3:
                cut = p.rfind(" ", 0, maxlen)
            out.append(p[:cut + 1].strip())
            p = p[cut + 1:].strip()
        if p:
            out.append(p)
    return out


def main():
    offset, n, out = 0.0, 1, []
    for k, s in enumerate(ORDER):
        data = json.load(open(os.path.join(ROOT, "build", "subs", f"{s}.json")))
        for seg in data["subs"]:
            chunks = split(seg["text"])
            total = sum(len(c) for c in chunks)
            t = seg["start"]
            for c in chunks:
                dt = (seg["end"] - seg["start"]) * len(c) / total
                out.append(f"{n}\n{ts(offset + t)} --> {ts(offset + t + dt)}\n{c}\n")
                t += dt
                n += 1
        # duración real del clip renderizado
        part = os.path.join(ROOT, "build", f"part_{k}.mp4")
        if os.path.exists(part):
            offset += float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                                     "-of", "csv=p=0", part]))
        else:
            offset += data["total"]
    open(os.path.join(ROOT, "desarrollo_multipolar.srt"), "w", encoding="utf-8").write("\n".join(out))


if __name__ == "__main__":
    main()
