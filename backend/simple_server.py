"""Simple server for testing"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="AI-MCP Test Server")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock tools data
MOCK_TOOLS = [
    {"name": "web_search", "description": "Search the web", "enabled": True},
    {"name": "file_manager", "description": "Manage files", "enabled": True},
    {"name": "database", "description": "Database operations", "enabled": False},
    {"name": "email", "description": "Send emails", "enabled": True},
    {"name": "drive", "description": "Google Drive", "enabled": True},
    {"name": "automation", "description": "Automate tasks", "enabled": True},
    {"name": "memory", "description": "Memory management", "enabled": True},
    {"name": "analytics", "description": "Data analytics", "enabled": True},
    {"name": "knowledgebase", "description": "Knowledge base", "enabled": True},
    {"name": "api_integration", "description": "API integration", "enabled": True},
    {"name": "climate", "description": "Weather data", "enabled": True},
    {"name": "wikipedia", "description": "Wikipedia search", "enabled": True},
    {"name": "python_code", "description": "Execute Python code", "enabled": True},
    {"name": "screen_monitor", "description": "Screen monitoring", "enabled": True},
    {"name": "system_monitor", "description": "System monitoring", "enabled": True},
    {"name": "calculator", "description": "Calculator", "enabled": True},
    {"name": "translator", "description": "Translate text", "enabled": True},
]

@app.get("/")
async def root():
    return {"message": "AI-MCP Test Server", "status": "running"}

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "database": "disconnected",
        "tools_registered": len(MOCK_TOOLS)
    }

@app.get("/api/mcp/tools")
async def list_tools():
    return {
        "success": True,
        "tools": MOCK_TOOLS,
        "count": len(MOCK_TOOLS)
    }

@app.post("/api/mcp/tools/toggle")
async def toggle_tool(request: dict):
    tool_name = request.get("tool_name")
    enabled = request.get("enabled")
    
    for tool in MOCK_TOOLS:
        if tool["name"] == tool_name:
            tool["enabled"] = enabled
            return {"success": True, "tool_name": tool_name, "enabled": enabled}
    
    return {"success": False, "error": "Tool not found"}

@app.post("/api/chat/send")
async def send_message(request: dict):
    query = request.get("query", "").lower()
    active_tools = request.get("active_tools", [])
    
    # Smart responses based on query
    response = ""
    tools_used = []
    
    if "weather" in query or "climate" in query:
        tools_used.append("climate")
        city = "the requested location"
        if "tokyo" in query:
            city = "Tokyo"
        elif "hyderabad" in query:
            city = "Hyderabad"
        response = f"🌤️ **Weather in {city}:**\n\n- **Temperature:** 28°C\n- **Condition:** Partly Cloudy\n- **Humidity:** 65%\n- **Wind:** 12 km/h\n\nThe weather looks pleasant today!"
    
    elif "search" in query or "news" in query or "find" in query:
        tools_used.append("web_search")
        response = f"🔍 **Search Results:**\n\nI found several relevant results for your query:\n\n1. **Latest AI Developments** - Recent breakthroughs in artificial intelligence\n2. **Technology News** - Top stories from the tech world\n3. **Industry Updates** - Current trends and innovations\n\nWould you like me to provide more details on any of these?"
    
    elif "wikipedia" in query or "tell me about" in query:
        tools_used.append("wikipedia")
        response = f"📚 **Wikipedia Summary:**\n\nBased on your query, here's what I found:\n\nThis is a comprehensive topic with rich history and significance. The subject has evolved significantly over time and continues to be relevant today.\n\nWould you like me to provide more specific information?"
    
    elif "calculate" in query or "math" in query or any(char.isdigit() for char in query):
        tools_used.append("calculator")
        response = f"🔢 **Calculation Result:**\n\nBased on your query, the result is: **110**\n\n(25 × 4 + 10 = 110)\n\nNeed help with another calculation?"
    
    elif "email" in query:
        tools_used.append("email")
        response = f"📧 **Email Tool:**\n\nTo send an email, I'll need:\n- **To:** Recipient email address\n- **Subject:** Email subject\n- **Body:** Message content\n\nPlease provide these details and I'll send the email for you!"
    
    elif "file" in query:
        tools_used.append("file_manager")
        response = f"📁 **File Manager:**\n\nI can help you with:\n- Creating new files\n- Reading file contents\n- Organizing files\n- Deleting files\n\nWhat would you like me to do?"
    
    elif "cpu" in query or "system" in query or "monitor" in query:
        tools_used.append("system_monitor")
        response = f"📊 **System Status:**\n\n- **CPU Usage:** 45%\n- **Memory:** 8.2 GB / 16 GB (51%)\n- **Disk:** 256 GB / 512 GB (50%)\n- **Network:** Active\n\nYour system is running smoothly!"
    
    else:
        response = f"I understand you're asking: \"{request.get('query', '')}\"\n\nI have access to 17 powerful MCP tools including:\n- 🔍 Web Search\n- 🌤️ Weather/Climate\n- 📚 Wikipedia\n- 🔢 Calculator\n- 📧 Email\n- 📁 File Manager\n- 📊 System Monitor\n- And 10 more!\n\nHow can I help you today?"
    
    return {
        "success": True,
        "response": response,
        "tools_used": tools_used,
        "session_id": request.get("session_id", "test")
    }

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🚀 AI-MCP TEST SERVER STARTING")
    print("="*80)
    print(f"   • API: http://localhost:8000")
    print(f"   • Docs: http://localhost:8000/docs")
    print(f"   • Health: http://localhost:8000/health")
    print(f"   • Tools: http://localhost:8000/api/mcp/tools")
    print("="*80 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
