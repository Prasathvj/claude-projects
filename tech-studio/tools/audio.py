"""Audio for tech-studio episodes: Gemini narration, a timed beat timeline, a synthesized SFX library and a music bed.

Usage:
  python3 tools/audio.py sfx                         # (re)build public/sfx/*.wav
  python3 tools/audio.py episode episodes/ep01/short.json
      -> public/<ep>/<id>-vo.wav, public/<ep>/<id>-music.wav, src/episodes/<id>.timeline.json

Narration reuses stickman-studio/stickgen/gtts.py (free Gemini TTS quotas, several lines per request).
Word timings are estimated inside each line (syllable-weighted), which is accurate enough for 1-3 word captions.
"""
import json
import math
import re
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "stickman-studio"))
from stickgen import gtts  # noqa: E402

SR = 44100
MODELS = ["gemini-3.1-flash-tts-preview", "gemini-3.8-flash-tts", "gemini-2.5-flash-preview-tts", "gemini-3.8-flash-lite-tts"]
PROFILES = {
    "fast": ("# AUDIO PROFILE: Fast-talking, charismatic male narrator of punchy tech YouTube Shorts. Quick, confident, "
             "about 175 words per minute, crisp consonants, natural breaths, a hint of a smile, never flat or robotic.\n"),
    "explainer": ("# AUDIO PROFILE: Energetic, clear male narrator of a fast-paced tech explainer video. About 160 words per "
                  "minute, confident and curious, crisp enunciation, short natural pauses between sentences, never flat.\n"),
}
TARGET_WPM = {"fast": 172, "explainer": 158}


# ------------------------------------------------------------------ wav helpers
def read(path):
    with wave.open(str(path)) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
        if w.getnchannels() == 2:
            x = x.reshape(-1, 2).mean(axis=1)
        if w.getframerate() != SR:
            raise ValueError(f"{path}: expected {SR} Hz")
        return x


def write(path, x):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


def tempo(src, factor, dst):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-af", f"atempo={factor:.4f}", "-ar", str(SR),
                    "-ac", "1", str(dst)], check=True)


# ------------------------------------------------------------------ SFX synth
def _noise(n, seed=0):
    return np.random.default_rng(seed).standard_normal(n)


def _band(x, lo, hi):
    spec = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    spec *= np.exp(-0.5 * ((np.log(np.maximum(f, 1)) - math.log(math.sqrt(lo * hi))) / (math.log(hi / lo) / 2.4)) ** 2)
    out = np.fft.irfft(spec, len(x))
    return out / (np.abs(out).max() + 1e-9)


def _t(sec):
    return np.arange(int(sec * SR)) / SR


def _norm(x, peak):
    return x / (np.abs(x).max() + 1e-9) * peak


