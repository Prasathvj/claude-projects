"""mh01: TECH MYSTERIES · CASE 002 Short (MH370: the plane only a satellite could hear). Vertical 1080x1920.
Built on the vertical Short helpers (hf_news01_short) + Tech Mysteries kit (kit_myst: typer, file, clue, grain/scanlines overlay).
Usage: STYLE=mystery THEME=navy CASE=002 python3 tools/hf_mh01_short.py   then  python3 tools/max_plan.py mh01-short 1.4"""
import json, math, os, re, shutil, subprocess, sys
from pathlib import Path
os.environ['SHORT_ID'] = 'mh01-short'
os.environ.setdefault('STYLE', 'mystery'); os.environ.setdefault('THEME', 'navy'); os.environ.setdefault('CASE', '002')
sys.path.insert(0, str(Path(__file__).resolve().parent))
import hf_news01_short as L   # noqa: E402
from hf_news01_short import S, BE, wl, pop, slam, shake, ring, out, scene, E, DUR, W, H, ROOT, P  # noqa: E402
import kit_myst as M   # noqa: E402

RED, INK, DIM, BLUE, GREEN = '#E5383B', '#E8EDF5', '#8FA3C2', '#9FC3FF', '#3DDC97'
CSS = M.CSS + """
.ctr { position:absolute; left:40px; right:40px; text-align:center; }
.lbl { font:700 28px 'SD Mono'; letter-spacing:6px; color:#8FA3C2; }
.big { font:900 120px 'SD Display'; color:#E8EDF5; letter-spacing:-2px; line-height:1; }
.mid { font:900 76px 'SD Display'; color:#E8EDF5; line-height:1.05; }
.mono { font-family:'SD Mono'; }
.red { color:#E5383B; } .blu { color:#9FC3FF; } .grn { color:#3DDC97; }
.panel { position:absolute; background:#0F1726; border:2px solid #26324A; border-radius:22px; box-shadow:0 30px 80px rgba(0,0,0,.65); }
.chip { position:absolute; padding:10px 22px; border-radius:12px; font:700 26px 'SD Mono'; letter-spacing:4px; white-space:nowrap; }
.chip.r { background:#E5383B; color:#fff; } .chip.d { border:2px solid #45577A; color:#8FA3C2; }
.ill { position:absolute; left:0; right:0; text-align:center; font:700 20px 'SD Mono'; letter-spacing:5px; color:#5A6E91; }
.stampx { position:absolute; padding:10px 34px; border:10px solid #E5383B; color:#E5383B; font:900 84px 'SD Display'; letter-spacing:6px; transform:rotate(-9deg); white-space:nowrap; opacity:0; background:rgba(8,12,20,.55); }
"""
PLANE = ('<svg width="{w}" height="{w}" viewBox="0 0 100 100"><path d="M50 4 C54 4 55 10 55 16 L55 38 L92 58 L92 66 L55 56 L55 80 L66 88 L66 94 L50 90 L34 94 L34 88 L45 80 L45 56 L8 66 L8 58 L45 38 L45 16 C45 10 46 4 50 4 Z" fill="{c}"/></svg>')
def plane(w=80, c=INK): return PLANE.format(w=w, c=c)
SAT = ('<svg width="{w}" height="{h}" viewBox="0 0 220 130"><rect x="86" y="40" width="48" height="50" rx="6" fill="#C3CEE0"/><rect x="92" y="48" width="36" height="8" fill="#8FA3C2"/>'
       '<rect x="6" y="50" width="74" height="30" fill="#26406B" stroke="#9FC3FF" stroke-width="2"/><rect x="140" y="50" width="74" height="30" fill="#26406B" stroke="#9FC3FF" stroke-width="2"/>'
       '<path d="M6 65h74M140 65h74M24 50v30M42 50v30M60 50v30M158 50v30M176 50v30M194 50v30" stroke="#9FC3FF" stroke-width="1.5"/>'
       '<path d="M110 40 L110 22" stroke="#C3CEE0" stroke-width="4"/><path d="M92 22 Q110 2 128 22 Z" fill="#E8EDF5"/><circle cx="110" cy="96" r="5" fill="#E5383B"/></svg>')
def sat(w=220): return SAT.format(w=w, h=int(w * 130 / 220))

def T(i, w, nth=0): return wl(i, w, nth)
def mk(i, body, sc, css='', punch=True):
    sid = f's{i}'
    sc = [y for x in sc for y in (x if isinstance(x, list) else [x])]
    head = [L.punch(sid)] if punch else []
    return scene(sid, f'<div id="{sid}-all" class="all">{body}</div>', '\n'.join(head + sc + [out(sid)]), CSS + css)
def tw(sel, t, frm, to, d=.4, ease='power2.out'):
    return f'    tl.fromTo("{sel}", {{ {frm} }}, {{ {to}, duration:{d}, ease:"{ease}", immediateRender:false }}, {round(max(0.02, t), 3)});'
def hide(sel): return f'    tl.set("{sel}", {{ opacity:0 }}, 0);'
def fade(sel, t, d=.35, y=24): return [hide(sel), tw(sel, t, f'opacity:0, y:{y}', 'opacity:1, y:0', d)]
def myst(sid, eid, e, t, pos, rot=''):
    """kit_myst element + its dynamics (word-timed)"""
    return M.el(eid, e, pos, rot), M.dyn(eid, e, t, lambda i, w: T(i, w), int(sid[1:]))
