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
const viewports = [{ width: 1440, height: 900 }, { width: 390, height: 844 }];
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: viewports[0] });
const page = await context.newPage();
const requests = [];
page.on('request', request => {
  const url = new URL(request.url());
  requests.push({ method: request.method(), path: url.pathname, hasCursor: url.searchParams.has('cursor'), hasLastEventId: Boolean(request.headers()['last-event-id']) });
});
page.on('pageerror', error => requests.push({ kind: 'pageerror', message: error.message }));
const manifest = {
  baseUrl,
  browserVersion: browser.version(),
  viewports,
  auth: { attempted: true, succeeded: false, secretPrintedOrStored: false, loggedOut: false },
  screenshots: [],
  flows: [],
  stateChecks: [],
  requests,
};
let releaseHeld;

async function saveScreenshot(name, viewport = viewports[0]) {
  await page.setViewportSize(viewport);
  await page.addStyleTag({ content: `
    /* Redaction for mentor-review package; keeps layout while hiding historical user text and opaque identifiers. */
    .playground-user p, .playground-assistant > p, .playground-assistant details,
    .inspector-summary code, .inspector-events li code, .replay-timeline code { filter: blur(7px) !important; }
  ` });
  const file = path.join(out, 'screenshots', `${name}`, `${viewport.width}x${viewport.height}.png`);
  await mkdir(path.dirname(file), { recursive: true });
  await page.screenshot({ path: file, fullPage: true });
  const state = await page.evaluate(() => ({
    documentWidth: document.documentElement.scrollWidth,
    viewportWidth: document.documentElement.clientWidth,
    horizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
    heading: document.querySelector('main h1')?.textContent?.trim() ?? null,
  }));
  manifest.screenshots.push({ screen: name, viewport, screenshot: path.relative(out, file).replaceAll('\\', '/'), ...state });
}

async function navigate(id) {
  await page.locator(`a.nav-link[href="#${id}"]`).click();
  await page.locator(`a.nav-link[href="#${id}"].active`).waitFor();
  await page.waitForTimeout(300);
}

