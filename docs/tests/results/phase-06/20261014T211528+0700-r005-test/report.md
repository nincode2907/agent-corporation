# Kiểm định Phase 06 — 20261014T211528+0700-r005-test

## Thông tin batch

- Phase: 06
- Vòng: r005
- Test batch: 20261014T211528+0700-r005-test
- Bắt đầu: 2026-10-14T21:15:28+07:00, Asia/Ho_Chi_Minh; kết thúc ghi tại source-manifest.
- AI kiểm định: `/root/cg01_demo_review`, agent khác với `/root` vừa triển khai. Chỉ test/review, không sửa product source.
- Quyền: chỉ thị Chủ tịch “tạm thời mở gateway để test, khi nào đến phase cuối thì khóa lại mở như hiện tại”; test ngoại lệ local demo CG01, dependency UI/config/docs/release checkpoint. Không phase mới, grant, inference, DB mutation, restart hoặc sửa gateway chung.
- Source: HEAD `3cb08c1259cd52ce7094313159e3b53fb2880481`, dirty worktree; [hash manifest](evidence/source-manifest.json).
- Môi trường: Windows, Python3.14.3/pytest9.0.2/FastAPI0.142.4; [commands/evidence](evidence/commands.md).
- Inference: không gọi; không tạo grant; không đọc/in secret hay real .env; fixture SQL không DB.
- Supersedes: [r004](../20261014T161904+0700-r004-test/report.md).
- Remake nguồn: Không có; kiểm định thay đổi ngoại lệ theo chỉ thị mới, không sửa history.
- Kết luận kỹ thuật: **chưa đủ bằng chứng**. Scope ngoại lệ: fixture/code/build đạt, không có lỗi implementation được xác nhận; chưa xác minh UI authenticated/live Windows.
- Quyết định Chủ tịch: cho phép ngoại lệ demo; chưa có nghiệm thu Phase06 hay grant inference batch.

## Mapping và phạm vi

| Tiêu chí hiện tại | Test IDs | Bắt buộc | Giới hạn |
| --- | --- | --- | --- |
| AC1: request thật hoàn tất; error/abort không success | P06-03, P06-04 | Có | Live call cần grant/môi trường riêng |
| AC2: sandbox/policy thực không thừa hưởng unrestricted | P06-01, P06-02, P06-08 | Có | Override không thay isolation proof |
| AC3: limits và usage/cost unknown trung thực | P06-05, P06-06, P06-07 | Có | Race/cancel/usage thật chưa chạy |
| Ngoại lệ có default strict, demo/loopback, Owner/CSRF/grant/limits/stop/tools-off | P06-09…P06-13 | Có trong thay đổi | Fixtures không inference |
| Snapshot gate và UI báo unverified | P06-14, P06-15 | Có trong thay đổi | Snapshot SQL/checkpoint fixture; UI live blocked |
| Toggle strict và checkpoint release Phase23 | P06-16 | Có trong thay đổi | Temporary fake env và settings fixture |
| RULES chung | C01…C08 | Có | Không dùng report cũ làm pass |

## Tổng hợp

| Tag | Số test |
| --- | ---: |
| clean | 13 |
| need-change | 11 |
| suggestion | 0 |

| Result | Số test |
| --- | ---: |
| pass | 13 |
| fail | 0 |
| blocked | 11 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

Mọi case bắt buộc, kết quả phản biện `none`. Điều kiện chung: Windows checkout, local fake fixture/transport/temp files, không real DB/model/secrets; lệnh/exit/output và test names tại [commands](evidence/commands.md), source hiện tại tại [manifest](evidence/source-manifest.json). `clean` chỉ khẳng định lớp kiểm chứng ghi trong từng dòng. Severity blocked là `major` cho khoảng trống bằng chứng, không phải bug đã xác nhận.

### C01 — Phạm vi/diff

- Nguồn/tiêu chí: RULES §5; git diff/status/hash
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: Đúng scope chỉ thị, giữ phase status
- Thực tế: CODE-VERIFIED: diff ngoại lệ Phase06 và release checkpoint, không mở phase; manifest
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: Không sửa product từ tester

### C02 — Dependency/quyết định

- Nguồn/tiêu chí: master-plan06/05/ADR/TDG
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: Có dependency/evidence đúng loại
- Thực tế: 05 chờ nghiệm thu;06 bị chặn; CG01 thật chưa đạt, ngoại lệ không nghiệm thu
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: Quyết định/evidence riêng

### C03 — Criteria/demo

- Nguồn/tiêu chí: checklist06 AC1–3
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: Live demo text/timeout/deny/stop
- Thực tế: Mapping đủ; demo thật chưa có grant/runtime Owner/gateway
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: Batch grant và live demo riêng

### C04 — Không tự thực thi

