# 🏗️ Architecture Documentation - AI-MCP Orchestrator

This document provides a detailed technical overview of the system architecture.

---

## 📐 System Architecture

### **High-Level Overview**

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                    (React + Tailwind + Framer)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   ChatBox    │  │  MCP Panel   │  │   Sidebar    │         │
│  │              │  │              │  │              │         │
│  │ - Messages   │  │ - Tool Cards │  │ - History    │         │
│  │ - Input      │  │ - Toggles    │  │ - Sessions   │         │
│  │ - Markdown   │  │ - Status     │  │ - Clear      │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                    ┌───────┴────────┐
                    │                │
              REST API          WebSocket
                    │                │
┌───────────────────┴────────────────┴─────────────────────────────┐
│                      FASTAPI BACKEND                              │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                  API LAYER                               │    │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐          │    │
│  │  │   Chat     │ │    MCP     │ │  Memory    │          │    │
│  │  │  Routes    │ │  Routes    │ │  Routes    │          │    │
│  │  └────────────┘ └────────────┘ └────────────┘          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                            │                                     │
│  ┌─────────────────────────▼─────────────────────────────┐      │
│  │              LANGGRAPH ORCHESTRATION                   │      │
│  │                                                         │      │
│  │  ┌──────────────────────────────────────────────┐     │      │
│  │  │           State Graph Workflow               │     │      │
│  │  │                                              │     │      │
│  │  │  ┌──────────┐    ┌──────────┐              │     │      │
│  │  │  │ Analyze  │───▶│  Route   │              │     │      │
│  │  │  │ Intent   │    │  Tools   │              │     │      │
│  │  │  └──────────┘    └─────┬────┘              │     │      │
│  │  │                         │                    │     │      │
│  │  │                    ┌────▼─────┐             │     │      │
│  │  │                    │ Execute  │             │     │      │
│  │  │                    │  Tools   │             │     │      │
│  │  │                    └────┬─────┘             │     │      │
│  │  │                         │                    │     │      │
│  │  │                    ┌────▼─────┐             │     │      │
│  │  │                    │ Generate │             │     │      │
│  │  │                    │ Response │             │     │      │
│  │  │                    └──────────┘             │     │      │
│  │  └──────────────────────────────────────────────┘     │      │
│  └─────────────────────────────────────────────────────────┘      │
│                            │                                     │
│  ┌─────────────────────────▼─────────────────────────────┐      │
│  │                  LLM AGENT                             │      │
│  │                                                         │      │
│  │  ┌──────────────────────────────────────────────┐     │      │
│  │  │         Google Gemini 2.0 Flash              │     │      │
│  │  │                                              │     │      │
│  │  │  - Intent Analysis                           │     │      │
│  │  │  - Response Generation                       │     │      │
│  │  │  - Conversation Memory                       │     │      │
│  │  │  - Context Management                        │     │      │
│  │  └──────────────────────────────────────────────┘     │      │
│  └─────────────────────────────────────────────────────────┘      │
│                            │                                     │
│  ┌─────────────────────────▼─────────────────────────────┐      │
│  │              TOOL REGISTRY                             │      │
│  │                                                         │      │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐       │      │
│  │  │ Web  │ │ File │ │  DB  │ │Email │ │Drive │       │      │
│  │  │Search│ │ Mgr  │ │      │ │      │ │      │       │      │
│  │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘       │      │
│  │                                                         │      │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐       │      │
│  │  │Auto  │ │Memory│ │Analyt│ │  KB  │ │ API  │       │      │
│  │  │mation│ │      │ │ics   │ │      │ │Integr│       │      │
│  │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘       │      │
│  └─────────────────────────────────────────────────────────┘      │
└───────────────────────────┬───────────────────────────────────────┘
                            │
                   ┌────────▼────────┐
                   │    MongoDB      │
                   │                 │
                   │ - Chat History  │
                   │ - Tool Logs     │
                   │ - Sessions      │
                   └─────────────────┘
```

---

## 🔄 Request Flow

### **1. User Sends Message**

```
User Input
    │
    ├─▶ ChatBox Component
    │       │
    │       ├─▶ ChatContext (State)
    │       │
    │       └─▶ API Call (POST /api/chat/send)
    │
    └─▶ Backend Receives Request
