#!/usr/bin/env python3
"""Thumbnail for the blizzard long video (1280x720)."""
import sys
from pathlib import Path

import numpy as np
import skia

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from stickgen import puppet, stage  # noqa: E402

W, H = 1280, 720
buf = np.zeros((H, W, 4), np.uint8)
surface = skia.Surface(buf)
c = surface.getCanvas()

# night road, mirrored so the car sits on the right and the text has empty snow on the left
img = skia.Image.open(str(Path(__file__).parent / "shots" / "night.jpg"))
c.save()
c.translate(W, 0)
c.scale(-1, 1)
scale = H / img.height()
c.drawImageRect(img, skia.Rect.MakeWH(img.width(), img.height()), skia.Rect.MakeXYWH(0, 0, img.width() * scale * 1.08, H * 1.08),   # slight zoom crops the corner watermark
                skia.SamplingOptions(skia.CubicResampler.Mitchell()))
c.restore()
c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Color=skia.Color(4, 8, 20, 70)))
vig = skia.GradientShader.MakeRadial((W * 0.6, H * 0.5), W * 0.75, [skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 170)], [0.5, 1.0])
c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=vig))
stage.Snow(W, H, seed=9).draw(c, 3.0, 1.0, wind=0.8)

# hero, scared, big, in front of the car
pose = puppet.ACTIONS["shock"](0.3, False)
pose["mood"] = "scared"
puppet.draw_hero(c, pose, 1010, 700, 640, facing=1, t=1.0, lamp=1.0)

# headline
lines = [("DON'T", skia.ColorWHITE), ("WALK", skia.Color(255, 150, 40)), ("AWAY", skia.ColorWHITE)]
size = 168
f = stage.font("Black", size)
y = 215
for text, color in lines:
    c.save()
    c.translate(40, y)
    c.rotate(-3)
    stage.outlined(c, text, 0, 0, f, color, size * 0.13)
    c.restore()
    y += size * 0.93
surface.makeImageSnapshot().save(str(Path(__file__).parent / "out" / "thumbnail.png"), skia.kPNG)
print("ok")
