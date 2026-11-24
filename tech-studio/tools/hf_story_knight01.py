"""knight01: first STORYTELLING Short in the context-driven motion style (refs/MOTION_STYLE.md).
Captions at the TOP built word by word (next word ghosted, accent words in italic serif), mono section label top-left,
live LOSS counter top-right, Max bottom-centre talking + a new reaction every line, one element per phrase landing on
its word, halftone-dot wipes between acts. Our colours only. Usage: python3 tools/hf_story_knight01.py"""
import json, re, shutil, sys
from pathlib import Path
sys.path.insert(0, 'tools')
from kit_assets import icon

ROOT = Path('.')
TID = 'knight01-short'
OUT = ROOT / 'hf' / TID
tl = json.load(open(f'src/episodes/{TID}.timeline.json'))
B = tl['beats']
DUR = round(tl['duration'] + 0.1, 3)
INK, ACC, ACC2, CREAM, CARD, DARK, GREEN, RED = '#2A2018', '#F87736', '#E8402E', '#F4EDE3', '#FFFAF7', '#2A2018', '#16A34A', '#E8402E'


def norm(w):
    return re.sub(r"[^a-z0-9]", '', w.lower())


def T(bi, word, nth=0, end=False):
    hits = [w for w in B[bi]['words'] if norm(w['w']).startswith(norm(word))]
    w = hits[nth]
    return round(B[bi]['start'] + (w['e'] if end else w['s']), 3)


def bs(bi):
    return B[bi]['start']


def be(bi):
    return round(B[bi]['start'] + B[bi]['dur'], 3)


H, J, SFX = [], [], []   # html elements, gsap js lines, sfx (name, t, vol)


def el(i, html, style, cls='el'):
    H.append(f'<div id="{i}" class="{cls}" style="{style}">{html}</div>')


def js(s):
    J.append(s)


def sfx(name, t, vol=0.5):
    SFX.append((name, round(t, 3), vol))


def pop(i, t, s=0.6, d=0.38, ease='back.out(2.2)'):
    js(f'tl.fromTo("#{i}",{{autoAlpha:0,scale:{s}}},{{autoAlpha:1,scale:1,duration:{d},ease:"{ease}",immediateRender:false}},{t});')


def slide(i, t, x=0, y=60, d=0.45):
    js(f'tl.fromTo("#{i}",{{autoAlpha:0,x:{x},y:{y}}},{{autoAlpha:1,x:0,y:0,duration:{d},ease:"expo.out",immediateRender:false}},{t});')


def tilt(i, t, d=0.55):
    js(f'tl.fromTo("#{i}",{{autoAlpha:0,rotationY:-70,rotationX:12,x:160,transformPerspective:1400}},{{autoAlpha:1,rotationY:0,rotationX:0,x:0,duration:{d},ease:"back.out(1.4)",immediateRender:false}},{t});')


def slam(i, t, rot=0, s=2.6, vol=0.7, snd='stamp'):
    js(f'tl.fromTo("#{i}",{{autoAlpha:0,scale:{s},rotation:{rot}}},{{autoAlpha:1,scale:1,rotation:{rot},duration:0.2,ease:"power4.in",immediateRender:false}},{t});')
    js(f'tl.fromTo("#{i}",{{x:-6}},{{x:0,duration:0.25,ease:"elastic.out(3,0.3)",immediateRender:false}},{t + 0.2});')
    if snd:
        sfx(snd, t + 0.16, vol)


def out(i, t, kind='fade', d=0.25):
    v = {'fade': 'autoAlpha:0', 'shrink': 'autoAlpha:0,scale:0.6', 'up': 'autoAlpha:0,y:-80', 'drop': 'autoAlpha:0,y:260,rotation:14'}[kind]
    js(f'tl.to("#{i}",{{{v},duration:{d},ease:"power2.in"}},{t});')


def to(i, t, props, d=0.4, ease='power3.out'):
    js(f'tl.to("#{i}",{{{props},duration:{d},ease:"{ease}"}},{t});')


def count(i, t, d, a, b, fmt='n', ease='power2.out'):
    """number tween written into #i; fmt n=1,234 | m=$460,000,000 | neg=-$460,000,000 | mmss | int"""
    js(f'(function(){{const o={{v:{a}}};tl.to(o,{{v:{b},duration:{d},ease:"{ease}",onUpdate:()=>{{document.getElementById("{i}").textContent=F_{fmt}(o.v)}}}},{t});}})();')


def settext(i, t, text):
    js(f'tl.set("#{i}",{{textContent:{json.dumps(text)}}},{t});')


_b = 0


def burst(x, y, t, color=ACC2, r=120):
    global _b
    _b += 1
    i = f'bu{_b}'
    lines = ''.join(f'<i style="position:absolute;left:-4px;top:-{r}px;width:8px;height:{int(r * .38)}px;border-radius:4px;background:{color};transform-origin:4px {r}px;transform:rotate({a}deg)"></i>' for a in range(0, 360, 45))
    el(i, lines, f'left:{x}px;top:{y}px;width:0;height:0;z-index:30')
    js(f'tl.fromTo("#{i}",{{autoAlpha:1,scale:0.4}},{{scale:1.35,autoAlpha:0,duration:0.5,ease:"expo.out",immediateRender:false}},{t});')


def ring(x, y, t, t_out, size=170):
    global _b
    _b += 1
    i = f'rg{_b}'
    el(i, '', f'left:{x - size // 2}px;top:{y - size // 2}px;width:{size}px;height:{size}px;border-radius:50%;border:6px solid {ACC2};z-index:28')
    js(f'tl.fromTo("#{i}",{{autoAlpha:0,scale:1.8}},{{autoAlpha:1,scale:1,duration:0.3,ease:"back.out(2)",immediateRender:false}},{t});')
    out(i, t_out)


def card(inner, extra=''):
    return f'<div class="card" style="{extra}">{inner}</div>'


# ---------------------------------------------------------------- captions (top), section label, live counter
ACCENT = [{'lost', 'hacker', 'missed', 'step'}, {'knight', 'capital', 'updating'}, {'seven'}, {'eighth', 'power', 'peg'},
          {'reuses', 'switch'}, {'97', 'nobody'}, {'opens', 'wakes'}, {'nonstop', 'million'}, {'gone'}, {'rescue', 'rival'},
          {'delete', 'alone'}, {'techdecoded', 'decoded'}]
