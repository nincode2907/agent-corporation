# Kiểm định Phase 07 — 20261009T105531+0700-r001-test

## Thông tin batch

- Phase: 07
- Test batch: 20261009T105531+0700-r001-test
- Vòng: r001
- Bắt đầu / kết thúc: 2026-10-09T10:55:31+07:00 / 2026-10-09T10:57:01+07:00 · Asia/Ho_Chi_Minh
- Người/AI kiểm định: Codex preflight
- Độc lập với AI triển khai/remake: Chưa có implementation; preflight và đánh giá blocker trong cùng vai trò.
- Yêu cầu/phạm vi được giao: “implement phase 7”; kiểm dependency trước, chỉ Phase 07.
- Source: worktree dirty; giữ thay đổi có sẵn; hashes trong [manifest](evidence/source-manifest.json).
- Môi trường/config/tool versions: source review + API unit/ASGI tests; không dừng/restart service, không DB write.
- Inference: không gọi; grant = 0.
- Dependency/quyết định nghiệm thu: Phase 07 phụ thuộc Phase 06; Phase 06 Bị chặn ở Phase 05/CG01; xem [blocked-dependency](evidence/blocker.md).
- Supersedes: Không có; r001 đầu tiên.
- Remake nguồn: Không có.
- Kết luận kỹ thuật: chưa đủ bằng chứng
- Quyết định Chủ tịch: Chưa có nghiệm thu Phase 07.

## Mapping criteria

| Tiêu chí / nguồn | Test IDs | Bắt buộc | Ghi chú |
| --- | --- | --- | --- |
| AC1: durable event fetch, sequence, no duplicates after reconnect | P07-01…P07-03 | Có | Event SSE/UI chưa có; Owner session/scope chưa triển khai. |
| AC2: heartbeat/offline, waiting state, unknown outcome reconciliation | P07-04, P07-05 | Có | Chưa có worker/run runtime Phase 06 để phát heartbeat/outcome. |
| AC3: no duplicate call/tool after crash; recover context; show gaps | P07-05…P07-07 | Có | Phase 06/CG01 chưa đạt; grant = 0. |
| C01–C08 | C01–C08 | Có | Preflight/report/doc validation; không phải nghiệm thu feature. |

## Tổng hợp

| Tag | Số test |
| --- | ---: |
| clean | 7 |
| need-change | 8 |
| suggestion | 0 |

| Result | Số test |
| --- | ---: |
| pass | 7 |
| fail | 0 |
| blocked | 8 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Scope và worktree

- Nguồn/tiêu chí: Chỉ thị triển khai Phase 07; `AGENTS.md` và [manifest](evidence/source-manifest.json).
- Bắt buộc: có
- Điều kiện/môi trường: Shared dirty worktree.
- Bước/lệnh: `rtk proxy git status --short`; so danh sách thay đổi với scope.
- Kỳ vọng: Chỉ sửa Phase 07 và tài liệu trạng thái/bằng chứng tương ứng; không chạm runtime/gateway.
- Thực tế: Không sửa source sản phẩm; tạo preflight report/evidence và cập nhật Phase 07 blocker trong roadmap.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md)
- Xử lý/đề xuất: Không mở phase khác.

### C02 — Dependency và nguồn quyết định

- Nguồn/tiêu chí: [Master plan Phase 06–07](../../../../master-plan.md), [Phase 06 preflight](../../phase-06/20261008T170343+0700-r001-test/report.md), [ADR D03–D06](../../../../decisions/0001-v1-foundation.md).
- Bắt buộc: có
- Điều kiện/môi trường: Đọc trạng thái và evidence hiện có.
- Bước/lệnh: Xác minh Phase 07 phụ thuộc 06, Phase 06 status/gap, CG01 và grant.
- Kỳ vọng: Blocker được nhận diện trước khi code; không tự bỏ qua phụ thuộc hoặc thay gateway.
- Thực tế: Phase 06 Bị chặn; Phase 05 Chờ nghiệm thu/CG01 BLOCKED; grant=0. Phase 07 không thể kiểm thử run/crash lifecycle như đã yêu cầu.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: major
- Evidence: [blocker](evidence/blocker.md), [Phase 06 report](../../phase-06/20261008T170343+0700-r001-test/report.md)
- Xử lý/đề xuất: Phase 07 được ghi Bị chặn tới khi dependency/gate được xử lý.

### C03 — Criteria và demo

