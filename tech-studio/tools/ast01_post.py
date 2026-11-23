"""ast01: mount the rendered ChatGPT-style exchange (hf/ast01-chat -> assets/chat.mp4) after every regeneration.
Cream version: the clip sits in a phone frame on the cream background; captions stay visible underneath."""
import os
from pathlib import Path
p = Path(__file__).resolve().parent.parent / 'hf/ast01-short/index.html'
h = p.read_text()
if 'id="chatclip"' not in h:
    if os.environ.get('THEME') == 'cream':
        st = ('position:absolute; left:232px; top:130px; width:616px; height:1095px; z-index:6; object-fit:cover; border:14px solid #2A2018; '
              'border-radius:72px; box-shadow:0 40px 80px rgba(74,50,28,.30)')
    else:
        st = 'position:absolute; left:0; top:0; width:1080px; height:1920px; z-index:6; object-fit:cover'
    v = f'<video id="chatclip" class="clip" src="assets/chat.mp4" data-start="17.85" data-duration="9.45" data-track-index="30" muted playsinline style="{st}"></video>\n      '
    h = h.replace('<div id="caps"', v + '<div id="caps"', 1)
    p.write_text(h)
print('chat clip mounted')
