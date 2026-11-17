"""Stage tools for puppet shorts: camera, captions, impact text, stickers, particles and synthesized sound."""
import math
import wave
from pathlib import Path

import numpy as np
import skia

from .tts import RATE as SR

FONT_DIR = Path("/usr/share/fonts/opentype/inter")
ORANGE = skia.Color(255, 150, 40)


def font(weight, size):
    for p in (Path(__file__).resolve().parent.parent / "assets" / f"Inter-{weight}.otf", FONT_DIR / f"Inter-{weight}.otf"):
        if p.exists():
            return skia.Font(skia.Typeface.MakeFromFile(str(p)), size)
    return skia.Font(skia.Typeface("Arial", skia.FontStyle.Bold()), size)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def snap(x):
    """Fast start, soft landing: for whip pans and snap zooms."""
    return 1 - (1 - clamp(x)) ** 4


def back(x):
    x = clamp(x)
    c = 2.2
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def lerp(a, b, k):
    return a + (b - a) * k


def keyed(keys, t, ease=smooth):
    """keys: [(time, value_tuple), ...] -> interpolated tuple."""
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t0 <= t < t1:
            k = ease((t - t0) / (t1 - t0))
            return tuple(lerp(a, b, k) for a, b in zip(v0, v1))
    return keys[-1][1]


def shake_offset(t, hits, amp=26):
    """hits: times of impacts. Returns (dx, dy) decaying after each."""
    dx = dy = 0.0
    for h in hits:
        d = t - h
        if 0 <= d < 0.4:
            k = amp * (1 - d / 0.4) ** 2
            dx += k * math.sin(d * 95)
            dy += k * math.cos(d * 78)
    return dx, dy


def outlined(canvas, s, x, y, f, fill, stroke_w, alpha=1.0):
    st = skia.Paint(AntiAlias=True, Color=skia.Color(10, 10, 14), Style=skia.Paint.kStroke_Style, StrokeWidth=stroke_w,
                    StrokeJoin=skia.Paint.kRound_Join)
    st.setAlphaf(clamp(alpha))
    fl = skia.Paint(AntiAlias=True, Color=fill)
    fl.setAlphaf(clamp(alpha))
    canvas.drawString(s, x, y, f, st)
    canvas.drawString(s, x, y, f, fl)


def captions(canvas, words, t, W, y, size=92, group=3):
    """Word-by-word captions: shows the current group, pops and colours the active word."""
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= group or w[0][-1:] in ".!?,":
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    for gi, g in enumerate(groups):
        end = groups[gi + 1][0][1] if gi + 1 < len(groups) else g[-1][2] + 0.3
        if g[0][1] <= t < end:
            f = font("Black", size)
            space = f.measureText(" ")
            widths = [f.measureText(w[0].upper()) for w in g]
            total = sum(widths) + space * (len(g) - 1)
            if total > W - 120:
                f = font("Black", size * (W - 120) / total)
                space = f.measureText(" ")
                widths = [f.measureText(w[0].upper()) for w in g]
                total = sum(widths) + space * (len(g) - 1)
            x = W / 2 - total / 2
            for (word, ws, we), wd in zip(g, widths):
                if t >= ws:
                    k = back((t - ws) / 0.12)
                    active = t < we + 0.05
                    canvas.save()
                    canvas.translate(x + wd / 2, y)
                    canvas.scale(0.6 + 0.4 * k, 0.6 + 0.4 * k)
                    outlined(canvas, word.upper(), -wd / 2, 0, f, ORANGE if active else skia.ColorWHITE, f.getSize() * 0.16)
                    canvas.restore()
                x += wd + space
            return


def impact_word(canvas, s, t0, t, W, y, size=210, color=ORANGE, hold=0.9):
    d = t - t0
    if d < 0 or d > hold:
        return
    k = 2.2 - 1.2 * snap(d / 0.1)
    f = font("Black", size)
    w = f.measureText(s)
    canvas.save()
    canvas.translate(W / 2, y)
    canvas.rotate(-5)
    canvas.scale(k, k)
    outlined(canvas, s, -w / 2, 0, f, color, size * 0.14, alpha=clamp((hold - d) / 0.15))
    canvas.restore()


