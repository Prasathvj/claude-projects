"""Three motion-style samples on the knight01 hook (line 0, ~9.4 s) for the owner to choose from (2026-11-24).
S1 KINETIC SLAM  - type-driven: giant words slam in, characters explode, slot-machine money roll + falling bills, camera shake.
S2 CAMERA JOURNEY - one big canvas, the camera flies between acting objects with motion blur and parallax.
S3 WHIP & FLIP   - full-screen cards whip-pan and 3D-flip in on every phrase, punch zooms, RGB glitch.
Old caption style + small Max bottom-right in S2/S3. Our colours. Usage: python3 tools/style3.py"""
import json, re, shutil, subprocess, wave
from pathlib import Path

tl = json.load(open('src/episodes/knight01-short.timeline.json'))
B0 = tl['beats'][0]
DUR = round(B0['start'] + B0['dur'] + 0.25, 2)
INK, ACC, ACC2, CREAM, GREEN = '#2A2018', '#F87736', '#E8402E', '#F4EDE3', '#16A34A'
GR = f'linear-gradient(90deg,{ACC},{ACC2})'
CLI = ['node', '/home/user/claude-projects/.claude/skills/hyperframes/scripts/plugin-cli.mjs']


def norm(w): return re.sub(r"[^a-z0-9]", '', w.lower())
def T(word): return round(B0['start'] + [w for w in B0['words'] if norm(w['w']).startswith(norm(word))][0]['s'], 3)


SFXD = {f.stem: round(wave.open(str(f)).getnframes() / 44100, 3) for f in Path('hf/ast01-short/assets/sfx').glob('*.wav')}
BASE_CSS = f'''@font-face{{font-family:'D';src:url('assets/fonts/InterDisplay-Black.otf');font-weight:900}}
@font-face{{font-family:'A';src:url('assets/fonts/anton-latin-400-normal.woff2')}}
@font-face{{font-family:'M';src:url('assets/fonts/JetBrainsMono-Bold.ttf');font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;overflow:hidden;background:{CREAM}}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:radial-gradient(circle at 12% 8%,rgba(248,119,54,.22),transparent 38%),radial-gradient(circle at 92% 92%,rgba(248,119,54,.28),transparent 42%),{CREAM}}}
.dots{{position:absolute;inset:-200px;background:radial-gradient(#E2CBB8 2.4px,transparent 2.6px) 0 0/34px 34px}}
.el{{position:absolute;opacity:0;visibility:hidden}}
.cap{{position:absolute;left:40px;right:40px;top:1240px;opacity:0;visibility:hidden;text-align:center;font:900 84px/1.15 'D';color:{INK};letter-spacing:-2px;z-index:60}}
.cap span{{display:inline-block;padding:0 14px 6px;border-radius:18px;margin:0 2px}} .cap span.hl{{background:{GR};color:#fff;box-shadow:0 10px 0 #A8301A}}
.mxp{{position:absolute;inset:0;opacity:0;visibility:hidden;filter:drop-shadow(0 20px 18px rgba(74,50,28,.3))}}
'''
MAXC = "{skin:'#F0C4A0',hair:'messy',hairCol:'#5A3A26',glasses:'round',hood:'down',top:'#F87736',topS:'#D85E25',phones:'none',beard:'stubble'}"
WATCH = '''<svg viewBox="0 0 400 460" width="100%" height="100%"><defs><radialGradient id="wf" cx=".45" cy=".4" r=".7"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#EDE4DA"/></radialGradient>
<linearGradient id="wr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5A4A3E"/><stop offset=".5" stop-color="#2A2018"/><stop offset="1" stop-color="#14100C"/></linearGradient></defs>
<rect x="170" y="8" width="60" height="40" rx="10" fill="#E8402E"/><rect x="186" y="44" width="28" height="26" fill="#2A2018"/>
<circle cx="200" cy="260" r="186" fill="url(#wr)"/><circle cx="200" cy="260" r="160" fill="url(#wf)"/>''' + \
    ''.join(f'<rect x="197" y="{108 if k % 5 else 104}" width="{6 if k % 5 else 9}" height="{16 if k % 5 else 26}" rx="3" fill="#2A2018" transform="rotate({k * 6} 200 260)"/>' for k in range(60)) + \
    '''<text x="200" y="232" text-anchor="middle" font-family="D" font-weight="900" font-size="96" fill="#2A2018">45</text>
<text x="200" y="330" text-anchor="middle" font-family="M" font-weight="700" font-size="30" fill="#9C8676" letter-spacing="4">MINUTES</text>
<g class="hand"><rect x="196" y="112" width="8" height="150" rx="4" fill="#E8402E"/></g><circle cx="200" cy="260" r="14" fill="#2A2018"/></svg>'''
HACK = '''<svg viewBox="0 0 420 460" width="100%" height="100%"><path d="M60 460 C60 330 110 250 210 250 C310 250 360 330 360 460 Z" fill="#2E2A30"/>
<path d="M120 250 C110 120 160 60 210 60 C260 60 310 120 300 250 C290 300 130 300 120 250 Z" fill="#3A353D"/><ellipse cx="210" cy="200" rx="62" ry="78" fill="#0E0C10"/>
<rect x="170" y="186" width="80" height="14" rx="7" fill="#9AD7FF" opacity=".85"/><rect x="90" y="360" width="240" height="100" rx="12" fill="#C9CED6"/><rect x="104" y="372" width="212" height="76" rx="6" fill="#1B2A3A"/></svg>'''


