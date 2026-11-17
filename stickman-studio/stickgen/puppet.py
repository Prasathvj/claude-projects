"""Rigged channel characters: the hero (headlamp + backpack stickman), his dog, and a snowman gag prop.

The hero reuses the pose system in rig.py (joint angles). Everything is drawn facing right; pass
facing=-1 to mirror.
"""
import math
from pathlib import Path

import skia

from . import rig

INK = skia.Color(20, 20, 24)
WHITE = skia.Color(250, 250, 252)
OLIVE, OLIVE_DARK = skia.Color(112, 120, 62), skia.Color(88, 96, 48)
ORANGE, LENS = skia.Color(240, 130, 40), skia.Color(255, 226, 140)
SPRITES = Path(__file__).resolve().parent.parent / "assets" / "sprites"


# ---- extra actions on top of rig.ACTIONS ----

def dig(t, up=False):
    a = math.sin(t * 13)
    return rig._pose("angry", lean=38, head=-18, ar1=62 + 26 * a, ar2=96 + 30 * a, al1=58 - 26 * a, al2=92 - 30 * a,
                     ll1=62, ll2=-58, lr1=-6, lr2=-92)


def crouch_look(t, up=False):
    return rig._pose("surprised", lean=30, head=-24 + 2 * math.sin(t * 3), ar1=40, ar2=80, al1=30, al2=70,
                     ll1=62, ll2=-58, lr1=-6, lr2=-92)


def lean_talk(t, up=False):
    return rig._pose("happy", lean=-9, head=6 + 3 * math.sin(t * 3), ar1=70 + 14 * math.sin(t * 5), ar2=140 + 20 * math.sin(t * 5 + 1),
                     al1=-30, al2=-70, ll1=-4, ll2=-4, lr1=22, lr2=8)


def stomp_point(t, up=False):
    return rig._pose("angry", lean=6, head=4, ar1=98, ar2=98, al1=-40, al2=-110, ll1=-16, ll2=-10, lr1=18, lr2=12)


ACTIONS = dict(rig.ACTIONS, dig=dig, crouch_look=crouch_look, lean_talk=lean_talk, stomp_point=stomp_point)


def _dir(deg):
    r = math.radians(deg)
    return math.sin(r), math.cos(r)


