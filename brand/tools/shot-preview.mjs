import { chromium } from 'playwright';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
const here = dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 900, height: 600 }, deviceScaleFactor: 2 });
await p.goto('file://' + join(here, 'preview.html'));
await p.locator('.wrap').screenshot({ path: join(here, '..', 'instagram-preview.png') });
await b.close();
