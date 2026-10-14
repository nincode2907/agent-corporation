# Validation tài liệu revision 02

- `python3 scripts/validate_phase00.py`: PASS baseline contract + HTML đồng bộ; không product/inference tests.
- Kiểm tra HTML/MD mới: PASS local links, lang/favicon, unique IDs, JavaScript syntax, không network/storage client.
- `git diff --check`: PASS.
- CUA Chrome prototype: desktop1440×1000/mobile390×844; screenshots và browser-checks.json ở cùng thư mục; không gọi API.
- Preview server riêng đã dừng; bản sao HTML tạm đã dọn, tab QA đóng và viewport reset. Shared app/API/DB/gateway không restart hoặc thay đổi.
- Proof mặc định vẫn không tồn tại; không cấp grant. CG01 BLOCKED, TDG OPEN.

## SHA-256 nguồn thiết kế cuối

- `docs/designs/employee-chat.md`: `985e3b35a33bd8b50c49b5a5d251ea359d44caa72d93de456f3ab52bda68debb`
- `docs/designs/employee-chat.html`: `ec01bff4b78a69f40acec4abf5586caf3fbbbd725161c11ffc752c3d8bc5a7ff`
- `docs/designs/employee-chat-prototype.html`: `7b19c17ebfa71a62d94b4ab7a683c5f997022b627a496e9a2835605c297c278b`
- `docs/designs/cg01-technical-decision.md`: `0fdd7e7ff829d51bb46152e8e2e903840f316cb0082e98c0560c9a4e39d8c037`
- `docs/designs/cg01-technical-decision.html`: `f49ac3ad2cffe008133fd652b245b3da21b6a320de61fb9833978bb564610dac`
- `docs/master-plan.md`: `f44df9ca9b7126cfe4c14273e7a473a5d2da3c11d710242801491587f9732dd8`
- `docs/product-spec.md`: `29ce13218e4e2d5179f04397b654ee47ebbb1fc2115fcb1605204ab6cf0c7d77`
- `docs/decisions/0002-employee-chat.md`: `c66d4bfe842925783fce268def8f1ed9ca50db4ef28ef0c3461ea0de5f4c2459`
