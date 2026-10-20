import { chromium } from '/tmp/deployment06-playwright/node_modules/playwright/index.mjs'
import { execFileSync } from 'node:child_process'
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

const root = process.cwd()
const controlPath = resolve(root, 'docs/reviews/integration-05/evidence/disposable-stack.json')
const control = JSON.parse(readFileSync(controlPath, 'utf8'))
const compose = control.compose
const project = control.project
const base = 'http://127.0.0.1:15502/'
const out = resolve(root, 'docs/reviews/deployment-06/evidence')
const screenshots = resolve(out, 'screenshots')
mkdirSync(screenshots, { recursive: true })

function runRtk(args, options = {}) {
  return execFileSync('rtk', ['proxy', 'docker', 'compose', '-p', project, '-f', compose, ...args], {
    cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], ...options,
  })
}
async function getRunStatus(page) {
  return await page.evaluate(async () => {
    const response = await fetch('/api/v1/runtime/status', { credentials: 'same-origin', cache: 'no-store' })
    if (!response.ok) return { status: `http_${response.status}` }
    const data = await response.json()
    return data.runs?.[0] ? { status: data.runs[0].status } : { status: 'missing' }
  })
}

const result = {
  date: new Date().toISOString(),
  target: 'separate disposable Integration 05 stack; synthetic Owner; fake gate/worker transport; no gateway/model',
  viewport: {},
  assertions: {},
  workerStopped: false,
  logout: false,
  cleanup: false,
}
const browser = await chromium.launch({ headless: true, executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' })
const context = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 })
const page = await context.newPage()

