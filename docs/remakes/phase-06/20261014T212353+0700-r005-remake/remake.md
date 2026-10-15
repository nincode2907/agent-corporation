# Remake Phase 06 — 20261014T212353+0700-r005-remake

- Phase: 06; Vòng: r005; AI remake: `/root`.
- Bắt đầu: 2026-10-14T21:23:53+07:00, Asia/Saigon.
- Report nguồn: [r005](../../../tests/results/phase-06/20261014T211528+0700-r005-test/report.md).
- Phạm vi: ngoại lệ CG01 demo theo chỉ thị Chủ tịch; sửa console Windows sau kiểm định r005, không thay CG01 thật/grant/phase.
- Source trước/sau: [manifest](evidence/source-manifest.json); [commands](evidence/commands.md).

## P06-16 — Diagnostic release-check trên Windows

- Trạng thái: changed. Finding bổ sung do parent phát hiện khi kích hoạt local sau khi report r005 chốt; không ghi đè report cũ.
- Nguyên nhân: CLI in tiếng Việt vào stdout cp1252 của Windows dẫn tới UnicodeEncodeError; ValueError handler báo lỗi cấu hình dù cấu hình hợp lệ. Fixture r005 kiểm hàm release_check trực tiếp nên chưa đi qua console CLI.
- Sửa: `scripts/cg01_mode.py` đặt stdout/stderr UTF-8 trước parse/print. Thêm subprocess fixture có PYTHONIOENCODING=cp1252/PYTHONUTF8=0, fake settings và fake release check, không đọc .env thật; xác nhận diagnostic tiếng Việt và exit 1.
- Parent check: 17 tests trong test_cg01_demo_mode.py pass. CLI thực `release-check` sau sửa trả đúng `CG01 release: BLOCKED · Ngoại lệ demo còn bật…`, exit 1 như kỳ vọng. [Evidence](evidence/commands.md).
- Còn lại: cần agent test độc lập retest r006; full-phase live/isolation/DB/UI/Owner Windows blockers giữ nguyên, không tạo proof/grant/inference.

## Kích hoạt local đã được user cho phép

Đã bật key `.env` bằng script, xác minh chỉ metadata `allowed=true, mode=demo-test, verified=false`, và restart đúng API project được xác minh identity. [Evidence kích hoạt](evidence/runtime-activation.md). Không gọi worker/model hoặc đổi gateway/DB. Phase 23 vẫn phải khóa strict và kiểm proof thật; flag local không tự tắt khi sửa Markdown.
