import { useEffect, useRef, useState } from 'react'
import type { FormEvent } from 'react'
import './RuntimePanel.css'

type OwnerSession = { authenticated: true; owner_id: string; session_id: string; scope: { environment_id: string; company_id: string }; csrf_token: string }
type Profile = { version: number; model: string | null; reasoning_effort: string | null; fallback_models: string[] }
type Grant = { id: string; phase: string; batch_id: string; purpose: string; model: string; effort: string; max_requests: number; used_requests: number; max_concurrency: number; expires_at: string; revoked: boolean }
type EmployeeOption = { employee_id: string; employee_version_id: string; lifecycle: string; version: number; display_name: string; role: string; department: string | null }
type Run = { id: string; task_id: string; status: string; task_status: string; task_goal: string; model: string; effort: string; stop_requested: boolean; outcome: unknown; usage: unknown; usage_provenance?: string; cost_basis?: string; output?: unknown; created_at: string; worker_heartbeat_at?: string | null; lease_until?: string | null; employee: { id: string; version_id: string; version: number; name: string; role: string } | null; synthetic_test_data?: boolean }
type RuntimeStatus = { cg01: { allowed: boolean; reason: string; mode?: 'strict' | 'demo-test'; verified?: boolean }; inference_grants: number; runs: Run[] }
type ReconciliationView = { run: { id: string; status: string; outcome: string | null; created_at: string; stop_requested: boolean; employee: { name: string | null; version: number | null } }; classification: string; request_span_id: string | null; gateway_call_id: string | null; calls: { id: string; attempt: number; status: string; reason: string | null; dispatched_at: string; heartbeat_at: string; lease_until: string; finished_at: string | null; usage: unknown; usage_provenance: string }[]; checkpoints: { sequence: number; boundary: string; created_at: string; status: string | null; request_span_id: string | null; attempt: number | null; replay_allowed: boolean | null }[]; grant: Record<string, unknown>; usage: unknown; usage_status: string; cost_status: string; lease: { heartbeat_at: string | null; lease_until: string | null; status: string }; dispatch_guard: { held: boolean; request_span_id: string | null; held_for_this_call: boolean }; evidence: { event_id: string; event_type: string; occurred_at: string; recorded_at: string; dedup_key: string }[]; decisions: { id: string; decision: string; reason: string; owner_id: string; created_at: string }[]; available_actions: string[] }
type WorkOrder = { task_id: string; created_at: string; status: string; revision: number; transition_version: number; goal: string; expected_outputs: string[]; acceptance_criteria: ({ id: string; description: string; evidence_kind: string } | string)[]; scope: { input_refs?: string[]; tool_capabilities?: string[] }; deadline_at: string | null; budget_limits: Record<string, unknown>; stop_conditions: Record<string, unknown>; assignee_id: string | null; reviewer_id: string | null; autonomy: string; priority: number | null; queue_status: string | null; ready_at: string | null; run_count: number }
type Assignee = { id: string; lifecycle: string; display_name: string | null; role: string | null; department: string | null }
type WorkBoardData = { tasks: WorkOrder[]; assignees: Assignee[] }
type ApprovalRecord = { id: string; task_id: string; run_id: string | null; task_revision: number | null; task_goal: string; action_type: string; action_payload: Record<string, unknown>; payload_hash: string; summary: string; status: string; policy_id: string | null; policy_version: number | null; policy_snapshot_version: number | null; budget_snapshot: Record<string, unknown>; expires_at: string | null; decided_at: string | null; decision_reason: string | null; decision_hash: string | null; created_at: string; dispatch_status?: string }
type ApprovalInboxData = { approvals: ApprovalRecord[] }
type DomainEvent = { event_id: string; stream_seq: number; event_type: string; occurred_at: string; recorded_at: string; run_id: string | null; task_id?: string | null; agent_id?: string | null; employee_version_id?: string | null; source: string; payload: unknown; sensitivity?: string; content_withheld?: boolean }
type EventBatch = { events: DomainEvent[]; cursor: string; latest_seq: number; server_time: string }
type EventSnapshot = { version: 1; events: DomainEvent[]; runs: Run[]; watermark_seq: number; first_retained_seq: number | null; replay_window_start_seq: number | null; history_gap: boolean; cursor: string; server_time: string }
type Connection = 'connecting' | 'recovering' | 'live' | 'reconnecting' | 'stale' | 'gap' | 'offline'
const connectionLabel: Record<Connection, string> = { connecting: 'Đang kết nối', recovering: 'Đang khôi phục dữ liệu', live: 'Đã kết nối', reconnecting: 'Đang kết nối lại', stale: 'Dữ liệu đã cũ', gap: 'Có khoảng trống dữ liệu', offline: 'Mất kết nối' }
type ReadState = 'loading' | 'available' | 'unavailable'
const activeRunStatuses = new Set(['queued', 'waiting', 'waiting_model', 'dispatching', 'running', 'pending'])
const unknownRunStatuses = new Set(['unknown', 'outcome_unknown', 'interrupted'])
const lifecycleLabel: Record<string, string> = { active: 'Đang công tác', probation: 'Thử việc', offboarded: 'Đã nghỉ', suspended: 'Tạm ngưng' }
type TaskActionName = 'enqueue' | 'pause' | 'resume' | 'cancel' | 'accept' | 'request_rework'
const taskLabel: Record<string, string> = { draft:'Bản nháp',queued:'Trong hàng đợi',planning:'Đang lập kế hoạch',awaiting_approval:'Chờ phê duyệt',executing:'Đang thực hiện',reviewing:'Đang rà soát',rework:'Cần làm lại',awaiting_acceptance:'Chờ Chủ tịch nghiệm thu',accepted:'Đã nghiệm thu',blocked:'Bị chặn',paused:'Đã tạm dừng',failed:'Thất bại',cancelled:'Đã hủy' }
const runLabel: Record<string, string> = { queued: 'Đang chờ', waiting: 'Đang chờ model', waiting_model: 'Đang chờ model', running: 'Đang xử lý', completed: 'Hoàn tất', succeeded: 'Hoàn tất', failed: 'Thất bại', aborted: 'Đã dừng', stopped: 'Đã dừng', cancelled: 'Đã dừng trước dispatch', interrupted: 'Bị gián đoạn · kết quả chưa được xác nhận', unknown: 'Chưa biết kết quả', outcome_unknown: 'Chưa biết kết quả' }
class ApiError extends Error { status: number; constructor(status: number, message: string) { super(message); this.status = status } }
function isDomainEvent(value: unknown): value is DomainEvent {
  if (!value || typeof value !== 'object') return false
  const event = value as Partial<DomainEvent>
  return typeof event.event_id === 'string' && Number.isSafeInteger(event.stream_seq) && Number(event.stream_seq) > 0 && typeof event.event_type === 'string' && typeof event.recorded_at === 'string' && typeof event.source === 'string'
}

function display(value: unknown) { return typeof value === 'string' ? value : value === null || value === undefined ? 'Chưa biết' : JSON.stringify(value) }
function time(value: string | null) { return value ? new Date(value).toLocaleString('vi-VN') : 'Chưa có cập nhật' }
function officeEmployeeFromHash() {
  const query = new URLSearchParams(window.location.hash.split('?')[1] ?? '')
  const employeeId = query.get('employee_id')
  const employeeVersionId = query.get('employee_version_id')
  return employeeId && employeeVersionId ? { employeeId, employeeVersionId } : null
}
function runtimeEmployeeHref(employee: EmployeeOption) {
  return `#settings?employee_id=${encodeURIComponent(employee.employee_id)}&employee_version_id=${encodeURIComponent(employee.employee_version_id)}`
}
function runtimeReconciliationHref(employee: EmployeeOption, run: Run) {
  return `${runtimeEmployeeHref(employee)}&run_id=${encodeURIComponent(run.id)}`
}

type ObservationView = 'office' | 'inspector' | 'replay' | 'work' | 'approvals'

