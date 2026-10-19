# Phase 08 — test batch r005

- **Batch:** `20261018T221600+0700-r005-test`
- **Thời gian:** 18/10/2026, Asia/Ho_Chi_Minh
- **Yêu cầu:** Stabilization Sprint 01; kiểm định Live Office, Inspector, Replay, responsive behavior và read-only boundary.
- **Vòng trước:** [r004](../20261015T073129+0700-r004-test/report.md)
- **Remake nguồn:** Không có. Đây là retest browser/source cho các màn đã có; không sửa API hay migration.
- **Revision:** `39321b177a60a20ecf327cfccaa9e6b865fe4db0`, `main`, worktree dirty; source manifest trong `evidence/source-manifest.json`.
- **Kết luận kỹ thuật:** **chưa đủ bằng chứng**. Inspector hiển thị run/event lịch sử và các trường thiếu nguồn một cách tường minh; UI overflow đã sửa và retest pass. ACL-negative, replay side-effect DB comparison, reload/gap và Live Office run thật chưa được thực hiện. **IG08: BLOCKED.**
- **Quyết định Chủ tịch:** Chưa có.

## Tóm tắt kết quả

| Nhóm | clean/pass | need-change/blocked | fail | Tổng |
| --- | ---: | ---: | ---: | ---: |
| C01–C08 | 5 | 3 | 0 | 8 |
| P08-01–P08-07 | 1 | 6 | 0 | 7 |
| **Tổng** | **6** | **9** | **0** | **15** |

## Ánh xạ acceptance criteria

| Criteria | Test | Kết quả |
| --- | --- | --- |
| AC1: Live Office/Inspector/Replay dựa trên dữ liệu run và event đã lưu | P08-01, P08-02, P08-06 | Các màn được chụp sau Owner auth; Inspector thấy một run cũ và 10 event liên quan. Live Office chưa có run đang hoạt động; cross-entry/reload/error state còn thiếu. |
| AC2: Replay chỉ đọc, không gọi tool/model hoặc thay state | P08-03, P08-04 | Mở route chỉ tạo GET; không có model/tool/write API trong browser log. DB before/after và cross-scope ACL actor test chưa chạy. |
| AC3: Summary rõ ràng, không giả dữ liệu/suy nghĩ thiếu nguồn | P08-05 | UI nói rõ chưa có summary, tools/file diff/messages/profile snapshot; usage/cost giữ đúng provenance/unknown. |

## Kiểm tra chung

### C01 — Phạm vi và diff

- **Kỳ vọng:** Chỉ Sprint 01; không mở Phase 11/Employee Chat; giữ nguyên các thay đổi ngoài phạm vi.
- **Thực tế:** Chỉ sửa UI/UX đã tái hiện, UI Lens config và tài liệu/evidence. Không thay runtime/API schema/DB/gateway. Các file untracked có trước sprint không bị xóa/ghi đè.
- Tag: `clean`
- Kết quả: `pass`
- Mức độ: `info`
- **Evidence:** `evidence/source-manifest.json`, [report sprint](../../../../reviews/stabilization-01/report.md).

### C02 — Dependency và phase boundary

- **Kỳ vọng:** Phase 08 phụ thuộc Phase 07; Inspector/Replay ảnh lịch sử không thay IG08.
- **Thực tế:** Phase 07 r006 tăng bằng chứng reconnect nhưng còn case blocked; Phase 06/CG01 và IG08 live run chưa được cấp. Run `100bc3c8…` là run Phase 06 cũ, không chứng minh Phase 08 grant/live integration.
- Tag: `need-change`
- Kết quả: `blocked`
- Mức độ: `major`
- **Evidence:** [master plan](../../../../master-plan.md), [checklist Phase 08](../../../phases/phase-08.md), [r004](../20261015T073129+0700-r004-test/report.md).

### C03 — Không thực thi âm thầm / replay boundary

- **Kỳ vọng:** Mở Office/Inspector/Replay không dispatch model/tool; Replay không ghi state.
- **Thực tế:** Browser request manifest chỉ có GET màn hình/event/runtime; POST chỉ login/logout. Không có gateway request, profile save, grant, message, run, decision hoặc task mutation. DB before/after và executor spy riêng chưa có.
- Tag: `clean`
- Kết quả: `pass` cho thao tác mở màn hình đã quan sát
- Mức độ: `info`
- **Evidence:** `evidence/authenticated/manifest.json`, `evidence/commands.md`.

### C04 — ACL/redaction

