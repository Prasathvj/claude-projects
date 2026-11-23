"""PAPERCUT KIT (owner chose papercut as the main look, 2026-11-23).
A style layer over the existing long-video scene types: every card, bubble, tile and chip becomes cut paper (paper grain,
torn edges, layered drop shadows), motion turns into stop-motion steps, the background becomes textured paper with grain,
captions sit on torn orange paper strips, and a torn kraft sheet wipes in at each new chapter. Max and Bit get the same
paper treatment (paper_max_layer / paper_max_render patch the Max overlay: texture, cut-out shadow, 10 fps stepping).
Enable with STYLE=paper (theme.apply calls paperize after the colour theme). Works with THEME=cream."""
import hashlib, os, re

ON = lambda: os.environ.get('STYLE') == 'paper'
FPS_STEP = 12          # stop-motion cadence for short tweens

DEFS = """<svg width="0" height="0" style="position:absolute"><defs>
<filter id="kp-tex" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" seed="9" result="n"/>
 <feColorMatrix in="n" type="matrix" values="0 0 0 0 .35  0 0 0 0 .24  0 0 0 0 .14  0 0 0 .32 0" result="g"/>
 <feComposite in="g" in2="SourceGraphic" operator="in" result="t"/><feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="t"/></feMerge></filter>
</defs></svg>"""

def torn(seed, n=14, amp=2.4):
    """a deterministic torn-paper polygon (percent coordinates) for clip-path"""
    h = hashlib.md5(seed.encode()).digest()
    r = lambda k: (h[k % 16] / 255.0) * amp
    pts = []
    for k in range(n + 1):
        pts.append(f'{k * 100 / n:.1f}% {r(k):.1f}%')
    for k in range(n + 1):
        pts.append(f'{100 - r(k + 3):.1f}% {k * 100 / n:.1f}%')
    for k in range(n, -1, -1):
        pts.append(f'{k * 100 / n:.1f}% {100 - r(k + 7):.1f}%')
    for k in range(n, -1, -1):
        pts.append(f'{r(k + 11):.1f}% {k * 100 / n:.1f}%')
    return 'polygon(' + ', '.join(pts) + ')'

CARDS = ['.card', '.sp', '.ib', '.cr', '.det', '.rr', '.fn', '.ft', '.rg', '.tw', '.pc', '.sk', '.duo', '.m', '.msg', '.ct6', '.vid9',
         '.co', '.st5', '.np', '.lp', '.nd', '.tl', '.nt', '.nt3', '.stat2', '.po', '.pf', '.lt', '.rcpt', '.vcard', '.shop', '.tg', '.note', '.qcard', '.qclip']
SMALL = ['.tile', '.chip', '.chip2', '.it', '.cf', '.sub', '.ok', '.bad', '.tag2', '.vc7', '.gc7']

def paper_css():
    rules = [f'{c} {{ filter:url(#kp-tex); clip-path:{torn(c)}; border:0 !important; box-shadow:none !important; }}' for c in CARDS]
    rules += [f'{c} {{ clip-path:{torn(c, 6, 4)}; box-shadow:none !important; }}' for c in SMALL]
    return '\n'.join(rules) + """
.stage, .all { filter:drop-shadow(0 9px 0 rgba(74,50,28,.24)) drop-shadow(0 20px 16px rgba(74,50,28,.26)); }
.big, .num, .val2, .qt { text-shadow:3px 5px 0 rgba(74,59,51,.85), 6px 10px 0 rgba(90,55,25,.18); }
.big .acc, .acc { text-shadow:3px 5px 0 #8A3A12, 6px 10px 0 rgba(90,55,25,.18); }
.kp-sheet { position:absolute; left:-120px; top:-140px; width:2200px; height:1300px; background:#C9A57A; filter:url(#kp-tex); z-index:50; }"""

def stepped(script):
    """short tweens snap through poses like stop-motion (long drifts and loops keep their smooth ease)"""
    out = []
    for line in script.split('\n'):
        m = re.search(r'duration:\s*([\d.]+)', line)
        if m and 'ease:' in line and float(m.group(1)) <= 1.2 and 'innerText' not in line:
            n = max(2, round(float(m.group(1)) * FPS_STEP))
            line = re.sub(r'ease:"[^"]*"', f'ease:"steps({n})"', line)
        elif m and 'ease:' not in line and float(m.group(1)) <= 1.2 and ('fromTo' in line or 'tl.to' in line) and 'innerText' not in line:
            n = max(2, round(float(m.group(1)) * FPS_STEP))
            line = re.sub(r'duration:\s*([\d.]+)', lambda x: f'duration:{x.group(1)}, ease:"steps({n})"', line, 1)
        out.append(line)
    return '\n'.join(out)

