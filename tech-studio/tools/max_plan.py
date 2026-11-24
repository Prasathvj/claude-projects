"""Build Max's overlay plan (expressions per segment + lip-sync envelope) for hf/<project>/max_layer.html.
Usage: python3 tools/max_plan.py ep01-short  (segments are defined in SEGS below, keyed by project)"""
import json, subprocess, sys
import numpy as np

SEGS = {'robo01-short': [
    (4.46, 'duo', {"brows": "skeptic", "eyes": "squint", "arms": "chin", "extra": ["question"]}),
    (10.97, 'duo', {"brows": "high", "eyes": "wide", "mouth": "shock", "arms": "hands-up", "extra": ["bang"]}),
    (13.92, 'duo', {"brows": "up", "arms": "point", "look": [-1, -0.6]}),
    (19.32, 'duo', {"brows": "high", "eyes": "wide", "mouth": "shock", "arms": "hands-up", "extra": ["bang"]}),
    (22.16, 'duo', {"brows": "skeptic", "eyes": "squint", "arms": "chin", "extra": ["question"]}),
    (26.25, 'duo', {"brows": "up", "eyes": "happy", "mouth": "grin", "arms": "thumbs"}),
    (31.99, 'duo', {"brows": "up", "mouth": "smirk", "arms": "shrug", "tilt": -5}),
    (38.2, 'duo', {"brows": "up", "arms": "point", "look": [-1, -0.6]}),
    (99, 'duo', {"brows": "up", "eyes": "happy", "mouth": "grin", "arms": "thumbs"}),
], 'net01-short': [
    (8.21, 'duo', {"brows": "high", "eyes": "wide", "mouth": "shock", "arms": "hands-up", "extra": ["bang"]}),
    (12.67, 'duo', {"brows": "focused", "arms": "point", "look": [-1, -0.6]}),
    (15.62, 'duo', {"brows": "up", "mouth": "smirk", "arms": "shrug", "tilt": -5}),
    (23.3, 'duo', {"brows": "up", "arms": "point", "look": [-1, -0.6]}),
    (29.19, 'duo', {"brows": "worried", "eyes": "worried", "extra": ["sweat"]}),
    (33.91, 'duo', {"brows": "worried", "eyes": "worried", "extra": ["sweat"]}),
    (41.36, 'duo', {"brows": "high", "eyes": "wide", "mouth": "shock", "arms": "hands-up", "extra": ["bang"]}),
    (48.18, 'duo', {"brows": "focused", "arms": "point", "look": [-1, -0.6]}),
    (99, 'duo', {"brows": "up", "eyes": "happy", "mouth": "grin", "arms": "thumbs"}),
], 'goog01-short': [
    (5.64, 'duo', {"brows": "skeptic", "eyes": "squint", "arms": "chin", "extra": ["question"]}),
    (9.72, 'duo', {"brows": "up", "arms": "point", "look": [-1, -0.6]}),
    (14.19, 'duo', {"brows": "focused", "arms": "point", "look": [-1, -0.6]}),
    (16.95, 'duo', {"brows": "skeptic", "eyes": "squint", "arms": "chin", "extra": ["question"]}),
    (21.7, 'duo', {"brows": "focused", "arms": "point", "look": [-1, -0.6]}),
    (28.73, 'duo', {"brows": "high", "eyes": "wide", "mouth": "shock", "arms": "hands-up", "extra": ["bang"]}),
    (35.03, 'duo', {"brows": "up", "arms": "point", "look": [-1, -0.6]}),
    (40.51, 'duo', {"brows": "focused", "arms": "point", "look": [-1, -0.6]}),
    (47.2, 'duo', {"brows": "up", "mouth": "smirk", "arms": "shrug", "tilt": -5}),
    (99, 'duo', {"brows": "up", "eyes": "happy", "mouth": "grin", "arms": "thumbs"}),
], 'sat01-short': [
    (4.84, 'duo', {"brows": "skeptic", "eyes": "squint", "arms": "chin", "extra": ["question"]}),
    (9.94, 'duo', {"brows": "up", "arms": "point", "look": [-1, -0.6]}),
    (16.68, 'duo', {"brows": "focused", "arms": "point", "look": [-1, -0.6]}),
    (22.57, 'duo', {"brows": "skeptic", "eyes": "squint", "arms": "chin", "extra": ["question"]}),
    (26.68, 'duo', {"brows": "focused", "arms": "point", "look": [-1, -0.6]}),
    (33.17, 'duo', {"brows": "up", "arms": "point", "look": [-1, -0.6]}),
    (40.29, 'duo', {"brows": "high", "eyes": "wide", "mouth": "shock", "arms": "hands-up", "extra": ["bang"]}),
    (44.81, 'duo', {"brows": "worried", "eyes": "worried", "extra": ["sweat"]}),
    (51.02, 'duo', {"brows": "up", "eyes": "happy", "mouth": "grin", "arms": "thumbs"}),
    (99, 'duo', {"brows": "up", "eyes": "happy", "mouth": "grin", "arms": "thumbs"}),
], 'job03-short': [
    (6.84, 'duo', {"brows": "high", "eyes": "wide", "mouth": "shock", "arms": "hands-up", "extra": ["bang"]}),
    (11.32, 'duo', {"brows": "up", "arms": "point", "look": [-1, -0.6]}),
    (14.72, 'duo', {"brows": "focused", "arms": "chin"}),
    (16.94, 'duo', {"brows": "high", "eyes": "wide", "mouth": "shock"}),
    (20.44, 'duo', {"brows": "worried", "eyes": "worried"}),
    (24.09, 'duo', {"brows": "skeptic", "eyes": "squint", "mouth": "smirk", "arms": "chin", "extra": ["question"]}),
    (32.9, 'duo', {"brows": "skeptic", "mouth": "smirk", "arms": "shrug", "tilt": -5}),
    (99, 'duo', {"brows": "up", "eyes": "happy", "mouth": "smile", "arms": "point", "look": [-1, -0.3]}),
], 'job02-short': [
    (10.25, 'duo', {"brows": "skeptic", "eyes": "squint", "arms": "chin", "extra": ["question"]}),
    (13.6, 'duo', {"brows": "up", "arms": "point", "look": [-1, -0.6]}),
    (18.47, 'duo', {"brows": "up", "eyes": "happy", "arms": "thumbs"}),
    (24.68, 'duo', {"brows": "high", "eyes": "wide", "mouth": "shock", "extra": ["bang"]}),
    (29.45, 'duo', {"brows": "focused", "arms": "point", "look": [-1, -0.6]}),
    (31.65, 'duo', {"brows": "worried", "eyes": "worried", "extra": ["sweat"]}),
    (34.68, 'duo', {"brows": "skeptic", "mouth": "smirk", "arms": "shrug"}),
    (99, 'duo', {"brows": "up", "eyes": "happy", "mouth": "smile", "arms": "thumbs"}),
], 'job01-short': [
    (4.75, 'duo', {"brows": "skeptic", "eyes": "squint", "arms": "chin", "extra": ["question"]}),
    (9.27, 'duo', {"brows": "up", "arms": "point", "look": [-1, -0.6]}),
    (10.79, 'duo', {"brows": "focused", "arms": "chin", "look": [-1, -0.6]}),
    (14.1, 'duo', {"brows": "high", "eyes": "wide", "mouth": "shock", "arms": "hands-up"}),
    (17.25, 'duo', {"brows": "up", "eyes": "happy", "mouth": "grin", "arms": "thumbs"}),
    (21.79, 'duo', {"brows": "worried", "eyes": "worried", "extra": ["sweat"]}),
    (24.65, 'duo', {"brows": "up", "mouth": "smirk", "arms": "shrug", "tilt": -5}),
    (28.86, 'duo', {"brows": "up", "eyes": "happy", "mouth": "smile", "arms": "point", "look": [-1, -0.3]}),
    (99, 'duo', {"brows": "up", "eyes": "happy", "mouth": "grin", "arms": "thumbs"}),
], 'tip01-short': [
    (5.41, 'duo', {"brows": "worried", "eyes": "wide", "mouth": "shock", "arms": "hands-up", "extra": ["bang"]}),
    (9.19, 'duo', {"brows": "skeptic", "eyes": "squint", "mouth": "smirk", "arms": "chin", "look": [-1, -0.6]}),
    (14.33, 'duo', {"brows": "up", "arms": "point", "look": [-1, -0.6]}),
    (18.7, 'duo', {"brows": "focused", "arms": "thumbs"}),
    (24.34, 'duo', {"brows": "up", "arms": "point", "look": [-1, -0.6]}),
    (27.93, 'duo', {"brows": "skeptic", "eyes": "squint", "arms": "chin", "look": [-1, -0.6]}),
    (32.2, 'duo', {"brows": "worried", "eyes": "worried", "extra": ["sweat"], "look": [-1, -0.6]}),
    (99, 'duo', {"brows": "up", "eyes": "happy", "mouth": "smile", "arms": "thumbs"}),
], 'news02-short': [
    (6.38, 'duo', {"brows": "high", "eyes": "wide", "mouth": "shock", "arms": "hands-up", "extra": ["bang"]}),
    (10.4, 'duo', {"brows": "up", "arms": "point", "look": [-1, -0.6]}),
    (14.33, 'duo', {"brows": "up", "eyes": "happy", "mouth": "grin", "arms": "thumbs"}),
    (17.92, 'duo', {"brows": "high", "eyes": "wide", "mouth": "shock", "extra": ["bang"]}),
    (22.8, 'duo', {"brows": "up", "eyes": "open", "arms": "chin", "look": [-1, -0.6]}),
    (27.37, 'duo', {"brows": "up", "eyes": "happy", "mouth": "smile", "arms": "shrug", "tilt": -5}),
    (33.58, 'duo', {"brows": "skeptic", "eyes": "squint", "mouth": "smirk", "arms": "chin", "extra": ["question"], "look": [-1, -0.6]}),
    (37.02, 'duo', {"brows": "focused", "arms": "point", "look": [-1, -0.6]}),
    (99, 'duo', {"brows": "up", "eyes": "happy", "mouth": "smile", "arms": "point", "look": [-1, -0.3]}),
], 'news01-short': [
    (2.11, 'duo', {'brows': 'up', 'eyes': 'open', 'arms': 'point', 'look': [-1, -0.6]}),
    (5.98, 'duo', {'brows': 'high', 'eyes': 'wide', 'mouth': 'shock', 'arms': 'hands-up', 'extra': ['bang']}),
    (10.41, 'duo', {'brows': 'skeptic', 'eyes': 'squint', 'mouth': 'smirk', 'arms': 'chin', 'look': [-1, -0.6]}),
    (18.99, 'duo', {'brows': 'worried', 'eyes': 'worried', 'extra': ['sweat'], 'look': [-1, -0.6]}),
    (21.27, 'duo', {'brows': 'high', 'eyes': 'wide', 'mouth': 'shock', 'arms': 'facepalm', 'extra': ['bang']}),
    (24.7, 'duo', {'brows': 'up', 'eyes': 'happy', 'mouth': 'smile', 'arms': 'shrug', 'tilt': -5}),
    (27.67, 'duo', {'brows': 'focused', 'arms': 'point', 'look': [-1, -0.6]}),
    (33.16, 'duo', {'brows': 'skeptic', 'mouth': 'smirk', 'arms': 'chin', 'extra': ['question'], 'look': [-1, -0.6]}),
    (37.73, 'duo', {'brows': 'worried', 'eyes': 'worried', 'arms': 'facepalm', 'extra': ['sweat']}),
    (99, 'duo', {'brows': 'up', 'eyes': 'happy', 'mouth': 'smile', 'arms': 'point', 'look': [-1, -0.3]}),
], 'ep01-short': [  # (until word or seconds, mode, expression)
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


# batch-3 Shorts: one expression per beat (Max stays in 'duo' position), keyed by mood
EX = {'shock': {'brows': 'high', 'eyes': 'wide', 'mouth': 'shock', 'arms': 'hands-up', 'extra': ['bang']},
      'point': {'brows': 'up', 'arms': 'point', 'look': [-1, -0.6]},
      'think': {'brows': 'skeptic', 'eyes': 'squint', 'arms': 'chin', 'extra': ['question']},
      'focus': {'brows': 'focused', 'arms': 'point', 'look': [-1, -0.6]},
      'worry': {'brows': 'worried', 'eyes': 'worried', 'extra': ['sweat']},
      'shrug': {'brows': 'up', 'mouth': 'smirk', 'arms': 'shrug', 'tilt': -5},
      'happy': {'brows': 'up', 'eyes': 'happy', 'mouth': 'grin', 'arms': 'thumbs'}}
MOODS = {'upi01-short': 'shock think point focus think focus point happy shrug shock shock happy',
         'ai01-short': 'think shock point focus focus shrug point shock think focus worry happy',
         'del01-short': 'shock think focus point focus worry point focus shock point happy',
         'face01-short': 'shock point focus shrug focus point shock focus worry happy happy',
         'pay01-short': 'think happy shock worry point happy',
         'swe01-short': 'shock think happy worry think shock point happy',
         'qnt01-short': 'shock shock think point think point happy',
         'lst01-short': 'shock think point shock think point happy',
         # ast01 (owner 2026-11-23: 'add max only required place'): Max only at the reveal, 'can't find it', the scam and the outro
         # mh01 (Tech Mysteries Short): Max only at 'Gone', the open question and the outro
         'mh01-short': 'off off off off worry off off off off off think happy',
         'mh01ta-short': 'off off off off worry off off off off off think happy',
         'news02ta-short': 'shock point happy shock think shrug think focus happy happy',
         'news01ta-short': 'point shock think worry shock shrug focus think worry happy',
         'ast01-short': 'off shock think off off off off off off worry happy'}

# automatic host acting for long videos: expression from each beat's visual type and delivery note
AUTO = {'slam': {'brows': 'up', 'arms': 'point', 'look': [-1, 0]}, 'quote': {'brows': 'focused', 'arms': 'chin', 'look': [-1, 0]},
        'checklist': {'brows': 'up', 'eyes': 'happy', 'arms': 'point', 'look': [-1, -0.2]}, 'end': {'brows': 'up', 'eyes': 'happy', 'mouth': 'smile', 'arms': 'thumbs'},
        'nolist': {'brows': 'skeptic', 'arms': 'shrug'}, 'memory': {'brows': 'worried', 'eyes': 'worried', 'look': [-1, 0]},
        'email': {'brows': 'skeptic', 'eyes': 'squint', 'arms': 'chin', 'look': [-1, 0]}, 'code': {'brows': 'focused', 'arms': 'chin', 'look': [-1, 0]},
        'split': {'brows': 'neutral', 'arms': 'point', 'look': [-1, 0]}, 'loop': {'brows': 'up', 'arms': 'point', 'look': [-1, 0]}}
MOOD = [('dark|ominous|creepy|grave|unsettling', {'brows': 'worried', 'eyes': 'worried', 'extra': ['sweat']}),
        ('twist', {'brows': 'high', 'eyes': 'wide', 'mouth': 'shock', 'arms': 'hands-up', 'extra': ['bang']}),
        ('curious|question', {'brows': 'skeptic', 'arms': 'chin', 'extra': ['question']}),
        ('warm|friendly|helpful|energetic', {'brows': 'up', 'eyes': 'happy', 'mouth': 'smile'})]

def auto(tl):
    import re
    segs, B = [], tl['beats']
    for i, b in enumerate(B):
        t0 = 0.0 if i == 0 else round(b['start'] - 0.12, 3)
        t1 = round(B[i + 1]['start'] - 0.12, 3) if i + 1 < len(B) else 9999
        o = dict(AUTO.get(b['v']['type'], {'brows': 'neutral', 'look': [-1, 0]}))
        if b['v']['type'] == 'agent' and b['v'].get('mode') == 'hijack':
            o = {'brows': 'high', 'eyes': 'wide', 'mouth': 'shock', 'arms': 'facepalm' if i % 2 else 'hands-up', 'extra': ['bang']}
        for pat, ex in MOOD:
            if re.search(pat, b.get('dir', '')):
                o = {**o, **ex}; break
        segs.append((t1, 'host' if i in HOSTB else 'off', o))
    return segs

pid = sys.argv[1]
tl = json.load(open(f'src/episodes/{pid}.timeline.json'))
if pid in MOODS:
    mm = MOODS[pid].split(); bb = tl['beats']
    SEGS[pid] = [(round(bb[i + 1]['start'] - 0.12, 3) if i + 1 < len(bb) else 99, 'off' if mm[min(i, len(mm) - 1)] == 'off' else 'duo',
                  EX.get(mm[min(i, len(mm) - 1)], {'brows': 'neutral'})) for i in range(len(bb))]
if pid not in SEGS:
    ep = json.load(open(f'episodes/{pid.split("-")[0]}/{pid.split("-")[1]}.json'))
    for b, e in zip(tl['beats'], ep['beats']):
        b['v'] = e['v']; b['dir'] = e.get('dir', '')
    HOSTB = set(ep.get('host_beats', range(len(ep['beats']))))
    SEGS[pid] = auto(tl)
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
