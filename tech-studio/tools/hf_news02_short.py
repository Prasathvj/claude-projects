"""News Short #2: Anthropic's record IPO, and the chip/cloud companies that bought in alongside it (Nov 2026).
Reuses the Short helper library (hf_news01_short.py, SHORT_ID selects the episode).
Usage: THEME=cream GRID=lines python3 tools/hf_news02_short.py"""
import os, sys
from pathlib import Path
os.environ['SHORT_ID'] = 'news02-short'
sys.path.insert(0, str(Path(__file__).resolve().parent))
import hf_news01_short as L
from hf_news01_short import S, wl, fly, pop, slam, shake, ring, head, out, icon, bit, bit_on, bit_float, scene, E

def num_steps(sel, t0, vals, dt=0.07):
    return [f'    tl.set("{sel}", {{ textContent:"{v}" }}, {round(t0 + k * dt, 3)});' for k, v in enumerate(vals)]

def s0():
    sid = 's0'
    t_big, t_riv = wl(0, 'biggest'), wl(0, 'rivals')
    h, hs = head(sid, 'BIGGEST IPO <span>EVER</span>', 'ticker: ANT · Nasdaq')
    body = f"""{h}
<div class="card" id="{sid}-c" style="top:620px; text-align:center;"><div class="lab">RAISED IN THE IPO</div><div class="big" id="{sid}-n">$0B</div></div>
<div class="riv" id="{sid}-r">…AND ITS RIVALS HELPED PAY?</div>
{bit(sid, [('n', {'state': 'normal'}), ('g', {'state': 'gasp', 'extra': ['sweat']})])}"""
    css = """.big { font:900 190px 'SD Display'; color:var(--accent); letter-spacing:-4px; text-shadow:0 0 50px rgba(248,119,54,.4); }
.riv { position:absolute; left:60px; right:60px; top:1010px; text-align:center; font:900 56px 'SD Display'; color:var(--red); opacity:0; }"""
    sc = [hs, fly(f'#{sid}-c', 0.1)] + num_steps(f'#{sid}-n', t_big - 0.2, ['$9B', '$22B', '$38B', '$55B', '$70B', '$81B'])
    sc += [f'    tl.fromTo("#{sid}-c", {{ scale:1 }}, {{ scale:1.08, duration:.18, yoyo:true, repeat:1, immediateRender:false }}, {t_big + 0.3});', slam(f'#{sid}-r', t_riv - 0.1), out(sid)]
    sc += bit_on(sid, 'n', 0, False) + bit_float(sid) + bit_on(sid, 'g', t_riv)
    return scene(sid, body.replace(f'class="card" id="{sid}-c"', f'class="card" id="{sid}-c"'), '\n'.join(sc), css)

def s1():
    sid = 's1'
    t_pr, t_ab = wl(1, 'priced'), wl(1, 'above')
    body = f"""<div class="card" id="{sid}-c" style="top:380px; text-align:center;">
  <div class="lab">ANTHROPIC IPO · PRICED NOV 18, 2026</div>
  <div class="rng" id="{sid}-rng">Target range: $70 – $78<i id="{sid}-x"></i></div>
  <div class="pr" id="{sid}-p">$83</div><div class="ab" id="{sid}-ab">ABOVE THE RANGE ↑</div></div>"""
    css = """.rng { position:relative; display:inline-block; font:700 50px 'SD Display'; color:#CDB8AA; margin:24px 0 10px; }
.rng i { position:absolute; left:-10px; right:-10px; top:52%; height:8px; background:var(--red); transform:scaleX(0); transform-origin:left; border-radius:4px; }
.pr { font:900 240px 'SD Display'; color:var(--ink); letter-spacing:-6px; line-height:1; opacity:0; } .ab { font:900 52px 'SD Display'; color:var(--green); opacity:0; }"""
    sc = [fly(f'#{sid}-c', 0.02), f'    tl.to("#{sid}-x", {{ scaleX:1, duration:.25 }}, {t_ab - 0.3});', slam(f'#{sid}-p', t_pr + 0.4), pop(f'#{sid}-ab', t_ab), out(sid)]
    return scene(sid, body, '\n'.join(sc), css)

