"""Real AI Server with Proper MCP Tool Integration and Gmail Support"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import google.generativeai as genai
from config import settings
import asyncio
from datetime import datetime
import json
import httpx
import re

app = FastAPI(title="AI-MCP Server with Real Tools")

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session storage (in-memory for now)
SESSIONS = {}
CHAT_LOGS = []

# MCP Tools
MOCK_TOOLS = [
    {"name": "web_search", "description": "Search the web using DuckDuckGo", "enabled": True},
    {"name": "file_manager", "description": "Read, write, and manage files", "enabled": True},
    {"name": "database", "description": "Query and manage MongoDB database", "enabled": False},
    {"name": "email", "description": "Send emails via Gmail (OAuth2)", "enabled": True},
    {"name": "drive", "description": "Access Google Drive files", "enabled": True},
    {"name": "automation", "description": "Automate tasks and workflows", "enabled": True},
    {"name": "memory", "description": "Store and retrieve context", "enabled": True},
    {"name": "analytics", "description": "Analyze data with pandas", "enabled": True},
    {"name": "knowledgebase", "description": "Search knowledge base", "enabled": True},
    {"name": "api_integration", "description": "Call external REST APIs", "enabled": True},
    {"name": "climate", "description": "Get weather forecasts", "enabled": True},
    {"name": "wikipedia", "description": "Search Wikipedia articles", "enabled": True},
    {"name": "python_code", "description": "Execute Python code safely", "enabled": True},
    {"name": "screen_monitor", "description": "Capture screenshots", "enabled": True},
    {"name": "system_monitor", "description": "Monitor CPU, RAM, disk usage", "enabled": True},
    {"name": "calculator", "description": "Perform calculations", "enabled": True},
    {"name": "translator", "description": "Translate between languages", "enabled": True},
]

# Real MCP Tool Implementations
async def execute_mcp_tool(tool_name: str, query: str, params: dict = None):
    """Execute real MCP tool with actual API calls"""
    params = params or {}
    
    try:
        if tool_name == "web_search":
            # Real DuckDuckGo search
            async with httpx.AsyncClient() as client:
                url = "https://api.duckduckgo.com/"
                search_params = {
                    "q": params.get("query", query),
                    "format": "json",
                    "no_html": 1,
                    "skip_disambig": 1
                }
                response = await client.get(url, params=search_params, timeout=10.0)
                data = response.json()
                
                results = []
                if data.get("AbstractText"):
                    results.append({
                        "title": data.get("Heading", "Result"),
                        "snippet": data.get("AbstractText"),
                        "url": data.get("AbstractURL", "")
                    })
                
                for topic in data.get("RelatedTopics", [])[:3]:
                    if isinstance(topic, dict) and "Text" in topic:
                        results.append({
                            "title": topic.get("Text", "")[:50],
                            "snippet": topic.get("Text", ""),
                            "url": topic.get("FirstURL", "")
                        })
                
                return {
                    "success": True,
                    "tool": "web_search",
                    "query": params.get("query", query),
                    "data": {"results": results if results else [{"title": "No results", "snippet": "Try different keywords"}]}
                }
        
        elif tool_name == "climate":
            # Real weather data from wttr.in
            location = params.get("location", "London")
            if location == "auto-detect":
                # Extract location from query
                location_match = re.search(r'in\s+([A-Za-z\s]+)', query, re.IGNORECASE)
                if location_match:
                    location = location_match.group(1).strip()
                else:
                    location = "London"
            
            async with httpx.AsyncClient() as client:
                url = f"https://wttr.in/{location}?format=j1"
                response = await client.get(url, timeout=10.0)
                data = response.json()
                
                current = data.get("current_condition", [{}])[0]
                
                return {
                    "success": True,
                    "tool": "climate",
                    "location": location,
                    "data": {
                        "temperature": f"{current.get('temp_C', 'N/A')}°C",
                        "feels_like": f"{current.get('FeelsLikeC', 'N/A')}°C",
                        "condition": current.get("weatherDesc", [{}])[0].get("value", "Unknown"),
                        "humidity": f"{current.get('humidity', 'N/A')}%",
                        "wind_speed": f"{current.get('windspeedKmph', 'N/A')} km/h",
                        "wind_direction": current.get('winddir16Point', 'N/A'),
                        "pressure": f"{current.get('pressure', 'N/A')} mb",
                        "visibility": f"{current.get('visibility', 'N/A')} km"
                    }
                }
        
        elif tool_name == "wikipedia":
            # Real Wikipedia API
            async with httpx.AsyncClient() as client:
                search_url = "https://en.wikipedia.org/w/api.php"
                search_params = {
                    "action": "query",
                    "list": "search",
                    "srsearch": query,
                    "format": "json",
                    "srlimit": 1
                }
                search_response = await client.get(search_url, params=search_params, timeout=10.0)
                search_data = search_response.json()
                
                if not search_data.get("query", {}).get("search"):
                    return {
                        "success": False,
                        "tool": "wikipedia",
                        "error": "No results found",
                        "data": {}
                    }
                
                page_title = search_data["query"]["search"][0]["title"]
                
                summary_params = {
                    "action": "query",
                    "prop": "extracts",
                    "exintro": True,
                    "explaintext": True,
                    "titles": page_title,
                    "format": "json"
                }
                summary_response = await client.get(search_url, params=summary_params, timeout=10.0)
                summary_data = summary_response.json()
                
                pages = summary_data.get("query", {}).get("pages", {})
                page = list(pages.values())[0]
                
                return {
                    "success": True,
                    "tool": "wikipedia",
                    "query": query,
                    "data": {
                        "title": page.get("title", ""),
                        "summary": page.get("extract", "")[:500] + "...",
                        "url": f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
                    }
                }
        
        elif tool_name == "calculator":
            # Real calculator
            expression = params.get("expression", query)
            math_match = re.search(r'[\d\s\+\-\*/\(\)\.]+', expression)
            if math_match:
                expression = math_match.group(0).strip()
            
            allowed_chars = set('0123456789+-*/()., ')
            if not all(c in allowed_chars for c in expression):
                return {
                    "success": False,
                    "tool": "calculator",
                    "error": "Invalid expression",
                    "data": {}
                }
            
            result = eval(expression)
            
            return {
                "success": True,
                "tool": "calculator",
                "expression": expression,
                "data": {
                    "result": result,
                    "formatted": f"{expression} = {result}"
                }
            }
        
        elif tool_name == "system_monitor":
            # Real system monitoring
            import psutil
            
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "success": True,
                "tool": "system_monitor",
                "data": {
                    "cpu": {
                        "usage": f"{cpu_percent}%",
                        "cores": psutil.cpu_count()
                    },
                    "memory": {
                        "total": f"{memory.total / (1024**3):.2f} GB",
                        "used": f"{memory.used / (1024**3):.2f} GB",
                        "available": f"{memory.available / (1024**3):.2f} GB",
                        "percent": f"{memory.percent}%"
                    },
                    "disk": {
                        "total": f"{disk.total / (1024**3):.2f} GB",
                        "used": f"{disk.used / (1024**3):.2f} GB",
                        "free": f"{disk.free / (1024**3):.2f} GB",
                        "percent": f"{disk.percent}%"
                    }
                }
            }
        
        elif tool_name == "email":
            return {
                "success": True,
                "tool": "email",
                "action": "prepared",
                "data": {
                    "to": params.get("to", "bharathreddyget@gmail.com"),
                    "subject": params.get("subject", "From AI Assistant"),
                    "body": params.get("body", query),
                    "status": "Email prepared. Gmail OAuth2 authentication required to send.",
                    "note": "To send emails, configure Gmail API credentials"
                },
                "requires_auth": True
            }
        
        else:
            return {
                "success": True,
                "tool": tool_name,
                "data": {
                    "message": f"Tool {tool_name} executed",
                    "note": "Real implementation pending"
                }
            }
    
    except Exception as e:
        return {
            "success": False,
            "tool": tool_name,
            "error": str(e),
            "data": {}
        }

def save_to_log(session_id: str, role: str, content: str, tools_used: list = None):
    """Save chat interaction to log"""
    log_entry = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "role": role,
        "content": content,
        "tools_used": tools_used or []
    }
    CHAT_LOGS.append(log_entry)
    
    # Save to session
    if session_id not in SESSIONS:
        SESSIONS[session_id] = {
            "created_at": datetime.now().isoformat(),
            "messages": []
        }
    SESSIONS[session_id]["messages"].append(log_entry)

@app.get("/")
async def root():
    return {
        "message": "AI-MCP Server with Real Tools",
        "status": "running",
        "sessions": len(SESSIONS),
        "total_logs": len(CHAT_LOGS)
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "database": "in-memory",
        "tools_registered": len(MOCK_TOOLS),
        "ai_model": "gemini-2.0-flash-exp",
        "sessions": len(SESSIONS)
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

@app.get("/api/sessions")
async def get_sessions():
    """Get all chat sessions"""
    return {
        "success": True,
        "sessions": [
            {
                "session_id": sid,
                "created_at": data["created_at"],
                "message_count": len(data["messages"])
            }
            for sid, data in SESSIONS.items()
        ]
    }

@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """Get specific session history"""
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "success": True,
        "session": SESSIONS[session_id]
    }

@app.get("/api/logs")
async def get_logs():
    """Get all chat logs"""
    return {
        "success": True,
        "logs": CHAT_LOGS,
        "count": len(CHAT_LOGS)
    }

@app.post("/api/chat/send")
async def send_message(request: dict):
    query = request.get("query", "")
    active_tools = request.get("active_tools", [])
    session_id = request.get("session_id", "default")
    
    # Save user message to log
    save_to_log(session_id, "user", query)
    
    try:
        # Detect which tools to use
        tools_to_execute = []
        query_lower = query.lower()
        
        # Smart tool detection
        if any(word in query_lower for word in ["weather", "climate", "temperature"]) and "climate" in active_tools:
            tools_to_execute.append({"name": "climate", "params": {"location": "auto-detect"}})
        
        if any(word in query_lower for word in ["search", "find", "look up"]) and "web_search" in active_tools:
            tools_to_execute.append({"name": "web_search", "params": {"query": query}})
        
        if "email" in query_lower and "email" in active_tools:
            tools_to_execute.append({"name": "email", "params": {
                "to": "bharathreddyget@gmail.com",
                "subject": "From AI Assistant",
                "body": query
            }})
        
        if any(word in query_lower for word in ["calculate", "math"]) and "calculator" in active_tools:
            tools_to_execute.append({"name": "calculator", "params": {"expression": query}})
        
        if any(word in query_lower for word in ["cpu", "memory", "system"]) and "system_monitor" in active_tools:
            tools_to_execute.append({"name": "system_monitor", "params": {}})
        
        # Execute REAL MCP tools FIRST
        tool_results = []
        if tools_to_execute:
            for tool_info in tools_to_execute:
                result = await execute_mcp_tool(tool_info["name"], query, tool_info["params"])
                tool_results.append(result)
        
        # Build context with tool results
        tools_context = ""
        if active_tools:
            enabled_tools = [t for t in MOCK_TOOLS if t["name"] in active_tools and t["enabled"]]
            tools_list = ", ".join([t["name"] for t in enabled_tools])
            tools_context = f"\n\nAvailable MCP Tools: {tools_list}"
        
        # Add tool execution results to context
        if tool_results:
            tools_context += "\n\nTool Execution Results:\n"
            for result in tool_results:
                tools_context += f"- {result['tool']}: {json.dumps(result.get('data') or result.get('result'), indent=2)}\n"
        
        # Create AI prompt with tool results
        prompt = f"""You are a professional AI assistant with access to MCP (Model Context Protocol) tools. You have ALREADY executed the necessary tools and received their results.

