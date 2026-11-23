"""PAPER PROPS (owner, 2026-11-23): cut-paper objects that act out the narration, like the first papercut sample.
Drawn in code from paper shapes (no pictures). Used through the 'paperscene' beat type (register with kit_props.register(B)),
best with STYLE=paper (tools/kit_paper.py adds paper grain, cut-paper shadows and stop-motion stepping).

Beat spec  {"type": "paperscene", ...}   stage 1320×760; x/y = top-left of the prop box; 'at' = fraction of the narration line
  props : [{"p": "laptop", "x": 100, "y": 200, "s": 1.0, "rot": -3, "in": "drop|fly|pop|slide|rise|fade", "at": .1,
            "loop": "boil|bob|spin|shake|float|wiggle", "id": "lap", "text": "for strip/label props", "c": "colour", "n": 24}]
  moves : [{"id": "lap", "x": 300, "y": 0, "rot": 0, "scale": 1, "fade": true, "at": .6, "d": .5}]   (x/y = offset to move by)
Props: bit, max-head, person, crowd, laptop, phone, monitor, server, chip, cloud, wifi, lock, doc, envelope, coin, money,
calendar, clock, magnifier, bulb, globe, wheel, strip, banner, arrow, belt, block, box, book, scissors, star, check, cross, gear
"""
P = {'o': '#F87736', 'd': '#4A3B33', 'c': '#FFF6E8', 't': '#C9B49C', 'p': '#FFD9B8', 'b': '#6EC8FF', 'g': '#3DDC97',
     'y': '#FFC24A', 'r': '#E0471C', 'k': '#2A2018', 'w': '#FFFFFF', 'l': '#E8D5BC'}

def sh(x, y, w, h, c, r='12px', extra=''):
    """one paper shape"""
    return f'<div class="ps" style="left:{x}px; top:{y}px; width:{w}px; height:{h}px; background:{P.get(c, c)}; border-radius:{r}; {extra}"></div>'

def txt(x, y, t, size=40, c='k', w=None, extra=''):
    ww = f'width:{w}px; text-align:center;' if w else ''
    return f'<div class="pt" style="left:{x}px; top:{y}px; {ww} font:900 {size}px \'SD Display\'; color:{P.get(c, c)}; {extra}">{t}</div>'

# ---------------------------------------------------------------- props: return (inner_html, width, height)
def bit(o):
    eyes = o.get('eyes', 'open')
    e = (sh(75, 70, 36, 44, 'b', '50%') + sh(150, 70, 36, 44, 'b', '50%')) if eyes == 'open' else \
        (sh(72, 88, 44, 12, 'b', '6px') + sh(148, 88, 44, 12, 'b', '6px')) if eyes == 'happy' else \
        (sh(78, 78, 30, 30, 'r', '4px', 'transform:rotate(45deg)') + sh(152, 78, 30, 30, 'r', '4px', 'transform:rotate(45deg)'))
    return (sh(120, -40, 18, 50, 't', '6px') + sh(106, -62, 46, 46, 'o', '50%') + sh(0, 0, 260, 180, 'c', '60px') + sh(36, 36, 188, 108, 'k', '40px') + e
            + sh(38, 180, 184, 118, 'o', '40px 40px 60px 60px') + sh(80, 215, 100, 46, 'k', '14px') + sh(96, 228, 20, 20, 'b', '50%') + sh(142, 228, 20, 20, 'o', '50%'),
            260, 300)

def person(o):
    c = o.get('c', 'o')
    return sh(14, 0, 36, 36, c, '50%') + sh(0, 40, 64, 60, c, '30px 30px 8px 8px'), 64, 100

