"""Story Short v2 (owner feedback 2026-11-24 on knight01 v1): OLD layout (captions mid-lower, 1-3 words, current word
highlighted; Max smaller, bottom-right, only at key moments) + reference-style ACTING objects: big detailed illustrations
that do what the words say (drop in with speed lines, squash + dust on landing, X drawn stroke by stroke, siren flashing,
spotlight, pages tearing off, building rising), one scene morphing into the next.
TEST build: lines 0-1 only (first ~16 s).   Usage: python3 tools/hf_story_v2.py [--full]"""
import json, re, shutil, sys, wave
from pathlib import Path
sys.path.insert(0, 'tools')
from kit_assets import icon

TID = 'knight01-short'
OUT = Path('hf') / 'knight01-v2'
tl = json.load(open(f'src/episodes/{TID}.timeline.json'))
B = tl['beats']
LAST = 1
DUR = round(B[LAST]['start'] + B[LAST]['dur'] + 0.3, 3)
INK, ACC, ACC2, CREAM, GREEN = '#2A2018', '#F87736', '#E8402E', '#F4EDE3', '#16A34A'
H, J, SFX = [], [], []


def norm(w): return re.sub(r"[^a-z0-9]", '', w.lower())


def T(bi, word, nth=0, end=False):
    w = [w for w in B[bi]['words'] if norm(w['w']).startswith(norm(word))][nth]
    return round(B[bi]['start'] + (w['e'] if end else w['s']), 3)


def be(bi): return round(B[bi]['start'] + B[bi]['dur'], 3)
def el(i, html, style, cls='el'): H.append(f'<div id="{i}" class="{cls}" style="{style}">{html}</div>')
def js(s): J.append(s)
def sfx(n, t, v=.5): SFX.append((n, round(t, 3), v))


def drop(i, t, h=900, land_sfx='thud'):
    """falls from above with speed lines, squash on landing, dust puff"""
    js(f'tl.fromTo("#{i}",{{autoAlpha:1,y:-{h},scaleY:1.12,scaleX:.92}},{{y:0,scaleY:1,scaleX:1,duration:0.42,ease:"power3.in",immediateRender:false}},{t});')
    js(f'tl.to("#{i}",{{scaleY:.86,scaleX:1.1,duration:0.08,yoyo:true,repeat:1,ease:"power1.out",transformOrigin:"50% 100%"}},{t + .42});')
    js(f'tl.fromTo("#{i} .spd",{{autoAlpha:1,scaleY:1}},{{autoAlpha:0,scaleY:.3,duration:0.3,immediateRender:false}},{t + .3});')
    js(f'tl.fromTo("#{i} .dust i",{{autoAlpha:.8,scale:.3,x:0}},{{autoAlpha:0,scale:1.4,x:(k)=>k%2?120:-120,duration:0.55,ease:"expo.out",immediateRender:false}},{t + .42});')
    sfx('whoosh', t, .35); sfx(land_sfx, t + .42, .7)


SPD = '<div class="spd">' + ''.join(f'<i style="left:{x}%;height:{h}px"></i>' for x, h in ((18, 160), (34, 240), (50, 200), (66, 260), (82, 170))) + '</div>'
DUST = '<div class="dust">' + '<i></i>' * 4 + '</div>'


def stamp(i, t, rot=-8):
    js(f'tl.fromTo("#{i}",{{autoAlpha:0,scale:2.6,rotation:{rot}}},{{autoAlpha:1,scale:1,rotation:{rot},duration:0.18,ease:"power4.in",immediateRender:false}},{t});')
    js(f'tl.fromTo("#root",{{x:-10}},{{x:0,duration:0.3,ease:"elastic.out(3,.3)",immediateRender:false}},{t + .18});')
    sfx('stamp', t + .14, .8)


def gone(i, t, how='fade'):
    v = {'fade': 'autoAlpha:0', 'left': 'x:-1200,rotation:-8', 'down': 'y:1400,rotation:10', 'back': 'scale:.55,autoAlpha:0,filter:"blur(8px)"'}[how]
    js(f'tl.to("#{i}",{{{v},duration:0.4,ease:"power3.in"}},{t});')


def count(i, t, d, a, b, fmt):
    js(f'(function(){{const o={{v:{a}}};tl.to(o,{{v:{b},duration:{d},ease:"power2.in",onUpdate:()=>{{document.getElementById("{i}").textContent=F_{fmt}(o.v)}}}},{t});}})();')


