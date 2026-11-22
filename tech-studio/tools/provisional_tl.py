"""Write an estimated timeline (no audio yet) so scenes can be built before narration is recorded.
Never overwrites a real timeline. Usage: python3 tools/provisional_tl.py <episode-dir-name>"""
import json, sys
from pathlib import Path
sys.path.insert(0, 'tools')
import audio
k = sys.argv[1]
ep = json.load(open(f'episodes/{k}/short.json'))
dst = Path(f"src/episodes/{ep['id']}.timeline.json")
if dst.exists() and not json.loads(dst.read_text()).get('provisional'):
    sys.exit(f'{dst} is a real timeline; not overwriting')
t, beats = 0.25, []
for b in ep['beats']:
    d = round(len(b['text'].split()) / 2.95 + 0.2, 3)
    beats.append({**b, 'start': round(t, 3), 'vo': d, 'dur': round(d + 0.15, 3), 'words': audio.words_timing(b['text'], d)})
    t += d + 0.15
dst.write_text(json.dumps({'id': ep['id'], 'provisional': True, 'duration': round(t + 1.0, 3), 'vo': None, 'beats': beats}, indent=1))
print(dst, round(t, 1), 's (estimated)')