def draw_hero(c, pose, x, feet_y, H, facing=1, mouth=0.0, t=0.0, squash=1.0, lamp=1.0, sweat=False):
    L, T, A, R, sw = 0.205 * H, 0.26 * H, 0.15 * H, 0.135 * H, 0.024 * H
    stroke = skia.Paint(AntiAlias=True, Color=INK, Style=skia.Paint.kStroke_Style, StrokeWidth=sw,
                        StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
    thin = skia.Paint(stroke)
    thin.setStrokeWidth(sw * 0.55)
    ink = skia.Paint(AntiAlias=True, Color=INK)
    white = skia.Paint(AntiAlias=True, Color=WHITE)

    c.drawOval(skia.Rect.MakeXYWH(x - 0.2 * H, feet_y - 0.02 * H, 0.4 * H, 0.045 * H),
               skia.Paint(AntiAlias=True, Color=skia.Color(0, 0, 20, 60)))
    c.save()
    c.translate(x, feet_y)
    c.scale(facing * (1 + (1 - squash) * 0.7), squash)

    reach = max(math.cos(math.radians(pose[a])) + math.cos(math.radians(pose[b]))
                for a, b in (("ll1", "ll2"), ("lr1", "lr2")))
    hip = (0.0, -reach * L - pose["dy"] * H)
    up = _dir(pose["lean"])
    sh = (hip[0] + up[0] * T, hip[1] - up[1] * T)
    hd = _dir(pose["lean"] + pose["head"])
    head = (sh[0] + hd[0] * (R + 0.01 * H), sh[1] - hd[1] * (R + 0.01 * H))

    def limb(origin, k1, k2, length):
        d1, d2 = _dir(pose[k1]), _dir(pose[k2])
        mid = (origin[0] + d1[0] * length, origin[1] + d1[1] * length)
        end = (mid[0] + d2[0] * length, mid[1] + d2[1] * length)
        p = skia.Path()
        p.moveTo(*origin)
        p.lineTo(*mid)
        p.lineTo(*end)
        c.drawPath(p, stroke)
        return end, pose[k2]

    def hand(pt):
        c.drawCircle(pt[0], pt[1], 0.032 * H, white)
        c.drawCircle(pt[0], pt[1], 0.032 * H, thin)

    def shoe(pt):
        r = skia.Rect.MakeXYWH(pt[0] - 0.022 * H, pt[1] - 0.034 * H, 0.085 * H, 0.046 * H)
        c.drawRoundRect(r, 0.022 * H, 0.022 * H, white)
        c.drawRoundRect(r, 0.022 * H, 0.022 * H, thin)

    end, _ = limb(sh, "al1", "al2", A)          # back arm
    hand(end)

    # backpack, hanging off the back of the torso
    c.save()
    c.translate((hip[0] + sh[0]) / 2, (hip[1] + sh[1]) / 2)
    c.rotate(pose["lean"])
    body = skia.Rect.MakeXYWH(-0.19 * H, -0.15 * H, 0.17 * H, 0.27 * H)
    c.drawRoundRect(body, 0.04 * H, 0.04 * H, skia.Paint(AntiAlias=True, Color=OLIVE))
    c.drawRoundRect(skia.Rect.MakeXYWH(-0.175 * H, 0.0, 0.11 * H, 0.09 * H), 0.02 * H, 0.02 * H,
                    skia.Paint(AntiAlias=True, Color=OLIVE_DARK))
    c.drawRoundRect(skia.Rect.MakeXYWH(-0.175 * H, 0.0, 0.11 * H, 0.09 * H), 0.02 * H, 0.02 * H, thin)
    c.drawLine(-0.19 * H, -0.07 * H, -0.02 * H, -0.07 * H, thin)
    c.drawRoundRect(body, 0.04 * H, 0.04 * H, thin)
    c.restore()

    for k1, k2 in (("ll1", "ll2"), ("lr1", "lr2")):
        end, _ = limb(hip, k1, k2, L)
        shoe(end)
    c.drawLine(hip[0], hip[1], sh[0], sh[1], stroke)

    # head
    c.save()
    c.translate(head[0], head[1])
    c.rotate((pose["lean"] + pose["head"]) * 0.6)
    c.drawCircle(0, 0, R, white)
    c.save()
    clip = skia.Path()
    clip.addCircle(0, 0, R)
    c.clipPath(clip, doAntiAlias=True)
    c.drawCircle(-0.35 * R, 0.3 * R, R * 1.02, skia.Paint(AntiAlias=True, Color=skia.Color(120, 140, 180, 0)))
    c.drawRect(skia.Rect.MakeLTRB(-R, -0.56 * R, R, -0.27 * R), skia.Paint(AntiAlias=True, Color=skia.Color(45, 45, 50)))
    c.restore()
    c.drawCircle(0, 0, R, stroke)
    lamp_box = skia.Rect.MakeXYWH(0.42 * R, -0.74 * R, 0.66 * R, 0.56 * R)
    c.drawRoundRect(lamp_box, 0.1 * R, 0.1 * R, skia.Paint(AntiAlias=True, Color=ORANGE))
    c.drawRoundRect(lamp_box, 0.1 * R, 0.1 * R, thin)
    c.drawCircle(0.86 * R, -0.46 * R, 0.14 * R, skia.Paint(AntiAlias=True, Color=LENS))
    c.drawCircle(0.86 * R, -0.46 * R, 0.14 * R, thin)
    if lamp > 0:
        glow = skia.GradientShader.MakeRadial((0.9 * R, -0.44 * R), 1.5 * R,
                                              [skia.Color(255, 190, 90, int(150 * lamp)), skia.Color(255, 170, 60, 0)])
        c.drawCircle(0.9 * R, -0.44 * R, 1.5 * R, skia.Paint(Shader=glow, BlendMode=skia.BlendMode.kPlus))

    mood = pose["mood"]
    ex, ey, gap = 0.22 * R, 0.08 * R, 0.3 * R
    big = mood in ("surprised", "scared")
    blink = (t % 3.3) < 0.11 and not big
    for sx in (ex - gap, ex + gap):
        if blink:
            c.drawLine(sx - 0.09 * R, ey, sx + 0.09 * R, ey, thin)
        else:
            c.drawOval(skia.Rect.MakeLTRB(sx - (0.1 if big else 0.075) * R, ey - (0.19 if big else 0.13) * R,
                                          sx + (0.1 if big else 0.075) * R, ey + (0.19 if big else 0.13) * R), ink)
    by, bw = ey - 0.33 * R, 0.13 * R
    if mood in ("angry", "sad", "scared", "confused"):
        for sx, inner in ((ex - gap, 1), (ex + gap, -1)):
            k = {"angry": -0.09, "sad": 0.08, "scared": 0.09, "confused": 0.0}[mood] * R * inner
            lift = 0.1 * R if (mood == "confused" and inner == -1) or mood == "scared" else 0
            c.drawLine(sx - bw, by + k - lift, sx + bw, by - k - lift, thin)
    mx, my = ex, 0.5 * R
    if mouth > 0.1 or mood in ("surprised", "scared"):
        open_h = (0.1 + 0.16 * mouth) * R if mouth > 0.1 else 0.16 * R
        c.drawOval(skia.Rect.MakeLTRB(mx - 0.13 * R, my - open_h * 0.4, mx + 0.13 * R, my + open_h), ink)
    else:
        bend = {"happy": 0.12, "sad": -0.1, "angry": -0.07}.get(mood, 0.0) * R
        p = skia.Path()
        p.moveTo(mx - 0.15 * R, my)
        p.quadTo(mx, my + bend * 2, mx + 0.15 * R, my)
        c.drawPath(p, thin)
    if sweat:
        drop = skia.Paint(AntiAlias=True, Color=skia.Color(150, 205, 255))
        for i, (dx, dy) in enumerate(((-0.95, -0.5), (-1.15, 0.0), (-0.85, 0.45))):
            ph = (t * 1.6 + i * 0.33) % 1
            c.drawOval(skia.Rect.MakeXYWH((dx - 0.2 * ph) * R, (dy + 0.5 * ph) * R, 0.13 * R, 0.2 * R), drop)
            c.drawOval(skia.Rect.MakeXYWH((dx - 0.2 * ph) * R, (dy + 0.5 * ph) * R, 0.13 * R, 0.2 * R), thin)
    c.restore()

    end, _ = limb(sh, "ar1", "ar2", A)          # front arm
    hand(end)
    c.restore()


def draw_snowman(c, x, feet_y, H, squash=1.0, t=0.0):
    stroke = skia.Paint(AntiAlias=True, Color=INK, Style=skia.Paint.kStroke_Style, StrokeWidth=0.022 * H,
                        StrokeCap=skia.Paint.kRound_Cap)
    white = skia.Paint(AntiAlias=True, Color=WHITE)
    ink = skia.Paint(AntiAlias=True, Color=INK)
    c.save()
    c.translate(x, feet_y)
    c.scale(1 + (1 - squash) * 0.7, squash)
    y = 0.0
    centers = []
    for r in (0.2 * H, 0.15 * H, 0.115 * H):
        y -= r
        centers.append((y, r))
        y -= r * 0.72
    for cy, r in centers:
        c.drawCircle(0, cy, r, white)
        c.drawCircle(0, cy, r, stroke)
    my, mr = centers[1]
    c.drawLine(-mr * 0.8, my, -mr * 2.0, my - mr * 0.9, stroke)
    c.drawLine(mr * 0.8, my, mr * 2.0, my - mr * 0.7, stroke)
    hy, hr = centers[2]
    c.drawRect(skia.Rect.MakeLTRB(-hr * 0.97, hy - 0.6 * hr, hr * 0.97, hy - 0.32 * hr), skia.Paint(Color=skia.Color(45, 45, 50)))
    box = skia.Rect.MakeXYWH(-0.25 * hr, hy - 0.72 * hr, 0.5 * hr, 0.44 * hr)
    c.drawRoundRect(box, 3, 3, skia.Paint(AntiAlias=True, Color=ORANGE))
    c.drawRoundRect(box, 3, 3, stroke)
    c.drawCircle(-0.33 * hr, hy + 0.02 * hr, 0.09 * hr, ink)
    c.drawCircle(0.33 * hr, hy + 0.02 * hr, 0.09 * hr, ink)
    nose = skia.Path()
    nose.moveTo(0, hy + 0.18 * hr)
    nose.lineTo(0.75 * hr, hy + 0.32 * hr)
    nose.lineTo(0, hy + 0.42 * hr)
    nose.close()
    c.drawPath(nose, skia.Paint(AntiAlias=True, Color=ORANGE))
    c.drawPath(nose, stroke)
    c.restore()


_sprites = {}


def draw_dog(c, kind, x, feet_y, H, facing=1, squash=1.0, rot=0.0):
    """kind is 'sit' or 'run'. The sprite faces right."""
    if kind not in _sprites:
        _sprites[kind] = skia.Image.open(str(SPRITES / f"dog_{kind}.png"))
    img = _sprites[kind]
    w = H * img.width() / img.height()
    c.drawOval(skia.Rect.MakeXYWH(x - w * 0.4, feet_y - H * 0.04, w * 0.8, H * 0.09),
               skia.Paint(AntiAlias=True, Color=skia.Color(0, 0, 20, 55)))
    c.save()
    c.translate(x, feet_y)
    c.rotate(rot)
    c.scale(facing * (1 + (1 - squash) * 0.7), squash)
    c.drawImageRect(img, skia.Rect.MakeXYWH(-w / 2, -H, w, H), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear))
    c.restore()
