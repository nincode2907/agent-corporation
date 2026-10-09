import { useEffect, useMemo, useState } from 'react'
import './App.css'
import RuntimePanel from './RuntimePanel'

type CheckState = 'checking' | 'ok' | 'unavailable'
type Mode = 'chairman' | 'operator'
type Theme = 'light' | 'dark'

type Health = {
  api: CheckState
  database: CheckState
  message?: string
}

type GatewayProbe = {
  status: 'available' | 'offline' | 'auth_required' | 'rate_limited' | 'contract_mismatch' | 'configuration_error'
  health: string
  catalog: string
  models: string[]
  auth_configured: boolean
  entitlement_verified: false
  message: string
}

function isGatewayProbe(value: unknown): value is GatewayProbe {
  if (!value || typeof value !== 'object') return false
  const probe = value as Partial<GatewayProbe>
  return ['available', 'offline', 'auth_required', 'rate_limited', 'contract_mismatch', 'configuration_error'].includes(String(probe.status))
    && typeof probe.health === 'string'
    && typeof probe.catalog === 'string'
    && Array.isArray(probe.models)
    && probe.models.every((model) => typeof model === 'string')
    && typeof probe.auth_configured === 'boolean'
    && probe.entitlement_verified === false
    && typeof probe.message === 'string'
}

function gatewayContractError(message: string): GatewayProbe {
  return { status: 'contract_mismatch', health: 'unavailable', catalog: 'unavailable', models: [], auth_configured: false, entitlement_verified: false, message }
}

type DemoTask = { id: string; goal: string; status: string; runs: { attempt: number; status: string }[]; pending_approvals: number; has_artifact: boolean; usage_status: string; cost_basis: string; usd_cost_micros: number | null; fixture: boolean }
type DemoDashboard = { available: boolean; seed?: string; seed_version: number; manifest_sha256?: string; environment?: { name: string; kind: string }; company?: { name: string }; departments?: { id: string; name: string; employee_count: number }[]; employees?: { id: string; profile: { display_name: string; role: string }; version: number; department: string }[]; tasks?: DemoTask[]; usage?: { status: string; cost_basis: string; usd_cost_micros: number | null }; event_count?: number; message?: string }

type Screen = {
  id: string
  code: string
  title: string
  group: string
  description: string
  next: string
  phase: string
}