def typer(eid, text, t, x, y, size=64, color=None, dur=None):
    e = {'k': 'typer', 'text': text, 'size': size, **({'color': color} if color else {}), 'dur': dur or .07 * len(text)}
    return M.el(eid, e, f'left:{x}px;top:{y}px;', ''), M.dyn(eid, e, t, None, 0)
def radar(eid, x, y, d=620, blip=None):
    """round radar scope with rotating sweep; optional blip (x%, y%)"""
    b = f'<div class="blip" id="{eid}-b" style="left:{blip[0]}%;top:{blip[1]}%">{plane(46, GREEN)}<span>MH370</span></div>' if blip else ''
    return (f'<div class="scope" id="{eid}" style="left:{x}px;top:{y}px;width:{d}px;height:{d}px"><div class="rg"></div><div class="sw" id="{eid}-sw"></div>{b}</div>',
            [f'    tl.fromTo("#{eid}-sw", {{ rotation:0 }}, {{ rotation:360, duration:2.4, ease:"none", repeat:12, immediateRender:false }}, 0);'])
SCOPE = """.scope { position:absolute; border-radius:50%; overflow:hidden; background:radial-gradient(circle,#06140F 0%,#030A08 70%); border:4px solid #1D4A38; box-shadow:0 0 60px rgba(61,220,151,.15), inset 0 0 60px rgba(0,0,0,.8); }
.scope .rg { position:absolute; inset:0; border-radius:50%; background:repeating-radial-gradient(circle,transparent 0 68px,rgba(61,220,151,.22) 68px 70px), linear-gradient(rgba(61,220,151,.18),rgba(61,220,151,.18)) 50% 0/2px 100% no-repeat, linear-gradient(90deg,rgba(61,220,151,.18),rgba(61,220,151,.18)) 0 50%/100% 2px no-repeat; }
.scope .sw { position:absolute; inset:0; border-radius:50%; background:conic-gradient(from 0deg,rgba(61,220,151,.55),rgba(61,220,151,0) 22%,transparent 100%); }
.blip { position:absolute; transform:translate(-50%,-50%); text-align:center; filter:drop-shadow(0 0 12px #3DDC97); }
.blip span { display:block; font:700 24px 'SD Mono'; color:#3DDC97; letter-spacing:3px; margin-top:4px; }
.pring { position:absolute; width:200px; height:200px; margin:-100px 0 0 -100px; border-radius:50%; border:4px solid #9FC3FF; opacity:0; }"""
def pings(sid, n, x, y, t0, every=1.0, k=3, col=BLUE):
    body = ''.join(f'<div class="pring" id="{sid}-pr{n}{j}" style="left:{x}px;top:{y}px;border-color:{col}"></div>' for j in range(k))
    sc = [f'    tl.fromTo("#{sid}-pr{n}{j}", {{ opacity:.9, scale:.2 }}, {{ opacity:0, scale:2.2, duration:1.2, ease:"power1.out", repeat:{max(0, int(12 / every))}, repeatDelay:{round(every * k - 1.2, 2) if every * k > 1.2 else 0}, immediateRender:false }}, {round(t0 + j * every, 3)});' for j in range(k)]
    return body, sc

