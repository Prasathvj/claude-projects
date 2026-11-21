"""Export an episode timeline to the motion engine: data/lyrics.json, data/audio.json and audio/mix.wav
(narration + synthesized SFX on the template cues + quiet music bed, SFX ducked under the voice).
Usage: python3 tools/motion_export.py <timeline-id>   -> motion/episodes/<id>/"""
import json, math, sys, wave
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent)); import audio as A

ROOT = Path(__file__).resolve().parent.parent
SR = A.SR

def cues(beats):
    """(time, sfx, gain) for every beat, matched to the motion templates' timings."""
    out = []
    for i, b in enumerate(beats):
        s, d, v, tr = b['cut'], b['end'] - b['cut'], b['v'], b.get('trans', '')
        T = v['type']; add = lambda dt, n, g=0.8: out.append((s + dt, n, g))
        if tr == 'rip': add(0, 'rip', 0.9)
        if tr == 'whip': add(0, 'whoosh', 0.9)
        if tr == 'punch': add(0, 'impact', 0.6)
        if T == 'slam':
            for j, _ in enumerate(v['text'].split()): add(0.03 + j * 0.11, 'impact' if j == 0 else 'pop', 0.7 if j == 0 else 0.5)
        elif T == 'chapter': add(0, 'scan', 0.5); add(0.05, 'impact', 0.7)
        elif T == 'quote': add(0.02, 'thud', 0.7); add(b['a0'] + 0.05, 'type', 0.35)
        elif T == 'browser':
            add(0, 'scan', 0.4)
            if v.get('reveal'): add(d * 0.3, 'click', 0.7); add(d * 0.3 + 0.12, 'glitch', 0.6)
        elif T == 'email': add(0, 'scan', 0.4); add(0.3, 'notify', 0.6); add(d * 0.45, 'error', 0.5)
        elif T == 'chat':
            n = len(v['msgs'])
            for j in range(n): add(0.3 + j * max(0.5, (d - 0.6) / (n + 0.5)), 'notify', 0.6)
        elif T == 'code':
            add(0, 'scan', 0.4)
            for j in range(int(max(1, (d * 0.8 - 0.35) / 0.9))): add(0.35 + j * 0.9, 'type', 0.45)
            if any(l.get('c') == 'hot' for l in v['lines']): add(d * 0.7, 'error', 0.45)
        elif T == 'agent':
            m = v['mode']
            if m == 'hijack': add(0, 'glitch', 0.7); add(0.1, 'error', 0.6); add(0.25, 'impact', 0.8)
            elif m == 'memory': add(0.1, 'scan', 0.4); add(d * 0.5, 'glitch', 0.6)
            else: add(0.3, 'scan', 0.6)
        elif T == 'rank':
            n = len(v['items'])
            for j in range(n): add(0.1 + (n - 1 - j) * 0.14, 'pop' if j else 'ding', 0.5 if j else 0.6)
        elif T == 'counter':
            for j in range(10): add(0.08 + 0.67 * (j / 10) ** 1.6, 'tick', 0.45)
            add(0.75, 'impact', 0.7)
        elif T == 'receipt':
            add(0, 'print', 0.5)
            for j in range(len(v['items'])): add(0.25 + j * 0.12, 'click', 0.5)
            add(0.35 + len(v['items']) * 0.12, 'impact', 0.7)
        elif T == 'stack':
            n = len(v['items'])
            for j in range(n): add(0.15 + j * max(0.12, (d - 0.6) / n) + 0.2, 'thud', 0.5)
        elif T == 'icons':
            for j in range(len(v['items'])): add(0.05 + j * 0.23, 'pop', 0.6)
        elif T == 'flow':
            for j in range(len(v['nodes'])): add(0.05 + j * 0.3, 'pop', 0.55)
            add(0.25, 'whoosh', 0.35)
        elif T == 'loop':
            for j in range(int(max(0, d - 0.3) / 0.45)): add(0.3 + j * 0.45, 'tick', 0.45)
        elif T == 'split':
            add(0.05, 'pop', 0.55); add(0.3, 'pop', 0.55)
            if v.get('merge'): add(d * 0.5, 'thud', 0.8)
            if v.get('bad'): add(0.45, 'error', 0.4)
        elif T == 'timeline':
            for j in range(len(v['events'])): add(0.2 + j * 0.25, 'tick', 0.6)
        elif T == 'paper': add(0, 'print', 0.4); add(0.5, 'scan', 0.4)
        elif T == 'trifecta':
            if v['show'] == 0: add(0.05, 'scan', 0.5)
            else: add(0.02, 'pop', 0.6)
            if v.get('danger'): add(0.05, 'error', 0.6)
            if v.get('cut') is not None: add(0.25, 'snip', 0.9); add(0.45, 'ding', 0.6)
        elif T == 'ruleoftwo':
            for j in range(3): add(0.15 + j * 0.2 + 0.15, 'click', 0.6)
            add(d * 0.6, 'error', 0.45)
        elif T == 'checklist': add(0.15, 'snip', 0.5); add(0.4, 'ding', 0.5)
        elif T == 'tease': add(0, 'riser', 0.6); add(0.45, 'ding', 0.6)
        elif T == 'end': add(0.05, 'pop', 0.5)
    return out

