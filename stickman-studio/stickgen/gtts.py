"""Expressive narration with Google's Gemini speech models: each line carries an acting direction.

Needs a Google AI Studio key (inside the cloud session the proxy supplies it).

Notes from testing (2026-11-17):
- The "3.8" models add a short, very loud burst after the last word of every clip. clean() removes it.
- "3.1-flash-tts-preview" does not. Free tier: about 10 requests per day per model, so say_batch() reads several
  lines in ONE request and splits the audio back into lines at the long silences, which also keeps one voice.
"""
import base64
import hashlib
import json
import os
import subprocess
import time
import wave
from pathlib import Path

import numpy as np

from .tts import RATE, wav_duration

CACHE = Path(__file__).resolve().parent.parent / ".cache" / "gtts"
MODEL = "gemini-3.8-flash-tts"
PROFILE = ("# AUDIO PROFILE: Fast-talking, charismatic young male narrator of animated YouTube Shorts. "
           "Quick, punchy pace, natural breaths, never flat.\n")
CALM_PROFILE = ("# AUDIO PROFILE: A clear, warm, confident male narrator of educational animated videos. "
                "Slow and deliberate, about 130 words per minute, crisp enunciation, a clear pause of about half a "
                "second between sentences, never rushed, even on exciting lines.\n")


class DailyQuota(RuntimeError):
    pass


def _key(parts):
    return hashlib.sha1(json.dumps(parts).encode()).hexdigest()[:16]


def _call(model, prompt, voice):
    """One speech request. Returns raw 24 kHz mono 16-bit PCM bytes."""
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    last = ""
    for attempt in range(5):
        r = subprocess.run(["curl", "-sS", "-m", "240", "-H", f"x-goog-api-key: {os.environ.get('GEMINI_API_KEY', 'placeholder')}",
                            "-H", "Content-Type: application/json", "-d", json.dumps(body), url],
                           capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
            return base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
        except Exception:
            last = (r.stdout or r.stderr)[:300]
            if "per day" in (r.stdout or "") or "PerDay" in (r.stdout or ""):
                raise DailyQuota("free daily limit reached")
            time.sleep(8 * (attempt + 1))
    raise RuntimeError(f"Gemini speech failed: {last}")


def _write_trimmed(pcm, dst):
    """24 kHz PCM -> wav at RATE with leading/trailing silence removed."""
    raw = Path(str(dst) + ".pcm")
    raw.write_bytes(pcm)
    trim = "silenceremove=start_periods=1:start_threshold=-45dB"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", str(raw),
                    "-af", f"{trim},areverse,{trim},areverse", "-ar", str(RATE), str(dst)], check=True)
    raw.unlink()


