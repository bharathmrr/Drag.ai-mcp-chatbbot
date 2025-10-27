# 📡 API Reference - AI-MCP Orchestrator

Complete API documentation for the AI-MCP Orchestrator backend.

**Base URL:** `http://localhost:8000`

---

## 🔐 Authentication

Currently, the API does not require authentication. For production deployment, implement JWT or API key authentication.

---

## 📬 Chat Endpoints

### **Send Message**

Send a message to the AI and get a response.

```http
POST /api/chat/send
```

**Request Body:**
```json
{
  "query": "What is artificial intelligence?",
  "session_id": "session_123",
  "active_tools": ["web_search", "memory"]
}
```

**Response:**
```json
{
  "success": true,
  "response": "Artificial intelligence (AI) is...",
  "session_id": "session_123",
  "tool_results": {
    "web_search": {
      "success": true,
      "results": [...]
    }
  },
  "error": null
}
```

---

### **Get Chat History**

Retrieve chat history for a session.

```http
GET /api/chat/history/{session_id}?limit=50
```

**Response:**
```json
{
  "success": true,
  "history": [
    {
      "role": "user",
      "content": "Hello",
      "timestamp": "2025-10-26T20:57:35+05:30"
    },
    {
      "role": "assistant",
      "content": "Hi! How can I help you?",
      "timestamp": "2025-10-26T20:57:36+05:30"
    }
  ],
  "session_id": "session_123"
}
```

---

### **Clear Session**

Clear chat history for a session.

```http
DELETE /api/chat/session/{session_id}
```

**Response:**
```json
{
  "success": true,
  "message": "Session session_123 cleared"
}
```

---

### **List Sessions**

Get list of recent chat sessions.

```http
GET /api/chat/sessions?limit=20
```

**Response:**
```json
{
  "success": true,
  "sessions": [
    {
      "session_id": "session_123",
      "last_message": "2025-10-26T20:57:35+05:30",
      "message_count": 10
    }
  ]
}
```

---

## 🔧 MCP Tools Endpoints

### **List All Tools**

Get information about all available MCP tools.

```http
GET /api/mcp/tools
```

**Response:**
```json
{
  "success": true,
  "tools": [
    {
      "name": "web_search",
      "description": "Search the web using DuckDuckGo",
      "enabled": true,
      "schema": {...}
    }
  ],
  "count": 10
}
```

---

### **Get Tool Info**

Get detailed information about a specific tool.

```http
GET /api/mcp/tools/{tool_name}
```

**Response:**
```json
{
  "success": true,
  "tool": {
    "name": "web_search",
    "description": "Search the web using DuckDuckGo",
    "enabled": true,
    "schema": {
      "name": "web_search",
      "parameters": {...}
    }
  }
}
```

---

### **Toggle Tool**

Enable or disable a tool.

```http
POST /api/mcp/tools/toggle
```

**Request Body:**
```json
{
  "tool_name": "web_search",
  "enabled": true
}
```

**Response:**
```json
{
  "success": true,
  "tool_name": "web_search",
  "enabled": true
}
```

---

### **Execute Tool**

Directly execute a tool action.

```http
POST /api/mcp/tools/execute
```

**Request Body:**
```json
{
  "tool_name": "web_search",
  "action": "execute",
  "params": {
    "query": "Python tutorials",
    "max_results": 5
  }
}
```

**Response:**
```json
{
  "success": true,
  "tool": "web_search",
  "action": "execute",
  "result": {
    "success": true,
    "query": "Python tutorials",
    "results": [...]
  }
}
```

---

### **Get Active Tools**

Get list of currently active tools.

```http
GET /api/mcp/tools/active
```

**Response:**
```json
{
  "success": true,
  "active_tools": ["web_search", "file_manager", "memory"],
  "count": 3
}
```

---

## 💾 Memory Endpoints

### **Get Tool Logs**

Retrieve tool execution logs.

```http
GET /api/memory/logs?session_id=session_123&tool_name=web_search&limit=50
```

**Response:**
```json
{
  "success": true,
  "logs": [
    {
      "session_id": "session_123",
      "tool_name": "web_search",
      "action": "execute",
      "result": {...},
      "timestamp": "2025-10-26T20:57:35+05:30"
    }
  ],
  "count": 1
}
```

---

### **Get Stats**

Get system statistics.

```http
GET /api/memory/stats
```

**Response:**
```json
{
  "success": true,
  "stats": {
    "database_connected": true,
    "total_tools": 10,
    "active_tools": 5
  }
}
```

