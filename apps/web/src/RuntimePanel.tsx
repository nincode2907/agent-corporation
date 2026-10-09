import { useEffect, useRef, useState } from 'react'
import type { FormEvent } from 'react'
import './RuntimePanel.css'

type OwnerSession = { authenticated: true; owner_id: string; session_id: string; scope: { environment_id: string; company_id: string }; csrf_token: string }
type Profile = { version: number; model: string | null; reasoning_effort: string | null; fallback_models: string[] }
type Grant = { id: string; phase: string; batch_id: string; purpose: string; model: string; effort: string; max_requests: number; used_requests: number; expires_at: string; revoked: boolean }
type Run = { id: string; task_id?: string; status: string; model: string; effort: string; stop_requested: boolean; outcome: unknown; usage: unknown; output?: unknown; created_at: string; worker_heartbeat_at?: string | null; lease_until?: string | null }
type RuntimeStatus = { cg01: { allowed: boolean; reason: string }; inference_grants: number; runs: Run[] }
type DomainEvent = { event_id: string; stream_seq: number; event_type: string; occurred_at: string; recorded_at: string; run_id: string | null; task_id?: string | null; agent_id?: string | null; source: string; payload: unknown; sensitivity?: string; content_withheld?: boolean }
type EventBatch = { events: DomainEvent[]; cursor: string; latest_seq: number; server_time: string }
type Connection = 'connecting' | 'live' | 'reconnecting' | 'stale' | 'gap' | 'offline'
const connectionLabel: Record<Connection, string> = { connecting: 'Đang kết nối', live: 'Đã kết nối', reconnecting: 'Đang kết nối lại', stale: 'Dữ liệu đã cũ', gap: 'Có khoảng trống dữ liệu', offline: 'Mất kết nối' }
const runLabel: Record<string, string> = { queued: 'Đang chờ', waiting: 'Đang chờ model', waiting_model: 'Đang chờ model', running: 'Đang xử lý', completed: 'Hoàn tất', succeeded: 'Hoàn tất', failed: 'Thất bại', aborted: 'Đã dừng', stopped: 'Đã dừng', cancelled: 'Đã dừng trước dispatch', interrupted: 'Bị gián đoạn · kết quả chưa được xác nhận', unknown: 'Chưa biết kết quả', outcome_unknown: 'Chưa biết kết quả' }
class ApiError extends Error { status: number; constructor(status: number, message: string) { super(message); this.status = status } }
function isDomainEvent(value: unknown): value is DomainEvent {
  if (!value || typeof value !== 'object') return false
  const event = value as Partial<DomainEvent>
  return typeof event.event_id === 'string' && Number.isSafeInteger(event.stream_seq) && Number(event.stream_seq) > 0 && typeof event.event_type === 'string' && typeof event.recorded_at === 'string' && typeof event.source === 'string'
}

function display(value: unknown) { return typeof value === 'string' ? value : value === null || value === undefined ? 'Chưa biết' : JSON.stringify(value) }
function time(value: string | null) { return value ? new Date(value).toLocaleString('vi-VN') : 'Chưa có cập nhật' }

type ObservationView = 'office' | 'inspector' | 'replay'

