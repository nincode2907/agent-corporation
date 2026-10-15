import { useEffect, useRef, useState } from 'react'
import type { FormEvent } from 'react'
import './RuntimePanel.css'
import './PlaygroundPanel.css'

type Owner = { session_id: string; csrf_token: string }
type Employee = { id: string; profile: { display_name: string; role: string }; version: number }
type Profile = { version: number; model: string | null; reasoning_effort: string | null; fallback_models: string[] }
type Session = { id: string; created_at?: string; employee_snapshot: { display_name: string; role: string }; profile_snapshot: { version: number; model: string; reasoning_effort: string }; max_requests: number; used_requests: number; expires_at: string; revoked: boolean; timeout_seconds: number }
type Turn = { id: string; idempotency_key: string; input_text: string; output: string | null; status: string; outcome: string | null; stop_requested: boolean; usage: { prompt_tokens: number; completion_tokens: number; total_tokens: number } | null; usage_provenance: string; gateway_call_id: string | null; resolved_at: string | null; profile_snapshot: Session['profile_snapshot'] }
type Detail = { session: Session; turns: Turn[]; events: { event_id: string; event_type: string; stream_seq: number; recorded_at: string }[]; owner_session_active: boolean }
type Worker = { enabled: boolean; running: boolean; error: string | null }
const states: Record<string, string> = { queued: 'Đang xếp hàng', dispatched: 'Đang chờ AI', completed: 'Đã trả lời', failed: 'Không hoàn tất', cancelled: 'Đã dừng trước dispatch', unknown: 'Chưa xác định kết quả · không tự gửi lại' }
const reasons: Record<string, string> = {
  playground_grant_expired: 'Grant đã hết hạn. Bạn có thể chủ động tạo phiên có grant mới.',
  playground_limit_exceeded: 'Đã dùng hết số request được cấp.',
  playground_grant_revoked: 'Grant đã được kết thúc.',
  playground_owner_session_expired: 'Phiên Owner cấp grant đã hết hạn hoặc đăng xuất. Hãy đăng nhập và chủ động tạo grant mới.',
  playground_concurrency_or_unknown: 'Một lượt đang chạy hoặc còn kết quả chưa xác định. Hãy đối chiếu trước khi gửi tiếp.',
  playground_save_profile_first: 'Model profile đã đổi. Tải lại cấu hình rồi cấp grant.',
  playground_demo_only: 'Playground chỉ sử dụng được trong demo cố định.',
  idempotency_payload_mismatch: 'Mã gửi này đã gắn với nội dung khác. Hãy tải lại phiên để đối chiếu.',
}
class RequestError extends Error { status: number; constructor(status: number, message: string) { super(message); this.status = status } }