class Comp:
    def __init__(s): s.H, s.J, s.SFX = [], [], []
    def el(s, i, html, style, cls='el'): s.H.append(f'<div id="{i}" class="{cls}" style="{style}">{html}</div>')
    def js(s, x): s.J.append(x)
    def fx(s, n, t, v=.5): s.SFX.append((n, round(t, 3), v))

    def shake(s, t, amt=22, sel='#stage'):
        s.js(f'tl.fromTo("{sel}",{{x:{amt},y:{-amt * .6}}},{{x:0,y:0,duration:0.42,ease:"elastic.out(2.5,0.25)",immediateRender:false}},{t});')

    def captions(s):
        ws = B0['words']; chunks, cur = [], []
        for w in ws:
            cur.append(w)
            if len(cur) == 3 or re.search(r'[.,:?!]$', w['w']): chunks.append(cur); cur = []
        if cur: chunks.append(cur)
        for k, ch in enumerate(chunks):
            t0 = B0['start'] + ch[0]['s'] - .04
            t1 = B0['start'] + chunks[k + 1][0]['s'] - .04 if k + 1 < len(chunks) else DUR
            s.el(f'cp{k}', ' '.join(f'<span id="cw{k}_{j}">{w["w"]}</span>' for j, w in enumerate(ch)), '', cls='cap')
            s.js(f'tl.fromTo("#cp{k}",{{autoAlpha:0,y:18,scale:.9}},{{autoAlpha:1,y:0,scale:1,duration:0.14,ease:"back.out(2)",immediateRender:false}},{t0:.3f});tl.set("#cp{k}",{{autoAlpha:0}},{t1:.3f});')
            for j, w in enumerate(ch):
                s.js(f'tl.set("#cw{k}_{j}",{{attr:{{class:"hl"}}}},{B0["start"] + w["s"]:.3f});tl.set("#cw{k}_{j}",{{attr:{{class:""}}}},{(B0["start"] + w["e"] + .02) if j + 1 < len(ch) else t1:.3f});')

    def max(s, poses):
        s.H.append('<div id="maxw" style="position:absolute;left:650px;top:1330px;width:420px;height:546px;z-index:55">' + ''.join(f'<div id="mxp{k}" class="mxp"></div>' for k in range(len(poses))) + '</div>')
        s.mx = [f'const MAXC={MAXC};', 'const MXP=[' + ','.join('{' + p + '}' for _, _, p in poses) + '];',
                'MXP.forEach((p,k)=>{document.getElementById("mxp"+k).innerHTML=HOST.render(Object.assign({char:MAXC,w:420,h:546},p));});']
        for k, (a, b, _) in enumerate(poses):
            s.js(f'tl.set("#mxp{k}",{{autoAlpha:1}},{a:.3f});tl.set("#mxp{k}",{{autoAlpha:0}},{b:.3f});tl.fromTo("#maxw",{{y:24,scale:.95}},{{y:0,scale:1,duration:0.3,ease:"back.out(2.5)",immediateRender:false}},{a:.3f});')
        s.js('tl.fromTo("#maxw",{x:500},{x:0,duration:0.45,ease:"back.out(1.5)",immediateRender:false},0.1);')

    def write(s, name, css, fmt=''):
        out = Path('hf') / name
        (out / 'assets' / 'fonts').mkdir(parents=True, exist_ok=True)
        for f in ('gsap.min.js', 'vo.wav', 'bgm.wav'): shutil.copy(Path('hf/knight01-v2/assets') / f, out / 'assets' / f)
        shutil.copy('hf/host/host.js', out / 'assets' / 'host.js')
        if not (out / 'assets' / 'sfx').exists(): shutil.copytree('hf/knight01-v2/assets/sfx', out / 'assets' / 'sfx')
        for f in ('InterDisplay-Black.otf', 'JetBrainsMono-Bold.ttf'): shutil.copy(Path('hf/ast01-short/assets/fonts') / f, out / 'assets' / 'fonts' / f)
        shutil.copy('hf/thumbs/fonts/anton-latin-400-normal.woff2', out / 'assets' / 'fonts')
        shutil.copy('hf/knight01-v2/hyperframes.json', out / 'hyperframes.json')
        (out / 'meta.json').write_text(json.dumps({'id': name, 'name': name}))
        aud = [f'<audio id="vo" class="clip" src="assets/vo.wav" data-start="0" data-duration="{DUR}" data-track-index="3" data-volume="1"></audio>',
               f'<audio id="bgm" class="clip" src="assets/bgm.wav" data-start="0" data-duration="{DUR}" data-track-index="4" data-volume="0.18"></audio>']
        aud += [f'<audio id="fx{k}" class="clip" src="assets/sfx/{n}.wav" data-start="{t}" data-duration="{SFXD[n]}" data-track-index="{5 + k % 3}" data-volume="{v}"></audio>' for k, (n, t, v) in enumerate(sorted(s.SFX, key=lambda x: x[1]))]
        html = f'''<!doctype html><html><head><meta charset="UTF-8"/><script src="assets/gsap.min.js"></script><script src="assets/host.js"></script><style>{BASE_CSS}{css}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920" data-fps="30">{chr(10).join(s.H)}{chr(10).join(aud)}</div>
<script>{fmt}
{chr(10).join(getattr(s, "mx", []))}
window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});
{chr(10).join(s.J)}
tl.set({{}},{{}},{DUR});window.__timelines["main"]=tl;</script></body></html>'''
        (out / 'index.html').write_text(html)
        return out


