@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo.
echo ==========================================
echo     JobTrack - AI Job Application Tracker
echo ==========================================
echo.

:: Check if .env file exists and has an API key
set "HAS_KEY=0"
if exist .env (
    for /f "tokens=1,* delims==" %%a in (.env) do (
        if "%%a"=="ANTHROPIC_API_KEY" (
            set "KEY_VALUE=%%b"
            if defined KEY_VALUE (
                echo %%b | findstr /B "sk-ant" >nul 2>&1
                if !errorlevel! equ 0 (
                    set "HAS_KEY=1"
                    echo [OK] API key found
                )
            )
        )
    )
)

:: If no valid API key, prompt the user
if "!HAS_KEY!"=="0" (
    echo ============================================
    echo   FIRST TIME SETUP - API Key Required
    echo ============================================
    echo.
    echo JobTrack uses Claude AI to analyze resumes
    echo and generate cover letters.
    echo.
    echo Get your API key at:
    echo   https://console.anthropic.com/settings/keys
    echo.
    echo ^(Anthropic offers free credits to start^)
    echo.
    echo ============================================
    echo.
    
    set /p "API_KEY=Paste your API key (starts with sk-ant-): "
    
    if defined API_KEY (
        echo !API_KEY! | findstr /B "sk-ant" >nul 2>&1
        if !errorlevel! equ 0 (
            echo ANTHROPIC_API_KEY=!API_KEY!> .env
            echo.
            echo [OK] API key saved!
            echo.
        ) else (
            echo.
            echo [WARNING] Key doesn't look valid - should start with sk-ant
            echo           Saving anyway...
            echo ANTHROPIC_API_KEY=!API_KEY!> .env
            echo.
        )
    ) else (
        echo.
        echo [ERROR] No API key entered. AI features won't work.
        echo         Run start.bat again to enter your key.
        echo.
        pause
        exit /b 1
    )
)

:: Check if Python is installed
echo.
echo [CHECK] Looking for Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python is not installed or not in PATH.
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)
python --version
echo [OK] Python found!

:: Install dependencies if needed
if not exist ".deps_installed" (
    echo.
    echo [SETUP] Installing dependencies - this may take a minute...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to install dependencies.
        echo.
        pause
        exit /b 1
    )
    echo. > .deps_installed
    echo.
    echo [OK] Dependencies installed!
)

echo.
echo ==========================================
echo     Starting JobTrack...
echo ==========================================
echo.
echo Open your browser to: http://localhost:8000
echo.
echo To stop: Close this window or press Ctrl+C
echo ==========================================
echo.

:: Start the server
python -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

:: If we get here, the server stopped or crashed
echo.
echo ==========================================
echo Server stopped or encountered an error.
echo ==========================================
echo.
pause
