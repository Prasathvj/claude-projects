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
GROUND = {'grey': '#EEEAE6', 'white': '#FFFFFF'}

def name():
    return os.environ.get('THEME', 'dark')

def apply(html):
    t = name()
    if t == 'dark':
        return html
    m = {**LIGHT, '#0C0704': GROUND[t]}
    pat = re.compile('|'.join(re.escape(k) for k in sorted(m, key=len, reverse=True)), re.I)
    return pat.sub(lambda x: m[next(k for k in m if k.lower() == x.group(0).lower())], html)
