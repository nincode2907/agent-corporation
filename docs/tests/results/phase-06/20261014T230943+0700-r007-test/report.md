# Kiểm định Phase 06 — 20261014T230943+0700-r007-test

## Thông tin batch

- Phase: 06
- Vòng: r007
- Test batch: 20261014T230943+0700-r007-test
- Bắt đầu: `2026-10-14T23:09:43+07:00`, Asia/Ho_Chi_Minh.
- AI kiểm định: `/root/phase06_independent_review`, độc lập với `/root` triển khai.
- Yêu cầu: retest Windows Owner ACL, Phase06 runtime/grant/stop, persistence suite, CG01 demo tests, API readiness/demo dashboard và web build khi phù hợp.
- Quyền/giới hạn: Chủ tịch miễn proof CG01 cho test demo; không cấp grant parameters. Không login automation, không secret read/print, không inference, không sửa source, không migration/seed, không DB writes.
- Revision: `3cb08c1259cd52ce7094313159e3b53fb2880481`, worktree dirty; hash manifest tại [source manifest](evidence/source-manifest.json).
- Môi trường: Windows PowerShell, PostgreSQL đã được parent migrate/seed trước batch. Test persistence opt-in không bật.
- Supersedes: [r006](../20261014T212618+0700-r006-test/report.md).
- Remake nguồn: Không có; batch này là independent retest implementation/runtime.
- Kết luận kỹ thuật: **chưa đủ bằng chứng**. Windows Owner/runtime fixtures và read-only readiness/demo dashboard đạt; live UI inference, isolation proof và persistence DB tests chưa được chứng minh.
- Quyết định Chủ tịch: **Chưa nghiệm thu Phase 06**; waiver CG01 chỉ dành cho demo test, không phải proof CG01 hay grant inference.

## Tổng hợp

| Tag | Số test |
| --- | ---: |
| clean | 12 |
| need-change | 12 |
| suggestion | 0 |

| Result | Số test |
| --- | ---: |
| pass | 12 |
| blocked | 12 |
| fail | 0 |
| not-run | 0 |

## Kết quả test

Mọi case là bắt buộc. Với `need-change/blocked`, severity `major` phản ánh thiếu proof bắt buộc, không khẳng định bug implementation. Test output, skip scope, runtime checks và source hashes được ghi trong [commands](evidence/commands.md), [runtime checks](evidence/runtime-checks.md) và [manifest](evidence/source-manifest.json).

### C01 — Scope/diff

- Bước: đối chiếu chỉ thị, changed files và diff runtime/UI/Auth; đọc source phục vụ test.
- Kỳ vọng: chỉ retest Phase 06, không đổi official status hoặc chạy inference.
- Thực tế: đúng scope; không sửa source hay DB. Worktree dirty do parent implementation và các artifacts trước đây.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Giữ nguyên scope; không inference.
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json).

### C02 — Dependency/quyết định

- Kỳ vọng: dependency/evidence phù hợp và có phê duyệt cần thiết.
- Thực tế: Phase 05 và Phase 03 vẫn chờ nghiệm thu; Phase 06 vẫn bị chặn theo master plan. CG01 waiver không phải proof; chưa có batch grant.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Chờ quyết định/evidence dependency và grant riêng.
- Cần tiếp tục: quyết định nghiệm thu dependencies/grant theo test batch riêng.

### C03 — Demo/criteria

- Kỳ vọng: live text turn, error/timeout, deny và stop có evidence đúng scope.
- Thực tế: demo dashboard fixture hiện đọc được; không có authenticated UI run, model result hoặc trace/artifact inference thật.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Owner UI thủ công và batch test được cấp.
- Cần tiếp tục: Chủ tịch xác thực Owner UI thủ công và chọn/cấp profile/model/grant phù hợp; sau đó chạy demo batch được cấp.

### C04 — Không thực thi âm thầm

