"""Thumbnails v4 = owner-approved style A1 for all long videos (2026-11-24).
OLD thumbnail texts + props, Montserrat Black, dark-brown text on cream + dots, key words in an orange->red gradient,
sub-line as WHITE text on an orange->red gradient button (never dark text on a flat orange box: adult-site look),
Max small (~440 px) with a reaction that matches the title (different on every thumbnail).
Writes hf/thumbs/v4_<id>.html.  Render: node tools/thumbs_v2_render.cjs v4_<id> ...   Usage: python3 tools/thumbs_v4.py"""
import pathlib, sys
sys.path.insert(0, 'tools')
from kit_assets import icon

OUT = pathlib.Path('hf/thumbs')
MAX = "{skin:'#F0C4A0',hair:'messy',hairCol:'#5A3A26',glasses:'round',hood:'down',top:'#F87736',topS:'#D85E25',phones:'none',beard:'stubble'}"
MAXN = "{skin:'#F0C4A0',hair:'messy',hairCol:'#5A3A26',glasses:'round',hood:'up',top:'#2B2F38',topS:'#1C1F26',inner:'#0D0F13',strings:'#F87736',phones:'none',beard:'stubble'}"
OPENAI = '<path fill="#2A2018" d="M239.184 106.203a64.72 64.72 0 0 0-5.576-53.103C219.452 28.459 191 15.784 163.213 21.74A65.586 65.586 0 0 0 52.096 45.22a64.72 64.72 0 0 0-43.23 31.36c-14.31 24.602-11.061 55.634 8.033 76.74a64.67 64.67 0 0 0 5.525 53.102c14.174 24.65 42.644 37.324 70.446 31.36a64.72 64.72 0 0 0 48.754 21.744c28.481.025 53.714-18.361 62.414-45.481a64.77 64.77 0 0 0 43.229-31.36c14.137-24.558 10.875-55.423-8.083-76.483m-97.56 136.338a48.4 48.4 0 0 1-31.105-11.255l1.535-.87l51.67-29.825a8.6 8.6 0 0 0 4.247-7.367v-72.85l21.845 12.636c.218.111.37.32.409.563v60.367c-.056 26.818-21.783 48.545-48.601 48.601M37.158 197.93a48.35 48.35 0 0 1-5.781-32.589l1.534.921l51.722 29.826a8.34 8.34 0 0 0 8.441 0l63.181-36.425v25.221a.87.87 0 0 1-.358.665l-52.335 30.184c-23.257 13.398-52.97 5.431-66.404-17.803M23.549 85.38a48.5 48.5 0 0 1 25.58-21.333v61.39a8.29 8.29 0 0 0 4.195 7.316l62.874 36.272l-21.845 12.636a.82.82 0 0 1-.767 0L41.353 151.53c-23.211-13.454-31.171-43.144-17.804-66.405zm179.466 41.695l-63.08-36.63L161.73 77.86a.82.82 0 0 1 .768 0l52.233 30.184a48.6 48.6 0 0 1-7.316 87.635v-61.391a8.54 8.54 0 0 0-4.4-7.213m21.742-32.69l-1.535-.922l-51.619-30.081a8.39 8.39 0 0 0-8.492 0L99.98 99.808V74.587a.72.72 0 0 1 .307-.665l52.233-30.133a48.652 48.652 0 0 1 72.236 50.391zM88.061 139.097l-21.845-12.585a.87.87 0 0 1-.41-.614V65.685a48.652 48.652 0 0 1 79.757-37.346l-1.535.87l-51.67 29.825a8.6 8.6 0 0 0-4.246 7.367zm11.868-25.58L128.067 97.3l28.188 16.218v32.434l-28.086 16.218l-28.188-16.218z"/>'
INR = '<svg viewBox="0 0 512 512" width="62" height="62"><mask id="m"><circle cx="256" cy="256" r="256" fill="#fff"/></mask><g mask="url(#m)"><path fill="#eee" d="m0 160l256-32l256 32v192l-256 32L0 352z"/><path fill="#ff9811" d="M0 0h512v160H0Z"/><path fill="#6da544" d="M0 352h512v160H0Z"/><circle cx="256" cy="256" r="72" fill="#0052b4"/><circle cx="256" cy="256" r="48" fill="#eee"/><circle cx="256" cy="256" r="24" fill="#0052b4"/></g></svg>'

