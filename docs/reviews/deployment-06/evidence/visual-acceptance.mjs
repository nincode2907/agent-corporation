import { chromium } from '/tmp/deployment06-playwright/node_modules/playwright/index.mjs'
import { execFileSync } from 'node:child_process'
import { mkdirSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

const root = process.cwd()
const base = 'http://agent-corporation.localhost/'
const out = resolve(root, 'docs/reviews/deployment-06/evidence')
const screenshots = resolve(out, 'screenshots')
mkdirSync(screenshots, { recursive: true })

// Read the local Owner credential only in memory for the explicitly authorized local login.
// It is never written to disk, logged, or included in the result manifest.
let ownerSecret = execFileSync('rtk', ['proxy', 'docker', 'compose', 'exec', '-T', 'api', 'cat', '/runtime-secrets/owner-secret'], {
  cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'],
}).trim()
if (!ownerSecret) throw new Error('Owner credential unavailable; no value was printed.')

const browser = await chromium.launch({
  headless: true,
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
})
const context = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 })
const page = await context.newPage()
const result = {
  date: new Date().toISOString(),
  base: 'http://agent-corporation.localhost/',
  viewports: {},
  assertions: {},
  pageErrors: 0,
  consoleErrors: 0,
  logout: false,
}
page.on('pageerror', () => { result.pageErrors++ })
page.on('console', message => { if (message.type() === 'error') result.consoleErrors++ })

async function view(route, viewName, filename, selector) {
  await page.goto(`${base}#${route}`, { waitUntil: 'domcontentloaded' })
  await page.locator(`a.nav-link[href="#${route}"].active`).waitFor()
  if (route === 'office' || route === 'inspector' || route === 'replay') await page.locator('#runtime-title').waitFor()
  if (selector) await page.locator(selector).scrollIntoViewIfNeeded()
  await page.screenshot({ path: resolve(screenshots, filename) })
  const dims = await page.evaluate(() => ({ width: window.innerWidth, height: window.innerHeight, scrollWidth: document.documentElement.scrollWidth }))
  result.viewports[`${viewName}:${route}`] = { ...dims, screenshot: `screenshots/${filename}` }
  return dims
}

try {
  await page.goto(base, { waitUntil: 'domcontentloaded' })
  await page.getByText('Demo Corporation', { exact: true }).first().waitFor()
  await page.screenshot({ path: resolve(screenshots, 'overview-desktop-1440x900.png') })
  result.assertions.dashboardDemo = await page.getByText('3 hồ sơ nhân sự', { exact: false }).count() > 0
  await view('office', 'desktop', 'office-unauthenticated-desktop-1440x900.png')
  result.assertions.ownerGate = await page.getByLabel('Secret Chủ tịch local').isVisible()
  await page.getByLabel('Secret Chủ tịch local').fill(ownerSecret)
  await page.getByRole('button', { name: 'Đăng nhập Chủ tịch' }).click()
  await page.getByText(/Đã xác thực Chủ tịch trong scope demo/).waitFor()
  ownerSecret = ''

  for (const route of ['office', 'inspector', 'replay']) {
    await view(route, 'desktop', `${route}-desktop-1440x900.png`)
  }
  await page.goto(`${base}#settings`, { waitUntil: 'domcontentloaded' })
  await page.locator('#runtime-title').scrollIntoViewIfNeeded()
  await page.locator('#runtime-employee').waitFor()
  await page.getByText(/Strict CG01 is blocking dispatch/).waitFor({ timeout: 15000 })
  await page.waitForFunction(() => [...document.querySelectorAll('#runtime-employee option')].some(option => (option.textContent ?? '').includes('hồ sơ v')), null, { timeout: 15000 })
  const options = await page.locator('#runtime-employee option').allTextContents()
  result.assertions.demoEmployeeOptions = options.filter(value => value.includes('hồ sơ v')).length
  if (result.assertions.demoEmployeeOptions > 0) {
    await page.locator('#runtime-employee').selectOption({ index: 1 })
    result.assertions.employeeVersionSelectable = await page.locator('.runtime-grant-detail').count() > 0
  } else {
    result.assertions.employeeVersionSelectable = false
  }
  result.assertions.strictGateMessage = await page.getByText(/Strict CG01 is blocking dispatch/).count() > 0
  result.assertions.noEligibleGrantMessage = await page.getByText(/Chưa có grant còn hạn mức/).count() > 0
  result.assertions.startDisabled = !(await page.getByRole('button', { name: 'Bắt đầu Run text-only' }).isEnabled())
  await page.locator('#runtime-employee').scrollIntoViewIfNeeded()
  await page.screenshot({ path: resolve(screenshots, 'runtime-blocked-desktop-1440x900.png') })
  result.viewports['desktop:settings-runtime'] = { width: 1440, height: 900, scrollWidth: await page.evaluate(() => document.documentElement.scrollWidth), screenshot: 'screenshots/runtime-blocked-desktop-1440x900.png' }
  await page.getByRole('link', { name: /DEV Playground/ }).click()
  await page.waitForURL(/#playground/)
  await page.screenshot({ path: resolve(screenshots, 'playground-desktop-1440x900.png') })
  result.assertions.playgroundRoute = new URL(page.url()).hash === '#playground'

  for (const route of ['overview', 'office', 'inspector', 'replay', 'settings', 'playground']) {
    await page.setViewportSize({ width: 390, height: 844 })
    await page.goto(`${base}#${route}`, { waitUntil: 'domcontentloaded' })
    await page.locator(`a.nav-link[href="#${route}"].active`).waitFor()
    if (route === 'office' || route === 'inspector' || route === 'replay' || route === 'settings') await page.locator('#runtime-title').waitFor()
    if (route === 'settings') {
      await page.getByText(/Strict CG01 is blocking dispatch/).waitFor({ timeout: 15000 })
      await page.locator('#runtime-employee').scrollIntoViewIfNeeded()
    }
    if (route === 'settings') await page.locator('#runtime-title').scrollIntoViewIfNeeded()
    const filename = route === 'settings' ? 'runtime-blocked-mobile-390x844.png' : `${route}-mobile-390x844.png`
    const dims = await page.evaluate(() => ({ width: window.innerWidth, height: window.innerHeight, scrollWidth: document.documentElement.scrollWidth }))
    await page.screenshot({ path: resolve(screenshots, filename) })
    result.viewports[`mobile:${route}`] = { ...dims, screenshot: `screenshots/${filename}` }
  }
  result.assertions.mobileNoHorizontalOverflow = Object.entries(result.viewports)
    .filter(([key]) => key.startsWith('mobile:')).every(([, value]) => value.scrollWidth <= value.width)

  await page.goto(`${base}#settings`, { waitUntil: 'domcontentloaded' })
  await page.getByText(/Chủ tịch đã xác thực · Demo scope/).waitFor({ timeout: 15000 })
  const logout = page.getByRole('button', { name: 'Đăng xuất' })
  await logout.waitFor({ timeout: 15000 })
  await logout.click()
  await page.getByLabel('Secret Chủ tịch local').waitFor({ timeout: 15000 })
  result.logout = true
  writeFileSync(resolve(out, 'visual-acceptance.json'), `${JSON.stringify(result, null, 2)}\n`, { mode: 0o600 })
  console.log(JSON.stringify({ assertions: result.assertions, pageErrors: result.pageErrors, consoleErrors: result.consoleErrors, logout: result.logout }))
} finally {
  ownerSecret = ''
  await context.close()
  await browser.close()
}
