"""Stickman rig: poses are joint angles, actions are functions of time.

Angles are degrees measured from "straight down", positive toward screen right.
0 = down, 90 = right, 180 = up, -90 = left.
"""
import math

import skia

INK = skia.Color(27, 27, 31)
POSE_KEYS = ["lean", "head", "al1", "al2", "ar1", "ar2", "ll1", "ll2", "lr1", "lr2", "dy"]
STAND = dict(lean=0, head=0, al1=-12, al2=-6, ar1=12, ar2=6, ll1=-9, ll2=-9, lr1=9, lr2=9, dy=0)


def _s(t, speed, phase=0.0):
    return math.sin(t * speed + phase)


def _pose(mood="neutral", **kw):
    p = dict(STAND)
    p.update(kw)
    p["mood"] = mood
    return p


def idle(t, up):
    return _pose(lean=1.5 * _s(t, 2), ar1=12 + 2 * _s(t, 2), al1=-12 - 2 * _s(t, 2))


def talk(t, up):
    return _pose(head=4 * _s(t, 2.2), ar1=58 + 12 * _s(t, 3), ar2=125 + 22 * _s(t, 3, 1),
                 al1=-18 - 5 * _s(t, 2.5), al2=-30 - 12 * _s(t, 2.5, 0.6))


def point(t, up):
    a = (158 if up else 104) + 3 * _s(t, 4)
    return _pose("happy", ar1=a, ar2=a, head=-4 if up else 3, lean=2)


def wave(t, up):
    return _pose("happy", ar1=150, ar2=168 + 26 * _s(t, 9), head=5 * _s(t, 4.5))


def think(t, up):
    return _pose(head=-9 + 2 * _s(t, 1.5), ar1=32, ar2=166 + 3 * _s(t, 2), al1=20, al2=62, lean=-2)


def shrug(t, up):
    lift = 6 * _s(t, 2.5)
    return _pose("confused", al1=-42, al2=-122 - lift, ar1=42, ar2=122 + lift, head=7 * _s(t, 2.5))


def celebrate(t, up):
    w = 12 * _s(t, 10)
    return _pose("happy", al1=-150, al2=-165 + w, ar1=150, ar2=165 + w, dy=0.07 * abs(_s(t, 5)),
                 ll1=-14, ll2=-6, lr1=14, lr2=6)


def sad(t, up):
    return _pose("sad", lean=13, head=20 + 2 * _s(t, 1.5), al1=3, al2=6, ar1=9, ar2=13)


def shock(t, up):
    j = 2 * _s(t, 30)
    return _pose("surprised", lean=-8, al1=-118 + j, al2=-152, ar1=118 + j, ar2=152,
                 ll1=-16, ll2=-10, lr1=16, lr2=10)


def facepalm(t, up):
    return _pose("sad", head=14, lean=5, ar1=28, ar2=176, al1=-8, al2=-4)


def _stride(t, speed, amp, lean, mood):
    p = t * speed
    a, b = amp * math.sin(p), amp * math.sin(p + math.pi)
    return _pose(mood, lean=lean,
                 ll1=a, ll2=a - amp * 0.9 * (1 + math.cos(p)) / 2,
                 lr1=b, lr2=b - amp * 0.9 * (1 + math.cos(p + math.pi)) / 2,
                 al1=b * 0.9, al2=b * 0.9 + amp, ar1=a * 0.9, ar2=a * 0.9 + amp)


def walk(t, up):
    return _stride(t, 6.5, 26, 4, "neutral")


def run(t, up):
    return _stride(t, 12, 42, 13, "surprised")


ACTIONS = dict(idle=idle, talk=talk, point=point, wave=wave, think=think, shrug=shrug,
               celebrate=celebrate, sad=sad, shock=shock, facepalm=facepalm, walk=walk, run=run)


def blend(a, b, s):
    s = s * s * (3 - 2 * s)
    out = {k: a[k] + (b[k] - a[k]) * s for k in POSE_KEYS}
    out["mood"] = b["mood"] if s > 0.5 else a["mood"]
    return out


def _dir(deg):
    r = math.radians(deg)
    return math.sin(r), math.cos(r)


