@echo off
echo ================================================================================
echo  PUSH AI-MCP ORCHESTRATOR TO GITHUB
echo ================================================================================
echo.

echo [Step 1/5] Initializing Git repository...
git init

echo.
echo [Step 2/5] Adding all files...
git add .

echo.
echo [Step 3/5] Creating initial commit...
git commit -m "Initial commit: AI-MCP Orchestrator with Gemini 2.0 Flash and 17 MCP Tools"

echo.
echo [Step 4/5] Adding GitHub remote...
echo Enter your GitHub username (default: bharathmrr):
set /p GITHUB_USER=
if "%GITHUB_USER%"=="" set GITHUB_USER=bharathmrr

git remote add origin https://github.com/%GITHUB_USER%/Drag.ai-mcp-chatbbot.git

echo.
echo [Step 5/5] Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo ================================================================================
echo  SUCCESS! Your code is now on GitHub!
echo ================================================================================
echo.
echo  Repository: https://github.com/%GITHUB_USER%/Drag.ai-mcp-chatbbot
echo  Actions: https://github.com/%GITHUB_USER%/Drag.ai-mcp-chatbbot/actions
echo.
echo  Next Steps:
echo  1. Go to GitHub repository settings
echo  2. Add secrets: DOCKER_USERNAME, DOCKER_PASSWORD
echo  3. Watch CI/CD pipeline run automatically!
echo.
echo ================================================================================

pause
