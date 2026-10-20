# Agent Corporation — UI Fix 07: Employee-first Live Office

**Ngày:** 20/10/2026  
**Kết quả triển khai:** Hoàn tất trong phạm vi UI Fix 07  
**Phase 08 / IG08:** Vẫn Bị chặn; đây không phải nghiệm thu phase hoặc live runtime.

## Đã làm

- Live Office lấy danh sách employee/version/departments từ API Owner-scoped đang có. Ba nhân viên vẫn hiện khi chưa có Runtime Run; department lấy từ quan hệ thật.
- Mỗi card cho biết tên, role, EmployeeVersion, trạng thái/freshness, cấu hình Owner và lịch sử Run. Chỉ trạng thái Run khớp đúng EmployeeVersion hiện hành mới ảnh hưởng badge; Run version cũ vẫn được giữ trong lịch sử.
- Card mở form Runtime với cặp `employee_id` + `employee_version_id`. Deep link version cũ để trống lựa chọn, báo rõ version không còn khớp và không cho đi tiếp bằng cách tự chọn nhân viên/version khác.
- Card liên kết Inspector, Replay cùng một Run ID và reconciliation khi outcome unknown. Inspector/Replay cập nhật Run ID theo URL hash khi điều hướng.
- Runtime form chỉ enable Start khi đủ profile, EmployeeVersion, grant, CG01 và các điều kiện backend; blocker hiển thị cụ thể. Không tự tạo grant.
- Thêm bố cục roster theo phòng ban, responsive card, focus ring bàn phím, reduced-motion support và chuyển trạng thái nhẹ. Không thêm Employee Chat, fake typing/thinking, 3D hoặc inference.

Không cần thay đổi API sản phẩm: `GET /api/v1/runtime/employees` và các endpoint Runtime/status hiện có đã cung cấp dữ liệu. `scripts/test_integration05_stack.py` chỉ được mở rộng để nhận fake worker tuỳ chọn cho stack disposable; `scripts/ui_fix07_fake_worker.py` là fake transport riêng của browser test.

## Ảnh trước/sau

Before từ Deployment 06:

- [Office desktop 1440×900](../deployment-06/evidence/screenshots/office-desktop-1440x900.png)
- [Office mobile 390×844](../deployment-06/evidence/screenshots/office-mobile-390x844.png)
- [Playground mobile capture cũ](../deployment-06/evidence/screenshots/playground-mobile-390x844.png)

After và state regression:

- [Roster desktop 1440×900](screenshots/office-roster-1440x900.png)
- [Roster mobile 390×844](screenshots/office-mobile-390x844.png)
- [Waiting model](screenshots/office-waiting-model-1440x900.png) · [completed + history](screenshots/office-completed-history-1440x900.png)
- [CG01/grant blocked](screenshots/runtime-blocked-1440x900.png) · [stale EmployeeVersion link](screenshots/runtime-stale-employee-version-link-1440x900.png)
- [SSE disconnected](screenshots/office-sse-disconnected-1440x900.png) · [unknown/reconciliation](screenshots/runtime-unknown-reconciliation-1440x900.png)

## Kiểm chứng

- Browser Chrome trong disposable Compose stack: **29/29 assertions pass**, không page errors; 1440×900 và 390×844 không tràn ngang, keyboard focus nhìn thấy.
- Hai synthetic Runs dùng fake transport: Run đầu chờ rồi hoàn tất; Run thứ hai bị worker cô lập dừng và được đối chiếu thành unknown/interrupted. Tổng model-call rows lần lượt 1 và 2; đọc/navigate Inspector, Replay và Office không tăng counter.
- Không có inference/model request thật, grant thật, thay đổi CG01, demo reset hay writes vào DB dùng chung. Disposable Compose project/volume đã xóa; JSON ghi `cleanup: true`.
- API: `rtk uv run --project apps/api pytest apps/api/tests` — **217 passed, 38 skipped, 1 warning**.
- Web: `rtk npm run --prefix apps/web build` — TypeScript và Vite production build pass.
- `rtk git diff --check` pass.
- Browser/API/build commands, warnings và giới hạn: [Phase 08 r009 commands](../../tests/results/phase-08/20261020T100810+0700-r009-test/evidence/commands.md). Sanitized browser result: [ui-regression.json](evidence/ui-regression.json).

### Bất thường Deployment 06

Hai capture đã xác nhận screenshot Playground mobile cũ phù hợp với việc chụp trong lúc Owner session/data đang tải; khi route sẵn sàng, Playground xuất hiện và không overflow ở 390 px. Đây là bằng chứng về timing/conditional loading, không xác định chính xác frame cũ được chụp lúc nào. Xem [diagnosis](evidence/shared-ui-diagnosis.json), [immediate](evidence/screenshots/playground-mobile-immediate-390x844.png) và [ready](evidence/screenshots/playground-mobile-ready-390x844.png).

HTTP 401 của `GET /api/v1/owner/session` trước login là Owner gate. Ở browser regression lần này, HTTP 409 là negative POST không grant và `ERR_FAILED` là SSE abort có chủ đích; cả ba được phân biệt với page error. Không sửa UI để che các response này.

## Independent review

Reviewer độc lập xác nhận hai finding được đóng bằng source và browser evidence: (1) Run của EmployeeVersion cũ còn trong history nhưng không đánh dấu version hiện tại active; (2) stale deep link không tự thay EmployeeVersion. Reviewer xác nhận screenshots, 29/29 assertions, cleanup và hai fake dispatch. Review chỉ áp dụng cho synthetic UI behavior, không phải acceptance của runtime thật.

### Gemini

**NOT PERFORMED.** Không có kết nối Gemini CLI/API đã được cấp sẵn trong môi trường. Việc này không chặn implementation.

## Tình trạng và giới hạn

UI Fix 07 implementation và isolated verification đã hoàn tất. **Phase 08 vẫn Bị chặn**: IG08 yêu cầu live text-only Run được authorize; fake gate/transport không thể PASS gate. Các ca cross-company ACL/redaction, full Replay DB-before/after, kiểm tra đầy đủ summary source và live event correlation cũng chưa được batch này chứng minh. Xem [Phase 08 r009 report](../../tests/results/phase-08/20261020T100810+0700-r009-test/report.md) và [next actions](next-actions.md).

Không rebuild/restart shared containers, không commit/push.
