"""Free text-to-speech with caching.

Backends, tried in order when voice backend is "auto":
  edge   - Microsoft Edge neural voices via the `edge-tts` package (free, needs internet)
  espeak - espeak-ng (offline, robotic; fallback only)

synth() returns (wav_path, words) where words is [(text, start_s, end_s), ...].
"""
import asyncio
import hashlib
import json
import re
import shutil
import subprocess
import wave
from pathlib import Path

RATE = 44100
CACHE = Path(__file__).resolve().parent.parent / ".cache" / "tts"


def wav_duration(path):
    with wave.open(str(path)) as w:
        return w.getnframes() / w.getframerate()


def _to_wav(src, dst):
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-ac", "1", "-ar", str(RATE),
         "-af", "silenceremove=start_periods=1:start_threshold=-50dB", str(dst)],
        check=True,
    )


def _edge(text, voice, rate, pitch, tmp):
    import os
    import certifi
    import edge_tts

    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    ca = os.environ.get("SSL_CERT_FILE") or "/root/.ccr/ca-bundle.crt"
    if proxy and os.path.exists(ca):      # behind a TLS-inspecting proxy
        certifi.where = lambda: ca

    async def run():
        words, audio = [], bytearray()
        com = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, boundary="WordBoundary", proxy=proxy)
        async for chunk in com.stream():
            if chunk["type"] == "audio":
                audio.extend(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                start = chunk["offset"] / 1e7
                words.append((chunk["text"], start, start + chunk["duration"] / 1e7))
        return bytes(audio), words

    audio, words = asyncio.run(run())
    if not audio:
        raise RuntimeError("edge-tts returned no audio")
    tmp.write_bytes(audio)
    return words


def _espeak(text, tmp):
    exe = shutil.which("espeak-ng") or shutil.which("espeak")
    if not exe:
        raise RuntimeError("espeak-ng is not installed")
    subprocess.run([exe, "-v", "en-us", "-s", "160", "-w", str(tmp), text], check=True)
    return None


def _estimate_words(text, duration):
    """Spread words across the clip in proportion to their length."""
    tokens = text.split()
    weights = [len(re.sub(r"\W", "", t)) + 1.5 + (2 if t[-1] in ".,!?;:" else 0) for t in tokens]
    total, t, out = sum(weights), 0.0, []
    for tok, w in zip(tokens, weights):
        d = duration * w / total
        out.append((tok, t, t + d))
        t += d
    return out


def synth(text, voice="en-US-AndrewNeural", rate="+5%", backend="auto", pitch="+0Hz"):
    CACHE.mkdir(parents=True, exist_ok=True)
    order = ["edge", "espeak"] if backend == "auto" else [backend]
    errors = []
    for b in order:
        key = hashlib.sha1(json.dumps([b, voice, rate, pitch, text]).encode()).hexdigest()[:16]
        wav, meta = CACHE / f"{key}.wav", CACHE / f"{key}.json"
        if wav.exists() and meta.exists():
            return wav, [tuple(w) for w in json.loads(meta.read_text())], b
        tmp = CACHE / f"{key}.tmp"
        try:
            words = _edge(text, voice, rate, pitch, tmp) if b == "edge" else _espeak(text, tmp)
            _to_wav(tmp, wav)
        except Exception as e:  # try the next backend
            errors.append(f"{b}: {e}")
            continue
        finally:
            tmp.unlink(missing_ok=True)
        if not words:
            words = _estimate_words(text, wav_duration(wav))
        meta.write_text(json.dumps(words))
        return wav, words, b
    raise RuntimeError("No TTS backend worked:\n  " + "\n  ".join(errors))
