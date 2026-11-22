"""IT-job Shorts (Nov 2026): job01 developer postings (Indeed), job02 India IT fresher hiring vs headcount,
job03 AI-cited layoffs (Challenger). Context-styled animated cards; Short helper library = hf_news01_short.py.
Usage: THEME=cream GRID=<pattern> python3 tools/hf_job_shorts.py job01|job02|job03"""
import os, sys
from pathlib import Path
JOB = sys.argv[1]
os.environ['SHORT_ID'] = f'{JOB}-short'
sys.path.insert(0, str(Path(__file__).resolve().parent))
import hf_news01_short as L
from hf_news01_short import S, wl, fly, pop, slam, shake, ring, out, icon, bit, bit_on, bit_float, scene, E

CSS0 = """.center { position:absolute; left:40px; right:40px; text-align:center; }
.kk { font:600 32px 'SD Text'; letter-spacing:4px; color:var(--dim); }
.big { font:900 200px 'SD Display'; color:var(--accent); letter-spacing:-5px; line-height:1; text-shadow:0 0 50px rgba(248,119,54,.4); }
.box { position:absolute; border-radius:36px; border:2px solid #3E2217; background:linear-gradient(180deg,#2C1A13,#1F120C); box-shadow:0 30px 70px rgba(0,0,0,.35); }
.src { position:absolute; left:96px; font:600 22px 'SD Text'; letter-spacing:2px; color:var(--dim); }"""

def steps(sel, t0, vals, dt=0.07):
    return [f'    tl.set("{sel}", {{ textContent:"{v}" }}, {round(t0 + k * dt, 3)});' for k, v in enumerate(vals)]
def donut(sid, pct, label, col='#F87736'):
    return f"""<svg class="dn" width="460" height="460" viewBox="0 0 120 120"><circle cx="60" cy="60" r="48" fill="none" stroke="#2A1912" stroke-width="16"/>
<circle id="{sid}-arc" cx="60" cy="60" r="48" fill="none" stroke="{col}" stroke-width="16" stroke-linecap="round" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100" transform="rotate(-90 60 60)"/>
<text x="60" y="66" text-anchor="middle" font-family="SD Display" font-weight="900" font-size="26" fill="#F6EEE8" id="{sid}-pct">0%</text></svg>
<div class="center dl" id="{sid}-lb">{label}</div>"""
DCSS = ".dn { position:absolute; left:310px; top:400px; } .dl { top:880px; font:900 68px 'SD Display'; color:var(--ink); opacity:0; }"
def donut_anim(sid, t, pct):
    vals = [f'{round(pct * k / 6)}%' for k in range(1, 7)]
    return [f'    tl.to("#{sid}-arc", {{ strokeDashoffset:{100 - pct}, duration:.6, ease:"power3.out" }}, {t});'] + steps(f'#{sid}-pct', t, vals, 0.09) + [pop(f'#{sid}-lb', t + 0.35)]