def crowd(o):
    n, cols = o.get('n', 24), o.get('cols', 12)
    h = ''.join(f'<div class="cr-p" style="position:absolute; left:{(k % cols) * 74}px; top:{(k // cols) * 112}px">{person({"c": "odt"[k % 3]})[0]}</div>' for k in range(n))
    return h, cols * 74, ((n - 1) // cols + 1) * 112

def laptop(o):
    return (sh(40, 0, 560, 360, 'd', '22px') + sh(70, 28, 500, 304, o.get('screen', 'c'), '10px') + sh(0, 350, 640, 66, 't', '10px 10px 30px 30px')
            + sh(260, 360, 120, 14, 'l', '7px'), 640, 420)

def phone(o):
    return sh(0, 0, 220, 420, 'd', '36px') + sh(16, 30, 188, 350, o.get('screen', 'c'), '18px') + sh(80, 12, 60, 10, 'k', '5px'), 220, 420

def monitor(o):
    return sh(0, 0, 520, 330, 'd', '18px') + sh(22, 22, 476, 286, o.get('screen', 'c'), '8px') + sh(230, 330, 60, 70, 't', '0') + sh(150, 395, 220, 26, 't', '13px'), 520, 425

def server(o):
    h = sh(0, 0, 260, 420, 'd', '16px')
    for k in range(5):
        h += sh(20, 20 + k * 78, 220, 60, 'k', '8px') + sh(36, 42 + k * 78, 16, 16, 'g' if k % 2 else 'o', '50%') + sh(70, 44 + k * 78, 140, 12, 't', '6px')
    return h, 260, 420

def chip(o):
    h = ''.join(sh(40 + k * 44, -24, 16, 30, 't', '4px') + sh(40 + k * 44, 234, 16, 30, 't', '4px') + sh(-24, 40 + k * 44, 30, 16, 't', '4px') + sh(234, 40 + k * 44, 30, 16, 't', '4px') for k in range(5))
    return h + sh(0, 0, 260, 260, 'd', '22px') + sh(50, 50, 160, 160, 'o', '14px') + txt(50, 105, o.get('text', 'AI'), 52, 'c', 160), 260, 260

def cloud(o):
    c = o.get('c', 'c')
    return sh(0, 90, 360, 120, c, '60px') + sh(50, 30, 160, 160, c, '50%') + sh(160, 0, 180, 180, c, '50%'), 360, 210

def wifi(o):
    return ''.join(f'<div class="ps" style="left:{110 - r}px; top:{150 - r}px; width:{2 * r}px; height:{2 * r}px; border-radius:50%; border:22px solid {P["o"]}; border-bottom-color:transparent; border-left-color:transparent; transform:rotate(-45deg); background:transparent"></div>' for r in (40, 85, 130)) + sh(92, 140, 36, 36, 'o', '50%'), 220, 190

def lock(o):
    return (f'<div class="ps" style="left:40px; top:0; width:160px; height:170px; border-radius:80px 80px 0 0; border:28px solid {P["t"]}; border-bottom:0; background:transparent"></div>'
            + sh(0, 120, 240, 200, 'o', '26px') + sh(100, 180, 40, 70, 'k', '20px'), 240, 320)

def doc(o):
    h = sh(0, 0, 300, 380, 'c', '10px') + sh(220, 0, 80, 80, 'l', '0 10px 0 22px')
    for k in range(6):
        h += sh(36, 110 + k * 40, 228 - (k % 3) * 40, 16, 't', '8px')
    return h + txt(36, 30, o.get('text', ''), 36, 'k'), 300, 380

def envelope(o):
    return (sh(0, 0, 360, 240, 'c', '14px') + f'<div class="ps" style="left:0; top:0; width:360px; height:150px; background:{P["l"]}; clip-path:polygon(0 0,100% 0,50% 100%)"></div>'
            + sh(160, 100, 40, 40, 'r', '50%'), 360, 240)

def coin(o):
    return sh(0, 0, 160, 160, 'y', '50%') + sh(22, 22, 116, 116, '#F2A93B', '50%') + txt(0, 44, o.get('text', '₹'), 64, 'c', 160), 160, 160

def money(o):
    return sh(0, 0, 360, 180, 'g', '14px') + sh(18, 18, 324, 144, '#2BB57D', '10px') + sh(140, 50, 80, 80, 'g', '50%') + txt(140, 62, o.get('text', '₹'), 48, 'c', 80), 360, 180

def calendar(o):
    return (sh(0, 30, 300, 280, 'c', '18px') + sh(0, 30, 300, 80, 'o', '18px 18px 0 0') + sh(60, 0, 26, 70, 'd', '13px') + sh(214, 0, 26, 70, 'd', '13px')
            + txt(0, 140, o.get('text', '12'), 110, 'k', 300), 300, 310)

def clock(o):
    return sh(0, 0, 280, 280, 'c', '50%') + f'<div class="ps" style="left:0; top:0; width:280px; height:280px; border-radius:50%; border:16px solid {P["d"]}; background:transparent"></div>' \
        + sh(132, 50, 16, 100, 'k', '8px') + f'<div class="ps hand" style="left:132px; top:132px; width:16px; height:110px; background:{P["o"]}; border-radius:8px; transform-origin:8px 8px; transform:rotate(-120deg)"></div>' + sh(124, 124, 32, 32, 'k', '50%'), 280, 280

def magnifier(o):
    return (f'<div class="ps" style="left:0; top:0; width:200px; height:200px; border-radius:50%; border:26px solid {P["d"]}; background:rgba(110,200,255,.35)"></div>'
            + f'<div class="ps" style="left:170px; top:160px; width:40px; height:150px; background:{P["d"]}; border-radius:20px; transform:rotate(-45deg); transform-origin:top center"></div>', 300, 300)

def bulb(o):
    return sh(30, 0, 200, 200, 'y', '50%') + sh(80, 180, 100, 60, 't', '10px') + sh(90, 240, 80, 30, 'd', '0 0 20px 20px') + sh(95, 70, 70, 14, 'c', '7px'), 260, 270

def globe(o):
    return (sh(0, 0, 300, 300, 'b', '50%') + sh(40, 60, 110, 90, 'g', '50% 40% 60% 50%') + sh(160, 140, 100, 110, 'g', '40% 60% 50% 50%')
            + f'<div class="ps" style="left:0; top:0; width:300px; height:300px; border-radius:50%; border:10px solid {P["d"]}; background:transparent"></div>', 300, 300)

def wheel(o):
    segs = ''.join(f'<div class="ps" style="left:180px; top:158px; width:150px; height:44px; transform-origin:0 50%; transform:rotate({k * 45}deg) translateX(40px); '
                   f'background:{P["c"] if k % 2 else P["p"]}; border-radius:8px"></div>' for k in range(8))
    return sh(0, 0, 360, 360, 'o', '50%') + segs + sh(150, 150, 60, 60, 'k', '50%'), 360, 360

def strip(o):
    c = o.get('c', 'c'); fc = 'c' if c in ('o', 'd', 'r', 'k') else 'k'
    return (f'<div class="ps strip" style="position:relative; display:inline-block; padding:14px 30px; background:{P.get(c, c)}; clip-path:polygon(0 6%,4% 0,30% 4%,62% 0,100% 5%,97% 50%,100% 96%,66% 100%,33% 95%,3% 100%,0 60%)">'
            f'<span style="font:900 {o.get("size", 52)}px \'SD Display\'; color:{P[fc]}; white-space:nowrap">{o.get("text", "")}</span></div>', 0, 0)

def banner(o):
    return (f'<div class="ps strip" style="position:relative; display:inline-block; padding:18px 44px; background:{P["o"]}; clip-path:polygon(0 8%,10% 0,50% 6%,92% 0,100% 12%,98% 90%,88% 100%,40% 94%,6% 100%,1% 70%)">'
            f'<span style="font:900 {o.get("size", 66)}px \'SD Display\'; color:{P["c"]}; white-space:nowrap">{o.get("text", "")}</span></div>', 0, 0)

def arrow(o):
    L = o.get('len', 260)
    return sh(0, 26, L - 40, 28, o.get('c', 'd'), '14px') + f'<div class="ps" style="left:{L - 70}px; top:0; width:80px; height:80px; background:{P[o.get("c", "d")]}; clip-path:polygon(0 0,100% 50%,0 100%)"></div>', L, 80

def belt(o):
    L = o.get('len', 900)
    return sh(0, 0, L, 60, 'd', '30px') + ''.join(sh(20 + k * 90, 12, 36, 36, 't', '50%') for k in range(L // 90)), L, 60

def block(o):
    return sh(0, 0, o.get('w', 180), 90, o.get('c', 'o'), '14px') + txt(0, 20, o.get('text', ''), 40, 'c' if o.get('c', 'o') in ('o', 'd', 'r') else 'k', o.get('w', 180)), o.get('w', 180), 90

def box(o):
    return (sh(0, 120, 360, 240, '#C8955E', '10px') + sh(0, 120, 360, 30, '#B07E48', '10px 10px 0 0')
            + f'<div class="ps lid" style="left:-10px; top:80px; width:380px; height:60px; background:#D8A56C; border-radius:10px; transform-origin:0 100%"></div>', 360, 360)

def book(o):
    return sh(0, 0, 220, 300, o.get('c', 'o'), '10px 18px 18px 10px') + sh(0, 0, 30, 300, 'd', '10px 0 0 10px') + sh(60, 60, 120, 20, 'c', '10px'), 220, 300

def scissors(o):
    return (f'<div class="ps" style="left:0; top:0; width:110px; height:110px; border-radius:50%; border:24px solid {P["o"]}; background:transparent"></div>'
            + f'<div class="ps" style="left:0; top:130px; width:110px; height:110px; border-radius:50%; border:24px solid {P["o"]}; background:transparent"></div>'
            + f'<div class="ps blade1" style="left:96px; top:96px; width:240px; height:30px; background:#B8B8B8; border-radius:0 30px 30px 0; transform-origin:0 50%; transform:rotate(-12deg)"></div>'
            + f'<div class="ps blade2" style="left:96px; top:120px; width:240px; height:30px; background:#D0D0D0; border-radius:0 30px 30px 0; transform-origin:0 50%; transform:rotate(12deg)"></div>', 340, 240)

def star(o):
    return f'<div class="ps" style="left:0; top:0; width:120px; height:120px; background:{P[o.get("c", "y")]}; clip-path:polygon(50% 0,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%)"></div>', 120, 120

def check(o):
    return sh(0, 0, 160, 160, 'g', '50%') + f'<div class="ps" style="left:38px; top:40px; width:90px; height:50px; border-left:22px solid {P["c"]}; border-bottom:22px solid {P["c"]}; background:transparent; transform:rotate(-45deg)"></div>', 160, 160

def cross(o):
    return sh(0, 0, 160, 160, 'r', '50%') + sh(30, 68, 100, 24, 'c', '12px', 'transform:rotate(45deg)') + sh(30, 68, 100, 24, 'c', '12px', 'transform:rotate(-45deg)'), 160, 160

def gear(o):
    return ''.join(sh(105, -10, 50, 280, o.get('c', 'd'), '12px', f'transform:rotate({k * 45}deg)') for k in range(4)) + sh(20, 20, 220, 220, o.get('c', 'd'), '50%') + sh(90, 90, 80, 80, 'c', '50%'), 260, 260

PROPS = {k: v for k, v in globals().items() if callable(v) and k not in ('sh', 'txt', 'register', 'prop_html')}

CSS = """.pp { position:absolute; } .pp .ps, .pp .pt { position:absolute; } .pp .ps { filter:url(#kp-tex); }
.pp .strip { filter:url(#kp-tex); } .pp-mid { position:relative; } .pp-in { position:relative; transform-origin:50% 100%; }"""

def prop_html(sid, k, it):
    inner, w, h = PROPS[it['p']](it)
    pid = f'{sid}-q{k}'
    return pid, (f'<div class="pp" id="{pid}" style="left:{it["x"]}px; top:{it["y"]}px; width:{w * it.get("s", 1):.0f}px; height:{h * it.get("s", 1):.0f}px">'
                 f'<div class="pp-mid" id="{pid}-m"><div class="pp-in" style="width:{w}px; height:{h}px; scale:{it.get("s", 1)}; rotate:{it.get("rot", 0)}deg; transform-origin:0 0">{inner}</div></div></div>')

def register(B):
    wf = B.wfrac

    def t_paperscene(i, sid, v):
        body, sc, ids = [], [], {}
        d = B.S[sid][1] - B.S[sid][0]
        for k, it in enumerate(v.get('props', [])):
            pid, h = prop_html(sid, k, it); body.append(h); ids[it.get('id', str(k))] = pid
            t = wf(i, it.get('at', 0.02 + k * 0.06)); how = it.get('in', 'drop')
            frm = {'drop': 'y:-700, rotation:-10', 'fly': 'x:-1500, y:-200, rotation:-25', 'pop': 'scale:0, rotation:-12', 'slide': 'x:1500, rotation:12',
                   'rise': 'y:800, rotation:8', 'fade': 'opacity:0'}[how]
            sc.append(f'    tl.fromTo("#{pid}", {{ {frm}, opacity:{0 if how == "fade" else 1} }}, {{ x:0, y:0, scale:1, rotation:0, opacity:1, duration:{.35 if how != "fly" else .5}, ease:"back.out(1.6)" }}, {t});')
            if how != 'fade':
                sc.append(f'    tl.set("#{pid}", {{ opacity:0 }}, 0); tl.set("#{pid}", {{ opacity:1 }}, {t});')
            lp = it.get('loop')
            if lp:
                dur = max(0.6, d - t - 0.4)
                loop = {'boil': ('rotation:-1.5', 'rotation:1.5', .17), 'bob': ('y:0', 'y:-16', .35), 'spin': ('rotation:0', 'rotation:360', 2.4),
                        'shake': ('x:-8', 'x:8', .08), 'float': ('y:0', 'y:-12', .7), 'wiggle': ('rotation:-6', 'rotation:6', .3)}[lp]
                rep = max(1, int(dur / loop[2]) - 1)
                ease = f'steps({max(2, round(loop[2] * 12))})' if lp != 'spin' else f'steps({round(loop[2] * 12)})'
                sc.append(f'    tl.fromTo("#{pid}-m", {{ {loop[0]} }}, {{ {loop[1]}, duration:{loop[2]}, ease:"{ease}", yoyo:{"false" if lp == "spin" else "true"}, repeat:{rep}, immediateRender:false }}, {round(t + 0.4, 3)});')
        for m in v.get('moves', []):
            pid = ids[m['id']]; props = []
            for key, g in (('x', 'x'), ('y', 'y'), ('rot', 'rotation'), ('scale', 'scale')):
                if key in m: props.append(f'{g}:{m[key]}')
            if m.get('fade'): props.append('opacity:0')
            sc.append(f'    tl.to("#{pid}", {{ {", ".join(props)}, duration:{m.get("d", .45)}, ease:"power2.inOut" }}, {wf(i, m["at"])});')
        for k, it in enumerate(v.get('props', [])):
            if it['p'] == 'crowd':
                pid = f'{sid}-q{k}'
                sc.append(f'    tl.fromTo("#{pid} .cr-p", {{ opacity:0, y:-50 }}, {{ opacity:1, y:0, duration:.2, ease:"steps(3)", stagger:.045 }}, {wf(i, it.get("at", 0.05))});')
            if it['p'] == 'box' and it.get('open'):
                sc.append(f'    tl.to("#{sid}-q{k} .lid", {{ rotation:-110, duration:.4, ease:"back.out(2)" }}, {wf(i, it["open"])});')
            if it['p'] == 'scissors' and it.get('snip'):
                for j, a in enumerate(it['snip']):
                    sc.append(f'    tl.to("#{sid}-q{k} .blade1", {{ rotation:0, duration:.1, yoyo:true, repeat:1, ease:"steps(2)" }}, {wf(i, a)}); tl.to("#{sid}-q{k} .blade2", {{ rotation:0, duration:.1, yoyo:true, repeat:1, ease:"steps(2)" }}, {wf(i, a)});')
        return '\n'.join(body), sc, CSS

    B.T['paperscene'] = t_paperscene
    B.SFX_BY_TYPE['paperscene'] = [(0.05, 'whoosh', .4), (0.4, 'pop', .4), (1.0, 'flip', .35)]