# ------------------------------------------------------------------ scenes
def s0():
    i, sid = 0, 's0'
    t_van, t_sat, t_two, t_hrs = T(0, 'vanished'), T(0, 'satellite'), T(0, 'two'), T(0, 'hours')
    rb, rs = radar(f'{sid}-r', 230, 300, 620, blip=(64, 38))
    tb, ts = typer(f'{sid}-ty', '01:21 · 8 MARCH 2014', 0.1, 220, 210, 52, RED)
    pb, ps = pings(sid, 0, 540, 470, t_sat + .3, 1.0)
    body = f"""{tb}{rb}<div class="chip r" id="{sid}-lost" style="left:340px;top:960px">SIGNAL LOST</div>
<div class="ctr mid" id="{sid}-239" style="top:1050px"><span class="red">239</span> PEOPLE ON BOARD</div>
<div id="{sid}-sat" style="position:absolute;left:430px;top:400px">{sat(220)}</div>{pb}
<div class="ctr lbl" id="{sid}-st" style="top:640px">SATELLITE · STILL HEARING IT</div>
<div class="ctr big mono" id="{sid}-clk" style="top:740px;font-family:'SD Mono'">01:21</div>
<div class="ctr lbl" id="{sid}-hr" style="top:890px;color:#E5383B">+ ALMOST 7 HOURS</div>"""
    sc = ts + rs + fade(f'#{sid}-r', 0.05, .5, 40)
    sc += [hide(f'#{sid}-lost'), hide(f'#{sid}-239'), hide(f'#{sid}-sat'), hide(f'#{sid}-st'), hide(f'#{sid}-clk'), hide(f'#{sid}-hr')]
    sc += [pop(f'#{sid}-239', t_two - .1)]
    sc += [f'    tl.fromTo("#{sid}-r-b", {{ opacity:1 }}, {{ opacity:0, duration:.06, yoyo:true, repeat:5, ease:"none", immediateRender:false }}, {t_van});',
           f'    tl.to("#{sid}-r-b", {{ opacity:0, duration:.2 }}, {t_van + .4});', slam(f'#{sid}-lost', t_van + .3)]
    sc += [tw(f'#{sid}-r', t_sat - .5, 'opacity:1, scale:1', 'opacity:0, scale:.6', .4, 'power2.in'), f'    tl.to("#{sid}-lost", {{ opacity:0, duration:.2 }}, {t_sat - .5});',
           f'    tl.to("#{sid}-239", {{ opacity:0, duration:.2 }}, {t_sat - .5});', f'    tl.to("#{sid}-ty", {{ opacity:0, duration:.2 }}, {t_sat - .5});',
           tw(f'#{sid}-sat', t_sat - .1, 'opacity:0, y:-200, rotation:-10', 'opacity:1, y:0, rotation:0', .6, 'expo.out'), tw(f'#{sid}-st', t_sat + .2, 'opacity:0', 'opacity:1', .3),
           tw(f'#{sid}-clk', t_sat + .6, 'opacity:0, scale:.7', 'opacity:1, scale:1', .3, 'back.out(2)')]
    sc += ps
    clock = ['01:21', '02:25', '03:41', '04:41', '05:41', '06:41', '08:10', '08:19']
    t0 = t_sat + 1.0; dt = max(.25, (t_hrs - t0) / len(clock))
    sc += L.steps if False else [f'    tl.set("#{sid}-clk", {{ textContent:"{c}" }}, {round(t0 + k * dt, 3)});' for k, c in enumerate(clock)]
    sc += [tw(f'#{sid}-hr', t_hrs - .3, 'opacity:0, y:20', 'opacity:1, y:0', .3)]
    return mk(i, body, sc, SCOPE, punch=False), [(0.02, 'swell', .5), (0.2, 'type', .35), (t_van, 'static', .45), (t_van + .3, 'powerdown', .55),
                                                (t_sat - .1, 'swell', .45), (t_sat + .3, 'ping', .35), (t_sat + 1.3, 'ping', .3), (t_sat + 2.3, 'ping', .3), (t_hrs - .3, 'impact', .45)]

def s1():
    i, sid = 1, 's1'
    t_bj = T(1, 'beijing')
    e = {'k': 'file', 'title': 'CASE 002 · MISSING AIRCRAFT', 'w': 900, 'gap': .4,
         'rows': [['DATE', '8 MARCH 2014'], ['FLIGHT', 'MH370 · BOEING 777'], ['FROM', 'KUALA LUMPUR'], ['TO', 'BEIJING'], ['ARRIVED', None]],
         'stamp': 'MISSING', 'stamp_at': 'beijing'}
    fb, fs = M.el(f'{sid}-f', e, 'left:90px;top:330px;', 'transform:rotate(-1.5deg);'), M.dyn(f'{sid}-f', {**e, 'stamp_at': None}, T(1, 'malaysia') - .2, None, 1)
    fs = [x for x in fs if '-s"' not in x]
    stamp = [f'    tl.set("#{sid}-f-s", {{ opacity:0 }}, 0); tl.fromTo("#{sid}-f-s", {{ scale:2.6, opacity:0 }}, {{ scale:1, opacity:1, duration:.22, ease:"power4.in", immediateRender:false }}, {round(t_bj - 1.2, 3)});']
    body = fb + f'<div class="ctr lbl" id="{sid}-r" style="top:1020px">KUALA LUMPUR ✈ BEIJING · RED-EYE FLIGHT</div>'
    sc = [tw(f'#{sid}-f', 0.05, 'opacity:0, y:120, rotation:4', 'opacity:1, y:0, rotation:-1.5', .5, 'expo.out')] + fs + stamp + fade(f'#{sid}-r', T(1, 'kuala'))
    return mk(i, body, sc), [(S['s1'][0] + .05, 'swell', .4), (S['s1'][0] + T(1, 'malaysia') + .3, 'stamp', .35), (S['s1'][0] + t_bj - 1.2, 'stamp', .7)]

