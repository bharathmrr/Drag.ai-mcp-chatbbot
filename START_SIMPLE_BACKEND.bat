@echo off
echo ================================================================================
echo  AI-MCP ORCHESTRATOR - SIMPLE BACKEND (FOR TESTING)
echo ================================================================================
echo.

cd backend

echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [2/3] Installing minimal dependencies...
pip install fastapi uvicorn --quiet

echo.
echo [3/3] Starting simple test server...
echo.
echo ================================================================================
python simple_server.py

pause
