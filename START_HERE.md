# 🚀 Quick Start Guide - AI-MCP Orchestrator

## ✨ Complete Setup in 2 Steps

### Step 1: Start AI Backend
**Double-click:** `START_AI_BACKEND.bat`

**What it does:**
1. Activates Python virtual environment
2. Installs `google-generativeai` package
3. Starts AI-powered backend with Gemini 2.0 Flash

**Expected output:**
```
================================================================================
🚀 AI-MCP SERVER WITH GEMINI 2.0 FLASH
================================================================================
   • API: http://localhost:8000
   • Docs: http://localhost:8000/docs
   • Health: http://localhost:8000/health
   • Tools: http://localhost:8000/api/mcp/tools
   • AI Model: Gemini 2.0 Flash Exp
================================================================================

INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this window open!**

---

### Step 2: Start Frontend
**Double-click:** `START_FRONTEND.bat`

**What it does:**
1. Starts Vite development server
2. Opens frontend on port 3000

**Expected output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

**Keep this window open too!**

---

### Step 3: Open Browser
```
http://localhost:3000
```

---

## 🎯 What You'll See

### 1. **Futuristic Header**
- "AI-MCP Orchestrator"
- "Powered by Gemini 2.0 Flash"
- MCP Tools button

### 2. **Sidebar** (Left)
- 🏠 Home
- 💬 Sessions (Chat)
- 🔧 Tools (MCP Info)
- 📝 Logs (Chat History)
- ⚙️ Settings

### 3. **Main Panel** (Center)
- Welcome card or Chat interface
- Streaming AI responses

### 4. **MCP Tools Panel** (Right)
- 17 tool cards with toggle switches
- Real-time status (🟢 ON / 🔴 OFF)
- Active/Total stats

### 5. **Starfield Background**
- 200 twinkling stars
- Shooting stars

---

## 💬 Try These Queries

### Weather
```
"What's the weather in Tokyo?"
"Tell me the climate in Hyderabad"
```

### Search
```
"Search for latest AI news"
"Find top 5 news stories today"
```

### Wikipedia
```
"Tell me about quantum computing"
"What is artificial intelligence?"
```

### Calculator
```
"Calculate 25 * 4 + 10"
"What is 15% of 200?"
```

### System
```
"Show me my CPU usage"
"What's my system status?"
```

### General
```
"How can you help me?"
"What tools do you have?"
```

---

## 🔧 Troubleshooting

### Problem: Backend won't start

**Error:** `ModuleNotFoundError: No module named 'google.generativeai'`

**Solution:** The batch file will install it automatically. If it fails:
```bash
cd backend
venv\Scripts\activate
pip install google-generativeai
python ai_server.py
```

### Problem: Port 8000 already in use

**Solution:** Kill existing Python processes:
```bash
Get-Process | Where-Object {$_.ProcessName -eq "python"} | Stop-Process -Force
```

Then restart `START_AI_BACKEND.bat`

### Problem: Frontend shows "Network Error"

**Solution:**
1. Ensure backend is running (check Step 1)
2. Verify: http://localhost:8000/health
3. Refresh browser (Ctrl+F5)

### Problem: MCP Tools not showing

**Solution:**
1. Backend must be running first
2. Check: http://localhost:8000/api/mcp/tools
3. Should return JSON with 17 tools
4. Refresh frontend

---

## 📁 File Structure

```
Drag.ai-mcp-chatbbot/
├── START_AI_BACKEND.bat      ← Start this first
├── START_FRONTEND.bat         ← Start this second
├── START_HERE.md              ← This file
│
├── backend/
│   ├── ai_server.py           ← Real AI server (Gemini)
│   ├── simple_server.py       ← Mock server (testing)
│   ├── config.py              ← API key configuration
│   └── requirements.txt       ← Python dependencies
│
└── frontend/
    ├── src/
    │   ├── App.jsx            ← Main app
    │   ├── components/        ← UI components
    │   └── styles/            ← CSS styles
    └── package.json           ← Node dependencies
```

---

## 🎨 Features

### AI-Powered
- ✅ Real Gemini 2.0 Flash responses
- ✅ Context-aware conversations
- ✅ Tool integration
- ✅ Streaming text display

### Beautiful UI
- ✅ Futuristic dark theme
- ✅ Starfield background
- ✅ Glassmorphism design
- ✅ Smooth animations
- ✅ Neon glows

### MCP Tools
- ✅ 17 integrated tools
- ✅ Toggle ON/OFF
- ✅ Real-time status
- ✅ Live statistics

---

## 🔑 API Key

The backend uses Gemini API key from `backend/config.py`:

```python
GEMINI_API_KEY = "AIzaSyD-Zay55zScSxixu87JsLZcsCSzLKJRjuo"
```

**Model:** `gemini-2.0-flash-exp`

If you need a new key:
1. Visit: https://ai.google.dev
2. Get API key
3. Update `backend/config.py`

---

## 📊 System Requirements

### Minimum:
- Python 3.10+
- Node.js 16+
- 4GB RAM
- Internet connection

### Recommended:
- Python 3.13+
- Node.js 18+
- 8GB RAM
- Fast internet

---

## ✅ Success Checklist

- [ ] Backend started (port 8000)
- [ ] Frontend started (port 3000)
- [ ] Browser opened (localhost:3000)
- [ ] Starfield background visible
- [ ] MCP Tools panel showing 17 tools
- [ ] Can toggle tools ON/OFF
- [ ] Can send chat messages
- [ ] AI responds with streaming text
- [ ] Tools show as active when used

---

## 🎉 You're All Set!

Your **AI-MCP Orchestrator** is now running with:

✨ Real Gemini AI
🎨 Beautiful futuristic UI
🛠️ 17 MCP tools
💬 Streaming chat
📊 Live statistics
🌟 Animated starfield

**Enjoy your AI-powered dashboard! 🚀**

---

## 📞 Quick Commands

### Start Everything:
```bash
# Terminal 1
START_AI_BACKEND.bat

# Terminal 2  
START_FRONTEND.bat
```

### Check Status:
```bash
# Backend health
curl http://localhost:8000/health

# MCP tools
curl http://localhost:8000/api/mcp/tools
```

### Stop Everything:
```bash
# Close both terminal windows
# Or press Ctrl+C in each
```

---

**Need help? Check the troubleshooting section above! 💡**
