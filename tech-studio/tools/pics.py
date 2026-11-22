"""Free picture library for TechDecoded scenes: Microsoft Fluent Emoji (MIT licence), installed in hf/lib via npm
(@iconify-json/fluent-emoji-flat = flat colour, @iconify-json/fluent-emoji = soft 3D). 3,000+ pictures of people, objects,
places, money, computers, books, animals, symbols.
    pic('man-technologist', 220)            -> inline <svg> string
    pic('brain', 300, style='3d')
    find('book')                             -> names containing 'book'
"""
import json
from functools import lru_cache
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / 'hf/lib/node_modules/@iconify-json'
SETS = {'flat': 'fluent-emoji-flat', '3d': 'fluent-emoji'}

@lru_cache(None)
def _set(style):
    return json.loads((LIB / SETS[style] / 'icons.json').read_text())

def _resolve(d, name):
    if name in d['icons']:
        return d['icons'][name]
    al = d.get('aliases', {}).get(name)
    if al:
        return _resolve(d, al['parent'])
    raise KeyError(f'picture not found: {name} (try pics.find)')

def pic(name, size=200, style='flat', cls='', pid=''):
    d = _set(style); ic = _resolve(d, name)
    w, h = ic.get('width', d.get('width', 32)), ic.get('height', d.get('height', 32))
    a = f' id="{pid}"' if pid else ''
    c = f' class="{cls}"' if cls else ''
    return f'<svg{a}{c} width="{size}" height="{round(size * h / w)}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">{ic["body"]}</svg>'

def find(word, style='flat'):
    d = _set(style)
    return sorted(n for n in list(d['icons']) + list(d.get('aliases', {})) if word in n)

if __name__ == '__main__':
    import sys
    print('\n'.join(find(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'flat')))
