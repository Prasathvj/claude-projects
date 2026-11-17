"""Turn a list of scenes into a narrated stickman video (16:9 or 9:16)."""
import subprocess
import wave
from pathlib import Path

import numpy as np
import skia

from . import rig, tts
from .icons import draw_icon

ROOT = Path(__file__).resolve().parent.parent
FPS = 30
GAP = 0.35          # silence after each scene
BLEND = 0.3         # seconds to move between poses
BG = skia.Color(251, 248, 241)

LAYOUTS = {
    "long": dict(W=1920, H=1080, man_x=470, ground=890, man_h=570, content=(1270, 400), text_w=1060,
                 font=124, icon=230, cap_y=1000, cap_font=52, up=False),
    "short": dict(W=1080, H=1920, man_x=540, ground=1400, man_h=640, content=(540, 480), text_w=960,
                  font=116, icon=250, cap_y=1540, cap_font=62, up=True),
}

FONT_CANDIDATES = [
    ROOT / "assets" / "font.ttf",
    "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
]


def typeface():
    for p in FONT_CANDIDATES:
        if Path(p).exists():
            tf = skia.Typeface.MakeFromFile(str(p))
            if tf:
                return tf
    return skia.Typeface("Arial", skia.FontStyle.Bold())


def color(hex_str, alpha=255):
    h = hex_str.lstrip("#")
    return skia.Color(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), alpha)


def wrap(text, tf, size, max_w, max_lines=3):
    """Greedy wrap, shrinking the font until the text fits in max_lines."""
    while True:
        font = skia.Font(tf, size)
        lines, cur = [], ""
        for word in text.split():
            trial = f"{cur} {word}".strip()
            if cur and font.measureText(trial) > max_w:
                lines.append(cur)
                cur = word
            else:
                cur = trial
        lines.append(cur)
        if (len(lines) <= max_lines and all(font.measureText(l) <= max_w for l in lines)) or size < 30:
            return font, lines
        size *= 0.9


def draw_headline(canvas, text, tf, cx, cy, size, max_w, accent, scale=1.0):
    """Centred headline with an accent highlighter stripe under each line."""
    font, lines = wrap(text, tf, size, max_w)
    lh = font.getSize() * 1.18
    ink = skia.Paint(AntiAlias=True, Color=rig.INK)
    mark = skia.Paint(AntiAlias=True, Color=accent)
    canvas.save()
    canvas.translate(cx, cy)
    canvas.scale(scale, scale)
    y = -lh * (len(lines) - 1) / 2 + font.getSize() * 0.35
    for line in lines:
        w = font.measureText(line)
        pad = font.getSize() * 0.12
        canvas.drawRoundRect(skia.Rect.MakeLTRB(-w / 2 - pad, y - font.getSize() * 0.36, w / 2 + pad,
                                                y + font.getSize() * 0.1), 10, 10, mark)
        canvas.drawString(line, -w / 2, y, font, ink)
        y += lh
    canvas.restore()
    return lh * len(lines)


def pop(x):
    """Ease-out-back from 0 to 1."""
    x = min(max(x, 0.0), 1.0)
    c = 1.70158
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def caption_chunks(words, max_words=4, max_chars=24):
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        text = " ".join(x[0] for x in cur)
        if len(cur) >= max_words or len(text) >= max_chars or w[0][-1:] in ".!?,;:":
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    return chunks


def draw_caption(canvas, chunk, t, tf, cx, cy, size, accent):
    font = skia.Font(tf, size)
    space = font.measureText(" ")
    widths = [font.measureText(w[0]) for w in chunk]
    total = sum(widths) + space * (len(chunk) - 1)
    pad_x, pad_y = size * 0.55, size * 0.38
    box = skia.Rect.MakeLTRB(cx - total / 2 - pad_x, cy - size * 0.5 - pad_y, cx + total / 2 + pad_x,
                             cy + size * 0.5 + pad_y)
    canvas.drawRoundRect(box, size * 0.45, size * 0.45, skia.Paint(AntiAlias=True, Color=rig.INK))
    x = cx - total / 2
    for (word, start, end), w in zip(chunk, widths):
        active = start <= t
        paint = skia.Paint(AntiAlias=True, Color=accent if active and t < end + 0.08 else skia.ColorWHITE)
        canvas.drawString(word, x, cy + size * 0.36, font, paint)
        x += w + space


def prepare(scenes, voice):
    """Synthesize narration; return (timeline, samples). Each timeline item has start/dur/words."""
    timeline, audio, t = [], [], 0.0
    backends = set()
    for i, sc in enumerate(scenes):
        wav, words, backend = tts.synth(sc["say"], **voice)
        backends.add(backend)
        with wave.open(str(wav)) as w:
            samples = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
        tail = GAP + (0.6 if i == len(scenes) - 1 else 0)
        samples = np.concatenate([samples, np.zeros(int(tail * tts.RATE), np.int16)])
        dur = len(samples) / tts.RATE
        timeline.append(dict(scene=sc, start=t, dur=dur, words=words, chunks=caption_chunks(words)))
        audio.append(samples)
        t += dur
    return timeline, np.concatenate(audio), backends


