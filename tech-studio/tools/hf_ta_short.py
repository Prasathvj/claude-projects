"""Tamil versions of the English explainer/news Shorts (owner 2026-11-24: news02, news01, tip01 → TechDecoded தமிழ்).
Re-runs the ENGLISH generator on the Tamil timeline: cue words are mapped English word -> Tamil word (CUE), on-screen
headings are translated (TR), Tamil glyphs come from Tamil fonts merged into the same families by unicode-range
(exact weights, so Latin text keeps its own font), and a spoken Tamil subscribe line gets its own outro scene.
Usage: THEME=cream GRID=lines python3 tools/hf_ta_short.py news02     (Tamil timeline: src/episodes/news02ta-short.timeline.json)"""
import importlib, json, os, re, shutil, sys
from pathlib import Path
K = sys.argv[1]
os.environ['SHORT_ID'] = f'{K}ta-short'
os.environ['CAP_MAX'] = '2'   # Tamil words are long: 2 words per caption so a group never wraps
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import hf_news01_short as L   # noqa: E402  (loaded first with the Tamil SHORT_ID; the English module reuses it)

EP = {
 'news02': dict(module='hf_news02_short', scenes=['s0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8'], sub_tag='Tech news, தமிழில்.',
   CUE={0: {'biggest': 'மிகப்', 'rivals': 'போட்டியாளர்களும்'}, 1: {'priced': '83', 'above': 'அதிகம்.'}, 2: {'raised': '80', 'spacexs': 'SpaceX-ஓட'},
        3: {'worth': 'மதிப்பு'}, 4: {'launched': 'launch', 'later': 'மூணே'}, 5: {'opened': 'open', 'cooled': 'இறங்கி,'},
        6: {'strange': 'விசித்திரமான', 'google': 'Google,', 'microsoft': 'Microsoft,', 'nvidia': 'Nvidia'}, 7: {'chips': 'chips-உம்', 'cloud': 'cloud-உம்'},
        8: {'wins': 'ஜெயிக்கும்போதும்,', 'shovels': 'மண்வெட்டி'}, 9: {'subscribe': 'சப்ஸ்க்ரைப்'}},
   TR=[('BIGGEST IPO <span>EVER</span>', 'வரலாற்றுலயே பெரிய <span>IPO</span>'), ('RAISED IN THE IPO', 'IPO-ல திரட்டியது'),
       ('…AND ITS RIVALS HELPED PAY?', '…போட்டியாளர்களும் பணம் போட்டாங்களா?'), ('ABOVE THE RANGE ↑', 'RANGE-ஐ விட அதிகம் ↑'),
       ('IPO price $83', 'IPO விலை $83 (≈ ₹7,700)'), ('PRICED NOV 18, 2026', 'விலை நிர்ணயம் 18 நவ. 2026'), ('LARGEST IPOs ON RECORD', 'வரலாற்றுலயே பெரிய IPO-க்கள்'),
       ('SpaceX (previous record)', 'SpaceX (முந்தைய record)'), ('BAR LENGTHS ILLUSTRATIVE', 'BAR நீளம் விளக்கத்துக்கு மட்டும்'),
       ('VALUED AT THE IPO PRICE', 'IPO விலையில மதிப்பு'), ('>TRILLION<', '>டிரில்லியன்<'), ('$1.5T company', '$1.5T கம்பெனி'),
       ('Claude launches', 'Claude launch'), ('3 YEARS', '3 வருஷம்'), ('DAY ONE · NOV 19, 2026', 'முதல் நாள் · 19 நவ. 2026'),
       ('OPENED +34%', 'OPEN +34%'), ('CLOSED +17%', 'CLOSE +17%'), ('first day of trading', 'முதல் trading நாள்'), ('THE <span>STRANGE</span> PART', '<span>விசித்திரமான</span> விஷயம்'),
       ('WHY WOULD THEY BUY IN?', 'அவங்க ஏன் வாங்குனாங்க?'), ('PRIVATE PLACEMENT ALONGSIDE THE IPO', 'IPO கூடவே PRIVATE PLACEMENT'),
       ('AI RUNS ON THEM', 'AI இதுல தான் ஓடுது'), ('AI GOLD RUSH', 'AI தங்க வேட்டை'), ('SELL THE <span>SHOVELS</span>', 'மண்வெட்டி <span>விக்கிறவங்க</span>'),
       ('When AI companies win, chip and cloud companies win too.', 'AI கம்பெனிகள் ஜெயிச்சா, chip & cloud கம்பெனிகளும் ஜெயிக்கும்.')],
   moods='shock point happy shock think shrug think focus happy happy'),
 'news01': dict(module='hf_news01_short', scenes=['s0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8'], sub_tag='Tech news, தமிழில்.',
   CUE={0: {'sends': 'அனுப்புது.', 'never': 'சொல்லவே', 'who': 'யாருக்கு?'}, 1: {'answered': 'பதில்', 'not': 'அது'},
        2: {'outside': 'வெளியில', 'everything': 'எல்லாமே', 'authorized': 'அனுமதிச்சதா'}, 3: {'ignores': 'மீறுனாலும்'},
        4: {'lend': 'சாவியை', 'they': 'party', 'you': 'Bill'}, 5: {'reports': 'reports', 'same': 'இதே'},
        6: {'catch': 'விஷயம்:', 'own': 'சொந்த', 'only': 'மட்டும்'}, 7: {'hidden': 'ஒளிஞ்சிருக்கிற', 'hijacked': 'hijack'},
        8: {'ask': 'கேள்வி', 'banks': 'bank-ஓட', 'someone': 'வேற'}, 9: {'subscribe': 'சப்ஸ்க்ரைப்'}},
   TR=[('WHO <span>PAYS?</span>', 'நஷ்டம் <span>யாருக்கு?</span>'), ('NOBODY PRESSED SEND', 'யாரும் SEND அழுத்தல'), ('THE ANSWER:', 'பதில்:'),
       ('BIGGEST BANKS', 'பெரிய BANK-கள்ல ஒண்ணு'), ("ONE OF AMERICA'S", 'அமெரிக்காவோட'), ('NOT THE BANK.', 'BANK இல்ல.'), ('AUTHORIZED BY YOU', 'உங்க அனுமதி ✓'), ('Lend your keys', 'சாவி கொடுக்கறீங்க'), ('They throw a party', 'அவர் party வைக்கிறார்'), ('You get the bill', 'Bill உங்களுக்கு'),
       ('An outside AI agent uses your login…', 'வெளி AI agent உங்க login-ஐ use பண்ணுது…'), ('…and every action it takes…', '…அது செய்யுற ஒவ்வொரு action-உம்…'),
       ('…is treated as authorized by you.', '…நீங்களே அனுமதிச்சதா கணக்கு.'), ('PARAPHRASED FROM REPORTING', 'செய்திகளின் சுருக்கம்'),
       ('SIMPLIFIED RECREATION', 'எளிமையான RECREATION'), ('EVEN IF IT', 'அது உங்களை'), ('IGNORES YOU', 'மீறுனாலும்'),
       ("Don't send", 'அனுப்பாதே'), ('anything!', 'எதையும்!'), ('Everything they do = you', 'அவங்க செய்யுறது எல்லாம் = நீங்க'),
       ('THE SAME LINE', 'இதே வழி'), ('SAME IDEA: YOUR LOGIN = YOUR RESPONSIBILITY', 'உங்க LOGIN = உங்க பொறுப்பு'),
       ('PER REPORTS · NO BANKS NAMED HERE', 'செய்திகளின்படி · BANK பெயர்கள் இங்க இல்ல'), ('THE <span>CATCH</span>', 'ஆனா <span>ஒரு விஷயம்</span>'),
       ("Bank's own AI tools", 'Bank-ஓட சொந்த AI tools'), ('Not covered by this rule', 'இந்த rule பொருந்தாது'), ('Outside AI agents', 'வெளி AI agents'),
       ('ILLUSTRATION · NOT A REAL SITE', 'ILLUSTRATION · உண்மையான SITE இல்ல'), ('ILLUSTRATION · BANK APP', 'ILLUSTRATION · BANK APP'),
       ('SEE: HOW A WEBPAGE HIJACKS AI (FULL VIDEO)', 'WEBPAGE எப்படி AI-ஐ HIJACK பண்ணுது (FULL VIDEO, ENGLISH)'),
       ('BEFORE YOU SHARE A BANK LOGIN, ASK:', 'BANK LOGIN கொடுக்கறதுக்கு முன்னாடி கேளுங்க:'), ('Your bank&#x27;s', 'உங்க bank-ஓட'), ("Your bank's", 'உங்க bank-ஓட'),
       ('own tool?', 'சொந்த tool-ஆ?'), ('>or<', '>இல்ல<'), ('>Someone<', '>வேற<'), ('else&#x27;s?', 'யாரோடதா?'), ("else's?", 'யாரோடதா?'),
       ('How agents get hijacked → full video on the channel', 'Agents எப்படி hijack ஆகுது → full video (English channel)'), ('Today&#x27;s top deals', 'இன்றைய top deals')],
   moods='point shock think worry shock shrug focus think worry happy'),
}
C = EP[K]