def s2():
    i, sid = 2, 's2'
    t_good, t_dark, t_tr = T(2, 'good'), T(2, 'dark'), T(2, 'transponder')
    a, sa = typer(f'{sid}-t1', '"GOOD NIGHT,', t_good, 130, 470, 66, INK, .5)
    b, sb = typer(f'{sid}-t2', 'MALAYSIAN 370"', t_good + .8, 130, 570, 66, INK, 1.4)
    body = f"""<div class="panel" id="{sid}-p" style="left:80px;top:300px;width:920px;height:420px"></div>
<div class="lbl" id="{sid}-h" style="position:absolute;left:130px;top:350px">COCKPIT → AIR TRAFFIC CONTROL · 01:19</div>{a}{b}
<div class="panel" id="{sid}-x" style="left:200px;top:800px;width:680px;height:300px;text-align:center">
  <div class="lbl" style="margin-top:36px">TRANSPONDER</div><div id="{sid}-led" style="width:70px;height:70px;border-radius:35px;margin:30px auto 0;background:#3DDC97;box-shadow:0 0 40px #3DDC97"></div>
  <div id="{sid}-st" style="font:900 52px 'SD Mono';color:#3DDC97;margin-top:22px">ON</div></div>
<div class="chip r" id="{sid}-at" style="left:400px;top:1130px">01:21 · OFF</div>"""
    sc = [tw(f'#{sid}-p', .05, 'opacity:0, y:60', 'opacity:1, y:0', .4, 'expo.out'), tw(f'#{sid}-h', .2, 'opacity:0', 'opacity:1', .3)] + sa + sb
    sc += fade(f'#{sid}-x', t_tr - .6) + [hide(f'#{sid}-at')]
    sc += [f'    tl.fromTo("#{sid}-led", {{ opacity:1 }}, {{ opacity:.2, duration:.05, yoyo:true, repeat:5, immediateRender:false }}, {t_dark - .25});',
           f'    tl.to("#{sid}-led", {{ background:"#1B2C4C", boxShadow:"0 0 0 rgba(0,0,0,0)", duration:.1 }}, {t_dark + .1});',
           f'    tl.set("#{sid}-st", {{ textContent:"OFF", color:"#E5383B" }}, {t_dark + .1});', slam(f'#{sid}-at', t_dark + .25)]
    s0_ = S['s2'][0]
    return mk(i, body, sc), [(s0_ + t_good, 'keys', .35), (s0_ + t_tr - .6, 'swell', .35), (s0_ + t_dark, 'powerdown', .6), (s0_ + t_dark + .25, 'impact', .45)]

MAP = """<svg width="980" height="860" viewBox="0 0 980 860">
<path d="M300 0 L360 60 L380 150 L430 230 L470 300 L500 380 L540 470 L590 560 L640 640 L700 700 L690 760 L630 740 L560 680 L500 600 L440 520 L400 440 L370 360 L330 300 L300 220 L280 120 Z" fill="#15233F" stroke="#26406B" stroke-width="3"/>
<path d="M0 520 L80 560 L160 640 L260 720 L360 800 L420 860 L0 860 Z" fill="#15233F" stroke="#26406B" stroke-width="3"/>
<path d="M980 0 L930 80 L900 190 L880 300 L860 380 L900 420 L980 430 Z" fill="#15233F" stroke="#26406B" stroke-width="3"/>
<text x="430" y="520" fill="#8FA3C2" font-family="SD Mono" font-size="26" letter-spacing="4">MALAYSIA</text>
<text x="50" y="300" fill="#7286A8" font-family="SD Mono" font-size="24" letter-spacing="4">ANDAMAN SEA</text>
<text x="620" y="220" fill="#7286A8" font-family="SD Mono" font-size="24" letter-spacing="4">S. CHINA SEA</text>
<circle cx="520" cy="640" r="12" fill="#E8EDF5"/><text x="540" y="650" fill="#C3CEE0" font-family="SD Mono" font-size="24">KL</text>
<path id="pth-a" d="M520 640 L620 480 L720 330" fill="none" stroke="#9FC3FF" stroke-width="7" stroke-dasharray="1000" stroke-dashoffset="1000"/>
<path id="pth-b" d="M720 330 L640 360 L480 420 L340 380 L200 260 L90 170" fill="none" stroke="#E5383B" stroke-width="8" stroke-dasharray="1400" stroke-dashoffset="1400"/>
<circle id="pth-x" cx="720" cy="330" r="16" fill="none" stroke="#E5383B" stroke-width="5" opacity="0"/>
</svg>"""
def s3():
    i, sid = 3, 's3'
    t_turn, t_cross, t_sea = T(3, 'turned'), T(3, 'crossed'), T(3, 'sea')
    body = f"""<div class="ctr lbl" id="{sid}-h" style="top:200px">MILITARY RADAR TRACK</div>
<div id="{sid}-m" style="position:absolute;left:50px;top:270px">{MAP}</div>
<div class="chip r" id="{sid}-tb" style="left:640px;top:520px">TURNED BACK</div>
<div class="ill" style="top:1150px">SCHEMATIC · NOT TO SCALE</div>"""
    sc = [tw(f'#{sid}-h', .05, 'opacity:0', 'opacity:1', .3), tw(f'#{sid}-m', .05, 'opacity:0, scale:1.08', 'opacity:1, scale:1', .6, 'expo.out'),
          tw('#pth-a', .3, 'strokeDashoffset:1000', 'strokeDashoffset:0', max(.6, t_turn - .6), 'none'),
          tw('#pth-x', t_turn - .1, 'opacity:0, scale:.3', 'opacity:1, scale:1', .3, 'back.out(3)'), hide(f'#{sid}-tb'), slam(f'#{sid}-tb', t_turn),
          tw('#pth-b', t_turn + .2, 'strokeDashoffset:1400', 'strokeDashoffset:0', max(1.0, t_sea - t_turn), 'none')]
    s0_ = S['s3'][0]
    return mk(i, body, sc), [(s0_ + .05, 'scan', .35), (s0_ + t_turn, 'impact', .5), (s0_ + t_cross, 'swell', .35)]

