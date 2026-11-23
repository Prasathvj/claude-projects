"""ep08 "How to Use GPT-6 Astra" (8:42): MIXED style + PRO UI kit (owner 2026-11-23: "same kind of motion graphics as the
Astra Short"): light app windows, agent cursor, menus/toggles/dialogs, phone chat, plan cards, on cream + dots; real logos and
exact icons; old pop cards/counters; Vox clippings for claims. One exact visual per line, word-timed. Stage 1320x760.
Run: python3 episodes/ep08/visuals_mix.py && THEME=cream GRID=dots python3 tools/hf_ep08_long.py"""
import json, re
from pathlib import Path
HERE = Path(__file__).parent
f = HERE / 'long.json'; e = json.loads(f.read_text())

def M(*els, acts=()):
    return {'type': 'mix', 'els': [x for x in els if x], 'acts': list(acts)}
def X(k, at, x, y, **o):
    d = dict(k=k, at=at, x=x, y=y); d.update(o); return d
def ic(at, x, y, ref, size=120, color='#2A2018', **o):          # plain icon (no paper disc)
    return X('icon', at, x, y, ref=ref, size=size, color=color, **o)
def tl_(at, x, y, ref, size=90, label=None, color=None, box=None, **o):   # clean app tile
    d = dict(ref=ref, size=size, **o)
    if label: d['label'] = label
    if color: d['color'] = color
    if box: d['box'] = box
    return X('tile', at, x, y, **d)
def tg(at, x, y, text, bg='#2A2018', size=32, **o):
    return X('tag', at, x, y, text=text, bg=bg, size=size, **o)
def bg_(at, x, y, text, size=96, **o):
    return X('big', at, x, y, text=text, size=size, **o)
def cd(at, x, y, big, label='', icon=None, color='#F87736', w=None, **o):
    d = dict(big=big, label=label, color=color, **o)
    if icon: d['icon'] = icon
    if w: d['w'] = w
    return X('card', at, x, y, **d)
def ch(at, x, y, text, icon=None, color='#F87736', size=28, **o):
    d = dict(text=text, color=color, size=size, **o)
    if icon: d['icon'] = icon
    return X('chip', at, x, y, **d)
def st(at, x, y, text, size=90, color='#E0471C', rot=-10, **o):
    return X('stamp', at, x, y, text=text, size=size, color=color, rot=rot, **o)
def win(at, x, y, w, h, title, body='', **o):
    return X('win', at, x, y, w=w, h=h, title=title, body=body, **o)
def cur(at, pts, **o):
    return X('cursor', at, 0, 0, pts=pts, **o)
def step(n, at=0.02):
    return tg(at, 0, 0, f'STEP {n}', bg='#F87736', size=34, id='step', color='#1A0A04')
def ILL(at=0.02):
    return tg(at, 1120, 0, 'ILLUSTRATION', bg='#EFE3D7', color='#A48A78', size=18, id='ill', **{'in': 'fade'})
SL = {'in': 'slam'}; SD = {'in': 'slide'}; DR = {'in': 'drop'}; FL = {'in': 'fly'}; LF = {'in': 'left'}; FD = {'in': 'fade'}; GR = {'in': 'grow'}
G, R, O, D, P, BL, Y, MU = '#2F9E44', '#E0471C', '#F87736', '#2A2018', '#7A5CFF', '#1C7ED6', '#F5B400', '#8C6B5A'

def sheet(rows, cw=170, top=56):
    out = ''
    for r, row in enumerate(rows):
        for c, v in enumerate(row):
            col = 'color:#F87736;font-weight:800;' if r == 0 else ''
            out += (f'<div style="position:absolute;left:{16 + c * cw}px;top:{top + r * 44}px;width:{cw}px;height:44px;border-right:1px solid #EFE3D7;'
                    f'border-bottom:1px solid #EFE3D7;font:600 22px \'SD Mono\';color:#2A2018;display:flex;align-items:center;padding-left:10px;{col}">{v}</div>')
    return out
def lines_html(items, top=70, size=24, color='#2A2018', gap=40, left=24, ids=None):
    return ''.join(f'<div{" id=" + chr(34) + ids + str(k) + chr(34) if ids else ""} style="position:absolute;left:{left}px;top:{top + k * gap}px;font:600 {size}px \'SD Text\';color:{color};white-space:nowrap">{t}</div>'
                   for k, t in enumerate(items))
SALES = [('Month', 'Sales'), ('Jan', '42'), ('Feb', '55'), ('Mar', '61'), ('Apr', '74'), ('May', '88')]
def chart_bars(at, x0, y0, hs, pre='cb'):
    return [X('html', at if k == 0 else at, x0 + k * 62, y0 - h, id=f'{pre}{k}', html=f'<div style="width:46px;height:{h}px;border-radius:8px 8px 0 0;background:linear-gradient(180deg,#FFB27A,#F87736);transform-origin:bottom"></div>', **GR)
            for k, h in enumerate(hs)]

