"""Shorten long silences INSIDE narration lines (no speed-up; only silent audio is cut).
Gemini 'mystery' takes (Charon) leave 1-6 s dramatic pauses mid-line; a Short can't afford them.
Usage: python3 tools/tighten.py <timeline-id> [max_pause=0.5]
Then re-run align.py and check_vo.py (the gate) before any render."""
import json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
import audio

tid = sys.argv[1]
MAXP = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
tp = Path(f'src/episodes/{tid}.timeline.json')
tl = json.loads(tp.read_text())
x = audio.read(Path('public') / tl['vo'])
SR = audio.SR
mono = x if x.ndim == 1 else x.mean(axis=1)
hop = int(0.01 * SR)
rms = np.sqrt(np.convolve(mono ** 2, np.ones(hop) / hop, 'same')[::hop])
thr = max(10 ** (-42 / 20), np.percentile(rms, 95) * 0.04)
XF = int(0.015 * SR)

out, cursor, t_new, saved = [], 0, 0.0, 0.0
pieces = []  # (src_a, src_b) kept ranges, in samples
for b in tl['beats']:
    a0, a1 = int(b['start'] * SR), int((b['start'] + b['vo']) * SR)
    f0, f1 = a0 // hop, a1 // hop
    quiet = rms[f0:f1] < thr
    cuts = []
    k = 0
    while k < len(quiet):
        if quiet[k]:
            j = k
            while j < len(quiet) and quiet[j]:
                j += 1
            # only inner silences (speech on both sides)
            if k > 0 and j < len(quiet) and (j - k) * hop > MAXP * SR:
                keep = int(MAXP * SR / 2)
                s, e = a0 + k * hop + keep, a0 + j * hop - keep
                cuts.append((s, e))
            k = j
        else:
            k += 1
    b['_cuts'] = cuts

# rebuild audio; remap beat starts
new = []
pos_src, pos_new = 0, 0
def emit(a, b_):
    global pos_new
    seg = x[a:b_]
    if new and len(seg) > XF and len(new[-1]) > XF:
        r = np.linspace(0, 1, XF)[:, None] if seg.ndim > 1 else np.linspace(0, 1, XF)
        new[-1][-XF:] = new[-1][-XF:] * (1 - r) + seg[:XF] * r
        seg = seg[XF:]
    new.append(seg.copy()); pos_new += len(seg)

def src2new(s, cuts_all):
    return s - sum(min(e, s) - c + XF for c, e in cuts_all if c < s)

allcuts = [c for b in tl['beats'] for c in b['_cuts']]
for c, e in allcuts:
    emit(pos_src, c); pos_src = e
emit(pos_src, len(x))
y = np.concatenate(new)
for b in tl['beats']:
    s0 = int(b['start'] * SR); s1 = int((b['start'] + b['vo']) * SR)
    cut = sum(e - c + XF for c, e in b.pop('_cuts'))
    ns = src2new(s0, allcuts)
    b['start'] = round(ns / SR, 3); b['vo'] = round((s1 - s0 - cut) / SR, 3)
    saved += cut / SR
for b, nb in zip(tl['beats'], tl['beats'][1:]):
    b['dur'] = round(nb['start'] - b['start'], 3)
tot = len(y) / SR
tl['beats'][-1]['dur'] = round(tot - tl['beats'][-1]['start'], 3)
tl['duration'] = round(tot, 3)
audio.write(Path('public') / tl['vo'], y)
audio.write(Path('public') / tl['music'], audio.music(tot))
tp.write_text(json.dumps(tl, indent=1, ensure_ascii=False))
print(f'{tid}: cut {saved:.1f} s of inner silence (max pause {MAXP} s) -> {tot:.1f} s')