export default function PlaygroundPanel({ employees }: { employees: Employee[] }) {
  const [owner, setOwner] = useState<Owner | null>(null)
  const ownerRef = useRef(owner); ownerRef.current = owner
  const [checked, setChecked] = useState(false)
  const [secret, setSecret] = useState('')
  const [profile, setProfile] = useState<Profile | null>(null)
  const [model, setModel] = useState('')
  const [models, setModels] = useState<string[]>([])
  const [effort, setEffort] = useState('medium')
  const [employee, setEmployee] = useState(employees[0]?.id ?? '')
  useEffect(() => { if (!employee && employees.length) setEmployee(employees[0].id) }, [employee, employees])
  const [limit, setLimit] = useState(20)
  const [minutes, setMinutes] = useState(30)
  const [accepted, setAccepted] = useState(false)
  const [sessions, setSessions] = useState<Session[]>([])
  const [selected, setSelected] = useState('')
  const selectedRef = useRef(selected); selectedRef.current = selected
  const [detail, setDetail] = useState<Detail | null>(null)
  const [worker, setWorker] = useState<Worker | null>(null)
  const [creating, setCreating] = useState(false)
  const [draft, setDraft] = useState('')
  const [pending, setPending] = useState<{ key: string; input: string } | null>(null)
  const creation = useRef<{ key: string; payload: object } | null>(null)
  const [busy, setBusy] = useState(false)
  const busyRef = useRef(false)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')
  const [settled, setSettled] = useState(false)
  const [now, setNow] = useState(Date.now())
  const messagesEnd = useRef<HTMLDivElement>(null)

  async function api<T>(path: string, body?: unknown, method = 'POST'): Promise<T> {
    let response: Response
    try {
      response = await fetch(`/api/v1/${path}`, { credentials: 'same-origin', cache: 'no-store', signal: AbortSignal.timeout(10000), ...(body === undefined ? {} : { method, headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': ownerRef.current?.csrf_token ?? '' }, body: JSON.stringify(body) }) })
    } catch { throw new RequestError(0, 'Chưa xác nhận được thao tác. Tải lại phiên hoặc đối chiếu cùng mã gửi trước khi gửi nội dung khác.') }
    const data = await response.json()
    if (!response.ok) {
      if (response.status === 401) setOwner(null)
      const reason = typeof data.detail === 'string' ? data.detail : 'Dữ liệu không hợp lệ. Kiểm tra lại các trường.'
      throw new RequestError(response.status, reasons[reason] ?? reason)
    }
    return data as T
  }
  async function action(work: () => Promise<void>) {
    if (busyRef.current) return
    busyRef.current = true; setBusy(true); setError(''); setNotice('')
    try { await work() } catch (reason) { setError((reason as Error).message) }
    finally { busyRef.current = false; setBusy(false) }
  }
  async function load(id = selectedRef.current) {
    const data = await api<{ sessions: Session[]; worker: Worker }>('playground/sessions')
    setSessions(data.sessions); setWorker(data.worker)
    if (id) { const value = await api<Detail>(`playground/sessions/${id}`); if (selectedRef.current === id) setDetail(value) }
    return data.sessions
  }
  useEffect(() => {
    let active = true
    fetch('/api/v1/owner/session', { credentials: 'same-origin', cache: 'no-store' }).then(async response => {
      if (response.status === 401) return null
      if (!response.ok) throw new Error('Chưa đọc được phiên Owner. Kiểm tra API local.')
      return await response.json() as Owner
    }).then(value => { if (active) setOwner(value) }).catch(reason => { if (active) setError(reason.message) }).finally(() => { if (active) setChecked(true) })
    return () => { active = false }
  }, [])
  useEffect(() => {
    if (!owner) return
    let active = true
    void Promise.all([api<Profile>('owner/profile'), api<{ sessions: Session[]; worker: Worker }>('playground/sessions')]).then(([saved, data]) => {
      if (!active) return
      setProfile(saved); setModel(saved.model ?? ''); setEffort(saved.reasoning_effort ?? 'medium'); setSessions(data.sessions); setWorker(data.worker)
      if (data.sessions.length) setSelected(data.sessions[0].id)
      else setCreating(true)
    }).catch(reason => { if (active) setError(reason.message) })
    return () => { active = false }
    // All calls in this effect are read-only. No grant or model request on mount.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [owner])
  useEffect(() => {
    if (!owner || !selected) { setDetail(null); return }
    let active = true
    setDetail(null); setSettled(false)
    void api<Detail>(`playground/sessions/${selected}`).then(value => { if (active) setDetail(value) }).catch(reason => { if (active) setError(reason.message) })
    return () => { active = false }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selected, owner])
  const activeTurn = detail?.turns.find(turn => ['queued', 'dispatched'].includes(turn.status))
  const unknown = detail?.turns.find(turn => turn.status === 'unknown' && !turn.resolved_at)
  useEffect(() => {
    if (!owner || !selected || !activeTurn) return
    let reading = false, live = true
    const timer = window.setInterval(() => {
      if (reading) return
      reading = true
      void api<Detail>(`playground/sessions/${selected}`).then(value => { if (live) { setDetail(value); setError('') } }).catch(reason => { if (live) setError(reason.message) }).finally(() => { reading = false })
    }, 1000)
    return () => { live = false; window.clearInterval(timer) }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selected, owner, activeTurn?.id])
  useEffect(() => { const timer = window.setInterval(() => setNow(Date.now()), 1000); return () => window.clearInterval(timer) }, [])
  useEffect(() => { messagesEnd.current?.scrollIntoView({ block: 'nearest' }) }, [detail?.turns.length, activeTurn?.status])

  function login(event: FormEvent) { event.preventDefault(); void action(async () => {
    const demo = await api<{ environment: { id: string }; company: { id: string } }>('demo/dashboard')
    try { setOwner(await api<Owner>('owner/login', { secret, environment_id: demo.environment.id, company_id: demo.company.id })) } finally { setSecret('') }
  }) }
  function start(event: FormEvent) { event.preventDefault(); void action(async () => {
    if (!profile || !accepted) return
    let saved = profile
    if (model.trim() !== profile.model || effort !== profile.reasoning_effort) {
      saved = await api<Profile>('owner/profile', { model: model.trim(), reasoning_effort: effort, fallback_models: profile.fallback_models, expected_version: profile.version }, 'PUT')
      setProfile(saved)
    }
    const payload = { employee_id: employee, profile_version: saved.version, max_requests: limit, expires_in_minutes: minutes, timeout_seconds: 120, accept_demo_policy: true }
    if (!creation.current || JSON.stringify(creation.current.payload) !== JSON.stringify(payload)) creation.current = { key: crypto.randomUUID(), payload }
    const created = await api<Session>('playground/sessions', { ...payload, idempotency_key: creation.current.key })
    creation.current = null; setSelected(created.id); setCreating(false); setAccepted(false)
    await load(''); setNotice('Session Grant đã hoạt động. Bạn có thể gửi nhiều tin nhắn trong số lượt và thời hạn đã cấp.')
  }) }
  function send(event: FormEvent) { event.preventDefault(); void action(async () => {
    const message = pending ?? { key: crypto.randomUUID(), input: draft }
    setPending(message)
    try {
      await api(`playground/sessions/${selected}/messages`, { input_text: message.input, idempotency_key: message.key })
      setPending(null); setDraft(''); await load()
    } catch (reason) {
      if (reason instanceof RequestError && reason.status >= 400 && reason.status < 500) setPending(null)
      throw reason
    }
  }) }
  const session = detail?.session
  const remaining = session ? session.max_requests - session.used_requests : 0
  const expired = !!session && new Date(session.expires_at).getTime() <= now
  const canSend = !!session && !session.revoked && !expired && remaining > 0 && detail?.owner_session_active && !activeTurn && !unknown && !creating
  return <section className="runtime-panel playground" aria-label="Development Playground">
    <header className="runtime-heading"><div><h2>Trò chuyện thử với nhân viên demo</h2><p>Text-only · không tools, file, terminal, deploy hoặc đổi công ty. Quyền nằm trong Session Grant.</p></div>{owner && <button className="quiet-button" disabled={busy} onClick={() => { setCreating(true); setError(''); creation.current = null }}>Tạo phiên mới</button>}</header>
    {error && <p className="runtime-error" role="alert">{error}</p>}{notice && <p className="runtime-notice" role="status">{notice}</p>}
    {!checked ? <p role="status">Đang kiểm tra phiên Owner…</p> : !owner ? <form className="runtime-login" onSubmit={login}><label htmlFor="playground-secret">Secret Owner local</label><input id="playground-secret" type="password" autoComplete="off" value={secret} onChange={event => setSecret(event.target.value)} required maxLength={128} /><p>Đăng nhập một lần trên máy này. Secret chỉ dùng để đăng nhập.</p><button className="primary-button" disabled={busy || !secret}>Đăng nhập Owner</button></form> : <>
      <div className="playground-session-nav"><label htmlFor="playground-session">Hội thoại đã lưu</label><select id="playground-session" disabled={busy || !!pending} value={selected} onChange={event => { setSelected(event.target.value); setCreating(false); setDraft('') }}><option value="">Chọn phiên</option>{sessions.map(item => <option key={item.id} value={item.id}>{item.employee_snapshot.display_name} · {item.profile_snapshot.model} · {item.used_requests}/{item.max_requests} lượt · {new Date(item.created_at ?? item.expires_at).toLocaleString('vi-VN')}</option>)}</select><button className="quiet-button" disabled={busy} onClick={() => void action(async () => { await load() })}>Tải lại phiên</button></div>
      {creating && <form className="playground-setup" onSubmit={start}><h3>Cấp Session Grant</h3><div className="playground-fields"><label>Nhân viên demo<select required value={employee} onChange={event => setEmployee(event.target.value)}>{employees.map(item => <option value={item.id} key={item.id}>{item.profile.display_name} · {item.profile.role}</option>)}</select></label><label>Model<input required list="playground-models" value={model} onChange={event => setModel(event.target.value)} maxLength={100} /><datalist id="playground-models">{models.map(item => <option key={item} value={item} />)}</datalist></label><label>Reasoning effort<select value={effort} onChange={event => setEffort(event.target.value)}>{['minimal', 'low', 'medium', 'high', 'xhigh', 'max', 'ultra', 'persistent'].map(item => <option key={item}>{item}</option>)}</select></label><label>Số request tối đa<input required type="number" min={1} max={100} value={limit} onChange={event => setLimit(Number(event.target.value))} /></label><label>Thời hạn (phút)<input required type="number" min={1} max={240} value={minutes} onChange={event => setMinutes(Number(event.target.value))} /></label></div><button className="quiet-button" type="button" disabled={busy} onClick={() => void action(async () => { const catalog = await api<{ models: string[] }>('codex/probe'); setModels(catalog.models); setNotice('Đã tải catalog. Danh sách không xác nhận entitlement của tài khoản.') })}>Tải danh sách model</button><p>Concurrency 1 · timeout mỗi request 120 giây · không retry/fallback. Usage và chi phí thiếu nguồn sẽ hiện chưa biết. Nhân viên chỉ là persona demo, không mang theo quyền hay dữ liệu Work Order.</p><label className="playground-consent"><input type="checkbox" checked={accepted} onChange={event => setAccepted(event.target.checked)} required />Tôi chấp nhận ngoại lệ Development Playground v1, chỉ gửi dữ liệu demo không nhạy cảm. Isolation/privacy của gateway chưa được xác minh; đây không phải CG01 production verified.</label><div className="playground-actions"><button className="primary-button" disabled={busy || !profile || !accepted || !employee}>Cấp quyền và bắt đầu trò chuyện</button>{selected && <button className="quiet-button" type="button" onClick={() => setCreating(false)}>Quay lại hội thoại</button>}</div></form>}
      {!creating && session && detail && <>
        <div className="playground-grant"><div><strong>{session.employee_snapshot.display_name}</strong><span>{session.profile_snapshot.model} · {session.profile_snapshot.reasoning_effort} · profile v{session.profile_snapshot.version}</span></div><div><strong>{session.revoked ? 'Grant đã kết thúc' : expired ? 'Grant đã hết hạn' : `${remaining}/${session.max_requests} request còn lại`}</strong><span>Hết hạn {new Date(session.expires_at).toLocaleString('vi-VN')} · concurrency 1</span></div><button className="quiet-button" disabled={busy || session.revoked} onClick={() => void action(async () => { await api(`playground/sessions/${selected}/revoke`, {}); await load() })}>Kết thúc grant</button></div>
        <p className="playground-policy">Development Playground · dữ liệu demo · CG01 chưa verified. Worker {worker?.running ? 'đang được app quản lý' : 'chưa sẵn sàng'}{worker?.error ? ` · ${worker.error}` : ''}. Lịch sử gửi model gồm tối đa 10 lượt hoàn tất gần nhất.</p>
        <div className="playground-messages" role="log" aria-label="Tin nhắn Playground" aria-live="polite">{!detail.turns.length && <div className="playground-empty"><h3>Bắt đầu từ một câu hỏi</h3><p>Hỏi về một ý tưởng, nhờ phân tích một đoạn văn hoặc thử phản hồi của nhân viên demo.</p></div>}{detail.turns.map(turn => <article className="playground-turn" key={turn.id}><div className="playground-user"><strong>Bạn</strong><p>{turn.input_text}</p></div><div className="playground-assistant"><strong>{session.employee_snapshot.display_name}</strong><span className="playground-turn-state">{states[turn.status] ?? turn.status}{turn.stop_requested ? ' · đã yêu cầu dừng' : ''}</span>{turn.output && <p>{turn.output}</p>}{turn.status === 'failed' && <p>{turn.outcome}</p>}<small>{turn.usage ? `Usage xác nhận: ${turn.usage.total_tokens.toLocaleString('vi-VN')} tokens (${turn.usage.prompt_tokens} vào / ${turn.usage.completion_tokens} ra)` : 'Usage: chưa biết'} · Chi phí: chưa biết</small><details><summary>Dấu vết lượt gọi</summary><p>Turn {turn.id} · call {turn.gateway_call_id ?? 'chưa biết'} · profile v{turn.profile_snapshot.version} · nguồn usage {turn.usage_provenance}</p></details></div></article>)}<div ref={messagesEnd} /></div>
        {unknown && <div className="runtime-error"><p>Kết quả lượt trước chưa xác định. App không phát lại và vẫn giữ lượt request đã dùng. Chỉ tiếp tục sau khi bạn kiểm tra request bên gateway đã kết thúc.</p><label className="playground-consent"><input type="checkbox" checked={settled} onChange={event => setSettled(event.target.checked)} />Tôi đã kiểm tra request gateway đã kết thúc; giữ kết quả và usage chưa biết.</label><button className="quiet-button" disabled={busy || !settled} onClick={() => void action(async () => { await api(`playground/sessions/${selected}/unknown/${unknown.id}/resolve`, { gateway_settled: true }); setSettled(false); await load() })}>Ghi xác nhận và mở khóa lượt mới</button></div>}
        <form className="playground-composer" onSubmit={send}><label htmlFor="playground-message">Tin nhắn</label><textarea id="playground-message" rows={3} maxLength={8000} value={draft} disabled={!!pending} onChange={event => setDraft(event.target.value)} placeholder="Nhập nội dung demo không nhạy cảm…" required /><div className="playground-actions"><button className="primary-button" disabled={busy || !canSend || (!pending && !draft.trim())}>{pending ? 'Xác nhận lại cùng mã gửi' : activeTurn ? 'Đang chờ phản hồi…' : 'Gửi tin nhắn'}</button>{activeTurn && <button className="quiet-button" type="button" disabled={busy || activeTurn.stop_requested} onClick={() => void action(async () => { await api(`playground/sessions/${selected}/stop`, {}); await load() })}>Stop</button>}</div><small>{expired || remaining <= 0 || session.revoked ? 'Grant đã dừng nhận tin nhắn. Tạo phiên mới khi bạn muốn cấp hạn mức mới.' : !detail.owner_session_active ? 'Phiên Owner cấp grant đã hết hạn; hãy đăng nhập và cấp grant mới.' : 'Mỗi tin nhắn dùng tối đa một request; không xác nhận lại trong grant đang hoạt động.'}</small></form>
        <details className="playground-events"><summary>Events của phiên ({detail.events.length})</summary><ol>{detail.events.map(event => <li key={event.event_id}>#{event.stream_seq} · {event.event_type} · {new Date(event.recorded_at).toLocaleString('vi-VN')}</li>)}</ol></details>
      </>}
    </>}
  </section>
}
