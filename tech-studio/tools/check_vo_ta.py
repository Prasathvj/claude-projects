"""Pre-render voice gate for Tamil episodes (same rule as check_vo.py: must print PASS before any render).
Per line: transcribe the line's own audio window with gemini-3.5-transcribe and let gemini-3.5-flash compare it with the
script (missing / extra / repeated words, English director notes read aloud). Between lines: no speech in the gaps.
Usage: python3 tools/check_vo_ta.py <timeline-id>"""
import io, json, os, re, sys, wave
import numpy as np
sys.path.insert(0, 'tools')
from gem_audio import gem
from align_ta import load, frames_db

tl = json.load(open(f'src/episodes/{sys.argv[1]}.timeline.json'))
x = load('public/' + tl['vo']); SR = 16000
fail = []


def wav_bytes(seg):
    b = io.BytesIO()
    with wave.open(b, 'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(seg, -1, 1) * 32767).astype('<i2').tobytes())
    return b.getvalue()


for k, bt in enumerate(tl['beats']):
    seg = x[int(max(0, bt['start'] - .05) * SR): int((bt['start'] + bt['vo'] + .05) * SR)]
    tr = gem(wav_bytes(seg), 'Transcribe this Tamil speech exactly in Tamil script (English words as spoken, numbers as digits). Output only the transcript.', os.environ.get('TR_MODEL', 'gemini-3.5-transcribe')).strip()
    q = ('You check a voice-over take against its script. Spelling variants of the same spoken word (e.g. ஸ்விட்சை / சுவிட்சை, '
         'numbers written as words or digits) are NOT errors. Report only real problems: words or phrases missing from the audio, '
         'extra or repeated words/phrases, words from a different line, or English director notes read aloud.\n'
         f'SCRIPT: {bt["text"]}\nTRANSCRIPT OF AUDIO: {tr}\n'
         'Reply with JSON only: {"ok": true|false, "problems": ["..."]}')
    r = gem(None, q, os.environ.get('JUDGE_MODEL', 'gemini-3.5-flash'))
    try: j = json.loads(re.search(r'\{.*\}', r, re.S).group(0))
    except Exception: j = {'ok': False, 'problems': ['unparsable: ' + r[:200]]}
    print(f"line {k + 1:2d} {'ok ' if j['ok'] else 'BAD'} | {tr}" + ('' if j['ok'] else f"\n         -> {j['problems']}"))
    if not j['ok']: fail.append(k + 1)
# speech in the gaps between lines (spill-over)
for a, b in zip(tl['beats'], tl['beats'][1:]):
    g0, g1 = a['start'] + a['vo'] + .03, b['start'] - .03
    if g1 - g0 > .05:
        db = frames_db(x[int(g0 * SR): int(g1 * SR)])
        if len(db) and db.max() > -38:
            print(f'speech between lines at {g0:.2f}-{g1:.2f} s ({db.max():.0f} dB)'); fail.append(f'gap {g0:.1f}')
print('PASS' if not fail else f'FAIL {fail}')
