const { chromium } = require('playwright'); const fs = require('node:fs');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('http://localhost:8765/job02-short/max_layer.html'); await p.evaluate(() => init()); await p.waitForTimeout(600);
  const dur = await p.evaluate(() => P.dur); const n = Math.ceil(dur * 30);
  fs.mkdirSync('maxframes', { recursive: true });
  for (let i = 0; i < n; i++) { await p.evaluate((i) => frame(i), i); await p.screenshot({ path: `maxframes/m${String(i).padStart(4, '0')}.png`, omitBackground: true }); }
  await b.close(); console.log('frames', n);
})();
