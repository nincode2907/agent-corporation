import { createRequire } from 'node:module';
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';

const root = process.env.UI_LENS_ROOT;
if (!root) throw new Error('Set UI_LENS_ROOT to the existing local UI Lens checkout.');
const require = createRequire(path.join(root, 'package.json'));
const { chromium } = require('playwright');
const baseUrl = process.env.APP_BASE_URL ?? 'http://127.0.0.1:15500';
const out = process.env.AUDIT_OUTPUT;
if (!out) throw new Error('Set AUDIT_OUTPUT to the sprint evidence directory.');

const screens = ['overview', 'playground', 'office', 'work', 'inspector', 'replay', 'organization', 'approvals', 'settings'];
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
const result = { baseUrl, browserVersion: browser.version(), viewport: { width: 390, height: 844 }, screens: [], keyboard: null };

try {
  await page.goto(baseUrl, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1500);
  await page.keyboard.press('Tab');
  const firstFocus = await page.evaluate(() => ({
    tag: document.activeElement?.tagName,
    text: document.activeElement?.textContent?.trim(),
    href: document.activeElement?.getAttribute('href'),
  }));
  await page.keyboard.press('Enter');
  await page.waitForTimeout(100);
  result.keyboard = { firstFocus, skipTargetFocused: await page.evaluate(() => document.activeElement?.id === 'main-content') };

  for (const id of screens) {
    await page.locator(`a.nav-link[href="#${id}"]`).click();
    await page.locator(`a.nav-link[href="#${id}"].active`).waitFor();
    await page.waitForTimeout(250);
    result.screens.push(await page.evaluate((screenId) => {
      const rootWidth = document.documentElement.clientWidth;
      const offending = [...document.body.querySelectorAll('*')]
        .filter((element) => {
          if (element.scrollWidth <= element.clientWidth + 1) return false;
          const style = getComputedStyle(element);
          return !['auto', 'scroll'].includes(style.overflowX);
        })
        .map((element) => ({ tag: element.tagName, className: String(element.className).slice(0, 100), scrollWidth: element.scrollWidth, clientWidth: element.clientWidth }))
        .slice(0, 8);
      return {
        id: screenId,
        viewportWidth: rootWidth,
        documentWidth: document.documentElement.scrollWidth,
        bodyWidth: document.body.scrollWidth,
        pageHorizontalOverflow: document.documentElement.scrollWidth > rootWidth + 1,
        horizontalScrollRegions: [...document.querySelectorAll('*')]
          .filter((el) => el.scrollWidth > el.clientWidth + 1 && ['auto', 'scroll'].includes(getComputedStyle(el).overflowX))
          .map((el) => ({ className: String(el.className).slice(0, 80), scrollWidth: el.scrollWidth, clientWidth: el.clientWidth }))
          .slice(0, 5),
        nonScrollingOverflowCandidates: offending,
        heading: document.querySelector('main h1')?.textContent?.trim() ?? null,
      };
    }, id));
  }
} finally {
  await browser.close();
}

await mkdir(path.dirname(out), { recursive: true });
await writeFile(out, `${JSON.stringify(result, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(result, null, 2));
