# Commands — Phase 02 remake r001

Worktree đang có thay đổi ngoài scope. Không dùng lệnh ghi/cập nhật test report nguồn.

| Lệnh | Exit | Kết quả |
| --- | ---: | --- |
| `rtk proxy sed -n '1,340p' apps/web/src/App.tsx` | 0 | Xác nhận trạng thái fetch, error UI và retry controls; chỉ đọc. |
| `rtk proxy npm run --prefix apps/web build` | 0 | TypeScript/Vite production build pass. |
| `rtk proxy npm run --prefix apps/web lint` | 0 | Oxlint pass. |
| `rtk proxy python3 scripts/render_plan.py` | 0 | HTML đồng bộ với 24 phase; 1 phase hoàn tất. |
| `rtk proxy python3 docs/tests/scripts/validate.py` | 0 | 24 checklist, 171 test, HTML deterministic/đồng bộ và local links đạt cấu trúc. |

Không chạy inference, không gọi codex-server, không reset demo hoặc sửa dữ liệu.
