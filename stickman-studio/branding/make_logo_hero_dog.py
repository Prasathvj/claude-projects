#!/usr/bin/env python3
"""Draw the channel logo (800x800; YouTube crops it to a circle): the hero's head with its headlamp beam, and the dog."""
import sys
from pathlib import Path

import numpy as np
import skia

ROOT = Path(__file__).resolve().parents[1]
S = 800
INK, WHITE, ORANGE, LENS = skia.Color(20, 20, 24), skia.Color(250, 250, 252), skia.Color(240, 130, 40), skia.Color(255, 226, 140)

buf = np.zeros((S, S, 4), np.uint8)
surface = skia.Surface(buf)
c = surface.getCanvas()

bg = skia.GradientShader.MakeRadial((360, 330), 640, [skia.Color(36, 58, 98), skia.Color(9, 15, 28)])
c.drawRect(skia.Rect.MakeWH(S, S), skia.Paint(Shader=bg))
rng = np.random.default_rng(4)
for _ in range(40):
    x, y, r = rng.uniform(30, 770), rng.uniform(30, 770), rng.uniform(2, 5.5)
    c.drawCircle(float(x), float(y), float(r), skia.Paint(AntiAlias=True, Color=skia.Color(255, 255, 255, int(rng.uniform(60, 160)))))

hx, hy, R = 290, 395, 205
lamp_lens = (hx + 0.86 * R, hy - 0.46 * R)

# soft light behind the head, then the beam
glow = skia.GradientShader.MakeRadial(lamp_lens, 330, [skia.Color(255, 190, 90, 120), skia.Color(255, 170, 60, 0)])
c.drawCircle(lamp_lens[0], lamp_lens[1], 330, skia.Paint(Shader=glow))
beam = skia.Path()
beam.moveTo(*lamp_lens)
beam.lineTo(S + 60, 10)
beam.lineTo(S + 60, 330)
beam.close()
bs = skia.GradientShader.MakeLinear([lamp_lens, (S, 170)], [skia.Color(255, 200, 110, 215), skia.Color(255, 180, 70, 0)])
c.drawPath(beam, skia.Paint(AntiAlias=True, Shader=bs))

# head
stroke = skia.Paint(AntiAlias=True, Color=INK, Style=skia.Paint.kStroke_Style, StrokeWidth=R * 0.15,
                    StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
thin = skia.Paint(stroke)
thin.setStrokeWidth(R * 0.085)
c.drawCircle(hx, hy, R, skia.Paint(AntiAlias=True, Color=WHITE))
c.save()
clip = skia.Path()
clip.addCircle(hx, hy, R)
c.clipPath(clip, doAntiAlias=True)
c.drawRect(skia.Rect.MakeLTRB(hx - R, hy - 0.58 * R, hx + R, hy - 0.26 * R), skia.Paint(Color=skia.Color(45, 45, 50)))
c.restore()
c.drawCircle(hx, hy, R, stroke)
lamp = skia.Rect.MakeXYWH(hx + 0.42 * R, hy - 0.76 * R, 0.68 * R, 0.58 * R)
c.drawRoundRect(lamp, 0.1 * R, 0.1 * R, skia.Paint(AntiAlias=True, Color=ORANGE))
c.drawRoundRect(lamp, 0.1 * R, 0.1 * R, thin)
c.drawCircle(*lamp_lens, 0.15 * R, skia.Paint(AntiAlias=True, Color=LENS))
c.drawCircle(*lamp_lens, 0.15 * R, thin)
for ex in (hx + 0.22 * R - 0.3 * R, hx + 0.22 * R + 0.3 * R):
    c.drawOval(skia.Rect.MakeLTRB(ex - 0.085 * R, hy + 0.08 * R - 0.15 * R, ex + 0.085 * R, hy + 0.08 * R + 0.15 * R),
               skia.Paint(AntiAlias=True, Color=INK))
mouth = skia.Path()
mouth.moveTo(hx + 0.22 * R - 0.2 * R, hy + 0.52 * R)
mouth.quadTo(hx + 0.22 * R, hy + 0.74 * R, hx + 0.22 * R + 0.2 * R, hy + 0.52 * R)
c.drawPath(mouth, thin)

# the dog, bottom right
dog = skia.Image.open(str(ROOT / "assets" / "sprites" / "dog_sit.png"))
dh = 180
dw = dh * dog.width() / dog.height()
c.drawImageRect(dog, skia.Rect.MakeXYWH(452, 684 - dh, dw, dh), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear))

c.drawCircle(S / 2, S / 2, 382, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=18, Color=skia.Color(255, 150, 40)))
img = surface.makeImageSnapshot()
img.save(str(ROOT / "branding" / "logo_hero_dog.png"), skia.kPNG)

prev = np.zeros((S, S * 2, 4), np.uint8)
ps = skia.Surface(prev)
pc = ps.getCanvas()
pc.drawRect(skia.Rect.MakeWH(S, S), skia.Paint(Color=skia.Color(15, 15, 15)))
pc.drawRect(skia.Rect.MakeXYWH(S, 0, S, S), skia.Paint(Color=skia.Color(245, 245, 245)))
for ox in (0, S):
    pc.save()
    cl = skia.Path()
    cl.addCircle(ox + S / 2, S / 2, S / 2 * 0.9)
    pc.clipPath(cl, doAntiAlias=True)
    pc.translate(ox + S * 0.05, S * 0.05)
    pc.scale(0.9, 0.9)
    pc.drawImage(img, 0, 0)
    pc.restore()
ps.makeImageSnapshot().save(str(ROOT / "branding" / "logo_hero_dog_preview.png"), skia.kPNG)
print("ok")