try {
  await page.goto(`${base}#settings`, { waitUntil: 'domcontentloaded' })
  const secret = `synthetic-owner-secret-${'a'.repeat(48)}`
  await page.getByLabel('Secret Chủ tịch local').fill(secret)
  await page.getByRole('button', { name: 'Đăng nhập Chủ tịch' }).click()
  await page.getByText(/Đã xác thực Chủ tịch trong scope demo/).waitFor({ timeout: 15000 })
  await page.locator('#runtime-model').waitFor({ timeout: 15000 })
  const saveProfile = page.getByRole('button', { name: /Lưu profile/ })
  for (let attempt = 0; attempt < 30 && !(await saveProfile.isEnabled()); attempt++) await page.waitForTimeout(250)
  if (!(await saveProfile.isEnabled())) {
    const diagnostics = await page.evaluate(async () => {
      const paths = ['owner/profile', 'runtime/status', 'runtime/grants', 'work-orders', 'runtime/employees']
      const statuses = {}
      for (const path of paths) {
        const response = await fetch(`/api/v1/${path}`, { credentials: 'same-origin', cache: 'no-store' })
        statuses[path] = response.status
        if (path === 'owner/profile' && response.ok) {
          const profile = await response.json()
          statuses.profile = { version: profile.version, model: profile.model, reasoning_effort: profile.reasoning_effort }
        }
      }
      return { statuses, buttonText: document.querySelector('.runtime-form button')?.textContent, buttonDisabled: document.querySelector('.runtime-form button')?.disabled, runtimeScope: document.querySelector('.runtime-scope')?.textContent }
    })
    const visibleError = await page.locator('.runtime-error').allTextContents()
    throw new Error(`Profile controls remained disabled; endpoint statuses=${JSON.stringify(diagnostics)}; visible errors=${JSON.stringify(visibleError)}`)
  }
  await page.locator('#runtime-model').fill('synthetic.fake-transport')
  await page.locator('#runtime-effort').selectOption('low')
  await saveProfile.click()
  await page.getByText(/Đã lưu model profile phiên bản/).waitFor({ timeout: 15000 })
  const grantButton = page.getByRole('button', { name: 'Tạo grant test Phase 06 riêng' })
  await grantButton.waitFor({ timeout: 15000 })
  await grantButton.click()
  await page.getByText(/Đã cấp grant Phase 06/).waitFor({ timeout: 15000 })
  await page.locator('#runtime-employee').selectOption({ index: 1 })
  await page.locator('#runtime-input').fill('Synthetic text-only request for unknown-outcome UI acceptance.')
  await page.getByRole('button', { name: 'Bắt đầu Run text-only' }).click()
  await page.getByText(/Đã tạo Run/).waitFor({ timeout: 15000 })

  let runState = { status: 'missing' }
  for (let attempt = 0; attempt < 40; attempt++) {
    runState = await getRunStatus(page)
    if (runState.status === 'waiting_model') break
    await page.waitForTimeout(250)
  }
  result.assertions.fakeTransportDispatched = runState.status === 'waiting_model'
  if (!result.assertions.fakeTransportDispatched) throw new Error(`Synthetic worker did not dispatch; observed ${runState.status}.`)

  runRtk(['stop', 'worker'])
  result.workerStopped = true
  const recovery = [
    'from uuid import UUID',
    'from sqlalchemy import text',
    'from agent_corporation_api.database import get_session_factory',
    'from agent_corporation_api.modules.execution import service',
    'from agent_corporation_api.modules.observability.scope import CompanyScope',
    'factory = get_session_factory()',
    'scope = CompanyScope(UUID("b93f752e-7b69-5e8b-8f74-1498a15a5609"), UUID("b4375333-b12b-5fca-b984-87864032d3a8"))',
    'with service.transaction(factory, scope) as session: session.execute(text("UPDATE model_calls SET lease_until=CURRENT_TIMESTAMP-interval \'1 second\' WHERE status=\'dispatched\'"))',
    'recovered = service.recover_expired(factory, scope)',
    'print("Recovered expired synthetic calls:", recovered)',
  ].join('\n')
  const recoveryOutput = runRtk(['exec', '-T', 'api', 'python', '-c', recovery])
  result.assertions.syntheticLeaseExpiredAndRecovered = /Recovered expired synthetic calls: 1/.test(recoveryOutput)
  if (!result.assertions.syntheticLeaseExpiredAndRecovered) throw new Error(`Synthetic lease recovery did not report exactly one isolated call: ${recoveryOutput}`)
  for (let attempt = 0; attempt < 40; attempt++) {
    runState = await getRunStatus(page)
    if (runState.status === 'interrupted') break
    await page.waitForTimeout(250)
  }
  result.assertions.unknownFenced = runState.status === 'interrupted'
  if (!result.assertions.unknownFenced) throw new Error(`Expected interrupted/unknown after stopping only the synthetic worker; observed ${runState.status}.`)

  await page.goto(`${base}#settings`, { waitUntil: 'domcontentloaded' })
  await page.locator('.runtime-run').waitFor({ timeout: 15000 })
  await page.getByRole('button', { name: 'Bằng chứng outcome' }).click()
  await page.locator('.runtime-reconciliation').waitFor({ timeout: 15000 })
  const panelText = await page.locator('.runtime-reconciliation').innerText()
  result.assertions.unresolvedVisible = /unresolved/.test(panelText)
  result.assertions.usageAndCostUnknown = /unknown/.test(panelText)
  result.assertions.noForceUnlock = (await page.locator('.runtime-reconciliation button').allTextContents()).every(label => !/force unlock|mở khóa cưỡng bức/i.test(label))
  if (!result.assertions.unresolvedVisible || !result.assertions.usageAndCostUnknown || !result.assertions.noForceUnlock) {
    throw new Error('Synthetic reconciliation panel did not show the expected safe unknown state.')
  }
  await page.locator('.runtime-reconciliation').scrollIntoViewIfNeeded()
  await page.screenshot({ path: resolve(screenshots, 'reconciliation-unknown-desktop-1440x900.png') })
  result.viewport.desktop = { width: 1440, height: 900, screenshot: 'screenshots/reconciliation-unknown-desktop-1440x900.png' }
  await page.setViewportSize({ width: 390, height: 844 })
  await page.locator('.runtime-reconciliation').scrollIntoViewIfNeeded()
  await page.screenshot({ path: resolve(screenshots, 'reconciliation-unknown-mobile-390x844.png') })
  result.viewport.mobile = {
    width: 390, height: 844,
    scrollWidth: await page.evaluate(() => document.documentElement.scrollWidth),
    screenshot: 'screenshots/reconciliation-unknown-mobile-390x844.png',
  }
  result.assertions.mobileNoHorizontalOverflow = result.viewport.mobile.scrollWidth <= 390

  await page.getByRole('button', { name: 'Đăng xuất' }).click()
  await page.getByLabel('Secret Chủ tịch local').waitFor({ timeout: 15000 })
  result.logout = true
} finally {
  await context.close()
  await browser.close()
  try { runRtk(['down', '--volumes', '--remove-orphans']) ; result.cleanup = true } catch { /* cleanup is verified separately */ }
  if (result.cleanup) {
    const { unlinkSync, rmSync } = await import('node:fs')
    try { rmSync(resolve(compose, '..'), { recursive: true, force: true }) } catch {}
    try { unlinkSync(controlPath) } catch {}
  }
  if (result.cleanup && result.workerStopped) console.log('Disposable synthetic reconciliation stack and volumes removed.')
}
writeFileSync(resolve(out, 'reconciliation-smoke.json'), `${JSON.stringify(result, null, 2)}\n`, { mode: 0o600 })
console.log(JSON.stringify(result))
