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


def smoke(canvas, x, y, t, strength=1.0, n=9, tone=(70, 72, 80)):
    for i in range(n):
        ph = (t * 0.55 + i / n) % 1
        r = 14 + 60 * ph
        px = x + 26 * math.sin(i * 2.1 + t * 1.2) * ph - 30 * ph
        py = y - 190 * ph
        paint = skia.Paint(AntiAlias=True, Color=skia.Color(tone[0], tone[1], tone[2], int(170 * (1 - ph) * clamp(strength))))
        canvas.drawCircle(px, py, r, paint)


NAVY = skia.Color(16, 26, 46)


def _text(canvas, s, x, y, f, color, alpha=1.0, spacing=0.0):
    paint = skia.Paint(AntiAlias=True, Color=color)
    paint.setAlphaf(clamp(alpha))
    if not spacing:
        canvas.drawString(s, x, y, f, paint)
        return f.measureText(s)
    cx = x
    for ch in s:
        canvas.drawString(ch, cx, y, f, paint)
        cx += f.measureText(ch) + spacing
    return cx - x - spacing


def card(canvas, W, H, header, rows, takeaway, lt):
    """Tip card for 16:9: orange header, KEY / value rows that slide in, optional takeaway bar.
    A row with an empty value is drawn as a single bullet line."""
    u = W / 1920
    canvas.clear(NAVY)
    canvas.drawRect(skia.Rect.MakeWH(W, 14 * u), skia.Paint(Color=ORANGE))
    left = 200 * u
    a = smooth(lt / 0.35)
    hw = _text(canvas, header, left, (300 - 30 * (1 - a)) * u, font("ExtraBold", 118 * u), ORANGE, a, spacing=4 * u)
    canvas.drawRect(skia.Rect.MakeXYWH(left, 336 * u, hw * smooth((lt - 0.2) / 0.5), 8 * u), skia.Paint(Color=skia.ColorWHITE))
    n = max(len(rows), 1)
    reserve = 210 if takeaway else 90
    step = min(104, (1080 - 450 - reserve) / n)
    y = 450.0
    for i, (key, val) in enumerate(rows):
        ra = smooth((lt - 0.7 - i * 0.5) / 0.4)
        dx = 40 * (1 - ra) * u
        base = (y + step * 0.62) * u
        if val:
            _text(canvas, key, left + dx, base, font("ExtraBold", 40 * u), ORANGE, ra, spacing=5 * u)
            _text(canvas, val, left + 420 * u + dx, base, font("Medium", 46 * u), skia.ColorWHITE, ra)
        else:
            canvas.drawRect(skia.Rect.MakeXYWH(left + dx, base - 30 * u, 14 * u, 14 * u),
                            skia.Paint(Color=skia.Color(255, 150, 40, int(255 * clamp(ra)))))
            _text(canvas, key, left + 40 * u + dx, base, font("ExtraBold", 52 * u), skia.ColorWHITE, ra, spacing=3 * u)
        y += step
    if takeaway:
        ta = smooth((lt - 0.9 - n * 0.5) / 0.5)
        top = (y + 14) * u
        canvas.drawRoundRect(skia.Rect.MakeXYWH(left, top, W - 2 * left, 110 * u), 14 * u, 14 * u,
                             skia.Paint(AntiAlias=True, Color=skia.Color(255, 255, 255, int(22 * ta))))
        canvas.drawRect(skia.Rect.MakeXYWH(left, top, 10 * u, 110 * u), skia.Paint(Color=skia.Color(255, 150, 40, int(255 * ta))))
        _text(canvas, takeaway, left + 50 * u, top + 72 * u, font("SemiBold", 46 * u), skia.ColorWHITE, ta)


def dust(canvas, t, W, H, amount=1.0, seed=6):
    """Light specks drifting down, for shaking rooms. Deterministic per speck."""
    rng = np.random.default_rng(seed)
    n = int(70 * clamp(amount, 0, 2))
    xs, ys, ph, sp, r = (rng.uniform(0, W, n), rng.uniform(0, H, n), rng.uniform(0, 6.28, n), rng.uniform(40, 140, n),
                         rng.uniform(2.0, 5.5, n))
    paint = skia.Paint(AntiAlias=True, Color=skia.Color(235, 220, 195, 120))
    for x, y, p0, s0, r0 in zip(xs, ys, ph, sp, r):
        canvas.drawCircle(float(x + 14 * math.sin(t * 1.7 + p0)), float((y + s0 * t) % (H + 20) - 10), float(r0), paint)


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


