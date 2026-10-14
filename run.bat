@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>nul || (echo Thieu Python trong PATH.& exit /b 1)
where docker >nul 2>nul || (echo Thieu Docker Compose trong PATH.& exit /b 1)
where uv >nul 2>nul || (echo Thieu uv trong PATH.& exit /b 1)
where npm >nul 2>nul || (echo Thieu npm trong PATH.& exit /b 1)

if not exist .env (
  python scripts\bootstrap_local.py
  if errorlevel 1 exit /b 1
)

docker compose up -d postgres
if errorlevel 1 exit /b 1
uv sync --project apps/api --locked
if errorlevel 1 exit /b 1
if not exist apps\web\node_modules (
  call npm --prefix apps/web ci
  if errorlevel 1 exit /b 1
)
uv run --project apps/api alembic -c apps/api/alembic.ini upgrade head
if errorlevel 1 exit /b 1

start "Agent Corporation API" /D "%~dp0" cmd /k uv run --project apps/api uvicorn agent_corporation_api.main:app --app-dir apps/api/src --host 127.0.0.1 --port 15501
start "Agent Corporation Web" /D "%~dp0" cmd /k npm run --prefix apps/web dev

echo.
echo Agent Corporation dang chay.
echo Web: http://127.0.0.1:15500
echo Dong hai cua so API va Web de dung ung dung. PostgreSQL van chay nen.
endlocal