def draw(canvas, pose, x, ground_y, H, mouth=0.0, t=0.0, head_fill=skia.ColorWHITE, ink=INK):
    """Draw the stickman standing at (x, ground_y), total height about H. mouth is 0..1."""
    L, T, A, R = 0.235 * H, 0.30 * H, 0.17 * H, 0.10 * H
    sw = 0.036 * H
    stroke = skia.Paint(AntiAlias=True, Color=ink, Style=skia.Paint.kStroke_Style, StrokeWidth=sw,
                        StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
    fill = skia.Paint(AntiAlias=True, Color=ink)

    def seg(origin, a1, a2, length):
        d1, d2 = _dir(a1), _dir(a2)
        mid = (origin[0] + d1[0] * length, origin[1] + d1[1] * length)
        return mid, (mid[0] + d2[0] * length, mid[1] + d2[1] * length)

    reach = max(math.cos(math.radians(pose[k1])) + math.cos(math.radians(pose[k2]))
                for k1, k2 in (("ll1", "ll2"), ("lr1", "lr2")))
    jump = pose["dy"] * H
    hip = (x, ground_y - reach * L - jump)
    up = _dir(pose["lean"])
    sh = (hip[0] + up[0] * T, hip[1] - up[1] * T)
    hd = _dir(pose["lean"] + pose["head"])
    head = (sh[0] + hd[0] * (R + 0.02 * H), sh[1] - hd[1] * (R + 0.02 * H))

    # ground shadow shrinks while jumping
    k = 1 - min(jump / (0.2 * H), 0.6)
    canvas.drawOval(skia.Rect.MakeXYWH(x - 0.2 * H * k, ground_y - 0.018 * H, 0.4 * H * k, 0.036 * H),
                    skia.Paint(AntiAlias=True, Color=skia.Color(0, 0, 0, 28)))

    def limb(origin, k1, k2, length):
        mid, end = seg(origin, pose[k1], pose[k2], length)
        path = skia.Path()
        path.moveTo(*origin)
        path.lineTo(*mid)
        path.lineTo(*end)
        canvas.drawPath(path, stroke)

    limb(sh, "al1", "al2", A)
    limb(hip, "ll1", "ll2", L)
    limb(hip, "lr1", "lr2", L)
    canvas.drawLine(hip[0], hip[1], sh[0], sh[1], stroke)
    canvas.drawCircle(head[0], head[1], R, skia.Paint(AntiAlias=True, Color=head_fill))
    canvas.drawCircle(head[0], head[1], R, stroke)

    # face, looking slightly toward screen right
    canvas.save()
    canvas.translate(head[0], head[1])
    canvas.rotate(-(pose["lean"] + pose["head"]) * 0.6)
    ex, ey, gap = 0.018 * H, -0.012 * H, 0.034 * H
    thin = skia.Paint(AntiAlias=True, Color=ink, Style=skia.Paint.kStroke_Style, StrokeWidth=sw * 0.45,
                      StrokeCap=skia.Paint.kRound_Cap)
    mood = pose["mood"]
    blinking = (t % 3.7) < 0.12
    for sx in (ex - gap, ex + gap):
        if blinking:
            canvas.drawLine(sx - 0.012 * H, ey, sx + 0.012 * H, ey, thin)
        else:
            canvas.drawCircle(sx, ey, (0.019 if mood == "surprised" else 0.014) * H, fill)
    if mood in ("sad", "confused"):
        bw, by, tilt = 0.017 * H, ey - 0.032 * H, 0.011 * H
        for sx, inner in ((ex - gap, 1), (ex + gap, -1)):
            if mood == "sad":      # inner ends raised
                canvas.drawLine(sx - bw, by + tilt * inner, sx + bw, by - tilt * inner, thin)
            else:                  # one eyebrow raised
                lift = 0.016 * H if inner == -1 else 0
                canvas.drawLine(sx - bw, by - lift, sx + bw, by - lift, thin)
    my, mw = 0.042 * H, 0.03 * H
    if mouth > 0.08:
        canvas.drawOval(skia.Rect.MakeLTRB(ex - mw * 0.8, my - 0.004 * H, ex + mw * 0.8,
                                           my + (0.012 + 0.034 * mouth) * H), fill)
    elif mood == "surprised":
        canvas.drawCircle(ex, my + 0.008 * H, 0.016 * H, fill)
    else:
        bend = {"happy": 0.024, "sad": -0.018}.get(mood, 0.006) * H
        path = skia.Path()
        path.moveTo(ex - mw, my)
        path.quadTo(ex, my + bend * 2, ex + mw, my)
        canvas.drawPath(path, thin)
    canvas.restore()

    limb(sh, "ar1", "ar2", A)
