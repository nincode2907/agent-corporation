# Gemini review package — Stabilization Sprint 01

**Trạng thái:** chuẩn bị nội dung để review độc lập; chưa gửi tới Gemini. CLI `gemini` và Gemini API/tool không sẵn có trong session. Không dùng browser impersonation, không tạo credential hoặc quota.

## Bối cảnh sản phẩm

Agent Corporation là nền tảng local-first: Chủ tịch giao mục tiêu, quản lý nhân viên AI, quan sát Work Order/run/event và nghiệm thu bằng evidence. UI V1 tiếng Việt gồm Overview, Live Office, Work Orders, Inspector/Replay, Organization, Approval Inbox, Settings và Development Playground. Backend là FastAPI modular monolith + PostgreSQL durable event/runtime state; React/TypeScript/Vite serve browser UI; REST và app-owned SSE kết nối UI với backend. Inference chỉ khi Owner cấp quyền/grant riêng và worker dispatch; mở trang hoặc replay không tự chạy agent.

## Phạm vi review đề nghị

- Responsive layout và hierarchy ở desktop 1440×900, mobile 390×844.
- Keyboard skip link, focus, semantic controls và trạng thái loading/empty/error.
- Playground session/expired grant affordance và cách phân biệt demo fixture với runtime thực.
- Inspector/Replay provenance, unknown usage/cost, missing data copy và read-only affordance.
- Office/live/reconnecting/stale/offline labels: liệu copy có nói đúng runtime state được quan sát không.
- Đề xuất ưu tiên P0/P1/P2, gắn ảnh và mô tả cụ thể, tránh redesign rộng nếu không có vấn đề usability chứng minh được.

## Ràng buộc review

- Không đề xuất đổi phase status, grant, quyền inference hoặc gọi model.
- Không coi historical Phase 06 run là Phase 08 acceptance.
- Không giả định codex-server có token streaming; app SSE chỉ chuyển events của Agent Corporation.
- Không suy ra chi phí từ token usage; unknown phải giữ là unknown.
- Screenshot có dữ liệu nội bộ demo; không trích transcript hoặc secret vào kết quả review.

## Screenshots

Ảnh authenticated browser (đăng nhập Owner, chỉ GET/read-only trong quá trình capture):

- [Overview desktop](evidence/authenticated/screenshots/overview/1440x900.png) · [mobile](evidence/authenticated/screenshots/overview/390x844.png)
- [Playground desktop](evidence/authenticated/screenshots/playground/1440x900.png) · [mobile](evidence/authenticated/screenshots/playground/390x844.png)
- [Office desktop](evidence/authenticated/screenshots/office/1440x900.png) · [mobile](evidence/authenticated/screenshots/office/390x844.png)
- [Work Orders desktop](evidence/authenticated/screenshots/work/1440x900.png) · [mobile](evidence/authenticated/screenshots/work/390x844.png)
- [Inspector desktop](evidence/authenticated/screenshots/inspector/1440x900.png) · [mobile](evidence/authenticated/screenshots/inspector/390x844.png)
- [Replay desktop](evidence/authenticated/screenshots/replay/1440x900.png) · [mobile](evidence/authenticated/screenshots/replay/390x844.png)
- [Organization desktop](evidence/authenticated/screenshots/organization/1440x900.png) · [mobile](evidence/authenticated/screenshots/organization/390x844.png)
- [Approvals desktop](evidence/authenticated/screenshots/approvals/1440x900.png) · [mobile](evidence/authenticated/screenshots/approvals/390x844.png)
- [Settings desktop](evidence/authenticated/screenshots/settings/1440x900.png) · [mobile](evidence/authenticated/screenshots/settings/390x844.png)
- [Manifest and viewport measurements](evidence/authenticated/manifest.json)

## Câu hỏi gửi reviewer

1. Ở mỗi màn, điểm nào làm người dùng khó hiểu trạng thái hoặc bước tiếp theo? Gắn screen/viewport cụ thể.
2. Trên mobile, hierarchy và điều hướng ngang có thể khám phá bằng touch/keyboard không? Có thành phần nào bị cắt hoặc khó thao tác dù document không overflow?
3. Inspector/Replay có phân biệt rõ dữ liệu lịch sử, nguồn event, thiếu dữ liệu, usage đã xác nhận và cost chưa biết không?
4. Playground có thể khiến Chủ tịch hiểu nhầm grant hết hạn/session lịch sử là khả dụng hiện tại không? Đề xuất copy/placement cụ thể.
5. Loading, empty, error, reconnecting, stale và offline có cần tách rõ hơn không? Nêu chỉ báo runtime cần thiết để tránh đoán.
6. Xếp 5 thay đổi UX có ROI cao nhất mà không đổi phạm vi V1, quyền hoặc kiến trúc.