try {
  await page.goto(`${baseUrl}/#playground`, { waitUntil: 'domcontentloaded' });
  await page.getByLabel('Secret Owner local').fill(secret);
  await page.getByRole('button', { name: 'Đăng nhập Owner' }).click();
  await page.getByRole('button', { name: 'Đăng nhập Owner' }).waitFor({ state: 'detached' });
  manifest.auth.succeeded = true;
  await page.waitForTimeout(400);

  // Authenticated screenshot inventory: nine screens at both required viewports.
  for (const id of screens) {
    await navigate(id);
    for (const viewport of viewports) await saveScreenshot(id, viewport);
  }

  // Read-only journey inventory; no approval decision, profile save, grant or message is submitted.
  const flows = [
    ['dashboard-office-inspector', ['overview', 'office', 'inspector']],
    ['dashboard-work-approval', ['overview', 'work', 'approvals']],
    ['playground-profile-grant-history', ['playground']],
    ['inspector-replay-source', ['inspector', 'replay']],
    ['organization-employee-list', ['organization']],
  ];
  for (const [id, routeIds] of flows) {
    for (const routeId of routeIds) await navigate(routeId);
    manifest.flows.push({ id, routes: routeIds, actions: 'authenticated navigation and read-only inspection' });
  }

  // Replay filter/seek/reload is a local projection plus GET-only event-feed reload.
  await navigate('replay');
  const eventReadsBeforeReplayActions = requests.filter(item => item.path === '/api/v1/events' || item.path === '/api/v1/events/stream').length;
  const replayOptions = await page.locator('#replay-run option').count();
  if (replayOptions > 1) await page.locator('#replay-run').selectOption({ index: 1 });
  const replaySlider = page.locator('#replay-position');
  if (await replaySlider.count()) { await replaySlider.focus(); await replaySlider.press('End'); }
  await page.getByRole('button', { name: 'Tải lại từ đầu' }).click();
  const replayReloadRecovered = await page.waitForFunction(() => document.querySelector('.observatory-status')?.textContent?.includes('Đã kết nối'), null, { timeout: 15000 }).then(() => true).catch(() => false);
  const eventReadsAfterReplayActions = requests.filter(item => item.path === '/api/v1/events' || item.path === '/api/v1/events/stream').length;
  manifest.flows.push({ id: 'replay-filter-seek-reload', routes: ['replay'], runOptions: replayOptions, sliderPresent: Boolean(await replaySlider.count()), reloadRecovered: replayReloadRecovered, eventReadRequests: eventReadsAfterReplayActions - eventReadsBeforeReplayActions, businessWrites: requests.filter(item => item.method !== 'GET' && !['/api/v1/owner/login', '/api/v1/owner/logout'].includes(item.path)).map(item => item.path) });

  // Settings hosts the Owner runtime/event feed used for connection-state checks.
  await navigate('settings');
  const connection = page.locator('.runtime-events [role="status"]');
  await connection.waitFor({ state: 'visible', timeout: 10000 });
  await page.waitForFunction(() => document.querySelector('.runtime-events [role="status"]')?.textContent?.includes('Đã kết nối'), null, { timeout: 15000 });

  // Cursor failure is injected only at the read endpoint. It verifies UI handling; backend cursor variants
  // are exercised independently against the disposable PostgreSQL test database.
  let cursorGapObserved = false;
  let cursorReadCount = 0;
  await page.route('**/api/v1/events**', async route => {
    const pathname = new URL(route.request().url()).pathname;
    if (pathname === '/api/v1/events') {
      cursorReadCount++;
      await route.fulfill({ status: 409, contentType: 'application/json', body: JSON.stringify({ detail: { code: 'event_gap', message: 'Fixture cursor gap.' } }) });
    } else {
      await route.continue();
    }
  });
  await page.getByRole('button', { name: 'Tải lại từ dữ liệu đã lưu' }).click();
  await page.waitForFunction(() => document.querySelector('.runtime-events [role="status"]')?.textContent?.includes('Có khoảng trống'), null, { timeout: 10000 }).catch(() => {});
  const cursorStatusText = await page.locator('.runtime-events [role="status"]').textContent();
  cursorGapObserved = cursorStatusText?.includes('Có khoảng trống') ?? false;
  manifest.stateChecks.push({ state: 'cursor-gap-read-error', observed: cursorGapObserved, injection: 'HTTP 409 read-only endpoint interception', interceptedReads: cursorReadCount, statusText: cursorStatusText });
  await page.unroute('**/api/v1/events**');
  if (cursorGapObserved) await saveScreenshot('states/cursor-gap');
  await page.getByRole('button', { name: 'Tải lại từ dữ liệu đã lưu' }).click();
  const cursorReloadRecovered = await page.waitForFunction(() => document.querySelector('.runtime-events [role="status"]')?.textContent?.includes('Đã kết nối'), null, { timeout: 15000 }).then(() => true).catch(() => false);
  manifest.stateChecks.push({ state: 'cursor-gap-reload-recovery', observed: cursorReloadRecovered });

  // Exercise browser-offline state, then restore the network and confirm feed recovery.
  await page.route('**/api/v1/events/stream**', route => route.abort());
  await context.setOffline(true);
  await page.getByRole('button', { name: 'Tải lại từ dữ liệu đã lưu' }).click().catch(() => {});
  const offlineNavigatorValue = await page.evaluate(() => navigator.onLine);
  const offlineObserved = await page.waitForFunction(() => document.querySelector('.runtime-events [role="status"]')?.textContent?.includes('Mất kết nối'), null, { timeout: 10000 }).then(() => true).catch(() => false);
  const offlineStatusText = await page.locator('.runtime-events [role="status"]').textContent();
  manifest.stateChecks.push({ state: 'browser-offline', observed: offlineObserved, navigatorOnLine: offlineNavigatorValue, statusText: offlineStatusText, method: 'Chromium context.setOffline(true)' });
  if (offlineObserved) await saveScreenshot('states/offline');
  await context.setOffline(false);
  await page.unroute('**/api/v1/events/stream**');
  await page.getByRole('button', { name: 'Tải lại từ dữ liệu đã lưu' }).click();
  const restored = await page.waitForFunction(() => document.querySelector('.runtime-events [role="status"]')?.textContent?.includes('Đã kết nối'), null, { timeout: 15000 }).then(() => true).catch(() => false);
  manifest.stateChecks.push({ state: 'offline-recovery', observed: restored, method: 'Chromium context.setOffline(false)' });

  // Hold the EventSource connection open without heartbeats. Initial saved-page read remains available;
  // advancing the persisted heartbeat timeout must transition the UI to stale, then the stream is restored.
  let heldFinishedResolve;
  const heldFinished = new Promise(resolve => { heldFinishedResolve = resolve; });
  let streamHeld = false;
  await page.route('**/api/v1/events/stream**', async route => {
    streamHeld = true;
    await new Promise(resolve => { releaseHeld = resolve; });
    try { await route.continue(); } finally { heldFinishedResolve(); }
  });
  await page.getByRole('button', { name: 'Tải lại từ dữ liệu đã lưu' }).click();
  await page.waitForFunction(() => document.querySelector('.runtime-events [role="status"]')?.textContent?.includes('Đã kết nối'), null, { timeout: 10000 }).catch(() => {});
  // route callback sets a Node variable; wait through bounded polling without recording the cursor or body.
  for (let attempt = 0; attempt < 40 && !streamHeld; attempt++) await page.waitForTimeout(100);
  await page.waitForTimeout(500);
  await page.evaluate(() => {
    const originalNow = Date.now.bind(Date);
    let offset = 0;
    Date.now = () => originalNow() + offset;
    window.__advanceStabilizationClock = milliseconds => { offset += milliseconds; };
    window.__advanceStabilizationClock(31000);
  });
  await page.waitForTimeout(5500);
  const staleStatusText = await page.locator('.runtime-events [role="status"]').textContent();
  const staleObserved = staleStatusText?.includes('Dữ liệu đã cũ') ?? false;
  manifest.stateChecks.push({ state: 'stalled-heartbeat-stale', observed: staleObserved, statusText: staleStatusText, eventSourceRequestHeld: streamHeld, method: 'hold SSE request and advance browser Date.now by 31 seconds' });
  if (staleObserved) await saveScreenshot('states/stale');
  releaseHeld?.();
  await Promise.race([heldFinished, page.waitForTimeout(5000)]);
  await page.unroute('**/api/v1/events/stream**');
  const heartbeatRecovered = await page.waitForFunction(() => document.querySelector('.runtime-events [role="status"]')?.textContent?.includes('Đã kết nối'), null, { timeout: 15000 }).then(() => true).catch(() => false);
  manifest.stateChecks.push({ state: 'stalled-heartbeat-recovery', observed: heartbeatRecovered });

  // Product logout revokes the temporary browser Owner session.
  await navigate('settings');
  await page.getByRole('button', { name: 'Đăng xuất' }).click();
  await page.getByLabel('Secret Chủ tịch local').waitFor({ state: 'visible' });
  manifest.auth.loggedOut = true;
} finally {
  releaseHeld?.();
  await context.close();
  await browser.close();
}

await mkdir(out, { recursive: true });
await writeFile(path.join(out, 'manifest.json'), `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({ auth: manifest.auth, screenshotCount: manifest.screenshots.length, stateChecks: manifest.stateChecks, pageErrors: requests.filter(item => item.kind === 'pageerror') }, null, 2));
