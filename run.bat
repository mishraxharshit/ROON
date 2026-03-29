@echo off
if not exist "venv\" (
    echo Run setup_and_run.bat first!
    pause & exit /b 1
)
call venv\Scripts\activate.bat
start "" pythonw pdf_reader.py
if errorlevel 1 python pdf_reader.py
deactivate
