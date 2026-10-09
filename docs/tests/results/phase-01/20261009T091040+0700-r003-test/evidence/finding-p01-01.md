# Finding P01-01 — Lệnh cài frontend trong README thất bại

- Severity: major — setup bắt buộc AC1 thất bại khi chạy đúng lệnh được tài liệu hóa.
- Expected: từ repo root, `npm ci --prefix apps/web` cài package theo lockfile trên checkout sạch.
- Actual: trên bản sao sạch và npm 11.19.0, lệnh tương đương `npm ci --prefix /tmp/ac-p01-prefix-r003.6xmgPP/web` thoát 1, báo `EUSAGE` và `Missing: web@0.0.0 from lock file`.
- Control: `npm ci` chạy với cwd trong chính thư mục web bản sao thoát 0, cài 28 packages, audit 0 vulnerabilities.
- Impact: người làm theo nguyên văn README không thể cài frontend; có workaround rõ ràng nhưng criteria cài đặt chưa đạt cho command công bố.
- Hướng sửa: dùng câu lệnh/setup tương đương đã pass từ cwd `apps/web`, rồi retest clean start. AI test không sửa source.
- Lệnh/output đã lọc: [commands](commands.md).
