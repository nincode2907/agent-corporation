# Agent Corporation

## Hướng dẫn áp dụng
- Đọc và tuân thủ `/Users/buivannin/.codex/RTK.md`; mọi lệnh shell dùng tiền tố `rtk`.
- Dự án local-first để Chủ tịch giao mục tiêu, quản lý nhân viên AI, quan sát thực thi và nghiệm thu bằng chứng.
- Hiện chỉ có kế hoạch và HTML theo dõi. Chưa có sản phẩm, Git, package manager, migration hay lệnh chạy app.
- Chỉ triển khai phase người dùng yêu cầu; hết phase thì báo cáo và dừng. Không tự chuyển phase, tạo công ty thật, gọi inference hoặc thay cấu hình toàn máy.

## Đọc đúng ngữ cảnh
- Trước khi triển khai: đọc `docs/master-plan.md`, phase được yêu cầu, dependency và các quy tắc V1.
- Đối chiếu ý tưởng khi cần: `docs/sources/`; bản 02 ưu tiên cho thứ tự xây sản phẩm trước, vận hành sau.
- Setup/runtime: dùng skill global `project-ai-bootstrap`; gateway: đọc README/source của codex-server; OpenAI native protocol dùng `openai-docs` khi cần.
- UI dùng `ui-page-builder` hoặc `frontend-design`; feature dùng `feature-builder`; QA sau phase dùng `task-qa-review` khi phù hợp. Không nạp toàn bộ skill cùng lúc.

## Ranh giới quan trọng
- Runtime dùng HTTP gateway `/Users/buivannin/Desktop/workspace/personal/codex-server`, hiện tại `127.0.0.1:4000`. Đọc contract/source; không đổi server chung, không giả định streaming hay model entitlement.
- Demo, benchmark và công ty thật phải tách dữ liệu, artifacts, threads, secrets và báo cáo.
- Model/policy/ngân sách/quyền do Chủ tịch quyết định. Agent chỉ đề xuất, backend kiểm tra quyền; prompt không phải permission engine.
- Event store và execution state bền vững từ đầu; ghi bằng chứng, tóm tắt quyết định tường minh, không hứa hiển thị suy nghĩ nội bộ.
- Không đoán usage/giá; phân biệt xác nhận, ước tính, chưa biết. Giới hạn run và dừng khẩn cấp trước agent thật.
- Không retry tool có side effect khi chưa biết kết quả; resume phải kiểm tra checkpoint và idempotency.
- Tiếng Việt cho giao diện/tài liệu người dùng, `lang="vi"`, favicon, responsive và accessibility.

## Tài liệu và nghiệm thu
- `docs/master-plan.md` là nguồn chuẩn cho phạm vi, trạng thái và bằng chứng phase; HTML là bản nhìn trực quan.
- Sửa Markdown trước, đồng bộ HTML bằng `rtk proxy python3 scripts/render_plan.py` từ root. Template tại `docs/assets/roadmap-template.html`.
- Ghi chú/checklist trong trình duyệt chỉ là ghi chú cá nhân; không thay trạng thái chính thức.
- Chỉ hoàn tất phase khi có demo, kiểm thử phù hợp, evidence và người dùng nghiệm thu; cập nhật Markdown rồi render HTML cùng lần.
- Không commit/push hoặc cài global tool khi chưa được yêu cầu.

## Runtime tương lai
- Trước quyết định host port đọc `/Users/buivannin/Desktop/workspace/personal/dev-hub/projects.yml`, kiểm tra toàn block và listener rồi reserve → verify → configure.
- Hiện dự án chưa có allocation/hostname hoạt động. Không dùng port dự đoán, không sửa Dev Hub trong bước lập kế hoạch.
- Khi triển khai runtime, giữ server trong terminal tương tác nhìn được log; chỉ công bố URL đã xác minh.
