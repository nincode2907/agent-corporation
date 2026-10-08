# Bằng chứng Phase 00 — Đặc tả V1

## Bổ sung sau Phase 03 — 08/10/2026

Phase 03 bổ sung `TASK_STATE_CHANGED` vào event catalog để biểu diễn execution-state transition được lưu cùng transaction. Đặc tả hiện có 31 event types; con số 30 ở các kết quả bên dưới là snapshot chính xác tại thời điểm Phase 00 được nghiệm thu, không bị viết lại lịch sử. Renderer/validator hiện kiểm tra catalog phiên bản hiện hành.

> Ngày: 08/10/2026 · Trạng thái: Hoàn tất về đặc tả/baseline sau review Chủ tịch (bản 1.1). Đây là evidence của tài liệu/spec, không là kết quả test runtime.

## Phạm vi và dependency

Phase 00 không có dependency. Chỉ triển khai đặc tả V1/ADR và đồng bộ HTML/master-plan. Phase 01–23 giữ nguyên; chưa scaffold, cài dependency, tạo migration, reserve port, start product server, tạo công ty thật, commit/push hoặc gọi inference. Gateway/Dev Hub không bị sửa. Grant inference hiện 0; candidate test grant là phương án chưa được cấp.

## Files bàn giao

- `docs/product-spec.md` + `docs/product-spec.html`: 17 mục, 14 màn hình, 26 requirements, 8 flows, 30 events, 8 release gates.
- `docs/decisions/0001-v1-foundation.md` + `.html`: D01–D08, rationale, ranh giới và hard gates; đã được Chủ tịch nghiệm thu, không cấp quyền inference/Phase 01.
- `docs/master-plan.md` + `.html`: Phase 00 Hoàn tất và links evidence; các phase khác giữ nguyên.
- `scripts/render_phase00.py`, `docs/assets/spec-template.html`: render spec/ADR và roadmap từ Markdown.
- `scripts/validate_phase00.py`: validation local của references/examples/phase scope; không inference.
- `scripts/render_plan.py`, `docs/assets/roadmap-template.html`: thêm link tài liệu theo phase.
- `README.md`, `AGENTS.md`: routing và lệnh render/validate tài liệu hiện có; AGENTS.md từ 34 thành 36 dòng.

## Quan sát gateway chỉ đọc — lịch sử bản 1.0

GET `http://127.0.0.1:4000/health` trả HTTP 200, `{"ok":true,"provider":"codex","active_requests":0}` trong lượt khảo sát này. Chỉ GET health; không POST chat/session, không truy secret/transcripts/native usage. Health không chứng minh model entitlement hay inference quality.

Source fingerprint (SHA-256), package version quan sát `0.1.0`:

| File codex-server | SHA-256 |
| --- | --- |
| src/schema.ts | 6ab2bc1217794dab4c59ce3bd41a3e81b20f15fd20fc5d7b0a35e418f1229916 |
| src/server.ts | f31d1cf1fa6ec2e913651522a95ce2776d3addf181595454474e1de41ed4dfbe |
| src/provider.ts | 99a84bd57ac97c5c60df2e839dd4eb937b3329b784f241bdeddeddc310b6d80e |

Đã đối chiếu `stream=false`, không `max_tokens`, function proposals, caller tool execution, final turn usage/call header, source rejects unexpected native tools và cancellation close handler. Chưa kiểm chứng behavior trên inference thật.

## Kết quả kiểm tra ban đầu — bản 1.0

Các lệnh đã chạy từ root (Python/Node sẵn có, không cài dependency):

```text
rtk proxy python3 scripts/render_phase00.py
rtk proxy python3 scripts/validate_phase00.py --baseline /tmp/agent-corporation-phase00-baseline.json
```

Output validation thực tế:

```text
PASS contract: 26 requirements/14 screens/8 flows/30 events/R1–R8; source/phase/decision/state refs và 2 JSON examples.
PASS scope: blocks Phase 01–23 và nguồn ý tưởng giữ nguyên; không scaffold sản phẩm.
PASS artifacts: 3 HTML đồng bộ/deterministic; links/anchors/IDs/lang=vi/favicon; JS syntax; không runtime/network client.
LIMIT: chưa chạy product tests/inference; chưa visual QA browser/mobile. Không suy Phase 00 đã được Chủ tịch nghiệm thu.
```

Baseline là SHA-256 của phase blocks và files trước thay đổi trong lượt này, lưu tạm ngoài repository để kiểm tra phạm vi, không là dependency của sản phẩm. Lệnh `rtk proxy python3 scripts/validate_phase00.py` chạy kiểm tra tài liệu không cần baseline; option baseline chỉ thêm kiểm tra phạm vi lần bàn giao. Checker không gửi HTTP, đọc secrets hay gọi model. Renderer không gọi runtime; node --check chỉ kiểm tra syntax, không thực thi UI trong trình duyệt.