def sticker(canvas, s, t0, t, x, y, size=54):
    d = t - t0
    if d < 0:
        return
    k = back(d / 0.2)
    f = font("ExtraBold", size)
    w = f.measureText(s)
    canvas.save()
    canvas.translate(x, y)
    canvas.rotate(-4)
    canvas.scale(k, k)
    box = skia.Rect.MakeXYWH(-w / 2 - 34, -size * 0.85, w + 68, size * 1.5)
    canvas.drawRoundRect(box, 22, 22, skia.Paint(AntiAlias=True, Color=skia.Color(255, 255, 255)))
    canvas.drawRoundRect(box, 22, 22, skia.Paint(AntiAlias=True, Color=skia.Color(10, 10, 14), Style=skia.Paint.kStroke_Style,
                                                 StrokeWidth=7))
    canvas.drawString(s, -w / 2, size * 0.22, f, skia.Paint(AntiAlias=True, Color=skia.Color(10, 10, 14)))
    canvas.restore()


class Snow:
    def __init__(self, W, H, seed=3):
        rng = np.random.default_rng(seed)
        self.W, self.H, self.layers = W, H, []
        for n, r, speed, alpha in ((170, 2.2, 150, 130), (90, 3.8, 280, 180), (36, 7.0, 480, 220)):
            self.layers.append((rng.uniform(0, W, n), rng.uniform(0, H, n), rng.uniform(0, 6.28, n), rng.uniform(0.7, 1.3, n),
                                r, speed, alpha))

    def draw(self, canvas, t, amount=1.0, wind=0.5):
        for xs0, ys0, ph, k, r, speed, alpha in self.layers:
            n = int(len(xs0) * clamp(amount, 0, 1.5) / 1.5)
            paint = skia.Paint(AntiAlias=True, Color=skia.Color(255, 255, 255, alpha))
            ys = (ys0[:n] + speed * k[:n] * t) % (self.H + 20) - 10
            xs = (xs0[:n] - wind * speed * t + 14 * np.sin(t * 1.5 + ph[:n])) % (self.W + 20) - 10
            for x, y, kk in zip(xs, ys, k[:n]):
                canvas.drawCircle(float(x), float(y), r * float(kk), paint)


def wind_lines(canvas, t, W, H, strength=1.0, seed=11):
    rng = np.random.default_rng(seed)
    paint = skia.Paint(AntiAlias=True, Color=skia.Color(255, 255, 255, int(150 * clamp(strength))), StrokeWidth=5,
                       StrokeCap=skia.Paint.kRound_Cap)
    for i in range(16):
        y = rng.uniform(0.12, 0.7) * H
        speed = rng.uniform(1900, 3000)
        length = rng.uniform(160, 420)
        x = W + 500 - ((t * speed + rng.uniform(0, 3000)) % (W + 1400))
        canvas.drawLine(x, y, x + length, y - 14, paint)


def burst(canvas, x, y, t0, t, n=14, seed=5, color=skia.ColorWHITE, speed=420, size=13, gravity=900, life=0.7):
    """Chunks or sparkles thrown out from (x, y) at time t0. Coordinates are in the current canvas space."""
    d = t - t0
    if d < 0 or d > life:
        return
    rng = np.random.default_rng(seed)
    paint = skia.Paint(AntiAlias=True, Color=color)
    paint.setAlphaf(clamp((life - d) / (life * 0.4)))
    edge = skia.Paint(AntiAlias=True, Color=skia.Color(10, 10, 14), Style=skia.Paint.kStroke_Style, StrokeWidth=size * 0.22)
    edge.setAlphaf(paint.getAlphaf())
    for _ in range(n):
        a, v, r = rng.uniform(-2.7, -0.45), rng.uniform(0.45, 1.0) * speed, rng.uniform(0.5, 1.0) * size
        px, py = x + math.cos(a) * v * d, y + math.sin(a) * v * d + 0.5 * gravity * d * d
        canvas.drawCircle(px, py, r, paint)
        canvas.drawCircle(px, py, r, edge)


def smoke(canvas, x, y, t, strength=1.0, n=9):
    for i in range(n):
        ph = (t * 0.55 + i / n) % 1
        r = 14 + 60 * ph
        px = x + 26 * math.sin(i * 2.1 + t * 1.2) * ph - 30 * ph
        py = y - 190 * ph
        paint = skia.Paint(AntiAlias=True, Color=skia.Color(70, 72, 80, int(170 * (1 - ph) * clamp(strength))))
        canvas.drawCircle(px, py, r, paint)


