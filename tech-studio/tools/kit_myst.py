"""TECH MYSTERIES kit (owner 2026-11-23: weekly series rotation; approved look test hf/mystery-look, Charon voice, Max 'B2' night hoodie
+ moonlight rim). Enable with STYLE=mystery THEME=navy: theme.apply() calls mysterize() on every composition:
  - background: near-black navy radial + drifting cold fog; overlay (in the chapters layer, above scenes): film grain, CRT scanlines,
    vignette, light flicker; series badge "TECH MYSTERIES · CASE NNN"
  - accents orange -> alarm red; captions in the typewriter mono font, red word box
Extra kit_mix element kinds (word-timed with 'at'):
  tv      w screen=sports|black|static|figure|drama|alert|bars  label   old CRT set; act {'do':'tv','id','at','screen'} switches channel
  file    title rows=[[label, text|None]] w stamp                         case file; None = black REDACTED bar wiping in
  typer   text size color dur                                             typewriter text with red cursor
  radar   label sub                                                       green radar ping on a city
  tower   name h w                                                        skyscraper silhouette with antenna (label under)
  beam    x2 y2 color                                                      microwave beam drawing from (x,y) to (x2,y2), dashes travel
  clue    n text w                                                         numbered clue card pinned to the board
  skyline w                                                                Chicago-like night skyline silhouette
  figure  w h                                                              masked silhouette in front of spinning metal stripes"""
import html as _h
import os, re

E = _h.escape
ON = lambda: os.environ.get('STYLE') == 'mystery'
RED = '#E5383B'
KINDS = {'tv', 'file', 'typer', 'radar', 'tower', 'beam', 'clue', 'skyline', 'figure'}
CASE = os.environ.get('CASE', '001')

