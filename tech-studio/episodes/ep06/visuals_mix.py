"""ep06 full rebuild in the MIXED style (owner approved the opening demo, 2026-11-23): kit_mix beats with exact visuals per
line (real logos, specific icons, papercut props/photo prints, old pop cards/counters/bars), Vox boards for the key studies.
Lines 0-9 come from episodes/ep06demo/visuals.py. Run: python3 episodes/ep06/visuals_mix.py, then
STYLE=paper THEME=cream GRID=plain python3 tools/hf_ep06_long.py (registers kit_mix)."""
import json
from pathlib import Path
HERE = Path(__file__).parent
f = HERE / 'long.json'; e = json.loads(f.read_text())
src = (HERE.parent / 'ep06demo/visuals.py').read_text().split('\nfor b, (v, ch) in zip')[0]
ns = {'__file__': str(HERE.parent / 'ep06demo/visuals.py')}; exec(src, ns)
M, X, V0 = ns['M'], ns['X'], ns['V']
OLD = {i: b['v'] for i, b in enumerate(e['beats'])}   # current visuals (Vox boards reused below)
G, R, O, D, P, BL = '#2F9E44', '#E0471C', '#F87736', '#2A2018', '#7A5CFF', '#1C7ED6'

V = V0 + [
 # 10 myth claim ★
 (M(X('clip', 'common', 30, 40, by='THE MOST COMMON EXPLANATION', text='"A quantum computer tries every answer at the same time"', hi='every answer at the same time', w=760, id='cl'),
    X('prop', 'tries', 860, 40, p='maze', s=.95, id='mz'),
    *[X('prop', 'every', 890 + (k % 3) * 95, 90 + (k // 3) * 110, p='bit', s=.22, id=f'g{k}') for k in range(6)],
    X('stamp', 'myth', 300, 420, text='MYTH', size=150, id='st', **{'in': 'slam'})), 'The biggest myth'),
 # 11 tried everything -> one random answer -> useless
 (M(*[X('arrow', 'everything', 40, 60 + k * 70, w=360, rot=(k - 2) * 8, id=f'a{k}') for k in range(5)],
    X('icon', 'one', 520, 60, ref='ph:dice-five-fill', size=200, color=P, paper=True, id='dice'),
    X('tag', 'random', 500, 360, text='one random answer', size=36, id='rt'),
    X('icon', 'look', 860, 80, ref='ph:eye-fill', size=150, color=D, id='eye'),
    X('icon', 'useless', 880, 320, ref='ph:thumbs-down-fill', size=170, color=R, id='td'),
    X('big', 'useless', 760, 540, text='*USELESS*', size=110, id='us', **{'in': 'slam'}),
    acts=[{'do': 'spin', 'id': 'dice', 'at': 'random', 'deg': 360, 'd': 1.2}]), None),
 # 12 interference: waves add up / cancel
 (M(X('big', 'interference', 40, 20, text='INTER*FERENCE*', size=110, id='h', **{'in': 'slam'}),
    X('prop', 'waves', 40, 200, p='waves', s=1.1, id='wv'),
    X('icon', 'water', 760, 180, ref='ph:waves-bold', size=160, color=BL, paper=True, id='wi'),
    X('card', 'add', 40, 520, icon='ph:plus-circle-fill', label='WAVES MEET', big='add *up*', w=460, id='up', color=G),
    X('card', 'cancel', 620, 520, icon='ph:minus-circle-fill', label='WAVES MEET', big='cancel out', w=520, id='dn', color=R, **{'in': 'slide'})), None),
 # 13 algorithm = recipe: wrong answers cancel, right one grows
 (M(X('icon', 'recipe', 40, 40, ref='ph:cooking-pot-fill', size=180, color=O, paper=True, id='rc'),
    X('tag', 'recipe', 30, 300, text='quantum algorithm = a recipe', size=32, id='rt'),
    *[X('tag', 'wrong', 560 + k * 170, 80, text=f'answer {k + 1}', bg='#8C6B5A', size=30, id=f'w{k}') for k in range(4)],
    X('tag', 'right', 760, 300, text='✓ right answer', bg=G, size=40, id='ok', **{'in': 'slam'}),
    X('icon', 'measure', 560, 440, ref='ph:eye-fill', size=120, color=D, id='ey'),
    X('big', 'likely', 700, 470, text='likely: the *right* one', size=64, id='lk'),
    acts=[*[{'do': 'out', 'id': f'w{k}', 'at': 'cancel'} for k in (0, 1, 2, 3)], {'do': 'move', 'id': 'ok', 'at': 'stronger', 'scale': 1.5, 'd': .5}]), None),
 # 14 not faster at everything
 (M(X('card', 'faster', 30, 40, icon='ph:rocket-launch-fill', label='QUANTUM COMPUTERS', big='faster at *everything*?', w=760, id='q'),
    X('stamp', 'aren\'t', 940, 150, text='NO', size=130, id='no', **{'in': 'slam'}),
    X('icon', 'win', 60, 330, ref='ph:atom-bold', size=150, color=P, paper=True, id='a1'),
    X('icon', 'win', 320, 330, ref='ph:lock-key-fill', size=150, color=R, paper=True, id='a2'),
    X('tag', 'problems', 60, 590, text='they win only where a recipe exists', bg=G, size=36, id='w')), None),
 # 15 why a golden chandelier? (chapter)
 (M(X('prop', 'computer', 60, 20, p='fridge', s=1.0, id='fr', **{'in': 'drop'}),
    X('big', 'chandelier', 560, 120, text='a giant *golden*', size=90, id='h1'),
    X('big', 'chandelier', 560, 230, text='chandelier?', size=120, id='h2', **{'in': 'slam'}),
    X('icon', 'why', 1100, 400, ref='ph:question-fill', size=180, color=O, id='q')), 'Colder than space'),
 # 16 fragile: heat, vibration, stray signal = noise
 (M(X('prop', 'fragile', 40, 60, p='qcoin', text='Q', s=1.1, id='qb'),
    X('tag', 'fragile', 40, 420, text='incredibly fragile', bg=R, size=36, id='fg'),
    X('icon', 'heat', 520, 40, ref='ph:fire-fill', size=140, color=R, paper=True, id='h'),
    X('icon', 'vibration', 760, 40, ref='ph:vibrate-bold', size=140, color=D, paper=True, id='v'),
    X('icon', 'signal', 1000, 40, ref='ph:wifi-high-bold', size=140, color=BL, paper=True, id='s'),
    X('big', 'noise', 600, 400, text='= *NOISE*', size=150, id='n', **{'in': 'slam'}),
    acts=[{'do': 'shake', 'id': 'qb', 'at': 'knocks'}, {'do': 'shake', 'id': 'qb', 'at': 'delicate'}]), None),
 # 17 Google's chips in special fridges at ~0.01 K
 (M(X('logo', "google's", 40, 40, ref='logos:google', size=260, id='gl'),
    X('prop', 'refrigerators', 60, 180, p='thermo', s=1.0, id='th'),
    X('card', 'cool', 420, 220, icon='ph:snowflake-bold', label='INSIDE THE FRIDGE', big='300 K', w=560, color=BL, id='k'),
    X('tag', 'absolute', 440, 470, text='just above absolute zero (−273.15 °C)', size=32, id='az'),
    acts=[{'do': 'count', 'id': 'k', 'at': 'cool', 'values': ['300 K', '77 K', '4 K', '1 K', '0.1 K', '0.01 K'], 'dt': .18}]), None),
 # 18 space 2.7 K vs chip 0.01 K -> 270x colder (Vox stat kept)
 (OLD[18], None),
 # 19 qubits make mistakes; biggest wall for decades (chapter)
 (M(*[X('prop', 'qubits', 40 + k * 210, 60, p='qcoin', text='Q', s=.6, id=f'c{k}') for k in range(5)],
    *[X('icon', 'mistakes', 120 + k * 420, 40, ref='ph:x-circle-fill', size=90, color=R, id=f'x{k}') for k in range(3)],
    X('icon', 'wall', 60, 360, ref='ph:wall-fill', size=200, color='#8C6B5A', paper=True, id='w'),
    X('big', 'wall', 360, 400, text='the *biggest wall*', size=96, id='bw'),
    X('tag', 'decades', 380, 540, text='for decades', bg=D, size=40, id='dc')), 'Errors: the real battle'),
 # 20 error correction: many physical -> one logical
 (M(*[X('prop', 'many', 40 + (k % 3) * 120, 60 + (k // 3) * 130, p='qcoin', text='q', s=.38, id=f'p{k}') for k in range(9)],
    X('arrow', 'combine', 440, 180, w=260, id='ar'),
    X('prop', 'logical', 760, 60, p='qcoin', text='L', s=1.1, id='lq', **{'in': 'slam'}),
    X('icon', 'reliable', 1040, 40, ref='ph:check-circle-fill', size=110, color=G, id='ck'),
    X('tag', 'correction', 40, 470, text='ERROR CORRECTION', bg=O, size=44, id='ec'),
    X('tag', 'logical', 700, 470, text='9 physical → 1 logical qubit', size=34, id='lg')), None),
 # 21 more qubits -> more errors
 (M(X('bars', 'adding', 40, 40, w=760, id='b', rows=[['qubits', .4, P], ['qubits', .75, P], ['errors', .45, R], ['errors', .85, R]], gap=.35),
    X('icon', 'errors', 900, 60, ref='ph:trend-up-bold', size=230, color=R, id='tu'),
    X('big', 'too', 860, 380, text='more *errors*', size=90, id='me')), None),
 # 22 Willow: bigger groups, fewer errors; ~30-year milestone (Vox words kept? use mix)
 (M(X('logo', "willow's", 40, 30, ref='logos:google-icon', size=110, paper=True, id='g'),
    X('bars', 'bigger', 260, 40, w=640, id='b', rows=[['3×3 group: errors', .9, R], ['5×5 group: errors', .55, O], ['7×7 group: errors', .28, G]], gap=.5),
    X('icon', 'down', 980, 60, ref='ph:trend-down-bold', size=200, color=G, id='td'),
    X('big', 'down', 260, 430, text='errors went *DOWN*', size=96, id='dn', **{'in': 'slam'}),
    X('tag', 'thirty', 280, 560, text='a goal since 1995 (≈30 years)', bg=D, size=34, id='yr')), None),
 # 23 Quantum Echoes (Vox stat kept)
 (OLD[23], None),
 # 24 useful for? not browsing / gaming / ChatGPT (chapter)
 (M(X('big', 'useful', 40, 20, text='Useful for…?', size=96, id='h'),
    X('icon', 'browsing', 60, 200, ref='ph:browser-fill', size=170, color=BL, paper=True, id='b'),
    X('icon', 'gaming', 420, 200, ref='ph:game-controller-fill', size=170, color=D, paper=True, id='gm'),
    X('logo', 'chatgpt', 780, 200, ref='logos:openai-icon', size=170, paper=True, id='ai'),
    *[X('icon', w, 200 + k * 360, 180, ref='ph:x-bold', size=110, color=R, id=f'x{k}', **{'in': 'slam'}) for k, w in enumerate(['browsing', 'gaming', 'faster'])],
    X('tag', 'faster', 60, 520, text='not your everyday apps', bg=R, size=38, id='t')), "What it's actually good for"),
 # 25 molecules: medicines, batteries, materials
 (M(X('prop', 'molecules', 40, 40, p='molecule', s=1.1, id='m'),
    X('tag', 'nature', 40, 470, text='quantum by nature', bg=P, size=36, id='qn'),
    X('icon', 'medicines', 560, 40, ref='ph:pill-fill', size=150, color=R, paper=True, id='pi'),
    X('icon', 'batteries', 820, 40, ref='ph:battery-charging-fill', size=150, color=G, paper=True, id='ba'),
    X('icon', 'materials', 1080, 40, ref='ph:cube-fill', size=130, color=O, paper=True, id='ma'),
    X('tag', 'medicines', 560, 290, text='new medicines', size=30, id='t1'),
    X('tag', 'batteries', 820, 290, text='better batteries', size=30, id='t2'),
    X('tag', 'materials', 1060, 290, text='new materials', size=30, id='t3')), None),
 # 26 optimisation & simulation, still debated
 (M(X('icon', 'optimisation', 40, 40, ref='ph:path-bold', size=200, color=O, paper=True, id='pa'),
    X('icon', 'optimisation', 360, 40, ref='ph:truck-fill', size=160, color=D, paper=True, id='tr'),
    X('icon', 'simulation', 660, 40, ref='ph:cloud-lightning-fill', size=170, color=BL, paper=True, id='we'),
    X('tag', 'hard', 60, 330, text='hard optimisation & simulation', size=36, id='t'),
    X('stamp', 'debating', 500, 430, text='STILL DEBATED', size=80, color='#8C6B5A', rot=-6, id='sd', **{'in': 'slam'})), None),
 # 27 the worry: governments & banks; encryption
 (M(X('icon', 'governments', 40, 40, ref='ph:flag-fill', size=150, color=D, paper=True, id='gv'),
    X('icon', 'banks', 300, 40, ref='ph:bank-fill', size=150, color=D, paper=True, id='bk'),
    X('prop', 'encryption', 640, 20, p='lock', s=1.0, id='lk'),
    X('big', 'breaking', 40, 330, text='breaking *encryption*', size=96, id='be', **{'in': 'slam'}),
    X('tag', 'online', 60, 470, text='it protects almost everything online', size=34, id='ol'),
    acts=[{'do': 'shake', 'id': 'lk', 'at': 'breaking'}]), None),
 # 28 UPI + WhatsApp rely on hard maths (chapter)
 (M(X('tag', 'upi', 40, 60, text='UPI ₹', bg=O, size=72, id='upi'),
    X('logo', 'whatsapp', 360, 30, ref='logos:whatsapp-icon', size=160, paper=True, id='wa'),
    X('icon', 'security', 640, 40, ref='ph:lock-key-fill', size=160, color=D, paper=True, id='lk'),
    X('card', 'maths', 40, 330, icon='ph:function-bold', label='HARD MATHS PROBLEM', big='crack time: ∞', w=640, id='mh'),
    X('icon', 'forever', 760, 330, ref='ph:hourglass-high-fill', size=170, color=R, id='hg'),
    acts=[{'do': 'spin', 'id': 'hg', 'at': 'forever', 'deg': 180, 'd': .8}]), 'Your bank is already preparing'),
 # 29 a big error-corrected QC could crack them much faster
 (M(X('prop', 'large', 40, 40, p='qcoin', text='Q', s=1.4, id='q'),
    X('icon', 'faster', 560, 40, ref='ph:lightning-fill', size=200, color='#F5B400', id='l'),
    X('icon', 'solve', 840, 40, ref='ph:lock-open-fill', size=220, color=R, paper=True, id='lo', **{'in': 'slam'}),
    X('tag', 'error', 40, 520, text='large + error-corrected (not built yet)', size=36, id='t')), None),
 # 30 nobody built it; 2030s? exact date unknown (Vox stat kept)
 (OLD[30], None),
 # 31 harvest now, decrypt later
 (M(X('prop', 'steal', 40, 60, p='thief', s=1.0, id='th'),
    *[X('prop', 'encrypted', 380 + k * 90, 80 + (k % 2) * 40, p='envelope', s=.5, id=f'e{k}') for k in range(3)],
    X('tag', 'harvest', 380, 330, text='HARVEST NOW', bg=R, size=48, id='h'),
    X('icon', 'wait', 820, 60, ref='ph:clock-countdown-fill', size=170, color=D, id='c'),
    X('tag', 'decrypt', 800, 330, text='DECRYPT LATER', bg=D, size=48, id='d'),
    X('icon', 'unlock', 900, 440, ref='ph:lock-open-fill', size=140, color=O, id='u')), None),
 # 32 NIST plan (Vox doc kept)
 (OLD[32], None),
 # 33 companies switching; apps update quietly
 (M(X('logo', 'tech', 40, 40, ref='logos:chrome', size=130, paper=True, id='c'),
    X('logo', 'tech', 260, 40, ref='logos:apple', size=120, paper=True, id='a'),
    X('logo', 'tech', 480, 40, ref='logos:signal', size=130, paper=True, id='s'),
    X('icon', 'banks', 700, 40, ref='ph:bank-fill', size=130, color=D, paper=True, id='b'),
    X('tag', 'switching', 40, 300, text='already switching to quantum-safe encryption', bg=G, size=36, id='sw'),
    X('card', 'update', 40, 420, icon='ph:arrows-clockwise-bold', label='YOUR APPS', big='security update…', w=620, id='up'),
    X('icon', 'reason', 900, 420, ref='ph:shield-check-fill', size=170, color=G, id='sh', **{'in': 'slam'})), None),
 # 34 India: National Quantum Mission (chapter) – flag + Vox stat
 (M(X('icon', 'india', 40, 40, ref='circle-flags:in', size=200, id='fl', **{'in': 'drop'}),
    X('big', 'mission', 300, 60, text='National *Quantum* Mission', size=72, id='nm'),
    X('card', 'crore', 300, 240, icon='ph:currency-inr-bold', label='APPROVED 2023', big='₹0 crore', w=640, id='cr'),
    X('tag', 'eight', 320, 470, text='over eight years', bg=D, size=36, id='8y'),
    acts=[{'do': 'count', 'id': 'cr', 'at': 'six', 'values': ['₹1,000 crore', '₹3,000 crore', '₹5,000 crore', '₹6,003 crore'], 'dt': .2}]), 'What about India?'),
 # 35 goal: up to 1,000 qubits by ~2031
 (M(X('icon', 'goal', 40, 40, ref='ph:target-bold', size=200, color=R, paper=True, id='t'),
    X('card', 'thousand', 360, 60, icon='ph:atom-bold', label='GOAL', big='0 qubits', w=620, id='q', color=P),
    X('prop', 'thirty-one', 380, 300, p='calendar', text='2031', s=.9, id='cal'),
    acts=[{'do': 'count', 'id': 'q', 'at': 'thousand', 'values': ['50 qubits', '250 qubits', '500 qubits', '1,000 qubits'], 'dt': .15}]), None),
 # 36 QpiAI 25 vs Google 105
 (M(X('prop', 'qpiai', 40, 60, p='chip', text='25', s=.7, id='qp'),
    X('tag', 'bengaluru', 30, 330, text='QpiAI · Bengaluru', size=34, id='qt'),
    X('prop', "google's", 520, 20, p='chip', text='105', s=1.25, id='gw'),
    X('logo', "google's", 880, 40, ref='logos:google-icon', size=90, id='gl'),
    X('tag', "google's", 540, 450, text='Google Willow', bg=D, size=34, id='gt'),
    X('tag', 'start', 40, 520, text="far smaller, but it's a start", bg=G, size=36, id='st')), None),
 # 37 1,000+ km quantum-secure links
 (M(X('icon', 'india', 40, 40, ref='circle-flags:in', size=130, id='fl'),
    X('icon', 'communication', 220, 40, ref='ph:broadcast-bold', size=130, color=BL, id='bc'),
    X('arrow', 'kilometres', 40, 260, w=900, id='ln'),
    X('card', 'thousand', 260, 360, icon='ph:shield-check-fill', label='QUANTUM-SECURE LINKS', big='1,000+ km', w=560, id='km', color=G, **{'in': 'slam'}),
    X('icon', 'ahead', 980, 60, ref='ph:trophy-fill', size=160, color='#F5B400', paper=True, id='tr')), None),
 # 38 own one at home? no (chapter)
 (M(X('icon', 'home', 40, 40, ref='ph:house-fill', size=220, color=D, paper=True, id='h'),
    X('stamp', 'not', 330, 60, text='NO', size=150, id='no', **{'in': 'slam'}),
    X('tag', 'huge', 40, 420, text='huge', bg=D, size=44, id='t1'),
    X('tag', 'fragile', 240, 420, text='fragile', bg=R, size=44, id='t2'),
    X('tag', 'specific', 480, 420, text='very specific problems', bg=P, size=44, id='t3')), 'Will you own one?'),
 # 39 through the cloud
 (M(X('prop', 'computers', 40, 120, p='laptop', s=.8, id='lp'),
    X('arrow', 'cloud', 370, 220, w=200, id='a1'),
    X('prop', 'cloud', 600, 60, p='cloud', s=.9, id='cl'),
    X('arrow', 'without', 900, 220, w=160, id='a2'),
    X('prop', 'knowing', 1080, 20, p='fridge', s=.55, id='fr'),
    X('tag', 'knowing', 300, 520, text='often without even knowing it', size=36, id='t')), None),
 # 40 run programs on real chips online, many free
 (M(X('logo', 'companies', 40, 40, ref='logos:ibm', size=260, id='ibm'),
    X('icon', 'students', 40, 260, ref='ph:student-fill', size=150, color=D, paper=True, id='st'),
    X('icon', 'developers', 300, 260, ref='ph:code-bold', size=150, color=O, paper=True, id='dv'),
    X('arrow', 'real', 560, 330, w=200, id='ar'),
    X('prop', 'chips', 800, 260, p='chip', text='Q', s=.75, id='ch'),
    X('stamp', 'free', 780, 30, text='FREE', size=110, color=G, id='fr', **{'in': 'slam'})), None),
 # 41 won't replace your laptop; works alongside
 (M(X('prop', 'laptop', 40, 120, p='laptop', s=.85, id='lp'),
    X('icon', 'alongside', 440, 160, ref='ph:plus-bold', size=150, color='#8C6B5A', id='pl'),
    X('prop', 'quantum', 640, 80, p='qcoin', text='Q', s=1.0, id='q'),
    X('icon', 'tools', 1000, 120, ref='ph:handshake-fill', size=200, color=O, paper=True, id='hs'),
    X('tag', 'alongside', 160, 520, text='a special tool, not a replacement', bg=D, size=38, id='t')), None),
 # 42 bottom line recap (chapter)
 (M(X('card', 'laptop', 40, 30, icon='ph:x-circle-fill', label='IT ISN\'T', big='a faster laptop', w=620, color=R, id='c1'),
    X('card', 'once', 40, 210, icon='ph:x-circle-fill', label='IT DOESN\'T', big='try every answer', w=620, color=R, id='c2'),
    X('card', 'different', 40, 390, icon='ph:check-circle-fill', label='IT IS', big='a *different* machine', w=700, color=G, id='c3', **{'in': 'slam'}),
    X('icon', 'physics', 860, 140, ref='tabler:atom', size=260, color=P, paper=True, id='at')), 'The bottom line'),
 # 43 hype: real vs overblown
 (M(X('icon', 'hype', 520, 20, ref='ph:scales-fill', size=240, color=D, id='sc'),
    X('tag', 'real', 40, 60, text='REAL', bg=G, size=60, id='r'),
    X('icon', 'real', 60, 180, ref='ph:flask-fill', size=120, color=G, paper=True, id='r1'),
    X('icon', 'real', 260, 180, ref='ph:lock-key-fill', size=120, color=G, paper=True, id='r2'),
    X('tag', 'overblown', 900, 60, text='OVERBLOWN', bg=R, size=60, id='o'),
    X('icon', 'overblown', 900, 180, ref='ph:laptop-fill', size=120, color=R, paper=True, id='o1'),
    X('icon', 'overblown', 1100, 180, ref='ph:game-controller-fill', size=120, color=R, paper=True, id='o2'),
    X('big', 'which', 300, 500, text='now you know *which is which*', size=72, id='k')), None),
 # 44 comments question
 (M(X('logo', 'comments', 40, 40, ref='logos:youtube-icon', size=200, id='yt'),
    X('icon', 'comments', 300, 30, ref='ph:chat-circle-text-fill', size=200, color=O, id='ch'),
    X('card', 'problem', 40, 300, icon='ph:user-circle-fill', label='YOUR COMMENT', big='Cure diseases faster…', w=760, id='cm', **{'in': 'fly'}),
    X('big', 'first', 40, 520, text='what should it solve *first*?', size=72, id='q')), None),
 # 45 subscribe end (kept)
 (OLD[45], None),
]
assert len(V) == len(e['beats']), (len(V), len(e['beats']))
for b, (v, ch) in zip(e['beats'], V):
    b['v'] = v
    if ch:
        b['chapter'] = ch
    else:
        b.pop('chapter', None)
f.write_text(json.dumps(e, indent=1, ensure_ascii=False))
print('beats', len(V))
