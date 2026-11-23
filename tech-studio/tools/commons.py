"""Free photos from Wikimedia Commons with licence + credit, paced (the API rate-limits this IP).
Usage: python3 tools/commons.py fetch "File:Name.jpg" [out_name]      -> assets_img/<out_name> + credits.json entry
       python3 tools/commons.py search "query" [n]                       -> prints file titles
Only free licences (CC0, PD, CC BY, CC BY-SA) are accepted; credit goes in the video description."""
import json, sys, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / 'assets_img'
UA = {'User-Agent': 'TechDecodedStudio/1.0 (educational explainer videos)'}
API = 'https://commons.wikimedia.org/w/api.php?'
OK = ('cc0', 'public domain', 'pd', 'cc by', 'cc-by')


def get(url, tries=7):
    wait = 15
    for k in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or k == tries - 1:
                raise
            time.sleep(wait); wait *= 2


def search(q, n=8):
    d = json.loads(get(API + urllib.parse.urlencode(dict(action='query', format='json', list='search', srnamespace=6, srlimit=n, srsearch=q))))
    return [x['title'] for x in d['query']['search']]


def fetch(title, name=None, width=1280):
    d = json.loads(get(API + urllib.parse.urlencode(dict(action='query', format='json', titles=title, prop='imageinfo', iiprop='url|extmetadata', iiurlwidth=width))))
    p = next(iter(d['query']['pages'].values()))
    ii = p['imageinfo'][0]; m = ii['extmetadata']
    lic = m.get('LicenseShortName', {}).get('value', '')
    if not lic.lower().startswith(OK):
        raise SystemExit(f'not a free licence: {lic}')
    import re
    artist = re.sub('<[^>]+>', '', m.get('Artist', {}).get('value', '')).strip()
    name = name or title[5:].replace(' ', '_')
    time.sleep(3)
    (IMG / name).write_bytes(get(ii['thumburl']))
    cf = IMG / 'credits.json'
    cr = json.loads(cf.read_text()) if cf.exists() else {}
    cr[name] = dict(title=title, license=lic, artist=artist, page=ii['descriptionurl'])
    cf.write_text(json.dumps(cr, indent=1, ensure_ascii=False))
    print('saved', name, '|', lic, '|', artist[:60])


if __name__ == '__main__':
    if sys.argv[1] == 'search':
        print('\n'.join(search(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 8)))
    else:
        fetch(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
