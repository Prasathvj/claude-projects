"""Picture scenes for long videos: show what the narration says with real illustrations (tools/pics.py, Fluent Emoji, MIT)
instead of text cards. Import after the long-video engine (it registers the 'pic' scene type into B.T).

Beat spec  {"type": "pic", ...}   canvas 1320×720, x/y = top-left in px, times 'at' = fraction of the narration line
  items : [{"p": "man-technologist", "x": 100, "y": 200, "s": 260, "in": "pop|fly|drop|fade|grow|rise|slide", "at": 0.1,
            "loop": "float|bob|spin|pulse|shake|wiggle", "style": "flat|3d", "flip": true, "label": "You", "id": "me"}]
  tags  : [{"text": "75%", "x": 900, "y": 80, "at": 0.4, "kind": "note|ok|bad|big|bubble", "size": 44}]
  arrows: [{"from": [x, y], "to": [x, y], "at": 0.3, "dash": true}]
  moves : [{"id": "me", "to": [x, y], "at": 0.5, "d": 0.8, "scale": 1, "rot": 0, "fade": false}]
  title : optional small kicker at the top
"""
import math
import pics

def register(B):
    E, wf = B.E, B.wfrac

    def t_pic(i, sid, v):
        body, sc, css = [], [], [""".pi { position:absolute; } .pi .pl { position:absolute; left:50%; top:100%; transform:translateX(-50%); margin-top:6px; white-space:nowrap;
  font:800 30px 'SD Display'; color:var(--ink); background:#FFFFFF; padding:6px 18px; border-radius:16px; box-shadow:0 10px 24px rgba(90,50,20,.12); }
.tg { position:absolute; opacity:0; white-space:nowrap; }
.tg.note { padding:14px 26px; border-radius:18px; background:#FFFFFF; color:var(--ink); font:800 40px 'SD Display'; box-shadow:0 16px 40px rgba(90,50,20,.15); }
.tg.ok { padding:14px 26px; border-radius:18px; background:#3DDC97; color:#0E3B26; font:900 40px 'SD Display'; }
.tg.bad { padding:14px 26px; border-radius:18px; background:#FF3B30; color:#FFFFFF; font:900 40px 'SD Display'; }
.tg.big { font:900 120px 'SD Display'; color:var(--accent); letter-spacing:-2px; padding:4px 30px 10px; border-radius:28px; background:rgba(255,250,247,.88); box-shadow:0 20px 50px rgba(90,50,20,.18); }
.tg.quote { padding:22px 34px; border-radius:26px; background:rgba(255,250,247,.92); color:var(--ink); font:600 italic 64px 'SD Serif'; box-shadow:0 20px 50px rgba(90,50,20,.18); white-space:normal; max-width:1100px; line-height:1.1; }
.tg.bubble { padding:18px 28px; border-radius:30px 30px 30px 8px; background:#FFFFFF; color:var(--ink); font:700 34px 'SD Text'; box-shadow:0 16px 40px rgba(90,50,20,.15); white-space:normal; max-width:520px; }
.kk { position:absolute; left:0; right:0; top:24px; text-align:center; font:800 24px 'SD Mono'; letter-spacing:4px; color:var(--accent); }"""]
        if v.get('title'):
            body.append(f'<div class="kk">{E(v["title"])}</div>')
        ids = {}
        for k, it in enumerate(v.get('items', [])):
            pid = f'{sid}-i{k}'; ids[it.get('id', str(k))] = pid
            svg = pics.pic(it['p'], it.get('s', 220), it.get('style', 'flat'))
            flip = ' style="transform:scaleX(-1)"' if it.get('flip') else ''
            lab = f'<div class="pl">{E(it["label"])}</div>' if it.get('label') else ''
            body.append(f'<div class="pi" id="{pid}" style="left:{it["x"]}px; top:{it["y"]}px"><div id="{pid}-in"{flip}>{svg}</div>{lab}</div>')
            t = wf(i, it.get('at', 0.02 + k * 0.08)); how = it.get('in', 'pop')
            frm = {'pop': 'opacity:0, scale:.3', 'fly': 'opacity:0, x:-260, rotation:-12', 'drop': 'opacity:0, y:-320', 'fade': 'opacity:0',
                   'grow': 'opacity:0, scale:0', 'rise': 'opacity:0, y:220', 'slide': 'opacity:0, x:300'}[how]
            to = 'opacity:1, scale:1, x:0, y:0, rotation:0'
            ease = {'drop': 'bounce.out', 'fade': 'power1.out', 'grow': 'elastic.out(1,.6)'}.get(how, 'back.out(1.8)')
            sc.append(f'    tl.fromTo("#{pid}", {{ {frm} }}, {{ {to}, duration:{.7 if how in ("drop", "grow") else .45}, ease:"{ease}" }}, {t});')
            lp = it.get('loop')
            if lp:
                d = max(1.0, B.S[sid][1] - B.S[sid][0] - t - 0.5)
                loop = {'float': ('y:0', 'y:-16', 1.1), 'bob': ('rotation:-4', 'rotation:4', .6), 'spin': ('rotation:0', 'rotation:360', 2.0),
                        'pulse': ('scale:1', 'scale:1.08', .5), 'shake': ('x:-8', 'x:8', .07), 'wiggle': ('rotation:-8', 'rotation:8', .25)}[lp]
                rep = max(1, int(d / loop[2]) - 1)
                yoyo = 'false' if lp == 'spin' else 'true'
                sc.append(f'    tl.fromTo("#{pid}-in", {{ {loop[0]} }}, {{ {loop[1]}, duration:{loop[2]}, ease:"{"none" if lp == "spin" else "sine.inOut"}", yoyo:{yoyo}, repeat:{rep}, immediateRender:false }}, {round(t + 0.5, 3)});')
        for k, tg in enumerate(v.get('tags', [])):
            tid = f'{sid}-t{k}'; kind = tg.get('kind', 'note')
            fs = f' font-size:{tg["size"]}px;' if tg.get('size') else ''
            body.append(f'<div class="tg {kind}" id="{tid}" style="left:{tg["x"]}px; top:{tg["y"]}px;{fs}">{E(tg["text"])}</div>')
            sc.append(f'    tl.fromTo("#{tid}", {{ opacity:0, scale:{1.6 if kind == "big" else .5}, y:20 }}, {{ opacity:1, scale:1, y:0, duration:.35, ease:"back.out(2)" }}, {wf(i, tg.get("at", 0.4))});')
        for k, a in enumerate(v.get('arrows', [])):
            (x1, y1), (x2, y2) = a['from'], a['to']; L = round(math.hypot(x2 - x1, y2 - y1)); ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
            aid = f'{sid}-a{k}'
            line = 'repeating-linear-gradient(90deg,#F87736 0 18px,transparent 18px 30px)' if a.get('dash') else '#F87736'
            body.append(f'<div id="{aid}" style="position:absolute; left:{x1}px; top:{y1 - 4}px; width:{L}px; height:8px; border-radius:4px; background:{line}; transform-origin:0 50%; transform:rotate({ang:.1f}deg) scaleX(0)">'
                        f'<i style="position:absolute; right:-6px; top:-14px; border-left:30px solid #F87736; border-top:18px solid transparent; border-bottom:18px solid transparent"></i></div>')
            sc.append(f'    tl.to("#{aid}", {{ scaleX:1, duration:.45, ease:"power2.out" }}, {wf(i, a.get("at", 0.3))});')
        for m in v.get('moves', []):
            pid = ids[m['id']]; props = []
            if 'to' in m:
                it = next(x for x in v['items'] if x.get('id') == m['id'])
                props += [f'x:{m["to"][0] - it["x"]}', f'y:{m["to"][1] - it["y"]}']
            if 'scale' in m: props.append(f'scale:{m["scale"]}')
            if 'rot' in m: props.append(f'rotation:{m["rot"]}')
            if m.get('fade'): props.append('opacity:0')
            sc.append(f'    tl.to("#{pid}", {{ {", ".join(props)}, duration:{m.get("d", .7)}, ease:"{m.get("ease", "power2.inOut")}" }}, {wf(i, m["at"])});')
        return '\n'.join(body), sc, css[0]

    B.T['pic'] = t_pic
    B.SFX_BY_TYPE['pic'] = [(0.05, 'pop', .4), (0.6, 'whoosh', .3)]