V = [
 # 0 hook: Astra makes a chart + PDF by itself
 (M(ILL(), win(0.02, 40, 20, 780, 560, 'sales.xlsx', sheet(SALES), id='w', **FL),
    ch(0.3, 420, 90, 'Insert ▸ Chart', size=24, id='ins'), ch(0.35, 420, 150, 'Save as PDF', size=24, id='pdfb'),
    *chart_bars('through', 470, 540, [110, 150, 170, 210, 250]),
    tl_('openais', 900, 40, 'logos:openai-icon', 110, label='OpenAI', id='oa', **DR),
    ch('apps', 880, 250, 'Uses your computer', icon='ph:cursor-click-fill', color=BL, id='uc', **SD),
    X('toast', 'finish', 860, 360, text='sales_report.pdf saved', id='t', **SD),
    tg('watch', 860, 470, 'nobody touches the mouse', bg=O, size=30, id='nm', **SL),
    cur(0.1, [[1000, 650, 0.1, False], [520, 110, 'click', True], [560, 260, 'through', True], [520, 170, 'finish', True], [880, 420, 'watch', False]], id='c')), None),
 # 1 GPT-6 Astra, India top search market
 (M(tl_('called', 40, 30, 'logos:openai-icon', 100, id='oa'), bg_('astra', 210, 40, 'GPT-6 *ASTRA*', 130, **SL),
    ch('searched', 40, 250, 'One of the most searched AI tools', icon='ph:trend-up-bold', color=G, id='ms'),
    ch('most', 40, 340, 'India: #1 search market', icon='circle-flags:in', size=34, id='in'),
    X('bars', 'searched', 40, 430, w=720, id='bars', rows=[['India · 20% of searches', .9, O], ['USA · 12%', .54, '#B09682'], ['Pakistan · 9%', .4, '#B09682']], gap=.25),
    tg('india', 800, 700, 'SHARE OF SEARCHES · vidIQ data', bg='#EFE3D7', color=MU, size=20)), None),
 # 2 can't find it ★
 (M(ILL(), win(0.02, 40, 20, 640, 500, 'ChatGPT', '', id='w', **FL),
    X('menu', 0.1, 80, 90, w=560, search='Search models', typeq='Astra', qat='look', items=[['GPT-5.6 Sol', 'everyday'], ['GPT-5.6 Luna', 'fast'], ['No results for "Astra"', '', R]], id='m'),
    bg_('wall', 720, 120, "CAN'T", 110, **SL), bg_('look', 720, 250, '*FIND IT?*', 110, **SL)),
  None),
 # 3 what we'll decode
 (M(bg_('decode', 40, 0, "Let's *decode* it", 84),
    tl_('hides', 60, 190, 'ph:magnifying-glass-bold', 90, label='where it hides', color=D, id='a'),
    tl_('switch', 360, 190, 'ph:toggle-right-fill', 90, label='switch it on', color=G, id='b'),
    tl_('costs', 660, 190, 'ph:currency-inr-bold', 90, label='India price', color=O, id='c'),
    tl_('trap', 960, 190, 'ph:warning-fill', 90, label='the free trap', color=R, id='d'),
    tg('stay', 930, 430, 'STAY FOR THIS ONE', bg=R, size=30, id='s', **SL), ic('stay', 1040, 370, 'ph:arrow-up-bold', 50, R, id='ar'),
    acts=[{'do': 'ring', 'id': 'd', 'at': 'catching'}, {'do': 'shake', 'id': 'd', 'at': 'people'}]), None),
 # 4 what it is
 (M(tl_(0.02, 40, 30, 'logos:openai-icon', 100, id='oa'), bg_('top', 210, 40, "OpenAI's *top* model", 84),
    cd('september', 40, 230, 'SEP 2026', 'LAUNCHED', 'ph:calendar-check-fill', BL, id='l', **FL),
    ch('computer', 520, 250, 'Computer work', icon='ph:cursor-click-fill', color=BL, id='c1'),
    ch('coding', 520, 340, 'Coding', icon='ph:code-bold', color=O, id='c2'),
    ch('long', 520, 430, 'Long, demanding tasks', icon='ph:hourglass-high-fill', color=P, id='c3')), 'What Astra is'),
 # 5 GPT-6.2 upgrade + Sol
 (M(ch(0.02, 40, 40, 'SEP 2026 · GPT-6 Astra', icon='ph:calendar-fill', color=MU, id='a'),
    X('arrow', 'november', 420, 60, w=160, id='ar'), ch('november', 600, 40, 'NOV 17 · GPT-6.2 Astra', icon='ph:rocket-launch-fill', color=O, border=O, id='b', **SD),
    st('upgraded', 1000, 130, 'UPGRADE', 54, G, -8, id='u'),
    X('pcard', 'astra', 120, 260, name='GPT-6.2 Astra', price='the hardest tasks', w=420, hi=True, id='p1', **FL),
    X('pcard', 'sol', 640, 260, name='GPT-6.2 Sol', price='cheaper, everyday work', w=420, id='p2', **FL),
    tg('sister', 640, 440, 'its cheaper "sister model"', bg=G, size=30, id='t')), None),
 # 6 Sol vs Astra analogy
 (M(cd('sol', 40, 60, 'SOL', 'FAST, EVERYDAY ASSISTANT', 'ph:lightning-fill', Y, w=520, id='s', **LF),
    cd('astra', 700, 60, 'ASTRA', 'THE SPECIALIST', 'ph:brain-fill', O, w=520, id='a', **SD),
    bg_('think', 590, 110, 'vs', 70, color=MU),
    ch('fast', 60, 300, 'quick questions', icon='ph:chat-circle-fill', color=Y, id='q'),
    ch('hardest', 720, 300, 'the hardest jobs', icon='ph:briefcase-fill', color=O, id='h'),
    ic('assistant', 140, 420, 'ph:user-circle-fill', 140, MU, id='u1'), ic('specialist', 800, 420, 'ph:user-gear-fill', 140, O, id='u2')), None),
 # 7 FUN ★ Max's big plan (hypothetical)
 (M(tg(0.02, 0, 0, 'HYPOTHETICAL SKIT', bg='#EFE3D7', color=MU, size=20, id='hy'),
    win('plan', 40, 50, 620, 420, "Max's plan.txt", lines_html(['1.  Ask Astra to do my entire job', '2.  Take the afternoon off', '3.  Profit'], top=80, size=30, gap=70, ids='pl'), id='w', **DR),
    ic('job', 700, 70, 'ph:briefcase-fill', 140, O, id='j'), ic('afternoon', 880, 60, 'ph:sun-horizon-fill', 160, Y, id='sun'),
    ic('off', 1080, 90, 'ph:beach-ball-fill', 120, R, id='bb'), bg_('big', 700, 330, 'The *big* plan', 80),
    acts=[{'do': 'bob', 'id': 'bb', 'at': 'off', 'n': 5}]), "Max can't find it"),
 # 8 ★ no Astra, refresh, Wi-Fi
 (M(win(0.02, 40, 40, 560, 420, 'ChatGPT', '', id='w'),
    X('menu', 0.05, 70, 110, w=500, items=[['GPT-5.6 Sol', 'everyday'], ['GPT-5.6 Luna', 'fast']], id='m'),
    st('no', 120, 330, 'NO ASTRA', 70, R, -8, id='n1', **SL),
    ic('refreshed', 680, 60, 'ph:arrows-clockwise-bold', 150, BL, id='rf'), st('still', 620, 260, 'STILL NO', 70, R, 6, id='n2', **SL),
    tl_('blamed', 980, 60, 'ph:wifi-slash-bold', 100, label='blame the Wi-Fi', color=R, id='wf', **DR),
    acts=[{'do': 'spin', 'id': 'rf', 'at': 'refreshed', 'deg': 720, 'd': 1.2}, {'do': 'shake', 'id': 'wf', 'at': 'wifi'}]), None),
 # 9 ★ Wi-Fi fine; Astra lives elsewhere
 (M(tl_(0.02, 40, 40, 'ph:wifi-high-bold', 100, label='Wi-Fi', color=G, id='wf'), X('toast', 'fine', 260, 70, text='Connected · all fine', id='t', **SD),
    bg_('live', 40, 290, "Astra doesn't live", 90), bg_('look', 40, 400, 'where most people *look*', 90),
    ic('look', 1000, 300, 'ph:binoculars-fill', 160, MU, id='b')), None),
 # 10 Plus: Work + Codex
 (M(X('pcard', 'plus', 40, 40, name='Plus', price='Astra included', ok=True, hi=True, w=340, id='p', **FL),
    X('arrow', 'inside', 420, 90, w=150, id='a1'),
    tl_('work', 620, 30, 'ph:briefcase-fill', 90, label='ChatGPT Work', color=O, id='w'),
    tl_('codex', 900, 30, 'ph:terminal-window-fill', 90, label='Codex', color=D, id='c'),
    ch('chat', 300, 380, 'the regular chat list', icon='ph:list-bullets-bold', color=MU, size=34, id='cl'),
    st('not', 780, 360, 'NOT HERE', 80, R, -6, id='nh', **SL)), 'Who gets it'),
 # 11 Free / Go no; Pro / business yes
 (M(X('pcard', 'free', 40, 60, name='Free', price='₹0', ok=False, w=280, id='f', **FL),
    X('pcard', 'go', 350, 60, name='Go', price='₹399 / month', ok=False, w=280, id='g', **FL),
    X('pcard', 'pro', 660, 60, name='Pro', price='much more', ok=True, w=280, id='p', **FL),
    X('pcard', 'business', 970, 60, name='Business', price='per seat', ok=True, w=300, id='b', **FL),
    tg('included', 120, 260, 'Astra not included', bg=R, size=30, id='ni'),
    ch('higher', 740, 270, 'much higher limits', icon='ph:gauge-fill', color=G, id='hl'),
    tg('free', 40, 680, 'Prices: check chatgpt.com/pricing', bg='#EFE3D7', color=MU, size=20)), None),
 # 12 Plus limit 5–45 per 5 h
 (M(X('pcard', 0.02, 40, 40, name='Plus', price='~₹1,999 / month', ok=True, w=340, id='p'),
    cd('five', 440, 40, '5', 'ASTRA MESSAGES · EVERY 5 HOURS', 'ph:hourglass-high-fill', O, w=640, id='lim', **FL),
    tg('estimates', 460, 250, "OpenAI's estimate, not a guarantee", bg=D, size=30, id='e'),
    ch('depending', 460, 340, 'light task → more messages', icon='ph:feather-fill', color=G, id='l1'),
    ch('task', 460, 420, 'heavy task → fewer', icon='ph:barbell-fill', color=R, id='l2'),
    acts=[{'do': 'count', 'id': 'lim', 'at': 'fortyfive', 'values': ['5', '5–15', '5–30', '5–45'], 'dt': .15}]), None),
 # 13 precious resource; not a birthday message
 (M(tl_('precious', 40, 40, 'ph:diamond-fill', 100, label='precious', color=BL, id='d'),
    ch('big', 40, 290, 'Big jobs only', icon='ph:check-circle-fill', color=G, size=36, id='bj'),
    X('phone', 'not', 760, 10, w=330, h=600, msgs=[['user', 'write me a birthday message', 'write']], id='ph', **SD),
    st('message', 40, 420, 'NOT FOR ASTRA', 56, R, -8, id='nf', **SL)), None),
 # 14 check your plan in settings
 (M(ILL(), win(0.02, 40, 20, 700, 480, 'ChatGPT · Settings', '', id='w', **FL),
    X('menu', 0.1, 70, 90, w=640, items=[['Account', ''], ['Plan', 'Free · Go · Plus · Pro'], ['Data controls', ''], ['Apps & Plugins', '']], id='m'),
    cur(0.1, [[700, 600, 0.1, False], [300, 205, 'plan', True]], id='c'),
    bg_('decides', 790, 160, 'This', 90), bg_('decides', 790, 260, 'decides', 90), bg_('everything', 790, 360, '*everything*', 90),
    acts=[{'do': 'pick', 'id': 'm', 'at': 'plan', 'n': 1}]), None),
 # 15 ★ step 1 desktop app
 (M(step(1), ILL(), win(0.05, 40, 70, 700, 460, 'chatgpt.com/download', lines_html(['Download ChatGPT', 'for your computer'], top=60, size=40, gap=56), id='w', **FL),
    tl_('windows', 80, 300, 'logos:microsoft-windows-icon', 80, label='Windows', id='win'),
    tl_('mac', 300, 300, 'logos:apple', 70, label='Mac', id='mac', box=140),
    X('toast', 'update', 790, 200, text='Updated to the latest version', id='t', **SD),
    tl_('install', 820, 340, 'ph:download-simple-bold', 90, label='install', color=O, id='dl'),
    cur(0.2, [[700, 650, 0.2, False], [150, 370, 'windows', True], [880, 390, 'install', True]], id='c')), 'Step by step'),
 # 16 step 2: Chat -> Work, pick Astra
 (M(step(2), ILL(), win(0.02, 40, 70, 820, 560, 'ChatGPT · desktop app', '', id='w', **FL),
    X('seg', 0.1, 300, 140, opts=['Chat', 'Work'], sel=0, id='sg'),
    X('menu', 'pick', 200, 260, w=520, items=[['GPT-6.2 Sol', 'everyday work'], ['GPT-6.2 Astra', 'hardest tasks']], id='m'),
    tg('work', 900, 160, 'Chat → Work', bg=O, size=44, id='cw', **SL), tg('menu', 900, 300, 'model menu → Astra', bg=D, size=36, id='mm'),
    cur(0.1, [[700, 700, 0.1, False], [520, 175, 'work', True], [460, 350, 'astra', True]], id='c'),
    acts=[{'do': 'sel', 'id': 'sg', 'at': 'work', 'n': 1}, {'do': 'pick', 'id': 'm', 'at': 'astra', 'n': 1}]), None),
 # 17 step 3: Plugins > Computer Use
 (M(step(3), ILL(), win(0.02, 40, 70, 760, 560, 'ChatGPT · Plugins', '', id='w', **FL),
    X('menu', 'plugins', 70, 140, w=700, search='Search plugins', typeq='Computer Use', qat='find', items=[], id='m'),
    X('toggle', 'install', 70, 260, w=700, label='Computer Use', icon='ph:cursor-click-fill', id='tg'),
    tg('exciting', 880, 140, 'the exciting part', bg=O, size=36, id='ex', **SL),
    cur(0.2, [[700, 700, 0.2, False], [300, 180, 'find', True], [690, 300, 'turn', True]], id='c'),
    acts=[{'do': 'on', 'id': 'tg', 'at': 'on'}]), None),
 # 18 Mac permissions / Windows keep visible
 (M(ILL(), tl_('mac', 40, 30, 'logos:apple', 70, label='Mac', id='mac', box=130),
    X('toggle', 'screen', 200, 30, w=460, label='Screen Recording', icon='ph:record-fill', color=R, id='t1'),
    X('toggle', 'accessibility', 200, 130, w=460, label='Accessibility', icon='ph:person-arms-spread-fill', id='t2'),
    tl_('windows', 720, 30, 'logos:microsoft-windows-icon', 70, label='Windows', id='win', box=130),
    win('keep', 720, 230, 520, 320, 'Excel · sales.xlsx', sheet(SALES[:5], 150), id='xw', **FL),
    tg('visible', 760, 580, 'keep the app visible on screen', bg=G, size=30, id='kv'),
    acts=[{'do': 'on', 'id': 't1', 'at': 'recording'}, {'do': 'on', 'id': 't2', 'at': 'accessibility'}]), None),
 # 19 step 4: @Computer / @Chrome
 (M(step(4), ILL(), X('type', 'computer', 40, 90, w=760, h=110, prefix='@Computer', text='Open my sales sheet…', dur=.8, id='t1'),
    tl_('desktop', 880, 80, 'ph:desktop-fill', 80, label='desktop apps', color=D, id='d'),
    X('type', 'chrome', 40, 330, w=760, h=110, prefix='@Chrome', text='Compare laptop prices on three sites…', dur=1.0, id='t2'),
    tl_('browser', 880, 320, 'logos:chrome', 80, label='your browser', id='c')), None),
 # 20 the example prompt
 (M(ILL(), X('type', 'example', 40, 30, w=1240, h=150, prefix='@Computer', text='Open my sales sheet, chart the monthly totals, and save it as a PDF on my desktop.', dur=2.6, id='p'),
    ch('done', 40, 230, 'Say exactly what "done" looks like', icon='ph:flag-checkered-fill', color=G, size=32, id='dn'),
    tl_('sales', 80, 360, 'ph:file-xls-fill', 90, label='open the sheet', color=G, id='a'), X('arrow', 'chart', 260, 410, w=120, id='a1'),
    tl_('chart', 420, 360, 'ph:chart-bar-fill', 90, label='make the chart', color=O, id='b'), X('arrow', 'pdf', 600, 410, w=120, id='a2'),
    tl_('pdf', 760, 360, 'ph:file-pdf-fill', 90, label='save as PDF', color=R, id='c'),
    tl_('desktop', 1040, 360, 'ph:desktop-fill', 90, label='on the desktop', color=D, id='d')), None),
 # 21 permission dialog, watch every click, stop
 (M(ILL(), X('dialog', 'permission', 40, 40, w=700, title='Allow ChatGPT to use Excel?', sub='Astra wants to control this app for your task.', id='dl', **FL),
    ch('watch', 820, 60, 'You watch every click', icon='ph:eye-fill', color=BL, size=32, id='wc'),
    ch('stop', 820, 170, 'Stop', icon='ph:stop-circle-fill', color=R, size=40, border=R, id='sp'),
    cur(0.2, [[700, 650, 0.2, False], [130, 255, 0.45, True], [400, 500, 'click', False], [900, 200, 'stop', True]], id='c'),
    acts=[{'do': 'press', 'id': 'dl', 'at': 0.45, 'n': 0}, {'do': 'ring', 'id': 'sp', 'at': 'time'}]), None),
 # 22 can't see unless allowed; you stay in control
 (M(tl_('screen', 60, 40, 'ph:eye-slash-fill', 90, label="can't see your screen", color=MU, id='s'),
    tl_('app', 440, 40, 'ph:lock-key-fill', 90, label="can't use an app", color=MU, id='a'),
    X('toggle', 'allow', 800, 60, w=440, label='Allow Excel', icon='ph:microsoft-excel-logo-fill', color=G, id='t'),
    bg_('control', 60, 380, 'You stay in *control*', 110, **SL), ic('control', 1100, 360, 'ph:hand-palm-fill', 140, O, id='h'),
    acts=[{'do': 'on', 'id': 't', 'at': 'allow'}]), None),
 # 23 one catch: web/phone tasks run in the cloud
 (M(tg('catch', 0, 0, 'ONE CATCH', bg=R, size=36, id='oc', **SL),
    tl_('website', 40, 120, 'ph:globe-fill', 80, label='website', color=BL, id='w'),
    tl_('phone', 40, 340, 'ph:device-mobile-fill', 80, label='phone app', color=D, id='p'),
    X('arrow', 'runs', 230, 260, w=160, id='a1'), tl_('cloud', 440, 200, 'ph:cloud-fill', 110, label='runs in the cloud', color=BL, id='cl', box=190),
    tl_('cant', 900, 200, 'ph:laptop-fill', 110, label='your own files', color=D, id='pc', box=190),
    st('reach', 820, 470, "CAN'T REACH", 64, R, -6, id='cr', **SL)), None),
 # 24 ★ Max tries again
 (M(ILL(), win(0.02, 40, 30, 760, 520, 'ChatGPT · Work', '', id='w', **FL), X('seg', 0.05, 230, 100, opts=['Chat', 'Work'], sel=1, id='sg'),
    ch('properly', 90, 220, 'Model: GPT-6.2 Astra', icon='ph:sparkle-fill', color=O, id='m'),
    X('toast', 'time', 90, 330, text='Astra is working on it…', icon='ph:gear-six-fill', id='t', **SD),
    bg_('jobs', 840, 150, 'Real jobs', 84), bg_('these', 840, 250, '*people try*', 84)), 'What people use it for'),
 # 25 receipts -> expense sheet
 (M(tl_('folder', 40, 60, 'ph:folder-open-fill', 100, label='receipts folder', color=Y, id='f'),
    *[ic('receipts', 60 + k * 70, 300 + (k % 2) * 40, 'ph:receipt-fill', 90, MU, id=f'r{k}', **DR) for k in range(4)],
    X('arrow', 'turned', 380, 260, w=180, id='a'),
    win('tidy', 620, 40, 640, 420, 'expenses.xlsx', sheet([('Date', 'Shop', '₹'), ('2 Nov', 'Cafe', '240'), ('5 Nov', 'Taxi', '310'), ('9 Nov', 'Books', '860'), ('Total', '', '1,410')], 200), id='x', **SD),
    tg('expense', 680, 500, 'one tidy expense sheet', bg=G, size=32, id='t')), None),
 # 26 website from a sketch, checked in the browser
 (M(win('simple', 40, 40, 480, 400, 'sketch.png', '<div style="position:absolute;left:30px;top:70px;width:420px;height:300px;border:4px dashed #A48A78;border-radius:14px"></div>' + lines_html(['[ logo ]   menu', 'BIG HEADLINE', '[ button ]'], top=110, size=28, color='#8C6B5A', gap=80, left=60), id='s', **LF),
    X('arrow', 'built', 560, 220, w=140, id='a'),
    win('browser', 740, 30, 540, 460, 'localhost:3000', '<div style="position:absolute;left:0;top:46px;right:0;height:60px;background:#F87736"></div>' + lines_html(['Fresh Bakes Daily', 'Order online →'], top=170, size=34, gap=90, left=40), id='b', **SD),
    X('toast', 'works', 780, 540, text='Checked: it really works', id='t', **SD),
    cur('browser', [[1100, 650, 'browser', False], [930, 360, 'check', True]], id='c')), None),
 # 27 Blender + BlenderWorld test
 (M(tl_('blender', 40, 40, 'logos:blender', 100, label='Blender', id='bl', box=170),
    ic('3d', 300, 60, 'ph:cube-fill', 150, O, id='cube'),
    X('clip', 'researchers', 520, 30, by='RESEARCH PAPER · arXiv 2026', text='BlenderWorld: a benchmark for AI agents creating 3D scenes', hi='BlenderWorld', w=740, id='cl', **FL),
    ch('measure', 520, 330, 'measures how well AI agents work', icon='ph:ruler-fill', color=P, id='m'),
    ch('scenes', 520, 420, 'create 3D scenes', icon='ph:mountains-fill', color=G, id='sc'),
    acts=[{'do': 'spin', 'id': 'cube', 'at': '3d', 'deg': 360, 'd': 3}]), None),
 # 28 Codex: whole project, tests, fixes
 (M(ILL(), tl_('coders', 40, 30, 'ph:terminal-window-fill', 90, label='Codex', color=D, id='cx'),
    ch('astra', 40, 260, 'Model: GPT-6.2 Astra', icon='ph:sparkle-fill', color=O, id='m'),
    win('project', 420, 20, 860, 520, 'codex · my-shop-app',
        '<div style="position:absolute;inset:46px 0 0 0;background:#2A2018"></div>', id='w', **FL),
    X('html', 'project', 450, 90, id='l1', html='<div style="font:600 26px \'SD Mono\';color:#E9DED6">› reading 48 files…</div>', **FD),
    X('html', 'tests', 450, 150, id='l2', html='<div style="font:600 26px \'SD Mono\';color:#FF8A6B">✗ 3 tests failed</div>', **FD),
    X('html', 'fix', 450, 210, id='l3', html='<div style="font:600 26px \'SD Mono\';color:#E9DED6">› fixing checkout.js …</div>', **FD),
    X('html', 'breaks', 450, 270, id='l4', html='<div style="font:600 26px \'SD Mono\';color:#7EE29A">✓ 51 tests passed</div>', **FD)), None),
 # 29 real files
 (M(tl_('documents', 60, 60, 'ph:file-doc-fill', 110, label='documents', color=BL, id='d', box=190),
    tl_('spreadsheets', 380, 60, 'ph:file-xls-fill', 110, label='spreadsheets', color=G, id='s', box=190),
    tl_('presentations', 700, 60, 'ph:file-ppt-fill', 110, label='presentations', color=O, id='p', box=190),
    ch('text', 300, 420, 'not just text in a chat window', icon='ph:chat-text-fill', color=MU, size=34, id='t'),
    bg_('real', 1000, 80, 'real', 80), bg_('files', 1000, 170, '*files*', 80)), None),
 # 30 1M tokens = a few thick books
 (M(tl_('api', 40, 40, 'ph:code-bold', 90, label='API', color=D, id='api'),
    cd('million', 300, 40, '1,000', 'READS AT ONCE (TOKENS)', 'ph:stack-fill', O, w=640, id='tk', **FL),
    *[ic('books', 340 + k * 170, 330, 'ph:books-fill', 140, [O, BL, G][k], id=f'b{k}', **DR) for k in range(3)],
    tg('thick', 360, 540, '≈ a few thick books in one go', bg=D, size=34, id='t'),
    acts=[{'do': 'count', 'id': 'tk', 'at': 'million', 'values': ['10,000', '100,000', '500,000', '~1,000,000'], 'dt': .14}]), None),
 # 31 OSWorld 2.0: 73%
 (M(cd('test', 40, 40, 'OSWorld 2.0', 'COMPUTER-USE TEST', 'ph:desktop-tower-fill', BL, id='o', **FL),
    X('bars', 'finished', 40, 300, w=900, id='bars', rows=[['GPT-6 Astra · 73% of tasks', .73, O]]),
    tg('reports', 700, 70, "OpenAI's reported figures", bg=D, size=30, id='r'),
    bg_('percent', 980, 300, '*73%*', 120, **SL)), 'How good is it?'),
 # 32 previous model 66%, 75 vs 40 minutes
 (M(X('bars', 'previous', 40, 20, w=900, id='bars', rows=[['GPT-6 Astra · 73%', .73, O], ['previous top model · 66%', .66, '#B09682']], gap=.3),
    cd('minutes', 40, 340, '75 MIN', 'PREVIOUS MODEL · PER TASK', 'ph:timer-fill', MU, w=520, id='m1', **FL),
    cd('forty', 640, 340, '40 MIN', 'ASTRA · PER TASK', 'ph:timer-fill', O, w=520, id='m2', **SL)), None),
 # 33 OpenAI's own testing
 (M(X('clip', 'testing', 40, 40, by='HOW TO READ THIS', text="OpenAI's own testing: a strong claim, not a guarantee", hi='not a guarantee', w=760, id='cl', **FL),
    st('own', 850, 60, 'OWN TEST', 70, MU, -8, id='s', **SL),
    ic('claim', 120, 400, 'ph:megaphone-fill', 140, O, id='m'), ic('guarantee', 360, 400, 'ph:seal-question-fill', 140, R, id='q'),
    tg('guarantee', 560, 450, 'independent results vary', bg=D, size=30, id='t')), None),
 # 34 OpenAI's chart ranks Astra above Claude Fable 5.2
 (M(tl_(0.02, 40, 20, 'logos:openai-icon', 80, label='OpenAI chart', id='oa'),
    X('bars', 'ranks', 260, 30, w=780, id='bars', rows=[['GPT-6.2 Astra · 1,318', 1.0, O], ['Claude Fable 5.2 · 1,271', .96, '#C98A5A']], gap=.4),
    tl_('anthropics', 1100, 40, 'simple-icons:anthropic', 70, label='Anthropic', color=D, id='an', box=130),
    st('again', 300, 420, "OPENAI'S OWN CHART", 64, MU, -6, id='s', **SL)), None),
 # 35 not instant: many minutes, assistant jobs
 (M(st('instant', 40, 30, 'NOT INSTANT', 80, R, -6, id='s', **SL),
    cd('minutes', 40, 230, '1 MIN', 'A BIG TASK CAN TAKE', 'ph:clock-fill', BL, w=480, id='mn', **FL),
    tl_('assistant', 820, 60, 'ph:user-gear-fill', 100, label='jobs for an assistant', color=O, id='as', box=180),
    ch('quick', 640, 420, 'quick questions → use Sol', icon='ph:lightning-fill', color=Y, size=32, id='q'),
    acts=[{'do': 'count', 'id': 'mn', 'at': 'minutes', 'values': ['3 MIN', '8 MIN', '15 MIN', '20+ MIN'], 'dt': .2}]), None),
 # 36 ★ quiz intro
 (M(tl_('game', 40, 40, 'ph:game-controller-fill', 100, label='quick game', color=P, id='g'),
    bg_('astra', 260, 60, 'ASTRA *or* SOL?', 120, **SL),
    cd('pick', 260, 320, 'ASTRA', 'BUZZER A', 'ph:brain-fill', O, w=380, id='a', **LF),
    cd('pick', 700, 320, 'SOL', 'BUZZER B', 'ph:lightning-fill', Y, w=380, id='b', **SD)), 'Astra or Sol?'),
 # 37 job 1: email -> Sol
 (M(tg(0.02, 0, 0, 'JOB 1', bg=P, size=34, id='j'),
    win('email', 40, 70, 640, 420, 'Inbox · 1 long email', lines_html(['Re: Q3 plan (2,400 words)', '…', 'Please summarise before 5 pm'], top=80, size=28, gap=70), id='w', **FL),
    st('sol', 760, 90, 'SOL', 140, G, -8, id='s', **SL),
    ch('fast', 760, 360, 'fast', icon='ph:lightning-fill', color=Y, id='f'), ch('cheap', 960, 360, 'cheap', icon='ph:coins-fill', color=G, id='c')), None),
 # 38 job 2: 50 invoices -> Astra
 (M(tg(0.02, 0, 0, 'JOB 2', bg=P, size=34, id='j'),
    cd('fifty', 40, 80, '0', 'INVOICES ON YOUR COMPUTER', 'ph:receipt-fill', MU, w=520, id='n', **FL),
    win('spreadsheet', 40, 330, 560, 300, 'invoices.xlsx', sheet([('No.', 'Vendor', '₹'), ('001', 'Acme', '4,200'), ('002', 'Ravi Traders', '1,150'), ('…', '…', '…')], 180), id='w', **FL),
    st('astra', 700, 120, 'ASTRA', 140, O, -8, id='s', **SL),
    tg('real', 720, 400, 'real computer work', bg=O, size=36, id='rw'),
    acts=[{'do': 'count', 'id': 'n', 'at': 'fifty', 'values': ['10', '25', '40', '50'], 'dt': .12}]), None),
 # 39 job 3: big codebase -> Astra, or Sol at 1/5 cost
 (M(tg(0.02, 0, 0, 'JOB 3', bg=P, size=34, id='j'),
    tl_('bug', 40, 80, 'ph:bug-fill', 100, label='bug in a big codebase', color=R, id='b', box=180),
    st('astra', 320, 80, 'ASTRA', 100, O, -8, id='s1', **SL), st('budget', 780, 110, 'or SOL', 80, G, 6, id='s2', **SL),
    cd('fifth', 320, 340, '1/5', 'SOL · COST OF ASTRA', 'ph:coins-fill', G, w=420, id='c', **FL),
    X('clip', 'matches', 800, 300, by='OPENAI SAYS', text='Sol nearly matches Astra on ready-to-merge code', hi='nearly matches', w=460, id='cl', **SD)), None),
 # 40 ★ job 4: birthday message -> Sol
 (M(tg(0.02, 0, 0, 'JOB 4', bg=P, size=34, id='j'),
    X('phone', 0.05, 40, 60, w=330, h=600, msgs=[['user', 'write a birthday message for Rahul', 'birthday'], ['ai', 'Happy birthday, Rahul! Wishing you a <b>brilliant</b> year ahead.', 'please']], id='ph', **FL),
    ic('friend', 440, 80, 'ph:cake-fill', 170, O, id='ck'),
    st('sol', 430, 330, 'USE SOL', 110, G, -8, id='s', **SL),
    tg('hard', 440, 560, 'save Astra for the hard stuff', bg=D, size=32, id='h')), None),
 # 41 India price: Go 399, no Astra
 (M(tl_('india', 40, 40, 'circle-flags:in', 90, label='India', id='in'),
    bg_('money', 240, 50, 'The money *question*', 96),
    X('pcard', 'go', 240, 280, name='ChatGPT Go', price='₹399 / month', ok=False, w=420, id='g', **FL),
    tg('include', 740, 330, 'no Astra', bg=R, size=44, id='na', **SL)), 'Price in India'),
 # 42 Plus ~1,999 incl GST
 (M(X('pcard', 'plus', 40, 40, name='ChatGPT Plus', price='Astra in Work + Codex', ok=True, hi=True, w=440, id='p', **FL),
    cd('thousand', 560, 40, '₹0', 'PER MONTH · INDIA', 'ph:currency-inr-bold', O, w=560, id='pr', **FL),
    tg('gst', 580, 280, 'including GST', bg=D, size=34, id='g'),
    ch('cheapest', 40, 400, 'the cheapest way to get Astra', icon='ph:tag-fill', color=G, size=36, id='c'),
    acts=[{'do': 'count', 'id': 'pr', 'at': 'thousand', 'values': ['₹500', '₹1,000', '₹1,500', '~₹1,999'], 'dt': .15}]), None),
 # 43 students: big bill; free / Go are enough for study
 (M(tl_('students', 40, 40, 'ph:student-fill', 100, label='students', color=BL, id='s'),
    cd('bill', 300, 40, '≈ ₹24,000', 'PLUS FOR A YEAR (12 × ₹1,999)', 'ph:wallet-fill', R, w=600, id='b', **FL),
    ch('writing', 60, 330, 'writing', icon='ph:pencil-simple-fill', color=O, id='w'),
    ch('study', 300, 330, 'study', icon='ph:book-open-fill', color=BL, id='st'),
    X('pcard', 'free', 620, 320, name='Free', price='everyday models', ok=True, w=300, id='f', **FL),
    X('pcard', 'go', 960, 320, name='Go', price='₹399 / month', ok=True, w=300, id='g', **FL),
    tg('fine', 620, 520, 'will do just fine', bg=G, size=32, id='ok')), None),
 # 44 check the official pricing page
 (M(ILL(), win(0.02, 40, 30, 760, 500, 'chatgpt.com/pricing', '', id='w', **FL),
    X('pcard', 0.1, 70, 110, name='Go', price='₹399', w=220, id='a'), X('pcard', 0.15, 310, 110, name='Plus', price='~₹1,999', w=220, hi=True, id='b'),
    X('pcard', 0.2, 550, 110, name='Pro', price='much more', w=220, id='c'),
    ic('change', 880, 60, 'ph:arrows-down-up-bold', 150, O, id='ch'), tg('change', 860, 260, 'prices change', bg=O, size=34, id='pc'),
    tg('pay', 860, 360, 'check before you pay', bg=D, size=34, id='pp'),
    cur(0.2, [[700, 650, 0.2, False], [420, 190, 'check', True]], id='cu')), None),
 # 45 API price: Astra $8 in / $40 out
 (M(tl_('developers', 40, 40, 'ph:code-bold', 90, label='developers', color=D, id='d'),
    cd('eight', 300, 40, '$8', 'ASTRA · PER 1M INPUT TOKENS', 'ph:arrow-down-bold', BL, w=560, id='i', **FL),
    cd('forty', 300, 300, '$40', 'ASTRA · PER 1M OUTPUT TOKENS', 'ph:arrow-up-bold', O, w=560, id='o', **FL),
    tg('api', 940, 80, 'API pricing (Nov 2026)', bg='#EFE3D7', color=MU, size=22)), None),
 # 46 Sol $2/$10; Astra 4x
 (M(cd('two', 40, 40, '$2 / $10', 'SOL · IN / OUT PER 1M', 'ph:lightning-fill', Y, w=520, id='s', **LF),
    cd(0.02, 640, 40, '$8 / $40', 'ASTRA · IN / OUT PER 1M', 'ph:brain-fill', O, w=520, id='a', **SD),
    bg_('four', 300, 320, 'Astra = *4×* the price', 110, **SL)), None),
 # 47 ★ the trap: "gpt 6 astra free" searches
 (M(ILL(), win(0.02, 40, 30, 760, 240, 'Search', '', id='w', **FL),
    X('type', 'free', 70, 100, w=700, h=90, text='gpt 6 astra free', dur=.7, id='q'),
    cd('biggest', 40, 330, '58K', 'SEARCHES A MONTH · vidIQ', 'ph:magnifying-glass-bold', O, w=480, id='n', **FL),
    tl_('scammers', 880, 60, 'ph:detective-fill', 110, label='scammers follow', color=R, id='sc', box=190),
    ic('follow', 900, 360, 'ph:footprints-fill', 140, R, id='fp')), 'The free Astra trap'),
 # 48 ★ fake APK site = SCAM
 (M(win('websites', 40, 30, 760, 480, 'free-gpt6-astra.apk.xyz',
        '<div style="text-align:center;padding-top:70px"><div style="font:900 60px \'SD Display\';color:#2A2018">FREE GPT-6 ASTRA</div><div style="font:800 32px \'SD Text\';color:#C98A00;margin:14px 0 30px">Unlimited · No login</div><span class="pbtn p" style="font-size:34px">⬇ Download APK</span></div>', id='w', **FL),
    st('steal', 180, 230, 'SCAM', 160, R, -12, id='s', **SL),
    tl_('account', 880, 40, 'ph:user-circle-minus-fill', 100, label='your account', color=R, id='ac', box=180),
    tl_('card', 880, 320, 'ph:credit-card-fill', 100, label='card details', color=R, id='cc', box=180),
    acts=[{'do': 'shake', 'id': 'w', 'at': 'promising'}]), None),
 # 49 the only safe places
 (M(ch('safe', 40, 60, 'chatgpt.com', icon='ph:lock-fill', color=G, size=40, id='a', **LF),
    ch('apps', 40, 180, 'Official ChatGPT apps', icon='ph:seal-check-fill', color=G, size=40, id='b', **LF),
    ch('api', 40, 300, "OpenAI's own API", icon='ph:code-bold', color=G, size=40, id='c', **LF),
    bg_('deal', 620, 120, 'Too good', 100), bg_('good', 620, 240, 'to be true?', 100), bg_('is', 620, 360, 'It *is*.', 100, **SL)), None),
 # 50 OpenAI's warning: first "Critical" for cybersecurity
 (M(tl_('warning', 40, 40, 'ph:shield-warning-fill', 100, label='OpenAI warning', color=R, id='sh', box=180),
    X('clip', 'first', 300, 40, by="OPENAI · PREPAREDNESS FRAMEWORK", text='GPT-6 Astra: the first model rated "Critical" for cybersecurity', hi='Critical', w=820, id='cl', **FL),
    st('critical', 380, 380, 'CRITICAL', 130, R, -6, id='s', **SL),
    acts=[{'do': 'shake', 'id': 's', 'at': 'framework'}]), "OpenAI's own warning"),
 # 51 could find security holes; monitors pause tasks
 (M(tl_('holes', 40, 40, 'ph:lock-open-fill', 100, label='serious security holes', color=R, id='h', box=180),
    ch('little', 40, 330, 'with very little human help', icon='ph:user-minus-fill', color=MU, id='lh'),
    win('watches', 560, 30, 700, 420, 'Safety monitor · task #4812', lines_html(['Task: update records', 'Status: running'], top=80, size=28, gap=60), id='w', **SD),
    ic('watches', 1100, 120, 'ph:eye-fill', 110, BL, id='ey'),
    X('toast', 'pause', 600, 320, text='Paused by safety monitor', icon='ph:pause-circle-fill', id='t', **SD)), None),
 # 52 harder to monitor
 (M(X('clip', 'admits', 40, 40, by='OPENAI ADMITS', text='Astra is harder to monitor than its previous model', hi='harder to monitor', w=760, id='cl', **FL),
    ic('monitor', 900, 40, 'ph:binoculars-fill', 180, MU, id='b'),
    ch('closely', 40, 380, 'so OpenAI watches it closely', icon='ph:eye-fill', color=BL, size=36, id='c')), None),
 # 53 least access
 (M(ILL(), X('toggle', 'apps', 40, 40, w=560, label='Excel (needed)', icon='ph:microsoft-excel-logo-fill', color=G, id='t1'),
    X('toggle', 'files', 40, 140, w=560, label='sales.xlsx (needed)', icon='ph:file-xls-fill', color=G, id='t2'),
    X('toggle', 'only', 40, 240, w=560, label='Banking app', icon='ph:bank-fill', color=R, id='t3'),
    X('toggle', 'only', 40, 340, w=560, label='Passwords', icon='ph:password-fill', color=R, id='t4'),
    bg_('needs', 700, 120, 'Only what', 96), bg_('needs', 700, 230, 'it *needs*', 96),
    acts=[{'do': 'on', 'id': 't1', 'at': 'apps'}, {'do': 'on', 'id': 't2', 'at': 'files'}]), None),
 # 54 ★ five tips
 (M(bg_('tips', 40, 40, 'FIVE *TIPS*', 150, **SL),
    *[tl_(round(.3 + k * .1, 2), 40 + k * 250, 330, r, 80, color=c, id=f't{k}') for k, (r, c) in enumerate(
        [('ph:target-bold', O), ('ph:bank-fill', R), ('ph:stack-fill', BL), ('ph:lightning-fill', Y), ('ph:magnifying-glass-bold', D)])]), 'Five tips'),
 # 55 tip 1 full picture
 (M(bg_('one', 40, 20, '*1*', 220, **SL), bg_('picture', 260, 60, 'the full picture', 80),
    ch('goal', 260, 260, 'the goal', icon='ph:target-bold', color=O, size=36, id='a'),
    ch('files', 560, 260, 'the files', icon='ph:files-fill', color=BL, size=36, id='b'),
    ch('finished', 260, 380, 'what "finished" looks like', icon='ph:flag-checkered-fill', color=G, size=36, id='c')), None),
 # 56 tip 2 never banking / passwords / payment
 (M(bg_('two', 40, 20, '*2*', 220, **SL),
    tl_('banking', 280, 60, 'ph:bank-fill', 90, label='banking apps', color=D, id='a', box=170),
    tl_('passwords', 580, 60, 'ph:password-fill', 90, label='passwords', color=D, id='b', box=170),
    tl_('payment', 880, 60, 'ph:credit-card-fill', 90, label='payment pages', color=D, id='c', box=170),
    st('never', 420, 360, 'NEVER', 140, R, -6, id='s', **SL)), None),
 # 57 tip 3 stages
 (M(bg_('three', 40, 20, '*3*', 220, **SL),
    ch('stages', 280, 60, 'Stage 1', icon='ph:number-circle-one-fill', color=BL, size=36, id='a'),
    ch('stages', 560, 140, 'Stage 2', icon='ph:number-circle-two-fill', color=BL, size=36, id='b'),
    ch('stages', 840, 220, 'Stage 3', icon='ph:number-circle-three-fill', color=BL, size=36, id='c'),
    ch('check', 280, 400, 'check after each one', icon='ph:check-circle-fill', color=G, size=40, id='d')), None),
 # 58 tip 4 Sol for small things
 (M(bg_('four', 40, 20, '*4*', 220, **SL),
    tl_('sol', 280, 60, 'ph:lightning-fill', 90, label='Sol: small things', color=Y, id='s', box=180),
    cd('limit', 560, 60, 'FULL', 'YOUR ASTRA LIMIT', 'ph:battery-full-fill', G, w=520, id='l', **FL),
    tg('lasts', 580, 320, 'lasts for the big jobs', bg=G, size=34, id='t')), None),
 # 59 tip 5 check its work
 (M(bg_('five', 40, 20, '*5*', 220, **SL), tl_('check', 280, 60, 'ph:magnifying-glass-bold', 90, label='check its work', color=D, id='m', box=180),
    X('phone', 'smartest', 620, 0, w=330, h=600, msgs=[['user', 'What is 17 × 24?', 'smartest'], ['ai', 'Definitely <b>418</b>!', 'confidently']], id='ph', **SD),
    st('wrong', 1010, 250, 'WRONG', 60, R, 8, id='s', **SL), tg('wrong', 1010, 400, 'answer: 408', bg=G, size=30, id='a')), None),
 # 60 ★ did Max get the afternoon off?
 (M(win('report', 40, 30, 640, 460, 'weekly_report.docx', lines_html(['Weekly sales report', 'Total: ₹4.2 lakh  ▲ 12%', 'Top region: South'], top=80, size=30, gap=70), id='w', **FL),
    st('partly', 720, 40, 'PARTLY', 110, O, -8, id='p', **SL),
    X('toast', 'built', 80, 520, text='Report built by Astra', id='t', **SD),
    ch('checking', 720, 330, 'time saved → checking it', icon='ph:magnifying-glass-bold', color=BL, size=34, id='c')), 'Wrap-up'),
 # 61 ★ not magic, not free, saves hours
 (M(st('magic', 40, 40, 'NOT MAGIC', 90, MU, -8, id='m', **SL), st('free', 40, 230, 'NOT FREE', 90, R, 6, id='f', **SL),
    tl_('computer', 780, 40, 'ph:laptop-fill', 100, label='work on a computer?', color=D, id='pc', box=180),
    cd('hours', 640, 330, 'HOURS', 'IT CAN SAVE YOU', 'ph:clock-countdown-fill', G, w=520, id='h', **FL)), None),
 # 62 ★ comments
 (M(tl_('comments', 40, 40, 'logos:youtube-icon', 90, label='comments', id='yt', box=170),
    X('card', 'first', 300, 60, icon='ph:user-circle-fill', label='YOUR COMMENT', big='The first job I’d hand to Astra…', bsize=46, color=O, id='cm', **FL),
    ic('astra', 400, 360, 'ph:chat-circle-dots-fill', 160, O, id='c')), None),
 # 63 subscribe
 ({'type': 'end', 'sub': 'More tech, decoded.'}, None),
]

