"""Tamil version of the knight01 Halftone Dossier Short (tamil01, 2026-11-24 test for a Tamil channel).
Reuses hf/knight01-dossier/index.html unchanged: the page keeps running on the ENGLISH timeline; every Tamil frame time
is mapped into English time with a piecewise-linear warp anchored on line starts/ends and scene cuts, and each visual cue
(Wt name) is re-pointed at the matching Tamil word. Captions are the Tamil words (times mapped into English time).
On-screen headings are translated; Tamil glyphs come from Tamil fonts merged into the same families by unicode-range.
Usage: python3 tools/build_dossier_ta.py  (env STILLS=t1,t2 for Tamil-time stills)"""
import json, os, re, subprocess, sys, wave
from pathlib import Path
import numpy as np

D = Path('hf/knight01-dossier')
EN = json.load(open('src/episodes/knight01-short.timeline.json'))
TA = json.load(open('src/episodes/tamil01-short.timeline.json'))
DUR_EN, DUR_TA = 69.8, TA['duration']
norm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
wen = [{'w': w['w'], 'n': norm(w['w']), 's': round(b['start'] + w['s'], 3), 'e': round(b['start'] + w['e'], 3)} for b in EN['beats'] for w in b['words']]
WtEN = lambda n, i=0: [w for w in wen if w['n'].startswith(n)][i]['s']
tw = lambda b, i: TA['beats'][b]['start'] + TA['beats'][b]['words'][i]['s']

# ---- warp anchors: (english time, tamil time)
A = [(0, 0)]
for be, bt in zip(EN['beats'], TA['beats']):
    A += [(be['start'], bt['start']), (be['start'] + be['vo'], bt['start'] + bt['vo'])]
A += [(2.02, tw(0, 3) - .05), (6.22, tw(0, 9) - .08), (7.27, tw(0, 11) - .06), (11.07, tw(1, 3) - .08), (14.22, tw(1, 10) - .1),
      (40.42, tw(6, 4) - .05), (51.55, tw(8, 5) - .08), (DUR_EN, DUR_TA)]
A = sorted(A)
assert all(b[1] > a[1] for a, b in zip(A, A[1:]) if b[0] > a[0]), A
AE, AT = np.array([a[0] for a in A]), np.array([a[1] for a in A])
warp = lambda te: float(np.interp(te, AE, AT))
unwarp = lambda tt: float(np.interp(tt, AT, AE))

# ---- cue map: english Wt(name, nth) -> tamil (beat, word)
CUE = {('in', 0): (0, 0), ('45', 0): (0, 1), ('minutes', 0): (0, 2), ('company', 0): (0, 4), ('460', 0): (0, 5), ('dollars', 0): (0, 7),
       ('lost', 0): (0, 8), ('no', 0): (0, 9), ('hacker', 0): (0, 9), ('one', 0): (0, 11), ('step', 0): (0, 13), ('missed', 0): (0, 14),
       ('august', 0): (1, 0), ('1st', 0): (1, 1), ('2012', 0): (1, 2), ('biggest', 0): (1, 4), ('knight', 0): (1, 8), ('capital', 0): (1, 9), ('updating', 0): (1, 13),
       ('eight', 0): (2, 0), ('code', 0): (2, 3), ('reaches', 0): (2, 4), ('only', 0): (2, 6), ('seven', 0): (2, 8),
       ('eighth', 0): (3, 0), ('old', 0): (3, 3), ('2003', 0): (3, 7), ('switched', 0): (3, 9), ('power', 0): (3, 12),
       ('old', 1): (4, 3), ('switch', 1): (4, 4), ('reuses', 0): (4, 6),
       ('801', 0): (5, 1), ('am', 1): (5, 1), ('sends', 0): (5, 2), ('97', 0): (5, 3), ('warning', 0): (5, 5), ('nobody', 0): (5, 7),
       ('930', 0): (6, 0), ('market', 0): (6, 1), ('opens', 0): (6, 2), ('power', 1): (6, 4), ('wakes', 0): (6, 6),
       ('orders', 0): (7, 1), ('154', 0): (7, 3), ('four', 0): (7, 5), ('trades', 0): (7, 7),
       ('45', 1): (8, 0), ('stop', 0): (8, 4), ('460', 1): (8, 5), ('dollars', 1): (8, 7), ('inr', 0): (8, 10), ('gone', 0): (8, 14),
       ('400', 0): (9, 4), ('rescue', 0): (9, 7), ('within', 1): (9, 9), ('rival', 0): (9, 12), ('takes', 0): (9, 14), ('over', 1): (9, 15),
       ('lesson', 0): (10, 0), ('delete', 0): (10, 5), ('dead', 0): (10, 6), ('alone', 0): (10, 7),
       ('subscribe', 0): (11, 0), ('techdecoded', 0): (11, 4), ('more', 0): (11, 6)}
