"""ep04 long video "Will AI Replace Software Engineers?" (16:9). Reuses the long-video engine (hf_ep01_long), the ep02 topic
scenes and the ep03 scenes, and adds: a self-typing code editor with an AI-share counter (and a vulnerability-scan mode),
a "75%" fine-print breakdown, a decades line chart, a career ladder whose bottom rung falls, twin stat cards, a speed race,
skill cards, a portfolio comparison and a comment poll.
Usage: THEME=cream GRID=<pattern> python3 tools/hf_ep04_long.py"""
import os, sys
from pathlib import Path
os.environ['EPID'] = 'ep04'
sys.path.insert(0, str(Path(__file__).resolve().parent))
import hf_ep03_long as Y   # noqa: E402  (registers the ep02 + ep03 scene types)
X = Y.X; B = Y.B
E, icon, CARD = B.E, X.icon, X.CARD
wf, pop, fly, fade, shake = B.wfrac, B.pop, B.fly, B.fade, B.shake
bitb = Y.bitb
WHITE = 'background:#FFFFFF; border-radius:30px; box-shadow:0 30px 70px rgba(90,50,20,.2);'

CODE = ['def checkout(cart, user):', '    total = sum(i.price for i in cart)', '    if user.coupon:', '        total *= 0.9',
        '    tax = round(total * 0.18, 2)', '    order = Order(user, cart, total + tax)', '    db.save(order)', '    return order']
VULN = ['def login(name, password):', '    q = "SELECT * FROM users WHERE name=\'" + name + "\'"', '    user = db.run(q)',
        '    if user.password == password:', '        page = "<h1>Welcome " + name + "</h1>"', '        return page']