# ---------------- sound ----------------

def _noise(n, seed):
    return np.random.default_rng(seed).standard_normal(n)


def _band(x, lo, hi):
    spec = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    spec *= np.exp(-0.5 * ((np.log(np.maximum(f, 1)) - math.log(math.sqrt(lo * hi))) / (math.log(hi / lo) / 2.4)) ** 2)
    out = np.fft.irfft(spec, len(x))
    return out / (np.abs(out).max() + 1e-9)


def sfx(kind, seed=0):
    if kind == "whoosh":
        n = int(0.42 * SR)
        t = np.arange(n) / n
        return _band(_noise(n, seed), 500, 5000) * np.sin(np.pi * t) ** 2 * 0.5
    if kind == "thud":
        n = int(0.5 * SR)
        t = np.arange(n) / SR
        return (np.sin(2 * np.pi * (52 + 70 * np.exp(-t * 22)) * t) * np.exp(-t * 9) * 0.9
                + _band(_noise(n, seed), 120, 900) * np.exp(-t * 30) * 0.4)
    if kind == "pop":
        n = int(0.12 * SR)
        t = np.arange(n) / SR
        return np.sin(2 * np.pi * (380 + 900 * t / 0.12) * t) * np.exp(-t * 30) * 0.45
    if kind == "ding":
        n = int(1.1 * SR)
        t = np.arange(n) / SR
        return (np.sin(2 * np.pi * 1320 * t) + 0.5 * np.sin(2 * np.pi * 1980 * t) + 0.3 * np.sin(2 * np.pi * 2640 * t)) \
            * np.exp(-t * 5) * 0.25
    if kind == "crunch":
        n = int(0.11 * SR)
        t = np.arange(n) / SR
        return _band(_noise(n, seed), 900, 4500) * np.exp(-t * 35) * 0.3
    if kind == "rumble":
        n = int(2.6 * SR)
        t = np.arange(n) / SR
        return (np.sin(2 * np.pi * 41 * t) + 0.6 * np.sin(2 * np.pi * 61.5 * t)) * np.minimum(1, t / 0.8) \
            * np.minimum(1, (2.6 - t) / 0.5) * 0.4
    raise ValueError(kind)


def wind_bed(n, level=1.0):
    t = np.arange(n) / SR
    gust = 0.6 + 0.25 * np.sin(t * 0.7) + 0.15 * np.sin(t * 1.9 + 1.3)
    return (_band(_noise(n, 1), 180, 900) * 0.7 + _band(_noise(n, 2), 900, 3500) * 0.2) * gust * 0.13 * level


def music(n, bpm=112, root=110.0):
    """Light minor pulse: bass on eighths, plucked arpeggio, soft hat. Replace with assets/music.mp3 for a real track."""
    out = np.zeros(n)
    step = 60 / bpm / 2
    scale = [1, 1.189, 1.498, 2, 1.498, 1.189, 1.782, 1.498]      # A C E A E C G E
    bass_seq = [1, 1, 1, 1, 0.794, 0.794, 0.891, 0.891]
    i = 0
    while i * step * SR < n:
        s = int(i * step * SR)
        m = min(int(step * 1.6 * SR), n - s)
        tt = np.arange(m) / SR
        bar = (i // 8) % len(bass_seq)
        out[s:s + m] += np.sin(2 * np.pi * root / 2 * bass_seq[bar] * tt) * np.exp(-tt * 7) * 0.5
        f = root * 2 * scale[i % 8] * bass_seq[bar]
        out[s:s + m] += (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt * 11) * 0.22
        if i % 2 == 1:
            h = min(int(0.04 * SR), n - s)
            out[s:s + h] += _noise(h, i) * np.exp(-np.arange(h) / SR * 90) * 0.07
        i += 1
    return out


def load_wav(path):
    with wave.open(str(path)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768


def place(track, clip, t, gain=1.0):
    i = int(t * SR)
    if i >= len(track) or i < 0:
        return
    m = min(len(clip), len(track) - i)
    track[i:i + m] += clip[:m] * gain


def save_wav(path, mix):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.tanh(mix) * 32000).astype(np.int16).tobytes())
