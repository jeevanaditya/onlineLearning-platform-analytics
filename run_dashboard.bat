@echo off
cd /d "%~dp0"
python --version >nul 2>&1 || (
    echo Python not found. Install from https://www.python.org/downloads/ and check "Add Python to PATH"
    pause
    exit /b 1
)
echo Installing dependencies...
python -m pip install -q -r requirements.txt
echo Starting dashboard at http://localhost:8501
python -m streamlit run dashboard/app.py --server.headless true
pause