OVR = {f'{n}|{i}': round(unwarp(tw(*bw)), 3) for (n, i), bw in CUE.items()}
Wt = lambda n, i=0: OVR.get(f'{n}|{i}', WtEN(n, i) if n != 'inr' else 0)   # english-time cue, re-pointed at Tamil words

# ---- Tamil caption chunks (in english time)
words, chunks = [], []
for b in TA['beats']:
    ws = [{'w': w['w'], 's': b['start'] + w['s'], 'e': b['start'] + w['e']} for w in b['words']]
    cur = []
    for w in ws:
        cur.append(w)
        if re.search(r'[.,:?!]$', w['w']) or len(cur) >= 2 or sum(len(x['w']) + 1 for x in cur) >= 15:
            chunks.append(cur); cur = []
    if cur: chunks.append(cur)
CH = []
for k, ch in enumerate(chunks):
    t0 = ch[0]['s'] - .05
    t1 = chunks[k + 1][0]['s'] - .05 if k + 1 < len(chunks) else DUR_TA
    if k + 1 < len(chunks) and chunks[k + 1][0]['s'] - ch[-1]['e'] > 1.2: t1 = ch[-1]['e'] + 1.2
    CH.append({'t0': round(unwarp(t0), 3), 't1': round(unwarp(t1), 3), 'w': [{'w': w['w'], 's': round(unwarp(w['s']), 3), 'e': round(unwarp(w['e']), 3)} for w in ch]})

# ---- shakes / flashes / sfx: the english lists, evaluated with the re-pointed cues (english time)
src = Path('tools/build_dossier.py').read_text()
ns = {'Wt': Wt, 'DUR': DUR_EN}
exec(src[src.index('SH = ['):src.index('html = (D')], ns)
exec(src[src.index('# ---- SFX plan'):src.index('SR = 48000')], ns)
SH, FL, SFX = ns['SH'], ns['FL'], ns['SFX']
SH += [[Wt('inr') + .05, 12, .25]]; SFX += [('stamp', Wt('inr') + .05, .7)]

# ---- page
html = (D / 'index.html').read_text()
html = html.replace('__WORDS__', json.dumps(wen)).replace('__CHUNKS__', json.dumps(CH, ensure_ascii=False)).replace('__SHAKES__', json.dumps(SH)).replace('__FLASHES__', json.dumps(FL)).replace('__MODE__', 'full')
html = html.replace('const W = 1080, H = 1920, FPS = 30, DUR = 16.3;', f'const W = 1080, H = 1920, FPS = 30, DUR = {DUR_EN};')
html = html.replace('const Wt = (w, n = 0) => WORDS.filter', f'const OVR = {json.dumps(OVR)};\nconst Wt = (w, n = 0) => OVR[w + "|" + n] ?? WORDS.filter')
TAF = ("@font-face{font-family:'Slab';src:url(fonts/catamaran-tamil-900-normal.woff2);unicode-range:U+0B80-0BFF,U+20B9;font-display:block}\n"
       "@font-face{font-family:'Bagel';src:url(fonts/baloo-thambi-2-tamil-800-normal.woff2);unicode-range:U+0B80-0BFF,U+20B9;font-display:block}\n"
       "@font-face{font-family:'JBM';src:url(fonts/mukta-malar-tamil-800-normal.woff2);font-weight:800;unicode-range:U+0B80-0BFF;font-display:block}\n"
       "@font-face{font-family:'Mont';src:url(fonts/mukta-malar-tamil-800-normal.woff2);font-weight:900;unicode-range:U+0B80-0BFF,U+20B9;font-display:block}\n")
