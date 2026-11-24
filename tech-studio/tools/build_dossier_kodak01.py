"""Build kodak01 (RISE & FALL) in the Halftone Dossier style. Engine = hf/knight01-dossier/index.html (helpers, captions,
Max, HUD, wipes, paper); scenes = hf/kodak01-dossier/scenes.js. Fills word times / cuts / shakes / flashes from the aligned
timeline, renders frames with Playwright through window.render(t), mixes VO + music + SFX, muxes.
Usage: python3 tools/build_dossier_kodak01.py        (STILLS=t1,t2,... for stills only)"""
import json, os, re, subprocess, sys, wave
from pathlib import Path
import numpy as np

D = Path('hf/kodak01-dossier')
tl = json.load(open('src/episodes/kodak01-short.timeline.json'))
DUR = round(tl['beats'][-1]['start'] + tl['beats'][-1]['vo'] + 1.3, 2)
norm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
words, chunks = [], []
for b in tl['beats']:
    ws = [{'w': w['w'], 'n': norm(w['w']), 's': round(b['start'] + w['s'], 3), 'e': round(b['start'] + w['e'], 3)} for w in b['words']]
    words += ws
    cur = []
    for w in ws:
        cur.append(w)
        if re.search(r'[.,:?!]$', w['w']) or len(cur) >= 4 or sum(len(x['w']) + 1 for x in cur) >= 20:
            chunks.append(cur); cur = []
    if cur: chunks.append(cur)
CH = []
for k, ch in enumerate(chunks):
    t0 = ch[0]['s'] - .05
    t1 = chunks[k + 1][0]['s'] - .05 if k + 1 < len(chunks) else DUR
    if k + 1 < len(chunks) and t1 - ch[-1]['e'] > 1.2: t1 = ch[-1]['e'] + 1.2
    CH.append({'t0': round(t0, 3), 't1': round(t1, 3), 'w': [{'w': w['w'].replace('...', '…'), 's': w['s'], 'e': w['e']} for w in ch]})
Wt = lambda n, i=0: [w for w in words if w['n'].startswith(n)][i]['s']
BS = [b['start'] for b in tl['beats']]
bw = lambda b, i: tl['beats'][b]['start'] + tl['beats'][b]['words'][i]['s']
K = {'bur': round(Wt('then') - .12, 3), 'c1': BS[1], 'eng': round(bw(1, 2) - .15, 3), 'c2': BS[2], 'c3': BS[3], 'c4': BS[4], 'c5': BS[5], 'c6': BS[6],
     'c7': BS[7], 'c8': BS[8], 'ph': round(Wt('then', 1) - .15, 3), 'c9': BS[9], 'ir': round(bw(9, 6) - .15, 3), 'c10': BS[10], 'c11': BS[11], 'end': DUR}
CUTS = [K[k] for k in ('bur', 'c1', 'eng', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'ph', 'c9', 'ir', 'c10', 'c11')]
STAMPS = [Wt('buried') + .1, Wt('first') + .05, Wt('shocking') + .05, Wt('yes') + .05, Wt('anyone') + .1, Wt('business') + .1, Wt('pocket') + .05,
          Wt('bankruptcy') + .1, Wt('disrupted') + .1, Wt('present') + .05, K['c11'] + .6]
SH = [[s, 18, .3] for s in STAMPS] + [[Wt('why') + .05, 22, .35]]
FL = [[Wt('why'), .45], [Wt('bankruptcy') + .1, .5], [Wt('disrupted') + .1, .45]]

# ---- page: knight01 engine + kodak01 scenes + kodak HUD / Max / wipes ----
src = Path('hf/knight01-dossier/index.html').read_text()
a = src.index('function buildAll() {') + len('function buildAll() {\n')
b = src.index('  // ---------- caption bar')
tail = src[b:]
tail = re.sub(r"  const MX = \[\[.*?\]\];\n", """  const MX = [[K.c5 + .15, K.c6 - .05, { brows: 'worried', eyes: 'wide', mouth: 'flat', arms: 'hush' }],
              [K.c10 + .1, K.c11 - .05, { brows: 'focused', eyes: 'squint', mouth: 'flat', arms: 'chin' }],
              [K.c11 + .05, K.end + 1, { brows: 'up', eyes: 'happy', mouth: 'grin', arms: 'point', extra: ['spark'] }]];\n""", tail, flags=re.S)
