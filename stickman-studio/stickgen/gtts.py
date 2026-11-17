"""Expressive narration with Google's Gemini speech model: each line carries an acting direction.

Needs a Google AI Studio API key in GEMINI_API_KEY (inside the cloud session the proxy supplies it).
"""
import base64
import hashlib
import json
import os
import subprocess
import time
from pathlib import Path

from .tts import RATE, wav_duration

CACHE = Path(__file__).resolve().parent.parent / ".cache" / "gtts"
MODEL = "gemini-3.8-flash-tts"
PROFILE = ("# AUDIO PROFILE: Fast-talking, charismatic young male narrator of animated YouTube Shorts. "
           "Quick, punchy pace, natural breaths, never flat.\n")


def say(text, direction="", voice="Fenrir", model=MODEL):
    """Return (wav_path, seconds) for one narration line, trimmed of leading and trailing silence."""
    CACHE.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha1(json.dumps([model, voice, direction, text]).encode()).hexdigest()[:16]
    wav = CACHE / f"{key}.wav"
    if wav.exists():
        return wav, wav_duration(wav)
    prompt = f"{PROFILE}# DIRECTOR'S NOTES\nDeliver this line: {direction or 'energetic and clear'}.\n# TRANSCRIPT\n{text}"
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    last = ""
    for attempt in range(5):
        r = subprocess.run(["curl", "-sS", "-m", "180", "-H", f"x-goog-api-key: {os.environ.get('GEMINI_API_KEY', 'placeholder')}",
                            "-H", "Content-Type: application/json", "-d", json.dumps(body), url],
                           capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
            data = d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
            break
        except Exception:
            last = (r.stdout or r.stderr)[:300]
            time.sleep(8 * (attempt + 1))
    else:
        raise RuntimeError(f"Gemini speech failed: {last}")
    pcm = CACHE / f"{key}.pcm"
    pcm.write_bytes(base64.b64decode(data))
    trim = "silenceremove=start_periods=1:start_threshold=-45dB"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", str(pcm),
                    "-af", f"{trim},areverse,{trim},areverse", "-ar", str(RATE), str(wav)], check=True)
    pcm.unlink()
    return wav, wav_duration(wav)
