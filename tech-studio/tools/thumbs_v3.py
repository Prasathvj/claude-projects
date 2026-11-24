"""Thumbnails v3 (owner 2026-11-24): keep the OLD thumbnail content and texts (owner found them more curious),
Max SMALLER, new fonts, and NO black-text-on-orange / orange-on-black text (owner: reads like an adult-site logo).
Orange stays only on Max's hoodie. Demo: 3 styles for ep08 -> hf/thumbs/v3_ep08_<a|b|c>.html.
Render: node tools/thumbs_v2_render.cjs v3... (same renderer; pass ids like v3x) -- see thumbs_v3_render below."""
import pathlib

OUT = pathlib.Path('hf/thumbs')
MAX = "{skin:'#F0C4A0',hair:'messy',hairCol:'#5A3A26',glasses:'round',hood:'down',top:'#F87736',topS:'#D85E25',phones:'none',beard:'stubble'}"
OPENAI = '<path fill="#0B1B3F" d="M239.184 106.203a64.72 64.72 0 0 0-5.576-53.103C219.452 28.459 191 15.784 163.213 21.74A65.586 65.586 0 0 0 52.096 45.22a64.72 64.72 0 0 0-43.23 31.36c-14.31 24.602-11.061 55.634 8.033 76.74a64.67 64.67 0 0 0 5.525 53.102c14.174 24.65 42.644 37.324 70.446 31.36a64.72 64.72 0 0 0 48.754 21.744c28.481.025 53.714-18.361 62.414-45.481a64.77 64.77 0 0 0 43.229-31.36c14.137-24.558 10.875-55.423-8.083-76.483m-97.56 136.338a48.4 48.4 0 0 1-31.105-11.255l1.535-.87l51.67-29.825a8.6 8.6 0 0 0 4.247-7.367v-72.85l21.845 12.636c.218.111.37.32.409.563v60.367c-.056 26.818-21.783 48.545-48.601 48.601M37.158 197.93a48.35 48.35 0 0 1-5.781-32.589l1.534.921l51.722 29.826a8.34 8.34 0 0 0 8.441 0l63.181-36.425v25.221a.87.87 0 0 1-.358.665l-52.335 30.184c-23.257 13.398-52.97 5.431-66.404-17.803M23.549 85.38a48.5 48.5 0 0 1 25.58-21.333v61.39a8.29 8.29 0 0 0 4.195 7.316l62.874 36.272l-21.845 12.636a.82.82 0 0 1-.767 0L41.353 151.53c-23.211-13.454-31.171-43.144-17.804-66.405zm179.466 41.695l-63.08-36.63L161.73 77.86a.82.82 0 0 1 .768 0l52.233 30.184a48.6 48.6 0 0 1-7.316 87.635v-61.391a8.54 8.54 0 0 0-4.4-7.213m21.742-32.69l-1.535-.922l-51.619-30.081a8.39 8.39 0 0 0-8.492 0L99.98 99.808V74.587a.72.72 0 0 1 .307-.665l52.233-30.133a48.652 48.652 0 0 1 72.236 50.391zM88.061 139.097l-21.845-12.585a.87.87 0 0 1-.41-.614V65.685a48.652 48.652 0 0 1 79.757-37.346l-1.535.87l-51.67 29.825a8.6 8.6 0 0 0-4.246 7.367zm11.868-25.58L128.067 97.3l28.188 16.218v32.434l-28.086 16.218l-28.188-16.218z"/>'
INR = '<svg viewBox="0 0 512 512" width="62" height="62"><mask id="m"><circle cx="256" cy="256" r="256" fill="#fff"/></mask><g mask="url(#m)"><path fill="#eee" d="m0 160l256-32l256 32v192l-256 32L0 352z"/><path fill="#ff9811" d="M0 0h512v160H0Z"/><path fill="#6da544" d="M0 352h512v160H0Z"/><circle cx="256" cy="256" r="72" fill="#0052b4"/><circle cx="256" cy="256" r="48" fill="#eee"/><circle cx="256" cy="256" r="24" fill="#0052b4"/></g></svg>'