_wl = L.wl
def wl(i, word, nth=0):
    b = L.BE[i]; cue = C['CUE'][i][word]
    hit = next((x for x in b['words'] if x['w'] == cue or x['w'].startswith(cue)), None)
    if hit is None:
        raise KeyError(f'line {i}: cue {cue!r} not in {[x["w"] for x in b["words"]]}')
    return round(b['start'] + hit['s'] - L.S[f's{i}'][0], 3)
L.wl = wl
M = importlib.import_module(C['module'])   # binds the patched wl

TAF = ''.join(f"@font-face {{ font-family:'{fam}'; src:url('assets/fonts/{f}'); font-weight:{w}; font-style:{st}; unicode-range:U+0B80-0BFF,U+20B9; }}\n"
              for fam, f, w, st in (('SD Display', 'catamaran-tamil-900-normal.woff2', 900, 'normal'), ('SD Display', 'catamaran-tamil-900-normal.woff2', 700, 'normal'),
                                    ('SD Mono', 'mukta-malar-tamil-800-normal.woff2', 700, 'normal'), ('SD Text', 'mukta-malar-tamil-800-normal.woff2', 600, 'normal'),
                                    ('SD Text', 'mukta-malar-tamil-800-normal.woff2', 500, 'normal'), ('SD Serif', 'mukta-malar-tamil-800-normal.woff2', 600, 'italic')))