- Nguồn/tiêu chí: [Phase 07 AC](../../../../master-plan.md), [checklist](../../../phases/phase-07.md).
- Bắt buộc: có
- Điều kiện/môi trường: Không có execution worker/dispatcher Phase 06 hoặc Owner session cho SSE.
- Bước/lệnh: Map AC1–AC3 sang P07-01…07; kiểm router/runtime có thể demo không.
- Kỳ vọng: Task thật, event stream, reconnect và recovery đối chiếu event store.
- Thực tế: Không thể chạy demo; không có UI/API event stream hay run worker; dựng fixture/mock không chứng minh run thật và recovery contract.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [blocker](evidence/blocker.md), [Phase 07 checklist](../../../phases/phase-07.md)
- Xử lý/đề xuất: Tiếp tục khi dependency và quyền/identity cần thiết có sẵn.

### C04 — Không thực thi âm thầm

- Nguồn/tiêu chí: RULES §5 C04; [API main](../../../../../apps/api/src/agent_corporation_api/main.py).
- Bắt buộc: có
- Điều kiện/môi trường: Grant=0; source review.
- Bước/lệnh: Kiểm router registration và call sites.
- Kỳ vọng: Không gọi model/tool khi mở trang/health/preflight.
- Thực tế: API chỉ đăng ký health, demo và GET gateway probe; không có execution dispatcher hay SSE/event router; batch không gọi gateway/model.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json)
- Xử lý/đề xuất: Giữ default deny.

### C05 — Scope và dữ liệu nhạy cảm

- Nguồn/tiêu chí: RULES §5 C05; Spec §§9–10.
- Bắt buộc: có
- Điều kiện/môi trường: Source/docs only; không đọc `.env`, không tạo event hoặc request.
- Bước/lệnh: Review event scope and Owner-auth requirement; không truy vấn nội dung DB.
- Kỳ vọng: Không gửi input/secrets; không mở read route thiếu authorization.
- Thực tế: Không đọc/ghi DB hay secrets; phát hiện spec yêu cầu scope từ session nhưng chưa có session/auth route.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: major
- Evidence: [blocker](evidence/blocker.md), [manifest](evidence/source-manifest.json)
- Xử lý/đề xuất: Chưa public SSE cho tới khi session-to-scope authorization tồn tại.

### C06 — Markdown/HTML và trạng thái

- Nguồn/tiêu chí: Master plan canonical; `scripts/render_plan.py`.
- Bắt buộc: có
- Điều kiện/môi trường: Phase 07 status/log được cập nhật thành blocked, HTML render sau report.
- Bước/lệnh: Render và validate docs.
- Kỳ vọng: HTML phản ánh Markdown; không ghi Hoàn tất.
- Thực tế: Renderer/validator đã chạy sau khi report tạo; Phase 07 Bị chặn, không Hoàn tất.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [roadmap HTML](../../../../master-plan.html)
- Xử lý/đề xuất: Không.

### C07 — Regression liên quan

