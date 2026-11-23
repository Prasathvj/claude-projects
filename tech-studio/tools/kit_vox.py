"""VOX KIT in TechDecoded colours (owner, 2026-11-23): "evidence board" scenes for news videos and for numbers, studies and
sources inside papercut videos. Cream paper, dark-brown ink, ORANGE highlighter, orange-red hand-drawn circles and arrows,
peach halftone dots, tape, handwritten notes (Caveat font: copy hf/style-samples/assets/fonts/Caveat-700-latin.woff2 into
the project's assets/fonts). Register with kit_vox.register(B) after the long-video engine.

  {"type": "vdoc",   "label": "OPENAI BLOG · 2025", "lines": ["...", "..."], "hi": [line, "words to highlight"],
                     "circle": [line, "word"], "note": "handwritten note"}
  {"type": "vwords", "kicker": "HOW IT WRITES", "words": ["It", "picks", "one", "piece"], "head": "ONE PIECE AT A TIME", "hiword": "ONE PIECE"}
  {"type": "vstat",  "kicker": "CHATGPT · WEEKLY USERS", "num": "1", "unit": "BILLION", "sub": "people use it every week", "hi": "every week",
                     "source": "OpenAI, September 2026", "note": "1 in 8 people on Earth*", "foot": "*approx., population ≈ 8.2 billion"}
"""
INK, ORANGE, RED, PAPER = '#2A2018', 'rgba(248,119,54,.42)', '#E0471C', '#FFFAF2'

CSS = """@font-face { font-family:'Hand'; src:url('assets/fonts/Caveat-700-latin.woff2'); font-weight:700; }
.vx-ht { position:absolute; width:820px; height:820px; border-radius:50%; background-image:radial-gradient(#F3B08A 30%, transparent 33%); background-size:22px 22px;
  -webkit-mask-image:radial-gradient(circle,#000 0%,transparent 68%); mask-image:radial-gradient(circle,#000 0%,transparent 68%); opacity:.55; }
.vx-doc { position:absolute; background:""" + PAPER + """; box-shadow:0 2px 0 rgba(0,0,0,.06), 0 26px 50px rgba(90,55,25,.20); padding:50px 60px; }
.vx-tape { position:absolute; width:150px; height:44px; background:rgba(248,190,140,.55); }
.vx-kick { font:900 26px 'SD Display'; letter-spacing:6px; color:""" + INK + """; }
.vx-line { position:relative; font:700 38px 'SD Mono'; color:""" + INK + """; line-height:1.65; white-space:nowrap; }
.vx-hl { position:absolute; left:-6px; top:4px; bottom:2px; background:""" + ORANGE + """; mix-blend-mode:multiply; transform-origin:left; transform:scaleX(0); border-radius:6px 14px 8px 12px; }
.vx-mark { position:relative; display:inline-block; }
.vx-hand { position:absolute; font:700 60px 'Hand'; color:""" + RED + """; line-height:1.05; }
.vx-ink { stroke:""" + RED + """; stroke-width:9; fill:none; stroke-linecap:round; stroke-linejoin:round; }
.vx-box { position:absolute; padding:10px 24px; font:900 54px 'SD Display'; color:""" + INK + """; background:""" + PAPER + """; border:4px solid """ + INK + """; }
.vx-head { position:absolute; font:900 120px 'SD Display'; color:""" + INK + """; letter-spacing:-3px; white-space:nowrap; }
.vx-num { position:absolute; font:900 250px 'SD Display'; color:""" + INK + """; letter-spacing:-8px; line-height:1; white-space:nowrap; }
.vx-num b { color:""" + RED + """; }
.vx-src { position:absolute; width:520px; background:""" + PAPER + """; padding:22px 28px; box-shadow:0 20px 40px rgba(90,55,25,.2); transform:rotate(3deg); }
.vx-src i { display:block; font:700 20px 'SD Mono'; color:#9C8576; font-style:normal; } .vx-src span { font:700 30px 'SD Display'; color:""" + INK + """; }"""

