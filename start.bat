@echo off
echo ========================================
echo   AI-MCP Orchestrator - Startup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)

echo [1/4] Setting up Backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
echo Installing backend dependencies...
pip install -r requirements.txt --quiet

REM Copy .env if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
)

REM Start backend in new window
echo Starting backend server...
start "AI-MCP Backend" cmd /k "cd /d %CD% && venv\Scripts\activate && python main.py"

cd ..

echo.
echo [2/4] Setting up Frontend...
cd frontend

REM Install dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
)

REM Start frontend in new window
echo Starting frontend server...
start "AI-MCP Frontend" cmd /k "cd /d %CD% && npm run dev"

cd ..

echo.
echo ========================================
echo   AI-MCP Orchestrator Started!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to open the application in your browser...
pause >nul

REM Open browser
start http://localhost:3000

echo.
echo Application is running!
echo Close the terminal windows to stop the servers.
echo.
pause
