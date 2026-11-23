"""Colour themes for the HyperFrames generators. The scenes are authored in the dark theme;
light themes are a one-pass colour remap of the generated HTML (so Bit/Max colours stay as designed).
Select with env THEME=dark|grey|white."""
import os, re

LIGHT = {
    '#2C1A13': '#FFFFFF', '#1F120C': '#FBF7F3', '#3E2217': '#E6D9CE', '#0E0806': '#F6EFE8',
    '#1A0F0A': '#F7F1EB', '#140B07': '#F4EDE6', '#2A1912': '#EFE4DA', '#2E1B13': '#E6D9CE', '#2A1A12': '#EFE4DA',
    '#2A1810': '#FFF1E8', '#3A2318': '#FBE3D3', '#160C08': '#F7F1EB',
    '#F6EEE8': '#1E120C', '#9E745A': '#8A6550', '#8C6B5A': '#9C8576', '#6E5444': '#A8968A', '#5C4337': '#C9BBB0',
    '#CDB8AA': '#6B5446', '#7A5A48': '#D5C6BA', '#2A0D0A': '#FDECEA', '#FF6B5E': '#D93025', '#55C2FF': '#1C7ED6',
    'rgba(0,0,0,.7)': 'rgba(110,70,40,.10)', 'rgba(0,0,0,.72)': 'rgba(110,70,40,.10)', 'rgba(0,0,0,.6)': 'rgba(110,70,40,.14)',
    'rgba(0,0,0,.65)': 'rgba(110,70,40,.14)', 'rgba(255,190,150,.06)': 'rgba(255,255,255,.8)',
}
GROUND = {'cream': '#F4EDE3', 'grey': '#EEEAE6', 'white': '#FFFFFF', 'slate': '#EEF2F7', 'charcoal': '#121417', 'navy': '#0B1424'}
SLATE = {**LIGHT, '#1F120C': '#F8FAFC', '#3E2217': '#DCE3EC', '#0E0806': '#F1F5F9', '#1A0F0A': '#F4F7FA', '#140B07': '#F1F5F9',
         '#2A1912': '#E7EDF4', '#2E1B13': '#DCE3EC', '#2A1A12': '#E7EDF4', '#160C08': '#F4F7FA', '#F6EEE8': '#14213D',
         '#9E745A': '#64748B', '#8C6B5A': '#7C8BA0', '#6E5444': '#94A3B8', '#5C4337': '#B6C2D1', '#CDB8AA': '#475569', '#7A5A48': '#CBD5E1',
         '#1E120C': '#14213D', 'rgba(248,119,54,.09)': 'rgba(20,33,61,.06)', 'rgba(248,119,54,.10)': 'rgba(20,33,61,.06)',
         'rgba(0,0,0,.7)': 'rgba(20,33,61,.08)', 'rgba(0,0,0,.6)': 'rgba(20,33,61,.12)'}
CHARCOAL = {'#2C1A13': '#23262C', '#1F120C': '#1B1E23', '#3E2217': '#33373F', '#0E0806': '#0F1114', '#1A0F0A': '#1A1D21', '#140B07': '#16181C',
            '#2A1912': '#262A30', '#2E1B13': '#2C3038', '#2A1A12': '#262A30', '#2A1810': '#2A2620', '#3A2318': '#3A2E26', '#160C08': '#1A1D21',
            '#9E745A': '#9AA3AF', '#8C6B5A': '#7D8794', '#6E5444': '#5F6873', '#5C4337': '#4B525C', '#CDB8AA': '#C4CAD2', '#7A5A48': '#4B525C'}
NAVY = {'#2C1A13': '#18294A', '#1F120C': '#122039', '#3E2217': '#26406B', '#0E0806': '#0A1220', '#1A0F0A': '#111E35', '#140B07': '#0F1A2E',
        '#2A1912': '#1B2C4C', '#2E1B13': '#22365A', '#2A1A12': '#1B2C4C', '#2A1810': '#2A2A3A', '#3A2318': '#3A3446', '#160C08': '#111E35',
        '#9E745A': '#8FA3C2', '#8C6B5A': '#7286A8', '#6E5444': '#5A6E91', '#5C4337': '#45577A', '#CDB8AA': '#C3CEE0', '#7A5A48': '#45577A'}