assert len(V) == len(e['beats']), (len(V), len(e['beats']))
# every word-timed 'at' must exist in its line (otherwise it silently falls back to the line start)
tl = json.loads((HERE.parent.parent / 'src/episodes/ep08-long.timeline.json').read_text())
bad = []
for i, (v, _) in enumerate(V):
    if v.get('type') != 'mix':
        continue
    words = {re.sub(r'[^a-z0-9]', '', w['w'].lower()) for w in tl['beats'][i]['words']}
    for it in v['els'] + v['acts']:
        a = it.get('at')
        if isinstance(a, str) and a not in words:
            bad.append((i, a))
        for p in it.get('pts', []):
            if isinstance(p[2], str) and p[2] not in words:
                bad.append((i, 'cursor:' + p[2]))
        for m in it.get('msgs', []):
            if isinstance(m[2], str) and m[2] not in words:
                bad.append((i, 'msg:' + m[2]))
        if isinstance(it.get('qat'), str) and it['qat'] not in words:
            bad.append((i, 'qat:' + it['qat']))
assert not bad, bad
for b, (v, chp) in zip(e['beats'], V):
    b['v'] = v
    if chp:
        b['chapter'] = chp
    else:
        b.pop('chapter', None)
f.write_text(json.dumps(e, indent=1, ensure_ascii=False))
print('beats', len(V))
