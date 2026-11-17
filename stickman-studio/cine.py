#!/usr/bin/env python3
"""Cinematic episode renderer: illustrated stills + camera moves, weather, cards, narration, sound.

    python cine.py episodes/night-one
"""
import json
import math
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
import skia

from stickgen import tts

W, H, FPS, SR = 1920, 1080, 30, tts.RATE
LEAD, TAIL = 0.4, 0.6            # silence before / after narration inside a beat
CROP = 0.94                      # keep the top-left 94% of each still (drops the corner watermark)
NAVY, ORANGE = skia.Color(16, 26, 46), skia.Color(255, 138, 31)
FONT_DIR = Path("/usr/share/fonts/opentype/inter")


def font(weight, size):
    for p in (Path(__file__).parent / "assets" / f"Inter-{weight}.otf", FONT_DIR / f"Inter-{weight}.otf"):
        if p.exists():
            return skia.Font(skia.Typeface.MakeFromFile(str(p)), size)
    return skia.Font(skia.Typeface("Arial", skia.FontStyle.Bold()), size)


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def text(canvas, s, x, y, f, color, alpha=1.0, align="left", spacing=0.0):
    paint = skia.Paint(AntiAlias=True, Color=color)
    paint.setAlphaf(max(0.0, min(1.0, alpha)))
    if spacing:
        widths = [f.measureText(ch) + spacing for ch in s]
        total = sum(widths) - spacing
        cx = x - total / 2 if align == "center" else x
        for ch, w in zip(s, widths):
            canvas.drawString(ch, cx, y, f, paint)
            cx += w
        return total
    w = f.measureText(s)
    canvas.drawString(s, x - w / 2 if align == "center" else x, y, f, paint)
    return w


# ---------- visuals ----------

class Snow:
    """Three depth layers of drifting flakes, deterministic per flake."""

    def __init__(self, seed=7):
        rng = np.random.default_rng(seed)
        self.layers = []
        for n, r, speed, alpha in ((260, 1.6, 90, 110), (150, 2.8, 170, 160), (60, 5.5, 300, 210)):
            self.layers.append(dict(x=rng.uniform(0, W, n), y=rng.uniform(0, H, n), ph=rng.uniform(0, 6.28, n),
                                    k=rng.uniform(0.7, 1.3, n), r=r, speed=speed, alpha=alpha))

    def draw(self, canvas, t, amount):
        if amount <= 0:
            return
        for L in self.layers:
            n = int(len(L["x"]) * min(amount, 1.5) / 1.5)
            paint = skia.Paint(AntiAlias=True, Color=skia.Color(255, 255, 255, L["alpha"]))
            ys = (L["y"][:n] + L["speed"] * L["k"][:n] * t) % (H + 20) - 10
            xs = (L["x"][:n] - 0.45 * L["speed"] * t + 18 * np.sin(t * 1.3 + L["ph"][:n])) % (W + 20) - 10
            for x, y, k in zip(xs, ys, L["k"][:n]):
                canvas.drawCircle(float(x), float(y), L["r"] * float(k), paint)


def vignette(canvas):
    shader = skia.GradientShader.MakeRadial((W / 2, H / 2), W * 0.72, [skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 150)],
                                            [0.55, 1.0])
    canvas.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=shader))


