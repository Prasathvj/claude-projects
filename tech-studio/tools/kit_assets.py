"""ASSET KIT (owner review 2026-11-23): exact, content-specific visuals, all free.
icon('logos:google-icon', 160)            -> inline SVG of a real brand logo (Iconify 'logos', colour) or any icon set
icon('ph:bank-fill', 140, '#2A2018')      -> single-colour icon (ph, tabler, mdi, simple-icons) tinted to our palette
sticker('frontier.jpg', w=520)            -> real photo cut out (rembg) as a PAPERCUT STICKER: torn white border, grain, shadow
paper_icon(...)                           -> icon on a torn paper disc/tile, so icons sit in the papercut world
Icon sets live in hf/lib/node_modules/@iconify-json/<set>/icons.json; photos in assets_img/ (credits.json)."""
import json, shutil
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / 'hf/lib/node_modules/@iconify-json'
IMG = ROOT / 'assets_img'
CUT = IMG / 'cut'
USED = {}          # photos used in the current video -> credits for the description


@lru_cache(None)
def _set(prefix):
    return json.loads((LIB / prefix / 'icons.json').read_text())


def _resolve(prefix, name):
    s = _set(prefix)
    if name in s['icons']:
        return s['icons'][name], s
    al = s.get('aliases', {}).get(name)
    if al:
        ic, _ = _resolve(prefix, al['parent'])
        return {**ic, **{k: v for k, v in al.items() if k != 'parent'}}, s
    raise KeyError(f'{prefix}:{name}')


def icon(ref, size=120, color=None, extra=''):
    prefix, name = ref.split(':', 1)
    ic, s = _resolve(prefix, name)
    w = ic.get('width', s.get('width', 16)); h = ic.get('height', s.get('height', 16))
    body = ic['body']
    style = f'color:{color};' if color else ''
    hh = round(size * h / w)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{ic.get("left", 0)} {ic.get("top", 0)} {w} {h}" width="{size}" height="{hh}" '
            f'style="{style}display:block;{extra}">{body}</svg>')


def paper_icon(ref, size=120, color='#2A2018', bg='#FFFAF2', pad=34, extra='', shape='50%'):
    """icon on a torn paper disc (cut-paper look matches kit_paper)"""
    d = size + 2 * pad
    return (f'<div class="kpi" style="width:{d}px;height:{d}px;border-radius:{shape};background:{bg};display:flex;align-items:center;'
            f'justify-content:center;filter:url(#kp-tex) drop-shadow(0 7px 0 rgba(74,50,28,.22)) drop-shadow(0 16px 12px rgba(74,50,28,.22));{extra}">'
            f'{icon(ref, size, color)}</div>')


def _cutout(name):
    CUT.mkdir(parents=True, exist_ok=True)
    out = CUT / (Path(name).stem + '_cut.png')
    if out.exists():
        return out
    from rembg import remove, new_session
    from PIL import Image
    im = Image.open(IMG / name).convert('RGB')
    remove(im, session=new_session('isnet-general-use')).save(out)
    return out


def _paperize(name, seed=7):
    """white torn border + grain + cut shadow around the cut-out subject"""
    out = CUT / (Path(name).stem + '_paper.png')
    if out.exists():
        return out
    from PIL import Image, ImageFilter, ImageChops
    import random
    random.seed(seed)
    im = Image.open(_cutout(name)).convert('RGBA')
    bb = im.split()[3].point(lambda v: 255 if v > 40 else 0).getbbox()
    im = im.crop(bb); im.thumbnail((1100, 1100))
    pad = 46; W, H = im.size[0] + 2 * pad, im.size[1] + 2 * pad
    base = Image.new('RGBA', (W, H), (0, 0, 0, 0)); base.paste(im, (pad, pad), im)
    a = base.split()[3].point(lambda v: 255 if v > 60 else 0)
    border = a.filter(ImageFilter.MaxFilter(27))
    noise = Image.effect_noise((W, H), 70).filter(ImageFilter.GaussianBlur(2.2)).point(lambda v: 255 if v > 116 else 0)
    rough = ImageChops.multiply(border, ImageChops.lighter(noise, a.filter(ImageFilter.MaxFilter(17))))
    rough = rough.filter(ImageFilter.MedianFilter(5))
    paper = Image.new('RGBA', (W, H), (255, 250, 242, 255)); paper.putalpha(rough)
    sh = Image.new('RGBA', (W, H), (74, 50, 28, 0)); sh.putalpha(rough.point(lambda v: int(v * .42)).filter(ImageFilter.GaussianBlur(9)))
    res = Image.new('RGBA', (W + 26, H + 30), (0, 0, 0, 0))
    res.alpha_composite(sh, (10, 18)); res.alpha_composite(paper, (0, 0)); res.alpha_composite(base, (0, 0))
    g = Image.effect_noise(res.size, 28).convert('L')
    res.alpha_composite(Image.merge('RGBA', (g, g, g, res.split()[3].point(lambda v: int(v * .09)))))
    res.save(out)
    return out


def sticker(name, project, w=520, extra='', cls='stk'):
    """papercut photo sticker <img>, copied into the project; records the credit"""
    src = _paperize(name)
    dst = Path(project) / 'assets/img'; dst.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, dst / src.name)
    cr = json.loads((IMG / 'credits.json').read_text()) if (IMG / 'credits.json').exists() else {}
    USED[name] = cr.get(name, {})
    return f'<img class="{cls}" src="assets/img/{src.name}" style="width:{w}px;display:block;{extra}"/>'


def credits_text():
    lines = []
    for n, c in USED.items():
        if c:
            lines.append(f'• {c["title"][5:]}: {c.get("artist") or "Wikimedia Commons"}, {c["license"]}, {c["page"]}')
    return '\n'.join(lines)
