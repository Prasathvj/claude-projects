"""Two 23-second style samples for the owner (2026-11-23): PAPERCUT and VOX (no photos), both on the first three
narration lines of ep05. Each is a single HyperFrames page (hf/sample-papercut, hf/sample-vox).
Usage: python3 tools/style_samples.py   then render each project."""
import json, shutil, subprocess
from pathlib import Path

R = Path(__file__).resolve().parent.parent
TL = json.loads((R / 'src/episodes/ep05-long.timeline.json').read_text())
BEATS = TL['beats'][:3]
DUR = round(BEATS[-1]['start'] + BEATS[-1]['dur'] + 0.6, 2)

FONTS = """@font-face { font-family:'D'; src:url('assets/fonts/InterDisplay-Black.otf'); font-weight:900; }
@font-face { font-family:'D'; src:url('assets/fonts/InterDisplay-Bold.otf'); font-weight:700; }
@font-face { font-family:'T'; src:url('assets/fonts/Inter-SemiBold.otf'); font-weight:600; }
@font-face { font-family:'H'; src:url('assets/fonts/Caveat-700-latin.woff2'); font-weight:700; }
@font-face { font-family:'M'; src:url('assets/fonts/JetBrainsMono-Bold.ttf'); font-weight:700; }"""

def captions(style):
    """one caption line per beat, current word highlighted (same idea as the channel captions)"""
    h, sc = [], []
    for bi, b in enumerate(BEATS):
        words = b['words']; t0 = b['start']
        # split the line into chunks of ~7 words so it fits
        chunks = [words[k:k + 7] for k in range(0, len(words), 7)]
        for ci, ch in enumerate(chunks):
            cid = f'cap{bi}_{ci}'
            spans = ' '.join(f'<span id="{cid}w{k}">{w["w"]}</span>' for k, w in enumerate(ch))
            h.append(f'<div class="cap" id="{cid}">{spans}</div>')
            a, z = t0 + ch[0]['s'], t0 + ch[-1]['e'] + 0.15
            sc.append(f'tl.set("#{cid}", {{ opacity:1 }}, {a:.2f}); tl.set("#{cid}", {{ opacity:0 }}, {z:.2f});')
            for k, w in enumerate(ch):
                sc.append(f'tl.set("#{cid}w{k}", {{ className:"on" }}, {t0 + w["s"]:.2f}); tl.set("#{cid}w{k}", {{ className:"" }}, {t0 + w["e"]:.2f});')
    return '\n'.join(h), '\n'.join(sc)

def page(name, css, body, script):
    cap_h, cap_s = captions(name)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1920, height=1080" />
<script src="assets/gsap.min.js"></script>
<style>{FONTS}
* {{ margin:0; padding:0; box-sizing:border-box; }} html, body {{ width:1920px; height:1080px; overflow:hidden; }}
#root {{ position:relative; width:1920px; height:1080px; overflow:hidden; }}
.a {{ position:absolute; }}
{css}
</style></head><body>
<svg width="0" height="0" style="position:absolute"><defs>
 <filter id="paper"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="4" result="n"/><feColorMatrix in="n" type="saturate" values="0" result="g"/>
  <feComponentTransfer in="g" result="g2"><feFuncA type="linear" slope=".18"/></feComponentTransfer><feComposite in="g2" in2="SourceGraphic" operator="in" result="tex"/>
  <feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="tex"/></feMerge></filter>
 <filter id="rough"><feTurbulence type="turbulence" baseFrequency=".035" numOctaves="2" seed="7" result="t"/><feDisplacementMap in="SourceGraphic" in2="t" scale="7"/></filter>
</defs></svg>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1920" data-height="1080" data-fps="30">
{body}
{cap_h}
<audio id="vo" class="clip" src="assets/vo.wav" data-start="0" data-duration="{DUR}" data-track-index="5" data-volume="1"></audio>
<audio id="bgm" class="clip" src="assets/bgm.wav" data-start="0" data-duration="{DUR}" data-track-index="6" data-volume="0.14"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused:true }});
{script}
{cap_s}
window.__timelines["main"] = tl;
</script></body></html>"""

def B(i, f=0.0):
    b = BEATS[i]; return round(b['start'] + f * b['dur'], 2)

# ================================================================== PAPERCUT
def papercut():
    css = """#root { background:#E9D8C0; }