def envelope(samples, n_frames):
    """Loudness per video frame, 0..1, used to open the mouth."""
    step = tts.RATE // FPS
    env = np.zeros(n_frames)
    for i in range(n_frames):
        seg = samples[i * step:(i + 1) * step].astype(np.float32)
        if len(seg):
            env[i] = np.sqrt(np.mean(seg ** 2))
    peak = np.percentile(env, 95) or 1.0
    return np.clip(env / peak, 0, 1)


def draw_frame(canvas, L, tf, accent, item, prev_item, t, mouth):
    sc = item["scene"]
    local = t - item["start"]
    canvas.clear(BG)
    cx, cy = L["content"]
    canvas.drawCircle(cx, cy, L["text_w"] * 0.5, skia.Paint(AntiAlias=True, Color=skia.Color(0, 0, 0, 10)))
    canvas.drawLine(0, L["ground"], L["W"], L["ground"],
                    skia.Paint(AntiAlias=True, Color=skia.Color(27, 27, 31, 60), StrokeWidth=6))

    # headline + icon
    s = pop((local - 0.12) / 0.35)
    text, icon = sc.get("text"), sc.get("icon")
    if s > 0 and (text or icon):
        if icon and text:
            draw_icon_scaled(canvas, icon, cx, cy - L["icon"] * 0.75, L["icon"] * s, accent, local)
            draw_headline(canvas, text, tf, cx, cy + L["icon"] * 0.45, L["font"] * 0.85, L["text_w"], accent, s)
        elif icon:
            draw_icon_scaled(canvas, icon, cx, cy, L["icon"] * 1.5 * s, accent, local)
        else:
            draw_headline(canvas, text, tf, cx, cy, L["font"], L["text_w"], accent, s)

    # stickman, easing out of the previous scene's pose
    pose = rig.ACTIONS.get(sc.get("action", "talk"), rig.talk)(t, L["up"])
    if prev_item and local < BLEND:
        prev = rig.ACTIONS.get(prev_item["scene"].get("action", "talk"), rig.talk)(t, L["up"])
        pose = rig.blend(prev, pose, local / BLEND)
    rig.draw(canvas, pose, L["man_x"], L["ground"], L["man_h"], mouth=mouth, t=t)

    for chunk in item["chunks"]:
        end = chunk[-1][2] + 0.25
        if chunk[0][1] <= local < end:
            draw_caption(canvas, chunk, local, tf, L["W"] / 2, L["cap_y"], L["cap_font"], accent)
            break


def draw_icon_scaled(canvas, name, x, y, size, accent, local):
    import math
    draw_icon(canvas, name, x, y + 8 * math.sin(local * 2.2), size, accent)


def render(scenes, fmt, out_path, accent="#FFC233", voice=None, music=None):
    L = LAYOUTS[fmt]
    tf = typeface()
    acc = color(accent)
    timeline, samples, backends = prepare(scenes, voice or {})
    total = len(samples) / tts.RATE
    n_frames = int(total * FPS)
    env = envelope(samples, n_frames)

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    wav_path = out_path.with_suffix(".wav")
    with wave.open(str(wav_path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(tts.RATE)
        w.writeframes(samples.tobytes())

    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba",
           "-s", f"{L['W']}x{L['H']}", "-r", str(FPS), "-i", "-", "-i", str(wav_path)]
    if music:
        cmd += ["-stream_loop", "-1", "-i", str(music), "-filter_complex",
                "[2:a]volume=0.07[m];[1:a][m]amix=inputs=2:duration=first:normalize=0[a]",
                "-map", "0:v", "-map", "[a]"]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "160k", "-t", f"{total:.3f}", "-movflags", "+faststart", str(out_path)]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    buf = np.zeros((L["H"], L["W"], 4), np.uint8)
    canvas = skia.Surface(buf).getCanvas()
    idx = 0
    for f in range(n_frames):
        t = f / FPS
        while idx + 1 < len(timeline) and t >= timeline[idx + 1]["start"]:
            idx += 1
        draw_frame(canvas, L, tf, acc, timeline[idx], timeline[idx - 1] if idx else None, t, env[f])
        ff.stdin.write(buf.tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError("ffmpeg failed")
    wav_path.unlink()
    return dict(path=str(out_path), seconds=round(total, 1), tts=sorted(backends))


def thumbnail(text, out_path, accent="#FFC233", action="point"):
    W, H = 1280, 720
    tf = typeface()
    buf = np.zeros((H, W, 4), np.uint8)
    surface = skia.Surface(buf)
    canvas = surface.getCanvas()
    canvas.clear(color(accent))
    canvas.drawCircle(300, 420, 330, skia.Paint(AntiAlias=True, Color=skia.Color(255, 255, 255, 70)))
    pose = rig.ACTIONS.get(action, rig.point)(0.4, False)
    rig.draw(canvas, pose, 300, 670, 560, t=1.0)
    draw_headline(canvas, text.upper(), tf, 860, 350, 150, 740, skia.ColorWHITE)
    surface.makeImageSnapshot().save(str(out_path), skia.kPNG)
    return str(out_path)