def main(tid):
    tl = json.loads((ROOT / 'src/episodes' / f'{tid}.timeline.json').read_text())
    beats = tl['beats']
    # cut in the pause before each line (never after its first word)
    for i, b in enumerate(beats):
        if i == 0: b['cut'] = 0.0; continue
        prev = beats[i - 1]; gap = b['start'] - (prev['start'] + prev['vo'])
        b['cut'] = round(b['start'] - min(0.18, max(0.04, gap * 0.45)), 3)
    for i, b in enumerate(beats):
        b['end'] = beats[i + 1]['cut'] if i + 1 < len(beats) else tl['duration']
        b['a0'] = b['start'] - b['cut']
    out = ROOT / 'motion/episodes' / tid
    (out / 'data').mkdir(parents=True, exist_ok=True); (out / 'audio').mkdir(parents=True, exist_ok=True)
    lines = []
    for b in beats:
        lines.append({'text': b['text'], 'start': b['start'], 'end': round(b['start'] + b['vo'], 3), 'cut': b['cut'],
                      'v': b['v'], 'trans': b.get('trans', ''),
                      'words': [{'w': w['w'], 'start': round(b['start'] + w['s'], 3), 'end': round(b['start'] + w['e'], 3)} for w in b['words']]})
    (out / 'data/lyrics.json').write_text(json.dumps({'source': 'tech-studio', 'lines': lines}, indent=1))
    vo = A.read(ROOT / 'public' / tl['vo'])
    dur = tl['duration']; n = int(dur * SR)
    vo = np.pad(vo, (0, max(0, n - len(vo))))[:n]
    # analysis: 100 fps envelopes
    hop = SR // 100; m = n // hop
    rms = np.sqrt((vo[:m * hop].reshape(m, hop) ** 2).mean(1)); rms = (rms / (rms.max() + 1e-9)).round(4).tolist()
    au = {'duration': round(dur, 3), 'bpm': 120.0, 'fps': 100, 'beats': [round(i * 0.5, 3) for i in range(int(dur * 2) + 1)],
          'downbeats': [round(i * 2.0, 3) for i in range(int(dur / 2) + 1)], 'sections': [],
          'features': {k: rms for k in ('rms', 'vocal', 'mid')}, 'onsets': {}}
    (out / 'data/audio.json').write_text(json.dumps(au))
    # mix
    sfx = np.zeros(n)
    lib = {p.stem: A.read(p) for p in (ROOT / 'public/sfx').glob('*.wav')}
    for t, name, g in cues(beats):
        x = lib[name]; i = int(t * SR)
        if 0 <= i < n: sfx[i:i + len(x)] += x[:n - i] * g
    env = np.repeat(np.array(rms), hop); env = np.pad(env, (0, n - len(env)))
    k = np.ones(int(0.15 * SR)) / int(0.15 * SR); env = np.convolve(env, k, 'same')
    duck = 1 - 0.55 * np.clip(env * 3, 0, 1)
    music = A.music(dur)[:n] * 0.10
    mix = vo * 1.0 + sfx * 0.55 * duck + music * duck
    mix = mix / (np.abs(mix).max() + 1e-9) * 0.95
    A.write(out / 'audio/mix.wav', mix)
    print(f'{tid}: {len(lines)} lines, {dur:.1f} s, {len(cues(beats))} sfx cues -> {out.relative_to(ROOT)}')

if __name__ == '__main__':
    main(sys.argv[1])