TA = re.compile(r'[\u0B80-\u0BFF][\u0B80-\u0BFF\s\-]*[\u0B80-\u0BFF]|[\u0B80-\u0BFF]')
def _text(seg):   # Tamil runs in text nodes get letter-spacing:0 (English letter-spacing splits Tamil letters apart)
    return re.sub(r'>([^<]+)<', lambda m: '>' + TA.sub(lambda t: f'<tx style="letter-spacing:0">{t.group(0)}</tx>', m.group(1)) + '<', seg)
def tamilize(html):
    for a, b in C['TR']:
        html = html.replace(a, b)
    parts = re.split(r'(<script>.*?</script>|<style>.*?</style>|<svg.*?</svg>)', html, flags=re.S)
    html = ''.join(p if p.startswith(('<script>', '<style>', '<svg')) else _text(p) for p in parts)
    html = html.replace(".w em { position:relative; font:700 66px", ".w em { position:relative; font:700 58px")
    return html.replace('<style>', '<style>\n' + TAF, 1)

def sub_scene(i):
    sid = f's{i}'
    t = wl(i, 'subscribe')
    body, sc, css, tc = L.subscribe(sid, t)
    body = body.replace('AI &amp; tech news, decoded.', C['sub_tag']).replace('>with Max<', '>தமிழ்<')
    return L.scene(sid, f'<div id="{sid}-all" class="all">{body}</div>', '\n'.join([L.punch(sid)] + sc), css), tc

if __name__ == '__main__':
    P = L.P
    src = ROOT / f'hf/{K}-short'
    (P / 'assets').mkdir(parents=True, exist_ok=True)
    for f in ('fonts', 'sfx', 'gsap.min.js'):
        s, d = src / 'assets' / f, P / 'assets' / f
        if not d.exists():
            shutil.copytree(s, d) if s.is_dir() else shutil.copy(s, d)
    for f in ('catamaran-tamil-900-normal.woff2', 'mukta-malar-tamil-800-normal.woff2'):
        shutil.copy(ROOT / 'hf/knight01-dossier/fonts' / f, P / 'assets/fonts' / f)
    tl = json.loads((ROOT / f'src/episodes/{K}ta-short.timeline.json').read_text())
    shutil.copy(ROOT / 'public' / tl['vo'], P / 'assets/vo.wav'); shutil.copy(ROOT / 'public' / tl['music'], P / 'assets/bgm.wav')
    for f in ('hyperframes.json',):
        shutil.copy(src / f, P / f)
    (P / 'meta.json').write_text(json.dumps({'id': f'{K}ta-short', 'name': f'{K}ta-short', 'createdAt': '2026-11-24T14:00:00.000Z'}))
    ml = (src / 'max_layer.html').read_text().replace(f'/{K}-short/', f'/{K}ta-short/')
    (P / 'max_layer.html').write_text(ml)
    (P / 'max_render.cjs').write_text((src / 'max_render.cjs').read_text().replace(f'{K}-short', f'{K}ta-short'))
    comp = P / 'compositions'; comp.mkdir(parents=True, exist_ok=True)
    for f in comp.glob('*.html'): f.unlink()
    for k, name in enumerate(C['scenes']):
        (comp / f's{k}.html').write_text(tamilize(getattr(M, name)()))
    n = len(C['scenes'])
    sub, tc = sub_scene(n)
    (comp / f's{n}.html').write_text(tamilize(sub))
    eng = sorted(M.sfx_list()) if hasattr(M, 'sfx_list') else []
    s0 = L.S[f's{n}'][0]
    L.sfx_list = lambda: sorted(eng + [(s0, 'whoosh', .5), (s0 + tc, 'click', .9), (s0 + tc + .1, 'ding', .7)])
    (comp / 'bg.html').write_text(L.bg())
    (comp / 'caps.html').write_text(tamilize(L.captions()))
    (P / 'index.html').write_text(L.index())
    left = sorted({m for f in comp.glob('s*.html') for m in re.findall(r'>([A-Z][A-Z ,.?!…\'’]{6,})<', f.read_text())})
    print('written', P, L.DUR, '| untranslated caps-text left:', left)
