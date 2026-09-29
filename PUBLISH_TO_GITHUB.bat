@echo off
title CHAKRAVYUHA PQC - Publish to GitHub
color 0B
echo =====================================================================
echo       CHAKRAVYUHA PQC : 1-CLICK GITHUB PUBLISHER
echo       Ministry of Defence - SIH Problem Statement 237
echo =====================================================================
echo.

set "GIT_EXE=C:\Users\aadid\AppData\Local\GitHubDesktop\app-3.6.5\resources\app\git\cmd\git.exe"
if not exist "%GIT_EXE%" (
    set "GIT_EXE=git"
)

echo [*] Checking local git status...
"%GIT_EXE%" status >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [*] Initializing git repository...
    "%GIT_EXE%" init
    "%GIT_EXE%" branch -M main
)

echo.
echo [1] Enter your GitHub Repository URL (e.g. https://github.com/USERNAME/CHAKRAVYUHA-PQC.git)
echo     OR press ENTER to skip remote push and manage via GitHub Desktop.
set /p REPO_URL="Repository URL: "

if not "%REPO_URL%"=="" (
    echo [*] Adding remote origin...
    "%GIT_EXE%" remote remove origin >nul 2>&1
    "%GIT_EXE%" remote add origin %REPO_URL%
    echo [*] Committing latest changes...
    "%GIT_EXE%" add .
    "%GIT_EXE%" commit -m "feat: Official Release of CHAKRAVYUHA PQC Defense Enclave (MoD PS 237)"
    echo [*] Pushing to GitHub (main branch)...
    "%GIT_EXE%" push -u origin main
    echo.
    echo [OK] Successfully published to GitHub!
) else (
    echo.
    echo [*] Skipping direct push. You can drag and drop this folder directly into GitHub Desktop!
)

echo.
pause
