# P05-01 / P05-05 / P05-06 — Contract, capabilities, gaps

Đọc gateway README/src/server.ts/schema.ts/provider.ts/config.ts/catalog.ts/data/models.json, hash [manifest](source-manifest.json); registry chỉ ra HTTP loopback15600. Không đọc .env, sessions/rollouts hay credential; không sửa/restart gateway. 

| Capability | Source +quan sát r004 | Trạng thái |
|---|---|---|
| GET /health | server.ts route trả ok/provider/active_requests; live normalized healthok |verified|
| GET /v1/models | objectlist/dataids; live7IDs, UI [observation](P05-ui-observation.md)|verified; không entitlement|
| Bearer/backend refs | adapter Bearer khi configured; bypass env proxy, deny redirects, canary absent response |fixture verified; live authfalse|
| POST text contract | source schema strict, streamfalse,n1; no max_tokens; chỉ đọc source |CODE-VERIFIED; không POST|
|429 | gateway rejects concurrency before provider; queue service persistence bounded,1then3seconds spec |fixture DB verifies bounded queue/no fallback|
|409/502/504/disconnect | parse_response409/502/504→unknown, only429 requeue; expired lease fences guard |fixture verified, không auto replay|
| Persona/model/tools/policy | runtime immutable profile/policy snapshot; effective model explicit Owner grant; toolsfalse |fixture persistence verified|
| Isolation/read boundary | provider now disables shell/unified/apps/plugins/web, ignore-user-config/rules, read-only separate runtime cwd; output rejects tool events |CODE-VERIFIED hardening; **không phải live proof**|
| Retention | route chat passes ephemeralfalse; playground-only ephemeraltrue; provider retains HOME/CODEX_HOME path |input persistence may remain; no native transcript inspected|
| Cancellation | gateway abort source +fake socket/worker test |không chứng minh cancellation subprocess thật|
|CG01 proof | check_gate(.local/cg01-proof.json,../codex-server,base_url15600) |allowedfalse,reasonmissing_or_invalid_proof|

Gateway fingerprint actual: `78f0a5ae3caa013fe3f667aee69855f08711380e6da3c98e51d56cce10b80a37`. Missing proof không chứng minh capability thực tế fail; gate vẫn BLOCKED, đúng default deny. Không lặp conclusion lịch sử “chắc chắn file đọc được” khi source hiện đã hardened. Cần trusted operator evidence gắn fingerprint/endpoint/expiry cho isolation/privacy-retention/cancellation, hoặc Chủ tịch quyết định contingency theo spec§6. Grant mới riêng đúng batch nếu đợt tiếp cần inference; health/models không cấp grant. Không tự sửa gateway/shared hoặc tạo instance thay thế.

Old blockers r003 đã outdated: gateway live available; Owner auth/profile/audit và durable queue đã triển khai, exercised ở batch này. Dependency03/04 vẫn Chờ nghiệm thu; đây là trạng thái nghiệm thu riêng, không lý do bỏ các fixture/read-only checks có thể chạy.