CSS = """.mtv { position:absolute; border-radius:44px; background:linear-gradient(160deg,#3A2E24,#1C1611); box-shadow:0 50px 110px rgba(0,0,0,.8), inset 0 0 0 8px #2A2119; }
.mtv .scr { position:absolute; left:6.5%; top:8%; width:73%; height:80%; border-radius:60px/44px; overflow:hidden; background:#000; }
.mtv .scr > div { position:absolute; inset:0; opacity:0; } .mtv .scr > div.on { opacity:1; }
.mtv .kn { position:absolute; right:5%; top:16%; width:9%; } .mtv .kn i { display:block; width:100%; padding-top:100%; border-radius:50%; background:#0E0B09; margin-bottom:40%; box-shadow:inset 0 0 0 5px #3A2E24; }
.mtv .glass { position:absolute; inset:0; background:radial-gradient(ellipse at 30% 20%,rgba(255,255,255,.10),transparent 45%); box-shadow:inset 0 0 70px rgba(0,0,0,.9); z-index:3; opacity:1 !important; }
.mtv .lbl { position:absolute; left:0; right:0; top:calc(100% + 16px); text-align:center; font:700 22px 'SD Mono'; letter-spacing:5px; color:#8FA3C2; white-space:nowrap; }
.s-sports { background:linear-gradient(180deg,#1F4E8C,#0E2A52); } .s-sports b { position:absolute; left:7%; top:12%; font:900 46em 'SD Display'; color:#fff; white-space:nowrap; }
.s-sports i { position:absolute; left:7%; top:34%; font:700 22em 'SD Mono'; color:#FFD54A; font-style:normal; white-space:nowrap; } .s-sports u { position:absolute; left:0; right:0; bottom:0; height:16%; background:#C62828; }
.s-static { background:url(assets/noise.png) 0 0/256px 256px; filter:contrast(1.6) brightness(1.1); }
.s-figure .st { position:absolute; inset:0; background:repeating-linear-gradient(90deg,#1B1B1B 0 22px,#5A5A5A 22px 30px,#2A2A2A 30px 52px); }
.s-figure svg { position:absolute; inset:0; width:100%; height:100%; }
.s-drama { background:radial-gradient(circle at 50% 50%,#0D1B3A,#02040A 70%); } .s-drama b { position:absolute; left:0; right:0; top:42%; text-align:center; font:900 40em 'SD Display'; color:#9FC3FF; letter-spacing:6px; white-space:nowrap; }
.s-alert { background:#B71C1C; } .s-alert b { position:absolute; left:6%; right:6%; top:14%; font:900 40em 'SD Display'; color:#fff; letter-spacing:3px; }
.s-alert i { position:absolute; left:6%; right:6%; top:38%; font:700 24em 'SD Mono'; color:#FFE6E6; font-style:normal; line-height:1.45; }
.s-bars { background:linear-gradient(90deg,#C0C0C0 0 14%,#C0C000 14% 28%,#00C0C0 28% 42%,#00C000 42% 56%,#C000C0 56% 70%,#C00000 70% 84%,#0000C0 84%); }
.mfile { position:absolute; background:#C9B58E; border-radius:10px; box-shadow:0 40px 100px rgba(0,0,0,.8); padding:44px 54px; }
.mfile:before { content:''; position:absolute; left:34px; top:-36px; width:220px; height:42px; background:#C9B58E; border-radius:12px 12px 0 0; }
.mfile h3 { font:700 24px 'SD Mono'; letter-spacing:6px; color:#3B2F1E; margin-bottom:26px; white-space:nowrap; }
.mfile .ln { font:700 30px 'SD Mono'; color:#2A2116; margin:18px 0; display:flex; gap:18px; align-items:center; white-space:nowrap; }
.mfile .rd { display:inline-block; height:34px; background:#0B0B0B; transform-origin:left center; }
.mfile .stp { position:absolute; right:40px; bottom:40px; padding:6px 26px; border:10px solid #C62828; color:#C62828; font:900 72px 'SD Display'; letter-spacing:5px; transform:rotate(-10deg); background:rgba(201,181,142,.6); white-space:nowrap; }
.mtyp { position:absolute; font:700 120px 'SD Mono'; color:#E8EDF5; letter-spacing:3px; white-space:nowrap; text-shadow:0 0 30px rgba(140,180,255,.25); } .mtyp .cu { color:#E5383B; }
.mrad { position:absolute; width:420px; height:420px; } .mrad .p { position:absolute; left:110px; top:110px; width:200px; height:200px; border-radius:50%; border:3px solid #3DDC97; }
.mrad .d { position:absolute; left:194px; top:194px; width:32px; height:32px; border-radius:16px; background:#3DDC97; box-shadow:0 0 30px #3DDC97; }
.mrad .g { position:absolute; inset:0; border-radius:50%; background:linear-gradient(rgba(61,220,151,.08) 1px,transparent 1px) 0 0/42px 42px,linear-gradient(90deg,rgba(61,220,151,.08) 1px,transparent 1px) 0 0/42px 42px; }
.mrad b { position:absolute; left:-200px; right:-200px; top:440px; text-align:center; font:900 84px 'SD Display'; letter-spacing:16px; color:#E8EDF5; white-space:nowrap; }
.mrad i { position:absolute; left:-200px; right:-200px; top:545px; text-align:center; font:700 24px 'SD Mono'; letter-spacing:6px; color:#3DDC97; font-style:normal; white-space:nowrap; }
.mtow { position:absolute; } .mtow .t { position:absolute; bottom:0; background:linear-gradient(90deg,#141B29,#1D2638 50%,#121826); border:2px solid #26324A; }
.mtow .t:after { content:''; position:absolute; inset:10px; background:repeating-linear-gradient(0deg,rgba(255,214,120,.16) 0 4px,transparent 4px 18px),repeating-linear-gradient(90deg,transparent 0 12px,rgba(0,0,0,.55) 12px 20px); }
.mtow .a { position:absolute; bottom:100%; width:6px; background:#8FA3C2; } .mtow .l { position:absolute; left:50%; transform:translateX(-50%); top:calc(100% + 12px); font:700 22px 'SD Mono'; letter-spacing:4px; color:#8FA3C2; white-space:nowrap; }
.mtow .bl { position:absolute; width:14px; height:14px; border-radius:7px; background:#E5383B; box-shadow:0 0 18px #E5383B; }
.mbeam { position:absolute; height:8px; transform-origin:0 50%; background:repeating-linear-gradient(90deg,var(--bc) 0 26px,transparent 26px 40px); filter:drop-shadow(0 0 10px var(--bc)); border-radius:4px; }
.mclue { position:absolute; background:#141B29; border:2px solid #26324A; border-left:8px solid #E5383B; border-radius:12px; padding:22px 28px; box-shadow:0 24px 60px rgba(0,0,0,.6); }
.mclue b { display:block; font:700 22px 'SD Mono'; letter-spacing:6px; color:#E5383B; margin-bottom:10px; } .mclue span { font:700 34px 'SD Text'; color:#E8EDF5; line-height:1.3; }
.mclue:before { content:''; position:absolute; left:50%; top:-12px; width:22px; height:22px; border-radius:11px; background:#E5383B; box-shadow:0 4px 8px rgba(0,0,0,.6); }
.msky { position:absolute; }
.mfig { position:absolute; overflow:hidden; border-radius:18px; } .mfig .st { position:absolute; inset:0; background:repeating-linear-gradient(90deg,#1B1B1B 0 26px,#5A5A5A 26px 36px,#2A2A2A 36px 62px); }
.mfig svg { position:absolute; inset:0; width:100%; height:100%; }
"""

