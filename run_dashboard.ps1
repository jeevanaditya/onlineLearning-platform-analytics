# Run Online Learning Platform Analytics Dashboard
# Usage: .\run_dashboard.ps1   (or right-click -> Run with PowerShell)

Set-Location $PSScriptRoot

# Install dependencies if needed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python not found. Please install Python 3.10+ and add it to PATH."
    Write-Host "Download: https://www.python.org/downloads/"
    exit 1
}

Write-Host "Installing dependencies..."
python -m pip install -q -r requirements.txt

Write-Host "Starting dashboard at http://localhost:8501"
python -m streamlit run dashboard/app.py --server.headless true