tail = tail.replace("'CASE No. 2012-KCG-001'", "'CASE No. 1975-KDK-001'")
tail = re.sub(r"  const chips = \[.*?\]\];\n", """  const chips = [[0, K.c1, 'EXHIBIT 01', 'THE CAMERA', '1975.12'], [K.c1, K.c3, 'FILE', 'THE INVENTOR', '1975.12'], [K.c3, K.c5, 'EXHIBIT 02', 'THE PROTOTYPE', '1975.12'],
    [K.c5, K.c6, 'EXHIBIT 03', 'THE MEETING', 'KODAK HQ'], [K.c6, K.c8, 'EXHIBIT 04', 'THE MONEY', 'FILM ERA'], [K.c8, K.c9, 'EXHIBIT 05', 'THE SHIFT', '2000s'],
    [K.c9, K.c10, 'VERDICT', 'THE FALL', '2012.01.19'], [K.c10, K.end + 1, 'CLOSED', 'THE LESSON', '1975-2012']];
  const rf = el('g', {}, hg); el('rect', { x: 50, y: 146, width: 214, height: 44, rx: 6, fill: C.red }, rf);
  txt(rf, 'RISE & FALL', { x: 157, y: 177, 'font-size': 26, 'font-family': F.sans, 'font-weight': 900, fill: C.cream, 'text-anchor': 'middle' });\n""", tail, flags=re.S)
tail = tail.replace("const dark = (t >= 6.22 && t < 7.27) || (t >= 40.42 && t < 42.31)", "const dark = t >= K.bur && t < K.c1")
tail = tail.replace("dateBg.setAttribute('stroke', ink);", "dateT.textContent = c[4]; dateBg.setAttribute('stroke', ink);")
tail = re.sub(r"  const WIPES = \[.*?\]\];\n", """  const WIPES = [[K.bur, C.ink], [K.c1, C.yellow], [K.eng, C.orange], [K.c2, C.yellow], [K.c3, C.orange], [K.c4, C.yellow], [K.c5, C.ink], [K.c6, C.yellow],
    [K.c7, C.red], [K.c8, C.orange], [K.ph, C.yellow], [K.c9, C.red], [K.ir, C.ink], [K.c10, C.orange], [K.c11, C.yellow]];\n""", tail, flags=re.S)
for need in ("CASE No. 1975", "K.c5 + .15", "RISE & FALL", "K.bur, C.ink", "dateT.textContent = c[4]", "const dark = t >= K.bur"):
    assert need in tail, need
html = src[:a] + (D / 'scenes.js').read_text().replace('__CUTS__', json.dumps(K)) + tail
html = html.replace('knight01 dossier</title>', 'kodak01 dossier</title>')
html = html.replace('__WORDS__', json.dumps(words)).replace('__CHUNKS__', json.dumps(CH)).replace('__SHAKES__', json.dumps(SH)).replace('__FLASHES__', json.dumps(FL))
html = html.replace('__MODE__', 'full').replace('const W = 1080, H = 1920, FPS = 30, DUR = 16.3;', f'const W = 1080, H = 1920, FPS = 30, DUR = {DUR};')
(D / 'build.html').write_text(html)
(D / 'out').mkdir(exist_ok=True)
print('DUR', DUR, 'cuts', K)

if os.environ.get('STILLS'):
    ts = [float(x) for x in os.environ['STILLS'].split(',')]
    js0 = "const { chromium } = require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});p.on('pageerror',e=>console.error('pageerror',e.message));p.on('console',m=>{if(m.type()==='error')console.error(m.text())});await p.goto('file://%s');await p.waitForFunction(()=>window.READY===true,null,{timeout:60000});for(const t of %s){await p.evaluate(t=>window.render(t),t);await p.screenshot({path:'%s/st_'+t+'.png'});}await b.close();})();" % ((D / 'build.html').resolve(), json.dumps(ts), (D / 'out').resolve())
    (D / 'out' / 'st.cjs').write_text(js0); subprocess.run(['node', str(D / 'out' / 'st.cjs')], check=True); sys.exit(0)

# ---- SFX plan ----
S = lambda n, t, v=.5: (n, t, v)
SFX = [S('whoosh', c - .15, .4) for c in CUTS] + [S('stamp', s - .02, .8) for s in STAMPS]
SFX += [S('thud', .1, .45), S('pop', Wt('invented') - .1, .35), S('thud', Wt('digital') - .1, .5), S('ding', Wt('camera'), .35),
        S('rumble', Wt('buried') - .1, .5), S('impact', Wt('why'), .7), S('snap', Wt('why') + .05, .4),
        S('thud', BS[1] + .2, .45)] + [S('flip', Wt('1975') - .1 + i * .14, .5) for i in range(3)] + [S('ding', Wt('1975') + .35, .35)]
