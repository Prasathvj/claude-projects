"""ep07 "Is Your Phone Secretly Listening to You?" in the MIXED style (standard since ep06 v2): kit_mix beats, one exact
visual per line, word-timed. Run: python3 episodes/ep07/visuals_mix.py, then
STYLE=paper THEME=cream GRID=plain python3 tools/hf_ep07_long.py"""
import json
from pathlib import Path
HERE = Path(__file__).parent
f = HERE / 'long.json'; e = json.loads(f.read_text())

def M(*els, acts=()):
    return {'type': 'mix', 'els': list(els), 'acts': list(acts)}
def X(k, at, x, y, **o):
    d = dict(k=k, at=at, x=x, y=y); d.update(o); return d
def ic(at, x, y, ref, size=150, color='#2A2018', paper=True, **o):
    return X('icon', at, x, y, ref=ref, size=size, color=color, paper=paper, **o)
def lg(at, x, y, ref, size=150, paper=True, **o):
    return X('logo', at, x, y, ref=ref, size=size, paper=paper, **o)
def tg(at, x, y, text, bg='#2A2018', size=36, **o):
    return X('tag', at, x, y, text=text, bg=bg, size=size, **o)
def bg_(at, x, y, text, size=96, **o):
    return X('big', at, x, y, text=text, size=size, **o)
def cd(at, x, y, big, label='', icon=None, color='#F87736', w=None, **o):
    d = dict(big=big, label=label, color=color, **o)
    if icon: d['icon'] = icon
    if w: d['w'] = w
    return X('card', at, x, y, **d)
SL = {'in': 'slam'}; SD = {'in': 'slide'}; DR = {'in': 'drop'}; FL = {'in': 'fly'}; LF = {'in': 'left'}
G, R, O, D, P, BL, Y = '#2F9E44', '#E0471C', '#F87736', '#2A2018', '#7A5CFF', '#1C7ED6', '#F5B400'

