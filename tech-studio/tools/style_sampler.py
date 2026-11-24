"""Render HyperFrames registry motion styles as labelled 9:16 samples for the owner (2026-11-24).
Each item renders on its own (components mounted full-frame 1080x1920 with our story text; landscape blocks rendered
1920x1080 and padded into 9:16), then all clips are joined with a label strip.  Usage: python3 tools/style_sampler.py"""
import json, re, shutil, subprocess
from pathlib import Path

P = Path('hf/style-samples')
CLI = ['node', '/home/user/claude-projects/.claude/skills/hyperframes/scripts/plugin-cli.mjs']
GSAP_CDN = 'https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js'
(P / 'assets').mkdir(exist_ok=True)
shutil.copy('hf/knight01-v2/assets/gsap.min.js', P / 'assets' / 'gsap.min.js')
for f in list((P / 'compositions').glob('*.html')) + list((P / 'compositions' / 'components').glob('*.html')):
    s = f.read_text()
    if GSAP_CDN in s:
        f.write_text(s.replace(GSAP_CDN, 'assets/gsap.min.js'))

COMP = [  # (label, file, id, duration, variables)
    ('A  Headline slam + shake', 'headline-slam', 'headline-slam', 3.5, {'text': 'NO HACKER. ONE MISSED STEP.', 'accent_word_index': 3}),
    ('B  Character slam explode', 'char-slam-explode', 'char-slam-explode', 3.5, {'text': '$460M'}),
    ('C  Marker highlight', 'marker-highlight', 'marker-highlight', 3.5, {'text': 'Just one missed step', 'emphasis_word': 'missed'}),
    ('D  Notification pile-up', 'notification-pileup', 'notification-pileup', 4, {'count': 7}),
    ('E  Slot-machine number roll', 'slot-machine-roll', 'slot-machine-roll', 3.5, {'result': '460'}),
    ('F  Stop-motion cadence', 'stop-motion-cadence', 'stop-motion-cadence', 4, {}),
    ('G  Torn paper rip (transition)', 'torn-paper-rip', 'torn-paper-rip', 2.4, {}),
    ('H  Camera depth stack', 'camera-rig-depth-stack', 'camera-rig-depth-stack', 4, {}),
]
BLOCK = [  # landscape blocks
    ('I  Money count', 'apple-money-count', {}),
    ('J  Exploded 3D stack', 'exploded-stack', {'title': 'One missed step', 'layer_1': 'Write code', 'layer_2': 'Test it', 'layer_3': 'Copy to 8 servers', 'layer_4': 'Deploy', 'accent': '#E8402E', 'background': '#F4EDE3'}),
    ('K  Glitch', 'glitch', None),
    ('L  Whip pan', 'whip-pan', None),
    ('M  3D transitions', 'transitions-3d', None),
    ('N  News ticker', 'news-ticker', {}),
]


def dur_of(html, default=4.0):
    m = re.search(r'data-duration="([0-9.]+)"', html)
    return float(m.group(1)) if m else default


def wrap(cid, src, d, w, h, vars_):
    vv = f" data-variable-values='{json.dumps(vars_)}'" if vars_ else ''
    return f'''<!doctype html><html><head><meta charset="UTF-8"/><script src="assets/gsap.min.js"></script>
<style>*{{margin:0;padding:0}} html,body{{width:{w}px;height:{h}px;overflow:hidden;background:#F4EDE3}}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{d}" data-width="{w}" data-height="{h}" data-fps="30" style="position:relative;width:{w}px;height:{h}px;background:#F4EDE3">
<div id="host" data-composition-id="{cid}" data-composition-src="{src}" data-start="0" data-duration="{d}" data-track-index="1" data-width="{w}" data-height="{h}"{vv} style="position:absolute;inset:0"></div>
</div><script>window.__timelines=window.__timelines||{{}};window.__timelines["main"]=gsap.timeline({{paused:true}});</script></body></html>'''


def render(tag, html):
    (P / 'index.html').write_text(html)
    out = P / 'out' / f'{tag}.mp4'
    out.parent.mkdir(exist_ok=True)
    r = subprocess.run(CLI + ['render', str(P), '--quality', 'draft', '-o', str(out)], capture_output=True, text=True)
    ok = out.exists()
    print(tag, 'OK' if ok else 'FAIL', '' if ok else (r.stdout + r.stderr)[-400:])
    return out if ok else None


clips = []
for label, f, cid, d, v in COMP:
    o = render(f, wrap(cid, f'compositions/components/{f}.html', d, 1080, 1920, v))
    if o: clips.append((label, o, False))
for label, f, v in BLOCK:
    src = P / 'compositions' / f'{f}.html'
    s = src.read_text()
    if v is None:  # standalone document: render it as the page itself
        o = render(f, s)
    else:
        o = render(f, wrap(f, f'compositions/{f}.html', dur_of(s, 5), 1920, 1080, v))
    if o: clips.append((label, o, True))

parts = []
for k, (label, o, land) in enumerate(clips):
    seg = P / 'out' / f'seg{k:02d}.mp4'
    vf = ('scale=1080:-2,pad=1080:1920:0:(oh-ih)/2:color=#F4EDE3,' if land else 'scale=1080:1920,') + \
         f"drawbox=x=0:y=0:w=1080:h=130:color=#2A2018@0.92:t=fill,drawtext=fontfile=hf/ast01-short/assets/fonts/InterDisplay-Black.otf:text='{label}':fontcolor=white:fontsize=50:x=40:y=40"
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(o), '-vf', vf, '-r', '30', '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', str(seg)], check=True)
    parts.append(seg)
lst = P / 'out' / 'list.txt'
lst.write_text(''.join(f"file '{p.resolve()}'\n" for p in parts))
dst = Path('release/style_samples/STYLE_SAMPLES.mp4')
dst.parent.mkdir(parents=True, exist_ok=True)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(lst), '-c', 'copy', str(dst)], check=True)
print('->', dst, len(parts), 'samples')