export default function RuntimePanel({ view = 'runtime', departments = [] }: { view?: 'runtime' | ObservationView; departments?: string[] }) {
  const [session, setSession] = useState<OwnerSession | null>(null)
  const [checked, setChecked] = useState(false)
  const [secret, setSecret] = useState('')
  const [profile, setProfile] = useState<Profile | null>(null)
  const [model, setModel] = useState('')
  const [effort, setEffort] = useState('medium')
  const [fallback, setFallback] = useState('')
  const [runtime, setRuntime] = useState<RuntimeStatus | null>(null)
  const [grants, setGrants] = useState<Grant[]>([])
  const [grantId, setGrantId] = useState('')
  const [input, setInput] = useState('')
  const [runs, setRuns] = useState<Run[]>([])
  const [events, setEvents] = useState<DomainEvent[]>([])
  const [connection, setConnection] = useState<Connection>('offline')
  const [lastSeen, setLastSeen] = useState<string | null>(null)
  const [clockNow, setClockNow] = useState(Date.now)
  const [runReadFailed, setRunReadFailed] = useState(false)
  const [cachedIds, setCachedIds] = useState<Set<string>>(new Set())
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')
  const [busy, setBusy] = useState(false)
  const [reload, setReload] = useState(0)
  const stream = useRef<EventSource | null>(null)
  const lastBeat = useRef(0)
  const sequence = useRef(0)
  const eventHistory = useRef<DomainEvent[]>([])
  const currentRuns = useRef<Run[]>([])
  const currentSession = useRef<OwnerSession | null>(null)
  currentSession.current = session
  currentRuns.current = runs

  function discardSession() {
    stream.current?.close()
    stream.current = null
    const previous = currentSession.current
    if (previous) { try { sessionStorage.removeItem(`ac.events.${previous.session_id}`) } catch { /* Storage is optional. */ } }
    setSession(null); setProfile(null); setRuntime(null); setGrants([]); setRuns([]); setEvents([]); setCachedIds(new Set()); eventHistory.current = []; setLastSeen(null); sequence.current = 0; setConnection('offline')
  }

  async function request<T>(path: string, body?: unknown, method = 'POST'): Promise<T> {
    const sentSessionId = currentSession.current?.session_id
    let response: Response
    try { response = await fetch(`/api/v1/${path}`, { credentials: 'same-origin', cache: 'no-store', signal: AbortSignal.timeout(10000), ...(body === undefined ? {} : { method, headers: { 'Content-Type': 'application/json', ...(currentSession.current ? { 'X-CSRF-Token': currentSession.current.csrf_token } : {}) }, body: JSON.stringify(body) }) }) }
    catch { throw new Error(body === undefined ? 'Không nhận được phản hồi từ API local. Kiểm tra kết nối rồi tải lại.' : 'Chưa biết API đã ghi thao tác hay chưa. Đối chiếu trạng thái trước khi gửi lại.') }
    let data: unknown
    try { data = await response.json() } catch { throw new Error('API không trả về dữ liệu hợp lệ. Kiểm tra phiên bản API rồi thử lại.') }
    if (!response.ok) {
      if (response.status === 401 && currentSession.current && currentSession.current.session_id === sentSessionId) discardSession()
      const detail = data && typeof data === 'object' && 'detail' in data ? (data as { detail: unknown }).detail : null
      throw new ApiError(response.status, typeof detail === 'string' ? detail : `API trả về lỗi ${response.status}. Thao tác chưa được xác nhận; không tự gửi lại.`)
    }
    return data as T
  }

  useEffect(() => {
    let active = true
    fetch('/api/v1/owner/session', { credentials: 'same-origin', cache: 'no-store', signal: AbortSignal.timeout(10000) }).then(async response => {
      if (response.status === 401) return null
      if (!response.ok) throw new Error('Chưa lấy được session Chủ tịch. Kiểm tra API local.')
      return await response.json() as OwnerSession
    }).then(value => { if (active) setSession(value) }).catch(() => { if (active) setError('Không xác minh được session. Kiểm tra API local rồi tải lại trang.') }).finally(() => { if (active) setChecked(true) })
    return () => { active = false }
  }, [])

  useEffect(() => {
    if (!session) return
    let active = true
    async function load() {
      try {
        const [saved, state, available] = await Promise.all([request<Profile>('owner/profile'), request<RuntimeStatus>('runtime/status'), request<Grant[] | { grants: Grant[] }>('runtime/grants')])
        if (!active) return
        setProfile(saved); setModel(saved.model ?? ''); setEffort(saved.reasoning_effort ?? 'medium'); setFallback(saved.fallback_models.join(', ')); setRuntime(state); setRuns(state.runs); setRunReadFailed(false)
        setGrants(Array.isArray(available) ? available : available.grants)
      } catch (reason) { if (active) setError((reason as Error).message) }
    }
    void load()
    return () => { active = false }
    // Read-only reload follows session or an explicit refresh, never model dispatch.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [session, reload])

  useEffect(() => {
    if (!session) return
    let active = true
    let reading = false
    const timer = window.setInterval(() => {
      setClockNow(Date.now())
      if (reading || !currentRuns.current.some(run => ['waiting_model', 'running'].includes(run.status))) return
      reading = true
      void request<RuntimeStatus>('runtime/status').then(state => { if (active && currentSession.current?.session_id === session.session_id) { setRuntime(state); setRuns(state.runs); setRunReadFailed(false) } }).catch(() => { if (active) setRunReadFailed(true) }).finally(() => { reading = false })
    }, 10000)
    return () => { active = false; window.clearInterval(timer) }
    // Only read stored run state; a heartbeat poll never dispatches inference.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [session])

  useEffect(() => {
    if (!session) return
    let active = true
    let source: EventSource | null = null
    let runRefreshTimer: number | undefined
    let runRefreshInFlight = false
    const sessionId = session.session_id
    const key = `ac.events.${session.session_id}`
    let cursor = ''
    sequence.current = 0; eventHistory.current = []
    try { const saved = JSON.parse(sessionStorage.getItem(key) ?? 'null') as { cursor: string; sequence: number; events: DomainEvent[] } | null; if (saved && typeof saved.cursor === 'string' && Number.isSafeInteger(saved.sequence) && Array.isArray(saved.events) && saved.events.every(isDomainEvent)) { cursor = saved.cursor; sequence.current = saved.sequence; eventHistory.current = saved.events.slice(-200); setEvents(eventHistory.current); setCachedIds(new Set(eventHistory.current.map(event => event.event_id))) } } catch { /* A bad saved cursor is not an authority. */ }
    function remember(nextCursor: string) { if (!nextCursor) return; cursor = nextCursor; try { const metadata = eventHistory.current.map(event => ({ ...event, payload: null })); sessionStorage.setItem(key, JSON.stringify({ cursor, sequence: sequence.current, events: metadata })) } catch { /* Continue without persistence. */ } }
    function receive(items: DomainEvent[]) {
      if (!Array.isArray(items) || !items.every(isDomainEvent)) throw new Error('Event không đúng contract. Cần tải lại luồng để đối chiếu.')
      const newItems = items.filter(event => event.stream_seq > sequence.current).sort((a, b) => a.stream_seq - b.stream_seq)
      if (newItems.length) { sequence.current = newItems[newItems.length - 1].stream_seq; const seen = new Set(eventHistory.current.map(event => event.event_id)); const metadata = newItems.filter(event => !seen.has(event.event_id)).map(event => ({ event_id: event.event_id, stream_seq: event.stream_seq, event_type: event.event_type, occurred_at: event.occurred_at, recorded_at: event.recorded_at, run_id: event.run_id, task_id: event.task_id ?? null, agent_id: event.agent_id ?? null, source: event.source, payload: event.payload ?? null, sensitivity: event.sensitivity, content_withheld: event.content_withheld })); eventHistory.current = [...eventHistory.current, ...metadata].slice(-200); setEvents(eventHistory.current) }
    }
    function beat(serverTime?: string) { lastBeat.current = Date.now(); setLastSeen(serverTime ?? new Date().toISOString()); setConnection('live') }
    function refreshCommittedRun() {
      if (runRefreshTimer !== undefined || runRefreshInFlight) return
      runRefreshTimer = window.setTimeout(() => {
        runRefreshTimer = undefined
        if (!active) return
        runRefreshInFlight = true
        void request<RuntimeStatus>('runtime/status').then(state => { if (active && currentSession.current?.session_id === sessionId) { setRuntime(state); setRuns(state.runs); setRunReadFailed(false) } }).catch(() => { if (active) setRunReadFailed(true) }).finally(() => { runRefreshInFlight = false })
      }, 500)
    }
    async function connect() {
      setConnection('connecting')
      try {
        const batch = await request<EventBatch>(`events${cursor ? `?cursor=${encodeURIComponent(cursor)}` : ''}`)
        if (!active) return
        if (!Number.isSafeInteger(batch.latest_seq) || sequence.current > batch.latest_seq) throw new ApiError(409, 'Sequence cache không khớp event store. Tải lại từ dữ liệu đã lưu để đối chiếu.')
        receive(batch.events); remember(batch.cursor); beat(batch.server_time)
        source = new EventSource(`/api/v1/events/stream${cursor ? `?cursor=${encodeURIComponent(cursor)}` : ''}`, { withCredentials: true }); stream.current = source
        source.addEventListener('domain', raw => { if (!active) return; try { const event = raw as MessageEvent; const data = JSON.parse(event.data) as DomainEvent; receive([data]); remember(event.lastEventId); beat(); if (data.run_id) refreshCommittedRun() } catch { setConnection('gap'); source?.close(); setError('Event không hợp lệ. Cần tải lại luồng để đối chiếu dữ liệu đã lưu.') } })
        source.addEventListener('heartbeat', raw => { try { const data = JSON.parse((raw as MessageEvent).data) as { cursor: string; server_time: string }; remember(data.cursor); beat(data.server_time) } catch { setConnection('stale') } })
        source.addEventListener('gap', () => { source?.close(); setConnection('gap'); setError('Cursor hết hạn hoặc luồng có khoảng trống. Bấm tải lại từ dữ liệu đã lưu.') })
        source.addEventListener('auth-expired', () => { source?.close(); discardSession(); setError('Session Chủ tịch đã hết hạn. Đăng nhập lại để phục hồi kết nối.') })
        source.onerror = () => { if (active) setConnection(navigator.onLine ? 'reconnecting' : 'offline') }
      } catch (reason) { if (active) { setConnection(reason instanceof ApiError && [400, 409, 410, 422].includes(reason.status) ? 'gap' : 'offline'); setError((reason as Error).message) } }
    }
    void connect()
    const stale = window.setInterval(() => { if (active && lastBeat.current && Date.now() - lastBeat.current > 30000) setConnection(previous => previous === 'live' ? 'stale' : previous) }, 5000)
    return () => { active = false; source?.close(); if (stream.current === source) stream.current = null; window.clearInterval(stale); if (runRefreshTimer !== undefined) window.clearTimeout(runRefreshTimer) }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [session, reload])

  async function action(work: () => Promise<void>) { if (busy) return; setBusy(true); setError(''); setNotice(''); try { await work() } catch (reason) { setError((reason as Error).message) } finally { setBusy(false) } }
  function login(event: FormEvent) { event.preventDefault(); void action(async () => {
    const metadata = await request<{ available: boolean; environment?: { id: string }; company?: { id: string } }>('demo/dashboard')
    if (!metadata.available || !metadata.environment?.id || !metadata.company?.id) throw new Error('Chưa có scope demo hợp lệ. Bootstrap demo trước khi đăng nhập.')
    try { const value = await request<OwnerSession>('owner/login', { secret, environment_id: metadata.environment.id, company_id: metadata.company.id }); setSession(value); setNotice('Đã xác thực Chủ tịch trong scope demo do backend cấp.') } finally { setSecret('') }
  }) }
  function saveProfile(event: FormEvent) { event.preventDefault(); void action(async () => { if (!profile) return; const saved = await request<Profile>('owner/profile', { model: model.trim(), reasoning_effort: effort, fallback_models: fallback.split(',').map(value => value.trim()).filter(Boolean), expected_version: profile.version }, 'PUT'); setProfile(saved); setNotice(`Đã lưu model profile phiên bản ${saved.version}. Lưu cấu hình không gọi model.`) }) }
  const eligibleGrants = grants.filter(grant => !grant.revoked && new Date(grant.expires_at).getTime() > Date.now() && grant.used_requests < grant.max_requests && ['06', '07'].includes(grant.phase))
  const grant = eligibleGrants.find(value => value.id === grantId)
  function submitRun(event: FormEvent) { event.preventDefault(); void action(async () => { if (!grant || !runtime?.cg01.allowed) throw new Error('Cần grant hợp lệ và CG01 cho phép trước khi gửi run.'); const run = await request<Run>('runtime/runs', { grant_id: grant.id, phase: grant.phase, batch_id: grant.batch_id, purpose: grant.purpose, model: grant.model, effort: grant.effort, input_text: input, idempotency_key: crypto.randomUUID() }); setRuns(previous => [run, ...previous.filter(value => value.id !== run.id)]); setNotice('Đã ghi run. Theo dõi kết quả đã lưu; không gửi lại khi chưa rõ kết quả.') }) }
  async function refreshRun(id: string) { const run = await request<Run>(`runtime/runs/${encodeURIComponent(id)}`); setRuns(previous => previous.map(value => value.id === id ? run : value)) }
  function resetStream() { if (session) { try { sessionStorage.removeItem(`ac.events.${session.session_id}`) } catch { /* Storage is optional. */ } } sequence.current = 0; setEvents([]); setCachedIds(new Set()); setError(''); setReload(value => value + 1) }
  function workerStatus(run: Run) {
    if (!['waiting_model', 'running'].includes(run.status)) return 'Không có worker đang chờ model cho trạng thái này'
    if (runReadFailed) return 'Không đối chiếu được worker · dữ liệu có thể đã cũ'
    const timestamp = run.worker_heartbeat_at ? new Date(run.worker_heartbeat_at).getTime() : NaN
    if (!Number.isFinite(timestamp)) return 'Worker: chưa có heartbeat đã lưu'
    if (run.lease_until && new Date(run.lease_until).getTime() < clockNow) return 'Worker: lease đã hết hạn · cần đối chiếu kết quả'
    return clockNow - timestamp <= 30000 ? 'Worker: heartbeat đã lưu trong 30 giây gần đây' : 'Worker: mất heartbeat / dữ liệu đã cũ'
  }

  return <section className={`runtime-panel${view !== 'runtime' ? ' observatory-panel' : ''}`} aria-labelledby="runtime-title">
    <header className="runtime-heading"><div><p className="eyebrow">{view === 'runtime' ? 'THỰC THI VÀ KẾT NỐI · PHASE 06–07' : 'LIVE OFFICE · INSPECTOR · REPLAY · PHASE 08'}</p><h2 id="runtime-title">{view === 'runtime' ? 'Runtime demo có kiểm soát' : view === 'office' ? 'Hoạt động đã ghi nhận' : view === 'inspector' ? 'Inspector lượt chạy' : 'Phát lại sự kiện đã lưu'}</h2><p>{view === 'runtime' ? 'Đăng nhập Chủ tịch để đọc event và quản lý run trong scope được backend cấp. Mở trang không gọi model.' : 'Đăng nhập Chủ tịch để đọc dữ liệu đã lưu trong scope được backend cấp. Các màn hình này không gọi model hoặc thay đổi trạng thái.'}</p></div>{session && <button className="quiet-button" type="button" disabled={busy} onClick={() => void action(async () => { await request('owner/logout', {}); discardSession(); setNotice('Đã đăng xuất và đóng luồng event.') })}>Đăng xuất</button>}</header>
    {error && <p className="runtime-error" role="alert">{error}</p>}{notice && <p className="runtime-notice" role="status">{notice}</p>}
    {!checked ? <p role="status">Đang xác minh session…</p> : !session ? <form className="runtime-login" onSubmit={login}><label htmlFor="owner-secret">Secret Chủ tịch local</label><input id="owner-secret" type="password" autoComplete="off" value={secret} onChange={event => setSecret(event.target.value)} required maxLength={128} /><p>Nhập secret được bootstrap riêng trên máy. Secret không được lưu trong trình duyệt; đăng nhập không cấp inference grant.</p><button className="primary-button" disabled={busy || !secret}>{busy ? 'Đang xác thực…' : 'Đăng nhập Chủ tịch'}</button></form> : <>
      <p className="runtime-scope">Chủ tịch đã xác thực · Demo scope <code>{session.scope.company_id.slice(0, 8)}</code> · Session có thể hết hạn hoặc bị thu hồi.</p>
      {view !== 'runtime' ? <Observatory view={view} runs={runs} events={events} cachedIds={cachedIds} connection={connection} lastSeen={lastSeen} departments={departments} onReload={resetStream} /> : <>
      <div className="runtime-columns"><form className="runtime-form" onSubmit={saveProfile}><h3>Model profile</h3><p>Backend kiểm tra quyền Owner. Catalog và profile chưa xác nhận entitlement.</p><label htmlFor="runtime-model">Model ID</label><input id="runtime-model" value={model} onChange={event => setModel(event.target.value)} required maxLength={120} /><label htmlFor="runtime-effort">Reasoning effort</label><select id="runtime-effort" value={effort} onChange={event => setEffort(event.target.value)}>{['minimal', 'low', 'medium', 'high', 'xhigh'].map(value => <option key={value}>{value}</option>)}</select><label htmlFor="runtime-fallback">Fallback được phép (phân cách bằng dấu phẩy)</label><input id="runtime-fallback" value={fallback} onChange={event => setFallback(event.target.value)} maxLength={600} /><small>Danh sách này chỉ là cấu hình. Runtime không tự retry hoặc đổi model khi kết quả chưa rõ.</small><button className="quiet-button" disabled={busy || !profile}>{busy ? 'Đang xử lý…' : `Lưu profile · v${profile?.version ?? '—'}`}</button></form>
      <form className="runtime-form" onSubmit={submitRun}><h3>Một run phân tích văn bản</h3><p className="runtime-gate">CG01: {runtime?.cg01.allowed ? 'Đã cho phép theo bằng chứng' : 'Đang khóa'} · {runtime?.cg01.reason ?? 'Chưa lấy được trạng thái gate'}</p><label htmlFor="runtime-grant">Grant riêng cho đợt test</label><select id="runtime-grant" value={grantId} onChange={event => setGrantId(event.target.value)} required><option value="">{eligibleGrants.length ? 'Chọn grant đã được cấp' : 'Chưa có grant hợp lệ'}</option>{eligibleGrants.map(value => <option key={value.id} value={value.id}>Phase {value.phase} · {value.batch_id} · {value.used_requests}/{value.max_requests} lượt</option>)}</select>{grant && <p className="runtime-grant-detail">Mục đích: {grant.purpose} · Model: {grant.model} / {grant.effort} · Hết hạn: {time(grant.expires_at)}</p>}<label htmlFor="runtime-input">Văn bản tin cậy trong scope demo</label><textarea id="runtime-input" rows={5} value={input} onChange={event => setInput(event.target.value)} required maxLength={16000} /><small>Text-only, một turn, tools tắt. Usage/chi phí thiếu nguồn sẽ hiển thị chưa biết. Không tạo grant tự động.</small><button className="primary-button" disabled={busy || !grant || !runtime?.cg01.allowed || !input.trim()}>Gửi một run được cấp quyền</button></form></div>
      <section className="runtime-runs" aria-labelledby="runtime-runs-title"><div className="runtime-subheading"><h3 id="runtime-runs-title">Run đã lưu</h3><button className="quiet-button" type="button" disabled={busy} onClick={() => setReload(value => value + 1)}>Tải trạng thái</button></div>{!runs.length ? <p>Chưa có run trong scope này.</p> : runs.map(run => <article className="runtime-run" key={run.id}><div><strong>{runLabel[run.status] ?? run.status}</strong><code>{run.id}</code><p>{run.model} · {run.effort} · {time(run.created_at)}</p><p>{workerStatus(run)} · Cập nhật worker: {time(run.worker_heartbeat_at ?? null)}</p><small>Trạng thái đã lưu không chứng minh agent còn hoạt động. Heartbeat event store độc lập với worker.</small><p>Usage: {display(run.usage)} · Outcome: {display(run.outcome)}</p>{run.stop_requested && <p>Đã yêu cầu dừng. Request đang bay có thể còn xử lý; kết quả phải được đối chiếu.</p>}{run.output !== undefined && run.output !== null && <details><summary>Kết quả đã lưu</summary><pre>{display(run.output)}</pre></details>}</div><div className="runtime-run-actions"><button className="quiet-button" type="button" disabled={busy} onClick={() => void action(() => refreshRun(run.id))}>Đối chiếu</button>{['queued', 'waiting', 'waiting_model', 'running', 'dispatching', 'pending'].includes(run.status) && <button className="quiet-button" type="button" disabled={busy || run.stop_requested} onClick={() => void action(async () => { const updated = await request<Run>(`runtime/runs/${encodeURIComponent(run.id)}/stop`, {}); setRuns(previous => previous.map(value => value.id === run.id ? updated : value)); setNotice('Đã ghi yêu cầu dừng; không giả định gateway đã hủy request.') })}>Yêu cầu dừng</button>}</div></article>)}</section>
      <section className="runtime-events" aria-labelledby="runtime-events-title"><div className="runtime-subheading"><div><h3 id="runtime-events-title">Luồng event đã commit</h3><p role="status">Kết nối event store: {connectionLabel[connection]} · Cập nhật kết nối: {time(lastSeen)}</p></div><button className="quiet-button" type="button" onClick={resetStream}>Tải lại từ dữ liệu đã lưu</button></div><p>Chỉ phản ánh event của ứng dụng. Trạng thái waiting không thể hiện tiến độ hay token nội bộ của model. Hiển thị tối đa 200 event gần đây; đây chưa phải giao diện replay.</p>{!events.length ? <p>Chưa nhận event kể từ cursor của session này.</p> : <ol>{events.map(event => <li key={event.event_id}><strong>#{event.stream_seq} · {event.event_type}</strong><span>{time(event.recorded_at)} · {event.source} {event.run_id ? `· run ${event.run_id.slice(0, 8)}` : ''}</span><code>{event.event_id}</code>{cachedIds.has(event.event_id) && <small>Metadata cache local · chưa đối chiếu nội dung với server; tải lại để xác minh.</small>}</li>)}</ol>}</section>
      </>}
    </>}
  </section>
}


const summaryPayloadKeys = ['status', 'outcome', 'error_code', 'reason_code', 'model', 'reasoning_effort', 'attempt', 'retry_count', 'usage_status', 'measurement', 'usage_available', 'input_tokens', 'output_tokens', 'cached_tokens', 'reasoning_tokens', 'total_tokens', 'cost_basis', 'usage_provenance', 'execution_outcome_unchanged']
function eventSummary(event: DomainEvent) {
  if (event.content_withheld || event.sensitivity === 'confidential') return 'Nội dung bị ẩn theo policy.'
  if (!event.payload || typeof event.payload !== 'object' || Array.isArray(event.payload)) return 'Event không có payload tóm tắt được phép hiển thị.'
  const payload = event.payload as Record<string, unknown>
  const entries = summaryPayloadKeys.filter(key => Object.hasOwn(payload, key) && (payload[key] === null || ['string', 'number', 'boolean'].includes(typeof payload[key])))
  return entries.length ? entries.map(key => `${key}: ${String(payload[key] ?? 'chưa biết')}`).join(' · ') : 'Chưa có trường tóm tắt được phép hiển thị.'
}
function Observatory({ view, runs, events, cachedIds, connection, lastSeen, departments, onReload }: { view: ObservationView; runs: Run[]; events: DomainEvent[]; cachedIds: Set<string>; connection: Connection; lastSeen: string | null; departments: string[]; onReload: () => void }) {
  const [runId, setRunId] = useState('all')
  const [position, setPosition] = useState(0)
  const selectedRunId = view === 'inspector' && runId === 'all' ? events.at(-1)?.run_id ?? runs[0]?.id ?? 'all' : runId
  const scopedEvents = events.filter(event => selectedRunId === 'all' || event.run_id === selectedRunId)
  const selectedRun = runs.find(run => run.id === selectedRunId) ?? null
  const currentEvent = scopedEvents[Math.min(position, Math.max(scopedEvents.length - 1, 0))] ?? null
  const statusGroups = [
    { key: 'running', title: 'Đang xử lý' }, { key: 'waiting', title: 'Đang chờ' },
    { key: 'failed', title: 'Thất bại' }, { key: 'unknown', title: 'Chưa biết kết quả' },
  ]
  return <div className="observatory-content">
    <div className="observatory-status"><span className={`live-indicator${connection === 'offline' || connection === 'gap' || connection === 'stale' ? ' offline' : ''}`}><span />{connectionLabel[connection]}</span><span>Cập nhật kết nối: {time(lastSeen)}</span><span>Scope: Chủ tịch đã xác thực</span></div>
    {view === 'office' && <>
      <div className="office-grid" aria-label="Trạng thái các lượt chạy đã lưu">{statusGroups.map(group => {
        const matching = runs.filter(run => group.key === 'unknown' ? ['unknown', 'outcome_unknown', 'interrupted'].includes(run.status) : group.key === 'waiting' ? ['queued', 'waiting', 'waiting_model'].includes(run.status) : run.status === group.key)
        return <section className="office-lane" key={group.key}><h3>{group.title}<span>{matching.length}</span></h3>{matching.length ? matching.map(run => <article className="office-run" key={run.id}><strong>{run.model || 'Model chưa biết'}</strong><small>{runLabel[run.status] ?? 'Trạng thái chưa biết'}</small><code>{run.id.slice(0, 8)}</code><small>{time(run.created_at)}</small></article>) : <p>Chưa có lượt chạy</p>}</section>
      })}</div>
      <p className="observatory-note">Trạng thái lấy từ run đã lưu. Chưa có quan hệ run → nhân viên/phòng ban trong nguồn Phase 06–07 nên không gán hoạt động cho một agent. Heartbeat kết nối phía trên không phải heartbeat của worker. <a href="#inspector">Mở Inspector</a></p>
      <section className="office-departments"><div className="runtime-subheading"><h3>Cơ cấu phòng ban · demo fixture</h3><span className="fixture-badge">FIXTURE</span></div>{departments.length ? <div className="office-department-grid">{departments.map(name => <article key={name}><span className="office-room-icon" aria-hidden="true">⌂</span><strong>{name}</strong><small>Không có trạng thái agent được suy diễn từ fixture.</small></article>)}</div> : <p>Chưa có dữ liệu phòng ban.</p>}</section>
    </>}
    {view === 'inspector' && <>
      <div className="observatory-controls"><label htmlFor="inspector-run">Lượt chạy đã lưu</label><select id="inspector-run" value={runId} onChange={event => setRunId(event.target.value)}><option value="all">Run có event mới nhất</option>{runs.map(run => <option key={run.id} value={run.id}>{run.id.slice(0, 8)} · {runLabel[run.status] ?? run.status}</option>)}</select><button className="quiet-button" type="button" onClick={onReload}>Đọc lại từ event store</button></div>
      {selectedRun ? <><section className="inspector-summary"><div><span>Trạng thái</span><strong>{runLabel[selectedRun.status] ?? 'Chưa biết'}</strong></div><div><span>Model · effort</span><strong>{selectedRun.model || 'Chưa biết'} · {selectedRun.effort || 'Chưa biết'}</strong></div><div><span>Usage</span><strong>{display(selectedRun.usage)}</strong></div><div><span>Outcome</span><strong>{display(selectedRun.outcome)}</strong></div><code>{selectedRun.id}</code><small>Task: {selectedRun.task_id ?? 'Chưa liên kết'} · Tạo lúc {time(selectedRun.created_at)}</small></section><div className="inspector-sections"><section><h3>Plan và tóm tắt quyết định</h3><p>Chưa có summary tường minh trong event projection hiện tại.</p></section><section><h3>Tools, file diff và messages</h3><p>Chưa có nguồn Phase 08 được phép hiển thị cho lượt này.</p></section><section><h3>Lỗi, profile và metrics</h3><p>Profile snapshot chi tiết không được API projection cung cấp. Metrics/usage: {display(selectedRun.usage)}.</p></section></div><section className="inspector-events"><h3>Sự kiện liên quan · {scopedEvents.length}</h3>{scopedEvents.length ? <ol>{scopedEvents.map(event => <li key={event.event_id}><div><strong>#{event.stream_seq} · {event.event_type}</strong><small>{time(event.recorded_at)} · {event.source}</small><p>{eventSummary(event)}</p></div><code>{event.event_id}</code></li>)}</ol> : <p>Chưa có event đã tải cho lượt này.</p>}</section></> : <p>Chọn một lượt chạy hoặc cần tải event đã lưu trước khi có lượt chạy phù hợp.</p>}
    </>}
    {view === 'replay' && <>
      <div className="observatory-controls"><label htmlFor="replay-run">Lọc theo lượt chạy</label><select id="replay-run" value={runId} onChange={event => { setRunId(event.target.value); setPosition(0) }}><option value="all">Tất cả event trong cửa sổ đã tải</option>{runs.map(run => <option key={run.id} value={run.id}>{run.id.slice(0, 8)} · {runLabel[run.status] ?? run.status}</option>)}</select><button className="quiet-button" type="button" onClick={onReload}>Tải lại từ đầu</button></div>
      <p className="observatory-note">Replay chỉ đọc dữ liệu đã commit. Đang hiển thị tối đa 200 event trong cửa sổ hiện tại; khoảng trống cần tải lại, không được nội suy.</p>
      {scopedEvents.length ? <><label className="replay-range-label" htmlFor="replay-position">Mốc {Math.min(position + 1, scopedEvents.length)} / {scopedEvents.length}</label><input id="replay-position" className="replay-range" type="range" min={0} max={Math.max(0, scopedEvents.length - 1)} value={Math.min(position, scopedEvents.length - 1)} onChange={event => setPosition(Number(event.target.value))} aria-valuetext={currentEvent ? `Event ${currentEvent.stream_seq}: ${currentEvent.event_type}` : 'Không có event'} /><ol className="replay-timeline">{scopedEvents.map((event, index) => <li className={index === Math.min(position, scopedEvents.length - 1) ? 'selected' : ''} key={event.event_id}><button type="button" onClick={() => setPosition(index)} aria-current={index === position ? 'step' : undefined}><span>#{event.stream_seq}</span><strong>{event.event_type}</strong><small>{time(event.recorded_at)}</small><p>{eventSummary(event)}</p></button></li>)}</ol></> : <section className="observatory-empty"><h3>Chưa có event phù hợp</h3><p>Đăng nhập Chủ tịch để tải event store; không có timeline nào được tạo từ fixture.</p></section>}
    </>}
    {cachedIds.size > 0 && <p className="observatory-note">Có metadata cũ từ cache session; nội dung chi tiết chỉ được đưa vào sau khi đối chiếu với event store.</p>}
  </div>
}
