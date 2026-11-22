"""ep02 long video "Will Robots Replace Human Jobs?" (16:9). Reuses the ep01 long-video engine (tools/hf_ep01_long.py)
with EPID=ep02 and adds topic scenes: dark factory, rolling counters, rankings, leaked document, ATM, branches, bars,
QR payment, gauges, task bundle and a subscribe click. Two beats mount HyperFrames registry blocks restyled to the
cream theme (robot-map, comparison-split; sources in hf/fx-lab/compositions).
Usage: THEME=cream GRID=blueprint python3 tools/hf_ep02_long.py"""
import json, math, os, random, re, shutil, sys
from pathlib import Path

os.environ.setdefault('EPID', 'ep02')
sys.path.insert(0, str(Path(__file__).resolve().parent))
import hf_ep01_long as B   # noqa: E402  (module globals now describe ep02)

ROOT, P, BE, S, E = B.ROOT, B.P, B.BE, B.S, B.E
LAB = ROOT / 'hf/fx-lab'

# ------------------------------------------------------------------ icons (extends the house set)
_base_icon = B.icon
EXTRA = {
    'eye': '<path d="M8 50s16-26 42-26 42 26 42 26-16 26-42 26S8 50 8 50z"/><circle cx="50" cy="50" r="12"/>',
    'hand': '<path d="M34 88V46l-10-12c-4-5 3-11 8-6l6 7V18a6 6 0 0 1 12 0v26-30a6 6 0 0 1 12 0v30-24a6 6 0 0 1 12 0v32-18a6 6 0 0 1 12 0v30c0 18-12 30-28 30z"/>',
    'walk': '<circle cx="54" cy="14" r="8"/><path d="M50 28l-10 26 14 10 4 26M46 40l-16 8M50 32l18 14 12-2M40 54l-14 30"/>',
    'box': '<path d="M14 32l36-16 36 16v40L50 88 14 72z"/><path d="M14 32l36 16 36-16M50 48v40"/>',
    'gear': '<circle cx="50" cy="50" r="14"/><path d="M50 10v14M50 76v14M10 50h14M76 50h14M22 22l10 10M68 68l10 10M22 78l10-10M68 32l10-10"/>',
    'tote': '<path d="M18 36h64l-6 50H24z"/><path d="M34 36V24a16 16 0 0 1 32 0v12"/>',
    'robot': '<rect x="22" y="30" width="56" height="44" rx="12"/><path d="M50 30V16"/><circle cx="50" cy="12" r="4"/><circle cx="38" cy="50" r="5"/><circle cx="62" cy="50" r="5"/><path d="M40 62h20M22 52h-8M78 52h8"/>',
    'wrench': '<path d="M62 14a20 20 0 0 0-22 26L14 66a8 8 0 0 0 12 12l26-26a20 20 0 0 0 26-22l-12 12-12-4-4-12z"/>',
    'heart': '<path d="M50 84S12 62 12 36a18 18 0 0 1 38-6 18 18 0 0 1 38 6c0 26-38 48-38 48z"/><path d="M36 48h8l4-8 6 16 4-8h8"/>',
    'bolt': '<path d="M56 8L22 56h24l-6 36 36-50H52z"/>',
    'bank': '<path d="M10 38L50 14l40 24z"/><path d="M18 42v32M38 42v32M62 42v32M82 42v32M10 82h80"/>',
    'cash': '<rect x="10" y="28" width="80" height="44" rx="6"/><circle cx="50" cy="50" r="10"/><path d="M22 40v20M78 40v20"/>',
    'people': '<circle cx="34" cy="34" r="12"/><circle cx="68" cy="38" r="10"/><path d="M12 84c2-18 12-28 22-28s20 10 22 28M54 84c2-14 8-22 14-22s14 8 16 22"/>',
    'tractor': '<circle cx="30" cy="68" r="16"/><circle cx="76" cy="74" r="10"/><path d="M30 52V30h22l8 22h24v14M60 52H46"/>',
    'truck': '<path d="M8 28h52v40H8zM60 42h18l14 14v12H60z"/><circle cx="26" cy="72" r="8"/><circle cx="76" cy="72" r="8"/>',
    'helmet': '<path d="M14 66a36 36 0 0 1 72 0z"/><path d="M8 66h84v10H8zM50 30v20"/>',
    'phone': '<rect x="28" y="8" width="44" height="84" rx="10"/><path d="M44 80h12"/>',
}
def icon(name, size=56, col='#F87736'):
    if name in EXTRA:
        return (f'<svg width="{size}" height="{size}" viewBox="0 0 100 100" fill="none" stroke="{col}" stroke-width="8" '
                f'stroke-linecap="round" stroke-linejoin="round">{EXTRA[name]}</svg>')
    return _base_icon(name, size, col)
B.icon = icon

wf, pop, fly, fade, shake, ring = B.wfrac, B.pop, B.fly, B.fade, B.shake, B.ring
def dur(sid):
    return round(S[sid][1] - S[sid][0], 3)
CARD = 'background:linear-gradient(180deg,#2C1A13,#1F120C); border:2px solid var(--edge); border-radius:30px;'