# ------------------------------------------------------------ captions: old style (1-3 words, current word boxed)
ci = 0
for bi in range(LAST + 1):
    b = B[bi]; ws = b['words']; chunks, cur = [], []
    for w in ws:
        cur.append(w)
        if len(cur) == 3 or re.search(r'[.,:?!]$', w['w']):
            chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    for k, ch in enumerate(chunks):
        t0 = b['start'] + ch[0]['s'] - .04
        t1 = (b['start'] + chunks[k + 1][0]['s'] - .04) if k + 1 < len(chunks) else (B[bi + 1]['start'] - .04 if bi + 1 <= LAST else DUR)
        el(f'cp{ci}', ' '.join(f'<span id="cw{ci}_{j}">{w["w"]}</span>' for j, w in enumerate(ch)), 'left:40px;right:40px;top:1235px', cls='cap')
        js(f'tl.fromTo("#cp{ci}",{{autoAlpha:0,y:18,scale:.92}},{{autoAlpha:1,y:0,scale:1,duration:0.14,ease:"back.out(2)",immediateRender:false}},{t0:.3f});tl.set("#cp{ci}",{{autoAlpha:0}},{t1:.3f});')
        for j, w in enumerate(ch):
            js(f'tl.set("#cw{ci}_{j}",{{attr:{{class:"hl"}}}},{b["start"] + w["s"]:.3f});tl.set("#cw{ci}_{j}",{{attr:{{class:""}}}},{(b["start"] + w["e"] + .02) if j + 1 < len(ch) else t1:.3f});')
        ci += 1

# ------------------------------------------------------------ Max: old placement (bottom-right, smaller, key moments only)
MAXC = "{skin:'#F0C4A0',hair:'messy',hairCol:'#5A3A26',glasses:'round',hood:'down',top:'#F87736',topS:'#D85E25',phones:'none',beard:'stubble'}"
MX = [(0.1, T(0, 'no') - .1, "brows:'high',eyes:'wide',mouth:'shock',arms:'hands-up',extra:['bang']"),
      (T(0, 'no') - .1, T(0, 'just') - .1, "brows:'skeptic',eyes:'open',mouth:'flat',arms:'shrug',extra:['question']"),
      (T(0, 'just') - .1, be(0) - .1, "brows:'worried',eyes:'closed',mouth:'frown',arms:'facepalm'")]
H.append('<div id="maxw" style="position:absolute;left:650px;top:1330px;width:420px;height:546px;z-index:20">' +
         ''.join(f'<div id="mxp{k}" class="mxp"></div>' for k in range(len(MX))) + '</div>')
mxjs = [f'const MAXC={MAXC};', 'const MXP=[' + ','.join('{' + p + '}' for _, _, p in MX) + '];',
        'MXP.forEach((p,k)=>{document.getElementById("mxp"+k).innerHTML=HOST.render(Object.assign({char:MAXC,w:420,h:546},p));});']
for k, (a, b2, _) in enumerate(MX):
    js(f'tl.set("#mxp{k}",{{autoAlpha:1}},{a:.3f});tl.set("#mxp{k}",{{autoAlpha:0}},{b2:.3f});')
    js(f'tl.fromTo("#maxw",{{y:20,scale:.96}},{{y:0,scale:1,duration:0.3,ease:"back.out(2.5)",immediateRender:false}},{a:.3f});')
js('tl.fromTo("#maxw",{x:500},{x:0,duration:0.45,ease:"back.out(1.5)",immediateRender:false},0.1);')
js(f'tl.to("#maxw",{{x:520,duration:0.4,ease:"power3.in"}},{be(0) - .25});')

