@echo off
REM Phantombuster Webhook Downloader Script for Windows
REM Usage: download_files.bat [webhook_url] [download_dir]

setlocal

REM Default values
set WEBHOOK_URL=%1
if "%WEBHOOK_URL%"=="" set WEBHOOK_URL=http://localhost:5000

set DOWNLOAD_DIR=%2
if "%DOWNLOAD_DIR%"=="" set DOWNLOAD_DIR=downloaded_files

echo Phantombuster Webhook Downloader
echo =================================
echo Webhook URL: %WEBHOOK_URL%
echo Download directory: %DOWNLOAD_DIR%
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is required but not installed.
    exit /b 1
)

REM Check if required Python packages are available
python -c "import requests" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required Python packages...
    pip install requests
)

REM Run the downloader
echo Starting download...
python download_from_webhook.py "%WEBHOOK_URL%" "%DOWNLOAD_DIR%"

echo Script completed.
pause