export default function RuntimePanel({ view = 'runtime' }: { view?: 'runtime' | ObservationView }) {
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
  const [employees, setEmployees] = useState<EmployeeOption[]>([])
  const [employeeReadState, setEmployeeReadState] = useState<ReadState>('loading')
  const [employeeId, setEmployeeId] = useState('')
  const [employeeVersionId, setEmployeeVersionId] = useState('')
  const [employeeLinkError, setEmployeeLinkError] = useState('')
  const [input, setInput] = useState('')
  const [runs, setRuns] = useState<Run[]>([])
  const [reconciliation, setReconciliation] = useState<Record<string, ReconciliationView>>({})
  const [reconciliationReason, setReconciliationReason] = useState<Record<string, string>>({})
  const [workOrders, setWorkOrders] = useState<WorkOrder[]>([])
  const [assignees, setAssignees] = useState<Assignee[]>([])
  const [approvals, setApprovals] = useState<ApprovalRecord[]>([])
  const [events, setEvents] = useState<DomainEvent[]>([])
  const [historyGap, setHistoryGap] = useState(false)
  const [replayWindowStart, setReplayWindowStart] = useState<number | null>(null)
  const [connection, setConnection] = useState<Connection>('offline')
  const [lastSeen, setLastSeen] = useState<string | null>(null)
  const [clockNow, setClockNow] = useState(Date.now)
  const [runReadFailed, setRunReadFailed] = useState(false)
  const [runtimeReadState, setRuntimeReadState] = useState<ReadState>('loading')
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
  const createKey = useRef<{ key: string; payload: Record<string, unknown> } | null>(null)
  const runCreateKey = useRef<{ key: string; payload: Record<string, unknown> } | null>(null)
  const actionKeys = useRef(new Map<string, string>())
  const currentSession = useRef<OwnerSession | null>(null)
  const deepLinkedEmployee = useRef(officeEmployeeFromHash())
  const autoOpenedReconciliations = useRef(new Set<string>())
  currentSession.current = session
  currentRuns.current = runs

  function discardSession() {
    stream.current?.close()
    stream.current = null
    const previous = currentSession.current
    if (previous) { try { sessionStorage.removeItem(`ac.events.${previous.session_id}`) } catch { /* Storage is optional. */ } }
    setSession(null); setProfile(null); setRuntime(null); setGrants([]); setEmployees([]); setEmployeeReadState('loading'); setRuntimeReadState('loading'); setEmployeeId(''); setEmployeeVersionId(''); setRuns([]); setRunReadFailed(false); setReconciliation({}); setReconciliationReason({}); setWorkOrders([]); setAssignees([]); setApprovals([]); setEvents([]); setCachedIds(new Set()); eventHistory.current = []; setHistoryGap(false); setReplayWindowStart(null); setLastSeen(null); sequence.current = 0; setConnection('offline')
  }

  async function request<T>(path: string, body?: unknown, method = 'POST', idempotencyKey?: string): Promise<T> {
    const sentSessionId = currentSession.current?.session_id
    let response: Response
    try { response = await fetch(`/api/v1/${path}`, { credentials: 'same-origin', cache: 'no-store', signal: AbortSignal.timeout(10000), ...(body === undefined ? {} : { method, headers: { 'Content-Type': 'application/json', ...(currentSession.current ? { 'X-CSRF-Token': currentSession.current.csrf_token } : {}), ...(idempotencyKey ? { 'Idempotency-Key': idempotencyKey } : {}) }, body: JSON.stringify(body) }) }) }
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
    setEmployeeReadState('loading'); setRuntimeReadState('loading')
    async function load() {
      try {
        const [saved, state, available, board, staff] = await Promise.all([request<Profile>('owner/profile'), request<RuntimeStatus>('runtime/status'), request<Grant[] | { grants: Grant[] }>('runtime/grants'), request<WorkBoardData>('work-orders'), request<{ employees: EmployeeOption[] }>('runtime/employees', undefined, 'GET')])
        if (!active) return
        setProfile(saved); setModel(saved.model ?? ''); setEffort(saved.reasoning_effort ?? 'medium'); setFallback(saved.fallback_models.join(', ')); setRuntime(state); setRuns(state.runs); setRunReadFailed(false); setRuntimeReadState('available'); setEmployeeReadState('available')
        setGrants(Array.isArray(available) ? available : available.grants); setWorkOrders(board.tasks); setAssignees(board.assignees)
        setEmployees(staff.employees)
        const requested = deepLinkedEmployee.current
        const linkedChoice = requested && staff.employees.find(item => item.employee_id === requested.employeeId && item.employee_version_id === requested.employeeVersionId)
        const chosen = requested
          ? linkedChoice
          : staff.employees.find(item => item.employee_id === employeeId) ?? staff.employees[0]
        setEmployeeLinkError(requested && !linkedChoice
          ? 'EmployeeVersion trong liên kết đã thay đổi hoặc không còn trong scope hiện tại. Đã giữ trống lựa chọn để tránh chạy nhầm phiên bản; hãy chọn lại EmployeeVersion đang hiển thị.'
          : '')
        deepLinkedEmployee.current = null
        setEmployeeId(chosen?.employee_id ?? '')
        setEmployeeVersionId(chosen?.employee_version_id ?? '')
        if (linkedChoice) {
          const requestedRunId = new URLSearchParams(window.location.hash.split('?')[1] ?? '').get('run_id')
          window.requestAnimationFrame(() => {
            const target = requestedRunId ? document.getElementById(`runtime-run-${requestedRunId}`) : null
            ;(target ?? document.getElementById('runtime-task-form'))?.scrollIntoView({ block: 'start' })
          })
        }
      } catch (reason) { if (active) { setEmployeeReadState('unavailable'); setRuntimeReadState('unavailable'); setRunReadFailed(true); setError((reason as Error).message) } }
    }
    void load()
    return () => { active = false }
    // Read-only reload follows session or an explicit refresh, never model dispatch.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [session, reload])

  useEffect(() => {
    if (view !== 'runtime') return
    const requestedRunId = new URLSearchParams(window.location.hash.split('?')[1] ?? '').get('run_id')
    const run = requestedRunId ? runs.find(item => item.id === requestedRunId) : undefined
    if (!run || !unknownRunStatuses.has(run.status) || autoOpenedReconciliations.current.has(run.id)) return
    autoOpenedReconciliations.current.add(run.id)
    void loadReconciliation(run.id).catch(reason => setError((reason as Error).message))
    // A deep link only triggers a scoped, read-only reconciliation lookup for an actual saved unknown Run.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [view, runs])

  useEffect(() => {
    if (!session || view !== 'approvals') return
    let active = true
    void request<ApprovalInboxData>('approvals', undefined, 'GET').then(value => {
      if (active && currentSession.current?.session_id === session.session_id) setApprovals(value.approvals)
    }).catch(reason => { if (active) setError((reason as Error).message) })
    return () => { active = false }
    // The inbox refreshes only after login or an explicit action/reload.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [session, view, reload])

  useEffect(() => {
    if (!session) return
    let active = true
    let reading = false
    const timer = window.setInterval(() => {
      setClockNow(Date.now())
      if (reading || !currentRuns.current.some(run => ['waiting_model', 'running'].includes(run.status))) return
      reading = true
      void request<RuntimeStatus>('runtime/status').then(state => { if (active && currentSession.current?.session_id === session.session_id) { setRuntime(state); setRuns(state.runs); setRunReadFailed(false); setRuntimeReadState('available') } }).catch(() => { if (active) { setRunReadFailed(true); setRuntimeReadState('unavailable') } }).finally(() => { reading = false })
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
    let reconnectProbeInFlight = false
    let snapshotRecoveryInFlight = false
    let snapshotRecoveryAttempts = 0
    const sessionId = session.session_id
    const key = `ac.events.${session.session_id}`
    let cursor = ''
    sequence.current = 0; eventHistory.current = []
    try { const saved = JSON.parse(sessionStorage.getItem(key) ?? 'null') as { cursor: string; sequence: number; events: DomainEvent[] } | null; if (saved && typeof saved.cursor === 'string' && Number.isSafeInteger(saved.sequence) && Array.isArray(saved.events) && saved.events.every(isDomainEvent)) { cursor = saved.cursor; sequence.current = saved.sequence; eventHistory.current = saved.events.slice(-200); setEvents(eventHistory.current); setCachedIds(new Set(eventHistory.current.map(event => event.event_id))) } } catch { /* A bad saved cursor is not an authority. */ }
    function remember(nextCursor: string) { if (!nextCursor) return; cursor = nextCursor; try { const metadata = eventHistory.current.map(event => ({ ...event, payload: null })); sessionStorage.setItem(key, JSON.stringify({ cursor, sequence: sequence.current, events: metadata })) } catch { /* Continue without persistence. */ } }
    function receive(items: DomainEvent[]) {
      if (!Array.isArray(items) || !items.every(isDomainEvent)) throw new Error('Event không đúng contract. Cần tải lại luồng để đối chiếu.')
      const seen = new Set(eventHistory.current.map(event => event.event_id))
      for (const event of items) {
        const prior = eventHistory.current.find(value => value.event_id === event.event_id)
        if (prior && prior.stream_seq !== event.stream_seq) throw new ApiError(409, 'Cùng event ID nhận sequence khác nhau.')
      }
      const candidates = items.filter(event => !seen.has(event.event_id) && event.stream_seq > sequence.current).sort((a, b) => a.stream_seq - b.stream_seq)
      const metadata: DomainEvent[] = []
      for (const event of candidates) {
        if (event.stream_seq !== sequence.current + 1) throw new ApiError(409, 'Event bị thiếu hoặc sai thứ tự. Đang dựng lại từ snapshot đã lưu.')
        sequence.current = event.stream_seq
        seen.add(event.event_id)
        metadata.push({ event_id: event.event_id, stream_seq: event.stream_seq, event_type: event.event_type, occurred_at: event.occurred_at, recorded_at: event.recorded_at, run_id: event.run_id, task_id: event.task_id ?? null, agent_id: event.agent_id ?? null, employee_version_id: event.employee_version_id ?? null, source: event.source, payload: event.payload ?? null, sensitivity: event.sensitivity, content_withheld: event.content_withheld })
      }
      if (metadata.length) { eventHistory.current = [...eventHistory.current, ...metadata].slice(-200); setEvents(eventHistory.current) }
    }
    function beat(serverTime?: string) { lastBeat.current = Date.now(); setLastSeen(serverTime ?? new Date().toISOString()); setConnection('live') }
    function refreshCommittedRun() {
      if (runRefreshTimer !== undefined || runRefreshInFlight) return
      runRefreshTimer = window.setTimeout(() => {
        runRefreshTimer = undefined
        if (!active) return
        runRefreshInFlight = true
        void request<RuntimeStatus>('runtime/status').then(state => { if (active && currentSession.current?.session_id === sessionId) { setRuntime(state); setRuns(state.runs); setRunReadFailed(false); setRuntimeReadState('available') } }).catch(() => { if (active) { setRunReadFailed(true); setRuntimeReadState('unavailable') } }).finally(() => { runRefreshInFlight = false })
      }, 500)
    }
    function openStream(nextCursor: string) {
      source?.close()
      source = new EventSource(`/api/v1/events/stream?cursor=${encodeURIComponent(nextCursor)}`, { withCredentials: true }); stream.current = source
      source.addEventListener('domain', raw => {
        if (!active) return
        try { const event = raw as MessageEvent; const data = JSON.parse(event.data) as DomainEvent; receive([data]); snapshotRecoveryAttempts = 0; remember(event.lastEventId); beat(); if (data.run_id) refreshCommittedRun() }
        catch (reason) { void recoverSnapshot(reason instanceof Error ? reason.message : 'Event không hợp lệ.') }
      })
      source.addEventListener('heartbeat', raw => { try { const data = JSON.parse((raw as MessageEvent).data) as { cursor: string; server_time: string }; snapshotRecoveryAttempts = 0; remember(data.cursor); beat(data.server_time) } catch { setConnection('stale') } })
      source.addEventListener('gap', () => { void recoverSnapshot('Event store báo cursor có khoảng trống.') })
      source.addEventListener('auth-expired', () => { source?.close(); discardSession(); setError('Session Chủ tịch đã hết hạn. Đăng nhập lại để phục hồi kết nối.') })
      source.onerror = () => {
        if (!active) return
        setConnection(navigator.onLine ? 'reconnecting' : 'offline')
        if (!navigator.onLine || reconnectProbeInFlight) return
        reconnectProbeInFlight = true
        void request<EventBatch>(`events${cursor ? `?cursor=${encodeURIComponent(cursor)}` : ''}`).then(batch => {
          if (active && sequence.current > batch.latest_seq) throw new ApiError(409, 'Sequence cache không khớp event store.')
        }).catch(reason => {
          if (active && reason instanceof ApiError && [400, 409].includes(reason.status)) void recoverSnapshot(reason.message)
        }).finally(() => { reconnectProbeInFlight = false })
      }
    }
    async function recoverSnapshot(reason: string) {
      if (!active || snapshotRecoveryInFlight) return
      if (snapshotRecoveryAttempts >= 2) { source?.close(); setConnection('gap'); setError(`${reason} Snapshot chưa đồng bộ được; lịch sử cũ vẫn chưa xác minh. Thử tải lại sau.`); return }
      snapshotRecoveryAttempts++
      snapshotRecoveryInFlight = true
      source?.close(); setConnection('recovering'); setError('Khoảng trống dữ liệu. Đang tải snapshot có scope để khôi phục trạng thái…')
      try {
        const snapshot = await request<EventSnapshot>('events/snapshot-v1', undefined, 'GET')
        if (!active || snapshot.version !== 1 || !Number.isSafeInteger(snapshot.watermark_seq) || snapshot.watermark_seq < 0 || typeof snapshot.cursor !== 'string' || !snapshot.cursor || typeof snapshot.history_gap !== 'boolean' || !Array.isArray(snapshot.events) || !snapshot.events.every(isDomainEvent) || !Array.isArray(snapshot.runs)) throw new Error('Snapshot không đúng phiên bản hoặc định dạng.')
        let expected = snapshot.events[0]?.stream_seq ?? snapshot.watermark_seq
        const seen = new Set<string>()
        for (const event of snapshot.events) {
          if (event.stream_seq < expected || (event.stream_seq > expected && !snapshot.history_gap) || seen.has(event.event_id)) throw new Error('Snapshot có event trùng hoặc sai thứ tự.')
          seen.add(event.event_id); expected = event.stream_seq + 1
        }
        if (snapshot.events.length && snapshot.events.at(-1)?.stream_seq !== snapshot.watermark_seq) throw new Error('Snapshot chưa đạt watermark hiện tại.')
        // Replace the event window and run projection together; no historical state is guessed.
        eventHistory.current = snapshot.events.slice(-200)
        sequence.current = snapshot.watermark_seq
        setEvents(eventHistory.current); setRuns(snapshot.runs); setCachedIds(new Set()); setHistoryGap(snapshot.history_gap)
        setReplayWindowStart(snapshot.replay_window_start_seq); setRunReadFailed(false)
        remember(snapshot.cursor); setError(''); openStream(snapshot.cursor)
      } catch (failure) {
        source?.close(); setConnection('gap')
        const detail = failure instanceof ApiError && failure.status === 413
          ? 'Snapshot vượt giới hạn an toàn; Replay không thể khôi phục cửa sổ dữ liệu này.'
          : `Không khôi phục được snapshot: ${(failure as Error).message}`
        setError(detail)
      } finally { snapshotRecoveryInFlight = false }
    }
    async function connect() {
      setConnection('connecting')
      try {
        const batch = await request<EventBatch>(`events${cursor ? `?cursor=${encodeURIComponent(cursor)}` : ''}`)
        if (!active) return
        if (!Number.isSafeInteger(batch.latest_seq) || sequence.current > batch.latest_seq) throw new ApiError(409, 'Sequence cache không khớp event store. Tải lại từ dữ liệu đã lưu để đối chiếu.')
        receive(batch.events); remember(batch.cursor); beat(batch.server_time)
        openStream(batch.cursor)
      } catch (reason) {
        if (!active) return
        if (reason instanceof ApiError && [400, 409].includes(reason.status)) { await recoverSnapshot(reason.message); return }
        setConnection('offline'); setError((reason as Error).message)
      }
    }
    void connect()
    const stale = window.setInterval(() => { if (active && lastBeat.current && Date.now() - lastBeat.current > 30000) setConnection(previous => previous === 'live' ? 'stale' : previous) }, 5000)
    return () => { active = false; source?.close(); if (stream.current === source) stream.current = null; window.clearInterval(stale); if (runRefreshTimer !== undefined) window.clearTimeout(runRefreshTimer) }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [session, reload])

  async function action(work: () => Promise<void>): Promise<boolean> { if (busy) return false; setBusy(true); setError(''); setNotice(''); try { await work(); return true } catch (reason) { setError((reason as Error).message); return false } finally { setBusy(false) } }
  function login(event: FormEvent) { event.preventDefault(); void action(async () => {
    const metadata = await request<{ available: boolean; environment?: { id: string }; company?: { id: string } }>('demo/dashboard')
    if (!metadata.available || !metadata.environment?.id || !metadata.company?.id) throw new Error('Chưa có scope demo hợp lệ. Bootstrap demo trước khi đăng nhập.')
    try { const value = await request<OwnerSession>('owner/login', { secret, environment_id: metadata.environment.id, company_id: metadata.company.id }); setSession(value); setNotice('Đã xác thực Chủ tịch trong scope demo do backend cấp.') } finally { setSecret('') }
  }) }
  function saveProfile(event: FormEvent) { event.preventDefault(); void action(async () => { if (!profile) return; const saved = await request<Profile>('owner/profile', { model: model.trim(), reasoning_effort: effort, fallback_models: fallback.split(',').map(value => value.trim()).filter(Boolean), expected_version: profile.version }, 'PUT'); setProfile(saved); setNotice(`Đã lưu model profile phiên bản ${saved.version}. Lưu cấu hình không gọi model.`) }) }
  const eligibleGrants = grants.filter(grant => !grant.revoked && new Date(grant.expires_at).getTime() > Date.now() && grant.used_requests < grant.max_requests && ['06', '07'].includes(grant.phase))
  const grant = eligibleGrants.find(value => value.id === grantId)
  const selectedEmployee = employees.find(value => value.employee_id === employeeId && value.employee_version_id === employeeVersionId)
  const gateMessage = runtime?.cg01.allowed
    ? runtime.cg01.mode === 'demo-test' ? 'Ngoại lệ CG01 demo đang bật nhưng capability chưa được xác minh.' : 'CG01 strict cho phép scope này theo proof hiện tại.'
    : runtime?.cg01.reason === 'missing_or_invalid_proof' ? 'CG01 strict đang chặn dispatch vì chưa có capability proof hợp lệ.' : `CG01 đang chặn dispatch (${runtime?.cg01.reason ?? 'chưa lấy được trạng thái'}).`
  const activeScopeRun = runs.find(run => activeRunStatuses.has(run.status))
  const unresolvedScopeRun = runs.find(run => unknownRunStatuses.has(run.status))
  const capacityRun = activeScopeRun ?? unresolvedScopeRun
  const grantMatchesProfile = !!grant && !!profile?.model && grant.model === profile.model && grant.effort === profile.reasoning_effort
  const startBlockers = [
    runtimeReadState !== 'available' && 'Chưa đọc được trạng thái Runtime và giới hạn hiện tại.',
    runReadFailed && 'Không đối chiếu được trạng thái Run mới nhất.',
    !profile?.model && 'Owner chưa chọn model profile Runtime.',
    profile?.model && (profile.model !== model.trim() || profile.reasoning_effort !== effort) && 'Model profile đang sửa chưa được lưu; grant phải khớp profile đã lưu.',
    !selectedEmployee && 'Cần chọn employee cùng EmployeeVersion hiện hành.',
    !!employeeLinkError && employeeLinkError,
    !grant && 'Cần inference grant còn hạn mức, đúng phase và scope.',
    grant && !grantMatchesProfile && 'Inference grant không khớp model/effort của Owner profile.',
    !runtime?.cg01.allowed && `CG01: ${runtime?.cg01.reason ?? 'chưa lấy được authorization proof'}.`,
    capacityRun && `Giới hạn Runtime concurrency 1 đang bị chiếm bởi Run ${capacityRun.id.slice(0, 8)} (${runLabel[capacityRun.status] ?? capacityRun.status}); chưa thể dispatch thêm.`,
  ].filter((value): value is string => typeof value === 'string')
  const demoBatchId = session ? `phase06-ui-${session.scope.company_id.slice(0, 8)}` : ''
  const testGrantExists = grants.some(value => value.phase === '06' && value.batch_id === demoBatchId)
  function createTestGrant() { void action(async () => {
    if (!session || !profile || !profile.model || profile.model !== model.trim() || profile.reasoning_effort !== effort) throw new Error('Hãy lưu model profile đang chọn trước khi cấp grant.')
    if (testGrantExists) throw new Error('Đợt test này đã có grant; tải lại trạng thái trước khi thao tác tiếp.')
    const created = await request<Grant>('runtime/grants', {
      phase: '06', batch_id: demoBatchId, purpose: 'Kiểm thử một lượt inference text-only qua giao diện Phase 06',
      model: profile.model, effort: profile.reasoning_effort, max_requests: 1, max_concurrency: 1,
      timeout_seconds: 120, max_requeues: 0, expires_at: new Date(Date.now() + 15 * 60 * 1000).toISOString(),
    })
    setGrants(previous => [created, ...previous.filter(value => value.id !== created.id)]); setGrantId(created.id)
    setNotice('Đã cấp grant Phase 06 · 1 lượt · 120 giây · hết hạn sau 15 phút · tools tắt. Chưa gọi model.')
  }) }
  function submitRun(event: FormEvent) { event.preventDefault(); void action(async () => {
    if (startBlockers.length || !grant || !runtime?.cg01.allowed || !selectedEmployee || !input.trim()) throw new Error(startBlockers.join(' '))
    const payload={grant_id:grant.id,employee_id:selectedEmployee.employee_id,employee_version_id:selectedEmployee.employee_version_id,phase:grant.phase,batch_id:grant.batch_id,purpose:grant.purpose,model:grant.model,effort:grant.effort,input_text:input,idempotency_key:''}
    const pending=runCreateKey.current
    if (pending && JSON.stringify({...pending.payload,idempotency_key:''}) !== JSON.stringify(payload)) throw new Error('Lần gửi trước chưa được đối chiếu. Giữ nguyên nhân viên, grant và nội dung rồi gửi lại cùng khóa để nhận kết quả đã ghi.')
    const stable=pending ?? {key:crypto.randomUUID(),payload:{...payload}}
    stable.payload.idempotency_key=stable.key
    runCreateKey.current=stable
    let run: Run
    try { run=await request<Run>('runtime/runs',stable.payload,'POST',stable.key) }
    catch (reason) {
      if (reason instanceof ApiError && reason.status < 500) runCreateKey.current=null
      throw reason
    }
    runCreateKey.current=null
    setRuns(previous=>[run,...previous.filter(value=>value.id!==run.id)])
    setNotice(`Đã tạo Run ${run.id.slice(0,8)} cho ${run.employee?.name ?? selectedEmployee.display_name}. Worker sẽ nhận khi grant và gate còn hợp lệ; không gửi lại request khi kết quả chưa rõ.`)
  }) }
  async function refreshRun(id: string) { const run = await request<Run>(`runtime/runs/${encodeURIComponent(id)}`); setRuns(previous => previous.map(value => value.id === id ? run : value)) }
  async function loadReconciliation(id: string) { const value = await request<ReconciliationView>(`runtime/runs/${encodeURIComponent(id)}/reconciliation`, undefined, 'GET'); setReconciliation(previous => ({ ...previous, [id]: value })) }
  function recordUnresolved(run: Run) { const reason = (reconciliationReason[run.id] ?? '').trim(); const keyParts = [run.id, 'unresolved_retained', reason].join(':'); const key = actionKeys.current.get(keyParts) ?? crypto.randomUUID(); actionKeys.current.set(keyParts, key); void action(async () => { const result = await request<{ decision: string; guard_released: boolean; idempotent_replay: boolean }>(`runtime/runs/${encodeURIComponent(run.id)}/reconciliation`, { decision: 'unresolved_retained', reason }, 'POST', key); await loadReconciliation(run.id); setNotice(`Đã ghi quyết định Owner: outcome vẫn chưa rõ; dispatch guard được giữ nguyên (${result.decision}).`) }) }
  function resetStream() { if (session) { try { sessionStorage.removeItem(`ac.events.${session.session_id}`) } catch { /* Storage is optional. */ } } sequence.current = 0; setEvents([]); setCachedIds(new Set()); setHistoryGap(false); setReplayWindowStart(null); setError(''); setReload(value => value + 1) }
  async function createWorkOrder(payload: Record<string, unknown>): Promise<boolean> {
    if (!createKey.current) createKey.current = { key: crypto.randomUUID(), payload }
    const stable = createKey.current
    return await action(async () => {
      const result = await request<{ task_id: string; duplicate: boolean }>('work-orders', stable.payload, 'POST', stable.key)
      createKey.current = null
      setNotice(`Đã lưu Work Order ${result.task_id.slice(0, 8)} ở trạng thái nháp. Chưa có inference.`)
      setReload(value => value + 1)
    })
  }
  async function changeWorkOrder(task: WorkOrder, actionName: TaskActionName, priority = 0, reason?: string): Promise<boolean> {
    const keyParts = [task.task_id, actionName, task.transition_version, priority, reason ?? ''].join(':')
    const key = actionKeys.current.get(keyParts) ?? crypto.randomUUID()
    actionKeys.current.set(keyParts, key)
    return await action(async () => {
      const response = await request<{ status: string; idempotent_replay: boolean }>(`work-orders/${encodeURIComponent(task.task_id)}/actions`, {
        action: actionName, expected_version: task.transition_version, priority, reason: reason ?? null,
      }, 'POST', key)
      actionKeys.current.delete(keyParts)
      setNotice(`${response.idempotent_replay ? 'Đã đối chiếu thao tác trước đó' : 'Đã cập nhật Work Order'} · ${taskLabel[response.status] ?? response.status}.`)
      setReload(value => value + 1)
    })
  }

  async function decideApprovalRecord(approval: ApprovalRecord, decision: 'approve' | 'reject', reason: string): Promise<boolean> {
    const keyParts = [approval.id, approval.payload_hash, decision, reason].join(':')
    const key = actionKeys.current.get(keyParts) ?? crypto.randomUUID()
    actionKeys.current.set(keyParts, key)
    return await action(async () => {
      const response = await request<{ status: string; idempotent_replay: boolean }>(`approvals/${encodeURIComponent(approval.id)}/decision`, {
        decision, expected_payload_hash: approval.payload_hash, reason: reason || null,
      }, 'POST', key)
      actionKeys.current.delete(keyParts)
      setNotice(`Đã ghi quyết định ${decision === 'approve' ? 'duyệt' : 'từ chối'} · ${response.status}. Hành động chưa được dispatch.`)
      setReload(value => value + 1)
    })
  }

  function workerStatus(run: Run) {
    if (!['waiting_model', 'running'].includes(run.status)) return 'Không có worker đang chờ model cho trạng thái này'
    if (runReadFailed) return 'Không đối chiếu được worker · dữ liệu có thể đã cũ'
    const timestamp = run.worker_heartbeat_at ? new Date(run.worker_heartbeat_at).getTime() : NaN
    if (!Number.isFinite(timestamp)) return 'Worker: chưa có heartbeat đã lưu'
    if (run.lease_until && new Date(run.lease_until).getTime() < clockNow) return 'Worker: lease đã hết hạn · cần đối chiếu kết quả'
    return clockNow - timestamp <= 30000 ? 'Worker: heartbeat đã lưu trong 30 giây gần đây' : 'Worker: mất heartbeat / dữ liệu đã cũ'
  }

  return <section className={`runtime-panel${view !== 'runtime' ? ' observatory-panel' : ''}`} aria-labelledby="runtime-title">
    <header className="runtime-heading"><div><p className="eyebrow">{view === 'runtime' ? 'THỰC THI VÀ KẾT NỐI · PHASE 06–07' : view === 'work' ? 'WORK ORDER · TASK QUEUE · PHASE 09' : view === 'approvals' ? 'QUYỀN HẠN · HỘP PHÊ DUYỆT · PHASE 10' : 'LIVE OFFICE · INSPECTOR · REPLAY · PHASE 08'}</p><h2 id="runtime-title">{view === 'runtime' ? 'Runtime demo có kiểm soát' : view === 'work' ? 'Bảng nhiệm vụ và hàng đợi' : view === 'approvals' ? 'Yêu cầu cần Chủ tịch quyết định' : view === 'office' ? 'Hoạt động đã ghi nhận' : view === 'inspector' ? 'Inspector lượt chạy' : 'Phát lại sự kiện đã lưu'}</h2><p>{view === 'runtime' ? 'Đăng nhập Chủ tịch để đọc event và quản lý run trong scope được backend cấp. Mở trang không gọi model.' : view === 'work' ? 'Đăng nhập Chủ tịch để quản lý Work Order trong scope được backend cấp. Thao tác chỉ ghi trạng thái; chưa dispatch hoặc gọi model.' : view === 'approvals' ? 'Quyết định được ghi audit theo payload cố định. Duyệt chỉ ghi nhận approval, không tự chạy công cụ hoặc thay cấu hình.' : 'Đăng nhập Chủ tịch để đọc dữ liệu đã lưu trong scope được backend cấp. Các màn hình này chỉ đọc và không gọi model.'}</p></div>{session && <button className="quiet-button" type="button" disabled={busy} onClick={() => void action(async () => { await request('owner/logout', {}); discardSession(); setNotice('Đã đăng xuất và đóng luồng event.') })}>Đăng xuất</button>}</header>
    {error && <p className="runtime-error" role="alert">{error}</p>}{notice && <p className="runtime-notice" role="status">{notice}</p>}
    {!checked ? <p role="status">Đang xác minh session…</p> : !session ? <form className="runtime-login" onSubmit={login}><label htmlFor="owner-secret">Secret Chủ tịch local</label><input id="owner-secret" type="password" autoComplete="off" value={secret} onChange={event => setSecret(event.target.value)} required maxLength={128} /><p>Nhập secret được bootstrap riêng trên máy. Secret không được lưu trong trình duyệt; đăng nhập không cấp inference grant.</p><button className="primary-button" disabled={busy || !secret}>{busy ? 'Đang xác thực…' : 'Đăng nhập Chủ tịch'}</button></form> : <>
      <p className="runtime-scope">Chủ tịch đã xác thực · Demo scope <code>{session.scope.company_id.slice(0, 8)}</code> · Session có thể hết hạn hoặc bị thu hồi.</p>
      {view === 'approvals' ? <ApprovalInbox approvals={approvals} busy={busy} now={clockNow} onReload={() => setReload(value => value + 1)} onDecision={decideApprovalRecord} /> : view !== 'runtime' ? <Observatory view={view} runs={runs} employees={employees} employeeReadState={employeeReadState} runtimeReadState={runtimeReadState} profile={profile} runReadFailed={runReadFailed} events={events} cachedIds={cachedIds} historyGap={historyGap} replayWindowStart={replayWindowStart} connection={connection} lastSeen={lastSeen} workOrders={workOrders} assignees={assignees} onCreateWorkOrder={createWorkOrder} onTaskAction={changeWorkOrder} onWorkRefresh={() => setReload(value => value + 1)} onReload={resetStream} /> : <>
      <div className="runtime-columns"><form className="runtime-form" onSubmit={saveProfile}><h3>Model profile</h3><p>Backend kiểm tra quyền Owner và catalog khi lưu. Catalog và profile chưa xác nhận entitlement.</p><label htmlFor="runtime-model">Model ID</label><input id="runtime-model" value={model} onChange={event => setModel(event.target.value)} required maxLength={100} /><label htmlFor="runtime-effort">Reasoning effort</label><select id="runtime-effort" value={effort} onChange={event => setEffort(event.target.value)}>{['minimal', 'low', 'medium', 'high', 'xhigh', 'max', 'ultra', 'persistent'].map(value => <option key={value}>{value}</option>)}</select><label htmlFor="runtime-fallback">Fallback được phép (phân cách bằng dấu phẩy)</label><input id="runtime-fallback" value={fallback} onChange={event => setFallback(event.target.value)} maxLength={600} /><small>Danh sách này chỉ là cấu hình. Runtime không tự retry hoặc đổi model khi kết quả chưa rõ.</small><button className="quiet-button" disabled={busy || !profile}>{busy ? 'Đang xử lý…' : `Lưu profile · v${profile?.version ?? '—'}`}</button></form>
      <form className="runtime-form" id="runtime-task-form" onSubmit={submitRun}>
        <h3>Chạy nhân viên demo · text-only</h3>
        <p className="runtime-gate" role="status">{gateMessage} · {runtime?.cg01.reason ?? 'Chưa lấy được trạng thái gate'}</p>
        {runtime?.cg01.mode === 'demo-test' && <p className="runtime-access-note">Ngoại lệ demo đang được cấu hình ở backend. CG01 vẫn chưa được xác minh; không dùng chế độ này để nghiệm thu release.</p>}
        <label htmlFor="runtime-employee">Nhân viên demo</label>
        <select id="runtime-employee" value={employeeId} onChange={event => { const selected=employees.find(item=>item.employee_id===event.target.value); setEmployeeId(selected?.employee_id ?? ''); setEmployeeVersionId(selected?.employee_version_id ?? ''); setEmployeeLinkError('') }} required disabled={!employees.length || !!runCreateKey.current}>
          <option value="">{employees.length ? 'Chọn nhân viên' : 'Không có nhân viên demo đang hoạt động'}</option>
          {employees.map(item => <option key={item.employee_id} value={item.employee_id}>{item.display_name} · {item.role} · hồ sơ v{item.version}</option>)}
        </select>
        {employeeLinkError && <p className="runtime-error" role="alert">{employeeLinkError}</p>}
        {selectedEmployee && <p className="runtime-grant-detail">{selectedEmployee.display_name} · {selectedEmployee.role} · hồ sơ v{selectedEmployee.version} · version {selectedEmployee.employee_version_id}{selectedEmployee.department ? ` · ${selectedEmployee.department}` : ''}. Run sẽ giữ đúng EmployeeVersion này.</p>}
        <p>Profile hiện lưu: <strong>{profile?.model ?? 'chưa chọn model'} · {profile?.reasoning_effort ?? 'chưa chọn effort'}</strong>. Model/effort thực thi phải khớp grant được Owner chọn.</p>
        <label htmlFor="runtime-grant">Grant riêng đã được Owner cấp</label>
        <select id="runtime-grant" value={grantId} onChange={event => setGrantId(event.target.value)} required disabled={!!runCreateKey.current}>
          <option value="">{eligibleGrants.length ? 'Chọn grant còn hạn mức' : 'Chưa có grant còn hạn mức'}</option>
          {eligibleGrants.map(value => <option key={value.id} value={value.id}>Phase {value.phase} · {value.batch_id} · còn {value.max_requests-value.used_requests}/{value.max_requests} request</option>)}
        </select>
        {grant ? <p className="runtime-grant-detail">{grant.purpose} · {grant.model} / {grant.effort} · còn {grant.max_requests-grant.used_requests}/{grant.max_requests} request · concurrency {grant.max_concurrency} · hết hạn {time(grant.expires_at)} · tools/fallback/retry tắt.</p> : <p className="runtime-access-note" role="status">Cần grant còn hạn, đúng phase, batch, model và effort. Bấm Start không tạo hoặc gia hạn grant.</p>}
        {!eligibleGrants.length && <button className="quiet-button" type="button" disabled={busy || !profile?.model || profile.model !== model.trim() || profile.reasoning_effort !== effort || testGrantExists} onClick={createTestGrant}>{testGrantExists ? 'Grant Phase 06 của đợt này đã được ghi' : 'Tạo grant test Phase 06 riêng'}</button>}
        <label htmlFor="runtime-input">Văn bản tin cậy trong scope demo</label>
        <textarea id="runtime-input" rows={5} value={input} onChange={event => setInput(event.target.value)} required maxLength={16000} disabled={!!runCreateKey.current} />
        <small>Start chỉ tạo một Run gắn employee/version và grant hiện chọn. Worker Compose mới dispatch khi authorization, grant, CG01 và giới hạn tài nguyên còn hợp lệ. Không có tools, fallback hoặc retry; usage/cost thiếu nguồn sẽ hiện unknown.</small>
        {runCreateKey.current && <p className="runtime-access-note" role="status">Lần gửi trước chưa được đối chiếu. Gửi lại cùng dữ liệu để dùng cùng idempotency key; không sửa nhân viên, grant hoặc nội dung trước khi biết kết quả.</p>}
        <div className="runtime-blocker-list" role="status" aria-label="Điều kiện cần để bắt đầu">
          <strong>{startBlockers.length ? 'Start đang bị chặn bởi:' : 'Điều kiện đã sẵn sàng để tạo Run.'}</strong>
          {startBlockers.length > 0 && <ul>{startBlockers.map((blocker, index) => <li key={`${index}-${blocker}`}>{blocker}</li>)}</ul>}
        </div>
        <button className="primary-button" disabled={busy || startBlockers.length > 0 || !input.trim()}>Bắt đầu Run text-only</button>
      </form>
      </div>
      <section className="runtime-runs" aria-labelledby="runtime-runs-title"><div className="runtime-subheading"><h3 id="runtime-runs-title">Run đã lưu</h3><button className="quiet-button" type="button" disabled={busy} onClick={() => setReload(value => value + 1)}>Tải trạng thái</button></div>{!runs.length ? <p>Chưa có run trong scope này.</p> : runs.map(run => <article className="runtime-run" id={`runtime-run-${run.id}`} key={run.id}><div><strong>{runLabel[run.status] ?? run.status}</strong><code>{run.id}</code><p>{run.model} · {run.effort} · {time(run.created_at)}</p><p>{workerStatus(run)} · Cập nhật worker: {time(run.worker_heartbeat_at ?? null)}</p><small>Trạng thái đã lưu không chứng minh agent còn hoạt động. Heartbeat event store độc lập với worker.</small><p>Usage: {display(run.usage)} · Outcome: {display(run.outcome)}</p>{run.stop_requested && <p>Đã yêu cầu dừng. Request đang bay có thể còn xử lý; kết quả phải được đối chiếu.</p>}{run.output !== undefined && run.output !== null && <details><summary>Kết quả đã lưu</summary><pre>{display(run.output)}</pre></details>}</div><div className="runtime-run-actions"><button className="quiet-button" type="button" disabled={busy} onClick={() => void action(() => refreshRun(run.id))}>Đối chiếu</button>{['queued', 'waiting', 'waiting_model', 'running', 'dispatching', 'pending'].includes(run.status) && <button className="quiet-button" type="button" disabled={busy || run.stop_requested} onClick={() => void action(async () => { const updated = await request<Run>(`runtime/runs/${encodeURIComponent(run.id)}/stop`, {}); setRuns(previous => previous.map(value => value.id === run.id ? updated : value)); setNotice('Đã ghi yêu cầu dừng; không giả định gateway đã hủy request.') })}>Yêu cầu dừng</button>}{run.status === 'interrupted' && <button className="quiet-button" type="button" disabled={busy} onClick={() => void action(() => loadReconciliation(run.id))}>Bằng chứng outcome</button>}</div>{reconciliation[run.id] && <div className="runtime-reconciliation" aria-label="Đối chiếu Runtime"><h4>Đối chiếu outcome · {reconciliation[run.id].classification}</h4><p>Request span: <code>{reconciliation[run.id].request_span_id ?? 'Chưa có'}</code> · Gateway call: <code>{reconciliation[run.id].gateway_call_id ?? 'Chưa có'}</code></p><p>Usage: {reconciliation[run.id].usage_status} · {display(reconciliation[run.id].usage)} · Cost: {reconciliation[run.id].cost_status}</p><p>Lease: {reconciliation[run.id].lease.status} · heartbeat {time(reconciliation[run.id].lease.heartbeat_at)} · hết hạn {time(reconciliation[run.id].lease.lease_until)}</p><p>Grant: {String(reconciliation[run.id].grant.batch_id)} · đã dùng {String(reconciliation[run.id].grant.used_requests)}/{String(reconciliation[run.id].grant.max_requests)} · hết hạn {time(String(reconciliation[run.id].grant.expires_at))}</p><p>Dispatch guard: {reconciliation[run.id].dispatch_guard.held_for_this_call ? 'đang giữ cho request này' : reconciliation[run.id].dispatch_guard.held ? 'đang giữ cho request khác' : 'không giữ'}. Kết quả gateway chưa đủ chứng cứ để xác nhận hủy/hoàn tất nếu classification là unresolved.</p><ul>{reconciliation[run.id].checkpoints.map(value => <li key={`${value.sequence}-${value.boundary}`}>Checkpoint {value.sequence} · {value.boundary} · {time(value.created_at)} · replay allowed: {display(value.replay_allowed)}</li>)}</ul><p>Events liên quan: {reconciliation[run.id].evidence.map(value => `${value.event_type} (${time(value.recorded_at)})`).join(' · ') || 'chưa có'}</p>{reconciliation[run.id].decisions.map(value => <p key={value.id}>Owner decision {value.decision} · {value.reason} · {time(value.created_at)}</p>)}{reconciliation[run.id].available_actions.includes('record_unresolved_keep_guard') && <form onSubmit={event => { event.preventDefault(); recordUnresolved(run) }}><label htmlFor={`reconciliation-reason-${run.id}`}>Lý do ghi nhận outcome vẫn chưa rõ</label><textarea id={`reconciliation-reason-${run.id}`} value={reconciliationReason[run.id] ?? ''} onChange={event => setReconciliationReason(previous => ({ ...previous, [run.id]: event.target.value }))} maxLength={500} required /><button className="quiet-button" type="submit" disabled={busy || !(reconciliationReason[run.id] ?? '').trim()}>Ghi quyết định Owner · giữ dispatch guard</button></form>}</div>}</article>)}</section>
      <section className="runtime-events" aria-labelledby="runtime-events-title"><div className="runtime-subheading"><div><h3 id="runtime-events-title">Luồng event đã commit</h3><p role="status">Kết nối event store: {connectionLabel[connection]} · Cập nhật kết nối: {time(lastSeen)}</p></div><button className="quiet-button" type="button" onClick={resetStream}>Tải lại từ dữ liệu đã lưu</button></div><p>Chỉ phản ánh event của ứng dụng. Trạng thái waiting không thể hiện tiến độ hay token nội bộ của model. Hiển thị tối đa 200 event gần đây; đây chưa phải giao diện replay.</p>{!events.length ? <p>Chưa nhận event kể từ cursor của session này.</p> : <ol>{events.map(event => <li key={event.event_id}><strong>#{event.stream_seq} · {event.event_type}</strong><span>{time(event.recorded_at)} · {event.source} {event.run_id ? `· run ${event.run_id.slice(0, 8)}` : ''}</span><code>{event.event_id}</code>{cachedIds.has(event.event_id) && <small>Metadata cache local · chưa đối chiếu nội dung với server; tải lại để xác minh.</small>}</li>)}</ol>}</section>
      </>}
    </>}
  </section>
}

function ApprovalInbox({ approvals, busy, now, onReload, onDecision }: { approvals: ApprovalRecord[]; busy: boolean; now: number; onReload: () => void; onDecision: (approval: ApprovalRecord, decision: 'approve' | 'reject', reason: string) => Promise<boolean> }) {
  const [reasons, setReasons] = useState<Record<string, string>>({})
  const live = approvals.filter(item => item.status === 'pending' && item.task_revision !== null && item.expires_at !== null && new Date(item.expires_at).getTime() > now)
  return <section className="approval-inbox" aria-labelledby="approval-inbox-title">
    <div className="runtime-subheading"><div><h3 id="approval-inbox-title">Hộp phê duyệt</h3><p>{live.length} yêu cầu còn hiệu lực · payload và phạm vi được chốt bằng hash.</p></div><button className="quiet-button" type="button" disabled={busy} onClick={onReload}>Tải lại inbox</button></div>
    <p className="approval-dispatch-note">Duyệt/từ chối chỉ ghi quyết định vào audit. Chưa có executor được nối để thực hiện hành động sau duyệt.</p>
    {!approvals.length ? <div className="approval-empty"><h4>Chưa có yêu cầu phê duyệt</h4><p>Yêu cầu sẽ xuất hiện khi một hành động trong Work Order cần Chủ tịch xem xét. Mở trang này không tạo yêu cầu hay gọi model.</p></div> : <div className="approval-list">{approvals.map(item => {
      const reviewable = item.status === 'pending' && item.task_revision !== null && item.expires_at !== null && new Date(item.expires_at).getTime() > now
      return <article className="approval-card" key={item.id}>
        <div className="approval-card-heading"><div><span className={`approval-state approval-${item.status}`}>{item.status === 'pending' ? reviewable ? 'Chờ quyết định' : 'Thiếu snapshot review' : item.status}</span><h4>{item.summary}</h4></div><code>{item.id.slice(0, 8)}</code></div>
        <p>{item.task_goal} · revision {item.task_revision ?? 'chưa ghi'} {item.run_id ? `· run ${item.run_id.slice(0, 8)}` : '· không gắn run'}</p>
        <dl className="approval-metadata"><div><dt>Hành động</dt><dd>{item.action_type}</dd></div><div><dt>Hạn</dt><dd>{item.expires_at ? time(item.expires_at) : 'Chưa ghi'}</dd></div><div><dt>Policy</dt><dd>{item.policy_id ? `v${item.policy_version}` : 'Chưa gắn policy'}</dd></div><div><dt>Ngân sách snapshot</dt><dd>{display(item.budget_snapshot)}</dd></div></dl>
        <details><summary>Payload, provenance và hash</summary><pre>{JSON.stringify(item.action_payload, null, 2)}</pre><p>Payload SHA-256 <code>{item.payload_hash}</code></p>{item.decision_hash && <p>Decision SHA-256 <code>{item.decision_hash}</code></p>}{item.decision_reason && <p>Lý do: {item.decision_reason}</p>}</details>
        {reviewable && <div className="approval-actions"><label htmlFor={`approval-reason-${item.id}`}>Lý do quyết định (tùy chọn)</label><input id={`approval-reason-${item.id}`} maxLength={500} value={reasons[item.id] ?? ''} onChange={event => setReasons(value => ({ ...value, [item.id]: event.target.value }))} /><button className="primary-button" type="button" disabled={busy} onClick={() => void onDecision(item, 'approve', reasons[item.id] ?? '')}>Ghi nhận duyệt</button><button className="quiet-button" type="button" disabled={busy} onClick={() => void onDecision(item, 'reject', reasons[item.id] ?? '')}>Từ chối</button></div>}
        {!reviewable && item.status === 'pending' && <p className="approval-legacy-note">Yêu cầu cũ/fixture thiếu expiry hoặc task revision; hệ thống khóa quyết định vì không đủ bằng chứng.</p>}
      </article>
    })}</div>}
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
function employeeRunState(employeeRuns: Run[], freshness: 'live' | 'offline' | 'stale' | 'gap' | 'reconnecting' | 'connecting'): { kind: string; label: string; active: Run | null; latest: Run | null; detail: string | null } {
  const active = employeeRuns.find(run => activeRunStatuses.has(run.status))
  const unknown = employeeRuns.find(run => unknownRunStatuses.has(run.status))
  const failed = employeeRuns.find(run => run.status === 'failed')
  const latest = employeeRuns[0]
  if (freshness !== 'live') {
    const label = freshness === 'offline' ? 'Mất kết nối' : freshness === 'stale' ? 'Dữ liệu đã cũ' : freshness === 'gap' ? 'Có khoảng trống dữ liệu' : freshness === 'reconnecting' ? 'Đang kết nối lại' : 'Đang xác minh trạng thái'
    return { kind: freshness, label: latest ? `${label} · Run gần nhất: ${runLabel[latest.status] ?? latest.status}` : `${label} · chưa xác minh có lượt đang chạy`, active: null, latest: latest ?? null, detail: null }
  }
  if (active) {
    const text = active.status === 'running' ? 'Đang thực hiện' : active.status === 'waiting_model' ? 'Đang chờ phản hồi model' : active.status === 'queued' ? 'Đang chờ worker' : runLabel[active.status] ?? active.status
    return { kind: active.status === 'queued' ? 'waiting' : 'active', label: text, active, latest: latest ?? null, detail: null }
  }
  if (unknown) return { kind: 'unknown', label: 'Kết quả Run chưa rõ · cần đối chiếu', active: null, latest: unknown, detail: null }
  if (failed) return { kind: 'failed', label: 'Run gần nhất thất bại', active: null, latest: failed, detail: null }
  const latestLabel = latest ? `Run gần nhất: ${runLabel[latest.status] ?? latest.status}` : 'Chưa có Run lịch sử trong 20 lượt gần nhất.'
  return { kind: 'idle', label: 'Không có Run đang hoạt động', active: null, latest: latest ?? null, detail: latestLabel }
}

function Observatory({ view, runs, employees, employeeReadState, runtimeReadState, profile, runReadFailed, events, cachedIds, historyGap, replayWindowStart, connection, lastSeen, workOrders, assignees, onCreateWorkOrder, onTaskAction, onWorkRefresh, onReload }: { view: Exclude<ObservationView, 'approvals'>; runs: Run[]; employees: EmployeeOption[]; employeeReadState: ReadState; runtimeReadState: ReadState; profile: Profile | null; runReadFailed: boolean; events: DomainEvent[]; cachedIds: Set<string>; historyGap: boolean; replayWindowStart: number | null; connection: Connection; lastSeen: string | null; workOrders: WorkOrder[]; assignees: Assignee[]; onCreateWorkOrder: (payload: Record<string, unknown>) => Promise<boolean>; onTaskAction: (task: WorkOrder, action: TaskActionName, priority?: number, reason?: string) => Promise<boolean>; onWorkRefresh: () => void; onReload: () => void }) {
  const [runId, setRunId] = useState(() => {
    const requested = new URLSearchParams(window.location.hash.split('?')[1] ?? '').get('run_id')
    return requested && /^[0-9a-f-]{36}$/i.test(requested) ? requested : 'all'
  })
  const [position, setPosition] = useState(0)
  useEffect(() => {
    const syncRunFromHash = () => {
      const requested = new URLSearchParams(window.location.hash.split('?')[1] ?? '').get('run_id')
      setRunId(requested && /^[0-9a-f-]{36}$/i.test(requested) ? requested : 'all')
      setPosition(0)
    }
    syncRunFromHash()
    window.addEventListener('hashchange', syncRunFromHash)
    return () => window.removeEventListener('hashchange', syncRunFromHash)
  }, [view])
  const selectedRunId = view === 'inspector' && runId === 'all' ? events.at(-1)?.run_id ?? runs[0]?.id ?? 'all' : runId
  const scopedEvents = events.filter(event => selectedRunId === 'all' || event.run_id === selectedRunId)
  const selectedRun = runs.find(run => run.id === selectedRunId) ?? null
  const currentEvent = scopedEvents[Math.min(position, Math.max(scopedEvents.length - 1, 0))] ?? null
  const freshness: 'live' | 'offline' | 'stale' | 'gap' | 'reconnecting' | 'connecting' = employeeReadState === 'unavailable' || runtimeReadState === 'unavailable' || runReadFailed || connection === 'offline'
    ? 'offline'
    : connection === 'live' && employeeReadState === 'available' && runtimeReadState === 'available' ? 'live'
      : connection === 'stale' ? 'stale'
        : connection === 'gap' ? 'gap'
          : connection === 'reconnecting' || connection === 'recovering' ? 'reconnecting' : 'connecting'
  const employeeGroups = new Map<string, EmployeeOption[]>()
  for (const employee of employees) {
    const name = employee.department?.trim() || 'Không có phòng ban được liên kết'
    employeeGroups.set(name, [...(employeeGroups.get(name) ?? []), employee])
  }
  const unassignedRuns = runs.filter(run => !run.employee)
  return <div className="observatory-content">
    <div className="observatory-status"><span className={`live-indicator${connection === 'offline' || connection === 'gap' || connection === 'stale' ? ' offline' : ''}`}><span />{connectionLabel[connection]}</span><span>Cập nhật kết nối: {time(lastSeen)}</span><span>Scope: Chủ tịch đã xác thực</span></div>
    {view === 'work' && <WorkBoard tasks={workOrders} assignees={assignees} onCreate={onCreateWorkOrder} onAction={onTaskAction} onRefresh={onWorkRefresh} />}
    {view === 'office' && <>
      <section className={`office-freshness freshness-${freshness}`} aria-live="polite">
        <span className="office-freshness-mark" aria-hidden="true" />
        <div><strong>{freshness === 'live' ? 'Trạng thái đã đối chiếu' : freshness === 'offline' ? 'Không thể xác minh trạng thái mới' : freshness === 'stale' ? 'Dữ liệu đang cũ' : freshness === 'gap' ? 'Event store có khoảng trống' : freshness === 'reconnecting' ? 'Đang nối lại dữ liệu' : 'Đang xác minh dữ liệu'}</strong>
          <p>{freshness === 'live' ? 'Employee và Runtime Run trong scope đã tải; trạng thái hoạt động chỉ dựa trên Run đã lưu.' : `Event feed: ${connectionLabel[connection]}${employeeReadState === 'unavailable' ? ' · API employee chưa trả lời' : ''}${runtimeReadState === 'unavailable' || runReadFailed ? ' · API Runtime chưa trả lời' : ''}. Không kết luận employee đang rảnh hoặc đang thực thi khi nguồn chưa được đối chiếu.`}</p>
        </div>
        <span className="office-freshness-time">{time(lastSeen)}</span>
      </section>
      <section className="office-roster" aria-labelledby="office-roster-title" data-freshness={freshness}>
        <div className="office-roster-heading"><div><p className="eyebrow">NHÂN SỰ TRONG SCOPE HIỆN TẠI</p><h3 id="office-roster-title">Đội ngũ demo</h3><p>Hồ sơ lấy từ API Owner-scoped; hoạt động lấy từ Runtime Run đã lưu.</p></div><span className="office-roster-count">{employeeReadState === 'available' ? `${employees.length} nhân viên` : employeeReadState === 'loading' ? 'Đang tải' : 'Không khả dụng'}</span></div>
        {employeeReadState === 'loading' && <p className="office-roster-state" role="status">Đang tải danh sách employee và EmployeeVersion…</p>}
        {employeeReadState === 'unavailable' && <p className="office-roster-state office-roster-error" role="alert">Không tải được danh sách employee trong scope Owner. Kiểm tra session hoặc kết nối API rồi mở lại trang.</p>}
        {employeeReadState === 'available' && !employees.length && <p className="office-roster-state">Không có employee active/probation trong scope Demo hiện tại.</p>}
        {employeeReadState === 'available' && employees.length > 0 && <div className="office-department-groups">{[...employeeGroups.entries()].map(([department, members]) => <section className="office-team" key={department} aria-label={`Phòng ban ${department}`}>
          <div className="office-team-heading"><h4>{department}</h4><span>{members.length}</span></div>
          <div className="office-employee-grid">{members.map(employee => {
            const employeeRuns = runs.filter(run => run.employee?.id === employee.employee_id)
            const currentVersionRuns = employeeRuns.filter(run => run.employee?.version_id === employee.employee_version_id)
            const status = employeeRunState(currentVersionRuns, freshness)
            const latestRun = status.latest
            return <article className="office-employee-card" key={`${employee.employee_id}:${employee.employee_version_id}`} data-employee-id={employee.employee_id} data-employee-version-id={employee.employee_version_id}>
              <header className="office-employee-header"><span className="office-employee-avatar" aria-hidden="true">{employee.display_name.trim().slice(0, 1).toLocaleUpperCase('vi-VN')}</span><div><h5>{employee.display_name}</h5><p>{employee.role}</p></div><span className={`office-employee-state state-${status.kind}`} title={status.label}>{status.label}</span></header>
              {status.detail && <p className="office-employee-state-detail">{status.detail}</p>}
              {status.active && <div className="office-active-run"><strong>Run đã lưu · {runLabel[status.active.status] ?? status.active.status}</strong><span>{status.active.task_goal || 'Mục tiêu chưa có'} · {status.active.model || 'Model chưa biết'} / {status.active.effort || 'effort chưa biết'}</span><small>Heartbeat worker: {time(status.active.worker_heartbeat_at ?? null)}. Dữ liệu này phản ánh Run, không khẳng định tiến độ token.</small></div>}
              <p className="office-employee-version">EmployeeVersion <strong>v{employee.version}</strong> · {lifecycleLabel[employee.lifecycle] ?? employee.lifecycle}</p>
              <p className="office-employee-profile">{latestRun ? <>Profile trong Run gần nhất: <strong>{latestRun.model || 'Model chưa biết'} · {latestRun.effort || 'effort chưa biết'}</strong> · version nhân viên v{latestRun.employee?.version ?? 'chưa biết'}</> : <>Runtime profile của Owner: <strong>{profile?.model ?? 'chưa chọn model'} · {profile?.reasoning_effort ?? 'chưa chọn effort'}</strong>. Đây là cấu hình dùng chung, không phải model riêng của employee.</>}</p>
              <nav className="office-employee-actions" aria-label={`Hành động cho ${employee.display_name}`}><a className="office-primary-link" href={runtimeEmployeeHref(employee)}>Mở form Runtime</a><details><summary>Chi tiết hồ sơ</summary><dl><div><dt>Employee ID</dt><dd><code>{employee.employee_id}</code></dd></div><div><dt>EmployeeVersion ID</dt><dd><code>{employee.employee_version_id}</code></dd></div><div><dt>Phòng ban</dt><dd>{employee.department ?? 'Không có phòng ban được liên kết'}</dd></div><div><dt>Lifecycle</dt><dd>{lifecycleLabel[employee.lifecycle] ?? employee.lifecycle}</dd></div></dl></details></nav>
              <details className="office-employee-history"><summary>Run gần đây <span>{employeeRuns.length}</span></summary>
                {!employeeRuns.length ? <p>Chưa có Run gắn với employee này trong 20 lượt gần nhất mà API trả về.</p> : <ol>{employeeRuns.map(run => <li key={run.id}><div><strong>{runLabel[run.status] ?? run.status} · hồ sơ v{run.employee?.version ?? 'chưa biết'}</strong><span>{run.task_goal || 'Mục tiêu chưa có'}</span><small>{run.model || 'Model chưa biết'} · {run.effort || 'effort chưa biết'} · {time(run.created_at)}</small>{run.synthetic_test_data && <span className="fixture-badge">SYNTHETIC TEST</span>}</div><nav aria-label={`Bằng chứng Run ${run.id.slice(0, 8)}`}><a href={`#inspector?run_id=${encodeURIComponent(run.id)}`}>Inspector</a><a href={`#replay?run_id=${encodeURIComponent(run.id)}`}>Replay</a>{unknownRunStatuses.has(run.status) && <a href={runtimeReconciliationHref(employee, run)}>Đối chiếu outcome</a>}</nav></li>)}</ol>}
              </details>
            </article>
          })}</div>
        </section>)}</div>}
      </section>
      {unassignedRuns.length > 0 && <section className="office-unassigned" aria-labelledby="office-unassigned-title"><div className="runtime-subheading"><h3 id="office-unassigned-title">Run chưa có employee liên kết</h3><span>{unassignedRuns.length}</span></div><p>Các Run lịch sử này không có EmployeeVersion phù hợp trong dữ liệu đã lưu; không gán chúng cho hồ sơ hiện tại.</p><ul>{unassignedRuns.map(run => <li key={run.id}><div><strong>{runLabel[run.status] ?? run.status}</strong><span>{run.model || 'Model chưa biết'} · {time(run.created_at)}</span></div><nav><a href={`#inspector?run_id=${encodeURIComponent(run.id)}`}>Inspector</a><a href={`#replay?run_id=${encodeURIComponent(run.id)}`}>Replay</a></nav></li>)}</ul></section>}
      <p className="observatory-note">Roster lấy employee active/probation, EmployeeVersion hiện hành và quan hệ phòng ban do backend trả về trong scope Owner. API cung cấp tối đa 20 Run gần nhất. Chỉ Run đã lưu quyết định trạng thái; không có Run không được suy diễn thành worker hoạt động.</p>
    </>}
    {view === 'inspector' && <>
      <div className="observatory-controls"><label htmlFor="inspector-run">Lượt chạy đã lưu</label><select id="inspector-run" value={runId} onChange={event => setRunId(event.target.value)}><option value="all">Run có event mới nhất</option>{runs.map(run => <option key={run.id} value={run.id}>{run.id.slice(0, 8)} · {runLabel[run.status] ?? run.status}</option>)}</select><button className="quiet-button" type="button" onClick={onReload}>Đọc lại từ event store</button></div>
      {selectedRun ? <><section className="inspector-summary"><div><span>Nhân viên</span><strong>{selectedRun.employee ? `${selectedRun.employee.name} · ${selectedRun.employee.role} · v${selectedRun.employee.version}` : 'Chưa phân công nhân viên'}</strong></div><div><span>Trạng thái run · task</span><strong>{runLabel[selectedRun.status] ?? 'Chưa biết'} · {taskLabel[selectedRun.task_status] ?? selectedRun.task_status ?? 'Chưa biết'}</strong></div><div><span>Model · effort</span><strong>{selectedRun.model || 'Chưa biết'} · {selectedRun.effort || 'Chưa biết'}</strong></div><div><span>Usage · nguồn</span><strong>{display(selectedRun.usage)} · {selectedRun.usage_provenance ?? 'unknown'}</strong></div><div><span>Chi phí</span><strong>{selectedRun.cost_basis === 'unknown' ? 'Chưa biết' : selectedRun.cost_basis ?? 'Chưa biết'}</strong></div><div><span>Outcome</span><strong>{display(selectedRun.outcome)}</strong></div><code>{selectedRun.id}</code><small>Task: {selectedRun.task_id ?? 'Chưa liên kết'} · {selectedRun.task_goal ?? 'Mục tiêu chưa có'} · Tạo lúc {time(selectedRun.created_at)}</small>{selectedRun.synthetic_test_data && <span className="fixture-badge">SYNTHETIC TEST DATA · KHÔNG PHẢI INFERENCE THẬT</span>}<div className="inspector-run-links"><a href={`#replay?run_id=${encodeURIComponent(selectedRun.id)}`}>Mở Replay chỉ đọc của Run này</a><a href="#office">Về Live Office</a></div></section>{selectedRun.output !== undefined && selectedRun.output !== null && <section className="inspector-events"><h3>Kết quả đã lưu</h3><pre>{display(selectedRun.output)}</pre></section>}<div className="inspector-sections"><section><h3>Plan và tóm tắt quyết định</h3><p>Chưa có summary tường minh trong event projection hiện tại.</p></section><section><h3>Tools, file diff và messages</h3><p>Tools bị tắt trong vertical slice này.</p></section><section><h3>Lỗi, profile và metrics</h3><p>Profile gắn employee/version và grant được chốt khi tạo Run. Usage provenance: {selectedRun.usage_provenance ?? 'unknown'} · cost basis: {selectedRun.cost_basis ?? 'unknown'}.</p></section></div><section className="inspector-events"><h3>Sự kiện liên quan · {scopedEvents.length}</h3>{scopedEvents.length ? <ol>{scopedEvents.map(event => <li key={event.event_id}><div><strong>#{event.stream_seq} · {event.event_type}</strong><small>{time(event.recorded_at)} · {event.source} · run {event.run_id?.slice(0,8) ?? '—'} · task {event.task_id?.slice(0,8) ?? '—'} · employee {event.agent_id?.slice(0,8) ?? '—'} · version {event.employee_version_id?.slice(0,8) ?? '—'}</small><p>{eventSummary(event)}</p></div><code>{event.event_id}</code></li>)}</ol> : <p>Chưa có event đã tải cho lượt này.</p>}</section></> : <p>Chọn một lượt chạy hoặc cần tải event đã lưu trước khi có lượt chạy phù hợp.</p>}
    </>}
    {view === 'replay' && <>
      <div className="observatory-controls"><label htmlFor="replay-run">Lọc theo lượt chạy</label><select id="replay-run" value={runId} onChange={event => { setRunId(event.target.value); setPosition(0) }}><option value="all">Tất cả event trong cửa sổ đã tải</option>{runs.map(run => <option key={run.id} value={run.id}>{run.id.slice(0, 8)} · {runLabel[run.status] ?? run.status}</option>)}</select><button className="quiet-button" type="button" onClick={onReload}>Tải lại từ đầu</button></div>
      <p className="observatory-note">Replay chỉ đọc dữ liệu đã commit. Đang hiển thị tối đa 200 event gần nhất; snapshot khôi phục trạng thái hiện tại, không tự dựng lại lịch sử đã mất.</p>
      {historyGap && <p className="runtime-error" role="status">Lịch sử trước event #{replayWindowStart ?? 'không xác định'} đã thiếu trong nguồn lưu. Replay không thể khôi phục các event đã bị retention loại bỏ.</p>}
      {!historyGap && replayWindowStart !== null && replayWindowStart > 1 && <p className="observatory-note" role="status">Cửa sổ này bắt đầu tại event #{replayWindowStart}; event cũ hơn vẫn nằm ngoài 200 event đang hiển thị.</p>}
      {scopedEvents.length ? <><label className="replay-range-label" htmlFor="replay-position">Mốc {Math.min(position + 1, scopedEvents.length)} / {scopedEvents.length}</label><input id="replay-position" className="replay-range" type="range" min={0} max={Math.max(0, scopedEvents.length - 1)} value={Math.min(position, scopedEvents.length - 1)} onChange={event => setPosition(Number(event.target.value))} aria-valuetext={currentEvent ? `Event ${currentEvent.stream_seq}: ${currentEvent.event_type}` : 'Không có event'} /><ol className="replay-timeline">{scopedEvents.map((event, index) => <li className={index === Math.min(position, scopedEvents.length - 1) ? 'selected' : ''} key={event.event_id}><button type="button" onClick={() => setPosition(index)} aria-current={index === position ? 'step' : undefined}><span>#{event.stream_seq}</span><strong>{event.event_type}</strong><small>{time(event.recorded_at)}</small><p>{eventSummary(event)}</p></button></li>)}</ol></> : <section className="observatory-empty"><h3>Chưa có event phù hợp</h3><p>Đăng nhập Chủ tịch để tải event store; không có timeline nào được tạo từ fixture.</p></section>}
    </>}
    {cachedIds.size > 0 && <p className="observatory-note">Có metadata cũ từ cache session; nội dung chi tiết chỉ được đưa vào sau khi đối chiếu với event store.</p>}
  </div>
}


function WorkBoard({ tasks, assignees, onCreate, onAction, onRefresh }: { tasks: WorkOrder[]; assignees: Assignee[]; onCreate: (payload: Record<string, unknown>) => Promise<boolean>; onAction: (task: WorkOrder, action: TaskActionName, priority?: number, reason?: string) => Promise<boolean>; onRefresh: () => void }) {
  const [goal,setGoal]=useState('')
  const [outputs,setOutputs]=useState('')
  const [criteria,setCriteria]=useState('')
  const [refs,setRefs]=useState('')
  const [duration,setDuration]=useState('120')
  const [reworkLimit,setReworkLimit]=useState('0')
  const [assignee,setAssignee]=useState('')
  const [reviewer,setReviewer]=useState('')
  const [priority,setPriority]=useState('0')
  const [filter,setFilter]=useState('all')
  const [query,setQuery]=useState('')
  const [createPending,setCreatePending]=useState(false)
  const [pendingPayload,setPendingPayload]=useState<Record<string,unknown>|null>(null)
  const [reworkReason,setReworkReason]=useState<Record<string,string>>({})
  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const payload = pendingPayload ?? {
      goal, expected_outputs: outputs.split('\n').map(value=>value.trim()).filter(Boolean),
      acceptance_criteria: [{id:'AC01',description:criteria.trim(),evidence_kind:'owner_review'}],
      scope: {input_refs:refs.split('\n').map(value=>value.trim()).filter(Boolean),tool_capabilities:[]},
      deadline_at:null,budget_limits:{max_model_requests:0,cost_basis:'unknown'},
      stop_conditions:{max_duration_seconds:Number(duration),max_rework_rounds:Number(reworkLimit)},
      assignee_id:assignee||null,reviewer_id:reviewer||null,autonomy:'strict',
    }
    setCreatePending(true);setPendingPayload(payload)
    void onCreate(payload).then(success=>{if(success){setGoal('');setOutputs('');setCriteria('');setRefs('');setAssignee('');setReviewer('');setCreatePending(false);setPendingPayload(null)}else{setCreatePending(false)}})
  }
  const visible = tasks.filter(task => (filter==='all'||task.status===filter) && (!query.trim()||task.goal.toLocaleLowerCase('vi').includes(query.trim().toLocaleLowerCase('vi'))))
  const groups: {title:string; statuses:string[]}[] = [
    {title:'Bản nháp',statuses:['draft']},{title:'Hàng đợi',statuses:['queued']},
    {title:'Đang xử lý / chờ',statuses:['planning','awaiting_approval','executing','reviewing','awaiting_acceptance']},
    {title:'Tạm dừng / cần xử lý',statuses:['paused','blocked','rework','failed']},
    {title:'Đã kết thúc',statuses:['accepted','cancelled']},
  ]
  const assigneeLabel=(id:string|null)=>id?assignees.find(value=>value.id===id)?.display_name??id.slice(0,8):'Chưa giao'
  return <div className="task-board">
    <div className="task-board-intro"><div><p className="eyebrow">OWNER TASK BOARD</p><h3>Work Order và trạng thái đã lưu</h3><p>Tạo task không gọi model. Budget request hiện khóa ở 0; task trong queue chưa có worker được bật để dispatch.</p></div><button className="quiet-button" type="button" onClick={onRefresh}>Tải lại bảng</button></div>
    <form className="task-create" onSubmit={submit}>
      <h3>Tạo Work Order</h3><p>Mọi task bắt đầu ở bản nháp. Chọn “Đưa vào queue” riêng để ghi hàng đợi bền vững.</p>
      <label htmlFor="task-goal">Mục tiêu</label><textarea id="task-goal" value={goal} onChange={event=>setGoal(event.target.value)} required minLength={1} maxLength={8000} rows={3} disabled={createPending||!!pendingPayload} />
      <div className="task-form-grid"><label htmlFor="task-outputs">Đầu ra mong đợi · mỗi dòng một mục<textarea id="task-outputs" value={outputs} onChange={event=>setOutputs(event.target.value)} required rows={3} disabled={createPending||!!pendingPayload} /></label><label htmlFor="task-criteria">Tiêu chí nghiệm thu<textarea id="task-criteria" value={criteria} onChange={event=>setCriteria(event.target.value)} required rows={3} disabled={createPending||!!pendingPayload} /></label><label htmlFor="task-refs">Reference đầu vào đã cấp · mỗi dòng một ref<input id="task-refs" value={refs} onChange={event=>setRefs(event.target.value)} required maxLength={4000} disabled={createPending||!!pendingPayload} /></label><label htmlFor="task-duration">Thời hạn tối đa · giây<input id="task-duration" type="number" min="1" max="86400" value={duration} onChange={event=>setDuration(event.target.value)} required disabled={createPending||!!pendingPayload} /></label><label htmlFor="task-rework-limit">Số vòng rework tối đa<input id="task-rework-limit" type="number" min="0" max="5" value={reworkLimit} onChange={event=>setReworkLimit(event.target.value)} required disabled={createPending||!!pendingPayload} /></label><label htmlFor="task-assignee">Người nhận việc<select id="task-assignee" value={assignee} onChange={event=>setAssignee(event.target.value)} disabled={createPending||!!pendingPayload}><option value="">Chưa giao</option>{assignees.map(person=><option value={person.id} key={person.id}>{person.display_name??person.id.slice(0,8)} · {person.role??person.lifecycle}</option>)}</select></label><label htmlFor="task-reviewer">Người rà soát<select id="task-reviewer" value={reviewer} onChange={event=>setReviewer(event.target.value)} disabled={createPending||!!pendingPayload}><option value="">Chưa chọn</option>{assignees.map(person=><option value={person.id} key={person.id}>{person.display_name??person.id.slice(0,8)} · {person.role??person.lifecycle}</option>)}</select></label></div>
      <p className="task-no-inference">Inference grant: 0 · Model requests: 0 · Cost basis: chưa biết. Chọn người nhận chỉ lưu assignment; không tự chạy worker.</p>
      <button className="primary-button" type="submit" disabled={createPending}>{createPending?'Đang ghi…':pendingPayload?'Gửi lại cùng Work Order':'Tạo bản nháp'}</button>
      {pendingPayload&&<small role="status">Phản hồi lần trước chưa rõ. Form được giữ nguyên để gửi lại cùng Idempotency-Key.</small>}
    </form>
    <div className="task-board-filters"><label htmlFor="task-filter">Lọc trạng thái<select id="task-filter" value={filter} onChange={event=>setFilter(event.target.value)}><option value="all">Tất cả</option>{Object.entries(taskLabel).map(([key,label])=><option key={key} value={key}>{label}</option>)}</select></label><label htmlFor="task-search">Tìm mục tiêu<input id="task-search" value={query} onChange={event=>setQuery(event.target.value)} maxLength={120} /></label><label htmlFor="queue-priority">Ưu tiên khi đưa vào queue<input id="queue-priority" type="number" min="-100" max="100" value={priority} onChange={event=>setPriority(event.target.value)} /></label><span>{visible.length} / {tasks.length} task</span></div>
    <div className="task-lanes">{groups.map(group=>{const rows=visible.filter(task=>group.statuses.includes(task.status));return <section className="task-lane" key={group.title}><h4>{group.title}<span>{rows.length}</span></h4>{rows.length?rows.map(task=><TaskCard key={task.task_id} task={task} assignee={assigneeLabel(task.assignee_id)} priority={Number(priority)} reason={reworkReason[task.task_id]??''} onReason={value=>setReworkReason(prev=>({...prev,[task.task_id]:value}))} onAction={onAction}/>):<p>Không có task</p>}</section>})}</div>
  </div>
}

function TaskCard({task,assignee,priority,reason,onReason,onAction}:{task:WorkOrder;assignee:string;priority:number;reason:string;onReason:(value:string)=>void;onAction:(task:WorkOrder,action:TaskActionName,priority?:number,reason?:string)=>Promise<boolean>}) {
  const outputs = Array.isArray(task.expected_outputs) ? task.expected_outputs : []
  const criteria = Array.isArray(task.acceptance_criteria) ? task.acceptance_criteria : []
  const inputRefs = Array.isArray(task.scope?.input_refs) ? task.scope.input_refs : []
  return <article className="task-card"><div className="task-card-top"><span className={`task-state state-${task.status}`}>{taskLabel[task.status]??task.status}</span><span className="task-revision">r{task.revision} · v{task.transition_version}</span></div><h5>{task.goal}</h5><p>{assignee}{task.reviewer_id?' · Có người rà soát':' · Chưa chọn người rà soát'}</p><div className="task-card-meta"><span>Hạn: {time(task.deadline_at)}</span><span>Queue: {task.queue_status??'chưa enqueue'}{task.priority!==null?` · ưu tiên ${task.priority}`:''}</span><span>{task.run_count} run liên kết</span></div><details><summary>Đầu ra, tiêu chí và scope</summary><strong>Đầu ra</strong><ul>{outputs.map((value,index)=><li key={`${index}-${value}`}>{value}</li>)}</ul><strong>Tiêu chí</strong><ul>{criteria.map((item,index)=><li key={typeof item==='string'?`legacy-${index}`:item.id||`criterion-${index}`}>{typeof item==='string'?item:`${item.id} · ${item.description} · ${item.evidence_kind}`}</li>)}</ul><small>Input refs: {inputRefs.length ? inputRefs.join(', ') : 'Không có'} · Model request cap: {String(task.budget_limits?.max_model_requests??0)}</small></details><div className="task-actions">
    {task.status==='draft'&&<button className="quiet-button" type="button" onClick={()=>void onAction(task,'enqueue',priority)}>Đưa vào queue</button>}
    {task.status==='queued'&&<><button className="quiet-button" type="button" onClick={()=>void onAction(task,'pause')}>Tạm dừng</button><button className="quiet-button" type="button" onClick={()=>void onAction(task,'cancel')}>Hủy</button></>}
    {task.status==='paused'&&<><button className="quiet-button" type="button" onClick={()=>void onAction(task,'resume')}>Tiếp tục</button><button className="quiet-button" type="button" onClick={()=>void onAction(task,'cancel')}>Hủy</button></>}
    {task.status==='awaiting_acceptance'&&<><button className="primary-button" type="button" disabled={task.run_count===0} onClick={()=>void onAction(task,'accept')}>Chủ tịch nghiệm thu</button><input aria-label="Lý do yêu cầu rework" value={reason} maxLength={500} onChange={event=>onReason(event.target.value)} placeholder="Lý do rework"/><button className="quiet-button" type="button" disabled={!reason.trim()} onClick={()=>void onAction(task,'request_rework',0,reason)}>Yêu cầu rework</button></>}
  </div><small>Task hoàn tất hoặc có run không tự được nghiệm thu. Hủy chỉ khả dụng ở trạng thái chưa dispatch an toàn.</small></article>
}
