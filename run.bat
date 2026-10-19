@echo off
setlocal
cd /d "%~dp0"
where docker >nul 2>nul || (echo Can Docker Desktop va Docker Compose v2.& exit /b 1)
docker info >nul 2>nul || (echo Hay khoi dong Docker Desktop.& exit /b 1)
docker compose -f compose.bootstrap.yml run --rm bootstrap
if errorlevel 1 exit /b 1
docker compose config --quiet
if errorlevel 1 exit /b 1
docker compose up --build --wait
if errorlevel 1 exit /b 1
echo.
echo Ung dung da san sang: http://agent-corporation.localhost
echo Truc tiep: http://127.0.0.1:15500
echo Dung ung dung bang: docker compose stop web api
docker compose logs --follow --tail=50 api web
endlocal