# =================================================================== job01: developer postings
def j1():
    sc_ = []
    # s0 code editor + chart
    sid = 's0'; t_up = wl(0, 'up'); t_c = wl(0, 'code')
    lines = ['def build_app():', '    # written by AI ✓', '    return deploy(code)']
    lh = ''.join(f'<div class="cl" id="{sid}-l{k}">{E(l)}</div>' for k, l in enumerate(lines))
    body = f"""<div class="card" id="{sid}-ed" style="top:300px;"><div class="hd"><div class="tile">{icon('doc')}</div><div><div class="lab">AI CODE ASSISTANT · ILLUSTRATION</div><div class="ttl">app.py</div></div></div>
<div class="inner2">{lh}</div></div>
<div class="box" id="{sid}-ch" style="left:190px; top:820px; width:700px; height:300px;"><svg width="700" height="300"><polyline id="{sid}-pl" points="40,250 180,230 320,200 460,150 640,70" fill="none" stroke="#3DDC97" stroke-width="12" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg><div class="q" id="{sid}-q">?!</div></div>"""
    css = CSS0 + """.inner2 { background:#0E0806; border-radius:22px; padding:24px 28px; } .cl { font:700 36px 'SD Mono'; color:#F6EEE8; line-height:1.6; opacity:0; } .cl:nth-child(2) { color:#3DDC97; }
.q { position:absolute; right:30px; top:10px; font:900 110px 'SD Display'; color:var(--accent); opacity:0; }"""
    sc = [fly('#s0-ed', 0.02)] + [pop(f'#s0-l{k}', t_c - 0.3 + k * 0.25, 8) for k in range(3)] + [fly('#s0-ch', t_up - 1.0),
          f'    tl.to("#s0-pl", {{ strokeDashoffset:0, duration:.7, ease:"power2.out" }}, {t_up - 0.6});', slam('#s0-q', t_up), out(sid)]
    sc += bit_on(sid, 'n', 0, False) + bit_float(sid)
    body += bit(sid, [('n', {'state': 'normal', 'arms': 'type'})])
    sc_.append(scene(sid, body, '\n'.join(sc), css))
    # s1 Indeed chart
    sid = 's1'; t_r = wl(1, 'rising')
    body = f"""<div class="center kk" style="top:330px">US SOFTWARE DEV JOB POSTINGS</div>
<div class="box" id="{sid}-c" style="left:90px; top:400px; width:900px; height:620px;">
<svg width="900" height="620"><line x1="60" y1="540" x2="860" y2="540" stroke="#5C4337" stroke-width="3"/>
<polyline id="{sid}-pl" points="60,300 200,420 340,470 480,440 620,380 760,300 860,250" fill="none" stroke="#F87736" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
<text x="470" y="590" font-family="SD Text" font-weight="600" font-size="28" fill="#9E745A">May 2025</text><text x="760" y="590" font-family="SD Text" font-weight="600" font-size="28" fill="#9E745A">May 2026</text></svg>
<div class="up" id="{sid}-up">RISING AGAIN ↑</div></div>
<div class="src" style="top:1050px">ILLUSTRATIVE CURVE · SOURCE: INDEED HIRING LAB (JUL 2026)</div>"""
    css = CSS0 + ".up { position:absolute; right:40px; top:40px; padding:14px 24px; border-radius:18px; background:var(--green); color:#0C3B26; font:900 40px 'SD Display'; opacity:0; }"
    sc = [fly(f'#{sid}-c', 0.02), f'    tl.to("#{sid}-pl", {{ strokeDashoffset:0, duration:1.4, ease:"power1.inOut" }}, 0.3);', pop(f'#{sid}-up', t_r), out(sid)]
    sc_.append(scene(sid, body, '\n'.join(sc), css))
    # s2 who
    sid = 's2'; t_w = wl(2, 'who')
    body = f"""<div class="center who" id="{sid}-w">WHO?</div><div class="lens" id="{sid}-ls"></div>
{bit(sid, [('n', {'state': 'scan', 'extra': ['laser']})])}"""
    css = CSS0 + """.who { top:560px; font:900 260px 'SD Display'; color:var(--ink); letter-spacing:-6px; opacity:0; }
.lens { position:absolute; left:340px; top:480px; width:400px; height:400px; border-radius:50%; border:22px solid var(--accent); box-shadow:0 0 60px rgba(248,119,54,.5); opacity:0; }"""
    sc = [f'    tl.fromTo("#{sid}-ls", {{ opacity:0, scale:.3, x:-300 }}, {{ opacity:1, scale:1, x:0, duration:.45, ease:"back.out(1.6)" }}, 0.05);', slam(f'#{sid}-w', t_w), out(sid)]
    sc += bit_on(sid, 'n', 0, False) + bit_float(sid)
    sc_.append(scene(sid, body, '\n'.join(sc), css))
    # s3 donut 71
    sid = 's3'; t = wl(3, 'seventyone')
    body = f'<div class="center kk" style="top:320px">SHARE OF THE GROWTH</div>{donut(sid, 71, "SENIOR ROLES")}'
    sc_.append(scene(sid, body, '\n'.join(donut_anim(sid, max(0.05, t), 71) + [out(sid)]), CSS0 + DCSS))
    # s4 donut 37
    sid = 's4'; t = wl(4, 'third')
    body = f'<div class="center kk" style="top:320px">SHARE OF THE GROWTH</div>{donut(sid, 37, "“AI” IN THE TITLE", "#3DDC97")}<div class="src" style="top:1000px">CATEGORIES OVERLAP · SOURCE: INDEED HIRING LAB</div>'
    sc_.append(scene(sid, body, '\n'.join(donut_anim(sid, max(0.05, t - 0.3), 37) + [out(sid)]), CSS0 + DCSS))
    # s5 below pre-pandemic
    sid = 's5'; t_q = wl(5, 'quarter')
    body = f"""<div class="center kk" style="top:340px">TOTAL SOFTWARE POSTINGS</div>
<div class="bars"><div class="bc"><div class="b a" id="{sid}-a"></div><span>Pre-pandemic</span></div><div class="bc"><div class="b n" id="{sid}-b"></div><span>Now</span></div></div>
<div class="center pc" id="{sid}-p">−27.5%</div><div class="src" style="top:1180px">SOURCE: INDEED HIRING LAB (JUL 2026)</div>"""
    css = CSS0 + """.bars { position:absolute; left:220px; top:440px; width:640px; height:520px; display:flex; align-items:flex-end; gap:80px; }
.bc { flex:1; display:flex; flex-direction:column; align-items:center; gap:16px; font:800 36px 'SD Display'; color:var(--ink); } .b { width:100%; border-radius:20px 20px 0 0; transform-origin:bottom; transform:scaleY(0); }
.b.a { height:440px; background:#8C6B5A; } .b.n { height:319px; background:var(--accent); } .pc { top:990px; font:900 120px 'SD Display'; color:var(--red); opacity:0; }"""
    sc = [f'    tl.to("#{sid}-a", {{ scaleY:1, duration:.5, ease:"power3.out" }}, 0.1);', f'    tl.to("#{sid}-b", {{ scaleY:1, duration:.6, ease:"power3.out" }}, 0.4);', slam(f'#{sid}-p', t_q), out(sid)]
    sc_.append(scene(sid, body, '\n'.join(sc), css))
    # s6 not dead, picky
    sid = 's6'; t_d, t_p = wl(6, 'dead'), wl(6, 'picky')
    body = f"""<div class="card" id="{sid}-c" style="top:380px;"><div class="hd"><div class="tile">{icon('doc')}</div><div><div class="lab">JOB BOARD · ILLUSTRATION</div><div class="ttl">Software Engineer</div></div></div>
<div class="req">Senior · AI experience · Ships to production</div></div>
<div class="stamp" id="{sid}-d" style="left:200px; top:780px; border-color:#3DDC97; color:#3DDC97;">NOT DEAD.</div>
<div class="stamp" id="{sid}-p" style="left:320px; top:940px;">PICKY.</div>
{bit(sid, [('n', {'state': 'worried'})])}"""
    css = CSS0 + ".req { font:700 38px 'SD Text'; color:#CDB8AA; padding:10px 6px; }"
    sc = [fly(f'#{sid}-c', 0.02), slam(f'#{sid}-d', t_d - 0.05), slam(f'#{sid}-p', t_p - 0.05), shake(f'#{sid}-c', t_p + 0.1), out(sid)]
    sc += bit_on(sid, 'n', 0, False) + bit_float(sid)
    sc_.append(scene(sid, body, '\n'.join(sc), css))
    # s7 payoff
    sid = 's7'; t_w, t_n = wl(7, 'with'), wl(7, 'next')
    body = f"""<div class="center kk" style="top:320px">THE FASTEST WAY IN</div>
<div class="opt g" id="{sid}-a"><b>✓</b> Build <span>WITH</span> AI</div><div class="opt r" id="{sid}-b"><b>×</b> Just work next to it</div>
<div class="center ft" id="{sid}-f">Ship one real project that uses AI — and show it.</div>
{bit(sid, [('n', {'state': 'normal'}), ('h', {'state': 'happy', 'arms': 'wave'})])}"""
    css = CSS0 + """.opt { position:absolute; left:120px; width:840px; padding:40px; border-radius:34px; font:900 68px 'SD Display'; color:var(--ink); display:flex; align-items:center; gap:28px; opacity:0; background:linear-gradient(180deg,#2C1A13,#1F120C); }
.opt b { width:90px; height:90px; border-radius:45px; display:flex; align-items:center; justify-content:center; font-size:56px; flex:none; }
.opt.g { top:420px; border:4px solid var(--green); } .opt.g b { background:var(--green); color:#0C3B26; } .opt.g span { color:var(--accent); }
.opt.r { top:680px; border:3px solid #3E2217; color:#8C6B5A; font-size:56px; } .opt.r b { background:#2A1912; color:var(--red); }
.ft { top:960px; font:700 40px 'SD Display'; color:var(--ink); opacity:0; }"""
    sc = [fly(f'#{sid}-a', t_w - 0.3, 10, 15), fly(f'#{sid}-b', t_n - 0.2, 10, -15), pop(f'#{sid}-f', t_n + 0.6)]
    sc += bit_on(sid, 'n', 0, False) + bit_float(sid) + bit_on(sid, 'h', t_w)
    sc_.append(scene(sid, body, '\n'.join(sc), css))
    sfx = lambda g: [(0.02, 'type', .5), (g(0, 'up'), 'impact', .8), (S['s1'][0], 'whoosh', .5), (g(1, 'rising'), 'ding', .6), (g(2, 'who'), 'impact', .8),
                     (g(3, 'seventyone'), 'riser', .4), (g(3, 'seventyone') + 0.5, 'pop', .7), (g(4, 'third'), 'pop', .7), (g(5, 'quarter'), 'thud', .8),
                     (g(6, 'dead'), 'impact', .7), (g(6, 'picky'), 'impact', .8), (S['s7'][0], 'whoosh', .5), (g(7, 'with'), 'ding', .7)]
    return sc_, sfx

