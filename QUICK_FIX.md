# 🔧 Quick Fix Guide - Backend & MCP Tools Not Working

## 🚨 Issues You're Facing

1. ❌ **"Error: Network Error"** - Backend not running
2. ❌ **"0 of 0 tools active"** - MCP tools not loading
3. ❌ **AI not responding** - No connection to Gemini API

---

## ✅ Solution - Follow These Steps

### Step 1: Start Backend Server

**Double-click this file:**
```
START_BACKEND.bat
```

**What it does:**
- Activates Python virtual environment
- Installs all required dependencies
- Starts the FastAPI backend server

**Expected Output:**
```
================================================================================
🚀 AI-MCP ORCHESTRATOR - SERVER STARTING
================================================================================
✅ Database connected successfully (or warning if MongoDB not available)
✅ Registered 17 MCP tools

📦 REGISTERED MCP TOOLS:
   • web_search
   • file_manager
   • database
   ... (all 17 tools)

🌐 SERVER RUNNING
   • API: http://localhost:8000
   • Docs: http://localhost:8000/docs
================================================================================
```

### Step 2: Verify Backend is Running

Open in browser: **http://localhost:8000/health**

**Expected Response:**
```json
{
  "status": "healthy",
  "database": "connected" or "disconnected",
  "tools_registered": 17
}
```

### Step 3: Start Frontend

**Double-click this file:**
```
START_FRONTEND.bat
```

### Step 4: Open Application

Open in browser: **http://localhost:3000**

---

## 🔍 Troubleshooting

### Problem 1: Backend Won't Start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

### Problem 2: Port Already in Use

**Error:** `Address already in use: 8000`

**Solution:**
```bash
# Find and kill the process
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

### Problem 3: MCP Tools Still Not Showing

**Check:**
1. Backend is running (http://localhost:8000/health)
2. Frontend is connected (no "Network Error")
3. Browser console for errors (F12)

**Test API directly:**
```bash
curl http://localhost:8000/api/mcp/tools
```

**Expected Response:**
```json
{
  "success": true,
  "tools": [
    {
      "name": "web_search",
      "description": "Search the web",
      "enabled": true
    },
    ...
  ],
  "count": 17
}
```

### Problem 4: AI Not Responding

**Check Gemini API Key:**

1. Open `backend/config.py`
2. Verify line 7:
```python
GEMINI_API_KEY: str = "AIzaSyD-Zay55zScSxixu87JsLZcsCSzLKJRjuo"
```

3. Test API key:
```bash
curl https://generativelanguage.googleapis.com/v1/models?key=AIzaSyD-Zay55zScSxixu87JsLZcsCSzLKJRjuo
```

---

## 📝 Manual Installation (If Batch Files Don't Work)

### Backend:

```bash
cd backend

# Activate venv
venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn pydantic pydantic-settings python-dotenv
pip install langchain langchain-google-genai google-generativeai
pip install wikipedia screeninfo psutil

# Start server
python main.py
```

### Frontend:

```bash
cd frontend

# Install dependencies (if not done)
npm install

# Start dev server
npm run dev
```

---

## 🎯 Quick Test Commands

### Test Backend Health:
```bash
curl http://localhost:8000/health
```

### Test MCP Tools:
```bash
curl http://localhost:8000/api/mcp/tools
```

### Test Chat API:
```bash
curl -X POST http://localhost:8000/api/chat/send \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"Hello\",\"session_id\":\"test123\"}"
```

---

## ✅ Success Checklist

- [ ] Backend starts without errors
- [ ] Health check returns `{"status": "healthy"}`
- [ ] MCP tools API returns 17 tools
- [ ] Frontend loads without "Network Error"
- [ ] MCP Tools panel shows "17 of 17 tools" (or similar)
- [ ] Can toggle tools ON/OFF
- [ ] AI responds to messages

---

## 🚀 Once Everything Works

1. **Enable Tools:**
   - Click "MCP Tools" button
   - Toggle ON the tools you want to use

2. **Test AI:**
   - Type: "Hello, what can you do?"
   - AI should respond with capabilities

3. **Test Tools:**
   - "What's the weather in Tokyo?" (Climate tool)
   - "Search Wikipedia for AI" (Wikipedia tool)
   - "Calculate 25 * 4" (Calculator tool)

---

## 📞 Still Having Issues?

### Check Logs:

**Backend Terminal:**
- Look for errors in red
- Check if all 17 tools registered
- Verify server is listening on port 8000

**Frontend Terminal:**
- Look for compilation errors
- Check if dev server started
- Verify it's on port 3000

**Browser Console (F12):**
- Look for network errors
- Check API call responses
- Verify WebSocket connection

---

## 🎨 Expected UI After Fix

- ✨ **Beautiful starfield background** with twinkling stars
- 🎯 **MCP Tools panel** on the right showing all 17 tools
- 💬 **Chat interface** in the center
- 📊 **Stats** showing "X of 17 tools active"
- ✅ **No "Network Error"** messages

---

## 💡 Pro Tips

1. **Keep both terminals open** (backend + frontend)
2. **Check backend first** before starting frontend
3. **Refresh browser** (Ctrl+F5) if UI doesn't update
4. **Clear browser cache** if styles look broken
5. **Use Chrome/Edge** for best compatibility

---

## 🔗 Important URLs

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **MCP Tools:** http://localhost:8000/api/mcp/tools

---

**Your AI-MCP Orchestrator will work perfectly after following these steps! 🚀**
