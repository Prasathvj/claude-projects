"""PRO UI KIT (owner 2026-11-23, after the ast01 Short): the professional product-demo look for long videos, on our cream + dots
background. Extra element kinds for kit_mix 'mix' beats (all word-timed with 'at', like every mix element):
  win     title w h body(html)            light app window with traffic-light bar
  tile    ref size box label color        icon / logo on a clean rounded app tile (replaces paper discs)
  menu    items=[[label, small]] w search hi   model menu / list; act {'do':'pick','id','at','n'} highlights item n
  dialog  title sub btns icon w           permission dialog (first button = primary)
  toggle  label icon w                    settings row with a switch; act {'do':'on','id','at'}
  seg     opts=['Chat','Work'] sel        segmented control; act {'do':'sel','id','at','n'}
  phone   msgs=[[role, text, at]] w h     ChatGPT-style phone chat; each message appears at its word ('user' bubble / 'ai' text)
  type    text prefix w h dur             prompt box; prefix chip (e.g. @Computer) then the text types in
  pcard   name price ok hi w              plan card with tick / cross
  chip    text icon color size            pill label with icon
  toast   text icon                       green success toast
  cursor  pts=[[x, y, at, click]] label   agent cursor that glides and clicks (blue 'Astra' label + ripple)
  html    html w                          any raw html
All UI mockups are illustrations: put an 'ILLUSTRATION' tag on screens that imitate a real app."""
import html as _h
import kit_assets as KA