def register(B):
    E, wf, pop = B.E, B.wfrac, B.pop

    def mark(text, key, sid, word):
        """wrap `word` inside `text` with a highlight span"""
        if word and word in text:
            a, b = text.split(word, 1)
            return f'{E(a)}<span class="vx-mark">{E(word)}<i class="vx-hl" id="{sid}-{key}" style="right:-6px"></i></span>{E(b)}'
        return E(text)

    def t_vdoc(i, sid, v):
        hl = v.get('hi') or [None, None]; ci = v.get('circle') or [None, None]
        rows = ''
        for k, ln in enumerate(v['lines']):
            txt = mark(ln, 'h', sid, hl[1]) if hl[0] == k else E(ln)
            if ci[0] == k and ci[1] in ln:
                a, b = txt.split(E(ci[1]), 1)
                txt = f'{a}<span class="vx-mark" id="{sid}-cw">{E(ci[1])}<svg style="position:absolute; left:-30px; top:-18px; width:calc(100% + 60px); height:100px; overflow:visible" viewBox="0 0 300 100" preserveAspectRatio="none"><path class="vx-ink" id="{sid}-c" d="M15 55 C 20 10, 250 0, 288 40 C 300 85, 140 100, 45 88 C 8 78, 15 30, 80 18"/></svg></span>{b}'
            rows += f'<div class="vx-line" id="{sid}-l{k}" style="opacity:0">{txt}</div>'
        note = f'<div class="vx-hand" id="{sid}-n" style="left:{v.get("nx", 1010)}px; top:{v.get("ny", 470)}px; transform:rotate(-6deg); opacity:0">{E(v["note"])}</div>' if v.get('note') else ''
        body = f"""<div class="vx-ht" style="left:-380px; top:300px"></div>
<div class="vx-doc" id="{sid}-d" style="left:40px; top:40px; width:{v.get("w", 960)}px; transform:rotate(-1deg)"><div class="vx-kick" style="color:#9C8576">{E(v.get("label", ""))}</div><div style="margin-top:26px">{rows}</div></div>
<div class="vx-tape" style="left:70px; top:20px; transform:rotate(-6deg)"></div><div class="vx-tape" style="left:{v.get("w", 960) - 110}px; top:20px; transform:rotate(5deg)"></div>{note}"""
        n = len(v['lines'])
        sc = [f'    tl.fromTo("#{sid}-d", {{ opacity:0, y:50, rotation:-3 }}, {{ opacity:1, y:0, rotation:-1, duration:.5, ease:"power3.out" }}, 0.05);']
        sc += [f'    tl.to("#{sid}-l{k}", {{ opacity:1, duration:.15 }}, {wf(i, 0.08 + k * 0.4 / max(1, n))});' for k in range(n)]
        if hl[0] is not None:
            sc.append(f'    tl.to("#{sid}-h", {{ scaleX:1, duration:.45, ease:"power2.out" }}, {wf(i, 0.55)});')
        if ci[0] is not None:
            sc += [f'    tl.set("#{sid}-c", {{ strokeDasharray:1000, strokeDashoffset:1000 }}, 0);',
                   f'    tl.to("#{sid}-c", {{ strokeDashoffset:0, duration:.7, ease:"power2.inOut" }}, {wf(i, 0.62)});']
        if note:
            sc.append(f'    tl.to("#{sid}-n", {{ opacity:1, duration:.25 }}, {wf(i, 0.75)});')
        return body, sc, CSS

    def t_vwords(i, sid, v):
        ws = v['words']; n = len(ws); gap = 230
        boxes = ''.join(f'<div class="vx-box" id="{sid}-k{k}" style="left:{40 + k * gap}px; top:200px; transform:rotate({(-1) ** k * 2}deg); opacity:0">{E(w)}</div>' for k, w in enumerate(ws))
        arrows = ''.join(f'<svg style="position:absolute; left:{150 + k * gap}px; top:110px" width="130" height="90"><path class="vx-ink" id="{sid}-a{k}" d="M10 70 C 40 10, 90 10, 120 60 M104 38 L120 60 L94 66"/></svg>' for k in range(n - 1))
        head = v['head']; hw = v.get('hiword', '')
        htxt = mark(head, 'h', sid, hw) if hw else E(head)
        body = f"""<div class="vx-ht" style="left:900px; top:-200px"></div><div class="vx-kick" style="position:absolute; left:40px; top:110px">{E(v.get("kicker", ""))}</div>
{boxes}{arrows}<div class="vx-head" id="{sid}-hd" style="left:30px; top:390px; opacity:0">{htxt}</div>"""
        sc = [f'    tl.fromTo("#{sid}-k{k}", {{ opacity:0, y:-40, scale:1.3 }}, {{ opacity:1, y:0, scale:1, duration:.3, ease:"back.out(2)" }}, {wf(i, 0.05 + k * 0.45 / n)});' for k in range(n)]
        sc += [f'    tl.set("#{sid}-a{k}", {{ strokeDasharray:300, strokeDashoffset:300 }}, 0); tl.to("#{sid}-a{k}", {{ strokeDashoffset:0, duration:.3 }}, {wf(i, 0.1 + k * 0.45 / n)});' for k in range(n - 1)]
        sc += [f'    tl.fromTo("#{sid}-hd", {{ opacity:0, y:30 }}, {{ opacity:1, y:0, duration:.4, ease:"power3.out" }}, {wf(i, 0.55)});']
        if hw:
            sc.append(f'    tl.to("#{sid}-h", {{ scaleX:1, duration:.5, ease:"power2.out" }}, {wf(i, 0.72)});')
        return body, sc, CSS

    def t_vstat(i, sid, v):
        sub = mark(v.get('sub', ''), 'h', sid, v.get('hi'))
        note = f'<div class="vx-hand" id="{sid}-n" style="left:{v.get("nx", 760)}px; top:{v.get("ny", 520)}px; transform:rotate(-7deg); opacity:0">{E(v["note"])}</div>' if v.get('note') else ''
        foot = f'<div style="position:absolute; left:{v.get("nx", 760) + 10}px; top:{v.get("ny", 520) + 150}px; font:600 20px \'SD Text\'; color:#9C8576">{E(v["foot"])}</div>' if v.get('foot') else ''
        src = f'<div class="vx-src" id="{sid}-s" style="left:{v.get("sx", 780)}px; top:{v.get("sy", 60)}px; opacity:0"><i>SOURCE</i><span>{E(v["source"])}</span></div><div class="vx-tape" style="left:{v.get("sx", 780) + 190}px; top:{v.get("sy", 60) - 20}px; transform:rotate(-4deg)"></div>' if v.get('source') else ''
        body = f"""<div class="vx-ht" style="left:700px; top:-120px"></div><div class="vx-kick" style="position:absolute; left:40px; top:120px">{E(v.get("kicker", ""))}</div>
<div class="vx-num" id="{sid}-v" style="left:20px; top:180px"><span id="{sid}-v1" style="display:inline-block">{E(v["num"])}</span> <b id="{sid}-v2" style="display:inline-block">{E(v.get("unit", ""))}</b></div>
<div style="position:absolute; left:40px; top:470px; font:700 46px 'SD Display'; color:{INK}">{sub}</div>{src}{note}{foot}"""
        sc = [f'    tl.fromTo("#{sid}-v1", {{ opacity:0, scale:2.4 }}, {{ opacity:1, scale:1, duration:.35, ease:"expo.out" }}, 0.08);',
              f'    tl.fromTo("#{sid}-v2", {{ opacity:0, x:120 }}, {{ opacity:1, x:0, duration:.4, ease:"back.out(2)" }}, 0.25);']
        if v.get('hi'):
            sc.append(f'    tl.to("#{sid}-h", {{ scaleX:1, duration:.4 }}, {wf(i, 0.35)});')
        if src:
            sc.append(f'    tl.fromTo("#{sid}-s", {{ opacity:0, y:-60 }}, {{ opacity:1, y:0, duration:.45, ease:"back.out(1.6)" }}, {wf(i, 0.45)});')
        if note:
            sc.append(f'    tl.to("#{sid}-n", {{ opacity:1, duration:.3 }}, {wf(i, 0.6)});')
        return body, sc, CSS

    B.T.update({'vdoc': t_vdoc, 'vwords': t_vwords, 'vstat': t_vstat})
    B.SFX_BY_TYPE.update({'vdoc': [(0.05, 'flip', .5), (1.2, 'type', .35)], 'vwords': [('each', 'pop', .4)], 'vstat': [(0.08, 'impact', .55), (1.0, 'stamp', .4)]})
