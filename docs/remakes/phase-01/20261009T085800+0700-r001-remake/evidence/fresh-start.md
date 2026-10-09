# Clean install/startup Phase 01

## Clean web install
- Command: `npm ci`
- Exit code: 0
```text
added 28 packages, and audited 29 packages in 2s

9 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
npm warn install-scripts 1 package has install scripts not yet covered by allowScripts:
npm warn install-scripts   fsevents@2.3.3 (install: (install scripts present))
npm warn install-scripts
npm warn install-scripts Run `npm install-scripts ls` to review, or `npm install-scripts approve <pkg>` to allow.
```

## Clean API locked sync
- Command: `uv sync --project /var/folders/nf/t8dhz5mx2pbgswwr4mk99_mr0000gq/T/agent-corp-p01-clean-start-ww1_htj5/project/apps/api --locked`
- Exit code: 0
```text
Using CPython 3.14.8 interpreter at: /opt/homebrew/opt/python@3.14/bin/python3.14
Creating virtual environment at: /var/folders/nf/t8dhz5mx2pbgswwr4mk99_mr0000gq/T/agent-corp-p01-clean-start-ww1_htj5/project/apps/api/.venv
Resolved 38 packages in 6ms
Installed 35 packages in 337ms
 + alembic==1.20.0
 + annotated-doc==0.0.5
 + annotated-types==0.8.0
 + anyio==4.15.1
 + certifi==2026.7.22
 + click==8.5.0
 + fastapi==0.142.4
 + h11==0.16.0
 + httpcore==1.0.9
 + httptools==0.8.0
 + httpx==0.28.1
 + idna==3.20
 + iniconfig==2.3.1
 + mako==1.4.3
 + markupsafe==3.0.4
 + opentelemetry-api==1.45.1
 + packaging==26.3
 + pluggy==1.6.0
 + psycopg==3.3.6
 + psycopg-binary==3.3.6
 + pydantic==2.13.5
 + pydantic-core==2.46.5
 + pydantic-settings==2.11.0
 + pygments==2.21.0
 + pytest==9.0.2
 + python-dotenv==1.2.4
 + pyyaml==6.0.3
 + sqlalchemy==2.1.4
 + starlette==1.7.0
 + typing-extensions==4.16.0
 + typing-inspection==0.4.4
 + uvicorn==0.38.0
 + uvloop==0.23.0
 + watchfiles==1.3.0
 + websockets==17.2
```

## Start isolated PostgreSQL
- Command: `docker run -d --rm --name ac-p01-start-22098-1791511490 -e POSTGRES_HOST_AUTH_METHOD=trust -e POSTGRES_DB=p01_run -p 127.0.0.1::5432 postgres:18.6-alpine@sha256:77f585114c32fbca283dc835b0596f4e52b51b4c6662d7810b2f4084f60a1873`
- Exit code: 0
```text
331413e4a8a3c06e5523c209c4eba44342262c6f6e97c6ce1c0edc340fd86c89
```

## Discover isolated PostgreSQL port
- Command: `docker port ac-p01-start-22098-1791511490 5432/tcp`
- Exit code: 0
```text
127.0.0.1:60443
```

## Apply Phase 01 baseline to isolated DB
- Command: `uv run --project /var/folders/nf/t8dhz5mx2pbgswwr4mk99_mr0000gq/T/agent-corp-p01-clean-start-ww1_htj5/project/apps/api alembic -c /var/folders/nf/t8dhz5mx2pbgswwr4mk99_mr0000gq/T/agent-corp-p01-clean-start-ww1_htj5/project/apps/api/alembic.ini upgrade 20261008_0001`
- Exit code: 0
```text
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 20261008_0001, Establish the empty Phase 01 schema baseline.
```

## Clean install startup smoke
- API command: `uv run --project /var/folders/nf/t8dhz5mx2pbgswwr4mk99_mr0000gq/T/agent-corp-p01-clean-start-ww1_htj5/project/apps/api uvicorn agent_corporation_api.main:app --app-dir /var/folders/nf/t8dhz5mx2pbgswwr4mk99_mr0000gq/T/agent-corp-p01-clean-start-ww1_htj5/project/apps/api/src --host 127.0.0.1 --port 62896`
- API /api/v1/health/ready: HTTP 200 {"status":"ok","checks":{"database":"ok"}}
- Web command: `npm run dev -- --host 127.0.0.1 --port 62897 --strictPort`
- Web `/`: HTTP 200; document response received.
- Web favicon: HTTP 200.
- Bind: 127.0.0.1 only; temporary dynamic ports API=62896, Vite=62897; no Dev Hub allocation changed.
- Database: isolated PostgreSQL `p01_run` on Docker-assigned ephemeral 127.0.0.1 port; baseline `20261008_0001`.
- Inference: none; only readiness, document, and favicon GETs.
- Cleanup: API/Vite stopped; container stopped; temporary project copy removed.

## Sanitized startup logs
API:
```text
INFO:     Started server process [23479]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:62896 (Press CTRL+C to quit)
INFO:     127.0.0.1:62919 - "GET /api/v1/health/ready HTTP/1.1" 200 OK
```
Web:
```text
> web@0.0.0 dev
> vite --host 127.0.0.1 --port 62897 --strictPort


  VITE v8.3.3  ready in 742 ms

  ➜  Local:   http://127.0.0.1:62897/
```