def s4():
    i, sid = 4, 's4'
    t_rng, t_gone = T(4, 'range'), T(4, 'gone')
    rb, rs = radar(f'{sid}-r', 190, 280, 700, blip=(18, 22))
    body = f"""{rb}<div class="ctr" id="{sid}-g" style="top:1010px;font:900 150px 'SD Display';color:#E5383B;letter-spacing:10px;line-height:1">GONE.</div>
<div class="chip d" id="{sid}-l" style="left:110px;top:200px">02:22 · LAST RADAR CONTACT</div>"""
    sc = rs + fade(f'#{sid}-r', .05, .5, 0) + fade(f'#{sid}-l', .3) + [
        tw(f'#{sid}-r-b', .3, 'x:0, y:0', 'x:-140, y:-120', max(1, t_rng), 'none'),
        f'    tl.fromTo("#{sid}-r-b", {{ opacity:1 }}, {{ opacity:0, duration:.08, yoyo:true, repeat:7, ease:"none", immediateRender:false }}, {t_rng});',
        f'    tl.to("#{sid}-r-b", {{ opacity:0, duration:.2 }}, {t_rng + .7});', hide(f'#{sid}-g'), slam(f'#{sid}-g', t_gone - .05), shake(f'#{sid}-all', t_gone + .1)]
    s0_ = S['s4'][0]
    return mk(i, body, sc, SCOPE), [(s0_ + .05, 'scan', .3), (s0_ + t_rng, 'static', .4), (s0_ + t_gone - .05, 'impact', .6), (s0_ + t_gone, 'rumble', .5)]

def s5():
    i, sid = 5, 's5'
    t_pg, t_ans = T(5, 'pings'), T(5, 'answering')
    pb, ps = pings(sid, 0, 540, 420, T(5, 'automatic'), 1.2, 2, BLUE)
    qb, qs = pings(sid, 1, 540, 1000, t_ans - .3, 1.2, 2, GREEN)
    body = f"""<div id="{sid}-sat" style="position:absolute;left:390px;top:300px">{sat(300)}</div>{pb}{qb}
<div class="ctr lbl" style="top:220px">SATELLITE · 35,800 KM UP</div>
<div id="{sid}-bm" style="position:absolute;left:536px;top:500px;width:8px;height:430px;background:repeating-linear-gradient(180deg,#9FC3FF 0 20px,transparent 20px 34px);transform-origin:50% 0"></div>
<div id="{sid}-pl" style="position:absolute;left:480px;top:940px">{plane(120, INK)}</div>
<div class="chip d" id="{sid}-q" style="left:640px;top:600px">PING?</div><div class="chip r" id="{sid}-a" style="left:640px;top:820px;background:#3DDC97;color:#06140F">STILL HERE ✓</div>"""
    sc = [tw(f'#{sid}-sat', .05, 'opacity:0, y:-120', 'opacity:1, y:0', .5, 'expo.out'), tw(f'#{sid}-pl', .2, 'opacity:0, y:120', 'opacity:1, y:0', .5, 'expo.out'),
          hide(f'#{sid}-bm'), tw(f'#{sid}-bm', T(5, 'sending'), 'opacity:1, scaleY:0', 'opacity:1, scaleY:1', .6), hide(f'#{sid}-q'), hide(f'#{sid}-a'),
          pop(f'#{sid}-q', t_pg - .2), pop(f'#{sid}-a', t_ans - .2),
          f'    tl.fromTo("#{sid}-bm", {{ backgroundPositionY:"0px" }}, {{ backgroundPositionY:"340px", duration:6, ease:"none", immediateRender:false }}, {T(5, "sending")});'] + ps + qs
    s0_ = S['s5'][0]
    return mk(i, body, sc), [(s0_ + T(5, 'automatic'), 'ping', .35), (s0_ + t_pg, 'ping', .35), (s0_ + t_ans - .3, 'chirp', .35), (s0_ + t_ans + .9, 'chirp', .3)]