# ------------------------------------------------------------------ dark factory (beats 0, 1, 14, 50)
def t_factory(i, sid, v):
    mode = v['mode']
    arms = ''
    xs = [230, 620, 1010]
    for k, x0 in enumerate(xs):
        arms += f'''<g id="{sid}-a{k}">
  <rect x="{x0 - 55}" y="470" width="110" height="46" rx="12" fill="#F87736"/>
  <g id="{sid}-u{k}"><rect x="{x0 - 16}" y="285" width="32" height="195" rx="16" fill="#E98F5E"/>
    <g id="{sid}-f{k}"><rect x="{x0}" y="272" width="170" height="28" rx="14" fill="#F87736"/>
      <path d="M{x0 + 168} 266 l26 -14 M{x0 + 168} 306 l26 14" stroke="#F87736" stroke-width="12" stroke-linecap="round"/>
      <circle class="led" cx="{x0 + 186}" cy="286" r="8" fill="#FFE08A"/></g>
    <circle cx="{x0}" cy="286" r="24" fill="#2A1A12"/><circle class="led" cx="{x0}" cy="286" r="9" fill="#FFE08A"/></g>
</g>'''
    lamps = ''.join(f'<div class="lamp" id="{sid}-l{k}" style="left:{180 + k * 380}px"></div>' for k in range(3))
    boxes = ''.join(f'<div class="bx" id="{sid}-b{k}"></div>' for k in range(6))
    extra = ''
    if mode == 'build':
        extra = f'<div class="chip" id="{sid}-chip">{icon("people", 44, "#FF6B5E")}<span>HUMANS INSIDE: 0</span></div>'
    if mode == 'weld':
        extra = ''.join(f'<div class="sp" id="{sid}-s{k}"></div>' for k in range(14)) + f'<div class="cnt" id="{sid}-c">×<span id="{sid}-n">0</span></div><div class="cl" id="{sid}-cl">SAME WELD, AGAIN AND AGAIN</div>'
    if mode == 'call':
        extra = f'<div class="ph" id="{sid}-ph">{icon("phone", 70, "#F6EEE8")}<div><b>3:00 AM</b><span>Robot 3 stopped · call the engineer</span></div></div>'
    body = f'''<div class="room" id="{sid}-room">{lamps}
<svg class="arms" width="1320" height="620" viewBox="0 0 1320 620">{arms}</svg>
<div class="belt" id="{sid}-belt"></div>{boxes}
<div class="dark" id="{sid}-dark"></div>{extra}</div>'''
    css = """.room { position:absolute; left:0; top:20px; width:1320px; height:720px; border-radius:36px; overflow:hidden; background:linear-gradient(180deg,#2C1A13,#1F120C); border:2px solid var(--edge); }
.arms { position:absolute; left:0; top:60px; }
.lamp { position:absolute; top:30px; width:120px; height:40px; border-radius:0 0 60px 60px; background:#FFE9A8; box-shadow:0 30px 120px 40px rgba(255,225,150,.55); }
.belt { position:absolute; left:0; right:0; top:576px; height:46px; background:repeating-linear-gradient(90deg,#3E2217 0 40px,#5C4337 40px 48px); }
.bx { position:absolute; top:530px; left:-120px; width:70px; height:50px; border-radius:8px; background:#E98F5E; border:3px solid #F87736; }
.dark { position:absolute; inset:0; background:#100804; opacity:0; }
.led { filter:drop-shadow(0 0 10px #FFE08A); }
.chip { position:absolute; right:40px; top:40px; display:flex; align-items:center; gap:16px; padding:16px 28px; border-radius:20px; background:#2A0D0A; border:3px solid #FF3B30; font:700 32px 'SD Mono'; color:#FF6B5E; }
.sp { position:absolute; left:836px; top:338px; width:12px; height:12px; border-radius:6px; background:#FFE08A; box-shadow:0 0 18px #FFC24A; opacity:0; }
.cnt { position:absolute; right:60px; top:50px; font:900 120px 'SD Display'; color:#F87736; }
.cl { position:absolute; right:60px; top:190px; font:700 26px 'SD Mono'; letter-spacing:3px; color:#E98F5E; }
.ph { position:absolute; left:360px; top:250px; width:600px; display:flex; align-items:center; gap:28px; padding:30px 36px; border-radius:30px; background:#F87736; box-shadow:0 0 90px rgba(248,119,54,.7); }
.ph b { display:block; font:900 64px 'SD Display'; color:#100804; } .ph span { font:700 28px 'SD Text'; color:#1E120C; }"""
    d = dur(sid)
    sc = [f'    tl.fromTo("#{sid}-room", {{ opacity:0, scale:.94 }}, {{ opacity:1, scale:1, duration:.5, ease:"expo.out" }}, 0.02);']
    for k, x0 in enumerate(xs):
        sc.append(f'    tl.fromTo("#{sid}-u{k}", {{ rotation:-18 }}, {{ rotation:14, duration:{0.9 + k * 0.15:.2f}, ease:"sine.inOut", yoyo:true, repeat:{int(d / 0.9) + 1}, svgOrigin:"{x0} 480" }}, {0.1 + k * 0.2:.2f});')
        sc.append(f'    tl.fromTo("#{sid}-f{k}", {{ rotation:24 }}, {{ rotation:-22, duration:{0.7 + k * 0.1:.2f}, ease:"sine.inOut", yoyo:true, repeat:{int(d / 0.7) + 1}, svgOrigin:"{x0} 286" }}, {0.2 + k * 0.1:.2f});')
    for k in range(6):
        sc.append(f'    tl.fromTo("#{sid}-b{k}", {{ x:0 }}, {{ x:1500, duration:4.2, ease:"none", repeat:{int(d / 4.2) + 1} }}, {round(k * 0.7, 2)});')
    sc.append(f'    tl.fromTo("#{sid}-belt", {{ backgroundPositionX:0 }}, {{ backgroundPositionX:480, duration:{d}, ease:"none" }}, 0);')
    if mode == 'off':
        t = wf(i, 0.62)
        sc += [f'    tl.to("#{sid}-room .lamp", {{ background:"#5C4337", boxShadow:"0 0 0 0 rgba(0,0,0,0)", duration:.08, stagger:.18 }}, {t});',
               f'    tl.to("#{sid}-dark", {{ opacity:.72, duration:.5 }}, {round(t + 0.35, 3)});']
    else:
        sc += [f'    tl.set("#{sid}-room .lamp", {{ background:"#5C4337", boxShadow:"0 0 0 0 rgba(0,0,0,0)" }}, 0);',
               f'    tl.set("#{sid}-dark", {{ opacity:{.55 if mode == "weld" else .72} }}, 0);']
    if mode == 'build':
        sc += [pop(f'#{sid}-chip', wf(i, 0.15)), shake(f'#{sid}-chip', wf(i, 0.2))]
    if mode == 'weld':
        rnd = random.Random(i)
        for k in range(14):
            a = rnd.uniform(-2.6, -0.4); r = rnd.uniform(60, 160); t0 = round(0.4 + (k % 7) * 0.35, 2)
            sc.append(f'    tl.fromTo("#{sid}-s{k}", {{ x:0, y:0, opacity:1 }}, {{ x:{r * math.cos(a):.0f}, y:{r * math.sin(a):.0f}, opacity:0, duration:.45, ease:"power2.out", repeat:{int(d / 2.5)}, repeatDelay:2.0 }}, {t0});')
        sc += [pop(f'#{sid}-c', 0.3), f'    tl.to("#{sid}-n", {{ innerText:9999, snap:{{ innerText:1 }}, duration:{max(1.0, d - 1.0):.2f}, ease:"power1.in" }}, 0.4);', pop(f'#{sid}-cl', 0.6)]
    if mode == 'call':
        sc += [f'    tl.fromTo("#{sid}-ph", {{ opacity:0, y:60, scale:.8 }}, {{ opacity:1, y:0, scale:1, duration:.4, ease:"back.out(2)" }}, {wf(i, 0.62)});',
               f'    tl.fromTo("#{sid}-ph", {{ rotation:-3 }}, {{ rotation:3, duration:.06, yoyo:true, repeat:15, ease:"none", immediateRender:false }}, {round(wf(i, 0.62) + 0.4, 3)});']
    return body, sc, css

