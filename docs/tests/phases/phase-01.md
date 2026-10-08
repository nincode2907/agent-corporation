# Kiểm định Phase 01 — Dựng nền phát triển local

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 01
- Dependency từ roadmap: 00
- Yêu cầu liên quan: REQ25, REQ26
- Gate: Không có gate IG riêng; vẫn kiểm criteria phase và C01–C08
- Contract hash: 4e1cc6cf0130c2c4b5d504e042d1cc5bafe78235301bcbec7cf99b85e3a68ca0

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- Tạo repo và cấu trúc frontend/backend sau khi được yêu cầu triển khai.
- Cấu hình React + TypeScript, FastAPI + Pydantic, PostgreSQL; Compose cho hạ tầng, codex-server hiện có chạy độc lập trên host, kết nối server-to-server.
- Đọc lại Dev Hub, reserve và kiểm tra port block; env mẫu, health check, migration baseline, lệnh vận hành.

### Demo bắt buộc

Khởi động từ hướng dẫn trên môi trường sạch; tắt database và xem health báo lỗi đúng.

### Giới hạn phase

Không triển khai production, không tự cài global/system service.

### Evidence bàn giao cần đối chiếu

Log khởi động, health responses, lệnh kiểm tra và registry diff.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | Lệnh cài/chạy/check hoạt động thực tế, không cần secret trong Git. | P01-01, P01-02, P01-03, P01-04 |
| AC2 | Service mapping khớp registry; toàn block đã kiểm tra trước khi reserve. | P01-05 |
| AC3 | URL loopback/proxy chỉ báo hoạt động sau kiểm tra HTTP IPv4/IPv6 và browser. | P01-06 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P01-01 | Cài và chạy local | Thực hiện README trên môi trường kiểm định được cấp, dùng pins/lockfiles | Web/API/PG chạy đúng stack và command; log nhìn được | Versions, install/start logs đã lọc | Spec §5/12 |
| P01-02 | Liveness/readiness | Gọi health với DB sẵn, chạy test_health.py; giả DB-down hoặc fault ở DB test riêng | Live tách ready; ready báo lỗi khi DB unavailable, không inference | HTTP statuses/bodies và pytest exit | Spec §5/12 |
| P01-03 | Migration baseline | Upgrade từ DB test sạch rồi kiểm current/schema | Baseline đúng và chạy lại không tạo trùng, không domain phase sau | Migration log/schema version | Spec §5/7 |
| P01-04 | Secret local | Kiểm .env ignore/mode 0600 và placeholders mẫu, không in giá trị | Không credential thật trong tracked files/log/UI | Metadata/ignore check đã lọc | Spec §10 |
| P01-05 | Registry và binds | Đối chiếu registry/block/listeners/compose/vite/API/proxy ở hiện trạng | Mapping khớp registry; mỗi bind theo capability đã được Chủ tịch xác nhận; trong môi trường hiện tại Caddy chỉ bind IPv4 loopback, không ingress LAN | Registry refs, listener/publication metadata; IPv6 không được kỳ vọng khi host từ chối bind | Spec §12; [AGENTS.md](../../../AGENTS.md) Runtime Phase 01 |
| P01-06 | URL đã xác minh | GET direct IPv4 và hostname/proxy, mở browser; ghi riêng IPv6 capability nếu host không hỗ trợ | Đúng app/response trên đường đã công bố; chỉ claim URL đã kiểm; không biến IPv6 bind không hỗ trợ thành route thành công | HTTP/browser evidence, IPv4/IPv6 listener facts | Spec §12; [AGENTS.md](../../../AGENTS.md) Runtime Phase 01 |
| P01-07 | Chưa có agent | Quan sát health/startup/landing và request spy | Không worker/inference/seed/công ty thật tự phát | Source và network/dispatch counts | Spec §2/10 |

## Lệnh và điều kiện chạy

Các lệnh đã tồn tại tại lúc soạn (từ root), chưa được chạy trong lượt tạo tài liệu này:

```sh
rtk proxy uv run --project apps/api pytest apps/api/tests/test_health.py
rtk proxy npm run --prefix apps/web build
rtk proxy uv run --project apps/api alembic -c apps/api/alembic.ini current
```

Phase 00 validator gọi renderer và có thể cập nhật HTML: kiểm diff/bản nhìn trước khi chạy. Pytest Phase 03 kết nối DB thật và tạo/xóa fixtures qua migration role: xác minh scope/cleanup từ source và chỉ chạy trên DB kiểm định được phép. Build/lint không thay proof runtime/UX. Migration `current` chỉ đọc version; `upgrade/downgrade`, restart và faults phải chuẩn bị môi trường riêng theo rule.

## Kết luận và lưu kết quả

Tạo `docs/tests/results/phase-01/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P01-01…P01-07 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Dừng tại Phase 01.