# ---------------------------------------------------------------- explainer diagrams (drawn in code, so every label is exact)
_PALETTE = [skia.Color(255, 150, 40), skia.Color(80, 180, 255), skia.Color(120, 220, 150), skia.Color(240, 110, 150),
            skia.Color(190, 150, 255), skia.Color(250, 220, 90)]


def _panel(canvas, x, y, w, h, alpha=0.82):
    canvas.drawRoundRect(skia.Rect.MakeXYWH(x, y, w, h), 36, 36, skia.Paint(AntiAlias=True, Color=skia.Color(10, 18, 36, int(255 * alpha))))
    canvas.drawRoundRect(skia.Rect.MakeXYWH(x, y, w, h), 36, 36, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4,
                                                                         Color=skia.Color(255, 150, 40, int(200 * alpha))))


def _ctext(canvas, s, cx, y, f, color, alpha=1.0, spacing=0.0):
    w = f.measureText(s) + spacing * max(len(s) - 1, 0)
    _text(canvas, s, cx - w / 2, y, f, color, alpha, spacing)


def _block(canvas, s, x, y, w, h, color, f, alpha=1.0):
    p = skia.Paint(AntiAlias=True, Color=color)
    p.setAlphaf(clamp(alpha))
    canvas.drawRoundRect(skia.Rect.MakeXYWH(x, y, w, h), 18, 18, p)
    _ctext(canvas, s, x + w / 2, y + h * 0.66, f, skia.Color(12, 18, 34), alpha)


