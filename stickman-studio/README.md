# Stickman Studio

Turns one JSON script into a narrated stickman long video (16:9), a Short (9:16), a thumbnail
and upload metadata. Everything it uses is free.

## Setup

Needs Python 3.10+ and ffmpeg on your PATH.

```bash
pip install -r requirements.txt
```

## Workflow

1. **Write the script.** Paste `prompts/script_prompt.md` into a chatbot with your topic and save
   the reply as `scripts/<name>.json`. Read it and fix anything wrong or dull.
2. **Render.**

   ```bash
   python make.py scripts/<name>.json
   ```

   Files land in `output/<name>/`: `long.mp4`, `short.mp4`, `thumbnail.png`, `metadata.json`.
3. **Review** the videos.
4. **Upload**, by hand in YouTube Studio or with:

   ```bash
   python upload.py output/<name>
   ```

   Uploads are always private. Add `--publish-at 2026-12-01T14:30:00Z` to schedule.

## Options

- `--only long` / `--only short` renders one format.
- `--voice en-US-GuyNeural` picks another voice (`edge-tts --list-voices` shows them all).
- `--rate +10%` changes speaking speed.
- `--tts espeak` forces the offline robotic voice. With the default `auto`, it is used only when
  the Edge voice service cannot be reached.
- Put a file named `assets/music.mp3` in place to get quiet looping background music.
- Put a font at `assets/font.ttf` to change the typeface.

## Script fields

| Field | Meaning |
| --- | --- |
| `say` | Narration for the scene (required) |
| `text` | On-screen headline, a few words |
| `action` | idle, talk, point, wave, think, shrug, celebrate, sad, shock, facepalm, walk, run |
| `icon` | bulb, clock, question, heart, star, coin, check, cross, chart, phone, zzz, warning, target, book |

New poses go in `stickgen/rig.py` (`ACTIONS`), new icons in `stickgen/icons.py` (`ICONS`).

## Upload setup (one time)

1. In Google Cloud Console create a project and enable **YouTube Data API v3**.
2. Create an OAuth client of type **Desktop app**, download it as `client_secret.json` into this folder.
3. The first `upload.py` run opens a browser to sign in to the channel.

The free API quota allows about six uploads a day. Google locks videos uploaded through a new,
unaudited API project to private, so until the project passes Google's API audit, upload
manually in YouTube Studio.