const screens: Screen[] = [
  { id: 'overview', code: 'S01', title: 'Tổng quan', group: 'Điều hành', description: 'Một điểm vào để xem tình hình doanh nghiệp và đi tới công việc cần quyết định.', next: 'Phase 03 đã bổ sung nền dữ liệu và event; Phase 04 mới tạo công ty demo để hiển thị dữ liệu.', phase: '03–04' },
  { id: 'office', code: 'S02', title: 'Văn phòng trực tiếp', group: 'Điều hành', description: 'Quan sát run và sự kiện đã ghi nhận trong phạm vi Owner.', next: 'Nguồn run thật phụ thuộc Phase 06–07, grant và gate CG01.', phase: '08' },
  { id: 'work', code: 'S05', title: 'Công việc', group: 'Điều hành', description: 'Work Order, kế hoạch và kết quả bàn giao được quản lý theo từng task.', next: 'Schema và command bền vững đã sẵn sàng; chưa có công ty demo hoặc Work Order để hiển thị.', phase: '03, 09' },
  { id: 'approvals', code: 'S06', title: 'Chờ Chủ tịch duyệt', group: 'Điều hành', description: 'Các đề xuất cần quyết định của Chủ tịch sẽ xuất hiện tại đây.', next: 'Approval queue được nối với task ở các phase dữ liệu và policy.', phase: '03, 10' },
  { id: 'inspector', code: 'S03', title: 'Agent Inspector', group: 'Quan sát', description: 'Mở run đã lưu để xem trạng thái, model, usage và event liên quan.', next: 'Thông tin chưa có nguồn được đánh dấu rõ; không suy diễn prompt, tool hoặc file diff.', phase: '08' },
  { id: 'replay', code: 'S04', title: 'Phát lại', group: 'Quan sát', description: 'Duyệt tuần tự event đã commit, lọc theo run và chọn mốc thời gian.', next: 'Replay chỉ đọc; khoảng trống và dữ liệu ngoài cửa sổ tải được hiển thị rõ.', phase: '08' },
  { id: 'quality', code: 'S10', title: 'Chất lượng', group: 'Quan sát', description: 'Theo dõi chất lượng bàn giao và kết quả benchmark có nguồn.', next: 'Chưa có kết quả đánh giá; số liệu unknown không được thay bằng 0.', phase: '13, 17' },
  { id: 'incidents', code: 'S11', title: 'Sự cố', group: 'Quan sát', description: 'Tập trung dấu hiệu lỗi, dừng khẩn cấp và hoạt động cần xử lý.', next: 'Chưa có incident domain. Health hệ thống nằm trong Quản trị.', phase: '19' },
  { id: 'organization', code: 'S07', title: 'Tổ chức', group: 'Quản trị', description: 'Cơ cấu phòng ban và hồ sơ nhân sự được version hóa.', next: 'Chưa có công ty hoặc nhân sự trong database.', phase: '12, 14' },
  { id: 'memory', code: 'S08', title: 'Bộ nhớ', group: 'Quản trị', description: 'Tài liệu và kiến thức có nguồn, phạm vi truy cập và lịch sử.', next: 'Memory chưa được tạo; không có dữ liệu seed.', phase: '15' },
  { id: 'finance', code: 'S09', title: 'Tài chính', group: 'Quản trị', description: 'Chi phí theo lượt gọi, task đã nghiệm thu và kỳ vận hành.', next: 'Không có usage hoặc giá được nạp; Phase 16 xây ledger.', phase: '16' },
  { id: 'reports', code: 'S12', title: 'Báo cáo', group: 'Quản trị', description: 'Báo cáo điều hành truy vết được về dữ liệu nguồn và thời điểm.', next: 'Chưa có nguồn báo cáo. Không tổng hợp từ fixture trong sản phẩm.', phase: '20' },
  { id: 'settings', code: 'S13', title: 'Cấu hình & sức khỏe', group: 'Quản trị', description: 'Cấu hình hiển thị và trạng thái các dịch vụ local đã kiểm tra.', next: 'Gateway chưa được probe ở Phase 02; bước kiểm tra gateway thuộc Phase 05.', phase: '05, 22' },
  { id: 'onboarding', code: 'S14', title: 'Thành lập tập đoàn', group: 'Quản trị', description: 'Wizard tạo công ty thật, chọn chính sách và bổ nhiệm Chief of Staff.', next: 'Đang khóa tới sau khi phát hành V1; Phase 02 không thể tạo công ty.', phase: '21, 23' },
]

const groups = ['Điều hành', 'Quan sát', 'Quản trị']

