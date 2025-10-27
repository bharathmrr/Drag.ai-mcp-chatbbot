# 🚀 Quick Setup Guide - AI-MCP Orchestrator

This guide will help you get the AI-MCP Orchestrator up and running in minutes.

---

## 📋 Prerequisites

Before you begin, ensure you have:

- ✅ **Python 3.10+** installed
- ✅ **Node.js 18+** installed
- ✅ **MongoDB** (optional - system works without it)
- ✅ **Google Gemini API Key** (already configured in the project)

---

## ⚡ Quick Start (Fastest Method)

### **Option 1: Run with Docker** 🐳

```bash
# 1. Clone or navigate to the project
cd Drag.ai-mcp-chatbbot

# 2. Start everything with Docker Compose
docker-compose up -d

# 3. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

That's it! The application is now running.

---

### **Option 2: Manual Setup** 🛠️

#### **Step 1: Backend Setup**

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac

# Start the backend
python main.py
```

✅ Backend running at `http://localhost:8000`

#### **Step 2: Frontend Setup**

Open a **new terminal**:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

✅ Frontend running at `http://localhost:3000`

---

## 🔑 Configuration

### **Environment Variables**

The Gemini API key is already configured, but you can customize settings in `backend/.env`:

```env
# AI Model
GEMINI_API_KEY=AIzaSyD-Zay55zScSxixu87JsLZcsCSzLKJRjuo
GEMINI_MODEL=gemini-2.0-flash-exp
TEMPERATURE=0.7

# Database (Optional)
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ai_mcp_orchestrator

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Email Tool (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

---

## 🧪 Testing the Installation

### **1. Test Backend Health**

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "tools_registered": 10
}
```

### **2. Test Chat Endpoint**

```bash
curl -X POST http://localhost:8000/api/chat/send \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"Hello! What can you do?\", \"active_tools\": [\"web_search\"]}"
```

### **3. Test MCP Tools**

```bash
curl http://localhost:8000/api/mcp/tools
```

### **4. Open Frontend**

Navigate to `http://localhost:3000` in your browser and start chatting!

---

## 🎯 First Steps

### **1. Activate MCP Tools**

- Click on the **MCP Tools** button in the header
- Toggle tools ON (green glow = active)
- Recommended to start with: `web_search`, `file_manager`, `memory`

### **2. Try Example Queries**

**Web Search:**
```
Search for the latest AI news
```

**File Operations:**
```
Create a file called test.txt with "Hello World"
```

**Multi-Tool:**
```
Search for Python tutorials and summarize the top 3 results
```

**Analytics:**
```
Analyze these numbers: [10, 20, 30, 40, 50]
```

---

## 🔧 Troubleshooting

### **Backend won't start**

**Problem:** `ModuleNotFoundError`
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

**Problem:** Port 8000 already in use
```bash
# Solution: Change port in backend/.env
PORT=8001
```

### **Frontend won't start**

**Problem:** `npm install` fails
```bash
# Solution: Clear cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Problem:** Port 3000 already in use
```bash
# Solution: The dev server will automatically use port 3001
```

### **MongoDB Connection Issues**

**Problem:** Can't connect to MongoDB
```
✅ No problem! The system runs in memory-only mode if MongoDB is unavailable.
```

To install MongoDB (optional):
```bash
# Windows: Download from https://www.mongodb.com/try/download/community
# Mac: brew install mongodb-community
# Linux: sudo apt-get install mongodb
```

### **API Key Issues**

**Problem:** Gemini API errors
```bash
# Check your API key in backend/.env
# Get a new key from: https://makersuite.google.com/app/apikey
```

---

## 📊 Verify Everything is Working

### **Backend Checklist**
- [ ] Backend starts without errors
- [ ] `/health` endpoint returns healthy status
- [ ] API docs accessible at `/docs`
- [ ] 10 MCP tools registered

### **Frontend Checklist**
- [ ] Frontend loads at `http://localhost:3000`
- [ ] Animated background visible
- [ ] MCP panel shows 10 tools
- [ ] Can send messages
- [ ] AI responds with Gemini

---

## 🎨 UI Features to Explore

1. **Animated Background** - Floating particles and gradient orbs
2. **MCP Tool Panel** - Toggle tools with visual feedback
3. **Chat History** - Sidebar with session management
4. **Real-time Updates** - WebSocket connection status
5. **Markdown Support** - Rich text formatting in responses
6. **Tool Results** - See which tools were used for each response

---

## 📚 Next Steps

1. **Explore MCP Tools** - Try each of the 10 tools
2. **Customize UI** - Edit `frontend/tailwind.config.js` for theme
3. **Add New Tools** - Create custom MCP tools
4. **Deploy** - Use Railway, Render, or Vercel
5. **Configure Email** - Set up SMTP for email tool
6. **Set up Drive** - Configure Google Drive API

---

## 🆘 Getting Help

- **API Documentation:** http://localhost:8000/docs
- **Check Logs:** Backend terminal shows detailed logs
- **Browser Console:** Frontend errors appear in DevTools
- **GitHub Issues:** Report bugs or request features

---

## 🎉 Success!

If you can:
- ✅ See the animated UI at `http://localhost:3000`
- ✅ Send a message and get an AI response
- ✅ Toggle MCP tools on/off
- ✅ See tool results in responses

**Congratulations! Your AI-MCP Orchestrator is fully operational! 🚀**

---

## 💡 Pro Tips

1. **Enable multiple tools** for complex queries
2. **Use Shift+Enter** for multi-line messages
3. **Check the sidebar** for chat history
4. **Monitor tool status** in the MCP panel
5. **Use markdown** in your queries for better formatting

---

**Happy Orchestrating! 🎯**
