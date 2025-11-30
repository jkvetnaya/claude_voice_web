@echo off
REM ==============================================================================
REM Claude Voice Assistant - Run Script (Windows)
REM ==============================================================================
REM This script activates the virtual environment and starts the server.
REM API key is read from .env file automatically.
REM ==============================================================================

echo ==============================================
echo   Claude Voice Assistant
echo ==============================================
echo.

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found.
    echo Please run setup.bat first.
    pause
    exit /b 1
)

REM Check if .env exists
if not exist ".env" (
    echo [ERROR] .env file not found.
    echo Please create it from the example:
    echo   copy .env.example .env
    echo   notepad .env
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

echo Starting server...
echo Open http://localhost:5000 in your browser
echo.
echo Press Ctrl+C to stop the server
echo ==============================================
echo.

python server.py

pause