FMT = 'function F_m(v){return "$"+Math.round(v).toLocaleString("en-US")}'

# =============================================================== S1 KINETIC SLAM
c = Comp()
c.H.append('<div id="stage" style="position:absolute;inset:0"><div class="dots" id="dots"></div>')
c.js(f'tl.to("#dots",{{x:-120,y:-200,duration:{DUR},ease:"none"}},0);')
c.el('k_in', 'IN', 'left:0;right:0;top:590px;text-align:center', cls='el small')
c.js(f'tl.fromTo("#k_in",{{autoAlpha:0,y:-60}},{{autoAlpha:1,y:0,duration:0.2,immediateRender:false}},{T("in") - .05});')
c.el('k45', '<span>4</span><span>5</span>', 'left:0;right:0;top:680px;text-align:center', cls='el giant')
c.js(f'tl.set("#k45",{{autoAlpha:1}},{T("45") - .2});tl.fromTo("#k45 span",{{scale:3.4,autoAlpha:0,rotation:(i)=>i?14:-14}},{{scale:1,autoAlpha:1,rotation:0,duration:0.22,stagger:0.08,ease:"power4.in",immediateRender:false}},{T("45") - .2});')
c.shake(T('45') + .1, 30); c.fx('impact', T('45') + .05, .7)
c.el('kmin', ''.join(f'<span>{ch}</span>' for ch in 'MINUTES'), 'left:0;right:0;top:1140px;text-align:center', cls='el mid')
c.js(f'tl.set("#kmin",{{autoAlpha:1}},{T("minutes") - .1});tl.fromTo("#kmin span",{{y:-300,autoAlpha:0}},{{y:0,autoAlpha:1,stagger:0.05,duration:0.35,ease:"bounce.out",immediateRender:false}},{T("minutes") - .1});')
for k in range(4): c.fx('tick', T('minutes') + .12 * k, .4)
# whip-zoom out of the first phrase
c.js(f'tl.to(["#k_in","#k45","#kmin"],{{scale:4,autoAlpha:0,filter:"blur(18px)",duration:0.3,ease:"power3.in"}},{T("company") - .3});')
c.fx('whoosh', T('company') - .3, .5)
c.el('kco', 'A COMPANY', 'left:0;right:0;top:620px;text-align:center', cls='el mid')
c.js(f'tl.fromTo("#kco",{{autoAlpha:0,x:-900,skewX:30}},{{autoAlpha:1,x:0,skewX:0,duration:0.3,ease:"expo.out",immediateRender:false}},{T("a") - .05});')
c.el('klost', 'LOST', 'left:0;right:0;top:730px;text-align:center', cls='el giant red')
c.js(f'tl.fromTo("#klost",{{autoAlpha:0,scale:3}},{{autoAlpha:1,scale:1,duration:0.2,ease:"power4.in",immediateRender:false}},{T("lost") - .12});')
c.shake(T('lost') + .08, 26); c.fx('impact', T('lost') + .05, .6)
c.el('kcrack', '<svg viewBox="0 0 600 300" width="900" height="450"><path d="M300 0 L280 90 L330 130 L290 200 L320 300 M280 90 L200 120 M330 130 L420 110" stroke="#2A2018" stroke-width="10" fill="none" stroke-linecap="round"/></svg>', 'left:90px;top:700px;z-index:5')
c.js(f'tl.fromTo("#kcrack path",{{strokeDasharray:900,strokeDashoffset:900}},{{strokeDashoffset:0,duration:0.25,immediateRender:false}},{T("lost") + .1});tl.set("#kcrack",{{autoAlpha:1}},{T("lost") + .1});')
c.js(f'tl.to(["#kco","#klost","#kcrack"],{{y:-700,autoAlpha:0,duration:0.35,ease:"power3.in"}},{T("460") - .35});')
# slot-machine roll of $460,000,000 with falling bills
digits = '$460,000,000'
reel = ''
for k, ch in enumerate(digits):
    if ch.isdigit():
        col = ''.join(f'<b>{(int(ch) + 10 - j) % 10}</b>' for j in range(12, -1, -1))
        reel += f'<span class="rl"><span class="rc" id="rc{k}">{col}</span></span>'
    else:
        reel += f'<span class="rs">{ch}</span>'