# =================================================================== job02: India IT freshers vs headcount
BUCKET = """<svg width="520" height="560" viewBox="0 0 260 280"><path d="M40 60 L220 60 L196 250 L64 250 Z" fill="#F3E6DC" stroke="#F87736" stroke-width="8" stroke-linejoin="round"/>
<rect id="BK-w" x="52" y="150" width="156" height="96" fill="#55C2FF" opacity=".75"/><circle cx="150" cy="250" r="10" fill="#0C0704"/></svg>"""
def j2():
    sc_ = []
    sid = 's0'; t_45, t_16 = wl(0, 'fortyfive'), wl(0, 'sixteen')
    body = f"""<div class="box" id="{sid}-a" style="left:90px; top:330px; width:900px; height:300px; text-align:center; padding-top:40px;"><div class="kk">FRESHERS PLANNED · TCS + INFOSYS</div><div class="big" id="{sid}-n1">0</div></div>
<div class="box" id="{sid}-b" style="left:90px; top:700px; width:900px; height:300px; text-align:center; padding-top:40px; border:4px solid #FF3B30;"><div class="kk">TOP 5 IT FIRMS · NET ADDED · 6 MONTHS</div><div class="big" id="{sid}-n2" style="color:#FF3B30">+0</div></div>
<div class="qq" id="{sid}-q">?</div>"""
    css = CSS0 + ".qq { position:absolute; left:0; right:0; text-align:center; top:1030px; font:900 150px 'SD Display'; color:var(--red); opacity:0; }"
    sc = [fly(f'#{sid}-a', 0.02)] + steps(f'#{sid}-n1', t_45 - 0.3, ['~9,000', '~18,000', '~27,000', '~36,000', '~45,000']) + [fly(f'#{sid}-b', t_16 - 0.8)]
    sc += steps(f'#{sid}-n2', t_16 - 0.2, ['+3,200', '+6,400', '+9,600', '+12,800', '+16,055']) + [slam(f'#{sid}-q', t_16 + 0.6), out(sid)]
    sc_.append(scene(sid, body, '\n'.join(sc), css))
    def co(sid, name, line1, badge, tb):
        body = f"""<div class="box" id="{sid}-c" style="left:110px; top:400px; width:860px; height:560px; text-align:center; padding-top:60px;">
<div class="co">{name}</div><div class="big" id="{sid}-n" style="font-size:150px">{line1}</div><div class="kk" style="margin-top:20px">FRESHERS · FY27</div>
{f'<div class="bd" id="{sid}-bd">{badge}</div>' if badge else ''}</div>
<div class="src" style="top:1000px">AS REPORTED BY INDIAN BUSINESS PRESS · TEXT ONLY, NO LOGOS</div>"""
        css = CSS0 + """.co { font:900 90px 'SD Display'; color:var(--ink); letter-spacing:4px; } .bd { display:inline-block; margin-top:30px; padding:16px 30px; border-radius:22px; background:var(--green); color:#0C3B26; font:900 44px 'SD Display'; opacity:0; }"""
        sc = [fly(f'#{sid}-c', 0.02, 20, 20)] + ([pop(f'#{sid}-bd', tb)] if badge else []) + [out(sid)]
        return scene(sid, body, '\n'.join(sc), css)
    sc_.append(co('s1', 'TCS', '~25,000', 'offers made', wl(1, 'offers')))
    sc_.append(co('s2', 'INFOSYS', '~20,000', '8,000+ hired last quarter', wl(2, 'eight')))
    sid = 's3'; t_16 = wl(3, 'sixteen')
    body = f"""<div class="center kk" style="top:380px">TOTAL HEADCOUNT CHANGE · TOP 5 IT FIRMS</div><div class="center big" id="{sid}-n" style="top:470px; font-size:230px">+0</div>
<div class="center kk" style="top:740px">APRIL → SEPTEMBER 2026 (H1 FY27)</div><div class="src" style="top:1000px">SOURCE: BUSINESS STANDARD, OCT 2026</div>
{bit(sid, [('n', {'state': 'normal'}), ('w', {'state': 'worried'})])}"""
    sc = steps(f'#{sid}-n', max(0.05, t_16 - 0.3), ['+2,700', '+5,400', '+8,100', '+10,800', '+13,500', '+16,055']) + [f'    tl.fromTo("#{sid}-n", {{ scale:1 }}, {{ scale:1.1, duration:.18, yoyo:true, repeat:1, immediateRender:false }}, {t_16 + 0.4});', out(sid)]
    sc += bit_on(sid, 'n', 0, False) + bit_float(sid) + bit_on(sid, 'w', t_16 + 0.4)
    sc_.append(scene(sid, body, '\n'.join(sc), CSS0))
    sid = 's4'; t_b, t_p, t_l = wl(4, 'bucket'), wl(4, 'pour'), wl(4, 'leave')
    drops_in = ''.join(f'<i class="din" id="{sid}-i{k}" style="left:{470 + (k % 3) * 40}px"></i>' for k in range(6))
    drops_out = ''.join(f'<i class="dout" id="{sid}-o{k}"></i>' for k in range(6))
    body = f"""<div class="bk" id="{sid}-b">{BUCKET.replace('BK-w', f'{sid}-w')}</div>{drops_in}{drops_out}
<div class="lbl" style="left:120px; top:360px">FRESHERS IN ↓</div><div class="lbl r" style="left:620px; top:1080px">PEOPLE LEAVING ↓</div>"""
    css = CSS0 + """.bk { position:absolute; left:280px; top:440px; opacity:0; } .din, .dout { position:absolute; width:34px; height:46px; border-radius:50% 50% 50% 50% / 60% 60% 40% 40%; background:#55C2FF; opacity:0; }
.din { top:330px; } .dout { left:575px; top:940px; } .lbl { position:absolute; font:900 44px 'SD Display'; color:var(--green); } .lbl.r { color:var(--red); }"""
    sc = [pop(f'#{sid}-b', 0.05)]
    for k in range(6):
        sc.append(f'    tl.fromTo("#{sid}-i{k}", {{ opacity:1, y:0 }}, {{ opacity:0, y:300, duration:.6, ease:"power2.in", immediateRender:false }}, {round(t_p + k * 0.22, 3)});')
        sc.append(f'    tl.fromTo("#{sid}-o{k}", {{ opacity:1, y:0 }}, {{ opacity:0, y:220, duration:.6, ease:"power2.in", immediateRender:false }}, {round(t_l + k * 0.22, 3)});')
    sc += [f'    tl.fromTo("#{sid}-w", {{ y:0 }}, {{ y:-6, duration:.3, yoyo:true, repeat:5, ease:"sine.inOut", immediateRender:false }}, {t_p});', out(sid)]
    sc_.append(scene(sid, body, '\n'.join(sc), css))
    sid = 's5'; t_w = wl(5, 'weak')
    body = f"""<div class="center kk" style="top:360px">IT SERVICES DEMAND</div>
<svg class="gg" width="700" height="400" viewBox="0 0 200 110"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#2A1912" stroke-width="18"/>
<path d="M20 100 A80 80 0 0 1 60 31" fill="none" stroke="#FF3B30" stroke-width="18"/><path d="M60 31 A80 80 0 0 1 140 31" fill="none" stroke="#F87736" stroke-width="18"/><path d="M140 31 A80 80 0 0 1 180 100" fill="none" stroke="#3DDC97" stroke-width="18"/>
<g id="{sid}-nd" style="transform-origin:100px 100px"><path d="M100 100 L100 30" stroke="#F6EEE8" stroke-width="7" stroke-linecap="round"/><circle cx="100" cy="100" r="9" fill="#F6EEE8"/></g></svg>
<div class="center wk" id="{sid}-wk">WEAK</div><div class="src" style="top:1100px">PER COMPANY COMMENTARY, AS REPORTED (OCT 2026)</div>"""
    css = CSS0 + ".gg { position:absolute; left:190px; top:450px; } .wk { top:900px; font:900 120px 'SD Display'; color:var(--red); opacity:0; }"
    sc = [f'    tl.fromTo("#{sid}-nd", {{ rotation:30 }}, {{ rotation:-62, duration:.8, ease:"back.out(1.5)" }}, {max(0.1, t_w - 0.6)});', slam(f'#{sid}-wk', t_w), out(sid)]
    sc_.append(scene(sid, body, '\n'.join(sc), css))
    sid = 's6'; t_o, t_r = wl(6, 'open'), wl(6, 'revolving')
    panels = ''.join(f'<line x1="150" y1="150" x2="{150 + 130 * [1, 0, -1, 0][k]}" y2="{150 + 130 * [0, 1, 0, -1][k]}" stroke="#F87736" stroke-width="10" stroke-linecap="round"/>' for k in range(4))
    body = f"""<div class="center kk" style="top:360px">THE DOOR IS OPEN…</div>
<svg class="rd" width="600" height="600" viewBox="0 0 300 300"><circle cx="150" cy="150" r="135" fill="none" stroke="#3E2217" stroke-width="8" stroke-dasharray="20 14"/><g id="{sid}-g" style="transform-origin:150px 150px">{panels}</g><circle cx="150" cy="150" r="14" fill="#F87736"/></svg>
<div class="center rv" id="{sid}-rv">…BUT IT'S REVOLVING</div>"""
    css = CSS0 + ".rd { position:absolute; left:240px; top:420px; } .rv { top:1050px; font:900 64px 'SD Display'; color:var(--accent); opacity:0; }"
    d = round(S[sid][1] - S[sid][0], 3)
    sc = [f'    tl.fromTo("#{sid}-g", {{ rotation:0 }}, {{ rotation:{int(d * 120)}, duration:{d}, ease:"none" }}, 0);', slam(f'#{sid}-rv', t_r - 0.1), out(sid)]
    sc_.append(scene(sid, body, '\n'.join(sc), css))
    sid = 's7'; t_s, t_c = wl(7, 'step'), wl(7, 'cloud')
    body = f"""<div class="st" id="{sid}-a" style="top:420px"><b>1</b><div>Get in<span>fresher offers are still out there</span></div></div>
<div class="st hot" id="{sid}-b" style="top:700px"><b>2</b><div>AI + cloud skills<span>decide who stays</span></div></div>
{bit(sid, [('n', {'state': 'normal'}), ('h', {'state': 'happy', 'arms': 'wave'})])}"""
    css = CSS0 + """.st { position:absolute; left:110px; width:860px; padding:36px; border-radius:34px; border:2px solid #3E2217; background:linear-gradient(180deg,#2C1A13,#1F120C); display:flex; align-items:center; gap:30px; font:900 64px 'SD Display'; color:var(--ink); opacity:0; }
.st b { width:110px; height:110px; border-radius:55px; background:#3A2318; color:var(--accent); display:flex; align-items:center; justify-content:center; flex:none; }
.st span { display:block; font:600 32px 'SD Text'; color:#CDB8AA; } .st.hot { border:4px solid var(--accent); box-shadow:0 0 60px rgba(248,119,54,.35); } .st.hot b { background:var(--accent); color:#1A0A04; }"""
    sc = [fly(f'#{sid}-a', max(0.05, t_s - 0.3), 10, 15), fly(f'#{sid}-b', t_c - 0.5, 10, -15)]
    sc += bit_on(sid, 'n', 0, False) + bit_float(sid) + bit_on(sid, 'h', t_c)
    sc_.append(scene(sid, body, '\n'.join(sc), css))
    sfx = lambda g: [(0.02, 'whoosh', .5), (g(0, 'fortyfive'), 'riser', .4), (g(0, 'sixteen'), 'impact', .8), (S['s1'][0], 'whoosh', .5), (g(1, 'offers'), 'ding', .5),
                     (S['s2'][0], 'whoosh', .5), (g(2, 'eight'), 'pop', .6), (g(3, 'sixteen') + 0.4, 'impact', .8), (g(4, 'pour'), 'pop', .5), (g(4, 'leave'), 'error', .4),
                     (g(5, 'weak'), 'thud', .8), (S['s6'][0], 'whoosh', .5), (g(6, 'revolving'), 'impact', .6), (g(7, 'cloud'), 'ding', .7)]
    return sc_, sfx

