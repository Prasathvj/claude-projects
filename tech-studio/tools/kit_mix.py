"""MIX KIT (owner review of ep06, 2026-11-23): one beat type 'mix' that combines all our styles in one scene:
old motion kit (pop cards, counters, bars, kinetic slams, 3D fly-ins), PAPERCUT (kit_props props, torn cards, photo
stickers/prints) and VOX (newspaper clippings, highlighter, stamps), with REAL logos and exact icons (kit_assets).
Every element is timed to a spoken word ('at': 'word' or ['word', nth] or a 0..1 fraction of the line), so the
picture changes every 1-2 s and explains the line with the sound off.

Element kinds (all take id, x, y, at, in = pop|drop|slide|slam|fly|fade|rise|left, rot):
  icon   ref='ph:bank-fill' size color paper(bool: on a torn paper disc) bg
  logo   ref='logos:google-icon' size paper(bool)
  photo  name='frontier.jpg' w mode=cut|print crop
  prop   p='chip' s text ... (any kit_props prop)
  card   icon label big w color count=[values]  (old pop card, torn paper)
  tag    text bg color size
  big    text size color   (kinetic headline; '*word*' = orange)
  clip   by text hi w      (Vox newspaper clipping; hi = phrase to underline in orange)
  stamp  text color size
  bars   rows=[[label, frac, color]] w   (bar race, grows at 'at')
  arrow  w color rot      (paper arrow)
Actions: {'do': 'move', 'id':..., 'at':..., x/y/scale/rot/fade} · {'do': 'count', 'id': card, 'at', 'values'} ·
         {'do': 'shake'|'ring'|'spin'|'bob'|'out', 'id', 'at'}"""
import html as _h
import kit_assets as KA
import kit_props as KPR

CSS = KPR.CSS + """
.mx { position:absolute; }
.mcard { position:absolute; background:#FFFAF2; border-radius:24px; padding:22px 30px; box-shadow:0 16px 36px rgba(74,50,28,.24); }
.mcard .ml { font:800 24px 'SD Text'; letter-spacing:3px; color:#8C6B5A; white-space:nowrap; }
.mcard .mb { font:900 84px 'SD Display'; color:#2A2018; line-height:1; letter-spacing:-2px; white-space:nowrap; }
.mrow { display:flex; align-items:center; gap:18px; }
.mtag { position:absolute; padding:10px 22px; border-radius:14px; font:800 32px 'SD Text'; white-space:nowrap; }
.mbig { position:absolute; font:900 96px 'SD Display'; color:#2A2018; line-height:1.02; letter-spacing:-2px; white-space:nowrap; }
.mbig b { color:#F87736; }
.mclip { position:absolute; background:#F4ECDD; padding:24px 30px; box-shadow:0 16px 36px rgba(74,50,28,.24); }
.mclip .cb { font:600 20px 'SD Text'; color:#8C6B5A; letter-spacing:2px; margin-bottom:10px; }
.mclip .ct { font:900 52px Georgia, serif; color:#2A2018; line-height:1.08; }
.mclip .ct u { text-decoration-color:#F87736; text-decoration-thickness:9px; text-underline-offset:6px; }
.mstamp { position:absolute; white-space:nowrap; font:900 120px 'SD Display'; border:12px solid; border-radius:20px; padding:0 28px; letter-spacing:5px; background:rgba(255,250,242,.55); }
.mbars .bl { font:800 30px 'SD Text'; color:#2A2018; margin:14px 0 8px; } .mbars .bt { height:54px; border-radius:12px; transform-origin:left center; }"""

FROM = {'pop': 'scale:0, rotation:-10, opacity:1', 'drop': 'y:-800, rotation:-8, opacity:1', 'slide': 'x:1500, rotation:10, opacity:1',
        'left': 'x:-1500, rotation:-10, opacity:1', 'rise': 'y:900, rotation:6, opacity:1', 'fade': 'opacity:0',
        'slam': 'scale:2.6, opacity:0', 'fly': 'opacity:0, scale:.75, rotationX:18, rotationY:-12, y:90'}
EASE = {'slam': ('power4.in', .22), 'fly': ('expo.out', .6), 'fade': ('power2.out', .4)}