- Nguồn/tiêu chí: Tests status/worker; source worker/startup/UI
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: Bật flag/status không grant/dispatch nền
- Thực tế: Fixture status grants0; fake worker explicit; source không startup/health/page dispatch
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: Giữ explicit worker

### C05 — Scope/secrets

- Nguồn/tiêu chí: demo negative tests + auth source
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: Không other scope/endpoint/secret leak
- Thực tế: Fixture demo scope/LAN/credentials deny đạt; RLS/API cross-scope DB chưa rerun
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: Disposable DB integration, không secret thật

### C06 — Docs/bản nhìn

- Nguồn/tiêu chí: README/spec/master-plan/AGENTS/checklists; parent validator
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: Tài liệu/render/link/runtime tương ứng
- Thực tế: Override unverified/checkpoint rõ; parent render đạt nhưng validator blocked sibling gateway README thiếu; live UI chưa QA
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: Gateway checkout/runtime riêng; không fake baseline link

### C07 — Regression

- Nguồn/tiêu chí: focused pytest + web build
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: Regression affected tests/build đạt
- Thực tế: 48pass8POSIXskip; build exit0; không overclaim skipped strict proof
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: Không broaden unrelated tests

### C08 — Tái kiểm định

- Nguồn/tiêu chí: report IDs/tags/evidence/hash
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: Evidence source/lệnh/giới hạn đủ
- Thực tế: Manifest + commands + fixture tái chạy, IDs đầy đủ; không nâng official status
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: Giữ history immutable

### P06-01 — Grant trước dispatch

- Nguồn/tiêu chí: checklist06; grant unit negatives, fake API denied
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: Thiếu/expired/revoked/wrong phase,batch,model,effort,stop deny
- Thực tế: validate_grant negatives đạt; override route vẫn 409 missing grant; Owner401/extra422
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: Đây fixture deny, không live grant

### P06-02 — Isolation thật

- Nguồn/tiêu chí: spec CG01; TDG
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: Proof inference boundary thật
- Thực tế: Không proof; demo override verified=false; không kiểm canary thật
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: Qualification riêng; CG01 vẫn BLOCKED

### P06-03 — Turn thật

- Nguồn/tiêu chí: checklist06 AC1
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: Model/artifact/call mapping thật
- Thực tế: Không grant/inference; gateway offline theo parent; native Owner chưa xác minh
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: Supported Owner/gateway và grant riêng

### P06-04 — Error/timeout/unknown

- Nguồn/tiêu chí: parse_response/post_text/worker fixtures
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: Error/unknown không success, không retry
- Thực tế: 502/504unknown401failed429limited,302 không follow, cancel fake đóng socket; tests pass
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: Live timeout thuộc P06-03/P06-06

### P06-05 — Resource race

- Nguồn/tiêu chí: checklist06; validate_grant limits
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: Concurrent reserve/expiry0dispatch trái giới hạn
- Thực tế: Limit unit pass; atomic reserve DB race chưa chạy
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: Disposable concurrent test

### P06-06 — Stop/abort

- Nguồn/tiêu chí: fake stop test; CG01 cancellation
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: App stop và provider cancellation đúng trạng thái
- Thực tế: Fake in-flight unknown/no retry pass; cancellation provider thật chưa có evidence
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: Live cancellation theo grant

### P06-07 — Usage provenance

- Nguồn/tiêu chí: parse/late usage tests
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: Confirmed/unknown và mapping live
- Thực tế: Unit null/zero/malformed/cache/reasoning pass; live/ledger DB chưa kiểm
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: Live grant + ledger reconcile

### P06-08 — Snapshot/idle

- Nguồn/tiêu chí: service/worker trace; independent fixture
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: Bền vững profile/policy/history/checkpoint/idle
- Thực tế: SQL/checkpoint fixture giữ snapshot/tools-off; actual DB persistence + authenticated idle chưa kiểm
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: Disposable DB và live Owner UI

### P06-09 — Default/strict Windows

- Nguồn/tiêu chí: test_default + unsupported_platform
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: Flag absent false; proof thiếu/unsupported deny
- Thực tế: Fixture Settings(_env_file=None)false; strict allowed=false/verified=false; Windows không crash POSIX
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: Strict POSIX success chưa kiểm ở batch này

### P06-10 — Demo scope/URL

- Nguồn/tiêu chí: 3 scope và5 URL negatives
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: Chỉ exact demo scope/literalloopback HTTP
- Thực tế: Other company/environment/None deny; Dockerhost/LAN/https/path/credentials deny; positive demo unverified
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: Không nới Docker/LAN

### P06-11 — API/Owner/override

- Nguồn/tiêu chí: TestClient status/run tests
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: Owner bắt buộc; request body không override; no auto grant
- Thực tế: Anonymous401; authenticated fixture demo-test verified=false grants0; extra fields422; missing grant409
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: Không coi dependency override là live session

