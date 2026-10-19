import { createRequire } from 'node:module';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';

const root = process.env.UI_LENS_ROOT;
const baseUrl = process.env.APP_BASE_URL ?? 'http://127.0.0.1:15500';
const out = process.env.AUTH_REVIEW_OUTPUT;
if (!root || !out) throw new Error('UI_LENS_ROOT and AUTH_REVIEW_OUTPUT are required.');
const require = createRequire(path.join(root, 'package.json'));
const { chromium } = require('playwright');
const secret = (await readFile(path.resolve('.local/owner-secret'), 'utf8')).trim();
if (!secret) throw new Error('Existing Owner secret file is empty.');

const screens = ['overview', 'playground', 'office', 'work', 'inspector', 'replay', 'organization', 'approvals', 'settings'];
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await context.newPage();
const requests = [];
page.on('request', request => {
  const url = new URL(request.url());
  const headers = request.headers();
  requests.push({ method: request.method(), path: url.pathname, hasCursor: url.searchParams.has('cursor'), hasLastEventId: Boolean(headers['last-event-id']) });
});
page.on('pageerror', error => requests.push({ kind: 'pageerror', message: error.message }));
const manifest = {
  baseUrl,
  browserVersion: browser.version(),
  viewports: [{ width: 1440, height: 900 }, { width: 390, height: 844 }],
  auth: { attempted: true, succeeded: false, secretPrintedOrStored: false },
  screens: [],
  networkInterruption: { attempted: false },
  requests,
};

try {
  await page.goto(`${baseUrl}/#playground`, { waitUntil: 'domcontentloaded' });
  await page.getByLabel('Secret Owner local').fill(secret);
  await page.getByRole('button', { name: 'Đăng nhập Owner' }).click();
  await page.getByRole('button', { name: 'Đăng nhập Owner' }).waitFor({ state: 'detached' });
  manifest.auth.succeeded = true;
  await page.waitForTimeout(300);

  for (const id of screens) {
    for (const viewport of manifest.viewports) {
      await page.setViewportSize(viewport);
      await page.locator(`a.nav-link[href="#${id}"]`).click();
      await page.locator(`a.nav-link[href="#${id}"].active`).waitFor();
      await page.waitForTimeout(300);
      const heading = (await page.locator('main h1').textContent())?.trim() ?? null;
      const file = path.join(out, 'screenshots', id, `${viewport.width}x${viewport.height}.png`);
      await mkdir(path.dirname(file), { recursive: true });
      await page.screenshot({ path: file, fullPage: true });
      const state = await page.evaluate(() => ({
        documentWidth: document.documentElement.scrollWidth,
        viewportWidth: document.documentElement.clientWidth,
        horizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
        scrollWidthCandidates: [...document.querySelectorAll('body *')]
          .filter((el) => el.scrollWidth > el.clientWidth + 1)
          .slice(0, 12)
          .map((el) => { const rect = el.getBoundingClientRect(); const style = getComputedStyle(el); return { tag: el.tagName, className: String(el.className).slice(0, 80), left: Math.round(rect.left), right: Math.round(rect.right), clientWidth: el.clientWidth, scrollWidth: el.scrollWidth, overflowX: style.overflowX, text: el.innerText?.trim().slice(0, 80) ?? '' }; }),
        overflowingElements: [...document.querySelectorAll('body *')]
          .filter((el) => {
            const rect = el.getBoundingClientRect();
            const style = getComputedStyle(el);
            return rect.width > 0 && rect.right > document.documentElement.clientWidth + 1
              && !['auto', 'scroll'].includes(style.overflowX)
              && !el.closest('.primary-nav');
          })
          .slice(0, 10)
          .map((el) => {
            const rect = el.getBoundingClientRect();
            return { tag: el.tagName, id: el.id, className: String(el.className).slice(0, 100), left: Math.round(rect.left), right: Math.round(rect.right), width: Math.round(rect.width), text: el.innerText?.trim().slice(0, 100) ?? '' };
          }),
        inspectorControlChain: location.hash === '#inspector' ? (() => {
          let node = document.querySelector('#inspector-run');
          const chain = [];
          while (node && chain.length < 8) {
            const rect = node.getBoundingClientRect();
            const style = getComputedStyle(node);
            chain.push({ tag: node.tagName, className: String(node.className).slice(0, 80), width: Math.round(rect.width), left: Math.round(rect.left), computedWidth: style.width, minWidth: style.minWidth, maxWidth: style.maxWidth, display: style.display, gridColumns: style.gridTemplateColumns, flex: style.flex });
            node = node.parentElement;
          }
          return chain;
        })() : [],
        visibleText: document.querySelector('main')?.innerText?.slice(0, 1800) ?? '',
      }));
      manifest.screens.push({ id, viewport, heading, screenshot: path.relative(out, file).replaceAll('\\', '/'), ...state });
    }
  }

  try {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.locator('a.nav-link[href="#playground"]').click();
    await page.waitForTimeout(300);
    await page.route('**/api/v1/events/stream**', route => route.abort());
    await page.locator('a.nav-link[href="#settings"]').click();
    await page.locator('.runtime-events').waitFor();
    await page.waitForFunction(() => document.querySelector('.runtime-events [role="status"]')?.textContent?.includes('Đã kết nối'), null, { timeout: 15000 });
    const eventIdsBefore = await page.locator('.runtime-events li code').allTextContents();
    manifest.networkInterruption.attempted = true;
    manifest.networkInterruption.eventIdsBefore = eventIdsBefore;
    await page.waitForFunction(() => document.querySelector('.runtime-events [role="status"]')?.textContent?.includes('Đang kết nối lại'), null, { timeout: 10000 });
    manifest.networkInterruption.interruptedStateObserved = true;
    manifest.networkInterruption.failedStreamAttempts = requests.filter(item => item.path === '/api/v1/events/stream').length;
    const streamResponse = page.waitForResponse(response => response.url().includes('/api/v1/events/stream') && response.status() === 200, { timeout: 15000 });
    await page.unroute('**/api/v1/events/stream**');
    await streamResponse;
    await page.waitForFunction(() => document.querySelector('.runtime-events [role="status"]')?.textContent?.includes('Đã kết nối'), null, { timeout: 15000 });
    const eventIdsAfter = await page.locator('.runtime-events li code').allTextContents();
    manifest.networkInterruption.eventIdsAfter = eventIdsAfter;
    manifest.networkInterruption.reconnected = true;
    manifest.networkInterruption.sameOrderedEvents = JSON.stringify(eventIdsBefore) === JSON.stringify(eventIdsAfter);
  } catch (error) {
    manifest.networkInterruption.error = error instanceof Error ? error.message : String(error);
    await page.unroute('**/api/v1/events/stream**').catch(() => {});
  }

  // End the temporary authenticated browser session through the product's own logout action.
  await page.locator('a.nav-link[href="#settings"]').click();
  await page.getByRole('button', { name: 'Đăng xuất' }).click();
  await page.getByLabel('Secret Chủ tịch local').waitFor({ state: 'visible' });
  manifest.auth.loggedOut = true;
} finally {
  await context.close();
  await browser.close();
}

await mkdir(out, { recursive: true });
await writeFile(path.join(out, 'manifest.json'), `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({
  auth: manifest.auth,
  browserVersion: manifest.browserVersion,
  screens: manifest.screens.map(({ id, viewport, heading, horizontalOverflow }) => ({ id, viewport, heading, horizontalOverflow })),
  requests: manifest.requests,
}, null, 2));
