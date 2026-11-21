#!/usr/bin/env python3
"""Puppet director: renders an episode described as data (see PUPPET.md).

    python direct.py episodes/night-one/short.json                # full render -> out/short.mp4
    python direct.py episodes/night-one/short.json --check        # validate only (no narration, no render)
    python direct.py episodes/night-one/short.json --frames 1,5,9 # stills for checking
"""
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
import skia

from stickgen import gtts, puppet, rig, stage, tts
from stickgen.stage import clamp, lerp, smooth, snap

FPS, SR = 30, tts.RATE
LAYOUT = {
    "short": dict(W=1080, H=1920, cap_y=1500, cap_size=92, impact_y=430, impact_size=230, sticker_y=400, sticker_dy=120),
    "long": dict(W=1920, H=1080, cap_y=985, cap_size=78, impact_y=300, impact_size=210, sticker_y=170, sticker_dy=105),
}
EASES = {"smooth": smooth, "snap": snap, "linear": clamp}
DOG_DOES = ("sit", "dig", "play")
FX = ("hit", "impact", "sticker", "sparkle", "chunks", "smoke", "dark", "wind_lines", "sfx", "shake", "dust", "diagram", "verdict")
SFX = ("whoosh", "thud", "pop", "ding", "crunch", "rumble")
SPEED = {"hero": 170, "dog": 230}


class Problem(Exception):
    pass


class Shot:
    def __init__(self, spec, index, start, dur, words):
        self.spec, self.index, self.start, self.dur, self.words = spec, index, start, dur, words

    def when(self, item, default=0.0):
        """Local time of a step/event: {"at": seconds|"end"} or {"on": "spoken word"} plus optional "delay"."""
        if "on" in item:
            needle, nth = item["on"], 0
            if "#" in needle:
                needle, n = needle.split("#")
                nth = int(n) - 1
            hits = [a for w, a, b in self.words if needle.lower() in w.lower()]
            if len(hits) <= nth:
                raise Problem(f"shot {self.index + 1}: word '{item['on']}' is not in this shot's narration")
            base = hits[nth] - self.start
        elif "at" in item:
            base = self.dur if item["at"] == "end" else float(item["at"])
        else:
            base = default
        return base + item.get("delay", 0.0)