def _star(t):
    out, on = '', False
    for k, part in enumerate(_h.escape(t).split('*')):
        out += f'<b>{part}</b>' if k % 2 else part
    return out


def register(B):
    def T(i, at):
        if isinstance(at, (int, float)):
            return B.wfrac(i, at)
        w, n = (at if isinstance(at, (list, tuple)) else (at, 0))
        return max(0.02, B.bword(i, w.lower(), n) - 0.08)

    def el_html(sid, k, e):
        kind = e['k']; eid = f'{sid}-{e.get("id", "m" + str(k))}'
        pos = f'left:{e.get("x", 0)}px; top:{e.get("y", 0)}px;'
        rot = f'rotate:{e["rot"]}deg;' if e.get('rot') else ''
        if kind in ('icon', 'logo'):
            inner = (KA.paper_icon(e['ref'], e.get('size', 120), e.get('color', '#2A2018'), e.get('bg', '#FFFAF2')) if e.get('paper')
                     else KA.icon(e['ref'], e.get('size', 120), e.get('color')))
            return eid, f'<div class="mx" id="{eid}" style="{pos}{rot}">{inner}</div>'
        if kind == 'photo':
            return eid, f'<div class="mx" id="{eid}" style="{pos}">{KA.sticker(e["name"], B.P, e.get("w", 460), extra=f"transform:rotate({e.get("rot", 0)}deg)", mode=e.get("mode", "print"), crop=e.get("crop"))}</div>'
        if kind == 'prop':
            it = {kk: vv for kk, vv in e.items() if kk not in ('k', 'id', 'at', 'in')}
            pid, h = KPR.prop_html(sid, f'p{k}', it)
            return pid, h
        if kind == 'card':
            ic = KA.icon(e['icon'], e.get('isize', 60), e.get('color', '#F87736')) if e.get('icon') else ''
            return eid, (f'<div class="mcard qcard" id="{eid}" style="{pos}{rot}{"min-width:" + str(e["w"]) + "px;" if e.get("w") else ""}"><div class="mrow">{ic}<div>'
                         f'<div class="ml">{_h.escape(e.get("label", ""))}</div><div class="mb" id="{eid}-v" style="{"color:" + e["bcolor"] + ";" if e.get("bcolor") else ""}{"font-size:" + str(e["bsize"]) + "px;" if e.get("bsize") else ""}">{_star(e.get("big", ""))}</div></div></div></div>')
        if kind == 'tag':
            return eid, f'<div class="mtag" id="{eid}" style="{pos}{rot}background:{e.get("bg", "#2A2018")}; color:{e.get("color", "#FFFAF2")}; font-size:{e.get("size", 32)}px">{_star(e["text"])}</div>'
        if kind == 'big':
            return eid, f'<div class="mbig" id="{eid}" style="{pos}{rot}font-size:{e.get("size", 96)}px; color:{e.get("color", "#2A2018")}">{_star(e["text"])}</div>'
        if kind == 'clip':
            t = _h.escape(e['text'])
            if e.get('hi'):
                t = t.replace(_h.escape(e['hi']), f'<u>{_h.escape(e["hi"])}</u>', 1)
            return eid, f'<div class="mclip qclip" id="{eid}" style="{pos}{rot}width:{e.get("w", 700)}px"><div class="cb">{_h.escape(e.get("by", ""))}</div><div class="ct">{t}</div></div>'
        if kind == 'stamp':
            c = e.get('color', '#E0471C')
            return eid, f'<div class="mstamp" id="{eid}" style="{pos}rotate:{e.get("rot", -12)}deg; color:{c}; border-color:{c}; font-size:{e.get("size", 120)}px">{_h.escape(e["text"])}</div>'
        if kind == 'bars':
            rows = ''.join(f'<div class="bl">{_h.escape(lab)}</div><div class="bt" id="{eid}-b{j}" style="width:{int(e.get("w", 900) * fr)}px; background:{col}"></div>'
                           for j, (lab, fr, col) in enumerate(e['rows']))
            return eid, f'<div class="mx mbars" id="{eid}" style="{pos}width:{e.get("w", 900)}px">{rows}</div>'
        if kind == 'arrow':
            it = dict(p='arrow', x=e.get('x', 0), y=e.get('y', 0), len=e.get('w', 300), c=e.get('c', 'o'), rot=e.get('rot', 0))
            pid, h = KPR.prop_html(sid, f'a{k}', it)
            return pid, h
        raise KeyError(kind)

    def t_mix(i, sid, v):
        body, sc, ids = [], [], {}
        times = [T(i, e.get('at', 0.02 + k * 0.05)) for k, e in enumerate(v['els'])]
        first = min(range(len(times)), key=lambda k: times[k])
        if times[first] > 0.5:          # never open on an empty stage: the first element lands at once
            for k in range(len(times)):
                if abs(times[k] - times[first]) < 0.05:
                    times[k] = 0.1
        for k, e in enumerate(v['els']):
            eid, h = el_html(sid, k, e); body.append(h); ids[e.get('id', 'm' + str(k))] = eid
            t = times[k]; how = e.get('in', 'pop')
            ease, d = EASE.get(how, ('back.out(1.6)', .38))
            to = 'x:0, y:0, scale:1, rotation:0, rotationX:0, rotationY:0, opacity:1'
            sc.append(f'    tl.set("#{eid}", {{ opacity:0 }}, 0);')
            sc.append(f'    tl.fromTo("#{eid}", {{ {FROM[how]} }}, {{ {to}, duration:{d}, ease:"{ease}", immediateRender:false }}, {t});')
            if e['k'] == 'bars':
                for j in range(len(e['rows'])):
                    sc.append(f'    tl.fromTo("#{eid}-b{j}", {{ scaleX:0 }}, {{ scaleX:1, duration:{e.get("grow", [.5] * 9)[j] if isinstance(e.get("grow"), list) else .6}, ease:"power2.out", immediateRender:false }}, {round(t + .2 + j * e.get("gap", .35), 3)});')
                    sc.append(f'    tl.set("#{eid}-b{j}", {{ scaleX:0 }}, 0);')
        for a in v.get('acts', []):
            eid = ids[a['id']]; t = T(i, a['at']); do = a['do']
            if do == 'count':
                vals = a['values']; dt = a.get('dt', .08)
                for j, val in enumerate(vals):
                    sc.append(f'    tl.set("#{eid}-v", {{ innerHTML:{_h.escape(val)!r} }}, {round(t + j * dt, 3)});')
            elif do == 'move':
                props = [f'{g}:{a[kk]}' for kk, g in (('x', 'x'), ('y', 'y'), ('rot', 'rotation'), ('scale', 'scale')) if kk in a]
                if a.get('fade'): props.append('opacity:0')
                sc.append(f'    tl.to("#{eid}", {{ {", ".join(props)}, duration:{a.get("d", .45)}, ease:"power2.inOut" }}, {t});')
            elif do == 'shake':
                sc.append(f'    tl.fromTo("#{eid}", {{ x:0 }}, {{ x:12, duration:.05, yoyo:true, repeat:5, ease:"none", immediateRender:false }}, {t});')
            elif do == 'spin':
                sc.append(f'    tl.fromTo("#{eid}", {{ rotation:0 }}, {{ rotation:{a.get("deg", 360)}, duration:{a.get("d", 2.4)}, ease:"none", immediateRender:false }}, {t});')
            elif do == 'bob':
                sc.append(f'    tl.fromTo("#{eid}", {{ y:0 }}, {{ y:-16, duration:.4, yoyo:true, repeat:{a.get("n", 5)}, ease:"sine.inOut", immediateRender:false }}, {t});')
            elif do == 'out':
                sc.append(f'    tl.to("#{eid}", {{ opacity:0, scale:.6, duration:.25, ease:"power2.in" }}, {t});')
            elif do == 'ring':
                sc.append(f'    tl.fromTo("#{eid}", {{ scale:1 }}, {{ scale:1.12, duration:.15, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false }}, {t});')
        return '\n'.join(body), sc, CSS

    B.T['mix'] = t_mix
    B.SFX_BY_TYPE['mix'] = [(0.05, 'whoosh', .4), (0.35, 'pop', .4), (0.7, 'pop', .35)]
