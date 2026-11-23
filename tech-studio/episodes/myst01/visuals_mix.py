"""myst01 TECH MYSTERIES · CASE 001 "The TV Hijack Nobody Ever Solved" (series look: tools/kit_myst.py, approved look test).
Word-timed kit_mix beats with the mystery kinds (tv, file, typer, radar, tower, beam, clue, skyline, figure) + stamps, Vox clippings,
icons, counters. Stage 1320x760. Max (night hoodie, moonlight rim) only on host beats.
Run: python3 episodes/myst01/visuals_mix.py && STYLE=mystery THEME=navy CASE=001 python3 tools/hf_myst01_long.py"""
import json, re
from pathlib import Path
HERE = Path(__file__).parent
f = HERE / 'long.json'; e = json.loads(f.read_text())

def M(*els, acts=()):
    return {'type': 'mix', 'els': [x for x in els if x], 'acts': list(acts)}
def X(k, at, x, y, **o):
    d = dict(k=k, at=at, x=x, y=y); d.update(o); return d
W, ST, R, G, Y, D = '#E8EDF5', '#8FA3C2', '#E5383B', '#3DDC97', '#FFD54A', '#0F1726'
def ic(at, x, y, ref, size=120, color=ST, **o): return X('icon', at, x, y, ref=ref, size=size, color=color, **o)
def tg(at, x, y, text, bg='#141B29', size=30, color=W, **o): return X('tag', at, x, y, text=text, bg=bg, size=size, color=color, **o)
def bg_(at, x, y, text, size=96, color=W, **o): return X('big', at, x, y, text=text, size=size, color=color, **o)
def st(at, x, y, text, size=90, color=R, rot=-10, **o): return X('stamp', at, x, y, text=text, size=size, color=color, rot=rot, **o)
def cd(at, x, y, big, label='', icon=None, color=R, w=None, **o):
    d = dict(big=big, label=label, color=color, **o)
    if icon: d['icon'] = icon
    if w: d['w'] = w
    return X('card', at, x, y, **d)
def tv(at, x, y, w=640, screen='sports', label=None, **o):
    d = dict(w=w, screen=screen, **o)
    if label: d['label'] = label
    return X('tv', at, x, y, **d)
def clip(at, x, y, by, text, hi=None, w=640, **o):
    d = dict(by=by, text=text, w=w, **o)
    if hi: d['hi'] = hi
    return X('clip', at, x, y, **d)
def TVSW(at, scr, id='tv'): return {'do': 'tv', 'id': id, 'at': at, 'screen': scr}
SL = {'in': 'slam'}; SD = {'in': 'slide'}; DR = {'in': 'drop'}; FL = {'in': 'fly'}; LF = {'in': 'left'}; FD = {'in': 'fade'}; RS = {'in': 'rise'}

