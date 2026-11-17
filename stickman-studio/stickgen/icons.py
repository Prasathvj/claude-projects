"""Small hand-drawn style icons. Each draws inside a box of side `s` centred on (0, 0)."""
import math

import skia

from .rig import INK


def _paints(s, accent):
    stroke = skia.Paint(AntiAlias=True, Color=INK, Style=skia.Paint.kStroke_Style, StrokeWidth=s * 0.06,
                        StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
    return stroke, skia.Paint(AntiAlias=True, Color=accent)


def _both(c, path, stroke, fill):
    c.drawPath(path, fill)
    c.drawPath(path, stroke)


def _poly(points):
    p = skia.Path()
    p.moveTo(*points[0])
    for pt in points[1:]:
        p.lineTo(*pt)
    p.close()
    return p


def bulb(c, s, st, fi):
    r = s * 0.3
    c.drawCircle(0, -s * 0.1, r, fi)
    c.drawCircle(0, -s * 0.1, r, st)
    for y in (0.28, 0.38):
        c.drawLine(-s * 0.13, s * y, s * 0.13, s * y, st)
    for a in range(-60, 61, 40):
        dx, dy = math.sin(math.radians(a)), -math.cos(math.radians(a))
        c.drawLine(dx * s * 0.4, -s * 0.1 + dy * s * 0.4, dx * s * 0.48, -s * 0.1 + dy * s * 0.48, st)


def clock(c, s, st, fi):
    c.drawCircle(0, 0, s * 0.42, fi)
    c.drawCircle(0, 0, s * 0.42, st)
    c.drawLine(0, 0, 0, -s * 0.27, st)
    c.drawLine(0, 0, s * 0.19, s * 0.08, st)


def question(c, s, st, fi):
    p = skia.Path()
    p.moveTo(-s * 0.2, -s * 0.2)
    p.cubicTo(-s * 0.2, -s * 0.52, s * 0.26, -s * 0.52, s * 0.24, -s * 0.2)
    p.cubicTo(s * 0.22, 0, 0, 0, 0, s * 0.18)
    big = skia.Paint(st)
    big.setStrokeWidth(s * 0.13)
    big.setColor(fi.getColor())
    c.drawPath(p, big)
    c.drawCircle(0, s * 0.4, s * 0.075, fi)


def heart(c, s, st, fi):
    p = skia.Path()
    p.moveTo(0, s * 0.38)
    p.cubicTo(-s * 0.62, -s * 0.05, -s * 0.3, -s * 0.5, 0, -s * 0.2)
    p.cubicTo(s * 0.3, -s * 0.5, s * 0.62, -s * 0.05, 0, s * 0.38)
    p.close()
    _both(c, p, st, fi)


def star(c, s, st, fi):
    pts = []
    for i in range(10):
        r = s * (0.46 if i % 2 == 0 else 0.2)
        a = math.radians(i * 36)
        pts.append((r * math.sin(a), -r * math.cos(a)))
    _both(c, _poly(pts), st, fi)


def coin(c, s, st, fi):
    c.drawCircle(0, 0, s * 0.42, fi)
    c.drawCircle(0, 0, s * 0.42, st)
    p = skia.Path()
    p.moveTo(s * 0.13, -s * 0.14)
    p.cubicTo(-s * 0.2, -s * 0.28, -s * 0.2, 0, 0, 0)
    p.cubicTo(s * 0.2, 0, s * 0.2, s * 0.28, -s * 0.13, s * 0.14)
    c.drawPath(p, st)
    c.drawLine(0, -s * 0.27, 0, s * 0.27, st)


def check(c, s, st, fi):
    c.drawCircle(0, 0, s * 0.42, fi)
    c.drawCircle(0, 0, s * 0.42, st)
    p = skia.Path()
    p.moveTo(-s * 0.2, 0)
    p.lineTo(-s * 0.05, s * 0.16)
    p.lineTo(s * 0.22, -s * 0.16)
    c.drawPath(p, st)


def cross(c, s, st, fi):
    c.drawCircle(0, 0, s * 0.42, fi)
    c.drawCircle(0, 0, s * 0.42, st)
    c.drawLine(-s * 0.17, -s * 0.17, s * 0.17, s * 0.17, st)
    c.drawLine(-s * 0.17, s * 0.17, s * 0.17, -s * 0.17, st)


def chart(c, s, st, fi):
    for i, h in enumerate((0.25, 0.42, 0.62, 0.85)):
        r = skia.Rect.MakeLTRB(-s * 0.42 + i * s * 0.22, s * 0.42 - h * s * 0.8, -s * 0.26 + i * s * 0.22, s * 0.42)
        c.drawRect(r, fi)
        c.drawRect(r, st)
    c.drawLine(-s * 0.48, s * 0.42, s * 0.48, s * 0.42, st)


def phone(c, s, st, fi):
    r = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-s * 0.24, -s * 0.45, s * 0.24, s * 0.45), s * 0.07, s * 0.07)
    c.drawRRect(r, fi)
    c.drawRRect(r, st)
    c.drawLine(-s * 0.07, s * 0.33, s * 0.07, s * 0.33, st)


def zzz(c, s, st, fi):
    big = skia.Paint(st)
    for k, (ox, oy) in zip((0.2, 0.15, 0.1), ((-0.2, 0.15), (0.12, -0.1), (0.34, -0.32))):
        p = skia.Path()
        p.moveTo((ox - k) * s, (oy - k) * s)
        p.lineTo((ox + k) * s, (oy - k) * s)
        p.lineTo((ox - k) * s, (oy + k) * s)
        p.lineTo((ox + k) * s, (oy + k) * s)
        c.drawPath(p, big)


def warning(c, s, st, fi):
    _both(c, _poly([(0, -s * 0.42), (s * 0.46, s * 0.38), (-s * 0.46, s * 0.38)]), st, fi)
    c.drawLine(0, -s * 0.12, 0, s * 0.1, st)
    c.drawCircle(0, s * 0.24, s * 0.035, skia.Paint(AntiAlias=True, Color=INK))


def target(c, s, st, fi):
    for r, p in ((0.44, fi), (0.28, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)), (0.12, fi)):
        c.drawCircle(0, 0, s * r, p)
        c.drawCircle(0, 0, s * r, st)


def book(c, s, st, fi):
    for sign in (-1, 1):
        p = _poly([(0, -s * 0.28), (sign * s * 0.46, -s * 0.36), (sign * s * 0.46, s * 0.3), (0, s * 0.38)])
        _both(c, p, st, fi)


ICONS = dict(bulb=bulb, clock=clock, question=question, heart=heart, star=star, coin=coin, check=check,
             cross=cross, chart=chart, phone=phone, zzz=zzz, warning=warning, target=target, book=book)


def draw_icon(canvas, name, x, y, size, accent):
    fn = ICONS.get(name)
    if not fn:
        return
    stroke, fill = _paints(size, accent)
    canvas.save()
    canvas.translate(x, y)
    fn(canvas, size, stroke, fill)
    canvas.restore()
