@echo off
REM ==============================================================================
REM Claude Voice Assistant - Setup Script (Windows)
REM ==============================================================================
REM This script creates a virtual environment and installs all dependencies.
REM
REM Usage:
REM   Double-click setup.bat or run from command prompt
REM
REM After setup, run:
REM   run.bat
REM ==============================================================================

echo ==============================================
echo   Claude Voice Assistant - Setup
echo ==============================================
echo.

REM Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Found Python:
python --version
echo.

REM Create virtual environment
echo [1/4] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)

REM Activate virtual environment
echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo [3/4] Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo [4/4] Installing dependencies (this may take a few minutes)...
echo    - Flask (web server)
echo    - flask-cors (cross-origin support)
echo    - openai-whisper (speech recognition)
echo    - anthropic (Claude API)
echo.

pip install flask flask-cors openai-whisper anthropic

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo ==============================================
echo   Setup Complete!
echo ==============================================
echo.
echo Next steps:
echo.
echo   1. Set your Anthropic API key:
echo      set ANTHROPIC_API_KEY=your-api-key-here
echo.
echo   2. Run the application:
echo      run.bat
echo.
echo   Or manually:
echo      venv\Scripts\activate.bat
echo      python server.py
echo.
echo ==============================================
pause
