"""Tamil version of reseg.py: line k's last word(s) landed at the start of line k+1's take (batch splitter cut at a
dramatic pause). Moves the boundary to the first real pause (>= 150 ms, after 0.3 s) inside line k+1's window. Audio is
unchanged. Then run align_ta.py + check_vo_ta.py again.
Usage: python3 tools/reseg_ta.py <timeline-id> <k> [<k> ...]   (k = 1-based line whose ending spilled into k+1)"""
import json, sys
import numpy as np
sys.path.insert(0, 'tools')
from align_ta import load, frames_db, pauses

tid = sys.argv[1]; p = f'src/episodes/{tid}.timeline.json'; tl = json.load(open(p)); B = tl['beats']
x = load('public/' + tl['vo'])
for k in map(int, sys.argv[2:]):
    a, b = B[k - 1], B[k]
    seg = x[int(b['start'] * 16000): int((b['start'] + b['vo']) * 16000)]
    db = frames_db(seg); v = db > max(-45, np.percentile(db, 95) - 32)
    idx = np.where(v)[0]; P = [(s, e) for s, e in pauses(v[idx[0]:], 15)]
    s, e = next((s + idx[0], e + idx[0]) for s, e in P if s + idx[0] > 30)
    cut0, cut1 = b['start'] + s * .01 + .03, b['start'] + e * .01 - .06
    end_b = b['start'] + b['vo']
    a['vo'] = round(cut0 - a['start'], 3)
    b['start'] = round(cut1, 3); b['vo'] = round(end_b - cut1, 3)
    print(f'line {k}/{k + 1}: boundary moved to {cut1:.2f} s (spill {s * .01:.2f} s long)')
for a, b in zip(B, B[1:]):
    a['dur'] = round(b['start'] - a['start'], 3)
B[-1]['dur'] = round(tl['duration'] - B[-1]['start'], 3)
json.dump(tl, open(p, 'w'), indent=1, ensure_ascii=False)
