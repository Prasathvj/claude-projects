"""Tamil narration for tamil-test episodes (2026-11-24): reuses tools/audio.py, with a Tamil narrator profile and a
pace check that measures characters per second instead of English words per minute (Tamil words are long, so the
English 85-250 wpm check would reject good takes and burn the 10-request daily quota).
Usage: python3 tools/tamil_audio.py episodes/tamil01/short.json"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import audio
from stickgen import gtts

audio.PROFILES['tamil'] = ("# AUDIO PROFILE: A native Tamil (Chennai) male narrator of punchy tech YouTube Shorts. Speaks natural, "
                           "conversational spoken Tamil, says English tech words (server, code, software, market) the way Tamil "
                           "speakers do, reads numbers in Tamil. Confident storyteller, crisp, natural breaths, never robotic.\n")
audio.TARGET_WPM['tamil'] = 1  # no speed-up (max_tempo 1.0)
audio.PROFILES['tamil-mystery'] = ("# AUDIO PROFILE: A native Tamil (Chennai) male narrator of a true-crime tech mystery documentary. "
                                   "Speaks natural, conversational spoken Tamil, says English tech words (flight, radar, satellite, ping) the way "
                                   "Tamil speakers do, reads numbers in Tamil. Low, calm and controlled, slightly hushed, with short dramatic "
                                   "pauses; respectful, never theatrical or robotic.\n")
audio.TARGET_WPM['tamil-mystery'] = 1


def say_batch_ta(lines, voice="Orus", model=gtts.MODEL, profile="", keep_partial=False):
    if isinstance(model, (list, tuple)):
        model = model[0]
    gtts.CACHE.mkdir(parents=True, exist_ok=True)
    bkey = gtts._key([model, voice, profile, lines])
    paths = [gtts.CACHE / f"b{bkey}_{i}.wav" for i in range(len(lines))]
    if all(p.exists() for p in paths):
        return [(p, gtts.wav_duration(p)) for p in paths]
    tones = "\n".join(f"- Take {i + 1}: {d or 'clear and natural'}" for i, (_, d) in enumerate(lines))
    prompt = (f"{profile}# DIRECTOR'S NOTES\nThis is {len(lines)} separate takes in Tamil, read in order. After each take, stay "
              f"completely silent for three full seconds before the next one. Keep the same steady pace in every take. "
              f"Read only the Tamil transcript; never read these English notes aloud.\n"
              f"Tone of each take:\n{tones}\n# TRANSCRIPT\n" + "\n\n".join(t for t, _ in lines))
    last = ""
    for attempt in range(2):
        try:
            takes = gtts._split(gtts._call(model, prompt, voice), len(lines), [len(t) for t, _ in lines])
        except ValueError as e:
            last = str(e); print('   split failed:', e); continue
        for p, pcm in zip(paths, takes):
            gtts._write_trimmed(pcm, p)
        cps = [len(t) / gtts.wav_duration(p) for (t, _), p in zip(lines, paths)]
        print('   chars/s per take:', [round(c, 1) for c in cps])
        bad = [i + 1 for i, c in enumerate(cps) if not 6 <= c <= 30]
        if not bad:
            return [(p, gtts.wav_duration(p)) for p in paths]
        last = f"takes {bad} look cut or merged"
        for p in paths:
            p.unlink(missing_ok=True)
    raise ValueError(f"Tamil batch failed: {last}")


gtts.say_batch = say_batch_ta
audio.episode(sys.argv[1])
