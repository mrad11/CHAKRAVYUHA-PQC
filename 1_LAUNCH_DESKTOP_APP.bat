@echo off
title CHAKRAVYUHA PQC // NATIVE DESKTOP ENCLAVE
cd /d "%~dp0"

echo ======================================================================
echo   CHAKRAVYUHA PQC // NATIVE DESKTOP ENCLAVE LAUNCHER
echo   Ministry of Defence - Problem Statement 237
echo   Status: 100%% Offline / Standalone Window / Zero External Cloud
echo ======================================================================
echo.

:: Detect Python executable with multiple fallback paths
set "PY_CMD="
if exist "C:\Program Files\Python313\python.exe" set "PY_CMD=C:\Program Files\Python313\python.exe"
if "%PY_CMD%"=="" where py.exe >nul 2>&1 && set "PY_CMD=py -3"
if "%PY_CMD%"=="" where python.exe >nul 2>&1 && set "PY_CMD=python"
if "%PY_CMD%"=="" if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" set "PY_CMD=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
if "%PY_CMD%"=="" if exist "C:\Program Files\Python312\python.exe" set "PY_CMD=C:\Program Files\Python312\python.exe"
if "%PY_CMD%"=="" if exist "C:\Program Files\Python311\python.exe" set "PY_CMD=C:\Program Files\Python311\python.exe"

if "%PY_CMD%"=="" (
    echo [ERROR] Python 3.10+ is required but was not found on this system!
    echo Please install Python from https://www.python.org/
    echo.
    pause
    exit /b 1
)

echo [*] Python executable: %PY_CMD%
echo [*] Launching sovereign desktop application window...
echo.

"%PY_CMD%" run_desktop_app.py

if errorlevel 1 (
    echo.
    echo [!] Desktop app exited with an error. Falling back to Web Dashboard launcher...
    "%PY_CMD%" run_web.py
)

echo.
pause
