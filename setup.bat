@echo off
echo ==================================================
echo Unified AI Verification API - Windows Setup
echo ==================================================

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to PATH.
    pause
    exit /b
)

echo [2/4] Setting up Virtual Environment (venv)...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created successfully.
) else (
    echo Virtual environment already exists. Skipping...
)

echo [3/4] Installing dependencies from requirements.txt...
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

echo [4/4] Setting up local FFmpeg binary...
python scripts\install_ffmpeg.py

if not exist ".env" (
    echo ==================================================
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo [IMPORTANT] Please open the .env file and fill in your credentials!
)

echo ==================================================
echo Setup Complete! 
echo To start the server, run:
echo venv\Scripts\uvicorn.exe app.main:app --host 0.0.0.0 --port 8000 --reload
echo ==================================================
pause