caps = []
ci = 0
for bi, b in enumerate(B):
    ws = b['words']
    chunks, cur = [], []
    for w in ws:
        cur.append(w)
        if re.search(r'[.,:?!]$', w['w']) and len(cur) >= 2 or len(cur) >= 6:
            chunks.append(cur); cur = []
    if cur:
        if chunks and len(cur) == 1:
            chunks[-1] += cur
        else:
            chunks.append(cur)
    for k, ch in enumerate(chunks):
        t0 = round(b['start'] + ch[0]['s'] - 0.06, 3)
        t1 = round(b['start'] + chunks[k + 1][0]['s'] - 0.08, 3) if k + 1 < len(chunks) else (round(B[bi + 1]['start'] - 0.05, 3) if bi + 1 < len(B) else DUR)
        spans = []
        for j, w in enumerate(ch):
            a = 'acc' if norm(w['w']) in ACCENT[bi] else ''
            spans.append(f'<span id="w{ci}_{j}" class="wd {a}">{w["w"]}</span>')
            ws_t = round(b['start'] + w['s'], 3)
            js(f'tl.fromTo("#w{ci}_{j}",{{opacity:0,y:10}},{{opacity:0.22,y:6,duration:0.12,immediateRender:false}},{max(t0, ws_t - 0.28)});')
            js(f'tl.to("#w{ci}_{j}",{{opacity:1,y:0,duration:0.16,ease:"power2.out"}},{ws_t});')
        el(f'cap{ci}', ' '.join(spans), 'left:64px;right:64px;top:118px', cls='cap')
        js(f'tl.set("#cap{ci}",{{autoAlpha:1}},{t0});tl.set("#cap{ci}",{{autoAlpha:0}},{t1});')
        ci += 1

SECT = [(0, '// 00 · the hook'), (1, '// 01 · the update'), (3, '// 02 · the old switch'), (5, '// 03 · 8:01 am'),
        (6, '// 04 · market open'), (8, '// 05 · the damage'), (10, '// 06 · the lesson')]
for k, (bi, txt) in enumerate(SECT):
    t0 = bs(bi) - 0.05
    t1 = bs(SECT[k + 1][0]) - 0.1 if k + 1 < len(SECT) else DUR
    el(f'sec{k}', txt, 'left:64px;top:52px', cls='mono')
    js(f'tl.fromTo("#sec{k}",{{autoAlpha:0,x:-20}},{{autoAlpha:1,x:0,duration:0.3,immediateRender:false}},{max(0, t0)});tl.set("#sec{k}",{{autoAlpha:0}},{t1});')
el('loss', 'LOSS <b id="lossv">$0</b>', 'right:64px;top:52px;text-align:right', cls='mono')
js('tl.set("#loss",{autoAlpha:1},0);')
count('lossv', bs(7), T(8, 'gone') - bs(7), 0, 460000000, 'm', 'power1.in')

# ---------------------------------------------------------------- Max (bottom-centre, talking, new reaction per line)
POSE = ["brows:'high',eyes:'wide',arms:'hands-up',extra:['bang']", "brows:'up',eyes:'open',arms:'point'",
        "brows:'focused',eyes:'squint',arms:'chin'", "brows:'skeptic',eyes:'open',arms:'shrug',extra:['question']",
        "brows:'worried',eyes:'wide',arms:'hush'", "brows:'angry',eyes:'open',arms:'phone',look:[0,1]",
        "brows:'high',eyes:'wide',arms:'point',look:[1,-1]", "brows:'worried',eyes:'wide',arms:'hands-up',extra:['sweat']",
        "brows:'worried',eyes:'closed',arms:'facepalm'", "brows:'worried',eyes:'worried',arms:'shrug'",
        "brows:'up',eyes:'open',arms:'thumbs'", "brows:'up',eyes:'happy',arms:'point',extra:['spark']"]
BASE = ['shock', 'smile', 'flat', 'flat', 'flat', 'frown', 'O', 'shock', 'frown', 'frown', 'smile', 'grin']
MAXC = "{skin:'#F0C4A0',hair:'messy',hairCol:'#5A3A26',glasses:'round',hood:'down',top:'#F87736',topS:'#D85E25',phones:'none',beard:'stubble'}"
mx_html = ''.join(f'<div id="mx{k}" class="mxl" data-m="b">' + ''.join(f'<div class="v v{m}"></div>' for m in ('b', 'A', 'E', 'O', 'M')) + '</div>' for k in range(len(B)))
H.append(f'<div id="maxwrap" style="position:absolute;left:250px;top:1240px;width:580px;height:760px;z-index:20"><div id="maxbreath" style="position:absolute;inset:0">{mx_html}</div></div>')
mx_js = ['const MAXC=' + MAXC + ';', 'const POSE=[' + ','.join('{' + p + '}' for p in POSE) + '];', 'const BASE=' + json.dumps(BASE) + ';',
         'POSE.forEach((p,k)=>{const d=document.getElementById("mx"+k);["b","A","E","O","M"].forEach(m=>{d.querySelector(".v"+m).innerHTML=HOST.render(Object.assign({char:MAXC,w:580,h:754},p,{mouth:m==="b"?BASE[k]:m}));});});']
for k, b in enumerate(B):
    t0 = b['start'] - 0.25 if k else 0
    t1 = B[k + 1]['start'] - 0.25 if k + 1 < len(B) else DUR
    js(f'tl.set("#mx{k}",{{autoAlpha:1}},{max(0, t0)});tl.set("#mx{k}",{{autoAlpha:0}},{t1});')
    vis = ['A', 'E', 'O']
    for j, w in enumerate(b['words']):
        s, e = b['start'] + w['s'], b['start'] + w['e']
        js(f'tl.set("#mx{k}",{{attr:{{"data-m":"{vis[j % 3]}"}}}},{s:.3f});')
        if e - s > 0.34:
            js(f'tl.set("#mx{k}",{{attr:{{"data-m":"M"}}}},{s + (e - s) * .45:.3f});tl.set("#mx{k}",{{attr:{{"data-m":"{vis[(j + 1) % 3]}"}}}},{s + (e - s) * .6:.3f});')
        js(f'tl.set("#mx{k}",{{attr:{{"data-m":"M"}}}},{e - 0.03:.3f});')
    js(f'tl.set("#mx{k}",{{attr:{{"data-m":"b"}}}},{b["start"] + b["words"][-1]["e"] + 0.08:.3f});')
    if k:
        js(f'tl.fromTo("#maxwrap",{{y:26,scale:0.97}},{{y:0,scale:1,duration:0.35,ease:"back.out(2.4)",immediateRender:false}},{b["start"] - 0.25:.3f});')
js(f'tl.to("#maxbreath",{{y:-8,duration:1.6,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / 1.6)}}},0);')
js('tl.fromTo("#maxwrap",{y:400},{y:0,duration:0.55,ease:"back.out(1.6)",immediateRender:false},0);')

# ---------------------------------------------------------------- halftone-dot wipe between acts
COLS, ROWS, CELL = 20, 36, 54
dots = ''.join(f'<i style="left:{c * CELL}px;top:{r * CELL}px"></i>' for r in range(ROWS) for c in range(COLS))
H.append(f'<div id="ht">{dots}</div>')


