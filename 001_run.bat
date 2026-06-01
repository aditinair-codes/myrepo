@echo off
title FirstStep.ai Designer Tool - Startup
echo =======================================================================
echo              Starting FirstStep.ai Designer Tool Server
echo =======================================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

:: Virtual environment directory
set VENV_DIR=applications\frontend\venv

:: Create venv if it doesn't exist
if not exist "%VENV_DIR%" (
    echo [INFO] Creating Python virtual environment in %VENV_DIR%...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [INFO] Virtual environment created successfully.
)

:: Activate virtual environment
echo [INFO] Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"

:: Install/Upgrade dependencies
echo [INFO] Upgrading pip and installing requirements...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install required packages!
    pause
    exit /b 1
)

:: Run the application
echo [INFO] Starting FastAPI App...
echo.
python main.py

pause
