"""Check every narration clip for repeats, garbage or truncation (offline, no quota).
Flags a beat when its speaking rate or the offline recogniser's word count doesn't fit the script line.
Usage: python3 tools/verify_vo.py <timeline-id>   (exit code 1 if anything is flagged)"""
import json, subprocess, sys
import numpy as np
sys.path.insert(0, 'tools')
import audio
from pocketsphinx import Decoder

tid = sys.argv[1]
t = json.load(open(f'src/episodes/{tid}.timeline.json'))
x = audio.read('public/' + t['vo']); sr = audio.SR
bad = 0
for i, b in enumerate(t['beats']):
    n = len(b['text'].split())
    seg = x[int(b['start'] * sr):int((b['start'] + b['vo']) * sr)]
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-f', 'f32le', '-ar', str(sr), '-ac', '1', '-i', '-', '-ar', '16000', '-f', 's16le', '-'],
                         input=seg.astype(np.float32).tobytes(), capture_output=True).stdout
    d = Decoder(samprate=16000, logfn='/dev/null'); d.start_utt(); d.process_raw(raw, full_utt=True); d.end_utt()
    hyp = d.hyp().hypstr if d.hyp() else ''
    wps, ratio = n / b['vo'], len(hyp.split()) / max(1, n)
    flag = []
    if wps < 1.9: flag.append(f'slow {wps:.1f} w/s (repeat or long pause?)')
    if wps > 4.2: flag.append(f'fast {wps:.1f} w/s (truncated?)')
    if ratio > 1.45: flag.append(f'recogniser heard {ratio:.1f}x the words (repeat/garbage?)')
    if ratio < 0.55: flag.append(f'recogniser heard {ratio:.1f}x the words (missing words?)')
    bad += bool(flag)
    print(f"{'!!' if flag else 'ok'} {i}: {b['vo']:.2f}s {n}w | {'; '.join(flag)} | {hyp[:80]}")
print('FLAGGED' if bad else 'ALL CLEAN', bad)
sys.exit(1 if bad else 0)
