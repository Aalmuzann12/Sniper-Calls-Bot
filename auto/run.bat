@echo off
echo Running Python project...
echo.

REM 
cd /d "%~dp0"

REM 
if not exist "venv" (
    echo Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM 
if not exist "main.py" (
    echo main.py not found in project root!
    pause
    exit /b 1
)

REM
call "venv\Scripts\activate.bat"
echo Virtual environment activated
echo Running main.py...
echo.

"venv\Scripts\python.exe" main.py

echo.
echo Program finished. Press any key to exit...
pause