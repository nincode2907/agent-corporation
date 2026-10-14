# C03/P05-01/P05-02/P05-07 — UI retest sau remake r004

Ngày14/10/2026, AI điều phối /root test Chrome/CUA tab2087261635. Import source app mới sau restart **chỉ** process QA do lượt này tạo. Không restart sharedAPI15501/PG15510/gateway15600, không đọc .env hoặc Ownersecret, không POSTinference.

QAbackend15592 / Gatewaystub15590 / Vite15500 (đã reserve và kiểm listener). Settings(_env_file=None), fakeDB15599 không listener; DB/demo/session unavailable thuộc fixture, không dùng để kết luận lỗi sản phẩm. Profile persistence/auth/audit được tester độc lập kiểm quaAPI/PG riêng; browser này chỉ kiểm probe.

Mở/reload `http://127.0.0.1:15500/#settings`: AX có Cấu hình&sức khỏe, grant chưa cấp, Chưa chạy probe trong phiên này. Sau mỗi thay đổi mode fixture, bấm đúng nút Probe gateway rồi lấy AX mới:

| Mode | Thực tế quan sát |
| --- | --- |
| UTF8invalid bxff / HTTP200 | UI Contract/cấu hình cần kiểm tra; Phản hồi gateway không khớp contract health/models đã xác nhận. APIGET/probe200 trong log QA, không500/không crash |
| auth401 | Cần xác thực gateway; kiểm tra secret reference phía backend |
| offline/no listener | Không kết nối được; thông báo kiểm tra dịch vụ mà không thay sharedconfig |
| schema sai200 | Contract/cấu hình cần kiểm tra; không lộ rawpayload |
| rate429 | Gateway đang giới hạn probe; thử lại thủ công sau |
| live recovery | Gateway thật15600 trả health/models; UI Gateway phản hồi, Health ok/Catalog ok,7modelIDs; catalog không xác nhận entitlement |
| reload sau recovery | Trở về Chưa chạy probe trong phiên này, không tự chạy model |

Rawstub metadata JSONL chỉ chứa8GET (UTF8/auth/schema/rate mỗi mode2GET), không POST. Offline không tới stub; liveGET dùng gateway thật. Browser không đăng nhập/seed/reset/run/grant. Script/config kèm evidence; fixture không có handlerPOST. Không dùng fakeUI để chứng minh inference/CG01.

Kiểm tra source sau remake:

- `npm run --prefix apps/web lint`: exit0.
- `npm run --prefix apps/web build`: exit0, TypeScript + Vite8.3.3,19modules,JS285.93kB.
- `git diff --check`: exit0.

UI RuntimePanel effort8choices được CODE-VERIFIED và TypeScriptbuild; không claim browser đã lưu Ownerprofile. Bản sửa profile được AItest độc lập kiểmAPI persistence.

Cleanup: Đã đóng tabQA, Ctrl+C các PTYQAbackend/Vite do lượt này tạo, xóa thư mục temp fixture riêng. Lsof toàn block15500–15599 sau cleanup chỉ còn APIshared15501 và PostgreSQLshared15510 ban đầu; không còn15500/15590/15592 của QA.