# ================================================================ LINE 0
# stopwatch: detailed, drops in, hand sweeps
WATCH = f'''<svg viewBox="0 0 400 460" width="460" height="530">
<defs><radialGradient id="wf" cx=".45" cy=".4" r=".7"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#EDE4DA"/></radialGradient>
<linearGradient id="wr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5A4A3E"/><stop offset=".5" stop-color="#2A2018"/><stop offset="1" stop-color="#14100C"/></linearGradient>
<linearGradient id="wb" x1="0" x2="1"><stop offset="0" stop-color="#F87736"/><stop offset="1" stop-color="#C2321F"/></linearGradient></defs>
<rect x="170" y="8" width="60" height="40" rx="10" fill="url(#wb)"/><rect x="186" y="44" width="28" height="26" fill="#2A2018"/>
<rect x="300" y="70" width="34" height="26" rx="8" fill="#2A2018" transform="rotate(40 317 83)"/>
<circle cx="200" cy="260" r="186" fill="url(#wr)"/><circle cx="200" cy="260" r="160" fill="url(#wf)"/>
<path d="M200 260 L200 100 A160 160 0 0 1 338.6 340 Z" fill="#E8402E" opacity=".16" id="wsec"/>
{''.join(f'<rect x="197" y="{108 if k % 5 else 104}" width="{6 if k % 5 else 9}" height="{16 if k % 5 else 26}" rx="3" fill="#2A2018" transform="rotate({k * 6} 200 260)"/>' for k in range(60))}
<text x="200" y="330" text-anchor="middle" font-family="M" font-weight="700" font-size="30" fill="#9C8676" letter-spacing="4">MINUTES</text>
<text x="200" y="232" text-anchor="middle" font-family="D" font-weight="900" font-size="96" fill="#2A2018">45</text>
<g id="whand"><rect x="196" y="112" width="8" height="150" rx="4" fill="#E8402E"/></g><circle cx="200" cy="260" r="14" fill="#2A2018"/><circle cx="200" cy="260" r="5" fill="#E8402E"/>
<ellipse cx="140" cy="160" rx="60" ry="26" fill="#fff" opacity=".5" transform="rotate(-30 140 160)"/></svg>'''
el('s0w', WATCH + SPD + DUST, 'left:310px;top:250px;width:460px;height:530px')
drop('s0w', T(0, '45') - .42)
js(f'tl.fromTo("#whand",{{rotation:0,svgOrigin:"200 260"}},{{rotation:270,svgOrigin:"200 260",duration:{T(0, "company") - T(0, "45") + .3:.2f},ease:"none",immediateRender:false}},{T(0, "45")});')
for k in range(5): sfx('tick', T(0, '45') + .3 * k, .35)
js(f'tl.to("#s0w",{{x:-250,y:-140,scale:.55,duration:0.45,ease:"power3.inOut"}},{T(0, "company") - .2});')
# trading terminal with crashing chart + siren
CHART = '<svg viewBox="0 0 640 240" width="640" height="240" class="chart"><path id="crash" d="M10 60 L80 70 L140 52 L200 80 L250 76 L300 120 L350 112 L400 160 L450 150 L500 200 L560 214 L630 232" fill="none" stroke="#FF5A47" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/></svg>'
TERM = f'''<div class="siren"><i class="glow"></i><i class="cap"></i><i class="base"></i></div>
<div class="term"><div class="tbar"><i></i><i></i><i></i><span>KNIGHT · P&amp;L · AUG 1</span></div>
<div class="tnum" id="s0n">$0</div>{CHART}</div>'''
el('s0t', TERM, 'left:180px;top:300px;z-index:4;width:720px;height:620px')
js(f'tl.fromTo("#s0t",{{autoAlpha:0,rotationX:70,y:200,transformPerspective:1400,transformOrigin:"50% 100%"}},{{autoAlpha:1,rotationX:0,y:0,duration:0.55,ease:"back.out(1.3)",immediateRender:false}},{T(0, "company") - .1});')
sfx('whoosh', T(0, 'company') - .1, .4)
js(f'tl.fromTo("#crash",{{strokeDasharray:900,strokeDashoffset:900}},{{strokeDashoffset:0,duration:{T(0, "dollars") - T(0, "lost") + .2:.2f},ease:"power1.in",immediateRender:false}},{T(0, "lost")});')
count('s0n', T(0, 'lost'), T(0, 'dollars') - T(0, 'lost'), 0, -460000000, 'neg')
js(f'tl.set("#s0n",{{textContent:"-$460M"}},{T(0, "dollars") + .02});tl.fromTo("#s0n",{{scale:1.6}},{{scale:1,duration:0.45,ease:"back.out(3)",immediateRender:false}},{T(0, "dollars") + .02});')
js(f'tl.fromTo("#s0t .glow",{{autoAlpha:0}},{{autoAlpha:1,duration:0.12,repeat:9,yoyo:true,immediateRender:false}},{T(0, "lost")});tl.to("#s0t .cap",{{backgroundColor:"#FF3B2E",duration:0.1}},{T(0, "lost")});')
sfx('error', T(0, 'lost'), .4); sfx('impact', T(0, 'dollars'), .6)
el('s0imp', ''.join(f'<i style="transform:rotate({a}deg)"></i>' for a in range(0, 360, 40)), 'left:540px;top:520px;width:0;height:0', cls='el imp')
js(f'tl.fromTo("#s0imp",{{autoAlpha:1,scale:.4}},{{autoAlpha:0,scale:1.3,duration:0.5,ease:"expo.out",immediateRender:false}},{T(0, "dollars") + .02});')
# "No hacker": scene pushes back, hooded hacker rises, X drawn in two strokes
gone('s0t', T(0, 'no') - .25, 'back'); gone('s0w', T(0, 'no') - .25, 'back')
HACK = '''<svg viewBox="0 0 420 460" width="480" height="525"><defs><radialGradient id="hs" cx=".5" cy=".75" r=".55"><stop offset="0" stop-color="#9AD7FF" stop-opacity=".55"/><stop offset="1" stop-color="#9AD7FF" stop-opacity="0"/></radialGradient></defs>
<ellipse cx="210" cy="300" rx="200" ry="150" fill="url(#hs)"/>
<path d="M60 460 C60 330 110 250 210 250 C310 250 360 330 360 460 Z" fill="#2E2A30"/>
<path d="M120 250 C110 120 160 60 210 60 C260 60 310 120 300 250 C290 300 130 300 120 250 Z" fill="#3A353D"/>
<ellipse cx="210" cy="200" rx="62" ry="78" fill="#0E0C10"/><rect x="170" y="186" width="80" height="14" rx="7" fill="#9AD7FF" opacity=".85"/>
<rect x="90" y="360" width="240" height="100" rx="12" fill="#C9CED6"/><rect x="104" y="372" width="212" height="76" rx="6" fill="#1B2A3A"/><circle cx="210" cy="410" r="12" fill="#9AD7FF" opacity=".6"/></svg>'''
el('s0h', HACK + '<svg class="xs" viewBox="0 0 400 400" width="460" height="460"><path id="x1" d="M50 50 L350 350" stroke="#E8402E" stroke-width="44" stroke-linecap="round"/><path id="x2" d="M350 50 L50 350" stroke="#E8402E" stroke-width="44" stroke-linecap="round"/></svg>',
   'left:300px;top:330px;width:480px;height:525px')