c.el('kroll', reel, 'left:0;right:0;top:900px;text-align:center', cls='el roll')
c.js(f'tl.set("#kroll",{{autoAlpha:1}},{T("460") - .1});')
for k, ch in enumerate(digits):
    if ch.isdigit():
        c.js(f'tl.fromTo("#rc{k}",{{yPercent:0}},{{yPercent:{-100 * 12 / 13:.4f},duration:{1.2 + k * .12:.2f},ease:"power3.out",immediateRender:false}},{T("460") - .1});')
c.fx('chain', T('460'), .4)
bills = ''.join(f'<i style="left:{(k * 137) % 1080}px;transform:rotate({(k * 47) % 60 - 30}deg)"></i>' for k in range(26))
c.el('kbills', bills, 'left:0;top:0;width:1080px;height:1920px;z-index:2')
c.js(f'tl.set("#kbills",{{autoAlpha:1}},{T("million") - .2});tl.fromTo("#kbills i",{{y:-200}},{{y:2100,rotation:"+=220",duration:1.6,stagger:{{each:0.04,from:"random"}},ease:"power1.in",immediateRender:false}},{T("million") - .2});')
c.el('kdol', 'DOLLARS', 'left:0;right:0;top:1160px;text-align:center', cls='el mid red')
c.js(f'tl.fromTo("#kdol",{{autoAlpha:0,scale:2.6}},{{autoAlpha:1,scale:1,duration:0.18,ease:"power4.in",immediateRender:false}},{T("dollars") - .1});')
c.shake(T('dollars') + .08, 34); c.fx('impact', T('dollars') + .05, .7)
c.js(f'tl.fromTo("#flash",{{autoAlpha:.9}},{{autoAlpha:0,duration:0.3,immediateRender:false}},{T("dollars") + .06});')
c.js(f'tl.to(["#kroll","#kdol"],{{scale:.2,rotation:-25,autoAlpha:0,duration:0.3,ease:"back.in(2)"}},{T("no") - .3});')
# NO HACKER: letters explode outward
c.el('kno', 'NO', 'left:0;right:0;top:680px;text-align:center', cls='el giant')
c.js(f'tl.fromTo("#kno",{{autoAlpha:0,scale:3}},{{autoAlpha:1,scale:1,duration:0.18,ease:"power4.in",immediateRender:false}},{T("no") - .1});')
c.el('khk', ''.join(f'<span>{ch}</span>' for ch in 'HACKER'), 'left:0;right:0;top:1020px;text-align:center', cls='el mid')
c.js(f'tl.set("#khk",{{autoAlpha:1}},{T("hacker") - .1});tl.fromTo("#khk span",{{autoAlpha:0,y:80}},{{autoAlpha:1,y:0,stagger:0.03,duration:0.15,immediateRender:false}},{T("hacker") - .1});')
c.js(f'tl.to("#khk span",{{x:(i)=>(i-2.5)*260,y:(i)=>(i%2?-1:1)*420,rotation:(i)=>(i-2.5)*60,autoAlpha:0,duration:0.55,ease:"power3.out"}},{T("hacker") + .45});')
c.fx('glitch', T('hacker') + .4, .5)
c.el('kslash', '', f'left:120px;top:920px;width:840px;height:34px;border-radius:17px;background:{ACC2};transform-origin:0 50%;transform:rotate(-12deg);z-index:6')
c.js(f'tl.fromTo("#kslash",{{autoAlpha:1,scaleX:0}},{{scaleX:1,duration:0.18,immediateRender:false}},{T("hacker") + .2});tl.to(["#kno","#kslash"],{{autoAlpha:0,duration:0.2}},{T("just") - .2});')
c.fx('rip', T('hacker') + .2, .5)
# JUST ONE MISSED STEP: marker highlight draws under MISSED
c.el('kj', 'JUST ONE', 'left:0;right:0;top:730px;text-align:center', cls='el mid')
c.js(f'tl.fromTo("#kj",{{autoAlpha:0,y:120}},{{autoAlpha:1,y:0,duration:0.25,ease:"back.out(2)",immediateRender:false}},{T("just") - .05});')
c.el('kms', '<span class="mk"></span>MISSED<br>STEP', 'left:0;right:0;top:900px;text-align:center', cls='el giant2')
c.js(f'tl.fromTo("#kms",{{autoAlpha:0,scale:2.6}},{{autoAlpha:1,scale:1,duration:0.2,ease:"power4.in",immediateRender:false}},{T("missed") - .12});tl.fromTo("#kms .mk",{{scaleX:0}},{{scaleX:1,duration:0.3,ease:"power2.out",immediateRender:false}},{T("missed") + .1});')
c.shake(T('step') + .05, 24); c.fx('impact', T('missed') - .02, .6); c.fx('powerdown', T('step'), .45)
c.js(f'tl.fromTo("#stage",{{scale:1}},{{scale:1.06,duration:{DUR},ease:"none",immediateRender:false}},0);')
c.H.append('</div><div id="flash" style="position:absolute;inset:0;background:#fff;opacity:0;visibility:hidden;z-index:80"></div>')
css1 = f'''.small{{font:900 90px 'D';color:{INK}}} .giant{{font:400 420px/1 'A';color:{INK}}} .giant span{{display:inline-block}} .red{{background:{GR};-webkit-background-clip:text;color:transparent}}
.mid{{font:400 170px/1 'A';color:{INK};letter-spacing:4px}} .mid span{{display:inline-block}} .giant2{{font:400 300px/.95 'A';color:{INK};position:absolute}}
.mk{{position:absolute;left:150px;top:150px;width:780px;height:90px;background:{GR};opacity:.85;transform-origin:0 50%;z-index:-1;border-radius:10px}}
.roll{{font:400 150px/1 'A';color:{INK};white-space:nowrap}} .rl{{display:inline-block;height:150px;overflow:hidden;vertical-align:top}} .rc{{display:flex;flex-direction:column}} .rc b{{font-weight:400;height:150px;display:block}} .rs{{display:inline-block}}
#kbills i{{position:absolute;top:0;width:110px;height:56px;border-radius:8px;background:linear-gradient(135deg,#7BC67E,#3E8E41);border:4px solid #2F6B32;box-shadow:0 8px 14px rgba(0,0,0,.15)}}'''
p1 = c.write('style-s1', css1, FMT)

