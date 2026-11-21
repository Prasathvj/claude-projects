"""Render one still per beat (at 65% of the beat) and tile them into a contact sheet for review.
Usage: python3 tools/sheet.py <CompositionId> [frac]"""
import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
comp = sys.argv[1]; frac = float(sys.argv[2]) if len(sys.argv) > 2 else 0.65
tl = json.loads((ROOT / "src/episodes" / f"{comp}.timeline.json").read_text())
out = ROOT / "out" / "stills" / comp; out.mkdir(parents=True, exist_ok=True); (out / "sheet.png").unlink(missing_ok=True)
frames = [int((b["start"] + b["dur"] * frac) * 30) for b in tl["beats"]]
procs = []
# one bundle, many stills: use remotion's --frame for each (bundling cached by remotion)
for i, f in enumerate(frames):
    subprocess.run(["npx", "remotion", "still", "src/index.ts", comp, str(out / f"{i:03d}.png"), f"--frame={f}", "--scale=0.25",
                    "--browser-executable=/opt/pw-browsers/chromium", "--log=error"], cwd=ROOT, check=True)
cols = 7 if tl["format"] == "vertical" else 5
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-pattern_type", "glob", "-i", str(out / "*.png"), "-vf",
                f"tile={cols}x{(len(frames) + cols - 1) // cols}:padding=6:color=white", "-frames:v", "1", str(out / "sheet.png")], check=True)
print(out / "sheet.png")