V = [
 # 0 cold open: date types out
 (M(tg(0.02, 300, 120, 'CASE FILE · SIGNAL INTRUSION', bg='rgba(0,0,0,0)', color=ST, size=28, **FD),
    X('typer', 0.05, 190, 230, text='NOV 22, 1987', size=150, dur=1.6, id='dt'),
    tg('chicago', 330, 470, 'CHICAGO · SUNDAY NIGHT', bg='rgba(0,0,0,0)', color=ST, size=34, **FD)), None),
 # 1 millions watching the sports news
 (M(tv(0.02, 300, 30, 660, 'sports', label='WGN-TV · CHANNEL 9', id='tv', **FL),
    cd('millions', 1000, 120, 'MILLIONS', 'WATCHING', 'ph:users-three-fill', ST, id='m', **SD)), None),
 # 2 9:14 PM, screen goes black
 (M(tv(0.02, 300, 30, 660, 'sports', id='tv'), X('typer', 'fourteen', 1000, 120, text='9:14 PM', size=80, color=R, dur=.6, id='tm'),
    acts=[TVSW('black', 'static'), TVSW(0.97, 'black')]), None),
 # 3 someone else appears
 (M(tv(0.02, 300, 30, 660, 'black', id='tv'), st('supposed', 330, 600, 'NOT SUPPOSED TO BE THERE', 44, R, -4, id='s', **SL),
    acts=[TVSW('appears', 'figure')]), None),
 # 4 nobody knows
 (M(X('figure', 0.02, 40, 40, w=560, h=420, id='fg', **FD), bg_('nobody', 660, 120, 'Nobody', 110), bg_('knows', 660, 250, 'knows who', 110), bg_('was', 660, 380, 'it *was*.', 110, **SL)), None),
 # 5 unsolved for almost 40 years
 (M(cd('story', 40, 60, '1987', 'TV HIJACK', 'ph:television-simple-fill', ST, w=420, id='y', **FL),
    cd('forty', 520, 60, '~40 YEARS', 'STILL UNSOLVED', 'ph:hourglass-high-fill', R, w=520, id='n', **FL),
    st('unsolved', 360, 380, 'UNSOLVED', 120, R, -8, id='u', **SL),
    acts=[{'do': 'count', 'id': 'n', 'at': 'forty', 'values': ['10 YEARS', '20 YEARS', '30 YEARS', '~40 YEARS'], 'dt': .15}]), None),
 # 6 one person, homemade gear, two stations
 (M(ic('person', 40, 60, 'ph:user-focus-fill', 170, W, id='p'), tg('homemade', 20, 290, 'homemade equipment', size=30, id='h'),
    ic('homemade', 320, 70, 'ph:wrench-fill', 120, ST, id='wr'),
    tv('two', 560, 30, 340, 'figure', label='WGN', id='t1', **SD), tv('two', 940, 30, 340, 'figure', label='WTTW', id='t2', **SD),
    tg('america', 640, 420, 'two of the biggest TV stations in America', bg=R, size=30, id='b')), None),
 # 7 ★ open the case file
 (M(X('file', 'open', 60, 60, w=820, title='CASE 001 · BROADCAST SIGNAL INTRUSION', rows=[['DATE', '22 NOV 1987'], ['CITY', 'CHICAGO'], ['SUSPECT', None], ['STATUS', 'OPEN']], id='cf', **DR)),
  'The first hijack'),
 # 8 Sunday night on WGN, sports highlights
 (M(tv(0.02, 40, 30, 640, 'sports', label='WGN · CHANNEL 9 · 9 PM NEWS', id='tv', **FL),
    tg('sunday', 760, 60, 'SUNDAY · 22 NOV 1987', size=30, id='d'), ic('sports', 760, 160, 'ph:football-fill', 140, ST, id='f'),
    tg('highlights', 760, 330, "reading the day's highlights", size=30, id='h')), None),
 # 9 picture flickers, newsroom disappears
 (M(tv(0.02, 300, 30, 660, 'sports', id='tv'), tg('flickers', 1000, 160, 'SIGNAL LOST', bg=R, size=34, id='sl', **SL),
    acts=[TVSW('flickers', 'static'), TVSW('disappears', 'black')]), None),
 # 10 masked figure rocking
 (M(tv(0.02, 300, 30, 660, 'figure', id='tv'), tg('mask', 1000, 120, 'rubber mask', size=32, id='m'),
    ic('rocking', 1020, 230, 'ph:arrows-left-right-bold', 110, R, id='r'), acts=[{'do': 'shake', 'id': 'tv', 'at': 'rocking'}]), None),
 # 11 spinning metal behind him
 (M(X('figure', 0.02, 40, 40, w=760, h=520, id='fg', **FD), ic('spinning', 880, 80, 'ph:spiral-bold', 160, ST, id='sp'),
    tg('metal', 860, 300, 'a sheet of spinning metal', size=30, id='m'), acts=[{'do': 'spin', 'id': 'sp', 'at': 'spinning', 'deg': 720, 'd': 3}]), None),
 # 12 ★ mask copies Max Headroom (fake CGI character); no relation to our Max
 (M(clip('copies', 40, 40, 'THE CHARACTER IT COPIED', 'Max Headroom: a 1980s TV host who was "computer-generated", actually an actor in make-up', hi='an actor in make-up', w=680, id='cl', **FL),
    ic('character', 120, 400, 'ph:robot-fill', 150, ST, id='rb'), st('relation', 400, 430, 'NO RELATION', 80, G, -6, id='nr', **SL)), None),
 # 13 no sound, buzzing hum
 (M(tv(0.02, 300, 30, 660, 'figure', id='tv'), ic('sound', 1000, 80, 'ph:speaker-x-fill', 140, R, id='s'),
    tg('buzzing', 980, 280, 'just a buzzing hum', size=30, id='b'), acts=[{'do': 'shake', 'id': 'tv', 'at': 'buzzing'}]), None),
 # 14 engineers change the frequency
 (M(ic('engineers', 40, 60, 'ph:headset-fill', 150, ST, id='e'), cd('half', 260, 60, '0 SEC', 'TIME ON AIR', 'ph:timer-fill', R, w=420, id='t', **FL),
    tg('frequency', 40, 330, 'change the link frequency', bg=G, color='#06130D', size=34, id='f'),
    tv('gone', 760, 60, 480, 'figure', id='tv'),
    acts=[{'do': 'count', 'id': 't', 'at': 'half', 'values': ['10 SEC', '20 SEC', '~30 SEC'], 'dt': .25}, TVSW('gone', 'sports')]), None),
 # 15 anchor: "so am I"
 (M(tv(0.02, 40, 30, 600, 'sports', label='BACK IN THE STUDIO', id='tv'),
    clip('says', 720, 80, 'THE ANCHOR, LIVE ON AIR', '"If you\'re wondering what\'s happened, so am I."', hi='so am I', w=560, id='cl', **SD)), None),
 # 16 two hours, Chicago thinks it's over
 (M(cd('hours', 40, 60, '9:14', 'CHICAGO TIME', 'ph:clock-fill', ST, w=420, id='c', **FL),
    X('skyline', 0.05, 0, 330, w=1320, id='sk', **RS), bg_('isnt', 600, 80, "It isn't.", 120, color=R, **SL),
    acts=[{'do': 'count', 'id': 'c', 'at': 'thinks', 'values': ['9:30', '10:00', '10:30', '11:00'], 'dt': .3}]), None),
 # 17 11:10 PM, WTTW, a sci-fi show
 (M(tv(0.02, 300, 30, 660, 'drama', label='WTTW · CHANNEL 11', id='tv', **FL), X('typer', 'eleven', 1000, 120, text='11:10 PM', size=70, color=R, dur=.6, id='tm'),
    tg('doctor', 1000, 260, 'a sci-fi series', size=30, id='d')), 'The second hijack'),
 # 18 he comes back, with sound
 (M(tv(0.02, 300, 30, 660, 'drama', id='tv'), ic('sound', 1000, 80, 'ph:speaker-high-fill', 140, R, id='s'), tg('sound', 980, 270, 'THIS TIME, WITH SOUND', bg=R, size=30, id='w', **SL),
    acts=[TVSW('masked', 'static'), TVSW('comes', 'figure')]), None),
 # 19 distorted voice, mocks the station
 (M(tv(0.02, 40, 30, 560, 'figure', id='tv'), ic('distorted', 660, 60, 'ph:waveform-bold', 150, ST, id='wf'),
    tg('robotic', 840, 100, 'distorted, robotic', size=30, id='r'), tg('mocks', 660, 300, 'mocks WGN, the station that cut him off', bg=R, size=30, id='m', **SL),
    acts=[{'do': 'shake', 'id': 'wf', 'at': 'laughs'}]), None),
 # 20 soft drink can + slogan; hums a cartoon song
 (M(ic('drink', 60, 60, 'ph:beer-bottle-fill', 170, R, id='c'), tg('slogan', 40, 300, '"Catch the wave!"', size=40, id='s', **SL),
    tg('slogan', 40, 390, 'an ad slogan of the time', bg='rgba(0,0,0,0)', color=ST, size=26, id='s2'),
    ic('hums', 600, 80, 'ph:music-notes-fill', 160, ST, id='mn'), tg('cartoon', 580, 300, 'hums a cartoon theme', size=32, id='h'),
    acts=[{'do': 'bob', 'id': 'mn', 'at': 'hums', 'n': 6}]), None),
 # 21 "my brother has the other one"
 (M(ic('brother', 60, 60, 'ph:users-fill', 170, ST, id='b'),
    clip('strange', 320, 60, 'WHAT HE SAID', '"My brother has the other one."', hi='the other one', w=620, id='cl', **FL), st('one', 420, 380, '???', 120, R, 4, id='q', **SL)), None),
 # 22 ends with a flyswatter
 (M(tv(0.02, 40, 30, 560, 'figure', id='tv'), ic('someone', 680, 60, 'ph:user-plus-fill', 150, ST, id='u'),
    tg('frame', 660, 260, 'a second person steps in', size=30, id='f'), tg('flyswatter', 660, 340, '…holding a flyswatter', bg=R, size=34, id='fs', **SL)), None),
 # 23 ~90 s, back to the show
 (M(cd('ninety', 40, 60, '0 SEC', 'ON AIR', 'ph:timer-fill', R, w=420, id='t', **FL), tv('cuts', 560, 30, 600, 'figure', id='tv'),
    acts=[{'do': 'count', 'id': 't', 'at': 'ninety', 'values': ['30 SEC', '60 SEC', '~90 SEC'], 'dt': .25}, TVSW('cuts', 'drama')]), None),
 # 24 no engineers at the transmitter
 (M(X('tower', 0.02, 200, 200, name='SEARS TOWER · WTTW', w=150, h=500, id='tw', **RS),
    ic('engineers', 600, 80, 'ph:user-circle-dashed-bold', 150, ST, id='e'), st('nobody', 560, 280, 'NO ENGINEERS', 80, R, -8, id='n', **SL),
    tg('night', 600, 460, 'nobody could stop him', size=32, id='s')), None),
 # 25 how do you hijack a TV station?
 (M(bg_('hijack', 40, 80, 'How do you', 110), bg_('hijack', 40, 210, '*hijack* a TV station?', 110, **SL), ic('outside', 1000, 380, 'ph:broadcast-bold', 180, R, id='b')),
  'How it was done'),
 # 26 studio and transmitter in different places
 (M(ic('studio', 60, 260, 'ph:video-camera-fill', 160, W, id='s'), tg('studio', 40, 460, 'STUDIO', size=32, id='sl'),
    X('tower', 'transmitter', 1000, 160, name='TRANSMITTER', w=140, h=520, id='tw', **RS),
    tg('different', 420, 120, 'different places', bg=R, size=34, id='d')), None),
 # 27 microwave beam = invisible cable
 (M(ic(0.02, 60, 260, 'ph:video-camera-fill', 160, W, id='s'), X('tower', 0.02, 1000, 160, name='TOWER', w=140, h=520, id='tw'),
    X('beam', 'beam', 240, 330, x2=1060, y2=150, color=G, id='bm'), tg('microwave', 420, 420, 'a narrow beam of microwave radio', bg=G, color='#06130D', size=30, id='m'),
    tg('cable', 420, 500, '≈ an invisible cable in the air', size=30, id='c')), None),
 # 28 Hancock (WGN) and Sears Tower (WTTW)
 (M(X('skyline', 0.02, 0, 360, w=1320, id='sk', **FD),
    X('tower', 'hancock', 260, 230, name='JOHN HANCOCK · WGN', w=130, h=470, id='t1', **RS),
    X('tower', 'sears', 860, 190, name='SEARS TOWER · WTTW', w=160, h=510, ant=120, id='t2', **RS)), None),
 # 29 tower broadcasts whatever arrives
 (M(X('tower', 0.02, 560, 160, name='TOWER', w=150, h=520, id='tw'), X('beam', 'arrived', 60, 330, x2=600, y2=150, color=G, id='b1'),
    *[ic('broadcast', 820 + k * 140, 180 + k * 60, 'ph:television-simple-fill', 100, ST, id=f'h{k}', **DR) for k in range(3)],
    tg('whatever', 760, 520, 'broadcasts whatever arrives', size=30, id='t')), None),
 # 30 stronger signal wins
 (M(X('tower', 0.02, 560, 160, name='RECEIVER', w=150, h=520, id='tw'), X('beam', 0.02, 60, 300, x2=600, y2=150, color=G, id='b1'),
    X('beam', 'stronger', 60, 520, x2=600, y2=160, color=R, id='b2'), tg('stronger', 40, 600, 'stronger signal', bg=R, size=32, id='s'),
    st('instead', 820, 260, 'THEM INSTEAD', 70, R, -8, id='i', **SL)), None),
 # 31 not easy: transmitter, dish, line of sight, knowledge
 (M(ic('transmitter', 40, 60, 'ph:broadcast-bold', 120, ST, id='a'), tg('transmitter', 20, 210, 'transmitter', size=28, id='at'),
    ic('dish', 330, 60, 'mdi:satellite-uplink', 120, ST, id='b'), tg('dish', 330, 210, 'dish', size=28, id='bt'),
    ic('sight', 620, 60, 'ph:eye-bold', 120, ST, id='c'), tg('sight', 560, 210, 'line of sight', size=28, id='ct'),
    ic('knowledge', 920, 60, 'ph:brain-fill', 120, R, id='d'), tg('knowledge', 860, 210, 'expert knowledge', bg=R, size=28, id='dt'),
    st('easy', 360, 400, "NOT EASY", 100, R, -6, id='ne', **SL)), None),
 # 32 not a random kid; knew how TV worked
 (M(ic('kid', 60, 60, 'ph:baby-fill', 160, ST, id='k'), st('prank', 40, 260, 'NOT A PRANK', 70, ST, -8, id='np', **SL),
    ic('knew', 660, 60, 'ph:user-gear-fill', 180, R, id='p'), tg('exactly', 620, 400, 'knew exactly how TV worked', bg=R, size=34, id='t')), None),
 # 33 a year earlier, someone else
 (M(cd('year', 40, 60, '1986', 'ONE YEAR EARLIER', 'ph:calendar-fill', ST, w=480, id='y', **FL),
    tg('catch', 40, 330, 'should have been easy to catch', size=32, id='c'), ic('similar', 760, 80, 'ph:copy-fill', 160, R, id='s')), 'The one who got caught'),
 # 34 Captain Midnight on HBO
 (M(tv(0.02, 40, 30, 600, 'bars', label='HBO · APRIL 1986', id='tv', **FL),
    clip('message', 700, 60, 'ON SCREEN, OVER A MOVIE', '"Good evening HBO, from Captain Midnight"', hi='Captain Midnight', w=580, id='cl', **SD)), None),
 # 35 protesting $12.95 a month
 (M(cd('twelve', 40, 60, '$12.95', 'HBO PER MONTH', 'ph:currency-dollar-bold', R, w=480, id='p', **FL),
    clip('protesting', 640, 60, 'HIS MESSAGE ENDED', '"$12.95/MONTH? NO WAY!"', hi='NO WAY!', w=600, id='cl', **SD),
    ic('protesting', 120, 330, 'ph:megaphone-fill', 150, ST, id='m')), None),
 # 36 traced to a technician in Florida
 (M(ic('satellite', 60, 60, 'mdi:satellite-uplink', 160, ST, id='s'), X('beam', 'traced', 240, 160, x2=780, y2=400, color=G, id='b'),
    X('radar', 'florida', 760, 140, label='FLORIDA', sub='OCALA · SATELLITE UPLINK', id='r'),
    tg('technician', 40, 480, 'a satellite technician: John MacDougall', bg=G, color='#06130D', size=30, id='t')), None),
 # 37 guilty, $5,000, probation
 (M(st('guilty', 40, 60, 'GUILTY', 110, R, -8, id='g', **SL), cd('thousand', 620, 60, '$5,000', 'FINE', 'ph:gavel-fill', ST, w=420, id='f', **FL),
    cd('probation', 620, 320, '1 YEAR', 'PROBATION', 'ph:calendar-x-fill', ST, w=420, id='p', **FL)), None),
 # 38 caught vs not caught
 (M(tg(0.02, 40, 60, 'CAPTAIN MIDNIGHT', size=34, id='a'), st('caught', 40, 150, 'CAUGHT', 90, G, -6, id='c', **SL),
    tg('mask', 700, 60, 'THE MAN IN THE MASK', size=34, id='b'), st('wasnt', 700, 150, '?', 160, R, 6, id='q', **SL),
    X('figure', 'mask', 700, 360, w=420, h=300, id='fg', **FD)), None),
 # 39 FCC investigated, trail went cold
 (M(X('file', 'investigated', 40, 40, w=760, title='FCC · INVESTIGATION', rows=[['CASE', 'SIGNAL INTRUSION'], ['LEADS', None], ['SUSPECTS', None]], id='f', **DR),
    ic('cold', 940, 120, 'ph:snowflake-bold', 170, ST, id='s'), tg('cold', 900, 340, 'the trail went cold', size=32, id='t')), 'Why the trail went cold'),
 # 40 microwave signal leaves no fingerprints
 (M(X('beam', 0.02, 60, 200, x2=760, y2=200, color=G, id='b'), ic('fingerprints', 880, 80, 'ph:fingerprint-bold', 200, ST, id='fp'),
    st('fingerprints', 820, 330, 'NO PRINTS', 80, R, -8, id='np', **SL), tg('stops', 60, 520, 'once it stops: nothing left to trace', size=32, id='t'),
    acts=[{'do': 'out', 'id': 'b', 'at': 'stops'}]), None),
 # 41 no money, no demand, never again
 (M(ic('money', 60, 60, 'ph:money-fill', 140, ST, id='a'), st('money', 20, 230, 'NO MONEY', 46, R, -8, id='a2', **SL),
    ic('demand', 500, 60, 'ph:note-pencil-fill', 140, ST, id='b'), st('demand', 450, 230, 'NO DEMAND', 46, R, 6, id='b2', **SL),
    ic('again', 960, 60, 'ph:arrow-counter-clockwise-bold', 140, ST, id='c'), st('again', 880, 230, 'NEVER AGAIN', 46, R, -6, id='c2', **SL)), None),
 # 42 "not a danger to public safety" -> never a priority
 (M(clip('investigator', 40, 40, 'AN INVESTIGATOR, LATER', '"He wasn\'t a danger to public safety"', hi='danger to public safety', w=660, id='cl', **FL),
    X('file', 'priority', 780, 60, w=460, title='PRIORITY', rows=[['LEVEL', 'LOW']], stamp='LOW', stamp_at='never', id='f', **SD)), None),
 # 43 ★ the clues ourselves
 (M(bg_('clues', 40, 80, 'THE', 130), bg_('clues', 40, 220, '*CLUES*', 160, **SL), ic('look', 640, 140, 'ph:magnifying-glass-bold', 200, R, id='m')), 'The clues'),
 # 44 clue 1: two towers, one night
 (M(X('clue', 'one', 40, 40, n=1, text='Two stations, two towers, one night', w=560, id='c', **DR),
    X('tower', 'stations', 760, 200, name='HANCOCK', w=110, h=440, id='t1', **RS), X('tower', 'towers', 1020, 150, name='SEARS', w=130, h=490, id='t2', **RS),
    X('beam', 'beams', 180, 560, x2=800, y2=200, color=R, id='b1'), X('beam', 'beams', 180, 560, x2=1070, y2=160, color=R, id='b2'),
    tg('knew', 40, 360, 'he knew where both beams were', size=30, id='k')), None),
 # 45 clue 2: cheap costume, expensive tech
 (M(X('clue', 'two', 40, 40, n=2, text='Cheap costume. Serious technology.', w=600, id='c', **DR),
    cd('cheap', 40, 300, '$', 'MASK + METAL', 'ph:mask-happy-fill', ST, w=360, id='a', **FL),
    cd('technology', 460, 300, '$$$$', 'TRANSMISSION GEAR', 'ph:broadcast-bold', R, w=460, id='b', **SL)), None),
 # 46 clue 3: watching live from the city
 (M(X('clue', 'three', 40, 40, n=3, text='He mocked WGN after they cut him off', w=620, id='c', **DR),
    tv('watching', 760, 40, 440, 'sports', label='WATCHING LIVE?', id='tv', **SD), X('skyline', 0.05, 0, 420, w=1320, id='sk', **FD),
    ic('city', 360, 300, 'ph:map-pin-fill', 90, R, id='pin', **DR)), None),
 # 47 clue 4: the brother / flyswatter person
 (M(X('clue', 'four', 40, 40, n=4, text='"My brother has the other one"', w=620, id='c', **DR),
    ic('second', 760, 60, 'ph:users-fill', 170, ST, id='u'), tg('flyswatter', 720, 290, 'the flyswatter person?', bg=R, size=32, id='f')), None),
 # 48 every clue points to an insider
 (M(*[X('clue', 0.02 + k * .05, 40 + (k % 2) * 330, 30 + (k // 2) * 150, n=k + 1, text=t, w=300, id=f'c{k}') for k, t in enumerate(['two towers', 'serious gear', 'watching live', 'a partner?'])],
    st('insider', 760, 80, 'INSIDER?', 100, R, -8, id='i', **SL), tg('forward', 720, 330, 'nobody ever came forward', size=32, id='n')), None),
 # 49 people tried to solve it
 (M(ic('solve', 60, 60, 'ph:users-four-fill', 170, ST, id='u'), ic('years', 320, 60, 'ph:calendar-dots-fill', 150, ST, id='c'),
    bg_('themselves', 40, 300, 'Internet detectives', 90)), 'The theories'),
 # 50 Reddit 2010: local hacker scene
 (M(X('logo', 'reddit', 40, 40, ref='logos:reddit-icon', size=140, id='r'),
    clip('claimed', 260, 40, 'REDDIT · 2010 · A THEORY, NOT PROOF', 'The culprits came from Chicago\'s local hacker scene', hi='hacker scene', w=640, id='cl', **FL),
    ic('equipment', 300, 380, 'ph:cpu-fill', 120, ST, id='e'), ic('city', 480, 380, 'ph:buildings-fill', 120, ST, id='b')), None),
 # 51 never named: no suspect, no witness, no confession
 (M(X('file', 'named', 40, 40, w=820, title='CHICAGO · CASE 001', rows=[['SUSPECT', None], ['WITNESS', None], ['CONFESSION', None]], stamp='NONE', stamp_at='confession', id='f', **DR)), None),
 # 52 the part that should worry you more
 (M(bg_('worry', 40, 120, 'The part that', 100), bg_('worry', 40, 240, 'should *worry* you', 100, **SL), ic('mask', 1000, 300, 'ph:warning-fill', 170, R, id='w')),
  'It happened again'),
 # 53 Feb 2013, Montana, emergency alert
 (M(tv(0.02, 40, 30, 600, 'drama', label='MONTANA · FEB 2013', id='tv', **FL), cd('february', 760, 60, '2013', 'FEBRUARY', 'ph:calendar-fill', ST, w=420, id='y', **SD),
    acts=[TVSW('alert', 'alert')]), None),
 # 54 the dead are rising
 (M(tv(0.02, 40, 30, 700, 'alert', id='tv'), ic('graves', 880, 80, 'ph:skull-fill', 180, W, id='sk'),
    acts=[{'do': 'shake', 'id': 'tv', 'at': 'attacking'}, {'do': 'bob', 'id': 'sk', 'at': 'rising', 'n': 4}]), None),
 # 55 it was a hack of EAS equipment
 (M(st('hack', 40, 60, 'HACKED', 120, R, -8, id='h', **SL), ic('equipment', 600, 60, 'ph:hard-drives-fill', 180, ST, id='e'),
    tg('emergency', 560, 300, 'Emergency Alert System equipment', size=32, id='t')), None),
 # 56 default passwords from public manuals
 (M(X('win', 'machines', 40, 40, w=640, h=300, title='EAS device · login', body='<div style="padding:40px 30px;font:700 30px \'SD Mono\';color:#2A2018">user: admin<br>pass: ●●●●●●</div>', id='lg', **FL),
    ic('manuals', 780, 60, 'ph:book-open-text-fill', 170, ST, id='m'), tg('printed', 760, 280, 'the password was in the public manual', bg=R, size=28, id='p', **SL),
    st('default', 200, 420, 'DEFAULT PASSWORD', 70, R, -6, id='d', **SL)), None),
 # 57 never caught either
 (M(X('file', 'people', 40, 40, w=760, title='ZOMBIE ALERT · 2013', rows=[['SUSPECTS', None], ['ARRESTS', None]], stamp='NEVER CAUGHT', stamp_at='caught', id='f', **DR)), None),
 # 58 trusted message, password anyone could look up
 (M(cd('millions', 40, 60, 'MILLIONS', 'WOULD TRUST IT', 'ph:users-three-fill', ST, w=500, id='m', **FL),
    ic('password', 700, 60, 'ph:password-fill', 160, R, id='p'), tg('anyone', 640, 280, 'a password anyone could look up', bg=R, size=30, id='a')), None),
 # 59 most hacks need one unlocked door
 (M(bg_('genius', 40, 60, 'No genius needed.', 96), ic('door', 160, 260, 'ph:door-open-fill', 220, R, id='d'),
    tg('nobody', 500, 360, 'just one door that nobody locked', bg=R, size=36, id='t', **SL)), 'The lesson'),
 # 60 check your router tonight
 (M(ic('router', 60, 60, 'ph:wifi-high-bold', 170, G, id='r'), tg('tonight', 40, 280, 'CHECK TONIGHT', bg=G, color='#06130D', size=34, id='t', **SL),
    X('win', 'admin', 460, 40, w=760, h=330, title='192.168.1.1 · router admin', body='<div style="padding:34px 30px;font:700 30px \'SD Mono\';color:#2A2018">admin password: admin<br><span style="color:#E5383B">→ change it</span></div>', id='w', **SD),
    st('change', 520, 420, 'CHANGE IT', 90, G, -6, id='c', **SL)), None),
 # 61 TV is digital and protected today
 (M(ic('digital', 60, 60, 'ph:lock-key-fill', 170, G, id='l'), tg('protected', 40, 290, 'digital, encrypted links', bg=G, color='#06130D', size=32, id='t'),
    tv('harder', 700, 40, 520, 'bars', label='TODAY', id='tv', **SD)), None),
 # 62 he's still out there... or not
 (M(X('figure', 0.02, 40, 40, w=640, h=480, id='fg', **FD), bg_('somewhere', 760, 120, 'Still out', 100), bg_('somewhere', 760, 240, '*there*…', 100),
    tg('isnt', 760, 400, "…or maybe he isn't", size=34, id='t')), None),
 # 63 two stations, two hijacks, one night, no answer
 (M(cd('stations', 40, 60, '2', 'STATIONS', 'ph:television-simple-fill', ST, w=300, id='a', **FL), cd('hijacks', 380, 60, '2', 'HIJACKS', 'ph:broadcast-bold', R, w=300, id='b', **FL),
    cd('night', 720, 60, '1', 'NIGHT', 'ph:moon-fill', ST, w=300, id='c', **FL), st('answer', 300, 360, 'NO ANSWER', 110, R, -6, id='n', **SL)), None),
 # 64 ★ detective question
 (M(X('file', 'detective', 40, 40, w=760, title='YOUR THEORY', rows=[['SUSPECT', '__________'], ['MOTIVE', '__________']], id='f', **DR),
    ic('comments', 140, 420, 'ph:chat-circle-dots-fill', 150, R, id='c')), None),
 # 65 subscribe
 ({'type': 'end', 'sub': 'More tech mysteries, decoded.'}, None),
]

assert len(V) == len(e['beats']), (len(V), len(e['beats']))
bad = []
for i, (v, _) in enumerate(V):
    if v.get('type') != 'mix':
        continue
    words = {re.sub(r'[^a-z0-9]', '', w.lower()) for w in e['beats'][i]['text'].split()}
    for it in v['els'] + v['acts']:
        for key in ('at', 'stamp_at'):
            a = it.get(key)
            if isinstance(a, str) and a not in words:
                bad.append((i, key, a))
assert not bad, bad
for b, (v, chp) in zip(e['beats'], V):
    b['v'] = v
    if chp:
        b['chapter'] = chp
    else:
        b.pop('chapter', None)
f.write_text(json.dumps(e, indent=1, ensure_ascii=False))
print('beats', len(V))
