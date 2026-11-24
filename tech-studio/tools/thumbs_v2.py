"""Thumbnails v2 (owner 2026-11-24, after thumbnail research): one big subject, Max smaller and DOING something
(varied emotion), 2-4 words that add to the title (never repeat it), <=3 main elements, high contrast (dark text,
no orange text on cream), nothing important bottom-right (YouTube's duration stamp), no brand watermark.
Writes hf/thumbs/v2_<id>.html. Render: node tools/thumbs_v2_render.cjs (4K screenshot -> lanczos downscale).
Usage: python3 tools/thumbs_v2.py"""
import pathlib

OUT = pathlib.Path('hf/thumbs')
MAX = "{skin:'#F0C4A0',hair:'messy',hairCol:'#5A3A26',glasses:'round',hood:'down',top:'#F87736',topS:'#D85E25',phones:'none',beard:'stubble'}"

HEAD = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'D';src:url('/ep01-test/assets/fonts/InterDisplay-Black.otf');font-weight:900}
@font-face{font-family:'B';src:url('/ep01-test/assets/fonts/InterDisplay-Bold.otf');font-weight:700}
@font-face{font-family:'T';src:url('/ep01-test/assets/fonts/Inter-SemiBold.otf');font-weight:600}
@font-face{font-family:'M';src:url('/ep01-test/assets/fonts/JetBrainsMono-Bold.ttf');font-weight:700}
*{margin:0;box-sizing:border-box} body{width:1920px;height:1080px;position:relative;overflow:hidden}
.cream{background:radial-gradient(ellipse at 38% 45%,#FBF5EE 0%,#F4EDE3 45%,#E9D7C4 100%)}
.cream:before{content:'';position:absolute;inset:0;background:radial-gradient(#DCC3AE 2.4px,transparent 2.6px) 0 0/38px 38px;opacity:.55}
.glow{position:absolute;border-radius:50%;filter:blur(60px)}
.h{position:absolute;font:900 190px/0.92 'D';color:#22180F;letter-spacing:-6px;text-shadow:0 6px 0 rgba(255,250,247,.9),0 14px 30px rgba(74,50,28,.18)}
.hl{display:inline-block;background:#F87736;color:#22180F;padding:0 26px 6px;border-radius:22px;transform:rotate(-2deg);box-shadow:0 14px 0 #C9521D,0 26px 40px rgba(74,50,28,.3);text-shadow:none}
.card{position:absolute;background:#FFFAF7;border-radius:40px;box-shadow:0 50px 100px rgba(60,38,20,.35),0 0 0 4px #E5CFBC}
#max{position:absolute;filter:drop-shadow(0 30px 26px rgba(60,38,20,.35))}
</style><script src="/host/host.js"></script></head>"""


def maxdiv(left, top, w, pose, flip=False, extra_style=''):
    fl = 'transform:scaleX(-1);' if flip else ''
    h = int(w * 1.3)
    return (f'<div id="max" style="left:{left}px;top:{top}px;{fl}{extra_style}"></div>'
            f"<script>document.getElementById('max').innerHTML=HOST.render({{char:{MAX},{pose},w:{w},h:{h}}});</script>")


T = {}

# ---------- ep08: GPT-6 Astra (title already says how/free) -> the hook: it's hidden
T['ep08'] = f"""<body class="cream">
<div class="glow" style="left:120px;top:300px;width:1000px;height:700px;background:rgba(248,119,54,.25)"></div>
<div class="h" style="left:80px;top:56px">IT'S <span class="hl">HIDDEN</span></div>
<div class="card" style="left:90px;top:330px;width:1080px;height:660px;transform:rotate(-1.5deg);overflow:hidden">
 <div style="height:92px;background:#F3EAE1;display:flex;align-items:center;gap:18px;padding:0 36px;font:700 40px 'B';color:#5A4636">
  <i style="width:24px;height:24px;border-radius:12px;background:#FF5F57"></i><i style="width:24px;height:24px;border-radius:12px;background:#FEBC2E"></i><i style="width:24px;height:24px;border-radius:12px;background:#28C840"></i>
  <svg viewBox="0 0 256 260" width="46" height="46" style="margin-left:14px"><path fill="#22180F" d="M239.184 106.203a64.72 64.72 0 0 0-5.576-53.103C219.452 28.459 191 15.784 163.213 21.74A65.586 65.586 0 0 0 52.096 45.22a64.72 64.72 0 0 0-43.23 31.36c-14.31 24.602-11.061 55.634 8.033 76.74a64.67 64.67 0 0 0 5.525 53.102c14.174 24.65 42.644 37.324 70.446 31.36a64.72 64.72 0 0 0 48.754 21.744c28.481.025 53.714-18.361 62.414-45.481a64.77 64.77 0 0 0 43.229-31.36c14.137-24.558 10.875-55.423-8.083-76.483m-97.56 136.338a48.4 48.4 0 0 1-31.105-11.255l1.535-.87l51.67-29.825a8.6 8.6 0 0 0 4.247-7.367v-72.85l21.845 12.636c.218.111.37.32.409.563v60.367c-.056 26.818-21.783 48.545-48.601 48.601M37.158 197.93a48.35 48.35 0 0 1-5.781-32.589l1.534.921l51.722 29.826a8.34 8.34 0 0 0 8.441 0l63.181-36.425v25.221a.87.87 0 0 1-.358.665l-52.335 30.184c-23.257 13.398-52.97 5.431-66.404-17.803M23.549 85.38a48.5 48.5 0 0 1 25.58-21.333v61.39a8.29 8.29 0 0 0 4.195 7.316l62.874 36.272l-21.845 12.636a.82.82 0 0 1-.767 0L41.353 151.53c-23.211-13.454-31.171-43.144-17.804-66.405zm179.466 41.695l-63.08-36.63L161.73 77.86a.82.82 0 0 1 .768 0l52.233 30.184a48.6 48.6 0 0 1-7.316 87.635v-61.391a8.54 8.54 0 0 0-4.4-7.213m21.742-32.69l-1.535-.922l-51.619-30.081a8.39 8.39 0 0 0-8.492 0L99.98 99.808V74.587a.72.72 0 0 1 .307-.665l52.233-30.133a48.652 48.652 0 0 1 72.236 50.391zM88.061 139.097l-21.845-12.585a.87.87 0 0 1-.41-.614V65.685a48.652 48.652 0 0 1 79.757-37.346l-1.535.87l-51.67 29.825a8.6 8.6 0 0 0-4.246 7.367zm11.868-25.58L128.067 97.3l28.188 16.218v32.434l-28.086 16.218l-28.188-16.218z"/></svg>ChatGPT</div>
 <div style="margin:40px 50px 0;padding:26px 34px;border:5px solid #22180F;border-radius:26px;font:700 66px 'B';color:#22180F;display:flex;gap:26px;align-items:center">
  <svg viewBox="0 0 256 256" width="64" height="64"><path fill="#22180F" d="M232.49 215.51L185 168a92.12 92.12 0 1 0-17 17l47.53 47.54a12 12 0 0 0 17-17ZM44 112a68 68 0 1 1 68 68a68.07 68.07 0 0 1-68-68"/></svg>Astra<span style="width:6px;height:70px;background:#22180F;margin-left:-14px"></span></div>
 <div style="margin:30px 84px 0;font:700 58px 'B';color:#9C8676">GPT-6.2 Sol</div>
 <div style="margin:26px 84px 0;font:700 58px 'B';color:#9C8676">GPT-6 mini</div>
 <div style="position:absolute;left:52px;top:520px;padding:14px 34px;background:#E0291C;color:#fff;font:900 64px 'D';border-radius:20px;transform:rotate(-2deg);box-shadow:0 14px 30px rgba(224,41,28,.4)">No results for "Astra"</div>
</div>
{maxdiv(1235, 175, 700, "brows:'skeptic',eyes:'open',look:[-1,0],mouth:'O',arms:'point'", flip=True)}
</body></html>"""

# ---------- myst01: TV hijack (dark mystery look)
T['myst01'] = """<body style="background:radial-gradient(ellipse at 35% 50%,#1A2438 0%,#0A0F1A 55%,#020305 100%)">
<div class="glow" style="left:160px;top:250px;width:900px;height:700px;background:rgba(90,140,255,.22)"></div>
<div style="position:absolute;left:56px;top:46px;display:flex;gap:16px;align-items:center;font:700 34px 'M';letter-spacing:8px;color:#AEB9CC"><i style="width:22px;height:22px;border-radius:11px;background:#E5383B;box-shadow:0 0 24px #E5383B;display:inline-block"></i>TECH MYSTERIES · CASE 001</div>
<div style="position:absolute;left:40px;top:150px;width:1120px;height:880px;border-radius:80px;background:linear-gradient(160deg,#4A3A2C,#1C1611);box-shadow:0 70px 140px rgba(0,0,0,.9),inset 0 0 0 12px #2E241B;transform:rotate(-3deg)">
 <div style="position:absolute;left:70px;top:70px;width:860px;height:680px;border-radius:90px/70px;overflow:hidden;background:repeating-linear-gradient(90deg,#16181D 0 30px,#6C7280 30px 42px,#262A33 42px 74px,#3B404B 74px 86px)">
  <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(255,40,80,.32),rgba(40,255,230,.22),rgba(255,40,80,.2));mix-blend-mode:screen"></div>
  <svg viewBox="0 0 860 680" width="860" height="680" style="position:absolute;inset:0"><defs><radialGradient id="r" cx=".5" cy=".4" r=".6"><stop offset="0" stop-color="#2A2A2A"/><stop offset="1" stop-color="#040404"/></radialGradient></defs>
   <ellipse cx="430" cy="300" rx="165" ry="205" fill="url(#r)"/><path d="M150 680 Q170 470 430 450 Q690 470 710 680 Z" fill="#050505"/>
   <rect x="320" y="250" width="220" height="44" rx="14" fill="#0B0B0B" stroke="#3A3A3A" stroke-width="4"/>
   <path d="M360 380 Q430 410 500 380" stroke="#555" stroke-width="10" fill="none" stroke-linecap="round"/></svg>
  <div style="position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,.35) 0 3px,transparent 3px 6px);box-shadow:inset 0 0 120px rgba(0,0,0,.95)"></div>
 </div>
 <div style="position:absolute;right:46px;top:160px"><i style="display:block;width:92px;height:92px;border-radius:46px;background:#0E0B09;margin-bottom:50px;box-shadow:inset 0 0 0 8px #3A2E24"></i><i style="display:block;width:92px;height:92px;border-radius:46px;background:#0E0B09;box-shadow:inset 0 0 0 8px #3A2E24"></i></div>
</div>
<div style="position:absolute;left:1190px;top:150px;font:900 205px/0.9 'D';color:#EEF2F8;letter-spacing:-6px;text-shadow:0 10px 40px rgba(0,0,0,.8)">WHO<br>WAS<br><span style="color:#FF3B3E;text-shadow:0 0 40px rgba(229,56,59,.6)">HE?</span></div>
<div style="position:absolute;left:1200px;top:800px;padding:8px 34px;border:12px solid #FF3B3E;color:#FF3B3E;font:900 96px 'D';letter-spacing:8px;transform:rotate(-7deg);background:rgba(8,12,20,.7);box-shadow:0 0 40px rgba(229,56,59,.35)">UNSOLVED</div>
<div style="position:absolute;inset:0;background:radial-gradient(ellipse at center,transparent 55%,rgba(0,0,0,.75) 100%)"></div>
</body></html>"""

# ---------- ep02: robots (title asks the question) -> the lights-out factory
ARM = lambda x, s, c: f"""<g transform="translate({x} 596) scale({s})"><rect x="-70" y="0" width="140" height="40" rx="10" fill="#3A2C22"/><rect x="-30" y="-40" width="60" height="50" rx="10" fill="{c}"/><path d="M0 -30 L-40 -230 L120 -330" stroke="{c}" stroke-width="44" fill="none" stroke-linecap="round" stroke-linejoin="round"/><circle cx="0" cy="-30" r="30" fill="#2A1E16"/><circle cx="-40" cy="-230" r="28" fill="#2A1E16"/><path d="M120 -330 l40 10 m-40 -10 l20 34" stroke="#FFD2B5" stroke-width="16" stroke-linecap="round"/><circle cx="162" cy="-306" r="10" fill="#FFE9A8"/></g>"""
T['ep02'] = f"""<body class="cream">
<div class="h" style="left:80px;top:56px">NO <span class="hl">HUMANS</span></div>
<div class="card" style="left:80px;top:320px;width:1120px;height:690px;background:#0E0B09;overflow:hidden;transform:rotate(-1.2deg);box-shadow:0 50px 100px rgba(60,38,20,.45),0 0 0 10px #2A2119">
 <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 30%,rgba(255,180,90,.18),transparent 60%)"></div>
 <svg viewBox="0 0 1120 690" width="1120" height="690" style="position:absolute;inset:0">
  <rect x="0" y="600" width="1120" height="90" fill="#1E1611"/><rect x="0" y="592" width="1120" height="14" fill="#3A2C22"/>
  <g fill="#F87736"><rect x="400" y="528" width="110" height="64" rx="8"/><rect x="820" y="528" width="110" height="64" rx="8"/></g>
  {ARM(230, 1.35, '#F87736')}{ARM(640, 1.35, '#F87736')}
  <g transform="translate(990 80)"><rect width="96" height="140" rx="16" fill="#2A1E16" stroke="#5A4636" stroke-width="5"/><rect x="28" y="70" width="40" height="50" rx="8" fill="#5A4636"/><text x="48" y="44" text-anchor="middle" font-family="M" font-weight="700" font-size="30" fill="#E0291C">OFF</text></g>
 </svg>
</div>
{maxdiv(1250, 200, 690, "brows:'worried',eyes:'wide',look:[-1,0],mouth:'frown',arms:'chin',extra:['sweat']", flip=True)}
</body></html>"""

# ---------- ep03: AI agents can spend your money -> the receipt
T['ep03'] = f"""<body class="cream">
<div class="h" style="left:80px;top:56px">MY AI <span class="hl">DID THIS</span></div>
<div class="card" style="left:150px;top:300px;width:900px;height:760px;transform:rotate(-4deg);border-radius:20px;padding:56px 70px;font:700 52px 'M';color:#22180F;box-shadow:0 50px 100px rgba(60,38,20,.4)">
 <div style="text-align:center;font:900 60px 'D';letter-spacing:4px">ORDER COMPLETE</div>
 <div style="text-align:center;font:700 34px 'M';color:#8C7462;margin-top:8px">placed by: AI SHOPPING AGENT</div>
 <div style="border-top:6px dashed #CDB6A3;margin:34px 0 26px"></div>
 <div style="display:flex;justify-content:space-between;color:#5A4636"><span>Smart watch x2</span><span>$380.00</span></div>
 <div style="border-top:6px dashed #CDB6A3;margin:26px 0"></div>
 <div style="display:flex;justify-content:space-between;font:900 110px 'D'"><span>TOTAL</span><span>$380</span></div>
 <div style="position:absolute;left:70px;top:560px;padding:6px 30px;border:12px solid #E0291C;color:#E0291C;font:900 78px 'D';white-space:nowrap;transform:rotate(-8deg);border-radius:16px;background:rgba(255,250,247,.85)">NON-REFUNDABLE</div>
</div>
{maxdiv(1180, 190, 720, "brows:'worried',eyes:'closed',mouth:'frown',arms:'facepalm',extra:['sweat']")}
</body></html>"""

# ---------- ep04: 75% code (title has the number) -> the missing first rung
T['ep04'] = f"""<body class="cream">
<div class="h" style="left:80px;top:56px">FIRST RUNG <span class="hl">GONE</span></div>
<svg viewBox="200 0 600 800" width="780" height="1040" style="position:absolute;left:180px;top:250px;filter:drop-shadow(0 40px 40px rgba(60,38,20,.35))">
 <rect x="250" y="0" width="44" height="800" rx="18" fill="#5A3A26"/><rect x="706" y="0" width="44" height="800" rx="18" fill="#5A3A26"/>
 <g font-family="D" font-weight="900" font-size="64" text-anchor="middle" fill="#FFFAF7">
  <rect x="270" y="70" width="460" height="96" rx="20" fill="#2A2018"/><text x="500" y="140">SENIOR</text>
  <rect x="270" y="260" width="460" height="96" rx="20" fill="#2A2018"/><text x="500" y="330">MID-LEVEL</text></g>
 <g transform="translate(0 450)"><path d="M270 0 h90 l-14 26 l20 22 l-18 34 h-78 z" fill="#E0291C"/><path d="M730 0 h-90 l16 24 l-18 26 l16 32 h76 z" fill="#E0291C"/>
  <text x="500" y="66" text-anchor="middle" font-family="D" font-weight="900" font-size="66" fill="#E0291C">JUNIOR</text>
  <g fill="#E0291C"><rect x="400" y="130" width="40" height="22" rx="6" transform="rotate(20 420 140)"/><rect x="540" y="160" width="34" height="20" rx="6" transform="rotate(-25 557 170)"/></g></g>
</svg>
{maxdiv(1240, 200, 700, "brows:'worried',eyes:'worried',look:[-1,1],mouth:'wavy',arms:'down',extra:['sweat']")}
</body></html>"""

# ---------- ep05: ChatGPT doesn't know what it will say -> probability bars
BAR = lambda w, word, pct, top, hi: f"""<div style="display:flex;align-items:center;gap:26px;margin-top:{top}px"><div style="width:250px;font:900 66px 'D';color:#22180F">{word}</div><div style="height:74px;width:{w}px;border-radius:18px;background:{'#F87736' if hi else '#D8C3B1'};box-shadow:{'0 10px 0 #C9521D' if hi else 'none'}"></div><div style="font:900 62px 'D';color:{'#22180F' if hi else '#8C7462'}">{pct}</div></div>"""
T['ep05'] = f"""<body class="cream">
<div class="h" style="left:80px;top:56px">IT'S <span class="hl">GUESSING</span></div>
<div class="card" style="left:90px;top:320px;width:1120px;height:700px;padding:56px 70px;transform:rotate(-1.2deg)">
 <div style="font:700 62px 'B';color:#22180F;line-height:1.2">The capital of India is <span style="display:inline-block;width:8px;height:70px;background:#22180F;vertical-align:-10px"></span></div>
 <div style="font:700 34px 'M';color:#8C7462;margin-top:30px;letter-spacing:3px">NEXT WORD?</div>
 {BAR(480, 'New', '92%', 20, True)}{BAR(90, 'Delhi', '5%', 26, False)}{BAR(30, 'Mumbai', '1%', 26, False)}
</div>
{maxdiv(1250, 190, 700, "brows:'skeptic',eyes:'squint',look:[-1,0],mouth:'smirk',arms:'point'", flip=True)}
</body></html>"""

# ---------- ep06: 10 septillion years (title has the number) -> colder than space
CHAND = """<svg viewBox="0 0 900 900" width="680" height="680" style="position:absolute;left:330px;top:400px;filter:drop-shadow(0 0 60px rgba(120,190,255,.55)) drop-shadow(0 40px 40px rgba(20,40,80,.35))">
 <defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#A86F1E"/><stop offset=".5" stop-color="#FFD77A"/><stop offset="1" stop-color="#A86F1E"/></linearGradient></defs>
 <rect x="430" y="0" width="40" height="120" fill="url(#g)"/>
 <g fill="url(#g)"><rect x="200" y="120" width="500" height="44" rx="14"/><rect x="250" y="330" width="400" height="40" rx="14"/><rect x="300" y="530" width="300" height="38" rx="14"/><rect x="350" y="720" width="200" height="36" rx="14"/></g>
 <g stroke="#E3B15A" stroke-width="10" fill="none"><path d="M260 164 C250 250 300 290 300 330"/><path d="M640 164 C650 250 600 290 600 330"/><path d="M380 164 C380 240 410 290 400 330"/><path d="M520 164 C520 240 490 290 500 330"/><path d="M300 370 C300 450 340 500 340 530"/><path d="M600 370 C600 450 560 500 560 530"/><path d="M450 370 L450 530"/><path d="M380 568 C380 640 400 690 400 720"/><path d="M520 568 C520 640 500 690 500 720"/></g>
 <rect x="410" y="756" width="80" height="60" rx="10" fill="#2A3B55"/>
</svg>"""
T['ep06'] = f"""<body class="cream" style="background:radial-gradient(ellipse at 34% 55%,#EAF4FF 0%,#DCEBFA 35%,#F4EDE3 70%,#E9D7C4 100%)">
<div class="h" style="left:80px;top:56px">COLDER THAN <span class="hl" style="background:#7CC4FF;box-shadow:0 14px 0 #3E8FD6,0 26px 40px rgba(30,60,110,.3)">SPACE</span></div>
{CHAND}
<div style="position:absolute;left:850px;top:760px;padding:10px 30px;background:#12233D;color:#BFE3FF;font:900 92px 'D';border-radius:22px;transform:rotate(4deg);box-shadow:0 20px 40px rgba(18,35,61,.4)">−273°C</div>
{maxdiv(1260, 190, 690, "brows:'worried',eyes:'squint',mouth:'wavy',arms:'hug',extra:['sweat']", extra_style='filter:drop-shadow(0 30px 26px rgba(30,50,90,.35)) hue-rotate(0deg) saturate(.85)')}
</body></html>"""

# ---------- ep07: phone listening (title asks) -> the evidence: 17,000 apps tested
T['ep07'] = f"""<body class="cream">
<div class="h" style="left:80px;top:56px;font-size:170px"><span class="hl">17,000</span> APPS<br>TESTED</div>
<div style="position:absolute;left:560px;top:380px;width:470px;height:900px;border-radius:70px;background:#16110D;box-shadow:0 50px 100px rgba(60,38,20,.45),inset 0 0 0 8px #3A2E24;transform:rotate(6deg)">
 <div style="position:absolute;left:22px;top:22px;right:22px;bottom:22px;border-radius:52px;background:#FFFAF7;overflow:hidden">
  <div style="height:80px;display:flex;align-items:center;justify-content:flex-end;padding:0 34px;gap:14px"><i style="width:34px;height:34px;border-radius:17px;background:#FF8A00;box-shadow:0 0 30px 8px rgba(255,138,0,.8);display:inline-block"></i></div>
  <div style="margin:20px 30px;padding:30px;border-radius:30px;background:#F87736;font:900 58px/1 'D';color:#22180F">RUNNING<br>SHOES<div style="font:900 90px 'D';margin-top:14px">−50%</div></div>
  <svg viewBox="0 0 24 24" width="150" height="150" style="position:absolute;left:140px;top:420px"><path fill="#22180F" d="M12 14a3 3 0 0 0 3-3V5a3 3 0 0 0-6 0v6a3 3 0 0 0 3 3m5.3-3a5.3 5.3 0 0 1-10.6 0H5a7 7 0 0 0 6 6.92V21h2v-3.08A7 7 0 0 0 19 11z"/></svg>
 </div>
</div>
<svg viewBox="0 0 200 300" width="200" height="300" style="position:absolute;left:330px;top:640px"><g stroke="#F87736" stroke-width="16" fill="none" stroke-linecap="round"><path d="M170 90 Q130 150 170 210"/><path d="M120 50 Q60 150 120 250"/><path d="M70 10 Q-10 150 70 290" opacity=".6"/></g></svg>
{maxdiv(1180, 200, 700, "brows:'up',eyes:'open',look:[-1,0],mouth:'rest',arms:'hush'", flip=True)}
</body></html>"""

for k, v in T.items():
    (OUT / f'v2_{k}.html').write_text(HEAD + v)
print('wrote', ', '.join(f'v2_{k}.html' for k in T))