def s2():
    sid = 's2'
    t_r, t_sx = wl(2, 'raised'), wl(2, 'spacexs')
    body = f"""<div class="center kk" style="top:360px">LARGEST IPOs ON RECORD</div>
<div class="bar" style="top:520px"><span>SpaceX (previous record)</span><div class="fill gr" id="{sid}-a"></div></div>
<div class="bar" style="top:760px"><span>Anthropic · 2026</span><div class="fill or" id="{sid}-b"></div><b id="{sid}-v">$81B+</b></div>
<div class="tag" style="left:96px; top:1020px;">BAR LENGTHS ILLUSTRATIVE · SOURCE: CNBC</div>"""
    css = """.center { position:absolute; left:0; right:0; text-align:center; } .kk { font:600 32px 'SD Text'; letter-spacing:4px; color:var(--dim); }
.bar { position:absolute; left:90px; width:900px; height:190px; } .bar span { display:block; font:800 42px 'SD Display'; color:var(--ink); margin-bottom:14px; }
.fill { height:100px; border-radius:24px; transform-origin:left; transform:scaleX(0); } .gr { width:620px; background:#8C6B5A; } .or { width:860px; background:var(--accent); box-shadow:0 0 50px rgba(248,119,54,.4); }
.bar b { position:absolute; right:70px; top:76px; font:900 60px 'SD Display'; color:#1A0A04; opacity:0; }"""
    sc = [f'    tl.to("#{sid}-a", {{ scaleX:1, duration:.6, ease:"power3.out" }}, 0.15);', f'    tl.to("#{sid}-b", {{ scaleX:1, duration:.9, ease:"power3.out" }}, {t_r});',
          pop(f'#{sid}-v', t_r + 0.8), shake(f'#{sid}-b', t_sx + 0.2), out(sid)]
    return scene(sid, body, '\n'.join(sc), css)

def s3():
    sid = 's3'
    t_w = wl(3, 'worth')
    body = f"""<div class="center kk" style="top:420px">VALUED AT THE IPO PRICE</div>
<div class="center tn" id="{sid}-n">$0</div><div class="center tw" id="{sid}-t">TRILLION</div>
{bit(sid, [('n', {'state': 'normal'}), ('g', {'state': 'gasp'})])}"""
    css = """.center { position:absolute; left:0; right:0; text-align:center; } .kk { font:600 32px 'SD Text'; letter-spacing:4px; color:var(--dim); }
.tn { top:520px; font:900 300px 'SD Display'; color:var(--accent); letter-spacing:-8px; line-height:1; text-shadow:0 0 60px rgba(248,119,54,.45); }
.tw { top:840px; font:900 110px 'SD Display'; color:var(--ink); letter-spacing:6px; opacity:0; }"""
    sc = num_steps(f'#{sid}-n', max(0.05, t_w - 0.3), ['$0.2', '$0.5', '$0.8', '$1.1', '$1.3', '$1.5']) + [slam(f'#{sid}-t', t_w + 0.3), out(sid)]
    sc += bit_on(sid, 'n', 0, False) + bit_float(sid) + bit_on(sid, 'g', t_w + 0.3)
    return scene(sid, body, '\n'.join(sc), css)

