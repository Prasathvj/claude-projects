"""Copy finished videos, thumbnails and upload packages into release/ (tracked in git), in posting order."""
import shutil, subprocess, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
OUT, REL, SCR = R/'out', R/'release', pathlib.Path(__import__('sys').argv[1])
# (folder, episode id, video file, thumbnail png, schedule IST, status)
PLAN = [
 ('00_ep01_long',  'ep01', 'TechDecoded_ep01_long.mp4',  OUT/'thumb_long_cream.jpg', 'Uploaded', 'Live'),
 ('00_ep01_short', 'ep01', 'TechDecoded_ep01_short.mp4', OUT/'thumb_short_cream.jpg', 'Uploaded', 'Live'),
 ('01_news02', 'news02', None, None, 'Mon 23 Nov 2026, 6:30 PM', 'Schedule'),
 ('02_news01', 'news01', None, None, 'Tue 24 Nov 2026, 6:30 PM', 'Schedule'),
 ('03_tip01',  'tip01',  None, None, 'Wed 25 Nov 2026, 6:30 PM', 'Schedule'),
 ('04_job02',  'job02',  None, None, 'Thu 26 Nov 2026, 6:30 PM', 'Schedule'),
 ('05_sat01',  'sat01',  None, None, 'Fri 27 Nov 2026, 6:30 PM', 'Schedule'),
 ('06_job01',  'job01',  None, None, 'Sat 28 Nov 2026, 12:30 PM', 'Schedule'),
 ('07_goog01', 'goog01', None, None, 'Sun 29 Nov 2026, 12:30 PM', 'Schedule'),
 ('08_job03',  'job03',  None, None, 'Mon 30 Nov 2026, 6:30 PM', 'Schedule'),
 ('09_net01',  'net01',  None, None, 'Tue 1 Dec 2026, 6:30 PM', 'Schedule'),
 ('10_robo01', 'robo01', None, None, 'Sun 29 Nov 2026, 12:30 PM', 'Schedule'),
 ('12_upi01', 'upi01', None, None, 'Mon 30 Nov 2026, 6:30 PM', 'Schedule'),
 ('13_ai01', 'ai01', None, None, 'Tue 1 Dec 2026, 6:30 PM', 'Schedule'),
 ('14_face01', 'face01', None, None, 'Thu 3 Dec 2026, 6:30 PM', 'Schedule'),
 ('15_del01', 'del01', None, None, 'Fri 4 Dec 2026, 6:30 PM', 'Schedule'),
 ('16_pay01', 'pay01', None, None, 'Sun 6 Dec 2026, 12:30 PM', 'Schedule'),
 ('11_ep02_long', 'ep02', 'TechDecoded_ep02_long.mp4', OUT/'thumb_ep02_long.jpg', 'Wed 2 Dec 2026, 6:30 PM', 'Schedule'),
 ('17_ep03_long', 'ep03', 'TechDecoded_ep03_long.mp4', SCR/'thumb_ep03_long.png', 'Sat 5 Dec 2026, 12:30 PM', 'Schedule'),
 ('18_ep04_long', 'ep04', 'TechDecoded_ep04_long.mp4', SCR/'thumb_ep04_long.png', 'Tue 8 Dec 2026, 6:30 PM', 'Schedule'),
]
for folder, ep, vid, thumb, when, status in PLAN:
    d = REL/folder; d.mkdir(parents=True, exist_ok=True)
    vid = vid or f'TechDecoded_{ep}_short.mp4'
    shutil.copy2(OUT/vid, d/vid)
    src = thumb or SCR/f'thumb_{ep}.png'
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-q:v','3',str(d/'thumbnail.jpg')], check=True)
    shutil.copy2(R/'episodes'/ep/'UPLOAD.md', d/'UPLOAD.md')
print('ok')