### P06-12 — CSRF/grant/stop/tools

- Nguồn/tiêu chí: Independent fixture + existing tests/source
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: Owner write Origin/CSRF; grant limits; stop/tools off
- Thực tế: 6 CSRF/boundary deny+6 GrantInput deny; stop test pass; payload tools[] choice none/max_turns1 unchanged
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: [Fixture](evidence/P06-12-fixture.py) không DB/network

### P06-13 — Worker/khóa lại

- Nguồn/tiêu chí: worker tests + independent fake execute
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: Same scoped gate trước reserve và trước network
- Thực tế: Other scope không reserve; relock giữa reserve/dispatch no execute; demo positive exactly1fakeexecutor
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: .env đổi cần stop/restart worker như README

### P06-14 — Gate snapshot

- Nguồn/tiêu chí: Independent service SQL/checkpoint fixture
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: cg01_at_creation retained unverified
- Thực tế: Captured runtime_runs policy JSON và before_dispatch checkpoint đúng demo state; tools=false
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: Không khẳng định persistence PostgreSQL; P06-08 blocked

### P06-15 — UI cảnh báo

- Nguồn/tiêu chí: RuntimePanel diff + build
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: UI Mở tạm cho demo/chưa xác minh; thật chạy đúng
- Thực tế: CODE-VERIFIED branch và build đúng; chưa render authenticated UI Windows, không screenshot
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: Browser Owner runtime hỗ trợ; không khởi động/reset scope

### P06-16 — Toggle/release

- Nguồn/tiêu chí: temp fake env/release_check tests; README/checklist23
- Bắt buộc: có
- Điều kiện/môi trường: fixture Windows local; không DB/model/secret thật.
- Bước/lệnh: xem evidence/commands.md; pytest/build/fixture exit 0 như ghi trong evidence.
- Kỳ vọng: Giữ values/ACL, reversible; release-check deny override/missing proof
- Thực tế: Fake CRLF secrets preserved, duplicates removed, mode same, strict toggled; fixture release_checkfalse ở cả2config
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json), [fixture](evidence/P06-12-fixture.py).
- Xử lý/đề xuất: Không bật .env trong tester; khóa/restart/release-check strict trước23

## Bypass attempts

| Bất biến | Thử bypass | Kết quả |
| --- | --- | --- |
| Ngoại lệ chỉ operator config | body override/company/cg01_approved | 422 trước service |
| Scope demo duy nhất | Other company/environment/None | Gate deny trước reserve |
| Literal loopback | LAN/Dockerhost/https/path/userinfo | Gate deny |
| Owner/grant | Anonymous/missing grant | 401/409; không dispatch |
| CSRF/boundary | Missing/wrongCSRF/missingOrigin/evilOrigin/Host/crosssite | 403 fixture |
| Limits vẫn giữ | requests0/11,concurrency2,timeout121,phase23 | GrantInput deny |
| Khóa trước dispatch | Config fixture đổi strict sau reserve | Fake execute không được gọi |
| Không giả verified/release | Override status/proof/release_check | verified=false; không proof; release_checkfalse |

## Gates và bàn giao

| Gate | Kết quả | Cases / evidence |
| --- | --- | --- |
| CG01 thật | BLOCKED | P06-02/03/06; không isolation/privacy/cancellation proof |
| Không IG riêng Phase06 | Không kết luận PASS cho phase | Live/race/DB/UI evidence còn blocked |
| Ngoại lệ local demo | Fixture/code checks PASS, live UI BLOCKED | P06-09…T08; owner authorization không thay grant |
| Release23 checkpoint | Negative fixture PASS; release chưa được phép | P06-16; strict proof thật + workers restarted còn bắt buộc |

Must fix trong implementation ngoại lệ: không finding xác nhận. Các `need-change/blocked` là gap bằng chứng/dependency thật; không remake source chỉ để biến chúng thành pass. Full release HOLD vì CG01/live/dependency còn thiếu; đây không nghiệm thu V1. Lỗi Native Windows Owner POSIX tồn tại sẵn; không thuộc scope ngoại lệ này.

Cleanup: pytest temp files/sockets đóng; independent fixture TemporaryDirectory tự dọn; không DB/shared runtime thay đổi. Chỉ artifact report/fixture và web dist ignored. Không inference/secret/grant/realenv change bởi tester.

Bàn giao parent: có thể dùng ngoại lệ demo theo quyết định Chủ tịch, giữ Owner/grant/limits/stop/tools-off; parent bật local flag là bước riêng. Trước Phase23 phải strict, stop/restart workers và release-check thật đạt; gate exception không tự tắt khi đổi Markdown. Không tự chuyển phase.
