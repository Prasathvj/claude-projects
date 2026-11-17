# Puppet episodes

An episode is one JSON file. `direct.py` turns it into a finished video: narration, animation,
captions, sound effects and music.

```bash
python direct.py episodes/<name>/<file>.json --check        # validate, no narration or render
python direct.py episodes/<name>/<file>.json --frames 1,5,9 # stills in out/ for checking
python direct.py episodes/<name>/<file>.json                # full render -> out/<file>.mp4
```

Working example: `episodes/night-one/short.json`.

## Top level

| Field | Meaning |
| --- | --- |
| `format` | `short` (1080x1920) or `long` (1920x1080) |
| `voice` | Gemini voice name, default `Fenrir` |
| `captions` | `false` to turn off word-by-word captions |
| `sets` | Named backgrounds (below) |
| `shots` | The shots, in order. One narration line per shot. |

## Sets

A set is one background image without characters, plus named places on it. All coordinates are
pixels on that image.

```json
"road": {
  "image": "shots/01.jpg",
  "hero_h": 400, "dog_h": 135,        // character heights in image pixels
  "snow": 1.0,                        // falling snow, 0 for none
  "marks": {"hero": [1815, 1375], "dog": [1935, 1400], "exhaust": [2128, 1262]},
  "views": {"wide": [1995, 911, 1250], "rear": [2165, 1180, 820]},
  "glows": [[2098, 1153, 150, 1.4]]   // x, y, radius, blinks per second (0 = steady)
}
```

- A **mark** is where feet stand (or where an effect happens). Marks named `hero` and `dog` are the
  default standing places.
- A **view** is `[centre x, centre y, visible height]`. Smaller height means closer.

## Shots

```json
{
  "set": "road",
  "say": "Narration for this shot.",
  "direct": "how to act the line: dry sarcasm, whisper, shouting...",
  "camera": [...], "actors": {...}, "events": [...],
  "snow": 0.5                          // optional override
}
```

The shot lasts as long as its narration. A shot without `say` uses `"hold": seconds`.

### Timing

Anything that happens at a moment takes one of:

- `"at": 1.3` seconds into the shot, or `"at": "end"`
- `"on": "word"` when the narrator says that word (`"word#2"` for its second use)
- plus optional `"delay": 0.2`

### Camera

A list of keys. The camera moves between them; a key keeps any field it does not restate.

```json
"camera": [{"view": "sky"}, {"at": 1.3, "view": "wide", "ease": "snap"}, {"at": "end", "view": "medium"}]
"camera": [{"follow": "hero", "dx": 40, "dy": -230, "zoom": 780}, {"on": "snowman", "delay": 0.2, "zoom": 610, "ease": "snap"}]
```

`ease`: `smooth` (default), `snap` (whip pan / snap zoom, adds a whoosh), `linear`.
A `view` can be a name or `[x, y, height]`.

### Actors

`hero` and `dog`, each a list of steps played in order. An actor keeps their position from the
previous shot on the same set.

| Step field | Meaning |
| --- | --- |
| `from` | Jump to a mark or `[x, y]` first |
| `to` | Walk/run there. With `for` (seconds) or `speed` (pixels per second) |
| `do` | What to do when not moving |
| `gait` | Hero only: `walk` (default) or `run` while moving |
| `face` | `left`, `right`, or a mark to look toward |
| `follow`, `dx`, `dy` | Stay beside another actor |
| `mood` | Hero face: `neutral happy sad angry surprised scared confused` |
| `mouth` | `talk` makes the hero's mouth move |
| `sweat` | `true` for sweat drops |
| `as` | `snowman` swaps the hero for a snowman with a pop |
| `tilt` | Dog head tilt in degrees while sitting |
| `scale` | Size multiplier for this step |

Hero `do`: `idle talk point wave think shrug celebrate sad shock facepalm walk run dig crouch_look lean_talk stomp_point`

Dog `do`: `sit dig play`

Footsteps and digging sounds are added automatically from what the hero is doing.

### Events

| `fx` | Fields | What it does |
| --- | --- | --- |
| `hit` | | Screen shake, zoom punch, thud; characters hop |
| `impact` | `text` | Giant slam-in word plus a hit. Captions are hidden in shots that use it |
| `sticker` | `text` | Pop-up label; several stack downward |
| `sparkle` | `actor` or `mark` | Sparkle burst and chime |
| `chunks` | `mark`, `every` | Repeating bursts of flying snow chunks |
| `smoke` | `mark` | Rising smoke |
| `dark` | `level` (0-255) | Darkens the scene, adds a rumble, lowers the music |
| `wind_lines` | | Streaking wind lines and stronger snow drift |
| `sfx` | `name`, `gain` | One sound: `whoosh thud pop ding crunch rumble` |

Lasting effects (`chunks`, `wind_lines`) stop at `"to_at"` / `"to_on"`, otherwise at the end of the shot.

## Music

Drop a file at `assets/music.mp3` to replace the built-in synthesized loop.

## Adding to the library

- New hero pose: a function in `stickgen/puppet.py`, added to `ACTIONS`.
- New effect: draw function in `stickgen/stage.py`, then handle it in `Director.frame` and
  `Director.soundtrack` in `direct.py` and add its name to `FX`.