js(f'tl.fromTo("#s0h",{{autoAlpha:0,y:420}},{{autoAlpha:1,y:0,duration:0.4,ease:"back.out(1.6)",immediateRender:false}},{T(0, "no") - .15});')
js(f'tl.fromTo(["#x1","#x2"],{{strokeDasharray:480,strokeDashoffset:480}},{{strokeDashoffset:0,duration:0.16,stagger:0.16,ease:"power2.out",immediateRender:false}},{T(0, "hacker")});')
js(f'tl.to(["#x1","#x2"],{{stroke:"#2A2018",duration:0.3}},{T(0, "hacker") + .5});')
sfx('rip', T(0, 'hacker'), .4); sfx('rip', T(0, 'hacker') + .16, .4)
gone('s0h', T(0, 'just') - .25, 'left')
# "Just one missed step": staircase, the third step missing, spotlight on the gap, a code block falls through
STAIR = ''.join(f'<div class="step" style="left:{60 + k * 230}px;top:{600 - k * 150}px;height:{150 + k * 150}px"><b>{t}</b>{"<em>✓</em>" if k < 2 else ""}</div>'
                for k, t in enumerate(['WRITE CODE', 'TEST IT'])) + \
        '<div class="gap" style="left:520px;top:300px;height:450px"><b>COPY TO<br>ALL 8</b></div>' + \
        '<div class="step" style="left:750px;top:150px;height:600px"><b>DEPLOY</b></div>'