- Nguồn/tiêu chí: Health/gateway adapter Phase 05 boundary; không inference.
- Bắt buộc: có
- Điều kiện/môi trường: API ASGI/unit tests; không DB/runtime restart.
- Bước/lệnh: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_health.py apps/api/tests/test_codex_gateway.py -q`.
- Kỳ vọng: Health/probe contract regression pass, không gọi model.
- Thực tế: Exit 0; 9 passed in 0.48s. Đây là regression preflight, không chứng minh Phase 07.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md)
- Xử lý/đề xuất: Cần test Phase 07 mới sau khi dependency được gỡ.

### C08 — Tái kiểm định được

- Nguồn/tiêu chí: RULES §5 C08/§7.
- Bắt buộc: có
- Điều kiện/môi trường: Source hashes và links được lưu; không runtime fixtures.
- Bước/lệnh: Validate report/links/tags/manifests.
- Kỳ vọng: Đủ IDs/evidence/cleanup và blocker cụ thể.
- Thực tế: C01–C08, P07-01…07, blocker/evidence/commands/manifest được lưu; validator pass cấu trúc.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/source-manifest.json), [blocker](evidence/blocker.md), [commands](evidence/commands.md)
- Xử lý/đề xuất: Không.

### P07-01 — Lưu trước phát

- Nguồn/tiêu chí: Checklist P07-01; Spec §9.
- Bắt buộc: có
- Điều kiện/môi trường: Chưa có SSE/feed implementation; không có worker events.
- Bước/lệnh: Chưa thể inject transaction failure và quan sát emit vì chưa có subscriber route.
- Kỳ vọng: Chỉ phát event đã commit.
- Thực tế: Chưa chạy; phụ thuộc Phase 06 event producer và Phase 07 stream/auth implementation.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [blocker](evidence/blocker.md)
- Xử lý/đề xuất: Implement/test sau khi Owner scope + dependency có sẵn.

### P07-02 — Ordering/reconnect

- Nguồn/tiêu chí: Checklist P07-02; Spec §9.
- Bắt buộc: có
- Điều kiện/môi trường: Không có cursor endpoint hoặc SSE client.
- Bước/lệnh: Chưa thể disconnect/reconnect với after_seq/Last-Event-ID.
- Kỳ vọng: Không mất/nhân event; đúng stream_seq.
- Thực tế: Chưa chạy.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [blocker](evidence/blocker.md)
- Xử lý/đề xuất: Cần event API/subscriber implementation.

### P07-03 — Gap/cursor boundary

- Nguồn/tiêu chí: Checklist P07-03; Spec §9.
- Bắt buộc: có
- Điều kiện/môi trường: Chưa có cursor/session-scoped API.
- Bước/lệnh: Chưa thể kiểm invalid/expired/cross-scope cursor.
- Kỳ vọng: Báo gap/reset rõ; không lộ event ngoài scope.
- Thực tế: Chưa chạy; ID do caller gửi không thể thay Owner-authorized company scope.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: critical
- Evidence: [blocker](evidence/blocker.md)
- Xử lý/đề xuất: Chặn endpoint cho đến khi auth/session scope được cung cấp.

### P07-04 — Heartbeat/offline

- Nguồn/tiêu chí: Checklist P07-04; Spec §§3/9.
- Bắt buộc: có
- Điều kiện/môi trường: Chưa có runtime worker heartbeat/stream.
- Bước/lệnh: Chưa thể ngắt stream/heartbeat thực và kiểm trạng thái UI.
- Kỳ vọng: UI stale/offline dựa nguồn, không tiếp tục báo active.
- Thực tế: Chưa chạy.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [blocker](evidence/blocker.md)
- Xử lý/đề xuất: Dependency Phase 06 chưa cung cấp heartbeat/run producer.

### P07-05 — Crash và unknown outcome

- Nguồn/tiêu chí: Checklist P07-05; Spec §§8–9.
- Bắt buộc: có
- Điều kiện/môi trường: Không có worker/lease/dispatcher thực.
- Bước/lệnh: Không kill process hoặc tạo synthetic run trên app/shared runtime.
- Kỳ vọng: Reconcile lease/outcome; không retry model/tool unknown.
- Thực tế: Chưa thể chạy; Phase 06 agent runtime chưa triển khai.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: critical
- Evidence: [blocker](evidence/blocker.md)
- Xử lý/đề xuất: Cần Phase 06 worker/gate trước crash recovery proof.

### P07-06 — Session/context recovery

- Nguồn/tiêu chí: Checklist P07-06; Spec §§6/8.
- Bắt buộc: có
- Điều kiện/môi trường: Gateway chưa được gọi; CG01 BLOCKED; grant=0.
- Bước/lệnh: Không tạo session, POST hoặc model request.
- Kỳ vọng: Context app phục hồi từ checkpoint, không resume session mù.
- Thực tế: Chưa thể kiểm live; gateway session lifecycle thuộc request runtime Phase 06 và quyền privacy chưa đạt.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [blocker](evidence/blocker.md), [Phase 05 evidence](../../../../evidence/phase-05.md)
- Xử lý/đề xuất: CG01 + grant đúng batch/model/purpose/scope/limits/expiry bắt buộc cho live case.

### P07-07 — Run thật tới UI

- Nguồn/tiêu chí: Checklist P07-07; Spec §§6/9/10.
- Bắt buộc: có
- Điều kiện/môi trường: Phase 06 Bị chặn; inference grant=0.
- Bước/lệnh: Không gửi input tới codex-server hoặc model.
- Kỳ vọng: Run/event IDs/UI khớp; waiting không có token giả.
- Thực tế: Chưa chạy và không được phép chạy khi không có gate/grant.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [blocker](evidence/blocker.md)
- Xử lý/đề xuất: Không kế thừa grant phase/test batch khác; grant mới phải cấp riêng.

## Integration / release gates

Phase 07 không có IG riêng. Gate Phase 08 không được đánh giá trong phase này.

## Cleanup, giới hạn và bàn giao

- Cleanup: Không tạo rows/process/container; không đụng API/DB/gateway shared.
- Chưa kiểm chứng: P07-01…P07-07 blocked theo blocker và dependency.
- Cần sửa: Không có bug sản phẩm được xác nhận; cần gỡ prerequisite trước implementation.
- Bước tiếp theo: Chờ Phase 06/CG01 và Owner-authenticated scope; yêu cầu triển khai Phase 07 lại sau khi dependency được giải quyết.
- Bàn giao: [blocker](evidence/blocker.md), [evidence commands](evidence/commands.md), [manifest](evidence/source-manifest.json). Không nghiệm thu Phase 07.