function getScreenFromHash() {
  const id = window.location.hash.replace(/^#\/?/, '') || 'overview'
  return screens.find((screen) => screen.id === id)?.id ?? 'overview'
}

function getInitialTheme(): Theme {
  try {
    const saved = window.localStorage.getItem('agent-corporation.theme')
    if (saved === 'dark' || saved === 'light') return saved
  } catch {
    // Storage may be unavailable in a restricted browser context.
  }
  return window.matchMedia?.('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

function App() {
  const [activeId, setActiveId] = useState(getScreenFromHash)
  const [mode, setMode] = useState<Mode>('chairman')
  const [theme, setTheme] = useState<Theme>(getInitialTheme)
  const [health, setHealth] = useState<Health>({ api: 'checking', database: 'checking' })
  const [healthReload, setHealthReload] = useState(0)
  const [gatewayProbe, setGatewayProbe] = useState<GatewayProbe | null>(null)
  const [gatewayProbing, setGatewayProbing] = useState(false)
  const [demo, setDemo] = useState<DemoDashboard | null>(null)
  const [demoError, setDemoError] = useState('')
  const [demoReload, setDemoReload] = useState(0)
  const [resetting, setResetting] = useState(false)
  const activeScreen = useMemo(() => screens.find((screen) => screen.id === activeId) ?? screens[0], [activeId])

  useEffect(() => {
    document.title = `Agent Corporation · ${activeScreen.title}`
  }, [activeScreen.title])

  useEffect(() => {
    document.documentElement.dataset.theme = theme
    document.documentElement.style.colorScheme = theme
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', theme === 'dark' ? '#111713' : '#f6f7f3')
    try {
      window.localStorage.setItem('agent-corporation.theme', theme)
    } catch {
      // The selected theme remains active for the current page even if it cannot persist.
    }
  }, [theme])

  useEffect(() => {
    const onHashChange = () => setActiveId(getScreenFromHash())
    window.addEventListener('hashchange', onHashChange)
    return () => window.removeEventListener('hashchange', onHashChange)
  }, [])

  useEffect(() => {
    const controller = new AbortController()
    const timeout = window.setTimeout(() => controller.abort(), 4000)
    async function checkHealth() {
      try {
        const live = await fetch('/api/v1/health/live', { signal: controller.signal })
        if (!live.ok) throw new Error('API trả về trạng thái không sẵn sàng')
        const ready = await fetch('/api/v1/health/ready', { signal: controller.signal })
        const data = (await ready.json()) as { checks?: { database?: string } }
        setHealth({
          api: 'ok',
          database: ready.ok && data.checks?.database === 'ok' ? 'ok' : 'unavailable',
          message: ready.ok ? undefined : 'API có phản hồi nhưng readiness chưa đạt.',
        })
      } catch {
        setHealth({ api: 'unavailable', database: 'unavailable', message: 'Không lấy được trạng thái hệ thống. Kiểm tra API local rồi thử lại.' })
      } finally {
        window.clearTimeout(timeout)
      }
    }
    void checkHealth()
    return () => {
      controller.abort()
      window.clearTimeout(timeout)
    }
  }, [healthReload])

  useEffect(() => {
    const controller = new AbortController()
    const timeout = window.setTimeout(() => controller.abort(), 5000)
    fetch('/api/v1/demo/dashboard', { signal: controller.signal })
      .then(async (response) => {
        if (!response.ok) throw new Error('Không đọc được bộ dữ liệu demo từ API local.')
        return await response.json() as DemoDashboard
      })
      .then((data) => { setDemo(data); setDemoError('') })
      .catch(() => { setDemo(null); setDemoError('Không đọc được demo. Seed tường minh bằng scripts/seed_demo.py --seed.') })
      .finally(() => window.clearTimeout(timeout))
    return () => { controller.abort(); window.clearTimeout(timeout) }
  }, [demoReload])

  async function resetDemo() {
    if (!window.confirm('Đặt lại toàn bộ fixture trong Demo Corporation? Chỉ scope demo cố định bị reset; không ảnh hưởng công ty thật.')) return
    setResetting(true)
    try {
      const sessionResponse = await fetch('/api/v1/owner/session', { credentials: 'same-origin' })
      if (!sessionResponse.ok) throw new Error('Đăng nhập Chủ tịch trong Quản trị trước khi reset demo.')
      const ownerSession = await sessionResponse.json() as { csrf_token: string }
      const response = await fetch('/api/v1/demo/reset', { method: 'POST', headers: { 'content-type': 'application/json', 'X-CSRF-Token': ownerSession.csrf_token }, body: JSON.stringify({ confirmed: true }) })
      if (!response.ok) throw new Error('API từ chối reset fixture demo.')
      setDemo(await response.json() as DemoDashboard)
      setDemoError('')
    } catch (error) {
      setDemoError(error instanceof Error ? error.message : 'Reset demo không thành công.')
    } finally {
      setResetting(false)
    }
  }

  async function probeGateway() {
    setGatewayProbing(true)
    try {
      const response = await fetch('/api/v1/codex/probe', { signal: AbortSignal.timeout(5000) })
      if (!response.ok) {
        setGatewayProbe(gatewayContractError(`API probe không khả dụng (HTTP ${response.status}). Cập nhật API local rồi thử lại.`))
        return
      }
      let data: unknown
      try {
        data = await response.json()
      } catch {
        setGatewayProbe(gatewayContractError('API probe trả dữ liệu không đọc được. Kiểm tra contract API rồi thử lại.'))
        return
      }
      setGatewayProbe(isGatewayProbe(data) ? data : gatewayContractError('API probe trả dữ liệu không đúng contract. Kiểm tra phiên bản API rồi thử lại.'))
    } catch {
      setGatewayProbe({ status: 'offline', health: 'unavailable', catalog: 'unavailable', models: [], auth_configured: false, entitlement_verified: false, message: 'Không kết nối được API nội bộ để probe. Kiểm tra dịch vụ local rồi thử lại.' })
    } finally {
      setGatewayProbing(false)
    }
  }

  const stateText = (state: CheckState) => state === 'ok' ? 'Đang hoạt động' : state === 'checking' ? 'Đang kiểm tra' : 'Chưa kết nối'

  return (
    <div className="app-shell">
      <a className="skip-link" href="#main-content">Bỏ qua điều hướng</a>
      <aside className="sidebar" aria-label="Điều hướng chính">
        <a className="brand" href="#overview" aria-label="Agent Corporation, tổng quan">
          <span className="brand-mark" aria-hidden="true">AC</span>
          <span className="brand-name">Agent Corporation<span>NỀN ĐIỀU HÀNH</span></span>
        </a>
        <div className="workspace-switcher"><span className="workspace-icon">A</span><span><strong>Không gian local</strong><small>{demo?.available ? 'Demo Corporation · fixture' : 'Chưa có công ty thật'}</small></span><span className="chevron">⌄</span></div>
        <nav className="primary-nav">
          {groups.map((group) => (
            <div className="nav-group" key={group}>
              <p className="nav-heading">{group}</p>
              {screens.filter((screen) => screen.group === group).map((screen) => (
                <a className={`nav-link${activeId === screen.id ? ' active' : ''}`} href={`#${screen.id}`} key={screen.id} aria-current={activeId === screen.id ? 'page' : undefined}>
                  <span className="nav-code">{screen.code}</span><span>{screen.title}</span>{screen.id === 'onboarding' && <span className="nav-lock" aria-label="Đang khóa">•</span>}
                </a>
              ))}
            </div>
          ))}
        </nav>
        <div className="sidebar-bottom">
          <div className="grant-note"><span className="grant-dot" /><span><strong>Inference grant</strong><small>Chưa được cấp</small></span></div>
          <a className="owner-profile" href="#settings"><span className="owner-avatar">C</span><span><strong>Chủ tịch</strong><small>Owner · local</small></span><span className="chevron">···</span></a>
        </div>
      </aside>

      <main id="main-content" className="main-area">
        <header className="topbar">
          <div className="breadcrumbs"><span>Không gian local</span><span className="crumb-sep">/</span><strong>{activeScreen.title}</strong></div>
          <div className="topbar-actions">
            <div className="environment"><span className="environment-dot" />Local</div>
            <button className="theme-toggle" type="button" aria-pressed={theme === 'dark'} aria-label={theme === 'dark' ? 'Chuyển sang giao diện sáng' : 'Chuyển sang giao diện tối'} onClick={() => setTheme((current) => current === 'dark' ? 'light' : 'dark')}>
              <span aria-hidden="true">{theme === 'dark' ? '☼' : '◐'}</span><span className="theme-label">{theme === 'dark' ? 'Giao diện tối' : 'Giao diện sáng'}</span>
            </button>
            <span className="topbar-divider" />
            <div className="mode-switch" role="group" aria-label="Chọn góc nhìn">
              <button type="button" className={mode === 'chairman' ? 'selected' : ''} aria-pressed={mode === 'chairman'} onClick={() => setMode('chairman')}>Chủ tịch</button>
              <button type="button" className={mode === 'operator' ? 'selected' : ''} aria-pressed={mode === 'operator'} onClick={() => setMode('operator')}>Vận hành</button>
            </div>
            <button className="avatar-button" type="button" aria-label="Tài khoản Chủ tịch">C</button>
          </div>
        </header>

        <div className="content-wrap">
          <section className="demo-strip" aria-label="Môi trường dữ liệu">
            <span className="demo-mark">DEMO</span>
            <span className="demo-strip-copy"><strong>{demo?.company?.name ?? 'Môi trường demo'}</strong><small>{demo?.available ? `Fixture v${demo.seed_version} · usage chưa biết · inference 0` : demoError || 'Đang đọc fixture…'}</small></span>
            <button className="demo-reset" type="button" onClick={() => void resetDemo()} disabled={!demo?.available || resetting}>{resetting ? 'Đang đặt lại…' : 'Đặt lại demo'}</button>
          </section>
          {demoError && <p className="demo-error" role="status">{demoError}</p>}
          <div className="page-heading">
            <div><p className="eyebrow">{activeScreen.code} <span>·</span> PHASE {activeScreen.phase}</p><h1>{activeScreen.title}</h1><p className="page-description">{activeScreen.description}</p></div>
            <span className={`page-state${activeId === 'onboarding' ? ' locked' : ''}`}>{activeId === 'onboarding' ? 'Đang khóa' : ['office', 'inspector', 'replay'].includes(activeId) ? 'Cần session Owner' : demo?.available ? 'Dữ liệu demo' : 'Chưa có dữ liệu'}</span>
          </div>

          {demo?.available && activeId === 'overview' ? (
            <>
              <section className="welcome-panel" aria-labelledby="welcome-title">
                <div className="welcome-copy"><p className="eyebrow">FIXTURE CỐ ĐỊNH · SEED V{demo.seed_version}</p><h2 id="welcome-title">Quan sát quy trình trên dữ liệu demo.</h2><p>Không tạo agent thật, không gọi model. Đây là môi trường demo tách biệt để nghiệm thu giao diện.</p><a className="text-link" href="#work">Xem các Work Order <span aria-hidden="true">↗</span></a></div>
                <div className="welcome-ornament" aria-hidden="true"><span className="orbit orbit-one" /><span className="orbit orbit-two" /><span className="orbit-core">AC</span><span className="orbit-star">✳</span></div>
              </section>
              <div className="section-heading"><div><p className="eyebrow">TÌNH HÌNH DEMO</p><h2>{demo.company?.name}</h2></div><span className="as-of">Manifest {demo.manifest_sha256?.slice(0, 12)}</span></div>
              <section className="overview-grid" aria-label="Tình hình hệ thống và doanh nghiệp">
                <article className="data-panel business-panel"><div className="panel-topline"><span className="panel-label">DOANH NGHIỆP GIẢ LẬP</span><span className="fixture-badge">DEMO</span></div><h3>{demo.employees?.length ?? 0} hồ sơ nhân sự</h3><p>{demo.departments?.length ?? 0} phòng ban · {demo.tasks?.length ?? 0} Work Order · {demo.event_count ?? 0} event fixture.</p><div className="panel-divider" /><a href="#organization" className="panel-link">Xem cấu trúc tổ chức <span>→</span></a></article>
                <article className="data-panel health-panel"><div className="panel-topline"><span className="panel-label">DỊCH VỤ LOCAL</span><span className={`live-indicator${health.api === 'unavailable' ? ' offline' : ''}`}><span /> {health.api === 'ok' ? 'SẴN SÀNG' : health.api === 'checking' ? 'ĐANG KIỂM TRA' : 'KHÔNG KẾT NỐI'}</span></div><div className="health-line"><span className={`health-icon ${health.api}`} aria-hidden="true">↗</span><span><strong>API nội bộ</strong><small>FastAPI · health/live</small></span><span className={`health-result ${health.api}`}>{stateText(health.api)}</span></div><div className="health-line"><span className={`health-icon ${health.database}`} aria-hidden="true">▤</span><span><strong>Cơ sở dữ liệu</strong><small>PostgreSQL · readiness</small></span><span className={`health-result ${health.database}`}>{stateText(health.database)}</span></div>{health.message && <p className="health-error" role="status">{health.message}</p>}<button className="quiet-button" type="button" onClick={() => { setHealth({ api: 'checking', database: 'checking' }); setHealthReload((value) => value + 1) }}>Kiểm tra lại dịch vụ <span aria-hidden="true">↻</span></button></article>
              </section>
              <div className="bottom-grid"><section className="data-panel next-panel"><div className="panel-topline"><span className="panel-label">USAGE VÀ CHI PHÍ</span><span className="fixture-badge">UNKNOWN</span></div><h3>Chưa xác định</h3><p>Usage chưa được đo; chi phí không phải 0. Không có inference request trong seed/reset.</p><a href="#finance" className="panel-link">Mở tài chính <span>→</span></a></section><section className="data-panel mode-panel"><div className="panel-topline"><span className="panel-label">GÓC NHÌN ĐANG DÙNG</span><span className="mode-symbol" aria-hidden="true">◉</span></div><h3>{mode === 'chairman' ? 'Chủ tịch' : 'Vận hành'}</h3><p>Chế độ chỉ đổi cách trình bày; không đổi quyền API.</p><span className="permission-note">Inference grant: chưa được cấp.</span></section></div>
            </>
          ) : demo?.available && ['work', 'approvals', 'quality', 'incidents', 'organization', 'memory', 'finance', 'reports'].includes(activeId) ? (
            <DemoScreen screenId={activeId} demo={demo} />
          ) : activeId === 'settings' ? (
            <section className="screen-panel settings-layout"><div className="settings-main"><p className="eyebrow">TRẠNG THÁI KẾT NỐI</p><h2>Dịch vụ trên máy này</h2><p className="screen-copy">Health API/DB được tải khi mở ứng dụng. Gateway chỉ được gọi khi bạn bấm probe; thao tác này chỉ GET health và catalog, không gọi model.</p><div className="settings-status"><span className={`health-icon ${health.api}`}>↗</span><div><strong>API nội bộ</strong><small>GET /api/v1/health/live</small></div><span className={`health-result ${health.api}`}>{stateText(health.api)}</span></div><div className="settings-status"><span className={`health-icon ${health.database}`}>▤</span><div><strong>PostgreSQL</strong><small>GET /api/v1/health/ready</small></div><span className={`health-result ${health.database}`}>{stateText(health.database)}</span></div>{health.message && <p className="health-error" role="status">{health.message}</p>}<button className="primary-button" onClick={() => { setHealth({ api: 'checking', database: 'checking' }); setHealthReload((value) => value + 1) }}>Kiểm tra lại</button><div className="gateway-panel"><div className="gateway-heading"><div><p className="eyebrow">CODEX SERVER LOCAL</p><h2>Gateway và model catalog</h2></div><button className="quiet-button" type="button" onClick={() => void probeGateway()} disabled={gatewayProbing}>{gatewayProbing ? 'Đang kiểm tra…' : 'Probe gateway'}</button></div><p className="screen-copy">Base URL do backend cấu hình. Không gửi prompt, không tạo session. Model trong catalog không đồng nghĩa account có entitlement.</p>{gatewayProbe ? <div className="gateway-result" role="status"><strong>{gatewayProbe.status === 'available' ? 'Gateway phản hồi' : gatewayProbe.status === 'offline' ? 'Không kết nối được' : gatewayProbe.status === 'auth_required' ? 'Cần xác thực gateway' : gatewayProbe.status === 'rate_limited' ? 'Gateway đang giới hạn probe' : 'Contract/cấu hình cần kiểm tra'}</strong><span>{gatewayProbe.message}</span><small>Health: {gatewayProbe.health} · Catalog: {gatewayProbe.catalog} · Secret reference phía backend: {gatewayProbe.auth_configured ? 'đã cấu hình' : 'chưa cấu hình'}</small>{gatewayProbe.models.length > 0 && <div className="gateway-model-list"><span>Catalog (chỉ để tham khảo)</span>{gatewayProbe.models.map((model) => <code key={model}>{model}</code>)}</div>}</div> : <p className="gateway-empty">Chưa chạy probe trong phiên này.</p>}<div className="profile-locked"><strong>Model profile / quyền Owner</strong><span>Đăng nhập Chủ tịch để cấu hình profile trong bảng runtime bên dưới. Entitlement chỉ được kiểm tra trong đợt run có grant riêng.</span></div></div></div><aside className="settings-aside"><span className="aside-mark">i</span><h3>Capability và quyền</h3><p>Probe chỉ xác nhận contract GET health/models. Không kiểm tra streaming, max_tokens, session API, quyền tài khoản hoặc privacy/retention.</p><strong>Inference grant: 0 · Chưa gọi model</strong></aside></section>
          ) : activeId === 'onboarding' ? (
            <section className="locked-panel"><span className="locked-icon" aria-hidden="true">⌑</span><p className="eyebrow">MỞ SAU KHI PHÁT HÀNH V1</p><h2>Chưa thể thành lập công ty thật</h2><p>Phase 04 chỉ tạo fixture trong scope demo cố định. Wizard này không tạo company thật, cấp quyền, chọn model hay khởi tạo agent.</p><span className="lock-caption">S14 · phase 21, 23</span></section>
          ) : ['office', 'inspector', 'replay'].includes(activeId) ? (
            <RuntimePanel view={activeId as 'office' | 'inspector' | 'replay'} departments={(demo?.departments ?? []).map((department) => department.name)} />
          ) : (
            <section className="screen-panel preview-layout"><div className="preview-main"><div className="preview-toolbar"><span className="preview-dot" /><span>MÔI TRƯỜNG DEMO</span><span className="preview-separator">·</span><span>CHƯA CÓ FIXTURE</span></div><div className="empty-illustration" aria-hidden="true"><span className="empty-ring ring-a" /><span className="empty-ring ring-b" /><span className="empty-glyph">{activeScreen.code.slice(1)}</span></div><p className="empty-title">Chưa có dữ liệu demo</p><p className="empty-copy">{demo?.message || demoError || activeScreen.next}</p><button className="primary-button" type="button" onClick={() => setDemoReload((value) => value + 1)}>Tải lại dữ liệu demo</button></div><aside className="preview-aside"><p className="eyebrow">ĐƯỢC XÂY Ở PHASE</p><strong>{activeScreen.phase}</strong><p>Seed là thao tác tường minh. Mở trang và health check không gọi model.</p><a href="#overview" className="panel-link">Quay lại tổng quan <span>→</span></a></aside></section>
          )}

          {activeId === 'settings' && <RuntimePanel />}
          <footer className="page-footer"><span>Agent Corporation <i>·</i> Không gian điều hành local</span><span>Inference chỉ theo grant riêng</span></footer>
        </div>
      </main>
    </div>
  )
}

function DemoScreen({ screenId, demo }: { screenId: string; demo: DemoDashboard }) {
  const tasks = demo.tasks ?? []
  const stateLabel: Record<string, string> = {
    draft: 'Chưa bắt đầu', executing: 'Đang chạy (fixture)', awaiting_approval: 'Chờ duyệt (fixture)',
    failed: 'Thất bại (fixture)', rework: 'Đang sửa / retry (fixture)',
  }
  if (screenId === 'organization') return <section className="demo-card"><div className="demo-card-heading"><div><p className="eyebrow">CƠ CẤU DEMO</p><h2>{demo.company?.name}</h2></div><span className="fixture-badge">DEMO FIXTURE</span></div><div className="org-grid">{(demo.departments ?? []).map((department) => <article className="org-unit" key={department.id}><span className="fixture-badge">DEMO</span><h3>{department.name}</h3><p>{department.employee_count} hồ sơ nhân sự</p>{(demo.employees ?? []).filter((employee) => employee.department === department.name).map((employee) => <div className="employee-row" key={employee.id}><span className="owner-avatar">{employee.profile.display_name.slice(0, 1)}</span><span><strong>{employee.profile.display_name}</strong><small>{employee.profile.role} · hồ sơ v{employee.version}</small></span></div>)}</article>)}</div></section>
  if (screenId === 'work' || screenId === 'approvals' || screenId === 'inspector' || screenId === 'replay' || screenId === 'incidents' || screenId === 'office') {
    const filtered = screenId === 'approvals' ? tasks.filter((task) => task.pending_approvals > 0) : screenId === 'incidents' ? tasks.filter((task) => task.status === 'failed' || task.status === 'rework') : tasks
    return <section className="demo-card"><div className="demo-card-heading"><div><p className="eyebrow">{screenId === 'approvals' ? 'HÀNG CHỜ PHÊ DUYỆT' : screenId === 'inspector' ? 'RUN VÀ BẰNG CHỨNG' : 'WORK ORDER FIXTURE'}</p><h2>{screenId === 'approvals' ? `${filtered.reduce((sum, task) => sum + task.pending_approvals, 0)} yêu cầu đang chờ` : screenId === 'inspector' ? 'Run mẫu trong scope demo' : screenId === 'incidents' ? 'Fixture lỗi có chủ đích' : screenId === 'office' ? 'Hoạt động được ghi nhận' : screenId === 'replay' ? 'Timeline từ event fixture' : 'Trạng thái công việc'}</h2></div><span className="fixture-badge">DEMO · V{demo.seed_version}</span></div><div className="task-list">{filtered.map((task) => <article className="task-row" key={task.id}><div className="task-main"><span className="fixture-badge">DEMO</span><strong>{task.goal}</strong><small>{task.id.slice(0, 8)} · usage chưa biết · không có inference</small></div><span className={`task-state state-${task.status}`}>{stateLabel[task.status] ?? task.status}</span><div className="run-list">{task.runs.map((run) => <span key={`${task.id}-${run.attempt}`}>Lượt {run.attempt}: {run.status}</span>)}{task.pending_approvals > 0 && <span>Phê duyệt: đang chờ</span>}{task.has_artifact && <span>Bằng chứng lỗi: metadata fixture</span>}</div></article>)}</div></section>
  }
  if (screenId === 'finance' || screenId === 'quality') return <section className="demo-card"><div className="demo-card-heading"><div><p className="eyebrow">BÁO CÁO FIXTURE</p><h2>{screenId === 'finance' ? 'Usage và chi phí chưa biết' : 'Chưa có kết quả đánh giá'}</h2></div><span className="fixture-badge">DEMO · UNKNOWN</span></div><div className="unknown-metric"><strong>Chưa biết</strong><span>Không có usage thực hoặc ledger trong Phase 04. Không hiển thị số 0 thay thế.</span></div></section>
  if (screenId === 'memory' || screenId === 'reports') return <section className="demo-card"><div className="demo-card-heading"><div><p className="eyebrow">KHÔNG CÓ NGUỒN FIXTURE CHO MÀN HÌNH NÀY</p><h2>{screenId === 'memory' ? 'Memory chưa được seed' : 'Chưa có báo cáo nghiệp vụ'}</h2></div><span className="fixture-badge">DEMO SCOPE</span></div><p className="screen-copy">Màn hình vẫn mang nhãn demo; không tổng hợp dữ liệu fixture thành memory hoặc báo cáo có vẻ là dữ liệu thật.</p></section>
  return <section className="demo-card"><div className="demo-card-heading"><div><p className="eyebrow">EVENT FIXTURE</p><h2>{demo.event_count ?? 0} sự kiện demo đã lưu</h2></div><span className="fixture-badge">DEMO</span></div><p className="screen-copy">Dữ liệu mô phỏng cố định · seed v{demo.seed_version} · trạng thái run không phản ánh agent đang hoạt động.</p></section>
}

export default App
