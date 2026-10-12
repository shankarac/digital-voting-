@echo off
setlocal
cd /d "%~dp0"

echo Setting up backend...
python -m venv env
if errorlevel 1 exit /b 1
call env\Scripts\activate.bat
python -m pip install -r requirements.txt
if errorlevel 1 exit /b 1
python -m alembic upgrade head
if errorlevel 1 exit /b 1
python -m app.seed_demo
if errorlevel 1 exit /b 1

echo Setting up frontend...
pushd frontend
call npm install
if errorlevel 1 exit /b 1
popd

echo Setup complete.
endlocal