V = [
 # 0 hook ★
 (M(ic('dinner', 40, 60, 'ph:fork-knife-fill', 150, O), ic('friend', 260, 60, 'ph:users-three-fill', 150, D),
    ic('shoes', 480, 40, 'ph:sneaker-fill', 200, R), tg('never', 40, 330, 'never searched', bg=G),
    lg('instagram', 760, 40, 'logos:instagram-icon', 160), *[tg('ads', 760 + (k % 2) * 220, 280 + k * 70, 'running shoe AD', bg=O, size=28, id=f'a{k}', **DR) for k in range(4)]), 'The dinner conversation'),
 # 1 feels like proof
 (M(ic('proof', 60, 60, 'ph:device-mobile-fill', 230, D), ic('heard', 360, 60, 'ph:ear-fill', 200, R),
    bg_('heard', 40, 420, 'Your phone *heard* you?', 96, **SL)), None),
 # 2 millions believe: tape, test words
 (M(ic('millions', 40, 40, 'ph:users-four-fill', 170, D), cd('millions', 300, 60, 'MILLIONS', 'BELIEVE IT', 'ph:megaphone-fill', R),
    ic('tape', 60, 340, 'ph:microphone-slash-fill', 160, R), tg('tape', 260, 380, 'tape over the mic', bg=D),
    ic('product', 700, 300, 'ph:chat-circle-dots-fill', 170, O), tg('product', 700, 520, '"…running shoes!"', bg=O)), None),
 # 3 what we'll decode (4 promises)
 (M(bg_('decode', 40, 10, "Let's *decode* it", 84),
    ic('scientists', 40, 170, 'ph:flask-fill', 140, P), tg('scientists', 30, 400, 'the scientists', size=30),
    ic('marketing', 360, 170, 'ph:megaphone-fill', 140, R), tg('marketing', 340, 400, 'the bragging company', size=30),
    ic('record', 680, 170, 'ph:record-fill', 140, R), tg('record', 660, 400, 'real recordings', size=30),
    ic('mind', 1000, 170, 'ph:brain-fill', 140, O), tg('mind', 980, 400, 'how ads "read minds"', size=30)), None),
 # 4 cat food test intro ★
 (M(bg_('experiment', 40, 30, 'The *cat food* test', 100, **SL), ic('max', 60, 260, 'ph:device-mobile-fill', 170, D),
    X('stamp', 'try', 700, 280, text='HYPOTHETICAL', size=60, color='#8C6B5A', rot=-6, id='hy')), 'FUN: the cat food test'),
 # 5 Max says cat food everywhere
 (M(ic('cat', 40, 40, 'ph:cat-fill', 180, D), X('stamp', 'own', 60, 120, text='NO CAT', size=60, rot=-10, id='nc'),
    ic('breakfast', 360, 40, 'ph:coffee-fill', 130, O), tg('breakfast', 330, 230, 'breakfast', size=28),
    ic('bus', 600, 40, 'ph:bus-fill', 130, Y), tg('bus', 600, 230, 'bus', size=28),
    ic('lift', 840, 40, 'ph:elevator-fill', 130, BL), tg('loudly', 800, 230, 'office lift', size=28),
    bg_('loudly', 300, 400, '"CAT FOOD!"', 120, color=R, **SL)), None),
 # 6 day counter, ad appears, gasp
 (M(cd('one', 40, 40, 'DAY 1', 'MAX\'S PHONE', 'ph:calendar-fill', BL, w=360, id='day'),
    tg('nothing', 60, 250, 'nothing…', bg='#8C6B5A'), X('prop', 'four', 560, 40, p='phone', s=.9, id='ph', **SD),
    tg('ad', 520, 420, 'AD: Cat food, 50% off!', bg=O, size=40, **SL), bg_('closed', 60, 520, 'Case *closed*?', 90),
    acts=[{'do': 'count', 'id': 'day', 'at': 'one', 'values': ['DAY 1', 'DAY 2', 'DAY 3', 'DAY 4'], 'dt': .7}, {'do': 'shake', 'id': 'ph', 'at': 'gasps'}]), None),
 # 7 a thousand forgotten ads + his own search
 (M(*[tg('thousand', 40 + (k % 5) * 200, 40 + (k // 5) * 70, 'ad', bg='#C9A57A', size=26, id=f'f{k}') for k in range(15)],
    cd('thousand', 40, 280, '~1,000 ads', 'FORGOTTEN THIS WEEK', 'ph:eye-slash-fill', '#8C6B5A'),
    X('card', 'searched', 40, 470, icon='ph:magnifying-glass-bold', label='MAX SEARCHED', big='"why does my cat food test not work"', bsize=40, color=R, id='sr', **FL),
    bg_('oops', 900, 300, 'Oops.', 110, color=R, **SL)), None),
 # 8 hits vs misses
 (M(X('bars', 'count', 40, 60, w=800, id='b', rows=[['hits you remember', .1, G], ['misses you forget', 1.0, '#8C6B5A']], gap=.6),
    ic('properly', 960, 60, 'ph:flask-fill', 170, P), tg('properly', 900, 330, 'test it properly →', bg=P)), None),
 # 9 Northeastern 2018 (chapter)
 (M(ic('researchers', 40, 40, 'ph:graduation-cap-fill', 170, R), bg_('northeastern', 280, 60, 'Northeastern *University*', 80),
    tg('boston', 300, 190, 'Boston · 2018', bg=D), ic('act', 700, 330, 'ph:magnifying-glass-bold', 200, O),
    X('prop', 'phones', 60, 330, p='phone', s=.8, id='ph')), 'The scientists tested it'),
 # 10 17,000 apps, captured all data
 (M(lg('android', 40, 40, 'logos:android-icon', 150), cd('seventeen', 280, 40, '0 apps', 'TESTED AUTOMATICALLY', 'ph:robot-fill', BL, w=560, id='n'),
    lg('facebook', 980, 40, 'logos:facebook', 130), ic('captured', 60, 360, 'ph:package-fill', 120, O),
    X('arrow', 'captured', 240, 400, w=380, id='ar'), ic('data', 680, 330, 'ph:database-fill', 170, D),
    acts=[{'do': 'count', 'id': 'n', 'at': 'seventeen', 'values': ['1,000 apps', '5,000 apps', '10,000 apps', '17,260 apps'], 'dt': .18}]), None),
 # 11 looking for audio: none
 (M(ic('audio', 40, 60, 'ph:waveform-bold', 200, BL), cd('none', 340, 60, 'AUDIO SENT: 0', 'RESULT', 'ph:microphone-slash-fill', G, **SL),
    X('stamp', 'secretly', 360, 360, text='NOT ONE APP', size=90, color=G, rot=-5, id='st', **SL)), None),
 # 12 careful: doesn't prove never; biggest test
 (M(ic('careful', 40, 40, 'ph:warning-circle-fill', 170, Y), tg('careful', 40, 260, "doesn't prove it never happens", bg='#8C6B5A'),
    cd('biggest', 560, 60, 'one of the biggest', 'TESTS OF ITS KIND', 'ph:trophy-fill', Y), bg_('empty', 40, 420, 'came up *empty*', 84, **SL)), None),
 # 13 something creepy: screen recordings
 (M(bg_('creepy', 40, 30, 'Something *creepy*', 90, **SL), X('prop', 'recording', 60, 200, p='phone', s=.8, id='ph'),
    ic('recording', 380, 220, 'ph:record-fill', 130, R), X('arrow', 'sending', 560, 280, w=300, id='ar'),
    ic('companies', 900, 200, 'ph:buildings-fill', 170, D), tg('videos', 380, 450, 'videos of your screen', bg=R)), None),
 # 14 GoPuff -> analytics firm, fixed
 (M(ic('delivery', 40, 40, 'ph:moped-fill', 170, O), tg('gopuff', 40, 250, 'GoPuff app', bg=D, size=40),
    X('arrow', 'sending', 300, 120, w=300, id='ar'), ic('analytics', 640, 40, 'ph:chart-bar-fill', 170, BL), tg('analytics', 620, 250, 'analytics firm', size=34),
    tg('stopped', 300, 400, 'stopped after researchers got in touch', bg=G, size=34), bg_('needed', 300, 500, 'No *microphone* needed', 80)), None),
 # 15 Facebook 2016 statement (Vox clipping)
 (M(lg('facebook', 40, 40, 'logos:facebook', 160), X('clip', 'record', 300, 40, by='FACEBOOK, JUNE 2016', text='"Facebook does not use your phone\'s microphone to inform ads"', hi='does not use', w=880, id='cl'),
    ic('choose', 60, 380, 'ph:microphone-slash-fill', 150, G)), None),
 # 16 the leak ★ (chapter)
 (M(bg_('leak', 40, 60, 'Then… a *leak*', 120, **SL), ic('leak', 980, 60, 'ph:file-text-fill', 200, R), tg('twenty-four', 60, 260, '2024', bg=D, size=48)), 'The leak'),
 # 17 404 Media pitch deck "Active Listening"
 (M(X('clip', 'published', 40, 40, by='404 MEDIA · SEPTEMBER 2024', text='Cox Media Group pitch deck: "Active Listening"', hi='"Active Listening"', w=760, id='cl'),
    ic('marketing', 900, 40, 'ph:megaphone-fill', 170, R), tg('company', 880, 260, 'big US marketing company', size=30)), None),
 # 18 claimed: voice data -> ads
 (M(ic('smart', 40, 60, 'ph:speaker-hifi-fill', 160, D), ic('voice', 260, 60, 'ph:waveform-bold', 160, BL), X('arrow', 'find', 460, 120, w=260, id='ar'),
    ic('target', 780, 40, 'ph:target-bold', 190, R), tg('claimed', 60, 330, 'THE CLAIM (sales deck)', bg='#8C6B5A', size=40)), None),
 # 19 Google removed; Amazon: not us
 (M(lg('google', 40, 40, 'logos:google-icon', 150), X('stamp', 'removed', 30, 240, text='REMOVED', size=70, rot=-8, id='rm', **SL),
    lg('amazon', 600, 40, 'simple-icons:amazon', 150), tg('nothing', 560, 260, '"nothing to do with it"', bg=D, size=34)), None),
 # 20 sales deck != evidence
 (M(ic('deck', 60, 60, 'ph:presentation-chart-fill', 200, O), bg_('evidence', 360, 80, '≠', 200, color=R), ic('evidence', 560, 60, 'ph:seal-check-fill', 200, G),
    tg('nobody', 60, 400, 'never shown to work at real scale', bg=R)), None),
 # 21 twist: phones listened to ads before (chapter)
 (M(bg_('twist', 40, 60, 'A strange *twist*', 110, **SL), ic('ads', 60, 300, 'ph:television-simple-fill', 180, D), ic('listened', 340, 300, 'ph:ear-fill', 170, O),
    tg('you', 600, 360, '…just not to you', bg=D, size=44)), 'Secret TV whistles'),
 # 22 SilverPush: whistles hidden in TV ads
 (M(ic('silverpush', 40, 40, 'ph:television-simple-fill', 190, D), X('prop', 'sounds', 280, 60, p='waves', s=.6, id='wv'),
    ic('humans', 700, 40, 'ph:ear-slash-fill', 150, R), tg('humans', 660, 230, 'humans: can\'t hear', bg=R, size=30),
    ic('phone', 960, 40, 'ph:device-mobile-fill', 150, G), tg('phone', 940, 230, 'phone: hears it', bg=G, size=30), tg('silverpush', 60, 330, 'SilverPush', bg=O, size=44)), None),
 # 23 app knows you watched the ad
 (M(ic('whistle', 60, 60, 'ph:waveform-bold', 170, BL), X('arrow', 'app', 290, 120, w=220, id='ar'), ic('knew', 560, 40, 'ph:check-circle-fill', 190, G),
    bg_('watched', 60, 380, 'You *watched* that ad', 90)), None),
 # 24 FTC warning letters to 12 developers
 (M(ic('commission', 40, 40, 'ph:scales-fill', 170, D), X('clip', 'letters', 300, 40, by='US FEDERAL TRADE COMMISSION · MARCH 2016', text='Warning letters to 12 app developers using SilverPush code', hi='12 app developers', w=820, id='cl'),
    tg('told', 320, 330, 'users were never told', bg=R, size=40)), None),
 # 25 tech is real; not recording you for shoes
 (M(cd('real', 40, 40, 'REAL', 'TECH TO LISTEN', 'ph:check-circle-fill', G), cd('found', 560, 40, 'NOT FOUND', 'SECRET CONVERSATION RECORDING', 'ph:x-circle-fill', R),
    ic('shoes', 400, 330, 'ph:sneaker-fill', 170, O)), None),
 # 26 voice assistants (chapter)
 (M(bg_('voice', 40, 40, 'Voice *assistants*', 110, **SL), lg('voice', 60, 260, 'logos:apple', 130), lg('voice', 280, 260, 'logos:google-icon', 130), lg('voice', 500, 260, 'simple-icons:amazon', 130)), 'When devices DID record'),
 # 27 wake word on device
 (M(tg('hey', 40, 60, '"Hey Siri"', bg=D, size=60), tg('hey', 440, 60, '"Hey Google"', bg=BL, size=60, id='hg'),
    X('prop', 'tiny', 60, 240, p='chip', text='wake', s=.8, id='ch'), tg('device', 340, 330, 'checked right on the device', bg=G)), None),
 # 28 "seriously" -> Siri wakes, records
 (M(X('card', 'seriously', 40, 40, icon='ph:chat-circle-dots-fill', label='SOMEONE SAYS', big='"Seriously…"', color=O, id='s'),
    lg('siri', 860, 40, 'logos:apple', 140), tg('called', 760, 260, 'Siri: "You called?"', bg=D, size=40, **SL),
    ic('records', 60, 330, 'ph:record-fill', 150, R), tg('mistake', 260, 380, 'records by mistake', bg=R)), None),
 # 29 request goes to servers
 (M(ic('wake', 40, 60, 'ph:device-mobile-fill', 170, D), X('arrow', 'request', 260, 120, w=320, id='ar'), ic('servers', 640, 40, 'ph:hard-drives-fill', 200, BL),
    tg('stored', 600, 330, 'where a recording can be stored', bg=O)), None),
 # 30 Apple $95M, Google $68M
 (M(lg('apple', 40, 40, 'logos:apple', 130), cd('ninety-five', 220, 40, '$95 million', 'APPLE · SIRI · 2025', 'ph:currency-dollar-bold', G, **SL),
    lg('google', 40, 290, 'logos:google-icon', 130), cd('sixty-eight', 220, 290, '$68 million', 'GOOGLE · ASSISTANT', 'ph:currency-dollar-bold', G, **SL),
    tg('admitted', 760, 500, 'no wrongdoing admitted', bg='#8C6B5A')), None),
 # 31 Alexa reviewers
 (M(lg('smart', 40, 40, 'simple-icons:amazon', 130), X('clip', 'bloomberg', 240, 40, by='BLOOMBERG · APRIL 2019', text='Thousands of Amazon staff listen to Alexa clips', hi='listen to Alexa clips', w=780, id='cl'),
    ic('listening', 60, 330, 'ph:headphones-fill', 160, O), cd('thousand', 300, 330, 'up to 1,000', 'CLIPS PER SHIFT', 'ph:list-numbers-bold', R)), None),
 # 32 FTC $25M kids' recordings
 (M(ic('children', 40, 40, 'ph:baby-fill', 160, P), cd('twenty-five', 260, 40, '$25 million', 'AMAZON · FTC · 2023', 'ph:gavel-fill', R, **SL),
    tg('deleted', 260, 280, "kept kids' recordings after delete requests", bg=D, size=32), tg('denied', 260, 380, 'Amazon denied breaking the law', bg='#8C6B5A', size=30)), None),
 # 33 risk real, but accidents
 (M(cd('real', 40, 40, 'risk is real', 'VERDICT', 'ph:warning-fill', R), tg('accidents', 40, 280, 'accidents', bg=O, size=48), tg('long', 340, 280, 'data kept too long', bg=O, size=48),
    X('stamp', 'machine', 400, 420, text='NOT AN AD MACHINE', size=70, color=G, rot=-4, id='st', **SL)), None),
 # 34 why experts don't believe (chapter)
 (M(ic('experts', 40, 60, 'ph:user-focus-fill', 190, D), bg_('everything', 300, 100, 'Recording *everything*?', 90), ic('why', 1050, 300, 'ph:question-fill', 160, O)), 'Why it is unlikely'),
 # 35 the maths
 (M(cd('sixteen', 40, 40, '16 kbps', 'COMPRESSED VOICE', 'ph:waveform-bold', BL), X('arrow', 'day', 560, 110, w=200, id='ar'),
    cd('hundred', 800, 40, '0 MB', 'PER PHONE, PER DAY', 'ph:database-fill', R, id='mb'), tg('every', 40, 330, 'example calculation: 16 kbps × 24 h', bg='#8C6B5A', size=30),
    acts=[{'do': 'count', 'id': 'mb', 'at': 'hundred', 'values': ['20 MB', '60 MB', '110 MB', '170 MB'], 'dt': .2}]), None),
 # 36 data pack, battery, researchers notice
 (M(ic('data', 40, 60, 'ph:cell-signal-full-bold', 170, BL), tg('data', 40, 270, 'data pack', size=32), ic('battery', 360, 60, 'ph:battery-warning-fill', 170, R), tg('battery', 360, 270, 'battery', size=32),
    ic('researchers', 680, 60, 'ph:magnifying-glass-bold', 170, O), tg('definitely', 660, 270, 'researchers', size=32), bg_('notice', 200, 400, 'Everyone would *notice*', 90, **SL)), None),
 # 37 orange / green dots
 (M(X('prop', 'iphone', 40, 40, p='phone', s=.85, id='ip'), X('big', 'orange', 120, 60, text='●', size=90, color=O, id='od', **SL), tg('iphone', 40, 450, 'iPhone: orange dot = microphone', bg=O, size=30),
    X('prop', 'android', 640, 40, p='phone', s=.85, id='an'), X('big', 'green', 720, 60, text='●', size=90, color=G, id='gd', **SL), tg('android', 600, 450, 'Android: green dot → tap to see app', bg=G, size=30)), None),
 # 38 bad deal for advertisers
 (M(ic('advertisers', 40, 60, 'ph:megaphone-fill', 170, R), cd('know', 300, 60, 'a whole profile', 'ADVERTISERS ALREADY HAVE', 'ph:identification-card-fill', BL),
    tg('sentence', 300, 300, 'vs one sentence at dinner', bg='#8C6B5A', size=40)), None),
 # 39 four routes (chapter) ★
 (M(ic('shoe', 40, 40, 'ph:sneaker-fill', 200, R), bg_('four', 320, 60, '*4* routes', 140, **SL),
    *[tg('routes', 320 + k * 200, 280, f'ROUTE {k + 1}', bg=[BL, P, O, G][k], size=34, id=f'r{k}') for k in range(4)]), 'The four routes'),
 # 40 route one: people around you, same Wi-Fi
 (M(tg('route', 40, 20, 'ROUTE 1 · the people around you', bg=BL, size=40), ic('friend', 40, 140, 'ph:user-fill', 140, D), ic('looked', 220, 140, 'ph:magnifying-glass-bold', 120, O),
    ic('wi-fi', 460, 140, 'ph:wifi-high-bold', 170, BL), lg('facebook', 760, 140, 'logos:facebook', 140), tg('location', 700, 340, 'location guessed from your connection', size=30),
    ic('spend', 60, 380, 'ph:users-three-fill', 150, P), tg('time', 240, 430, 'who you spend time with', bg=P)), None),
 # 41 route two: Meta Pixel
 (M(tg('route', 40, 20, 'ROUTE 2 · the trail you leave', bg=P, size=40), ic('websites', 40, 140, 'ph:browser-fill', 170, BL), X('card', 'code', 300, 150, icon='ph:code-bold', label='HIDDEN ON THE PAGE', big='Meta Pixel', color=P, id='px'),
    X('arrow', 'report', 300, 380, w=300, id='ar'), lg('meta', 660, 330, 'logos:meta-icon', 170), tg('account', 40, 520, "…even if you don't have an account", bg=R, size=32)), None),
 # 42 customer lists matched
 (M(ic('shops', 40, 60, 'ph:storefront-fill', 170, O), ic('email', 280, 60, 'ph:envelope-simple-fill', 140, BL), ic('phone', 460, 60, 'ph:phone-fill', 140, G), X('arrow', 'matches', 640, 120, w=200, id='ar'),
    lg('meta', 900, 40, 'logos:meta-icon', 160), tg('store', 60, 330, 'that store keeps finding you', bg=D)), None),
 # 43 route three: data brokers & location
 (M(tg('route', 40, 20, 'ROUTE 3 · brokers & location', bg=O, size=40), ic('brokers', 40, 140, 'ph:briefcase-fill', 150, D), ic('where', 300, 140, 'ph:map-pin-fill', 150, R),
    ic('gym', 560, 140, 'ph:barbell-fill', 160, D), tg('three', 540, 360, 'gym × 3 a week', bg=O), ic('shoes', 900, 140, 'ph:sneaker-fill', 170, R)), None),
 # 44 route four: your brain, frequency illusion, Max's cat
 (M(tg('route', 40, 20, 'ROUTE 4 · your own brain', bg=G, size=40), ic('brain', 40, 140, 'ph:brain-fill', 180, P),
    cd('illusion', 300, 150, 'frequency illusion', 'PSYCHOLOGISTS CALL IT', 'ph:eye-fill', G), ic('cat', 900, 330, 'ph:cat-fill', 150, D), tg('max', 860, 520, "Max's imaginary cat", bg=D, size=30)), None),
 # 45 bonus: lookalikes
 (M(tg('bonus', 40, 20, 'BONUS · lookalikes', bg=R, size=44), *[ic('people', 40 + k * 150, 150, 'ph:user-fill', 110, '#8C6B5A', paper=False, id=f'u{k}') for k in range(6)],
    ic('you', 960, 130, 'ph:user-circle-fill', 160, O), tg('age', 40, 330, 'same age · same city · same apps', size=34), bg_('like', 40, 440, 'people *like you*', 90, **SL)), None),
 # 46 predicts
 (M(ic('predicts', 40, 60, 'ph:sparkle-fill', 220, P), bg_('hear', 340, 80, "doesn't need to *hear* you", 84), tg('want', 340, 260, 'it predicts what you want next', bg=P, size=40)), None),
 # 47 quiz (chapter) ★
 (M(bg_('game', 40, 40, 'REAL or *FAKE*?', 130, **SL), tg('real', 60, 300, 'REAL', bg=G, size=70), tg('fake', 400, 300, 'FAKE', bg=R, size=70)), 'FUN: Real or fake?'),
 # 48 myth 1 airplane mode
 (M(ic('airplane', 40, 40, 'ph:airplane-tilt-fill', 190, BL), tg('one', 300, 60, 'MYTH 1', bg=D, size=40), bg_('tracking', 300, 140, 'stops all tracking?', 72),
    X('stamp', 'fake', 300, 300, text='FAKE', size=110, id='f', **SL), tg('reconnect', 60, 470, 'apps send it when you reconnect', bg='#8C6B5A', size=32)), None),
 # 49 myth 2 incognito
 (M(ic('incognito', 40, 40, 'ph:detective-fill', 190, D), tg('two', 300, 60, 'MYTH 2', bg=D, size=40), bg_('hides', 300, 140, 'hides you from websites?', 72),
    X('stamp', 'fake', 300, 300, text='FAKE', size=110, id='f', **SL), tg('history', 60, 470, 'only your own history is not saved', bg='#8C6B5A', size=32)), None),
 # 50 myth 3 wake word: REAL
 (M(ic('listening', 40, 40, 'ph:ear-fill', 190, O), tg('three', 300, 60, 'MYTH 3', bg=D, size=40), bg_('always', 300, 140, 'always listening for one thing?', 64),
    X('stamp', 'real', 300, 300, text='REAL', size=110, color=G, id='r', **SL), tg('wake', 60, 470, 'the wake word · turn it off = easy win', bg=G, size=32)), None),
 # 51 myth 4 camera sticker
 (M(ic('camera', 40, 40, 'ph:camera-slash-fill', 190, D), tg('four', 300, 60, 'MYTH 4', bg=D, size=40), bg_('blocks', 300, 140, 'camera sticker blocks the mic?', 64),
    X('stamp', 'fake', 300, 300, text='FAKE', size=110, id='f', **SL), ic('mic', 900, 330, 'ph:microphone-fill', 140, R)), None),
 # 52 India DPDP (chapter)
 (M(X('icon', 'india', 40, 40, ref='circle-flags:in', size=180, **DR), X('clip', 'dpdp', 280, 40, by='INDIA · DATA PROTECTION', text='DPDP Act rules in place since November 2025', hi='November 2025', w=820, id='cl')), 'What about India?'),
 # 53 phases to 2027, consent
 (M(X('bars', 'phases', 40, 40, w=760, id='b', rows=[['Nov 2025 · rules notified', .3, BL], ['Nov 2026 · consent managers', .6, P], ['May 2027 · full compliance', 1.0, G]], gap=.5),
    ic('withdraw', 900, 60, 'ph:toggle-left-fill', 200, G), tg('consent', 860, 300, 'withdraw consent easily', bg=G, size=32)), None),
 # 54 5 minutes
 (M(ic('today', 40, 60, 'ph:timer-fill', 220, O), bg_('five', 400, 100, '*5 minutes*, 5 steps', 96, **SL)), 'Five things to do today'),
 # 55 step 1 mic permissions
 (M(tg('one', 40, 20, 'STEP 1 · microphone permissions', bg=O, size=40), X('card', 'iphone', 40, 140, icon='ph:gear-six-fill', label='IPHONE', big='Settings › Privacy & Security › Microphone', bsize=36, color=D, id='i'),
    X('card', 'android', 40, 330, icon='ph:shield-check-fill', label='ANDROID', big='Privacy dashboard', bsize=44, color=G, id='a'), ic('switch', 960, 300, 'ph:toggle-left-fill', 170, R)), None),
 # 56 torch / calculator joke
 (M(ic('torch', 40, 60, 'ph:flashlight-fill', 180, Y), tg('torch', 40, 290, 'torch app', size=32), ic('calculator', 360, 60, 'ph:calculator-fill', 180, D), tg('calculator', 360, 290, 'calculator', size=32),
    ic('microphone', 700, 60, 'ph:microphone-fill', 150, R), X('stamp', 'no', 680, 280, text='NO!', size=110, id='n', **SL)), None),
 # 57 step 2 watch the dot
 (M(tg('two', 40, 20, 'STEP 2 · watch the dot', bg=O, size=40), X('prop', 'dot', 60, 120, p='phone', s=.85, id='ph'), X('big', 'orange', 150, 150, text='●', size=80, color=O, id='od', **SL),
    ic('call', 560, 160, 'ph:phone-slash-fill', 150, D), tg('which', 560, 380, 'not on a call? find the app', bg=R, size=34)), None),
 # 58 step 3 ad tracking
 (M(tg('three', 40, 20, 'STEP 3 · limit ad tracking', bg=O, size=40), lg('iphone', 40, 140, 'logos:apple', 120), tg('ask', 220, 170, '"Ask App Not to Track"', bg=D, size=40),
    lg('android', 40, 330, 'logos:android-icon', 120), tg('delete', 220, 360, 'Delete advertising ID', bg=G, size=40)), None),
 # 59 step 4 off-Meta activity
 (M(tg('four', 40, 20, 'STEP 4 · off-Meta activity', bg=O, size=40), lg('facebook', 40, 140, 'logos:facebook', 130), lg('instagram', 240, 140, 'logos:instagram-icon', 130),
    X('card', 'activity', 480, 150, icon='ph:list-bullets-bold', label='SETTINGS', big='Your activity off Meta technologies', bsize=36, color=P, id='c'), ic('disconnect', 480, 360, 'ph:link-break-bold', 150, R)), None),
 # 60 step 5 wake word off, delete recordings
 (M(tg('five', 40, 20, 'STEP 5 · voice assistants', bg=O, size=40), ic('wake', 40, 150, 'ph:microphone-slash-fill', 170, R), tg('wake', 260, 190, 'wake word: OFF', bg=R, size=40),
    ic('delete', 40, 370, 'ph:trash-fill', 160, D), tg('delete', 260, 410, 'delete saved recordings', bg=D, size=40)), None),
 # 61 verdict (chapter) ★
 (M(ic('phone', 40, 60, 'ph:device-mobile-fill', 200, D), bg_('listening', 320, 80, 'Listening for ads?', 96), X('stamp', 'almost', 340, 260, text='ALMOST CERTAINLY NOT', size=70, color=G, rot=-4, id='n', **SL)), 'The verdict'),
 # 62 doesn't need to
 (M(ic('shoe', 480, 30, 'ph:sneaker-fill', 200, R), ic('searches', 60, 300, 'ph:magnifying-glass-bold', 140, O), ic('location', 360, 300, 'ph:map-pin-fill', 140, R), ic('people', 660, 300, 'ph:users-three-fill', 140, P),
    bg_('story', 200, 560, 'already tell the *story*', 80)), None),
 # 63 Max buys cat food
 (M(ic('cat', 60, 60, 'ph:cat-fill', 170, D), ic('buying', 300, 60, 'ph:shopping-bag-fill', 190, O), bg_('won', 60, 380, 'The ads *won*.', 120, **SL)), None),
 # 64 comments
 (M(lg('comments', 40, 40, 'logos:youtube-icon', 180), ic('comments', 280, 40, 'ph:chat-circle-text-fill', 180, O),
    X('card', 'creepiest', 40, 300, icon='ph:user-circle-fill', label='YOUR COMMENT', big='The creepiest ad I ever saw…', color=O, id='cm', **FL)), None),
 # 65 subscribe
 ({'type': 'end', 'sub': 'More tech, decoded.'}, None),
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