def s4():
    sid = 's4'
    t_l, t_t = wl(4, 'launched'), wl(4, 'later')
    body = f"""<div class="line" id="{sid}-ln"></div>
<div class="pt" id="{sid}-a" style="left:110px"><b>2023</b><span>Claude launches</span></div>
<div class="pt hot" id="{sid}-b" style="left:600px"><b>2026</b><span>$1.5T company</span></div>
<div class="center yr" id="{sid}-y">3 YEARS</div>"""
    css = """.line { position:absolute; left:200px; right:200px; top:720px; height:10px; border-radius:5px; background:var(--accent); transform:scaleX(0); transform-origin:left; }
.pt { position:absolute; top:520px; width:370px; height:400px; border-radius:36px; border:2px solid #3E2217; background:linear-gradient(180deg,#2C1A13,#1F120C); display:flex; flex-direction:column; align-items:center; justify-content:center; gap:14px; opacity:0; }
.pt b { font:900 110px 'SD Display'; color:var(--ink); } .pt span { font:700 40px 'SD Display'; color:#CDB8AA; } .pt.hot { border:4px solid var(--accent); box-shadow:0 0 60px rgba(248,119,54,.35); } .pt.hot b { color:var(--accent); }
.center { position:absolute; left:0; right:0; text-align:center; } .yr { top:380px; font:900 76px 'SD Display'; color:var(--accent); letter-spacing:4px; opacity:0; }"""
    sc = [pop(f'#{sid}-a', t_l - 0.2), f'    tl.to("#{sid}-ln", {{ scaleX:1, duration:.6, ease:"power2.inOut" }}, {t_t - 0.3});', pop(f'#{sid}-b', t_t + 0.2), slam(f'#{sid}-y', t_t), out(sid)]
    return scene(sid, body, '\n'.join(sc), css)

def s5():
    sid = 's5'
    t_o, t_c = wl(5, 'opened'), wl(5, 'cooled')
    pts = '80,640 220,600 330,250 420,300 520,380 640,420 760,450 860,440'
    body = f"""<div class="card" id="{sid}-c" style="top:330px; height:820px;">
  <div class="hd"><div class="tile">{icon('bank')}</div><div><div class="lab">DAY ONE · NOV 19, 2026</div><div class="ttl">ANT · first day of trading</div></div></div>
  <svg width="900" height="660" viewBox="0 0 940 700" style="position:absolute;left:0;top:150px">
    <line x1="60" y1="640" x2="900" y2="640" stroke="#5C4337" stroke-width="3" stroke-dasharray="10 10"/>
    <text x="70" y="680" font-family="SD Text" font-weight="600" font-size="28" fill="#9E745A">IPO price $83</text>
    <polyline id="{sid}-ln" points="{pts}" fill="none" stroke="#3DDC97" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
  </svg>
  <div class="pk" id="{sid}-pk" style="left:250px; top:290px">OPENED +34%<br><small>$111.50</small></div>
  <div class="pk cl" id="{sid}-cl" style="left:560px; top:520px">CLOSED +17%<br><small>$97.17</small></div>
</div>"""
    css = """.pk { position:absolute; padding:16px 24px; border-radius:20px; background:var(--green); color:#0C3B26; font:900 40px 'SD Display'; line-height:1.05; opacity:0; } .pk small { font:700 30px 'SD Text'; }
.pk.cl { background:#F3E6DC; color:#1E120C; border:3px solid var(--green); }"""
    sc = [fly(f'#{sid}-c', 0.02), f'    tl.to("#{sid}-ln", {{ strokeDashoffset:0.55, duration:.5, ease:"power2.out" }}, {t_o - 0.2});', pop(f'#{sid}-pk', t_o + 0.2),
          f'    tl.to("#{sid}-ln", {{ strokeDashoffset:0, duration:1.0, ease:"power1.inOut" }}, {t_c - 0.1});', pop(f'#{sid}-cl', t_c + 0.8), out(sid)]
    return scene(sid, body, '\n'.join(sc), css)

