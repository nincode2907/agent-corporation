# Lệnh và môi trường r003

Mọi shell qua rtk. Env process riêng: PYTHONPATH=apps/api/src; DATABASE_URL=postgresql+psycopg://qa_app:<fake-canary>@127.0.0.1:50822/qa067; MIGRATION_DATABASE_URL=postgresql+psycopg://qa_admin:<fake-canary>@127.0.0.1:50822/qa067; APP_DATABASE_USER=qa_app; APP_DATABASE_PASSWORD=<fake-canary>; OWNER_SECRET_PATH=/private/tmp/ac067-qa-owner-canary(0600); RUNTIME_GATE_PATH=/private/tmp/ac067-no-proof; RUNTIME_GATEWAY_SOURCE_PATH=/private/tmp/ac067-no-gateway; CODEX_SERVER_BASE_URL=http://127.0.0.1:1; CODEX_SERVER_API_KEY empty; PHASE_RUNTIME_TEST_ISOLATED=1. Credentials là canary tự tạo trong disposable resource, không .env thật.

Wrapper executable ở isolated-bootstrap.py: Settings.model_config.env_file=None trước Alembic/pytest. Chạy qua uvrun projectapps/api. Đường dẫn testcases evidence/independent-cases.py có thể thay temp path khi tái kiểm; DB role/port cần own disposable instance, không chép lệnh sang DB chung.

1. rtk proxy env <isolated-env> uv run --project apps/api python /tmp/ac067-qa-bootstrap.py migrate → exit0, actualhead0006. PG image pinned18.6 digest theo compose; root migration source0005 unchanged sau r002,0006 additive.
2. rtk proxy env <isolated-env> uv run --project apps/api python /tmp/ac067-qa-bootstrap.py test apps/api/tests -v --tb=short → exit0,73PASS, captured in C07-api-suite.txt. Repeated once because source-finalfeed whitelist changed after first pass; final source rerun output saved.
3. rtk proxy env <isolated-env> uv run --project apps/api python /tmp/ac067-qa-bootstrap.py test /tmp/test_ac067_independent.py -v --tb=short → final exit0,5PASS. Intermediate ownbrowserguard interference noted in runtime-observations.md, scoped cleanup done then rerun. Captured C05-independent-runtime.txt.
4. rtk proxy python3 -m unittest discover -s scripts/tests -v → exit0,14PASS, logicalroundorder regression included.
5. rtk proxy npm run --prefix apps/web lint → exit0.
6. rtk proxy npm run --prefix apps/web build → exit0,TS/Vite8.3.3 build.
7. rtk proxy git diff --check → exit0.
8. Own Uvicorn preview from /private/tmp/ac067-preview.py running in tty session13334; ephemeral64520 ownDB only, no proof/model. CUA native/Playwright readonlyDOM measured390px and captured evidence. rtk proxy ps -p92031 -o pid=,command= verifiedowned launcher; rtk proxy kill -KILL92031 stoppedonlyownpreview. QAcreatedtabclosed/viewportreset.

Tool versions: Python3.14.8; pytest9.0.2; uv0.12.23; Node24.21.0; Vite8.3.3. Framework/debug warnings are deprecations in TestClient/websockets, no test failures in final pass. Document projection check remains separate until root finalizes.

9. rtk proxy docker inspect --format name/QA-label/image agent-corporation-qa067-disposable → xác minh owned pinnedresource; rtk proxy docker rm -fv agent-corporation-qa067-disposable → exit0; dockerps exactname→empty. Pythonunlink chỉ fakecanary và ownpreview metadata; không cleanup globaltmp.

10. Final SQL privacy handler patch: isolated no-.env wrapper, dummyDBport1, pytest test_codex_gateway/test_health/test_owner_auth/test_phase06_runtime/test_phase07_feed/test_sensitive_validation -v --tb=short →53PASS, exit0; no PG. API503 generic+cache no-store/no echoed SQL parameters; workerCLI stops1/no traceback. Runtime service/migration unchanged; PG not rerun after cleanup.
11. rtk proxy python3 scripts/validate_phase00.py →PASS35events/3HTMLdeterministic; targetedreportvalidators bothPASS16/15cases; framework14 rerunPASS; diffcheckPASS.