def t_editor(i, sid, v):
    lines = VULN if v['mode'] == 'vuln' else CODE
    rows = ''.join(f'<div class="el" id="{sid}-l{k}"><i>{k + 1}</i><span>{E(x)}</span></div>' for k, x in enumerate(lines))
    if v['mode'] == 'vuln':
        side = (f'<div class="tg" id="{sid}-t0" style="top:150px">⚠ SQL injection</div><div class="tg" id="{sid}-t1" style="top:300px">⚠ Cross-site scripting</div>'
                f'<div class="pc" id="{sid}-pc"><b>45%</b><span>of tasks had a<br>security flaw</span></div>')
    else:
        side = (f'<div class="pc" id="{sid}-pc"><small>{E(v["label"])}</small><b><i class="nn" id="{sid}-n">{v["from"]}</i>%</b>'
                f'<div class="pb"><i id="{sid}-bar" style="width:{v["from"]}%"></i></div><span id="{sid}-y">2024 → 2026</span></div>')
    body = f"""<div class="ed" id="{sid}-e"><div class="eb"><i></i><i></i><i></i><span>{"login.py" if v["mode"] == "vuln" else "checkout.py"} · ILLUSTRATION</span>
<em id="{sid}-ai">✦ AI suggesting…</em></div><div class="ec">{rows}</div><div class="mg" id="{sid}-m">🔍</div></div>{side}"""
    css = """.ed { position:absolute; left:40px; top:40px; width:820px; height:600px; border-radius:26px; background:#1E1A24; box-shadow:0 30px 80px rgba(60,30,10,.35); overflow:hidden; }
.eb { height:58px; background:#2A2533; display:flex; align-items:center; gap:10px; padding:0 22px; font:700 20px 'SD Mono'; color:#A59DB3; }
.eb i { width:16px; height:16px; border-radius:8px; background:#FF5F57; } .eb i:nth-child(2) { background:#FEBC2E; } .eb i:nth-child(3) { background:#28C840; }
.eb span { margin-left:14px; } .eb em { margin-left:auto; font-style:normal; color:#F87736; }
.ec { padding:26px 20px; } .el { display:flex; gap:22px; font:600 25px 'SD Mono'; color:#E8E2F0; line-height:1.9; white-space:pre; opacity:0; }
.el i { font-style:normal; width:30px; text-align:right; color:#6B6378; }
.mg { position:absolute; left:40px; top:120px; font-size:90px; opacity:0; }
.pc { position:absolute; left:900px; top:150px; width:380px; padding:34px; """ + WHITE + """ text-align:center; }
.pc small { display:block; font:800 18px 'SD Mono'; letter-spacing:1px; color:#8C6B5A; line-height:1.4; } .pc b { display:block; font:900 140px 'SD Display'; color:#F87736; line-height:1.1; }
.pc span { font:700 30px 'SD Display'; color:#2A2018; } .pc .nn { font-style:normal; } .pb { height:20px; border-radius:10px; background:#F3E6DC; margin:10px 0 16px; overflow:hidden; } .pb i { display:block; height:100%; background:#F87736; border-radius:10px; }
.tg { position:absolute; left:640px; padding:16px 26px; border-radius:18px; background:#FF3B30; color:#fff; font:900 32px 'SD Display'; opacity:0; transform:rotate(3deg); box-shadow:0 16px 40px rgba(255,59,48,.35); }"""
    n = len(lines)
    sc = [fly(f'#{sid}-e', 0.05, 8, 10)]
    sc += [f'    tl.fromTo("#{sid}-l{k}", {{ opacity:0, x:-30 }}, {{ opacity:1, x:0, duration:.18 }}, {round(0.3 + k * 0.32, 2)});' for k in range(n)]
    if v['mode'] == 'vuln':
        t = wf(i, 0.4)
        sc += [f'    tl.fromTo("#{sid}-m", {{ opacity:1, x:0, y:0 }}, {{ x:560, y:200, duration:1.6, ease:"sine.inOut" }}, {t});',
               f'    tl.to("#{sid}-l1", {{ backgroundColor:"rgba(255,59,48,.25)", duration:.2 }}, {round(t + 0.6, 2)});', pop(f'#{sid}-t0', round(t + 0.6, 2)),
               f'    tl.to("#{sid}-l4", {{ backgroundColor:"rgba(255,59,48,.25)", duration:.2 }}, {round(t + 1.3, 2)});', pop(f'#{sid}-t1', round(t + 1.3, 2)),
               pop(f'#{sid}-pc', wf(i, 0.2)), shake(f'#{sid}-e', round(t + 1.4, 2))]
    else:
        t = wf(i, 0.15)
        sc += [pop(f'#{sid}-pc', 0.2),
               f'    tl.fromTo("#{sid}-n", {{ innerText:{v["from"]} }}, {{ innerText:{v["to"]}, snap:{{ innerText:1 }}, duration:2.2, ease:"power2.inOut" }}, {t});',
               f'    tl.fromTo("#{sid}-bar", {{ width:"{v["from"]}%" }}, {{ width:"{v["to"]}%", duration:2.2, ease:"power2.inOut" }}, {t});',
               f'    tl.fromTo("#{sid}-ai", {{ opacity:.3 }}, {{ opacity:1, duration:.4, yoyo:true, repeat:9, immediateRender:false }}, 0.3);']
    return body, sc, css

