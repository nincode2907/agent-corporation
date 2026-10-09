# Finding P01-01 — Lệnh cài frontend trong README thất bại

Severity: major (ảnh hưởng tiêu chí cài đặt bắt buộc, workaround rõ ràng)
Status: Confirmed, tái hiện trên bản sao sạch

## Bằng chứng

- Kỳ vọng: README có thể chạy từ root trên checkout sạch để cài frontend theo lockfile.
- Lệnh ghi trong [README](../../../../../../README.md): `npm ci --prefix apps/web`.
- Thực tế: cùng lệnh trên bản sao sạch trả exit 1 với npm 11.19.0: `EUSAGE`, “`npm ci` can only install packages when your package.json and package-lock.json or npm-shrinkwrap.json are in sync”, cụ thể `Missing: web@0.0.0 from lock file`.
- Cách thay thế kiểm chứng: `npm ci` với cwd là thư mục `apps/web` trên bản sao sạch trả exit 0, cài 28 packages, audit 0 vulnerabilities.
- Build từ checkout hiện tại vẫn pass; điều này không làm lệnh hướng dẫn cài sạch trở thành pass.

## Đánh giá

- Impact: Medium; người dùng làm theo đúng README không cài được frontend.
- Likelihood: Common với npm 11.19.0 và câu lệnh hiện ghi.
- Reach: mọi người dựng frontend từ hướng dẫn hiện tại.
- Recoverability: Easy; chạy lệnh trong `apps/web` hoặc chỉnh README theo lệnh đã xác minh.
- Có thể bypass: Có, bằng cách chuyển cwd vào `apps/web`.
- Root cause hypothesis: `npm ci --prefix` trong npm 11 xử lý project root/lock context khác với kỳ vọng của README.
- Khuyến nghị: cập nhật README/setup command sang dạng chạy từ thư mục `apps/web` và kiểm lại clean install. Không sửa source trong lượt test độc lập.
- Ship decision: Có thể chạy với workaround được ghi rõ; nên sửa trước khi yêu cầu người mới dựng môi trường theo README.
- Evidence: [commands](commands.md).
