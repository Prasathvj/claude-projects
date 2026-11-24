// Render hf/thumbs/v2_<id>.html at 4K (1920x1080 @2x) for crisp edges; tools/thumbs_v2_post.sh downsizes.
// Needs: python3 -m http.server 8765 in tech-studio/hf.   Usage: node tools/thumbs_v2_render.cjs [id ...]
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const ids = process.argv.slice(2).length ? process.argv.slice(2)
    : fs.readdirSync('hf/thumbs').filter((f) => /^v2_.*\.html$/.test(f)).map((f) => f.slice(3, -5));
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 });
  fs.mkdirSync('hf/thumbs/out', { recursive: true });
  for (const id of ids) {
    await p.goto(`http://localhost:8765/thumbs/v2_${id}.html`, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(300);
    await p.screenshot({ path: `hf/thumbs/out/v2_${id}_4k.png` });
    console.log('rendered', id);
  }
  await b.close();
})();