def t_fine(i, sid, v):
    tags = ''.join(f'<div class="ft" id="{sid}-t{k}" style="left:{100 + k * 400}px">{E(x)}</div>' for k, x in enumerate(v['tags']))
    body = f"""<div class="center fb" id="{sid}-b" style="top:40px">{E(v['big'])}</div><div class="fl" id="{sid}-ln"></div>{tags}
{bitb(sid, [('a', {'state': 'happy'})], 120, 470, 200)}<div class="ok" id="{sid}-ok">✓ APPROVE</div>"""
    css = """.fb { font:900 260px 'SD Display'; color:#F87736; line-height:1; } .fl { position:absolute; left:160px; right:160px; top:330px; height:4px; background:#E6D5C6; transform:scaleX(0); }
.ft { position:absolute; top:360px; width:340px; padding:22px; border-radius:22px; background:#FFFFFF; box-shadow:0 20px 50px rgba(90,50,20,.15); font:800 36px 'SD Display'; color:#2A2018; text-align:center; opacity:0; }
.ft:nth-of-type(3) { } .ok { position:absolute; left:860px; top:560px; padding:22px 44px; border-radius:40px; background:#3DDC97; color:#0E3B26; font:900 44px 'SD Display'; opacity:0; }"""
    sc = [f'    tl.fromTo("#{sid}-b", {{ opacity:0, scale:1.6, filter:"blur(14px)" }}, {{ opacity:1, scale:1, filter:"blur(0px)", duration:.4, ease:"expo.out" }}, 0.05);',
          f'    tl.to("#{sid}-ln", {{ scaleX:1, duration:.5 }}, {wf(i, 0.2)});']
    sc += [pop(f'#{sid}-t{k}', wf(i, 0.25 + k * 0.2)) for k in range(len(v['tags']))]
    sc += B.bit_on(sid, 'a', wf(i, 0.55)) + B.bit_float(sid, wf(i, 0.55)) + [pop(f'#{sid}-ok', wf(i, 0.75)),
          f'    tl.fromTo("#{sid}-ok", {{ scale:1 }}, {{ scale:.9, duration:.1, yoyo:true, repeat:1, immediateRender:false }}, {round(wf(i, 0.75) + 0.5, 2)});']
    return body, sc, css

def t_decades(i, sid, v):
    pts = [(120, 560), (330, 520), (540, 450), (750, 380), (960, 270), (1170, 130)]
    labs = ['1950s FORTRAN', 'PCs', 'Internet', 'Smartphones', 'Cloud', 'AI?']
    d = 'M' + ' L'.join(f'{x} {y}' for x, y in pts)
    dots = ''.join(f'<div class="dd" id="{sid}-d{k}" style="left:{x - 14}px; top:{y - 14}px"></div><div class="dl2" id="{sid}-l{k}" style="left:{x - 110}px; top:{y + 26 if k < 5 else y - 70}px">{E(labs[k])}</div>'
                   for k, (x, y) in enumerate(pts))
    body = f"""<div class="kick" style="position:absolute; left:120px; top:40px">PROGRAMMERS WORLDWIDE · ILLUSTRATION</div>
<svg class="ch" width="1320" height="720" viewBox="0 0 1320 720"><path d="M100 600 H1240" stroke="#E6D5C6" stroke-width="4"/>
<path id="{sid}-p" d="{d}" fill="none" stroke="#F87736" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1400" stroke-dashoffset="1400"/></svg>{dots}"""
    css = """.ch { position:absolute; left:0; top:0; } .dd { position:absolute; width:28px; height:28px; border-radius:14px; background:#FFFFFF; border:6px solid #F87736; opacity:0; }
.dl2 { position:absolute; width:220px; text-align:center; font:800 30px 'SD Display'; color:#2A2018; opacity:0; }"""
    sc = [f'    tl.to("#{sid}-p", {{ strokeDashoffset:0, duration:{round(X.dur(sid) * 0.8, 2)}, ease:"none" }}, 0.2);']
    for k in range(6):
        t = round(0.2 + X.dur(sid) * 0.8 * k / 5, 2)
        sc += [pop(f'#{sid}-d{k}', t, 10), pop(f'#{sid}-l{k}', round(t + 0.1, 2), 10)]
    return body, sc, css

