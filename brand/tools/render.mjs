// Renders every SVG in ../svg to a PNG in ../png using the headless Chromium.
import { chromium } from 'playwright';
import { readdirSync, readFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const svgDir = join(here, '..', 'svg');
const pngDir = join(here, '..', 'png');
mkdirSync(pngDir, { recursive: true });

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined });
const page = await browser.newPage();
for (const file of readdirSync(svgDir).filter((f) => f.endsWith('.svg'))) {
  const svg = readFileSync(join(svgDir, file), 'utf8');
  const [, w, h] = svg.match(/width="(\d+)" height="(\d+)"/);
  await page.setViewportSize({ width: +w, height: +h });
  await page.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
  const out = join(pngDir, file.replace('.svg', '.png'));
  await page.screenshot({ path: out, omitBackground: true, clip: { x: 0, y: 0, width: +w, height: +h } });
  console.log('rendered', out);
}
await browser.close();