CSS = """.pw { position:absolute; background:#FFFAF7; border:2px solid #E8D6C6; border-radius:22px; box-shadow:0 30px 70px rgba(74,50,28,.16); overflow:hidden; }
.pbar { height:46px; background:#FFF4EA; display:flex; align-items:center; gap:10px; padding:0 18px; font:600 20px 'SD Text'; color:#8C6B5A; border-bottom:1px solid #EFE3D7; white-space:nowrap; }
.pbar i { width:13px; height:13px; border-radius:7px; display:inline-block; } .pbar .r { background:#FF5F57; } .pbar .y { background:#FEBC2E; } .pbar .g { background:#28C840; }
.ptile { position:absolute; background:#FFFAF7; border:2px solid #E8D6C6; border-radius:30px; display:flex; align-items:center; justify-content:center; box-shadow:0 16px 36px rgba(74,50,28,.14); }
.ptl { position:absolute; left:50%; transform:translateX(-50%); top:calc(100% + 12px); font:800 24px 'SD Text'; color:#2A2018; white-space:nowrap; }
.pmenu { position:absolute; background:#FFFAF7; border:2px solid #E2CBB8; border-radius:20px; padding:10px; box-shadow:0 26px 60px rgba(74,50,28,.16); }
.pmi { padding:14px 20px; border-radius:12px; font:700 28px 'SD Text'; color:#2A2018; display:flex; justify-content:space-between; align-items:center; gap:24px; white-space:nowrap; }
.pmi small { font:600 20px 'SD Text'; color:#A48A78; } .pms { border:2px solid #E8D6C6; color:#8C6B5A; justify-content:flex-start; gap:14px; }
.pdlg { position:absolute; background:#FFFAF7; border:2px solid #E2CBB8; border-radius:26px; padding:32px; box-shadow:0 34px 80px rgba(74,50,28,.18); }
.pdt { font:900 36px 'SD Display'; color:#2A2018; } .pds { font:600 24px 'SD Text'; color:#8C6B5A; margin:12px 0 24px; }
.pbtn { display:inline-block; padding:14px 24px; border-radius:14px; font:800 26px 'SD Text'; margin-right:12px; background:#EFE3D7; color:#2A2018; white-space:nowrap; } .pbtn.p { background:#F87736; color:#1A0A04; }
.ptog { width:96px; height:52px; border-radius:26px; background:#E2CBB8; position:relative; flex:none; } .ptog i { position:absolute; left:6px; top:6px; width:40px; height:40px; border-radius:20px; background:#8C6B5A; }
.pseg { position:absolute; display:flex; background:#EFE3D7; border-radius:18px; padding:6px; border:2px solid #E8D6C6; } .pseg b { padding:12px 34px; border-radius:13px; font:800 30px 'SD Text'; color:#A48A78; }
.pph { position:absolute; background:#FFFFFF; border:12px solid #2A2018; border-radius:52px; overflow:hidden; box-shadow:0 30px 70px rgba(74,50,28,.22); }
.pph .st { height:40px; display:flex; justify-content:space-between; padding:12px 26px 0; font:700 16px 'SD Text'; color:#2A2018; }
.pph .hd { text-align:center; font:800 18px 'SD Text'; color:#2A2018; padding:6px 0 10px; border-bottom:1px solid #EEE; }
.pph .ms { padding:16px 18px; display:flex; flex-direction:column; gap:14px; }
.pph .u { align-self:flex-end; max-width:78%; background:#F1ECE8; border-radius:20px; padding:12px 16px; font:600 19px 'SD Text'; color:#2A2018; line-height:1.3; }
.pph .a { align-self:flex-start; max-width:92%; font:500 19px 'SD Text'; color:#2A2018; line-height:1.4; } .pph .a b { color:#F87736; }
.pph .in { position:absolute; left:14px; right:14px; bottom:16px; height:52px; border-radius:26px; border:1.5px solid #E6E0DA; display:flex; align-items:center; padding:0 18px; font:500 18px 'SD Text'; color:#A9A29C; }
.ptype { position:absolute; background:#FFFAF7; border:2px solid #E2CBB8; border-radius:24px; padding:24px 26px; font:600 32px 'SD Text'; color:#2A2018; line-height:1.4; box-shadow:0 20px 50px rgba(74,50,28,.12); }
.patc { background:rgba(28,126,214,.14); color:#1C6ED6; border-radius:10px; padding:2px 10px; }
.pcard2 { position:absolute; padding:24px 26px; border-radius:24px; background:#FFFAF7; border:2px solid #E8D6C6; box-shadow:0 16px 36px rgba(74,50,28,.12); }
.pcard2.hi { border:3px solid #F87736; box-shadow:0 0 0 6px rgba(248,119,54,.15), 0 16px 36px rgba(74,50,28,.14); }
.pcard2 h4 { font:900 42px 'SD Display'; color:#2A2018; margin:0; } .pcard2 p { font:700 24px 'SD Text'; color:#8C6B5A; margin:6px 0 0; white-space:nowrap; }
.pcard2 em { position:absolute; right:22px; top:18px; font:900 44px 'SD Display'; font-style:normal; }
.pchip { position:absolute; padding:12px 22px; border-radius:16px; background:#FFFAF7; border:2px solid #E2CBB8; font:800 28px 'SD Text'; color:#2A2018; display:flex; gap:12px; align-items:center; white-space:nowrap; box-shadow:0 10px 24px rgba(74,50,28,.10); }
.ptoast { position:absolute; padding:16px 24px; border-radius:16px; background:#E3F5E8; border:2px solid #2F9E44; font:800 28px 'SD Text'; color:#1E6B34; display:flex; gap:12px; align-items:center; white-space:nowrap; }
.pcur { position:absolute; left:0; top:0; z-index:20; } .pcur .lbl { position:absolute; left:38px; top:34px; background:#1C7ED6; color:#fff; font:800 20px 'SD Text'; padding:4px 12px; border-radius:10px; white-space:nowrap; }
.pring { position:absolute; left:0; top:0; width:64px; height:64px; border-radius:32px; border:4px solid #1C7ED6; opacity:0; z-index:19; }"""

CURSOR = ('<svg width="44" height="50" viewBox="0 0 28 32"><path d="M2 2 L2 26 L8.5 19.5 L13 30 L17.5 28 L13 18 L22 18 Z" '
          'fill="#FFFFFF" stroke="#111" stroke-width="2" stroke-linejoin="round"/></svg>')
KINDS = {'win', 'tile', 'menu', 'dialog', 'toggle', 'seg', 'phone', 'type', 'pcard', 'chip', 'toast', 'cursor', 'html'}
E = _h.escape


def _ic(ref, size, color=None):
    return KA.icon(ref, size, color) if ref else ''


