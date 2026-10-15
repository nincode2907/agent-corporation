# Kiểm định Phase 06 — 20261014T231522+0700-r008-test

## Thông tin batch

- Phase: 06
- Vòng: r008
- Test batch: 20261014T231522+0700-r008-test
- Bắt đầu: `2026-10-14T23:15:22+07:00`, Asia/Ho_Chi_Minh.
- AI kiểm định: `/root/phase06_independent_review`, độc lập với `/root` remake.
- Yêu cầu: retest thay đổi Windows Owner ACL và UI cấp grant; kiểm tra auth/grant API permission paths, web build và runtime readiness.
- Revision: `3cb08c1259cd52ce7094313159e3b53fb2880481`, worktree dirty; [source manifest](evidence/source-manifest.json).
- Supersedes: [r007 test](../20261014T230943+0700-r007-test/report.md).
- Remake nguồn: [r007 remake](../../../../remakes/phase-06/20261014T231406+0700-r007-remake/remake.md).
- Quyền/giới hạn: không login, đọc Owner secret, tạo grant/runtime run, DB write/migration/seed hoặc inference. API tests dùng fake service; HTTP checks chỉ GET.
- Kết luận kỹ thuật: **chưa đủ bằng chứng**. Windows ACL/unit tests, grant route fixture và web build đạt; authenticated browser UI, grant persistence/live inference, CG01 isolation và DB persistence/race vẫn blocked.
- Quyết định Chủ tịch: **Phase 06 tiếp tục Bị chặn**; không cập nhật official status.

## Tổng hợp

| Tag | Số test |
| --- | ---: |
| clean | 12 |
| need-change | 13 |
| suggestion | 0 |

| Result | Số test |
| --- | ---: |
| pass | 12 |
| blocked | 13 |
| fail | 0 |
| not-run | 0 |

## Kết quả

Các test `clean` chỉ kết luận đúng lớp được chạy. Với test `need-change/blocked`, severity `major` là thiếu bằng chứng bắt buộc, không xác nhận lỗi implementation. Lệnh/exit code tại [commands](evidence/commands.md); read-only runtime observations tại [runtime checks](evidence/runtime-checks.md); file hashes tại [manifest](evidence/source-manifest.json).

### C01 — Phạm vi/diff

- Kỳ vọng: kiểm riêng remake Phase 06, không đổi status và không dispatch model.
- Thực tế: diff Windows ACL, grant UI và test liên quan được đọc; chỉ report/evidence, ledger và rendered roadmap được ghi. Không login/DB write/inference.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Không mở rộng sang phase khác.

### C02 — Dependency/quyết định

- Kỳ vọng: dependency/evidence và quyền phù hợp để nghiệm thu.
- Thực tế: master plan vẫn ghi Phase 06 Bị chặn; CG01 waiver áp dụng demo test, không tạo isolation proof hay inference grant. Phase 03/05 vẫn chờ nghiệm thu.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Giữ trạng thái; chờ evidence dependency và quyết định riêng cho live batch.

### C03 — Demo/criteria

- Kỳ vọng: run inference thật có artifact/trace, error/deny/stop evidence.
- Thực tế: không login hoặc gọi model. UI browser chưa xác thực; không có run/artifact/usage mới.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Owner phải đăng nhập thủ công; sau đó test theo profile/model và grant được chọn.

### C04 — Không thực thi âm thầm

- Kỳ vọng: mở UI/health/profile/grant không tự gọi inference.
- Thực tế: source tách rõ “Cấp grant” khỏi “Gửi một run”; API live status không xác thực trả 401; gateway health cho `active_requests=0`. Không có POST.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Giữ action grant và action run tách biệt.

### C05 — Scope/ACL/secrets

- Kỳ vọng: Owner secret có ACL riêng, boundary và dữ liệu DB đúng scope.
- Thực tế: Windows ACL test thực trên file fixture pass; bootstrap temporary directory/file ACL pass; auth boundary suite pass. Không kiểm populated DB RLS/cross-scope trong lượt này.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Chạy DB cross-scope test trên disposable isolated DB; không dùng runtime DB chung.

### C06 — Tài liệu/UI

- Kỳ vọng: UI grant/profile tương tác đúng trên browser Owner session.
- Thực tế: Vite/TypeScript build pass; không có browser login/session hoặc screenshot. Build không xác minh interaction.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Browser UI cần Owner đăng nhập thủ công để kiểm tra và lưu evidence.

### C07 — Regression liên quan

- Bước: Owner auth, Phase06 runtime, CG01 và gateway focused tests trên Windows; web build.
- Thực tế: **67 passed, 9 skipped**, 1 Starlette TestClient deprecation warning; web build exit 0. POSIX permission/symlink cases skip; Windows ACL case chạy.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Theo dõi warning TestClient; skip không được coi là pass.

### C08 — Tái kiểm định

- Thực tế: report/evidence có source hashes, links, output và giới hạn rõ; report có 25 test IDs, không lưu secret/session.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Sổ vòng được cập nhật r008.

### P06-01 — Grant trước dispatch

- Bước: unit grant negatives và API grant route fixture.
- Thực tế: missing Owner bị 401 trước service; body hợp lệ qua route fixture với limits của UI; các bounds sai trả 422 trước fake service. `service.grant_create` được thay bằng fake, không DB.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Kết luận route validation/auth fixture; persistence chưa được chứng minh.

