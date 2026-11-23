"""ep05 visual spec in the OLD card style (owner, 2026-11-23: no images). Writes each beat's 'v' into long.json.
Run: python3 episodes/ep05/visuals_cards.py"""
import json
from pathlib import Path
f = Path(__file__).with_name('long.json'); e = json.loads(f.read_text())

HAB = ['Give it context', 'Let it say "I don\'t know"', 'Check anything that matters', 'Ask for step by step']
V = [
 # 1 hook (Max)
 ({'type': 'chat', 'label': 'CHATGPT · ILLUSTRATION', 'msgs': [{'from': 'you', 'text': 'Write a poem about chai'}, {'from': 'agent', 'text': 'Chai…'}]}, 'No plan, one word at a time'),
 ({'type': 'loop', 'steps': ['Pick one piece', 'Add it', 'Look again', 'Pick the next'], 'upto': 3}, None),
 ({'type': 'counter', 'value': '1', 'prefix': '≈ ', 'suffix': 'BILLION', 'label': 'PEOPLE USE CHATGPT EVERY WEEK', 'sub': 'emails · <b>code</b> · homework', 'src': 'Source: OpenAI, Sept 2026'}, None),
 ({'type': 'slam', 'text': "Let's open the box"}, None),
 # 2 tokens
 ({'type': 'split', 'left': {'icon': 'doc', 'title': 'Words', 'body': 'What you see'}, 'right': {'icon': 'code', 'title': 'Tokens', 'body': 'What it reads'}, 'merge': 'It reads TOKENS'}, 'Words become tokens'),
 ({'type': 'code', 'file': 'tokens · ILLUSTRATION', 'label': 'ONE SENTENCE, CUT INTO TOKENS', 'lines': [{'t': 'ChatGPT is unbelievable', 'c': 'text'}, {'t': '[Chat] [G] [PT] [ is] [ un] [believ] [able]', 'c': 'cyan'}, {'t': '≈ 100 tokens ≈ 75 English words', 'c': 'hot'}]}, None),
 ({'type': 'code', 'file': 'numbers · EXAMPLE', 'label': 'EVERY TOKEN BECOMES A NUMBER', 'lines': [{'t': '[Chat]  →  1201', 'c': 'cyan'}, {'t': '[G]     →  38', 'c': 'cyan'}, {'t': '[PT]    →  2507', 'c': 'cyan'}, {'t': '(example numbers)', 'c': 'dim'}]}, None),
 ({'type': 'chat', 'label': 'A FAMOUS FAIL · ILLUSTRATION', 'msgs': [{'from': 'you', 'text': 'How many R\'s in "strawberry"?'}, {'from': 'agent', 'text': 'There are 2 R\'s.'}]}, None),
 ({'type': 'split', 'left': {'icon': 'doc', 'title': 's-t-r-a-w-b-e-r-r-y', 'body': 'You see 10 letters'}, 'right': {'icon': 'code', 'title': '[straw] [berry]', 'body': 'It sees 2 numbers'}, 'bad': 'right'}, None),
 ({'type': 'icons', 'title': 'WHY IT FAILED', 'items': [{'icon': 'code', 'label': 'Letters hidden in tokens'}, {'icon': 'brain', 'label': 'Counting is hard'}, {'icon': 'check', 'label': 'Step-by-step models fix it'}]}, None),
 ({'type': 'slam', 'text': 'A long row of numbers'}, None),
 # 3 guessing game
 ({'type': 'slam', 'text': 'What comes next?'}, 'The guessing game'),
 ({'type': 'chat', 'label': 'YOUR PHONE KEYBOARD · ILLUSTRATION', 'msgs': [{'from': 'you', 'text': "I'll be there in"}, {'from': 'agent', 'text': '5 · 10 · a few'}]}, None),
 ({'type': 'bars', 'title': 'NEXT TOKEN PROBABILITIES · ILLUSTRATION', 'bars': [['minutes', 62, '#F87736', '62%'], ['mins', 21, '#FFC24A', '21%'], ['hours', 9, '#55C2FF', '9%']], 'src': 'Illustrative numbers'}, None),
 ({'type': 'loop', 'steps': ['Predict', 'Pick', 'Add', 'Repeat'], 'upto': 3}, None),
 ({'type': 'split', 'left': {'icon': 'chat', 'title': 'Answer A', 'body': 'Same question'}, 'right': {'icon': 'chat', 'title': 'Answer B', 'body': 'Different words'}, 'merge': 'It rolls the dice a little'}, None),
 # 4 attention
 ({'type': 'slam', 'text': 'It re-reads everything'}, 'It re-reads everything'),
 ({'type': 'stack', 'title': 'BEFORE EVERY NEW TOKEN, IT LOOKS BACK AT', 'items': ['Your question', 'Its own earlier words', 'The whole conversation']}, None),
 ({'type': 'quote', 'text': 'Attention Is All You Need', 'who': 'Google researchers', 'when': '2017 · the T in GPT = Transformer'}, None),
 ({'type': 'chat', 'label': 'ATTENTION · ILLUSTRATION', 'msgs': [{'from': 'you', 'text': "I dropped my laptop and now it won't start"}, {'from': 'agent', 'text': '"it" → laptop ✓   (not "I")'}]}, None),
 ({'type': 'doc', 'label': 'CONTEXT WINDOW · ILLUSTRATION', 'title': 'A very long chat', 'lines': ['Message 1: my name is Priya…', 'Message 2: …', '… 300 messages later …'], 'hi': 'The earliest details can drop out', 'stamp': 'LIMIT'}, None),
 # 5 how it learned (Max)
 ({'type': 'slam', 'text': 'It learned by reading'}, 'How it learned'),
 ({'type': 'icons', 'title': 'TRAINING TEXT', 'items': [{'icon': 'doc', 'label': 'Books'}, {'icon': 'globe', 'label': 'Websites'}, {'icon': 'code', 'label': 'Code'}]}, None),
 ({'type': 'loop', 'steps': ['Hide next word', 'Guess', 'Check', 'Adjust'], 'upto': 3}, None),
 ({'type': 'counter', 'value': '175,000,000,000', 'label': 'GPT-3 PARAMETERS (2020)', 'sub': 'adjustable "knobs"', 'src': 'Source: Brown et al., 2020'}, None),
 ({'type': 'icons', 'title': 'WHAT IT PICKS UP', 'items': [{'icon': 'doc', 'label': 'Grammar'}, {'icon': 'globe', 'label': 'Facts'}, {'icon': 'chat', 'label': 'Styles'}, {'icon': 'brain', 'label': 'Reasoning patterns'}]}, None),
 # 6 parrot to assistant
 ({'type': 'chat', 'label': 'A RAW MODEL · ILLUSTRATION', 'msgs': [{'from': 'you', 'text': 'What is the capital of India?'}, {'from': 'agent', 'text': 'What is the capital of France? What is the capital of…'}]}, 'From parrot to assistant'),
 ({'type': 'rank', 'title': 'PEOPLE RANK THE ANSWERS', 'items': [['#1', 'Clear, correct, helpful', 'hi'], ['#2', 'Correct but rambling', ''], ['#3', 'Wrong or off-topic', '']], 'source': 'Illustration'}, None),
 ({'type': 'flow', 'nodes': [{'icon': 'user', 'label': 'People rank'}, {'icon': 'brain', 'label': 'Reward model'}, {'icon': 'agent', 'label': 'Better answers'}], 'end': 'RLHF'}, None),
 ({'type': 'bars', 'title': 'OPENAI STUDY, 2022 · MODEL SIZE (PARAMETERS)', 'bars': [['InstructGPT ★ preferred', 1.3, '#3DDC97', '1.3B'], ['GPT-3', 175, '#C9A98E', '175B']], 'src': 'Source: OpenAI, Training language models to follow instructions (2022)'}, None),
 # 7 hallucination (Max)
 ({'type': 'split', 'left': {'icon': 'check', 'title': 'Likely', 'body': 'What it aims for'}, 'right': {'icon': 'warn', 'title': 'True', 'body': 'Not guaranteed'}, 'bad': 'right'}, 'Why it makes things up'),
 ({'type': 'chat', 'label': 'HALLUCINATION · ILLUSTRATION', 'msgs': [{'from': 'you', 'text': "When is Max's birthday?"}, {'from': 'agent', 'text': "Max's birthday is 12 March! (made up)"}]}, None),
 ({'type': 'split', 'left': {'icon': 'x', 'title': '"I don\'t know"', 'body': '0 points'}, 'right': {'icon': 'check', 'title': 'Lucky guess', 'body': '+1 point'}, 'merge': 'Guessing looks smarter'}, None),
 ({'type': 'doc', 'label': 'AI TEST SCORECARD · ILLUSTRATION', 'title': 'Graded on accuracy only', 'lines': ['Honest "not sure" = wrong', 'Confident guess = maybe right'], 'hi': 'Rewards guessing', 'stamp': 'FLAWED'}, None),
 ({'type': 'nolist', 'items': ['Specific dates', 'Small company details', 'Quotes from non-famous people']}, None),
 # 8 understand?
 ({'type': 'split', 'left': {'icon': 'code', 'title': 'Fancy autocomplete?', 'body': 'Just predicting'}, 'right': {'icon': 'brain', 'title': 'Understanding?', 'body': 'Deep patterns'}}, 'Does it understand?'),
 ({'type': 'nolist', 'items': ['No memory of your life', 'No experience of the world']}, None),
 ({'type': 'icons', 'title': 'YET IT CAN', 'items': [{'icon': 'code', 'label': 'Explain code'}, {'icon': 'globe', 'label': 'Translate'}, {'icon': 'brain', 'label': 'Solve new problems'}]}, None),
 ({'type': 'quote', 'text': 'An incredibly well-read prediction machine.', 'who': 'Powerful, but not a source of truth on its own', 'when': ''}, None),
 # 9 habits (Max)
 ({'type': 'slam', 'text': '4 habits for better answers'}, 'Get better answers'),
 ({'type': 'checklist', 'title': '4 HABITS FOR BETTER ANSWERS', 'suffix': '', 'items': HAB, 'upto': 0, 'detail': '"Write a polite email to my manager asking for Friday off"'}, None),
 ({'type': 'checklist', 'title': '4 HABITS FOR BETTER ANSWERS', 'suffix': '', 'items': HAB, 'upto': 1, 'detail': '"If you\'re not sure, say so."'}, None),
 ({'type': 'checklist', 'title': '4 HABITS FOR BETTER ANSWERS', 'suffix': '', 'items': HAB, 'upto': 2, 'detail': 'Ask for sources, then open them'}, None),
 ({'type': 'checklist', 'title': '4 HABITS FOR BETTER ANSWERS', 'suffix': '', 'items': HAB, 'upto': 3, 'detail': 'More steps = more text to build on'}, None),
 # 10 close (Max)
 ({'type': 'loop', 'steps': ['Predict', 'Pick', 'Add', 'Repeat'], 'upto': 3}, 'The bottom line'),
 ({'type': 'quote', 'text': 'Never switch your own brain off.', 'who': 'TechDecoded', 'when': ''}, None),
 ({'type': 'callback', 'title': 'A Webpage Can Hijack Your AI Agent', 'dur': '6:46'}, None),
 ({'type': 'end', 'sub': 'More tech, decoded.'}, None),
]
assert len(V) == len(e['beats']) == 48, (len(V), len(e['beats']))
for b, (v, ch) in zip(e['beats'], V):
    b.pop('chapter', None)
    if ch: b['chapter'] = ch
    b['v'] = v
e['host_beats'] = [0, 1, 2, 3, 21, 22, 30, 31, 39, 40, 41, 42, 43, 44, 45, 46, 47]
f.write_text(json.dumps(e, indent=1))
print('card visuals written')
