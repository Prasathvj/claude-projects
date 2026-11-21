# Standing format for every new video

Agreed with the channel owner on 2026-11-17. Follow this every time.

When a script is approved, deliver ALL of the following, in this order, copy-paste ready, each with its own full prompt
(the style line included, never "same as above"):

1. **Characters** - a design prompt for every NEW character. For existing ones (hero, dog), say which reference to attach.
2. **Locations** - one prompt per place, no characters in the picture, floor/ground clear so puppets can stand on it.
   Give a code to each: L1, L2, ...
3. **Scenes** - one prompt per extra illustrated moment (characters in the picture). Codes S1, S2, ...
   Say what each one is for, and which are required and which are optional upgrades.
4. **Thumbnail** - two concept prompts, codes T1, T2.
5. A table: code, what it is, which beats of the script it serves, and what to attach as a reference.

Every prompt says: 16:9, no text (unless it is a thumbnail), no watermark, no falling snow or rain (added in code),
and "characters exactly as in the attached character sheet" when characters appear.

The owner generates the images in Google Flow (Nano Banana Pro), puts them in the Drive folder, and asks to build.
Then: look at every image, match it to its code, measure positions, build the Short first, then the long video.
Ask the owner to start each Drive filename with the code (L1, S2...). If they do not, match by looking and ask if unsure.

Common style line:
2D cartoon, clean graphic-novel style, uniform solid black outlines, flat cel shading, muted cold colours with orange as
the only warm accent, detailed background.

Character reference to attach whenever characters appear: `style/character-sheet-v1.jpg`.
Style reference for locations: any approved background, for example `episodes/blizzard/shots/01.jpg`.


## Upload package (added 2026-11-17, rule from the owner)

Whenever a video is finished, send TWO complete, separate upload packages in the same message: one for the LONG video
and one for the SHORT. Each package has: title, description (with sources, disclaimer, AI-narration line, hashtags for
the Short, chapters for the long), tags, pinned comment, thumbnail (which file to use), settings, and the order and
timing to publish. Never bury the Short's details inside the long video's. Also save them as UPLOAD.md in the episode folder.

## Shorts get their own vertical pictures (rule from the owner, 2026-11-17)

Shorts must NOT use puppets and must NOT crop the 16:9 pictures: the puppet's face never matched the Flow artwork, and
cropped landscape pictures lose the scene. Instead:
- Generate dedicated 9:16 pictures for every Short, one per line or per beat (codes V1, V2, ...), in Flow, with the character sheet attached.
- Every Short prompt says: vertical 9:16 composition, subject centred and fully visible, key action in the middle 60% of the
  frame, top 10% and bottom 25% free of important detail (captions go at the bottom).
- Animation stays minimal so the character is never altered: slow zoom, gentle shake on impacts, drifting dust or snow,
  sticker pops, word-by-word captions. Use `{"z": ...}` camera keys (see PUPPET.md).
- The long (16:9) video keeps its approach: puppets on locations plus illustrated scenes.
- So every video's prompt package now has TWO parts: long-video pictures (S, L, T) and Short pictures (V).
