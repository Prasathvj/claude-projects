"""ep01 long video (16:9) in the TechDecoded HyperFrames style: one composition per beat, built from the
beat's "v" spec in episodes/ep01/long.json. Max (host) is composited on the right third afterwards; Bit acts
inside the scenes. Uses the real narration timeline when it matches the script, else a provisional one.
Usage: python3 tools/hf_ep01_long.py"""
import html, json, re, subprocess, sys, wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
P = ROOT / 'hf/ep01-long'
EP = json.loads((ROOT / 'episodes/ep01/long.json').read_text())
W, H = 1920, 1080
TAIL = 2.0

def timeline():
    real = ROOT / 'src/episodes/ep01-long.timeline.json'
    if real.exists():
        t = json.loads(real.read_text())
        if [b['text'] for b in t['beats']] == [b['text'] for b in EP['beats']]:
            return t, False
    import audio
    t, beats = 0.4, []
    for b in EP['beats']:
        d = round(len(b['text'].split()) / 2.55 + 0.25, 3)
        beats.append({**b, 'start': round(t, 3), 'vo': d, 'dur': round(d + 0.25, 3), 'words': audio.words_timing(b['text'], d)})
        t += d + 0.25
    return {'duration': round(t + 0.5, 3), 'beats': beats, 'vo': None}, True

TL, PROVISIONAL = timeline()
BE = TL['beats']
for b, e in zip(BE, EP['beats']):
    b['v'] = e['v']; b['chapter'] = e.get('chapter')
DUR = round(TL['duration'] + TAIL, 3)
WORDS = [(w['w'], round(b['start'] + w['s'], 3), round(b['start'] + w['e'], 3)) for b in BE for w in b['words']]
CUT = [0.0] + [round(b['start'] - 0.12, 3) for b in BE[1:]] + [DUR]
S = {f'b{i:02d}': (CUT[i], CUT[i + 1]) for i in range(len(BE))}
CHAPTERS = [(i, b['chapter']) for i, b in enumerate(BE) if b.get('chapter')]

def bword(i, word, nth=0):
    """local time of a word inside beat i (falls back to beat start)."""
    b = BE[i]
    hits = [w for w in b['words'] if re.sub(r'[^a-z0-9]', '', w['w'].lower()) == word]
    sid = f'b{i:02d}'
    return round(b['start'] + hits[min(nth, len(hits) - 1)]['s'] - S[sid][0], 3) if hits else round(b['start'] - S[sid][0], 3)

def wfrac(i, f):
    """local time at fraction f of beat i's narration."""
    b = BE[i]; sid = f'b{i:02d}'
    return round(b['start'] + b['vo'] * f - S[sid][0], 3)

FONTS = """
@font-face { font-family: 'SD Display'; src: url('assets/fonts/InterDisplay-Black.otf'); font-weight: 900; }
@font-face { font-family: 'SD Display'; src: url('assets/fonts/InterDisplay-Bold.otf'); font-weight: 700; }
@font-face { font-family: 'SD Text'; src: url('assets/fonts/Inter-SemiBold.otf'); font-weight: 600; }
@font-face { font-family: 'SD Text'; src: url('assets/fonts/Inter-Medium.otf'); font-weight: 500; }
@font-face { font-family: 'SD Serif'; src: url('assets/fonts/CormorantItalic-600.ttf'); font-weight: 600; font-style: italic; }
@font-face { font-family: 'SD Mono'; src: url('assets/fonts/JetBrainsMono-Bold.ttf'); font-weight: 700; }
"""
BASE_CSS = """
:root { --ground:#0C0704; --edge:#3E2217; --inner:#0E0806; --accent:#F87736; --accent-soft:#E98F5E; --dim:#9E745A; --ink:#F6EEE8;
        --mute:#5C4337; --red:#FF3B30; --green:#3DDC97; --blue:#55C2FF; }
#root { position:absolute; inset:0; overflow:hidden; }
.stage { position:absolute; left:80px; top:110px; width:1320px; height:760px; perspective:1800px; }
.card { position:absolute; border-radius:30px; border:2px solid var(--edge); background:linear-gradient(180deg,#2C1A13 0%,#1F120C 100%);
  box-shadow:0 36px 80px rgba(0,0,0,.6), inset 0 2px 0 rgba(255,190,150,.06); padding:26px; }
.hd { display:flex; align-items:center; gap:20px; margin-bottom:20px; }
.tile { width:80px; height:80px; border-radius:20px; background:#F3E6DC; display:flex; align-items:center; justify-content:center; flex:none; }
.lab { font:600 22px 'SD Text'; letter-spacing:2.5px; color:var(--accent); }
.ttl { font:700 38px 'SD Display'; color:var(--ink); white-space:nowrap; }
.inner { background:var(--inner); border-radius:22px; padding:24px 28px; position:relative; overflow:hidden; }
.tag { position:absolute; font:600 20px 'SD Text'; letter-spacing:2px; color:var(--dim); }
.kick { font:600 26px 'SD Text'; letter-spacing:6px; color:var(--dim); }
.big { font:900 120px 'SD Display'; color:var(--ink); line-height:1; letter-spacing:-2px; }
.acc { color:var(--accent); text-shadow:0 0 50px rgba(248,119,54,.5); }
.ring { position:absolute; width:260px; height:260px; margin:-130px 0 0 -130px; border-radius:50%; border:5px solid var(--accent);
  box-shadow:0 0 40px rgba(248,119,54,.6); opacity:0; }
.bit { position:absolute; } .bit > div { position:absolute; left:0; top:0; opacity:0; }
.center { position:absolute; left:0; right:0; text-align:center; }
"""