def s6():
    sid = 's6'
    t_st, ts = wl(6, 'strange'), [wl(6, 'google'), wl(6, 'microsoft'), wl(6, 'nvidia')]
    h, hs = head(sid, 'THE <span>STRANGE</span> PART')
    names = ['Google', 'Microsoft', 'Nvidia']
    cards = ''.join(f'<div class="nm" id="{sid}-n{k}">{n}</div>' for k, n in enumerate(names))
    body = f"""{h}<div class="col">{cards}</div>
<div class="center bil" id="{sid}-b">+ AMD, Broadcom, Micron, TSMC · ~$26B at $83/share</div>
<div class="tag" style="left:96px; top:1200px;">PRIVATE PLACEMENT ALONGSIDE THE IPO · SOURCE: ANTHROPIC</div>
{bit(sid, [('n', {'state': 'normal'}), ('w', {'state': 'worried', 'extra': ['uhoh']})])}"""
    css = """.col { position:absolute; left:160px; right:160px; top:520px; display:flex; flex-direction:column; gap:22px; }
.nm { height:130px; border-radius:30px; border:3px solid var(--accent); background:linear-gradient(90deg,#2C1A13,#1F120C); display:flex; align-items:center; justify-content:center; font:900 70px 'SD Display'; color:var(--ink); opacity:0; }
.center { position:absolute; left:40px; right:40px; text-align:center; } .bil { top:1010px; font:700 36px 'SD Display'; color:#CDB8AA; opacity:0; }"""
    sc = [hs.replace('}, 0.0);', f'}}, {max(0.02, t_st - 0.2)});'), f'    tl.set("#{sid}-head", {{ opacity:0 }}, 0);']
    sc += [pop(f'#{sid}-n{k}', t - 0.05) for k, t in enumerate(ts)] + [pop(f'#{sid}-b', ts[2] + 0.5), out(sid)]
    sc += bit_on(sid, 'n', 0, False) + bit_float(sid) + bit_on(sid, 'w', ts[0])
    return scene(sid, body, '\n'.join(sc), css)

CHIP = '<svg width="150" height="150" viewBox="0 0 100 100" fill="none" stroke="#F87736" stroke-width="7" stroke-linecap="round"><rect x="24" y="24" width="52" height="52" rx="8"/><rect x="38" y="38" width="24" height="24" rx="3"/><path d="M36 10v12M50 10v12M64 10v12M36 78v12M50 78v12M64 78v12M10 36h12M10 50h12M10 64h12M78 36h12M78 50h12M78 64h12"/></svg>'
CLOUD = '<svg width="150" height="150" viewBox="0 0 100 100" fill="none" stroke="#F87736" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"><path d="M28 76h46a16 16 0 0 0 0-32 22 22 0 0 0-42-6 18 18 0 0 0-4 38z"/></svg>'
def s7():
    sid = 's7'
    t_ch, t_cl = wl(7, 'chips'), wl(7, 'cloud')
    body = f"""<div class="center kk" style="top:380px">WHY WOULD THEY BUY IN?</div>
<div class="bx" id="{sid}-a" style="left:110px">{CHIP}<span>Chips</span></div>
<div class="bx" id="{sid}-b" style="left:580px">{CLOUD}<span>Cloud</span></div>
<div class="center ai" id="{sid}-ai">AI RUNS ON THEM</div>"""
    css = """.center { position:absolute; left:0; right:0; text-align:center; } .kk { font:600 32px 'SD Text'; letter-spacing:4px; color:var(--dim); }
.bx { position:absolute; top:480px; width:390px; height:420px; border-radius:36px; border:2px solid #3E2217; background:linear-gradient(180deg,#2C1A13,#1F120C); display:flex; flex-direction:column; align-items:center; justify-content:center; gap:20px; font:900 64px 'SD Display'; color:var(--ink); opacity:0; }
.ai { top:960px; font:900 80px 'SD Display'; color:var(--accent); opacity:0; }"""
    sc = [pop('#s7-a', t_ch - 0.1), pop('#s7-b', t_cl - 0.1), slam('#s7-ai', t_cl + 0.4), out(sid)]
    return scene(sid, body, '\n'.join(sc), css)

