import { useEffect, useMemo, useState } from 'react'
import './App.css'

type CheckState = 'checking' | 'ok' | 'unavailable'
type Mode = 'chairman' | 'operator'

type Health = {
  api: CheckState
  database: CheckState
  message?: string
}

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
  { id: 'overview', code: 'S01', title: 'Tổng quan', group: 'Điều hành', description: 'Một điểm vào để xem tình hình doanh nghiệp và đi tới công việc cần quyết định.', next: 'Phase 03 bổ sung dữ liệu doanh nghiệp; Phase 04 mới có công ty demo.', phase: '03–04' },
  { id: 'office', code: 'S02', title: 'Văn phòng trực tiếp', group: 'Điều hành', description: 'Không gian 2D để quan sát hoạt động đã được hệ thống ghi nhận.', next: 'Sẽ hiển thị hoạt động từ event store; hiện chưa có event.', phase: '07' },
  { id: 'work', code: 'S05', title: 'Công việc', group: 'Điều hành', description: 'Work Order, kế hoạch và kết quả bàn giao được quản lý theo từng task.', next: 'Chưa có Work Order trong database. Không tạo task mẫu ở Phase 02.', phase: '03, 09' },
  { id: 'approvals', code: 'S06', title: 'Chờ Chủ tịch duyệt', group: 'Điều hành', description: 'Các đề xuất cần quyết định của Chủ tịch sẽ xuất hiện tại đây.', next: 'Approval queue được nối với task ở các phase dữ liệu và policy.', phase: '03, 10' },
  { id: 'inspector', code: 'S03', title: 'Agent Inspector', group: 'Quan sát', description: 'Xem danh tính, trạng thái, run và bằng chứng trong cùng một phạm vi.', next: 'Chưa có nhân sự hoặc run; màn hình này hiện là khung điều hướng.', phase: '07–08' },
  { id: 'replay', code: 'S04', title: 'Phát lại', group: 'Quan sát', description: 'Tái dựng một lượt chạy chỉ từ những event đã lưu.', next: 'Chưa có event để phát lại. Replay sau này chỉ đọc, không gọi tool.', phase: '08' },
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

