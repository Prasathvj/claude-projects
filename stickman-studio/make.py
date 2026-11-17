#!/usr/bin/env python3
"""Build a long video, a Short, a thumbnail and upload metadata from one script file.

    python make.py scripts/why-you-procrastinate.json
    python make.py scripts/foo.json --only short --tts espeak
"""
import argparse
import json
import sys
from pathlib import Path

from stickgen import render, rig
from stickgen.icons import ICONS

ROOT = Path(__file__).resolve().parent


def check(script):
    """Catch script mistakes before spending time on rendering."""
    problems = []
    for part, scenes in (("scenes", script.get("scenes", [])), ("short", script.get("short", {}).get("scenes", []))):
        for i, sc in enumerate(scenes, 1):
            where = f"{part}[{i}]"
            if not sc.get("say", "").strip():
                problems.append(f"{where}: missing 'say'")
            if sc.get("action", "talk") not in rig.ACTIONS:
                problems.append(f"{where}: unknown action '{sc['action']}' (use: {', '.join(rig.ACTIONS)})")
            if sc.get("icon") and sc["icon"] not in ICONS:
                problems.append(f"{where}: unknown icon '{sc['icon']}' (use: {', '.join(ICONS)})")
    if not script.get("scenes"):
        problems.append("no scenes")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--only", choices=["long", "short"])
    ap.add_argument("--tts", default="auto", choices=["auto", "edge", "espeak"])
    ap.add_argument("--voice", default="en-US-AndrewNeural", help="edge-tts voice name")
    ap.add_argument("--rate", default="+5%", help="speaking rate, e.g. +10%%")
    args = ap.parse_args()

    path = Path(args.script)
    script = json.loads(path.read_text())
    problems = check(script)
    if problems:
        sys.exit("Script problems:\n  " + "\n  ".join(problems))

    out = ROOT / "output" / path.stem
    out.mkdir(parents=True, exist_ok=True)
    accent = script.get("accent", "#FFC233")
    voice = dict(voice=args.voice, rate=args.rate, backend=args.tts)
    music = next(iter(sorted((ROOT / "assets").glob("music.*"))), None)
    meta = dict(title=script["title"], description=script.get("description", ""), tags=script.get("tags", []))

    if args.only != "short":
        info = render.render(script["scenes"], "long", out / "long.mp4", accent, voice, music)
        print(f"long.mp4   {info['seconds']}s  voice: {', '.join(info['tts'])}")
        render.thumbnail(script.get("thumbnail_text", script["title"]), out / "thumbnail.png", accent,
                         script.get("thumbnail_action", "point"))
        meta["long"] = dict(file="long.mp4", thumbnail="thumbnail.png", seconds=info["seconds"])

    short = script.get("short")
    if short and args.only != "long":
        info = render.render(short["scenes"], "short", out / "short.mp4", accent, voice, music)
        print(f"short.mp4  {info['seconds']}s  voice: {', '.join(info['tts'])}")
        if info["seconds"] > 180:
            print("  warning: longer than 3 minutes, YouTube will not treat it as a Short")
        meta["short"] = dict(file="short.mp4", seconds=info["seconds"],
                             title=short.get("title", script["title"]),
                             description=short.get("description", script.get("description", "")))

    (out / "metadata.json").write_text(json.dumps(meta, indent=2))
    print(f"Review the files in {out}")


if __name__ == "__main__":
    main()