FIG_SVG = ('<svg viewBox="0 0 760 570" preserveAspectRatio="xMidYMid slice"><ellipse cx="380" cy="250" rx="120" ry="150" fill="#050505"/>'
           '<path d="M180 570 Q190 400 380 380 Q570 400 580 570 Z" fill="#050505"/><rect x="300" y="215" width="160" height="30" rx="10" fill="#111"/></svg>')
SCREENS = {
    'sports': '<b>SPORTS NEWS</b><i>TONIGHT · HIGHLIGHTS</i><u></u>',
    'black': '', 'static': '',
    'figure': '<div class="st"></div>' + FIG_SVG,
    'drama': '<b>SCI-FI SERIES</b>',
    'alert': '<b>⚠ EMERGENCY ALERT</b><i>The bodies of the dead are rising from their graves and attacking the living.</i>',
    'bars': '',
}


def skyline_svg(w):
    xs, out, x = [0], '', 0
    blds = [(70, 220), (50, 300), (90, 260), (60, 520), (80, 340), (40, 280), (110, 600), (70, 360), (55, 250), (95, 430), (60, 300), (85, 240), (50, 330), (75, 270)]
    for k, (bw, bh) in enumerate(blds):
        out += f'<rect x="{x}" y="{620 - bh}" width="{bw}" height="{bh}" fill="{"#0E1420" if k % 2 else "#121A28"}"/>'
        for r in range(620 - bh + 20, 600, 26):
            for c in range(x + 10, x + bw - 10, 18):
                if (r * 7 + c * 3 + k) % 5 == 0:
                    out += f'<rect x="{c}" y="{r}" width="6" height="9" fill="rgba(255,214,120,.45)"/>'
        x += bw + 6
    return f'<svg viewBox="0 0 {x} 620" width="{w}" height="{int(w * 620 / x)}" preserveAspectRatio="xMidYMax meet">{out}</svg>'


