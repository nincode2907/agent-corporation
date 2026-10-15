# P11-06 — Redaction canary

## Điều kiện và kỳ vọng

Chỉ dùng chuỗi giả, không dùng credential thật. Nội dung đi qua `redact_text`, hàm mà `WorkspaceReader.read_text` áp dụng trước khi trả file content. Kỳ vọng là nhãn credential nhạy cảm được che, giá trị canary không còn trong kết quả.

## Quan sát

Đầu vào gồm `Authorization: Basic test-canary-123`, `cookie=test-cookie-456`, và `api_key=masked-canary-789` trên ba dòng. Hàm chỉ có các mẫu text cho `bearer`, `password`, `passwd`, `api_key`, `access_token`, `refresh_token`, `secret`; không có `authorization` hoặc `cookie`. Kết quả giữ nguyên hai canary Authorization/cookie, còn api_key được thay bằng `[REDACTED]`.

## Kết luận

`CODE-VERIFIED` security finding: `Authorization`/`cookie` credential formats are not redacted from tool output. Severity major pending integration review. Chưa chạy runtime executor; chưa có call site production của reader. Xem `../commands.md` và `../source-manifest.json`.