html = html.replace("@font-face{font-family:'Slab'", TAF + "@font-face{font-family:'Slab'", 1)
html = html.replace("'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789$,.:?!·…→✓%&\\''", "'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789$,.:?!·…→✓%&\\'அஆஇஈஉஊஎஏஐஒஓகஙசஞடணதநபமயரலவழளறனஜஷஸஹாிீுூெேைொோௌ்₹'")
FIT = "  const ws = arr.map(c => measure(c, size, family, weight)); const total = ws.reduce((a, b) => a + b, 0) + ls * (arr.length - 1);\n"
html = html.replace(FIT, FIT + "  if (!o._fit) { const avail = anchor === 'middle' ? W - 90 : anchor === 'end' ? x - 45 : W - 45 - x; if (total > avail) { parent.removeChild(g); return chars(parent, str, { ...o, size: size * avail / total, _fit: 1 }); } }\n")
assert 'o._fit' in html
html = html.replace('const arr = [...str];', "const arr = [...new Intl.Segmenter('ta', { granularity: 'grapheme' }).segment(str)].map(s => s.segment);")
html = html.replace("Math.round(v).toLocaleString('en-US'); bS.textContent = s; bT.textContent = s;\n      op(big, t > Wt('four')", "Math.round(v).toLocaleString('en-IN'); bS.textContent = s; bT.textContent = s;\n      op(big, t > Wt('four')")
# rupee line under the dollar count (S16)
html = html.replace("    const gone = chars(g, 'GONE',", "    const inr = chars(g, '₹4,000 கோடி+', { x: 540, y: 655, size: 104, family: F.slab, weight: 400, fill: C.red, anchor: 'middle', shadow: { fill: C.ink, dx: 6, dy: 6 } });\n    const gone = chars(g, 'GONE',")
html = html.replace("      charsPop(gone, t, Wt('gone') - .05, .07, .35, 120);", "      charsPop(inr, t, Wt('inr') - .05, .05, .3, 50); op(inr.g, t < Wt('gone') ? 1 : 1 - seg(t, Wt('gone'), Wt('gone') + .2));\n      charsPop(gone, t, Wt('gone') - .05, .07, .35, 120);")
TR = {'IN': 'வெறும்', 'MINUTES': 'நிமிஷம்', 'A COMPANY': 'ஒரு கம்பெனி', 'LOST': 'நஷ்டம்', 'NO HACKER': 'ஹேக்கர் இல்ல', 'ONE MISSED': 'ஒரே ஒரு', 'STEP': 'ஸ்டெப் மிஸ்',
      'MISSED': 'மிஸ்!', 'AUG 1, 2012': 'ஆகஸ்ட் 1, 2012', 'THE SUSPECT': 'சந்தேக நபர்', 'BIG PLAYER': 'பெரிய புள்ளி', 'UPDATING…': 'அப்டேட்…',
      '8 SERVERS': '8 சர்வர்', 'SERVER #8': 'சர்வர் #8', 'SINCE 2003': '2003 முதல்', 'OLD FEATURE': 'பழைய ஃபீச்சர்', 'SAME SWITCH': 'அதே ஸ்விட்ச்',
      'IGNORED': 'கண்டுக்கல', 'MARKET OPEN': 'மார்க்கெட் ஓப்பன்', 'WAKES UP': 'முழிச்சுக்குது!', 'TRADES': 'டிரேட்ஸ்', '154 STOCKS': '154 ஸ்டாக்ஸ்',
      '45 MIN LATER': '45 நிமிஷம் கழிச்சு', 'STOPPED': 'நிறுத்தம்', 'GONE': 'போச்சு!', '$400M RESCUE': '$400M உதவி', 'TAKEN OVER 2013': 'கைமாறியது 2013',
      'RIVAL': 'போட்டி', 'THE LESSON': 'பாடம்', 'REVIEWED BY 2': '2 பேர் ரிவ்யூ ✓', 'CASE CLOSED': 'கேஸ் க்ளோஸ்', 'with Max': 'தமிழ்',
      'SUBSCRIBE': 'சப்ஸ்க்ரைப்', 'SUBSCRIBED ✓': 'சப்ஸ்க்ரைப் ✓',
      'THE LOSS': 'நஷ்டம்', 'THE CAUSE': 'காரணம்', 'THE COMPANY': 'கம்பெனி', 'THE SERVERS': 'சர்வர்கள்', 'THE OLD SWITCH': 'பழைய ஸ்விட்ச்',
      'THE WARNINGS': 'எச்சரிக்கை', 'THE OPEN': 'ஓப்பன்', 'THE DAMAGE': 'சேதம்', 'FILE': 'கோப்பு', 'VERDICT': 'தீர்ப்பு', 'CLOSED': 'முடிவு'}