HS = ['02:25', '03:41', '04:41', '05:41', '06:41', '08:10', '08:19']
def s6():
    i, sid = 6, 's6'
    t_no1, t_no2, t_sev, t_ts, t_fr = T(6, 'messages'), T(6, 'voices'), T(6, 'seven'), T(6, 'time'), T(6, 'frequency')
    rows = ''.join(f'<div class="hr" id="{sid}-h{k}"><b>#{k + 1}</b><span>{t}</span><i class="tc">✓</i><i class="fc">✓</i></div>' for k, t in enumerate(HS))
    body = f"""<div class="ctr" id="{sid}-n1" style="top:230px;font:900 64px 'SD Display';color:#5A6E91"><s>MESSAGES</s> &nbsp; <s id="{sid}-n2">VOICES</s></div>
<div class="panel" id="{sid}-lg" style="left:90px;top:340px;width:900px;padding:26px 40px">
<div class="hh"><b>LOG</b><span>TIME (MYT)</span><i id="{sid}-ct">TIME STAMP</i><i id="{sid}-cf">FREQ. SHIFT</i></div>{rows}</div>
<div class="ill" style="top:1180px">INMARSAT LOG · ATSB · RECREATION</div>"""
    css = """.hh, .hr { display:flex; align-items:center; gap:20px; font:700 30px 'SD Mono'; color:#C3CEE0; height:96px; border-bottom:1px solid #22304A; }
.hh { height:64px; font-size:20px; letter-spacing:3px; color:#8FA3C2; } .hh b, .hr b { width:90px; color:#E5383B; } .hh span, .hr span { width:250px; }
.hh i, .hr i { width:220px; text-align:center; font-style:normal; } .hr i { font-size:42px; color:#3DDC97; opacity:0; } .hr span { font-size:44px; color:#E8EDF5; }
#s6-ct, #s6-cf { border-radius:10px; padding:6px 0; }"""
    sc = [hide(f'#{sid}-n1'), pop(f'#{sid}-n1', t_no1 - .3), hide(f'#{sid}-n2'), tw(f'#{sid}-n2', t_no2 - .2, 'opacity:0', 'opacity:1', .2),
          tw(f'#{sid}-lg', t_sev - .9, 'opacity:0, y:80', 'opacity:1, y:0', .4, 'expo.out'), hide(f'#{sid}-lg')]
    sc += [f'    tl.set("#{sid}-h{k}", {{ opacity:0 }}, 0); tl.fromTo("#{sid}-h{k}", {{ opacity:0, x:-60 }}, {{ opacity:1, x:0, duration:.18, immediateRender:false }}, {round(t_sev - .3 + k * .22, 3)});' for k in range(7)]
    sc += [tw(f'#{sid}-ct', t_ts - .1, 'backgroundColor:"rgba(0,0,0,0)"', 'backgroundColor:"rgba(229,56,59,.35)"', .2),
           f'    tl.to("#{sid}-lg .tc", {{ opacity:1, duration:.1, stagger:.1 }}, {round(t_ts, 3)});',
           tw(f'#{sid}-cf', t_fr - .3, 'backgroundColor:"rgba(0,0,0,0)"', 'backgroundColor:"rgba(229,56,59,.35)"', .2),
           f'    tl.to("#{sid}-lg .fc", {{ opacity:1, duration:.1, stagger:.1 }}, {round(t_fr - .2, 3)});']
    s0_ = S['s6'][0]
    return mk(i, body, sc, css), ([(s0_ + t_no1 - .3, 'swell', .35), (s0_ + t_no2 - .2, 'thud', .35)] + [(s0_ + t_sev - .3 + k * .22, 'tick', .3) for k in range(7)]
                                  + [(s0_ + t_ts, 'chirp', .3), (s0_ + t_fr - .2, 'chirp', .3)])

def s7():
    i, sid = 7, 's7'
    t_pings, t_path, t_oc = T(7, 'pings'), T(7, 'path'), T(7, 'ocean')
    arcs = ''.join(f'<path id="{sid}-a{k}" d="M{-150 + 0} {0} m0 0 A{260 + k * 105} {260 + k * 105} 0 0 1 {-150 + 0} {0}" />' for k in range(0))
    circ = ''.join(f'<circle id="{sid}-c{k}" cx="960" cy="-120" r="{300 + k * 120}" fill="none" stroke="{RED if k == 6 else "#26406B"}" stroke-width="{8 if k == 6 else 3}" stroke-dasharray="{"18 10" if k == 6 else "none"}"/>' for k in range(7))
    body = f"""<div style="position:absolute;left:0;top:200px;width:1080px;height:1000px;overflow:hidden" id="{sid}-box">
<svg width="1080" height="1000" viewBox="0 0 1080 1000">{circ}
<path id="{sid}-p" d="M770 40 C700 300 560 560 330 900" fill="none" stroke="#E8EDF5" stroke-width="6" stroke-dasharray="1100" stroke-dashoffset="1100"/>
<circle id="{sid}-x" cx="330" cy="900" r="22" fill="#E5383B"/></svg></div>
<div class="chip r" id="{sid}-7" style="left:600px;top:930px">7TH ARC</div>
<div class="ctr lbl" id="{sid}-oc" style="top:1140px;color:#E8EDF5;font-size:34px">SOUTHERN INDIAN OCEAN</div>
<div class="ctr" style="top:200px"><span class="lbl" style="background:#080C14;padding:10px 18px;border-radius:10px">EACH RING = ONE PING'S DISTANCE</span></div>"""
    sc = [f'    tl.set("#{sid}-c{k}", {{ opacity:0 }}, 0); tl.fromTo("#{sid}-c{k}", {{ opacity:0, scale:.9, transformOrigin:"960px -120px" }}, {{ opacity:1, scale:1, duration:.3, immediateRender:false }}, {round(max(.05, t_pings - .8) + k * .25, 3)});' for k in range(7)]
    sc += [hide(f'#{sid}-7'), pop(f'#{sid}-7', t_pings + 1.0), tw(f'#{sid}-p', t_path - .6, 'strokeDashoffset:1100', 'strokeDashoffset:0', max(1, t_oc - t_path + .4), 'power1.inOut'),
           hide(f'#{sid}-x'), tw(f'#{sid}-x', t_oc - .1, 'opacity:0, scale:.2, transformOrigin:"330px 900px"', 'opacity:1, scale:1', .3, 'back.out(3)'), hide(f'#{sid}-oc'), slam(f'#{sid}-oc', t_oc)]
    s0_ = S['s7'][0]
    return mk(i, body, sc), [(s0_ + max(.05, t_pings - .8) + k * .25, 'ping', .22) for k in range(7)] + [(s0_ + t_path - .6, 'swell', .4), (s0_ + t_oc, 'impact', .5)]

