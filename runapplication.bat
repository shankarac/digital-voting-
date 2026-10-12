@echo off
setlocal
cd /d "%~dp0"

if not exist "env\Scripts\activate.bat" (
  echo Run setupdev.bat first.
  exit /b 1
)

set "ROOT=%~dp0"
if "%ROOT:~-1%"=="\" set "ROOT=%ROOT:~0,-1%"

echo Stopping any old backend on port 8000...
powershell -NoProfile -Command "$c = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -First 1; if ($c) { Stop-Process -Id $c.OwningProcess -Force -ErrorAction SilentlyContinue }"

echo Starting backend...
start "Voting Backend" /D "%ROOT%" cmd /k "call env\Scripts\activate.bat && python -m alembic upgrade head && python -m app.seed_demo && python main.py"

echo Waiting for the API...
set /a TRIES=0
:waitloop
set /a TRIES+=1
if %TRIES% GTR 30 (
  echo Backend did not respond. Check the Voting Backend window.
  goto frontend
)
powershell -NoProfile -Command "Start-Sleep -Seconds 1"
powershell -NoProfile -Command "try { (Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/openapi.json).StatusCode; exit 0 } catch { exit 1 }"
if errorlevel 1 goto waitloop

:frontend
echo Starting frontend...
cd frontend
call npm start
endlocal