def el(eid, e, pos, rot):
    k = e['k']
    if k == 'tv':
        w = e.get('w', 640); h = int(w * .76); scr0 = e.get('screen', 'sports')
        scr = ''.join(f'<div class="s-{n}{" on" if n == scr0 else ""}" id="{eid}-{n}" style="font-size:{w / 640:.2f}px">{SCREENS[n]}</div>' for n in SCREENS)
        lab = f'<div class="lbl">{E(e["label"])}</div>' if e.get('label') else ''
        return f'<div class="mtv" id="{eid}" style="{pos}{rot}width:{w}px;height:{h}px"><div class="scr">{scr}<div class="glass"></div></div><div class="kn"><i></i><i></i></div>{lab}</div>'
    if k == 'file':
        rows = ''.join(f'<div class="ln">{E(lab)}: ' + (f'<span>{E(v)}</span>' if v is not None else f'<span class="rd" id="{eid}-r{j}" style="width:{260 + (j * 67) % 200}px"></span>') + '</div>'
                       for j, (lab, v) in enumerate(e['rows']))
        stp = f'<div class="stp" id="{eid}-s">{E(e["stamp"])}</div>' if e.get('stamp') else ''
        return f'<div class="mfile" id="{eid}" style="{pos}{rot}width:{e.get("w", 760)}px"><h3>{E(e.get("title", ""))}</h3>{rows}{stp}</div>'
    if k == 'typer':
        return f'<div class="mtyp" id="{eid}" style="{pos}{rot}font-size:{e.get("size", 120)}px;{"color:" + e["color"] + ";" if e.get("color") else ""}"><span id="{eid}-x"></span><span class="cu" id="{eid}-c">_</span></div>'
    if k == 'radar':
        return (f'<div class="mrad" id="{eid}" style="{pos}"><div class="g"></div><div class="p" id="{eid}-p0"></div><div class="p" id="{eid}-p1"></div><div class="p" id="{eid}-p2"></div>'
                f'<div class="d"></div><b>{E(e.get("label", ""))}</b><i>{E(e.get("sub", ""))}</i></div>')
    if k == 'tower':
        w, h = e.get('w', 120), e.get('h', 520)
        return (f'<div class="mtow" id="{eid}" style="{pos}width:{w}px;height:{h}px"><div class="t" style="left:0;width:{w}px;height:{h}px"></div>'
                f'<div class="a" style="left:{w * .3:.0f}px;height:{e.get("ant", 110)}px"></div><div class="a" style="left:{w * .7:.0f}px;height:{e.get("ant", 110) * .8:.0f}px"></div>'
                f'<div class="bl" id="{eid}-bl" style="left:{w * .3 - 4:.0f}px;top:{-e.get("ant", 110) - 8}px"></div><div class="l">{E(e.get("name", ""))}</div></div>')
    if k == 'beam':
        import math
        dx, dy = e['x2'] - e['x'], e['y2'] - e['y']; ln = math.hypot(dx, dy); ang = math.degrees(math.atan2(dy, dx))
        return f'<div class="mbeam" id="{eid}" style="{pos}width:{ln:.0f}px;transform:rotate({ang:.1f}deg);--bc:{e.get("color", "#3DDC97")}"></div>'
    if k == 'clue':
        return f'<div class="mclue" id="{eid}" style="{pos}{rot}width:{e.get("w", 560)}px"><b>CLUE {e["n"]:02d}</b><span>{E(e["text"])}</span></div>'
    if k == 'skyline':
        return f'<div class="msky" id="{eid}" style="{pos}">{skyline_svg(e.get("w", 1320))}</div>'
    if k == 'figure':
        return f'<div class="mfig" id="{eid}" style="{pos}{rot}width:{e.get("w", 640)}px;height:{e.get("h", 480)}px"><div class="st" id="{eid}-st"></div>{FIG_SVG}</div>'
    raise KeyError(k)


