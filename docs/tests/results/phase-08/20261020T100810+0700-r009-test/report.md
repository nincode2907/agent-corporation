# Kiểm định Phase 08 — 20261020T100810+0700-r009-test

## Batch

- Phase: 08 · vòng r009.
- Test batch: `20261020T100810+0700-r009-test`
- Vòng: r009
- Kết luận kỹ thuật: **chưa đủ bằng chứng**
- Supersedes: [Phase 08 r008](../20261019T1132+0700-r008-test/report.md) cho phạm vi UI employee-first, định danh EmployeeVersion/Run và regression browser tổng hợp.
- Remake nguồn: Không có; đây là retest implementation UI Fix 07 trong cùng scope Phase 08.
- Thời gian bắt đầu browser regression: 20/10/2026 10:08:10 ICT (03:08:10 UTC).
- Source commit nền: `6c7f7bd09a4e6985d8ece72c2c9e6bde327ab081`; worktree có nhiều thay đổi staged/unstaged từ trước. File manifest ghi hash các file trực tiếp được kiểm định.
- Người kiểm định implementation: `/root`; independent source/evidence review: `/root/ui_fix07_independent`, recorded in [independent addendum](evidence/independent-addendum.md).
- Môi trường: Compose disposable riêng, PostgreSQL/volume riêng, Owner canary tổng hợp, browser Chrome; transport/gate fake chỉ trong harness; cổng test `127.0.0.1:15502` đã reserve/verify; stack và volume kiểm định đã cleanup.
- Quyền: không gọi gateway/model inference thật; chỉ 2 fake dispatch trong DB disposable cho 2 synthetic Run. Không tạo grant/Run trong DB dùng chung, không đổi CG01, không reset demo, không restart/deploy stack dùng chung.
- Gemini: **NOT PERFORMED** — không có Gemini CLI/API connection được xác nhận sẵn có.
- Kết luận kỹ thuật: **chưa đủ bằng chứng**. UI Fix 07 và browser checks đã pass trong môi trường tổng hợp; Phase 08/IG08 vẫn blocked vì chưa có live Run thật và các kiểm tra phase đầy đủ còn thiếu.
- Trạng thái phase: **Bị chặn**, không thay đổi; Chủ tịch nghiệm thu: **Chưa có**.
- Lệnh, phiên bản, output và giới hạn: [commands](evidence/commands.md). Hash manifest: [source-manifest.json](evidence/source-manifest.json).

## Tóm tắt kết quả

| Tag | Số ca | Kết quả |
|---|---:|---|
| `clean` | 6 | pass |
| `need-change` | 9 | blocked; chưa chứng minh tiêu chí live/đầy đủ, không phải lỗi sản phẩm đã xác nhận |
| `suggestion` | 0 | — |
| Fail | 0 | — |

## Mapping tiêu chí Phase 08

| Tiêu chí | Test IDs | Kết quả batch này |
|---|---|---|
| AC1 — UI dùng Run thật; fixture chỉ test UI có nhãn | P08-01, P08-02, P08-06, P08-07 | Synthetic UI checks pass; live Run/gate blocked. |
| AC2 — Replay chỉ đọc, không side effect | P08-03, P08-04 | UI navigation counter pass; full DB side-effect/cross-scope proof blocked. |
| AC3 — Summary rõ ràng, không lộ hidden reasoning | P08-05 | Source copy có giới hạn; payload comparison chưa chạy, blocked. |

## Integration gate

| Gate | Verdict | Test IDs | Bằng chứng/điều kiện còn thiếu |
|---|---|---|---|
| IG08 | **BLOCKED** | P08-01, P08-02, P08-07 | Browser fake transport chỉ chứng minh UI; cần Owner-approved live text-only Run/grant riêng, CG01 proof theo policy và saved event/UI correlation. Không inference được gọi trong batch này. |

Browser regression có 29 assertion pass, không có page error; model-call counter của DB tổng hợp là 1 sau Run thứ nhất, vẫn 1 sau Inspector/Replay/completion navigation, và 2 sau Run unknown thứ hai. Viewport 1440×900 và 390×844 không tràn ngang; keyboard focus hiển thị. Các HTTP 401 (Owner session trước login), 409 (negative POST không grant) và `ERR_FAILED` (SSE bị browser abort có chủ đích) được kỳ vọng, đã lọc; không được coi là page error.

## Kết quả từng ca

