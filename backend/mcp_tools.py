"""Real MCP Tools Implementation with Actual APIs"""

import httpx
import asyncio
from datetime import datetime
import json
import re

class MCPTools:
    """Real MCP Tool implementations"""
    
    @staticmethod
    async def web_search(query: str):
        """Real web search using DuckDuckGo API"""
        try:
            async with httpx.AsyncClient() as client:
                url = "https://api.duckduckgo.com/"
                params = {
                    "q": query,
                    "format": "json",
                    "no_html": 1,
                    "skip_disambig": 1
                }
                response = await client.get(url, params=params, timeout=10.0)
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
                    "query": query,
                    "results": results if results else [{"title": "No results", "snippet": "Try a different search term"}],
                    "count": len(results)
                }
        except Exception as e:
            return {
                "success": False,
                "tool": "web_search",
                "error": str(e),
                "results": []
            }
    
    @staticmethod
    async def climate(location: str = None, query: str = ""):
        """Real weather data using wttr.in API"""
        try:
            # Extract location from query if not provided
            if not location or location == "auto-detect":
                # Try to extract city name from query
                location_match = re.search(r'in\s+([A-Za-z\s]+)', query, re.IGNORECASE)
                if location_match:
                    location = location_match.group(1).strip()
                else:
                    location = "London"  # Default
            
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
                        "visibility": f"{current.get('visibility', 'N/A')} km",
                        "uv_index": current.get('uvIndex', 'N/A')
                    }
                }
        except Exception as e:
            return {
                "success": False,
                "tool": "climate",
                "error": str(e),
                "data": {}
            }
    
    @staticmethod
    async def wikipedia(query: str):
        """Real Wikipedia search"""
        try:
            async with httpx.AsyncClient() as client:
                # Search for article
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
                
                # Get article summary
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
        except Exception as e:
            return {
                "success": False,
                "tool": "wikipedia",
                "error": str(e),
                "data": {}
            }
    
    @staticmethod
    async def calculator(expression: str, query: str = ""):
        """Real calculator using eval (safe subset)"""
        try:
            # Extract numbers and operators from query
            if not expression or expression == query:
                # Try to extract math expression from query
                math_match = re.search(r'[\d\s\+\-\*/\(\)\.]+', query)
                if math_match:
                    expression = math_match.group(0).strip()
            
            # Safe eval - only allow numbers and basic operators
            allowed_chars = set('0123456789+-*/()., ')
            if not all(c in allowed_chars for c in expression):
                return {
                    "success": False,
                    "tool": "calculator",
                    "error": "Invalid expression - only numbers and +, -, *, /, () allowed",
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
        except Exception as e:
            return {
                "success": False,
                "tool": "calculator",
                "error": str(e),
                "data": {}
            }
    
    @staticmethod
    async def system_monitor():
        """Real system monitoring using psutil"""
        try:
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
        except Exception as e:
            return {
                "success": False,
                "tool": "system_monitor",
                "error": str(e),
                "data": {}
            }
    
    @staticmethod
    async def email(to: str, subject: str, body: str):
        """Email tool - shows OAuth requirement"""
        return {
            "success": True,
            "tool": "email",
            "action": "prepared",
            "data": {
                "to": to,
                "subject": subject,
                "body": body,
                "status": "Ready to send via Gmail OAuth2",
                "note": "Email prepared. Gmail authentication required to send."
            },
            "requires_auth": True
        }
    
    @staticmethod
    async def translator(text: str, target_lang: str = "es"):
        """Translation using LibreTranslate API"""
        try:
            async with httpx.AsyncClient() as client:
                url = "https://libretranslate.de/translate"
                data = {
                    "q": text,
                    "source": "auto",
                    "target": target_lang,
                    "format": "text"
                }
                response = await client.post(url, json=data, timeout=10.0)
                result = response.json()
                
                return {
                    "success": True,
                    "tool": "translator",
                    "data": {
                        "original": text,
                        "translated": result.get("translatedText", ""),
                        "target_language": target_lang
                    }
                }
        except Exception as e:
            return {
                "success": False,
                "tool": "translator",
                "error": str(e),
                "data": {}
            }

# Tool executor
async def execute_mcp_tool(tool_name: str, query: str, params: dict = None):
    """Execute real MCP tool"""
    params = params or {}
    
    if tool_name == "web_search":
        return await MCPTools.web_search(params.get("query", query))
    
    elif tool_name == "climate":
        return await MCPTools.climate(params.get("location"), query)
    
    elif tool_name == "wikipedia":
        return await MCPTools.wikipedia(query)
    
    elif tool_name == "calculator":
        return await MCPTools.calculator(params.get("expression", query), query)
    
    elif tool_name == "system_monitor":
        return await MCPTools.system_monitor()
    
    elif tool_name == "email":
        return await MCPTools.email(
            params.get("to", "bharathreddyget@gmail.com"),
            params.get("subject", "From AI Assistant"),
            params.get("body", query)
        )
    
    elif tool_name == "translator":
        return await MCPTools.translator(query, params.get("target_lang", "es"))
    
    else:
        # Generic tool response
        return {
            "success": True,
            "tool": tool_name,
            "data": {
                "message": f"Tool {tool_name} executed",
                "note": "This tool needs real implementation"
            }
        }
