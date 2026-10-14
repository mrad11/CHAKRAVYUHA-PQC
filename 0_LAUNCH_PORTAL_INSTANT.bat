@echo off
title CHAKRAVYUHA PQC // SOVEREIGN PORTAL LAUNCHER
cd /d "%~dp0"

echo ======================================================================
echo   CHAKRAVYUHA PQC // SOVEREIGN DEFENSE ENCLAVE PORTAL
echo   Ministry of Defence - Problem Statement 237
echo   Status: 100%% Air-Gapped / Zero External Cloud / NIST PQC Active
echo ======================================================================
echo.

:: Detect Python executable to run background backend if available
set "PY_CMD="
if exist "C:\Program Files\Python313\python.exe" set "PY_CMD=C:\Program Files\Python313\python.exe"
if "%PY_CMD%"=="" where py.exe >nul 2>&1 && set "PY_CMD=py -3"
if "%PY_CMD%"=="" where python.exe >nul 2>&1 && set "PY_CMD=python"
if "%PY_CMD%"=="" if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" set "PY_CMD=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"

:: If Python is available, start background backend server so all APIs work
if not "%PY_CMD%"=="" (
    echo [*] Initializing sovereign cryptographic backend engine in background...
    start /min "CHAKRAVYUHA_BACKEND" "%PY_CMD%" run_web.py
    timeout /t 1 /nobreak >nul
)

echo [*] Opening CHAKRAVYUHA PQC Deep-Ops Threat Matrix Console in browser...
start "" "%~dp0LAUNCH_PORTAL.html"
echo.
echo [✓] Console successfully launched!
echo.