def t_ladder(i, sid, v):
    now = v.get('mode') == 'now'
    rungs = ''.join(f'<div class="rg{" low" if k == 4 else ""}" id="{sid}-r{k}" style="top:{90 + k * 115}px"><span>{E(t)}</span></div>'
                    for k, t in enumerate(['Architect', 'Senior engineer', 'Mid-level engineer', 'Junior engineer', 'First job: simple tickets']))
    side = ('<div class="lt" id="{0}-t"><b>AI takes:</b><span>boilerplate</span><span>simple tickets</span><span>small bug fixes</span></div>'.format(sid) if not now
            else f'<div class="lt" id="{sid}-t"><b>Changing now:</b><span>who gets hired</span><span>what they do</span></div>')
    body = f"""<div class="rl" style="left:220px"></div><div class="rl" style="left:760px"></div>{rungs}{side}
{bitb(sid, [('a', {'state': 'scan', 'extra': ['laser']})], 1000, 470, 220)}"""
    css = """.rl { position:absolute; top:40px; width:22px; height:660px; border-radius:11px; background:#C9A98E; }
.rg { position:absolute; left:200px; width:600px; height:70px; border-radius:18px; background:#FFFFFF; box-shadow:0 12px 30px rgba(90,50,20,.15); display:flex; align-items:center; justify-content:center; font:800 32px 'SD Display'; color:#2A2018; }
.rg.low { background:#FFE3DC; color:#D93025; border:3px dashed #FF3B30; }
.lt { position:absolute; left:880px; top:110px; width:400px; padding:28px; """ + WHITE + """ display:flex; flex-direction:column; gap:10px; font:800 34px 'SD Display'; color:#2A2018; }
.lt b { color:#F87736; font-size:30px; letter-spacing:1px; } .lt span:before { content:'✕ '; color:#FF3B30; }"""
    sc = [fade(f'#{sid}-r{k}', round(0.05 + k * 0.08, 2), -60) for k in range(5)] + [pop(f'#{sid}-t', wf(i, 0.3))]
    sc += B.bit_on(sid, 'a', 0, False) + B.bit_float(sid)
    t = wf(i, 0.25 if not now else 0.6)
    sc += [shake(f'#{sid}-r4', t), f'    tl.to("#{sid}-r4", {{ y:260, rotation:-14, opacity:0, duration:.8, ease:"power3.in" }}, {round(t + 0.4, 2)});']
    return body, sc, css

def t_twin(i, sid, v):
    def card(k, d, x):
        fs = 120 if len(d[0]) <= 6 else 92
        return f'<div class="tw" id="{sid}-c{k}" style="left:{x}px"><b style="font-size:{fs}px; color:{"#3DDC97" if k == 0 else "#F87736"}">{E(d[0])}</b><span>{E(d[1])}</span></div>'
    body = f"""<div class="center kick" style="top:60px">{E(v['title'])}</div>{card(0, v['a'], 150)}{card(1, v['b'], 720)}
<div class="center csrc" style="top:640px">{E(v.get('src', ''))}</div>"""
    css = """.tw { position:absolute; top:170px; width:450px; height:380px; """ + WHITE + """ display:flex; flex-direction:column; align-items:center; justify-content:center; gap:14px; }
.tw b { font:900 120px 'SD Display'; line-height:1; white-space:nowrap; } .tw span { font:800 40px 'SD Display'; color:#2A2018; text-align:center; padding:0 20px; }
.csrc { font:600 22px 'SD Text'; color:var(--dim); letter-spacing:1px; }"""
    sc = [fly(f'#{sid}-c0', 0.1, 8, 14), fly(f'#{sid}-c1', wf(i, 0.35), 8, -14)]
    return body, sc, css