# ------------------------------------------------------------------ rolling counter (number wheel, registry idea)
def t_counter(i, sid, v):
    digits = ''
    k = 0
    for ch in v['value']:
        if ch.isdigit():
            n = 10 + int(ch)   # one full spin then land
            strip = ''.join(f'<span>{j % 10}</span>' for j in range(n + 1))
            digits += f'<span class="dg"><span class="st" id="{sid}-d{k}" data-n="{n}">{strip}</span></span>'; k += 1
        else:
            digits += f'<span class="sep">{E(ch)}</span>'
    pre = f'<span class="sep">{E(v.get("prefix", ""))}</span>' if v.get('prefix') else ''
    suf = f'<span class="suf">{E(v.get("suffix", ""))}</span>' if v.get('suffix') else ''
    dots = ''.join(f'<div class="pd" id="{sid}-p{j}"></div>' for j in range(16))
    body = f'''<div class="center kick" id="{sid}-lab" style="top:130px; color:#F87736">{E(v['label'])}</div>
<div class="center num" id="{sid}-num" style="top:220px">{pre}{digits}{suf}</div>
<div class="center csub" id="{sid}-sub" style="top:470px">{v.get('sub', '')}</div>
<div class="center csrc" id="{sid}-src" style="top:640px">{E(v.get('src', ''))}</div>
<div class="band" id="{sid}-band"></div>{dots}'''
    size = 210 if len(v['value']) <= 7 else 170 if len(v['value']) <= 10 else 140
    css = f""".num {{ font:900 {size}px 'SD Display'; color:var(--ink); letter-spacing:-4px; line-height:1; white-space:nowrap; }}
.dg {{ display:inline-block; height:1em; overflow:hidden; vertical-align:top; }} .st {{ display:grid; }} .st span {{ height:1em; line-height:1em; }}
.sep {{ display:inline-block; vertical-align:top; }} .suf {{ font-size:.45em; color:var(--accent); margin-left:12px; vertical-align:top; line-height:2.1; }}
.csub {{ font:600 46px 'SD Text'; color:var(--dim); }} .csub b {{ color:var(--accent); }}
.csrc {{ font:600 22px 'SD Text'; color:var(--dim); letter-spacing:1px; }}
.band {{ position:absolute; top:-200px; left:-600px; width:380px; height:1300px; transform:rotate(18deg); background:linear-gradient(90deg,transparent,rgba(255,240,225,.6),transparent); }}
.pd {{ position:absolute; left:660px; top:330px; width:16px; height:16px; border-radius:8px; background:var(--accent); opacity:0; }}"""
    land = 1.9
    ns = [10 + int(c) for c in v['value'] if c.isdigit()]
    sc = [pop(f'#{sid}-lab', 0.05), f'    tl.fromTo("#{sid}-num", {{ opacity:0, scale:.85 }}, {{ opacity:1, scale:1, duration:.4, ease:"back.out(2)" }}, 0.12);']
    for j in range(k):
        sc.append(f'    tl.fromTo("#{sid}-d{j}", {{ y:0 }}, {{ y:"-{ns[j]}em", duration:{land - 0.2 + j * 0.06:.2f}, ease:"power3.out" }}, 0.2);')
    tl = round(0.2 + land + k * 0.06, 2)
    for j in range(16):
        a = j / 16 * math.tau; r = 360 + (j % 3) * 90
        sc.append(f'    tl.fromTo("#{sid}-p{j}", {{ opacity:1, x:0, y:0, scale:1 }}, {{ opacity:0, x:{r * math.cos(a):.0f}, y:{r * math.sin(a) * .55:.0f}, scale:.3, duration:.9, ease:"power2.out" }}, {tl});')
    sc += [f'    tl.fromTo("#{sid}-num", {{ scale:1 }}, {{ scale:1.06, duration:.12, yoyo:true, repeat:1, immediateRender:false }}, {tl});',
           pop(f'#{sid}-sub', round(tl + 0.1, 2)), pop(f'#{sid}-src', round(tl + 0.3, 2)),
           f'    tl.fromTo("#{sid}-band", {{ x:0 }}, {{ x:2600, duration:1.3, ease:"power2.inOut" }}, {round(tl + 0.2, 2)});']
    return body, sc, css