# =============================================================== S2 CAMERA JOURNEY (one canvas, camera flies)
c = Comp()
# canvas 2400x3600; objects placed; camera = #world transform
c.H.append('<div id="cam" style="position:absolute;inset:0;transform-origin:50% 50%"><div id="world" style="position:absolute;left:0;top:0;width:2400px;height:3600px"><div class="dots" id="pdots" style="inset:-400px"></div>')
c.el('w_watch', f'<div style="width:560px;height:640px">{WATCH}</div>', 'left:200px;top:300px', cls='obj')
c.el('w_term', '<div class="term"><div class="tbar">KNIGHT · P&amp;L · AUG 1</div><div class="tnum" id="tn">$0</div><svg viewBox="0 0 640 240" width="640" height="240"><path id="crash" d="M10 60 L80 70 L140 52 L200 80 L250 76 L300 120 L350 112 L400 160 L450 150 L500 200 L560 214 L630 232" fill="none" stroke="#FF5A47" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/></svg></div><div class="siren"><i class="glow"></i><i class="cap"></i></div>', 'left:1300px;top:420px', cls='obj')
c.el('w_hack', f'<div style="width:520px;height:570px;position:relative">{HACK}<svg viewBox="0 0 400 400" width="520" height="520" style="position:absolute;left:0;top:20px"><path id="x1" d="M50 50 L350 350" stroke="#E8402E" stroke-width="44" stroke-linecap="round"/><path id="x2" d="M350 50 L50 350" stroke="#E8402E" stroke-width="44" stroke-linecap="round"/></svg></div>', 'left:1500px;top:1700px', cls='obj')
steps = ''.join(f'<div class="step" style="left:{k * 250}px;top:{500 - k * 160}px;height:{160 + k * 160}px"><b>{t}</b>{"<em>✓</em>" if k < 2 else ""}</div>' for k, t in enumerate(['WRITE CODE', 'TEST IT'])) + \
        '<div class="gap" style="left:500px;top:180px;height:480px"><b>COPY TO<br>ALL 8</b></div><div class="step" style="left:750px;top:20px;height:640px"><b>DEPLOY</b></div><div class="ball" id="ball"></div><div class="beam"></div>'
c.el('w_stairs', steps, 'left:300px;top:2600px;width:1000px;height:660px', cls='obj')
c.H.append('</div></div>')
# camera keyframes: (time, centre x, centre y, scale, rotation)
CAM = [(0, 480, 620, 1.35, 0), (T('company') - .3, 1660, 760, 1.25, -3), (T('no') - .35, 1760, 2000, 1.2, 4), (T('just') - .35, 820, 2900, 1.0, -2)]
c.js(f'gsap.set("#world",{{x:{540 - CAM[0][1]},y:{900 - CAM[0][2]}}});gsap.set("#cam",{{scale:{CAM[0][3]}}});')
for t, x, y, sc, rot in CAM[1:]:
    c.js(f'tl.to("#world",{{x:{540 - x},y:{900 - y},duration:0.55,ease:"power3.inOut"}},{t:.3f});tl.to("#cam",{{scale:{sc},rotation:{rot},duration:0.55,ease:"power3.inOut"}},{t:.3f});')
    c.js(f'tl.fromTo("#cam",{{filter:"blur(0px)"}},{{filter:"blur(10px)",duration:0.27,yoyo:true,repeat:1,immediateRender:false}},{t:.3f});')
    c.fx('whoosh', t, .45)
