
@echo off
setlocal
title ShadowLedger - Flask Server

REM Move to the project directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo First-time setup...

    REM Run Windows setup script if available
    if exist "setup.bat" (
        call setup.bat
    ) else (
        echo Creating virtual environment...
        py -3 -m venv .venv
        if errorlevel 1 goto :error

        echo Installing dependencies...
        ".venv\Scripts\python.exe" -m pip install -r requirements.txt
        if errorlevel 1 goto :error
    )
)

echo.
echo Starting ShadowLedger...
echo Website: http://127.0.0.1:5002/
echo Press Ctrl+C to stop.
echo.

REM Open browser after a short delay
start "" powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 3; Start-Process 'http://127.0.0.1:5002/'"

REM Start Flask server
".venv\Scripts\python.exe" -m flask --app app run --host 127.0.0.1 --port 5002

echo.
echo Flask server stopped.
pause
exit /b 0

:error
echo.
echo Setup failed. Check Python and dependencies.
pause
exit /b 1