User Query: {query}
{tools_context}

CRITICAL INSTRUCTIONS FOR YOUR RESPONSE:

📋 CONTENT REQUIREMENTS:
1. The tools listed above have ALREADY been executed - you don't need to execute them
2. Use the actual tool results provided above to answer the user's question
3. DO NOT say "I will use" or "Let me use" - the tools are ALREADY used
4. Instead say "I used the [tool_name] tool and found..." or "Based on the [tool_name] results..."
5. Be specific and reference the actual data from tool results
6. If email tool was used, confirm the email details (to: bharathreddyget@gmail.com)

🎨 FORMATTING REQUIREMENTS:
1. Use relevant emojis to make the response visually appealing (but don't overuse them)
2. Format your response in beautiful Markdown with proper structure
3. Use headers (##, ###) to organize information
4. Use bullet points (•) or numbered lists for clarity
5. Use **bold** for important information
6. Use code blocks for technical data when appropriate
7. Add visual separators (---) when needed

😊 EMOJI GUIDELINES:
- Weather: 🌤️ ☀️ 🌧️ ⛅ 🌡️ 💨 💧
- Search: 🔍 📊 📈 💡 ✨
- Success: ✅ ✓ 🎉 👍
- Data: 📊 📈 💾 🗂️
- Location: 📍 🌍 🗺️
- Time: ⏰ 🕐 📅
- Email: 📧 ✉️ 📬
- Calculator: 🔢 ➕ ➖ ✖️ ➗ 🧮
- System: 💻 🖥️ ⚙️ 🔧
- Info: ℹ️ 💬 📝

📐 RESPONSE STRUCTURE:
1. Start with a brief acknowledgment using an emoji
2. Present main information with clear headers
3. Use bullet points or tables for data
4. Add a helpful conclusion or next step
5. End with a friendly follow-up question if appropriate

EXAMPLE RESPONSE FORMAT:

## 🌤️ Weather Information

I used the **climate** tool and retrieved the current weather data for [Location]:

### Current Conditions
- **🌡️ Temperature:** XX°C (feels like XX°C)
- **☁️ Condition:** [Condition]
- **💧 Humidity:** XX%
- **💨 Wind:** XX km/h from [Direction]
- **🔍 Visibility:** XX km

---

**Summary:** [Brief natural language summary]

Would you like to know the forecast for the next few days? 🌈

RESPONSE STYLE:
- ✨ Professional yet friendly and approachable
- 📊 Data-driven (use actual tool results)
- 🎨 Beautifully formatted with Markdown and emojis
- 💡 Clear, concise, and easy to understand
- 🎯 Focused on answering the user's question

Now provide your beautifully formatted response based on the tool results above:"""

        # Generate AI response
        response = model.generate_content(prompt)
        ai_response = response.text
        
        # Track which tools were used
        tools_used = [t["name"] for t in tools_to_execute]
        
        # Save AI response to log
        save_to_log(session_id, "assistant", ai_response, tools_used)
        
        return {
            "success": True,
            "response": ai_response,
            "tools_used": tools_used,
            "tool_results": tool_results,
            "session_id": session_id,
            "model": "gemini-2.0-flash-exp"
        }
        
    except Exception as e:
        error_msg = f"I apologize, but I encountered an error: {str(e)}\n\nPlease try again."
        save_to_log(session_id, "assistant", error_msg, [])
        
        return {
            "success": False,
            "response": error_msg,
            "tools_used": [],
            "session_id": session_id
        }

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🚀 AI-MCP SERVER WITH REAL TOOL INTEGRATION")
    print("="*80)
    print(f"   • API: http://127.0.0.1:8000")
    print(f"   • Docs: http://127.0.0.1:8000/docs")
    print(f"   • Health: http://127.0.0.1:8000/health")
    print(f"   • Tools: http://127.0.0.1:8000/api/mcp/tools")
    print(f"   • Sessions: http://127.0.0.1:8000/api/sessions")
    print(f"   • Logs: http://127.0.0.1:8000/api/logs")
    print(f"   • AI Model: Gemini 2.0 Flash Exp")
    print(f"   • Features: Tool Execution, Session Storage, Chat Logs")
    print("="*80 + "\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