class Director:
    def __init__(self, path, synth=True):
        self.path = Path(path)
        self.ep = json.loads(self.path.read_text())
        self.L = LAYOUT[self.ep.get("format", "short")]
        self.W, self.H = self.L["W"], self.L["H"]
        self.sets = self.ep["sets"]
        self.images = {}
        self.vclips = {}
        self.snow = stage.Snow(self.W, self.H)
        self._time_shots(synth)
        self._resolve()

    # ---------- timing ----------
    def _time_shots(self, synth):
        self.shots, self.clips, t = [], [], 0.3
        gap = self.ep.get("gap", 0.16)
        takes = {}
        lines = [(i, sp["say"], sp.get("direct", "")) for i, sp in enumerate(self.ep["shots"]) if sp.get("say")]
        if synth and self.ep.get("tts_batch"):                 # several lines per request: one voice, few requests
            size = int(self.ep["tts_batch"])
            for k in range(0, len(lines), size):
                block = lines[k:k + size]
                try:
                    got = gtts.say_batch([(t_, d_) for _, t_, d_ in block], self.ep.get("voice", "Fenrir"),
                                         self.ep.get("tts_model", gtts.MODEL), self.ep.get("voice_profile") or gtts.CALM_PROFILE)
                    for (idx, _, _), r in zip(block, got):
                        takes[idx] = r
                except ValueError as e:
                    print("could not split a batch, reading those lines one at a time:", e)
        for i, spec in enumerate(self.ep["shots"]):
            text = spec.get("say", "")
            if text and synth:
                wav, dur = takes[i] if i in takes else gtts.say(text, spec.get("direct", ""), self.ep.get("voice", "Fenrir"),
                                                                 self.ep.get("tts_model", gtts.MODEL),
                                                                 self.ep.get("voice_profile") or (gtts.CALM_PROFILE if self.ep.get("tts_batch") else None))
                wav, dur = gtts.clean(wav)                      # remove the end-of-clip burst, add fades
                cap = self.ep.get("max_wpm")
                if cap and len(text.split()) / dur * 60 > cap:     # slow down lines that came out rushed
                    wav, dur = gtts.stretch(wav, cap / (len(text.split()) / dur * 60))
                self.clips.append((wav, t))
            else:
                dur = max(len(text.split()) * 0.33, spec.get("hold", 1.5 if not text else 0))
            words = [(w, a + t, b + t) for w, a, b in tts._estimate_words(text, dur)] if text else []
            start = 0.0 if i == 0 else t - 0.06
            self.shots.append(Shot(spec, i, start, 0, words))
            t += dur + gap
        self.total = t + 0.7
        for a, b in zip(self.shots, self.shots[1:] + [None]):
            a.dur = (b.start if b else self.total) - a.start
        self.all_words = [w for s in self.shots for w in s.words]

    # ---------- resolve actors, cameras, events ----------
    def mark(self, set_name, ref, shot):
        if isinstance(ref, (list, tuple)):
            return float(ref[0]), float(ref[1])
        marks = self.sets[set_name].get("marks", {})
        if ref not in marks:
            raise Problem(f"shot {shot.index + 1}: unknown mark '{ref}' (set '{set_name}' has: {', '.join(marks)})")
        return tuple(map(float, marks[ref]))

    def _resolve(self):
        last = {}       # (set, actor) -> (pos, facing)
        for shot in self.shots:
            spec = shot.spec
            if spec.get("type") == "card":
                if self.ep.get("format", "short") != "long":
                    raise Problem(f"shot {shot.index + 1}: cards are only supported in format 'long'")
                if not spec.get("header"):
                    raise Problem(f"shot {shot.index + 1}: a card needs a 'header'")
                for row in spec.get("rows", []):
                    if not (isinstance(row, list) and len(row) == 2):
                        raise Problem(f"shot {shot.index + 1}: card rows must look like [\"KEY\", \"value\"]")
                shot.tracks, shot.cam, shot.events, shot.hits = {}, [], [], []
                continue
            if spec.get("set") not in self.sets:
                raise Problem(f"shot {shot.index + 1}: unknown set '{spec.get('set')}' (have: {', '.join(self.sets)})")
            sname = spec["set"]
            shot.tracks = {}
            order = sorted(spec.get("actors", {}), key=lambda a: any("follow" in s for s in spec["actors"][a]))
            for actor in order:
                if actor not in ("hero", "dog"):
                    raise Problem(f"shot {shot.index + 1}: unknown actor '{actor}' (use hero, dog)")
                steps, track, t_prev = spec["actors"][actor], [], 0.0
                pos, facing = last.get((sname, actor), (self.mark(sname, actor, shot), 1))
                for step in steps:
                    do = step.get("do")
                    valid = puppet.ACTIONS if actor == "hero" else DOG_DOES
                    if do and do not in valid:
                        raise Problem(f"shot {shot.index + 1}: {actor} cannot '{do}' (use: {', '.join(valid)})")
                    t0 = shot.when(step, t_prev)
                    if track:                     # where the actor had got to when this step begins
                        pos = self._track_pos(shot, track, t0)
                    if "from" in step:
                        pos = self.mark(sname, step["from"], shot)
                    end, move = pos, 0.0
                    if "to" in step:
                        end = self.mark(sname, step["to"], shot)
                        dist = math.hypot(end[0] - pos[0], end[1] - pos[1])
                        move = step.get("for") or dist / step.get("speed", SPEED[actor])
                        if abs(end[0] - pos[0]) > 1:
                            facing = 1 if end[0] > pos[0] else -1
                    if "face" in step:
                        f = step["face"]
                        facing = {"left": -1, "right": 1}.get(f) or (1 if self.mark(sname, f, shot)[0] >= pos[0] else -1)
                    track.append(dict(step, t0=t0, p0=pos, p1=end, move=move, facing=facing))
                    t_prev = t0 + move
                shot.tracks[actor] = track
                last[(sname, actor)] = (self._track_pos(shot, track, shot.dur), track[-1]["facing"])

            # camera keys inherit missing fields from the previous key
            cam, prev = [], {"zoom": None, "dx": 0, "dy": 0}
            for key in spec.get("camera", [{"view": "wide"}]):
                k = dict(prev, **key)
                if "z" in key:                                   # full-frame zoom on the whole picture
                    k.pop("view", None)
                    k.pop("follow", None)
                elif "view" in key or "follow" in key:
                    for n in ("z", "fx", "fy"):
                        k.pop(n, None)
                if "view" in key:
                    k.pop("follow", None)
                    k["zoom"] = key.get("zoom")
                if "follow" in key:
                    k.pop("view", None)
                k["t"] = shot.when(key, 0.0)
                if "view" in k and not isinstance(k["view"], list):
                    views = self.sets[sname].get("views", {})
                    if k["view"] not in views:
                        raise Problem(f"shot {shot.index + 1}: unknown view '{k['view']}' (have: {', '.join(views)})")
                if k.get("ease", "smooth") not in EASES:
                    raise Problem(f"shot {shot.index + 1}: unknown ease '{k['ease']}' (use: {', '.join(EASES)})")
                cam.append(k)
                prev = {x: k[x] for x in k if x not in ("t", "at", "on", "delay", "ease")}
            shot.cam = cam

            shot.events, shot.hits = [], []
            for ev in spec.get("events", []):
                if ev.get("fx") not in FX:
                    raise Problem(f"shot {shot.index + 1}: unknown fx '{ev.get('fx')}' (use: {', '.join(FX)})")
                if ev["fx"] == "sfx" and ev.get("name") not in SFX:
                    raise Problem(f"shot {shot.index + 1}: unknown sfx '{ev.get('name')}' (use: {', '.join(SFX)})")
                e = dict(ev, t=shot.when(ev, 0.0))
                e["end"] = shot.when({k[3:]: v for k, v in ev.items() if k in ("to_on", "to_at")}, shot.dur) \
                    if ("to_on" in ev or "to_at" in ev) else shot.dur
                if "mark" in e:
                    e["xy"] = self.mark(sname, e["mark"], shot)
                shot.events.append(e)
                if e["fx"] in ("hit", "impact"):
                    shot.hits.append(e["t"])

    # ---------- actor state ----------
    @staticmethod
    def _active(track, lt):
        cur = None
        for i, s in enumerate(track):
            if s["t0"] <= lt + 1e-6:
                cur = i
        return cur

    def _track_pos(self, shot, track, lt):
        i = self._active(track, lt)
        if i is None:
            return track[0]["p0"]
        s = track[i]
        if "follow" in s:
            tx, ty = self._track_pos(shot, shot.tracks[s["follow"]], lt)
            return tx + s.get("dx", 0), ty + s.get("dy", 0)
        if s["move"] <= 0:
            return s["p1"]
        k = clamp((lt - s["t0"]) / s["move"])
        return lerp(s["p0"][0], s["p1"][0], k), lerp(s["p0"][1], s["p1"][1], k)

    def _state(self, shot, actor, lt):
        """-> dict(pos, facing, action, since, prev, step) or None while the actor has not appeared."""
        track = shot.tracks[actor]
        i = self._active(track, lt)
        if i is None:
            return None
        s = track[i]
        pos = self._track_pos(shot, track, lt)
        if "follow" in s:
            tgt = self._state(shot, s["follow"], lt)
            moving, facing = bool(tgt and tgt["moving"]), (tgt["facing"] if tgt and tgt["moving"] else s["facing"])
            since = lt - s["t0"]
        else:
            moving, facing = s["move"] > 0 and lt < s["t0"] + s["move"], s["facing"]
            since = lt - s["t0"] - (0 if moving else s["move"])
        rest = s.get("do", "idle" if actor == "hero" else "sit")
        action = s.get("gait", "walk") if moving else rest
        prev = s.get("gait", "walk") if (not moving and s["move"] > 0) else (
            track[i - 1].get("do", "idle") if i else action)
        return dict(pos=pos, facing=facing, action=action, since=since, prev=prev, step=s, moving=moving)

    def _bump(self, shot, lt):
        return max([math.sin(clamp((lt - h) / 0.28) * math.pi) for h in shot.hits] + [0.0])

    # ---------- drawing ----------
    def _clip_frames(self, clip, delogo=None):
        """Decode a video clip once into a folder of JPEG frames (cached next to the episode)."""
        if clip in self.vclips:
            return self.vclips[clip]
        src = self.path.parent / clip
        out = self.path.parent / "out" / ".clips" / Path(clip).stem
        if not list(out.glob("*.jpg")):
            out.mkdir(parents=True, exist_ok=True)
            scale = "scale='min(1920,iw)':-2" if self.W > self.H else "scale=-2:'min(1920,ih)'"
            logo = f"delogo=x={delogo[0]}:y={delogo[1]}:w={delogo[2]}:h={delogo[3]}," if delogo else ""   # hides a corner watermark
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(src), "-an", "-vf", f"{logo}fps={FPS},{scale}",
                            "-q:v", "3", str(out / "%05d.jpg")], check=True)
        frames = sorted(out.resolve().glob("*.jpg"))
        if not frames:
            raise SystemExit(f"no frames decoded from {src}")
        self.vclips[clip] = frames
        return frames

    def _bg(self, shot, lt=0.0):
        sset = self.sets[shot.spec["set"]]
        if "clip" in sset:            # video clip background: loop (default), pingpong or hold the last frame
            frames = self._clip_frames(sset["clip"], sset.get("delogo"))
            n, i = len(frames), int(max(lt, 0) * FPS * sset.get("speed", 1.0))
            mode = sset.get("loop", "pingpong")
            if mode == "hold":
                i = min(i, n - 1)
            elif mode == "loop" or n < 2:
                i %= n
            else:
                i %= 2 * (n - 1)
                i = i if i < n else 2 * (n - 1) - i
            path = str(frames[i])
        else:
            path = sset["image"]
        if path not in self.images:
            if len(self.images) > 90:                 # frames of clips: keep memory small
                for k in [k for k in self.images if k.endswith(".jpg") and "/.clips/" in k][:60]:
                    del self.images[k]
            self.images[path] = skia.Image.open(path if path.startswith("/") else str(self.path.parent / path))
        return self.images[path]

    def camera(self, shot, lt):
        def value(k):
            if "z" in k:           # {"z": 1.1, "fx": 0.5, "fy": 0.45}: zoom on the whole picture, centre as a fraction
                bg = self._bg(shot)
                return (bg.width() * k.get("fx", 0.5), bg.height() * k.get("fy", 0.5),
                        min(bg.height(), bg.width() * self.H / self.W) / k["z"])
            if "follow" in k:
                st = self._state(shot, k["follow"], lt) or dict(pos=shot.tracks[k["follow"]][0]["p0"])
                return st["pos"][0] + k.get("dx", 0), st["pos"][1] + k.get("dy", 0), k["zoom"]
            v = k["view"] if isinstance(k["view"], list) else self.sets[shot.spec["set"]]["views"][k["view"]]
            return v[0], v[1], k.get("zoom") or v[2]
        keys = shot.cam
        if lt <= keys[0]["t"] or len(keys) == 1:
            return value(keys[0])
        for a, b in zip(keys, keys[1:]):
            if a["t"] <= lt < b["t"]:
                k = EASES[b.get("ease", "smooth")]((lt - a["t"]) / max(b["t"] - a["t"], 1e-6))
                return tuple(lerp(x, y, k) for x, y in zip(value(a), value(b)))
        return value(keys[-1])

    def frame(self, canvas, t):
        W, H, L = self.W, self.H, self.L
        shot = max((s for s in self.shots if t >= s.start), key=lambda s: s.start)
        if shot.spec.get("type") == "card":
            stage.card(canvas, W, H, shot.spec["header"], shot.spec.get("rows", []), shot.spec.get("takeaway", ""), t - shot.start)
            fade = min(clamp(t / 0.25), clamp((self.total - t) / 0.45))
            if fade < 1:
                canvas.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Color=skia.Color(0, 0, 0, int(255 * (1 - fade)))))
            return
        lt, st_set = t - shot.start, self.sets[shot.spec["set"]]
        bg = self._bg(shot, lt)
        bump = self._bump(shot, lt)

        cx, cy, vh = self.camera(shot, lt)
        vh *= 1 - 0.07 * bump
        vw = vh * W / H
        cx = clamp(cx, vw / 2, bg.width() * st_set.get("crop", 0.955) - vw / 2)
        cy = clamp(cy, vh / 2, bg.height() - vh / 2)
        sx, sy = stage.shake_offset(lt, shot.hits, 30)
        for e in shot.events:                                    # steady rumble
            if e["fx"] == "shake" and e["t"] <= lt < e["end"]:
                a = e.get("amp", 9) * min(1.0, (lt - e["t"]) / 0.2, (e["end"] - lt) / 0.3)
                sx += a * math.sin(lt * 53)
                sy += a * math.cos(lt * 41)
        canvas.save()
        canvas.translate(W / 2 + sx, H / 2 + sy)
        canvas.scale(H / vh, H / vh)
        canvas.translate(-cx, -cy)
        canvas.drawImage(bg, 0, 0, skia.SamplingOptions(skia.CubicResampler.Mitchell()))

        for gx, gy, gr, hz in st_set.get("glows", []):
            level = (0.5 + 0.5 * math.tanh(4 * math.sin(t * hz * 6.283))) if hz else 0.4 + 0.08 * math.sin(t * 9)
            sh = skia.GradientShader.MakeRadial((gx, gy), gr, [skia.Color(255, 150, 40, int(170 * level)), skia.Color(255, 150, 40, 0)])
            canvas.drawCircle(gx, gy, gr, skia.Paint(Shader=sh, BlendMode=skia.BlendMode.kPlus))

        dark = 0.0
        for e in shot.events:
            d = lt - e["t"]
            if d < 0:
                continue
            if e["fx"] == "smoke":
                stage.smoke(canvas, e["xy"][0], e["xy"][1], t, strength=smooth(d / 0.6), tone=tuple(e.get("tone", (70, 72, 80))))
            elif e["fx"] == "dark":
                dark = e.get("level", 150) * smooth(d / 0.8)

        states = [(a, self._state(shot, a, lt)) for a in shot.tracks]
        for actor, s in sorted([x for x in states if x[1]], key=lambda x: x[1]["pos"][1]):
            (x, y), step = s["pos"], s["step"]
            scale = step.get("scale", 1.0)
            if actor == "dog":
                h = st_set.get("dog_h", 135) * scale
                if s["moving"] or s["action"] == "play":
                    px = x + (110 * math.sin(s["since"] * 3.2) if s["action"] == "play" else 0)
                    face = s["facing"] if s["moving"] else (1 if math.cos(s["since"] * 3.2) > 0 else -1)
                    puppet.draw_dog(canvas, "run", px, y - 24 * abs(math.sin(t * 13)), h, facing=face, rot=5 * face * math.sin(t * 13))
                elif s["action"] == "dig":
                    puppet.draw_dog(canvas, "run", x, y, h, facing=s["facing"], rot=8 * math.sin(t * 14),
                                    squash=1 + 0.05 * math.sin(t * 28))
                else:
                    tilt = step.get("tilt", 0) * smooth(s["since"] / 0.25)
                    puppet.draw_dog(canvas, "sit", x, y - 46 * bump, h, facing=s["facing"], rot=tilt,
                                    squash=1 + 0.1 * bump + 0.02 * math.sin(t * 4))
            else:
                h = st_set.get("hero_h", 400) * scale
                if step.get("as") == "snowman":
                    d = s["since"]
                    puppet.draw_snowman(canvas, x, y, h * 0.95, squash=1 + 0.35 * math.exp(-d * 9) * math.cos(d * 28))
                    continue
                pose = puppet.ACTIONS[s["action"]](t, False)
                if s["prev"] != s["action"]:
                    pose = rig.blend(puppet.ACTIONS[s["prev"]](t, False), pose, clamp(s["since"] / 0.15))
                if "mood" in step:
                    pose["mood"] = step["mood"]
                pose["dy"] = pose["dy"] + 0.09 * bump
                mouth = (0.5 + 0.5 * math.sin(t * 17)) if step.get("mouth") == "talk" else 0.0
                puppet.draw_hero(canvas, pose, x, y, h, facing=s["facing"], t=t, squash=1 + 0.1 * bump,
                                 mouth=mouth, sweat=step.get("sweat", False))

        for e in shot.events:      # world-space particles in front of the actors
            if e["fx"] == "sparkle":
                x, y = e["xy"] if "xy" in e else self._state(shot, e.get("actor", "hero"), lt)["pos"]
                stage.burst(canvas, x, y - (0 if "xy" in e else st_set.get("hero_h", 400) * 0.6), e["t"], lt, n=16, seed=4,
                            color=skia.Color(255, 226, 140), speed=330, size=9, gravity=260, life=0.8)
            elif e["fx"] == "chunks":
                n = 0
                while e["t"] + n * e.get("every", 0.28) < min(e["end"], lt):
                    stage.burst(canvas, e["xy"][0], e["xy"][1], e["t"] + n * e.get("every", 0.28), lt, n=7, seed=n,
                                speed=260, size=7, gravity=700, life=0.55)
                    n += 1
        canvas.restore()

        # ---- screen space ----
        if dark:
            canvas.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Color=skia.Color(4, 6, 14, int(dark))))
        windy = [e for e in shot.events if e["fx"] == "wind_lines" and e["t"] <= lt]
        for e in windy:
            stage.wind_lines(canvas, t, W, H, strength=clamp((lt - e["t"]) / 0.3) * clamp((e["end"] - lt) / 0.4 + 0.35))
        amount = shot.spec.get("snow", st_set.get("snow", 0))
        if amount:
            self.snow.draw(canvas, t, amount, wind=1.6 if windy else st_set.get("wind", 0.5))
        for e in shot.events:
            if e["fx"] == "dust" and e["t"] <= lt < e["end"]:
                stage.dust(canvas, t, W, H, e.get("amount", 1.0))
        for e in shot.events:
            if e["fx"] == "diagram" and e["t"] <= lt < e["end"]:
                stage.diagram(canvas, W, H, e, lt - e["t"], e["end"] - e["t"])
        vig = skia.GradientShader.MakeRadial((W / 2, H / 2), max(W, H) * 0.62, [skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 150)],
                                             [0.55, 1.0])
        canvas.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=vig))

        impacts = sorted([e for e in shot.events if e["fx"] == "impact"], key=lambda e: e["t"])
        for a, b in zip(impacts, impacts[1:] + [None]):
            size = L["impact_size"] * min(1.0, 7.5 / max(len(a["text"]), 1) + 0.25)
            stage.impact_word(canvas, a["text"], a["t"], lt, W, L["impact_y"], size=size,
                              hold=(b["t"] if b else shot.dur) - a["t"])
        for e in shot.events:
            if e["fx"] == "verdict" and e["t"] <= lt:
                px, py = e.get("pos", [0.8, 0.28])
                stage.verdict(canvas, e.get("kind", "cross"), e["t"], lt, W * px, H * py, e.get("size", 300))
        for n, e in enumerate([e for e in shot.events if e["fx"] == "sticker"]):
            stage.sticker(canvas, e["text"], e["t"], lt, W / 2, L["sticker_y"] + n * L["sticker_dy"])
        if not impacts and self.ep.get("captions", True):
            stage.captions(canvas, self.all_words, t, W, L["cap_y"], L["cap_size"])
        fade = min(clamp(t / 0.25), clamp((self.total - t) / 0.45))
        if fade < 1:
            canvas.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Color=skia.Color(0, 0, 0, int(255 * (1 - fade)))))

    # ---------- sound ----------
    def soundtrack(self):
        n = int(self.total * SR)
        tt = np.arange(n) / SR
        narr, fx, duck, seed = np.zeros(n), np.zeros(n), np.ones(n), 0
        for wav, s in self.clips:
            clip = stage.load_wav(wav)
            act = clip[np.abs(clip) > 0.02]
            if len(act):                                          # even loudness from line to line
                clip = clip * float(np.clip(0.1 / (np.sqrt((act ** 2).mean()) + 1e-9), 0.5, 2.5))
            stage.place(narr, clip, s)
        narr *= 0.9 / (np.abs(narr).max() + 1e-9)
        for shot in self.shots:
            if shot.spec.get("type") == "card":
                stage.place(fx, stage.sfx("thud"), shot.start + 0.05, 0.6)
            for key in shot.cam:
                if key.get("ease") == "snap":
                    prev_t = max([k["t"] for k in shot.cam if k["t"] < key["t"]] + [0.0])
                    stage.place(fx, stage.sfx("whoosh", seed), shot.start + prev_t, 0.9)
            for actor, track in shot.tracks.items():
                lt = 0.0
                while lt < shot.dur:           # footsteps and digging from what the actor is doing
                    s = self._state(shot, actor, lt)
                    step = 0.12
                    if s and actor == "hero" and s["step"].get("as") is None:
                        if s["moving"]:
                            stage.place(fx, stage.sfx("crunch", seed), shot.start + lt, 0.6)
                            step = 0.24
                        elif s["action"] == "dig":
                            stage.place(fx, stage.sfx("crunch", seed), shot.start + lt, 0.8)
                            step = 0.14
                    seed += 1
                    lt += step
                for s in track:
                    if s.get("as"):
                        stage.place(fx, stage.sfx("pop"), shot.start + s["t0"], 1.0)
            for e in shot.events:
                at = shot.start + e["t"]
                if e["fx"] in ("hit", "impact"):
                    stage.place(fx, stage.sfx("thud"), at, 1.0)
                elif e["fx"] == "sticker":
                    stage.place(fx, stage.sfx("pop"), at, 0.9)
                elif e["fx"] == "sparkle":
                    stage.place(fx, stage.sfx("ding"), at + 0.03, 1.0)
                elif e["fx"] == "wind_lines":
                    stage.place(fx, stage.sfx("whoosh", 7), at, 0.7)
                elif e["fx"] == "dark":
                    stage.place(fx, stage.sfx("rumble"), at, 0.9)
                    duck[int(at * SR):int((shot.start + shot.dur) * SR)] = 0.25
                elif e["fx"] == "sfx":
                    stage.place(fx, stage.sfx(e["name"]), at, e.get("gain", 0.9))
                elif e["fx"] == "shake":
                    stage.place(fx, stage.sfx("rumble"), at, 0.8)
        k = int(0.25 * SR)
        duck = np.convolve(duck, np.ones(k) / k, mode="same")
        track_file = next(iter(sorted((Path(__file__).parent / "assets").glob("music.*"))), None)
        if track_file:
            raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-stream_loop", "-1", "-i", str(track_file), "-t", str(self.total),
                                  "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True, check=True).stdout
            mus = np.frombuffer(raw, dtype=np.int16).astype(np.float64)[:n] / 32768
            mus = np.pad(mus, (0, n - len(mus))) * 0.08
        else:
            mus = stage.music(n) * 0.09
        wind = stage.wind_bed(n) * 0.6 if any(s.get("snow") for s in self.sets.values()) else 0
        # everything except the voice gets quieter whenever the narrator is speaking
        w = int(0.03 * SR)
        e = np.clip(np.convolve(np.abs(narr), np.ones(w) / w, mode="same") / 0.06, 0, 1)
        r = int(0.3 * SR)
        e = np.maximum(e, np.convolve(e, np.ones(r) / r, mode="same"))
        voice_duck = 1 - 0.85 * e
        mix = narr + (fx * 0.38 + wind + mus * duck) * voice_duck
        return mix * np.minimum(1, np.minimum(tt / 0.2, (self.total - tt) / 0.5))


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    try:
        d = Director(args[0], synth="--check" not in args)
    except Problem as e:
        sys.exit(f"Episode problem: {e}")
    if "--check" in args:
        print(f"OK: {len(d.shots)} shots, about {d.total:.0f}s (estimated without narration)")
        return
    out = d.path.parent / "out"
    out.mkdir(exist_ok=True)
    buf = np.zeros((d.H, d.W, 4), np.uint8)
    surface = skia.Surface(buf)
    canvas = surface.getCanvas()
    if "--frames" in args:
        for s in args[args.index("--frames") + 1].split(","):
            d.frame(canvas, float(s))
            surface.makeImageSnapshot().save(str(out / f"frame_{float(s):05.2f}.png"), skia.kPNG)
        print("shot starts:", [round(s.start, 2) for s in d.shots], "total", round(d.total, 2))
        return
    wav, mp4 = out / f"{d.path.stem}.wav", out / f"{d.path.stem}.mp4"
    stage.save_wav(wav, d.soundtrack())
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{d.W}x{d.H}",
                           "-r", str(FPS), "-i", "-", "-i", str(wav), "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                           "-pix_fmt", "yuv420p", "-af", "highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=10:release=180:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=9", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(mp4)],
                          stdin=subprocess.PIPE)
    for f in range(int(d.total * FPS)):
        d.frame(canvas, f / FPS)
        ff.stdin.write(buf.tobytes())
    ff.stdin.close()
    if ff.wait():
        sys.exit("ffmpeg failed")
    wav.unlink()
    print(f"{mp4}  {d.total:.1f}s")


if __name__ == "__main__":
    main()