c.js(f'tl.to("#pdots",{{x:240,y:400,duration:{DUR},ease:"none"}},0);')
c.js(f'tl.to("#cam",{{scale:"+=0.08",duration:1.6,ease:"none"}},0.2);')
# objects acting
c.js('tl.set(".obj",{autoAlpha:1},0);')
c.js(f'tl.fromTo("#w_watch",{{y:-900}},{{y:0,duration:0.42,ease:"power3.in",immediateRender:false}},{T("45") - .45});tl.to("#w_watch",{{scaleY:.86,scaleX:1.1,duration:0.08,yoyo:true,repeat:1,transformOrigin:"50% 100%"}},{T("45") - .03});')
c.fx('thud', T('45') - .03, .7)
c.js(f'tl.fromTo("#w_watch .hand",{{rotation:0,svgOrigin:"200 260"}},{{rotation:720,svgOrigin:"200 260",duration:2.2,ease:"none",immediateRender:false}},{T("45")});')
c.js(f'tl.fromTo("#crash",{{strokeDasharray:900,strokeDashoffset:900}},{{strokeDashoffset:0,duration:2.6,ease:"power1.in",immediateRender:false}},{T("lost")});')
c.js(f'(function(){{const o={{v:0}};tl.to(o,{{v:460000000,duration:{T("dollars") - T("lost"):.2f},ease:"power2.in",onUpdate:()=>{{document.getElementById("tn").textContent="-"+F_m(o.v)}}}},{T("lost")});}})();')
c.js(f'tl.set("#tn",{{textContent:"-$460M"}},{T("dollars") + .02});tl.fromTo("#tn",{{scale:1.6}},{{scale:1,duration:0.45,ease:"back.out(3)",immediateRender:false}},{T("dollars") + .02});')
c.js(f'tl.fromTo("#w_term .glow",{{autoAlpha:0}},{{autoAlpha:1,duration:0.12,repeat:11,yoyo:true,immediateRender:false}},{T("lost")});')
c.shake(T('dollars') + .05, 26, '#cam'); c.fx('error', T('lost'), .4); c.fx('impact', T('dollars'), .7)
c.js(f'tl.fromTo("#w_hack",{{y:500,autoAlpha:0}},{{y:0,autoAlpha:1,duration:0.45,ease:"back.out(1.6)",immediateRender:false}},{T("no") - .2});')
c.js(f'tl.fromTo(["#x1","#x2"],{{strokeDasharray:480,strokeDashoffset:480}},{{strokeDashoffset:0,duration:0.16,stagger:0.16,immediateRender:false}},{T("hacker")});')
c.fx('rip', T('hacker'), .45); c.fx('rip', T('hacker') + .16, .45)
c.js(f'tl.fromTo("#w_stairs .step,#w_stairs .gap",{{y:220,autoAlpha:0}},{{y:0,autoAlpha:1,stagger:0.09,duration:0.35,ease:"back.out(2)",immediateRender:false}},{T("just") - .2});')
c.js(f'tl.fromTo("#ball",{{x:60,y:260,autoAlpha:1}},{{x:310,y:80,duration:0.35,ease:"power1.out",immediateRender:false}},{T("one") - .05});tl.to("#ball",{{x:560,y:40,duration:0.3}},{T("missed") - .3});tl.to("#ball",{{y:900,rotation:200,duration:0.5,ease:"power2.in"}},{T("missed") + .05});')
c.js(f'tl.fromTo("#w_stairs .beam",{{autoAlpha:0,scaleY:0}},{{autoAlpha:1,scaleY:1,transformOrigin:"50% 0%",duration:0.25,immediateRender:false}},{T("missed")});')
c.fx('powerdown', T('step'), .45)
c.captions()
c.max([(0.1, T('no') - .1, "brows:'high',eyes:'wide',mouth:'shock',arms:'hands-up',extra:['bang']"), (T('no') - .1, T('just') - .1, "brows:'skeptic',eyes:'open',mouth:'flat',arms:'shrug',extra:['question']"), (T('just') - .1, DUR, "brows:'worried',eyes:'closed',mouth:'frown',arms:'facepalm'")])
css2 = f'''.obj{{position:absolute;opacity:0;visibility:hidden;filter:drop-shadow(0 40px 50px rgba(74,50,28,.3))}}
.term{{width:760px;height:540px;border-radius:44px;background:linear-gradient(180deg,#2E241C,#1C1510);padding:34px 44px}} .tbar{{font:700 28px 'M';color:#9C8676;letter-spacing:2px}}
.tnum{{font:900 92px 'D';color:#FF5A47;letter-spacing:-4px;margin:20px 0 10px}}
.siren{{position:absolute;left:300px;top:-120px;width:150px;height:130px}} .siren .cap{{position:absolute;left:20px;top:10px;width:110px;height:110px;border-radius:55px 55px 10px 10px;background:#C0392B}}
.siren .glow{{position:absolute;left:-120px;top:-120px;width:390px;height:350px;border-radius:50%;background:radial-gradient(circle,rgba(255,70,50,.8),transparent 65%);opacity:0;visibility:hidden}}
.step{{position:absolute;width:250px;border-radius:18px 18px 0 0;background:linear-gradient(180deg,#FFFAF7,#EFE2D6);border:4px solid #E0CDBC;padding:22px 14px;text-align:center}}
.step b{{font:900 36px/1.1 'D';color:{INK}}} .step em{{display:block;margin:16px auto 0;width:66px;height:66px;border-radius:33px;background:{GREEN};color:#fff;font:900 40px/66px 'D';font-style:normal}}
.gap{{position:absolute;width:250px;border:6px dashed {ACC2};border-bottom:none;border-radius:18px 18px 0 0;text-align:center;padding-top:26px;background:rgba(232,64,46,.06)}} .gap b{{font:900 36px/1.15 'D';color:{ACC2}}}
.ball{{position:absolute;left:0;top:0;width:96px;height:96px;border-radius:22px;background:{GR};opacity:0;visibility:hidden}} .ball:after{{content:'v2';position:absolute;inset:0;font:900 40px/96px 'D';color:#fff;text-align:center}}
.beam{{position:absolute;left:440px;top:-500px;width:380px;height:1200px;background:linear-gradient(180deg,rgba(255,250,235,.95),rgba(255,240,210,0));clip-path:polygon(38% 0,62% 0,100% 100%,0 100%);opacity:0;visibility:hidden}}'''
p2 = c.write('style-s2', css2, FMT)

