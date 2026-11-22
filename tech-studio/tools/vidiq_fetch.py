"""Fetch a vidIQ voiceover job (scriptLines) into the per-line cache used by audio.py's 'vidiq' engine.
Usage: python3 tools/vidiq_fetch.py <episode-json> <result-json>   (result-json = the job result saved from vidiq_job_poll)
Lines are matched to the episode's beats by order, or by 'index' for a partial job (vidIQ takes at most 50 lines per call); each line becomes .cache/vidiq/<key>.wav (mono, audio.SR)."""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, 'tools')
import audio
ep = json.load(open(sys.argv[1])); res = json.load(open(sys.argv[2]))
res = res.get('result', res)
lines = res.get('lines') or [res]
texts = [b['text'] for b in ep['beats']] if len(lines) > 1 else [json.load(open(sys.argv[3]))['text'] if len(sys.argv) > 3 else None]
if len(lines) > 1 and all('index' in ln for ln in lines) and len(lines) != len(texts):
    pairs = [(ln, texts[ln['index']]) for ln in lines]   # partial job (scripts over 50 lines are split across calls)
else:
    assert len(lines) == len(texts) or len(sys.argv) > 3, (len(lines), len(texts))
    pairs = list(zip(lines, texts))
for ln, txt in pairs:
    dst = audio.vidiq_path(ep['voice'], txt)
    if dst.exists():
        continue
    tmp = dst.with_suffix('.mp3')
    subprocess.run(['curl', '-sS', '-f', '-o', str(tmp), ln['audioUrl']], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(tmp), '-ac', '1', '-ar', str(audio.SR), str(dst)], check=True)
    tmp.unlink()
print('cached', len(lines), 'lines')