SHOVEL = '<svg width="230" height="230" viewBox="0 0 100 100" fill="none" stroke="#F87736" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"><path d="M70 12l18 18M79 21L44 56"/><path d="M44 56l-6-6-22 22c-6 6-4 16 4 16s10-2 14-6l16-20z"/></svg>'
def s8():
    sid = 's8'
    t_w, t_sh = wl(8, 'wins'), wl(8, 'shovels')
    body = f"""<div class="pay" id="{sid}-p">
  <div class="k">AI GOLD RUSH</div>{SHOVEL}<div class="t">SELL THE <span>SHOVELS</span></div>
  <div class="s">When AI companies win, chip and cloud companies win too.</div></div>
{bit(sid, [('n', {'state': 'normal'}), ('h', {'state': 'happy', 'arms': 'wave'})])}"""
    css = """.pay { position:absolute; left:90px; width:900px; top:330px; padding:50px; border-radius:40px; border:4px solid var(--accent); background:linear-gradient(180deg,#2C1A13,#1F120C);
  box-shadow:0 0 90px rgba(248,119,54,.35); text-align:center; }
.k { font:600 34px 'SD Text'; letter-spacing:6px; color:var(--dim); } .t { font:900 96px 'SD Display'; color:var(--ink); line-height:1; opacity:0; } .t span { color:var(--accent); }
.s { font:600 38px 'SD Text'; color:#CDB8AA; margin-top:24px; opacity:0; }"""
    sc = [fly(f'#{sid}-p', 0.05), slam(f'#{sid}-p .t', t_sh - 0.2), pop(f'#{sid}-p .s', t_sh + 0.6)]
    sc += bit_on(sid, 'n', 0, False) + bit_float(sid) + bit_on(sid, 'h', t_sh)
    return scene(sid, body, '\n'.join(sc), css)

def sfx_list():
    def g(i, w): return S[f's{i}'][0] + wl(i, w)
    return sorted([(0.02, 'whoosh', .5), (g(0, 'biggest') - 0.2, 'riser', .45), (g(0, 'biggest') + 0.25, 'impact', .8), (g(0, 'rivals'), 'glitch', .6),
        (S['s1'][0], 'whoosh', .5), (g(1, 'priced') + 0.4, 'impact', .8), (g(1, 'above'), 'ding', .6),
        (S['s2'][0], 'whoosh', .5), (g(2, 'raised'), 'riser', .4), (g(2, 'spacexs') + 0.2, 'impact', .7),
        (g(3, 'worth') - 0.3, 'tick', .5), (g(3, 'worth') + 0.3, 'impact', .9),
        (g(4, 'launched') - 0.2, 'pop', .6), (g(4, 'later') + 0.2, 'ding', .6),
        (S['s5'][0], 'whoosh', .5), (g(5, 'opened') + 0.2, 'pop', .6), (g(5, 'cooled'), 'thud', .5),
        (g(6, 'strange') - 0.2, 'glitch', .55), (g(6, 'google'), 'pop', .6), (g(6, 'microsoft'), 'pop', .6), (g(6, 'nvidia'), 'pop', .6),
        (g(7, 'chips'), 'pop', .6), (g(7, 'cloud'), 'pop', .6), (g(7, 'cloud') + 0.4, 'impact', .6),
        (S['s8'][0], 'whoosh', .5), (g(8, 'shovels') - 0.2, 'impact', .8), (g(8, 'shovels') + 0.6, 'ding', .7)])

if __name__ == '__main__':
    L.sfx_list = sfx_list
    comp = L.P / 'compositions'; comp.mkdir(parents=True, exist_ok=True)
    for f in comp.glob('*.html'): f.unlink()
    for i, fn in enumerate([s0, s1, s2, s3, s4, s5, s6, s7, s8]):
        (comp / f's{i}.html').write_text(fn())
    (comp / 'bg.html').write_text(L.bg())
    (comp / 'caps.html').write_text(L.captions())
    (L.P / 'index.html').write_text(L.index())
    print('written', L.P, L.DUR)
