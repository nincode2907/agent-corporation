import { chromium } from '/tmp/deployment06-playwright/node_modules/playwright/index.mjs'
import { execFileSync } from 'node:child_process'
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

const root = process.cwd()
const controlPath = resolve(root, 'docs/reviews/integration-05/evidence/disposable-stack.json')
const control = JSON.parse(readFileSync(controlPath, 'utf8'))
const base = 'http://127.0.0.1:15502/'
const evidence = resolve(root, 'docs/reviews/ui-fix-07/evidence')
const screenshots = resolve(root, 'docs/reviews/ui-fix-07/screenshots')
mkdirSync(evidence, { recursive: true })
mkdirSync(screenshots, { recursive: true })

function compose(args) {
  return execFileSync('rtk', ['proxy', 'docker', 'compose', '-p', control.project, '-f', control.compose, ...args], {
    cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'],
  })
}
function apiCode(source) {
  return compose(['exec', '-T', 'api', 'python', '-c', source]).trim()
}
const modelCallCount = () => Number(apiCode([
  'from uuid import UUID',
  'from sqlalchemy import text',
  'from agent_corporation_api.database import get_session_factory',
  'from agent_corporation_api.modules.observability.scope import CompanyScope, set_company_scope',
  's=get_session_factory()()',
  'set_company_scope(s,CompanyScope(UUID("b93f752e-7b69-5e8b-8f74-1498a15a5609"),UUID("b4375333-b12b-5fca-b984-87864032d3a8")))',
  'print(s.execute(text("SELECT count(*) FROM model_calls")).scalar_one())',
  's.close()',
].join('\n')))
async function waitForModelCallCount(expected, timeout = 15000) {
  const deadline = Date.now() + timeout
  let count = 0
  while (Date.now() < deadline) {
    count = modelCallCount()
    if (count === expected) return count
    if (count > expected) throw new Error(`Expected ${expected} isolated fake dispatches, observed ${count}`)
    await new Promise(resolveDelay => setTimeout(resolveDelay, 250))
  }
  throw new Error(`Expected ${expected} isolated fake dispatches, observed ${count}`)
}
async function savedStatus(page) {
  return page.evaluate(async () => {
    const response = await fetch('/api/v1/runtime/status', { credentials: 'same-origin', cache: 'no-store' })
    if (!response.ok) throw new Error(`runtime/status returned ${response.status}`)
    return response.json()
  })
}
async function waitForStatus(page, expected, timeout = 15000, runId = null) {
  await page.waitForFunction(async ({ expectedStatus, expectedRunId }) => {
    const response = await fetch('/api/v1/runtime/status', { credentials: 'same-origin', cache: 'no-store' })
    if (!response.ok) return false
    const data = await response.json()
    return data.runs?.some(run => run.status === expectedStatus && (!expectedRunId || run.id === expectedRunId))
  }, { expectedStatus: expected, expectedRunId: runId }, { timeout })
  return savedStatus(page)
}
async function waitForRunStatus(page, runId, expected, timeout = 15000) {
  const deadline = Date.now() + timeout
  let status
  while (Date.now() < deadline) {
    status = await savedStatus(page)
    const run = status.runs?.find(item => item.id === runId)
    if (run?.status === expected) return status
    await page.waitForTimeout(500)
  }
  const last = status?.runs?.find(item => item.id === runId)
  throw new Error(`Run ${runId} did not reach ${expected}; observed ${last?.status ?? 'missing'}`)
}
function check(name, value, detail) {
  result.assertions[name] = Boolean(value)
  if (!value) throw new Error(`${name} failed${detail ? `: ${detail}` : ''}`)
}

const result = {
  date: new Date().toISOString(),
  target: 'isolated disposable Integration 05 stack; synthetic Owner, fake gate and transport; no gateway/model inference',
  viewports: {},
  assertions: {},
  modelCallCounts: {},
  consoleErrors: [],
  pageErrors: [],
  cleanup: false,
}
const browser = await chromium.launch({ headless: true, executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' })
const context = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 })
const page = await context.newPage()
page.on('pageerror', error => result.pageErrors.push(error.message))
page.on('console', message => { if (message.type() === 'error') result.consoleErrors.push(message.text().slice(0, 200)) })

