# Lệnh và kiểm tra preflight Phase 08 r001

Không khởi động/restart service, không ghi DB, không probe gateway, không inference.

| Kiểm tra | Lệnh | Kết quả |
| --- | --- | --- |
| API health + gateway regression | `rtk proxy uv run --project apps/api pytest apps/api/tests/test_health.py apps/api/tests/test_codex_gateway.py -q` | Exit 0; 9 passed (1.39s) |
| Web lint | `rtk proxy npm run --prefix apps/web lint` | Exit 0; oxlint pass |
| Web build | `rtk proxy npm run --prefix apps/web build` | Exit 0; TypeScript + Vite 8.3.3 |
| Diff whitespace | `rtk proxy git diff --check` | Exit 0 |
| Dependency | Đọc master-plan, Phase 07 preflight, Phase 06/05 evidence và product-spec §§6, 9, 13 | Phase 07/06 blocked; IG08 runtime inputs không khả dụng |
| Docs validator | `rtk proxy python3 docs/tests/scripts/validate.py --batch docs/tests/results/phase-08/20261009T114228+0700-r001-test` | Exit 0; 15 cases, evidence links và HTML consistency hợp lệ |
| Inference/gateway | Không gọi | Grant = 0; giữ CG01 boundary |