el('s0s', '<div class="beam"></div>' + STAIR + '<div class="ball" id="s0b"></div>', 'left:60px;top:300px;width:960px;height:760px')
js(f'tl.fromTo("#s0s",{{autoAlpha:0,x:900}},{{autoAlpha:1,x:0,duration:0.45,ease:"expo.out",immediateRender:false}},{T(0, "just") - .2});')
js(f'tl.fromTo("#s0s .step",{{y:200,autoAlpha:0}},{{y:0,autoAlpha:1,stagger:0.1,duration:0.3,ease:"back.out(2)",immediateRender:false}},{T(0, "just") - .1});')
js(f'tl.fromTo("#s0s .beam",{{autoAlpha:0,scaleY:0}},{{autoAlpha:1,scaleY:1,duration:0.25,transformOrigin:"50% 0%",immediateRender:false}},{T(0, "missed")});')
js(f'tl.fromTo("#s0b",{{x:120,y:380,autoAlpha:1}},{{x:350,y:230,duration:0.35,ease:"power1.out",immediateRender:false}},{T(0, "one") - .05});')
js(f'tl.to("#s0b",{{x:560,y:200,duration:0.3,ease:"power1.out"}},{T(0, "missed") - .25});tl.to("#s0b",{{y:900,rotation:200,duration:0.5,ease:"power2.in"}},{T(0, "missed") + .05});')
sfx('scan', T(0, 'missed'), .4); sfx('powerdown', T(0, 'step'), .45)
gone('s0s', be(0) - .25, 'left')

# ================================================================ LINE 1
CAL = '''<div class="pin"></div><div class="calb"><div class="ch">AUGUST</div><div class="cn">1</div><div class="cy" id="s1y">2012</div></div>'''
pages = ''.join(f'<div class="calp" id="cp_{k}"><div class="ch" style="background:#9C8676">JULY</div><div class="cn">{d}</div><div class="cy">2012</div></div>' for k, d in enumerate(['29', '30', '31']))
el('s1c', CAL + pages + SPD + DUST, 'left:300px;top:260px;width:480px;height:600px')
drop('s1c', T(1, 'august') - .45)
for k in range(3):
    js(f'tl.to("#cp_{k}",{{rotationX:-110,y:-60,x:{(k - 1) * 260},rotation:{(k - 1) * 30},autoAlpha:0,transformPerspective:1000,transformOrigin:"50% 0%",duration:0.45,ease:"power2.in"}},{T(1, "august") + .1 + .14 * (2 - k)});')
    sfx('flip', T(1, 'august') + .1 + .14 * (2 - k), .5)
js(f'tl.fromTo("#s1y",{{scale:1.7,color:"#E8402E"}},{{scale:1,color:"#2A2018",duration:0.45,ease:"back.out(3)",immediateRender:false}},{T(1, "2012")});')
js(f'tl.to("#s1c",{{x:-270,y:-110,scale:.42,rotation:-6,duration:0.5,ease:"power3.inOut"}},{T(1, "knight") - .35});')
win = ''.join(f'<i style="left:{40 + (k % 5) * 64}px;top:{110 + (k // 5) * 62}px"></i>' for k in range(45))
TOWER = f'<div class="tower"><div class="sign">KNIGHT CAPITAL</div><div class="tw">{win}</div></div>'
el('s1b', TOWER, 'left:330px;top:360px;width:420px;height:820px')
js(f'tl.fromTo("#s1b",{{autoAlpha:1,y:820,clipPath:"inset(-200px -300px 100% -300px)"}},{{y:0,clipPath:"inset(-200px -300px 0% -300px)",duration:0.6,ease:"expo.out",immediateRender:false}},{T(1, "knight") - .25});')
js(f'tl.fromTo("#s1b .tw i",{{backgroundColor:"#3A2E26"}},{{backgroundColor:"#FFD27A",stagger:{{each:0.012,from:"random"}},duration:0.05,immediateRender:false}},{T(1, "knight")});')
sfx('rumble', T(1, 'knight') - .25, .4)
js(f'tl.fromTo("#s1b .sign",{{scale:0,rotation:-10}},{{scale:1,rotation:-3,duration:0.35,ease:"back.out(3)",immediateRender:false}},{T(1, "capital")});')
TICK = ''.join(f'<span>{s} <b class="{"up" if u else "dn"}">{"▲" if u else "▼"} {v}</b></span>' for s, u, v in
               (('NYSE', 1, '0.8%'), ('KCG', 1, '1.2%'), ('IBM', 0, '0.3%'), ('GE', 1, '0.5%'), ('F', 0, '0.9%'), ('AAPL', 1, '1.1%')) * 2)
