# Desarrollo multipolar — vídeo (estilo 3Blue1Brown)

Vídeo explicativo del desarrollo multipolar del potencial (Tema 2, Electromagnetismo I),
hecho con [Manim Community](https://www.manim.community/) y narrado con ElevenLabs.

| Fichero | Qué es |
|---|---|
| `narration.json` | Guion de la narración, frase a frase por escena |
| `common.py` | Estilo, sincronización voz–animación (`VScene.say`) y utilidades (curvas de campo, mapas de potencial) |
| `scenes_a.py`, `scenes_b.py` | Las 9 escenas |
| `tts.py` | Genera `audio/*.mp3` y `audio/durations.json` con la API de ElevenLabs |
| `build.sh` | Renderiza y monta `desarrollo_multipolar.mp4` (+ `.srt`) |

## Cómo generarlo

```bash
pip install manim            # requiere LaTeX, ffmpeg y pango
export ELEVENLABS_API_KEY=... # opcional: ELEVEN_VOICE_ID=... para otra voz
python tts.py                # crea la narración (una llamada por frase)
./build.sh                   # 1080p60; QUALITY=l ./build.sh para un borrador rápido
```

Cada escena se ajusta sola a la duración real de cada frase de audio. Sin `audio/`,
se renderiza con duraciones estimadas (vídeo mudo, útil como borrador).