def el(eid, e, pos, rot):
    k = e['k']
    if k == 'win':
        return (f'<div class="pw" id="{eid}" style="{pos}{rot}width:{e.get("w", 700)}px;height:{e.get("h", 440)}px"><div class="pbar"><i class="r"></i><i class="y"></i>'
                f'<i class="g"></i>&nbsp;{E(e.get("title", ""))}</div>{e.get("body", "")}</div>')
    if k == 'tile':
        sz = e.get('size', 90); bx = e.get('box', sz + 60)
        lab = f'<div class="ptl">{E(e["label"])}</div>' if e.get('label') else ''
        return f'<div class="ptile" id="{eid}" style="{pos}{rot}width:{bx}px;height:{bx}px">{_ic(e["ref"], sz, e.get("color"))}{lab}</div>'
    if k == 'menu':
        rows = ''
        if 'search' in e:
            rows += f'<div class="pmi pms">{_ic("ph:magnifying-glass-bold", 28, "#A48A78")}<span id="{eid}-q">{E(e.get("search") or "Search models")}</span></div>'
        for j, it in enumerate(e['items']):
            lab, sm = (it + [''])[:2] if isinstance(it, list) else (it, '')
            col = f'color:{it[2]};' if isinstance(it, list) and len(it) > 2 else ''
            rows += f'<div class="pmi" id="{eid}-i{j}" style="{col}">{E(lab)}<small>{E(sm)}</small></div>'
        return f'<div class="pmenu" id="{eid}" style="{pos}{rot}width:{e.get("w", 560)}px">{rows}</div>'
    if k == 'dialog':
        btns = ''.join(f'<span class="pbtn{" p" if j == 0 else ""}" id="{eid}-b{j}">{E(b)}</span>' for j, b in enumerate(e.get('btns', ['Allow once', 'Always allow', 'Deny'])))
        return (f'<div class="pdlg" id="{eid}" style="{pos}{rot}width:{e.get("w", 640)}px"><div style="display:flex;gap:16px;align-items:center">'
                f'{_ic(e.get("icon", "ph:shield-check-fill"), 52, "#F87736")}<div class="pdt">{E(e["title"])}</div></div><div class="pds">{E(e.get("sub", ""))}</div>{btns}</div>')
    if k == 'toggle':
        return (f'<div class="pmenu" id="{eid}" style="{pos}{rot}width:{e.get("w", 560)}px"><div class="pmi">{_ic(e.get("icon"), 36, e.get("color", "#1C7ED6"))}'
                f'<span style="flex:1">{E(e["label"])}</span><div class="ptog" id="{eid}-t"><i id="{eid}-k"></i></div></div></div>')
    if k == 'seg':
        sel = e.get('sel', 0)
        bs = ''.join(f'<b id="{eid}-o{j}" style="{"background:#FFFAF7;color:#2A2018;" if j == sel else ""}">{E(o)}</b>' for j, o in enumerate(e['opts']))
        return f'<div class="pseg" id="{eid}" style="{pos}{rot}">{bs}</div>'
    if k == 'phone':
        w = e.get('w', 330); h = e.get('h', 640)
        ms = ''.join(f'<div class="{"u" if r == "user" else "a"}" id="{eid}-m{j}">{t}</div>' for j, (r, t, _) in enumerate(e['msgs']))
        return (f'<div class="pph" id="{eid}" style="{pos}{rot}width:{w}px;height:{h}px"><div class="st"><span>9:41</span><span>5G ▮</span></div>'
                f'<div class="hd">{E(e.get("head", "ChatGPT"))}</div><div class="ms">{ms}</div><div class="in">Ask anything</div></div>')
    if k == 'type':
        pre = f'<span class="patc">{E(e["prefix"])}</span> ' if e.get('prefix') else ''
        return f'<div class="ptype" id="{eid}" style="{pos}{rot}width:{e.get("w", 760)}px;min-height:{e.get("h", 160)}px">{pre}<span id="{eid}-x"></span></div>'
    if k == 'pcard':
        ok = e.get('ok')
        mark = '' if ok is None else f'<em style="color:{"#2F9E44" if ok else "#E0471C"}">{"✓" if ok else "✗"}</em>'
        return (f'<div class="pcard2{" hi" if e.get("hi") else ""}" id="{eid}" style="{pos}{rot}width:{e.get("w", 300)}px"><h4>{E(e["name"])}</h4>'
                f'<p>{E(e.get("price", ""))}</p>{mark}</div>')
    if k == 'chip':
        return (f'<div class="pchip" id="{eid}" style="{pos}{rot}font-size:{e.get("size", 28)}px;{"border-color:" + e["border"] + ";" if e.get("border") else ""}">'
                f'{_ic(e.get("icon"), int(e.get("size", 28) * 1.3), e.get("color", "#F87736"))}{E(e["text"])}</div>')
    if k == 'toast':
        return f'<div class="ptoast" id="{eid}" style="{pos}{rot}">{_ic(e.get("icon", "ph:check-circle-fill"), 38, "#2F9E44")}{E(e["text"])}</div>'
    if k == 'cursor':
        x0, y0 = e['pts'][0][0], e['pts'][0][1]
        return (f'<div class="pcur" id="{eid}" style="transform:translate({x0}px,{y0}px)">{CURSOR}<div class="lbl">{E(e.get("label", "Astra"))}</div></div>'
                f'<div class="pring" id="{eid}-r"></div>')
    if k == 'html':
        return f'<div class="mx" id="{eid}" style="{pos}{rot}{"width:" + str(e["w"]) + "px;" if e.get("w") else ""}">{e["html"]}</div>'
    raise KeyError(k)


