# UI assertions — Phase 04

Nguồn: DOM snapshot trên tab local `http://127.0.0.1:15500/` qua browser CUA, 08/10/2026 (Asia/Ho_Chi_Minh). Snapshot đã được xem trực tiếp; không chứa dữ liệu người dùng hoặc credential.

- Banner toàn cục: `DEMO`, `Demo Corporation`, `Fixture v1 · usage chưa biết · inference 0` và nút `Đặt lại demo`.
- Overview: 3 hồ sơ nhân sự, 2 phòng ban, 5 Work Order, 20 event fixture.
- Chờ Chủ tịch duyệt: `1 yêu cầu đang chờ`, task `[DEMO] Mẫu công việc approval`, `waiting_approval`.
- Tài chính: `Usage và chi phí chưa biết`, badge `DEMO · UNKNOWN`, copy xác nhận không có ledger và không hiển thị số 0.
- Navigation đổi màn hình giữ nguyên banner; dữ liệu fixture có badge DEMO; onboarding thật vẫn khóa.
- Reset button mở confirm dialog trước POST. Backend chỉ nhận `{confirmed:true}`; negative route test bao phủ body thiếu/giả target.

Giới hạn evidence: ảnh đã hiển thị trong phiên kiểm tra browser nhưng không được lưu thành file. Do checklist P04-05 yêu cầu ảnh tái kiểm tra, case đó được gắn `need-change / blocked`; report không coi DOM assertions là thay thế cho ảnh bắt buộc.
