"""Fix wrong line boundaries after a Gemini batch take (the splitter cut at the wrong pause, so a line's ending lands on the
next line). The audio is fine; only the beat boundaries are wrong. Works locally, two lines at a time: force-aligns the text of
line k + line k+1 against their joint window and moves the boundary to just before line k+1's first word. Audio is unchanged.
Then run align.py + verify_vo.py again.   Usage: python3 tools/reseg.py <timeline-id>"""
import json, subprocess, sys
import numpy as np
from pocketsphinx import Decoder
sys.path.insert(0, 'tools')
from align import spoken

tid = sys.argv[1]
p = f'src/episodes/{tid}.timeline.json'
tl = json.load(open(p)); B = tl['beats']; S = 16000
raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', f"public/{tl['vo']}", '-ac', '1', '-ar', str(S), '-f', 's16le', '-'], capture_output=True, check=True).stdout
pcm = np.frombuffer(raw, dtype=np.int16)
dec = Decoder(samprate=S, bestpath=False)

def toks_of(text):
    out = []
    for w in text.split():
        out += [s for s in spoken(w) if dec.lookup_word(s) is not None]
    return out

def align(a0, a1, toks):
    try:
        dec.set_align_text(' '.join(toks))
        dec.start_utt(); dec.process_raw(pcm[int(a0 * S):int(a1 * S)].tobytes(), full_utt=True); dec.end_utt()
        segs = [s for s in (dec.seg() or []) if s.word not in ('<s>', '</s>', '<sil>', '[NOISE]') and not s.word.startswith('+')]
        return segs if len(segs) == len(toks) else None
    except Exception:
        return None

moved = 0
for k in range(len(B) - 1):
    a, b = B[k], B[k + 1]
    ta, tb = toks_of(a['text']), toks_of(b['text'])
    a0 = max(0.0, a['start'] - 0.1); a1 = b['start'] + b['vo'] + 0.25
    segs = align(a0, a1, ta + tb)
    if not segs:
        print(f'  {k}|{k + 1}: kept'); continue
    end_a = a0 + (segs[len(ta) - 1].end_frame + 1) / 100
    start_b = a0 + segs[len(ta)].start_frame / 100
    nb = round(max(end_a, start_b - 0.12), 3)
    if abs(nb - b['start']) > 0.25:
        moved += 1; print(f'  {k}|{k + 1}: boundary {b["start"]:.2f} -> {nb:.2f}')
    old_end = b['start'] + b['vo']
    a['vo'] = round(end_a + 0.12 - a['start'], 3)
    b['start'] = nb; b['vo'] = round(old_end - nb, 3)
for i, bb in enumerate(B):
    if i + 1 < len(B):
        bb['dur'] = round(B[i + 1]['start'] - bb['start'], 3)
json.dump(tl, open(p, 'w'), indent=1, ensure_ascii=False)
print(f'{moved} boundaries moved')