def scene(sid, body, script, css=''):
    return f"""<template>
  <style>
{FONTS}{BASE_CSS}
{css}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="{W}" data-height="{H}">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{script}
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""

E = html.escape
def fly(sel, t=0.05, rx=18, ry=-12):
    return f'    tl.fromTo("{sel}", {{ opacity:0, scale:.78, rotationX:{rx}, rotationY:{ry}, y:90, filter:"blur(14px)" }}, {{ opacity:1, scale:1, rotationX:0, rotationY:0, y:0, filter:"blur(0px)", duration:.6, ease:"expo.out" }}, {t});'
def pop(sel, t, dy=24):
    return f'    tl.fromTo("{sel}", {{ opacity:0, scale:.7, y:{dy} }}, {{ opacity:1, scale:1, y:0, duration:.32, ease:"back.out(2)" }}, {t});'
def fade(sel, t, dx=-60):
    return f'    tl.fromTo("{sel}", {{ opacity:0, x:{dx} }}, {{ opacity:1, x:0, duration:.35, ease:"expo.out" }}, {t});'
def ring(sel, t):
    return f'    tl.fromTo("{sel}", {{ opacity:1, scale:.15 }}, {{ opacity:0, scale:2.4, duration:.7, ease:"expo.out", immediateRender:false }}, {t});'
def shake(sel, t):
    return f'    tl.fromTo("{sel}", {{ x:0 }}, {{ x:10, duration:.05, yoyo:true, repeat:5, ease:"none", immediateRender:false }}, {t});'
def out(sid):
    d = round(S[sid][1] - S[sid][0], 3)
    return f'    tl.to("#{sid}-all", {{ opacity:0, filter:"blur(10px)", scale:1.03, duration:.14, ease:"power3.in" }}, {round(d - 0.15, 3)});'

# ------------------------------------------------------------------ icons
def icon(name, size=56, col='#F87736'):
    s = f'width="{size}" height="{size}" viewBox="0 0 100 100" fill="none" stroke="{col}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"'
    P_ = {
        'user': '<circle cx="50" cy="34" r="16"/><path d="M18 88c4-20 18-30 32-30s28 10 32 30"/>',
        'brain': '<path d="M38 18a14 14 0 0 0-14 14 14 14 0 0 0-8 26 14 14 0 0 0 14 22h20V18zM62 18a14 14 0 0 1 14 14 14 14 0 0 1 8 26 14 14 0 0 1-14 22H50"/>',
        'doc': '<path d="M26 10h34l18 18v62H26z"/><path d="M60 10v18h18M38 50h28M38 66h28"/>',
        'globe': '<circle cx="50" cy="50" r="36"/><ellipse cx="50" cy="50" rx="16" ry="36"/><path d="M15 38h70M15 62h70"/>',
        'skull': '<path d="M50 12c-20 0-34 14-34 32 0 12 6 20 14 24v14h40V68c8-4 14-12 14-24 0-18-14-32-34-32z"/><circle cx="38" cy="46" r="6"/><circle cx="62" cy="46" r="6"/><path d="M44 82v-8M56 82v-8"/>',
        'code': '<path d="M34 28L12 50l22 22M66 28l22 22-22 22M56 18L44 82"/>',
        'chat': '<path d="M14 18h72a8 8 0 0 1 8 8v40a8 8 0 0 1-8 8H44L26 90V74H14a8 8 0 0 1-8-8V26a8 8 0 0 1 8-8z"/>',
        'send': '<path d="M12 50L88 14 70 88 48 58z"/><path d="M48 58L88 14"/>',
        'shield': '<path d="M50 10l34 12v26c0 22-15 36-34 42-19-6-34-20-34-42V22z"/><path d="M36 50l10 10 20-22"/>',
        'warn': '<path d="M50 12L90 84H10z"/><path d="M50 40v20M50 72v1"/>',
        'server': '<rect x="14" y="14" width="72" height="30" rx="6"/><rect x="14" y="56" width="72" height="30" rx="6"/><path d="M28 29h1M28 71h1"/>',
        'mail': '<rect x="12" y="24" width="76" height="54" rx="8"/><path d="M14 28l36 28 36-28"/>',
        'lock': '<rect x="20" y="44" width="60" height="44" rx="8"/><path d="M32 44V32a18 18 0 0 1 36 0v12"/>',
        'calendar': '<rect x="14" y="20" width="72" height="66" rx="8"/><path d="M14 40h72M34 12v16M66 12v16"/>',
        'agent': '<rect x="18" y="26" width="64" height="56" rx="18"/><path d="M50 26V12"/><circle cx="38" cy="54" r="5"/><circle cx="62" cy="54" r="5"/>',
        'x': '<path d="M24 24l52 52M76 24L24 76"/>',
        'check': '<path d="M22 52l18 18 38-40"/>',
    }
    return f'<svg {s}>{P_.get(name, P_["doc"])}</svg>'

# ------------------------------------------------------------------ Bit
def bit_svgs(opts):
    r = subprocess.run(['node', str(ROOT / 'tools/bitsvg.cjs')], input=json.dumps(opts), capture_output=True, text=True, check=True)
    return json.loads(r.stdout)
def bit_block(sid, states, left, top, w):
    h = round(w * 0.9)
    svgs = bit_svgs([{**o, 'style': 'classic', 'w': w, 'h': h} for _, o in states])
    inner = ''.join(f'<div id="{sid}-bit-{k}">{s}</div>' for (k, _), s in zip(states, svgs))
    return f'<div class="bit" id="{sid}-bit" style="left:{left}px; top:{top}px; width:{w}px; height:{h}px;">{inner}</div>'
def bit_on(sid, key, t, popit=True):
    sc = [f'    tl.set("#{sid}-bit > div", {{ opacity:0 }}, {t});', f'    tl.set("#{sid}-bit-{key}", {{ opacity:1 }}, {t});']
    if popit and t > 0:
        sc.append(f'    tl.fromTo("#{sid}-bit", {{ scale:1.1 }}, {{ scale:1, duration:.25, ease:"back.out(3)", immediateRender:false }}, {t});')
    return sc
def bit_float(sid, t0=0.1):
    d = round(S[sid][1] - S[sid][0], 3)
    return [f'    tl.fromTo("#{sid}-bit", {{ opacity:0, y:60 }}, {{ opacity:1, y:0, duration:.45, ease:"back.out(1.8)" }}, {t0});',
            f'    tl.fromTo("#{sid}-bit", {{ y:0 }}, {{ y:-14, duration:.8, ease:"sine.inOut", yoyo:true, repeat:{max(1, int(d / 0.8) - 1)}, immediateRender:false }}, {t0 + 0.45});']

# ------------------------------------------------------------------ templates (i = beat index, v = spec)
def t_slam(i, sid, v):
    words = v['text'].split()
    n = len(words); acc = n - 1 if n < 4 else n - 2
    spans = ' '.join(f'<span id="{sid}-w{k}" class="{"acc" if k >= acc else ""}" style="display:inline-block">{E(w)}</span>' for k, w in enumerate(words))
    size = 140 if len(v['text']) < 14 else 112 if len(v['text']) < 22 else 92
    body = f'<div class="center big" style="top:{430 - size // 2}px; font-size:{size}px; padding:0 40px">{spans}</div><div class="ring" id="{sid}-ring" style="left:740px; top:470px"></div>'
    sc = []
    for k in range(n):
        t = round(0.08 + k * 0.12, 3)
        sc.append(f'    tl.fromTo("#{sid}-w{k}", {{ opacity:0, scale:1.5, filter:"blur(14px)" }}, {{ opacity:1, scale:1, filter:"blur(0px)", duration:.24, ease:"expo.out" }}, {max(0.03, t)});')
    sc.append(ring(f'#{sid}-ring', round(0.1 + n * 0.12, 3)))
    return body, sc, ''

def t_browser(i, sid, v):
    hid = v.get('hidden', [])
    rows = ''.join(f'<div class="pv">{E(x)}</div>' for x in v['body'])
    hrows = ''.join(f'<div class="hx" id="{sid}-h{k}">{E(x)}</div>' for k, x in enumerate(hid))
    body = f"""<div class="card" id="{sid}-card" style="left:110px; top:70px; width:1100px;">
      <div class="hd"><div class="tile">{icon('globe')}</div><div><div class="lab">{E(v.get('label', 'ILLUSTRATION'))} · NOT A REAL SITE</div><div class="ttl">{E(v['url'])}</div></div></div>
      <div class="paper"><div class="ph">{E(v['title'])}</div>{rows}<div class="img"></div><div class="blank">{hrows}</div></div></div>"""
    css = """.paper { background:#FFFFFF; border-radius:20px; padding:30px 40px; height:460px; position:relative; }
.ph { font:700 44px 'SD Display'; color:#1E120C; } .pv { font:500 28px 'SD Text'; color:#7A6558; }
.img { height:120px; border-radius:14px; background:linear-gradient(90deg,#F87736,#FFB36B); margin:18px 0; }
.blank { position:absolute; left:40px; right:40px; bottom:24px; height:110px; }
.hx { font:700 30px 'SD Mono'; color:#FFFFFF; position:relative; } .hx::before { content:''; position:absolute; left:-8px; right:-8px; top:0; bottom:0; background:rgba(248,119,54,.25); transform:scaleX(0); transform-origin:left; }"""
    sc = [fly(f'#{sid}-card')]
    if v.get('reveal'):
        t0 = wfrac(i, 0.45)
        for k in range(len(hid)):
            sc.append(f'    tl.to("#{sid}-h{k}", {{ color:"#E0261B", duration:.25 }}, {round(t0 + k * 0.25, 3)});')
        sc.append(shake(f'#{sid}-card', round(t0, 3)))
    return body, sc, css

def t_agent(i, sid, v):
    mode = v.get('mode', 'normal')
    st = {'hijack': ('hijack', ['alert']), 'normal': ('normal', []), 'happy': ('happy', ['done'] if 0 else []), 'scan': ('scan', ['laser'])}[mode]
    states = [('a', {'state': 'normal', 'arms': 'type' if v.get('log') else 'down'}), ('b', {'state': st[0], 'extra': st[1], 'arms': 'type' if v.get('log') else ('wave' if mode == 'happy' else 'down')})]
    log = v.get('log')
    bx = 120 if log else 430
    body = bit_block(sid, states, bx, 150, 460)
    sc = bit_on(sid, 'a', 0, False) + bit_float(sid)
    if log:
        rows = ''.join(f'<div class="lr{" bad" if k == len(log) - 1 else ""}" id="{sid}-r{k}"><span>{E(x)}</span><b>{"●" if k else "✓"}</b></div>' for k, x in enumerate(log))
        body += f'<div class="card" id="{sid}-log" style="left:640px; top:140px; width:660px;"><div class="hd"><div class="tile">{icon("code")}</div><div><div class="lab">AGENT ACTIVITY LOG</div><div class="ttl">ILLUSTRATION</div></div></div><div class="inner">{rows}</div></div>'
        sc.append(fly(f'#{sid}-log', 0.15))
        for k in range(len(log)):
            sc.append(fade(f'#{sid}-r{k}', wfrac(i, 0.35 + k * 0.2)))
        sc += bit_on(sid, 'b', wfrac(i, 0.75)) + [f'    tl.to("#{sid}-log", {{ borderColor:"#FF3B30", boxShadow:"0 0 60px rgba(255,59,48,.45)", duration:.25 }}, {wfrac(i, 0.75)});']
    else:
        sc += bit_on(sid, 'b', 0.6 if mode != 'normal' else 0, mode != 'normal')
    if v.get('caption'):
        body += f'<div class="center capt" id="{sid}-cap" style="top:640px">{E(v["caption"])}</div>'
        sc.append(pop(f'#{sid}-cap', wfrac(i, 0.3)))
    css = """.lr { display:flex; align-items:center; justify-content:space-between; height:74px; padding:0 20px; margin:8px 0; border-radius:16px; background:#1A0F0A; border:2px solid #2E1B13; font:700 24px 'SD Mono'; color:var(--ink); }
.lr b { color:var(--green); } .lr.bad { border-color:var(--red); background:#2A0D0A; color:#FF6B5E; } .lr.bad b { color:var(--red); }
.capt { font:900 64px 'SD Display'; color:var(--accent); letter-spacing:2px; }"""
    return body, sc, css

def t_nolist(i, sid, v):
    items = v['items']
    cards = ''.join(f'<div class="nl" id="{sid}-n{k}"><div class="ic">{icon("lock" if v.get("lock") else "x", 64, "#FF3B30")}</div><div class="nt">{E(x)}</div></div>' for k, x in enumerate(items))
    body = f'<div class="row" id="{sid}-row">{cards}</div>'
    css = """.row { position:absolute; left:60px; right:60px; top:230px; display:flex; gap:30px; justify-content:center; }
.nl { width:360px; height:300px; border-radius:30px; background:linear-gradient(180deg,#2C1A13,#1F120C); border:2px solid var(--edge); display:flex; flex-direction:column; align-items:center; justify-content:center; gap:24px; }
.ic { width:120px; height:120px; border-radius:60px; background:#2A0D0A; border:3px solid var(--red); display:flex; align-items:center; justify-content:center; }
.nt { font:700 42px 'SD Display'; color:var(--ink); text-align:center; padding:0 20px; }"""
    sc = [pop(f'#{sid}-n{k}', wfrac(i, k / len(items) * 0.85 + 0.02)) for k in range(len(items))]
    return body, sc, css

def t_shift(i, sid, v):
    body = f"""<div class="sb" id="{sid}-a" style="left:110px">{icon('chat', 70)}<div>{E(v['from'])}</div></div>
<div class="arrow" id="{sid}-ar">→</div>
<div class="sb hot" id="{sid}-b" style="left:760px">{icon('agent', 70)}<div>{E(v['to'])}</div></div>
<div class="center tagl" id="{sid}-t" style="top:600px">{E(v['tag'])}</div>"""
    css = """.sb { position:absolute; top:200px; width:460px; height:300px; border-radius:30px; background:linear-gradient(180deg,#2C1A13,#1F120C); border:2px solid var(--edge);
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:24px; font:700 44px 'SD Display'; color:var(--ink); text-align:center; }
.sb.hot { border:3px solid var(--accent); box-shadow:0 0 60px rgba(248,119,54,.35); }
.arrow { position:absolute; left:610px; top:290px; font:900 110px 'SD Display'; color:var(--accent); }
.tagl { font:600 italic 52px 'SD Serif'; color:var(--accent-soft); }"""
    sc = [fly(f'#{sid}-a'), pop(f'#{sid}-ar', wfrac(i, 0.3)), fly(f'#{sid}-b', wfrac(i, 0.35)), pop(f'#{sid}-t', wfrac(i, 0.65))]
    return body, sc, css

def t_flow(i, sid, v):
    nodes = v['nodes']; n = len(nodes); gap = 1240 // n
    hi = v.get('hi', -1)
    h = ''
    for k, nd in enumerate(nodes):
        x = 60 + k * gap + (gap - 240) // 2
        h += f'<div class="fn{" hi" if k == hi else ""}" id="{sid}-n{k}" style="left:{x}px">{icon(nd["icon"], 84)}<div>{E(nd["label"])}</div></div>'
        if k < n - 1:
            h += f'<div class="fa" id="{sid}-a{k}" style="left:{x + 250}px; width:{gap - 260}px"></div>'
    if v.get('end'):
        h += f'<div class="center endt" id="{sid}-end" style="top:580px">{E(v["end"])}</div>'
    css = """.fn { position:absolute; top:230px; width:240px; height:240px; border-radius:30px; background:linear-gradient(180deg,#2C1A13,#1F120C); border:2px solid var(--edge);
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:18px; font:700 34px 'SD Display'; color:var(--ink); }
.fn.hi { border:3px solid var(--red); box-shadow:0 0 50px rgba(255,59,48,.4); }
.fa { position:absolute; top:346px; height:8px; border-radius:4px; background:var(--accent); transform-origin:left; }
.endt { font:900 90px 'SD Display'; color:var(--red); letter-spacing:6px; }"""
    sc = []
    for k in range(n):
        t = wfrac(i, k / n * 0.8)
        sc.append(pop(f'#{sid}-n{k}', t))
        if k < n - 1:
            sc.append(f'    tl.fromTo("#{sid}-a{k}", {{ scaleX:0 }}, {{ scaleX:1, duration:.3, ease:"power2.out" }}, {round(t + 0.25, 3)});')
    if v.get('end'):
        sc.append(f'    tl.fromTo("#{sid}-end", {{ opacity:0, scale:1.6 }}, {{ opacity:1, scale:1, duration:.22, ease:"power4.in" }}, {wfrac(i, 0.85)});')
    return h, sc, css

def t_loop(i, sid, v):
    steps = v['steps']; up = v.get('upto', -1); danger = v.get('danger')
    import math
    cx, cy, r = 470, 380, 270
    h = f'<div class="hub" id="{sid}-hub">AI<br><span>AGENT</span></div><svg class="orb" width="1000" height="800"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#3E2217" stroke-width="6" stroke-dasharray="14 14"/></svg>'
    for k, s in enumerate(steps):
        a = -math.pi / 2 + k * 2 * math.pi / len(steps)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        cls = ' bad' if danger == k else ' on' if k == up else ' done' if 0 <= k < up or up == len(steps) - 1 and k < up else ''
        h += f'<div class="st{cls}" id="{sid}-s{k}" style="left:{x - 140:.0f}px; top:{y - 50:.0f}px"><b>{k + 1}</b>{E(s)}</div>'
    side = ''
    if v.get('tools'):
        side = ''.join(f'<div class="tl" id="{sid}-t{k}">{icon(ic, 46)}<span>{E(t)}</span></div>' for k, (t, ic) in enumerate(zip(v['tools'], ['globe', 'mail', 'code'])))
        h += f'<div class="tools">{side}</div>'
    if danger is not None:
        h += f'<div class="inj" id="{sid}-inj">untrusted text →</div>'
    if v.get('note'):
        h += f'<div class="note" id="{sid}-note">a note from someone else</div>'
    css = """.orb { position:absolute; left:0; top:0; }
.hub { position:absolute; left:370px; top:290px; width:200px; height:180px; border-radius:40px; background:#F87736; color:#1A0A04; text-align:center; font:900 70px 'SD Display'; line-height:.95; padding-top:30px; }
.hub span { font:700 24px 'SD Text'; letter-spacing:4px; }
.st { position:absolute; width:280px; height:100px; border-radius:24px; background:#1A0F0A; border:2px solid var(--edge); display:flex; align-items:center; gap:16px; padding:0 18px; font:700 32px 'SD Display'; color:#8C6B5A; }
.st b { width:56px; height:56px; flex:none; border-radius:28px; background:#2A1912; display:flex; align-items:center; justify-content:center; font-size:30px; color:#8C6B5A; }
.st.done { color:var(--ink); } .st.done b { background:#3A2318; color:var(--accent); }
.st.on { border:3px solid var(--accent); color:var(--ink); box-shadow:0 0 40px rgba(248,119,54,.45); } .st.on b { background:var(--accent); color:#1A0A04; }
.st.bad { border:3px solid var(--red); color:#FF6B5E; box-shadow:0 0 50px rgba(255,59,48,.5); } .st.bad b { background:var(--red); color:#fff; }
.tools { position:absolute; left:1000px; top:150px; display:flex; flex-direction:column; gap:20px; }
.tl { width:290px; height:110px; border-radius:24px; background:linear-gradient(180deg,#2C1A13,#1F120C); border:2px solid var(--edge); display:flex; align-items:center; gap:18px; padding:0 22px; font:700 32px 'SD Display'; color:var(--ink); }
.inj { position:absolute; left:960px; top:560px; padding:20px 28px; border-radius:20px; background:#2A0D0A; border:3px solid var(--red); font:700 30px 'SD Mono'; color:#FF6B5E; }
.note { position:absolute; left:960px; top:100px; width:320px; padding:24px; border-radius:6px; background:#FFE9A8; color:#3A2A10; font:600 italic 40px 'SD Serif'; transform:rotate(4deg); }"""
    sc = [pop(f'#{sid}-hub', 0.05)] + [pop(f'#{sid}-s{k}', round(0.1 + k * 0.08, 3)) for k in range(len(steps))]
    if up >= 0:
        sc.append(f'    tl.fromTo("#{sid}-s{up}", {{ scale:1 }}, {{ scale:1.1, duration:.18, yoyo:true, repeat:1, immediateRender:false }}, {wfrac(i, 0.1)});')
    for k in range(len(v.get('tools', []))):
        sc.append(fade(f'#{sid}-t{k}', wfrac(i, 0.4 + k * 0.15), 60))
    if danger is not None:
        sc += [fade(f'#{sid}-inj', wfrac(i, 0.5), 80), shake(f'#{sid}-s{danger}', wfrac(i, 0.55))]
    if v.get('note'):
        sc.append(f'    tl.fromTo("#{sid}-note", {{ opacity:0, x:200, rotation:20 }}, {{ opacity:1, x:0, rotation:4, duration:.45, ease:"back.out(1.6)" }}, {wfrac(i, 0.7)});')
    return h, sc, css

def t_chat(i, sid, v):
    msgs = ''.join(f'<div class="m {m["from"]}" id="{sid}-m{k}">{E(m["text"])}</div>' for k, m in enumerate(v['msgs']))
    body = f'<div class="card" id="{sid}-card" style="left:160px; top:90px; width:1000px;"><div class="hd"><div class="tile">{icon("chat")}</div><div><div class="lab">{E(v.get("label", "ILLUSTRATION"))}</div><div class="ttl">Chat</div></div></div><div class="inner" style="min-height:360px">{msgs}</div></div>'
    css = """.m { max-width:720px; padding:22px 30px; border-radius:30px; margin:16px 0; font:700 36px 'SD Display'; }
.m.you { margin-left:auto; background:var(--accent); color:#1A0A04; border-bottom-right-radius:8px; }
.m.agent { background:#F3E6DC; color:#2A1A12; border-bottom-left-radius:8px; }"""
    sc = [fly(f'#{sid}-card')] + [pop(f'#{sid}-m{k}', wfrac(i, 0.05 + k * 0.5)) for k in range(len(v['msgs']))]
    return body, sc, css

def t_split(i, sid, v):
    L_, R_ = v['left'], v['right']; bad = v.get('bad')
    def box(side, d, x):
        return f'<div class="sp{" bad" if bad == side else ""}" id="{sid}-{side}" style="left:{x}px">{icon(d["icon"], 90, "#FF3B30" if bad == side else "#F87736")}<div class="t">{E(d["title"])}</div><div class="bd">{E(d["body"])}</div></div>'
    body = box('left', L_, 90) + box('right', R_, 720)
    if v.get('merge'):
        body += f'<div class="center mg" id="{sid}-mg" style="top:620px">{E(v["merge"])}</div>'
    css = """.sp { position:absolute; top:130px; width:510px; height:420px; border-radius:30px; background:linear-gradient(180deg,#2C1A13,#1F120C); border:2px solid var(--edge);
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:16px; text-align:center; padding:30px; }
.sp.bad { border:3px solid var(--red); box-shadow:0 0 60px rgba(255,59,48,.35); }
.sp .t { font:900 56px 'SD Display'; color:var(--ink); } .sp .bd { font:500 34px 'SD Text'; color:#CDB8AA; }
.mg { font:900 64px 'SD Display'; color:var(--accent); letter-spacing:2px; }"""
    sc = [fly(f'#{sid}-left', 0.05, 10, 20), fly(f'#{sid}-right', wfrac(i, 0.4), 10, -20)]
    if v.get('merge'):
        sc += [f'    tl.to("#{sid}-left", {{ x:55, duration:.5, ease:"power3.inOut" }}, {wfrac(i, 0.72)});',
               f'    tl.to("#{sid}-right", {{ x:-55, duration:.5, ease:"power3.inOut" }}, {wfrac(i, 0.72)});',
               pop(f'#{sid}-mg', wfrac(i, 0.8))]
    return body, sc, css

COLS = {'dim': '#8C6B5A', 'cyan': '#55C2FF', 'text': '#F6EEE8', 'hot': '#FF6B5E'}
def t_code(i, sid, v):
    lines = ''.join(f'<div class="cl" id="{sid}-l{k}" style="color:{COLS.get(l["c"], "#F6EEE8")}">{E(l["t"])}</div>' for k, l in enumerate(v['lines']))
    body = f'<div class="card" id="{sid}-card" style="left:100px; top:110px; width:1120px;"><div class="hd"><div class="tile">{icon("code")}</div><div><div class="lab">{E(v.get("label", "ILLUSTRATION"))}</div><div class="ttl">{E(v["file"])}</div></div></div><div class="inner" style="min-height:300px">{lines}</div></div>'
    css = ".cl { font:700 30px 'SD Mono'; line-height:1.8; white-space:pre; }"
    sc = [fly(f'#{sid}-card')] + [fade(f'#{sid}-l{k}', wfrac(i, 0.05 + k * 0.7 / len(v['lines'])), -40) for k in range(len(v['lines']))]
    return body, sc, css

def t_email(i, sid, v):
    body = f"""<div class="card" id="{sid}-card" style="left:140px; top:80px; width:1040px;">
  <div class="hd"><div class="tile">{icon('mail')}</div><div><div class="lab">{E(v.get('label', 'ILLUSTRATION'))}</div><div class="ttl">{E(v['subject'])}</div></div></div>
  <div class="paper"><div class="fr">From: {E(v['from'])}</div>{''.join(f'<div class="bd">{E(x)}</div>' for x in v['body'])}
  {''.join(f'<div class="hx" id="{sid}-h{k}">{E(x)}</div>' for k, x in enumerate(v['hidden']))}</div></div>"""
    css = """.paper { background:#FFFFFF; border-radius:20px; padding:30px 40px; min-height:360px; }
.fr { font:500 26px 'SD Text'; color:#9A8576; margin-bottom:20px; } .bd { font:700 40px 'SD Display'; color:#1E120C; }
.hx { margin-top:80px; font:700 30px 'SD Mono'; color:#FFFFFF; }"""
    sc = [fly(f'#{sid}-card'), f'    tl.to("#{sid}-h0", {{ color:"#E0261B", duration:.3 }}, {wfrac(i, 0.55)});', shake(f'#{sid}-card', wfrac(i, 0.55))]
    return body, sc, css

def t_icons(i, sid, v):
    items = v['items']; n = len(items)
    cards = ''.join(f'<div class="ib" id="{sid}-c{k}"><div class="it">{icon(it["icon"], 90)}</div><div>{E(it["label"])}</div></div>' for k, it in enumerate(items))
    body = f'<div class="row">{cards}</div>'
    css = """.row { position:absolute; left:40px; right:40px; top:220px; display:flex; gap:30px; justify-content:center; }
.ib { width:360px; height:330px; border-radius:30px; background:linear-gradient(180deg,#2C1A13,#1F120C); border:2px solid var(--edge); display:flex; flex-direction:column; align-items:center; justify-content:center; gap:26px;
  font:700 40px 'SD Display'; color:var(--ink); text-align:center; padding:0 20px; }
.it { width:150px; height:150px; border-radius:36px; background:#F3E6DC; display:flex; align-items:center; justify-content:center; }"""
    sc = [pop(f'#{sid}-c{k}', wfrac(i, 0.05 + k / n * 0.75)) for k in range(n)]
    return body, sc, css

def t_stream(i, sid, v):
    cols = {'dim': '#8C6B5A', 'green': '#3DDC97', 'red': '#FF3B30'}
    parts = ''.join(f'<div class="pt" id="{sid}-p{k}" style="background:{cols[c]}">{E(t)}</div>' for k, (t, c) in enumerate(v['parts']))
    toks = ''.join(f'<i style="background:{cols[c]}"></i>' * 9 for _, c in v['parts'])
    body = f'<div class="parts">{parts}</div><div class="seq" id="{sid}-seq">{toks}</div><div class="center sl" id="{sid}-sl" style="top:620px">{E(v["label"])}</div>'
    css = """.parts { position:absolute; left:80px; right:80px; top:120px; display:flex; gap:30px; justify-content:center; }
.pt { width:360px; height:150px; border-radius:26px; display:flex; align-items:center; justify-content:center; font:800 40px 'SD Display'; color:#0C0704; text-align:center; padding:0 20px; }
.seq { position:absolute; left:110px; top:420px; width:1100px; height:90px; display:flex; gap:6px; padding:14px; border-radius:24px; background:#1A0F0A; border:3px solid var(--accent); }
.seq i { flex:1; border-radius:8px; opacity:.9; }
.sl { font:900 60px 'SD Display'; color:var(--accent); letter-spacing:3px; }"""
    sc = [pop(f'#{sid}-p{k}', wfrac(i, 0.08 + k * 0.2)) for k in range(len(v['parts']))]
    sc += [f'    tl.to("#{sid}-p0, #{sid}-p1, #{sid}-p2", {{ y:300, opacity:0, scale:.4, duration:.5, ease:"power3.in", stagger:.08 }}, {wfrac(i, 0.75)});',
           f'    tl.fromTo("#{sid}-seq", {{ opacity:0, scaleX:.2 }}, {{ opacity:1, scaleX:1, duration:.45, ease:"expo.out" }}, {wfrac(i, 0.82)});',
           pop(f'#{sid}-sl', wfrac(i, 0.9))]
    return body, sc, css

def t_wall(i, sid, v):
    body = f"""<div class="wb" id="{sid}-l" style="left:150px">{icon('code', 100)}<div>{E(v['left'])}</div></div>
<div class="wl" id="{sid}-w"></div>
<div class="wb" id="{sid}-r" style="left:780px">{icon('doc', 100)}<div>{E(v['right'])}</div></div>"""
    css = """.wb { position:absolute; top:180px; width:390px; height:380px; border-radius:30px; background:linear-gradient(180deg,#2C1A13,#1F120C); border:2px solid var(--edge);
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:30px; font:900 64px 'SD Display'; color:var(--ink); }
.wl { position:absolute; left:620px; top:110px; width:80px; height:520px; border-radius:12px;
  background:repeating-linear-gradient(0deg,#F87736 0 56px,#1A0A04 56px 62px), #F87736; box-shadow:0 0 60px rgba(248,119,54,.5); transform-origin:bottom; }"""
    sc = [fly(f'#{sid}-l'), fly(f'#{sid}-r', 0.15),
          f'    tl.fromTo("#{sid}-w", {{ scaleY:0 }}, {{ scaleY:1, duration:.6, ease:"back.out(1.5)" }}, {wfrac(i, 0.45)});']
    return body, sc, css

def t_merge(i, sid, v):
    body = f"""<div class="mb g" id="{sid}-a"><small>YOUR REQUEST</small>{E(v['a'])}</div>
<div class="mb r" id="{sid}-b"><small>HIDDEN COMMAND</small>{E(v['b'])}</div>
<div class="center ml" id="{sid}-l" style="top:600px">{E(v['label'])}</div>"""
    css = """.mb { position:absolute; left:210px; width:900px; padding:30px 40px; border-radius:28px; font:800 50px 'SD Display'; color:#0C0704; }
.mb small { display:block; font:700 24px 'SD Mono'; letter-spacing:3px; margin-bottom:8px; opacity:.75; }
.mb.g { top:110px; background:var(--green); } .mb.r { top:330px; background:var(--red); color:#fff; }
.ml { font:900 54px 'SD Display'; color:var(--accent); letter-spacing:2px; }"""
    sc = [fade(f'#{sid}-a', wfrac(i, 0.1), -200), fade(f'#{sid}-b', wfrac(i, 0.4), 200),
          f'    tl.to("#{sid}-a, #{sid}-b", {{ background:"#F3E6DC", color:"#1E120C", duration:.4 }}, {wfrac(i, 0.82)});',
          pop(f'#{sid}-l', wfrac(i, 0.82))]
    return body, sc, css

def t_stack(i, sid, v):
    items = v['items']; hi = v.get('hi', -1); rank = v.get('rank')
    rows = ''.join(f'<div class="sr{" hi" if k == hi else ""}" id="{sid}-r{k}" style="margin-left:{k * 40 if not rank else 0}px; width:{760 - (k * 80 if rank else 0)}px"><b>{k + 1}</b>{E(x)}</div>' for k, x in enumerate(items))
    src = f'<div class="tag" style="left:230px; top:680px">{E(v["source"])}</div>' if v.get('source') else ''
    body = f'<div class="center kick" style="top:60px" id="{sid}-k">{E(v["title"])}</div><div class="stk">{rows}</div>{src}'
    css = """.stk { position:absolute; left:230px; top:130px; }
.sr { height:92px; margin-bottom:14px; border-radius:22px; background:linear-gradient(90deg,#2C1A13,#1F120C); border:2px solid var(--edge); display:flex; align-items:center; gap:22px; padding:0 22px;
  font:700 40px 'SD Display'; color:var(--ink); }
.sr b { width:58px; height:58px; border-radius:29px; background:#3A2318; color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:30px; }
.sr.hi { border:3px solid var(--red); box-shadow:0 0 50px rgba(255,59,48,.45); color:#FF6B5E; } .sr.hi b { background:var(--red); color:#fff; }"""
    sc = [pop(f'#{sid}-k', 0.05)] + [fade(f'#{sid}-r{k}', wfrac(i, 0.05 + k * 0.6 / len(items))) for k in range(len(items))]
    if hi >= 0:
        sc += [shake(f'#{sid}-r{hi}', wfrac(i, 0.6)), f'    tl.fromTo("#{sid}-r{hi}", {{ scale:1 }}, {{ scale:1.06, duration:.2, yoyo:true, repeat:1, immediateRender:false }}, {wfrac(i, 0.6)});']
    return body, sc, css

def t_memory(i, sid, v):
    bad = v.get('bad', -1)
    notes = ''.join(f'<div class="nt{" x" if k == bad else ""}" id="{sid}-n{k}">{E(x)}</div>' for k, x in enumerate(v['notes']))
    body = f'<div class="card" id="{sid}-card" style="left:90px; top:60px; width:{760 if v.get("chats") else 1100}px;"><div class="hd"><div class="tile">{icon("server")}</div><div><div class="lab">ILLUSTRATION</div><div class="ttl">Your agent\'s long-term memory</div></div></div><div class="inner">{notes}</div></div>'
    chats = v.get('chats', [])
    body += ''.join(f'<div class="ch" id="{sid}-c{k}" style="top:{90 + k * 190}px"><span>New chat · {E(c)}</span><b>loads memory ●</b></div>' for k, c in enumerate(chats))
    css = """.nt { padding:20px 26px; margin:12px 0; border-radius:16px; background:#F3E6DC; color:#2A1A12; font:600 34px 'SD Text'; }
.nt.x { background:#2A0D0A; border:3px solid var(--red); color:#FF6B5E; font:700 30px 'SD Mono'; }
.ch { position:absolute; left:900px; width:400px; height:150px; border-radius:26px; background:linear-gradient(180deg,#2C1A13,#1F120C); border:2px solid var(--edge);
  display:flex; flex-direction:column; justify-content:center; gap:10px; padding:0 26px; font:700 32px 'SD Display'; color:var(--ink); }
.ch b { font:600 24px 'SD Text'; color:var(--red); }"""
    sc = [fly(f'#{sid}-card')]
    for k in range(len(v['notes'])):
        if k == bad and not chats:
            sc += [f'    tl.fromTo("#{sid}-n{k}", {{ opacity:0, x:300, rotation:5 }}, {{ opacity:1, x:0, rotation:-1, duration:.4, ease:"back.out(2)" }}, {wfrac(i, 0.3)});',
                   f'    tl.to("#{sid}-card", {{ borderColor:"#FF3B30", duration:.3 }}, {wfrac(i, 0.35)});']
        else:
            sc.append(pop(f'#{sid}-n{k}', round(0.25 + k * 0.12, 3)))
    for k in range(len(chats)):
        sc.append(fade(f'#{sid}-c{k}', wfrac(i, 0.2 + k * 0.22), 120))
    return body, sc, css

def t_quote(i, sid, v):
    body = f"""<div class="center qm" style="top:80px">“</div><div class="center qt" id="{sid}-q" style="top:250px">{E(v['text'])}</div>
<div class="center qw" id="{sid}-w" style="top:470px">— {E(v['who'])} · {E(v['when'])}</div>"""
    css = """.qm { font:900 220px 'SD Serif'; color:var(--accent); line-height:1; } .qt { font:600 italic 92px 'SD Serif'; color:var(--ink); padding:0 80px; line-height:1.1; }
.qw { font:600 32px 'SD Text'; color:var(--dim); letter-spacing:1px; }"""
    sc = [f'    tl.fromTo("#{sid}-q", {{ opacity:0, y:40, filter:"blur(12px)" }}, {{ opacity:1, y:0, filter:"blur(0px)", duration:.6, ease:"expo.out" }}, {wfrac(i, 0.1)});', pop(f'#{sid}-w', wfrac(i, 0.3))]
    return body, sc, css

def t_checklist(i, sid, v):
    items, up = v['items'], v['upto']
    rows = ''
    for k, x in enumerate(items):
        cls = ' on' if k == up else ' done' if k < up else ''
        rows += f'<div class="cr{cls}" id="{sid}-r{k}"><b>{k + 1}</b>{E(x)}</div>'
    det = f'<div class="det" id="{sid}-d">{E(v["detail"])}</div>' if v.get('detail') else ''
    body = f'<div class="kick" style="position:absolute; left:120px; top:40px">{E(v["title"])} TO STAY SAFE</div><div class="cl">{rows}</div>{det}'
    css = """.cl { position:absolute; left:120px; top:100px; width:1080px; }
.cr { height:88px; margin-bottom:12px; border-radius:22px; background:#140B07; border:2px solid #2E1B13; display:flex; align-items:center; gap:22px; padding:0 22px; font:700 40px 'SD Display'; color:#6E5444; }
.cr b { width:56px; height:56px; border-radius:28px; background:#2A1912; color:#8C6B5A; display:flex; align-items:center; justify-content:center; font-size:30px; flex:none; }
.cr.done { color:var(--ink); } .cr.done b { background:#3A2318; color:var(--accent); }
.cr.on { border:3px solid var(--accent); color:var(--ink); box-shadow:0 0 50px rgba(248,119,54,.4); background:#2A1810; } .cr.on b { background:var(--accent); color:#1A0A04; }
.det { position:absolute; left:120px; top:620px; width:1080px; padding:24px 34px; border-radius:24px; background:#F3E6DC; color:#1E120C; font:800 44px 'SD Display'; }"""
    if up < 0:
        sc = [fade(f'#{sid}-r{k}', wfrac(i, 0.55 + k * 0.08)) for k in range(len(items))]
    else:
        sc = [fade(f'#{sid}-r{k}', round(0.04 + k * 0.04, 3)) for k in range(len(items))]
        sc.append(f'    tl.fromTo("#{sid}-r{up}", {{ scale:1 }}, {{ scale:1.05, duration:.2, yoyo:true, repeat:1, immediateRender:false }}, 0.25);')
    if det:
        sc.append(pop(f'#{sid}-d', wfrac(i, 0.45)))
    return body, sc, css

def t_end(i, sid, v):
    body = f"""<div class="center big" id="{sid}-t" style="top:250px"><span class="acc">TECH</span>DECODED</div>
<div class="center es" id="{sid}-s" style="top:400px">{E(v['sub'])}</div>
<div class="sub" id="{sid}-b">SUBSCRIBE</div>"""
    css = """.es { font:600 italic 56px 'SD Serif'; color:var(--accent-soft); }
.sub { position:absolute; left:500px; top:540px; width:320px; height:96px; border-radius:48px; background:var(--red); color:#fff; font:900 40px 'SD Display'; display:flex; align-items:center; justify-content:center; letter-spacing:2px; }"""
    sc = [f'    tl.fromTo("#{sid}-t", {{ opacity:0, scale:1.4, filter:"blur(14px)" }}, {{ opacity:1, scale:1, filter:"blur(0px)", duration:.4, ease:"expo.out" }}, 0.05);',
          pop(f'#{sid}-s', 0.4), pop(f'#{sid}-b', wfrac(i, 0.75)),
          f'    tl.fromTo("#{sid}-b", {{ scale:1 }}, {{ scale:1.08, duration:.3, yoyo:true, repeat:7, ease:"sine.inOut", immediateRender:false }}, {wfrac(i, 0.75) + 0.35});']
    return body, sc, css

T = {'slam': t_slam, 'browser': t_browser, 'agent': t_agent, 'nolist': t_nolist, 'shift': t_shift, 'flow': t_flow, 'loop': t_loop, 'chat': t_chat,
     'split': t_split, 'code': t_code, 'email': t_email, 'icons': t_icons, 'stream': t_stream, 'wall': t_wall, 'merge': t_merge, 'stack': t_stack,
     'memory': t_memory, 'quote': t_quote, 'checklist': t_checklist, 'end': t_end}

def beat_scene(i):
    sid = f'b{i:02d}'
    v = BE[i]['v']
    body, sc, css = T[v['type']](i, sid, v)
    body = f'<div class="stage" id="{sid}-all">{body}</div>'
    if i + 1 < len(BE):
        sc.append(out(sid))
    return scene(sid, body, '\n'.join(sc), css)

# ------------------------------------------------------------------ chapter pill (persistent, top-left) + bumper
def chapters():
    body, sc = [], []
    for k, (i, title) in enumerate(CHAPTERS):
        a = S[f'b{i:02d}'][0]
        b = S[f'b{CHAPTERS[k + 1][0]:02d}'][0] if k + 1 < len(CHAPTERS) else DUR
        body.append(f'<div class="cp" id="ch{k}"><b>{k + 1:02d}</b>{E(title)}</div>')
        sc.append(f'    tl.fromTo("#ch{k}", {{ opacity:0, x:-40 }}, {{ opacity:1, x:0, duration:.35, ease:"expo.out" }}, {round(a + 0.05, 3)});')
        sc.append(f'    tl.to("#ch{k}", {{ opacity:0, duration:.15 }}, {round(b - 0.15, 3)});')
    css = """.cp { position:absolute; left:80px; top:36px; height:56px; padding:0 26px 0 8px; border-radius:28px; background:#140B07; border:2px solid #3E2217; display:flex; align-items:center; gap:14px;
  font:600 24px 'SD Text'; color:var(--ink); letter-spacing:1px; opacity:0; }
.cp b { width:42px; height:42px; border-radius:21px; background:var(--accent); color:#1A0A04; display:flex; align-items:center; justify-content:center; font:700 20px 'SD Display'; }"""
    return scene('chapters', '\n'.join(body), '\n'.join(sc), css)

def bg():
    body = """<div class="grid"></div><div class="vig"></div>
<div class="glow" id="bg-g0" style="left:-200px; top:200px;"></div><div class="glow" id="bg-g1" style="left:1200px; top:400px; width:1100px; height:1100px;"></div>
<div class="plus" style="left:60px; top:960px;">+</div><div class="plus" style="left:1400px; top:60px;">+</div><div class="sq" style="left:1360px; top:980px;"></div>"""
    css = """#root { background:var(--ground); }
.grid { position:absolute; inset:-120px; background-image:linear-gradient(rgba(248,119,54,.09) 2px, transparent 2px), linear-gradient(90deg, rgba(248,119,54,.09) 2px, transparent 2px); background-size:96px 96px; }
.glow { position:absolute; width:900px; height:900px; border-radius:50%; background:radial-gradient(circle, rgba(248,119,54,.22) 0%, rgba(248,119,54,.07) 38%, transparent 66%); }
.plus { position:absolute; font:500 50px 'SD Text'; color:var(--accent); opacity:.7; } .sq { position:absolute; width:24px; height:24px; border:3px solid #7A5A48; border-radius:5px; }
.vig { position:absolute; inset:0; background:radial-gradient(ellipse at 45% 45%, transparent 50%, rgba(0,0,0,.7) 100%); }"""
    sc = [f'    tl.fromTo("#bg-g0", {{ x:0, y:0 }}, {{ x:500, y:-100, duration:{DUR}, ease:"sine.inOut" }}, 0);',
          f'    tl.fromTo("#bg-g1", {{ x:0, y:0 }}, {{ x:-400, y:-300, duration:{DUR}, ease:"sine.inOut" }}, 0);',
          f'    tl.fromTo(".grid", {{ y:0 }}, {{ y:-96 * {int(DUR // 20)}, duration:{DUR}, ease:"none" }}, 0);']
    return scene('bg', body, '\n'.join(sc), css)

def caption_groups():
    groups, cur = [], []
    for w in WORDS:
        if w[0] in ('—', '-'):
            continue
        cur.append(w)
        if re.search(r'[.,:;!?]$', w[0]) or len(cur) >= 4:
            groups.append(cur); cur = []
    if cur: groups.append(cur)
    return groups

def captions(groups, part):
    body, sc = [], []
    for gi, g in groups:
        start = round(g[0][1] - 0.06, 3)
        nxt = next((gg for gj, gg in groups if gj == gi + 1), None)
        end = round(nxt[0][1] - 0.06, 3) if nxt else round(g[-1][2] + 0.6, 3)
        end = min(end, round(g[-1][2] + 0.8, 3))
        spans = []
        for wi, (txt, s, e) in enumerate(g):
            spans.append(f'<span class="w" id="c{gi}w{wi}"><b class="bx" id="c{gi}b{wi}"></b><em>{E(txt)}</em></span>')
            sc.append(f'    tl.to("#c{gi}w{wi} em", {{ color:"#F6EEE8", duration:.06 }}, {s});')
            sc.append(f'    tl.fromTo("#c{gi}b{wi}", {{ opacity:0 }}, {{ opacity:1, duration:.06 }}, {s});')
            nx = g[wi + 1][1] if wi + 1 < len(g) else end
            sc.append(f'    tl.to("#c{gi}b{wi}", {{ opacity:0, duration:.05 }}, {round(max(s + 0.08, min(nx, end) - 0.02), 3)});')
        body.append(f'    <div class="grp" id="c{gi}">{"".join(spans)}</div>')
        sc.append(f'    tl.set("#c{gi}", {{ visibility:"visible" }}, {start}); tl.fromTo("#c{gi}", {{ opacity:0 }}, {{ opacity:1, duration:.1 }}, {start});')
        sc.append(f'    tl.to("#c{gi}", {{ opacity:0, duration:.08 }}, {round(end - 0.08, 3)}); tl.set("#c{gi}", {{ visibility:"hidden" }}, {end});')
    css = """.grp { position:absolute; left:80px; width:1320px; top:930px; text-align:center; visibility:hidden; }
.w { position:relative; display:inline-block; margin:0 8px; } .w em { position:relative; font:700 52px 'SD Display'; font-style:normal; color:#5C4337; }
.bx { position:absolute; left:-10px; right:-10px; top:4px; bottom:-2px; border-radius:10px; background:#F87736; opacity:0; }"""
    return scene(f'caps{part}', '\n'.join(body), '\n'.join(sc), css)

SFX_BY_TYPE = {'slam': [(0.0, 'whoosh', .5), ('w', 'impact', .6)], 'browser': [(0.05, 'whoosh', .5)], 'agent': [(0.1, 'pop', .5)],
               'nolist': [('each', 'thud', .55)], 'flow': [('each', 'pop', .45)], 'icons': [('each', 'pop', .45)], 'chat': [(0.1, 'notify', .5)],
               'code': [(0.1, 'type', .4)], 'email': [(0.05, 'notify', .5)], 'split': [(0.05, 'whoosh', .45)], 'loop': [(0.1, 'tick', .5)],
               'stack': [(0.1, 'whoosh', .45)], 'memory': [(0.1, 'whoosh', .45)], 'quote': [(0.1, 'thud', .6)], 'checklist': [(0.15, 'ding', .45)],
               'end': [(0.1, 'riser', .5), (0.6, 'ding', .6)], 'stream': [(0.1, 'pop', .45)], 'wall': [(0.1, 'whoosh', .4)], 'merge': [(0.1, 'whoosh', .45)],
               'shift': [(0.1, 'whoosh', .45)]}
def sfx_list():
    c = []
    for i, b in enumerate(BE):
        a = S[f'b{i:02d}'][0]; v = b['v']
        for t, n, g in SFX_BY_TYPE.get(v['type'], []):
            if t == 'each':
                k = len(v.get('items', v.get('nodes', [])))
                c += [(a + wfrac(i, j / k * 0.8 + 0.02), n, g) for j in range(k)]
            elif t == 'w':
                c.append((a + wfrac(i, 0.75), n, g))
            else:
                c.append((a + t, n, g))
        if v['type'] == 'agent' and v.get('mode') == 'hijack':
            c += [(a + wfrac(i, 0.75), 'glitch', .55), (a + wfrac(i, 0.75), 'error', .4)]
        if v.get('reveal') or v['type'] == 'email':
            c.append((a + wfrac(i, 0.5), 'glitch', .5))
    return sorted(c)

def index():
    hosts = [f'<div id="bg" data-composition-id="bg" data-composition-src="compositions/bg.html" data-start="0" data-duration="{DUR}" data-track-index="0" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:1"></div>']
    for sid, (a, b) in S.items():
        hosts.append(f'<div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{a}" data-duration="{round(b - a, 3)}" data-track-index="1" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:2"></div>')
    hosts.append(f'<div id="chapters" data-composition-id="chapters" data-composition-src="compositions/chapters.html" data-start="0" data-duration="{DUR}" data-track-index="2" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:3"></div>')
    for part, (a, b) in enumerate(CAPPARTS):
        hosts.append(f'<div id="caps{part}" data-composition-id="caps{part}" data-composition-src="compositions/caps{part}.html" data-start="0" data-duration="{DUR}" data-track-index="{3 + part}" data-track-kind="captions" data-width="{W}" data-height="{H}" style="z-index:5"></div>')
    tr = 3 + len(CAPPARTS)
    if (P / 'assets/vo.wav').exists():
        hosts.append(f'<audio id="vo" class="clip" src="assets/vo.wav" data-start="0" data-duration="{DUR}" data-track-index="{tr}" data-volume="1"></audio>')
    if (P / 'assets/bgm.wav').exists():
        hosts.append(f'<audio id="bgm" class="clip" src="assets/bgm.wav" data-start="0" data-duration="{DUR}" data-track-index="{tr + 1}" data-volume="0.16"></audio>')
    lanes = []
    for k, (t, n, g) in enumerate(sfx_list()):
        lane = next((j for j, e in enumerate(lanes) if e <= t), None)
        if lane is None: lanes.append(0); lane = len(lanes) - 1
        lanes[lane] = t + 1.3
        with wave.open(str(P / 'assets/sfx' / f'{n}.wav')) as wf: dd = round(wf.getnframes() / wf.getframerate(), 3)
        hosts.append(f'<audio id="sfx{k}" class="clip" src="assets/sfx/{n}.wav" data-start="{round(t, 3)}" data-duration="{dd}" data-track-index="{tr + 2 + lane}" data-volume="{g}"></audio>')
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="assets/gsap.min.js"></script>
    <style>* {{ margin:0; padding:0; box-sizing:border-box; }} html, body {{ margin:0; width:{W}px; height:{H}px; overflow:hidden; background:#0C0704; }} #root {{ position:relative; width:100%; height:100%; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}" data-fps="30">
      {chr(10).join('      ' + h for h in hosts).strip()}
    </div>
    <script>window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
  </body>
</html>
"""

if __name__ == '__main__':
    comp = P / 'compositions'; comp.mkdir(parents=True, exist_ok=True)
    for f in comp.glob('*.html'):
        f.unlink()
    for i in range(len(BE)):
        (comp / f'b{i:02d}.html').write_text(beat_scene(i))
    (comp / 'bg.html').write_text(bg())
    (comp / 'chapters.html').write_text(chapters())
    G = list(enumerate(caption_groups()))
    CAPPARTS = []
    per = 40
    for part in range(0, len(G), per):
        chunk = G[part:part + per]
        (comp / f'caps{len(CAPPARTS)}.html').write_text(captions(chunk, len(CAPPARTS)))
        CAPPARTS.append((chunk[0][1][0][1], chunk[-1][1][-1][2]))
    (P / 'index.html').write_text(index())
    (P / 'assets/plan.json').write_text(json.dumps({'dur': DUR, 'provisional': PROVISIONAL, 'chapters': [(S[f"b{i:02d}"][0], t) for i, t in CHAPTERS]}, indent=1))
    print('written', len(BE), 'beats', DUR, 's', 'PROVISIONAL timing' if PROVISIONAL else 'real timing')