el('s1tk', f'<div class="tkin">{TICK}</div>', 'left:0;top:960px;width:1080px', cls='el ticker')
js(f'tl.fromTo("#s1tk",{{autoAlpha:0,y:40}},{{autoAlpha:1,y:0,duration:0.3,immediateRender:false}},{T(1, "stock") - .1});tl.fromTo("#s1tk .tkin",{{x:0}},{{x:-900,duration:5,ease:"none",immediateRender:false}},{T(1, "stock") - .1});')
el('s1bg', 'ONE OF THE BIGGEST', 'left:470px;top:780px', cls='el badge')
js(f'tl.fromTo("#s1bg",{{autoAlpha:0,scale:2.4,rotation:8}},{{autoAlpha:1,scale:1,rotation:8,duration:0.2,ease:"power4.in",immediateRender:false}},{T(1, "biggest")});')
sfx('stamp', T(1, 'biggest') + .15, .6)
gone('s1bg', T(1, 'updating') - .3, 'fade'); gone('s1c', T(1, 'updating') - .3, 'fade')
js(f'tl.to("#s1b",{{x:-230,scale:.78,duration:0.45,ease:"power3.inOut"}},{T(1, "updating") - .35});')
MON = '''<div class="mon"><div class="scr"><div class="ml">deploy_v2.sh</div><div class="code" id="s1code"></div>
<div class="bar"><i id="s1bar"></i></div><div class="pct" id="s1p">0%</div></div><div class="neck"></div><div class="foot"></div></div>'''
el('s1m', MON, 'left:470px;top:470px;width:560px;height:520px')
js(f'tl.fromTo("#s1m",{{autoAlpha:0,x:500,rotationY:-50,transformPerspective:1400}},{{autoAlpha:1,x:0,rotationY:-8,duration:0.5,ease:"back.out(1.4)",immediateRender:false}},{T(1, "updating") - .25});')
CODE_LINES = ['$ copy smars_v2 → srv1 ✓', '$ copy smars_v2 → srv2 ✓', '$ copy smars_v2 → srv3 ✓', '$ copy smars_v2 → srv4 ✓']
for k, ln in enumerate(CODE_LINES):
    js(f'tl.set("#s1code",{{innerHTML:{json.dumps("<br>".join(CODE_LINES[:k + 1]))}}},{T(1, "updating") + .15 + .28 * k:.3f});')
    sfx('type', T(1, 'updating') + .15 + .28 * k, .3)
js(f'tl.fromTo("#s1bar",{{scaleX:0}},{{scaleX:.62,duration:{be(1) - T(1, "updating") - .1:.2f},ease:"none",immediateRender:false}},{T(1, "updating")});')
count('s1p', T(1, 'updating'), be(1) - T(1, 'updating') - .1, 0, 62, 'pct')

