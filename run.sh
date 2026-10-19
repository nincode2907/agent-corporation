#!/usr/bin/env bash
set -Eeuo pipefail
ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"
export BOOTSTRAP_UID="$(id -u)"
export BOOTSTRAP_GID="$(id -g)"
command -v docker >/dev/null 2>&1 || { printf 'Cần Docker Desktop và Docker Compose v2.\n' >&2; exit 1; }
docker info >/dev/null 2>&1 || { printf 'Hãy khởi động Docker Desktop.\n' >&2; exit 1; }
docker compose -f compose.bootstrap.yml run --rm bootstrap
docker compose config --quiet
docker compose up --build --wait
printf '\nỨng dụng đã sẵn sàng: http://agent-corporation.localhost\nTrực tiếp: http://127.0.0.1:15500\nCtrl+C dừng web/API; PostgreSQL giữ dữ liệu và tiếp tục chạy.\n\n'
trap 'docker compose stop web api' EXIT
docker compose logs --follow --tail=50 api web