Các checks đạt nghĩa là đặc tả có cấu trúc/references/examples và artifacts nhất quán. Chúng không chứng minh implementation đã đạt release gate. Lúc bàn giao bản 1.0, Chủ tịch nghiệm thu còn đang chờ; bản 1.1 đã được nghiệm thu sau review theo mục cập nhật dưới đây.

## Giới hạn và quyết định đang chờ

- O01 đã đóng: Chủ tịch nghiệm thu đặc tả/baseline sau bốn điều chỉnh review và validation đạt. Đây không là V1 runtime release, inference authorization hoặc yêu cầu bắt đầu Phase 01.
- O03–O07 là gates runtime/release cần kiểm chứng khi đến phase tương ứng, không claim đã đạt.
- Browser automation trước đó bị policy chặn navigation `file://`; không thử workaround/đổi proxy. Chưa xác minh render/mobile qua ảnh trình duyệt; validation HTML/link/syntax không thay thế visual QA.
- Đầu lượt khảo sát Git branch master với tài liệu untracked; `git diff --stat` ban đầu rỗng không có nghĩa không thay đổi. Cuối lượt Git status cho thấy files cũ modified và files Phase 00 mới untracked; agent không stage/commit, giữ các thay đổi Git bên ngoài. Baseline file hashes/phase blocks dùng để kiểm tra phạm vi; không stage/commit.

## Demo để Chủ tịch kiểm tra

Mở [đặc tả HTML](../product-spec.html), chọn 7 bước F01, đọc kiến trúc và mở các mục 7–11/14–16 để đối chiếu contracts/authority/traceability. Mở [Phase 00](../master-plan.html#phase-00) để xem phần mới, evidence và trạng thái. Mô phỏng chỉ thay nội dung tài liệu trên trang, không kết nối backend/model/tool.

## Cập nhật sau review Chủ tịch — bản 1.1

Bốn yêu cầu đã hoàn tất, không đổi stack/adapter hoặc D01–D08:

1. KPI cohort accepted_at tính chi phí trọn đời task/children/retry/rework/review xuyên kỳ không đếm trùng; period operating cost theo occurred_at tách riêng. Có ví dụ tháng 9 = 2 USD, tháng 10 = 3 USD, task accepted tháng 10 lifetime = 5 USD; late corrections/as_of/coverage và cost basis được quy định.
2. CG01 quy định capability/isolation/privacy fail → blocked + gap report cho Chủ tịch; mock không pass gate run thật; không tự nới/sửa/restart gateway shared, đổi adapter hoặc provision instance. Phương án tiếp theo cần quyết định riêng và grant mới.
3. IG03/08/12/16/20 có điểm chặn trước phase kế tiếp, integrated flow/evidence/grant/PASS–FAIL behavior; tất cả Chưa thực hiện. Release phải có evidence IG và R1–R8; PASS không tự cho phép phase tiếp.
4. Grant riêng cho phase_id/test_batch_id/mục đích/cases/model/scope/requests/concurrency/timeout/basis/expiry/Owner; kết thúc/fail/revoke/chuyển phase không còn quyền dispatch. Không chuyển dư hạn mức hoặc kế thừa giữa phase/batch. Usage muộn chỉ settle grant gốc.

Các kiểm tra sau sửa và sau cập nhật nghiệm thu đều đạt:

```text
rtk proxy python3 scripts/render_phase00.py
rtk proxy python3 scripts/validate_phase00.py --baseline /tmp/agent-corporation-phase00-review-baseline.json

PASS contract: 26 requirements/14 screens/8 flows/30 events/R1–R8; source/phase/decision/state refs và 2 JSON examples.
PASS scope: blocks Phase 01–23 và nguồn ý tưởng giữ nguyên; không scaffold sản phẩm.
PASS artifacts: 3 HTML đồng bộ/deterministic; links/anchors/IDs/lang=vi/favicon; JS syntax; không runtime/network client.
```

Kiểm tra bổ sung local của nội dung review đạt: bỏ công thức period numerator cũ; có cohort lifetime/period cost/late usage/dedup; CG01 deny và decision riêng; đúng một dòng cho mỗi IG trong spec/roadmap; batch grants không kế thừa. Baseline scope lấy ngay đầu lượt review; bảo toàn các thay đổi có trước.

Chủ tịch đã chỉ dẫn nghiệm thu có điều kiện sau khi sửa bốn điểm và kiểm tra nhất quán. Điều kiện đã được đáp ứng; Phase 00 Hoàn tất về đặc tả/baseline, ADR được nghiệm thu. Validator chỉ kiểm chứng tài liệu, không tự cấp thẩm quyền: quyết định nghiệm thu lấy từ lời nhắn Chủ tịch. Không nghiệm thu runtime gates bằng các checks này.

Trong lượt review chỉ cập nhật tài liệu/template/render metadata rồi chạy kiểm tra file local, không gửi HTTP, không gọi model, không cấp inference grant, không start product server hoặc Phase 01, không thay gateway/Dev Hub, không stage/commit/push. Grant hiện vẫn 0; Phase 01–23 Chưa triển khai. Hạn chế visual QA file:// từ lần trước vẫn giữ nguyên, không có kiểm tra browser/runtime mới.