# ------------------------------------------------------------------ ranked list with custom badges
def t_rank(i, sid, v):
    rows = ''
    for k, (badge, label, kind) in enumerate(v['items']):
        rows += f'<div class="rr {kind}" id="{sid}-r{k}"><b>{E(badge)}</b><span>{E(label)}</span></div>'
    body = f'<div class="center kick" id="{sid}-k" style="top:60px">{E(v["title"])}</div><div class="rk">{rows}</div><div class="center csrc" style="top:680px">{E(v.get("source", ""))}</div>'
    css = """.rk { position:absolute; left:160px; top:140px; width:1000px; }
.rr { height:104px; margin-bottom:18px; border-radius:24px; background:linear-gradient(90deg,#2C1A13,#1F120C); border:2px solid var(--edge); display:flex; align-items:center; gap:26px; padding:0 26px; font:700 44px 'SD Display'; color:var(--ink); }
.rr b { min-width:76px; height:66px; padding:0 14px; border-radius:33px; background:#3A2318; color:var(--accent); display:flex; align-items:center; justify-content:center; font:800 32px 'SD Display'; }
.rr.hi { border:3px solid var(--accent); box-shadow:0 0 50px rgba(248,119,54,.45); } .rr.hi b { background:var(--accent); color:#100804; }
.rr.up b { background:#123524; color:#3DDC97; }
.csrc { font:600 22px 'SD Text'; color:var(--dim); letter-spacing:1px; }"""
    n = len(v['items'])
    sc = [pop(f'#{sid}-k', 0.05)] + [fade(f'#{sid}-r{k}', wf(i, 0.04 + k * 0.7 / n), -120) for k in range(n)]
    for k, it in enumerate(v['items']):
        if it[2] == 'hi':
            sc.append(f'    tl.fromTo("#{sid}-r{k}", {{ scale:1 }}, {{ scale:1.05, duration:.2, yoyo:true, repeat:1, immediateRender:false }}, {wf(i, min(0.85, 0.12 + k * 0.7 / n))});')
    return body, sc, css

# ------------------------------------------------------------------ leaked document with marker highlight
def t_doc(i, sid, v):
    lines = ''.join(f'<div class="dl">{E(x)}</div>' for x in v['lines'])
    body = f'''<div class="card" id="{sid}-card" style="left:170px; top:60px; width:980px; transform:rotate(-1.5deg)">
<div class="hd"><div class="tile">{icon("doc")}</div><div><div class="lab">{E(v['label'])}</div><div class="ttl">{E(v['title'])}</div></div></div>
<div class="paper">{lines}<div class="hl" id="{sid}-hl"><i id="{sid}-mk"></i><span>{E(v['hi'])}</span></div><div class="stamp" id="{sid}-st">{E(v.get('stamp', 'REPORTED'))}</div></div></div>'''
    css = """.paper { background:#FFFFFF; border-radius:20px; padding:34px 44px; min-height:380px; position:relative; }
.dl { font:500 32px 'SD Text'; color:#9A8576; margin:10px 0; } .hl { position:relative; margin-top:40px; font:800 50px 'SD Display'; color:#1E120C; }
.hl i { position:absolute; left:-12px; right:-12px; top:6px; bottom:-4px; background:#FFD166; border-radius:8px; transform:scaleX(0); transform-origin:left; } .hl span { position:relative; }
.stamp { position:absolute; right:40px; top:30px; padding:10px 24px; border:5px solid #FF3B30; border-radius:12px; color:#FF3B30; font:900 40px 'SD Display'; transform:rotate(8deg); opacity:0; }"""
    t = wf(i, 0.55)
    sc = [fly(f'#{sid}-card'), f'    tl.fromTo("#{sid}-mk", {{ scaleX:0 }}, {{ scaleX:1, duration:.45, ease:"power2.out" }}, {t});',
          f'    tl.fromTo("#{sid}-st", {{ opacity:0, scale:2 }}, {{ opacity:1, scale:1, duration:.25, ease:"power4.in" }}, {round(t + 0.4, 3)});']
    return body, sc, css

# ------------------------------------------------------------------ ATM (beats 4, 20) and newspaper headline (21)
def atm_svg(sid):
    return f'''<svg class="atm" id="{sid}-atm" width="360" height="520" viewBox="0 0 360 520">
<rect x="10" y="10" width="340" height="500" rx="34" fill="#F87736"/><rect x="40" y="50" width="280" height="170" rx="16" fill="#100804"/>
<text x="180" y="125" text-anchor="middle" font-family="SD Mono" font-size="30" font-weight="700" fill="#3DDC97" id="{sid}-scr">WELCOME</text>
<text x="180" y="170" text-anchor="middle" font-family="SD Text" font-size="22" fill="#E98F5E">Insert card</text>
<g fill="#FFE2CC">{''.join(f'<rect x="{60 + c * 84}" y="{250 + r * 52}" width="70" height="40" rx="8"/>' for r in range(3) for c in range(3))}</g>
<rect x="70" y="420" width="220" height="22" rx="11" fill="#100804"/></svg>'''
def t_atm(i, sid, v):
    bills = ''.join(f'<div class="bill" id="{sid}-c{k}">₹</div>' for k in range(5))
    q = '<div class="qmk" id="%s-q">?</div>' % sid if v.get('mystery') else ''
    body = f'''<div class="atmw" id="{sid}-w">{atm_svg(sid)}{bills}{q}</div>
<div class="center big" id="{sid}-t" style="top:640px; font-size:92px">{E(v['text'])}</div>'''
    css = """.atmw { position:absolute; left:480px; top:20px; width:360px; height:540px; }
.bill { position:absolute; left:110px; top:420px; width:140px; height:66px; border-radius:10px; background:#3DDC97; border:3px solid #1F8F5F; font:900 40px 'SD Display'; color:#0E3B26; display:flex; align-items:center; justify-content:center; opacity:0; }
.qmk { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font:900 360px 'SD Display'; color:#FFFFFF; background:rgba(16,8,4,.75); border-radius:34px; }"""
    sc = [f'    tl.fromTo("#{sid}-w", {{ opacity:0, y:120, rotation:-6 }}, {{ opacity:1, y:0, rotation:0, duration:.55, ease:"back.out(1.6)" }}, 0.05);']
    if v.get('mystery'):
        sc += [f'    tl.to("#{sid}-q", {{ opacity:0, duration:.35 }}, {wf(i, 0.7)});']
    for k in range(5):
        sc.append(f'    tl.fromTo("#{sid}-c{k}", {{ opacity:0, y:0, x:0, rotation:0 }}, {{ opacity:1, y:{10 + k * 12}, x:{(k - 2) * 80}, rotation:{(k - 2) * 9}, duration:.4, ease:"back.out(2)" }}, {round(wf(i, 0.45) + k * 0.08, 3)});')
    sc.append(f'    tl.fromTo("#{sid}-t", {{ opacity:0, scale:1.4, filter:"blur(12px)" }}, {{ opacity:1, scale:1, filter:"blur(0px)", duration:.35, ease:"expo.out" }}, {wf(i, 0.3)});')
    return body, sc, css

