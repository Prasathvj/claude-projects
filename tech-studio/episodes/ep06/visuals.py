"""ep06 visuals: PAPERCUT props (kit_props 'paperscene'), Vox evidence boards (kit_vox) for numbers and sources, paper cards.
Run: python3 episodes/ep06/visuals.py"""
import json
from pathlib import Path
f = Path(__file__).with_name('long.json'); e = json.loads(f.read_text())

def S(text, x, y, at=.3, c='c', size=50, inn='drop', **k):
    d = dict(p='strip', text=text, x=x, y=y, at=at, c=c, size=size, **{'in': inn}); d.update(k); return d
def Pp(p, x, y, at=.05, inn='drop', **k):
    d = dict(p=p, x=x, y=y, at=at, **{'in': inn}); d.update(k); return d
def PS(*props, moves=None):
    d = {'type': 'paperscene', 'props': list(props)}
    if moves: d['moves'] = moves
    return d
def B(text, x, y, at=.5, size=64):
    return dict(p='banner', text=text, x=x, y=y, at=at, size=size, **{'in': 'drop'})

V = [
 # 1 hook ★
 (PS(Pp('chip', 60, 180, .02, 'drop', text='Q', s=1.0, loop='boil'), Pp('clock', 400, 190, .15, 'pop', s=.85), S('under 5 minutes', 380, 470, .3, 'o', 44),
     *[Pp('calendar', 760 + (k % 2) * 16, 420 - k * 62, .4 + k * .07, 'drop', text='∞', s=.55) for k in range(8)]), 'Ten septillion years'),
 ({'type': 'vstat', 'kicker': 'ONE FOLLOWED BY 25 ZEROS', 'num': '10²⁵', 'unit': 'YEARS', 'sub': 'vs under 5 minutes on Willow', 'hi': 'under 5 minutes',
   'source': 'Google, Willow announcement, Dec 2024', 'note': 'the universe: ~13.8 billion years', 'sx': 760, 'sy': 560, 'nx': 60, 'ny': 580}, None),
 (PS(Pp('chip', 440, 150, .05, 'pop', text='Q', s=1.15, loop='boil'), B('GOOGLE WILLOW', 300, 30, .25, 60),
     Pp('star', 300, 220, .45, 'pop', s=.6, loop='spin'), Pp('star', 820, 330, .55, 'pop', s=.5, loop='spin'), S('magic?', 760, 520, .7, 'r', 54, 'pop')), None),
 (PS(Pp('qcoin', 60, 150, .05, 'drop', s=.8, loop='spin'), Pp('thermo', 330, 120, .2, 'drop', s=.7), Pp('check', 560, 170, .35, 'pop', s=.9), Pp('lock', 800, 120, .5, 'drop', s=.6),
     S('what it is', 40, 420, .1, size=36), S('colder than space', 280, 520, .25, size=36), S("can & can't", 560, 420, .4, size=36), S('your bank', 800, 520, .55, 'o', 36)), None),
 # 2 bits vs qubits
 (PS(Pp('laptop', 240, 150, .02, 'drop', s=.8), S('0', 120, 160, .3, 'c', 70, 'pop'), S('1', 860, 180, .4, 'o', 70, 'pop'), S('0', 900, 420, .5, 'c', 70, 'pop'),
     S('1', 90, 430, .6, 'o', 70, 'pop'), B('BITS', 470, 40, .7, 60)), 'Bits vs qubits'),
 (PS(*[Pp('switch', 40 + k * 205, 140, .05 + k * .08, 'drop', s=.85, on=bool(k % 2), loop='boil') for k in range(6)], S('billions of switches', 360, 500, .7, 'o', 48)), None),
 (PS(Pp('qcoin', 480, 110, .05, 'pop', text='Q', s=1.4, loop='spin'), B('SUPERPOSITION', 330, 470, .5, 64)), None),
 (PS(Pp('qcoin', 140, 160, .05, 'drop', text='1', s=1.2), S('bit: heads OR tails', 60, 470, .2, size=42), Pp('qcoin', 760, 120, .45, 'pop', text='?', s=1.2, loop='spin'),
     S('qubit: still spinning', 680, 470, .55, 'o', 42)), None),
 (PS(Pp('qcoin', 160, 160, .05, 'pop', text='Q', s=1.1, loop='spin'), Pp('arrow', 450, 260, .3, 'fly', len=420, c='o'), Pp('qcoin', 900, 160, .15, 'pop', text='Q', s=1.1, loop='spin'),
     B('ENTANGLEMENT', 350, 480, .55, 60)), None),
 ({'type': 'vdoc', 'label': 'POSSIBLE STATES = 2 TO THE POWER OF n', 'lines': ['2 qubits   →  4 states', '10 qubits  →  1,024 states', '300 qubits →  more states than', '              atoms in the universe'],
   'hi': [2, 'more states than'], 'circle': [1, '1,024'], 'note': 'exponential!', 'nx': 1000, 'ny': 470}, None),
 # 3 myth ★
 (PS(Pp('maze', 160, 80, .02, 'drop', s=1.25), Pp('bit', 230, 150, .2, 'pop', s=.35, loop='boil'), Pp('cross', 760, 120, .75, 'pop', s=1.0), S('"tries every answer at once"', 560, 470, .3, 'c', 40)), 'The biggest myth'),
 (PS(*[Pp('qcoin', 40 + k * 210, 120, .05 + k * .07, 'drop', text='?', s=.8, loop='spin') for k in range(5)], S('look → ONE random answer', 260, 450, .55, 'r', 50)), None),
 (PS(Pp('waves', 80, 200, .05, 'slide', n=7, c='o', loop='bob'), B('INTERFERENCE', 330, 40, .4, 66), S('waves add up or cancel', 340, 470, .65, size=44)), None),
 (PS(Pp('waves', 40, 120, .05, 'slide', n=4, c='t', id='bad'), Pp('waves', 560, 300, .3, 'slide', n=5, c='o', s=1.2, loop='bob'), S('wrong answers cancel', 40, 330, .25, 'l', 40),
     S('right answer grows', 620, 120, .5, 'g', 44), Pp('check', 1020, 460, .75, 'pop', s=.8),
     moves=[{'id': 'bad', 'at': .45, 'fade': True, 'y': 40}]), None),
 (PS(S('faster at everything', 80, 150, .05, 'c', 54), Pp('cross', 760, 110, .25, 'pop', s=.9), S('only with the right recipe', 80, 400, .5, 'o', 54), Pp('check', 860, 360, .7, 'pop', s=.9)), None),
 # 4 colder than space
 (PS(Pp('fridge', 420, 20, .02, 'drop', s=.95, loop='boil'), S('?', 900, 160, .5, 'o', 90, 'pop')), 'Colder than space'),
 (PS(Pp('fridge', 60, 40, .02, 'fade', s=.85, loop='shake'), S('heat', 560, 80, .25, 'r', 52), S('vibration', 760, 230, .4, 'r', 52), S('stray signals', 600, 390, .55, 'r', 52), B('NOISE', 820, 520, .75, 70)), None),
 (PS(Pp('thermo', 160, 60, .02, 'drop', s=1.4), S('4 K', 460, 80, .2, size=56), S('0.1 K', 460, 250, .4, size=56), S('0.01 K', 460, 420, .6, 'o', 60), Pp('fridge', 860, 60, .1, 'fade', s=.75)), None),
 ({'type': 'vstat', 'kicker': 'QUBITS ≈ 0.01 K · DEEP SPACE ≈ 2.7 K', 'num': '≈270×', 'unit': 'COLDER', 'sub': 'than outer space', 'hi': 'outer space',
   'source': 'Dilution refrigerators run at ~10 millikelvin (MIT, Bluefors)', 'note': 'brrr!', 'sx': 760, 'sy': 560, 'nx': 120, 'ny': 590}, None),
 # 5 errors
 (PS(*[Pp('qcoin', 30 + k * 205, 140, .02 + k * .05, 'drop', text='Q', s=.8, loop='spin') for k in range(6)],
     *[Pp('cross', 90 + k * 410, 110, .45 + k * .1, 'pop', s=.55) for k in range(3)], Pp('clock', 1000, 420, .2, 'pop', s=.6)), 'Errors: the real battle'),
 (PS(*[Pp('qcoin', 60 + (k % 3) * 120, 60 + (k // 3) * 120, .02 + k * .04, 'pop', text='Q', s=.55) for k in range(9)], Pp('arrow', 460, 230, .45, 'fly', len=260, c='o'),
     Pp('qcoin', 800, 140, .6, 'pop', text='L', s=1.4, loop='boil'), Pp('check', 1050, 360, .8, 'pop', s=.6), S('one reliable "logical" qubit', 640, 500, .7, 'g', 40)), None),
 (PS(S('more qubits', 80, 200, .05, 'c', 58), Pp('arrow', 470, 210, .3, 'fly', len=260), S('more errors', 780, 200, .5, 'r', 58), Pp('cross', 520, 380, .7, 'pop', s=.7)), None),
 ({'type': 'vwords', 'kicker': 'GOOGLE WILLOW · 2024', 'words': ['bigger', 'groups', 'fewer', 'errors'], 'head': 'ERRORS WENT DOWN', 'hiword': 'DOWN'}, None),
 ({'type': 'vstat', 'kicker': 'QUANTUM ECHOES · OCTOBER 2025', 'num': '13,000×', 'unit': 'FASTER', 'sub': 'and other machines can check it', 'hi': 'check it',
   'source': 'Google Research, published in Nature', 'note': 'verifiable!', 'sx': 760, 'sy': 560, 'nx': 120, 'ny': 590}, None),
 # 6 useful for
 (PS(Pp('laptop', 60, 120, .02, 'drop', s=.65), S('browsing', 560, 80, .25, size=48), S('gaming', 560, 230, .4, size=48), S('ChatGPT', 560, 380, .55, size=48),
     Pp('cross', 900, 80, .35, 'pop', s=.55), Pp('cross', 900, 230, .5, 'pop', s=.55), Pp('cross', 900, 380, .65, 'pop', s=.55)), "What it's actually good for"),
 (PS(Pp('molecule', 40, 80, .05, 'pop', s=1.0, loop='spin'), Pp('battery', 500, 80, .3, 'drop', s=.9), Pp('book', 860, 100, .5, 'drop', s=1.0, c='g'),
     S('medicines', 60, 470, .2, 'o', 44), S('batteries', 470, 470, .4, 'g', 44), S('materials', 850, 470, .6, 'b', 44)), None),
 (PS(Pp('gear', 120, 100, .05, 'pop', s=1.0, loop='spin'), Pp('globe', 520, 90, .25, 'drop', s=1.0, loop='boil'), S('optimisation & simulation', 120, 470, .45, size=46),
     S('maybe: still debated', 760, 140, .7, 'l', 38)), None),
 (PS(Pp('lock', 460, 60, .05, 'drop', s=1.1, loop='shake'), B('ENCRYPTION', 330, 470, .5, 70)), None),
 # 7 bank ★
 (PS(Pp('phone', 80, 60, .02, 'drop', s=.95), Pp('lock', 380, 150, .25, 'pop', s=.7), Pp('envelope', 640, 180, .4, 'slide', s=1.0), S('UPI', 100, 500, .55, 'o', 48), S('WhatsApp', 640, 470, .65, 'g', 48)),
  'Your bank is already preparing'),
 (PS(Pp('chip', 80, 160, .05, 'drop', text='Q', s=.9, loop='boil'), Pp('arrow', 400, 260, .3, 'fly', len=300, c='o'), Pp('lock', 760, 140, .45, 'drop', s=.8, loop='shake'), Pp('cross', 820, 100, .75, 'pop', s=.7)), None),
 ({'type': 'vstat', 'kicker': 'WHEN COULD IT BREAK ENCRYPTION?', 'num': '2030s', 'unit': '?', 'sub': 'official estimates · exact date unknown', 'hi': 'unknown',
   'source': 'Industry summaries of official estimates (CSA, Palo Alto Networks)', 'note': 'no one knows!', 'sx': 760, 'sy': 560, 'nx': 120, 'ny': 590}, None),
 (PS(Pp('thief', 60, 160, .05, 'slide', s=1.2, loop='boil'), Pp('envelope', 500, 60, .25, 'fly', s=.6, id='e1'), Pp('envelope', 520, 240, .35, 'fly', s=.6, id='e2'),
     Pp('box', 820, 160, .45, 'drop', s=.8), S('LATER', 860, 120, .6, 'o', 48, 'pop'), S('harvest now, decrypt later', 300, 520, .7, size=42),
     moves=[{'id': 'e1', 'at': .55, 'x': 380, 'y': 220, 'scale': .5, 'fade': True}, {'id': 'e2', 'at': .62, 'x': 360, 'y': 60, 'scale': .5, 'fade': True}]), None),
 ({'type': 'vdoc', 'label': 'NIST · POST-QUANTUM PLAN', 'lines': ['Aug 2024: first post-quantum standards', 'After 2030: vulnerable encryption deprecated', 'After 2035: disallowed'],
   'hi': [0, 'first post-quantum standards'], 'circle': [1, '2030'], 'note': 'switching has begun', 'nx': 980, 'ny': 470}, None),
 (PS(Pp('phone', 120, 60, .02, 'drop', s=.95), Pp('gear', 480, 120, .2, 'pop', s=.7, loop='spin'), Pp('lock', 760, 120, .4, 'drop', s=.7), Pp('check', 960, 100, .6, 'pop', s=.6),
     S('quiet security updates', 440, 470, .5, 'g', 46)), None),
 # 8 India
 ({'type': 'vstat', 'kicker': 'NATIONAL QUANTUM MISSION · APPROVED 2023', 'num': '₹6,003', 'unit': 'CRORE', 'sub': 'over eight years', 'hi': 'eight years',
   'source': 'Government of India, approved 19 April 2023', 'note': 'India is in!', 'sx': 760, 'sy': 560, 'nx': 120, 'ny': 590}, 'What about India?'),
 (PS(Pp('chip', 120, 120, .05, 'drop', text='1000', s=1.0), Pp('calendar', 520, 120, .3, 'drop', text='2031', s=.95), B('UP TO 1,000 QUBITS', 300, 480, .55, 60)), None),
 (PS(Pp('chip', 140, 220, .05, 'drop', text='25', s=.75), S('QpiAI · Bengaluru', 60, 520, .25, 'o', 40), Pp('chip', 640, 80, .45, 'drop', text='105', s=1.35), S('Google Willow', 680, 520, .6, 'c', 40)), None),
 (PS(Pp('globe', 60, 120, .05, 'pop', s=1.0, loop='boil'), Pp('arrow', 420, 250, .3, 'fly', len=700, c='o'), S('1,000+ km quantum-secure links', 400, 470, .55, 'g', 46)), None),
 # 9 own one ★
 (PS(Pp('fridge', 80, 20, .02, 'drop', s=.85), S('at home?', 560, 160, .3, 'c', 60), Pp('cross', 640, 300, .6, 'pop', s=1.0)), 'Will you own one?'),
 (PS(Pp('laptop', 20, 220, .02, 'drop', s=.5), Pp('arrow', 350, 300, .2, 'fly', len=200), Pp('cloud', 560, 230, .35, 'pop', s=.75, loop='float'), Pp('arrow', 850, 300, .5, 'fly', len=160),
     Pp('fridge', 1020, 120, .6, 'drop', s=.55)), None),
 (PS(Pp('laptop', 120, 120, .02, 'drop', s=.75), S('real quantum chips online', 660, 160, .3, size=44), S('free tiers', 700, 320, .5, 'g', 52), Pp('star', 1000, 420, .7, 'pop', s=.7, loop='spin')), None),
 (PS(Pp('laptop', 60, 160, .02, 'drop', s=.7), S('+', 560, 260, .3, 'o', 90, 'pop'), Pp('fridge', 700, 60, .4, 'drop', s=.75), S('tools, not replacements', 300, 520, .65, 'g', 44)), None),
 # 10 close ★
 (PS(Pp('qcoin', 760, 100, .02, 'drop', text='Q', s=1.4, loop='boil'), S('not a faster laptop', 40, 120, .3, 'c', 40), S('not every answer at once', 40, 260, .45, 'c', 40),
     S('a different machine', 40, 400, .65, 'o', 44)), 'The bottom line'),
 (PS(Pp('magnifier', 440, 80, .05, 'pop', s=1.0, loop='wiggle'), S('HYPE: sometimes real', 60, 470, .3, 'g', 44), S('HYPE: often overblown', 640, 470, .55, 'r', 44)), None),
 (PS(B('WHICH PROBLEM FIRST? 👇', 160, 60, .05, 60), S('new medicines', 120, 300, .3, 'o', 44), S('climate', 520, 300, .45, 'g', 44), S('new materials', 800, 300, .6, 'b', 44)), None),
 ({'type': 'end', 'sub': 'More tech, decoded.'}, None),
]
assert len(V) == len(e['beats']) == 46, (len(V), len(e['beats']))
for b, (v, ch) in zip(e['beats'], V):
    b.pop('chapter', None)
    if ch: b['chapter'] = ch
    b['v'] = v
e['host_beats'] = [0, 2, 3, 10, 11, 14, 28, 29, 31, 33, 38, 40, 41, 42, 43, 44, 45]
f.write_text(json.dumps(e, indent=1, ensure_ascii=False))
print('visuals written')