SFX += [S('thud', K['eng'] + .2, .45), S('snap', Wt('steve'), .45), S('thud', Wt('builds') + .05, .45), S('pop', Wt('portable'), .35)]
SFX += [S('thud', Wt('iphone') - .15, .45), S('error', Wt('and') - .05, .45), S('thud', Wt('toaster') - .1, .5), S('ding', Wt('college') - .05, .45), S('chirp', Wt('college') + .1, .3)]
SFX += [S('thud', K['c3'] + .15, .45), S('type', Wt('36') - .15, .35), S('type', Wt('16') - .15, .35)] + [S('tick2', Wt('16') + k * .04, .15) for k in range(0, 16, 2)] + [S('scan', Wt('megapixels') - .1, .4)]
SFX += [S('thud', K['c4'] + .2, .45), S('servo', Wt('takes'), .35), S('hum', Wt('takes') + .4, .25), S('ding', Wt('seconds') + .1, .45)]
SFX += [S('thud', K['c5'] + .2, .4), S('pop', Wt('reportedly') - .1, .3), S('pop', Wt('thats') - .1, .4), S('pop', Wt('dont') - .2, .4), S('hiss', Wt('dont') + .1, .25)]
SFX += [S('thud', Wt('kodak', 2) - .05, .5), S('chain', Wt('money'), .45), S('ding', Wt('money') + .1, .35), S('snap', Wt('film') + .2, .4)]
SFX += [S('pop', Wt('film', 1) - .1, .35), S('pop', Wt('developing') - .1, .35), S('pop', Wt('prints') - .1, .35), S('chain', Wt('prints') + .45, .4), S('pop', Wt('digital', 2) - .1, .4)]
SFX += [S('error', Wt('no') - .05, .4), S('error', Wt('no', 1) - .2, .4), S('error', Wt('repeat') - .1, .4)]
SFX += [S('thud', K['c8'] + .2, .45), S('lock', Wt('past') + .1, .5), S('riser', Wt('future'), .3), S('ding', Wt('loaded') + .3, .4)]
SFX += [S('pop', Wt('smartphones') + k * .1, .3) for k in range(6)]
SFX += [S('thud', Wt('kodak', 4) - .1, .5), S('flip', Wt('kodak', 4) - .15, .4), S('thud', K['ir'] + .2, .4), S('pop', Wt('invented', 1), .35), S('rumble', Wt('disrupted'), .5), S('impact', Wt('disrupted') + .1, .5)]
SFX += [S('ding', Wt('see') - .1, .4), S('thud', Wt('afraid') - .2, .45), S('thud', K['c11'] + .1, .4), S('pop', Wt('subscribe'), .4), S('click', Wt('more') + .1, .6), S('ding', Wt('more') + .2, .4)]
SR = 48000


def load(p):
    r = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', str(p), '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(r, dtype=np.float32).reshape(-1, 2).copy()


n = int(DUR * SR)
mix = np.zeros((n, 2), np.float32)
vo = load('public/' + tl['vo'])[:n]; mix[:len(vo)] += vo
mu = load('public/' + tl['music'])[:n] * .16; mix[:len(mu)] += mu
for name, t, v in SFX:
    if t >= DUR: continue
    a = load(f'hf/ast01-short/assets/sfx/{name}.wav') * v; i = int(max(0, t) * SR); m = min(len(a), n - i); mix[i:i + m] += a[:m]
mix = np.tanh(mix * 1.1) / 1.1
with wave.open(str(D / 'out' / 'mix.wav'), 'w') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes())

# ---- picture ----
js = f'''const {{ chromium }} = require('playwright'); const {{ spawn }} = require('child_process');
(async () => {{ const b = await chromium.launch({{ args: ['--font-render-hinting=none', '--force-color-profile=srgb'] }});
 const p = await b.newPage({{ viewport: {{ width: 1080, height: 1920 }} }}); p.on('pageerror', e => console.error('pageerror', e.message));
 await p.goto('file://{(D / 'build.html').resolve()}'); await p.waitForFunction(() => window.READY === true, null, {{ timeout: 60000 }});
 const ff = spawn('ffmpeg', ['-y','-loglevel','error','-f','image2pipe','-framerate','30','-c:v','png','-i','-','-c:v','libx264','-crf','14','-pix_fmt','yuv420p','{(D / 'out' / 'video.mp4').resolve()}']);
 const N = Math.round({DUR} * 30);
 for (let f = 0; f < N; f++) {{ await p.evaluate(t => window.render(t), f / 30); const png = await p.screenshot({{ type: 'png' }}); if (!ff.stdin.write(png)) await new Promise(r => ff.stdin.once('drain', r)); if (f % 150 === 0) console.log('frame', f, '/', N); }}
 ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close(); }})();'''
(D / 'out' / 'render.cjs').write_text(js)
subprocess.run(['node', str(D / 'out' / 'render.cjs')], check=True)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(D / 'out' / 'video.mp4'), '-i', str(D / 'out' / 'mix.wav'), '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11',
                '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-shortest', str(D / 'out' / 'kodak01_dossier.mp4')], check=True)
print('done')