def t_headline(i, sid, v):
    body = f'''<div class="np" id="{sid}-np"><div class="mh">{E(v['paper'])}</div><div class="nh">{E(v['head'])}</div><div class="ns">{E(v['sub'])}</div>
<div class="cols"><i></i><i></i><i></i></div></div>
<div class="atmw" id="{sid}-w" style="left:960px; top:200px; transform:scale(.62); transform-origin:top left">{atm_svg(sid)}</div>'''
    css = """.np { position:absolute; left:60px; top:40px; width:860px; height:640px; background:#FFF8EC; border-radius:10px; padding:40px 46px; box-shadow:0 40px 80px rgba(90,50,20,.25); }
.mh { font:700 24px 'SD Mono'; letter-spacing:4px; color:#8C6B5A; border-bottom:4px double #1E120C; padding-bottom:12px; }
.nh { font:900 84px 'SD Display'; color:#1E120C; line-height:1; margin-top:26px; } .ns { font:600 italic 40px 'SD Serif'; color:#5C4337; margin-top:18px; }
.cols { display:flex; gap:20px; margin-top:28px; } .cols i { flex:1; height:170px; background:repeating-linear-gradient(180deg,#D8C7B5 0 6px,transparent 6px 22px); }
.atmw { position:absolute; width:360px; height:520px; }"""
    sc = [f'    tl.fromTo("#{sid}-np", {{ opacity:0, rotation:-25, scale:.3 }}, {{ opacity:1, rotation:-3, scale:1, duration:.6, ease:"back.out(1.4)" }}, 0.05);',
          f'    tl.fromTo("#{sid}-w", {{ opacity:0, x:200 }}, {{ opacity:1, x:0, duration:.5, ease:"expo.out" }}, {wf(i, 0.45)});']
    return body, sc, css

def t_branches(i, sid, v):
    grid = ''
    for k in range(15):
        r, c = divmod(k, 5)
        grid += f'<div class="br" id="{sid}-g{k}" style="left:{560 + c * 150}px; top:{70 + r * 200}px">{icon("bank", 92)}</div>'
    body = f'''<div class="one" id="{sid}-one">{icon("bank", 200)}<div>1 branch</div></div>{grid}
<div class="arr" id="{sid}-ar">→</div><div class="center cap2" id="{sid}-cap" style="top:660px">Cheaper branches → <span>more branches</span></div>'''
    css = """.one { position:absolute; left:40px; top:120px; width:360px; height:420px; """ + CARD + """ display:flex; flex-direction:column; align-items:center; justify-content:center; gap:20px; font:800 44px 'SD Display'; color:var(--ink); }
.br { position:absolute; width:126px; height:150px; border-radius:24px; background:#1A0F0A; border:2px solid var(--edge); display:flex; align-items:center; justify-content:center; }
.arr { position:absolute; left:420px; top:260px; font:900 110px 'SD Display'; color:var(--accent); }
.cap2 { font:800 50px 'SD Display'; color:var(--ink); } .cap2 span { color:var(--accent); }"""
    sc = [fly(f'#{sid}-one'), pop(f'#{sid}-ar', wf(i, 0.45))]
    for k in range(15):
        sc.append(pop(f'#{sid}-g{k}', round(wf(i, 0.5) + k * 0.06, 3), 30))
    sc.append(pop(f'#{sid}-cap', wf(i, 0.75)))
    return body, sc, css

# ------------------------------------------------------------------ bars, gauges, QR, bundle
def t_bars(i, sid, v):
    bars = v['bars']; mx = max(b[1] for b in bars); n = len(bars); w = 260; gap = 140
    x0 = (1320 - n * w - (n - 1) * gap) // 2
    h = ''
    for k, (lab, val, col, disp) in enumerate(bars):
        hh = round(360 * val / mx)
        h += f'''<div class="bar" id="{sid}-b{k}" style="left:{x0 + k * (w + gap)}px; height:{hh}px; background:{col}"></div>
<div class="bv" id="{sid}-v{k}" style="left:{x0 + k * (w + gap) - 60}px; top:{560 - hh - 80}px; color:{col}">{E(disp)}</div>
<div class="bl" style="left:{x0 + k * (w + gap) - 60}px">{E(lab)}</div>'''
    body = f'<div class="center kick" id="{sid}-k" style="top:30px">{E(v["title"])}</div>{h}<div class="axis"></div><div class="center csrc" style="top:690px">{E(v.get("src", ""))}</div>'
    css = """.bar { position:absolute; bottom:200px; width:260px; border-radius:20px 20px 6px 6px; transform-origin:bottom; box-shadow:0 20px 60px rgba(248,119,54,.25); }
.bv { position:absolute; width:380px; text-align:center; font:900 46px 'SD Display'; white-space:nowrap; }
.bl { position:absolute; top:578px; width:380px; text-align:center; font:700 40px 'SD Display'; color:var(--ink); }
.axis { position:absolute; left:120px; right:120px; top:560px; height:4px; background:var(--edge); }
.csrc { font:600 22px 'SD Text'; color:var(--dim); letter-spacing:1px; }"""
    sc = [pop(f'#{sid}-k', 0.05)]
    for k in range(n):
        t = wf(i, 0.15 + k * 0.4)
        sc += [f'    tl.fromTo("#{sid}-b{k}", {{ scaleY:0 }}, {{ scaleY:1, duration:.7, ease:"expo.out" }}, {t});', pop(f'#{sid}-v{k}', round(t + 0.45, 3))]
    return body, sc, css

