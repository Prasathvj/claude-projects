"""Move a beat boundary inside the existing narration (audio untouched; only which visual is on screen changes).
Usage: python3 tools/retime.py <id> <beat_index_of_second_beat> <first_ends_s> <second_starts_s>"""
import json, sys
sys.path.insert(0, 'tools'); import audio
tid, k, a_end, b_start = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
p = f'src/episodes/{tid}.timeline.json'; tl = json.load(open(p))
A, B = tl['beats'][k - 1], tl['beats'][k]
b_end = B['start'] + B['vo']
A['vo'] = round(a_end - A['start'], 3); A['dur'] = round(b_start - A['start'], 3)
B['vo'] = round(b_end - b_start, 3); B['dur'] = round(B['dur'] + (B['start'] - b_start), 3); B['start'] = round(b_start, 3)
A['words'] = audio.words_timing(A['text'], A['vo']); B['words'] = audio.words_timing(B['text'], B['vo'])
json.dump(tl, open(p, 'w'), indent=1)
print(k - 1, A['start'], A['vo'], '|', k, B['start'], B['vo'])