BG_CSS = """
#root { background:#E6D3B6 !important; }
.grid, .vig { display:none; }
.kp-base { position:absolute; inset:0; background:radial-gradient(ellipse at 40% 35%, #F3E6D2 0%, #E6D3B6 55%, #D2B690 100%); filter:url(#kp-tex); }
.kp-scrap { position:absolute; filter:url(#kp-tex) drop-shadow(0 6px 0 rgba(90,55,25,.12)); }
.kp-grain { position:absolute; inset:-60px; background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='f'><feTurbulence type='fractalNoise' baseFrequency='1.05' numOctaves='2'/></filter><rect width='180' height='180' filter='url(%23f)' opacity='.6'/></svg>"); opacity:.12; mix-blend-mode:multiply; }
.glow { opacity:.45; } .plus, .sq { display:none; }"""

CAP_CSS = """
.bx { clip-path:%s; border-radius:0 !important; }
.w em { text-shadow:none; }""" % torn('.bx', 5, 6)

def paperize(html):
    if not ON():
        return html
    m = re.search(r'data-composition-id="([^"]+)"', html)
    cid = m.group(1) if m else ''
    html = re.sub(r'(<div id="root"[^>]*>)', r'\1\n' + DEFS.replace('\\', '\\\\'), html, 1)
    extra = paper_css()
    if cid == 'bg':
        extra = BG_CSS
        scraps = (f'<div class="kp-base"></div>'
                  f'<div class="kp-scrap" style="left:-60px; top:780px; width:520px; height:380px; background:#F3E3CC; clip-path:{torn("s1", 8, 6)}; transform:rotate(-8deg)"></div>'
                  f'<div class="kp-scrap" style="left:1500px; top:-90px; width:520px; height:330px; background:#F6D5B8; clip-path:{torn("s2", 8, 6)}; transform:rotate(7deg)"></div>'
                  f'<div class="kp-scrap" style="left:1620px; top:840px; width:360px; height:300px; background:#E8CBA4; clip-path:{torn("s3", 8, 6)}; transform:rotate(-5deg)"></div>'
                  f'<div class="kp-grain" id="kp-grain"></div>')
        html = re.sub(r'(<div id="root"[^>]*>\n(?:<svg[^\n]*\n(?:[^\n]*\n)*?</defs></svg>\n)?)', lambda x: x.group(1) + scraps + '\n', html, 1)
        html = html.replace('window.__timelines["bg"] = tl;',
                            'tl.fromTo("#kp-grain", { x:0, y:0 }, { x:-50, y:30, duration:9999, ease:"steps(119988)" }, 0);\n    window.__timelines["bg"] = tl;')
    elif cid.startswith('caps'):
        extra = CAP_CSS
    html = html.replace('</style>', extra + '\n</style>', 1)
    html = re.sub(r'(const tl = gsap\.timeline\(\{ paused: true \}\);\n)(.*?)(\n\s*window\.__timelines)',
                  lambda x: x.group(1) + stepped(x.group(2)) + x.group(3), html, 1, re.S)
    return html

def sheet_wipe(sid):
    """torn kraft sheet that covers the stage at the start of a chapter and tears away (stop-motion)"""
    body = f'<div class="kp-sheet" id="{sid}-sheet" style="clip-path:{torn(sid + "sheet", 16, 3)}"></div>'
    sc = f'    tl.fromTo("#{sid}-sheet", {{ x:0, rotation:0 }}, {{ x:2300, y:-160, rotation:9, duration:.55, ease:"steps(7)" }}, 0.02);'
    return body, sc

PAPER_MAX_CSS = """#m svg { filter:url(#kp-tex) drop-shadow(0 6px 0 rgba(90,55,25,.20)) drop-shadow(0 16px 12px rgba(90,55,25,.25)); }"""

def paper_max_layer(path):
    """patch a project's max_layer.html: paper texture + cut-out shadow on Max"""
    s = open(path).read()
    if 'kp-tex' in s:
        return
    s = s.replace('</style>', PAPER_MAX_CSS + '\n</style>', 1).replace('<body>', '<body>' + DEFS, 1)
    open(path, 'w').write(s)

def paper_max_render(path, hold=3):
    """patch max_render.cjs so Max moves on 'threes' (10 fps at 30 fps), like stop-motion"""
    s = open(path).read()
    s = s.replace('await p.evaluate((i) => frame(i), i);', f'await p.evaluate((i) => frame(i), Math.floor(i / {hold}) * {hold});')
    open(path, 'w').write(s)
