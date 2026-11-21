const { chromium } = require('playwright'); const fs = require('node:fs');
(async () => {
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1080 } });
await p.goto('http://localhost:8765/host/act.html', { waitUntil: 'load' });
await p.evaluate(() => init()); await p.waitForTimeout(500);
fs.mkdirSync('frames', { recursive: true });
const n = Math.floor(10.37 * 30);
for (let i = 0; i < n; i++) { await p.evaluate((i) => frame(i), i); await p.screenshot({ path: `frames/f${String(i).padStart(4, '0')}.jpg`, quality: 92 }); }
await b.close();
})();