def register_scenes(B):
    """'scene' beat: a full-frame AI illustration (assets/scenes/<img>.jpg) with a camera move plus the 'pic' overlays.
    spec {"type": "scene", "img": "library", "cam": [fx, fy, zoom], "from": [fx, fy, zoom] (optional), ...pic overlay keys}
    fx, fy = focus point as fractions of the picture; zoom 1 = whole picture. Consecutive beats on the same picture continue
    the camera from the previous beat's 'cam', so the move is one smooth shot; a new picture fades in from a slight push-in."""
    t_pic = B.T['pic']

    def t_scene(i, sid, v):
        prev = B.BE[i - 1]['v'] if i > 0 else {}
        cam = v.get('cam', [0.5, 0.5, 1.0])
        same = prev.get('type') == 'scene' and prev.get('img') == v['img']
        frm = v.get('from') or (prev.get('cam', [0.5, 0.5, 1.0]) if same else [cam[0], cam[1], max(1.0, cam[2] * 0.92)])
        def org(c): return f'{c[0] * 100:.1f}% {c[1] * 100:.1f}%'
        d = round(B.S[sid][1] - B.S[sid][0], 2)
        sl = 80 if i in B.HOST else B.CENTER_X   # the stage's left edge (beat_scene); the picture covers the whole frame
        img = (f'<div id="{sid}-img" style="position:absolute; left:-{sl}px; top:-110px; width:1920px; height:1080px; overflow:hidden">'
               f'<div id="{sid}-cam" style="position:absolute; inset:0; background:url(assets/scenes/{v["img"]}.jpg) center/cover; transform-origin:{org(frm)}; transform:scale({frm[2]})"></div>'
               f'<div style="position:absolute; left:0; right:0; bottom:0; height:300px; background:linear-gradient(180deg,rgba(244,237,227,0),rgba(244,237,227,.85))"></div></div>')
        body, sc, css = t_pic(i, sid, v)
        sc = [f'    tl.fromTo("#{sid}-cam", {{ scale:{frm[2]}, transformOrigin:"{org(frm)}" }}, {{ scale:{cam[2]}, transformOrigin:"{org(cam)}", duration:{d}, ease:"sine.inOut" }}, 0);']
        if not same:
            sc.append(f'    tl.fromTo("#{sid}-img", {{ opacity:0 }}, {{ opacity:1, duration:.35, ease:"power1.out" }}, 0);')
        sc += t_pic(i, sid, v)[1]
        return img + body, sc, css

    B.T['scene'] = t_scene
    B.SFX_BY_TYPE['scene'] = [(0.6, 'whoosh', .25)]
