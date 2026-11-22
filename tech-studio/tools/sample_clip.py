"""Make a short sample project from hf/ep01-long (first N seconds) for theme/background previews.
Usage: THEME=cream GRID=dots python3 tools/sample_clip.py <out_dir> [seconds]"""
import re, shutil, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
out = Path(sys.argv[1]); secs = float(sys.argv[2]) if len(sys.argv) > 2 else 20.0
subprocess.run([sys.executable, str(ROOT / 'tools/hf_ep01_long.py')], check=True, capture_output=True)
src = ROOT / 'hf/ep01-long'
if out.exists(): shutil.rmtree(out)
out.mkdir(parents=True)
for f in ('compositions', 'assets'):
    shutil.copytree(src / f, out / f, ignore=shutil.ignore_patterns('max_plan.json'))
for f in ('hyperframes.json', 'meta.json', 'package.json'):
    if (src / f).exists(): shutil.copy(src / f, out / f)
html = (src / 'index.html').read_text()
keep = []
for line in html.split('\n'):
    m = re.search(r'data-start="([\d.]+)"', line)
    if m and 'id="root"' not in line and float(m.group(1)) >= secs:
        continue
    keep.append(line)
html = '\n'.join(keep)
html = re.sub(r'(id="root"[^>]*data-duration=")[\d.]+', rf'\g<1>{secs}', html)
html = re.sub(r'(id="(?:bg|chapters|caps\d|vo|bgm)"[^>]*data-duration=")[\d.]+', rf'\g<1>{secs}', html)
(out / 'index.html').write_text(html)
print('sample project', out)
