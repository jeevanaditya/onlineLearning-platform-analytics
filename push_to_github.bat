@echo off
cd /d "%~dp0"
echo Pushing to GitHub - you may be asked to sign in.
echo.
"C:\Program Files\Git\bin\git.exe" push -u origin main
echo.
pause
