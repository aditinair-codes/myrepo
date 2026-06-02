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
    echo [ERROR] Virtual environment not found!
    echo [INFO] Please run setup_env.bat first to set up the environment.
    echo.
    pause
    exit /b 1
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run the script
echo [INFO] Starting FastAPI server...
python main.py
pause
