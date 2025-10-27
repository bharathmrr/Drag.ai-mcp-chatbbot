@echo off
echo ================================================================================
echo  AI-MCP ORCHESTRATOR - BACKEND SETUP
echo ================================================================================
echo.

cd backend

echo [1/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [2/4] Installing core dependencies...
pip install fastapi uvicorn pydantic pydantic-settings python-dotenv --quiet

echo.
echo [3/4] Installing AI & tool dependencies...
pip install langchain langchain-google-genai google-generativeai --quiet
pip install wikipedia screeninfo psutil --quiet

echo.
echo [4/4] Starting backend server...
echo.
echo ================================================================================
python main.py

pause