def t_race(i, sid, v):
    act = v['stage'] == 'actual'
    body = f"""<div class="center kick" style="top:40px">{"MEASURED RESULT" if act else "WHAT DEVELOPERS EXPECTED"} · METR 2025</div>
<div class="ln" style="top:170px"><span>Without AI</span><div class="tr"><i id="{sid}-a" style="background:#C9A98E"></i></div></div>
<div class="ln" style="top:340px"><span>With AI</span><div class="tr"><i id="{sid}-b" style="background:{"#FF3B30" if act else "#3DDC97"}"></i></div></div>
<div class="rv" id="{sid}-v" style="color:{"#FF3B30" if act else "#1F9D63"}">{"19% SLOWER" if act else "24% FASTER?"}</div>
<div class="sw" id="{sid}-sw">⏱</div>"""
    css = """.ln { position:absolute; left:100px; width:1120px; display:flex; align-items:center; gap:30px; font:800 40px 'SD Display'; color:#2A2018; }
.ln span { width:240px; } .tr { flex:1; height:90px; border-radius:45px; background:#FFFFFF; box-shadow:0 12px 30px rgba(90,50,20,.12); overflow:hidden; } .tr i { display:block; height:100%; width:0; border-radius:45px; }
.rv { position:absolute; left:0; right:0; top:500px; text-align:center; font:900 110px 'SD Display'; opacity:0; } .sw { position:absolute; left:1160px; top:40px; font-size:90px; }"""
    a, b = (100, 81) if act else (80, 100)
    sc = [f'    tl.fromTo("#{sid}-a", {{ width:"0%" }}, {{ width:"{a}%", duration:2.2, ease:"power1.inOut" }}, 0.3);',
          f'    tl.fromTo("#{sid}-b", {{ width:"0%" }}, {{ width:"{b}%", duration:2.2, ease:"power1.inOut" }}, 0.3);',
          f'    tl.fromTo("#{sid}-sw", {{ rotation:-10 }}, {{ rotation:10, duration:.2, yoyo:true, repeat:9, immediateRender:false }}, 0.3);',
          pop(f'#{sid}-v', 2.6)] + ([shake(f'#{sid}-v', 2.9)] if act else [])
    return body, sc, css

SKILLS = [('chat', 'Understanding what the customer really needs'), ('globe', 'Designing systems that survive a million users'),
          ('shield', 'Judging if AI code is secure and right'), ('warn', 'Owning it when things break at 2 AM')]
def t_skill(i, sid, v):
    k0 = v['k']
    cards = ''.join(f'<div class="sk{" on" if k == k0 else " done" if k < k0 else ""}" id="{sid}-c{k}" style="left:{40 + k * 315}px">{icon(ic, 80)}<span>{E(t)}</span></div>'
                    for k, (ic, t) in enumerate(SKILLS))
    body = f'<div class="center kick" style="top:60px">WHAT AI CAN\'T TAKE (YET)</div>{cards}'
    css = """.sk { position:absolute; top:170px; width:290px; height:420px; border-radius:30px; background:#FFFFFF; box-shadow:0 20px 50px rgba(90,50,20,.12); opacity:.35;
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:26px; padding:24px; text-align:center; font:800 32px 'SD Display'; color:#2A2018; }
.sk.done { opacity:.8; } .sk.on { opacity:1; border:4px solid #F87736; box-shadow:0 0 60px rgba(248,119,54,.35); }"""
    sc = [f'    tl.fromTo("#{sid}-c{k0}", {{ y:60, scale:.9 }}, {{ y:-20, scale:1.06, duration:.5, ease:"back.out(2)" }}, 0.1);']
    return body, sc, css

def t_portfolio(i, sid, v):
    body = f"""<div class="pf" id="{sid}-a" style="left:90px"><div class="pt">🏅 Certificate</div><div class="pl">Completed course</div><div class="pl">No users</div></div>
<div class="pf hi" id="{sid}-b" style="left:690px"><div class="pt">🚀 Live app</div><div class="pl">✓ 200 real users</div><div class="pl">✓ Bugs found and fixed</div><div class="pl">✓ Clear write-up</div></div>
<div class="center csrc" style="top:640px">Example portfolio · illustration</div>"""
    css = """.pf { position:absolute; top:110px; width:540px; height:460px; """ + WHITE + """ padding:40px; }
.pf.hi { border:4px solid #3DDC97; } .pt { font:900 58px 'SD Display'; color:#2A2018; margin-bottom:26px; } .pl { font:700 36px 'SD Display'; color:#5C4337; margin:16px 0; }
.csrc { font:600 22px 'SD Text'; color:var(--dim); letter-spacing:1px; }"""
    sc = [fly(f'#{sid}-a', 0.1, 8, 12), fly(f'#{sid}-b', wf(i, 0.3), 8, -12), f'    tl.to("#{sid}-a", {{ opacity:.35, scale:.92, duration:.4 }}, {wf(i, 0.6)});',
          f'    tl.fromTo("#{sid}-b", {{ scale:1 }}, {{ scale:1.05, duration:.25, yoyo:true, repeat:1, immediateRender:false }}, {wf(i, 0.65)});']
    return body, sc, css