FLAP = ('<svg width="520" height="200" viewBox="0 0 260 100"><path d="M6 30 L250 8 L254 34 L10 92 Z" fill="#C9CED6" stroke="#8C949F" stroke-width="3"/>'
        '<path d="M40 40 L230 20 M60 60 L232 32" stroke="#9AA2AD" stroke-width="2"/>' + ''.join(f'<circle cx="{30 + (k * 37) % 200}" cy="{50 + (k * 23) % 34}" r="{3 + k % 3}" fill="#6F6A5E"/>' for k in range(16)) + '</svg>')
def s8():
    i, sid = 8, 's8'
    t_wing, t_re = T(8, 'wing'), T(8, 'reunion')
    body = f"""<div class="ctr lbl" id="{sid}-h" style="top:220px">29 JULY 2015 · FIRST CONFIRMED DEBRIS</div>
<div id="{sid}-w" style="position:absolute;left:280px;top:420px">{FLAP}</div>
<div class="ctr lbl" id="{sid}-n" style="top:660px;color:#C3CEE0">FLAPERON · PART OF THE WING</div>
<div class="wave" style="top:760px"></div><div class="wave" style="top:800px;opacity:.5"></div>
<div id="{sid}-pin" style="position:absolute;left:470px;top:860px;text-align:center;width:140px"><div style="width:60px;height:60px;margin:0 auto;border-radius:30px 30px 30px 0;transform:rotate(-45deg);background:#E5383B"></div></div>
<div class="ctr mid" id="{sid}-r" style="top:960px">RÉUNION ISLAND</div><div class="ctr lbl" id="{sid}-a" style="top:1060px">INDIAN OCEAN · NEAR AFRICA</div>
<div class="stampx" id="{sid}-c" style="left:300px;top:480px">MH370</div>"""
    css = """.wave { position:absolute; left:0; right:0; height:40px; background:repeating-radial-gradient(circle at 50% -60%,transparent 0 30px,rgba(159,195,255,.35) 30px 34px) 0 0/120px 80px; }"""
    sc = fade(f'#{sid}-h', .05) + [tw(f'#{sid}-w', .1, 'opacity:0, x:-500, rotation:-8', 'opacity:1, x:0, rotation:0', max(.8, t_wing), 'power2.out'),
          f'    tl.fromTo("#{sid}-w", {{ y:0 }}, {{ y:-16, duration:.9, yoyo:true, repeat:5, ease:"sine.inOut", immediateRender:false }}, {max(.9, t_wing)});'] + fade(f'#{sid}-n', t_wing)
    sc += [hide(f'#{sid}-pin'), tw(f'#{sid}-pin', t_re - .3, 'opacity:0, y:-120', 'opacity:1, y:0', .4, 'bounce.out'), hide(f'#{sid}-r'), slam(f'#{sid}-r', t_re), hide(f'#{sid}-a'), pop(f'#{sid}-a', T(8, 'africa') - .2),
           f'    tl.set("#{sid}-c", {{ opacity:0 }}, 0); tl.fromTo("#{sid}-c", {{ scale:2.6, opacity:0 }}, {{ scale:1, opacity:1, duration:.22, ease:"power4.in", immediateRender:false }}, {round(T(8, "africa") + .5, 3)});']
    s0_ = S['s8'][0]
    return mk(i, body, sc, css), [(s0_ + .1, 'swell', .4), (s0_ + t_re, 'impact', .45), (s0_ + T(8, 'africa') + .5, 'stamp', .6)]

