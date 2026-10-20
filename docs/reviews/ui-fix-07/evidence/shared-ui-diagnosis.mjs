import { chromium } from '/tmp/deployment06-playwright/node_modules/playwright/index.mjs'
import { execFileSync } from 'node:child_process'
import { mkdirSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

const root = process.cwd()
const output = resolve(root, 'docs/reviews/ui-fix-07/evidence')
mkdirSync(resolve(output, 'screenshots'), { recursive: true })
let ownerSecret = execFileSync('rtk', ['proxy', 'docker', 'compose', 'exec', '-T', 'api', 'cat', '/runtime-secrets/owner-secret'], {
  cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'],
}).trim()
const errors = []
const pageErrors = []
const browser = await chromium.launch({ headless: true, executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' })
const context = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 })
const page = await context.newPage()
page.on('console', message => { if (message.type() === 'error') errors.push({ text: message.text().slice(0, 500) }) })
page.on('pageerror', error => pageErrors.push(error.message.slice(0, 500)))

const httpErrors = []
page.on('response', response => {
  if (response.status() >= 400) {
    const url = new URL(response.url())
    httpErrors.push({ status: response.status(), method: response.request().method(), path: url.pathname })
  }
})
const result = { date: new Date().toISOString(), target: 'shared deployment; Owner-authenticated read-only route inspection', captures: {}, consoleErrors: errors, pageErrors, httpErrors }
try {
  await page.goto('http://agent-corporation.localhost/#settings', { waitUntil: 'domcontentloaded' })
  await page.getByLabel('Secret Chủ tịch local').fill(ownerSecret)
  await page.getByRole('button', { name: 'Đăng nhập Chủ tịch' }).click()
  await page.getByText(/Đã xác thực Chủ tịch trong scope demo/).waitFor({ timeout: 15000 })
  ownerSecret = ''

  await page.goto('http://agent-corporation.localhost/#playground', { waitUntil: 'domcontentloaded' })
  await page.locator('a.nav-link[href="#playground"].active').waitFor()
  await page.screenshot({ path: resolve(output, 'screenshots/playground-mobile-immediate-390x844.png') })
  result.captures.immediate = await page.evaluate(() => ({
    viewport: { width: innerWidth, height: innerHeight },
    bodyTextLength: document.body.innerText.length,
    playgroundHeadingPresent: Boolean(document.querySelector('.playground h2')),
    playgroundPanelPresent: Boolean(document.querySelector('.playground')),
  }))

  await page.getByRole('heading', { name: 'Trò chuyện thử với nhân viên demo' }).waitFor({ timeout: 15000 })
  await page.locator('.playground').waitFor({ state: 'visible', timeout: 15000 })
  await page.screenshot({ path: resolve(output, 'screenshots/playground-mobile-ready-390x844.png') })
  result.captures.ready = await page.evaluate(() => ({
    viewport: { width: innerWidth, height: innerHeight },
    scrollWidth: document.documentElement.scrollWidth,
    bodyTextLength: document.body.innerText.length,
    playgroundHeadingPresent: Boolean(document.querySelector('.playground h2')),
    loginFormPresent: Boolean(document.querySelector('.playground .runtime-login')),
    noGrantStatePresent: Boolean(document.querySelector('.playground-empty')),
  }))

  const owner = await page.evaluate(async () => {
    const response = await fetch('/api/v1/owner/session', { credentials: 'same-origin', cache: 'no-store' })
    return response.ok ? response.json() : null
  })
  if (owner) await page.evaluate(async csrf => {
    await fetch('/api/v1/owner/logout', { method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': csrf }, body: '{}' })
  }, owner.csrf_token)
  result.loggedOut = true
} finally {
  ownerSecret = ''
  await context.close()
  await browser.close()
}
result.consoleErrors = errors
result.pageErrors = pageErrors
result.httpErrors = httpErrors
writeFileSync(resolve(output, 'shared-ui-diagnosis.json'), `${JSON.stringify(result, null, 2)}\n`, { mode: 0o600 })
console.log(JSON.stringify(result))
