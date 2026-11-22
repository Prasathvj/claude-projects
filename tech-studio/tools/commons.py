"""Wikimedia Commons helper: search files and show licence/author, or download a scaled copy with a credits record.
Usage: python3 tools/commons.py search "<query>" [n]
       python3 tools/commons.py get "File:Name.jpg" <out.jpg> [width]   (appends credit to <out dir>/credits.json)"""
import json, sys, urllib.parse, urllib.request
from pathlib import Path
UA = {'User-Agent': 'TechDecodedStudio/1.0 (educational explainer videos)'}
API = 'https://commons.wikimedia.org/w/api.php?'

def api(**p):
    p['format'] = 'json'
    with urllib.request.urlopen(urllib.request.Request(API + urllib.parse.urlencode(p), headers=UA), timeout=30) as r:
        return json.load(r)

def info(titles, width=1080):
    d = api(action='query', titles='|'.join(titles), prop='imageinfo', iiprop='url|extmetadata|size', iiurlwidth=width)
    out = []
    for pg in d['query']['pages'].values():
        if 'imageinfo' not in pg: continue
        ii = pg['imageinfo'][0]; m = ii.get('extmetadata', {})
        g = lambda k: (m.get(k, {}).get('value') or '').replace('\n', ' ')
        import re
        strip = lambda s: re.sub('<[^>]+>', '', s).strip()
        out.append({'title': pg['title'], 'thumb': ii.get('thumburl') or ii['url'], 'orig': ii['url'], 'w': ii.get('width'), 'h': ii.get('height'),
                    'license': strip(g('LicenseShortName')), 'artist': strip(g('Artist'))[:80], 'credit': strip(g('Credit'))[:80],
                    'page': ii.get('descriptionurl')})
    return out

if __name__ == '__main__':
    if sys.argv[1] == 'search':
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 6
        hits = [x['title'] for x in api(action='query', list='search', srsearch=sys.argv[2], srnamespace=6, srlimit=n)['query']['search']]
        for x in info(hits) if hits else []:
            print(f"{x['license']:<14} {x['w']}x{x['h']} | {x['title']} | {x['artist']}")
    else:
        title, dst = sys.argv[2], Path(sys.argv[3]); w = int(sys.argv[4]) if len(sys.argv) > 4 else 1280
        w = min((960, 1280, 1920), key=lambda s: abs(s - w))
        x = info([title], w)[0]
        dst.parent.mkdir(parents=True, exist_ok=True)
        src = x['thumb']   # standard-size thumbnails only (Wikimedia asks for cached sizes: 960, 1280, ...)
        with urllib.request.urlopen(urllib.request.Request(src, headers=UA), timeout=120) as r: dst.write_bytes(r.read())
        if src == x['orig']:
            from PIL import Image
            im = Image.open(dst).convert('RGB'); im.thumbnail((w, w * 2)); im.save(dst, quality=90)
        cf = dst.parent / 'credits.json'
        cr = json.loads(cf.read_text()) if cf.exists() else {}
        cr[dst.name] = {k: x[k] for k in ('title', 'license', 'artist', 'credit', 'page')}
        cf.write_text(json.dumps(cr, indent=1))
        print('saved', dst, x['license'], '|', x['artist'])
