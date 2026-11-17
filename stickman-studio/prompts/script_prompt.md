Paste this into any free chatbot, replace the TOPIC line, and save the reply as `scripts/<name>.json`.

---

Write a script for a faceless stickman explainer YouTube video.

TOPIC: <your topic here>

Rules:
- Reply with JSON only, in exactly the format below.
- `scenes` is the long video: 35 to 60 scenes, each `say` is 1 or 2 short spoken sentences in plain, simple English. Aim for 5 to 8 minutes in total (about 150 words per minute).
- The first scene is a hook that makes the viewer curious. The last scene has a clear takeaway and asks the viewer to subscribe.
- `short.scenes` is a separate 4 to 6 scene version for YouTube Shorts, under 45 seconds, with its own strong first line.
- Only state facts that are true and well established. Do not invent studies, numbers or quotes.
- `text` is the on-screen headline: at most 4 words. It should not just repeat `say`.
- `action` must be one of: idle, talk, point, wave, think, shrug, celebrate, sad, shock, facepalm, walk, run. Vary it; do not use `talk` more than twice in a row.
- `icon` is optional and must be one of: bulb, clock, question, heart, star, coin, check, cross, chart, phone, zzz, warning, target, book.
- Write numbers the way they should be spoken ("two minutes", not "2 min").
- `thumbnail_text` is at most 3 words.

Format:

{
  "title": "Video title under 60 characters",
  "description": "Two or three sentences for the YouTube description.",
  "tags": ["tag one", "tag two"],
  "thumbnail_text": "Three words max",
  "thumbnail_action": "shrug",
  "accent": "#FFC233",
  "scenes": [
    {"say": "Spoken narration.", "action": "wave", "text": "Short headline", "icon": "bulb"}
  ],
  "short": {
    "title": "Short title #shorts",
    "scenes": [
      {"say": "Spoken narration.", "action": "shock", "text": "Short headline"}
    ]
  }
}