HEAD = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'Mont';src:url('fonts/montserrat-latin-900-normal.woff2');font-weight:900}
@font-face{font-family:'Mont';src:url('fonts/montserrat-latin-800-normal.woff2');font-weight:800}
@font-face{font-family:'T';src:url('/ep01-test/assets/fonts/Inter-SemiBold.otf');font-weight:600}
@font-face{font-family:'M';src:url('/ep01-test/assets/fonts/JetBrainsMono-Bold.ttf');font-weight:700}
*{margin:0;box-sizing:border-box} body{width:1920px;height:1080px;position:relative;overflow:hidden;background:radial-gradient(ellipse at 40% 45%,#FBF6F0 0%,#F4EDE3 50%,#E8D8C8 100%)}
body.cr:before{content:'';position:absolute;inset:0;background:radial-gradient(#DCC6B2 2.4px,transparent 2.6px) 0 0/38px 38px;opacity:.6}
.t1{position:absolute;left:76px;top:40px;font:900 150px/1.02 'Mont';color:#2A2018;letter-spacing:-5px}
.t1 b,.g{background:linear-gradient(90deg,#F87736,#E8402E);-webkit-background-clip:text;color:transparent;filter:drop-shadow(0 6px 0 rgba(216,94,37,.2))}
.btn{position:absolute;left:84px;padding:10px 36px 14px;background:linear-gradient(90deg,#F26B2A,#D9381E);color:#fff;font:900 84px 'Mont';border-radius:24px;transform:rotate(-2deg);box-shadow:0 14px 0 #A8301A,0 28px 50px rgba(217,56,30,.35);letter-spacing:-2px;text-shadow:0 3px 0 rgba(120,30,10,.35);white-space:nowrap}
.card{position:absolute;background:#fff;border-radius:30px;box-shadow:0 30px 70px rgba(60,40,25,.25),0 0 0 3px #EADBCC}
.pill{position:absolute;padding:10px 30px;border-radius:22px;font:900 76px 'Mont';box-shadow:0 18px 40px rgba(60,40,25,.25)}
.stamp{position:absolute;padding:6px 28px;border:11px solid #E11D48;color:#E11D48;border-radius:18px;background:rgba(255,255,255,.88);white-space:nowrap;font:900 64px 'Mont'}
.logo{position:absolute;width:170px;height:170px;border-radius:40px;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 20px 40px rgba(30,40,70,.18),0 0 0 3px #E2E6EE}
#max{position:absolute;filter:drop-shadow(0 24px 20px rgba(60,40,25,.3))}
</style><script src="/host/host.js"></script><script src="/host/bit.js"></script></head>"""


def mx(left, top, pose, w=440, char=MAX, flip=False, filt=''):
    st = f'left:{left}px;top:{top}px;' + ('transform:scaleX(-1);' if flip else '') + (f'filter:{filt};' if filt else '')
    return (f'<div id="max" style="{st}"></div><script>document.getElementById("max").innerHTML='
            f'HOST.render({{char:{char},{pose},w:{w},h:{int(w * 1.3)}}});</script>')


def bit(left, top, state, w=260, arms='down', extra='[]', id_='bit'):
    return (f'<div id="{id_}" style="position:absolute;left:{left}px;top:{top}px;filter:drop-shadow(0 20px 18px rgba(60,40,25,.28))"></div>'
            f'<script>document.getElementById("{id_}").innerHTML=BIT.render({{style:"classic",state:"{state}",arms:"{arms}",extra:{extra},w:{w},h:{int(w * .9)}}});</script>')


T = {}

# ep08 "GPT-6 Astra - where is it?" -> Max searching, palms up: "where?!"
T['ep08'] = f"""<body class="cr"><div class="t1" style="font-size:178px;letter-spacing:-6px">GPT-6 <b>ASTRA</b></div><div class="btn" style="top:250px;font-size:96px">WHERE IS IT?</div>
<div class="logo" style="left:1290px;top:60px"><svg viewBox="0 0 256 260" width="120" height="122">{OPENAI}</svg></div>
<div class="card" style="left:80px;top:470px;width:900px;height:520px;overflow:hidden;transform:rotate(-1.5deg);border-radius:32px">
 <div style="height:70px;background:#F3F5F9;display:flex;align-items:center;gap:14px;padding:0 28px;font:600 32px 'T';color:#4A5568"><i style="width:20px;height:20px;border-radius:10px;background:#FF5F57"></i><i style="width:20px;height:20px;border-radius:10px;background:#FEBC2E"></i><i style="width:20px;height:20px;border-radius:10px;background:#28C840"></i>&nbsp;ChatGPT</div>
 <div style="margin:24px 36px 0;padding:22px 28px;border-radius:18px;border:4px solid #CBD5E1;font:600 44px 'T';color:#1A202C;display:flex;align-items:center;gap:20px">{icon('ph:magnifying-glass-bold', 46, '#94A3B8')} Astra<span style="width:5px;height:52px;background:#1A202C;margin-left:-12px"></span></div>
 <div style="margin:24px 36px 0;padding:22px 28px;font:600 44px 'T';color:#1A202C">GPT-6.2 Sol</div>
 <div style="margin:0 36px;padding:22px 28px;font:600 44px 'T';color:#E11D48">No results for "Astra"</div></div>
<div style="position:absolute;left:770px;top:640px"><svg width="96" height="110" viewBox="0 0 28 32"><path d="M2 2 L2 26 L8.5 19.5 L13 30 L17.5 28 L13 18 L22 18 Z" fill="#fff" stroke="#111" stroke-width="2" stroke-linejoin="round"/></svg></div>
<div class="card" style="left:1010px;top:500px;padding:20px 30px;border-radius:26px;display:flex;gap:18px;align-items:center;transform:rotate(4deg);font:900 66px 'Mont';color:#2A2018;box-shadow:0 20px 50px rgba(30,40,70,.22),0 0 0 5px #F87736">{INR} ₹1,999</div>
<div class="stamp" style="left:940px;top:780px;transform:rotate(-8deg)">FREE? SCAM</div>
{mx(1480, 440, "brows:'up',eyes:'open',look:[-1,0],mouth:'O',arms:'shrug',extra:['question']")}</body></html>"""

# ep02 "Will robots take your job? The real data" -> Max nervous, hugging himself, sweating
ARM = """<svg style="position:absolute;left:770px;top:440px" width="520" height="560" viewBox="0 0 520 560"><rect x="40" y="480" width="200" height="70" rx="18" fill="#2A2018"/>
<g transform="rotate(-12 140 480)"><rect x="112" y="200" width="56" height="290" rx="28" fill="#E98F5E"/><circle cx="140" cy="200" r="40" fill="#2A2018"/><circle cx="140" cy="200" r="15" fill="#FFE08A"/>
<g transform="rotate(-20 140 200)"><rect x="140" y="176" width="280" height="48" rx="24" fill="#F87736"/><path d="M416 168 l46 -26 M416 232 l46 26" stroke="#F87736" stroke-width="20" stroke-linecap="round"/></g></g></svg>"""
T['ep02'] = f"""<body class="cr"><div class="t1">WILL ROBOTS<br><b>TAKE YOUR</b> JOB?</div><div class="btn" style="top:370px">THE REAL DATA</div>
<div class="pill" style="left:90px;top:640px;background:#E11D48;color:#fff;transform:rotate(-3deg)">92M OUT</div>
<div class="pill" style="left:150px;top:770px;background:#16A34A;color:#fff;transform:rotate(2deg)">170M IN</div>
<div style="position:absolute;left:100px;top:905px;font:800 34px 'Mont';color:#6B5444;letter-spacing:1px">JOBS BY 2030 · WEF</div>
{ARM}{bit(1170, 690, 'worried', extra='["alert"]')}
{mx(1490, 440, "brows:'worried',eyes:'worried',look:[-1,0],mouth:'wavy',arms:'hug',extra:['sweat']")}</body></html>"""

# ep03 "AI can now spend your money - what could go wrong?" -> Max shocked, hands up
T['ep03'] = f"""<body class="cr"><div class="t1" style="font-size:136px">AI CAN NOW<br><b>SPEND YOUR</b><br>MONEY</div><div class="btn" style="top:470px;font-size:76px">WHAT COULD GO WRONG?</div>
<div style="position:absolute;left:100px;top:660px;width:520px;height:320px;border-radius:30px;background:linear-gradient(135deg,#F87736,#D9381E);transform:rotate(-6deg);box-shadow:0 30px 60px rgba(217,56,30,.35);padding:40px 44px;color:#fff">
 <div style="width:90px;height:66px;border-radius:12px;background:linear-gradient(135deg,#FFE7A8,#E5B54A)"></div>
 <div style="font:900 64px 'Mont';margin-top:44px;letter-spacing:2px">•••• 4821</div><div style="font:800 32px 'Mont';margin-top:8px;opacity:.9">YOUR CARD</div></div>
<div class="card" style="left:690px;top:760px;padding:26px 36px;transform:rotate(3deg);border-radius:26px;box-shadow:0 24px 60px rgba(60,40,25,.3),0 0 0 4px #16A34A">
 <div style="font:800 40px 'Mont';color:#16A34A">✓ Payment approved</div><div style="font:900 64px 'Mont';color:#2A2018;margin-top:6px">$380.00 <span style="font:800 34px 'Mont';color:#E11D48">non-refundable</span></div></div>
{bit(1120, 110, 'hijack', w=280, extra='["alert"]')}
{mx(1490, 430, "brows:'high',eyes:'wide',mouth:'shock',arms:'hands-up',extra:['bang']")}</body></html>"""

# ep04 "75% of Google's new code is written by AI - are coders done?" -> Max facepalm (despair)
T['ep04'] = f"""<body class="cr"><div class="t1 g" style="font-size:300px;letter-spacing:-12px;top:10px;line-height:1">75%</div>
<div class="t1" style="top:330px;font-size:92px;letter-spacing:-3px;line-height:1.05">OF GOOGLE'S NEW CODE<br>IS WRITTEN BY AI</div><div class="btn" style="top:560px">ARE CODERS DONE?</div>
<div style="position:absolute;left:90px;top:760px;width:760px;padding:30px 40px;border-radius:26px;background:#1E293B;box-shadow:0 30px 60px rgba(30,41,59,.35);transform:rotate(-2deg);font:700 40px/1.5 'M';color:#E2E8F0">
 <span style="color:#60A5FA">✦ AI:</span> <span style="color:#C084FC">def</span> <span style="color:#FCD34D">checkout</span>(cart):<br>&nbsp;&nbsp;total = <span style="color:#FCD34D">sum</span>(cart)<br>&nbsp;&nbsp;<span style="color:#C084FC">return</span> total</div>
{bit(1050, 660, 'happy', w=280, arms='type')}
{mx(1490, 440, "brows:'worried',eyes:'closed',mouth:'frown',arms:'facepalm',extra:['sweat']")}</body></html>"""

# ep05 "ChatGPT is guessing every word - so how is it so smart?" -> Max skeptical, hand on chin
T['ep05'] = f"""<body class="cr"><div class="t1" style="font-size:140px">CHATGPT<br>IS <b>GUESSING</b><br>EVERY WORD</div><div class="btn" style="top:480px;font-size:76px">SO HOW IS IT SO SMART?</div>
<div class="card" style="left:90px;top:670px;width:1080px;padding:34px 44px;transform:rotate(-1.5deg)">
 <div style="font:600 46px 'T';color:#1A202C">The capital of India is <span style="background:#FDE2D3;border-radius:10px;padding:0 10px">New</span><span style="display:inline-block;width:5px;height:50px;background:#1A202C;vertical-align:-8px;margin-left:6px"></span></div>
 <div style="display:flex;gap:18px;margin-top:26px;font:800 40px 'Mont'"><span style="padding:8px 22px;border-radius:16px;background:linear-gradient(90deg,#F26B2A,#D9381E);color:#fff">New 92%</span><span style="padding:8px 22px;border-radius:16px;background:#EFE6DD;color:#6B5444">Delhi 5%</span><span style="padding:8px 22px;border-radius:16px;background:#EFE6DD;color:#6B5444">Mumbai 1%</span></div></div>
<div class="logo" style="left:1250px;top:520px;width:150px;height:150px"><svg viewBox="0 0 256 260" width="100" height="102">{OPENAI}</svg></div>
{mx(1490, 440, "brows:'skeptic',eyes:'squint',look:[-1,0],mouth:'smirk',arms:'chin',extra:['question']")}</body></html>"""

# ep06 "10 septillion years in 5 minutes?" -> Max mind-blown, amazed
CAL = ''.join(f'<div style="width:230px;height:84px;margin-top:-8px;border-radius:14px;background:#fff;box-shadow:0 8px 0 #E0CFC0;display:flex;align-items:center;justify-content:center;font:900 60px Mont;color:#2A2018">∞</div>' for _ in range(5))
T['ep06'] = f"""<body class="cr"><div class="t1" style="font-size:150px"><b>10 SEPTILLION</b><br>YEARS</div><div class="btn" style="top:370px;font-size:100px">IN 5 MINUTES?</div>
<div style="position:absolute;left:110px;top:640px;width:300px;height:300px;border-radius:40px;background:#1E293B;box-shadow:0 30px 60px rgba(30,41,59,.35);transform:rotate(-5deg)">
 <div style="position:absolute;inset:40px;border-radius:24px;background:linear-gradient(135deg,#F87736,#D9381E);display:flex;align-items:center;justify-content:center;font:900 130px 'Mont';color:#fff">Q</div>
 {''.join(f'<i style="position:absolute;left:{40 + i * 48}px;top:-22px;width:22px;height:30px;border-radius:6px;background:#E5B54A"></i><i style="position:absolute;left:{40 + i * 48}px;bottom:-22px;width:22px;height:30px;border-radius:6px;background:#E5B54A"></i>' for i in range(5))}</div>
<div style="position:absolute;left:520px;top:680px;width:250px;height:250px;border-radius:50%;background:#fff;border:16px solid #2A2018;box-shadow:0 30px 60px rgba(42,32,24,.3)"><i style="position:absolute;left:101px;top:30px;width:16px;height:90px;border-radius:8px;background:#2A2018"></i><i style="position:absolute;left:105px;top:105px;width:80px;height:16px;border-radius:8px;background:#E8402E;transform:rotate(30deg);transform-origin:4px 8px"></i></div>
<div style="position:absolute;left:860px;top:560px;transform:rotate(5deg)">{CAL}<div style="font:800 34px 'Mont';color:#6B5444;text-align:center;margin-top:18px">SUPERCOMPUTER</div></div>
{mx(1480, 430, "brows:'high',eyes:'wide',mouth:'A',arms:'hands-up',extra:['spark']")}</body></html>"""

# ep07 "Is your phone listening?" -> Max suspicious, squinting at his phone
T['ep07'] = f"""<body class="cr"><div class="t1" style="font-size:150px">IS YOUR PHONE</div><div class="btn" style="top:230px;font-size:130px;padding:10px 44px 18px">LISTENING?</div>
<div style="position:absolute;left:120px;top:560px;width:250px;height:250px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 24px 50px rgba(60,40,25,.25),0 0 0 6px #F87736">{icon('ph:ear-bold', 150, '#E8402E')}</div>
<div style="position:absolute;left:480px;top:470px;width:400px;height:760px;border-radius:60px;background:#3A3F4A;transform:rotate(-5deg);box-shadow:0 40px 80px rgba(42,32,24,.4)">
 <div style="position:absolute;inset:18px;border-radius:44px;background:#FFFAF7;padding:70px 30px 0">
  <i style="position:absolute;right:40px;top:30px;width:26px;height:26px;border-radius:13px;background:#F87736;box-shadow:0 0 22px 6px rgba(248,119,54,.7)"></i>
  <div style="display:flex;justify-content:center">{icon('logos:instagram-icon', 100)}</div>
  <div style="margin-top:30px;padding:18px;border-radius:20px;background:linear-gradient(90deg,#F26B2A,#D9381E);color:#fff;font:900 44px 'Mont';text-align:center;white-space:nowrap">AD: SHOES</div>
  <div style="margin-top:20px;padding:18px;border-radius:20px;background:linear-gradient(90deg,#F26B2A,#D9381E);color:#fff;font:900 44px 'Mont';text-align:center;white-space:nowrap">AD: SHOES</div></div></div>
<div style="position:absolute;left:960px;top:640px;width:230px;height:230px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 24px 50px rgba(60,40,25,.25)">{icon('mdi:shoe-sneaker', 150, '#E8402E')}</div>
{mx(1480, 440, "brows:'skeptic',eyes:'squint',look:[1,0],mouth:'frown',arms:'phone',extra:['question']")}</body></html>"""

# myst01 (Tech Mysteries look: navy, grain, red) "Who hijacked this TV? Unsolved, Chicago 1987" -> Max in night hoodie, scared
T['myst01'] = f"""<body style="background:radial-gradient(ellipse at 35% 50%,#1A2438 0%,#0A0F1A 55%,#020305 100%)">
<div style="position:absolute;left:56px;top:40px;display:flex;gap:16px;align-items:center;font:700 32px 'M';letter-spacing:8px;color:#AEB9CC"><i style="width:22px;height:22px;border-radius:11px;background:#E5383B;box-shadow:0 0 24px #E5383B;display:inline-block"></i>TECH MYSTERIES · CASE 001</div>
<div style="position:absolute;left:40px;top:150px;width:1000px;height:800px;border-radius:72px;background:linear-gradient(160deg,#4A3A2C,#1C1611);box-shadow:0 70px 140px rgba(0,0,0,.9),inset 0 0 0 12px #2E241B;transform:rotate(-3deg)">
 <div style="position:absolute;left:64px;top:64px;width:760px;height:620px;border-radius:84px/64px;overflow:hidden;background:repeating-linear-gradient(90deg,#16181D 0 28px,#6C7280 28px 40px,#262A33 40px 70px,#3B404B 70px 82px)">
  <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(255,40,80,.32),rgba(40,255,230,.22),rgba(255,40,80,.2));mix-blend-mode:screen"></div>
  <svg viewBox="0 0 760 620" width="760" height="620" style="position:absolute;inset:0"><defs><radialGradient id="r" cx=".5" cy=".4" r=".6"><stop offset="0" stop-color="#2A2A2A"/><stop offset="1" stop-color="#040404"/></radialGradient></defs>
   <ellipse cx="380" cy="270" rx="150" ry="185" fill="url(#r)"/><path d="M130 620 Q150 430 380 410 Q610 430 630 620 Z" fill="#050505"/><rect x="280" y="225" width="200" height="40" rx="14" fill="#0B0B0B" stroke="#3A3A3A" stroke-width="4"/></svg>
  <div style="position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,.35) 0 3px,transparent 3px 6px);box-shadow:inset 0 0 120px rgba(0,0,0,.95)"></div></div>
 <div style="position:absolute;right:44px;top:150px"><i style="display:block;width:86px;height:86px;border-radius:43px;background:#0E0B09;margin-bottom:46px;box-shadow:inset 0 0 0 8px #3A2E24"></i><i style="display:block;width:86px;height:86px;border-radius:43px;background:#0E0B09;box-shadow:inset 0 0 0 8px #3A2E24"></i></div></div>
<div style="position:absolute;left:1080px;top:110px;font:900 136px/1 'Mont';color:#EEF2F8;letter-spacing:-4px;text-shadow:0 10px 40px rgba(0,0,0,.8)">WHO<br>HIJACKED<br><span style="color:#FF3B3E;text-shadow:0 0 40px rgba(229,56,59,.55)">THIS TV?</span></div>
<div style="position:absolute;left:1090px;top:560px;padding:6px 30px;border:11px solid #FF3B3E;color:#FF3B3E;font:900 86px 'Mont';letter-spacing:6px;transform:rotate(-7deg);background:rgba(8,12,20,.7)">UNSOLVED</div>
<div style="position:absolute;left:1100px;top:770px;font:700 40px 'M';color:#8FA3C2;letter-spacing:8px">CHICAGO · 1987</div>
{mx(1540, 700, "brows:'worried',eyes:'wide',look:[-1,0],mouth:'wavy'", w=330, char=MAXN, filt='brightness(.85) drop-shadow(-10px -4px 14px rgba(170,200,255,.45))')}
<div style="position:absolute;inset:0;background:radial-gradient(ellipse at center,transparent 55%,rgba(0,0,0,.7) 100%);pointer-events:none"></div></body></html>"""

for k, v in T.items():
    (OUT / f'v4_{k}.html').write_text(HEAD + v)
print('wrote', ' '.join(f'v4_{k}' for k in T))
