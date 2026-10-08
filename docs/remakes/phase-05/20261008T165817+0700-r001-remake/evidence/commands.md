# Kiểm tra trong remake Phase 05 r001

| Kiểm tra | Lệnh / thao tác | Kết quả |
| --- | --- | --- |
| Web lint | `rtk proxy npm run --prefix apps/web lint` | Exit 0; oxlint pass |
| Web production build | `rtk proxy npm run --prefix apps/web build` | Exit 0; TypeScript + Vite 8.3.3 pass |
| Diff whitespace | `rtk proxy git diff --check` | Exit 0 |
| UI retest | Chrome Settings → Probe gateway trên API process đang nghe, response HTTP 404 | Trang vẫn render; báo Contract/cấu hình cần kiểm tra + HTTP 404; không thấy exception trong accessibility state |

Không restart API/DB/gateway. Không gọi inference. Screenshot không lưu được bằng giao diện CUA hiện có; state accessibility và mô tả trực tiếp đã được ghi trong report retest mới.
