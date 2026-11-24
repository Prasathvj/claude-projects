"""Hard pre-render gate for narration + captions (owner 2026-11-24: never ship a sync/repeat/missing-word mistake again).
Fails (exit 1) when, for any line:
  1. its text does not force-align to its own audio window (missing / wrong / extra words),
  2. there is speech inside its window outside the aligned words (a repeated phrase or leftover audio),
  3. there is speech in the gap before the next line that belongs to no line (spill-over between lines),
  4. caption word times are out of order or run past the next line.
Usage: python3 tools/check_vo.py <timeline-id>      Run AFTER align.py, BEFORE the generator/render. Must print PASS."""
import json, subprocess, sys
import numpy as np
from pocketsphinx import Decoder
sys.path.insert(0, 'tools')
from align import spoken

tid = sys.argv[1]
tl = json.load(open(f'src/episodes/{tid}.timeline.json')); B = tl['beats']; S = 16000
raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', f"public/{tl['vo']}", '-ac', '1', '-ar', str(S), '-f', 's16le', '-'], capture_output=True, check=True).stdout
pcm = np.frombuffer(raw, dtype=np.int16); x = pcm.astype(np.float64) / 32768
dec = Decoder(samprate=S, bestpath=False)
hop = int(0.02 * S); rms = np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, 'same')[::hop])
thr = max(10 ** (-38 / 20), np.percentile(rms, 95) * 0.06)
def speech(a, b):
    """seconds of speech-level audio in [a, b)"""
    i0, i1 = max(0, int(a / .02)), min(len(rms), int(b / .02))
    return float((rms[i0:i1] > thr).sum() * .02) if i1 > i0 else 0.0

bad = []
for i, b in enumerate(B):
    a0 = max(0.0, b['start'] - 0.08); a1 = b['start'] + b['vo'] + 0.12
    toks = [s for w in b['text'].split() for s in spoken(w) if dec.lookup_word(s) is not None]
    segs = []
    for pad in (0.0, 0.12, 0.3):          # forced alignment is brittle at the exact edges: try a few paddings
        q0, q1 = max(0.0, a0 - pad), a1 + pad
        try:
            dec.set_align_text(' '.join(toks)); dec.start_utt(); dec.process_raw(pcm[int(q0 * S):int(q1 * S)].tobytes(), full_utt=True); dec.end_utt()
            segs = [s for s in (dec.seg() or []) if s.word not in ('<s>', '</s>', '<sil>', '[NOISE]') and not s.word.startswith('+')]
        except Exception:
            segs = []
        if len(segs) == len(toks):
            a0 = q0; break
    if len(segs) != len(toks):
        bad.append((i, 'text does not match audio (missing/extra words)')); continue
    w0 = a0 + segs[0].start_frame / 100; w1 = a0 + (segs[-1].end_frame + 1) / 100
    extra = speech(a0, w0 - 0.25) + speech(w1 + 0.25, a1)
    if extra > 0.8:
        bad.append((i, f'{extra:.1f}s of extra speech inside the line window (repeat/leftover?)'))
    if i + 1 < len(B):
        gap = speech(b['start'] + b['vo'] + 0.12, B[i + 1]['start'] - 0.08)
        if gap > 0.4:
            bad.append((i, f'{gap:.1f}s of speech between this line and the next (belongs to no line)'))
    prev = -1
    lim = (B[i + 1]['start'] - b['start']) if i + 1 < len(B) else 1e9
    for w in b['words']:
        if w['s'] < prev - 1e-3 or w['e'] < w['s'] or w['e'] > lim:
            bad.append((i, f'caption word "{w["w"]}" out of order or past the next line')); break
        prev = w['e']
for i, msg in bad:
    print(f'FAIL line {i}: {msg} | {B[i]["text"][:70]}')
print('PASS' if not bad else f'{len(bad)} problem(s): fix before rendering')
sys.exit(1 if bad else 0)