def t_gauge(i, sid, v):
    rings = v['rings']; n = len(rings); R = 170; C = round(2 * math.pi * R, 1)
    h = ''
    for k, (pct, lab, col) in enumerate(rings):
        cx = 660 if n == 1 else 360 + k * 600
        h += f'''<svg class="gs" style="left:{cx - 220}px" width="440" height="440" viewBox="0 0 440 440"><circle cx="220" cy="220" r="{R}" fill="none" stroke="#3E2217" stroke-width="44"/>
<circle id="{sid}-c{k}" cx="220" cy="220" r="{R}" fill="none" stroke="{col}" stroke-width="44" stroke-linecap="round" stroke-dasharray="{C}" stroke-dashoffset="{C}" transform="rotate(-90 220 220)"/></svg>
<div class="gp" style="left:{cx - 220}px; color:{col}"><span id="{sid}-n{k}">0</span>%</div><div class="gl" style="left:{cx - 260}px">{E(lab)}</div>'''
    note = f'<div class="gn" id="{sid}-note">{E(v["note"])}</div>' if v.get('note') else ''
    body = f'<div class="center kick" style="top:20px">{E(v["title"])}</div>{h}{note}<div class="center csrc" style="top:690px">{E(v.get("src", ""))}</div>'
    css = """.gs { position:absolute; top:90px; } .gp { position:absolute; top:250px; width:440px; text-align:center; font:900 110px 'SD Display'; }
.gl { position:absolute; top:550px; width:520px; text-align:center; font:700 42px 'SD Display'; color:var(--ink); }
.gn { position:absolute; right:30px; top:110px; padding:18px 30px; border-radius:20px; background:#F87736; color:#100804; font:900 44px 'SD Display'; transform:rotate(4deg); }
.csrc { font:600 22px 'SD Text'; color:var(--dim); letter-spacing:1px; }"""
    sc = []
    for k, (pct, lab, col) in enumerate(rings):
        t = wf(i, 0.1 + k * 0.45)
        sc += [f'    tl.fromTo("#{sid}-c{k}", {{ strokeDashoffset:{C} }}, {{ strokeDashoffset:{round(C * (1 - pct / 100), 1)}, duration:1.1, ease:"power3.out" }}, {t});',
               f'    tl.fromTo("#{sid}-n{k}", {{ innerText:0 }}, {{ innerText:{pct}, snap:{{ innerText:1 }}, duration:1.1, ease:"power3.out" }}, {t});']
    if note:
        sc.append(pop(f'#{sid}-note', wf(i, 0.3)))
    return body, sc, css

def t_qr(i, sid, v):
    rnd = random.Random(7)
    cells = ''.join(f'<rect x="{x * 14}" y="{y * 14}" width="14" height="14"/>' for y in range(21) for x in range(21)
                    if (x < 7 and y < 7) or (x > 13 and y < 7) or (x < 7 and y > 13) or rnd.random() < .45)
    body = f'''<div class="phn" id="{sid}-p"><div class="scr"><svg width="294" height="294" viewBox="0 0 294 294" fill="#100804">{cells}</svg>
<div class="scan" id="{sid}-sc"></div><div class="paid" id="{sid}-ok">{icon("check", 120, "#FFFFFF")}<b>Paid</b><span>No cashier needed</span></div></div></div>
<div class="side" id="{sid}-sd">Scan.<br>Pay.<br><span>Done.</span></div>'''
    css = """.phn { position:absolute; left:250px; top:10px; width:400px; height:720px; border-radius:60px; background:#100804; padding:24px; box-shadow:0 40px 90px rgba(90,50,20,.35); }
.scr { position:relative; width:100%; height:100%; border-radius:40px; background:#FFFFFF; display:flex; align-items:center; justify-content:center; overflow:hidden; }
.scan { position:absolute; left:20px; right:20px; height:6px; top:150px; background:#F87736; box-shadow:0 0 24px #F87736; }
.paid { position:absolute; inset:0; background:#3DDC97; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:10px; opacity:0; }
.paid b { font:900 80px 'SD Display'; color:#fff; } .paid span { font:700 28px 'SD Text'; color:#0E3B26; }
.side { position:absolute; left:760px; top:170px; font:900 110px 'SD Display'; color:var(--ink); line-height:1.05; } .side span { color:var(--accent); }"""
    t = wf(i, 0.55)
    sc = [f'    tl.fromTo("#{sid}-p", {{ opacity:0, y:120, rotation:8 }}, {{ opacity:1, y:0, rotation:0, duration:.55, ease:"back.out(1.5)" }}, 0.05);',
          f'    tl.fromTo("#{sid}-sc", {{ y:0 }}, {{ y:370, duration:.8, ease:"sine.inOut", yoyo:true, repeat:1 }}, 0.4);',
          f'    tl.fromTo("#{sid}-ok", {{ opacity:0, scale:.6 }}, {{ opacity:1, scale:1, duration:.3, ease:"back.out(2)" }}, {t});',
          fade(f'#{sid}-sd', wf(i, 0.25), 80)]
    return body, sc, css

