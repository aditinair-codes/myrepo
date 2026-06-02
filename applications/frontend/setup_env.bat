@echo off
title FirstStep.ai Designer - Environment Setup
echo =======================================================================
echo         Setting Up Python Virtual Environment & Dependencies
echo =======================================================================
echo.

:: Change directory to current batch directory
cd %~dp0

:: Check and create virtual environment
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    echo [INFO] Virtual environment created successfully.
) else (
    echo [INFO] Virtual environment already exists.
)

:: Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

:: Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

:: Install requirements
echo [INFO] Installing requirements...
python -m pip install -r ..\..\requirements.txt

echo.
echo =======================================================================
echo [SUCCESS] Setup completed! You can now run 001_run.bat
echo =======================================================================
pause