def dyn(eid, e, t, T, i):
    k, sc = e['k'], []
    if k == 'tv':
        sc.append(f'    tl.fromTo("#{eid}-static", {{ backgroundPosition:"0px 0px" }}, {{ backgroundPosition:"-2000px 900px", duration:30, ease:"steps(360)", immediateRender:false }}, 0);')
        sc.append(f'    tl.fromTo("#{eid}-figure .st", {{ backgroundPositionX:"0px" }}, {{ backgroundPositionX:"-1200px", duration:12, ease:"none", immediateRender:false }}, 0);')
    elif k == 'file':
        n = 0
        for j, (_, v) in enumerate(e['rows']):
            if v is None:
                rt = round(t + .5 + n * e.get('gap', .45), 3); n += 1
                sc.append(f'    tl.set("#{eid}-r{j}", {{ scaleX:0 }}, 0); tl.fromTo("#{eid}-r{j}", {{ scaleX:0 }}, {{ scaleX:1, duration:.3, ease:"power2.inOut", immediateRender:false }}, {rt});')
        if e.get('stamp'):
            st = T(i, e['stamp_at']) if e.get('stamp_at') is not None else t + .6 + n * .45
            sc.append(f'    tl.set("#{eid}-s", {{ opacity:0 }}, 0); tl.fromTo("#{eid}-s", {{ scale:2.6, opacity:0 }}, {{ scale:1, opacity:1, duration:.22, ease:"power4.in", immediateRender:false }}, {round(st, 3)});')
    elif k == 'typer':
        txt = e['text']; d = e.get('dur', .12 * len(txt))
        for j in range(1, len(txt) + 1):
            sc.append(f'    tl.set("#{eid}-x", {{ innerHTML:{E(txt[:j])!r} }}, {round(t + d * j / len(txt), 3)});')
        sc.append(f'    tl.set("#{eid}-x", {{ innerHTML:"" }}, 0);')
        sc.append(f'    tl.fromTo("#{eid}-c", {{ opacity:1 }}, {{ opacity:0, duration:.01, repeat:41, yoyo:true, repeatDelay:.3, immediateRender:false }}, {round(t + d, 3)});')
    elif k == 'radar':
        sc.append(f'    tl.fromTo("#{eid} .p", {{ scale:.2, opacity:.9 }}, {{ scale:2.4, opacity:0, duration:1.4, stagger:{{ each:.45, repeat:3 }}, ease:"power1.out", immediateRender:false }}, {t});')
    elif k == 'tower':
        sc.append(f'    tl.fromTo("#{eid}-bl", {{ opacity:1 }}, {{ opacity:.15, duration:.6, yoyo:true, repeat:15, ease:"sine.inOut", immediateRender:false }}, {t});')
    elif k == 'beam':
        sc.append(f'    tl.set("#{eid}", {{ scaleX:0 }}, 0); tl.fromTo("#{eid}", {{ scaleX:0 }}, {{ scaleX:1, duration:.6, ease:"power2.out", immediateRender:false }}, {t});')
        sc.append(f'    tl.fromTo("#{eid}", {{ backgroundPositionX:"0px" }}, {{ backgroundPositionX:"400px", duration:4, ease:"none", repeat:2, immediateRender:false }}, {t});')
    elif k == 'figure':
        sc.append(f'    tl.fromTo("#{eid}-st", {{ backgroundPositionX:"0px" }}, {{ backgroundPositionX:"-1200px", duration:10, ease:"none", immediateRender:false }}, 0);')
        for gt in (.3, 1.4, 2.6, 3.7):
            sc.append(f'    tl.fromTo("#{eid}", {{ x:-16, filter:"hue-rotate(90deg) saturate(3)" }}, {{ x:0, filter:"hue-rotate(0deg) saturate(1)", duration:.12, immediateRender:false }}, {round(t + gt, 3)});')
    return sc


def act(eid, a, t):
    if a['do'] == 'tv':
        n = a['screen']
        return [f'    tl.set("#{eid} .scr > div:not(.glass)", {{ opacity:0 }}, {t}); tl.set("#{eid}-{n}", {{ opacity:1 }}, {t});',
                f'    tl.fromTo("#{eid}", {{ x:0 }}, {{ x:10, duration:.04, yoyo:true, repeat:5, ease:"none", immediateRender:false }}, {t});']
    return None