# =============================================================== S3 WHIP & FLIP (full-screen cards)
c = Comp()
CARDS = [  # (id, start word, background, inner html)
    ('c1', 'in', CREAM, f'<div style="width:620px;height:710px;margin:300px auto 0">{WATCH}</div>'),
    ('c2', 'company', '#2A2018', '<div class="t3">KNIGHT CAPITAL · AUG 1</div><div class="bignum" id="c2n">$0</div><div class="arrow">▼</div>'),
    ('c3', 'no', '#141017', f'<div style="width:560px;height:620px;margin:360px auto 0;position:relative" id="c3h">{HACK}</div><div class="glitchtxt" data-t="NO HACKER">NO HACKER</div>'),
    ('c4', 'just', GR, '<div class="step3"><div><b>✓</b>WRITE CODE</div><div><b>✓</b>TEST IT</div><div class="miss"><b>✗</b>COPY TO ALL 8 SERVERS</div></div>'),
]
for k, (i, w, bg, inner) in enumerate(CARDS):
    t = T(w) - (.05 if k == 0 else .22)
    c.el(i, inner, f'left:0;top:0;width:1080px;height:1920px;background:{bg};z-index:{10 + k}', cls='el card3')
    if k == 0:
        c.js(f'tl.fromTo("#{i}",{{autoAlpha:0,scale:1.3}},{{autoAlpha:1,scale:1,duration:0.35,ease:"expo.out",immediateRender:false}},{t:.3f});')
    elif k % 2:
        c.js(f'tl.fromTo("#{i}",{{autoAlpha:1,x:1200,skewX:-18,filter:"blur(24px)"}},{{x:0,skewX:0,filter:"blur(0px)",duration:0.32,ease:"expo.out",immediateRender:false}},{t:.3f});')
        c.js(f'tl.to("#{CARDS[k - 1][0]}",{{x:-1200,skewX:18,filter:"blur(24px)",duration:0.32,ease:"expo.out"}},{t:.3f});')
        c.fx('whoosh', t, .55)
    else:
        c.js(f'tl.fromTo("#{i}",{{autoAlpha:1,rotationY:-95,transformPerspective:1600,transformOrigin:"0% 50%"}},{{rotationY:0,duration:0.42,ease:"back.out(1.2)",immediateRender:false}},{t:.3f});')
        c.js(f'tl.to("#{CARDS[k - 1][0]}",{{rotationY:60,transformPerspective:1600,transformOrigin:"100% 50%",autoAlpha:0,duration:0.42,ease:"power2.in"}},{t:.3f});')
        c.fx('flip', t, .55)
