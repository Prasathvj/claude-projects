// Render the TechDecoded தமிழ் brand kit (profile picture, banner, watermark) from hf/brand-ta/brand_ta.html.
// Usage: node tools/brand_ta.cjs   -> brand/tamil/*.png
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const page = 'file://' + path.resolve(__dirname, '../hf/brand-ta/brand_ta.html');
  const out = path.resolve(__dirname, '../brand/tamil') + '/';
  for (const [m, w, h, f, tr] of [['avatar', 800, 800, 'profile_800x800.png', false], ['banner', 2560, 1440, 'banner_2560x1440.png', false], ['watermark', 150, 150, 'watermark_150x150.png', true]]) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    p.on('pageerror', e => console.error('pageerror', e.message));
    await p.goto(`${page}?m=${m}`);
    await p.waitForFunction(() => window.READY === true);
    await p.waitForTimeout(400);
    await p.screenshot({ path: out + f, omitBackground: tr });
    await p.close();
    console.log(f);
  }
  await b.close();
})();