# ------------------------------------------------------------------ whole-video look
GRAIN_CSS = """.mz-grain { position:absolute; inset:-60px; background:url(assets/noise.png) 0 0/256px 256px; opacity:.10; mix-blend-mode:screen; z-index:50; }
.mz-scan { position:absolute; inset:0; background:repeating-linear-gradient(0deg,rgba(0,0,0,.22) 0 2px,transparent 2px 4px); z-index:51; }
.mz-vig { position:absolute; inset:0; background:radial-gradient(ellipse at center,transparent 50%,rgba(0,0,0,.78) 100%); z-index:52; }
.mz-flick { position:absolute; inset:0; background:#fff; opacity:0; z-index:53; }
.mz-badge { position:absolute; right:80px; top:46px; display:flex; gap:12px; align-items:center; font:700 22px 'SD Mono'; letter-spacing:5px; color:#8FA3C2; z-index:54; }
.mz-badge i { width:14px; height:14px; border-radius:7px; background:#E5383B; box-shadow:0 0 16px #E5383B; display:inline-block; }
.cp { background:#0F1726 !important; border-color:#22304A !important; color:#C9D2E0 !important; font-family:'SD Mono' !important; letter-spacing:3px !important; }
.cp b { background:#E5383B !important; color:#fff !important; }"""
BG = """#root { background:radial-gradient(ellipse at 50% 40%,#121A2B 0%,#080C14 60%,#030406 100%) !important; }
.grid, .plus, .sq { display:none !important; }
.glow { background:radial-gradient(circle, rgba(120,150,210,.10) 0%, rgba(120,150,210,.04) 38%, transparent 66%) !important; }"""
MIXD = """.mcard { background:#111827 !important; border:2px solid #26324A; box-shadow:0 24px 60px rgba(0,0,0,.6) !important; }
.mcard .ml { color:#8FA3C2 !important; font-family:'SD Mono' !important; letter-spacing:4px !important; } .mcard .mb { color:#E8EDF5 !important; }
.mstamp { background:rgba(6,9,15,.55) !important; } .mtag { font-family:'SD Mono' !important; letter-spacing:2px; border:1px solid rgba(143,163,194,.25); }
.mbig { text-shadow:0 0 40px rgba(140,180,255,.18); }"""
CAPS = """.w em { font-family:'SD Mono' !important; font-weight:700 !important; font-size:44px !important; color:#5E6B80; letter-spacing:1px; }
.bx { background:#C62828 !important; }"""


def mysterize(html):
    if not ON():
        return html
    m = re.search(r'data-composition-id="([^"]+)"', html)
    cid = m.group(1) if m else ''
    html = html.replace('#F87736', RED).replace('rgba(248,119,54', 'rgba(229,56,59')
    if cid == 'bg':
        html = html.replace('</style>', BG + '\n</style>', 1)
    elif cid.startswith('caps'):
        html = html.replace('</style>', CAPS + '\n</style>', 1)
    elif re.match(r'b\d+$', cid):
        html = html.replace('</style>', MIXD + '\n</style>', 1)
    elif cid == 'chapters':
        html = html.replace('</style>', GRAIN_CSS + '\n</style>', 1)
        if 'data-height="1920"' in html:   # owner 2026-11-24: in the phone app the top-right corner is covered by YouTube's buttons
            html = html.replace('</style>', '.mz-badge { top:250px !important; right:60px !important; }\n</style>', 1)
        over = (f'<div class="mz-grain" id="mz-grain"></div><div class="mz-scan"></div><div class="mz-vig"></div><div class="mz-flick" id="mz-flick"></div>'
                f'<div class="mz-badge"><i></i>TECH MYSTERIES · CASE {CASE}</div>')
        html = re.sub(r'(<div id="root"[^>]*>)', lambda x: x.group(1) + '\n' + over, html, 1)
        html = html.replace('window.__timelines["chapters"] = tl;',
                            'tl.fromTo("#mz-grain", { backgroundPosition:"0px 0px" }, { backgroundPosition:"-9000px 6000px", duration:600, ease:"steps(7200)" }, 0);\n'
                            '    tl.fromTo("#mz-flick", { opacity:0 }, { opacity:.035, duration:.06, yoyo:true, repeat:4999, repeatDelay:.05, ease:"none" }, 0);\n'
                            '    window.__timelines["chapters"] = tl;')
    return html


def noise_png(path):
    """256x256 grey noise tile for grain and TV static (deterministic)"""
    from PIL import Image
    import random
    r = random.Random(7)
    im = Image.new('L', (256, 256))
    im.putdata([r.randint(0, 255) for _ in range(256 * 256)])
    im.save(path)
