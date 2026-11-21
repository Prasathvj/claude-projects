# tech-studio/motion — the cinematic look (ink · bone · signal orange)

Engine: **pdoom-video** by mexicat (Giacomo Magnanini), MIT licence, see `LICENSE.pdoom-engine`, via the owner's
Motion_as_kit. Kept: the engine (three.js HDR, bloom, halation, grain, motion blur), palette, fonts
(Archivo, IBM Plex Mono, Cormorant; OFL) and the plotter toolkit (`src/scenes/_vo.ts`). Not used: the kit's
ElevenLabs SFX and voiceover (free-plan licence); we use our own synthesized SFX and Gemini narration.

New here:
- `src/scenes/beat.ts`: one reusable plate per narration line; the line's `v.type` picks a template
  (slam, chapter, quote, browser, chat, email, code, agent, rank, counter, receipt, stack, icons, flow, loop,
  split, timeline, paper, trifecta, ruleoftwo, checklist, tease, end). Karaoke captions on aligned words,
  pen spark on traced outlines, rip / whip / punch transitions, post hits.
- `src/scenes/_draw.ts`: hairline primitives, line-art icons, the agent character.
- `src/timeline.ts`: one entry per line, cut in the pause before it.
- Vertical canvas: `?w=1080&h=1920` (render with `--w 1080 --h 1920`).

## Per episode
```sh
cd tech-studio
python3 tools/audio.py episode episodes/ep01/short.json   # Gemini narration + timeline
python3 tools/align.py ep01-short                          # word alignment (pocketsphinx, offline)
python3 tools/motion_export.py ep01-short                  # data/lyrics.json, data/audio.json, audio/mix.wav (VO + SFX + music)
cd motion && bun install
./render_ep.sh ep01-short vertical                         # -> episodes/ep01-short/out/ep01-short-final.mp4 (-14 LUFS)
./render_ep.sh ep01-long
```
Preview: `EP=$PWD/episodes/ep01-long bunx vite` then open http://localhost:5173 (add `?w=1080&h=1920` for Shorts).
Contact sheet: `bun scripts/render.ts sheet --ep episodes/<id> --times 1,5,9 [--w 1080 --h 1920]`.
In this cloud box set `CHROME_PATH=/opt/pw-browsers/chromium`; on Windows/Mac the script uses installed Chrome.