def sfx_library():
    L = {}
    t = _t(0.45)
    L["whoosh"] = _norm(_band(_noise(len(t), 1), 400, 6000) * np.sin(np.pi * (t / t[-1]) ** 0.7) ** 2, 0.55)
    t = _t(0.55)
    rip = _band(_noise(len(t), 2), 1500, 9000) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 37 * t)))
    crackle = (np.random.default_rng(3).random(len(t)) > 0.985) * _noise(len(t), 4) * 2.5
    L["rip"] = _norm((rip + crackle) * np.exp(-((t - 0.18) / 0.22) ** 2), 0.6)
    t = _t(0.14)
    L["pop"] = _norm(np.sin(2 * np.pi * (300 + 1100 * t / t[-1]) * t) * np.exp(-t * 32), 0.5)
    t = _t(1.2)
    L["ding"] = _norm((np.sin(2 * np.pi * 1568 * t) + 0.45 * np.sin(2 * np.pi * 2352 * t) + 0.2 * np.sin(2 * np.pi * 3136 * t))
                      * np.exp(-t * 4.5), 0.32)
    t = _t(0.05)
    L["click"] = _norm(_band(_noise(len(t), 5), 2000, 8000) * np.exp(-t * 160), 0.45)
    L["tick"] = _norm(np.sin(2 * np.pi * 2600 * t) * np.exp(-t * 220), 0.28)
    t = _t(0.42)
    sq = np.sign(np.sin(2 * np.pi * (180 + 900 * np.floor(t * 28) % 700) * t))
    L["glitch"] = _norm(np.round(sq * (np.random.default_rng(6).random(len(t)) > 0.3) * 4) / 4 * np.exp(-t * 4), 0.3)
    t = _t(0.9)
    L["impact"] = _norm(np.sin(2 * np.pi * (45 + 90 * np.exp(-t * 18)) * t) * np.exp(-t * 4.5)
                        + _band(_noise(len(t), 7), 150, 3000) * np.exp(-t * 22) * 0.5, 0.85)
    t = _t(0.5)
    L["thud"] = _norm(np.sin(2 * np.pi * (55 + 60 * np.exp(-t * 25)) * t) * np.exp(-t * 9), 0.7)
    t = _t(0.7)
    note = lambda f, s: np.where(t >= s, np.sin(2 * np.pi * f * (t - s)) * np.exp(-np.maximum(t - s, 0) * 7), 0)
    L["notify"] = _norm(note(988, 0) + note(1319, 0.11), 0.32)
    t = _t(0.6)
    L["scan"] = _norm(np.sin(2 * np.pi * (400 * t + 1400 * t ** 2)) * np.sin(np.pi * t / t[-1]) * 0.6
                      + _band(_noise(len(t), 8), 3000, 9000) * 0.15 * np.sin(np.pi * t / t[-1]), 0.25)
    t = _t(0.55)
    buzz = np.sign(np.sin(2 * np.pi * 110 * t)) * 0.6 + np.sin(2 * np.pi * 220 * t) * 0.4
    L["error"] = _norm(buzz * ((t < 0.2) | ((t > 0.28) & (t < 0.48))) * np.exp(-t * 1.5), 0.25)
    t = _t(1.3)
    L["riser"] = _norm(_band(_noise(len(t), 9), 800, 8000) * (t / t[-1]) ** 2 + np.sin(2 * np.pi * (200 + 800 * (t / t[-1]) ** 2) * t)
                       * (t / t[-1]) ** 2 * 0.3, 0.4)
    t = _t(0.9)
    keys = np.zeros(len(t))
    rng = np.random.default_rng(10)
    for s in np.cumsum(rng.uniform(0.055, 0.11, 14)):
        i = int(s * SR)
        if i < len(t) - 2000:
            keys[i:i + 2000] += _band(_noise(2000, int(s * 1000)), 1500, 7000) * np.exp(-np.arange(2000) / SR * 120) * rng.uniform(0.5, 1)
    L["type"] = _norm(keys, 0.35)
    t = _t(0.8)
    L["print"] = _norm((np.sign(np.sin(2 * np.pi * 70 * t)) * 0.4 + _band(_noise(len(t), 11), 500, 3000) * 0.6)
                       * (0.6 + 0.4 * np.sin(2 * np.pi * 14 * t)) * np.minimum(1, (t[-1] - t) / 0.1), 0.22)
    t = _t(0.25)
    snip = _band(_noise(len(t), 12), 2500, 9000) * (np.exp(-t * 60) + np.where(t > 0.1, np.exp(-(t - 0.1) * 70), 0))
    L["snip"] = _norm(snip, 0.5)
    for k, v in L.items():
        write(ROOT / "public" / "sfx" / f"{k}.wav", v)
    print("sfx:", ", ".join(sorted(L)))


# ------------------------------------------------------------------ music bed (original, synthesized)
def music(seconds, bpm=98):
    n = int(seconds * SR)
    out = np.zeros(n + SR * 2)
    beat = 60 / bpm
    A = 220.0
    # i - vi - III - VII style progression in A minor: Am7, Fmaj7, Cmaj7, G6 (semitones from A3)
    chords = [[0, 3, 7, 10], [-4, 0, 3, 7], [3, 7, 10, 14], [-2, 2, 5, 9]]
    roots = [0, -4, 3, -2]
    hz = lambda s: A * 2 ** (s / 12)

    def put(x, at):
        i = int(at * SR)
        if i < len(out):
            m = min(len(x), len(out) - i)
            out[i:i + m] += x[:m]

    bar = 0
    while bar * 4 * beat < seconds:
        b0 = bar * 4 * beat
        ch = chords[bar % 4]
        # keys: soft electric-piano stabs on beat 1 and the "and" of 2 (bouncy)
        for at, length in ((0, 1.4), (1.5, 0.9), (3, 0.6)):
            tt = _t(length * beat)
            stab = sum(np.sin(2 * np.pi * hz(s) * tt) + 0.25 * np.sin(4 * np.pi * hz(s) * tt) for s in ch)
            put(stab * np.exp(-tt * 3.2) * 0.05, b0 + at * beat)
        # bass
        for at in (0, 1.5, 2, 3.5):
            tt = _t(0.45 * beat)
            put(np.sin(2 * np.pi * hz(roots[bar % 4] - 24) * tt) * np.exp(-tt * 4) * 0.22, b0 + at * beat)
        # drums with light swing on the hats
        for k in range(4):
            if k in (0, 2):
                tt = _t(0.3)
                put(np.sin(2 * np.pi * (50 + 70 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 12) * 0.35, b0 + k * beat)
            else:
                tt = _t(0.2)
                put(_band(_noise(len(tt), bar * 4 + k), 900, 6000) * np.exp(-tt * 22) * 0.10, b0 + k * beat)
            for h, swing in ((0, 0), (0.5, 0.08)):
                tt = _t(0.05)
                put(_band(_noise(len(tt), bar * 40 + k * 2 + int(h * 2)), 6000, 12000) * np.exp(-tt * 90) * 0.05,
                    b0 + (k + h + swing) * beat)
        bar += 1
    out = out[:n]
    fade = int(1.5 * SR)
    out[-fade:] *= np.linspace(1, 0, fade)
    out[:int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR))
    return _norm(out, 0.6)


