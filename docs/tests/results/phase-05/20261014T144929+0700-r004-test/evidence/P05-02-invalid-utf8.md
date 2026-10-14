# P05-02 — malformed UTF8 response crashes probe

Confirmed RUNTIME-VERIFIED trong ASGI app/router thật với fake HTTP opener; không chạm gateway/runtime thật. Fake Response200 trả bytes `b"\xff"`. `_get_json` gọi json.loads(bytes), except chỉ có JSONDecodeError nhưng UnicodeDecodeError thoát ra. `probe_gateway` throw UnicodeDecodeError; TestClient(raise_server_exceptions=False) GET `/api/v1/codex/probe` trả **500 Internal Server Error**. Expected normalized offline/contract mismatch và recoverable UI error; không unhandled exception. Existing6 gateway tests chưa phủ encoding failure.

Severity P2/major checklist: impactMedium, likelihoodPossible khi bad gateway/proxy/body, reachprobe users, recoveryEasy(manual retry), bypassNo; fix trong adapter catch decode failure ở boundary, test invalid encoding qua fake opener/ASGI. Không chuyển exception text/raw response vào UI hoặc log credential. Các fake401/schema hợp lệ JSON/offline/429 qua Chrome đạt [UI](P05-ui-observation.md), nhưng encoding variant vẫnfail.

Reproduce bằng body fake; không cần DB/secret. `adapter.build_opener=lambda *handlers:Opener()` với `Opener.open` trả Response context manager status200/read→b'\xff'; app.include_router(codex_gateway.router.router); TestClient(...raise_server_exceptions=False).get('/api/v1/codex/probe')→500. Settings(_env_file=None) với DB giả, không .env.