def t_bundle(i, sid, v):
    chips = ''.join(f'<div class="tk{" au" if a else ""}" id="{sid}-t{k}">{E(t)}</div>' for k, (t, a) in enumerate(v['tasks']))
    body = f'''<div class="job" id="{sid}-job"><div class="jt">YOUR JOB</div>{chips}</div>
<div class="bot" id="{sid}-bot">{icon("robot", 150)}<div>Takes the predictable</div></div>
<div class="keep" id="{sid}-keep">You keep the messy, human part</div>'''
    css = """.job { position:absolute; left:40px; top:40px; width:640px; padding:30px; """ + CARD + """ }
.jt { font:700 26px 'SD Mono'; letter-spacing:4px; color:var(--accent); margin-bottom:16px; }
.tk { height:84px; margin:12px 0; border-radius:20px; background:#F3E6DC; color:#1E120C; display:flex; align-items:center; padding:0 28px; font:800 38px 'SD Display'; }
.bot { position:absolute; left:900px; top:120px; width:360px; height:360px; """ + CARD + """ display:flex; flex-direction:column; align-items:center; justify-content:center; gap:14px; font:700 32px 'SD Display'; color:var(--ink); text-align:center; }
.keep { position:absolute; left:40px; top:640px; width:1240px; text-align:center; font:900 56px 'SD Display'; color:var(--accent); }"""
    sc = [fly(f'#{sid}-job')] + [fade(f'#{sid}-t{k}', round(0.15 + k * 0.08, 2), -60) for k in range(len(v['tasks']))] + [fly(f'#{sid}-bot', wf(i, 0.2), 10, -20)]
    t = wf(i, 0.45)
    for k, (_, a) in enumerate(v['tasks']):
        if a:
            sc.append(f'    tl.to("#{sid}-t{k}", {{ x:820, y:{140 - k * 60}, scale:.5, opacity:0, duration:.6, ease:"power3.in" }}, {round(t + k * 0.15, 3)});')
    sc += [f'    tl.to("#{sid}-job .tk:not(.au)", {{ background:"#3DDC97", color:"#0E3B26", duration:.3, stagger:.1 }}, {wf(i, 0.75)});', pop(f'#{sid}-keep', wf(i, 0.8))]
    return body, sc, css

# ------------------------------------------------------------------ overrides of house templates
def t_icons(i, sid, v):
    items = v['items']; n = len(items); w = 300 if n > 3 else 340
    cards = ''.join(f'<div class="ib" id="{sid}-c{k}" style="width:{w}px"><div class="it">{icon(it["icon"], 90)}</div><div>{E(it["label"])}</div></div>' for k, it in enumerate(items))
    title = f'<div class="center kick" id="{sid}-k" style="top:70px">{E(v["title"])}</div>' if v.get('title') else ''
    body = f'{title}<div class="row">{cards}</div>'
    css = """.row { position:absolute; left:0; right:0; top:200px; display:flex; gap:30px; justify-content:center; }
.ib { height:360px; """ + CARD + """ display:flex; flex-direction:column; align-items:center; justify-content:center; gap:26px; font:700 40px 'SD Display'; color:var(--ink); text-align:center; padding:0 20px; }
.it { width:150px; height:150px; border-radius:36px; background:#F3E6DC; display:flex; align-items:center; justify-content:center; }"""
    sc = ([pop(f'#{sid}-k', 0.05)] if title else []) + [pop(f'#{sid}-c{k}', wf(i, 0.05 + k / n * 0.75)) for k in range(n)]
    return body, sc, css

def t_shift(i, sid, v):
    body = f"""<div class="sb" id="{sid}-a" style="left:60px">{icon('cash', 90)}<div>{E(v['from'])}</div></div>
<div class="arrow" id="{sid}-ar">→</div>
<div class="sb hot" id="{sid}-b" style="left:800px">{icon('people', 90)}<div>{E(v['to'])}</div></div>
<div class="center tagl" id="{sid}-t" style="top:600px">{E(v['tag'])}</div>"""
    css = """.sb { position:absolute; top:150px; width:460px; height:340px; """ + CARD + """ display:flex; flex-direction:column; align-items:center; justify-content:center; gap:24px; font:800 48px 'SD Display'; color:var(--ink); text-align:center; }
.sb.hot { border:3px solid var(--accent); box-shadow:0 0 60px rgba(248,119,54,.35); }
.arrow { position:absolute; left:590px; top:250px; font:900 120px 'SD Display'; color:var(--accent); }
.tagl { font:600 italic 56px 'SD Serif'; color:var(--accent-soft); }"""
    sc = [fly(f'#{sid}-a'), f'    tl.to("#{sid}-a", {{ opacity:.45, scale:.92, duration:.4 }}, {wf(i, 0.4)});', pop(f'#{sid}-ar', wf(i, 0.3)), fly(f'#{sid}-b', wf(i, 0.35)), pop(f'#{sid}-t', wf(i, 0.65))]
    return body, sc, css

def t_end(i, sid, v):
    body = f"""<div class="center big" id="{sid}-t" style="top:200px"><span class="acc">TECH</span>DECODED</div>
<div class="center es" id="{sid}-s" style="top:340px">with Max · {E(v['sub'])}</div>
<div class="sub" id="{sid}-b"><span id="{sid}-bt">SUBSCRIBE</span></div><div class="bell" id="{sid}-bell">🔔</div>
<svg class="cur" id="{sid}-cur" width="70" height="90" viewBox="0 0 70 90"><path d="M6 4l56 44-26 4 14 30-12 6-14-30-18 18z" fill="#FFFFFF" stroke="#100804" stroke-width="5" stroke-linejoin="round"/></svg>"""
    css = """.es { font:600 italic 56px 'SD Serif'; color:var(--accent-soft); }
.sub { position:absolute; left:470px; top:480px; width:380px; height:110px; border-radius:55px; background:#FF3B30; color:#fff; font:900 46px 'SD Display'; display:flex; align-items:center; justify-content:center; letter-spacing:2px; }
.bell { position:absolute; left:880px; top:490px; font-size:80px; }
.cur { position:absolute; left:900px; top:700px; }"""
    tc = wf(i, 0.7)
    sc = [f'    tl.fromTo("#{sid}-t", {{ opacity:0, scale:1.4, filter:"blur(14px)" }}, {{ opacity:1, scale:1, filter:"blur(0px)", duration:.4, ease:"expo.out" }}, 0.05);',
          pop(f'#{sid}-s', 0.35), pop(f'#{sid}-b', 0.6), pop(f'#{sid}-bell', 0.75),
          f'    tl.fromTo("#{sid}-cur", {{ x:300, y:200, opacity:0 }}, {{ x:-240, y:-150, opacity:1, duration:.7, ease:"power2.inOut" }}, {round(tc - 0.7, 3)});',
          f'    tl.fromTo("#{sid}-b", {{ scale:1 }}, {{ scale:.9, duration:.08, yoyo:true, repeat:1, immediateRender:false }}, {tc});',
          f'    tl.to("#{sid}-b", {{ backgroundColor:"#8C6B5A", duration:.15 }}, {round(tc + 0.1, 3)});',
          f'    tl.set("#{sid}-bt", {{ innerText:"SUBSCRIBED ✓" }}, {round(tc + 0.1, 3)});',
          f'    tl.fromTo("#{sid}-bell", {{ rotation:-18 }}, {{ rotation:18, duration:.09, yoyo:true, repeat:9, ease:"none", transformOrigin:"50% 10%", immediateRender:false }}, {round(tc + 0.35, 3)});']
    return body, sc, css

