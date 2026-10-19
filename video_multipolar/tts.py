"""Genera la narración con ElevenLabs: un mp3 por frase + audio/durations.json.

Uso:  ELEVENLABS_API_KEY=... python tts.py [--voice VOICE_ID] [--force]
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(ROOT, "audio")
API = "https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128"


def duration(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                   "-of", "csv=p=0", path])
    return float(out)


def synth(key, voice, text, prev_text, next_text, path):
    body = {
        "text": text,
        "model_id": os.environ.get("ELEVEN_MODEL", "eleven_multilingual_v2"),
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.15,
                           "use_speaker_boost": True},
        "previous_text": prev_text,
        "next_text": next_text,
    }
    req = urllib.request.Request(API.format(voice=voice), data=json.dumps(body).encode(),
                                 headers={"xi-api-key": key, "Content-Type": "application/json",
                                          "Accept": "audio/mpeg"})
    with urllib.request.urlopen(req, timeout=180) as r, open(path, "wb") as f:
        f.write(r.read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default=os.environ.get("ELEVEN_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb"))
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        sys.exit("Falta ELEVENLABS_API_KEY")
    narr = json.load(open(os.path.join(ROOT, "narration.json"), encoding="utf-8"))
    flat = [(f"{s}_{k}", t) for s, segs in narr.items() for k, t in segs.items()]
    os.makedirs(AUDIO, exist_ok=True)
    durs = {}
    for i, (name, text) in enumerate(flat):
        path = os.path.join(AUDIO, f"{name}.mp3")
        if args.force or not os.path.exists(path):
            prev_t = flat[i - 1][1] if i > 0 else ""
            next_t = flat[i + 1][1] if i + 1 < len(flat) else ""
            print("TTS", name, flush=True)
            synth(key, args.voice, text, prev_t, next_t, path)
        durs[name] = duration(path)
    json.dump(durs, open(os.path.join(AUDIO, "durations.json"), "w"), indent=1)
    print(f"Total narración: {sum(durs.values()):.1f} s")


if __name__ == "__main__":
    main()
