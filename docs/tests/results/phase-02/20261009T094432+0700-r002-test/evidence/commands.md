# Commands — Phase 02 r002

| Lệnh/thao tác | Exit/kết quả | Quan sát |
| --- | ---: | --- |
| `rtk proxy npm run --prefix apps/web build` | 0 | TypeScript + Vite build pass. |
| `rtk proxy npm run --prefix apps/web lint` | 0 | Oxlint pass. |
| GET `http://127.0.0.1:15501/api/v1/health/live` và `/ready` | 200/200 | Chỉ health local; không gọi gateway/model. |
| Chrome/CUA: mở dashboard → S05 Work Order → S03 Inspector | pass | AX tree ghi nhãn route, fixture, trạng thái và nội dung shell; chi tiết tại [ui-observations](ui-observations.md). |
| Chrome/CUA: S06 approvals → S09 finance → S07 organization → reload | pass | Các trang render; finance hiển thị usage unknown, organization dùng nhãn DEMO fixture. |
| Chrome/CUA: mode Chủ tịch/Vận hành và keyboard Tab + Space | pass | Checkbox đổi góc nhìn bằng Space; đã khôi phục Chủ tịch. |
| Chrome/CUA: reload organization | transient error → data visible | Quan sát được error copy “Không đọc được demo…” rồi fixture render lại trong lượt đọc tiếp theo; không có network fault injection nên không kết luận nguyên nhân/phục hồi sau outage. |
| `rtk proxy python3 scripts/render_plan.py` | 0 | HTML đồng bộ từ Markdown, 24 phases, 1 phase hoàn tất; Phase02/03 vẫn Chờ nghiệm thu. |
| `rtk proxy python3 docs/tests/scripts/validate.py` | 0 | Cấu trúc checklist 24/171; HTML; Phase02 r002 15 cases and all reports validated. |

Không lưu screenshot vào batch: CUA trong phiên cung cấp ảnh để xem trực tiếp nhưng không có API ghi PNG vào workspace; browser viewport override 390×844 không được cung cấp qua surface khả dụng. Không đổi API/DB dùng chung, không gọi inference, không tạo hoặc reset fixture.
