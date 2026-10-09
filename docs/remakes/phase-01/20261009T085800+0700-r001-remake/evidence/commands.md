# Lệnh và kết quả remake Phase 01

## Node version
- Command: `node --version`
- Exit code: 0
```text
v24.21.0
```

## npm version
- Command: `npm --version`
- Exit code: 0
```text
11.19.0
```

## uv version
- Command: `uv --version`
- Exit code: 0
```text
uv 0.12.23 (46b84fd0b 2026-10-03 aarch64-apple-darwin)
```

## Docker version
- Command: `docker --version`
- Exit code: 0
```text
Docker version 20.10.23, build 7155243
```

## Fresh web dependency installation
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

## Fresh web production build
- Command: `npm run build`
- Exit code: 0
```text
> web@0.0.0 build
> tsc -b && vite build

vite v8.3.3 building client environment for production...
transforming...
✓ 17 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   1.02 kB │ gzip:  0.59 kB
dist/assets/index-CKwIEvP2.css   28.07 kB │ gzip:  6.70 kB
dist/assets/index-CvdjjsjA.js   247.91 kB │ gzip: 76.51 kB

✓ built in 328ms
```

## Fresh API dependency sync from lockfile
- Command: `uv sync --project /var/folders/nf/t8dhz5mx2pbgswwr4mk99_mr0000gq/T/agent-corp-p01-remake-sog3opcc/project/apps/api --locked`
- Exit code: 0
```text
Using CPython 3.14.8 interpreter at: /opt/homebrew/opt/python@3.14/bin/python3.14
Creating virtual environment at: /var/folders/nf/t8dhz5mx2pbgswwr4mk99_mr0000gq/T/agent-corp-p01-remake-sog3opcc/project/apps/api/.venv
Resolved 38 packages in 18ms
Installed 35 packages in 74ms
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

## Phase 01 API health unit tests
- Command: `uv run --project /var/folders/nf/t8dhz5mx2pbgswwr4mk99_mr0000gq/T/agent-corp-p01-remake-sog3opcc/project/apps/api pytest apps/api/tests/test_health.py -q`
- Exit code: 0
```text
...                                                                      [100%]
3 passed in 6.06s
```

## Start isolated PostgreSQL container
- Command: `docker run -d --rm --name ac-p01-88227-1791511140 -e POSTGRES_HOST_AUTH_METHOD=trust -e POSTGRES_DB=p01_clean -p 127.0.0.1::5432 postgres:18.6-alpine@sha256:77f585114c32fbca283dc835b0596f4e52b51b4c6662d7810b2f4084f60a1873`
- Exit code: 0
```text
ae22a9b94f2edbea3fa9381d08417db2c9db6afe1d67b98fab46d39326782505
```

## Discover Docker-assigned ephemeral loopback port
- Command: `docker port ac-p01-88227-1791511140 5432/tcp`
- Exit code: 0
```text
127.0.0.1:54868
```

## Isolated PostgreSQL readiness
- Exit code: 0
```text
/var/run/postgresql:5432 - accepting connections
```

## Upgrade empty DB to Phase 01 baseline only
- Command: `uv run --project /var/folders/nf/t8dhz5mx2pbgswwr4mk99_mr0000gq/T/agent-corp-p01-remake-sog3opcc/project/apps/api alembic -c /var/folders/nf/t8dhz5mx2pbgswwr4mk99_mr0000gq/T/agent-corp-p01-remake-sog3opcc/project/apps/api/alembic.ini upgrade 20261008_0001`
- Exit code: 0
```text
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 20261008_0001, Establish the empty Phase 01 schema baseline.
```

## Read current migration revision
- Command: `uv run --project /var/folders/nf/t8dhz5mx2pbgswwr4mk99_mr0000gq/T/agent-corp-p01-remake-sog3opcc/project/apps/api alembic -c /var/folders/nf/t8dhz5mx2pbgswwr4mk99_mr0000gq/T/agent-corp-p01-remake-sog3opcc/project/apps/api/alembic.ini current`
- Exit code: 0
```text
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
20261008_0001
```

## Inspect public schema tables
- Command: `docker exec ac-p01-88227-1791511140 psql -U postgres -d p01_clean -Atc SELECT string_agg(tablename, ',' ORDER BY tablename) FROM pg_tables WHERE schemaname='public'`
- Exit code: 0
```text
alembic_version
```

## Idempotent repeat at Phase 01 baseline
- Command: `uv run --project /var/folders/nf/t8dhz5mx2pbgswwr4mk99_mr0000gq/T/agent-corp-p01-remake-sog3opcc/project/apps/api alembic -c /var/folders/nf/t8dhz5mx2pbgswwr4mk99_mr0000gq/T/agent-corp-p01-remake-sog3opcc/project/apps/api/alembic.ini upgrade 20261008_0001`
- Exit code: 0
```text
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
```

## Isolated target
- Container: ac-p01-88227-1791511140
- Image: postgres:18.6-alpine@sha256:77f585114c32fbca283dc835b0596f4e52b51b4c6662d7810b2f4084f60a1873
- Published interface: 127.0.0.1:54868
- Database: p01_clean (new container; no project volume)
- Baseline schema tables: alembic_version
- Cleanup: container stopped and temporary project copy removed.
