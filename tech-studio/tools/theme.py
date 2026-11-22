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
         'rgba(248,119,54,.09)': 'rgba(0,0,0,0)', 'rgba(248,119,54,.10)': 'rgba(0,0,0,0)', 'rgba(248,119,54,.22)': 'rgba(236,150,110,.30)',
         'rgba(0,0,0,.7)': 'rgba(214,160,125,.38)', 'rgba(0,0,0,.72)': 'rgba(214,160,125,.38)', 'rgba(0,0,0,.6)': 'rgba(120,70,40,.12)'}
MAPS = {'cream': CREAM, 'grey': LIGHT, 'white': LIGHT, 'slate': SLATE, 'charcoal': CHARCOAL, 'navy': NAVY}

def name():
    return os.environ.get('THEME', 'dark')

def apply(html):
    t = name()
    if t == 'dark':
        return html
    m = {**MAPS[t], '#0C0704': GROUND[t]}
    pat = re.compile('|'.join(re.escape(k) for k in sorted(m, key=len, reverse=True)), re.I)
    return pat.sub(lambda x: m[next(k for k in m if k.lower() == x.group(0).lower())], html)
