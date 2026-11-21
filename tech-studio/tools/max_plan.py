"""Build Max's overlay plan (expressions per segment + lip-sync envelope) for hf/<project>/max_layer.html.
Usage: python3 tools/max_plan.py ep01-short  (segments are defined in SEGS below, keyed by project)"""
import json, subprocess, sys
import numpy as np

SEGS = {'ep01-short': [  # (until word or seconds, mode, expression)
    (2.2, 'duo', {'brows': 'up', 'arms': 'point', 'look': [-1, -0.6]}),
    (4.5, 'duo', {'brows': 'skeptic', 'eyes': 'squint', 'mouth': 'smirk', 'look': [-1, -0.4], 'tilt': -5}),
    (7.3, 'duo', {'brows': 'neutral', 'arms': 'chin', 'look': [-1, -0.8]}),
    (9.4, 'duo', {'brows': 'worried', 'eyes': 'worried', 'extra': ['sweat'], 'look': [-1, -0.6]}),
    (10.2, 'duo', {'brows': 'high', 'eyes': 'wide', 'mouth': 'shock', 'arms': 'hands-up', 'extra': ['bang']}),
    (13.5, 'duo', {'brows': 'skeptic', 'eyes': 'squint', 'arms': 'chin', 'look': [-1, -0.8]}),
    (15.85, 'duo', {'brows': 'focused', 'arms': 'point', 'look': [-1, -0.7]}),
    (18.17, 'duo', {'brows': 'up', 'eyes': 'open', 'mouth': 'grin', 'arms': 'thumbs', 'look': [-1, -0.5]}),
    (22.8, 'duo', {'brows': 'worried', 'eyes': 'worried', 'arms': 'shrug', 'look': [-1, -0.6]}),
    (25.5, 'duo', {'brows': 'focused', 'arms': 'point', 'look': [-1, -0.8]}),
    (27.9, 'duo', {'brows': 'worried', 'eyes': 'worried', 'extra': ['sweat'], 'look': [-1, -0.6]}),
    (29.8, 'duo', {'brows': 'worried', 'eyes': 'closed', 'mouth': 'flat', 'arms': 'facepalm', 'tilt': 8}),
    (32.0, 'duo', {'brows': 'skeptic', 'mouth': 'flat', 'arms': 'shrug', 'tilt': -4}),
    (99, 'duo', {'brows': 'up', 'eyes': 'happy', 'mouth': 'smile', 'arms': 'point', 'look': [-1, -0.3]}),
]}

pid = sys.argv[1]
tl = json.load(open(f'src/episodes/{pid}.timeline.json'))
B = tl['beats']; dur = tl['duration'] + float(sys.argv[2] if len(sys.argv) > 2 else 0)
segs, t0 = [], 0.0
for until, mode, o in SEGS[pid]:
    t1 = min(until, dur); segs.append({'t0': t0, 't1': t1, 'mode': mode, 'o': o}); t0 = t1
words = [(b['start'] + w['s'], b['start'] + w['e']) for b in B for w in b['words']]
raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', f"hf/{pid}/assets/vo.wav", '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
x = np.frombuffer(raw, dtype=np.int16).astype(float) / 32768; fps = 30; hop = 16000 // fps; m = len(x) // hop
env = np.sqrt((x[:m * hop].reshape(m, hop) ** 2).mean(1)); env = np.clip(env / np.percentile(env, 98), 0, 1)
zc = [float(np.mean(np.abs(np.diff(np.sign(x[i * hop:(i + 1) * hop]))))) / 2 for i in range(m)]
json.dump({'fps': fps, 'dur': dur, 'env': env.round(3).tolist(), 'zc': [round(z, 3) for z in zc], 'words': words, 'segs': segs},
          open(f'hf/{pid}/assets/max_plan.json', 'w'))
print(len(segs), 'segs', dur)