for k in range(1, 7): TR[f'EXHIBIT 0{k}'] = f'சாட்சி 0{k}'
for en, ta in TR.items():
    html = html.replace(f"'{en}'", f"'{ta}'")
OUT = D / 'out_ta'; OUT.mkdir(exist_ok=True)
(D / 'build_ta.html').write_text(html)

page = (D / 'build_ta.html').resolve()
if os.environ.get('STILLS'):
    ts = [float(x) for x in os.environ['STILLS'].split(',')]
    js = "const { chromium } = require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});p.on('pageerror',e=>console.error('pageerror',e.message));await p.goto('file://%s');await p.waitForFunction(()=>window.READY===true,null,{timeout:60000});for(const [t,te] of %s){await p.evaluate(t=>window.render(t),te);await p.screenshot({path:'%s/st_'+t+'.png'});}await b.close();})();" % (page, json.dumps([[t, unwarp(t)] for t in ts]), OUT.resolve())
    (OUT / 'st.cjs').write_text(js); subprocess.run(['node', str(OUT / 'st.cjs')], check=True); sys.exit(0)

# ---- audio: Tamil VO + music + warped SFX
SR = 48000
def load(p):
    r = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', str(p), '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(r, dtype=np.float32).reshape(-1, 2).copy()
n = int(DUR_TA * SR); mix = np.zeros((n, 2), np.float32)
vo = load('public/' + TA['vo'])[:n]; mix[:len(vo)] += vo
mu = load('public/' + TA['music'])[:n] * .16; mix[:len(mu)] += mu
for name, t, v in SFX:
    tt = warp(t)
    if tt >= DUR_TA: continue
    a = load(f'hf/ast01-short/assets/sfx/{name}.wav') * v; i = int(tt * SR); m = min(len(a), n - i); mix[i:i + m] += a[:m]
mix = np.tanh(mix * 1.1) / 1.1
with wave.open(str(OUT / 'mix.wav'), 'w') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes())

# ---- picture: Tamil frame f -> english time unwarp(f/30)
N = round(DUR_TA * 30)
(OUT / 'times.json').write_text(json.dumps([round(unwarp(f / 30), 4) for f in range(N)]))
js = f'''const {{ chromium }} = require('playwright'); const {{ spawn }} = require('child_process'); const T = require('{(OUT / 'times.json').resolve()}');
(async () => {{ const b = await chromium.launch({{ args: ['--font-render-hinting=none', '--force-color-profile=srgb'] }});
 const p = await b.newPage({{ viewport: {{ width: 1080, height: 1920 }} }}); p.on('pageerror', e => console.error('pageerror', e.message));
 await p.goto('file://{page}'); await p.waitForFunction(() => window.READY === true, null, {{ timeout: 60000 }});
 const ff = spawn('ffmpeg', ['-y','-loglevel','error','-f','image2pipe','-framerate','30','-c:v','png','-i','-','-c:v','libx264','-crf','14','-pix_fmt','yuv420p','{(OUT / 'video.mp4').resolve()}']);
 for (let f = 0; f < T.length; f++) {{ await p.evaluate(t => window.render(t), T[f]); const png = await p.screenshot({{ type: 'png' }}); if (!ff.stdin.write(png)) await new Promise(r => ff.stdin.once('drain', r)); if (f % 120 === 0) console.log('frame', f, '/', T.length); }}
 ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close(); }})();'''
(OUT / 'render.cjs').write_text(js)
subprocess.run(['node', str(OUT / 'render.cjs')], check=True)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(OUT / 'video.mp4'), '-i', str(OUT / 'mix.wav'), '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11',
                '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-shortest', str(OUT / 'tamil01_dossier.mp4')], check=True)
print('done')
