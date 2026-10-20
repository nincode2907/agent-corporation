import { createRequire } from 'node:module';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';

const repo = process.cwd();
const webRoot = path.join(repo, 'apps/web');
const playwrightRoot = path.resolve(process.env.PLAYWRIGHT_MODULE_ROOT ?? webRoot);
const require = createRequire(path.join(playwrightRoot, 'package.json'));
const { chromium } = require('playwright');
const baseUrl = process.env.APP_BASE_URL ?? 'http://127.0.0.1:15500';
const output = path.resolve(process.env.AUTH_REVIEW_OUTPUT ?? 'docs/reviews/stabilization-03/evidence');
const secret = (await readFile(path.join(repo, '.local/owner-secret'), 'utf8')).trim();
if (!secret) throw new Error('Owner secret is empty.');

const browser = await chromium.launch({ headless: true,
  ...(process.env.PLAYWRIGHT_EXECUTABLE ? { executablePath: process.env.PLAYWRIGHT_EXECUTABLE } : {}) });
const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await context.newPage();
  const requests = [];
const interceptions = [];
const pageErrors = [];
page.on('request', request => {
  const url = new URL(request.url());
  requests.push({ method: request.method(), path: url.pathname });
});
page.on('pageerror', error => pageErrors.push(error.message));
await mkdir(path.join(output, 'screenshots'), { recursive: true });

async function capture(name, viewport) {
  await page.setViewportSize(viewport);
  await page.evaluate(() => window.scrollTo({ top: 0, left: 0, behavior: 'instant' }));
  await page.waitForTimeout(100);
  await page.addStyleTag({ content: `
    .playground-user p, .playground-assistant > p, .playground-assistant details,
    .inspector-summary code, .inspector-events li code, .inspector-events li p,
    .replay-timeline code, .replay-timeline li p, .runtime-scope code { filter: blur(8px) !important; }
  ` });
  const file = path.join(output, 'screenshots', `${name}-${viewport.width}x${viewport.height}.png`);
  await page.screenshot({ path: file, fullPage: false });
  return path.relative(output, file).replaceAll('\\', '/');
}

async function navigate(id) {
  await page.locator(`a.nav-link[href="#${id}"]`).click();
  await page.locator(`a.nav-link[href="#${id}"].active`).waitFor();
  await page.waitForTimeout(250);
  if (await page.locator('input[type="password"]').count()) throw new Error(`Owner session was lost on ${id}.`);
}

const result = {
  baseUrl,
  viewport: { desktop: [1440, 900], mobile: [390, 844] },
  ownerAuth: { attempted: true, succeeded: false, secretRecorded: false, logout: false },
  navigation: [],
  screenshots: [],
  snapshotRecovery: {},
  interceptions,
  pageErrors,
  observedRequests: requests,
};