```

### **2. Backend Processing**

```
FastAPI Endpoint
    │
    ├─▶ LangGraph Pipeline
    │       │
    │       ├─▶ Analyze Intent Node
    │       │       │
    │       │       └─▶ Gemini: "What does user want?"
    │       │
    │       ├─▶ Route Tools Node
    │       │       │
    │       │       └─▶ Router: "Which tools needed?"
    │       │
    │       ├─▶ Execute Tools Node (if needed)
    │       │       │
    │       │       ├─▶ Tool 1 (e.g., Web Search)
    │       │       ├─▶ Tool 2 (e.g., File Manager)
    │       │       └─▶ Collect Results
    │       │
    │       └─▶ Generate Response Node
    │               │
    │               └─▶ Gemini: "Create response with tool results"
    │
    └─▶ Return Response to Frontend
```

### **3. Frontend Updates**

```
API Response
    │
    ├─▶ ChatContext Updates
    │       │
    │       ├─▶ Add User Message
    │       ├─▶ Add AI Response
    │       └─▶ Update Tool Results
    │
    └─▶ UI Re-renders
            │
            ├─▶ New messages appear
            ├─▶ Tool indicators show
            └─▶ Scroll to bottom
```

---

## 🧩 Component Architecture

### **Frontend Components**

```
App.jsx
│
├─▶ ChatProvider (Context)
│   └─▶ State: messages, sessionId, isLoading
│
├─▶ MCPProvider (Context)
│   └─▶ State: tools, activeTools, isLoading
│
├─▶ AIBrain (Background Animation)
│   ├─▶ Gradient Orbs
│   ├─▶ Floating Particles
│   └─▶ Grid Lines
│
├─▶ Header
│   ├─▶ Logo
│   ├─▶ Toggle Buttons
│   └─▶ Settings
│
├─▶ Sidebar
│   ├─▶ New Chat Button
│   ├─▶ Session List
│   └─▶ Clear Session Button
│
├─▶ ChatBox
│   ├─▶ Messages Area
│   │   ├─▶ User Messages
│   │   ├─▶ AI Messages
│   │   └─▶ Tool Results
│   │
│   └─▶ Input Area
│       ├─▶ Textarea
│       ├─▶ Send Button
│       └─▶ Active Tools Display
│
└─▶ MCPPanel
    ├─▶ Header
    ├─▶ Tool Grid
    │   └─▶ MCPCard (x10)
    │       ├─▶ Icon
    │       ├─▶ Name
    │       ├─▶ Description
    │       └─▶ Status Indicator
    │
    └─▶ Stats
```

### **Backend Modules**

```
main.py (FastAPI App)
│
├─▶ Routes
│   ├─▶ chat_routes.py
│   │   ├─▶ POST /api/chat/send
│   │   ├─▶ GET /api/chat/history/{session_id}
│   │   ├─▶ DELETE /api/chat/session/{session_id}
│   │   └─▶ GET /api/chat/sessions
│   │
│   ├─▶ mcp_routes.py
│   │   ├─▶ GET /api/mcp/tools
│   │   ├─▶ GET /api/mcp/tools/{tool_name}
│   │   ├─▶ POST /api/mcp/tools/toggle
│   │   ├─▶ POST /api/mcp/tools/execute
│   │   └─▶ GET /api/mcp/tools/active
│   │
│   ├─▶ memory_routes.py
│   │   ├─▶ GET /api/memory/logs
│   │   └─▶ GET /api/memory/stats
│   │
│   └─▶ websocket_routes.py
│       └─▶ WS /api/ws/chat/{session_id}
│
├─▶ LangGraph Pipeline
│   ├─▶ graph_builder.py
│   │   ├─▶ StateGraph Definition
│   │   ├─▶ Node Functions
│   │   └─▶ Edge Conditions
│   │
│   ├─▶ llm_agent.py
│   │   ├─▶ Gemini Integration
│   │   ├─▶ Conversation Memory
│   │   └─▶ Intent Analysis
│   │
│   └─▶ router.py
│       ├─▶ Tool Routing Logic
│       ├─▶ Keyword Matching
│       └─▶ Tool Execution
│
├─▶ MCP Tools
│   ├─▶ web_search_mcp.py
│   ├─▶ file_manager_mcp.py
│   ├─▶ db_mcp.py
│   ├─▶ email_mcp.py
│   ├─▶ drive_mcp.py
│   ├─▶ automation_mcp.py
│   ├─▶ memory_mcp.py
│   ├─▶ analytics_mcp.py
│   ├─▶ knowledgebase_mcp.py
│   └─▶ api_integration_mcp.py
│
├─▶ Services
│   └─▶ db_service.py
│       ├─▶ MongoDB Connection
│       ├─▶ Chat History
│       └─▶ Tool Logs
│
└─▶ Utils
    └─▶ tool_registry.py
        ├─▶ Tool Registration
        ├─▶ Enable/Disable
        └─▶ Tool Info
