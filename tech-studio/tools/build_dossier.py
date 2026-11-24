"""Build knight01 in the Halftone Dossier style (hf/knight01-dossier/index.html is the engine + scenes).
Fills word times / caption chunks / shakes / flashes from the aligned timeline, renders frames with Playwright through
window.render(t), mixes VO + music + SFX with numpy, muxes.  Usage: python3 tools/build_dossier.py [dur_seconds]"""
import json, os, re, subprocess, sys, wave
from pathlib import Path
import numpy as np

D = Path('hf/knight01-dossier')
tl = json.load(open('src/episodes/knight01-short.timeline.json'))
DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 16.3
norm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
words, chunks = [], []
for b in tl['beats']:
    if b['start'] >= DUR: break
    ws = [{'w': w['w'], 'n': norm(w['w']), 's': round(b['start'] + w['s'], 3), 'e': round(b['start'] + w['e'], 3)} for w in b['words']]
    words += ws
    cur = []
    for w in ws:
        cur.append(w)
        if re.search(r'[.,:?!]$', w['w']) or len(cur) >= 4:
            chunks.append(cur); cur = []
    if cur: chunks.append(cur)
CH = []
for k, ch in enumerate(chunks):
    t0 = ch[0]['s'] - .05
    t1 = chunks[k + 1][0]['s'] - .05 if k + 1 < len(chunks) else DUR
    CH.append({'t0': round(t0, 3), 't1': round(min(t1, ch[-1]['e'] + 1.2) if k + 1 < len(chunks) and chunks[k + 1][0]['s'] - ch[-1]['e'] > 1.2 else t1, 3), 'w': [{'w': w['w'], 's': w['s'], 'e': w['e']} for w in ch]})
Wt = lambda n, i=0: [w for w in words if w['n'].startswith(n)][i]['s']
SH = [[Wt('45') + .05, 16, .3], [Wt('lost') + .05, 18, .3], [Wt('dollars'), 24, .4], [Wt('hacker') + .2, 10, .25], [Wt('step') + .05, 18, .3], [Wt('biggest') + .05, 16, .3]]
FL = [[Wt('dollars'), .5], [Wt('knight'), .5], [Wt('capital'), .45]]
html = (D / 'index.html').read_text()
html = html.replace('__WORDS__', json.dumps(words)).replace('__CHUNKS__', json.dumps(CH)).replace('__SHAKES__', json.dumps(SH)).replace('__FLASHES__', json.dumps(FL))
MODE = os.environ.get('MODE', 'full')
html = html.replace('__MODE__', MODE)
html = html.replace('const W = 1080, H = 1920, FPS = 30, DUR = 16.3;', f'const W = 1080, H = 1920, FPS = 30, DUR = {DUR};')
(D / 'build.html').write_text(html)

import os
if os.environ.get('STILLS'):
    ts = os.environ['STILLS'].split(',')
    js0 = "const { chromium } = require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});p.on('pageerror',e=>console.error('pageerror',e.message));p.on('console',m=>{if(m.type()==='error')console.error(m.text())});await p.goto('file://%s');await p.waitForFunction(()=>window.READY===true,null,{timeout:60000});for(const t of %s){await p.evaluate(t=>window.render(t),t);await p.screenshot({path:'%s/st_'+t+'.png'});}await b.close();})();" % ((D / 'build.html').resolve(), json.dumps([float(x) for x in ts]), (D / 'out').resolve())
    (D / 'out').mkdir(exist_ok=True); (D / 'out' / 'st.cjs').write_text(js0); subprocess.run(['node', str(D / 'out' / 'st.cjs')], check=True); sys.exit(0)
# ---- SFX plan (our library) ----
S = lambda n, t, v=.5: (n, t, v)
SFX = [S('pop', Wt('in') - .05, .3), S('impact', Wt('45'), .6), S('tick', Wt('45') + .4, .35), S('tick', Wt('45') + .8, .35), S('tick', Wt('minutes'), .35),
       S('whoosh', 1.85, .4), S('thud', Wt('company') + .45, .5), S('stamp', Wt('lost') + .02, .8), S('chain', Wt('460'), .35), S('impact', Wt('dollars'), .7), S('snap', Wt('dollars'), .5),
       S('whoosh', 6.05, .4), S('rip', Wt('hacker') + .15, .5), S('rip', Wt('hacker') + .29, .5), S('whoosh', 7.1, .4),
       S('pop', 7.4, .3), S('pop', 7.62, .3), S('pop', 7.97, .3), S('error', 8.35, .4), S('stamp', Wt('step') + .02, .8), S('whoosh', 9.05, .4),
       S('thud', Wt('august') - .1, .5), S('flip', Wt('august') + .1, .5), S('flip', Wt('august') + .26, .5), S('flip', Wt('august') + .42, .5), S('ding', Wt('2012'), .4),
       S('snap', Wt('knight'), .6), S('snap', Wt('capital'), .55), S('thud', Wt('capital') + .25, .45), S('stamp', Wt('biggest') + .02, .8), S('whoosh', 14.05, .4)]
SFX += [S('type', Wt('updating') + .1 + .3 * i, .35) for i in range(4)]
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
    a = load(f'hf/ast01-short/assets/sfx/{name}.wav') * v; i = int(t * SR); m = min(len(a), n - i); mix[i:i + m] += a[:m]
mix = np.tanh(mix * 1.1) / 1.1
(D / 'out').mkdir(exist_ok=True)
with wave.open(str(D / 'out' / 'mix.wav'), 'w') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes())

# ---- picture ----
js = f'''const {{ chromium }} = require('playwright'); const {{ spawn }} = require('child_process');
(async () => {{ const b = await chromium.launch({{ args: ['--font-render-hinting=none', '--force-color-profile=srgb'] }});
 const p = await b.newPage({{ viewport: {{ width: 1080, height: 1920 }} }}); p.on('pageerror', e => console.error('pageerror', e.message));
 await p.goto('file://{(D / 'build.html').resolve()}'); await p.waitForFunction(() => window.READY === true, null, {{ timeout: 60000 }});
 const ff = spawn('ffmpeg', ['-y','-loglevel','error','-f','image2pipe','-framerate','30','-c:v','png','-i','-','-c:v','libx264','-crf','14','-pix_fmt','yuv420p','{(D / 'out' / 'video.mp4').resolve()}']);
 const N = Math.round({DUR} * 30);
 for (let f = 0; f < N; f++) {{ await p.evaluate(t => window.render(t), f / 30); const png = await p.screenshot({{ type: 'png' }}); if (!ff.stdin.write(png)) await new Promise(r => ff.stdin.once('drain', r)); if (f % 60 === 0) console.log('frame', f, '/', N); }}
 ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close(); }})();'''
(D / 'out' / 'render.cjs').write_text(js)
subprocess.run(['node', str(D / 'out' / 'render.cjs')], check=True)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(D / 'out' / 'video.mp4'), '-i', str(D / 'out' / 'mix.wav'), '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11',
                '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-shortest', str(D / 'out' / f'knight01_dossier_{MODE}.mp4')], check=True)
print('done', MODE)