- **Kỳ vọng:** Cross-company/environment deny và nội dung nhạy cảm không lộ trong API/SSE/UI.
- **Thực tế:** Browser chạy đúng scope Owner hiện có; API test isolated cho session/scope/feed/redaction đạt. Không tạo actor/company thứ hai để browser negative test trong batch này.
- Tag: `need-change`
- Kết quả: `blocked`
- Mức độ: `major`
- **Evidence:** `evidence/commands.md`; tests `test_cursor_rejects_tamper_expiry_different_scope_and_session`, `test_event_envelope_omits_raw_context_and_confidential_payloads`.
- **Còn thiếu:** Populated cross-scope HTTP/SSE/Inspector negative test.

### C05 — API regression

- **Kỳ vọng:** API regression liên quan chạy trên DB tạm biệt lập.
- **Thực tế:** Full isolated suite **143 passed, 11 skipped, 1 warning**; migrations chạy trên DB tạm và runner xác nhận DB/role đã xóa.
- Tag: `clean`
- Kết quả: `pass`
- Mức độ: `info`
- **Evidence:** `evidence/commands.md`.

### C06 — Browser/build/responsive

- **Kỳ vọng:** Chụp màn cuối ở desktop 1440×900/mobile 390×844; không page overflow; kết quả build.
- **Thực tế:** UI Lens 18/18 target success; authenticated Playwright 18/18 screen/viewport có documentWidth bằng viewport. Inspector/Playground overflow trước sửa được retest hết; keyboard skip link chuyển focus vào `main`. Web build exit 0.
- Tag: `clean`
- Kết quả: `pass`
- Mức độ: `info`
- **Evidence:** [UI Lens manifest](../../../../../artifacts/ui-review/2026-10-18T15-28-04-437Z_c80b5d46-9af9-4eb2-8155-e3d97c33cd0d/manifest.json), `evidence/authenticated/manifest.json`, [browser audit](../../../../../reviews/stabilization-01/evidence/browser-audit-after.json).

### C07 — Replay evidence completeness

- **Kỳ vọng:** Compare selected-run event source/cursor before and after seek/reload; spy API/model/tool/write; compare DB state.
- **Thực tế:** Screenshot/source show read-only projection, explicit missing-summary/tool/profile copy, and known saved run. Browser navigation/reconnect request log shows GET only. No explicit seek/reload action or DB snapshot comparison.
- Tag: `need-change`
- Kết quả: `blocked`
- Mức độ: `major`
- **Evidence:** `evidence/authenticated/manifest.json`; screenshot paths linked in `ui-ux-review.md`.
- **Còn thiếu:** Replay mutation spy + DB before/after and reload/seek correlation.

### C08 — Reporting and status boundary

- **Kỳ vọng:** Evidence traceable; không tự PASS gate hay đổi trạng thái phase.
- **Thực tế:** 18 UI Lens captures, authenticated screenshots, Playwright manifest, commands and source hashes are linked. IG08 remains BLOCKED; master plan phase statuses unchanged.
- Tag: `clean`
- Kết quả: `pass`
- Mức độ: `info`
- **Evidence:** `evidence/source-manifest.json`, `evidence/commands.md`, [report sprint](../../../../reviews/stabilization-01/report.md).

## Ca Phase 08

### P08-01 — Live Office theo event

- **Nguồn:** Checklist P08-01 / Spec §3/9.
- **Kỳ vọng:** Active run text-only đã authorize; trạng thái phòng/agent từ events; fixture gắn nhãn.
- **Thực tế:** Authenticated Office hiển thị saved run/status theo source, fixture department có nhãn và không gán nhân viên khi thiếu quan hệ. Không có run Phase 08 mới/active được cấp.
- Tag: `need-change`
- Kết quả: `blocked`
- Mức độ: `major`
- **Evidence:** [Office desktop](../../../../reviews/stabilization-01/evidence/authenticated/screenshots/office/1440x900.png), [Office mobile](../../../../reviews/stabilization-01/evidence/authenticated/screenshots/office/390x844.png).
- **Còn thiếu:** Live authorized run và correlation run/event/UI.

### P08-02 — Inspector dùng chung

- **Nguồn:** Checklist P08-02 / Spec §3.
- **Kỳ vọng:** Dashboard/task/org mở cùng agent/run IDs; tabs/errors/profile/metrics thống nhất.
- **Thực tế:** Inspector authenticated đọc selected historical run, state/model/usage/outcome/10 related events. Cross-entry navigation từ dashboard, task và organization chưa test.
- Tag: `need-change`
- Kết quả: `blocked`
- Mức độ: `major`
- **Evidence:** [Inspector desktop](../../../../reviews/stabilization-01/evidence/authenticated/screenshots/inspector/1440x900.png), [Inspector mobile](../../../../reviews/stabilization-01/evidence/authenticated/screenshots/inspector/390x844.png).
- **Còn thiếu:** ID/source equality giữa các entry point; thêm ACL-redaction.

