#!/bin/bash
set -e

echo "=================================================="
echo "Unified AI Verification API - Linux/macOS Setup"
echo "=================================================="

echo "[1/4] Checking Python installation..."
if ! command -v python3 &> /dev/null
then
    echo "[ERROR] python3 could not be found."
    exit 1
fi

echo "[2/4] Setting up Virtual Environment (venv)..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created successfully."
else
    echo "Virtual environment already exists. Skipping..."
fi

echo "[3/4] Installing dependencies from requirements.txt..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "[4/4] Setting up local FFmpeg binary..."
python scripts/install_ffmpeg.py

if [ ! -f ".env" ]; then
    echo "=================================================="
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "[IMPORTANT] Please open the .env file and fill in your credentials!"
fi

echo "=================================================="
echo "Setup Complete!"
echo "To start the server, run:"
echo "source venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
echo "=================================================="
