# ⚡ Quick Start Guide - AI-MCP Orchestrator

Get up and running in **5 minutes**!

---

## 📋 Prerequisites Check

```bash
# Check Python version (need 3.13+)
python --version

# Check Node.js version (need 18+)
node --version

# Check if MongoDB is installed
mongod --version
```

---

## 🚀 Installation (3 Steps)

### Step 1: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Key packages installed:**
- FastAPI, Uvicorn (Web server)
- LangChain, LangGraph (AI orchestration)
- Google Generative AI (Gemini)
- MongoDB Motor (Database)
- 40+ other tools and utilities

### Step 2: Install Frontend Dependencies

```bash
cd frontend
npm install
```

**Key packages installed:**
- React, Vite (UI framework)
- TailwindCSS (Styling)
- Framer Motion (Animations)
- Axios (HTTP client)

### Step 3: Configure Environment

Create `backend/.env`:

```env
GEMINI_API_KEY=AIzaSyD-Zay55zScSxixu87JsLZcsCSzLKJRjuo
GEMINI_MODEL=gemini-2.0-flash-exp
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ai_mcp_orchestrator
HOST=0.0.0.0
PORT=8000
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## ▶️ Start Application

### Option 1: Automatic (Recommended)

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Option 2: Manual

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

---

## ✅ Verify Installation

### 1. Check Backend

Open: http://localhost:8000/health

**Expected Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "tools_registered": 17
}
```

### 2. Check Frontend

Open: http://localhost:3000

**Expected:** Beautiful chat interface with MCP tools panel

### 3. Check API Docs

Open: http://localhost:8000/docs

**Expected:** Interactive Swagger UI documentation

---

## 🎮 First Steps

### 1. Enable Tools

Click **"MCP Tools"** button → Toggle ON desired tools:
- ✅ Web Search
- ✅ Wikipedia
- ✅ Calculator
- ✅ System Monitor
- ✅ Weather

### 2. Try Example Queries

**Simple Query:**
```
Hello! What can you do?
```

**Web Search:**
```
Search for latest AI news
```

**Weather:**
```
What's the weather in Tokyo?
```

**Wikipedia:**
```
Tell me about quantum computing
```

**Calculator:**
```
Calculate 25 * 4 + 10
```

**System Info:**
```
Show me my CPU usage
```

**Multi-Tool:**
```
Search for Python tutorials and summarize the top result
```

---

## 🎯 Key Features to Try

### 1. **Tool Chaining**
```
Search for "machine learning" and save the results to a file called ml_results.txt
```

### 2. **Code Execution**
```
Run this Python code: 
for i in range(5):
    print(f"Count: {i}")
```

### 3. **Unit Conversion**
```
Convert 100 kilometers to miles
```

### 4. **Translation**
```
Translate "Good morning, how are you?" to Spanish
```

### 5. **System Monitoring**
```
Give me a complete system overview
```

---

## 📊 Understanding the UI

```
┌─────────────────────────────────────────────────────────┐
│  🤖 AI-MCP Orchestrator          [MCP Tools] [Clear]   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  💬 Chat Messages                                       │
│  ┌────────────────────────────────────────────────┐    │
│  │ User: What's the weather in Tokyo?             │    │
│  │                                                 │    │
│  │ AI: The current weather in Tokyo is...         │    │
│  │ 🔧 Tools Used: climate                         │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
├─────────────────────────────────────────────────────────┤
│  💬 Type your message...                    [Send]      │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  📦 MCP Tools Panel (Toggle with button)                │
├─────────────────────────────────────────────────────────┤
│  [✓] Web Search      [✓] Wikipedia     [✓] Calculator  │
│  [✓] File Manager    [✓] Database      [✓] Email       │
│  [✓] Weather         [✓] System Mon    [✓] Translator  │
│  [ ] Google Drive    [ ] Automation    [ ] Analytics    │
└─────────────────────────────────────────────────────────┘
```

---

## 🔍 Exploring API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### List All Tools
```bash
curl http://localhost:8000/api/mcp/tools
```

### Send Chat Message
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is 2+2?",
    "active_tools": ["calculator"]
  }'
```

### Get Chat History
```bash
curl http://localhost:8000/api/memory/history?limit=10
```

---

## 🎨 Customization

### Change Port

**Backend** - Edit `backend/.env`:
```env
PORT=8080
```

**Frontend** - Edit `frontend/vite.config.js`:
```js
export default defineConfig({
  server: {
    port: 3001
  }
})
```

### Change Theme Colors

Edit `frontend/tailwind.config.js`:
```js
colors: {
  'ai-purple': '#8b5cf6',  // Change this
  'ai-green': '#10b981',   // And this
  'ai-dark': '#0a0a0f',    // And this
}
```

### Add Custom Tool

See `README.md` → Development → Adding a New MCP Tool

---

## 🐛 Common Issues & Quick Fixes

### Issue 1: "Module not found: fastapi"
```bash
cd backend
pip install fastapi uvicorn pydantic-settings
```

### Issue 2: "MongoDB connection failed"
```bash
# Start MongoDB
net start MongoDB

# Or use MongoDB Atlas (cloud)
# Update MONGODB_URL in .env
```

### Issue 3: "Port 8000 already in use"
```bash
# Windows - Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or change port in .env
```

### Issue 4: Frontend won't start
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Issue 5: CORS errors
Check `backend/.env`:
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## 📚 Next Steps

1. **Read Full Documentation:** See `README.md`
2. **Explore API Docs:** http://localhost:8000/docs
3. **Try All 17 Tools:** Enable them in the UI
4. **Build Custom Workflows:** Combine multiple tools
5. **Monitor Performance:** Check system logs

---

## 🎯 Example Workflows

### Workflow 1: Research Assistant
```
1. "Search for quantum computing papers"
2. "Summarize the top result from Wikipedia"
3. "Save the summary to quantum_notes.txt"
```

### Workflow 2: Data Analysis
```
1. "Show me my system performance"
2. "Calculate the average CPU usage"
3. "Send me an email with the results"
```

### Workflow 3: Content Creation
```
1. "Search for AI trends 2024"
2. "Create a summary in Spanish"
3. "Save it to a file"
```

---

## 💡 Pro Tips

1. **Enable Multiple Tools:** The AI will automatically choose the best one
2. **Be Specific:** "Search Wikipedia for Python programming" vs "Python"
3. **Chain Commands:** Use "and" to combine multiple actions
4. **Check Logs:** Backend terminal shows detailed execution info
5. **Use Shortcuts:** Ctrl+Enter to send message

---

## 📞 Need Help?

- **Documentation:** `README.md`
- **API Reference:** http://localhost:8000/docs
- **Troubleshooting:** `FIXES_APPLIED.md`
- **Updates:** `UPDATE_SUMMARY.md`

---

## ✨ You're All Set!

Your AI-MCP Orchestrator is ready to use! 🚀

**Start chatting and explore the power of 17+ MCP tools!**

---

**Enjoy! 🎉**
