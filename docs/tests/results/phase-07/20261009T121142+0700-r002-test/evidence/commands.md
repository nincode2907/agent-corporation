# Lệnh và quan sát

1. rtk proxy docker run -d --name agent-corporation-qa067-disposable --label agent-corporation.qa=phase06-07 --env POSTGRES_USER=qa_admin --env POSTGRES_PASSWORD=<fake-canary> --env POSTGRES_DB=qa067 --publish 127.0.0.1::5432 <compose-pinned-postgres-image>; exit0; loopback50822.
2. rtk proxy env PYTHONPATH=apps/api/src DATABASE_URL=<isolated-app> MIGRATION_DATABASE_URL=<isolated-admin> APP_DATABASE_USER=qa_app APP_DATABASE_PASSWORD=<fake-canary> OWNER_SECRET_PATH=/private/tmp/ac067-qa-owner-canary RUNTIME_GATE_PATH=/private/tmp/ac067-no-proof RUNTIME_GATEWAY_SOURCE_PATH=/private/tmp/ac067-no-gateway CODEX_SERVER_BASE_URL=http://127.0.0.1:1 CODEX_SERVER_API_KEY= PHASE_RUNTIME_TEST_ISOLATED=1 uv run --project apps/api python /tmp/ac067-qa-bootstrap.py migrate; exit0; migrations0001→0005. Wrapper disables env_file entirely.
3. Same isolated env + bootstrap.py test apps/api/tests -v; exit1; 57collected56pass1fail (runtime read missingcompany FK). First attempt wrapper missing PYTHONPATH exit1 ModuleNotFoundError, corrected before migrations.
4. Same isolated env + bootstrap.py test /tmp/test_ac067_independent.py -v --tb=short; exit1; durableAuth pass, missingusage reservation fail, malformedCG01proof fail. No real POST; runtime service reservation and fakeCallOutcome only.

Suite and independent case observations at evidence/runtime-observations.md. Source frozen bymanifest; UI/docs still in-flight and not claimed currentvisualverified. Container retained solely for r003 retest; cleanup scoped after completion.