- Bước: GET health và demo dashboard; chạy focused fake transport tests; không POST gateway.
- Kỳ vọng: mở trang/dashboard/health không gọi inference.
- Thực tế: dashboard báo `inference_requests=0`; Codex gateway `active_requests=0`; test không gửi model request.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Giữ health/read-only, không tự dispatch.
- Evidence: [runtime checks](evidence/runtime-checks.md), [commands](evidence/commands.md).

### C05 — Scope/ACL/secrets

- Kỳ vọng: Owner boundary, secret protection, data ACL và cross-scope được kiểm ở đúng lớp.
- Thực tế: Owner auth/ACL unit tests thuộc suite đạt; không đọc secret. Runtime DB RLS/populated cross-scope chưa chạy lại; Owner login thực tế chưa thử.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Chạy DB cross-scope test trong disposable DB và Owner browser.
- Cần tiếp tục: DB integration/cross-scope checks được cô lập và browser Owner session test thủ công.

### C06 — Docs/bản nhìn

- Kỳ vọng: tài liệu/UI render và browser interaction đúng.
- Thực tế: production web build pass, nhưng không kiểm browser đã xác thực hoặc chụp evidence UI. Build không thay thế UI QA.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Kiểm UI Owner thật và lưu browser evidence.
- Cần tiếp tục: kiểm UI Owner thật bằng browser và ghi screenshot/state phù hợp.

### C07 — Regression

- Bước: chạy auth/runtime/persistence-default-skip/CG01 suite trên Windows và web build.
- Kỳ vọng: changed paths/regression liên quan pass.
- Thực tế: `54 passed, 19 skipped`; web build exit `0`. Skip không tính pass; details trong [commands](evidence/commands.md).
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Theo dõi warning TestClient riêng.

### C08 — Tái kiểm định

- Kỳ vọng: report có IDs/tags, commands, runtime facts và source hashes.
- Thực tế: có report/evidence/manifest, không lưu secret hoặc full demo payload.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Giữ manifest và evidence nguyên trạng.

### P06-01 — Grant trước dispatch

- Bước: rerun unit/runtime deny matrix bằng fake service/transport.
- Kỳ vọng: thiếu/sai grant, batch/model/effort/expiry/stop bị từ chối trước dispatch.
- Thực tế: assertions trong focused suite đạt; không có request live.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Không gửi live request khi chưa có grant.

### P06-02 — Isolation thật

- Kỳ vọng: proof isolation/privacy/cancellation của inference environment.
- Thực tế: Chủ tịch miễn proof CG01 riêng cho demo test; test này không tạo isolation evidence. Windows strict POSIX filesystem cases skip.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: User waiver không thay proof isolation/privacy/cancellation.
- Ranh giới: waiver không đồng nghĩa CG01 verified và không được ghi P06-02 pass.

### P06-03 — Một turn text-only thật

- Kỳ vọng: model result/artifact thật, call/run mapping và usage provenance.
- Thực tế: chưa gửi inference. Owner UI yêu cầu đăng nhập thủ công; runtime status trả `401`. Model/profile selection/grant chưa sẵn có trong session được kiểm tra; không tự tạo grant.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Owner login/profile/model/grant cần được cấu hình thủ công.
- Cần tiếp tục: Owner đăng nhập thủ công, chọn profile/model và cấp grant có scope/limits/expiry cho batch test.

### P06-04 — Error/timeout/unknown

- Bước: fake transport/runtime error tests.
- Kỳ vọng: lỗi/timeout không success; unknown không auto-retry.
- Thực tế: unit/runtime failure-path tests đạt; live timeout chưa thử.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Chỉ kết luận fake failure path.
- Giới hạn: không khẳng định live provider cancellation/timeout.

### P06-05 — Resource limits race

- Kỳ vọng: DB reservation race và expiry không vượt hạn mức.
- Thực tế: unit limits chạy trong focused suite; persistence suite skip do opt-in PostgreSQL test fixture tắt, tránh DB writes.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Dùng disposable isolated PostgreSQL fixture khi được chuẩn bị.
- Cần tiếp tục: disposable isolated PostgreSQL test DB được chỉ định riêng rồi mới bật fixture.

### P06-06 — Stop/abort