def _read(path):
    with wave.open(str(path)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768, w.getframerate()


def _write(path, x, sr):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


def _runs(x, sr, thresh_db=-38, merge=0.12, win=0.01):
    """Speech runs as (start_s, end_s, mean_db), merging gaps shorter than `merge` seconds."""
    n = int(win * sr)
    m = len(x) // n
    db = 20 * np.log10(np.sqrt((x[:m * n].reshape(m, n) ** 2).mean(axis=1)) + 1e-9)
    on, runs, start = db > thresh_db, [], None
    for i, s in enumerate(on):
        if s and start is None:
            start = i
        if not s and start is not None:
            runs.append([start, i]); start = None
    if start is not None:
        runs.append([start, m])
    merged = []
    for r in runs:
        if merged and (r[0] - merged[-1][1]) * win < merge:
            merged[-1][1] = r[1]
        else:
            merged.append(r)
    return [(a * win, b * win, float(10 * np.log10(np.mean(10 ** (db[a:b] / 10))))) for a, b in merged], db


def clean(wav):
    """Remove the loud end-of-clip burst, trim silence, add short fades. Cached as <name>_c.wav."""
    wav = Path(wav)
    out = wav.with_name(wav.stem + "_c.wav")
    if out.exists():
        return out, wav_duration(out)
    x, sr = _read(wav)
    runs, _ = _runs(x, sr)
    if len(runs) >= 2:
        *body, tail = runs
        body_db = float(np.median([r[2] for r in body]))
        if tail[1] - tail[0] <= 0.35 and tail[0] - body[-1][1] >= 0.12 and tail[2] > body_db + 8:
            x = x[:int((body[-1][1] + 0.04) * sr)]            # drop the burst
            runs, _ = _runs(x, sr)
    if runs:
        x = x[max(0, int((runs[0][0] - 0.03) * sr)):int((runs[-1][1] + 0.05) * sr)]
    f_in, f_out = int(0.008 * sr), int(0.045 * sr)
    x = x.copy()
    x[:f_in] *= np.linspace(0, 1, f_in)
    x[-f_out:] *= np.linspace(1, 0, f_out)
    _write(out, x, sr)
    return out, wav_duration(out)


def say(text, direction="", voice="Fenrir", model=MODEL, profile=None):
    """Return (wav_path, seconds) for one narration line. `model` may be a list (tried in order on daily limits)."""
    if isinstance(model, (list, tuple)):
        for m in model:                                    # reuse anything already generated first
            if (CACHE / f"{_key([m, voice, direction, text] + ([profile] if profile else []))}.wav").exists():
                return say(text, direction, voice, m, profile)
        errors = []
        for m in model:
            try:
                return say(text, direction, voice, m, profile)
            except DailyQuota as e:
                errors.append(f"{m}: {e}")
        raise DailyQuota("; ".join(errors))
    CACHE.mkdir(parents=True, exist_ok=True)
    wav = CACHE / f"{_key([model, voice, direction, text] + ([profile] if profile else []))}.wav"
    if wav.exists():
        return wav, wav_duration(wav)
    prompt = f"{profile or PROFILE}# DIRECTOR'S NOTES\nDeliver this line: {direction or 'energetic and clear'}.\n# TRANSCRIPT\n{text}"
    _write_trimmed(_call(model, prompt, voice), wav)
    return wav, wav_duration(wav)


def _split(pcm, n, lens):
    """Split one recording of n takes at pauses. The pauses are chosen from where each line should end, judged by
    how long the line is, with a bonus for longer silences. lens: characters per line. Returns n PCM byte strings."""
    if n == 1:
        return [pcm]
    x = np.frombuffer(pcm, dtype=np.int16).astype(np.float64) / 32768
    runs, _ = _runs(x, 24000, thresh_db=-40, merge=0.0)
    gaps = [(runs[i][1], runs[i + 1][0]) for i in range(len(runs) - 1) if runs[i + 1][0] - runs[i][1] >= 0.25]
    if len(gaps) < n - 1:
        raise ValueError(f"only {len(gaps)} pauses found for {n} takes")
    t0, t1 = runs[0][0], runs[-1][1]
    cum = np.cumsum(lens) / float(sum(lens))
    pred = [t0 + f * (t1 - t0) for f in cum[:-1]]
    mid = [(a + b) / 2 for a, b in gaps]
    cost = lambda k, j: abs(mid[j] - pred[k]) - 1.5 * min(gaps[j][1] - gaps[j][0], 2.0)
    # dynamic programme over increasing gap indices
    best = [[(cost(0, j), -1) for j in range(len(gaps))]]
    for k in range(1, n - 1):
        row = []
        for j in range(len(gaps)):
            cands = [(best[k - 1][i][0], i) for i in range(j)]
            row.append((cost(k, j) + min(cands)[0], min(cands)[1]) if cands else (float("inf"), -1))
        best.append(row)
    j = min(range(len(gaps)), key=lambda j: best[-1][j][0])
    chosen = []
    for k in range(n - 2, -1, -1):
        chosen.append(j)
        j = best[k][j][1]
    chosen.reverse()
    bounds, prev = [], t0
    for g in chosen:
        bounds.append((prev, gaps[g][0]))
        prev = gaps[g][1]
    bounds.append((prev, t1))
    takes = []
    for a, b in bounds:
        if b - a < 0.5:
            raise ValueError("a take came out shorter than half a second")
        seg = x[max(0, int((a - 0.05) * 24000)):int((b + 0.1) * 24000)]
        takes.append((seg * 32767).astype(np.int16).tobytes())
    return takes


def say_batch(lines, voice="Fenrir", model=MODEL, profile=CALM_PROFILE, keep_partial=False):
    """Read several lines in ONE request, then split. lines: [(text, direction)]. Returns [(wav, seconds)]."""
    if isinstance(model, (list, tuple)):
        errors = []
        for m in model:
            try:
                return say_batch(lines, voice, m, profile, keep_partial)
            except DailyQuota as e:
                errors.append(f"{m}: {e}")
        raise DailyQuota("; ".join(errors))
    CACHE.mkdir(parents=True, exist_ok=True)
    bkey = _key([model, voice, profile, lines])
    paths = [CACHE / f"b{bkey}_{i}.wav" for i in range(len(lines))]
    if all(p.exists() for p in paths):
        return [(p, wav_duration(p)) for p in paths]
    tones = "\n".join(f"- Take {i + 1}: {d or 'clear and natural'}" for i, (_, d) in enumerate(lines))
    prompt = (f"{profile}# DIRECTOR'S NOTES\nThis is {len(lines)} separate takes, read in order. After each take, stay "
              f"completely silent for three full seconds before the next one. Keep the same slow, steady pace in every take. "
              f"Never read these notes aloud.\n"
              f"Tone of each take:\n{tones}\n# TRANSCRIPT\n" + "\n\n".join(t for t, _ in lines))
    last = ""
    for attempt in range(3):                      # the model sometimes cuts a long request short: check and retry
        try:
            takes = _split(_call(model, prompt, voice), len(lines), [len(t) for t, _ in lines])
        except ValueError as e:
            last = str(e)
            continue
        for p, pcm in zip(paths, takes):
            _write_trimmed(pcm, p)
        bad = [i + 1 for i, (t, _) in enumerate(lines)
               if len(t.split()) >= 4 and not 85 <= len(t.split()) / wav_duration(paths[i]) * 60 <= 250]
        if not bad:
            return [(p, wav_duration(p)) for p in paths]
        last = f"takes {bad} came out too fast or too slow"
        if keep_partial and len(bad) <= 2:       # keep the good takes; the caller re-records only the bad lines
            print(f"    kept batch; re-record takes {bad} separately")
            return [(p, wav_duration(p)) for p in paths]
        for p in paths:
            p.unlink(missing_ok=True)
    raise ValueError(f"narration batch failed after 3 tries: {last}")


def stretch(wav, factor):
    """Time-stretch a clip without changing pitch (factor < 1 slows it down). Cached next to the original."""
    factor = max(0.75, min(1.0, factor))          # slowing more than this sounds artificial
    out = wav.with_name(f"{wav.stem}_x{int(round(factor * 100))}.wav")
    if not out.exists():
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-af", f"atempo={factor:.3f}",
                        "-ar", str(RATE), str(out)], check=True)
    return out, wav_duration(out)