def dyn(eid, e, t, T, i):
    """extra timeline lines for elements that move on their own (cursor, typing, chat messages)"""
    k, sc = e['k'], []
    if k == 'cursor':
        pts = [(x, y, T(i, at), c) for x, y, at, c in e['pts']]
        for j in range(1, len(pts)):
            (px, py, pt, _), (x, y, tt, c) = pts[j - 1], pts[j]
            d = max(.25, min(.7, tt - pt - .05)); st = round(max(0.02, tt - d), 3)
            sc.append(f'    tl.fromTo("#{eid}", {{ x:{px}, y:{py} }}, {{ x:{x}, y:{y}, duration:{d:.2f}, ease:"power3.inOut", immediateRender:false }}, {st});')
            if c:
                sc.append(f'    tl.fromTo("#{eid} svg", {{ scale:1 }}, {{ scale:.82, duration:.08, yoyo:true, repeat:1, immediateRender:false }}, {round(tt, 3)});')
                sc.append(f'    tl.set("#{eid}-r", {{ x:{x - 28}, y:{y - 28} }}, {round(tt, 3)}); tl.fromTo("#{eid}-r", {{ opacity:1, scale:.3 }}, '
                          f'{{ opacity:0, scale:1.6, duration:.5, ease:"expo.out", immediateRender:false }}, {round(tt, 3)});')
    elif k == 'type':
        txt = e['text']; n = max(1, -(-len(txt) // 3)); d = e.get('dur', 1.6)
        for j in range(1, n + 1):
            sc.append(f'    tl.set("#{eid}-x", {{ innerHTML:{E(txt[:min(len(txt), j * 3)])!r} }}, {round(t + .35 + d * j / n, 3)});')
        sc.append(f'    tl.set("#{eid}-x", {{ innerHTML:"" }}, 0);')
    elif k == 'phone':
        for j, (_, _, at) in enumerate(e['msgs']):
            mt = T(i, at)
            sc.append(f'    tl.set("#{eid}-m{j}", {{ opacity:0 }}, 0);')
            sc.append(f'    tl.fromTo("#{eid}-m{j}", {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:.35, ease:"power2.out", immediateRender:false }}, {round(mt, 3)});')
    elif k == 'menu' and e.get('typeq'):
        q = e['typeq']; tq = T(i, e.get('qat', 0.3))
        for j in range(1, len(q) + 1):
            sc.append(f'    tl.set("#{eid}-q", {{ innerHTML:{E(q[:j])!r}, color:"#2A2018" }}, {round(tq + j * .07, 3)});')
    return sc


def act(eid, a, t):
    do = a['do']
    if do == 'pick':
        return [f'    tl.to("#{eid}-i{a["n"]}", {{ backgroundColor:"#F3DCCB", color:"#F87736", duration:.2 }}, {t});']
    if do == 'on':
        return [f'    tl.to("#{eid}-t", {{ backgroundColor:"#2F9E44", duration:.2 }}, {t}); tl.to("#{eid}-k", {{ x:44, backgroundColor:"#FFFFFF", duration:.2 }}, {t});']
    if do == 'sel':
        return [f'    tl.to("#{eid} b", {{ backgroundColor:"rgba(0,0,0,0)", color:"#A48A78", duration:.2 }}, {t}); '
                f'tl.to("#{eid}-o{a["n"]}", {{ backgroundColor:"#F87736", color:"#1A0A04", duration:.2 }}, {t});']
    if do == 'press':
        return [f'    tl.fromTo("#{eid}-b{a.get("n", 0)}", {{ scale:1 }}, {{ scale:.9, duration:.1, yoyo:true, repeat:1, immediateRender:false }}, {t});']
    return None
