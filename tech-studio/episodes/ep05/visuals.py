"""Visual spec for ep05 (writes the 'v' of each beat into long.json). Run: python3 episodes/ep05/visuals.py"""
import json
from pathlib import Path
f = Path(__file__).with_name('long.json'); e = json.loads(f.read_text())

def sc(img, cam, **k):
    d = {'type': 'scene', 'img': img, 'cam': cam}; d.update(k); return d

def T(text, x, y, at=.3, kind='note', size=None):
    d = dict(text=text, x=x, y=y, at=at, kind=kind)
    if size: d['size'] = size
    return d

HAB = ['Give it context', 'Let it say "I don\'t know"', 'Check anything that matters', 'Ask for step by step']
V = [
 sc('hook', [0.5, 0.45, 1.0], chapter='No plan, one word at a time', tags=[T('"Write a poem about chai"', 40, 40, .15, 'bubble')]),
 sc('hook', [0.55, 0.3, 1.25], tags=[T('Chai', 520, 330, .35, 'ok'), T('is', 700, 330, .5, 'ok'), T('warm', 820, 330, .65, 'ok'), T('…', 1010, 330, .8, 'ok')]),
 sc('hook', [0.5, 0.45, 1.05], tags=[T('≈ 1 BILLION', 640, 360, .2, 'big', 100), T('people use it every week', 650, 480, .35)]),
 sc('hook', [0.78, 0.5, 1.35], tags=[T('How?', 560, 380, .35, 'big', 130)]),
 sc('tokens', [0.5, 0.5, 1.0], chapter='Words become tokens', tags=[T('TOKENS', 60, 40, .3, 'big', 120)]),
 sc('tokens', [0.45, 0.6, 1.2], tags=[T('100 tokens ≈ 75 words', 380, 40, .5, 'note', 56)]),
 sc('tokens', [0.5, 0.55, 1.4], tags=[T('every token → a number', 60, 60, .3, 'note', 52)]),
 sc('tokens', [0.88, 0.6, 1.7], tags=[T('"strawberry" has 2 R\'s!', 60, 60, .4, 'bubble')]),
 sc('tokens', [0.88, 0.6, 1.7], tags=[T('straw', 60, 80, .35, 'ok', 64), T('berry', 360, 80, .5, 'ok', 64), T('= just numbers', 60, 230, .7)]),
 sc('tokens', [0.8, 0.6, 1.4], tags=[T('s t r a w b e r r y', 60, 60, .3, 'note', 60), T('3 R\'s', 60, 190, .6, 'bad', 60)]),
 sc('tokens', [0.5, 0.5, 1.0], tags=[T('your question = a row of numbers', 60, 60, .3, 'note', 50)]),
 sc('dice', [0.7, 0.5, 1.1], chapter='The guessing game', tags=[T('What comes next?', 60, 60, .25, 'big', 90)]),
 sc('dice', [0.62, 0.55, 1.0], tags=[T('"I\'ll be there in …"', 60, 40, .2, 'bubble'), T('5', 660, 40, .55, 'ok'), T('10', 760, 40, .65, 'ok'), T('a', 880, 40, .75, 'ok')]),
 sc('dice', [0.72, 0.5, 1.15], tags=[T('a probability for every option', 60, 40, .3)]),
 sc('dice', [0.85, 0.4, 1.4], tags=[T('pick → add → repeat', 60, 60, .3, 'big', 80)]),
 sc('dice', [0.2, 0.5, 1.5], tags=[T('Same question', 60, 40, .2), T('Answer A', 60, 150, .45, 'ok'), T('Answer B', 300, 150, .6, 'ok')]),
 sc('attention', [0.5, 0.5, 1.0], chapter='It re-reads everything', tags=[T('looks back at EVERYTHING', 60, 40, .4, 'note', 50)]),
 sc('attention', [0.55, 0.5, 1.3], tags=[T('"it"', 100, 60, .3, 'ok', 56), T('"that"', 300, 60, .5, 'ok', 56)]),
 sc('attention', [0.6, 0.5, 1.15], tags=[T('ATTENTION', 60, 30, .25, 'big', 110), T('Google · 2017 · "Attention Is All You Need"', 60, 170, .45, 'note', 34),
                                          T('GPT = Generative Pre-trained Transformer', 60, 260, .7, 'note', 34)]),
 sc('attention', [0.6, 0.5, 1.25], tags=[T('I dropped my laptop and now it won\'t start', 60, 40, .15, 'bubble')]),
 sc('attention', [0.15, 0.5, 1.35], tags=[T('CONTEXT WINDOW', 60, 40, .3, 'big', 80), T('the oldest messages fade', 60, 170, .55)]),
 sc('library', [0.5, 0.5, 1.0], chapter='How it learned', tags=[T('It learned by reading', 60, 40, .3, 'note', 56)]),
 sc('library', [0.3, 0.35, 1.25], tags=[T('books · websites · code', 60, 40, .3), T('next word hidden: ___', 60, 150, .6, 'ok')]),
 sc('library', [0.5, 0.45, 1.3], tags=[T('The capital of India is ___', 60, 40, .15), T('Mumbai ✗', 60, 150, .45, 'bad'), T('New Delhi ✓', 330, 150, .7, 'ok')]),
 sc('library', [0.93, 0.65, 1.8], tags=[T('175,000,000,000', 60, 40, .35, 'big', 110), T('knobs (parameters) in GPT-3, 2020', 60, 190, .55)]),
 sc('library', [0.5, 0.45, 1.05], tags=[T('grammar', 60, 40, .3, 'ok'), T('facts', 300, 40, .45, 'ok'), T('style', 490, 40, .6, 'ok'), T('reasoning patterns', 680, 40, .75, 'ok')]),
 sc('rlhf', [0.15, 0.5, 1.5], chapter='From parrot to assistant', tags=[T('A very well-read parrot', 60, 40, .35, 'note', 52)]),
 sc('rlhf', [0.75, 0.45, 1.3], tags=[T('Real people rank answers', 60, 40, .3, 'note', 52)]),
 sc('rlhf', [0.55, 0.45, 1.1], tags=[T('RLHF', 60, 30, .2, 'big', 120), T('reinforcement learning from human feedback', 60, 180, .4, 'note', 36)]),
 sc('rlhf', [0.74, 0.55, 1.6], tags=[T('1.3B model 🥇', 60, 40, .35, 'ok', 56), T('beat 175B GPT-3', 60, 150, .6, 'note', 48)]),
 sc('exam', [0.5, 0.5, 1.0], chapter='Why it makes things up', tags=[T('likely ≠ true', 60, 40, .4, 'big', 100)]),
 sc('exam', [0.5, 0.4, 1.25], tags=[T('"Max\'s birthday is 12 March!"', 60, 40, .3, 'bubble'), T('HALLUCINATION', 60, 170, .7, 'bad', 60)]),
 sc('exam', [0.5, 0.68, 1.45], tags=[T('"I don\'t know" = 0 points', 60, 40, .25), T('Lucky guess = +1', 60, 150, .55, 'ok')]),
 sc('exam', [0.5, 0.5, 1.1], tags=[T('Guessing gets rewarded', 60, 40, .4, 'bad', 56)]),
 sc('exam', [0.4, 0.15, 1.6], tags=[T('dates', 60, 60, .25), T('small companies', 250, 60, .45), T('rare quotes', 620, 60, .65)]),
 sc('scale', [0.5, 0.45, 1.0], chapter='Does it understand?', tags=[T('Autocomplete… or understanding?', 60, 40, .3, 'note', 50)]),
 sc('scale', [0.5, 0.55, 1.3], tags=[T('Researchers disagree', 60, 40, .15, 'bad', 50), T('no memory of your life', 60, 150, .45), T('no experience of the world', 60, 250, .65)]),
 sc('library', [0.5, 0.45, 1.0], tags=[T('explain code', 60, 40, .35, 'ok'), T('translate', 330, 40, .5, 'ok'), T('solve new problems', 560, 40, .65, 'ok')]),
 sc('library', [0.5, 0.45, 1.12], tags=[T('An incredibly well-read prediction machine.', 60, 40, .15, 'quote'), T('Powerful, but not a source of truth', 60, 260, .5, 'bad', 44)]),
 {'type': 'slam', 'text': '4 habits for better answers', 'chapter': 'Get better answers'},
 {'type': 'checklist', 'title': '4 HABITS FOR BETTER ANSWERS', 'suffix': '', 'items': HAB, 'upto': 0, 'detail': '"Write a polite email to my manager asking for Friday off"'},
 {'type': 'checklist', 'title': '4 HABITS FOR BETTER ANSWERS', 'suffix': '', 'items': HAB, 'upto': 1, 'detail': '"If you\'re not sure, say so."'},
 {'type': 'checklist', 'title': '4 HABITS FOR BETTER ANSWERS', 'suffix': '', 'items': HAB, 'upto': 2, 'detail': 'Ask for sources, then open them'},
 {'type': 'checklist', 'title': '4 HABITS FOR BETTER ANSWERS', 'suffix': '', 'items': HAB, 'upto': 3, 'detail': 'More steps = more text to build on'},
 sc('hook', [0.5, 0.45, 1.0], chapter='The bottom line', tags=[T('one token at a time', 60, 40, .4, 'big', 90)]),
 sc('hook', [0.3, 0.45, 1.3], tags=[T('Never switch your own brain off.', 760, 40, .2, 'quote')]),
 {'type': 'callback', 'title': 'A Webpage Can Hijack Your AI Agent', 'dur': '6:46'},
 {'type': 'end', 'sub': 'More tech, decoded.'},
]
assert len(V) == len(e['beats']) == 48, (len(V), len(e['beats']))
for b, v in zip(e['beats'], V):
    v = dict(v); ch = v.pop('chapter', None)
    b.pop('chapter', None)
    if ch: b['chapter'] = ch
    b['v'] = v
e['host_beats'] = [39, 40, 41, 42, 43, 45, 46, 47]
f.write_text(json.dumps(e, indent=1))
print('visuals written')