- Kỳ vọng: live provider cancellation được xác minh; state unknown trung thực.
- Thực tế: fake stop/cancel paths trong runtime suite đạt; không có live model request.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Live cancel chỉ trong grant test có giới hạn.
- Cần tiếp tục: live cancellation test trong grant batch có hạn mức và quan sát được.

### P06-07 — Usage provenance

- Kỳ vọng: usage thật đối chiếu được với gateway call và ledger.
- Thực tế: fake parsing/regression tests thuộc suite đạt; không có gateway response/ledger entry mới.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Reconcile ledger sau live call được cấp.
- Cần tiếp tục: live call grant + ledger reconcile.

### P06-08 — Snapshot/idle

- Kỳ vọng: DB snapshot/checkpoint bền vững và authenticated idle không gọi model.
- Thực tế: API DB readiness và seeded demo dashboard GET pass, nhưng runtime persistence test file skip mặc định; không login UI. Dashboard hiển thị inference request count 0.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Chạy persistence trên isolated DB; không dùng shared runtime.
- Cần tiếp tục: test persistence trên disposable DB và idle state trong Owner browser session.

### P06-09 — Default strict trên Windows

- Thực tế: CG01 tests chạy; absent override defaults strict/unverified qua fixture. Strict proof trên Windows không được suy ra từ POSIX-only cases.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Kết luận chỉ cho default-mode assertion trên Windows.

### P06-10 — Demo scope/URL

- Thực tế: CG01 fake tests xác nhận exception bị ràng buộc scope/loopback và không đánh dấu verified; negative cases đạt.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Không tuyên bố CG01 verified.

### P06-11 — API/Owner/override

- Thực tế: Owner auth tests pass; live runtime status không có cookie trả `401`; không dùng API override để tự xác thực.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Owner browser login chưa kiểm.
- Giới hạn: không kiểm tra Owner login UI thật.

### P06-12 — CSRF/grant/stop/tools

- Thực tế: runtime/grant/stop fake tests pass; không gửi live request, tools không được kích hoạt.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Tools vẫn off, không gọi inference.

### P06-13 — Worker/relock

- Thực tế: demo worker gate/relock fake tests chạy và pass trong CG01 suite.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Chỉ kiểm fake worker path.

### P06-14 — Gate snapshot

- Kỳ vọng: persisted run snapshot/checkpoint trên DB.
- Thực tế: SQL persistence fixture không chạy do không bật isolated DB opt-in; không dùng fixture snapshot cũ làm pass mới.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Chạy persisted snapshot test trên isolated DB.

### P06-15 — UI cảnh báo

- Thực tế: TypeScript/Vite build pass. Không có authenticated browser session/screenshot; UI runtime state không được quan sát trực tiếp.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Owner login thủ công, lưu screenshot/state.
- Cần tiếp tục: Owner đăng nhập thủ công và kiểm nội dung/state trên UI.

### P06-16 — Toggle/release

- Thực tế: CG01 toggle/release CLI fake-config tests rerun trong suite và pass. Không thay đổi runtime `.env` hoặc khóa/restart worker trong tester batch.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Không sửa local runtime config trong tester batch.

## Gates và bàn giao

| Gate | Kết quả | Evidence |
| --- | --- | --- |
| CG01 thật | BLOCKED | User waiver chỉ cho demo; không có isolation/privacy/cancellation proof; P06-02 |
| Live model turn | BLOCKED | Chưa login Owner thủ công, chưa có profile/model/grant test batch; P06-03 |
| DB persistence/race | BLOCKED | Opt-in isolated PG suite không chạy để tránh DB writes; P06-05/08/14 |
| Read-only app runtime | PASS | API live/ready và demo dashboard GET 200; dashboard `inference_requests=0` |
| Regression/build | PASS giới hạn fixture/build | 54 passed,19 skipped; web build exit0 |

Không có finding implementation được xác nhận từ batch này. Không mở inference hoặc thay đổi phase status. Các test UI authenticated, live model, CG01 isolation, cancellation và isolated DB persistence vẫn phải có evidence riêng trước nghiệm thu.

