"""Fetch a vidIQ voiceover job (scriptLines) into the per-line cache used by audio.py's 'vidiq' engine.
Usage: python3 tools/vidiq_fetch.py <episode-json> <result-json>   (result-json = the job result saved from vidiq_job_poll)
Lines are matched to the episode's beats by order; each line becomes .cache/vidiq/<key>.wav (mono, audio.SR)."""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, 'tools')
import audio
ep = json.load(open(sys.argv[1])); res = json.load(open(sys.argv[2]))
res = res.get('result', res)
lines = res.get('lines') or [res]
texts = [b['text'] for b in ep['beats']] if len(lines) > 1 else [json.load(open(sys.argv[3]))['text'] if len(sys.argv) > 3 else None]
assert len(lines) == len(texts) or len(sys.argv) > 3, (len(lines), len(texts))
for ln, txt in zip(lines, texts):
    dst = audio.vidiq_path(ep['voice'], txt)
    if dst.exists():
        continue
    tmp = dst.with_suffix('.mp3')
    subprocess.run(['curl', '-sS', '-f', '-o', str(tmp), ln['audioUrl']], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(tmp), '-ac', '1', '-ar', str(audio.SR), str(dst)], check=True)
    tmp.unlink()
print('cached', len(lines), 'lines')
