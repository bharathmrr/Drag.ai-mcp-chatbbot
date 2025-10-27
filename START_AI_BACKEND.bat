@echo off
echo ================================================================================
echo  AI-MCP ORCHESTRATOR - REAL AI BACKEND (GEMINI 2.0 FLASH)
echo ================================================================================
echo.

cd backend

echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [2/3] Installing required packages...
pip install google-generativeai --quiet

echo.
echo [3/3] Starting AI-powered backend server with real tool integration...
echo.
echo ================================================================================
python real_ai_server.py

pause