def wipe(t_mid):
    js(f'tl.fromTo("#ht i",{{scale:0}},{{scale:1.5,duration:0.22,ease:"power2.in",stagger:{{grid:[{ROWS},{COLS}],from:"start",amount:0.26}},immediateRender:false}},{t_mid - 0.5:.3f});')
    js(f'tl.to("#ht i",{{scale:0,duration:0.22,ease:"power2.out",stagger:{{grid:[{ROWS},{COLS}],from:"end",amount:0.26}}}},{t_mid + 0.02:.3f});')
    sfx('whoosh', t_mid - 0.45, 0.45)


# ================================================================= LINE 0  hook
watch = f'''<div class="watch"><i class="btn"></i><div class="dial"><b>45</b><span>MINUTES</span></div></div>'''
el('l0watch', watch, 'left:90px;top:420px;width:340px;height:380px')
pop('l0watch', T(0, '45'), .4); sfx('tick', T(0, '45'), .6)
el('l0pnl', card('<div class="lbl">P&amp;L · AUG 1</div><div class="big neg" id="l0n">$0</div><div class="sub">one trading firm</div>', f'background:{DARK};border-color:#3E2F24;width:560px'), 'left:450px;top:470px')
tilt('l0pnl', T(0, 'company') - .1)
count('l0n', T(0, 'lost'), T(0, 'dollars') - T(0, 'lost'), 0, -460000000, 'neg', 'power2.in')
settext('l0n', T(0, 'dollars') + .02, '-$460M')
js(f'tl.fromTo("#l0n",{{scale:1.5}},{{scale:1,duration:0.4,ease:"back.out(3)",immediateRender:false}},{T(0, "dollars") + .02});')
burst(730, 610, T(0, 'dollars')); sfx('impact', T(0, 'dollars'), .6)
out('l0watch', T(0, 'no') - .15, 'shrink'); out('l0pnl', T(0, 'no') - .15, 'shrink')
el('l0hack', f'<div class="disc">{icon("mdi:incognito", 230, INK)}</div>', 'left:370px;top:440px')
pop('l0hack', T(0, 'no') - .05)
el('l0x', '<i class="x1"></i><i class="x2"></i>', 'left:360px;top:430px;width:360px;height:360px;z-index:12')
js(f'tl.fromTo("#l0x i",{{scaleX:0}},{{scaleX:1,duration:0.18,stagger:0.1,ease:"power3.out",immediateRender:false}},{T(0, "hacker")});tl.set("#l0x",{{autoAlpha:1}},{T(0, "hacker")});')
el('l0st', 'NO HACKER', 'left:300px;top:840px', cls='el stamp')
slam('l0st', T(0, 'hacker') + .15, -8)
for i in ('l0hack', 'l0x', 'l0st'):
    out(i, T(0, 'just') - .12, 'up')
chk = ''.join(f'<div class="row{" miss" if k == 2 else ""}"><span class="box">{"" if k == 2 else icon("mdi:check-bold", 44, "#fff")}</span>{txt}</div>'
              for k, txt in enumerate(['Write the new code', 'Test it', 'Copy it to every server']))
el('l0chk', card('<div class="lbl">DEPLOY CHECKLIST</div>' + chk, 'width:800px'), 'left:140px;top:430px')
slide('l0chk', T(0, 'just') - .05)
js(f'tl.fromTo("#l0chk .row",{{autoAlpha:0,x:-40}},{{autoAlpha:1,x:0,stagger:0.18,duration:0.3,immediateRender:false}},{T(0, "just")});')
ring(220, 775, T(0, 'missed'), be(0) - .05, 120); sfx('error', T(0, 'missed'), .4)
out('l0chk', be(0) - .1)

# ================================================================= LINE 1  Aug 1 2012, Knight Capital updating
cal = '<div class="cal"><div class="ct">AUGUST</div><div class="cd" id="l1d">1</div><div class="cy" id="l1y">2012</div></div>'
el('l1cal', cal, 'left:300px;top:420px;width:480px;height:470px')
pop('l1cal', T(1, 'august') - .1, .7)
for k, d in enumerate(['31', '30', '29']):
    el(f'l1p{k}', f'<div class="cal page"><div class="ct">JULY</div><div class="cd">{d}</div><div class="cy">2012</div></div>', 'left:300px;top:420px;width:480px;height:470px;z-index:8')
    js(f'tl.set("#l1p{2 - k}",{{autoAlpha:1}},{T(1, "august") - .1});')
    js(f'tl.to("#l1p{2 - k}",{{y:-500,x:{220 - 160 * k},rotation:{-30 + 25 * k},autoAlpha:0,duration:0.42,ease:"power2.in"}},{T(1, "august") + .1 + .14 * k});')
    sfx('flip', T(1, 'august') + .1 + .14 * k, .5)
js(f'tl.fromTo("#l1y",{{scale:1.6,color:"{ACC2}"}},{{scale:1,color:"{INK}",duration:0.4,immediateRender:false}},{T(1, "2012")});')
to('l1cal', T(1, 'knight') - .2, 'scale:0.42,x:-330,y:-190', .45)
el('l1co', card(f'<div class="hd">{icon("mdi:office-building", 96, INK)}<div><div class="ttl">KNIGHT CAPITAL</div><div class="sub">US stock trading firm</div></div></div>'
                f'<div class="badge" id="l1bg">ONE OF THE BIGGEST</div><div class="pb"><i id="l1bar"></i></div><div class="sub" id="l1up">Deploying update…</div>', 'width:760px'),
   'left:160px;top:560px')
tilt('l1co', T(1, 'knight') - .15); sfx('whoosh', T(1, 'knight') - .15, .4)
pop('l1bg', T(1, 'biggest'), .5); sfx('pop', T(1, 'biggest'), .45)
js(f'tl.set("#l1bar",{{scaleX:0}},0);tl.to("#l1bar",{{scaleX:1,duration:{be(1) - T(1, "updating") - .2:.2f},ease:"none"}},{T(1, "updating")});')
sfx('scan', T(1, 'updating'), .35)
out('l1co', be(1) - .12, 'up'); out('l1cal', be(1) - .12)