function App() {
  const [activeId, setActiveId] = useState(getScreenFromHash)
  const [mode, setMode] = useState<Mode>('chairman')
  const [health, setHealth] = useState<Health>({ api: 'checking', database: 'checking' })
  const [healthReload, setHealthReload] = useState(0)
  const activeScreen = useMemo(() => screens.find((screen) => screen.id === activeId) ?? screens[0], [activeId])

  useEffect(() => {
    document.title = `Agent Corporation · ${activeScreen.title}`
  }, [activeScreen.title])

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

  const stateText = (state: CheckState) => state === 'ok' ? 'Đang hoạt động' : state === 'checking' ? 'Đang kiểm tra' : 'Chưa kết nối'

  return (
    <div className="app-shell">
      <a className="skip-link" href="#main-content">Bỏ qua điều hướng</a>
      <aside className="sidebar" aria-label="Điều hướng chính">
        <a className="brand" href="#overview" aria-label="Agent Corporation, tổng quan">
          <span className="brand-mark" aria-hidden="true">AC</span>
          <span className="brand-name">Agent Corporation<span>NỀN ĐIỀU HÀNH</span></span>
        </a>
        <div className="workspace-switcher"><span className="workspace-icon">A</span><span><strong>Không gian local</strong><small>Chưa có tập đoàn</small></span><span className="chevron">⌄</span></div>
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
            <span className="topbar-divider" />
            <div className="mode-switch" role="group" aria-label="Chọn góc nhìn">
              <button type="button" className={mode === 'chairman' ? 'selected' : ''} aria-pressed={mode === 'chairman'} onClick={() => setMode('chairman')}>Chủ tịch</button>
              <button type="button" className={mode === 'operator' ? 'selected' : ''} aria-pressed={mode === 'operator'} onClick={() => setMode('operator')}>Vận hành</button>
            </div>
            <button className="avatar-button" type="button" aria-label="Tài khoản Chủ tịch">C</button>
          </div>
        </header>

        <div className="content-wrap">
          <div className="page-heading">
            <div><p className="eyebrow">{activeScreen.code} <span>·</span> PHASE {activeScreen.phase}</p><h1>{activeScreen.title}</h1><p className="page-description">{activeScreen.description}</p></div>
            <span className={`page-state${activeId === 'onboarding' ? ' locked' : ''}`}>{activeId === 'onboarding' ? 'Đang khóa' : 'Chưa có dữ liệu'}</span>
          </div>

          {activeId === 'overview' ? (
            <>
              <section className="welcome-panel" aria-labelledby="welcome-title">
                <div className="welcome-copy"><p className="eyebrow">BẢN ĐIỀU HÀNH · LOCAL</p><h2 id="welcome-title">Một nền tảng đang thành hình.</h2><p>Dịch vụ nền đã sẵn sàng. Dữ liệu doanh nghiệp sẽ xuất hiện khi các phase tiếp theo được triển khai.</p><a className="text-link" href="#work">Khám phá không gian công việc <span aria-hidden="true">↗</span></a></div>
                <div className="welcome-ornament" aria-hidden="true"><span className="orbit orbit-one" /><span className="orbit orbit-two" /><span className="orbit-core">AC</span><span className="orbit-star">✳</span></div>
              </section>
              <div className="section-heading"><div><p className="eyebrow">TÌNH HÌNH HIỆN TẠI</p><h2>Chưa có nguồn dữ liệu nghiệp vụ</h2></div><span className="as-of">Dữ liệu được kiểm tra trực tiếp</span></div>
              <section className="overview-grid" aria-label="Tình hình hệ thống và doanh nghiệp">
                <article className="data-panel business-panel"><div className="panel-topline"><span className="panel-label">DOANH NGHIỆP</span><span className="unknown-mark">—</span></div><h3>Chưa được khởi tạo</h3><p>Chưa có công ty, nhân sự, công việc hay khoản chi trong môi trường này.</p><div className="panel-divider" /><a href="#organization" className="panel-link">Xem cấu trúc tổ chức <span>→</span></a></article>
                <article className="data-panel health-panel"><div className="panel-topline"><span className="panel-label">DỊCH VỤ LOCAL</span><span className={`live-indicator${health.api === 'unavailable' ? ' offline' : ''}`}><span /> {health.api === 'ok' ? 'SẴN SÀNG' : health.api === 'checking' ? 'ĐANG KIỂM TRA' : 'KHÔNG KẾT NỐI'}</span></div><div className="health-line"><span className={`health-icon ${health.api}`} aria-hidden="true">↗</span><span><strong>API nội bộ</strong><small>FastAPI · health/live</small></span><span className={`health-result ${health.api}`}>{stateText(health.api)}</span></div><div className="health-line"><span className={`health-icon ${health.database}`} aria-hidden="true">▤</span><span><strong>Cơ sở dữ liệu</strong><small>PostgreSQL · readiness</small></span><span className={`health-result ${health.database}`}>{stateText(health.database)}</span></div>{health.message && <p className="health-error" role="status">{health.message}</p>}<button className="quiet-button" type="button" onClick={() => { setHealth({ api: 'checking', database: 'checking' }); setHealthReload((value) => value + 1) }}>Kiểm tra lại dịch vụ <span aria-hidden="true">↻</span></button></article>
              </section>
              <div className="bottom-grid"><section className="data-panel next-panel"><div className="panel-topline"><span className="panel-label">LỘ TRÌNH SẮP TỚI</span><span className="phase-pill">PHASE 03</span></div><h3>Nền dữ liệu bền vững</h3><p>Task, trạng thái thực thi và event sẽ có định danh cùng lịch sử truy xuất.</p><a href="#work" className="panel-link">Xem khu vực công việc <span>→</span></a></section><section className="data-panel mode-panel"><div className="panel-topline"><span className="panel-label">GÓC NHÌN ĐANG DÙNG</span><span className="mode-symbol" aria-hidden="true">◉</span></div><h3>{mode === 'chairman' ? 'Chủ tịch' : 'Vận hành'}</h3><p>Hai góc nhìn cùng quyền Owner. Chuyển chế độ chỉ thay đổi cách trình bày.</p><span className="permission-note">Quyền API không thay đổi theo chế độ.</span></section></div>
            </>
          ) : activeId === 'settings' ? (
            <section className="screen-panel settings-layout"><div className="settings-main"><p className="eyebrow">TRẠNG THÁI KẾT NỐI</p><h2>Dịch vụ trên máy này</h2><p className="screen-copy">Các trạng thái bên dưới lấy từ health endpoint của API. Không thực hiện yêu cầu tới model hoặc gateway.</p><div className="settings-status"><span className={`health-icon ${health.api}`}>↗</span><div><strong>API nội bộ</strong><small>GET /api/v1/health/live</small></div><span className={`health-result ${health.api}`}>{stateText(health.api)}</span></div><div className="settings-status"><span className={`health-icon ${health.database}`}>▤</span><div><strong>PostgreSQL</strong><small>GET /api/v1/health/ready</small></div><span className={`health-result ${health.database}`}>{stateText(health.database)}</span></div>{health.message && <p className="health-error" role="status">{health.message}</p>}<button className="primary-button" onClick={() => { setHealth({ api: 'checking', database: 'checking' }); setHealthReload((value) => value + 1) }}>Kiểm tra lại</button></div><aside className="settings-aside"><span className="aside-mark">i</span><h3>Gateway inference</h3><p>Chưa được kiểm tra trong Phase 02. Capability probe thuộc Phase 05 và cần gate riêng.</p><strong>Grant hiện tại: 0</strong></aside></section>
          ) : activeId === 'onboarding' ? (
            <section className="locked-panel"><span className="locked-icon" aria-hidden="true">⌑</span><p className="eyebrow">MỞ SAU KHI PHÁT HÀNH V1</p><h2>Chưa thể thành lập công ty thật</h2><p>Wizard sẽ được mở sau release gate. Giao diện Phase 02 không tạo company, cấp quyền, chọn model hay khởi tạo agent.</p><span className="lock-caption">S14 · phase 21, 23</span></section>
          ) : (
            <section className="screen-panel preview-layout"><div className="preview-main"><div className="preview-toolbar"><span className="preview-dot" /><span>KHUNG GIAO DIỆN</span><span className="preview-separator">·</span><span>CHƯA CÓ DỮ LIỆU</span></div><div className="empty-illustration" aria-hidden="true"><span className="empty-ring ring-a" /><span className="empty-ring ring-b" /><span className="empty-glyph">{activeScreen.code.slice(1)}</span></div><p className="empty-title">Khu vực này đang chờ dữ liệu nền</p><p className="empty-copy">{activeScreen.next}</p><span className="empty-boundary">Phase 02 chỉ cung cấp điều hướng và trạng thái trống.</span></div><aside className="preview-aside"><p className="eyebrow">ĐƯỢC XÂY Ở PHASE</p><strong>{activeScreen.phase}</strong><p>Phạm vi được chia theo lộ trình đã duyệt. Khi phase tương ứng hoàn tất, dữ liệu thật sẽ được kết nối tại đây.</p><a href="#overview" className="panel-link">Quay lại tổng quan <span>→</span></a></aside></section>
          )}

          <footer className="page-footer"><span>Agent Corporation <i>·</i> Giao diện Phase 02</span><span>Inference chưa được cấp</span></footer>
        </div>
      </main>
    </div>
  )
}

export default App
