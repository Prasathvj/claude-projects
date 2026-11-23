"""Style sample for the owner (2026-11-23): first 8 beats of ep05 as cards with pictures inside (imgcard). ep05 long video "ChatGPT Doesn't Know What It's Going to Say Next" (16:9). First video in the AI-scenes style (owner chose
option A, 2026-11-22): full-frame illustrations from vidIQ (hf/ep05-long/assets/scenes/*.jpg) with camera moves and live overlays
(tools/hf_pics.py), plus the earlier scene types for numbers, checklist and outro.
Usage: THEME=cream GRID=<pattern> python3 tools/hf_ep05_long.py"""
import os, sys
from pathlib import Path
os.environ['EPID'] = 'ep05s'
sys.path.insert(0, str(Path(__file__).resolve().parent))
import hf_ep04_long as Z   # noqa: E402  (registers ep02-ep04 scene types)
import hf_pics             # noqa: E402
B = Z.B
hf_pics.register(B)
hf_pics.register_scenes(B)
hf_pics.register_imgcards(B)

if __name__ == '__main__':
    import json
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
    (B.P / 'index.html').write_text(B.index())
    (B.P / 'assets/plan.json').write_text(json.dumps({'dur': B.DUR, 'provisional': B.PROVISIONAL,
                                                     'chapters': [(S[f"b{i:02d}"][0], t) for i, t in B.CHAPTERS]}, indent=1))
    print('written', len(BE), 'beats', B.DUR, 's', 'PROVISIONAL timing' if B.PROVISIONAL else 'real timing')