HEAD = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'Anton';src:url('fonts/anton-latin-400-normal.woff2')}
@font-face{font-family:'Bebas';src:url('fonts/bebas-neue-latin-400-normal.woff2')}
@font-face{font-family:'Mont';src:url('fonts/montserrat-latin-900-normal.woff2');font-weight:900}
@font-face{font-family:'Mont';src:url('fonts/montserrat-latin-800-normal.woff2');font-weight:800}
@font-face{font-family:'Pop';src:url('fonts/poppins-latin-900-normal.woff2');font-weight:900}
@font-face{font-family:'Brico';src:url('fonts/bricolage-grotesque-latin-800-normal.woff2');font-weight:800}
@font-face{font-family:'Caveat';src:url('/ep08-long/assets/fonts/Caveat-700-latin.woff2');font-weight:700}
@font-face{font-family:'T';src:url('/ep01-test/assets/fonts/Inter-SemiBold.otf');font-weight:600}
*{margin:0;box-sizing:border-box} body{width:1920px;height:1080px;position:relative;overflow:hidden;background:radial-gradient(ellipse at 40% 45%,#FBF6F0 0%,#F4EDE3 50%,#E8D8C8 100%)}
body:before{content:'';position:absolute;inset:0;background:radial-gradient(#DCC6B2 2.4px,transparent 2.6px) 0 0/38px 38px;opacity:.6}
.win{position:absolute;left:80px;top:470px;width:900px;height:520px;background:#FFFFFF;border-radius:32px;box-shadow:0 40px 90px rgba(30,40,70,.25),0 0 0 3px #E2E6EE;overflow:hidden;transform:rotate(-1.5deg)}
.bar{height:70px;background:#F3F5F9;display:flex;align-items:center;gap:14px;padding:0 28px;font:600 32px 'T';color:#4A5568}.bar i{width:20px;height:20px;border-radius:10px;display:inline-block}
.row{margin:24px 36px 0;padding:22px 28px;border-radius:18px;font:600 44px 'T';color:#1A202C;display:flex;align-items:center;gap:20px}
.q{border:4px solid #CBD5E1}.no{color:#E11D48}
.logo{position:absolute;width:170px;height:170px;border-radius:40px;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 20px 40px rgba(30,40,70,.18),0 0 0 3px #E2E6EE}
.price{position:absolute;left:1010px;top:500px;padding:20px 30px;background:#fff;border-radius:26px;display:flex;gap:18px;align-items:center;transform:rotate(4deg);box-shadow:0 20px 50px rgba(30,40,70,.22)}
.stamp{position:absolute;left:940px;top:780px;padding:6px 28px;border:11px solid #E11D48;color:#E11D48;border-radius:18px;transform:rotate(-8deg);background:rgba(255,255,255,.85);white-space:nowrap}
#max{position:absolute;left:1490px;top:430px;filter:drop-shadow(0 24px 20px rgba(30,40,70,.3))}
</style><script src="/host/host.js"></script></head><body>"""

WIN = """<div class="win"><div class="bar"><i style="background:#FF5F57"></i><i style="background:#FEBC2E"></i><i style="background:#28C840"></i>&nbsp;ChatGPT</div>
<div class="row q"><svg viewBox="0 0 256 256" width="46" height="46"><path fill="#94A3B8" d="M232.49 215.51L185 168a92.12 92.12 0 1 0-17 17l47.53 47.54a12 12 0 0 0 17-17ZM44 112a68 68 0 1 1 68 68a68.07 68.07 0 0 1-68-68"/></svg> Astra<span style="width:5px;height:52px;background:#1A202C;margin-left:-12px"></span></div>
<div class="row">GPT-6.2 Sol</div><div class="row no">No results for "Astra"</div></div>
<div style="position:absolute;left:770px;top:640px"><svg width="96" height="110" viewBox="0 0 28 32"><path d="M2 2 L2 26 L8.5 19.5 L13 30 L17.5 28 L13 18 L22 18 Z" fill="#fff" stroke="#111" stroke-width="2" stroke-linejoin="round"/></svg></div>"""

MAXJS = f"""<div id="max"></div><script>document.getElementById('max').innerHTML=HOST.render({{char:{MAX},brows:'high',eyes:'wide',mouth:'shock',arms:'hands-up',extra:['q'],w:440,h:572}});</script>"""

V = {}
# A: Montserrat Black, navy + electric-blue gradient, white-on-blue pill
V['a'] = """<style>
.t1{position:absolute;left:76px;top:40px;font:900 178px/1 'Mont';color:#0B1B3F;letter-spacing:-6px}
.t1 b{background:linear-gradient(90deg,#2563EB,#7C3AED);-webkit-background-clip:text;color:transparent;filter:drop-shadow(0 6px 0 rgba(37,99,235,.18))}
.t2{position:absolute;left:84px;top:250px;padding:12px 36px;background:linear-gradient(90deg,#2563EB,#4F46E5);color:#fff;font:900 96px 'Mont';border-radius:24px;transform:rotate(-2deg);box-shadow:0 14px 0 #1E3A8A,0 28px 50px rgba(37,99,235,.35);letter-spacing:-2px}
.price{font:900 66px 'Mont';color:#0B1B3F;border:5px solid #2563EB}.stamp{font:900 64px 'Mont'}
</style><div class="t1">GPT-6 <b>ASTRA</b></div><div class="t2">WHERE IS IT?</div>
<div class="logo" style="left:1290px;top:60px">""" + f'<svg viewBox="0 0 256 260" width="120" height="122">{OPENAI}</svg></div>'
# B: Anton condensed, white with heavy navy outline + yellow keyword, red banner
V['b'] = """<style>
.t1{position:absolute;left:70px;top:20px;font:400 230px/1 'Anton';color:#fff;letter-spacing:2px;-webkit-text-stroke:16px #0B1B3F;paint-order:stroke fill;text-shadow:12px 12px 0 #0B1B3F}
.t1 b{color:#FFD23F;font-weight:400}
.t2{position:absolute;left:80px;top:290px;padding:6px 40px 10px;background:#E11D48;color:#fff;font:400 120px/1.05 'Anton';letter-spacing:3px;transform:rotate(-3deg);box-shadow:10px 10px 0 #0B1B3F}
.price{font:400 78px 'Anton';color:#0B1B3F;border:6px solid #0B1B3F;letter-spacing:1px}.stamp{font:400 80px 'Anton';letter-spacing:3px}
</style><div class="t1">GPT-6 <b>ASTRA</b></div><div class="t2">WHERE IS IT?</div>
<div class="logo" style="left:1210px;top:70px">""" + f'<svg viewBox="0 0 256 260" width="120" height="122">{OPENAI}</svg></div>'
# C: Bricolage Grotesque, deep teal + yellow highlighter swipe, handwritten red note with arrow
V['c'] = """<style>
.t1{position:absolute;left:78px;top:38px;font:800 190px/1 'Brico';color:#0F2E3D;letter-spacing:-6px}
.t1 b{position:relative;color:#0F2E3D;z-index:1}.t1 b:before{content:'';position:absolute;left:-14px;right:-18px;top:52%;height:46%;background:#5EEAD4;z-index:-1;transform:rotate(-2deg);border-radius:10px 30px 12px 26px}
.t2{position:absolute;left:96px;top:248px;font:700 150px/1 'Caveat';color:#E11D48;transform:rotate(-4deg)}
.price{font:800 70px 'Brico';color:#0F2E3D;border:5px solid #0EA5A4}.stamp{font:800 66px 'Brico'}
</style><div class="t1">GPT-6 <b>ASTRA</b></div><div class="t2">where is it?!</div>
<svg viewBox="0 0 300 200" width="300" height="200" style="position:absolute;left:640px;top:270px"><path d="M20 30 C120 10 220 60 240 170" stroke="#E11D48" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M200 140 L242 176 L262 124" stroke="#E11D48" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
<div class="logo" style="left:1300px;top:56px">""" + f'<svg viewBox="0 0 256 260" width="120" height="122">{OPENAI}</svg></div>'

# A in channel colours (owner pick A, 2026-11-24). Brown #2A2018 text on cream (no dark boxes), orange only as a
# warm orange->red gradient (never a flat orange box with dark text = the adult-site look).
LOGO = """<div class="logo" style="left:1290px;top:60px"><svg viewBox="0 0 256 260" width="120" height="122">""" + OPENAI.replace('#0B1B3F', '#2A2018') + "</svg></div>"
V['a1'] = """<style>
.t1{position:absolute;left:76px;top:40px;font:900 178px/1 'Mont';color:#2A2018;letter-spacing:-6px}
.t1 b{background:linear-gradient(90deg,#F87736,#E8402E);-webkit-background-clip:text;color:transparent;filter:drop-shadow(0 6px 0 rgba(216,94,37,.2))}
.t2{position:absolute;left:84px;top:250px;padding:12px 38px;background:linear-gradient(90deg,#F26B2A,#D9381E);color:#fff;font:900 96px 'Mont';border-radius:24px;transform:rotate(-2deg);box-shadow:0 14px 0 #A8301A,0 28px 50px rgba(217,56,30,.35);letter-spacing:-2px;text-shadow:0 3px 0 rgba(120,30,10,.35)}
.price{font:900 66px 'Mont';color:#2A2018;border:5px solid #F87736}.stamp{font:900 64px 'Mont'}
</style><div class="t1">GPT-6 <b>ASTRA</b></div><div class="t2">WHERE IS IT?</div>""" + LOGO
V['a2'] = """<style>
.t1{position:absolute;left:76px;top:40px;font:900 178px/1 'Mont';color:#2A2018;letter-spacing:-6px}
.t1 b{background:linear-gradient(90deg,#F87736,#E8402E);-webkit-background-clip:text;color:transparent;filter:drop-shadow(0 6px 0 rgba(216,94,37,.2))}
.t2{position:absolute;left:84px;top:250px;padding:10px 36px;background:#FFFAF7;color:#2A2018;font:900 96px 'Mont';border-radius:24px;border:7px solid #F87736;transform:rotate(-2deg);box-shadow:0 14px 0 #F87736,0 28px 50px rgba(216,94,37,.28);letter-spacing:-2px}
.price{font:900 66px 'Mont';color:#2A2018;border:5px solid #F87736}.stamp{font:900 64px 'Mont'}
</style><div class="t1">GPT-6 <b>ASTRA</b></div><div class="t2">WHERE IS IT?</div>""" + LOGO

for k, css in V.items():
    body = css + WIN + f'<div class="price">{INR} ₹1,999</div><div class="stamp">FREE? SCAM</div>' + MAXJS + '</body></html>'
    (OUT / f'v3_ep08_{k}.html').write_text(HEAD + body)
print('wrote v3_ep08_a/b/c')
