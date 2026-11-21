# tech-studio template library

Navy #0B1226 · cyan #2EE6FF · hot #FF4D6D · off-white #F4F7FF. Fonts ship in `public/fonts` (Inter Display, Inter, JetBrains Mono; all OFL).
Everything is drawn in code; nothing is copied from any reference video.

## Workflow (one episode)
1. Write `episodes/<ep>/<name>.json`: `id`, `format` (`vertical` | `horizontal`), `profile` (`fast` for Shorts, `explainer` for long),
   `gap` (seconds between lines), `captions` (`big` | `small`), and `beats`: `{text, dir, v: {type, ...props}, trans?, sfx?}`.
2. `python3 tools/audio.py sfx` (once) and `python3 tools/audio.py episode episodes/<ep>/<name>.json`
   → Gemini narration (free quota; 8 lines per request, falls back across models and to single lines), timed beats,
   estimated word timings for captions, music bed, `src/episodes/<id>.timeline.json`, and `src/episodes/index.ts`.
3. Review: `python3 tools/sheet.py <id>` → `out/stills/<id>/sheet.png` (one still per beat).
4. Render: `npx remotion render src/index.ts <id> out/<id>.mp4 --browser-executable=/opt/pw-browsers/chromium --concurrency=4`
5. `tools/finish.sh out/<id>.mp4` → loudness-normalised `-final.mp4` (-14 LUFS).
6. Thumbnail: `npx remotion still src/index.ts Thumb-<ep> out/<ep>-thumbnail.png --frame=29 ...`

## Beat options
- `trans`: `punch` (big scale kick), `whip` (sideways slam with motion blur + whoosh), `rip` (torn sheet tears away). Every beat gets a small punch by default.
- `sfx`: names from `public/sfx`: whoosh rip pop ding click tick glitch impact thud notify scan error riser type print snip.
  The n-th sound fires on the n-th staggered pop (7 frames apart) unless the scene has its own cue (see `cues()` in `src/lib/Episode.tsx`).
- `v.label`: red corner chip, e.g. `ILLUSTRATION`, `RECREATION`, `SIMPLIFIED`. Use it on every mock-up and illustrative number.

## Scenes (`v.type`)
| type | props | what it does |
|---|---|---|
| slam | text, sub?, accent (cyan/hot) | kinetic headline: words slam in with blur, flash and shake |
| chapter | n, title | outlined chapter number, hot bar wipe |
| quote | text, who, when? | typed quote with marker highlight |
| browser | url, title, body[], hidden[]?, reveal? | 3D-tilted browser mock-up; select-all exposes hidden text |
| chat | msgs[{from: you/agent, text}] | chat bubbles pop in; "reading…" typing bubble |
| email | from, subject, body[], hidden[]? | inbox mock-up; hidden line revealed in red |
| code | file, lines[{t, c: text/cyan/hot/dim/gold/green}] | editor window that types; hot lines glow |
| agent | mode: scan / hijack / memory | the robot character reading, turned evil (glitch + stamp), or with planted memory |
| rank | title, items[] ("" = blurred placeholder), source? | top-N list, #1 lands last with a glow |
| counter | from, to, decimals?, prefix?, suffix?, label | motion-blur number ticker with audible ticks and landing punch |
| receipt | title, items[[k, v]], total[k, v] | receipt prints line by line, total stamps in |
| stack | title?, items[] | blocks drop and stack ("total stacks") |
| icons | items[{icon, label}] | clay icon tiles pop in on the beat |
| flow | nodes[{icon, label}], hi? | pipeline with travelling dots; hi node glows red |
| loop | steps[] | circular loop around the agent, active step cycles |
| split | left, right {icon, title, body}, merge?, bad? | two cards; optional merge stamp or "bad side" |
| timeline | events[[date, text]], hi? | dated events on a line |
| paper | title, sub, point | research-paper card with highlighted takeaway |
| trifecta | legs[3], show (0-3), danger?, cut? | three-leg risk triangle; build, warn, then cut a leg |
| ruleoftwo | items[3] | toggles: two on, third needs a human |
| checklist | title, items[], upto | numbered tips revealed one per beat |
| tease | title, sub | locked, blurred payoff card for Short endings |
| end | title, sub | agent character sign-off card |

Icons (`src/lib/icons.tsx`): globe mail doc code send cart gear shield skull server brain chat warn user agent.

## Building blocks (`src/lib`)
`motion.tsx` PopIn, Rise, PunchZoom, Float, Whip, Rip, Tilt, Sfx, LabelChip, Bg · `widgets.tsx` Counter, Receipt, Stack, Captions, CodeWindow,
BrowserCard, ChatCard, EmailCard · `icons.tsx` Icon, Agent · `scenes.tsx` scene registry · `Episode.tsx` timeline player · `Thumbnail.tsx`.
To add a scene: write a component in `scenes.tsx`, add it to `SCENES`, and give it a cue rule in `Episode.tsx` if its sounds are not on the 7-frame stagger.
