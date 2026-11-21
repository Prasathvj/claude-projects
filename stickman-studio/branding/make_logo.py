#!/usr/bin/env python3
"""Neutral channel logo (800x800; YouTube crops it to a circle): a classic stick figure, not tied to any one character."""
from pathlib import Path

import numpy as np
import skia

ROOT = Path(__file__).resolve().parents[1]
S = 800
INK, WHITE = skia.Color(20, 20, 24), skia.Color(252, 250, 244)

buf = np.zeros((S, S, 4), np.uint8)
surface = skia.Surface(buf)
c = surface.getCanvas()

bg = skia.GradientShader.MakeRadial((400, 300), 620, [skia.Color(255, 176, 70), skia.Color(240, 120, 30)])
c.drawRect(skia.Rect.MakeWH(S, S), skia.Paint(Shader=bg))

line = skia.Paint(AntiAlias=True, Color=INK, Style=skia.Paint.kStroke_Style, StrokeWidth=30,
                  StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
thin = skia.Paint(line)
thin.setStrokeWidth(16)


def limb(*pts):
    p = skia.Path()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    c.drawPath(p, line)


# a stick figure with both arms raised, mid-"ta-da"
hx, hy, R = 400, 262, 100
shoulder, hip = (400, 392), (400, 548)
limb(shoulder, hip)
limb((400, 400), (318, 452), (226, 350))        # left arm
limb((400, 400), (482, 452), (574, 350))        # right arm
limb(hip, (340, 620), (318, 722))               # left leg
limb(hip, (460, 620), (482, 722))               # right leg
for hand in ((226, 350), (574, 350)):
    c.drawCircle(*hand, 24, skia.Paint(AntiAlias=True, Color=WHITE))
    c.drawCircle(*hand, 24, thin)
for foot in ((318, 722), (482, 722)):
    r = skia.Rect.MakeXYWH(foot[0] - 34 + (-8 if foot[0] < 400 else 8), foot[1] - 14, 70, 40)
    c.drawRoundRect(r, 20, 20, skia.Paint(AntiAlias=True, Color=WHITE))
    c.drawRoundRect(r, 20, 20, thin)

c.drawCircle(hx, hy, R, skia.Paint(AntiAlias=True, Color=WHITE))
c.drawCircle(hx, hy, R, line)
for ex in (hx - 34, hx + 34):
    c.drawOval(skia.Rect.MakeLTRB(ex - 9, hy - 28, ex + 9, hy + 4), skia.Paint(AntiAlias=True, Color=INK))
smile = skia.Path()
smile.moveTo(hx - 30, hy + 36)
smile.quadTo(hx, hy + 66, hx + 30, hy + 36)
c.drawPath(smile, thin)

# sparks of an idea around the raised hands
spark = skia.Paint(AntiAlias=True, Color=WHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=12, StrokeCap=skia.Paint.kRound_Cap)
for (x, y, dx, dy) in ((196, 292, -26, -26), (158, 352, -34, 0), (222, 244, -12, -36),
                       (604, 292, 26, -26), (642, 352, 34, 0), (578, 244, 12, -36)):
    c.drawLine(x, y, x + dx, y + dy, spark)

c.drawCircle(S / 2, S / 2, 382, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=18, Color=skia.Color(16, 26, 46)))
img = surface.makeImageSnapshot()
img.save(str(ROOT / "branding" / "logo.png"), skia.kPNG)

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
ps.makeImageSnapshot().save(str(ROOT / "branding" / "logo_preview.png"), skia.kPNG)
print("ok")
