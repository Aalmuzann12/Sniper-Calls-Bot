@echo off
chcp 65001 >nul
echo Setting up Python project for Windows...
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Starting installation...
    echo.
    
    REM Download Python
    echo Downloading Python...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe' -OutFile 'python_installer.exe'"
    
    if not exist python_installer.exe (
        echo Error downloading Python!
        pause
        exit /b 1
    )
    
    echo Installing Python...
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    REM Wait for installation to complete
    timeout /t 10 /nobreak >nul
    
    REM Refresh PATH
    call refreshenv.cmd 2>nul || (
        echo Please restart command prompt after Python installation
        pause
        exit /b 1
    )
    
    del python_installer.exe
    echo Python installed successfully!
    echo.
) else (
    echo Python found:
    python --version
    echo.
)

REM Check pip
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing pip...
    python -m ensurepip --upgrade
    echo.
)

REM Create virtual environment
if exist venv (
    echo Virtual environment already exists
    echo.
) else (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Error creating virtual environment!
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
    echo.
)

REM Activate and install dependencies
echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat

REM Update pip
python -m pip install --upgrade pip

REM Install dependencies if requirements.txt exists
if exist requirements.txt (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
) else (
    echo requirements.txt not found, skipping dependency installation
)

echo.
echo ===== SETUP COMPLETED =====
echo To run the project use: run.bat
echo.
pause