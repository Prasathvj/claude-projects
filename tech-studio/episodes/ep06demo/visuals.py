"""ep06 OPENING DEMO in the MIXED style (owner review 2026-11-23): old pop cards/counters + papercut props/photo prints +
Vox clippings/boards + real logos/exact icons, every element timed to a spoken word (tools/kit_mix.py).
Stage 1320x760. Run: python3 episodes/ep06demo/visuals.py && STYLE=paper THEME=cream GRID=plain python3 tools/hf_ep06demo_long.py"""
import json
from pathlib import Path
f = Path(__file__).with_name('long.json'); e = json.loads(f.read_text())

def M(*els, acts=()):
    return {'type': 'mix', 'els': list(els), 'acts': list(acts)}

def X(k, at, x, y, **o):
    d = dict(k=k, at=at, x=x, y=y); d.update(o); return d

V = [
 # 0  hook: chip (stamp-sized) in 5 min vs supercomputer 10^25 years
 (M(X('prop', 'chip', 40, 70, p='chip', text='Willow', s=.95, id='chip', **{'in': 'drop'}),
    X('logo', 'chip', 250, 290, ref='logos:google-icon', size=64, paper=True, id='g'),
    X('tag', 'postage', 20, 390, text='≈ size of a postage stamp', bg='#FFFAF2', color='#2A2018', size=30, id='st'),
    X('card', 'five', 30, 480, icon='ph:clock-countdown-fill', label='QUANTUM CHIP', big='0 MIN', w=420, id='min', **{'in': 'fly'}),
    X('photo', 'fastest', 700, 30, name='frontier.jpg', w=520, rot=3, id='fr', **{'in': 'slide'}),
    X('tag', 'supercomputers', 760, 420, text='Frontier: one of the fastest supercomputers', size=26, id='frt'),
    X('card', 'ten', 520, 520, icon='ph:hourglass-high-fill', label='SUPERCOMPUTER', big='10 *septillion* YEARS', bcolor='#2A2018', bsize=64, id='yrs', **{'in': 'slam'}),
    acts=[{'do': 'count', 'id': 'min', 'at': 'minutes', 'values': ['1 MIN', '2 MIN', '3 MIN', '4 MIN', '5 MIN'], 'dt': .12},
          {'do': 'shake', 'id': 'yrs', 'at': 'years'}]), 'Ten septillion years'),
 # 1  one followed by 25 zeros; universe
 (M(X('big', 'one', 40, 60, text='1', size=150, color='#F87736', id='one'),
    X('big', 'twenty', 140, 75, text='0000000000000000000000000', size=60, id='zeros', **{'in': 'left'}),
    X('tag', 'zeros', 150, 170, text='25 zeros', bg='#F87736', size=34, id='z25'),
    X('photo', 'universe', 40, 280, name='deepfield.jpg', w=430, rot=-4, crop=[.15, .15, .85, .85], id='udf', **{'in': 'drop'}),
    X('card', 'universe', 560, 330, icon='ph:planet-fill', label='AGE OF THE UNIVERSE', big='13.8 *billion* yrs', id='age'),
    X('tag', 'longer', 560, 560, text='10 septillion yrs ≈ 700 trillion × longer', bg='#E0471C', size=34, id='lg', **{'in': 'slam'})), None),
 # 2  Google's Willow; sounds like magic; much of what you hear is wrong
 (M(X('logo', "google's", 40, 40, ref='logos:google', size=300, id='gl', **{'in': 'drop'}),
    X('prop', 'willow', 90, 200, p='chip', text='Willow', s=1.05, id='ch'),
    X('tag', 'quantum', 60, 560, text='a quantum computer', size=38, id='qc'),
    X('icon', 'magic', 640, 60, ref='ph:magic-wand-fill', size=170, color='#7A5CFF', id='mw'),
    X('icon', 'magic', 830, 40, ref='ph:sparkle-fill', size=80, color='#F87736', id='sp1'),
    X('icon', 'magic', 600, 260, ref='ph:sparkle-fill', size=60, color='#F87736', id='sp2'),
    X('clip', 'hear', 560, 330, by='WHAT YOU HEAR', text='"Quantum computers will replace your laptop"', hi='replace your laptop', w=700, id='cl'),
    X('stamp', 'wrong', 760, 520, text='WRONG', size=100, id='wr', **{'in': 'slam'}),
    acts=[{'do': 'spin', 'id': 'sp1', 'at': 'magic', 'deg': 180, 'd': 3}]), None),
 # 3  what we'll decode: 4 exact icons, one per promise
 (M(X('big', 'decode', 40, 20, text="Let's *decode*", size=80, id='dh'),
    X('icon', 'really', 40, 170, ref='tabler:atom', size=150, color='#7A5CFF', paper=True, id='i1'),
    X('tag', 'really', 30, 410, text='what it really is', size=30, id='t1'),
    X('icon', 'colder', 360, 170, ref='ph:snowflake-bold', size=150, color='#1C7ED6', paper=True, id='i2'),
    X('tag', 'colder', 330, 410, text='colder than space', size=30, id='t2'),
    X('icon', 'can', 680, 170, ref='ph:check-fat-fill', size=80, color='#2F9E44', id='i3a'),
    X('icon', "can't", 780, 250, ref='ph:x-circle-fill', size=90, color='#E0471C', id='i3b'),
    X('tag', "can't", 640, 410, text="can & can't do", size=30, id='t3'),
    X('icon', 'bank', 1000, 170, ref='ph:bank-fill', size=150, color='#2A2018', paper=True, id='i4'),
    X('tag', 'bank', 990, 410, text='banks prepare', size=30, bg='#E0471C', id='t4')), None),
 # 4  bits: tiny switches 0 or 1
 (M(X('icon', 'computer', 40, 60, ref='ph:laptop-fill', size=260, color='#2A2018', id='lap'),
    X('icon', 'computer', 330, 150, ref='ph:device-mobile-fill', size=130, color='#2A2018', id='mob'),
    X('big', 'bits', 560, 40, text='BITS', size=130, color='#F87736', id='bits', **{'in': 'slam'}),
    X('prop', 'switches', 560, 260, p='switch', s=.95, on=False, id='sw0'),
    X('prop', 'switches', 860, 260, p='switch', s=.95, on=True, id='sw1'),
    X('big', 'zero', 620, 560, text='0 = off', size=64, id='z'),
    X('big', 'one', 910, 560, text='*1* = on', size=64, id='o')), 'Bits vs qubits'),
 # 5  every photo / video / message = billions of switches flipping
 (M(X('icon', 'photo', 40, 40, ref='ph:image-fill', size=150, color='#2F9E44', paper=True, id='ph'),
    X('icon', 'video', 300, 40, ref='ph:video-camera-fill', size=150, color='#E0471C', paper=True, id='vd'),
    X('logo', 'message', 560, 40, ref='logos:whatsapp-icon', size=150, paper=True, id='wa'),
    X('card', 'billions', 40, 330, label='SWITCHES', big='0', w=700, id='cnt', **{'in': 'fly'}),
    X('big', 'flipping', 620, 340, text='0110100101101001', size=72, color='#2A2018', id='bin', **{'in': 'fade'}),
    X('tag', 'fast', 640, 470, text='billions of flips every second', bg='#F87736', size=34, id='fs'),
    acts=[{'do': 'count', 'id': 'cnt', 'at': 'billions', 'values': ['1,000', '1,000,000', '1,000,000,000', 'BILLIONS'], 'dt': .25},
          {'do': 'shake', 'id': 'bin', 'at': 'fast'}]), None),
 # 6  qubits: mix of 0 and 1 at once = superposition
 (M(X('prop', 'qubits', 60, 60, p='qcoin', text='Q', s=1.3, id='q'),
    X('tag', 'qubits', 70, 420, text='QUBIT', size=44, bg='#7A5CFF', id='qt'),
    X('big', 'zero', 560, 60, text='0', size=180, color='#2A2018', id='z0', **{'in': 'left'}),
    X('big', 'mix', 700, 90, text='+', size=140, color='#8C6B5A', id='pl'),
    X('big', 'one', 860, 60, text='*1*', size=180, id='o1', **{'in': 'slide'}),
    X('tag', 'same', 600, 300, text='both at the same time', size=38, id='bt'),
    X('big', 'superposition', 470, 430, text='SUPER*POSITION*', size=110, id='sp', **{'in': 'slam'}),
    acts=[{'do': 'spin', 'id': 'q', 'at': 'qubits', 'deg': 720, 'd': 6}, {'do': 'bob', 'id': 'z0', 'at': 'mix', 'n': 7}, {'do': 'bob', 'id': 'o1', 'at': 'mix', 'n': 7}]), None),
 # 7  coin analogy: flat coin (bit) vs spinning coin (qubit) -> look -> lands
 (M(X('icon', 'flat', 60, 80, ref='ph:coin-vertical-fill', size=190, color='#C9A57A', paper=True, id='flat'),
    X('tag', 'heads', 40, 380, text='BIT: heads OR tails', size=36, id='bt'),
    X('prop', 'spinning', 620, 40, p='qcoin', text='?', s=1.2, id='spin'),
    X('tag', 'spinning', 600, 380, text='QUBIT: still spinning', size=36, bg='#7A5CFF', id='qt'),
    X('icon', 'look', 1000, 120, ref='ph:eye-fill', size=140, color='#2A2018', id='eye'),
    X('tag', 'land', 920, 520, text='look → it lands on 1', bg='#F87736', size=36, id='ld'),
    acts=[{'do': 'spin', 'id': 'spin', 'at': 'spinning', 'deg': 1080, 'd': 4.2}, {'do': 'ring', 'id': 'eye', 'at': 'look'}]), None),
 # 8  entanglement: two linked coins
 (M(X('prop', 'qubits', 60, 80, p='qcoin', text='Q', s=1.0, id='a'),
    X('prop', 'linked', 880, 80, p='qcoin', text='Q', s=1.0, id='b'),
    X('icon', 'linked', 520, 130, ref='ph:link-bold', size=220, color='#F87736', id='ln'),
    X('icon', 'instantly', 560, 370, ref='ph:lightning-fill', size=120, color='#F5B400', id='lt'),
    X('big', 'entanglement', 300, 520, text='ENTANGLE*MENT*', size=110, id='en', **{'in': 'slam'}),
    acts=[{'do': 'shake', 'id': 'ln', 'at': 'instantly'}]), None),
 # 9  2^n: bars explode; Vox-style clipping for the 300-qubit fact
 (M(X('bars', 'two', 40, 40, w=760, id='bars', rows=[['2 qubits → 4', .012, '#7A5CFF'], ['10 qubits → 1,024', .08, '#F87736'], ['300 qubits → more than atoms in the universe', 1.0, '#E0471C']],
      gap=1.6, **{'in': 'fade'}),
    X('icon', 'atoms', 880, 70, ref='tabler:atom', size=230, color='#7A5CFF', paper=True, id='at'),
    X('clip', 'universe', 820, 400, by='THE MATHS (2 TO THE POWER OF n)', text='2³⁰⁰ ≈ 10⁹⁰ > 10⁸⁰ atoms in the observable universe', hi='10⁸⁰ atoms', w=480, id='cl')), None),
]

for b, (v, ch) in zip(e['beats'], V):
    b['v'] = v
    if ch:
        b['chapter'] = ch
    else:
        b.pop('chapter', None)
f.write_text(json.dumps(e, indent=1, ensure_ascii=False))
print('beats', len(V))
