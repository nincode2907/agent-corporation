# Remake Phase 01 — 20261009T092011+0700-r004-remake

## Thông tin vòng sửa

- Phase: 01
- Remake batch: 20261009T092011+0700-r004-remake
- Người/AI remake: /root
- Vòng: r004
- Report nguồn: [kiểm định độc lập r004](../../../tests/results/phase-01/20261009T091446+0700-r004-test/report.md)
- Bắt đầu / kết thúc: 2026-10-09 09:20:11 / 09:24:30 +07:00 (Asia/Ho_Chi_Minh)
- Phạm vi/quyền: Review lại Phase 01; chỉ sửa hướng dẫn setup frontend trong phase được giao
- Source trước/sau: Worktree bẩn, giữ nguyên phần thay đổi khác; diff README duy nhất là lệnh cài npm. [Manifest/hash](evidence/source-manifest.json)
- Inference: Không gọi; grant = 0
- Kết luận vòng sửa: Đã thay đổi và cần retest

## Mapping results → thay đổi

| Test ID / tag-result nguồn | Nguyên nhân | Thay đổi thực tế / file refs | Trạng thái xử lý | Test cần rerun |
| --- | --- | --- | --- | --- |
| P01-01 · need-change/fail ([report](../../../tests/results/phase-01/20261009T091446+0700-r004-test/report.md)) | `npm ci --prefix apps/web` làm npm 11 dùng lock context sai, fail `Missing: web@0.0.0 from lock file` | Đổi thành `npm --prefix apps/web ci`; exact command pass trên bản sao tạm cùng layout `apps/web` | changed | Clean-copy cài theo README; build; test Health API độc lập |
| C03 · need-change/blocked | Chưa chạy demo từ bản sao sạch với DB riêng và kiểm tra trạng thái UI khi DB dừng | Dựng bản sao API/web cùng PostgreSQL ephemeral; migration baseline sạch, UI settings báo DB chưa kết nối khi test DB dừng | changed | AI độc lập chạy lại demo sạch và DB-down UI |
| P01-02 · need-change/blocked | Runtime DB dùng chung không được dừng/fault; report r004 chưa chạy bản sao API+DB cô lập | Không đổi code health: đã kiểm live API/Vite copy cùng PostgreSQL batch riêng, stop đúng container đó và thấy live 200/readiness 503/UI lỗi | changed | AI độc lập tạo môi trường riêng và lặp outage check |
| P01-03 · need-change/blocked | DB dự án đang ở head 0003, không thể dùng làm DB mới | Chạy migration baseline trên PostgreSQL 18.6 ephemeral, không gắn named volume dự án; current đúng `20261008_0001`, upgrade lần hai không lỗi, schema chỉ có `alembic_version` | changed | AI độc lập tạo DB rỗng và lặp upgrade/idempotency/schema check |

## Chi tiết từng finding

### P01-01 — Lệnh cài frontend

- Expected/actual nguồn: README yêu cầu clean install từ root; đúng lệnh cũ fail trên npm 11.19.0. [Evidence nguồn](../../../tests/results/phase-01/20261009T091446+0700-r004-test/evidence/finding-p01-01.md)
- Nguyên nhân: Đặt `--prefix` sau `ci` khiến npm 11 giải quyết package/lock context khác với thư mục web.
- Trạng thái xử lý: changed
- Thay đổi: [README.md](../../../../../README.md) dùng `npm --prefix apps/web ci`.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Chạy chính xác `rtk proxy npm --prefix apps/web ci` trên bản sao tạm có đúng cấu trúc `<copy>/apps/web`; exit 0, 28 packages, không sửa node_modules của repo. [Lệnh](evidence/commands.md)
- Còn thiếu/blocker: Chờ AI test độc lập rerun clean-copy setup và build.
- Retest cần chạy: Tạo bản sao sạch, dùng đúng lệnh mới từ root, xác minh install/build thành công.

### P01-02 — DB down khi API chạy

- Expected/actual nguồn: Demo yêu cầu health liveness/readiness đúng khi DB dừng; batch r004 chỉ kiểm unit âm và runtime DB đang dùng, chưa thử outage.
- Nguyên nhân: Chưa có bằng chứng live DB-down trong batch r004.
- Trạng thái xử lý: changed
- Thay đổi: Không thay source health; kiểm chứng live bằng API/Vite copy và PostgreSQL disposable, chỉ stop container test.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Khi DB sẵn liveness/readiness 200; sau khi stop DB test liveness 200, readiness 503 đã lọc; browser báo PostgreSQL chưa kết nối.
- Còn thiếu/blocker: Không còn blocker môi trường; cần AI test khác lặp lại bằng chứng độc lập.
- Retest cần chạy: Tạo PostgreSQL test không dùng project volume, API/UI copy trỏ duy nhất vào DB đó; khi stop container, liveness 200, readiness 503 body đã lọc, UI báo unavailable; cleanup scoped.

### C03 — Demo sạch với DB down

- Expected/actual nguồn: Cần xác nhận đúng hướng dẫn trên môi trường sạch và nhìn trạng thái health khi DB dừng; r004 chỉ xác minh runtime hiện có. [Report nguồn](../../../tests/results/phase-01/20261009T091446+0700-r004-test/report.md)
- Nguyên nhân: Thiếu kiểm chứng từ copy sạch trong batch r004.
- Trạng thái xử lý: changed
- Thay đổi: Tạo API/web copy và PostgreSQL rỗng tách biệt; cài dependency, apply Phase01 baseline; khởi động API/Vite trên port ephemeral; kiểm UI khi DB test dừng. [Evidence](evidence/phase01-isolated.md)
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: UI/browser cho thấy API vẫn hoạt động, PostgreSQL chưa kết nối và readiness chưa đạt.
- Còn thiếu/blocker: Chờ AI test độc lập chạy lại clean demo, xác minh đúng các điều kiện P01-01..03.
- Retest cần chạy: Lặp toàn bộ luồng setup trên temporary copy cùng DB riêng, kiểm HTTP health và UI khi DB tắt; cleanup.

### P01-03 — Migration baseline

- Expected/actual nguồn: Upgrade DB sạch đến revision Phase 01 và lặp lại không lỗi; batch r004 chỉ đọc current của DB dự án ở `20261008_0003`.
- Nguyên nhân: Baseline migration chưa được chạy trong batch độc lập hiện tại.
- Trạng thái xử lý: changed
- Thay đổi: Không thay migration. Chạy upgrade trên container PostgreSQL rỗng, không named volume.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Upgrade baseline hai lần exit 0; current `20261008_0001`; public schema chỉ có `alembic_version`.
- Còn thiếu/blocker: Không còn blocker môi trường; cần AI test khác kiểm chứng lại.
- Retest cần chạy: DB test ephemeral không gắn project volume; upgrade tới `20261008_0001` hai lần; current đúng 0001; schema chỉ có `alembic_version`.

## Cleanup và bước tiếp theo

- Cleanup: Bản sao web/API `/tmp/ac-p01-r004-copy` đã xóa; container `ac-p01-r004-pg` chạy `--rm` đã dừng và tự xóa; API/Vite ephemeral được Ctrl-C đúng session. DB/runtime project vẫn chạy.
- Evidence: [Commands](evidence/commands.md), [isolated health/migration](evidence/phase01-isolated.md), [source manifest](evidence/source-manifest.json)
- Retest tiếp theo: r005, kiểm định độc lập sau remake.
- Blocker/giới hạn: Không còn blocker môi trường trong remediation; AI test độc lập cần xác minh lại P01-01…03.
- Sổ vòng: [README kết quả Phase 01](../../../tests/results/phase-01/README.md)
