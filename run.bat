@echo off
REM ==============================================================================
REM Claude Voice Assistant - Run Script (Windows)
REM ==============================================================================
REM This script activates the virtual environment and starts the server.
REM
REM Make sure to set your API key first:
REM   set ANTHROPIC_API_KEY=your-api-key-here
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

REM Check for API key
if "%ANTHROPIC_API_KEY%"=="" (
    echo [WARNING] ANTHROPIC_API_KEY is not set.
    echo.
    echo Please set it with:
    echo   set ANTHROPIC_API_KEY=your-api-key-here
    echo.
    echo Or enter it now:
    set /p ANTHROPIC_API_KEY="API Key: "
    echo.
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