try {
  await page.goto(`${base}#office`, { waitUntil: 'domcontentloaded' })
  await page.getByLabel('Secret Chủ tịch local').fill(`synthetic-owner-secret-${'a'.repeat(48)}`)
  await page.getByRole('button', { name: 'Đăng nhập Chủ tịch' }).click()
  await page.getByText(/Đã xác thực Chủ tịch trong scope demo/).waitFor({ timeout: 15000 })
  await page.locator('.office-employee-card').first().waitFor({ timeout: 15000 })
  await page.waitForFunction(() => document.querySelectorAll('.office-employee-card').length === 3, null, { timeout: 15000 })
  await page.getByText('Trạng thái đã đối chiếu').waitFor({ timeout: 15000 })
  const emptyCards = await page.locator('.office-employee-card').evaluateAll(cards => cards.map(card => ({
    name: card.querySelector('h5')?.textContent,
    employeeId: card.getAttribute('data-employee-id'),
    versionId: card.getAttribute('data-employee-version-id'),
    state: card.querySelector('.office-employee-state')?.textContent,
    history: card.querySelector('.office-employee-history')?.textContent,
  })))
  check('threeEmployeesNoRuns', emptyCards.length === 3 && emptyCards.every(card => /Không có Run đang hoạt động/.test(card.state) && /Chưa có Run/.test(card.history)), JSON.stringify(emptyCards))
  check('departmentGroupsAreReal', await page.locator('.office-team').count() > 0 && !(await page.locator('.fixture-badge').filter({ hasText: 'FIXTURE' }).count()))
  check('desktopNoOverflow', await page.evaluate(() => document.documentElement.scrollWidth <= 1440))
  await page.locator('.office-roster').scrollIntoViewIfNeeded()
  await page.screenshot({ path: resolve(screenshots, 'office-roster-1440x900.png') })

  const firstCard = page.locator('.office-employee-card').first()
  const employeeId = await firstCard.getAttribute('data-employee-id')
  const versionId = await firstCard.getAttribute('data-employee-version-id')
  const runtimeHref = await firstCard.locator('a.office-primary-link').getAttribute('href')
  check('runtimeLinkHasImmutableAssignment', runtimeHref.includes(encodeURIComponent(employeeId)) && runtimeHref.includes(encodeURIComponent(versionId)), runtimeHref)

  // Route-level negative proof only: the isolated API remains untouched; display a strict deny response once.
  await page.route('**/api/v1/runtime/status', async route => {
    const response = await route.fetch()
    const data = await response.json()
    data.cg01 = { allowed: false, mode: 'strict', verified: false, reason: 'missing_or_invalid_proof' }
    await route.fulfill({ response, body: JSON.stringify(data) })
  })
  await firstCard.locator('a.office-primary-link').click()
  await page.waitForFunction(() => location.hash.startsWith('#settings?'), null, { timeout: 10000 })
  await page.locator('#runtime-employee').waitFor()
  await page.waitForFunction(([id, version]) => {
    const select = document.querySelector('#runtime-employee')
    const detail = document.querySelector('.runtime-grant-detail')?.textContent ?? ''
    return select?.value === id && detail.includes(version)
  }, [employeeId, versionId], { timeout: 15000 })
  check('runtimeFormKeepsSelectedVersion', await page.locator('#runtime-employee').inputValue() === employeeId && (await page.locator('.runtime-grant-detail').textContent()).includes(versionId))
  const noGrantAttempt = await page.evaluate(async assignment => {
    const sessionResponse = await fetch('/api/v1/owner/session', { credentials: 'same-origin', cache: 'no-store' })
    const session = await sessionResponse.json()
    const response = await fetch('/api/v1/runtime/runs', {
      method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': session.csrf_token },
      body: JSON.stringify({ grant_id: '00000000-0000-4000-8000-000000000088', ...assignment, phase: '06', batch_id: 'ui-fix-07-no-grant-bypass', purpose: 'Negative authorization UI regression', model: 'synthetic.fake-transport', effort: 'low', input_text: 'This must be denied before creating a Run.', idempotency_key: crypto.randomUUID() }),
    })
    return { status: response.status, body: await response.json() }
  }, { employee_id: employeeId, employee_version_id: versionId })
  check('noGrantDirectPostDenied', noGrantAttempt.status >= 400 && noGrantAttempt.status < 500, JSON.stringify(noGrantAttempt.body))
  check('noGrantDeniedWithoutRunCreation', (await savedStatus(page)).runs.length === 0)
  await page.locator('#runtime-input').fill('Synthetic UI Fix 07 test request; fake transport only.')
  await page.waitForFunction(() => {
    const text = document.querySelector('.runtime-blocker-list')?.textContent ?? ''
    return text.includes('grant') && text.includes('CG01')
  }, null, { timeout: 15000 })
  check('cg01AndGrantBlockStart', !(await page.getByRole('button', { name: 'Bắt đầu Run text-only' }).isEnabled()) && /grant/i.test(await page.locator('.runtime-blocker-list').innerText()) && /CG01/i.test(await page.locator('.runtime-blocker-list').innerText()))
  await page.locator('.runtime-blocker-list').scrollIntoViewIfNeeded()
  await page.screenshot({ path: resolve(screenshots, 'runtime-blocked-1440x900.png') })
  await page.unroute('**/api/v1/runtime/status')
  await page.reload({ waitUntil: 'domcontentloaded' })
  await page.locator('#runtime-employee').waitFor()
  await page.waitForFunction(() => {
    const button = [...document.querySelectorAll('.runtime-form button')].find(item => item.textContent?.includes('Lưu profile'))
    return Boolean(button && !(button instanceof HTMLButtonElement && button.disabled) && document.querySelector('#runtime-employee option:nth-child(2)'))
  }, null, { timeout: 15000 })

  await page.locator('#runtime-model').fill('synthetic.fake-transport')
  await page.locator('#runtime-effort').selectOption('low')
  await page.getByRole('button', { name: /Lưu profile/ }).click()
  await page.waitForFunction(() => Boolean(document.querySelector('.runtime-notice')?.textContent?.includes('Đã lưu model profile') || document.querySelector('.runtime-error')?.textContent), null, { timeout: 15000 })
  await page.locator('#runtime-task-form').scrollIntoViewIfNeeded()
  await page.screenshot({ path: resolve(screenshots, 'runtime-profile-save-1440x900.png') })
  const profileNotice = await page.locator('.runtime-notice').textContent().catch(() => '')
  if (!profileNotice?.includes('Đã lưu model profile')) throw new Error(`Profile save failed: ${await page.locator('.runtime-error').allTextContents()}`)
  await page.getByRole('button', { name: 'Tạo grant test Phase 06 riêng' }).click()
  await page.getByText(/Đã cấp grant Phase 06/).waitFor({ timeout: 15000 })
  await page.locator('#runtime-input').fill('Synthetic UI Fix 07 waiting/completion path.')
  await page.getByRole('button', { name: 'Bắt đầu Run text-only' }).click()
  await page.getByText(/Đã tạo Run/).waitFor({ timeout: 15000 })
  let status = await waitForStatus(page, 'waiting_model', 20000)
  const firstRun = status.runs.find(run => ['queued', 'waiting', 'waiting_model', 'dispatching', 'running', 'pending'].includes(run.status))
  check('firstRunReachedPersistedActiveState', Boolean(firstRun), JSON.stringify(status.runs.map(run => ({ id: run.id, status: run.status }))))
  const runId = firstRun.id
  result.modelCallCounts.afterInitialDispatch = await waitForModelCallCount(1)
  check('oneFakeTransportDispatch', result.modelCallCounts.afterInitialDispatch === 1)
  check('runCarriesSelectedVersion', firstRun.employee?.id === employeeId && firstRun.employee?.version_id === versionId)

  await page.goto(`${base}#office`, { waitUntil: 'domcontentloaded' })
  await page.getByText('Trạng thái đã đối chiếu').waitFor({ timeout: 15000 })
  const activeCard = page.locator(`.office-employee-card[data-employee-id="${employeeId}"]`)
  await activeCard.getByText(/Đang chờ phản hồi model|Đang thực hiện/).waitFor({ timeout: 10000 })
  await activeCard.scrollIntoViewIfNeeded()
  await page.screenshot({ path: resolve(screenshots, 'office-waiting-model-1440x900.png') })
  const inspectorLink = activeCard.locator(`a[href="#inspector?run_id=${runId}"]`)
  await activeCard.locator('.office-employee-history > summary').click()
  await inspectorLink.click()
  await page.locator('#inspector-run').waitFor()
  await page.waitForFunction(expected => document.querySelector('#inspector-run')?.value === expected, runId)
  check('inspectorKeepsSameRunId', await page.locator('#inspector-run').inputValue() === runId)
  await page.goto(`${base}#office`, { waitUntil: 'domcontentloaded' })
  const replayCard = page.locator(`.office-employee-card[data-employee-id="${employeeId}"]`)
  await replayCard.locator('.office-employee-history > summary').click()
  const replayLink = replayCard.locator(`a[href="#replay?run_id=${runId}"]`)
  await replayLink.click()
  await page.locator('#replay-run').waitFor()
  await page.waitForFunction(expected => document.querySelector('#replay-run')?.value === expected, runId)
  check('replayKeepsSameRunId', await page.locator('#replay-run').inputValue() === runId)
  result.modelCallCounts.afterReadNavigation = modelCallCount()
  check('noDuplicateDispatchFromReadNavigation', result.modelCallCounts.afterReadNavigation === result.modelCallCounts.afterInitialDispatch)

  status = await waitForRunStatus(page, runId, 'completed', 110000)
  const completedRun = status.runs.find(run => run.id === runId)
  result.fakeCompletion = { runId, status: completedRun?.status ?? null, output: completedRun?.output ?? null, outcome: completedRun?.outcome ?? null }
  check('fakeTransportCompleted', completedRun?.status === 'completed' && completedRun?.output === 'Báo cáo tổng hợp từ fake transport.', JSON.stringify(result.fakeCompletion))
  await page.goto(`${base}#office`, { waitUntil: 'domcontentloaded' })
  await page.getByText('Trạng thái đã đối chiếu').waitFor({ timeout: 15000 })
  const completedCard = page.locator(`.office-employee-card[data-employee-id="${employeeId}"]`)
  await completedCard.getByText('Không có Run đang hoạt động').waitFor()
  await completedCard.locator('.office-employee-history > summary').click()
  const completedHistory = completedCard.locator('.office-employee-history')
  check('completedRunRemainsHistorical', /Hoàn tất/.test(await completedHistory.innerText()) && await completedHistory.locator(`a[href="#inspector?run_id=${runId}"]`).count() === 1)
  await completedCard.scrollIntoViewIfNeeded()
  await page.screenshot({ path: resolve(screenshots, 'office-completed-history-1440x900.png') })
  result.modelCallCounts.afterCompletedReadNavigation = modelCallCount()
  check('noDuplicateDispatchAfterCompletionNavigation', result.modelCallCounts.afterCompletedReadNavigation === 1)

  // A saved Run on an older immutable version stays in history and cannot mark the current version active.
  const oldVersionId = '00000000-0000-4000-8000-000000000099'
  const projectOldRun = payload => {
    for (const run of payload.runs ?? []) if (run.id === runId && run.employee) {
      run.status = 'running'
      run.employee.version_id = oldVersionId
      run.employee.version = 0
    }
    return payload
  }
  await page.route('**/api/v1/runtime/status', async route => {
    const response = await route.fetch()
    await route.fulfill({ response, body: JSON.stringify(projectOldRun(await response.json())) })
  })
  await page.route('**/api/v1/events/snapshot-v1', async route => {
    const response = await route.fetch()
    const payload = projectOldRun(await response.json())
    await route.fulfill({ response, body: JSON.stringify(payload) })
  })
  await page.reload({ waitUntil: 'domcontentloaded' })
  await page.getByText('Trạng thái đã đối chiếu').waitFor({ timeout: 15000 })
  const currentVersionCard = page.locator(`.office-employee-card[data-employee-id="${employeeId}"]`)
  await currentVersionCard.getByText('Không có Run đang hoạt động').waitFor()
  await currentVersionCard.locator('.office-employee-history > summary').click()
  const oldVersionHistory = currentVersionCard.locator('.office-employee-history')
  check('oldVersionRunDoesNotSetCurrentActive', /Không có Run đang hoạt động/.test(await currentVersionCard.locator('.office-employee-state').innerText()) && /hồ sơ v0/.test(await oldVersionHistory.innerText()) && await oldVersionHistory.locator(`a[href="#inspector?run_id=${runId}"]`).count() === 1)
  await page.unroute('**/api/v1/runtime/status')
  await page.unroute('**/api/v1/events/snapshot-v1')

  await page.goto(`${base}#settings?employee_id=${employeeId}&employee_version_id=${oldVersionId}`, { waitUntil: 'domcontentloaded' })
  await page.locator('#runtime-employee').waitFor()
  await page.waitForFunction(() => Boolean(document.querySelector('.runtime-error')?.textContent?.includes('EmployeeVersion trong liên kết')) , null, { timeout: 15000 })
  check('staleEmployeeVersionLinkNeverSubstitutes', await page.locator('#runtime-employee').inputValue() === '' && /EmployeeVersion trong liên kết/.test(await page.locator('.runtime-error').innerText()))
  await page.locator('.runtime-error').scrollIntoViewIfNeeded()
  await page.screenshot({ path: resolve(screenshots, 'runtime-stale-employee-version-link-1440x900.png') })

  // Explicitly test that a disconnected event feed cannot claim the employee is idle.
  await page.goto(`${base}#office`, { waitUntil: 'domcontentloaded' })
  await page.route('**/api/v1/events/stream**', route => route.abort())
  await page.reload({ waitUntil: 'domcontentloaded' })
  await page.locator('.live-indicator').getByText(/Đang kết nối lại/).waitFor({ timeout: 15000 })
  const disconnectText = await page.locator(`.office-employee-card[data-employee-id="${employeeId}"] .office-employee-state`).innerText()
  check('sseDisconnectDoesNotImplyIdle', /mất kết nối|kết nối lại|chưa xác minh/i.test(disconnectText) && !(await page.locator('.office-freshness').innerText()).includes('Trạng thái đã đối chiếu'))
  await page.locator('.office-roster').scrollIntoViewIfNeeded()
  await page.screenshot({ path: resolve(screenshots, 'office-sse-disconnected-1440x900.png') })
  await page.unroute('**/api/v1/events/stream**')

  // The second synthetic grant/run exists only in this throwaway database and is used to verify unknown recovery UX.
  const grantResult = await page.evaluate(async () => {
    const sessionResponse = await fetch('/api/v1/owner/session', { credentials: 'same-origin', cache: 'no-store' })
    const session = await sessionResponse.json()
    const response = await fetch('/api/v1/runtime/grants', {
      method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': session.csrf_token },
      body: JSON.stringify({ phase: '06', batch_id: 'ui-fix-07-unknown', purpose: 'Synthetic unknown outcome UI regression', model: 'synthetic.fake-transport', effort: 'low', max_requests: 1, max_concurrency: 1, timeout_seconds: 120, max_requeues: 0, expires_at: new Date(Date.now() + 15 * 60 * 1000).toISOString() }),
    })
    return { status: response.status, body: await response.json() }
  })
  check('isolatedUnknownGrantCreated', grantResult.status === 201 || grantResult.status === 200, JSON.stringify(grantResult.body))
  await page.goto(`${base}#settings?employee_id=${employeeId}&employee_version_id=${versionId}`, { waitUntil: 'domcontentloaded' })
  await page.locator('#runtime-input').waitFor()
  await page.locator('#runtime-employee').selectOption(employeeId)
  await page.locator('#runtime-grant').selectOption(grantResult.body.id)
  await page.locator('#runtime-input').fill('Synthetic request whose worker will be stopped before a response.')
  await page.getByRole('button', { name: 'Bắt đầu Run text-only' }).click()
  await page.getByText(/Đã tạo Run/).waitFor({ timeout: 15000 })
  status = await waitForStatus(page, 'waiting_model', 20000)
  const unknownRun = status.runs.find(run => run.id !== runId && ['queued', 'waiting', 'waiting_model', 'dispatching', 'running', 'pending'].includes(run.status))
  check('unknownRunDispatchedToFakeTransport', Boolean(unknownRun && unknownRun.id !== runId))
  result.modelCallCounts.beforeUnknownWorkerStop = await waitForModelCallCount(2)
  compose(['stop', 'worker'])
  result.workerStoppedForUnknown = true
  const recovery = [
    'from uuid import UUID',
    'from sqlalchemy import text',
    'from agent_corporation_api.database import get_session_factory',
    'from agent_corporation_api.modules.execution import service',
    'from agent_corporation_api.modules.observability.scope import CompanyScope',
    'factory=get_session_factory()',
    'scope=CompanyScope(UUID("b93f752e-7b69-5e8b-8f74-1498a15a5609"),UUID("b4375333-b12b-5fca-b984-87864032d3a8"))',
    'with service.transaction(factory,scope) as s: s.execute(text("UPDATE model_calls SET lease_until=CURRENT_TIMESTAMP-interval \'1 second\' WHERE status=\'dispatched\'"))',
    'print("recovered",service.recover_expired(factory,scope))',
  ].join('\n')
  check('syntheticLeaseRecovered', /recovered 1/.test(compose(['exec', '-T', 'api', 'python', '-c', recovery])))
  status = await waitForRunStatus(page, unknownRun.id, 'interrupted', 15000)
  const interruptedRun = status.runs.find(run => run.id === unknownRun.id)
  check('unknownOutcomePersisted', interruptedRun?.status === 'interrupted')
  await page.goto(`${base}#office`, { waitUntil: 'domcontentloaded' })
  await page.getByText('Trạng thái đã đối chiếu').waitFor({ timeout: 15000 })
  const unknownCard = page.locator(`.office-employee-card[data-employee-id="${employeeId}"]`)
  await unknownCard.getByText(/Kết quả Run chưa rõ/).waitFor()
  await unknownCard.locator('.office-employee-history > summary').click()
  await unknownCard.locator('a', { hasText: 'Đối chiếu outcome' }).click()
  await page.locator('.runtime-reconciliation').waitFor({ timeout: 15000 })
  check('reconciliationEntryAndUnknownWarning', /unresolved/.test(await page.locator('.runtime-reconciliation').innerText()) && /chưa được xác nhận/.test(await page.locator('.runtime-runs').innerText()))
  result.modelCallCounts.final = modelCallCount()
  check('readsDidNotRedispatchUnknownRun', result.modelCallCounts.final === 2)
  await page.locator('.runtime-reconciliation').scrollIntoViewIfNeeded()
  await page.screenshot({ path: resolve(screenshots, 'runtime-unknown-reconciliation-1440x900.png') })

  await page.setViewportSize({ width: 390, height: 844 })
  await page.goto(`${base}#office`, { waitUntil: 'domcontentloaded' })
  await page.getByText(/Đã kết nối/).waitFor({ timeout: 15000 })
  const mobile = await page.evaluate(() => ({ width: innerWidth, height: innerHeight, scrollWidth: document.documentElement.scrollWidth }))
  result.viewports.mobile = mobile
  check('mobileNoOverflow', mobile.width === 390 && mobile.scrollWidth === 390, JSON.stringify(mobile))
  await page.evaluate(() => (document.activeElement instanceof HTMLElement) && document.activeElement.blur())
  const primaryAction = page.locator('.office-employee-card .office-primary-link').first()
  let focused = false
  for (let index = 0; index < 50 && !focused; index++) {
    await page.keyboard.press('Tab')
    focused = await primaryAction.evaluate(element => element === document.activeElement)
  }
  check('keyboardFocusVisible', focused && await primaryAction.evaluate(element => element.matches(':focus-visible') && getComputedStyle(element).outlineWidth !== '0px'))
  await page.locator('.office-roster').scrollIntoViewIfNeeded()
  await page.screenshot({ path: resolve(screenshots, 'office-mobile-390x844.png') })
  result.viewports.desktop = { width: 1440, height: 900, scrollWidth: 1440 }
  check('noPageErrors', result.pageErrors.length === 0, JSON.stringify(result.pageErrors))
} finally {
  await context.close()
  await browser.close()
  try {
    compose(['down', '--volumes', '--remove-orphans'])
    result.cleanup = true
  } catch { /* recorded and retried during cleanup */ }
  if (result.cleanup) {
    const { rmSync, unlinkSync } = await import('node:fs')
    try { rmSync(resolve(control.compose, '..'), { recursive: true, force: true }) } catch {}
    try { unlinkSync(controlPath) } catch {}
  }
  writeFileSync(resolve(evidence, 'ui-regression.json'), `${JSON.stringify(result, null, 2)}\n`, { mode: 0o600 })
}
console.log(JSON.stringify({ assertions: result.assertions, modelCallCounts: result.modelCallCounts, viewports: result.viewports, cleanup: result.cleanup }))
