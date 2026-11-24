"""Word timing for Tamil narration (no Tamil forced-aligner model is reachable here, 2026-11-24).
Inside each line's own audio window: find the voiced span and the pauses, snap every punctuation boundary
(. , : ?) to the nearest real pause, then share each phrase's time between its words by Tamil syllable weight
(consonant+vowel = 1, consonant+pulli = 0.5, long vowel +0.4, numbers by their spoken Tamil length) and snap
inner word boundaries to short pauses when one is close.  Good enough for 1-3 word captions.
Usage: python3 tools/align_ta.py <timeline-id>"""
import json, re, subprocess, sys
import numpy as np

NUMW = {'45': 5, '460': 7, '1': 3, '2012': 9, '2003': 7, '8:01': 6, '97': 5, '9:30': 5, '154': 7, '40': 3, '4,000': 4, '4000': 4, '400': 3, '1:21': 8, '239': 11, '8': 2, '2014': 9, '370': 7, '2015': 9, '2026': 10, '83': 5, '7,700': 8, '80': 3, '7': 2, '1.5': 6, '2023': 9, '34': 5, '17': 4}
LONG = set('ாீூேைோௌ')


def weight(w):
    core = re.sub(r'[.,:;?!]+$', '', w)
    m = re.match(r'^([0-9][0-9,:]*)(.*)$', core)
    k = 0.0
    if m:
        k += NUMW.get(m.group(1).rstrip(','), max(2, len(m.group(1))))
        core = m.group(2)
    lat = re.sub(r'[^a-zA-Z]', '', core)
    if lat:
        k += max(1, len(re.findall(r'[aeiouy]+', lat.lower())))
    for i, c in enumerate(core):
        o = ord(c)
        if 0x0B95 <= o <= 0x0BB9:
            k += 0.5 if i + 1 < len(core) and core[i + 1] == '்' else 1
        elif 0x0B85 <= o <= 0x0B94:
            k += 1
        elif c in LONG:
            k += 0.4
    return max(k, 0.5) + (0.5 if re.search(r'[.,:;?!]$', w) else 0)


def load(p, sr=16000):
    r = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', p, '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(r, np.float32)


def frames_db(x, sr=16000, hop=0.01):
    n = int(sr * hop); m = len(x) // n
    e = np.sqrt((x[:m * n].reshape(m, n) ** 2).mean(1) + 1e-12)
    return 20 * np.log10(e)


def pauses(voiced, minlen):
    out, i = [], 0
    while i < len(voiced):
        if not voiced[i]:
            j = i
            while j < len(voiced) and not voiced[j]: j += 1
            if j - i >= minlen: out.append((i, j))
            i = j
        else: i += 1
    return out


def align_line(text, x, sr=16000):
    db = frames_db(x, sr); thr = max(-45, np.percentile(db, 95) - 32); v = db > thr
    idx = np.where(v)[0]
    a, b = (idx[0], idx[-1] + 1) if len(idx) else (0, len(db))
    inner = v[a:b]
    P = [(s + a, e + a) for s, e in pauses(inner, 13)]       # >= 130 ms pauses
    p_small = [(s + a, e + a) for s, e in pauses(inner, 6)]  # >= 60 ms
    ws = text.split(); W = [weight(w) for w in ws]; cum = np.concatenate([[0], np.cumsum(W)]) / sum(W)
    bounds = [(i, cum[i + 1]) for i, w in enumerate(ws[:-1]) if re.search(r'[.,:;?!]$', w)]
    cuts = {}   # word index -> (end of word i, start of word i+1) in frames
    used, last = set(), a
    for i, frac in bounds:
        e = a + frac * (b - a)
        cand = [(abs((s + t) / 2 - e) - 0.3 * (t - s), k) for k, (s, t) in enumerate(P) if k not in used and s >= last and abs((s + t) / 2 - e) < 0.3 * (b - a)]
        if cand:
            _, k = min(cand); used.add(k); cuts[i] = P[k]; last = P[k][1]
    # phrases between cuts
    out = [None] * len(ws)
    edges = [-1] + sorted(cuts) + [len(ws) - 1]
    for q in range(len(edges) - 1):
        i0, i1 = edges[q] + 1, edges[q + 1]
        t0 = cuts[edges[q]][1] if edges[q] in cuts else a
        t1 = cuts[i1][0] if i1 in cuts else b
        sub = W[i0:i1 + 1]; c = np.concatenate([[0], np.cumsum(sub)]) / sum(sub)
        bt = [t0 + f * (t1 - t0) for f in c]
        for j in range(1, len(bt) - 1):   # snap to a nearby short pause
            near = [(abs((s + t) / 2 - bt[j]), s, t) for s, t in p_small if t0 < s and t < t1 and abs((s + t) / 2 - bt[j]) < 25]
            if near: bt[j] = min(near)[1:]
        for j in range(len(sub)):
            s = bt[j][1] if isinstance(bt[j], tuple) else bt[j]
            e = bt[j + 1][0] if isinstance(bt[j + 1], tuple) else bt[j + 1]
            out[i0 + j] = {'w': ws[i0 + j], 's': round(s * .01, 3), 'e': round(max(e, s + 5) * .01, 3)}
    return out


if __name__ == '__main__':
    tid = sys.argv[1]
    p = f'src/episodes/{tid}.timeline.json'; tl = json.load(open(p))
    x = load('public/' + tl['vo'])
    for bt in tl['beats']:
        seg = x[int(bt['start'] * 16000): int((bt['start'] + bt['vo']) * 16000)]
        bt['words'] = align_line(bt['text'], seg)
        print(f"{bt['start']:6.2f}", ' '.join(f"{w['w']}@{bt['start'] + w['s']:.2f}" for w in bt['words']))
    json.dump(tl, open(p, 'w'), indent=1, ensure_ascii=False)
