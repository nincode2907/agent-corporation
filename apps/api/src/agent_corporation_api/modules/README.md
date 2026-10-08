# Ranh giới module

Các package này chỉ đánh dấu nơi đặt domain code sau khi phase liên quan được giao. Chưa có model, API hay side effect domain trong Phase 01. Module chỉ sửa dữ liệu mình sở hữu qua service/command contract; schema/state/event bắt đầu ở Phase 03.

| Package | Lĩnh vực |
|---|---|
| `companies` | Công ty và môi trường |
| `organization` | Phòng ban, vai trò, hồ sơ nhân viên |
| `work` | Work Order và task |
| `execution` | Run và worker |
| `governance` | Policy, quyền và approval |
| `observability` | Event, trace và replay |
| `finance` | Reservation, usage và cost |
| `knowledge` | Memory và artifact tham chiếu |
| `quality` | Review và benchmark |
| `operations` | Lịch, incident và báo cáo |