# ------------------------------------------------------------------ word timing estimate
def _syll(w):
    w = re.sub(r"[^a-z0-9]", "", w.lower())
    if not w:
        return 1
    if w.isdigit():
        return max(1, len(w))
    return max(1, len(re.findall(r"[aeiouy]+", w)) - (1 if w.endswith("e") and len(w) > 3 else 0))


def words_timing(text, dur):
    ws = text.split()
    weights = [_syll(w) + (0.6 if re.search(r"[,.:;!?]$", w) else 0) for w in ws]
    total = sum(weights)
    out, t = [], 0.0
    for w, k in zip(ws, weights):
        d = dur * k / total
        out.append({"w": w, "s": round(t, 3), "e": round(t + d, 3)})
        t += d
    return out


# ------------------------------------------------------------------ episode
def write_index():
    files = sorted((ROOT / "src" / "episodes").glob("*.timeline.json"))
    names = [f.name.replace(".timeline.json", "").replace("-", "_") for f in files]
    lines = [f"import {n} from './{f.name}';" for n, f in zip(names, files)]
    lines.append("import type {Timeline} from '../lib/Episode';")
    lines.append(f"export const TIMELINES = [{', '.join(names)}] as unknown as Timeline[];")
    (ROOT / "src" / "episodes" / "index.ts").write_text("\n".join(lines) + "\n")


def narrate(chunk, voice, profile):
    """One request for the chunk; if the split fails on every model, fall back to one request per line."""
    for m in MODELS:
        try:
            return gtts.say_batch(chunk, voice=voice, model=m, profile=profile)
        except (ValueError, gtts.DailyQuota, RuntimeError) as e:
            print(f"    batch on {m}: {e}")
    out = []
    for text, d in chunk:
        out.append(gtts.say(text, d, voice=voice, model=MODELS, profile=profile))
    return out



def episode(path):
    path = Path(path)
    ep = json.loads(path.read_text())
    epdir = path.parent.name
    profile = ep.get("profile", "fast")
    beats = ep["beats"]
    lines = [(b["text"], b.get("dir", "")) for b in beats]
    takes = []
    size = ep.get("batch", 8)  # batch 1 = one request per line (no batch-split errors, costs more quota)
    for i in range(0, len(lines), size):
        chunk = lines[i:i + size]
        if size == 1:
            p, _ = gtts.say(chunk[0][0], chunk[0][1], voice=ep.get("voice", "Fenrir"), model=MODELS, profile=PROFILES[profile])
            takes.append(gtts.clean(p)[0])
        else:
            takes += [gtts.clean(p)[0] for p, _ in narrate(chunk, ep.get("voice", "Fenrir"), PROFILES[profile])]
        print(f"  narration {min(i + size, len(lines))}/{len(lines)}")
    # measure pace and speed up to the target if needed (never slow down)
    words = sum(len(t.split()) for t, _ in lines)
    secs = sum(gtts.wav_duration(p) for p in takes)
    wpm = words / secs * 60
    factor = min(ep.get("max_tempo", 1.25), max(1.0, TARGET_WPM[profile] / wpm))
    print(f"  raw pace {wpm:.0f} wpm -> tempo x{factor:.2f}")
    gap, lead, tail = ep.get("gap", 0.15), 0.25, 1.2
    t = lead
    vo = np.zeros(int(SR * 2000))
    out_beats = []
    for b, p in zip(beats, takes):
        src = p
        if factor > 1.001:
            src = p.with_name(p.stem + f"_t{int(factor * 100)}.wav")
            if not src.exists():
                tempo(p, factor, src)
        x = read(src)
        i = int(t * SR)
        vo[i:i + len(x)] += x
        d = len(x) / SR
        out_beats.append({**b, "start": round(t, 3), "vo": round(d, 3), "dur": round(d + gap, 3),
                          "words": words_timing(b["text"], d)})
        t += d + gap
    total = t + tail
    out_beats[-1]["dur"] = round(out_beats[-1]["dur"] + tail, 3)
    vo = vo[:int(total * SR)]
    vo = _norm(vo, 0.89)
    pub = ROOT / "public" / epdir
    write(pub / f"{ep['id']}-vo.wav", vo)
    write(pub / f"{ep['id']}-music.wav", music(total))
    tl = {"id": ep["id"], "format": ep["format"], "captions": ep.get("captions", "big"), "fps": 30,
          "duration": round(total, 3), "vo": f"{epdir}/{ep['id']}-vo.wav", "music": f"{epdir}/{ep['id']}-music.wav",
          "beats": out_beats}
    dst = ROOT / "src" / "episodes" / f"{ep['id']}.timeline.json"
    dst.write_text(json.dumps(tl, indent=1))
    write_index()
    print(f"  {len(beats)} beats, {total:.1f} s, {words / (secs / factor) * 60:.0f} wpm -> {dst.relative_to(ROOT)}")


if __name__ == "__main__":
    if sys.argv[1] == "sfx":
        sfx_library()
    elif sys.argv[1] == "episode":
        episode(sys.argv[2])