B.T.update({'factory': t_factory, 'counter': t_counter, 'rank': t_rank, 'doc': t_doc, 'atm': t_atm, 'headline': t_headline,
            'branches': t_branches, 'bars': t_bars, 'gauge': t_gauge, 'qr': t_qr, 'bundle': t_bundle, 'icons': t_icons,
            'shift': t_shift, 'end': t_end, 'block': lambda i, sid, v: ('', [], '')})
B.SFX_BY_TYPE.update({'factory': [(0.05, 'hum', .45)], 'counter': [(0.15, 'tick2', .45), (2.1, 'impact', .55)], 'rank': [(0.1, 'whoosh', .45)],
                      'doc': [(0.05, 'flip', .5)], 'atm': [(0.05, 'whoosh', .5)], 'headline': [(0.05, 'flip', .55)], 'branches': [(0.1, 'pop', .45)],
                      'bars': [(0.2, 'riser', .4)], 'gauge': [(0.15, 'servo', .4)], 'qr': [(0.1, 'ping', .5)], 'bundle': [(0.1, 'whoosh', .45)],
                      'block': [(0.05, 'whoosh', .5)], 'end': [(0.1, 'riser', .5), (0.6, 'ding', .6)]})

# ------------------------------------------------------------------ registry blocks restyled for this video
BLOCKS = {'map': ('robot-map', 'compositions/robot-map.html'),
          'compare': ('comparison-split', 'compositions/components/comparison-split.html')}

def prepare_blocks():
    (P / 'compositions/components').mkdir(parents=True, exist_ok=True)
    m = (LAB / 'compositions/robot-map.html').read_text()
    m = m.replace('top: 48px;', 'top: 120px;', 1).replace('top: 150px;', 'top: 214px;', 1)
    m = m.replace('top: 170px;\n        left: 80px;', 'top: 250px;\n        left: 270px;', 1)
    m = re.sub(r'(#robot-map \.legend-group \{)', r'\1 display:none !important;', m)
    (P / 'compositions/robot-map.html').write_text(m)
    cs = (LAB / 'compositions/components/comparison-split.html').read_text()
    ci = next(i for i, b in enumerate(BE) if b['v'].get('block') == 'compare')
    cd = dur(f'b{ci:02d}')
    cs = cs.replace('data-duration="4"', f'data-duration="{cd}"')
    cs = cs.replace('parseFloat(root.dataset.duration || "4")', str(cd))      # the mount strips the root's data-duration
    cs = cs.replace('top: var(--space-3, 4cqh);', 'top: 12cqh;', 1)          # clear of the chapter pill
    (P / 'compositions/components/comparison-split.html').write_text(cs)
    for a in ('d3.min.js', 'topojson-client.min.js', 'countries-110m.json'):
        shutil.copy(LAB / 'assets' / a, P / 'assets' / a)

def patch_index(html):
    for i, b in enumerate(BE):
        if b['v']['type'] != 'block':
            continue
        sid = f'b{i:02d}'; cid, src = BLOCKS[b['v']['block']]
        vals = ''
        if cid == 'comparison-split':
            vals = """ data-variable-values='{"labelA":"Easy for humans","labelB":"Hard for humans"}'"""
        html = re.sub(rf'<div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html"',
                      f'<div id="{sid}" data-composition-id="{cid}" data-composition-src="{src}"{vals}', html)
    html = html.replace('#root { position:relative; width:100%; height:100%; }',
                        "#root { position:relative; width:100%; height:100%; --bg:#F4EDE3; --surface:#FFFAF7; --fg:#2A2018; --border:#EADCCD; --muted:#E6D8C8; --accent:#F87736; --brand:#F87736; --accent-2:#E98F5E; --font-body:'SD Text'; }")
    return html

if __name__ == '__main__':
    comp = P / 'compositions'; comp.mkdir(parents=True, exist_ok=True)
    for f in comp.glob('*.html'):
        f.unlink()
    prepare_blocks()
    for i in range(len(BE)):
        if BE[i]['v']['type'] != 'block':
            (comp / f'b{i:02d}.html').write_text(B.beat_scene(i))
    (comp / 'bg.html').write_text(B.bg())
    (comp / 'chapters.html').write_text(B.chapters())
    G = list(enumerate(B.caption_groups()))
    B.CAPPARTS = []
    for part in range(0, len(G), 40):
        chunk = G[part:part + 40]
        (comp / f'caps{len(B.CAPPARTS)}.html').write_text(B.captions(chunk, len(B.CAPPARTS)))
        B.CAPPARTS.append((chunk[0][1][0][1], chunk[-1][1][-1][2]))
    (P / 'index.html').write_text(patch_index(B.index()))
    (P / 'assets/plan.json').write_text(json.dumps({'dur': B.DUR, 'provisional': B.PROVISIONAL,
                                                     'chapters': [(S[f"b{i:02d}"][0], t) for i, t in B.CHAPTERS]}, indent=1))
    print('written', len(BE), 'beats', B.DUR, 's', 'PROVISIONAL timing' if B.PROVISIONAL else 'real timing')