def t_poll(i, sid, v):
    opts = [('😀', 'Easier', 64), ('😩', 'Harder', 21), ('🤷', "Don't use it yet", 15)]
    rows = ''.join(f'<div class="po" id="{sid}-o{k}"><b>{e}</b><span>{E(t)}</span></div>' for k, (e, t, p) in enumerate(opts))
    body = f"""<div class="pq">💬 Do you use AI at work?</div><div class="pw">{rows}</div><div class="center csrc" style="top:650px">👇 Tell me in the comments</div>"""
    css = """.pq { position:absolute; left:120px; top:50px; font:900 70px 'SD Display'; color:#2A2018; } .pw { position:absolute; left:120px; top:200px; } .po { position:relative; width:1080px; margin-bottom:24px; height:110px; """ + WHITE + """
  display:flex; align-items:center; gap:24px; padding:0 30px; font:800 40px 'SD Display'; color:#2A2018; overflow:hidden; }
.po b { font-size:56px; z-index:1; } .po span { z-index:1; } .pbar { position:absolute; inset:0; } .pbar i { display:block; height:100%; background:rgba(248,119,54,.15); transform-origin:left; transform:scaleX(0); }
.csrc { font:800 34px 'SD Display'; color:var(--accent); }"""
    sc = [pop(f'#{sid}-o{k}', round(0.2 + k * 0.25, 2)) for k in range(3)]
    return body, sc, css

B.T.update({'editor': t_editor, 'fine': t_fine, 'decades': t_decades, 'ladder': t_ladder, 'twin': t_twin, 'race': t_race,
            'skill': t_skill, 'portfolio': t_portfolio, 'poll': t_poll})
B.SFX_BY_TYPE.update({'editor': [(0.3, 'type', .45), (1.5, 'type', .4)], 'fine': [(0.05, 'thud', .5), (1.5, 'pop', .4)],
                      'decades': [(0.2, 'whoosh', .4)], 'ladder': [(0.05, 'pop', .4), (1.8, 'error', .45)], 'twin': [(0.1, 'pop', .45), (1.5, 'pop', .45)],
                      'race': [(0.3, 'whoosh', .5), (2.6, 'ding', .5)], 'skill': [(0.1, 'pop', .45)], 'portfolio': [(0.1, 'whoosh', .4), (1.5, 'ding', .45)],
                      'poll': [(0.2, 'pop', .4), (1.0, 'pop', .4)]})

if __name__ == '__main__':
    import json
    P, BE, S = B.P, B.BE, B.S
    comp = P / 'compositions'; comp.mkdir(parents=True, exist_ok=True)
    for f in comp.glob('*.html'):
        f.unlink()
    for i in range(len(BE)):
        (comp / f'b{i:02d}.html').write_text(B.beat_scene(i))
    (comp / 'bg.html').write_text(B.bg())
    (comp / 'chapters.html').write_text(B.chapters())
    G = list(enumerate(B.caption_groups()))
    B.CAPPARTS = []
    for part in range(0, len(G), 40):
        chunk = G[part:part + 40]
        (comp / f'caps{len(B.CAPPARTS)}.html').write_text(B.captions(chunk, len(B.CAPPARTS)))
        B.CAPPARTS.append((chunk[0][1][0][1], chunk[-1][1][-1][2]))
    (B.P / 'index.html').write_text(B.index())
    (B.P / 'assets/plan.json').write_text(json.dumps({'dur': B.DUR, 'provisional': B.PROVISIONAL,
                                                     'chapters': [(S[f"b{i:02d}"][0], t) for i, t in B.CHAPTERS]}, indent=1))
    print('written', len(BE), 'beats', B.DUR, 's', 'PROVISIONAL timing' if B.PROVISIONAL else 'real timing')