# ---------------------------------------------------------------- page
CSS = f'''
@font-face{{font-family:'D';src:url('assets/fonts/InterDisplay-Black.otf');font-weight:900}}
@font-face{{font-family:'T';src:url('assets/fonts/Inter-SemiBold.otf');font-weight:600}}
@font-face{{font-family:'M';src:url('assets/fonts/JetBrainsMono-Bold.ttf');font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;overflow:hidden;background:{CREAM}}}
#root{{position:relative;width:100%;height:100%;overflow:hidden;background:radial-gradient(circle at 12% 8%,rgba(248,119,54,.22),transparent 38%),radial-gradient(circle at 92% 92%,rgba(248,119,54,.28),transparent 42%),{CREAM}}}
#root:before{{content:'';position:absolute;inset:0;background:radial-gradient(#E2CBB8 2.4px,transparent 2.6px) 0 0/34px 34px}}
.el{{position:absolute;opacity:0;visibility:hidden}}
.cap{{position:absolute;opacity:0;visibility:hidden;text-align:center;font:900 84px/1.15 'D';color:{INK};letter-spacing:-2px;z-index:40}}
.cap span{{display:inline-block;padding:0 14px 6px;border-radius:18px;margin:0 2px}}
.cap span.hl{{background:linear-gradient(90deg,{ACC},{ACC2});color:#fff;box-shadow:0 10px 0 #A8301A}}
.mxp{{position:absolute;inset:0;opacity:0;visibility:hidden;filter:drop-shadow(0 20px 18px rgba(74,50,28,.3))}}
.spd{{position:absolute;left:0;right:0;top:-280px;height:280px}} .spd i{{position:absolute;bottom:0;width:8px;border-radius:4px;background:{INK};opacity:.35}}
.dust{{position:absolute;left:50%;bottom:-10px}} .dust i{{position:absolute;width:120px;height:60px;margin-left:-60px;border-radius:50%;background:#E0CDBC;opacity:0}}
.term{{position:absolute;left:0;top:90px;width:720px;height:520px;border-radius:40px;background:linear-gradient(180deg,#2E241C,#1C1510);box-shadow:0 50px 90px rgba(42,32,24,.45),inset 0 2px 0 rgba(255,255,255,.08);padding:30px 40px}}
.tbar{{display:flex;align-items:center;gap:12px;font:700 26px 'M';color:#9C8676;letter-spacing:2px}} .tbar i{{width:16px;height:16px;border-radius:8px;background:#5A4A3E}} .tbar span{{margin-left:12px}}
.tnum{{font:900 120px 'D';color:#FF5A47;letter-spacing:-4px;margin-top:20px}}
.chart{{position:absolute;left:40px;bottom:30px}}
.siren{{position:absolute;left:290px;top:-60px;width:140px;height:150px;z-index:3;transform:scale(1.45);transform-origin:50% 100%}} .siren .cap{{position:absolute;left:14px;top:10px;width:72px;height:70px;border-radius:36px 36px 8px 8px;background:#B04A3A}}
.siren .base{{position:absolute;left:0;top:76px;width:100px;height:26px;border-radius:8px;background:#3A2E26}} .siren .glow{{position:absolute;left:-90px;top:-80px;width:280px;height:240px;border-radius:50%;background:radial-gradient(circle,rgba(255,70,50,.75),transparent 65%);opacity:0;visibility:hidden}}
.imp i{{position:absolute;left:-5px;top:-230px;width:10px;height:70px;border-radius:5px;background:{ACC2};transform-origin:5px 230px}}
.xs{{position:absolute;left:10px;top:20px}}
.step{{position:absolute;width:230px;border-radius:18px 18px 0 0;background:linear-gradient(180deg,#FFFAF7,#EFE2D6);border:4px solid #E0CDBC;box-shadow:0 30px 50px rgba(74,50,28,.25);padding:22px 16px;text-align:center}}
.step b{{font:900 34px/1.1 'D';color:{INK}}} .step em{{display:block;margin:16px auto 0;width:64px;height:64px;border-radius:32px;background:{GREEN};color:#fff;font:900 40px/64px 'D';font-style:normal}}
.gap{{position:absolute;width:230px;border:6px dashed {ACC2};border-bottom:none;border-radius:18px 18px 0 0;text-align:center;padding-top:26px;background:rgba(232,64,46,.06)}} .gap b{{font:900 34px/1.15 'D';color:{ACC2}}}
.beam{{position:absolute;left:470px;top:-320px;width:330px;height:1080px;background:linear-gradient(180deg,rgba(255,250,235,.95),rgba(255,240,210,.0));clip-path:polygon(38% 0,62% 0,100% 100%,0 100%);opacity:0;visibility:hidden;mix-blend-mode:screen}}
.ball{{position:absolute;left:0;top:0;width:90px;height:90px;border-radius:20px;background:linear-gradient(135deg,{ACC},{ACC2});box-shadow:0 14px 30px rgba(217,56,30,.4);opacity:0;visibility:hidden}}
.ball:after{{content:'v2';position:absolute;inset:0;font:900 38px/90px 'D';color:#fff;text-align:center}}
.pin{{position:absolute;left:220px;top:-26px;width:40px;height:40px;border-radius:20px;background:{ACC2};box-shadow:0 6px 10px rgba(0,0,0,.25);z-index:5}}
.calb,.calp{{position:absolute;inset:0;border-radius:36px;background:#fff;overflow:hidden;box-shadow:0 40px 80px rgba(74,50,28,.3);text-align:center}}
.ch{{background:linear-gradient(90deg,{ACC},{ACC2});color:#fff;font:900 64px 'D';padding:24px 0;letter-spacing:4px}} .cn{{font:900 280px/1.02 'D';color:{INK}}} .cy{{font:700 60px 'M';color:{INK};display:inline-block}}
.tower{{position:absolute;inset:0;border-radius:24px 24px 0 0;background:linear-gradient(90deg,#4A3B30,#2A2018 55%,#3A2E26);box-shadow:0 40px 80px rgba(42,32,24,.4)}}
.tw i{{position:absolute;width:44px;height:40px;border-radius:6px;background:#3A2E26}}
.sign{{position:absolute;left:-40px;top:20px;width:500px;padding:14px 0;border-radius:16px;background:#fff;text-align:center;font:900 54px 'D';color:{INK};box-shadow:0 14px 30px rgba(0,0,0,.3);transform:rotate(-3deg)}}
.ticker{{height:90px;background:{INK};overflow:hidden;white-space:nowrap}} .tkin{{display:inline-block;padding:20px 0;font:700 40px 'M';color:#F4EDE3}} .tkin span{{margin:0 30px}} .up{{color:#4ADE80}} .dn{{color:#FF6B57}}
.badge{{padding:14px 30px;border-radius:18px;background:linear-gradient(90deg,{ACC},{ACC2});color:#fff;font:900 44px 'D';box-shadow:0 12px 0 #A8301A;white-space:nowrap}}
.mon .scr{{width:560px;height:380px;border-radius:26px;background:#1C1510;border:14px solid #3A2E26;padding:24px 26px;box-shadow:0 40px 80px rgba(42,32,24,.4)}}
.mon .neck{{width:90px;height:60px;margin:0 auto;background:#3A2E26}} .mon .foot{{width:260px;height:24px;margin:0 auto;border-radius:12px;background:#3A2E26}}
.ml{{font:700 24px 'M';color:#9C8676;letter-spacing:2px}} .code{{font:700 26px/1.55 'M';color:#7CE0A3;margin-top:12px;height:170px}}
.bar{{height:26px;border-radius:13px;background:#3A2E26;overflow:hidden;margin-top:8px}} .bar i{{display:block;height:100%;background:linear-gradient(90deg,{ACC},{ACC2});transform-origin:0 50%}}
.pct{{font:900 40px 'D';color:#fff;text-align:right;margin-top:6px}}
'''
FMT = '''function F_neg(v){return (v<0?"-":"")+"$"+Math.abs(Math.round(v)).toLocaleString("en-US")}
function F_pct(v){return Math.round(v)+"%"}'''
SFXD = {f.stem: round(wave.open(str(f)).getnframes() / 44100, 3) for f in (Path('hf/ast01-short/assets/sfx')).glob('*.wav')}
aud = [f'<audio id="vo" class="clip" src="assets/vo.wav" data-start="0" data-duration="{DUR}" data-track-index="3" data-volume="1"></audio>',
       f'<audio id="bgm" class="clip" src="assets/bgm.wav" data-start="0" data-duration="{DUR}" data-track-index="4" data-volume="0.16"></audio>']
