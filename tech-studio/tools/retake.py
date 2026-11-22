"""Re-record single narration lines (one request each) and splice them into an existing take.
Usage: python3 tools/retake.py <episode-dir> <beat> [<beat> ...]   then re-run align.py + verify_vo.py
Saves whatever was re-recorded even if the daily quota runs out part-way (cached takes cost nothing next time)."""
import json, os, sys
import numpy as np
sys.path.insert(0, 'tools')
import audio

k, idx = sys.argv[1], sorted(int(x) for x in sys.argv[2:])
k = k.rstrip('/').split('/')[-1]
epf = f'episodes/{k}/short.json' if os.path.exists(f'episodes/{k}/short.json') else f'episodes/{k}/long.json'
ep = json.load(open(epf))
audio.lock_model(ep)
tp = f"src/episodes/{ep['id']}.timeline.json"
t = json.load(open(tp)); sr = audio.SR
x = audio.read('public/' + t['vo'])
done = []
try:
    for i in reversed(idx):   # back to front so earlier offsets stay valid
        b = ep['beats'][i]
        if ep.get('engine') == 'vidiq':
            new = audio.read(audio.vidiq_path(ep['voice'], b['text']))
        elif ep.get('engine') == 'kokoro':
            new = audio.read(audio.kokoro_say(b['text'], ep['voice'], ep.get('speed', 0.95)))
        else:
            p, _ = audio.gtts.say(b['text'], b.get('dir', '') + '; read this line exactly once', voice=ep.get('voice', 'Orus'),
                                  model=audio.MODELS, profile=audio.PROFILES[ep.get('profile', 'fast')])
            new = audio.read(audio.gtts.clean(p)[0])
        tb = t['beats'][i]; a0, a1 = int(tb['start'] * sr), int((tb['start'] + tb['vo']) * sr)
        d = len(new) / sr - tb['vo']
        x = np.concatenate([x[:a0], new, x[a1:]])
        tb['vo'] = round(len(new) / sr, 3); tb['dur'] = round(tb['dur'] + d, 3)
        tb['words'] = audio.words_timing(tb['text'], tb['vo'])
        for nb in t['beats'][i + 1:]:
            nb['start'] = round(nb['start'] + d, 3)
        t['duration'] = round(t['duration'] + d, 3)
        done.append(i)
        print(f'beat {i}: {len(new) / sr:.2f}s (was {len(new) / sr - d:.2f}s)')
except audio.gtts.DailyQuota as e:
    print('quota reached; saved beats', done, '-', e)
audio.write('public/' + t['vo'], x)
json.dump(t, open(tp, 'w'), indent=1)
print('total', t['duration'])