---

## 🔌 WebSocket Endpoints

### **Chat WebSocket**

Real-time chat communication.

```
WS /api/ws/chat/{session_id}
```

**Send Message:**
```json
{
  "type": "chat",
  "query": "Hello!",
  "active_tools": ["web_search"]
}
```

**Receive Response:**
```json
{
  "type": "response",
  "data": {
    "success": true,
    "response": "Hi! How can I help?",
    "session_id": "session_123"
  }
}
```

**Toggle Tool:**
```json
{
  "type": "tool_toggle",
  "tool_name": "web_search",
  "enabled": true
}
```

**Ping/Pong:**
```json
{
  "type": "ping"
}
```

---

## 🛠️ MCP Tool Schemas

### **Web Search Tool**

```json
{
  "name": "web_search",
  "description": "Search the web using DuckDuckGo",
  "parameters": {
    "query": "string (required)",
    "max_results": "integer (default: 5)"
  }
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/mcp/tools/execute \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "web_search",
    "action": "execute",
    "params": {"query": "AI news", "max_results": 3}
  }'
```

---

### **File Manager Tool**

```json
{
  "name": "file_manager",
  "description": "Read, write, list, and manage files",
  "parameters": {
    "action": "read|write|list|delete|exists (required)",
    "path": "string (required)",
    "content": "string (for write action)"
  }
}
```

**Example - Write File:**
```bash
curl -X POST http://localhost:8000/api/mcp/tools/execute \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "file_manager",
    "action": "write",
    "params": {
      "path": "test.txt",
      "content": "Hello World"
    }
  }'
```

---

### **Database Tool**

```json
{
  "name": "database",
  "description": "Query and manage MongoDB database",
  "parameters": {
    "action": "find|insert|update|delete|count (required)",
    "collection": "string (required)",
    "query": "object",
    "document": "object (for insert)",
    "update": "object (for update)",
    "limit": "integer (default: 10)"
  }
}
```

**Example - Find Documents:**
```bash
curl -X POST http://localhost:8000/api/mcp/tools/execute \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "database",
    "action": "find",
    "params": {
      "collection": "users",
      "query": {},
      "limit": 5
    }
  }'
```

---

### **Email Tool**

```json
{
  "name": "email",
  "description": "Send and compose emails via SMTP",
  "parameters": {
    "action": "send|draft (required)",
    "to": "string (required)",
    "subject": "string (required)",
    "body": "string (required)",
    "html": "boolean (default: false)"
  }
}
```

---

### **Analytics Tool**

```json
{
  "name": "analytics",
  "description": "Analyze data and generate insights",
  "parameters": {
    "action": "analyze|stats|trend|summary (required)",
    "data": "array or object (required)",
    "metrics": "array of strings",
    "period": "string (for trend)"
  }
}
```

**Example - Calculate Stats:**
```bash
curl -X POST http://localhost:8000/api/mcp/tools/execute \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "analytics",
    "action": "stats",
    "params": {
      "data": [10, 20, 30, 40, 50]
    }
  }'
```

---

## 📊 Response Codes

| Code | Description |
|------|-------------|
| 200  | Success |
| 400  | Bad Request |
| 404  | Not Found |
| 500  | Internal Server Error |

---

## 🔄 Error Handling

All endpoints return errors in this format:

```json
{
  "success": false,
  "error": "Error message here",
  "detail": "Additional details"
}
```

---

## 💡 Usage Examples

### **Python Example**

```python
import requests

# Send chat message
response = requests.post(
    "http://localhost:8000/api/chat/send",
    json={
        "query": "What is AI?",
        "active_tools": ["web_search"]
    }
)
print(response.json())

# Toggle tool
requests.post(
    "http://localhost:8000/api/mcp/tools/toggle",
    json={"tool_name": "web_search", "enabled": True}
)
```

### **JavaScript Example**

```javascript
// Send chat message
const response = await fetch('http://localhost:8000/api/chat/send', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'What is AI?',
    active_tools: ['web_search']
  })
});
const data = await response.json();
console.log(data);
```

### **cURL Example**

```bash
# Send message
curl -X POST http://localhost:8000/api/chat/send \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello!", "active_tools": ["web_search"]}'

# List tools
curl http://localhost:8000/api/mcp/tools

# Get health status
curl http://localhost:8000/health
```

---

## 📖 Interactive Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation where you can test all endpoints directly in your browser.

---

**For more information, see the main [README.md](README.md)**