.bgp { position:absolute; inset:0; background:radial-gradient(circle at 30% 30%,#F3E6D3,#E2CDAF 70%,#D3B892); filter:url(#paper); }
.sheet { filter:url(#paper) url(#rough); box-shadow:0 14px 0 rgba(70,40,15,.18), 0 26px 40px rgba(70,40,15,.25); }
.cut { filter:url(#paper); }
.sh { filter:drop-shadow(0 10px 0 rgba(70,40,15,.18)) drop-shadow(0 22px 22px rgba(70,40,15,.25)); }
.strip { position:absolute; padding:14px 30px; font:900 58px 'D'; color:#2A2018; background:#FFF6E8; clip-path:polygon(0 6%,4% 0,30% 4%,62% 0,100% 5%,97% 50%,100% 96%,66% 100%,33% 95%,3% 100%,0 60%); }
.lbl { position:absolute; padding:18px 40px; font:900 64px 'D'; color:#FFF6E8; background:#F87736; clip-path:polygon(0 8%,10% 0,50% 6%,92% 0,100% 12%,98% 90%,88% 100%,40% 94%,6% 100%,1% 70%); }
.cap { position:absolute; left:0; right:0; top:930px; text-align:center; font:800 52px 'D'; color:#2A2018; opacity:0; }
.cap span { padding:2px 10px; } .cap span.on { background:#F87736; color:#FFF6E8; clip-path:polygon(0 8%,96% 0,100% 90%,4% 100%); }
.grain { position:absolute; inset:-50%; background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='f'><feTurbulence type='fractalNoise' baseFrequency='1.1' numOctaves='2'/></filter><rect width='160' height='160' filter='url(%23f)' opacity='.55'/></svg>"); opacity:.13; mix-blend-mode:multiply; pointer-events:none; }"""
    laptop = """<div class="a sh" id="lap" style="left:300px; top:330px; width:640px; height:470px">
  <div class="a sheet" style="left:40px; top:0; width:560px; height:360px; background:#4A3B33; border-radius:22px"></div>
  <div class="a cut" style="left:70px; top:28px; width:500px; height:304px; background:#FFF6E8; border-radius:10px"></div>
  <div class="a sheet" style="left:0; top:350px; width:640px; height:70px; background:#C9B49C; border-radius:10px 10px 30px 30px"></div>
</div>"""
    bubble = """<div class="a sh" id="bub" style="left:390px; top:380px"><div class="strip" style="position:relative; font-size:40px; background:#F87736; color:#FFF6E8">Write a poem about chai</div></div>"""
    words = ''.join(f'<div class="a sh" id="w{k}" style="left:{390 + k * 160}px; top:500px"><div class="strip" style="position:relative; font-size:46px">{w}</div></div>'
                    for k, w in enumerate(['Chai', 'is', 'warm', '…']))
    # Bit as paper cut-out
    bit = """<div class="a sh" id="bit" style="left:1180px; top:380px; width:300px; height:360px">
  <div class="a sheet" style="left:140px; top:0; width:20px; height:60px; background:#C9B49C"></div><div class="a cut" style="left:126px; top:-20px; width:48px; height:48px; border-radius:50%; background:#F87736"></div>
  <div class="a sheet" style="left:20px; top:50px; width:260px; height:190px; border-radius:60px; background:#FFF6E8"></div>
  <div class="a cut" style="left:55px; top:90px; width:190px; height:110px; border-radius:40px; background:#2A2018"></div>
  <div class="a cut" id="eyeL" style="left:95px; top:120px; width:36px; height:44px; border-radius:50%; background:#6EC8FF"></div><div class="a cut" id="eyeR" style="left:170px; top:120px; width:36px; height:44px; border-radius:50%; background:#6EC8FF"></div>
  <div class="a sheet" style="left:55px; top:235px; width:190px; height:120px; border-radius:40px 40px 60px 60px; background:#F87736"></div>
</div>"""
    wheel_segs = ''.join(f'<div class="a cut" style="left:180px; top:180px; width:160px; height:44px; margin:-22px 0 0 0; transform-origin:0 50%; transform:rotate({k * 45}deg) translateX(40px); background:{"#FFF6E8" if k % 2 else "#FFD9B8"}; border-radius:8px"></div>' for k in range(8))
    wheel = f"""<div class="a sh" id="wheel" style="left:220px; top:150px; width:360px; height:360px; opacity:0">
  <div class="a sheet" style="inset:0; border-radius:50%; background:#F87736"></div>{wheel_segs}
  <div class="a cut" style="left:150px; top:150px; width:60px; height:60px; border-radius:50%; background:#2A2018"></div></div>"""
    line = '<div class="a sheet" id="line" style="left:700px; top:610px; width:980px; height:14px; background:#4A3B33; border-radius:7px; transform-origin:left"></div>'
    pieces = ''.join(f'<div class="a sh" id="p{k}" style="left:{720 + k * 240}px; top:520px; opacity:0"><div class="strip" style="position:relative; font-size:44px">{w}</div></div>'
                     for k, w in enumerate(['It', ' picks', ' one', ' piece']))
    lbl1 = '<div class="a sh" id="lbl1" style="left:760px; top:200px; opacity:0"><div class="lbl" style="position:relative">ONE PIECE AT A TIME</div></div>'
    people = ''.join(f'<div class="a sh pp" id="pp{k}" style="left:{180 + (k % 12) * 70}px; top:{560 + (k // 12) * 110}px; opacity:0">'
                     f'<div class="a cut" style="left:14px; top:0; width:34px; height:34px; border-radius:50%; background:{["#F87736","#4A3B33","#C9B49C"][k % 3]}"></div>'
                     f'<div class="a cut" style="left:0; top:38px; width:62px; height:58px; border-radius:30px 30px 8px 8px; background:{["#F87736","#4A3B33","#C9B49C"][k % 3]}"></div></div>' for k in range(36))
    big = """<div class="a" id="big" style="left:1080px; top:250px; opacity:0">
  <div style="position:relative; font:900 210px 'D'; color:#F87736; line-height:.9; text-shadow:6px 8px 0 #4A3B33, 12px 16px 0 rgba(70,40,15,.25)">≈1B</div>
  <div class="strip" style="position:relative; margin-top:30px; font-size:48px">people every week</div></div>"""
    src = '<div class="a" id="src" style="left:1120px; top:760px; opacity:0; font:600 26px \'T\'; color:#4A3B33">Source: OpenAI, Sept 2026</div>'
    body = f'<div class="bgp"></div>{laptop}{bubble}{words}{bit}{wheel}{line}{pieces}{lbl1}{people}{big}{src}<div class="grain" id="grain"></div>'
    s = []
    step = 'steps(5)'   # stop-motion: every move snaps through a few poses
    s.append('tl.fromTo("#grain", { x:0, y:0 }, { x:-60, y:40, duration:%s, ease:"steps(%d)" }, 0);' % (DUR, int(DUR * 12)))
    # beat 0
    s += [f'tl.fromTo("#lap", {{ y:500, rotation:-8 }}, {{ y:0, rotation:-2, duration:.6, ease:"{step}" }}, 0.1);',
          f'tl.fromTo("#bit", {{ x:500, rotation:12 }}, {{ x:0, rotation:3, duration:.6, ease:"{step}" }}, 0.4);',
          f'tl.fromTo("#bub", {{ scale:0, rotation:-10 }}, {{ scale:1, rotation:-3, duration:.4, ease:"steps(4)" }}, {B(0, .08)});']
    for k in range(4):
        s.append(f'tl.fromTo("#w{k}", {{ opacity:0, y:-400, rotation:{(-1) ** k * 14} }}, {{ opacity:1, y:0, rotation:{(-1) ** k * 3}, duration:.4, ease:"steps(4)" }}, {B(0, .3 + k * .14)});')
    s.append(f'tl.to("#bit", {{ y:-14, duration:.25, ease:"steps(2)", yoyo:true, repeat:{int(B(0, 1) / .5)} }}, 1.0);')
    # beat 1: clear, wheel + pieces
    s += [f'tl.to(["#lap","#bub","#w0","#w1","#w2","#w3"], {{ y:900, rotation:12, duration:.5, ease:"steps(4)", stagger:.04 }}, {B(1) - .3});',
          f'tl.to("#bit", {{ x:180, y:-60, scale:.8, duration:.5, ease:"steps(4)" }}, {B(1) - .3});',
          f'tl.fromTo("#wheel", {{ opacity:0, scale:.3 }}, {{ opacity:1, scale:1, duration:.4, ease:"steps(4)" }}, {B(1, .02)});',
          f'tl.to("#wheel", {{ rotation:720, duration:{BEATS[1]["dur"]:.2f}, ease:"steps(48)" }}, {B(1, .05)});',
          f'tl.fromTo("#line", {{ scaleX:0 }}, {{ scaleX:1, duration:.5, ease:"steps(5)" }}, {B(1, .15)});',
          f'tl.fromTo("#lbl1", {{ opacity:0, y:-200, rotation:-6 }}, {{ opacity:1, y:0, rotation:-2, duration:.4, ease:"steps(4)" }}, {B(1, .55)});']
    for k in range(4):
        s.append(f'tl.fromTo("#p{k}", {{ opacity:0, x:-500, y:-300, rotation:-30 }}, {{ opacity:1, x:0, y:0, rotation:{(-1) ** k * 3}, duration:.45, ease:"steps(5)" }}, {B(1, .25 + k * .16)});')
    # beat 2: people + number
    s += [f'tl.to(["#wheel","#line","#p0","#p1","#p2","#p3","#lbl1"], {{ y:-900, rotation:-10, duration:.5, ease:"steps(4)", stagger:.03 }}, {B(2) - .3});',
          f'tl.to("#bit", {{ x:-1600, y:300, scale:.6, duration:.5, ease:"steps(4)" }}, {B(2) - .3});']
    for k in range(36):
        s.append(f'tl.fromTo("#pp{k}", {{ opacity:0, y:-60 }}, {{ opacity:1, y:0, duration:.2, ease:"steps(2)" }}, {B(2, .05) + k * .05:.2f});')
    s += [f'tl.fromTo("#big", {{ opacity:0, scale:2.4, rotation:-8 }}, {{ opacity:1, scale:1, rotation:-3, duration:.35, ease:"steps(4)" }}, {B(2, .2)});',
          f'tl.to("#src", {{ opacity:1, duration:.2 }}, {B(2, .5)});',
          f'tl.to(".pp", {{ y:-10, duration:.25, ease:"steps(2)", yoyo:true, repeat:9, stagger:.02 }}, {B(2, .6)});']
    return page('papercut', css, body, '\n'.join(s))

# ================================================================== VOX (no photos)
def vox():
    css = """#root { background:#F2EEE6; }
.bgv { position:absolute; inset:0; background:#F2EEE6; }
.ht { position:absolute; width:900px; height:900px; border-radius:50%; background-image:radial-gradient(#E8B898 30%, transparent 32%); background-size:22px 22px;
  -webkit-mask-image:radial-gradient(circle, #000 0%, transparent 70%); mask-image:radial-gradient(circle, #000 0%, transparent 70%); opacity:.55; }
.fold { position:absolute; top:0; bottom:0; width:2px; background:linear-gradient(180deg,transparent,rgba(0,0,0,.06),transparent); }
.doc { position:absolute; background:#FFFDF8; box-shadow:0 2px 0 rgba(0,0,0,.08), 0 30px 60px rgba(40,30,20,.18); filter:url(#paper); }
.mono { font:700 40px 'M'; color:#222; line-height:1.7; }
.hl { position:absolute; height:58px; background:#FFE14D; mix-blend-mode:multiply; transform-origin:left; transform:scaleX(0); border-radius:6px 14px 8px 12px; }
.hand { font:700 64px 'H'; color:#E5332A; }
.kick { font:900 30px 'D'; letter-spacing:6px; color:#111; }
.tape { position:absolute; width:150px; height:46px; background:rgba(255,236,170,.75); box-shadow:0 2px 6px rgba(0,0,0,.08); }
.cap { position:absolute; left:0; right:0; top:950px; text-align:center; font:700 50px 'D'; color:#111; opacity:0; }
.cap span { padding:0 8px; } .cap span.on { background:#FFE14D; }
.grain { position:absolute; inset:-50%; background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='f'><feTurbulence type='fractalNoise' baseFrequency='1.1' numOctaves='2'/></filter><rect width='160' height='160' filter='url(%23f)' opacity='.5'/></svg>"); opacity:.10; mix-blend-mode:multiply; }
.tok { position:absolute; padding:10px 22px; font:900 54px 'D'; color:#111; background:#FFFDF8; border:4px solid #111; opacity:0; }
.ink { stroke:#E5332A; stroke-width:9; fill:none; stroke-linecap:round; stroke-linejoin:round; }"""
    doc = """<div class="doc" id="doc" style="left:220px; top:170px; width:1000px; height:560px; padding:56px 64px">
  <div class="kick" style="color:#999">CHATGPT · LIVE ANSWER (ILLUSTRATION)</div>
  <div class="mono" style="margin-top:30px; color:#888">&gt; Write a poem about chai</div>
  <div class="mono" style="margin-top:16px"><span id="t0" style="opacity:0">Chai </span><span id="t1" style="opacity:0">is </span><span id="t2" style="opacity:0">warm, </span><span id="t3" style="opacity:0">a </span><span id="t4" style="opacity:0">quiet </span><span id="t5" style="opacity:0">…</span><span id="cur" style="background:#111; color:#111">_</span></div>
  <div class="mono" style="margin-top:50px; font-size:30px; color:#555; position:relative">The model has <span style="position:relative">no plan<div class="hl" id="hl1" style="left:-8px; top:-6px; width:180px; height:56px"></div></span> for the rest of the sentence.</div>
</div>
<div class="tape" style="left:240px; top:150px; transform:rotate(-6deg)"></div><div class="tape" style="left:1100px; top:150px; transform:rotate(5deg)"></div>
<svg class="a" id="circ" width="300" height="170" style="left:505px; top:432px"><path class="ink" id="cpath" d="M15 85 C 20 25, 230 10, 262 65 C 278 120, 135 150, 50 132 C 10 118, 18 55, 78 38"/></svg>
<div class="a hand" id="note1" style="left:1280px; top:470px; transform:rotate(-6deg); opacity:0">no idea<br>what's next!</div>"""
    toks = ''.join(f'<div class="tok" id="k{k}" style="left:{190 + k * 230}px; top:420px; transform:rotate({(-1) ** k * 2}deg)">{w}</div>' for k, w in enumerate(['It', 'picks', 'one', 'piece', '→ next']))
    arrows = ''.join(f'<svg class="a" width="120" height="80" style="left:{360 + k * 230}px; top:330px"><path class="ink arr" id="ar{k}" d="M10 60 C 40 10, 80 10, 110 50 M95 30 L110 50 L86 58"/></svg>' for k in range(4))
    strip = f"""<div class="a" id="strip" style="left:0; top:0; width:1920px; height:1080px; opacity:0">
  <div class="a kick" style="left:190px; top:250px">HOW IT WRITES</div>{toks}{arrows}
  <div class="a" style="left:190px; top:600px; font:900 120px 'D'; color:#111; letter-spacing:-3px; position:absolute"><span style="position:relative">ONE PIECE<div class="hl" id="hl2" style="left:-10px; top:20px; width:720px; height:110px"></div></span> AT A TIME</div></div>"""
    big = """<div class="a" id="stat" style="left:0; top:0; width:1920px; height:1080px; opacity:0">
  <div class="ht" style="left:900px; top:60px"></div>
  <div class="a kick" style="left:200px; top:200px">CHATGPT · WEEKLY USERS</div>
  <div class="a" style="left:190px; top:300px; font:900 250px 'D'; color:#111; letter-spacing:-8px; line-height:1"><span id="num" style="display:inline-block">1</span> <span id="bil" style="color:#E5332A; display:inline-block">BILLION</span></div>
  <div class="a" style="left:200px; top:620px; font:700 46px 'D'; color:#333">people use it <span style="position:relative">every week<div class="hl" id="hl3" style="left:-6px; top:-2px; width:270px; height:58px"></div></span></div>
  <div class="doc" id="clip" style="left:1180px; top:560px; width:520px; padding:26px 30px; transform:rotate(3deg)"><div style="font:700 22px 'M'; color:#888">SOURCE</div><div style="font:700 30px 'T'; color:#111; margin-top:8px">OpenAI, September 2026: ≈ 1 billion weekly users</div></div>
  <div class="tape" style="left:1380px; top:540px; transform:rotate(-4deg)"></div>
  <div class="a hand" id="note2" style="left:760px; top:600px; transform:rotate(-8deg); opacity:0">that's 1 in 8<br>people on Earth*</div>
  <div class="a" style="left:770px; top:790px; font:600 20px 'T'; color:#777" id="fn">*approx., world population ≈ 8.2 billion</div></div>"""
    body = f'<div class="bgv"></div><div class="ht" style="left:-300px; top:500px"></div><div class="fold" style="left:640px"></div><div class="fold" style="left:1280px"></div>{doc}{strip}{big}<div class="grain" id="grain"></div>'
    s = ['tl.fromTo("#grain", { x:0, y:0 }, { x:-60, y:40, duration:%s, ease:"steps(%d)" }, 0);' % (DUR, int(DUR * 12)),
         'tl.fromTo("#doc", { y:60, rotation:-1.5, opacity:0 }, { y:0, rotation:-.5, opacity:1, duration:.6, ease:"power3.out" }, 0.1);',
         'tl.to("#cur", { opacity:0, duration:.01, repeat:%d, yoyo:true, repeatDelay:.4 }, 0.3);' % int(B(1) / .41)]
    for k in range(6):
        s.append(f'tl.to("#t{k}", {{ opacity:1, duration:.01 }}, {B(0, .12 + k * .09):.2f});')
    s += [f'tl.to("#hl1", {{ scaleX:1, duration:.45, ease:"power2.out" }}, {B(0, .7)});',
          'tl.set("#cpath", { strokeDasharray:1400, strokeDashoffset:1400 }, 0);',
          f'tl.to("#cpath", {{ strokeDashoffset:0, duration:.7, ease:"power2.inOut" }}, {B(0, .78)});',
          f'tl.to("#note1", {{ opacity:1, duration:.3 }}, {B(0, .86)});',
          # beat 1
          f'tl.to(["#doc","#circ","#note1",".tape"], {{ opacity:0, x:-120, duration:.35, ease:"power2.in" }}, {B(1) - .2});',
          f'tl.to("#strip", {{ opacity:1, duration:.3 }}, {B(1, .02)});']
    for k in range(5):
        s.append(f'tl.fromTo("#k{k}", {{ opacity:0, y:-40, scale:1.3 }}, {{ opacity:1, y:0, scale:1, duration:.3, ease:"back.out(2)" }}, {B(1, .1 + k * .13):.2f});')
    s.append('tl.set(".arr", { strokeDasharray:300, strokeDashoffset:300 }, 0);')
    for k in range(4):
        s.append(f'tl.to("#ar{k}", {{ strokeDashoffset:0, duration:.35 }}, {B(1, .17 + k * .13):.2f});')
    s += [f'tl.to("#hl2", {{ scaleX:1, duration:.5, ease:"power2.out" }}, {B(1, .8)});',
          # beat 2
          f'tl.to("#strip", {{ opacity:0, y:-80, duration:.35 }}, {B(2) - .2});',
          f'tl.to("#stat", {{ opacity:1, duration:.3 }}, {B(2, .02)});',
          f'tl.fromTo("#num", {{ opacity:0, scale:2.5 }}, {{ opacity:1, scale:1, duration:.35, ease:"expo.out" }}, {B(2, .05)});', f'tl.fromTo("#bil", {{ opacity:0, x:120 }}, {{ opacity:1, x:0, duration:.4, ease:"back.out(2)" }}, {B(2, .15)});',
          f'tl.to("#hl3", {{ scaleX:1, duration:.4 }}, {B(2, .35)});',
          f'tl.fromTo("#clip", {{ opacity:0, y:80 }}, {{ opacity:1, y:0, duration:.45, ease:"back.out(1.6)" }}, {B(2, .45)});',
          f'tl.to("#note2", {{ opacity:1, duration:.3 }}, {B(2, .6)});']
    return page('vox', css, body, '\n'.join(s))

if __name__ == '__main__':
    src = R / 'hf/ep05-long/assets'
    for name, fn in (('sample-papercut', papercut), ('sample-vox', vox)):
        P = R / 'hf' / name; (P / 'assets').mkdir(parents=True, exist_ok=True)
        for a in ('fonts', 'gsap.min.js'):
            if not (P / 'assets' / a).exists():
                (shutil.copytree if (src / a).is_dir() else shutil.copy)(src / a, P / 'assets' / a)
        shutil.copy(R / 'hf/style-samples/assets/fonts/Caveat-700-latin.woff2', P / 'assets/fonts/Caveat-700-latin.woff2')
        shutil.copy(R / 'hf/ep05-long/hyperframes.json', P / 'hyperframes.json')
        (P / 'meta.json').write_text(json.dumps({'id': name, 'name': name, 'createdAt': '2026-11-23T05:00:00.000Z'}))
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(src / 'vo.wav'), '-t', str(DUR), str(P / 'assets/vo.wav')], check=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(src / 'bgm.wav'), '-t', str(DUR), '-af', f'afade=t=out:st={DUR - 2}:d=2', str(P / 'assets/bgm.wav')], check=True)
        (P / 'index.html').write_text(fn())
        print('written', P, DUR)