# ================================================================= LINE 2  eight servers, code reaches seven
racks = ''
for k in range(8):
    x, y = 70 + (k % 4) * 240, 470 + (k // 4) * 330
    racks += f'<div id="rk{k}" class="rack" style="left:{x}px;top:{y}px"><i></i><i></i><i></i><b>#{k + 1}</b><span class="ok">{icon("mdi:check-bold", 40, "#fff")}</span></div>'
el('l2', racks, 'left:0;top:0;width:1080px;height:1300px')
js(f'tl.set("#l2",{{autoAlpha:1}},{bs(2)});')
js(f'tl.fromTo("#l2 .rack",{{autoAlpha:0,y:50}},{{autoAlpha:1,y:0,stagger:0.06,duration:0.3,ease:"back.out(2)",immediateRender:false}},{T(2, "eight") - .05});')
el('l2pk', '<span class="chip">NEW CODE v2</span>', 'left:390px;top:390px')
pop('l2pk', T(2, 'code')); sfx('pop', T(2, 'code'), .4)
for k in range(7):
    t = T(2, 'reaches') + .1 * k
    js(f'tl.fromTo("#rk{k} .ok",{{autoAlpha:0,scale:0}},{{autoAlpha:1,scale:1,duration:0.2,ease:"back.out(3)",immediateRender:false}},{t:.3f});tl.to("#rk{k}",{{borderColor:"{GREEN}",duration:0.1}},{t:.3f});')
    sfx('tick', t, .35)
js(f'tl.to("#rk7",{{borderColor:"{ACC2}",borderStyle:"dashed",backgroundColor:"#EFE6DD",duration:0.2}},{T(2, "only")});')
ring(70 + 3 * 240 + 95, 470 + 330 + 110, T(2, 'only'), be(2) - .05, 280); sfx('error', T(2, 'only'), .4)
el('l2n', '7 / 8', 'left:690px;top:1150px', cls='el stamp')
slam('l2n', T(2, 'seven'), -6)
out('l2', be(2) - .1); out('l2pk', be(2) - .1); out('l2n', be(2) - .1)

# ================================================================= LINE 3  the eighth server: Power Peg, off since 2003
el('l3rk', f'<div class="rack big" style="position:relative"><i></i><i></i><i></i><b>#8</b></div>', 'left:90px;top:520px')
pop('l3rk', bs(3), .5)
el('l3f', f'<div class="folder">{icon("mdi:folder", 300, "#C9A887")}<div class="fl">old_feature/</div><div class="dust"></div></div>', 'left:470px;top:470px')
slide('l3f', T(3, 'old'), 120, 0)
el('l3off', '<span class="tog off"><i></i></span> OFF', 'left:520px;top:880px', cls='el pilltxt')
pop('l3off', T(3, 'switched')); sfx('switch', T(3, 'switched'), .5)
el('l3yr', 'since 2003', 'left:640px;top:405px', cls='el serif')
slam('l3yr', T(3, '2003'), -5, snd='pop')
el('l3pp', 'POWER PEG', 'left:110px;top:1010px', cls='el slab')
slam('l3pp', T(3, 'power') - .05, -3, vol=.8, snd='impact')
burst(540, 1080, T(3, 'power'))
js(f'tl.set("#l3f .fl",{{textContent:"power_peg/"}},{T(3, "power")});')
out('l3rk', be(3) - .1); out('l3off', be(3) - .1); out('l3yr', be(3) - .1); out('l3pp', be(3) - .1)
# folder stays into line 4
# ================================================================= LINE 4  new code reuses its old switch
el('l4code', card('<div class="lbl">new_code.py</div><pre class="code">if order.<b>flag</b> == 1:\n    route(order)</pre>', 'width:520px;padding:26px'), 'left:60px;top:470px')
slide('l4code', bs(4), -120, 0)
to('l3f', bs(4) - .1, 'x:200,scale:0.82', .45)
el('l4sw', '<span class="tog" id="l4tg"><i></i></span><span class="swl">FLAG</span>', 'left:180px;top:830px', cls='el pilltxt')
pop('l4sw', T(4, 'reuses') - .3)
js(f'tl.to("#l4tg",{{backgroundColor:"{ACC2}",duration:0.15}},{T(4, "reuses")});tl.to("#l4tg i",{{x:76,duration:0.2,ease:"back.out(3)"}},{T(4, "reuses")});')
sfx('switch', T(4, 'reuses'), .6)
el('l4wire', '', 'left:500px;top:868px;width:270px;height:10px;border-radius:5px;background:linear-gradient(90deg,#F87736,#E8402E);transform-origin:0 50%;transform:rotate(-40deg)')
js(f'tl.fromTo("#l4wire",{{autoAlpha:1,scaleX:0}},{{scaleX:1,duration:0.35,ease:"power2.out",immediateRender:false}},{T(4, "old")});')
js(f'tl.to("#l3f",{{filter:"drop-shadow(0 0 40px rgba(232,64,46,.85))",duration:0.4}},{T(4, "switch")});')
burst(640, 620, T(4, 'switch')); sfx('hum', T(4, 'switch'), .45)
for i in ('l4code', 'l4sw', 'l4wire', 'l3f'):
    out(i, be(4) - .55, 'fade', .2)
wipe(be(4) - .02)

# ================================================================= LINE 5  8:01 AM, 97 warning emails, nobody acts
el('l5clk', '8:01 <small>AM</small>', 'left:300px;top:380px', cls='el clock')
pop('l5clk', T(5, '8'), .6); sfx('tick', T(5, '8'), .6)
rows = ''.join(f'<div class="mrow"><i></i><b>SMARS alert</b><span>Power Peg disabled</span><em>8:01</em></div>' for _ in range(6))
el('l5in', card(f'<div class="hd">{icon("mdi:email", 70, INK)}<div class="ttl">Inbox</div><span class="cnt" id="l5c">0</span></div>' + rows, 'width:820px'), 'left:130px;top:560px')
tilt('l5in', T(5, 'system') - .1)
js(f'tl.fromTo("#l5in .mrow",{{autoAlpha:0,y:-30}},{{autoAlpha:1,y:0,stagger:0.16,duration:0.25,immediateRender:false}},{T(5, "sends")});')
for k in range(4):
    sfx('notify', T(5, 'sends') + .3 * k, .35)
count('l5c', T(5, '97'), .9, 0, 97, 'int')
js(f'tl.fromTo("#l5c",{{scale:1.8}},{{scale:1,duration:0.35,ease:"back.out(3)",immediateRender:false}},{T(5, "97") + .9});')
el('l5st', 'IGNORED', 'left:330px;top:900px', cls='el stamp')
slam('l5st', T(5, 'nobody'), -9, .8)
for i in ('l5clk', 'l5in', 'l5st'):
    out(i, be(5) - .5, 'fade', .2)
wipe(be(5) - .02)

# ================================================================= LINE 6  9:30 market opens, Power Peg wakes up
el('l6rays', '', 'left:40px;top:300px;width:1000px;height:1000px', cls='el rays')
el('l6clk', f'{icon("mdi:bell-ring", 120, INK)}<span>9:30</span>', 'left:300px;top:420px', cls='el clock big')
pop('l6clk', bs(6) - .05, .5); sfx('ding', bs(6), .55)
el('l6open', '<i></i>MARKET OPEN', 'left:250px;top:700px', cls='el open')
slam('l6open', T(6, 'market'), -4, snd='impact')
js(f'tl.fromTo("#l6rays",{{autoAlpha:0,rotation:0,scale:.6}},{{autoAlpha:.55,scale:1,duration:0.5,immediateRender:false}},{T(6, "market")});tl.to("#l6rays",{{rotation:40,duration:4,ease:"none"}},{T(6, "market")});')
out('l6clk', T(6, 'power') - .2, 'up'); out('l6open', T(6, 'power') - .2, 'up')
el('l6f', f'<div class="folder">{icon("mdi:folder", 330, "#C9A887")}<div class="fl">power_peg/</div></div><span class="active">ACTIVE</span>', 'left:350px;top:520px')
pop('l6f', T(6, 'power') - .1, .4)
js(f'tl.to("#l6f",{{filter:"drop-shadow(0 0 50px rgba(232,64,46,.9))",duration:0.3}},{T(6, "wakes")});tl.fromTo("#l6f",{{x:-8}},{{x:8,duration:0.06,repeat:9,yoyo:true,immediateRender:false}},{T(6, "wakes")});')
sfx('glitch', T(6, 'wakes'), .5)
js(f'tl.to("#l6rays",{{backgroundImage:"repeating-conic-gradient(rgba(232,64,46,.28) 0 8deg, transparent 8deg 22deg)",duration:0.2}},{T(6, "wakes")});')
out('l6rays', be(6) - .1); out('l6f', be(6) - .1, 'shrink')

# ================================================================= LINE 7  orders nonstop, 4 million trades, 154 stocks
el('l7rk', '<div class="rack big glow" style="position:relative"><i></i><i></i><i></i><b>#8</b></div>', 'left:50px;top:620px')
pop('l7rk', bs(7) - .05, .5)
chips = ''
for k in range(16):
    buy = k % 2 == 0
    chips += f'<span id="oc{k}" class="oc {"buy" if buy else "sell"}">{"BUY" if buy else "SELL"} 100</span>'
el('l7oc', chips, 'left:0;top:0;width:1080px;height:1300px')
js(f'tl.set("#l7oc",{{autoAlpha:1}},{T(7, "orders")});')
for k in range(16):
    for rep in range(3):
        t = T(7, 'orders') + .1 * k + 1.6 * rep
        if t > be(7) - .3:
            continue
        y0 = 720 + (k % 5) * 40
        js(f'tl.fromTo("#oc{k}",{{x:260,y:{y0},autoAlpha:1,scale:.6}},{{x:{1100 + (k % 3) * 40},y:{y0 - 200 + (k % 7) * 60},scale:1,autoAlpha:1,duration:0.9,ease:"power1.in",immediateRender:false}},{t:.3f});')
sfx('keys', T(7, 'orders'), .35); sfx('riser', T(7, 'fly'), .35)
el('l7tr', card('<div class="lbl">TRADES</div><div class="big" id="l7n">0</div>', 'width:520px;padding:24px 34px'), 'left:480px;top:380px')
pop('l7tr', T(7, 'four') - .25)
count('l7n', T(7, 'four'), T(7, 'trades') - T(7, 'four'), 0, 4000000, 'n', 'power2.in')
burst(740, 520, T(7, 'trades')); sfx('impact', T(7, 'trades'), .5)
grid = ''.join('<i></i>' for _ in range(154))
el('l7g', f'<div class="lbl" style="margin-bottom:12px">154 STOCKS</div><div class="g154">{grid}</div>', 'left:470px;top:640px;width:560px')
js(f'tl.set("#l7g",{{autoAlpha:1}},{T(7, "154") - .1});tl.fromTo("#l7g .g154 i",{{backgroundColor:"#E6D9CE"}},{{backgroundColor:"{ACC2}",stagger:{{each:0.006,from:"random"}},duration:0.1,immediateRender:false}},{T(7, "154")});')
for i in ('l7rk', 'l7oc', 'l7tr', 'l7g'):
    out(i, be(7) - .12)

# ================================================================= LINE 8  45 minutes later... over $460M gone
el('l8w', '<div class="watch big"><i class="btn"></i><div class="dial"><b id="l8t">00:00</b><span>MIN : SEC</span></div></div>', 'left:300px;top:390px;width:480px;height:520px')
pop('l8w', bs(8) - .05, .5)
count('l8t', T(8, '45'), T(8, 'stop') - T(8, '45'), 0, 2700, 'mmss', 'power1.in')
for k in range(8):
    sfx('tick', T(8, '45') + k * (T(8, 'stop') - T(8, '45')) / 8, .3)
js(f'tl.to("#l8w .dial",{{borderColor:"{ACC2}",color:"{ACC2}",duration:0.15}},{T(8, "stop")});')
el('l8st', 'STOPPED', 'left:330px;top:900px', cls='el stamp')
slam('l8st', T(8, 'stop'), -7)
out('l8w', T(8, 'over') - .2, 'up'); out('l8st', T(8, 'over') - .2, 'up')
el('l8p', card('<div class="lbl">P&amp;L · 10:15 AM</div><div class="big neg" id="l8n">$0</div>', f'background:{DARK};border-color:#3E2F24;width:760px'), 'left:160px;top:480px')
tilt('l8p', T(8, 'over') - .15)
count('l8n', T(8, '460'), T(8, 'dollars') - T(8, '460'), 0, -460000000, 'neg', 'power2.in')
js(f'tl.to("#l8p",{{y:700,rotation:18,autoAlpha:0,duration:0.6,ease:"power2.in"}},{T(8, "gone")});')
sfx('powerdown', T(8, 'gone'), .5)
el('l8g', 'GONE', 'left:270px;top:600px', cls='el slab huge')
slam('l8g', T(8, 'gone') - .02, -6, vol=.9, snd='impact')
burst(540, 720, T(8, 'gone') + .25, r=200)
js(f'tl.set("#l8g",{{autoAlpha:0}},{be(8) - .1});')
wipe(be(8) - .02)

# ================================================================= LINE 9  $400M rescue within a week, taken over within a year
days = ''.join(f'<i>{d}</i>' for d in 'MTWTFSS')
el('l9wk', f'<div class="lbl">WITHIN A WEEK</div><div class="wk">{days}</div>', 'left:200px;top:390px;width:680px')
js(f'tl.set("#l9wk",{{autoAlpha:1}},{bs(9)});tl.fromTo("#l9wk .wk i",{{backgroundColor:"#FFFAF7",color:"{INK}"}},{{backgroundColor:"{ACC}",color:"#fff",stagger:0.08,duration:0.1,immediateRender:false}},{bs(9) + .05});')
el('l9lb', f'{icon("mdi:lifebuoy", 230, ACC2)}<div class="chip big">$400M RESCUE</div>', 'left:330px;top:560px;text-align:center')
pop('l9lb', T(9, '400') - .1, .4); sfx('whoosh', T(9, '400') - .1, .4)
burst(540, 680, T(9, 'rescue'))
out('l9wk', T(9, 'within', 1) - .2, 'up'); out('l9lb', T(9, 'within', 1) - .2, 'up')
el('l9co', card(f'<div class="hd">{icon("mdi:office-building", 90, INK)}<div class="ttl">KNIGHT CAPITAL</div></div>', 'width:600px'), 'left:60px;top:470px')
tilt('l9co', T(9, 'within', 1) - .1)
el('l9rv', card(f'<div class="hd">{icon("mdi:domain", 90, ACC2)}<div class="ttl">RIVAL</div></div>', 'width:420px'), 'left:600px;top:800px')
slide('l9rv', T(9, 'rival') - .1, 200, 0); sfx('whoosh', T(9, 'rival'), .4)
js(f'tl.to("#l9rv",{{x:-150,y:-150,duration:0.45,ease:"power3.inOut"}},{T(9, "takes")});tl.to("#l9co",{{scale:0.92,duration:0.3}},{T(9, "takes") + .3});')
el('l9st', 'TAKEN OVER · 2013', 'left:110px;top:900px;font-size:68px', cls='el stamp')
slam('l9st', T(9, 'over') - .05, -8)
for i in ('l9co', 'l9rv', 'l9st'):
    out(i, be(9) - .12)

# ================================================================= LINE 10 lesson: delete dead code, never deploy alone
code = ''.join(f'<div class="cl{" dead" if k == 2 else ""}" id="cl{k}">{t}</div>' for k, t in enumerate(
    ['def route(order):', '    send(order)', '    power_peg()  # unused since 2003', '    log(order)']))
el('l10c', card('<div class="lbl">trading_system.py</div>' + code, 'width:880px'), 'left:100px;top:420px')
slide('l10c', bs(10) - .05)
el('l10bin', icon('mdi:delete-outline', 150, ACC2), 'left:830px;top:830px')
pop('l10bin', T(10, 'delete') - .15)
js(f'tl.to("#cl2",{{x:620,y:260,scale:0.3,rotation:20,autoAlpha:0,duration:0.5,ease:"power2.in"}},{T(10, "delete") + .1});')
sfx('whoosh', T(10, 'delete') + .1, .45); sfx('snap', T(10, 'delete') + .55, .5)
out('l10c', T(10, 'never') - .2, 'up'); out('l10bin', T(10, 'never') - .2, 'up')
el('l10ppl', f'{icon("mdi:account-multiple-check", 220, GREEN)}', 'left:420px;top:470px')
pop('l10ppl', T(10, 'never') - .05)
el('l10rv', 'REVIEWED BY 2 ✓', 'left:170px;top:770px;font-size:64px', cls='el stamp green')
slam('l10rv', T(10, 'alone'), -4, snd='ding')
out('l10ppl', be(10) - .1); out('l10rv', be(10) - .1)

# ================================================================= LINE 11 subscribe outro
el('l11n', 'TechDecoded <span>with Max</span>', 'left:0;right:0;top:470px;text-align:center', cls='el brand')
pop('l11n', bs(11) - .05, .7)
el('l11b', f'<span id="l11t">SUBSCRIBE</span>', 'left:290px;top:640px', cls='el sub')
pop('l11b', T(11, 'subscribe'), .5)
el('l11cur', icon('mdi:cursor-default', 110, INK), 'left:900px;top:900px;z-index:25')
js(f'tl.fromTo("#l11cur",{{autoAlpha:0,x:120,y:160}},{{autoAlpha:1,x:-260,y:-170,duration:0.6,ease:"power3.out",immediateRender:false}},{T(11, "subscribe") + .2});')
js(f'tl.to("#l11cur",{{scale:0.85,duration:0.08,yoyo:true,repeat:1}},{T(11, "subscribe") + .85});')
sfx('click', T(11, 'subscribe') + .85, .8)
js(f'tl.set("#l11t",{{textContent:"SUBSCRIBED ✓"}},{T(11, "subscribe") + .9});tl.to("#l11b",{{background:"#EFE6DD",color:"{INK}",duration:0.2}},{T(11, "subscribe") + .9});')
el('l11bell', icon('mdi:bell-ring', 120, ACC2), 'left:110px;top:650px')
pop('l11bell', T(11, 'subscribe') + 1.1)
js(f'tl.fromTo("#l11bell",{{rotation:-18}},{{rotation:18,duration:0.12,repeat:7,yoyo:true,immediateRender:false}},{T(11, "subscribe") + 1.2});')
sfx('ding', T(11, 'subscribe') + 1.15, .6)
el('l11x', 'more tech stories, decoded.', 'left:0;right:0;top:860px;text-align:center', cls='el serif big')
slide('l11x', T(11, 'more') - .1, 0, 40)

# ---------------------------------------------------------------- write the composition
CSS = f'''
@font-face{{font-family:'Mont';src:url('assets/fonts/montserrat-latin-900-normal.woff2');font-weight:900}}
@font-face{{font-family:'Mont';src:url('assets/fonts/montserrat-latin-800-normal.woff2');font-weight:800}}
@font-face{{font-family:'T';src:url('assets/fonts/Inter-SemiBold.otf');font-weight:600}}
@font-face{{font-family:'Ser';src:url('assets/fonts/CormorantItalic-600.ttf');font-weight:600;font-style:italic}}
@font-face{{font-family:'M';src:url('assets/fonts/JetBrainsMono-Bold.ttf');font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;overflow:hidden;background:{CREAM}}}
#root{{position:relative;width:100%;height:100%;overflow:hidden;background:radial-gradient(ellipse at 50% 40%,#FBF6F0 0%,{CREAM} 55%,#EBDCCB 100%)}}
#root:before{{content:'';position:absolute;inset:0;background:radial-gradient(#D9C3AE 2.2px,transparent 2.4px) 0 0/30px 30px;opacity:.45}}
.el{{position:absolute;opacity:0;visibility:hidden}}
.cap{{position:absolute;opacity:0;visibility:hidden;font:800 66px/1.12 'Mont';color:{INK};letter-spacing:-1.5px}}
.wd{{display:inline-block;opacity:0;margin-right:2px}}
.wd.acc{{font:600 italic 80px/1 'Ser';letter-spacing:0;background:linear-gradient(90deg,{ACC},{ACC2});-webkit-background-clip:text;color:transparent;padding-right:6px}}
.mono{{position:absolute;opacity:0;visibility:hidden;font:700 28px 'M';letter-spacing:3px;color:#9C8676}} .mono b{{color:{ACC2}}}
.card{{background:{CARD};border:3px solid #EADBCC;border-radius:34px;padding:34px 40px;box-shadow:0 34px 70px rgba(74,50,28,.22)}}
.lbl{{font:700 26px 'M';letter-spacing:3px;color:#9C8676}}
.big{{font:900 92px/1.1 'Mont';color:{INK};letter-spacing:-3px;margin-top:8px}} .neg{{color:#FF6B57}}
.sub{{font:600 32px 'T';color:#9C8676;margin-top:6px}}
.ttl{{font:900 56px 'Mont';color:{INK};letter-spacing:-1px}} .hd{{display:flex;align-items:center;gap:26px}}
.watch{{position:relative;width:100%;height:100%}} .watch .btn{{position:absolute;left:50%;top:0;width:70px;height:46px;margin-left:-35px;border-radius:12px;background:{ACC2}}}
.watch .dial{{position:absolute;left:0;right:0;top:36px;bottom:0;border-radius:50%;background:#fff;border:18px solid {INK};display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 30px 60px rgba(74,50,28,.25);color:{INK}}}
.watch .dial b{{font:900 120px 'Mont';letter-spacing:-4px}} .watch .dial span{{font:700 26px 'M';letter-spacing:4px;color:#9C8676}}
.watch.big .dial b{{font:700 104px 'M'}}
.disc{{width:340px;height:340px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 30px 60px rgba(74,50,28,.22)}}
.x1,.x2{{position:absolute;left:-10px;top:160px;width:380px;height:34px;border-radius:17px;background:{ACC2};transform-origin:50% 50%}}
.x1{{rotate:45deg}} .x2{{rotate:-45deg}}
.stamp{{padding:10px 34px;border:12px solid {ACC2};color:{ACC2};font:900 92px 'Mont';letter-spacing:3px;border-radius:20px;background:rgba(255,250,247,.9);white-space:nowrap;z-index:14}}
.stamp.green{{border-color:{GREEN};color:{GREEN};font-size:78px}}
.row{{display:flex;align-items:center;gap:26px;font:700 48px 'T';color:{INK};margin-top:30px}}
.box{{width:66px;height:66px;border-radius:16px;background:{GREEN};display:flex;align-items:center;justify-content:center;flex:none}}
.row.miss .box{{background:#fff;border:6px dashed {ACC2}}} .row.miss{{color:{ACC2}}}
.cal{{position:absolute;inset:0;background:#fff;border-radius:40px;overflow:hidden;box-shadow:0 34px 70px rgba(74,50,28,.25);text-align:center}}
.cal .ct{{background:linear-gradient(90deg,{ACC},{ACC2});color:#fff;font:900 60px 'Mont';padding:22px 0;letter-spacing:4px}}
.cal .cd{{font:900 230px/1.05 'Mont';color:{INK}}} .cal .cy{{font:700 54px 'M';color:{INK}}}
.cal.page .ct{{background:#9C8676}}
.badge{{display:inline-block;margin-top:24px;padding:10px 24px;border-radius:14px;background:linear-gradient(90deg,{ACC},{ACC2});color:#fff;font:900 34px 'Mont';opacity:0;visibility:hidden}}
.pb{{margin-top:30px;height:30px;border-radius:15px;background:#EFE6DD;overflow:hidden}} .pb i{{display:block;height:100%;background:linear-gradient(90deg,{ACC},{ACC2});transform-origin:0 50%}}
.rack{{position:absolute;width:190px;height:240px;border-radius:24px;background:#fff;border:6px solid #D9CBBE;box-shadow:0 20px 40px rgba(74,50,28,.18);padding:22px 18px;opacity:0;visibility:hidden}}
.rack i{{display:block;height:34px;border-radius:9px;background:#3A2E26;margin-bottom:14px;position:relative}} .rack i:after{{content:'';position:absolute;right:12px;top:12px;width:10px;height:10px;border-radius:5px;background:#7CE0A3}}
.rack b{{font:900 40px 'Mont';color:{INK}}} .rack .ok{{position:absolute;right:-18px;top:-18px;width:64px;height:64px;border-radius:50%;background:{GREEN};display:flex;align-items:center;justify-content:center;opacity:0;visibility:hidden}}
.rack.big{{width:300px;height:380px;padding:34px 30px;opacity:1;visibility:visible}} .rack.big i{{height:56px;margin-bottom:24px}} .rack.big b{{font-size:64px}}
.rack.glow{{border-color:{ACC2};box-shadow:0 0 60px rgba(232,64,46,.55)}}
.chip{{display:inline-block;padding:12px 28px;border-radius:16px;background:{INK};color:#fff;font:800 36px 'M';letter-spacing:2px}} .chip.big{{font:900 54px 'Mont';background:linear-gradient(90deg,{ACC},{ACC2});margin-top:10px}}
.folder{{position:relative;width:330px}} .folder .fl{{position:absolute;left:30px;top:150px;font:700 34px 'M';color:{INK}}}
.dust{{position:absolute;inset:40px 20px;background:radial-gradient(#9C8676 2px,transparent 2.5px) 0 0/22px 22px;opacity:.35}}
.pilltxt{{display:flex;align-items:center;gap:22px;font:900 56px 'Mont';color:{INK}}}
.tog{{display:inline-block;width:150px;height:74px;border-radius:37px;background:#CDBEB0;position:relative}} .tog i{{position:absolute;left:7px;top:7px;width:60px;height:60px;border-radius:30px;background:#fff;box-shadow:0 4px 10px rgba(0,0,0,.2)}}
.swl{{font:700 44px 'M'}}
.serif{{font:600 italic 84px 'Ser';background:linear-gradient(90deg,{ACC},{ACC2});-webkit-background-clip:text;color:transparent;padding-right:10px}}
.serif.big{{font-size:96px}}
.slab{{font:900 150px/1 'Mont';color:{INK};letter-spacing:-5px;white-space:nowrap}} .slab.huge{{font-size:230px;color:{ACC2}}}
.code{{font:700 40px/1.5 'M';color:{INK};margin-top:14px;white-space:pre}} .code b{{background:#FDE2D3;color:{ACC2};border-radius:8px;padding:0 6px}}
.clock{{font:700 150px 'M';color:{INK};display:flex;align-items:center;gap:20px}} .clock small{{font-size:70px}} .clock.big span{{font-size:170px}}
.mrow{{display:flex;align-items:center;gap:16px;margin-top:22px;padding:16px 20px;border-radius:16px;background:#FBF3EC;font:600 32px 'T';color:{INK};opacity:0;visibility:hidden}}
.mrow i{{width:16px;height:16px;border-radius:8px;background:{ACC2};flex:none}} .mrow span{{color:#9C8676;flex:1}} .mrow em{{font:700 26px 'M';font-style:normal;color:#9C8676}}
.cnt{{margin-left:auto;min-width:120px;text-align:center;padding:8px 22px;border-radius:40px;background:linear-gradient(90deg,{ACC},{ACC2});color:#fff;font:900 54px 'Mont'}}
.rays{{border-radius:50%;background:repeating-conic-gradient(rgba(156,134,118,.22) 0 8deg,transparent 8deg 22deg);-webkit-mask:radial-gradient(circle,#000 30%,transparent 70%)}}
.open{{display:flex;align-items:center;gap:20px;padding:18px 40px;border-radius:24px;background:#fff;border:6px solid {GREEN};color:{GREEN};font:900 80px 'Mont';white-space:nowrap}} .open i{{width:34px;height:34px;border-radius:17px;background:{GREEN}}}
.active{{position:absolute;left:60px;top:-40px;padding:8px 22px;border-radius:12px;background:{ACC2};color:#fff;font:900 40px 'Mont'}}
.oc{{position:absolute;left:0;top:0;padding:10px 18px;border-radius:12px;font:800 30px 'M';color:#fff;opacity:0;visibility:hidden;white-space:nowrap}} .oc.buy{{background:{GREEN}}} .oc.sell{{background:{ACC2}}}
.g154{{display:grid;grid-template-columns:repeat(14,1fr);gap:8px}} .g154 i{{display:block;height:30px;border-radius:6px;background:#E6D9CE}}
.wk{{display:flex;gap:14px;margin-top:16px}} .wk i{{flex:1;height:90px;border-radius:16px;border:4px solid #EADBCC;display:flex;align-items:center;justify-content:center;font:900 40px 'Mont';font-style:normal}}
.cl{{font:700 38px/1.6 'M';color:{INK};white-space:pre;margin-top:6px}} .cl.dead{{background:#FDE2D3;color:{ACC2};border-radius:10px;display:inline-block;padding:0 10px}}
.brand{{font:900 84px 'Mont';color:{INK};letter-spacing:-2px}} .brand span{{font:600 italic 84px 'Ser';background:linear-gradient(90deg,{ACC},{ACC2});-webkit-background-clip:text;color:transparent;padding-right:8px}}
.sub{{}} #l11b{{padding:28px 64px;border-radius:30px;background:linear-gradient(90deg,{ACC},{ACC2});color:#fff;font:900 76px 'Mont';box-shadow:0 18px 0 #A8301A,0 30px 60px rgba(217,56,30,.35);white-space:nowrap}}
.mxl{{position:absolute;inset:0;opacity:0;visibility:hidden}} .mxl .v{{position:absolute;inset:0;display:none}}
.mxl[data-m="b"] .vb,.mxl[data-m="A"] .vA,.mxl[data-m="E"] .vE,.mxl[data-m="O"] .vO,.mxl[data-m="M"] .vM{{display:block}}
#maxwrap{{filter:drop-shadow(0 24px 22px rgba(74,50,28,.3))}}
#ht{{position:absolute;inset:0;z-index:50;pointer-events:none}} #ht i{{position:absolute;width:54px;height:54px;border-radius:50%;background:{INK};transform:scale(0)}}
'''
SFX_SRC = ROOT / 'hf' / 'ast01-short' / 'assets' / 'sfx'
FX_DUR = {}
import wave
for f in SFX_SRC.glob('*.wav'):
    with wave.open(str(f)) as w:
        FX_DUR[f.stem] = round(w.getnframes() / w.getframerate(), 3)
aud = [f'<audio id="vo" class="clip" src="assets/vo.wav" data-start="0" data-duration="{DUR}" data-track-index="3" data-volume="1"></audio>',
       f'<audio id="bgm" class="clip" src="assets/bgm.wav" data-start="0" data-duration="{DUR}" data-track-index="4" data-volume="0.16"></audio>']
for k, (n, t, v) in enumerate(sorted(SFX, key=lambda s: s[1])):
    aud.append(f'<audio id="fx{k}" class="clip" src="assets/sfx/{n}.wav" data-start="{max(0, t)}" data-duration="{FX_DUR[n]}" data-track-index="{5 + k % 2}" data-volume="{v}"></audio>')

FMT = '''function F_n(v){return Math.round(v).toLocaleString("en-US")}
function F_int(v){return String(Math.round(v))}
function F_m(v){return "$"+Math.round(v).toLocaleString("en-US")}
function F_neg(v){return (v<0?"-":"")+"$"+Math.abs(Math.round(v)).toLocaleString("en-US")}
function F_mmss(v){v=Math.round(v);return String(Math.floor(v/60)).padStart(2,"0")+":"+String(v%60).padStart(2,"0")}'''
html = f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="assets/gsap.min.js"></script><script src="assets/host.js"></script><style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920" data-fps="30">
{chr(10).join(H)}
{chr(10).join(aud)}
</div>
<script>
{FMT}
{chr(10).join(mx_js)}
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(J)}
tl.set({{}},{{}},{DUR});
window.__timelines["main"] = tl;
</script></body></html>'''

OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'assets' / 'fonts').mkdir(parents=True, exist_ok=True)
src = ROOT / 'hf' / 'ast01-short'
for f in ('gsap.min.js',):
    shutil.copy(src / 'assets' / f, OUT / 'assets' / f)
shutil.copy(ROOT / 'hf' / 'host' / 'host.js', OUT / 'assets' / 'host.js')
if not (OUT / 'assets' / 'sfx').exists():
    shutil.copytree(SFX_SRC, OUT / 'assets' / 'sfx')
for f in ('Inter-SemiBold.otf', 'CormorantItalic-600.ttf', 'JetBrainsMono-Bold.ttf'):
    shutil.copy(src / 'assets' / 'fonts' / f, OUT / 'assets' / 'fonts' / f)
for f in ('montserrat-latin-900-normal.woff2', 'montserrat-latin-800-normal.woff2'):
    shutil.copy(ROOT / 'hf' / 'thumbs' / 'fonts' / f, OUT / 'assets' / 'fonts' / f)
shutil.copy(ROOT / 'public' / tl['vo'], OUT / 'assets' / 'vo.wav')
shutil.copy(ROOT / 'public' / tl['music'], OUT / 'assets' / 'bgm.wav')
for f in ('hyperframes.json', 'meta.json'):
    if (src / f).exists() and not (OUT / f).exists():
        shutil.copy(src / f, OUT / f)
m = json.loads((OUT / 'meta.json').read_text()); m.update(id=TID, name=TID); (OUT / 'meta.json').write_text(json.dumps(m))
(OUT / 'index.html').write_text(html)
print(f'wrote {OUT}/index.html  dur {DUR}s  elements {len(H)}  tweens {len(J)}  sfx {len(SFX)}')