def diagram(canvas, W, H, e, lt, dur):
    """Animated explainer overlay. kind: tokens | dials | attention | writing | context | gpu. lt = seconds since the event started.
    Short (vertical) draws a narrow panel; long (landscape) a wide one. All text is exact, never generated."""
    kind = e.get("kind", "tokens")
    wide = W > H
    if wide:
        k, cx, pw = 0.9, W / 2 / 0.9, 1560
    else:
        k, cx, pw = W / 1080, 540, 1000
    canvas.save()
    canvas.scale(k, k)
    if wide:
        canvas.translate(0, -250)                 # panels were laid out from y=330; pull them up for 16:9
    L = cx - pw / 2
    fade = clamp(lt / 0.3) * clamp((dur - lt) / 0.3 + 0.2)
    white = skia.ColorWHITE
    soft = skia.Color(170, 200, 255)
    if kind == "tokens":
        _panel(canvas, L, 330, pw, 900, 0.82 * fade)
        _ctext(canvas, "TOKENS", cx, 420, font("ExtraBold", 54), ORANGE, fade, 8)
        words = e.get("words", ["The", " cat", " sat", " on", " the", " mat"])
        nums = e.get("numbers", ["12", "845", "301", "47", "9", "2210"])
        f = font("ExtraBold", 50)
        wid = [f.measureText(w.strip()) + 52 for w in words]
        gap = 24 * clamp((lt - 0.7) / 0.5)
        total = sum(wid) + gap * (len(words) - 1)
        x = cx - total / 2
        for i, (w, ww) in enumerate(zip(words, wid)):
            col = skia.Color(70, 88, 120) if lt < 0.7 else _PALETTE[i % len(_PALETTE)]
            _block(canvas, w.strip(), x, 500, ww, 100, col, f, fade)
            na = smooth((lt - 1.4 - i * 0.25) / 0.3)
            if na > 0:
                _ctext(canvas, nums[i % len(nums)], x + ww / 2, 680, font("ExtraBold", 46), white, na * fade)
                canvas.drawRect(skia.Rect.MakeXYWH(x + ww / 2 - 3, 610, 6, 36 * na), skia.Paint(Color=skia.Color(255, 255, 255, int(150 * fade))))
            x += ww + gap
        _ctext(canvas, "EACH PIECE BECOMES A NUMBER", cx, 770, font("SemiBold", 38), soft, smooth((lt - 2.0) / 0.4) * fade, 3)
        ra = smooth((lt - 2.6) / 0.5)
        if ra > 0:
            _ctext(canvas, "RARE WORDS GET SPLIT", cx, 880, font("SemiBold", 38), soft, ra * fade, 3)
            parts = e.get("rare", ["un", "believ", "able"])
            f2 = font("ExtraBold", 50)
            wd = [f2.measureText(p) + 52 for p in parts]
            xx = cx - (sum(wd) + 24 * (len(parts) - 1)) / 2
            for i, (p, ww) in enumerate(zip(parts, wd)):
                _block(canvas, p, xx, 930, ww, 100, _PALETTE[(i + 2) % len(_PALETTE)], f2, ra * fade)
                xx += ww + 24
        _ctext(canvas, "EXAMPLE", cx, 1190, font("Medium", 30), skia.Color(150, 170, 210), fade, 6)
    elif kind == "dials":
        _panel(canvas, L, 330, pw, 960, 0.82 * fade)
        steps = ["GUESS", "CHECK", "NUDGE"]
        active = int(lt / 0.9) % 3
        fx = font("ExtraBold", 46)
        x = L + 60
        for i, s_ in enumerate(steps):
            w = fx.measureText(s_) + 56
            _block(canvas, s_, x, 390, w, 92, ORANGE if i == active else skia.Color(60, 76, 110), fx, fade)
            x += w + 40
            if i < 2:
                _text(canvas, ">", x - 30, 452, fx, soft, fade)
        pulse = smooth((lt % 0.9) / 0.45) if active == 2 else 0.0
        cycle = int(lt / 2.7)
        step = min(225, (pw - 160) / 3.6)
        for r in range(3):
            for c in range(4):
                gx, gy = cx + (c - 1.5) * step, 640 + r * 190
                a = -2.2 + ((r * 4 + c) * 0.9 % 4.2) + 0.55 * (cycle + (pulse if active == 2 else 0)) * (1 if (r + c) % 2 else -1)
                canvas.drawCircle(gx, gy, 70, skia.Paint(AntiAlias=True, Color=skia.Color(52, 66, 96, int(255 * fade))))
                canvas.drawCircle(gx, gy, 70, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5,
                                                      Color=skia.Color(160, 190, 240, int(255 * fade))))
                canvas.drawLine(gx, gy, gx + 54 * math.sin(a), gy - 54 * math.cos(a),
                                skia.Paint(AntiAlias=True, StrokeWidth=10, StrokeCap=skia.Paint.kRound_Cap,
                                           Color=skia.Color(255, 150, 40, int(255 * fade)) if active == 2 else skia.Color(255, 255, 255, int(255 * fade))))
        _ctext(canvas, "MANY BILLIONS OF DIALS", cx, 1235, font("ExtraBold", 44), white, fade, 4)
    elif kind == "attention":
        _panel(canvas, L, 400, pw, 700, 0.82 * fade)
        _ctext(canvas, "ATTENTION", cx, 485, font("ExtraBold", 54), ORANGE, fade, 8)
        sets = e.get("sentences") or [
            dict(words=["The", "mole", "dug", "a", "tunnel"], focus=1, links={2: 0.9, 4: 0.8}, label="ANIMAL"),
            dict(words=["The", "mole", "on", "his", "skin"], focus=1, links={4: 0.9, 3: 0.4}, label="SKIN SPOT")]
        kk = min(int(lt / max(dur / len(sets), 0.5)), len(sets) - 1)
        s_ = sets[kk]
        local = lt - kk * dur / len(sets)
        f = font("ExtraBold", 46)
        wid = [f.measureText(w) + 40 for w in s_["words"]]
        total = sum(wid) + 20 * (len(wid) - 1)
        x, centers = cx - total / 2, []
        for i, (w, ww) in enumerate(zip(s_["words"], wid)):
            _block(canvas, w, x, 800, ww, 90, ORANGE if i == s_["focus"] else skia.Color(70, 88, 120), f, fade)
            centers.append(x + ww / 2)
            x += ww + 20
        grow = smooth(local / 0.5)
        for j, wgt in s_["links"].items():
            x0, x1 = centers[s_["focus"]], centers[j]
            path = skia.Path()
            path.moveTo(x0, 800)
            path.quadTo((x0 + x1) / 2, 800 - 120 - abs(x1 - x0) * 0.25, x1, 800)
            canvas.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4 + 16 * wgt * grow,
                                             StrokeCap=skia.Paint.kRound_Cap, Color=skia.Color(80, 180, 255, int(230 * fade * grow))))
        _ctext(canvas, s_["label"], cx, 1000, font("ExtraBold", 56), skia.Color(120, 220, 150), smooth((local - 0.5) / 0.4) * fade, 6)
        _ctext(canvas, "THICKER LINE = MORE ATTENTION", cx, 1060, font("SemiBold", 32), soft, fade, 3)
    elif kind == "writing":
        y0 = e.get("y", 250)
        _panel(canvas, L, y0, pw, 640, 0.84 * fade)
        prompt = e.get("prompt", "The sky is")
        cands = e.get("cands", [["blue", 70], ["clear", 12], ["grey", 8], ["green", 1]])
        chosen = lt > e.get("pick_at", 2.6)
        _ctext(canvas, prompt + (" " + cands[0][0] if chosen else " ..."), cx, y0 + 100, font("ExtraBold", 64), white, fade)
        maxw = pw - 360
        for i, (w, pct) in enumerate(cands):
            by = y0 + 170 + i * 92
            a = smooth((lt - 0.4 - i * 0.2) / 0.4)
            _text(canvas, w, L + 60, by + 56, font("ExtraBold", 44), white, a * fade)
            hl = chosen and i == 0
            canvas.drawRoundRect(skia.Rect.MakeXYWH(L + 260, by + 12, max(maxw * pct / 100 * a, 8), 56), 14, 14,
                                 skia.Paint(AntiAlias=True, Color=skia.Color(255, 150, 40, int(255 * fade)) if hl
                                            else skia.Color(80, 140, 230, int(255 * fade))))
            _text(canvas, f"{pct}%", L + 260 + maxw * pct / 100 * a + 18, by + 56, font("SemiBold", 40), white, a * fade)
        _ctext(canvas, "ILLUSTRATIVE NUMBERS", cx, y0 + 600, font("Medium", 30), skia.Color(150, 170, 210), fade, 6)
    elif kind == "context":      # a window that fills up with the parts of a conversation, counted in tokens
        _panel(canvas, L, 400, pw, 700, 0.84 * fade)
        _ctext(canvas, "CONTEXT WINDOW", cx, 485, font("ExtraBold", 54), ORANGE, fade, 8)
        bw, bx, by = pw - 160, L + 80, 560
        canvas.drawRoundRect(skia.Rect.MakeXYWH(bx, by, bw, 150), 22, 22, skia.Paint(AntiAlias=True, Color=skia.Color(30, 44, 74, int(255 * fade))))
        canvas.drawRoundRect(skia.Rect.MakeXYWH(bx, by, bw, 150), 22, 22, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style,
                                                                                 StrokeWidth=5, Color=skia.Color(160, 190, 240, int(255 * fade))))
        parts = e.get("parts", [("EARLIER CHAT", 0.32, 1), ("YOUR QUESTION", 0.24, 2), ("THE ANSWER", 0.26, 3)])
        x = bx + 8
        for name, share, order in parts:
            g = smooth((lt - 0.4 - order * 0.7) / 0.7)
            ww = (bw - 16) * share * g
            if ww > 2:
                canvas.drawRoundRect(skia.Rect.MakeXYWH(x, by + 12, ww, 126), 14, 14,
                                     skia.Paint(AntiAlias=True, Color=skia.Color(*[(255, 150, 40), (80, 180, 255), (120, 220, 150)][order - 1], int(235 * fade))))
            _ctext(canvas, name, x + (bw - 16) * share / 2, by + 220, font("SemiBold", 27), soft, g * fade, 1)
            x += (bw - 16) * share
        _ctext(canvas, "THE WINDOW HOLDS A LIMITED NUMBER OF TOKENS", cx, 890, font("ExtraBold", 40), white, smooth((lt - 3.0) / 0.5) * fade, 3)
        _ctext(canvas, "WHEN IT IS FULL, OLDER TEXT CAN BE DROPPED", cx, 960, font("SemiBold", 34), soft, smooth((lt - 4.0) / 0.5) * fade, 3)
    elif kind == "gpu":          # a few strong cores working in turn, against thousands of small ones working together
        _panel(canvas, L, 380, pw, 740, 0.84 * fade)
        half = pw / 2
        for side, (title, n, cols, col, size) in enumerate([("CPU: A FEW STRONG CORES", 4, 2, (255, 150, 40), 90),
                                                             ("GPU: THOUSANDS OF SMALL CORES", 140, 14, (80, 180, 255), 22)]):
            ccx = L + half * (side + 0.5)
            _ctext(canvas, title, ccx, 470, font("ExtraBold", 34), white, fade, 2)
            rows = math.ceil(n / cols)
            gw = cols * (size + 8) - 8
            gx0 = ccx - gw / 2
            gy0 = 560 if side == 0 else 540
            for idx in range(n):
                r_, c_ = divmod(idx, cols)
                if side == 0:
                    on = int(lt / 0.8) % n == idx            # one after another
                else:
                    on = ((idx * 7 + int(lt * 6)) % 3) != 0   # many at once
                a_ = 255 if on else 70
                canvas.drawRoundRect(skia.Rect.MakeXYWH(gx0 + c_ * (size + 8), gy0 + r_ * (size + 8), size, size), size / 5, size / 5,
                                     skia.Paint(AntiAlias=True, Color=skia.Color(*col, int(a_ * fade))))
        canvas.drawRect(skia.Rect.MakeXYWH(cx - 2, 450, 4, 600), skia.Paint(Color=skia.Color(255, 255, 255, int(70 * fade))))
        _ctext(canvas, "ONE BY ONE", L + half * 0.5, 1060, font("SemiBold", 34), soft, fade, 4)
        _ctext(canvas, "MANY AT ONCE", L + half * 1.5, 1060, font("SemiBold", 34), soft, fade, 4)
    canvas.restore()