### P06-02 — Isolation thật

- Thực tế: Chủ tịch miễn proof CG01 cho demo test; không có evidence inference isolation/privacy/cancellation. Windows không chạy POSIX strict-proof cases.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Không coi waiver hoặc fixture thay proof CG01.

### P06-03 — Một turn text-only thật

- Thực tế: không login UI, không tạo runtime grant/run và không POST gateway. Model/profile selection chưa được kiểm trên authenticated UI.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Owner chọn model/effort trong UI, cấp grant cho test batch, rồi mới chạy một turn riêng.

### P06-04 — Error/timeout/unknown

- Thực tế: fake gateway error/timeout/cancel tests chạy trong suite; live timeout/cancellation chưa thực hiện.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Chỉ kết luận behavior fake transport.

### P06-05 — Resource limits race

- Thực tế: unit limit negatives pass; không bật PostgreSQL persistence fixture vì fixture ghi vào DB đã cấu hình và chưa xác minh disposable DB riêng.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Chạy race trên disposable isolated PostgreSQL sau khi được chuẩn bị.

### P06-06 — Stop/abort

- Thực tế: fake worker stop/cancel pass; không có provider request live để chứng minh cancellation.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Live cancellation cần batch grant được cấp và quan sát được.

### P06-07 — Usage provenance

- Thực tế: parser/unit tests chạy; không có gateway response/ledger entry mới.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Đối chiếu live call ID và usage ledger sau test được cấp.

### P06-08 — Snapshot/idle

- Thực tế: không chạy test DB persistence; không đăng nhập UI để kiểm idle state/profile snapshot.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Dùng isolated DB fixture và Owner browser session.

### P06-09 — Default strict trên Windows

- Thực tế: CG01 suite chạy; strict/default assertion và Windows unsupported-proof behavior được kiểm bằng fixture. POSIX permission proof không chạy trên Windows.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Kết luận giới hạn trong các fixture Windows đã chạy.

### P06-10 — Demo scope/URL

- Thực tế: CG01 fake suite xác nhận scope/URL boundary; không đánh dấu verified và không nới phạm vi.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Giữ `verified=false` cho demo override.

### P06-11 — API/Owner/override

- Thực tế: Owner auth suite 67-pass tổng; unauthenticated runtime status live trả 401. Windows secret ACL acceptance và quyền ACL bị nới trên fixture đều được kiểm.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Live Owner login vẫn cần kiểm thủ công.

### P06-12 — CSRF/grant/stop/tools

- Thực tế: auth/runtime tests và grant route fixture pass ở lớp fixture; anonymous grant không tới service; tools không bật, không model call.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Grant persistence và live UI chưa được tính pass.

### P06-13 — Worker/relock

- Thực tế: CG01 fake worker scope/relock tests chạy và pass; không khởi động worker live.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Không suy ra live dispatch behavior ngoài fixture.

### P06-14 — Gate snapshot

- Thực tế: không chạy PostgreSQL runtime snapshot/checkpoint integration.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Persistence test cần isolated DB riêng.

### P06-15 — UI cảnh báo

- Thực tế: source/build xác nhận hiển thị demo unverified và action text; không có browser Owner session để kiểm trạng thái thật.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Xác minh UI sau Owner login thủ công; không dùng build làm thay evidence.

### P06-16 — Toggle/release

- Thực tế: CG01 release/toggle fixtures rerun và pass; không đổi `.env`, restart worker hoặc chạy release config thật.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Giữ strict release checkpoint ở Phase 23.

### P06-17 — UI cấp grant test một lượt

- Nguồn: r007 remake; thay đổi `RuntimePanel.tsx`.
- Kỳ vọng: grant UI dùng profile đã lưu, 1 request, concurrency 1, timeout 120s, no-retry, expiry 15 phút; cấp grant không dispatch.
- Thực tế: source inspection/build xác nhận payload và điều kiện; route contract fixture trả 201 với fake service và negative bounds 422. Không kiểm browser state, actual profile persistence, grant DB/audit persistence hoặc authenticated click.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Owner đăng nhập thủ công, kiểm UI/model/profile và grant persistence trên môi trường được phép; không gửi run khi chưa có chỉ thị/grant inference.

## Gates và bàn giao

| Gate | Kết quả | Bằng chứng |
| --- | --- | --- |
| CG01 thật | BLOCKED | Waiver chỉ cho demo test; chưa có isolation/privacy/cancellation proof; P06-02 |
| Grant UI/runtime DB | BLOCKED | Route fake fixture pass, nhưng không login hoặc ghi grant thật; P06-17 |
| Live model run | BLOCKED | Không Owner browser session/grant inference; P06-03 |
| Windows Owner ACL | PASS giới hạn test fixture | Windows ACL test và temporary bootstrap ACL fixture pass |
| DB persistence/race | BLOCKED | Opt-in integration không chạy để tránh DB writes; P06-05/08/14 |
| API readiness/build | PASS | Readiness 200; web build 0; không suy ra authenticated UI |

Không có lỗi implementation được xác nhận. Không có Owner login, runtime grant/run, DB mutation hoặc inference trong batch. Phase 06 tiếp tục Bị chặn; browser verification, persistence DB, isolation, live call/usage/abort và các dependency còn lại chưa có evidence.