CREAM = {**LIGHT, '#2C1A13': '#FFFAF7', '#1F120C': '#FFF6EF', '#3E2217': '#EADCCD', '#0E0806': '#F8F1E8', '#F6EEE8': '#2A2018',
         'rgba(248,119,54,.09)': 'rgba(232,110,60,.16)', 'rgba(248,119,54,.10)': 'rgba(232,110,60,.16)', 'rgba(248,119,54,.22)': 'rgba(236,150,110,.30)',
         'rgba(0,0,0,.7)': 'rgba(214,160,125,.38)', 'rgba(0,0,0,.72)': 'rgba(214,160,125,.38)', 'rgba(0,0,0,.6)': 'rgba(120,70,40,.12)'}
MAPS = {'cream': CREAM, 'grey': LIGHT, 'white': LIGHT, 'slate': SLATE, 'charcoal': CHARCOAL, 'navy': NAVY}

def name():
    return os.environ.get('THEME', 'dark')

GRIDS = {
    'zigzag': ('background-image:url("data:image/svg+xml;utf8,<svg xmlns=%27http://www.w3.org/2000/svg%27 width=%2780%27 height=%2740%27><path d=%27M0 30 L20 10 L40 30 L60 10 L80 30%27 fill=%27none%27 stroke=%27rgba(232,110,60,.28)%27 stroke-width=%273%27/></svg>");', 'background-size:80px 40px;')[0] + ('background-image:url("data:image/svg+xml;utf8,<svg xmlns=%27http://www.w3.org/2000/svg%27 width=%2780%27 height=%2740%27><path d=%27M0 30 L20 10 L40 30 L60 10 L80 30%27 fill=%27none%27 stroke=%27rgba(232,110,60,.28)%27 stroke-width=%273%27/></svg>");', 'background-size:80px 40px;')[1],
    'circuit': ('background-image:url("data:image/svg+xml;utf8,<svg xmlns=%27http://www.w3.org/2000/svg%27 width=%27120%27 height=%27120%27><path d=%27M10 60 H50 V20 H110 M60 120 V80 H100 M0 100 H30%27 fill=%27none%27 stroke=%27rgba(232,110,60,.24)%27 stroke-width=%273%27/><circle cx=%2750%27 cy=%2760%27 r=%275%27 fill=%27rgba(232,110,60,.35)%27/><circle cx=%27100%27 cy=%2780%27 r=%275%27 fill=%27rgba(232,110,60,.35)%27/></svg>");', 'background-size:120px 120px;')[0] + ('background-image:url("data:image/svg+xml;utf8,<svg xmlns=%27http://www.w3.org/2000/svg%27 width=%27120%27 height=%27120%27><path d=%27M10 60 H50 V20 H110 M60 120 V80 H100 M0 100 H30%27 fill=%27none%27 stroke=%27rgba(232,110,60,.24)%27 stroke-width=%273%27/><circle cx=%2750%27 cy=%2760%27 r=%275%27 fill=%27rgba(232,110,60,.35)%27/><circle cx=%27100%27 cy=%2780%27 r=%275%27 fill=%27rgba(232,110,60,.35)%27/></svg>");', 'background-size:120px 120px;')[1],
    'triangles': ('background-image:url("data:image/svg+xml;utf8,<svg xmlns=%27http://www.w3.org/2000/svg%27 width=%2790%27 height=%2778%27><path d=%27M45 8 L82 70 H8 Z%27 fill=%27none%27 stroke=%27rgba(232,110,60,.22)%27 stroke-width=%273%27/></svg>");', 'background-size:90px 78px;')[0] + ('background-image:url("data:image/svg+xml;utf8,<svg xmlns=%27http://www.w3.org/2000/svg%27 width=%2790%27 height=%2778%27><path d=%27M45 8 L82 70 H8 Z%27 fill=%27none%27 stroke=%27rgba(232,110,60,.22)%27 stroke-width=%273%27/></svg>");', 'background-size:90px 78px;')[1],
    'rings': ('background-image:url("data:image/svg+xml;utf8,<svg xmlns=%27http://www.w3.org/2000/svg%27 width=%27100%27 height=%27100%27><circle cx=%2750%27 cy=%2750%27 r=%2730%27 fill=%27none%27 stroke=%27rgba(232,110,60,.22)%27 stroke-width=%273%27/><circle cx=%2750%27 cy=%2750%27 r=%2712%27 fill=%27none%27 stroke=%27rgba(232,110,60,.18)%27 stroke-width=%273%27/></svg>");', 'background-size:100px 100px;')[0] + ('background-image:url("data:image/svg+xml;utf8,<svg xmlns=%27http://www.w3.org/2000/svg%27 width=%27100%27 height=%27100%27><circle cx=%2750%27 cy=%2750%27 r=%2730%27 fill=%27none%27 stroke=%27rgba(232,110,60,.22)%27 stroke-width=%273%27/><circle cx=%2750%27 cy=%2750%27 r=%2712%27 fill=%27none%27 stroke=%27rgba(232,110,60,.18)%27 stroke-width=%273%27/></svg>");', 'background-size:100px 100px;')[1],
    'orbits': ('background-image:url("data:image/svg+xml;utf8,<svg xmlns=%27http://www.w3.org/2000/svg%27 width=%27220%27 height=%27220%27><circle cx=%27110%27 cy=%27110%27 r=%2730%27 stroke=%27%23E86E3C%27 stroke-opacity=%27.28%27 stroke-width=%272.5%27 fill=%27none%27/><circle cx=%27110%27 cy=%27110%27 r=%2770%27 stroke=%27%23E86E3C%27 stroke-opacity=%27.28%27 stroke-width=%272.5%27 fill=%27none%27/><circle cx=%27110%27 cy=%27110%27 r=%27108%27 stroke=%27%23E86E3C%27 stroke-opacity=%27.28%27 stroke-width=%272.5%27 fill=%27none%27/><circle cx=%27180%27 cy=%27110%27 r=%275%27 fill=%27%23E86E3C%27 fill-opacity=%27.30%27/></svg>"); background-size:220px 220px;'),
    'pixels': ('background-image:url("data:image/svg+xml;utf8,<svg xmlns=%27http://www.w3.org/2000/svg%27 width=%2748%27 height=%2748%27><rect x=%274%27 y=%274%27 width=%2710%27 height=%2710%27 rx=%272%27 fill=%27%23E86E3C%27 fill-opacity=%27.30%27/><rect x=%2728%27 y=%2728%27 width=%2710%27 height=%2710%27 rx=%272%27 fill=%27%23E86E3C%27 fill-opacity=%27.14%27/></svg>"); background-size:48px 48px;'),
    'network': ('background-image:url("data:image/svg+xml;utf8,<svg xmlns=%27http://www.w3.org/2000/svg%27 width=%27160%27 height=%27140%27><path d=%27M20 20L90 50L140 20M90 50L60 120L140 110M20 20L60 120%27 stroke=%27%23E86E3C%27 stroke-opacity=%27.28%27 stroke-width=%272.5%27 fill=%27none%27/><circle cx=%2720%27 cy=%2720%27 r=%275%27 fill=%27%23E86E3C%27 fill-opacity=%27.30%27/><circle cx=%2790%27 cy=%2750%27 r=%276%27 fill=%27%23E86E3C%27 fill-opacity=%27.30%27/><circle cx=%27140%27 cy=%2720%27 r=%274%27 fill=%27%23E86E3C%27 fill-opacity=%27.30%27/><circle cx=%2760%27 cy=%27120%27 r=%275%27 fill=%27%23E86E3C%27 fill-opacity=%27.30%27/><circle cx=%27140%27 cy=%27110%27 r=%274%27 fill=%27%23E86E3C%27 fill-opacity=%27.30%27/></svg>"); background-size:160px 140px;'),
    'gears': ('background-image:url("data:image/svg+xml;utf8,<svg xmlns=%27http://www.w3.org/2000/svg%27 width=%27140%27 height=%27140%27><circle cx=%2750%27 cy=%2750%27 r=%2722%27 stroke=%27%23E86E3C%27 stroke-opacity=%27.28%27 stroke-width=%272.5%27 fill=%27none%27/><circle cx=%2750%27 cy=%2750%27 r=%278%27 stroke=%27%23E86E3C%27 stroke-opacity=%27.28%27 stroke-width=%272.5%27 fill=%27none%27/><path d=%27M50 20v-8M50 80v8M20 50h-8M80 50h8M29 29l-6-6M71 71l6 6M71 29l6-6M29 71l-6 6%27 stroke=%27%23E86E3C%27 stroke-opacity=%27.28%27 stroke-width=%272.5%27 fill=%27none%27/><circle cx=%27108%27 cy=%27108%27 r=%2714%27 stroke=%27%23E86E3C%27 stroke-opacity=%27.28%27 stroke-width=%272.5%27 fill=%27none%27/></svg>"); background-size:140px 140px;'),
    'diagonal': ('background-image:url("data:image/svg+xml;utf8,<svg xmlns=%27http://www.w3.org/2000/svg%27 width=%2756%27 height=%2756%27><path d=%27M-14 14L14 -14M0 56L56 0M42 70L70 42%27 stroke=%27%23E86E3C%27 stroke-opacity=%27.30%27 stroke-width=%272.5%27 fill=%27none%27/></svg>"); background-size:56px 56px;'),
    'hex': ('background-image:url("data:image/svg+xml;utf8,<svg xmlns=%27http://www.w3.org/2000/svg%27 width=%2784%27 height=%2748%27><path d=%27M14 0L0 24L14 48M14 0H42L56 24L42 48H14M56 24H84%27 stroke=%27%23E86E3C%27 stroke-opacity=%27.30%27 stroke-width=%272.5%27 fill=%27none%27/></svg>"); background-size:84px 48px;'),
    'waves': ('background-image:url("data:image/svg+xml;utf8,<svg xmlns=%27http://www.w3.org/2000/svg%27 width=%27120%27 height=%2740%27><path d=%27M0 20 C20 4 40 4 60 20 S100 36 120 20%27 stroke=%27%23E86E3C%27 stroke-opacity=%27.30%27 stroke-width=%272.5%27 fill=%27none%27/></svg>"); background-size:120px 40px;'),
    'plus': ('background-image:url("data:image/svg+xml;utf8,<svg xmlns=%27http://www.w3.org/2000/svg%27 width=%2764%27 height=%2764%27><path d=%27M32 23v18M23 32h18%27 stroke=%27%23E86E3C%27 stroke-opacity=%27.45%27 stroke-width=%273%27 stroke-linecap=%27round%27/></svg>"); '
             'background-size:64px 64px;'),  # background pattern variants (env GRID); 'lines' keeps the house grid
    'plain': 'background-image:none;',
    'dots': 'background-image:radial-gradient(rgba(232,110,60,.38) 2.5px, transparent 3px); background-size:48px 48px;',
    'blueprint': ('background-image:linear-gradient(rgba(232,110,60,.20) 2px, transparent 2px), linear-gradient(90deg, rgba(232,110,60,.20) 2px, transparent 2px), '
                  'linear-gradient(rgba(232,110,60,.08) 1px, transparent 1px), linear-gradient(90deg, rgba(232,110,60,.08) 1px, transparent 1px); '
                  'background-size:96px 96px, 96px 96px, 24px 24px, 24px 24px;'),
}

def apply(html):
    g = os.environ.get('GRID', 'lines')
    if g in GRIDS:
        html = re.sub(r'background-image:linear-gradient\(rgba\(248,119,54,\.(?:09|10)\) 2px, transparent 2px\), linear-gradient\(90deg, rgba\(248,119,54,\.(?:09|10)\) 2px, transparent 2px\); background-size:\d+px \d+px;', GRIDS[g], html)
    t = name()
    if t != 'dark':
        m = {**MAPS[t], '#0C0704': GROUND[t]}
        pat = re.compile('|'.join(re.escape(k) for k in sorted(m, key=len, reverse=True)), re.I)
        html = pat.sub(lambda x: m[next(k for k in m if k.lower() == x.group(0).lower())], html)
    import kit_paper, kit_myst   # STYLE=paper: papercut layer; STYLE=mystery: Tech Mysteries layer (no-ops otherwise)
    return kit_myst.mysterize(kit_paper.paperize(html))
