"""Explainer Shorts (Nov 2026): sat01 GPS, goog01 Google search, net01 internet outage, robo01 dark factories.
Each topic has its own card designs, motion and sound palette; real photos (Wikimedia Commons, credited) are used
when present in tech-studio/assets_img/, with drawn fallbacks otherwise.
Usage: THEME=cream GRID=<pattern> python3 tools/hf_explainers.py sat01|goog01|net01|robo01"""
import json, math, os, shutil, sys
from pathlib import Path
K = sys.argv[1]
os.environ['SHORT_ID'] = f'{K}-short'
sys.path.insert(0, str(Path(__file__).resolve().parent))
import hf_news01_short as L
from hf_news01_short import S, wl, fly, pop, slam, shake, ring, out, icon, bit, bit_on, bit_float, scene, E

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / 'assets_img'
CREDITS = json.loads((IMG / 'credits.json').read_text()) if (IMG / 'credits.json').exists() else {}
USED = {}

def photo(name, fallback, w, h, extra=''):
    """real photo in a framed card (Ken-Burns ready) or a drawn fallback."""
    src = IMG / name
    if src.exists():
        (L.P / 'assets/img').mkdir(parents=True, exist_ok=True)
        shutil.copy(src, L.P / 'assets/img' / name)
        USED[name] = CREDITS.get(name, {})
        return f'<div class="ph" style="width:{w}px; height:{h}px;{extra}"><img src="assets/img/{name}" class="kb"/></div>'
    return f'<div class="ph fb" style="width:{w}px; height:{h}px;{extra}">{fallback}</div>'

BASE = """.center { position:absolute; left:40px; right:40px; text-align:center; }
.kk { font:600 32px 'SD Text'; letter-spacing:4px; color:var(--dim); }
.big { font:900 180px 'SD Display'; color:var(--accent); letter-spacing:-4px; line-height:1; }
.box { position:absolute; border-radius:36px; border:2px solid #3E2217; background:linear-gradient(180deg,#2C1A13,#1F120C); box-shadow:0 30px 70px rgba(0,0,0,.35); }
.src { position:absolute; left:96px; font:600 22px 'SD Text'; letter-spacing:2px; color:var(--dim); }
.ph { position:relative; border-radius:28px; overflow:hidden; border:8px solid #FFFFFF; box-shadow:0 30px 70px rgba(0,0,0,.35); background:#1A0F0A; }
.ph img { width:100%; height:100%; object-fit:cover; display:block; } .ph.fb { display:flex; align-items:center; justify-content:center; }
.chip { display:inline-flex; align-items:center; gap:12px; padding:16px 26px; border-radius:24px; background:#F3E6DC; color:#1E120C; font:800 38px 'SD Display'; }
.hl { color:var(--accent); }"""

def kb(sel, d):
    return f'    tl.fromTo("{sel} .kb", {{ scale:1 }}, {{ scale:1.1, duration:{d}, ease:"none" }}, 0);'
def steps(sel, t0, vals, dt=0.07):
    return [f'    tl.set("{sel}", {{ textContent:"{v}" }}, {round(t0 + k * dt, 3)});' for k, v in enumerate(vals)]
def dur(sid): return round(S[sid][1] - S[sid][0], 3)
def sc_join(sid, sc): return '\n'.join([L.punch(sid)] + sc)
def subscribe_scene(i):
    sid = f's{i}'
    body, sc, css, tc = L.subscribe(sid, wl(i, 'subscribe'), bit(sid, [('n', {'state': 'happy', 'arms': 'wave'})]))
    return scene(sid, body, sc_join(sid, sc + bit_on(sid, 'n', 0, False) + bit_float(sid)), BASE + css), tc

SAT_SVG = '<svg width="{w}" height="{h}" viewBox="0 0 200 120"><rect x="80" y="40" width="40" height="40" rx="6" fill="#D8C4B4"/><rect x="10" y="48" width="64" height="24" fill="#2F5FA8"/><rect x="126" y="48" width="64" height="24" fill="#2F5FA8"/><path d="M10 60h64M126 60h64M22 48v24M34 48v24M46 48v24M58 48v24M138 48v24M150 48v24M162 48v24M174 48v24" stroke="#9CC3FF" stroke-width="1.5"/><circle cx="100" cy="30" r="6" fill="#F87736"/><path d="M100 36v4" stroke="#D8C4B4" stroke-width="3"/></svg>'
def sat_svg(w=200, h=120): return SAT_SVG.format(w=w, h=h)
PHONE = '<svg width="{w}" height="{h}" viewBox="0 0 120 220"><rect x="4" y="4" width="112" height="212" rx="22" fill="#1A0F0A" stroke="#3E2217" stroke-width="4"/><rect x="14" y="26" width="92" height="168" rx="10" fill="#EAF3FF"/><path d="M14 90 L106 70 M14 140 L106 120 M40 26 L60 194 M80 26 L90 194" stroke="#C9DCF5" stroke-width="5"/>{dot}</svg>'
def phone(w=240, h=440, dot=True):
    d = '<circle cx="60" cy="110" r="22" fill="#1C7ED6" opacity=".25"/><circle cx="60" cy="110" r="10" fill="#1C7ED6" stroke="#fff" stroke-width="4"/>' if dot else ''
    return PHONE.format(w=w, h=h, dot=d)