def draw_shot(canvas, beat, img, local, t, snow):
    z0, x0, y0, z1, x1, y1 = beat["cam"]
    p = ease(local / beat["dur"]) * 0.7 + (local / beat["dur"]) * 0.3
    z, fx, fy = z0 + (z1 - z0) * p, x0 + (x1 - x0) * p, y0 + (y1 - y0) * p
    iw, ih = img.width() * CROP, img.height() * CROP
    sw, sh = iw / z, ih / z
    left = min(max(fx * iw - sw / 2, 0), iw - sw)
    top = min(max(fy * ih - sh / 2, 0), ih - sh)
    canvas.drawImageRect(img, skia.Rect.MakeXYWH(left, top, sw, sh), skia.Rect.MakeWH(W, H),
                         skia.SamplingOptions(skia.CubicResampler.Mitchell()), skia.Paint())
    for gx, gy, gr, hz in beat.get("glows", []):
        sx = (gx * img.width() - left) / sw * W
        sy = (gy * img.height() - top) / sh * H
        level = (0.5 + 0.5 * math.tanh(4 * math.sin(t * hz * 6.283))) if hz else 0.35 + 0.08 * math.sin(t * 9) * math.sin(t * 2.3)
        col = skia.Color(255, 150, 40, int(190 * level))
        shader = skia.GradientShader.MakeRadial((sx, sy), gr * W * z, [col, skia.Color(255, 150, 40, 0)])
        canvas.drawCircle(sx, sy, gr * W * z, skia.Paint(Shader=shader, BlendMode=skia.BlendMode.kPlus))
    snow.draw(canvas, t, beat.get("snow", 0))
    vignette(canvas)


def draw_chapter(canvas, beat, local):
    canvas.clear(skia.ColorBLACK)
    a = ease(local / 0.5) * ease((beat["dur"] - local) / 0.4)
    text(canvas, beat["text"], W / 2, H / 2 + 20, font("ExtraBold", 120), skia.ColorWHITE, a, "center", spacing=14)
    if beat.get("sub"):
        text(canvas, beat["sub"], W / 2, H / 2 + 100, font("Medium", 34), skia.Color(170, 175, 185),
             a * ease((local - 0.5) / 0.5), "center", spacing=6)


def draw_card(canvas, beat, local):
    canvas.clear(NAVY)
    canvas.drawRect(skia.Rect.MakeWH(W, 14), skia.Paint(Color=ORANGE))
    a = ease(local / 0.35)
    hf = font("ExtraBold", 118)
    hw = text(canvas, beat["header"], 200, 300 - 30 * (1 - a), hf, ORANGE, a, spacing=4)
    canvas.drawRect(skia.Rect.MakeXYWH(200, 336, hw * ease((local - 0.2) / 0.5), 8), skia.Paint(Color=skia.ColorWHITE))
    y = 480
    for i, (key, val) in enumerate(beat.get("rows", [])):
        ra = ease((local - 0.7 - i * 0.55) / 0.4)
        dx = 40 * (1 - ra)
        text(canvas, key, 200 + dx, y, font("ExtraBold", 40), ORANGE, ra, spacing=5)
        text(canvas, val, 620 + dx, y, font("Medium", 46), skia.ColorWHITE, ra)
        y += 104
    if beat.get("takeaway"):
        ta = ease((local - 0.9 - len(beat.get("rows", [])) * 0.55) / 0.5)
        box = skia.Paint(AntiAlias=True, Color=skia.Color(255, 255, 255, int(22 * ta)))
        canvas.drawRoundRect(skia.Rect.MakeXYWH(200, y + 10, W - 400, 110), 14, 14, box)
        canvas.drawRect(skia.Rect.MakeXYWH(200, y + 10, 10, 110), skia.Paint(Color=skia.Color(255, 138, 31, int(255 * ta))))
        text(canvas, beat["takeaway"], 250, y + 82, font("SemiBold", 46), skia.ColorWHITE, ta)


# ---------- audio ----------

def shaped_noise(n, lo, hi, seed):
    rng = np.random.default_rng(seed)
    spec = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR)
    shape = np.exp(-0.5 * ((np.log(np.maximum(f, 1)) - math.log(math.sqrt(lo * hi))) / (math.log(hi / lo) / 2.4)) ** 2)
    out = np.fft.irfft(spec * shape, n)
    return out / (np.abs(out).max() + 1e-9)