| ID | Kỳ vọng | Thực tế / evidence | Tag | Result | Mức độ / xử lý |
|---|---|---|---|---|---|
| C01 | Giữ đúng phạm vi UI Fix 07, không chuyển phase hay làm thay đổi ngoài quyền | Thay đổi thuộc Live Office/Runtime deep link, styling, isolated test harness và hồ sơ UI. Không sửa API sản phẩm, gateway, CG01, compose runtime đang dùng hay phase sau. Worktree nền vốn dirty; không stage/commit. | clean | pass | info · giữ nguyên các thay đổi có sẵn |
| C02 | Dependency và contract hiện hành khớp Phase 08/Phase 07 | Đã đọc master-plan, spec/ADR, checklist/rules Phase 08 và báo cáo Fix 05/05.1/Deployment 06. Phase 08 phụ thuộc 07; gate IG08 yêu cầu Run thật, fake UI test không đóng gate. | clean | pass | info · trạng thái Bị chặn giữ nguyên |
| C03 | Demo Phase 08 dùng Run thật đã được authorize | Browser tái hiện đúng UI bằng hai Run synthetic ở disposable stack. Điều kiện live Run và acceptance không được cấp, nên demo tổng hợp không đáp ứng AC Phase 08. | need-change | blocked | major · cần Owner authorization/grant riêng theo quy định IG08 |
| C04 | Mở màn hình/đọc/navigate không dispatch ngầm | DB disposable ghi 1 dispatch sau Run đầu; mở Office/Inspector/Replay và tải lịch sử vẫn 1; Run thứ hai đưa tổng lên đúng 2. Không có dispatch khi chỉ đọc/navigate. Evidence: `ui-regression.json`. | clean | pass | info · proof giới hạn trong fake transport/UI scope |
| C05 | Scope công ty/môi trường và dữ liệu nhạy cảm được kiểm tra | UI login dùng canary tổng hợp; negative POST thiếu grant bị từ chối và không tạo Run. Không chạy actor khác company/environment cho API/SSE/artifact và chưa kiểm đầy đủ redaction cross-scope. | need-change | blocked | major · cần kiểm thử authenticated scope-negative riêng |
| C06 | Tài liệu, trạng thái và UI tiếng Việt trung thực | Report ghi rõ dữ liệu synthetic/live, thiếu proof và phase không nghiệm thu; UI tiếng Việt. Master-plan sẽ được render lại từ Markdown sau khi ghi nhật ký r009. | clean | pass | info · giữ nguyên trạng thái roadmap |
| C07 | Regression/build liên quan đạt | `rtk uv run --project apps/api pytest apps/api/tests`: 217 passed, 38 skipped, 1 warning. `rtk npm run --prefix apps/web build`: TypeScript/Vite production build pass. Browser: 29 assertions pass. | clean | pass | info · một Starlette/httpx deprecation warning |
| C08 | Evidence tái kiểm định được và cleanup có scope | JSON assertions, screenshots, commands, source hashes; synthetic stack/volume được dọn, `cleanup: true`. Không có secret hoặc output inference thật trong artifact. | clean | pass | info · không stage/commit |
| P08-01 | Office status từ Run/event thật, không gán hoạt động giả | Synthetic waiting/completed và SSE-disconnect path pass; chỉ dữ liệu tổng hợp. Không có live Run được authorize để chứng minh Phase 08 event correlation. | need-change | blocked | major · live test cần grant/permission Phase 08 riêng |
| P08-02 | Inspector/Replay dùng cùng Run ID, profile/employee identity | Browser mở Inspector và Replay từ đúng card, giữ cùng `run_id`; Run lưu EmployeeVersion. Cross-entry từ dashboard/task/org và mọi tab/profile metrics chưa được kiểm đủ cho Phase 08. | need-change | blocked | major · bổ sung live/cross-entry checks trong đúng quyền |
| P08-03 | Replay filter/seek/reload chỉ đọc, không đổi DB | Điều hướng UI không tăng fake dispatch counter; nhưng batch này không chạy đủ filter/seek/reload và snapshot DB đa bảng trước/sau. | need-change | blocked | major · cần read-only DB comparison đầy đủ |
| P08-04 | ACL/redaction chặn cross-scope trên API/SSE/UI | Negative no-grant được kiểm; không thử actor company/environment khác hoặc các artifact-content paths. | need-change | blocked | major · cần scope-negative suite và redaction evidence |
| P08-05 | Summary là tường minh, không dựng suy nghĩ/nội dung thiếu | Source hiển thị ghi rõ thiếu decision summary/tool data; browser batch không kiểm đối chiếu đầy đủ summary với event payload trên Run thật. | need-change | blocked | major · cần source-to-event comparison |
| P08-06 | Offline/reconnect/gap/unknown usage hiển thị trung thực | Browser abort SSE: trạng thái không bị ghi thành idle; fake worker stop/recovery tạo interrupted/unknown và entry reconciliation; UI thể hiện unknown. Chưa kiểm đầy đủ gap/filter/reconnect và usage provenance trên live Run. | need-change | blocked | major · cần kiểm tra phase đầy đủ, không suy diễn giá/usage |
| P08-07 | IG08 live text-only Run → saved events → Office/Inspector/Replay | Chỉ có fake gate/transport ở disposable stack; không có gateway/model call thật, grant IG08, CG01 verification hay Owner acceptance. IG08 **BLOCKED**, không PASS. | need-change | blocked | major · chờ quyết định/grant Owner cho batch riêng |

## Test records for roadmap renderer

