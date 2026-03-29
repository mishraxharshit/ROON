@echo off
title Roon - First Time Setup
color 0A
echo.
echo  ============================================
echo    Roon v1.0 - Setup
echo  ============================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found!
    echo.
    echo  Please install Python from:
    echo  https://python.org/downloads
    echo.
    echo  IMPORTANT: Check "Add Python to PATH"
    echo  during installation!
    echo.
    pause & exit /b 1
)

for /f "tokens=2" %%v in ('python --version') do set PYVER=%%v
echo  [OK] Python %PYVER% found

if not exist "venv\" (
    echo  [1/3] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo  [ERROR] Could not create venv
        pause & exit /b 1
    )
) else (
    echo  [1/3] Virtual environment ready
)

call venv\Scripts\activate.bat

echo  [2/3] Installing libraries (first time may take a moment)...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo  [ERROR] Library installation failed
    pause & exit /b 1
)

echo  [3/3] Generating app icon...
python generate_icon.py >nul 2>&1

echo.
echo  ============================================
echo    Setup complete! Launching app...
echo  ============================================
echo.

start "" pythonw pdf_reader.py
if errorlevel 1 python pdf_reader.py

deactivate
