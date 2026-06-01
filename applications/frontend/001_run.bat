@echo off
title FirstStep.ai Designer - Frontend Local Launcher
echo =======================================================================
echo              Starting Local Frontend Server (Inside Context)
echo =======================================================================
echo.

:: Change directory to current batch directory
cd %~dp0

:: Check virtual environment
if not exist "venv" (
    echo [INFO] No virtual environment found at applications\frontend\venv. Creating...
    python -m venv venv
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    python -m pip install -r ..\..\requirements.txt
) else (
    call venv\Scripts\activate.bat
)

:: Run the script
python main.py
pause