def soundtrack(beats, total):
    n = int(total * SR)
    t = np.arange(n) / SR
    narr = np.zeros(n)
    for b in beats:
        if "wav" in b:
            with wave.open(str(b["wav"])) as w:
                s = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
            i = int((b["start"] + LEAD) * SR)
            narr[i:i + len(s)] += s[:max(0, n - i)]
    narr *= 0.9 / (np.abs(narr).max() + 1e-9)

    # wind: loud outdoors, muffled indoors, silent-ish on cards
    gust = 0.6 + 0.25 * np.sin(t * 0.37) + 0.15 * np.sin(t * 0.9 + 1.3)
    target = np.zeros(n)
    for b in beats:
        level = {"chapter": 0.25, "card": 0.15}.get(b["type"], 1.0 if b.get("snow", 0) > 0 else 0.3)
        target[int(b["start"] * SR):int((b["start"] + b["dur"]) * SR)] = level
    k = int(0.5 * SR)
    target = np.convolve(target, np.ones(k) / k, mode="same")
    wind = (shaped_noise(n, 180, 900, 1) * 0.7 + shaped_noise(n, 900, 3500, 2) * 0.15 * gust) * gust * target * 0.2

    drone = (np.sin(2 * np.pi * 55 * t) + 0.5 * np.sin(2 * np.pi * 82.5 * t) + 0.3 * np.sin(2 * np.pi * 110.4 * t)) \
        * (0.75 + 0.25 * np.sin(t * 0.5)) * 0.07

    hits = np.zeros(n)
    for b in beats:
        if b["type"] in ("card", "chapter"):
            i = int(b["start"] * SR)
            m = min(int(1.6 * SR), n - i)
            tt = np.arange(m) / SR
            hits[i:i + m] += np.sin(2 * np.pi * (48 + 30 * np.exp(-tt * 9)) * tt) * np.exp(-tt * 3.2) * 0.45

    mix = narr + wind + drone + hits
    fade = np.minimum(1, np.minimum(t / 0.8, (total - t) / 1.2))
    mix = np.tanh(mix * fade * 1.1)
    return (mix * 32000).astype(np.int16)


# ---------- main ----------

def main(folder):
    folder = Path(folder)
    ep = json.loads((folder / "episode.json").read_text())
    beats, t = ep["beats"], 0.0
    used = set()
    for b in beats:
        if b.get("say"):
            b["wav"], _, backend = tts.synth(b["say"], **ep.get("voice", {}))
            used.add(backend)
            b["dur"] = LEAD + tts.wav_duration(b["wav"]) + TAIL
        b["start"] = t
        t += b["dur"]
    total = t + 0.8
    beats[-1]["dur"] += 0.8

    out = folder / "out"
    out.mkdir(exist_ok=True)
    wav_path = out / "mix.wav"
    with wave.open(str(wav_path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(soundtrack(beats, total).tobytes())

    mp4 = out / "scene.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-i", str(wav_path), "-c:v", "libx264", "-preset", "medium",
                           "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
                           str(mp4)], stdin=subprocess.PIPE)
    buf = np.zeros((H, W, 4), np.uint8)
    canvas = skia.Surface(buf).getCanvas()
    snow, images, i = Snow(), {}, 0
    n_frames = int(total * FPS)
    for f in range(n_frames):
        t = f / FPS
        while i + 1 < len(beats) and t >= beats[i + 1]["start"]:
            i += 1
        b, local = beats[i], t - beats[i]["start"]
        if b["type"] == "shot":
            if b["image"] not in images:
                images[b["image"]] = skia.Image.open(str(folder / b["image"]))
            draw_shot(canvas, b, images[b["image"]], local, t, snow)
        elif b["type"] == "card":
            draw_card(canvas, b, local)
        else:
            draw_chapter(canvas, b, local)
        fade = min(1.0, (total - t) / 1.0)
        if fade < 1:
            canvas.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Color=skia.Color(0, 0, 0, int(255 * (1 - max(fade, 0))))))
        ff.stdin.write(buf.tobytes())
    ff.stdin.close()
    if ff.wait():
        sys.exit("ffmpeg failed")
    wav_path.unlink()
    print(f"{mp4}  {total:.1f}s  voice: {', '.join(sorted(used))}")


if __name__ == "__main__":
    main(sys.argv[1])
