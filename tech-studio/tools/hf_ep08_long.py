"""ep08 long video "How to Use GPT-6 Astra": MIXED style + PRO UI kit (tools/kit_pro.py) on cream + dots (owner 2026-11-23).
Usage: THEME=cream GRID=dots python3 tools/hf_ep08_long.py"""
import json, os, sys
from pathlib import Path
os.environ['EPID'] = 'ep08'
sys.path.insert(0, str(Path(__file__).resolve().parent))
import hf_ep04_long as Z   # noqa: E402
import kit_paper, kit_vox, kit_props, kit_mix  # noqa: E402
B = Z.B
kit_vox.register(B)
kit_props.register(B)
kit_mix.register(B)
_beat = B.beat_scene
def beat_scene(i):
    html = _beat(i)
    if kit_paper.ON() and i > 0 and B.BE[i].get('chapter'):
        sid = f'b{i:02d}'; body, sc = kit_paper.sheet_wipe(sid)
        html = html.replace('</div>\n  </div>\n  <script>', '</div>\n' + body + '\n  </div>\n  <script>', 1) if '</div>\n  </div>\n  <script>' in html else html
        html = html.replace(f'    window.__timelines["{sid}"] = tl;', sc + f'\n    window.__timelines["{sid}"] = tl;')
    return html
B.beat_scene = beat_scene

if __name__ == '__main__':
    P, BE, S = B.P, B.BE, B.S
    comp = P / 'compositions'; comp.mkdir(parents=True, exist_ok=True)
    for f in comp.glob('*.html'):
        f.unlink()
    for i in range(len(BE)):
        (comp / f'b{i:02d}.html').write_text(B.beat_scene(i))
    (comp / 'bg.html').write_text(B.bg())
    (comp / 'chapters.html').write_text(B.chapters())
    G = list(enumerate(B.caption_groups()))
    B.CAPPARTS = []
    for part in range(0, len(G), 40):
        chunk = G[part:part + 40]
        (comp / f'caps{len(B.CAPPARTS)}.html').write_text(B.captions(chunk, len(B.CAPPARTS)))
        B.CAPPARTS.append((chunk[0][1][0][1], chunk[-1][1][-1][2]))
    (P / 'index.html').write_text(B.index())
    (P / 'assets/plan.json').write_text(json.dumps({'dur': B.DUR, 'provisional': B.PROVISIONAL,
                                                     'chapters': [(S[f"b{i:02d}"][0], t) for i, t in B.CHAPTERS]}, indent=1))
    print('written', len(BE), 'beats', B.DUR)