def verdict(canvas, kind, t0, t, x, y, size=300):
    """Big animated red X ('cross') or green tick ('check') that pops in, for myth versus fact. Drawn in code, never baked into pictures."""
    d = t - t0
    if d < 0:
        return
    k = back(d / 0.25) * (1 + 0.04 * math.sin(d * 14) * math.exp(-d * 4))
    canvas.save()
    canvas.translate(x, y)
    canvas.scale(k, k)
    col = skia.Color(235, 50, 50) if kind == "cross" else skia.Color(60, 200, 110)
    ring = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=size * 0.09, Color=skia.Color(0, 0, 0))
    canvas.drawCircle(0, 0, size * 0.5, skia.Paint(AntiAlias=True, Color=skia.Color(255, 255, 255)))
    canvas.drawCircle(0, 0, size * 0.5, ring)
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=size * 0.16, StrokeCap=skia.Paint.kRound_Cap,
                   StrokeJoin=skia.Paint.kRound_Join, Color=col)
    edge = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=size * 0.16 + 12, StrokeCap=skia.Paint.kRound_Cap,
                      StrokeJoin=skia.Paint.kRound_Join, Color=skia.Color(0, 0, 0))
    path = skia.Path()
    if kind == "cross":
        path.moveTo(-size * 0.24, -size * 0.24); path.lineTo(size * 0.24, size * 0.24)
        path.moveTo(size * 0.24, -size * 0.24); path.lineTo(-size * 0.24, size * 0.24)
    else:
        path.moveTo(-size * 0.26, 0); path.lineTo(-size * 0.07, size * 0.2); path.lineTo(size * 0.28, -size * 0.22)
    canvas.drawPath(path, edge)
    canvas.drawPath(path, p)
    canvas.restore()