# =================================================================== job03: AI-cited layoffs (Challenger)
def j3():
    sc_ = []
    sid = 's0'; t_t, t_s = wl(0, 'twenty'), wl(0, 'stopped')
    body = f"""<div class="center kk" style="top:380px">US JOB CUTS WHERE COMPANIES CITED AI · 2026</div><div class="center big" id="{sid}-n" style="top:470px; font-size:210px">0</div>
<div class="center sp" id="{sid}-sp">THEN… STOPPED?</div>
{bit(sid, [('n', {'state': 'normal'}), ('g', {'state': 'gasp', 'extra': ['sweat']})])}"""
    css = CSS0 + "  .sp { top:820px; font:900 76px 'SD Display'; color:var(--red); opacity:0; }"
    sc = steps(f'#{sid}-n', max(0.05, t_t - 0.6), ['20,000', '45,000', '70,000', '95,000', '120,000+']) + [slam(f'#{sid}-sp', t_s - 0.1), out(sid)]
    sc += bit_on(sid, 'n', 0, False) + bit_float(sid) + bit_on(sid, 'g', t_s)
    sc_.append(scene(sid, body, '\n'.join(sc), css))
    sid = 's1'; t_tr = wl(1, 'tracks')
    body = f"""<div class="card" id="{sid}-c" style="top:420px;"><div class="hd"><div class="tile">{icon('doc')}</div><div><div class="lab">MONTHLY REPORT</div><div class="ttl">Job Cut Announcements</div></div></div>
<div class="ch">Challenger, Gray &amp; Christmas</div><div class="rows" id="{sid}-r"><span>Company</span><span>Cuts</span><span>Reason</span></div></div>"""
    css = CSS0 + ".ch { font:800 46px 'SD Display'; color:var(--ink); padding:6px; } .rows { display:flex; justify-content:space-between; margin-top:24px; padding:20px; border-radius:18px; background:#0E0806; font:700 32px 'SD Mono'; color:var(--accent); opacity:0; }"
    sc = [fly(f'#{sid}-c', 0.02), pop(f'#{sid}-r', t_tr), out(sid)]
    sc_.append(scene(sid, body, '\n'.join(sc), css))
    sid = 's2'; t_m, t_n = wl(2, 'march'), wl(2, 'number')
    months = ['MAR', 'APR', 'MAY', 'JUN', 'JUL']
    cols = ''.join(f'<div class="mc" id="{sid}-m{k}"><div class="cr">#1</div><div class="bar"></div><span>{m}</span></div>' for k, m in enumerate(months))
    body = f"""<div class="center kk" style="top:360px">TOP REASON GIVEN FOR CUTS</div><div class="cols">{cols}</div><div class="center ai" id="{sid}-ai">AI · #1 FIVE MONTHS RUNNING</div>"""
    css = CSS0 + """.cols { position:absolute; left:90px; right:90px; top:460px; height:480px; display:flex; gap:24px; align-items:flex-end; }
.mc { flex:1; display:flex; flex-direction:column; align-items:center; gap:10px; opacity:0; } .cr { font:900 44px 'SD Display'; color:var(--accent); } .bar { width:100%; height:300px; border-radius:16px; background:var(--accent); }
.mc span { font:800 34px 'SD Display'; color:var(--ink); } .ai { top:1000px; font:900 54px 'SD Display'; color:var(--accent); opacity:0; }"""
    sc = [pop(f'#{sid}-m{k}', round(max(0.05, t_m - 0.2) + k * 0.15, 3)) for k in range(5)] + [pop(f'#{sid}-ai', t_n), out(sid)]
    sc_.append(scene(sid, body, '\n'.join(sc), css))
    sid = 's3'; t_f = wl(3, 'fourth')
    ranks = ['Restructuring', '…', '…', 'AI']
    rows = ''.join(f'<div class="rk{" ai" if k == 3 else ""}" id="{sid}-r{k}"><b>{k + 1}</b>{r}</div>' for k, r in enumerate(ranks))
    body = f"""<div class="center kk" style="top:340px">AUGUST 2026 · TOP REASONS</div><div class="lst">{rows}</div><div class="aitag" id="{sid}-t">AI</div>
<div class="src" style="top:1080px">SOURCE: CHALLENGER, GRAY &amp; CHRISTMAS, AUGUST 2026 REPORT</div>"""
    css = CSS0 + """.lst { position:absolute; left:150px; right:150px; top:420px; } .rk { height:120px; margin:16px 0; border-radius:26px; border:2px solid #3E2217; background:linear-gradient(90deg,#2C1A13,#1F120C); display:flex; align-items:center; gap:28px; padding:0 30px; font:900 52px 'SD Display'; color:var(--ink); }
.rk b { width:80px; height:80px; border-radius:40px; background:#3A2318; color:var(--accent); display:flex; align-items:center; justify-content:center; } .rk.ai { border:4px solid var(--red); color:var(--red); opacity:0; }
.aitag { position:absolute; left:330px; top:436px; padding:20px 40px; border-radius:22px; background:var(--red); color:#fff; font:900 60px 'SD Display'; }"""
    sc = [pop(f'#{sid}-r{k}', 0.05 + k * 0.08, 10) for k in range(3)]
    sc += [f'    tl.to("#{sid}-t", {{ y:410, duration:.6, ease:"bounce.out" }}, {max(0.3, t_f - 0.5)});', f'    tl.to("#{sid}-t", {{ opacity:0, duration:.1 }}, {t_f + 0.15});', pop(f'#{sid}-r3', t_f + 0.1), out(sid)]
    sc_.append(scene(sid, body, '\n'.join(sc), css))
    sid = 's4'; t_m = wl(4, 'market')
    body = f"""<div class="center kk" style="top:380px">NOW THE TOP REASON</div><div class="nw" id="{sid}-c"><div class="cr">#1</div>Market &amp;<br>economic conditions</div>"""
    css = CSS0 + ".nw { position:absolute; left:120px; width:840px; top:470px; padding:60px 40px; border-radius:40px; border:4px solid var(--accent); background:linear-gradient(180deg,#2C1A13,#1F120C); text-align:center; font:900 76px 'SD Display'; color:var(--ink); line-height:1.05; } .nw .cr { font-size:90px; color:var(--accent); }"
    sc = [fly(f'#{sid}-c', max(0.05, t_m - 0.4)), out(sid)]
    sc_.append(scene(sid, body, '\n'.join(sc), css))
    sid = 's5'; t_ne = wl(5, 'not')
    body = f"""<div class="center q" id="{sid}-q">Did AI stop<br>replacing jobs?</div><div class="stamp" id="{sid}-s" style="left:190px; top:820px;">NOT EXACTLY.</div>
{bit(sid, [('n', {'state': 'normal'}), ('w', {'state': 'worried', 'extra': ['uhoh']})])}"""
    css = CSS0 + ".q { top:420px; font:900 96px 'SD Display'; color:var(--ink); line-height:1.05; }"
    sc = [pop(f'#{sid}-q', 0.05), slam(f'#{sid}-s', t_ne - 0.05), out(sid)]
    sc += bit_on(sid, 'n', 0, False) + bit_float(sid) + bit_on(sid, 'w', t_ne)
    sc_.append(scene(sid, body, '\n'.join(sc), css))
    sid = 's6'; t_pr, t_tr, t_h = wl(6, 'progress'), wl(6, 'trouble'), wl(6, 'headlines')
    body = f"""<div class="mk g" id="{sid}-a"><b>“AI”</b><span>sounds like progress</span></div><div class="mk r" id="{sid}-b"><b>“The economy”</b><span>sounds like trouble</span></div>
<div class="center hl" id="{sid}-h">The story can change with the headlines</div>"""
    css = CSS0 + """.mk { position:absolute; left:120px; width:840px; padding:40px; border-radius:34px; background:linear-gradient(180deg,#2C1A13,#1F120C); text-align:center; opacity:0; }
.mk b { display:block; font:900 84px 'SD Display'; color:var(--ink); } .mk span { font:700 40px 'SD Text'; } .mk.g { top:380px; border:4px solid var(--green); } .mk.g span { color:var(--green); }
.mk.r { top:690px; border:4px solid var(--red); } .mk.r span { color:var(--red); } .hl { top:1010px; font:700 40px 'SD Display'; color:var(--ink); opacity:0; }"""
    sc = [fly(f'#{sid}-a', max(0.05, t_pr - 0.6), 10, 15), fly(f'#{sid}-b', t_tr - 0.5, 10, -15), pop(f'#{sid}-h', t_h - 0.6), out(sid)]
    sc_.append(scene(sid, body, '\n'.join(sc), css))
    sid = 's7'; t_r, t_w = wl(7, 'reason'), wl(7, 'whos')
    body = f"""<div class="card" id="{sid}-c" style="top:340px;"><div class="hd"><div class="tile">{icon('doc')}</div><div><div class="lab">HEADLINE · ILLUSTRATION</div><div class="ttl">Company cuts 5,000 jobs, citing AI</div></div></div></div>
<div class="ck" id="{sid}-a" style="top:640px"><b>✓</b> Check the reason</div><div class="ck" id="{sid}-b" style="top:830px"><b>✓</b> Check who's saying it</div>
{bit(sid, [('n', {'state': 'scan'}), ('h', {'state': 'happy', 'arms': 'wave'})])}"""
    css = CSS0 + """.ttl { white-space:normal; font-size:50px; } .ck { position:absolute; left:120px; width:840px; padding:34px 40px; border-radius:30px; border:3px solid var(--green); background:linear-gradient(180deg,#2C1A13,#1F120C); display:flex; align-items:center; gap:26px; font:900 58px 'SD Display'; color:var(--ink); opacity:0; }
.ck b { width:80px; height:80px; border-radius:40px; background:var(--green); color:#0C3B26; display:flex; align-items:center; justify-content:center; flex:none; }"""
    sc = [fly(f'#{sid}-c', 0.02), pop(f'#{sid}-a', t_r - 0.2), pop(f'#{sid}-b', t_w - 0.2)]
    sc += bit_on(sid, 'n', 0, False) + bit_float(sid) + bit_on(sid, 'h', t_w)
    sc_.append(scene(sid, body, '\n'.join(sc), css))
    sfx = lambda g: [(0.02, 'whoosh', .5), (g(0, 'twenty') - 0.6, 'riser', .4), (g(0, 'stopped'), 'impact', .9), (S['s1'][0], 'whoosh', .5), (g(1, 'tracks'), 'type', .5),
                     (g(2, 'march'), 'tick', .6), (g(2, 'number'), 'ding', .6), (g(3, 'fourth') - 0.5, 'whoosh', .5), (g(3, 'fourth') + 0.1, 'thud', .8),
                     (g(4, 'market'), 'impact', .6), (g(5, 'not'), 'impact', .8), (g(6, 'progress'), 'pop', .6), (g(6, 'trouble'), 'pop', .6),
                     (S['s7'][0], 'whoosh', .5), (g(7, 'reason'), 'ding', .6), (g(7, 'whos'), 'ding', .6)]
    return sc_, sfx

if __name__ == '__main__':
    scenes, sfx = {'job01': j1, 'job02': j2, 'job03': j3}[JOB]()
    L.sfx_list = lambda: sorted(sfx(lambda i, w: S[f's{i}'][0] + wl(i, w)))
    comp = L.P / 'compositions'; comp.mkdir(parents=True, exist_ok=True)
    for f in comp.glob('*.html'): f.unlink()
    for i, html in enumerate(scenes):
        (comp / f's{i}.html').write_text(html)
    (comp / 'bg.html').write_text(L.bg())
    (comp / 'caps.html').write_text(L.captions())
    (L.P / 'index.html').write_text(L.index())
    print('written', L.P, L.DUR)
