# P05-03 / P05-04 — Owner profile persisted API

RUNTIME-VERIFIED với FastAPI TestClient + PostgreSQL18.6 riêng15591 migration0007. Owner scope mới tự tạo: environment fcd0b92e-fb50-4e5a-9401-9fc43c25af30/company1f26297b-88ab-40f7-86c3-a4920097a645. Owner secret là canary tạm mode0600, bỏ sau context; không đọc credential thật. Request cookie/CSRF không lưu.

| Thử | HTTP/quan sát |
|---|---|
| PUT profile không session, header X-Actor agent/X-Owner true |401|
| Login bằng canary +scope đã cấp |200/session server scoped|
| Owner PUT thiếu CSRF |403|
| PUT model gpt-6.1-sol, effortlow, version0 |200/version1|
| PUT stale version0 |409|
| PUT not-in-catalog-p05-r004, effortlow, version1 |**200/version2**|
| GET profile sau write unsupported |**version2, model not-in-catalog-p05-r004 persisted**|
| Effort max (gateway schema chấp nhận) |422 app Literal|
| Fallback trùng lặp |422|

Hai event OWNER_MODEL_PROFILE_UPDATED trong DB ghi version1/2, model, effort, tools_enabledfalse, inference_authorizedfalse; không secret. Profile source chỉ regex +Literal, không catalog/capability validation. Live catalog trước test: gpt-6.1-sol, gpt-6-luna, gpt-6-astra, gpt-6-sol, gpt-5.6-sol, gpt-5.6-terra, gpt-5.6-luna. Unsupported ID ở trên vắng trong catalog nhưng vẫn persisted; chưa thể hiển thị lỗi model không hỗ trợ đúng Phase05.

P05-03 cần sửa: validate supported IDs và effort theo capability evidence đúng source/time, gồm fallback IDs; offline/schema mismatch không mặc nhiên xác minh model. Không gọi inference hoặc coi catalog membership là entitlement. Capability schema cho phép minimal..persistent, data/models.json cho biết effort mỗi model; app hiện không kiểm tương thích từng model. Việc app chọn subset effort có thể là quyết định sản phẩm nhưng phải công khai và đúng contract; không suy rằng schema-wide enum chứng minh mọi model hỗ trợ mọi effort.

P05-04 đạt: authenticated Owner write, missing session/CSRF deny, spoofed actor flags deny; version409 và audit persistence thật được kiểm. Không tự suy auth có nghĩa grant inference. [Fixture tái lập](P05-profile-fixture.py), [commands](commands.md).