aud += [f'<audio id="fx{k}" class="clip" src="assets/sfx/{n}.wav" data-start="{t}" data-duration="{SFXD[n]}" data-track-index="{5 + k % 3}" data-volume="{v}"></audio>'
        for k, (n, t, v) in enumerate(sorted(SFX, key=lambda s: s[1]))]
html = f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="assets/gsap.min.js"></script><script src="assets/host.js"></script><style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920" data-fps="30">
{chr(10).join(H)}
{chr(10).join(aud)}
</div><script>{FMT}
{chr(10).join(mxjs)}
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(J)}
tl.set({{}},{{}},{DUR});
window.__timelines["main"] = tl;
</script></body></html>'''
src = Path('hf/knight01-short')
(OUT / 'assets' / 'fonts').mkdir(parents=True, exist_ok=True)
for f in ('gsap.min.js', 'host.js', 'vo.wav', 'bgm.wav'):
    shutil.copy(src / 'assets' / f, OUT / 'assets' / f)
shutil.copy(Path('hf/host/host.js'), OUT / 'assets' / 'host.js')
if not (OUT / 'assets' / 'sfx').exists():
    shutil.copytree(src / 'assets' / 'sfx', OUT / 'assets' / 'sfx')
for f in ('InterDisplay-Black.otf', 'Inter-SemiBold.otf', 'JetBrainsMono-Bold.ttf'):
    shutil.copy(Path('hf/ast01-short/assets/fonts') / f, OUT / 'assets' / 'fonts' / f)
for f in ('hyperframes.json',):
    shutil.copy(src / f, OUT / f)
(OUT / 'meta.json').write_text(json.dumps({'id': 'knight01-v2', 'name': 'knight01-v2'}))
(OUT / 'index.html').write_text(html)
print(f'wrote {OUT}/index.html dur {DUR}s elements {len(H)} tweens {len(J)} sfx {len(SFX)}')