### P08-03 — Replay chỉ đọc

- **Nguồn:** Checklist P08-03 / Spec §9.
- **Kỳ vọng:** Cursor/filter/seek/reload chỉ đọc; model/tool calls = 0 và DB state không đổi.
- **Thực tế:** Replay route được capture authenticated; request log cho cả route/navigation không có write/model/tool request. Seek/reload/DB before-after chưa được chạy.
- Tag: `need-change`
- Kết quả: `blocked`
- Mức độ: `major`
- **Evidence:** [Replay desktop](../../../../reviews/stabilization-01/evidence/authenticated/screenshots/replay/1440x900.png), `evidence/authenticated/manifest.json`.
- **Còn thiếu:** Network spy + DB snapshot; test seek/reload với IDs/cursor cố định.

### P08-04 — ACL/redaction

- **Nguồn:** Checklist P08-04 / Spec §9/10.
- **Kỳ vọng:** Backend deny/filtered ở environment/company khác; secret/raw prompt không lộ.
- **Thực tế:** API feed/redaction unit/integration coverage chạy pass; không có browser cross-company actor hoặc canary secret ở UI trong batch.
- Tag: `need-change`
- Kết quả: `blocked`
- Mức độ: `major`
- **Evidence:** `evidence/commands.md`.
- **Còn thiếu:** Actor thứ hai + payload canary + HTTP/SSE/UI checks.

### P08-05 — Summary tường minh

- **Nguồn:** Checklist P08-05 / Spec §3/9.
- **Kỳ vọng:** Không hiển thị raw internal thought; thiếu nguồn được nói rõ.
- **Thực tế:** Inspector nói rõ chưa có summary/decision source, tools/file diff/messages chưa có nguồn cho run, profile snapshot không được projection cung cấp. UI chỉ hiện usage provenance đã lưu.
- Tag: `clean`
- Kết quả: `pass`
- Mức độ: `info`
- **Evidence:** [Inspector desktop](../../../../reviews/stabilization-01/evidence/authenticated/screenshots/inspector/1440x900.png), [source](../../../../../apps/web/src/RuntimePanel.tsx).

### P08-06 — Reload, usage và gap wording

- **Nguồn:** Checklist P08-06 / Spec §9/11.
- **Kỳ vọng:** Reload/reconnect không mất event; unknown usage/cost và gaps được biểu diễn chính xác.
- **Thực tế:** Historical run ghi confirmed gateway usage và cost basis unknown; P07 reconnect browser giữ 40 ordered IDs. Trong vòng Phase08 này chưa click Replay reload/seek hoặc inject gap state.
- Tag: `need-change`
- Kết quả: `blocked`
- Mức độ: `major`
- **Evidence:** `evidence/authenticated/manifest.json`, [Inspector screenshot](../../../../reviews/stabilization-01/evidence/authenticated/screenshots/inspector/1440x900.png), `evidence/browser-interruption.md`.
- **Còn thiếu:** Replay reload/seek và missing/unknown usage/gap UI case.

### P08-07 — IG08

- **Nguồn:** Checklist P08-07 / Spec §13.
- **Kỳ vọng:** Live text-only run → saved event/SSE → Office/Inspector/Replay; grant riêng nếu inference.
- **Thực tế:** Phase 06 historical run và fake/API/browser read-only tests không đủ thay Phase08 live proof; không cấp grant hoặc gọi inference trong sprint.
- Tag: `need-change`
- Kết quả: `blocked`
- Mức độ: `major`
- **Evidence:** [master plan](../../../../master-plan.md), `evidence/commands.md`.
- **Điều kiện tiếp tục:** Phase dependency, CG01 acceptance policy và IG08-specific authorization do Owner quyết định.

## Kết luận

Responsive overflow và missing focus target đã được sửa trong scope UI; authenticated screenshots cho thấy các màn quan trọng đều fit ở desktop/mobile. Inspector/Replay vẫn dựa trên run Phase 06 đã lưu. Checklist live Office, cross-entry/ACL, replay no-side-effect instrumentation và IG08 chưa hoàn tất; **Phase 08 giữ trạng thái Bị chặn**.