try {
  await page.goto(`${baseUrl}/#office`, { waitUntil: 'domcontentloaded' });
  await page.getByLabel('Secret Chủ tịch local').fill(secret);
  await page.getByRole('button', { name: 'Đăng nhập Chủ tịch' }).click();
  await page.getByLabel('Secret Chủ tịch local').waitFor({ state: 'detached' });
  result.ownerAuth.succeeded = true;

  for (const id of ['overview', 'playground', 'office', 'work', 'inspector', 'replay', 'approvals']) {
    await navigate(id);
    result.navigation.push({ id, passwordFormVisible: false });
  }
  for (const id of ['office', 'inspector', 'replay']) {
    await navigate(id);
    result.screenshots.push(await capture(`${id}-before`, { width: 1440, height: 900 }));
    result.screenshots.push(await capture(`${id}-before`, { width: 390, height: 844 }));
  }

  await navigate('replay');
  let recoveryEnabled = false;
  let snapshotCount = 0;
  const uuid = n => `00000000-0000-4000-8000-${String(n).padStart(12, '0')}`;
  const domain = (seq, id) => ({ event_id: uuid(id), schema_version: 1, event_type: 'RUN_STATE_CHANGED', stream_seq: seq,
    occurred_at: '2026-10-19T00:00:00Z', recorded_at: '2026-10-19T00:00:00Z', task_id: null, run_id: null,
    agent_id: null, employee_version_id: null, correlation_id: uuid(id), parent_event_id: null, source: 'app',
    payload: { to: 'completed' }, sensitivity: 'internal', content_withheld: false });
  const projection = (watermark, seqs, gap = true) => ({ version: 1, events: seqs.map(([seq, id]) => domain(seq, id)), runs: [],
    watermark_seq: watermark, first_retained_seq: gap ? seqs[0]?.[0] ?? null : 1,
    replay_window_start_seq: seqs[0]?.[0] ?? null, history_gap: gap, cursor: `signed-fixture-${watermark}`,
    server_time: '2026-10-19T00:00:00Z' });

  let gapInjected = false;
  await page.route('**/api/v1/events**', async route => {
    if (recoveryEnabled && !gapInjected) { gapInjected = true; interceptions.push({ path: '/api/v1/events', status: 409 }); return route.fulfill({ status: 409, contentType: 'application/json',
      body: JSON.stringify({ detail: { code: 'event_gap', message: 'Fixture retention gap.' } }) });
    }
    if (recoveryEnabled) { interceptions.push({ path: '/api/v1/events', status: 200 }); return route.fulfill({ status: 200, contentType: 'application/json',
      body: JSON.stringify({ events: [], cursor: 'signed-fixture-probe', latest_seq: snapshotCount >= 2 ? 43 : 42, server_time: '2026-10-19T00:00:00Z' }) }); }
    return route.continue();
  });
  await page.route('**/api/v1/events/snapshot-v1', async route => {
    if (!recoveryEnabled) return route.continue();
    snapshotCount++;
    interceptions.push({ path: '/api/v1/events/snapshot-v1', status: 200, snapshot: snapshotCount });
    const body = snapshotCount === 1 ? projection(41, [[41, 41]]) : projection(43, [[41, 41], [42, 42], [43, 43]], true);
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(body) });
  });
  let recoveryStreamCount = 0;
  let holdNextStream = false;
  let releaseHeldStream;
  let abortHeldStream = false;
  let heldStreamStartedResolve;
  let heldStreamStarted = new Promise(resolve => { heldStreamStartedResolve = resolve; });
  await page.route('**/api/v1/events/stream**', async route => {
    if (holdNextStream) {
      holdNextStream = false;
      recoveryStreamCount++;
      interceptions.push({ path: '/api/v1/events/stream', status: 200, stream: recoveryStreamCount, held: true });
      heldStreamStartedResolve();
      await new Promise(resolve => { releaseHeldStream = async () => {
        if (abortHeldStream) { await route.abort('failed').catch(() => {}); resolve(); return; }
        await route.fulfill({ status: 200, contentType: 'text/event-stream; charset=utf-8',
          body: `event: heartbeat\ndata: ${JSON.stringify({ cursor: 'fixture-43', server_time: new Date().toISOString() })}\n\n` });
        resolve();
      }; });
      return;
    }
    if (!recoveryEnabled) return route.continue();
    recoveryStreamCount++;
    interceptions.push({ path: '/api/v1/events/stream', status: 200, stream: recoveryStreamCount });
    const items = recoveryStreamCount === 1 ? [domain(42, 42), domain(42, 42), domain(44, 44)] : [];
    const frames = items.map(item => `id: fixture-${item.stream_seq}\nevent: domain\ndata: ${JSON.stringify(item)}\n\n`).join('');
    return route.fulfill({ status: 200, contentType: 'text/event-stream; charset=utf-8',
      body: `${frames}event: heartbeat\ndata: ${JSON.stringify({ cursor: `fixture-${items.at(-1)?.stream_seq ?? 43}`, server_time: new Date().toISOString() })}\n\n` });
  });
  recoveryEnabled = true;
  await page.getByRole('button', { name: 'Tải lại từ đầu' }).click();
  const replayRows = async () => page.locator('.replay-timeline li').evaluateAll(items => items.map(item => ({
    sequence: item.querySelector('span')?.textContent ?? '', type: item.querySelector('strong')?.textContent ?? '' })));
  await page.waitForTimeout(2500);
  const recoveryText = await page.locator('main').innerText();
  const renderedRows = await replayRows();
  result.snapshotRecovery = { snapshotCount, streamCount: recoveryStreamCount,
    historyGapVisible: recoveryText.includes('Lịch sử trước event #41'),
    event42Visible: renderedRows.some(row => row.sequence === '#42' && row.type === 'RUN_STATE_CHANGED'),
    event43Visible: renderedRows.some(row => row.sequence === '#43' && row.type === 'RUN_STATE_CHANGED'),
    renderedRows,
    recoveryErrorVisible: false };
  if (!result.snapshotRecovery.historyGapVisible || !result.snapshotRecovery.event42Visible) {
    result.snapshotRecovery.connectionLabel = await page.locator('.observatory-status').innerText().catch(() => 'missing');
    result.snapshotRecovery.recoveryErrorVisible = (await page.locator('.runtime-error').allTextContents().catch(() => []))
      .some(text => /Không khôi phục được snapshot|Snapshot chưa đồng bộ được|Snapshot vượt giới hạn/i.test(text));
    throw new Error(`Recovery fixture did not render expected state: ${JSON.stringify(result.snapshotRecovery)}`);
  }
  const duplicateCount = renderedRows.filter(row => row.sequence === '#42' && row.type === 'RUN_STATE_CHANGED').length;
  if (duplicateCount !== 1) throw new Error(`Duplicate event was not removed: ${duplicateCount}`);
  // The fixture stream's out-of-order seq 44 forces one more atomic snapshot at watermark 43.
  if (!result.snapshotRecovery.event43Visible || snapshotCount !== 2) throw new Error('Out-of-order recovery snapshot did not replace the replay projection at watermark 43.');
  result.snapshotRecovery = { status: 'recovered', snapshots: snapshotCount, watermarkAfterConcurrentCommit: 41,
    concurrentEventReceived: true, duplicateEventCount: duplicateCount, outOfOrderTriggeredRecovery: snapshotCount >= 2,
    replayShowsHistoricalGap: true };
  result.screenshots.push(await capture('replay-after-recovery', { width: 1440, height: 900 }));
  result.screenshots.push(await capture('replay-after-recovery', { width: 390, height: 844 }));

  // Leave the synthetic fixture routes and reconcile the fixture cursor with the real read-only API.
  await page.unroute('**/api/v1/events**');
  await page.unroute('**/api/v1/events/snapshot-v1');
  recoveryEnabled = false;
  await navigate('replay');
  await page.getByRole('button', { name: 'Tải lại từ đầu' }).click();
  await navigate('office');
  await page.locator('.observatory-status').waitFor({ state: 'visible', timeout: 10000 });
  result.connectionChecks = { liveBeforeOffline: await page.waitForFunction(() => document.querySelector('.observatory-status')?.textContent?.includes('Đã kết nối'), null, { timeout: 15000 }).then(() => true).catch(() => false) };
  if (!result.connectionChecks.liveBeforeOffline) throw new Error('Real Owner event feed did not resume after the synthetic fixture was removed.');
  await navigate('replay');
  holdNextStream = true;
  await page.getByRole('button', { name: 'Tải lại từ đầu' }).click();
  await heldStreamStarted;
  await context.setOffline(true);
  abortHeldStream = true;
  releaseHeldStream?.();
  const offlineObserved = await page.waitForFunction(() => document.querySelector('.observatory-status')?.textContent?.includes('Mất kết nối'), null, { timeout: 15000 }).then(() => true).catch(() => false);
  result.connectionChecks.offlineObserved = offlineObserved;
  if (!offlineObserved) throw new Error('Offline state was not visible after browser network was disabled.');
  result.screenshots.push(await capture('replay-offline', { width: 1440, height: 900 }));
  result.screenshots.push(await capture('replay-offline', { width: 390, height: 844 }));
  await context.setOffline(false);
  result.connectionChecks.offlineRecovered = await page.waitForFunction(() => document.querySelector('.observatory-status')?.textContent?.includes('Đã kết nối'), null, { timeout: 15000 }).then(() => true).catch(() => false);
  if (!result.connectionChecks.offlineRecovered) throw new Error('Owner observability stream did not recover after browser network returned.');

  await navigate('replay');
  abortHeldStream = false;
  heldStreamStarted = new Promise(resolve => { heldStreamStartedResolve = resolve; });
  holdNextStream = true;
  await page.getByRole('button', { name: 'Tải lại từ đầu' }).click();
  await heldStreamStarted;
  await page.evaluate(() => { window.__stabilizationRealDateNow = Date.now.bind(Date); Date.now = () => window.__stabilizationRealDateNow() + 31000; });
  await page.waitForTimeout(5500);
  result.connectionChecks.staleObserved = await page.locator('.observatory-status').innerText().then(text => text.includes('Dữ liệu đã cũ'));
  if (!result.connectionChecks.staleObserved) throw new Error('Stalled SSE did not move the connection into the stale state.');
  result.screenshots.push(await capture('replay-stale', { width: 1440, height: 900 }));
  result.screenshots.push(await capture('replay-stale', { width: 390, height: 844 }));
  releaseHeldStream?.();
  result.connectionChecks.heartbeatRecovered = await page.waitForFunction(() => document.querySelector('.observatory-status')?.textContent?.includes('Đã kết nối'), null, { timeout: 15000 }).then(() => true).catch(() => false);
  await page.evaluate(() => { if (window.__stabilizationRealDateNow) Date.now = window.__stabilizationRealDateNow; delete window.__stabilizationRealDateNow; });
  if (!result.connectionChecks.heartbeatRecovered) throw new Error('Heartbeat did not restore the connected state after SSE resumed.');
  result.screenshots.push(await capture('replay-heartbeat-recovered', { width: 1440, height: 900 }));
  result.screenshots.push(await capture('replay-heartbeat-recovered', { width: 390, height: 844 }));

  await navigate('office');
  await page.getByRole('button', { name: 'Đăng xuất' }).click();
  await page.getByLabel('Secret Chủ tịch local').waitFor({ state: 'visible' });
  result.ownerAuth.logout = true;
} catch (error) {
  result.failure = error instanceof Error ? error.message : 'unknown';
} finally {
  await context.close();
  await browser.close();
}

await writeFile(path.join(output, 'browser-result.json'), `${JSON.stringify(result, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({ ownerAuth: result.ownerAuth, navigation: result.navigation, snapshotRecovery: result.snapshotRecovery, failure: result.failure,
  screenshotCount: result.screenshots.length, pageErrorCount: result.pageErrors.length }, null, 2));
if (result.failure) process.exitCode = 1;
