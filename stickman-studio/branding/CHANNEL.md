# Channel identity (draft 3: not tied to any character or topic)

The channel will have different stories and different characters, so the name and logo must not belong to one
hero, one dog or one topic.

## Name

Recommended: **Twigwise**   Handle to try: `@Twigwise`
(Twig = stick figure, wise = smart. Works for stories, explainers, psychology, comedy and survival.)

Other options:
- **Plot Twig**   `@PlotTwig`   (stick pun on "plot twist"; leans toward stories and comedy)
- **Doodlewise**   `@Doodlewise`   (not yet checked in vidIQ, only a web search that found nothing)

Checked with vidIQ and web search on 2026-11-17. Both cover only part of YouTube, so none of this is proof. The real
test is YouTube's create-channel screen (handles must be unique). Also do a quick web search for trademark conflicts.

Ruled out because a channel already exists: Stickwise, Stickling, Linewise, Stickverse / StickVerse, Twigverse, TwigTales,
Sticksmith / Sticksmith Tales, Survivio, Stranded Stick.

Dropped because they tie the brand to the first two characters: Bandana & Beam, Twig & Beam.

## Tagline options

- Big ideas, drawn with sticks.
- Little stories. Big questions.
- Stick figures with something to say.

## Description (paste into YouTube Studio > Customization > Basic info)

```
Big ideas, drawn with sticks. ✏️

Short animated stories with a new cast every time: survival scenarios, why people do the things they do, curious facts, and "what would you do?" dilemmas.

Every script is checked against published sources, which we list in each video's description.

For education and entertainment only. Not professional advice. In an emergency, call your local emergency number.

Animated stories. Narration is AI-generated.

New videos and Shorts regularly. Follow along.
```

## Content pillars

1. "What would you do?" scenarios (survival and everyday emergencies)
2. Mistakes and myths (quick, searchable, tip-card heavy)
3. Explainers and everyday psychology
4. Short comedy, such as "worst advice ever"

Each pillar can use different characters. The puppet tool currently has two (the headlamp hero and his dog); new
characters need to be built before a story can use them.

## Logo

`logo.png` (800 x 800): a neutral celebrating stick figure on orange, not tied to any story. YouTube crops it to a
circle; `logo_preview.png` shows the crop on dark and light. Regenerate with `python branding/make_logo.py`.

The earlier hero-and-dog logo is kept as `logo_hero_dog.png` for use as a mascot on one series.

Prompt for a more polished version in Flow:

```
Square profile picture for a YouTube channel, 2D cartoon in a clean graphic-novel style, uniform solid black outlines, flat cel shading. A simple stick figure with a large white round head, dot eyes and a smile, both arms raised in excitement, small white mitten hands and white shoes, with small white spark lines around the hands. Warm orange background, thin dark navy ring border. Centered composition that still reads when cropped to a circle. No text.
```

## Create the channel

1. YouTube, profile picture, Create a channel.
2. Enter the name and handle; YouTube tells you if the handle is taken.
3. Studio > Customization > Branding: upload `logo.png`; banner later.
4. Basic info: paste the description.
5. Verify your phone number (Studio, Settings, Channel, Feature eligibility) to unlock custom thumbnails and longer videos.
