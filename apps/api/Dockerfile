FROM python:3.14.8-slim@sha256:a2b82f3c48559aa0a8446d9af49826b6e2b2016f4cd2afabfe6013ec53729170 AS build
ENV UV_PYTHON_DOWNLOADS=never UV_LINK_MODE=copy
WORKDIR /app
RUN pip install --no-cache-dir uv==0.12.23
COPY apps/api/pyproject.toml apps/api/uv.lock apps/api/
RUN uv sync --project apps/api --locked --no-dev --no-install-project --no-managed-python

FROM build AS test
RUN uv sync --project apps/api --locked --no-install-project --no-managed-python
COPY apps/api apps/api
COPY scripts scripts
ENV PYTHONPATH=/app/apps/api/src
CMD ["uv", "run", "--project", "apps/api", "pytest"]

FROM python:3.14.8-slim@sha256:a2b82f3c48559aa0a8446d9af49826b6e2b2016f4cd2afabfe6013ec53729170 AS runtime
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 \
    PATH=/app/apps/api/.venv/bin:$PATH PYTHONPATH=/app/apps/api/src
WORKDIR /app
COPY --from=build /app/apps/api/.venv apps/api/.venv
COPY apps/api/src apps/api/src
COPY apps/api/migrations apps/api/migrations
COPY apps/api/alembic.ini apps/api/alembic.ini
COPY scripts/docker_init_secrets.py scripts/docker_init_secrets.py
COPY scripts/cg01_mode.py scripts/cg01_mode.py
RUN mkdir -p /app/storage && chown 1000:1000 /app/storage
USER 1000:1000
EXPOSE 15501
CMD ["python", "-m", "uvicorn", "agent_corporation_api.main:app", "--host", "0.0.0.0", "--port", "15501", "--no-proxy-headers"]
