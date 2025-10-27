# 🤖 AI-MCP Orchestrator

<div align="center">

**Next-Generation Agentic AI System with 17+ MCP Tools**

[![AI-MCP Orchestrator](https://img.shields.io/badge/AI-MCP%20Orchestrator-8b5cf6?style=for-the-badge)](https://github.com)
[![Gemini 2.0](https://img.shields.io/badge/Gemini-2.0%20Flash-4285f4?style=for-the-badge)](https://ai.google.dev)
[![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-10b981?style=for-the-badge)](https://langchain.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-Frontend-61dafb?style=for-the-badge)](https://react.dev)

*A production-ready ChatGPT-style system integrating **LangChain**, **LangGraph**, **FastMCP**, and **Google Gemini 2.0 Flash** with 17+ powerful MCP tools, intelligent routing, persistent memory, and a beautiful reactive UI.*

[Features](#-features) • [Architecture](#-architecture) • [Installation](#-installation) • [Usage](#-usage) • [API Docs](#-api-documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-features)
- [System Architecture](#-architecture)
- [MCP Tools](#-mcp-tools-17)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

**AI-MCP Orchestrator** is a sophisticated agentic AI system that combines the power of Google's Gemini 2.0 Flash model with an extensive suite of Model Context Protocol (MCP) tools. Built on LangChain and LangGraph, it provides intelligent tool routing, multi-step reasoning, and seamless integration with external services.

### What Makes It Special?

- 🎯 **17+ MCP Tools** - From web search to system monitoring, weather to translation
- 🧠 **Intelligent Routing** - Automatically selects the right tools for each query
- 🔄 **LangGraph Pipeline** - Multi-agent orchestration with state management
- 💾 **Persistent Memory** - Conversation history and context retention
- 🎨 **Beautiful UI** - Modern, responsive interface with real-time updates
- ⚡ **Real-time WebSocket** - Streaming responses and live tool execution
- 🔧 **Toggleable Tools** - Enable/disable tools on-the-fly
- 📊 **Analytics Dashboard** - Monitor system performance and tool usage

---

## ✨ Features

### 🤖 AI Capabilities
- **Multi-turn Conversations** with context awareness
- **Tool Chaining** - Combine multiple tools in a single query
- **Intelligent Fallbacks** - Graceful degradation when tools fail
- **Streaming Responses** - Real-time token-by-token output
- **Memory Management** - Short-term and long-term context

### 🛠️ MCP Tools Suite
- **Web Search** - DuckDuckGo integration
- **File Management** - Read, write, organize files
- **Database Operations** - MongoDB CRUD operations
- **Email Automation** - Send and manage emails
- **Google Drive** - Cloud storage integration
- **Workflow Automation** - Schedule and execute tasks
- **Knowledge Base** - Store and retrieve information
- **Analytics** - Data analysis and visualization
- **API Integration** - Connect to external APIs
- **Weather/Climate** - Real-time weather data
- **Wikipedia** - Encyclopedia search and retrieval
- **Python Execution** - Safe code execution sandbox
- **Screen Monitoring** - Screenshots and display info
- **System Monitoring** - CPU, memory, disk metrics
- **Calculator** - Math operations and unit conversion
- **Translator** - Multi-language translation

### 🎨 User Interface
- **ChatGPT-style Interface** - Familiar and intuitive
- **Tool Status Cards** - Visual tool management
- **Animated Particles** - Dynamic background effects
- **Dark Theme** - Eye-friendly design
- **Responsive Layout** - Works on all devices
- **Message History** - Scroll through past conversations
- **Typing Indicators** - Real-time feedback

---

## 🏗️ Architecture

### High-Level System Design

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Chat UI    │  │  Tool Panel  │  │  Analytics   │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                  │
│         └──────────────────┴──────────────────┘                  │
│                            │                                      │
│                    WebSocket / REST API                          │
└────────────────────────────┼────────────────────────────────────┘
                             │
┌────────────────────────────┼────────────────────────────────────┐
│                    BACKEND (FastAPI)                             │
│  ┌──────────────────────────┴──────────────────────────┐        │
│  │              API Layer (Routes)                      │        │
│  │  • Chat Routes    • MCP Routes    • Memory Routes   │        │
│  └──────────────────────┬──────────────────────────────┘        │
│                         │                                         │
│  ┌──────────────────────┴──────────────────────────────┐        │
│  │         LangGraph Orchestration Pipeline             │        │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │        │
│  │  │  Router  │→ │ Executor │→ │ Aggregator│          │        │
│  │  └──────────┘  └──────────┘  └──────────┘          │        │
│  └──────────────────────┬──────────────────────────────┘        │
│                         │                                         │
│  ┌──────────────────────┴──────────────────────────────┐        │
│  │              Tool Registry (17 Tools)                │        │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐       │        │
│  │  │Web Srch│ │File Mgr│ │Database│ │ Email  │ ...   │        │
│  │  └────────┘ └────────┘ └────────┘ └────────┘       │        │
│  └──────────────────────┬──────────────────────────────┘        │
│                         │                                         │
│  ┌──────────────────────┴──────────────────────────────┐        │
│  │            Services & Integrations                   │        │
│  │  • Database Service (MongoDB)                        │        │
│  │  • Gemini AI Service (Google)                        │        │
│  │  • Memory Service (Context Management)               │        │
│  └──────────────────────────────────────────────────────┘        │
└──────────────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────┼────────────────────────────────────┐
│                    EXTERNAL SERVICES                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Gemini   │  │ MongoDB  │  │  Google  │  │   APIs   │       │
│  │ 2.0 Flash│  │          │  │  Drive   │  │          │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
└──────────────────────────────────────────────────────────────────┘
```

### LangGraph Pipeline Flow

```
User Query
    ↓
┌───────────────┐
│  Query Router │ ← Analyzes query and selects appropriate tools
└───────┬───────┘
        ↓
┌───────────────┐
│ Tool Executor │ ← Executes selected MCP tools in parallel/sequence
└───────┬───────┘
        ↓
┌───────────────┐
│  Aggregator   │ ← Combines results from multiple tools
└───────┬───────┘
        ↓
┌───────────────┐
│ Response Gen  │ ← Generates natural language response
└───────┬───────┘
        ↓
   User Response
```

### Data Flow Architecture

```
┌──────────────┐
│   User Input │
└──────┬───────┘
       ↓
┌──────────────────────────────────────┐
│  1. WebSocket Connection Established │
└──────┬───────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│  2. Query Preprocessing               │
│     • Tokenization                    │
│     • Context Injection               │
│     • Memory Retrieval                │
└──────┬───────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│  3. Tool Selection (Router)           │
│     • Keyword Matching                │
│     • Semantic Analysis               │
│     • Multi-tool Detection            │
└──────┬───────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│  4. Tool Execution                    │
│     • Parallel Execution              │
│     • Error Handling                  │
│     • Result Caching                  │
└──────┬───────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│  5. Response Generation               │
│     • Result Aggregation              │
│     • Gemini 2.0 Processing           │
│     • Streaming Output                │
└──────┬───────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│  6. Memory Update                     │
│     • Conversation Storage            │
│     • Context Update                  │
└──────┬───────────────────────────────┘
       ↓
┌──────────────┐
│ User Response│
└──────────────┘
```

---

## 🧰 MCP Tools (17)

### 1. **Web Search** 🔍
- **Provider:** DuckDuckGo
- **Actions:** Search web, get snippets, extract URLs
- **Use Cases:** Research, fact-checking, current events

### 2. **File Manager** 📁
- **Actions:** Read, write, delete, list files
- **Supported:** Text, JSON, CSV, Markdown
- **Use Cases:** Document management, data processing

### 3. **Database** 🗄️
- **Provider:** MongoDB
- **Actions:** CRUD operations, queries, aggregations
- **Use Cases:** Data storage, retrieval, analytics

### 4. **Email** 📧
- **Protocol:** SMTP
- **Actions:** Send emails, attachments, templates
- **Use Cases:** Notifications, reports, communication

### 5. **Google Drive** ☁️
- **Actions:** Upload, download, share, organize
- **Use Cases:** Cloud storage, collaboration

### 6. **Automation** ⚡
- **Actions:** Schedule tasks, workflows, triggers
- **Use Cases:** Recurring tasks, batch processing

### 7. **Memory** 🧠
- **Actions:** Store, recall, search context
- **Use Cases:** Conversation history, user preferences

### 8. **Analytics** 📊
- **Actions:** Data analysis, visualization, trends
- **Use Cases:** Business intelligence, reporting

### 9. **Knowledge Base** 📚
- **Actions:** Store articles, search, categorize
- **Use Cases:** Documentation, wiki, FAQs

### 10. **API Integration** 🔗
- **Actions:** REST calls, webhooks, OAuth
- **Use Cases:** Third-party integrations

### 11. **Climate/Weather** 🌤️
- **Provider:** Python Weather API
- **Actions:** Current weather, forecasts, climate data
- **Use Cases:** Travel planning, weather alerts

### 12. **Wikipedia** 📖
- **Actions:** Search, summaries, full articles
- **Use Cases:** Research, definitions, learning

### 13. **Python Code** 💻
- **Actions:** Execute code, validate syntax, analyze
- **Use Cases:** Calculations, data processing, automation

### 14. **Screen Monitor** 🖥️
- **Actions:** Screenshots, display info, resolution
- **Use Cases:** Documentation, troubleshooting

### 15. **System Monitor** 📈
- **Actions:** CPU, memory, disk, network stats
- **Use Cases:** Performance monitoring, diagnostics

### 16. **Calculator** 🔢
- **Actions:** Math operations, unit conversions
- **Use Cases:** Calculations, conversions, equations

### 17. **Translator** 🌐
- **Actions:** Translate text, detect language
- **Supported:** 12+ languages
- **Use Cases:** Multilingual communication

---

## 🔧 Technology Stack

### Backend
- **Framework:** FastAPI 0.120.0
- **AI/ML:** 
  - Google Gemini 2.0 Flash
  - LangChain (latest)
  - LangGraph (latest)
- **Database:** MongoDB (Motor async driver)
- **WebSocket:** FastAPI WebSockets
- **Validation:** Pydantic v2

### Frontend
- **Framework:** React 18
- **Build Tool:** Vite
- **Styling:** TailwindCSS
- **Animations:** Framer Motion
- **Icons:** Lucide React
- **HTTP Client:** Axios

### DevOps
- **Environment:** Python 3.13+
- **Package Manager:** pip, npm
- **Process Manager:** Uvicorn
- **Logging:** Python logging with colors

---

## 📦 Installation

### Prerequisites

- **Python 3.13+**
- **Node.js 18+**
- **MongoDB** (local or cloud)
- **Git**

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/ai-mcp-orchestrator.git
cd ai-mcp-orchestrator
```

### Step 2: Backend Setup

```bash
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
```

### Step 3: Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

### Step 4: Environment Configuration

Create `.env` file in `backend/` directory:

```env
# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=

# Model Configuration
GEMINI_MODEL=gemini-2.0-flash-exp
TEMPERATURE=0.7
MAX_TOKENS=8192

# Database
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ai_mcp_orchestrator

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# MCP Configuration
MCP_TIMEOUT=30
MAX_CONCURRENT_TOOLS=5
```

### Step 5: Start MongoDB

```bash
# Windows (if installed as service)
net start MongoDB

# Linux/Mac
sudo systemctl start mongod

# Or use MongoDB Atlas (cloud)
```

---

## 🚀 Usage Guide

### Starting the Application

#### Option 1: Manual Start

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

#### Option 2: Using Start Scripts

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Accessing the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

### Using the Chat Interface

1. **Open** http://localhost:3000
2. **Enable Tools** - Click "MCP Tools" button and toggle desired tools
3. **Start Chatting** - Type your query in the input box
4. **View Results** - See AI responses with tool execution details

### Example Queries

```
🔍 Web Search:
"Search for latest AI news"

🌤️ Weather:
"What's the weather in Tokyo?"

📖 Wikipedia:
"Tell me about quantum computing"

💻 Python Code:
"Run this code: print('Hello World')"

📊 System Monitor:
"Show me my CPU usage"

🔢 Calculator:
"Calculate 25 * 4 + 10"

🌐 Translator:
"Translate 'Good morning' to Spanish"

🔗 Multi-Tool:
"Search for Python tutorials and save the results to a file"
```

---

## 📚 API Documentation

### REST Endpoints

#### Chat API

**POST** `/api/chat/message`
```json
{
  "message": "Your query here",
  "session_id": "optional-session-id",
  "active_tools": ["web_search", "calculator"]
}
```

**Response:**
```json
{
  "response": "AI generated response",
  "tools_used": ["web_search"],
  "execution_time": 1.23,
  "session_id": "session-123"
}
```

#### MCP Tools API

**GET** `/api/mcp/tools`
```json
{
  "tools": [
    {
      "name": "web_search",
      "description": "Search the web",
      "enabled": true
    }
  ]
}
```

**POST** `/api/mcp/tools/{tool_name}/toggle`
```json
{
  "enabled": true
}
```

#### Memory API

**GET** `/api/memory/history?session_id=123&limit=10`

**DELETE** `/api/memory/clear?session_id=123`

### WebSocket API

**Connect:** `ws://localhost:8000/api/ws/chat`

**Send Message:**
```json
{
  "type": "message",
  "content": "Your query",
  "session_id": "session-123"
}
```

**Receive Response:**
```json
{
  "type": "response",
  "content": "AI response",
  "tools_used": ["web_search"],
  "done": true
}
```

---

## 📁 Project Structure

```
ai-mcp-orchestrator/
├── backend/
│   ├── config.py              # Configuration settings
│   ├── main.py                # FastAPI application entry
│   ├── requirements.txt       # Python dependencies
│   │
│   ├── routes/                # API route handlers
│   │   ├── chat_routes.py
│   │   ├── mcp_routes.py
│   │   ├── memory_routes.py
│   │   └── websocket_routes.py
│   │
│   ├── services/              # Business logic services
│   │   ├── db_service.py
│   │   ├── gemini_service.py
│   │   └── memory_service.py
│   │
│   ├── mcp_tools/             # 17 MCP tool implementations
│   │   ├── web_search_mcp.py
│   │   ├── file_manager_mcp.py
│   │   ├── climate_mcp.py
│   │   ├── wikipedia_mcp.py
│   │   └── ... (13 more)
│   │
│   ├── langgraph_pipeline/    # LangGraph orchestration
│   │   ├── graph_builder.py
│   │   ├── router.py
│   │   ├── executor.py
│   │   └── aggregator.py
│   │
│   └── utils/                 # Utility functions
│       ├── tool_registry.py
│       └── helpers.py
│
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   │
│   ├── src/
│   │   ├── App.jsx            # Main application
│   │   ├── main.jsx           # Entry point
│   │   │
│   │   ├── components/        # React components
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── MCPToolPanel.jsx
│   │   │   ├── MCPCard.jsx
│   │   │   └── ParticleBackground.jsx
│   │   │
│   │   ├── context/           # React context
│   │   │   └── MCPContext.jsx
│   │   │
│   │   ├── services/          # API services
│   │   │   └── api.js
│   │   │
│   │   └── styles/            # CSS styles
│   │       └── index.css
│   │
│   └── public/                # Static assets
│
├── README.md                  # This file
├── UPDATE_SUMMARY.md          # Recent updates
└── .gitignore
```

---

## 🛠️ Development

### Adding a New MCP Tool

1. **Create tool file:** `backend/mcp_tools/your_tool_mcp.py`

```python
class YourTool:
    def __init__(self):
        self.name = "your_tool"
        self.description = "Tool description"
        self.enabled = True
    
    async def execute(self, action: str, **kwargs):
        # Implementation
        return {"success": True, "data": "result"}
    
    def get_schema(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {...}
        }
```

2. **Register in `__init__.py`:**
```python
from .your_tool_mcp import YourTool
__all__ = [..., "YourTool"]
```

3. **Add to tool registry:** `utils/tool_registry.py`

4. **Add keywords:** `langgraph_pipeline/router.py`

5. **Add frontend icon:** `frontend/src/components/MCPCard.jsx`

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Formatting

```bash
# Backend
black backend/
flake8 backend/

# Frontend
npm run lint
npm run format
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. **CORS Error**
```
Error: CORS policy blocked
```
**Solution:** Check `CORS_ORIGINS` in `.env` matches your frontend URL

#### 2. **MongoDB Connection Failed**
```
Error: Could not connect to MongoDB
```
**Solution:** 
- Ensure MongoDB is running
- Check `MONGODB_URL` in `.env`
- Try: `mongodb://localhost:27017` or MongoDB Atlas URL

#### 3. **Gemini API Error**
```
Error: Invalid API key
```
**Solution:** 
- Get API key from https://ai.google.dev
- Update `GEMINI_API_KEY` in `.env`

#### 4. **Module Not Found**
```
ModuleNotFoundError: No module named 'fastapi'
```
**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

#### 5. **Port Already in Use**
```
Error: Address already in use
```
**Solution:**
- Change `PORT` in `.env`
- Or kill process: `lsof -ti:8000 | xargs kill -9` (Mac/Linux)

### Logs Location

- **Backend:** Console output with colored logging
- **Frontend:** Browser console (F12)
- **MongoDB:** Check MongoDB logs

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Contribution Guidelines

- Follow existing code style
- Add tests for new features
- Update documentation
- Keep commits atomic and well-described

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google** - Gemini 2.0 Flash API
- **LangChain** - AI orchestration framework
- **FastAPI** - Modern Python web framework
- **React** - UI library
- **MongoDB** - Database solution

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/ai-mcp-orchestrator/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/ai-mcp-orchestrator/discussions)
- **Email:** your.email@example.com

---

## 🗺️ Roadmap

- [ ] Add more MCP tools (20+ target)
- [ ] Voice input/output support
- [ ] Multi-user authentication
- [ ] Tool marketplace
- [ ] Mobile app (React Native)
- [ ] Docker containerization
- [ ] Kubernetes deployment
- [ ] Advanced analytics dashboard
- [ ] Plugin system for custom tools
- [ ] RAG (Retrieval Augmented Generation)

---

<div align="center">

**Built with ❤️ by the AI-MCP Team**

⭐ Star us on GitHub if you find this useful!

</div>
