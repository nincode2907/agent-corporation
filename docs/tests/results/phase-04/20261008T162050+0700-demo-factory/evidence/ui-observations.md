# UI observations — runtime verified

Browser mở `http://127.0.0.1:15500/#overview`, sau đó điều hướng qua #work, #approvals, #inspector, #finance bằng sidebar. Mọi route tải đúng heading.

- Overview: Demo Corporation, fixture v1, manifest prefix, “Không tạo agent thật, không gọi model”.
- Work: `WORK ORDER FIXTURE`, task IDs gắn usage chưa biết/no inference, trạng thái fixture.
- Approvals: một yêu cầu đang chờ, task DEMO fixture.
- Inspector: run mẫu trong scope demo; task/run có DEMO label.
- Finance: `BÁO CÁO FIXTURE`, `DEMO · UNKNOWN`, “Chưa biết”, thông báo không có usage thật/ledger; không hiển thị 0.
- Metadata DOM: `lang=vi`; favicon là SVG data URI; title `Agent Corporation · Tài chính`.
- Screenshot desktop được chụp/xem trực tiếp trong CUA. Công cụ trả ảnh trong phiên nhưng không lưu bytes thành file workspace; do checklist cần ảnh lưu làm evidence nên P04-05 vẫn blocked.
- Không bấm “Đặt lại demo”, không probe gateway, không thao tác mutation từ UI.