def s9():
    i, sid = 9, 's9'
    t_sc, t_sb, t_lt, t_no = T(9, 'scanned'), T(9, 'seabed'), T(9, 'latest'), T(9, 'nothing')
    stripes = ''.join(f'<i style="top:{k * 46}px;animation:none"></i>' for k in range(10))
    body = f"""<div class="ctr lbl" style="top:220px">SEABED SONAR SEARCH</div>
<div class="sea" id="{sid}-sea"><div class="sn" id="{sid}-sn"></div><div class="fish" id="{sid}-f"></div></div>
<div class="ctr big" id="{sid}-n" style="top:820px;font-size:110px">0</div><div class="ctr lbl" style="top:950px">SQUARE KM SCANNED</div>
<div class="chip d" id="{sid}-l" style="left:290px;top:1040px">LATEST SEARCH ENDED · 2026</div>
<div class="stampx" id="{sid}-x" style="left:190px;top:480px;font-size:66px">NOTHING FOUND</div>"""
    css = """.sea { position:absolute; left:90px; top:300px; width:900px; height:480px; border-radius:22px; overflow:hidden; background:#0A1220; border:2px solid #26324A; }
.sn { position:absolute; left:0; top:0; bottom:0; width:0; background:repeating-linear-gradient(90deg,#13305A 0 6px,#0E2446 6px 11px,#1A3E70 11px 13px); }
.fish { position:absolute; top:0; bottom:0; width:6px; left:0; background:#9FC3FF; box-shadow:0 0 24px #9FC3FF; }"""
    sc = [tw(f'#{sid}-sn', .1, 'width:0', 'width:900', max(1.5, t_lt), 'none'), tw(f'#{sid}-f', .1, 'x:0', 'x:894', max(1.5, t_lt), 'none')]
    sc += [f'    tl.set("#{sid}-n", {{ textContent:"{v}" }}, {round(t_sc + k * (max(.6, t_sb - t_sc) / 6), 3)});' for k, v in enumerate(['10,000', '30,000', '50,000', '70,000', '90,000', '100,000+'])]
    sc += [hide(f'#{sid}-l'), pop(f'#{sid}-l', t_lt - .1), hide(f'#{sid}-x'),
           f'    tl.fromTo("#{sid}-x", {{ scale:2.6, opacity:0 }}, {{ scale:1, opacity:1, duration:.22, ease:"power4.in", immediateRender:false }}, {round(t_no - .4, 3)});', shake(f'#{sid}-all', t_no - .2)]
    s0_ = S['s9'][0]
    return mk(i, body, sc, css), [(s0_ + .1, 'scan', .3), (s0_ + 2.5, 'scan', .25)] + [(s0_ + t_sc + k * (max(.6, t_sb - t_sc) / 6), 'tick', .25) for k in range(6)] + [(s0_ + t_no - .4, 'stamp', .7), (s0_ + t_no, 'rumble', .45)]

def s10():
    i, sid = 10, 's10'
    t_who, t_why, t_no = T(10, 'who'), T(10, 'why'), T(10, 'knows')
    cl1 = {'k': 'clue', 'n': 1, 'text': 'Turned back by hand, not autopilot (2018 report)', 'w': 820}
    body = f"""<div class="ctr mid" id="{sid}-a" style="top:300px">WHO TURNED<br>THE PLANE AROUND?</div>
<div class="ctr" id="{sid}-b" style="top:520px;font:900 180px 'SD Display';color:#E5383B">WHY?</div>
{M.el(f'{sid}-c', cl1, 'left:130px;top:780px;', 'transform:rotate(-2deg);')}
<div class="stampx" id="{sid}-u" style="left:250px;top:560px">UNSOLVED</div>"""
    sc = [hide(f'#{sid}-a'), slam(f'#{sid}-a', max(.05, t_who - .05)), hide(f'#{sid}-b'), slam(f'#{sid}-b', t_why - .05),
          tw(f'#{sid}-c', t_why + .5, 'opacity:0, y:60', 'opacity:1, y:0', .35, 'back.out(1.6)'), hide(f'#{sid}-c'), hide(f'#{sid}-u'),
          tw(f'#{sid}-b', t_no - .6, 'opacity:1', 'opacity:.15', .3),
          f'    tl.fromTo("#{sid}-u", {{ scale:2.6, opacity:0 }}, {{ scale:1, opacity:1, duration:.22, ease:"power4.in", immediateRender:false }}, {round(t_no - .3, 3)});']
    s0_ = S['s10'][0]
    return mk(i, body, sc), [(s0_ + t_who, 'impact', .45), (s0_ + t_why - .05, 'impact', .55), (s0_ + t_why + .5, 'swell', .3), (s0_ + t_no - .3, 'stamp', .7)]

def s11():
    i, sid = 11, 's11'
    t_sub = T(11, 'subscribe')
    body, sc, css, tc = L.subscribe(sid, t_sub)
    body = body.replace('AI &amp; tech news, decoded.', 'Tech mysteries, decoded.')
    body += '<div class="ctr lbl" style="top:1100px;color:#E5383B">TECH MYSTERIES · CASE 002</div>'
    s0_ = S['s11'][0]
    return mk(i, body, sc, css), [(s0_, 'swell', .4), (s0_ + tc, 'click', .9), (s0_ + tc + .1, 'ding', .5)]

def overlay():
    """empty 'chapters' layer: kit_myst.mysterize adds grain, scanlines, vignette, flicker and the CASE badge"""
    return scene('chapters', '', '', '').replace('<div class="all" id="chapters-all">', '<div class="all">')

if __name__ == '__main__':
    res = [f() for f in (s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11)]
    SFX = sorted(x for _, s in res for x in s)
    L.sfx_list = lambda: SFX
    comp = P / 'compositions'; comp.mkdir(parents=True, exist_ok=True)
    for f in comp.glob('*.html'): f.unlink()
    for k, (html, _) in enumerate(res):
        (comp / f's{k}.html').write_text(html)
    (comp / 'bg.html').write_text(L.bg())
    (comp / 'caps.html').write_text(L.captions())
    (comp / 'chapters.html').write_text(overlay())
    idx = L.index().replace('<div id="caps"', f'<div id="chapters" data-composition-id="chapters" data-composition-src="compositions/chapters.html" data-start="0" data-duration="{DUR}" data-track-index="2" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:4"></div>\n      <div id="caps"', 1)
    idx = idx.replace('data-track-index="2" data-track-kind="captions"', 'data-track-index="20" data-track-kind="captions"')
    (P / 'index.html').write_text(idx)
    print('written', P, DUR, len(SFX), 'sfx')