# ============================================================== sat01: GPS
def sat():
    out_ = []
    sid = 's0'; t_n, t_ph = wl(0, 'no'), wl(0, 'phone')
    body = f"""<div class="sat0" id="{sid}-sat">{photo('gps_sat.jpg', sat_svg(360, 220), 420, 330)}<div class="qb" id="{sid}-q">?</div></div>
<div class="ph0" id="{sid}-ph">{phone(280, 510)}<div class="pulse" id="{sid}-pl"></div></div>
<div class="center lab0" id="{sid}-t">THE SATELLITE DOESN'T KNOW.<br><span class="hl">YOUR PHONE DOES.</span></div>"""
    css = BASE + """.sat0 { position:absolute; left:80px; top:300px; } .qb { position:absolute; right:-40px; top:-40px; width:120px; height:120px; border-radius:60px; background:#FF3B30; color:#fff; font:900 90px 'SD Display'; display:flex; align-items:center; justify-content:center; opacity:0; }
.ph0 { position:absolute; left:680px; top:560px; } .pulse { position:absolute; left:110px; top:220px; width:60px; height:60px; margin:-30px; border-radius:50%; border:6px solid #1C7ED6; opacity:0; }
.lab0 { top:1110px; font:900 52px 'SD Display'; color:var(--ink); line-height:1.1; opacity:0; }"""
    sc = [fly(f'#{sid}-sat', 0.02), kb(f'#{sid}-sat', dur(sid)), slam(f'#{sid}-q', t_n), fly(f'#{sid}-ph', t_ph - 0.4, 10, -20),
          f'    tl.fromTo("#{sid}-pl", {{ opacity:1, scale:.5 }}, {{ opacity:0, scale:3.5, duration:1, repeat:3, ease:"power2.out", immediateRender:false }}, {t_ph});',
          pop(f'#{sid}-t', t_ph + 0.2), out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    # s1 globe + orbits
    sid = 's1'; t_k = wl(1, 'twenty')
    earth = photo('earth.jpg', '<div class="eg"></div>', 520, 520, ' border-radius:50%;')
    sats = ''.join(f'<div class="os" id="{sid}-o{k}">{sat_svg(90, 54)}</div>' for k in range(6))
    body = f"""<div class="center kk" style="top:330px">THE GPS CONSTELLATION</div><div class="globe">{earth}</div>
<svg class="orb" width="1000" height="900" viewBox="0 0 1000 900"><ellipse cx="500" cy="450" rx="430" ry="170" fill="none" stroke="#F87736" stroke-opacity=".5" stroke-width="3" stroke-dasharray="10 10" transform="rotate(-20 500 450)"/><ellipse cx="500" cy="450" rx="430" ry="170" fill="none" stroke="#F87736" stroke-opacity=".5" stroke-width="3" stroke-dasharray="10 10" transform="rotate(25 500 450)"/><ellipse cx="500" cy="450" rx="200" ry="430" fill="none" stroke="#F87736" stroke-opacity=".4" stroke-width="3" stroke-dasharray="10 10"/></svg>
{sats}<div class="center st1" id="{sid}-st"><span class="chip">~30 satellites</span> <span class="chip">~20,000 km up</span></div>"""
    css = BASE + """.globe { position:absolute; left:280px; top:470px; } .eg { width:100%; height:100%; background:radial-gradient(circle at 35% 35%, #7FB7FF, #1C4E9A 60%, #0B2554); }
.orb { position:absolute; left:40px; top:280px; } .os { position:absolute; left:0; top:0; } .st1 { top:1110px; opacity:0; } .st1 .chip { margin:0 8px; }"""
    sc = [pop('.globe', 0.02), kb('.globe', dur(sid))]
    d = dur(sid)
    for k in range(6):
        a0 = k * 60; pts = []
        for j in range(5):
            a = math.radians(a0 + j * 30); rx, ry, rot = (430, 170, -20) if k % 2 == 0 else (430, 170, 25)
            x, y = rx * math.cos(a), ry * math.sin(a); r = math.radians(rot)
            pts.append((540 + x * math.cos(r) - y * math.sin(r) - 45, 730 + x * math.sin(r) + y * math.cos(r) - 27))
        kf = ','.join(f'{{ x:{round(x)}, y:{round(y)}, duration:{round(d / 4, 2)} }}' for x, y in pts[1:])
        sc += [f'    tl.set("#{sid}-o{k}", {{ x:{round(pts[0][0])}, y:{round(pts[0][1])} }}, 0);', f'    tl.to("#{sid}-o{k}", {{ keyframes:[{kf}], ease:"none" }}, 0);']
    sc += [pop(f'#{sid}-st', t_k - 0.3), out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    # s2 broadcast: position + time
    sid = 's2'; t_tr, t_wh, t_ti = wl(2, 'track'), wl(2, 'where'), wl(2, 'time')
    rings = ''.join(f'<div class="rp" id="{sid}-r{k}"></div>' for k in range(4))
    body = f"""<div class="center sat2">{photo('gps_sat.jpg', sat_svg(360, 220), 440, 330)}</div>{rings}
<div class="nt" id="{sid}-nt"><s>TRACKS YOU</s></div>
<div class="dc" id="{sid}-a" style="left:110px">📍<b>POSITION</b><span>orbit data</span></div>
<div class="dc" id="{sid}-b" style="left:560px">🕒<b>TIME</b><span id="{sid}-clk">12:00:00.000000</span></div>"""
    css = BASE + """.sat2 { top:300px; display:flex; justify-content:center; } .rp { position:absolute; left:540px; top:470px; width:200px; height:200px; margin:-100px; border-radius:50%; border:5px solid #F87736; opacity:0; }
.nt { position:absolute; left:0; right:0; text-align:center; top:690px; font:900 64px 'SD Display'; color:var(--red); opacity:0; }
.dc { position:absolute; top:820px; width:410px; height:250px; border-radius:30px; border:3px solid var(--accent); background:linear-gradient(180deg,#2C1A13,#1F120C); display:flex; flex-direction:column; align-items:center; justify-content:center; gap:6px; font-size:60px; opacity:0; }
.dc b { font:900 54px 'SD Display'; color:var(--ink); } .dc span { font:700 30px 'SD Mono'; color:var(--accent); }"""
    sc = [pop('.sat2', 0.02), kb('.sat2', dur(sid))]
    sc += [f'    tl.fromTo("#{sid}-r{k}", {{ opacity:.9, scale:.6 }}, {{ opacity:0, scale:5, duration:1.6, repeat:3, ease:"power1.out", immediateRender:false }}, {round(0.2 + k * 0.4, 2)});' for k in range(4)]
    sc += [slam(f'#{sid}-nt', t_tr - 0.1), f'    tl.to("#{sid}-nt", {{ opacity:0, duration:.2 }}, {t_wh - 0.4});', pop(f'#{sid}-a', t_wh - 0.1), pop(f'#{sid}-b', t_ti - 0.2)]
    sc += steps(f'#{sid}-clk', t_ti, [f'12:00:0{k}.{k * 137:06d}' for k in range(1, 8)], 0.25) + [out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    # s3 signal travel + stopwatch
    sid = 's3'; t_l, t_fr = wl(3, 'listens'), wl(3, 'fraction')
    body = f"""<div class="s3s">{sat_svg(300, 180)}</div><div class="beam" id="{sid}-bm"></div><div class="pk" id="{sid}-pk"></div>
<div class="s3p">{phone(220, 400)}</div>
<div class="sw" id="{sid}-sw"><div class="kk">SIGNAL TRAVEL TIME</div><div class="swn" id="{sid}-n">0.000 s</div><div class="swl">≈ 20,000 km at light speed</div></div>"""
    css = BASE + """.s3s { position:absolute; left:120px; top:300px; } .s3p { position:absolute; left:130px; top:880px; }
.beam { position:absolute; left:265px; top:420px; width:8px; height:480px; background:repeating-linear-gradient(180deg,#F87736 0 18px,transparent 18px 34px); opacity:.6; }
.pk { position:absolute; left:250px; top:420px; width:38px; height:38px; border-radius:19px; background:#F87736; box-shadow:0 0 30px #F87736; opacity:0; }
.sw { position:absolute; left:470px; top:560px; width:520px; padding:40px; border-radius:36px; border:4px solid var(--accent); background:linear-gradient(180deg,#2C1A13,#1F120C); text-align:center; opacity:0; }
.swn { font:900 84px 'SD Mono'; white-space:nowrap; color:var(--ink); } .swl { font:700 32px 'SD Text'; color:#CDB8AA; }"""
    sc = [pop('.s3s', 0.02), pop('.s3p', 0.1),
          f'    tl.fromTo("#{sid}-pk", {{ opacity:1, y:0 }}, {{ y:460, duration:.8, repeat:2, ease:"power1.in", immediateRender:false }}, {t_l});',
          pop(f'#{sid}-sw', t_fr - 0.6)] + steps(f'#{sid}-n', t_fr - 0.4, ['0.011 s', '0.023 s', '0.034 s', '0.045 s', '0.056 s', '0.067 s'], 0.08) + [out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    # s4 formula
    sid = 's4'; t_m, t_sp, t_ds = wl(4, 'multiply'), wl(4, 'speed'), wl(4, 'distance')
    body = f"""<div class="center kk" style="top:380px">THE MATH YOUR PHONE DOES</div>
<div class="fr"><div class="tm" id="{sid}-a"><b>0.067 s</b><span>delay</span></div><div class="op" id="{sid}-x">×</div><div class="tm" id="{sid}-b"><b>300,000 km/s</b><span>speed of light</span></div>
<div class="op" id="{sid}-e">=</div><div class="tm res" id="{sid}-c"><b>~20,000 km</b><span>your distance</span></div></div>"""
    css = BASE + """.fr { position:absolute; left:90px; right:90px; top:430px; display:flex; flex-direction:column; align-items:center; gap:8px; }
.tm { width:760px; padding:18px; border-radius:30px; border:2px solid #3E2217; background:linear-gradient(180deg,#2C1A13,#1F120C); text-align:center; opacity:0; }
.tm b { display:block; font:900 66px 'SD Mono'; color:var(--ink); } .tm span { font:700 32px 'SD Text'; color:#CDB8AA; } .tm.res { border:4px solid var(--accent); } .tm.res b { color:var(--accent); }
.op { font:900 56px 'SD Display'; color:var(--accent); opacity:0; line-height:1; }"""
    sc = [pop(f'#{sid}-a', max(0.05, t_m - 0.3)), pop(f'#{sid}-x', t_m), pop(f'#{sid}-b', t_sp - 0.2), pop(f'#{sid}-e', t_ds - 0.5), slam(f'#{sid}-c', t_ds - 0.2), out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    # s5 trilateration
    sid = 's5'; t1, t3, t4 = wl(5, 'one'), wl(5, 'three'), wl(5, 'fourth')
    C = [(330, 640, 330), (760, 600, 300), (560, 1010, 260)]
    circ = ''.join(f'<circle id="{sid}-c{k}" cx="{x}" cy="{y}" r="{r}" fill="rgba(248,119,54,.08)" stroke="#F87736" stroke-width="5" style="transform-origin:{x}px {y}px"/><g id="{sid}-g{k}"><circle cx="{x}" cy="{y}" r="16" fill="#2F5FA8"/></g>' for k, (x, y, r) in enumerate(C))
    body = f"""<svg class="tri" width="1080" height="1400" viewBox="0 0 1080 1400">{circ}</svg><div class="you" id="{sid}-y">YOU</div>
<div class="clk" id="{sid}-k">🕒 4th satellite: clock synced</div>"""
    css = BASE + """.tri { position:absolute; left:0; top:0; } .you { position:absolute; left:500px; top:690px; padding:12px 22px; border-radius:18px; background:#1C7ED6; color:#fff; font:900 40px 'SD Display'; opacity:0; }
.clk { position:absolute; left:120px; right:120px; top:1110px; text-align:center; padding:20px; border-radius:24px; background:#F3E6DC; color:#1E120C; font:800 40px 'SD Display'; opacity:0; }"""
    ts = [t1, (t1 + t3) / 2, t3]
    sc = [f'    tl.fromTo("#{sid}-c{k}", {{ scale:0 }}, {{ scale:1, duration:.6, ease:"power3.out" }}, {round(ts[k], 3)});' for k in range(3)]
    sc += [f'    tl.fromTo("#{sid}-g{k}", {{ opacity:0 }}, {{ opacity:1, duration:.2 }}, {round(ts[k], 3)});' for k in range(3)]
    sc += [slam(f'#{sid}-y', t3 + 0.6), pop(f'#{sid}-k', t4 - 0.2), out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    # s6 relativity clocks
    sid = 's6'; t_e, t_38 = wl(6, 'einstein'), wl(6, 'thirtyeight')
    def clock(cid, label, col):
        return f'<div class="ck"><svg width="300" height="300" viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="#FFFAF7" stroke="{col}" stroke-width="5"/><path d="M50 10v6M50 84v6M10 50h6M84 50h6" stroke="#8C6B5A" stroke-width="3"/><line id="{cid}" x1="50" y1="50" x2="50" y2="14" stroke="{col}" stroke-width="4" stroke-linecap="round" style="transform-origin:50px 50px"/><circle cx="50" cy="50" r="4" fill="{col}"/></svg><b>{label}</b></div>'
    body = f"""<div class="center kk" style="top:330px">RELATIVITY IS REAL</div>
<div class="cks">{clock(f'{sid}-h1', 'On the ground', '#8C6B5A')}{clock(f'{sid}-h2', 'In orbit', '#F87736')}</div>
<div class="center d38" id="{sid}-d">+38 µs <span>per day, faster</span></div><div class="src" style="top:1150px">SOURCE: N. ASHBY, PHYSICS TODAY (2002)</div>"""
    css = BASE + """.cks { position:absolute; left:80px; right:80px; top:420px; display:flex; justify-content:space-around; } .ck { text-align:center; } .ck b { display:block; font:800 40px 'SD Display'; color:var(--ink); margin-top:10px; }
.d38 { top:900px; font:900 120px 'SD Display'; color:var(--accent); opacity:0; } .d38 span { display:block; font:700 40px 'SD Text'; color:var(--ink); }"""
    sc = [pop('.cks', 0.02), f'    tl.fromTo("#{sid}-h1", {{ rotation:0 }}, {{ rotation:{int(dur(sid) * 60)}, duration:{dur(sid)}, ease:"none" }}, 0);',
          f'    tl.fromTo("#{sid}-h2", {{ rotation:0 }}, {{ rotation:{int(dur(sid) * 75)}, duration:{dur(sid)}, ease:"none" }}, 0);', slam(f'#{sid}-d', t_38 - 0.1), out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    # s7 drifting pin on map
    sid = 's7'; t_dr, t_11 = wl(7, 'drift'), wl(7, 'eleven')
    body = f"""<div class="box map" style="left:90px; top:330px; width:900px; height:760px;"><svg width="900" height="760"><path d="M0 200 L900 140 M0 520 L900 440 M240 0 L300 760 M620 0 L680 760" stroke="#E6D9CE" stroke-width="26"/><path d="M0 200 L900 140 M0 520 L900 440 M240 0 L300 760 M620 0 L680 760" stroke="#FFFFFF" stroke-width="4" stroke-dasharray="20 20"/>
<path id="{sid}-tr" d="M280 360 C420 300 560 420 760 300" fill="none" stroke="#FF3B30" stroke-width="8" stroke-dasharray="16 12" pathLength="1" style="stroke-dashoffset:1"/></svg>
<div class="pin" id="{sid}-pin">📍</div><div class="real">YOU ARE HERE</div></div><div class="center km" id="{sid}-k">+11 KM</div>"""
    css = BASE + """.map { background:#F3EDE4; overflow:hidden; } .pin { position:absolute; left:250px; top:290px; font-size:80px; } .real { position:absolute; left:200px; top:400px; font:800 26px 'SD Text'; color:#1C7ED6; }
.km { top:1120px; font:900 110px 'SD Display'; color:var(--red); opacity:0; }"""
    sc = [fly('.map', 0.02), f'    tl.to("#{sid}-pin", {{ x:480, y:-60, duration:1.6, ease:"power1.in" }}, {t_dr});',
          f'    tl.to("#{sid}-tr", {{ strokeDashoffset:0, duration:1.6, ease:"power1.in" }}, {t_dr});', slam(f'#{sid}-k', t_11 - 0.1), out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    # s8 payoff
    sid = 's8'; t_c, t_g = wl(8, 'clocks'), wl(8, 'genius')
    body = f"""<div class="pp">{phone(380, 700)}<div class="lk" id="{sid}-l">LOCKED ✓</div></div>
<div class="center pay" id="{sid}-p">Satellites = clocks.<br><span class="hl">The genius is in your pocket.</span></div>"""
    css = BASE + """.pp { position:absolute; left:350px; top:300px; } .lk { position:absolute; left:60px; top:330px; padding:12px 22px; border-radius:16px; background:#3DDC97; color:#0C3B26; font:900 40px 'SD Display'; opacity:0; }
.pay { top:1040px; font:900 58px 'SD Display'; color:var(--ink); line-height:1.1; opacity:0; }"""
    sc = [fly('.pp', 0.02), pop(f'#{sid}-l', t_c - 0.4), pop(f'#{sid}-p', t_g - 0.6), out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    s9, tc = subscribe_scene(9); out_.append(s9)
    def sfx(g):
        return [(0.02, 'chirp', .5), (g(0, 'no'), 'impact', .7), (g(0, 'phone') + 0.05, 'ping', .55), (S['s1'][0], 'whoosh', .5), (S['s1'][0] + 0.3, 'hum', .25),
                (g(1, 'twenty'), 'ding', .5), (S['s2'][0] + 0.2, 'ping', .5), (S['s2'][0] + 1.0, 'ping', .35), (g(2, 'track'), 'error', .4), (g(2, 'time'), 'tick2', .7),
                (g(2, 'time') + 0.5, 'tick2', .6), (g(3, 'listens'), 'chirp', .5), (g(3, 'fraction') - 0.4, 'tick2', .6), (g(4, 'multiply'), 'pop', .6), (g(4, 'distance') - 0.2, 'stamp', .7),
                (g(5, 'one'), 'ping', .5), (g(5, 'three'), 'ping', .5), (g(5, 'three') + 0.6, 'lock', .7), (g(5, 'fourth'), 'tick2', .6),
                (S['s6'][0], 'whoosh', .5), (g(6, 'thirtyeight') - 0.1, 'impact', .7), (g(7, 'drift'), 'riser', .4), (g(7, 'eleven') - 0.1, 'thud', .8),
                (g(8, 'clocks') - 0.4, 'lock', .8), (g(8, 'genius'), 'ding', .6), (S['s9'][0], 'whoosh', .5), (tc + S['s9'][0], 'click', .9), (tc + S['s9'][0] + 0.1, 'ding', .7)]
    return out_, sfx

# ============================================================== goog01: how Google knows
def goog():
    out_ = []
    def sbar(sid, txt_id):
        return f'<div class="sb"><svg width="54" height="54" viewBox="0 0 100 100" fill="none" stroke="#8C6B5A" stroke-width="10" stroke-linecap="round"><circle cx="42" cy="42" r="26"/><path d="M62 62l22 22"/></svg><span id="{txt_id}"></span><i class="cur"></i></div>'
    BAR = BASE + """.sb { position:absolute; left:90px; width:900px; top:400px; height:130px; border-radius:65px; background:#FFFFFF; border:3px solid #E6D9CE; box-shadow:0 20px 50px rgba(0,0,0,.25); display:flex; align-items:center; gap:24px; padding:0 40px; font:600 54px 'SD Text'; color:#1E120C; }
.cur { width:4px; height:60px; background:#1E120C; } .dd { position:absolute; left:90px; width:900px; top:545px; border-radius:30px; background:#FFFFFF; border:3px solid #E6D9CE; box-shadow:0 30px 60px rgba(0,0,0,.25); overflow:hidden; }
.dd div { display:flex; align-items:center; gap:22px; padding:22px 40px; font:600 44px 'SD Text'; color:#1E120C; border-bottom:2px solid #F3EDE4; opacity:0; } .dd b { font-weight:800; } .dd i { margin-left:auto; font:700 24px 'SD Text'; font-style:normal; color:#8A6550; }"""
    sid = 's0'; t_g, t_m = wl(0, 'guesses'), wl(0, 'mind')
    sugg = ['how to <b>tie a tie</b>', 'how to <b>screenshot on laptop</b>', 'how to <b>make money online</b>', 'how to <b>cook rice</b>']
    body = f"""{sbar(sid, f'{sid}-tx')}<div class="dd">{''.join(f'<div id="{sid}-d{k}">{s}</div>' for k, s in enumerate(sugg))}</div>
<div class="stamp" id="{sid}-st" style="left:250px; top:1090px;">MIND-READING?</div><div class="xx" id="{sid}-x"></div>"""
    css = BAR + ".xx { position:absolute; left:230px; top:1150px; width:620px; height:14px; border-radius:7px; background:#1E120C; transform:scaleX(0) rotate(-8deg); transform-origin:left; }"
    sc = steps(f'#{sid}-tx', 0.1, ['h', 'ho', 'how', 'how ', 'how t', 'how to'], 0.1)
    sc += [pop(f'#{sid}-d{k}', round(0.75 + k * 0.12, 3), 8) for k in range(4)] + [slam(f'#{sid}-st', t_m - 0.6), f'    tl.to("#{sid}-x", {{ scaleX:1, duration:.25 }}, {t_m});', out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    sid = 's1'; t_r = wl(1, 'real')
    rows = ['how to <b>tie a tie</b>', 'how to <b>cook rice</b>', 'how to <b>screenshot</b>']
    body = f"""{sbar(sid, f'{sid}-tx')}<div class="dd">{''.join(f'<div id="{sid}-d{k}">{s}<i id="{sid}-i{k}">REAL SEARCHES ✓</i></div>' for k, s in enumerate(rows))}</div>
<div class="center ppl" id="{sid}-p">Built from what people actually type</div>"""
    css = BAR + ".dd i { opacity:0; color:#2E9E6B; } .ppl { top:1000px; font:800 46px 'SD Display'; color:var(--ink); opacity:0; }"
    sc = [f'    tl.set("#{sid}-tx", {{ textContent:"how to" }}, 0);'] + [pop(f'#{sid}-d{k}', 0.05 + k * 0.08, 8) for k in range(3)]
    sc += [pop(f'#{sid}-i{k}', round(t_r + k * 0.15, 3), 4) for k in range(3)] + [pop(f'#{sid}-p', t_r + 0.6), out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    sid = 's2'; ts = [wl(2, 'trending'), wl(2, 'common'), wl(2, 'searched')]
    chips = [('📈', 'Trending now'), ('📍', 'Common where you are'), ('🕘', 'Your past searches')]
    body = f"""<div class="center kk" style="top:360px">WHAT SHAPES YOUR SUGGESTIONS</div>
{''.join(f'<div class="fc" id="{sid}-c{k}" style="top:{460 + k * 220}px"><span>{ic}</span>{t}</div>' for k, (ic, t) in enumerate(chips))}
<div class="src" style="top:1150px">SOURCE: GOOGLE, "HOW AUTOCOMPLETE PREDICTIONS WORK"</div>"""
    css = BASE + """.fc { position:absolute; left:120px; width:840px; height:180px; border-radius:34px; border:3px solid #3E2217; background:linear-gradient(90deg,#2C1A13,#1F120C); display:flex; align-items:center; gap:30px; padding:0 40px; font:900 54px 'SD Display'; color:var(--ink); opacity:.25; }
.fc span { font-size:80px; }"""
    sc = []
    for k, t in enumerate(ts):
        sc += [f'    tl.to("#{sid}-c{k}", {{ opacity:1, borderColor:"#F87736", scale:1.04, duration:.25, ease:"back.out(2)" }}, {round(t - 0.1, 3)});', f'    tl.to("#{sid}-c{k}", {{ scale:1, duration:.2 }}, {round(t + 0.2, 3)});']
    out_.append(scene(sid, body, sc_join(sid, sc + [out(sid)]), css))
    sid = 's3'; t_b = wl(3, 'bigger')
    body = f"""<div class="box" id="{sid}-r" style="left:90px; top:330px; width:900px; height:700px; padding:40px;">{''.join('<div class="rl"><i></i><b></b><u></u></div>' for _ in range(3))}</div><div class="center qq" id="{sid}-q">?</div>"""
    css = BASE + ".rl { margin:20px 0 40px; } .rl i { display:block; width:40%; height:18px; border-radius:9px; background:#3DDC97; opacity:.5; } .rl b { display:block; width:80%; height:34px; border-radius:12px; background:#1C7ED6; opacity:.6; margin:12px 0; } .rl u { display:block; width:95%; height:20px; border-radius:10px; background:#5C4337; } .qq { top:520px; font:900 360px 'SD Display'; color:var(--accent); opacity:0; }"
    sc = [fly(f'#{sid}-r', 0.02), slam(f'#{sid}-q', t_b - 0.2), out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    sid = 's4'; t_c, t_l = wl(4, 'crawlers'), wl(4, 'link')
    N = [(180, 560), (480, 500), (800, 580), (300, 840), (640, 790), (900, 960), (420, 1090), (160, 1110)]
    E_ = [(0, 1), (1, 2), (0, 3), (1, 4), (2, 5), (4, 5), (3, 6), (6, 7), (4, 6)]
    lines = ''.join(f'<line x1="{N[a][0]}" y1="{N[a][1]}" x2="{N[b][0]}" y2="{N[b][1]}" stroke="#F87736" stroke-width="5" stroke-opacity=".45"/>' for a, b in E_)
    nodes = ''.join(f'<div class="pg" id="{sid}-n{k}" style="left:{x - 60}px; top:{y - 75}px"><i></i><i></i><i></i></div>' for k, (x, y) in enumerate(N))
    spider = '<svg width="110" height="110" viewBox="0 0 100 100"><circle cx="50" cy="55" r="20" fill="#1E120C"/><circle cx="50" cy="30" r="12" fill="#1E120C"/><circle cx="45" cy="28" r="3" fill="#F87736"/><circle cx="55" cy="28" r="3" fill="#F87736"/><path d="M32 48L10 36M32 56L8 58M32 64L12 82M68 48L90 36M68 56L92 58M68 64L88 82" stroke="#1E120C" stroke-width="5" stroke-linecap="round"/></svg>'
    path_ = [0, 1, 2, 5, 4, 6, 7]
    body = f"""<div class="center kk" style="top:330px">CRAWLERS FOLLOW EVERY LINK</div><svg class="ln" width="1080" height="1400">{lines}</svg>{nodes}<div class="sp" id="{sid}-sp">{spider}</div>"""
    css = BASE + """.ln { position:absolute; left:0; top:0; } .pg { position:absolute; width:120px; height:150px; border-radius:16px; background:#FFFFFF; border:3px solid #E6D9CE; padding:16px; opacity:.5; }
.pg i { display:block; height:12px; border-radius:6px; background:#E6D9CE; margin:10px 0; } .sp { position:absolute; left:0; top:0; }"""
    sc = [f'    tl.set("#{sid}-sp", {{ x:{N[0][0] - 55}, y:{N[0][1] - 55} }}, 0);']
    hop = max(0.25, (dur(sid) - t_c - 0.5) / len(path_))
    kf = ','.join(f'{{ x:{N[p][0] - 55}, y:{N[p][1] - 55}, duration:{round(hop, 2)} }}' for p in path_[1:])
    sc += [f'    tl.to("#{sid}-sp", {{ keyframes:[{kf}], ease:"power1.inOut" }}, {round(t_c, 3)});']
    sc += [f'    tl.to("#{sid}-n{p}", {{ opacity:1, borderColor:"#F87736", duration:.2 }}, {round(t_c + j * hop, 3)});' for j, p in enumerate(path_)] + [out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    sid = 's5'; t_h, t_gb = wl(5, 'hundreds'), wl(5, 'gigabytes')
    shelves = '<div class="shv">' + ''.join('<div class="row">' + ''.join(f'<i style="height:{90 + (k * 37) % 50}px; background:{["#F87736", "#1C7ED6", "#3DDC97", "#D8C4B4", "#8C6B5A"][k % 5]}"></i>' for k in range(16)) + '</div>' for _ in range(4)) + '</div>'
    body = f"""<div class="lib" id="{sid}-lb">{photo('library.jpg', shelves, 900, 560)}</div>
<div class="st5" id="{sid}-a"><b>HUNDREDS OF BILLIONS</b><span>of pages</span></div><div class="st5" id="{sid}-b" style="top:1020px"><b>100,000,000+ GB</b><span>index size</span></div>
<div class="src" style="top:1170px">SOURCE: GOOGLE, "HOW SEARCH WORKS"{' · PHOTO: WIKIMEDIA COMMONS' if (IMG / 'library.jpg').exists() else ''}</div>"""
    css = BASE + """.lib { position:absolute; left:90px; top:280px; } .shv { padding:30px; width:100%; } .row { display:flex; align-items:flex-end; gap:8px; height:130px; border-bottom:10px solid #8C6B5A; margin-bottom:14px; } .row i { flex:1; border-radius:4px; }
.st5 { position:absolute; left:120px; width:840px; top:880px; padding:14px 30px; border-radius:26px; background:#F3E6DC; text-align:center; opacity:0; } .st5 b { display:block; font:900 58px 'SD Display'; color:var(--accent); } .st5 span { font:700 30px 'SD Text'; color:#1E120C; }"""
    sc = [fly(f'#{sid}-lb', 0.02), kb(f'#{sid}-lb', dur(sid)), f'    tl.fromTo("#{sid}-lb .kb, #{sid}-lb .shv", {{ y:0 }}, {{ y:-30, duration:{dur(sid)}, ease:"none" }}, 0);',
          pop(f'#{sid}-a', t_h - 0.1), pop(f'#{sid}-b', t_gb - 0.4), out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    sid = 's6'; t_bk, t_in = wl(6, 'book'), wl(6, 'instant')
    entries = [('crawling', '12'), ('GPS', '31'), ('index', '47'), ('ranking', '63'), ('robots', '88')]
    body = f"""<div class="bk" id="{sid}-bk"><div class="bt">INDEX</div>{''.join(f'<div class="en" id="{sid}-e{k}"><span>{a}</span><i></i><b>{p}</b></div>' for k, (a, p) in enumerate(entries))}</div>
<div class="fg" id="{sid}-fg">👉</div><div class="center ins" id="{sid}-is">CHECK THE INDEX, NOT THE WEB → <span class="hl">INSTANT</span></div>"""
    css = BASE + """.bk { position:absolute; left:190px; top:330px; width:700px; padding:50px 60px; border-radius:16px 40px 40px 16px; background:#FFFAF2; box-shadow:0 30px 70px rgba(0,0,0,.3); border-left:24px solid #8C6B5A; }
.bt { font:900 64px 'SD Serif'; color:#1E120C; margin-bottom:24px; } .en { display:flex; align-items:center; gap:14px; font:600 44px 'SD Serif'; color:#3A2A10; margin:18px 0; border-radius:10px; padding:4px 8px; }
.en i { flex:1; border-bottom:4px dotted #B8A090; } .en b { font:800 40px 'SD Mono'; } .fg { position:absolute; left:80px; top:560px; font-size:90px; opacity:0; }
.ins { top:1050px; font:900 48px 'SD Display'; color:var(--ink); opacity:0; }"""
    sc = [f'    tl.fromTo("#{sid}-bk", {{ rotationY:-80, opacity:0 }}, {{ rotationY:0, opacity:1, duration:.6, ease:"power3.out" }}, 0.02);',
          f'    tl.fromTo("#{sid}-fg", {{ opacity:0, x:-100 }}, {{ opacity:1, x:0, duration:.3 }}, {t_bk + 0.3});', f'    tl.to("#{sid}-fg", {{ y:180, duration:.4, ease:"power2.inOut" }}, {t_bk + 0.8});',
          f'    tl.to("#{sid}-e2", {{ backgroundColor:"rgba(248,119,54,.3)", duration:.25 }}, {t_bk + 1.2});', slam(f'#{sid}-is', t_in - 0.3), out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    sid = 's7'; t_s, t_f = wl(7, 'signals'), wl(7, 'first')
    res = ['Result A', 'Result B', 'Result C', 'Result D']
    body = f"""<div class="sig"><span class="chip">🌐 language</span><span class="chip">📍 location</span><span class="chip">📱 device</span></div>
{''.join(f'<div class="rc" id="{sid}-r{k}" style="top:{560 + k * 150}px"><b id="{sid}-n{k}">{k + 1}</b>{r}</div>' for k, r in enumerate(res))}<div class="src" style="top:1180px">"HUNDREDS OF FACTORS" · SOURCE: GOOGLE</div>"""
    css = BASE + """.sig { position:absolute; left:60px; right:60px; top:360px; display:flex; justify-content:center; gap:16px; } .sig .chip { font-size:32px; padding:12px 20px; }
.rc { position:absolute; left:150px; width:780px; height:120px; border-radius:26px; border:2px solid #3E2217; background:linear-gradient(90deg,#2C1A13,#1F120C); display:flex; align-items:center; gap:24px; padding:0 30px; font:800 46px 'SD Display'; color:var(--ink); }
.rc b { width:70px; height:70px; border-radius:35px; background:#3A2318; color:var(--accent); display:flex; align-items:center; justify-content:center; }"""
    order = [2, 0, 3, 1]
    sc = [pop('.sig', 0.05)] + [fly(f'#{sid}-r{k}', 0.1 + k * 0.08, 0, 10) for k in range(4)]
    sc += [f'    tl.to("#{sid}-r{k}", {{ y:{(order.index(k) - k) * 150}, duration:.6, ease:"power3.inOut" }}, {round(t_s + 0.3, 3)});' for k in range(4)]
    sc += [f'    tl.set("#{sid}-n{k}", {{ textContent:"{order.index(k) + 1}" }}, {round(t_s + 0.9, 3)});' for k in range(4)]
    sc += [f'    tl.to("#{sid}-r2", {{ borderColor:"#F87736", boxShadow:"0 0 50px rgba(248,119,54,.4)", duration:.3 }}, {t_f - 0.2});', out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    sid = 's8'; t_en, t_n = wl(8, 'enter'), wl(8, 'notes')
    body = f"""<div class="key" id="{sid}-k">ENTER ↵</div><div class="nb" id="{sid}-nb"><b>Google's notes</b><div>✓ already crawled</div><div>✓ already indexed</div><div>✓ ranked in milliseconds</div></div>"""
    css = BASE + """.key { position:absolute; left:290px; top:330px; width:500px; height:220px; border-radius:36px; background:#F3E6DC; border-bottom:24px solid #D8C4B4; display:flex; align-items:center; justify-content:center; font:900 90px 'SD Display'; color:#1E120C; }
.nb { position:absolute; left:150px; width:780px; top:660px; padding:40px 50px; border-radius:24px; background:#FFF8D6; box-shadow:0 30px 60px rgba(0,0,0,.3); transform:rotate(-2deg); font:700 46px 'SD Serif'; color:#3A2A10; opacity:0; }
.nb b { display:block; font:900 56px 'SD Display'; color:#1E120C; margin-bottom:10px; } .nb div { margin:10px 0; }"""
    sc = [pop(f'#{sid}-k', 0.02), f'    tl.fromTo("#{sid}-k", {{ y:0, borderBottomWidth:24 }}, {{ y:18, borderBottomWidth:6, duration:.08, yoyo:true, repeat:1, immediateRender:false }}, {t_en});',
          pop(f'#{sid}-nb', t_n - 0.9), out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    s9, tc = subscribe_scene(9); out_.append(s9)
    def sfx(g):
        return [(0.1, 'keys', .55), (0.75, 'pop', .45), (0.87, 'pop', .4), (g(0, 'mind') - 0.6, 'stamp', .7), (g(0, 'mind'), 'rip', .5),
                (S['s1'][0], 'whoosh', .45), (g(1, 'real'), 'ding', .5), (g(2, 'trending'), 'pop', .6), (g(2, 'common'), 'pop', .6), (g(2, 'searched'), 'pop', .6),
                (g(3, 'bigger') - 0.2, 'impact', .7), (g(4, 'crawlers'), 'servo', .35), (g(4, 'link'), 'tick2', .5), (S['s5'][0], 'whoosh', .5), (g(5, 'hundreds'), 'flip', .6),
                (g(5, 'gigabytes') - 0.4, 'stamp', .6), (S['s6'][0], 'flip', .7), (g(6, 'book') + 1.2, 'ding', .5), (g(6, 'instant') - 0.3, 'impact', .6),
                (g(7, 'signals') + 0.3, 'whoosh', .5), (g(7, 'first') - 0.2, 'ding', .6), (g(8, 'enter'), 'click', .9), (g(8, 'enter') + 0.05, 'stamp', .6), (g(8, 'notes') - 0.9, 'flip', .5),
                (S['s9'][0], 'whoosh', .5), (tc + S['s9'][0], 'click', .9), (tc + S['s9'][0] + 0.1, 'ding', .7)]
    return out_, sfx

# ============================================================== net01: if the internet disappeared
def net():
    out_ = []
    sid = 's0'; t_v, t_im = wl(0, 'vanish'), wl(0, 'imagine')
    apps = [('Facebook', '#1877F2'), ('Instagram', '#D6249F'), ('WhatsApp', '#25D366')]
    body = f"""<div class="apps">{''.join(f'<div class="ap" id="{sid}-a{k}"><i style="background:{c}"></i><b>{n}</b><span id="{sid}-s{k}">online</span></div>' for k, (n, c) in enumerate(apps))}</div>
<div class="center h6" id="{sid}-h">≈ 6 HOURS OFFLINE · OCT 2021</div><div class="dark" id="{sid}-dk"></div><div class="center wi" id="{sid}-w">NOW IMAGINE THE <span class="hl">WHOLE INTERNET</span></div>"""
    css = BASE + """.apps { position:absolute; left:90px; right:90px; top:360px; display:flex; justify-content:space-between; } .ap { width:280px; height:360px; border-radius:36px; background:linear-gradient(180deg,#2C1A13,#1F120C); border:2px solid #3E2217; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:16px; }
.ap i { width:150px; height:150px; border-radius:40px; } .ap b { font:900 40px 'SD Display'; color:var(--ink); } .ap span { font:700 28px 'SD Mono'; color:#2E9E6B; }
.h6 { top:800px; font:900 56px 'SD Display'; color:var(--red); opacity:0; } .dark { position:absolute; inset:0; background:#100804; opacity:0; } .wi { top:960px; font:900 58px 'SD Display'; color:#FFFFFF; opacity:0; z-index:2; }"""
    sc = [pop(f'#{sid}-a{k}', 0.05 + k * 0.1) for k in range(3)]
    for k in range(3):
        sc += [f'    tl.to("#{sid}-a{k} i", {{ filter:"grayscale(1)", opacity:.35, duration:.3 }}, {round(t_v + k * 0.15, 3)});', f'    tl.set("#{sid}-s{k}", {{ textContent:"server not found", color:"#FF3B30" }}, {round(t_v + k * 0.15, 3)});']
    sc += [slam(f'#{sid}-h', t_v + 0.6), f'    tl.to("#{sid}-dk", {{ opacity:.9, duration:.6 }}, {t_im - 0.2});', pop(f'#{sid}-w', t_im + 0.1), out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    sid = 's1'; t_f, t_c = wl(1, 'faulty'), wl(1, 'cut')
    cfg = ['router bgp 32934', '  network backbone', '  ...', '- withdraw routes   ← one bad change', '  ...']
    body = f"""<div class="card" id="{sid}-c" style="top:330px;"><div class="hd"><div class="tile">{icon('doc')}</div><div><div class="lab">ILLUSTRATION · SIMPLIFIED</div><div class="ttl">backbone-router.conf</div></div></div>
<div class="code">{''.join(f'<div id="{sid}-l{k}" class="{"bad" if k == 3 else ""}">{E(l)}</div>' for k, l in enumerate(cfg))}</div></div>
<div class="dcs">{''.join(f'<div class="dcx" id="{sid}-d{k}">DATA<br>CENTER</div>' for k in range(3))}</div><div class="src" style="top:1220px">PER META'S STATEMENT, OCT 2021</div>"""
    css = BASE + """.code { background:#0E0806; border-radius:20px; padding:20px 26px; font:700 30px 'SD Mono'; color:#CDB8AA; line-height:1.6; } .code .bad { color:#FF6B5E; background:rgba(255,59,48,.15); border-radius:8px; }
.dcs { position:absolute; left:90px; right:90px; top:900px; display:flex; justify-content:space-between; } .dcx { width:260px; height:220px; border-radius:24px; border:4px solid #3DDC97; background:linear-gradient(180deg,#2C1A13,#1F120C); display:flex; align-items:center; justify-content:center; text-align:center; font:900 40px 'SD Display'; color:var(--ink); }"""
    sc = [fly(f'#{sid}-c', 0.02), f'    tl.fromTo("#{sid}-l3", {{ opacity:.2 }}, {{ opacity:1, duration:.1, repeat:5, yoyo:true, immediateRender:false }}, {t_f});']
    sc += [f'    tl.to("#{sid}-d{k}", {{ borderColor:"#FF3B30", opacity:.4, duration:.25 }}, {round(t_c + k * 0.15, 3)});' for k in range(3)] + [shake('.dcs', t_c), out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    sid = 's2'; t_in = wl(2, 'internal')
    body = f"""<div class="badge" id="{sid}-b"><div class="led" id="{sid}-led"></div><b>BADGE READER</b><span id="{sid}-bs">tap to enter</span></div>
<div class="chat" id="{sid}-ch"><b>Internal chat</b><span id="{sid}-cs">● connecting…</span></div><div class="center ir" id="{sid}-i">EVEN THEIR OWN TOOLS WENT DOWN</div>"""
    css = BASE + """.badge { position:absolute; left:160px; top:330px; width:340px; height:520px; border-radius:40px; background:#2C2A28; border:6px solid #3E2217; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:20px; }
.led { width:80px; height:80px; border-radius:40px; background:#3DDC97; box-shadow:0 0 40px #3DDC97; } .badge b { font:900 34px 'SD Display'; color:#F6EEE8; } .badge span { font:700 28px 'SD Mono'; color:#CDB8AA; }
.chat { position:absolute; left:560px; top:430px; width:380px; padding:40px; border-radius:30px; background:#F3E6DC; text-align:center; } .chat b { display:block; font:900 42px 'SD Display'; color:#1E120C; } .chat span { font:700 30px 'SD Mono'; color:#2E9E6B; }
.ir { top:1000px; font:900 56px 'SD Display'; color:var(--ink); opacity:0; }"""
    sc = [pop(f'#{sid}-b', 0.02), pop(f'#{sid}-ch', 0.15), f'    tl.to("#{sid}-led", {{ backgroundColor:"#FF3B30", boxShadow:"0 0 40px #FF3B30", duration:.1, repeat:5, yoyo:true }}, {t_in - 0.2});',
          f'    tl.set("#{sid}-bs", {{ textContent:"ERROR", color:"#FF3B30" }}, {t_in});', f'    tl.set("#{sid}-cs", {{ textContent:"● offline", color:"#FF3B30" }}, {t_in + 0.3});', pop(f'#{sid}-i', t_in + 0.4), out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    sid = 's3'; t_99, t_sea = wl(3, 'ninetynine'), wl(3, 'sea')
    cables = ''.join(f'<path id="{sid}-p{k}" d="{d}" fill="none" stroke="#F87736" stroke-width="7" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" opacity=".9"/>' for k, d in enumerate(['M60 300 C300 200 600 420 1000 260', 'M40 520 C360 600 640 380 1020 560', 'M80 760 C380 660 700 900 1000 780', 'M120 980 C420 1060 640 880 980 1020']))
    body = f"""<div class="sea"><svg width="1080" height="1200">{cables}</svg></div><div class="xs" id="{sid}-x">{photo('cable_xsec.png', '<svg width="360" height="360" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="#1E120C"/><circle cx="50" cy="50" r="36" fill="#8C6B5A"/><circle cx="50" cy="50" r="26" fill="#D8C4B4"/><circle cx="50" cy="50" r="14" fill="#F87736"/><circle cx="50" cy="50" r="6" fill="#FFE9A8"/></svg>', 380, 380)}</div>
<div class="center p99" id="{sid}-n">99%+</div><div class="center p99s" id="{sid}-s">of data between continents runs through<br><span class="hl">cables on the sea floor</span></div><div class="src" style="top:1250px">SOURCE: TELEGEOGRAPHY</div>"""
    css = BASE + """.sea { position:absolute; left:0; top:260px; width:1080px; height:1000px; background:linear-gradient(180deg, rgba(28,126,214,.10), rgba(28,126,214,.25)); }
.xs { position:absolute; left:350px; top:330px; opacity:0; } .p99 { top:760px; font:900 200px 'SD Display'; color:var(--accent); opacity:0; } .p99s { top:990px; font:800 44px 'SD Display'; color:var(--ink); opacity:0; }"""
    sc = [f'    tl.to("#{sid}-p{k}", {{ strokeDashoffset:0, duration:1.2, ease:"power2.out" }}, {round(0.1 + k * 0.2, 2)});' for k in range(4)]
    sc += [pop(f'#{sid}-x', 0.5), slam(f'#{sid}-n', t_99 - 0.1), pop(f'#{sid}-s', t_sea - 0.6), out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    sid = 's4'; t_cut, t_an = wl(4, 'cut'), wl(4, 'anchor')
    ANCH = '<svg width="200" height="240" viewBox="0 0 100 120" fill="none" stroke="#5C4337" stroke-width="9" stroke-linecap="round"><circle cx="50" cy="14" r="9"/><path d="M50 23v80M26 44h48M12 82c8 22 30 28 38 28s30-6 38-28"/></svg>'
    body = f"""<div class="water"></div><div class="ship">{photo('cable_ship.jpg', '<svg width="540" height="260" viewBox="0 0 270 130"><path d="M10 80 L260 80 L235 120 L35 120 Z" fill="#5C4337"/><rect x="60" y="50" width="120" height="30" rx="4" fill="#D8C4B4"/><rect x="80" y="28" width="60" height="24" rx="4" fill="#F3E6DC"/><rect x="190" y="20" width="8" height="60" fill="#8C6B5A"/><path d="M198 24 L250 60" stroke="#8C6B5A" stroke-width="5"/></svg>', 560, 300)}</div><div class="chn" id="{sid}-ch"></div><div class="anc" id="{sid}-a">{ANCH}</div>
<div class="bed"></div>{''.join(f'<div class="cb" id="{sid}-c{k}" style="top:{1040 + k * 46}px"></div>' for k in range(3))}<div class="center rs" id="{sid}-r">RED SEA · 2024 · 3 CABLES CUT</div><div class="src" style="top:1270px">ILLUSTRATION · SOURCE: TELEGEOGRAPHY</div>"""
    css = BASE + """.water { position:absolute; left:0; right:0; top:560px; bottom:0; background:linear-gradient(180deg, rgba(28,126,214,.18), rgba(11,37,84,.45)); }
.ship { position:absolute; left:80px; top:300px; } .hull { width:100%; height:100%; background:linear-gradient(180deg,#D8C4B4 60%,#5C4337 60%); }
.chn { position:absolute; left:500px; top:560px; width:8px; height:0; background:repeating-linear-gradient(180deg,#5C4337 0 14px,transparent 14px 20px); } .anc { position:absolute; left:405px; top:520px; }
.bed { position:absolute; left:0; right:0; top:1180px; height:80px; background:#C9A98A; } .cb { position:absolute; left:0; right:0; height:16px; border-radius:8px; background:#1E120C; }
.rs { top:340px; font:900 50px 'SD Display'; color:var(--red); opacity:0; z-index:3; }"""
    sc = [fly('.ship', 0.02), f'    tl.to("#{sid}-ch", {{ height:520, duration:1.1, ease:"power1.in" }}, 0.3);', f'    tl.to("#{sid}-a", {{ y:520, duration:1.1, ease:"power1.in" }}, 0.3);',
          f'    tl.to("#{sid}-a", {{ x:420, rotation:-25, duration:1.2, ease:"power1.inOut" }}, {t_an - 0.2});', f'    tl.to("#{sid}-ch", {{ x:420, duration:1.2, ease:"power1.inOut" }}, {t_an - 0.2});']
    sc += [f'    tl.to("#{sid}-c{k}", {{ clipPath:"inset(0 0 0 0)", backgroundColor:"#FF3B30", duration:.1 }}, {round(t_an + 0.2 + k * 0.25, 3)});' for k in range(3)]
    sc += [f'    tl.to("#{sid}-c{k}", {{ scaleX:.45, transformOrigin:"left center", duration:.3 }}, {round(t_an + 0.3 + k * 0.25, 3)});' for k in range(3)]
    sc += [slam(f'#{sid}-r', t_cut - 0.2), out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    sid = 's5'; t_q, t_d = wl(5, 'quarter'), wl(5, 'disrupted')
    body = f"""<div class="center kk" style="top:340px">EUROPE ⇄ ASIA DATA TRAFFIC</div><div class="eu">EUROPE</div><div class="as">ASIA</div>
<svg class="arc" width="1080" height="700" viewBox="0 0 1080 700"><path d="M160 520 C360 120 720 120 920 520" fill="none" stroke="#3DDC97" stroke-width="40" stroke-linecap="round" pathLength="100" stroke-dasharray="75 100"/>
<path id="{sid}-bad" d="M160 520 C360 120 720 120 920 520" fill="none" stroke="#FF3B30" stroke-width="40" stroke-linecap="round" pathLength="100" stroke-dasharray="0 75 25 100" opacity="0"/>
<path id="{sid}-alt" d="M160 560 C360 760 720 760 920 560" fill="none" stroke="#F87736" stroke-width="12" stroke-dasharray="20 14" pathLength="1" style="stroke-dashoffset:1" opacity=".9"/></svg>
<div class="center q4" id="{sid}-n">~25% DISRUPTED</div><div class="src" style="top:1230px">UN ESTIMATE, 2024 · TRAFFIC WAS PARTLY REROUTED</div>"""
    css = BASE + """.eu, .as { position:absolute; top:880px; padding:16px 28px; border-radius:20px; background:#F3E6DC; font:900 40px 'SD Display'; color:#1E120C; } .eu { left:80px; } .as { right:100px; }
.arc { position:absolute; left:0; top:380px; } .q4 { top:1090px; font:900 80px 'SD Display'; color:var(--red); opacity:0; }"""
    sc = [pop('.eu', 0.05), pop('.as', 0.1), f'    tl.to("#{sid}-bad", {{ opacity:1, duration:.2 }}, {t_q - 0.1});', slam(f'#{sid}-n', t_q),
          f'    tl.to("#{sid}-alt", {{ strokeDashoffset:0, duration:1, ease:"power2.out" }}, {t_d});', out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    sid = 's6'; ts = [wl(6, 'card'), wl(6, 'maps'), wl(6, 'online')]
    cards = [('💳', 'Card payment', 'NO CONNECTION'), ('🗺️', 'Maps', 'OFFLINE'), ('🏦', 'Online banking', 'CAN\'T CONNECT')]
    body = ''.join(f'<div class="oc" id="{sid}-c{k}" style="top:{330 + k * 290}px"><span>{ic}</span><div><b>{n}</b><i id="{sid}-s{k}">connecting…</i></div></div>' for k, (ic, n, s) in enumerate(cards))
    css = BASE + """.oc { position:absolute; left:120px; width:840px; height:240px; border-radius:36px; background:linear-gradient(90deg,#2C1A13,#1F120C); border:3px solid #3E2217; display:flex; align-items:center; gap:34px; padding:0 40px; opacity:0; }
.oc span { font-size:110px; } .oc b { display:block; font:900 54px 'SD Display'; color:var(--ink); } .oc i { font:800 36px 'SD Mono'; font-style:normal; color:#9C8576; }"""
    sc = []
    for k, (t, c) in enumerate(zip(ts, cards)):
        sc += [pop(f'#{sid}-c{k}', t - 0.25), f'    tl.set("#{sid}-s{k}", {{ textContent:"{c[2]}", color:"#FF3B30" }}, {round(t + 0.4, 3)});', f'    tl.to("#{sid}-c{k}", {{ borderColor:"#FF3B30", duration:.2 }}, {round(t + 0.4, 3)});']
    out_.append(scene(sid, body, sc_join(sid, sc + [out(sid)]), css))
    sid = 's7'; t_cl, t_bk = wl(7, 'cloud'), wl(7, 'backup')
    CLOUD = '<svg width="420" height="260" viewBox="0 0 100 62" fill="#F3E6DC"><path d="M22 58h56a16 16 0 0 0 0-32 22 22 0 0 0-42-6 18 18 0 0 0-14 38z"/></svg>'
    body = f"""<div class="cl" id="{sid}-cl">{CLOUD}</div><div class="center isnt" id="{sid}-n">NOT A CLOUD.</div>
<div class="parts" id="{sid}-p"><span class="chip">🧵 Cables</span><span class="chip">📡 Routers</span><span class="chip">⚙️ Settings</span></div>
<svg class="bkp" width="1000" height="300"><path id="{sid}-b0" d="M60 150 C300 20 700 20 940 150" fill="none" stroke="#3DDC97" stroke-width="10" pathLength="1" style="stroke-dashoffset:1" stroke-dasharray="1"/><path id="{sid}-b1" d="M60 150 C300 280 700 280 940 150" fill="none" stroke="#3DDC97" stroke-width="10" pathLength="1" style="stroke-dashoffset:1" stroke-dasharray="1"/><path d="M60 150 L940 150" stroke="#F87736" stroke-width="10"/></svg>
<div class="center bk" id="{sid}-bk">→ SO ENGINEERS BUILD <span style="color:#2E9E6B">BACKUP ROUTES</span></div>"""
    css = BASE + """.cl { position:absolute; left:330px; top:320px; } .isnt { top:620px; font:900 80px 'SD Display'; color:var(--ink); opacity:0; }
.parts { position:absolute; left:60px; right:60px; top:740px; display:flex; justify-content:center; gap:16px; opacity:0; } .bkp { position:absolute; left:40px; top:860px; } .bk { top:1180px; font:900 44px 'SD Display'; color:var(--ink); opacity:0; }"""
    sc = [pop(f'#{sid}-cl', 0.02), f'    tl.to("#{sid}-cl", {{ opacity:0, scale:1.4, filter:"blur(12px)", duration:.5 }}, {t_cl + 0.3});', slam(f'#{sid}-n', t_cl + 0.2), pop(f'#{sid}-p', t_cl + 0.8),
          f'    tl.to("#{sid}-b0", {{ strokeDashoffset:0, duration:.8 }}, {t_bk - 0.2});', f'    tl.to("#{sid}-b1", {{ strokeDashoffset:0, duration:.8 }}, {t_bk + 0.1});', pop(f'#{sid}-bk', t_bk), out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    s8, tc = subscribe_scene(8); out_.append(s8)
    def sfx(g):
        return [(g(0, 'vanish'), 'powerdown', .6), (g(0, 'vanish') + 0.3, 'error', .4), (g(0, 'imagine') - 0.2, 'powerdown', .5), (S['s1'][0], 'keys', .4), (g(1, 'faulty'), 'static', .5),
                (g(1, 'cut'), 'snap', .7), (g(2, 'internal') - 0.2, 'error', .5), (g(2, 'internal') + 0.3, 'static', .35), (S['s3'][0], 'rumble', .5), (g(3, 'ninetynine') - 0.1, 'impact', .8),
                (S['s4'][0], 'rumble', .55), (S['s4'][0] + 0.3, 'chain', .6), (g(4, 'anchor') + 0.2, 'snap', .8), (g(4, 'anchor') + 0.45, 'snap', .7), (g(4, 'anchor') + 0.7, 'snap', .7),
                (g(5, 'quarter'), 'thud', .8), (g(5, 'disrupted'), 'whoosh', .4), (g(6, 'card') + 0.4, 'error', .5), (g(6, 'maps') + 0.4, 'error', .5), (g(6, 'online') + 0.4, 'error', .5),
                (g(7, 'cloud') + 0.2, 'impact', .7), (g(7, 'backup'), 'ding', .7), (S['s8'][0], 'whoosh', .5), (tc + S['s8'][0], 'click', .9), (tc + S['s8'][0] + 0.1, 'ding', .7)]
    return out_, sfx

# ============================================================== robo01: dark factories
ARM = '<svg width="{w}" height="{h}" viewBox="0 0 200 240"><rect x="60" y="210" width="80" height="24" rx="6" fill="#5C4337"/><g class="a1" style="transform-origin:100px 210px"><rect x="88" y="110" width="24" height="104" rx="12" fill="#F87736"/><circle cx="100" cy="110" r="18" fill="#D85E25"/><g class="a2" style="transform-origin:100px 110px"><rect x="96" y="40" width="80" height="22" rx="11" fill="#F87736" transform="rotate(20 100 110)"/><circle cx="170" cy="60" r="12" fill="#5C4337"/><circle cx="182" cy="44" r="6" fill="#FFB36B"/></g></g></svg>'
def robo():
    out_ = []
    sid = 's0'; t_d = wl(0, 'dark')
    arms = ''.join(f'<div class="arm" id="{sid}-a{k}" style="left:{80 + k * 330}px">{ARM.format(w=280, h=336)}</div>' for k in range(3))
    lights = ''.join(f'<div class="lt" id="{sid}-l{k}" style="left:{140 + k * 280}px"></div>' for k in range(4))
    body = f"""<div class="fac" id="{sid}-f">{lights}{arms}<div class="belt"></div></div><div class="dk" id="{sid}-dk"></div><div class="center rb" id="{sid}-t">ROBOTS BUILDING ROBOTS<br><span class="hl">IN THE DARK</span></div>"""
    css = BASE + """.fac { position:absolute; left:0; right:0; top:330px; height:760px; } .lt { position:absolute; top:0; width:120px; height:30px; border-radius:0 0 60px 60px; background:#FFE9A8; box-shadow:0 60px 120px 40px rgba(255,233,168,.45); }
.arm { position:absolute; top:300px; } .belt { position:absolute; left:40px; right:40px; top:640px; height:40px; border-radius:20px; background:repeating-linear-gradient(90deg,#5C4337 0 40px,#3E2217 40px 80px); }
.dk { position:absolute; inset:0; background:#100804; opacity:0; } .rb { top:1110px; font:900 58px 'SD Display'; color:var(--ink); line-height:1.1; z-index:2; opacity:0; }"""
    d = dur(sid)
    sc = [pop(f'#{sid}-f', 0.02)]
    for k in range(3):
        sc += [f'    tl.fromTo("#{sid}-a{k} .a1", {{ rotation:-12 }}, {{ rotation:12, duration:.9, yoyo:true, repeat:{max(1, int(d / .9))}, ease:"sine.inOut", immediateRender:false }}, {k * 0.2});',
               f'    tl.fromTo("#{sid}-a{k} .a2", {{ rotation:10 }}, {{ rotation:-20, duration:.7, yoyo:true, repeat:{max(1, int(d / .7))}, ease:"sine.inOut", immediateRender:false }}, {k * 0.15});']
    sc += [f'    tl.to("#{sid}-l{k}", {{ opacity:0, duration:.05 }}, {round(t_d - 1.2 + k * 0.25, 3)});' for k in range(4)]
    sc += [f'    tl.to("#{sid}-dk", {{ opacity:.82, duration:.4 }}, {t_d - 0.2});', f'    tl.to("#{sid}-t", {{ opacity:1, color:"#F6EEE8", duration:.3 }}, {t_d});', out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc).replace('color:"#F6EEE8"', 'color:"#FFFFFF"'), css))
    sid = 's1'; t_01, t_30 = wl(1, '2001'), wl(1, 'thirty')
    body = f"""<div class="ffac">{photo('fanuc_factory.jpg', ARM.format(w=420, h=500), 900, 520)}</div><div class="since" id="{sid}-s">LIGHTS-OUT SINCE 2001</div>
<div class="cal" id="{sid}-c"><div class="ct">DAYS UNSUPERVISED</div><div class="cn" id="{sid}-n">1</div></div><div class="src" style="top:1250px">FANUC, JAPAN · AS REPORTED{' · PHOTO: WIKIMEDIA COMMONS' if (IMG / 'fanuc_factory.jpg').exists() else ''}</div>"""
    css = BASE + """.ffac { position:absolute; left:90px; top:300px; } .since { position:absolute; left:120px; top:760px; padding:14px 26px; border-radius:16px; background:#1E120C; color:#FFB36B; font:900 40px 'SD Mono'; opacity:0; }
.cal { position:absolute; left:290px; top:880px; width:500px; border-radius:30px; background:#FFFAF2; box-shadow:0 30px 60px rgba(0,0,0,.3); text-align:center; overflow:hidden; opacity:0; }
.ct { background:#FF3B30; color:#fff; font:900 34px 'SD Display'; padding:16px; } .cn { font:900 180px 'SD Display'; color:#1E120C; line-height:1.1; }"""
    sc = [fly('.ffac', 0.02), kb('.ffac', dur(sid)), pop(f'#{sid}-s', t_01 - 0.2), pop(f'#{sid}-c', t_30 - 1.2)]
    sc += steps(f'#{sid}-n', t_30 - 0.9, [str(x) for x in (3, 7, 12, 18, 24, 28, 30)], 0.12) + [out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    sid = 's2'; ts = [wl(2, 'lights'), wl(2, 'breaks'), wl(2, 'shift')]
    items = [('💡', 'LIGHTS'), ('☕', 'BREAKS'), ('🔄', 'SHIFT CHANGES')]
    body = ''.join(f'<div class="no" id="{sid}-i{k}" style="top:{330 + k * 300}px"><span>{ic}</span><b>NO {t}</b><i id="{sid}-x{k}"></i></div>' for k, (ic, t) in enumerate(items))
    css = BASE + """.no { position:absolute; left:120px; width:840px; height:250px; border-radius:36px; background:linear-gradient(90deg,#2C1A13,#1F120C); border:3px solid #3E2217; display:flex; align-items:center; gap:40px; padding:0 50px; opacity:0; }
.no span { font-size:120px; } .no b { font:900 64px 'SD Display'; color:var(--ink); } .no i { position:absolute; left:40px; right:40px; top:50%; height:12px; border-radius:6px; background:#FF3B30; transform:scaleX(0); transform-origin:left; }"""
    sc = []
    for k, t in enumerate(ts):
        sc += [pop(f'#{sid}-i{k}', t - 0.15), f'    tl.to("#{sid}-x{k}", {{ scaleX:1, duration:.2 }}, {round(t + 0.15, 3)});']
    out_.append(scene(sid, body, sc_join(sid, sc + [out(sid)]), css))
    sid = 's3'; t_24, t_10 = wl(3, '2024'), wl(3, 'ten')
    stack = ''.join(f'<i style="bottom:{k * 26}px"></i>' for k in range(14))
    body = f"""<div class="center kk" style="top:340px">DARK FACTORY · CHINA · 2024</div><div class="stk" id="{sid}-st">{stack}</div>
<div class="center cnt" id="{sid}-n">0</div><div class="center py">phones a year (designed capacity)</div><div class="src" style="top:1230px">PER XIAOMI · NO LOGOS SHOWN</div>"""
    css = BASE + """.stk { position:absolute; left:390px; top:420px; width:300px; height:420px; } .stk i { position:absolute; left:0; width:300px; height:22px; border-radius:8px; background:#1E120C; border:3px solid #5C4337; }
.cnt { top:880px; font:900 150px 'SD Display'; color:var(--accent); } .py { top:1060px; font:700 40px 'SD Text'; color:var(--ink); }"""
    sc = [f'    tl.fromTo("#{sid}-st i", {{ opacity:0, y:-300 }}, {{ opacity:1, y:0, duration:.3, stagger:.12, ease:"bounce.out" }}, 0.1);']
    sc += steps(f'#{sid}-n', t_10 - 0.5, ['1,000,000', '3,000,000', '5,000,000', '7,500,000', '~10,000,000'], 0.12) + [out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    sid = 's4'; t_lc = wl(4, 'closer')
    body = f"""<div class="center endj" id="{sid}-e">THE END OF<br>FACTORY JOBS?</div><div class="lens2" id="{sid}-l"></div>
{bit(sid, [('n', {'state': 'scan', 'extra': ['laser']})])}"""
    css = BASE + """.endj { top:440px; font:900 110px 'SD Display'; color:var(--ink); line-height:1; opacity:0; }
.lens2 { position:absolute; left:300px; top:380px; width:480px; height:480px; border-radius:50%; border:24px solid var(--accent); box-shadow:0 0 60px rgba(248,119,54,.5); opacity:0; }"""
    sc = [slam(f'#{sid}-e', 0.05), f'    tl.fromTo("#{sid}-l", {{ opacity:0, scale:.3, x:-400 }}, {{ opacity:1, scale:1, x:0, duration:.5, ease:"back.out(1.6)" }}, {t_lc - 0.4});', out(sid)]
    sc += bit_on(sid, 'n', 0, False) + bit_float(sid)
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    sid = 's5'; ts = [wl(5, 'design'), wl(5, 'program'), wl(5, 'fix')]
    roles = [('✏️', 'Product designer'), ('💻', 'Robot programmer'), ('🔧', 'Maintenance technician')]
    body = f"""<div class="center kk" style="top:330px">STILL HUMAN JOBS</div>""" + ''.join(f'<div class="role" id="{sid}-r{k}" style="top:{420 + k * 270}px"><span>{ic}</span><b>{t}</b></div>' for k, (ic, t) in enumerate(roles))
    css = BASE + """.role { position:absolute; left:120px; width:840px; height:220px; border-radius:36px; background:linear-gradient(90deg,#2C1A13,#1F120C); border:3px solid #3E2217; display:flex; align-items:center; gap:36px; padding:0 46px; opacity:.2; }
.role span { font-size:100px; } .role b { font:900 54px 'SD Display'; color:var(--ink); }"""
    sc = []
    for k, t in enumerate(ts):
        sc += [f'    tl.to("#{sid}-r{k}", {{ opacity:1, borderColor:"#3DDC97", scale:1.04, duration:.25, ease:"back.out(2)" }}, {round(t - 0.1, 3)});', f'    tl.to("#{sid}-r{k}", {{ scale:1, duration:.2 }}, {round(t + 0.2, 3)});']
    out_.append(scene(sid, body, sc_join(sid, sc + [out(sid)]), css))
    sid = 's6'; t_cr, t_st = wl(6, 'cruise'), wl(6, 'steer')
    WHEEL = '<svg width="360" height="360" viewBox="0 0 100 100" fill="none" stroke="#1E120C" stroke-width="7"><circle cx="50" cy="50" r="42"/><circle cx="50" cy="50" r="10" fill="#1E120C"/><path d="M50 40V8M41 55L14 70M59 55L86 70"/></svg>'
    body = f"""<div class="gauge"><svg width="620" height="380" viewBox="0 0 200 120"><path d="M20 110 A80 80 0 0 1 180 110" fill="none" stroke="#2A1912" stroke-width="16"/><path d="M20 110 A80 80 0 0 1 150 45" fill="none" stroke="#F87736" stroke-width="16"/>
<g id="{sid}-nd" style="transform-origin:100px 110px"><path d="M100 110 L100 40" stroke="#1E120C" stroke-width="6" stroke-linecap="round"/></g><circle cx="100" cy="110" r="8" fill="#1E120C"/></svg><div class="cc" id="{sid}-cc">CRUISE ON · 24/7</div></div>
<div class="wh" id="{sid}-w">{WHEEL}</div><div class="center stx" id="{sid}-s">…SOMEONE STILL HAS TO <span class="hl">STEER</span></div>"""
    css = BASE + """.gauge { position:absolute; left:230px; top:320px; text-align:center; } .cc { display:inline-block; padding:12px 26px; border-radius:18px; background:#3DDC97; color:#0C3B26; font:900 40px 'SD Display'; opacity:0; }
.wh { position:absolute; left:360px; top:800px; opacity:0; } .stx { top:1180px; font:900 52px 'SD Display'; color:var(--ink); opacity:0; }"""
    sc = [pop('.gauge', 0.02), f'    tl.fromTo("#{sid}-nd", {{ rotation:-80 }}, {{ rotation:40, duration:.8, ease:"back.out(1.5)" }}, {max(0.1, t_cr - 0.4)});', pop(f'#{sid}-cc', t_cr + 0.3),
          pop(f'#{sid}-w', t_st - 1.0), f'    tl.fromTo("#{sid}-w", {{ rotation:-15 }}, {{ rotation:15, duration:.6, yoyo:true, repeat:3, ease:"sine.inOut", immediateRender:false }}, {t_st - 0.6});', pop(f'#{sid}-s', t_st - 0.2), out(sid)]
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    sid = 's7'; t_vs, t_gr, t_nx = wl(7, 'versus'), wl(7, 'grow'), wl(7, 'next')
    body = f"""<div class="vs" id="{sid}-a">ROBOTS vs HUMANS<i id="{sid}-x"></i></div><div class="gw" id="{sid}-b">WHICH JOBS GROW<br>AROUND THEM?</div>
<div class="center nx" id="{sid}-n">▶ FULL VIDEO SOON</div>{bit(sid, [('n', {'state': 'happy', 'arms': 'wave'})])}"""
    css = BASE + """.vs { position:absolute; left:120px; width:840px; top:380px; padding:46px; border-radius:36px; background:linear-gradient(180deg,#2C1A13,#1F120C); border:3px solid #3E2217; text-align:center; font:900 70px 'SD Display'; color:#9C8576; opacity:0; }
.vs i { position:absolute; left:40px; right:40px; top:50%; height:12px; border-radius:6px; background:#FF3B30; transform:scaleX(0); transform-origin:left; }
.gw { position:absolute; left:120px; width:840px; top:660px; padding:46px; border-radius:36px; background:linear-gradient(180deg,#2C1A13,#1F120C); border:4px solid #3DDC97; text-align:center; font:900 70px 'SD Display'; color:var(--ink); line-height:1.05; opacity:0; }
.nx { top:1050px; font:900 56px 'SD Display'; color:var(--accent); opacity:0; }"""
    sc = [pop(f'#{sid}-a', max(0.05, t_vs - 0.5)), f'    tl.to("#{sid}-x", {{ scaleX:1, duration:.25 }}, {t_vs + 0.3});', fly(f'#{sid}-b', t_gr - 0.5, 10, -15), slam(f'#{sid}-n', t_nx - 0.1), out(sid)]
    sc += bit_on(sid, 'n', 0, False) + bit_float(sid)
    out_.append(scene(sid, body, sc_join(sid, sc), css))
    s8, tc = subscribe_scene(8); out_.append(s8)
    def sfx(g):
        return [(0.02, 'hum', .4), (0.1, 'servo', .45), (0.9, 'servo', .4), (g(0, 'dark') - 1.2, 'switch', .8), (g(0, 'dark') - 0.95, 'switch', .8), (g(0, 'dark') - 0.7, 'switch', .8), (g(0, 'dark') - 0.45, 'switch', .8),
                (S['s1'][0], 'hiss', .5), (g(1, '2001') - 0.2, 'stamp', .6), (g(1, 'thirty') - 0.9, 'flip', .5), (g(1, 'thirty'), 'ding', .5),
                (g(2, 'lights'), 'thud', .7), (g(2, 'breaks'), 'thud', .7), (g(2, 'shift'), 'thud', .7), (S['s3'][0] + 0.1, 'chain', .4), (g(3, 'ten'), 'impact', .7),
                (g(4, 'closer') - 0.4, 'riser', .45), (g(5, 'design'), 'ding', .5), (g(5, 'program'), 'ding', .5), (g(5, 'fix'), 'ding', .5),
                (g(6, 'cruise') - 0.4, 'servo', .4), (g(6, 'steer') - 0.2, 'whoosh', .5), (g(7, 'versus') + 0.3, 'rip', .6), (g(7, 'next') - 0.1, 'impact', .7),
                (S['s8'][0], 'whoosh', .5), (tc + S['s8'][0], 'click', .9), (tc + S['s8'][0] + 0.1, 'ding', .7)]
    return out_, sfx

if __name__ == '__main__':
    scenes, sfx = {'sat01': sat, 'goog01': goog, 'net01': net, 'robo01': robo}[K]()
    L.sfx_list = lambda: sorted(sfx(lambda i, w: S[f's{i}'][0] + wl(i, w)))
    comp = L.P / 'compositions'; comp.mkdir(parents=True, exist_ok=True)
    for f in comp.glob('*.html'): f.unlink()
    for i, html in enumerate(scenes):
        (comp / f's{i}.html').write_text(html)
    (comp / 'bg.html').write_text(L.bg())
    (comp / 'caps.html').write_text(L.captions())
    (L.P / 'index.html').write_text(L.index())
    (L.P / 'assets/img_credits.json').write_text(json.dumps(USED, indent=1))
    print('written', L.P, L.DUR, 'photos used:', list(USED))
