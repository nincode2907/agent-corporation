#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

for command_name in python3 docker uv npm; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    printf 'Thiếu lệnh cần thiết: %s\n' "$command_name" >&2
    exit 1
  fi
done

if [[ ! -f .env ]]; then
  python3 scripts/bootstrap_local.py
fi

docker compose up -d postgres
uv sync --project apps/api --locked
if [[ ! -d apps/web/node_modules ]]; then
  npm --prefix apps/web ci
fi
uv run --project apps/api alembic -c apps/api/alembic.ini upgrade head

printf '\nAgent Corporation đang chạy. Web: http://127.0.0.1:15500\nNhấn Ctrl+C để dừng API và web. PostgreSQL vẫn chạy nền.\n\n'

api_pid=''
web_pid=''
stop_children() {
  trap - INT TERM EXIT
  if [[ -n "$api_pid" ]] && kill -0 "$api_pid" 2>/dev/null; then
    kill "$api_pid" 2>/dev/null || true
  fi
  if [[ -n "$web_pid" ]] && kill -0 "$web_pid" 2>/dev/null; then
    kill "$web_pid" 2>/dev/null || true
  fi
  [[ -z "$api_pid" ]] || wait "$api_pid" 2>/dev/null || true
  [[ -z "$web_pid" ]] || wait "$web_pid" 2>/dev/null || true
}
trap stop_children INT TERM EXIT

uv run --project apps/api uvicorn agent_corporation_api.main:app \
  --app-dir apps/api/src --host 127.0.0.1 --port 15501 &
api_pid=$!
npm run --prefix apps/web dev &
web_pid=$!

while kill -0 "$api_pid" 2>/dev/null && kill -0 "$web_pid" 2>/dev/null; do
  sleep 1
done

if ! kill -0 "$api_pid" 2>/dev/null; then
  wait "$api_pid" || status=$?
  printf 'API đã dừng; đóng web.\n' >&2
else
  wait "$web_pid" || status=$?
  printf 'Web đã dừng; đóng API.\n' >&2
fi
exit "${status:-1}"
