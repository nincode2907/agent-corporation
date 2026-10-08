# Remediation follow-up — Phase 01

Ngày: 2026-10-08 · Nguồn: [report kiểm định Phase 01](../tests/results/phase-01/20261008T154512+0700-phase01/report.md)

## Finding đã xử lý

Finding C02 ghi nhận README mô tả proxy hostname publish trên cả IPv4 và IPv6 loopback, trong khi listener đã xác minh chỉ publish trên IPv4 loopback. README đã được sửa để nói rõ hostname `agent-corporation.localhost` chỉ dùng IPv4 loopback và môi trường hiện tại không bind IPv6 loopback. Không thay đổi Dev Hub, proxy, port hoặc cấu hình toàn máy.

Các liên kết evidence mà report gốc tham chiếu (`commands.md`, `routes.md`, `finding-c02.md`, `source-manifest.json`) đều hiện diện. Report gốc được giữ nguyên như lịch sử; follow-up này không nâng kết quả các case chưa chạy.

## Còn thiếu kiểm chứng

- P01-01 fresh install: `not-run`; cần môi trường cài đặt sạch để chạy `npm ci`/`uv sync` độc lập, không đụng dependency runtime đang dùng.
- P01-03 migration từ database sạch: `blocked`; DB local hiện tại đang được các phase sau dùng. Chạy migration sạch cần PostgreSQL kiểm định riêng.

Các khoảng trống trên chưa được chạy lại trong follow-up này và không được coi là PASS.

## Kiểm chứng remediation

- Assertion trên nội dung README xác nhận câu cũ `IPv4/IPv6 loopback` không còn, và mô tả mới về IPv4-only có mặt.
- Không thay đổi bind/proxy; bằng chứng runtime cũ về IPv4 hoạt động và IPv6 không bind vẫn ở report gốc.

Kết quả: finding C02 đã sửa ở tài liệu; P01-01/P01-03 giữ nguyên trạng thái not-run/blocked.
