"""Word-level forced alignment of narration with pocketsphinx (bundled English model, offline).
Aligns each beat's text inside its own audio window, so an error can never spread past one line.
Usage: python3 tools/align.py <timeline-id>   (rewrites the beats' "words" with aligned times)"""
import json, re, subprocess, sys, wave
import numpy as np
from pocketsphinx import Decoder

NUM = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'}

def spoken(w):
    """Display word -> words the aligner should hear (numbers spelled out)."""
    x = w.lower().replace('’', "'")
    t = re.fullmatch(r"(\d{1,2}):(\d{2})[^0-9]*", x)  # clock times: 9:30 -> nine thirty, 8:01 -> eight oh one
    if t:
        h, m = int(t.group(1)), int(t.group(2))
        return spoken(str(h)) + ([] if m == 0 else (['oh'] + spoken(str(m)) if m < 10 else spoken(str(m))))
    o = re.fullmatch(r"(\d+)(st|nd|rd|th)[^a-z0-9]*", x)  # ordinals: 1st -> first
    if o:
        ORD = {1: 'first', 2: 'second', 3: 'third', 4: 'fourth', 5: 'fifth', 6: 'sixth', 7: 'seventh', 8: 'eighth', 9: 'ninth', 10: 'tenth'}
        n = int(o.group(1))
        return [ORD[n]] if n in ORD else spoken(o.group(1))
    x = re.sub(r"[^a-z0-9.']", '', x).strip('.').strip("'")
    if not x:
        return []
    if re.fullmatch(r"\d+(\.\d+)?", x):
        if '.' in x:
            a, b = x.split('.')
            return spoken(a) + ['point'] + [NUM[d] for d in b]
        n = int(x)
        if 1900 <= n <= 2099:
            hi, lo = divmod(n, 100)
            return ['twenty'] + (spoken(str(lo)) if lo >= 10 else ['oh' if lo else 'hundred'] + ([NUM[str(lo)]] if lo else [])) if hi == 20 else [x]
        ones = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
        tens = 'x x twenty thirty forty fifty sixty seventy eighty ninety'.split()
        if n < 20: return [ones[n]]
        if n < 100: return [tens[n // 10]] + ([ones[n % 10]] if n % 10 else [])
        if n < 1000: return [ones[n // 100], 'hundred'] + (spoken(str(n % 100)) if n % 100 else [])  # 460 -> four hundred sixty
        if n < 1000000: return spoken(str(n // 1000)) + ['thousand'] + (spoken(str(n % 1000)) if n % 1000 else [])
        return [NUM[d] for d in x]
    return [x.replace('.', '')]

def main(tid):
    p = f'src/episodes/{tid}.timeline.json'
    tl = json.load(open(p))
    S = 16000
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', f"public/{tl['vo']}", '-ac', '1', '-ar', str(S), '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    pcm = np.frombuffer(raw, dtype=np.int16)
    dec = Decoder(samprate=S, bestpath=False)
    vocab = dec.get_config()  # noqa
    bad = 0
    for bi, b in enumerate(tl['beats']):
        a0 = max(0.0, b['start'] - 0.08); a1 = b['start'] + b['vo'] + 0.12
        seg = pcm[int(a0 * S):int(a1 * S)]
        disp = b['text'].split()
        toks, owner = [], []
        for i, w in enumerate(disp):
            for s in spoken(w):
                if dec.lookup_word(s) is None:
                    continue
                toks.append(s); owner.append(i)
        try:
            dec.set_align_text(' '.join(toks))
            dec.start_utt(); dec.process_raw(seg.tobytes(), full_utt=True); dec.end_utt()
            segs = [s for s in dec.seg() if s.word not in ('<s>', '</s>', '<sil>', '[NOISE]') and not s.word.startswith('+')]
            if len(segs) != len(toks):
                raise ValueError(f'{len(segs)} vs {len(toks)}')
        except Exception as e:
            bad += 1
            print(f'  beat {bi}: alignment failed ({e}); keeping estimate')
            continue
        spans = {}
        for s, o in zip(segs, owner):
            t0, t1 = a0 + s.start_frame / 100, a0 + (s.end_frame + 1) / 100
            if o in spans: spans[o] = (spans[o][0], t1)
            else: spans[o] = (t0, t1)
        words = []
        for i, w in enumerate(disp):
            if i in spans:
                words.append({'w': w, 's': round(spans[i][0] - b['start'], 3), 'e': round(spans[i][1] - b['start'], 3)})
            else:  # unknown to the dictionary: fill between neighbours
                words.append({'w': w, 's': None, 'e': None})
        for i, x in enumerate(words):
            if x['s'] is None:
                prev = words[i - 1]['e'] if i else 0.0
                nxt = next((y['s'] for y in words[i + 1:] if y['s'] is not None), b['vo'])
                x['s'], x['e'] = round(prev, 3), round(max(prev + 0.05, nxt), 3)
        b['words'] = words
    # caption safety (2026-11-24): word times strictly in order and never past the next line's start (a stuck/overlapping
    # caption group otherwise stays on screen; myst01 'worked.' bug)
    B = tl['beats']
    for bi, b in enumerate(B):
        lim = (B[bi + 1]['start'] - b['start'] - 0.06) if bi + 1 < len(B) else b['vo'] + 1.0
        prev = 0.0
        for w in b['words']:
            w['s'] = round(min(max(w['s'], prev), lim - 0.05), 3)
            w['e'] = round(min(max(w['e'], w['s'] + 0.05), lim), 3)
            prev = w['e']
    json.dump(tl, open(p, 'w'), indent=1)
    print(f'{tid}: aligned {len(tl["beats"]) - bad}/{len(tl["beats"])} beats')

if __name__ == '__main__':
    main(sys.argv[1])