```

---

## 💾 Data Models

### **Chat Message**

```python
{
    "session_id": "session_123",
    "role": "user" | "assistant",
    "content": "Message text",
    "timestamp": "2025-10-26T20:57:35+05:30",
    "metadata": {
        "tool_results": {...}
    }
}
```

### **MCP Tool**

```python
{
    "name": "web_search",
    "description": "Search the web using DuckDuckGo",
    "enabled": true,
    "schema": {
        "parameters": {...}
    }
}
```

### **Tool Execution Log**

```python
{
    "session_id": "session_123",
    "tool_name": "web_search",
    "action": "execute",
    "result": {
        "success": true,
        "data": {...}
    },
    "timestamp": "2025-10-26T20:57:35+05:30"
}
```

---

## 🔐 Security Architecture

```
┌─────────────────────────────────────┐
│         Security Layers             │
├─────────────────────────────────────┤
│ 1. CORS Protection                  │
│    - Whitelisted origins            │
│    - Credential handling            │
├─────────────────────────────────────┤
│ 2. Environment Variables            │
│    - API keys in .env               │
│    - No hardcoded secrets           │
├─────────────────────────────────────┤
│ 3. Input Validation                 │
│    - Pydantic models                │
│    - Type checking                  │
├─────────────────────────────────────┤
│ 4. Error Handling                   │
│    - Try-catch blocks               │
│    - Graceful degradation           │
├─────────────────────────────────────┤
│ 5. Database Security                │
│    - Connection pooling             │
│    - Query sanitization             │
└─────────────────────────────────────┘
```

---

## 📊 Performance Optimization

### **Backend**

- **Async Operations:** All I/O is non-blocking
- **Connection Pooling:** MongoDB connections reused
- **Lazy Loading:** Tools initialized on demand
- **Caching:** (Planned) Redis for frequent queries

### **Frontend**

- **Code Splitting:** Vite automatic chunking
- **Lazy Components:** React.lazy for large components
- **Memoization:** useMemo and useCallback hooks
- **Optimistic Updates:** UI updates before API response

---

## 🔄 State Management

### **Frontend State Flow**

```
User Action
    │
    ├─▶ Component Event Handler
    │       │
    │       ├─▶ Context Action
    │       │       │
    │       │       ├─▶ API Call
    │       │       │       │
    │       │       │       └─▶ Backend Processing
    │       │       │
    │       │       └─▶ Update Context State
    │       │
    │       └─▶ Component Re-renders
    │
    └─▶ UI Updates
```

---

## 🌐 Deployment Architecture

```
┌──────────────────────────────────────┐
│         Production Setup             │
├──────────────────────────────────────┤
│                                      │
│  ┌────────────┐    ┌────────────┐  │
│  │  Frontend  │    │  Backend   │  │
│  │  (Vercel)  │◀──▶│ (Railway)  │  │
│  └────────────┘    └─────┬──────┘  │
│                          │          │
│                    ┌─────▼──────┐   │
│                    │  MongoDB   │   │
│                    │  (Atlas)   │   │
│                    └────────────┘   │
└──────────────────────────────────────┘
```

---

## 📈 Scalability

### **Horizontal Scaling**

```
Load Balancer
    │
    ├─▶ Backend Instance 1
    ├─▶ Backend Instance 2
    └─▶ Backend Instance 3
            │
            └─▶ Shared MongoDB
```

### **Vertical Scaling**

- Increase server resources
- Optimize database queries
- Enable caching layer

---

## 🧪 Testing Strategy

```
┌─────────────────────────────────┐
│      Testing Pyramid            │
├─────────────────────────────────┤
│         E2E Tests               │
│      (Playwright/Cypress)       │
├─────────────────────────────────┤
│     Integration Tests           │
│    (API + Database)             │
├─────────────────────────────────┤
│       Unit Tests                │
│  (Components + Functions)       │
└─────────────────────────────────┘
```

---

## 📚 Technology Decisions

| Decision | Rationale |
|----------|-----------|
| **FastAPI** | Async support, auto docs, type safety |
| **Gemini 2.0 Flash** | Latest model, fast responses, cost-effective |
| **LangGraph** | Flexible orchestration, state management |
| **React** | Component reusability, large ecosystem |
| **Tailwind CSS** | Rapid development, consistent styling |
| **MongoDB** | Flexible schema, good for chat data |
| **WebSocket** | Real-time bidirectional communication |

---

**For implementation details, see the source code and inline documentation.**
