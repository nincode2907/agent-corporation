# C03 / P05-01 / P05-02 / P05-07 — UI runtime Phase 05

Ngày 14/10/2026, AI điều phối `/root` tương tác bằng Chrome/CUA tab 2087261635. Reviewer độc lập kiểm source/test ở cùng batch. Không đăng nhập Owner thật, không đọc `.env`, không gọi POST/session/inference.

## Môi trường

- Trước kiểm tra, web15500 connection refused; lsof xác nhận API15501, PostgreSQL15510 và gateway15600 đang hoạt động. Không thay đổi các process này.
- QA backend riêng15592: import nguyên app/source hiện tại, thay `get_settings` bằng Settings(_env_file=None) với DB giả ở15599 không listener và không có secret Owner/gateway. Readiness/demo unavailable là điều kiện fixture, không kết luận bug DB sản phẩm.
- Vite15500 dùng source apps/web và proxy/API QA15592. Gateway stub15590 chỉ phục vụ GET. Cổng thuộc block15500–15599 của project trong registry; xác minh listener trước start. Gateway15600 theo registry/source và GET health200.
- Script fixture và Vite config kèm batch; launch qua rtk: `env PYTHONPATH=apps/api/src uv run --project apps/api python <tmp>/fixture.py`; `node apps/web/node_modules/vite/bin/vite.js --config <tmp>/vite.config.mjs`. Các process gắn PTY có log. Lần đầu chưa có PYTHONPATH lỗi import, đã sửa launch; không sửa source.

## Quan sát thực

Mở `http://127.0.0.1:15500/#settings`: trang Cấu hình & sức khỏe, `Inference grant Chưa được cấp`; đoạn giải thích gateway chỉ gọi khi bấm probe, chưa chạy probe trong phiên. Nút Probe gateway có tên truy cập rõ. Không bấm đăng nhập/seed/reset/runtime.

Mỗi dòng sau là một lần bấm nút Probe gateway rồi đọc AX mới:

| Mode | HTTP/adapter | AX text hiển thị sau thao tác |
| --- | --- | --- |
| live | GET health/models tới gateway thật15600 | Gateway phản hồi; Health ok, Catalog ok; catalog chỉ để tham khảo, không xác nhận entitlement; 7 model IDs |
| auth | stub GET401 | Cần xác thực gateway; Gateway yêu cầu xác thực, kiểm tra secret reference phía backend; catalog cũ được bỏ |
| schema | stub GET200 payload sai | Contract/cấu hình cần kiểm tra; Phản hồi gateway không khớp contract health/models đã xác nhận |
| offline | target15599 không listener | Không kết nối được; Không kết nối được gateway local, kiểm tra dịch vụ mà không thay cấu hình dùng chung |
| rate | stub GET429 | Gateway đang giới hạn probe; thử lại thủ công sau |
| live recovery | GET health/models tới gateway thật15600 | Gateway phản hồi; Health/Catalog ok; 7 model IDs trở lại |

UI giữ nguyên màn hình/nút ở mọi nhánh, không crash; thông báo rõ cách khắc phục. Sau lỗi auth không còn liệt kê catalog cũ. Không có secret/token trong các thông báo.

`P05-ui-stub-requests.jsonl`: 8 GET cho auth/schema/rate, đúng hai GET mỗi click; offline không tới stub. Các request thực live không lưu raw payload nhạy cảm; gateway health trả `{ok:true,provider:codex,active_requests:0}`. Fixture không có handler POST.

Evidence này là RUNTIME-VERIFIED cho UI probe và HTTP adapter thật trong môi trường QA; các lỗi gateway là server fixture để kiểm tra error contract, không thay live inference proof hoặc CG01. Không có model call.
