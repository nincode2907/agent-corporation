# Finding — tài liệu IPv6 proxy cũ

Severity: P2 / minor · Status: Confirmed documentation mismatch (RUNTIME-VERIFIED)

- [AGENTS.md](../../../../../../AGENTS.md#runtime-phase-01) và Dev Hub registry ghi Caddy local-only, IPv4 loopback; Docker host từ chối bind IPv6.
- [README.md](../../../../../../README.md) hiện ghi hostname đi qua Caddy publish trên “IPv4/IPv6 loopback”.
- Batch này xác nhận hostname/direct IPv4 và browser trả đúng app; `::1:15500` không có listener.
- Tác động: người đọc có thể thử route IPv6 không hỗ trợ; đường IPv4 local vẫn dùng được.
- Đề xuất: sửa README mô tả IPv4-only ở lượt docs được giao; không đổi proxy/system binding để ép IPv6. Finding này không tự đổi trạng thái Phase 01.
