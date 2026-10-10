// Render SVG files to PNG with headless Chrome. Called by svg_cards.py.
const { chromium } = require('playwright-core');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true,
  });
  const page = await browser.newPage();
  for (const [src, dst] of JSON.parse(process.argv[2])) {
    await page.setContent('<html><body style="margin:0">' + fs.readFileSync(src, 'utf8') + '</body></html>');
    await page.locator('svg').screenshot({ path: dst });
  }
  await browser.close();
})();
