# Handoff: start of the tech-studio session (2026-11-21)

## Who and what
Owner: IT professional, builds a faceless YouTube channel "Stick Dude" (English, free tools only, review before upload). New direction: TECH explainer content only, high-end motion-graphics editing, long videos as the main goal; Shorts tease the long video with a curiosity gap, plus stand-alone Shorts. First topic: AI agents (research trending, verify facts, 5 options first).

## Style reference analysed (vidIQ, 10 credits)
Instagram reel DfEOKuNyyqv ("Ditch" ad, 37 s, made in code with Remotion): cut every 0.8-1.4 s on the voice beat; hook = bold relatable claim + receipt unfolding + rip transition + counter ticking up; personified clay-3D icons (1 s each); object-driven transition (3D scissors cut to the next scene); UI mockup with depth; total stacks; payoff; brand card; behind-the-scenes code shot; comment-keyword CTA. Big geometric sans, numbers as heroes, spring-overshoot reveals, motion-blur counters, bouncy lo-fi beat, whooshes/dings/rips/coin clinks, VO ~160-175 wpm. Recreate TECHNIQUES only, never its content or branding.

## New look
Navy #0B1226, cyan #2EE6FF, hot accent #FF4D6D, off-white #F4F7FF.

## Tools that work
- Remotion 4.0.250 installed and tested (counter test rendered): `npx remotion render src/index.ts Test out/test.mp4 --browser-executable=/opt/pw-browsers/chromium --concurrency=2`.
- Existing Python pipeline in `stickman-studio/` (code only; media is not in git): Gemini TTS (`stickgen/gtts.py`, free daily quotas, batch + clean end-burst), SFX synth and diagrams (`stickgen/stage.py`), skia/ffmpeg director (`direct.py`), PUPPET.md docs, style rules in `style/`. Voice: Fenrir; fast profile ~160 wpm for Shorts.
- Google Drive MCP: owner uploads Flow images/clips to a Drive folder; download, remove the Flow sparkle (bottom-right) with inpaint/delogo. Flow clips are 5-8 s, vertical 1080x1920 or 1920x1080.
- vidIQ MCP (about 80 credits left; renews 2026-12-17): keyword_research (5 credits), outliers, watch_shortform_content (10).
- WebSearch for fact-checking (primary sources first; label illustrative numbers).

## Lessons from the channel so far
- Channel (3 subscribers, 7 videos): only the winter "Your car dies in a blizzard. What do you do?" Short broke out (1,461 views); everything else under ~65. In-season plain-question titles under 50 chars beat hashtag/long titles. Judge a video at 48-72 h. Ask the owner for Studio "viewed vs swiped away".
- Shorts: 25-40 s, hook in 1 s, one idea per beat, no hashtags in title, keywords in description, pinned comment question.
- Never claim unverifiable numbers. Always include "AI narrator" line and a disclaimer.
- Every finished video: send TWO upload packages (long + Short) with SEO from vidIQ data.

## Open decisions for the owner
Model choice (Opus 5.5 recommended for building the animation system, Sonnet 5.5 for episode production); first topic = AI agents (pick 1 of 5 options after research).