### C01 — Scope/diff
- Actual: UI Fix 07, isolated harness và evidence trong scope; không commit/stage hoặc chuyển phase.
- Result: pass; severity: info; tag: clean
- Follow-up: Không có.

### C02 — Dependency/contract
- Actual: Phase 07 dependency giữ nguyên; IG08 vẫn đòi Run thật.
- Result: pass; severity: info; tag: clean
- Follow-up: Không thay quyết định nghiệm thu.

### C03 — Demo và criteria
- Actual: Chỉ synthetic Run được chạy; live demo chưa được authorize.
- Result: blocked; severity: major; tag: need-change
- Follow-up: Cần Owner authorization/grant IG08 riêng.

### C04 — Không dispatch khi đọc
- Actual: Counter giữ 1 qua các trang đọc, tổng 2 sau synthetic Run thứ hai.
- Result: pass; severity: info; tag: clean
- Follow-up: Không có.

### C05 — Scope/redaction
- Actual: No-grant bị deny; actor khác company/environment và redaction chưa được kiểm.
- Result: blocked; severity: major; tag: need-change
- Follow-up: Cần authenticated cross-scope cases.

### C06 — Tài liệu và giao diện tiếng Việt
- Actual: Report/evidence ghi rõ synthetic/live; roadmap được render từ Markdown.
- Result: pass; severity: info; tag: clean
- Follow-up: Giữ phase Bị chặn.

### C07 — Regression/build
- Actual: API 217 passed/38 skipped; web build và 29 browser assertions pass.
- Result: pass; severity: info; tag: clean
- Follow-up: Một warning deprecation còn lại.

### C08 — Evidence/cleanup
- Actual: Browser JSON, screenshots, hash manifest; isolated cleanup true.
- Result: pass; severity: info; tag: clean
- Follow-up: Không có.

### P08-01 — Live Office event state
- Actual: Synthetic waiting/completed/disconnect pass; live Run chưa có.
- Result: blocked; severity: major; tag: need-change
- Follow-up: Cần live Run đã được authorize.

### P08-02 — Inspector identity/cross-entry
- Actual: Cùng Run ID từ Office vào Inspector/Replay; mọi cross-entry và tabs chưa đủ.
- Result: blocked; severity: major; tag: need-change
- Follow-up: Cần full Phase 08 scope/live checks.

### P08-03 — Replay side effects
- Actual: Read navigation không dispatch; DB snapshot đa bảng và đầy đủ filter/seek/reload chưa chạy trong batch này.
- Result: blocked; severity: major; tag: need-change
- Follow-up: Cần authenticated read-only DB comparison.

### P08-04 — ACL/redaction
- Actual: Thiếu actor cross-scope/API/SSE/artifact verification.
- Result: blocked; severity: major; tag: need-change
- Follow-up: Cần negative scope suite và redaction evidence.

### P08-05 — Explicit summary
- Actual: UI ghi rõ summary không có nguồn; không có source-to-live-event comparison trong batch.
- Result: blocked; severity: major; tag: need-change
- Follow-up: Đối chiếu payload/event khi có live Run.

### P08-06 — Reconnect/unknown usage
- Actual: SSE disconnect không hiện idle; synthetic unknown/reconciliation pass; gap và usage provenance chưa đủ.
- Result: blocked; severity: major; tag: need-change
- Follow-up: Cần hoàn tất các boundary của checklist Phase 08.

### P08-07 — IG08
- Actual: Fake transport không phải inference thật; không có grant hay gate evidence.
- Result: blocked; severity: major; tag: need-change
- Follow-up: Chờ Owner quyết định và grant IG08 riêng.

## Evidence UI Fix 07

- Before: [Deployment 06 Office desktop](../../../../reviews/deployment-06/evidence/screenshots/office-desktop-1440x900.png), [mobile](../../../../reviews/deployment-06/evidence/screenshots/office-mobile-390x844.png). Đây là baseline đã ghi trước UI Fix 07.
- After: [roster desktop 1440×900](../../../../reviews/ui-fix-07/screenshots/office-roster-1440x900.png), [mobile 390×844](../../../../reviews/ui-fix-07/screenshots/office-mobile-390x844.png), [waiting model](../../../../reviews/ui-fix-07/screenshots/office-waiting-model-1440x900.png), [completed history](../../../../reviews/ui-fix-07/screenshots/office-completed-history-1440x900.png), [stale EmployeeVersion link](../../../../reviews/ui-fix-07/screenshots/runtime-stale-employee-version-link-1440x900.png), [SSE disconnected](../../../../reviews/ui-fix-07/screenshots/office-sse-disconnected-1440x900.png), [unknown reconciliation](../../../../reviews/ui-fix-07/screenshots/runtime-unknown-reconciliation-1440x900.png).
- Browser result: [sanitized assertion record](../../../../reviews/ui-fix-07/evidence/ui-regression.json). Independent source/evidence review: both version-scoped status and stale-link safeguards closed; see [independent verdict](../../../../reviews/ui-fix-07/report.md#independent-review).

