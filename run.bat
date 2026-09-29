@echo off
REM Launcher script for sherpa-onnx real-time microphone app

cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo [Setup] Virtual environment not found. Creating venv...
    python -m venv venv
    echo [Setup] Installing requirements...
    call .\venv\Scripts\pip install -r requirements.txt
)

set PYTHONUNBUFFERED=1
REM Run application forwarding any command line arguments
.\venv\Scripts\python.exe main.py %*