c.js(f'tl.fromTo("#c1 .hand",{{rotation:0,svgOrigin:"200 260"}},{{rotation:540,svgOrigin:"200 260",duration:1.8,ease:"none",immediateRender:false}},{T("45")});')
c.js(f'tl.fromTo("#c1 svg",{{scale:1.4}},{{scale:1,duration:0.35,ease:"back.out(2.5)",immediateRender:false}},{T("45")});')
c.fx('impact', T('45'), .55)
c.js(f'(function(){{const o={{v:0}};tl.to(o,{{v:460000000,duration:{T("dollars") - T("lost"):.2f},ease:"power2.in",onUpdate:()=>{{document.getElementById("c2n").textContent="-"+F_m(o.v)}}}},{T("lost")});}})();')
c.js(f'tl.set("#c2n",{{textContent:"-$460M"}},{T("dollars") + .02});tl.fromTo("#c2n",{{scale:1.9}},{{scale:1,duration:0.4,ease:"back.out(3)",immediateRender:false}},{T("dollars") + .02});')
c.js(f'tl.fromTo("#c2 .arrow",{{y:-100,autoAlpha:0}},{{y:120,autoAlpha:1,duration:0.6,repeat:4,ease:"power2.in",immediateRender:false}},{T("lost")});')
c.js(f'tl.fromTo("#c2",{{scale:1}},{{scale:1.12,duration:0.12,yoyo:true,repeat:1,immediateRender:false}},{T("dollars") + .02});')
c.fx('impact', T('dollars'), .7); c.fx('error', T('lost'), .4)
c.js(f'tl.fromTo("#c3 .glitchtxt",{{autoAlpha:0}},{{autoAlpha:1,duration:0.05,immediateRender:false}},{T("hacker")});tl.fromTo("#c3 .glitchtxt",{{x:-20,skewX:20}},{{x:0,skewX:0,duration:0.06,repeat:7,yoyo:true,immediateRender:false}},{T("hacker")});')
c.js(f'tl.fromTo("#c3h",{{x:-14}},{{x:14,duration:0.05,repeat:9,yoyo:true,immediateRender:false}},{T("hacker")});')
c.fx('glitch', T('hacker'), .55); c.fx('static', T('hacker') + .1, .3)
c.js(f'tl.fromTo("#c4 .step3 div",{{x:-700,autoAlpha:0}},{{x:0,autoAlpha:1,stagger:0.18,duration:0.3,ease:"back.out(1.8)",immediateRender:false}},{T("just") - .05});')
c.js(f'tl.fromTo("#c4 .miss",{{scale:1}},{{scale:1.12,duration:0.1,repeat:5,yoyo:true,immediateRender:false}},{T("missed")});tl.fromTo("#c4",{{scale:1}},{{scale:1.15,duration:0.5,ease:"power2.out",immediateRender:false}},{T("missed")});')
c.fx('error', T('missed'), .45); c.fx('powerdown', T('step'), .45)
c.captions()
c.max([(T('no') - .15, T('just') - .25, "brows:'skeptic',eyes:'open',mouth:'flat',arms:'shrug',extra:['question']"), (T('just') - .2, DUR, "brows:'worried',eyes:'closed',mouth:'frown',arms:'facepalm'")])
css3 = f'''.card3{{overflow:hidden}} .t3{{font:700 40px 'M';color:#9C8676;letter-spacing:3px;text-align:center;margin-top:330px}}
.bignum{{font:400 150px/1 'A';color:#FF5A47;text-align:center;margin-top:60px}} .arrow{{font:400 260px/1 'A';color:#FF5A47;text-align:center}}
.glitchtxt{{position:absolute;left:0;right:0;top:1000px;text-align:center;font:400 210px/1 'A';color:#fff;text-shadow:-10px 0 #ff2a6d,10px 0 #05d9e8}}
.step3{{margin:330px 70px 0}} .step3 div{{display:flex;align-items:center;gap:30px;margin-bottom:40px;padding:34px 40px;border-radius:30px;background:rgba(255,250,247,.95);font:900 60px 'D';color:{INK}}}
.step3 b{{width:90px;height:90px;border-radius:45px;background:{GREEN};color:#fff;font:900 56px/90px 'D';text-align:center;flex:none}} .step3 .miss{{background:#2A2018;color:#fff}} .step3 .miss b{{background:{ACC2}}}
.cap{{z-index:70;color:#fff;-webkit-text-stroke:12px #2A2018;paint-order:stroke fill}} .cap span.hl{{-webkit-text-stroke:0}}'''
p3 = c.write('style-s3', css3, FMT)

import os
for p in (() if os.environ.get('NORENDER') else (p1, p2, p3)):
    o = p / 'out' / 'sample.mp4'; o.parent.mkdir(exist_ok=True)
    r = subprocess.run(CLI + ['render', str(p), '--quality', 'looks', '-o', str(o)], capture_output=True, text=True)
    print(p.name, 'OK' if o.exists() else 'FAIL ' + (r.stdout + r.stderr)[-300:])
