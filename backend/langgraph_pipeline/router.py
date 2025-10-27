"""Tool Router - Route queries to appropriate MCP tools"""

from typing import Dict, Any, List
import re
import logging

logger = logging.getLogger(__name__)

class ToolRouter:
    """Routes user queries to appropriate MCP tools"""
    
    def __init__(self, tool_registry):
        self.tool_registry = tool_registry
        
        # Tool keywords for routing
        self.tool_keywords = {
            "web_search": ["search", "find", "look up", "google", "web", "internet", "online"],
            "file_manager": ["file", "read", "write", "save", "open", "delete", "folder", "directory"],
            "database": ["database", "db", "query", "insert", "update", "delete", "collection", "record"],
            "email": ["email", "send", "mail", "message", "compose"],
            "drive": ["drive", "google drive", "upload", "download", "share"],
            "automation": ["automate", "workflow", "schedule", "run", "execute"],
            "memory": ["remember", "recall", "memory", "history", "context"],
            "analytics": ["analyze", "stats", "statistics", "trend", "data", "metrics"],
            "knowledgebase": ["knowledge", "kb", "article", "documentation", "wiki"],
            "api_integration": ["api", "endpoint", "rest", "http", "request"],
            "climate": ["weather", "climate", "temperature", "forecast", "rain", "sunny", "cloudy"],
            "wikipedia": ["wikipedia", "wiki", "encyclopedia", "definition", "explain"],
            "python_code": ["python", "code", "execute", "run code", "script", "program"],
            "screen_monitor": ["screen", "screenshot", "capture", "display", "monitor"],
            "system_monitor": ["system", "cpu", "memory", "disk", "performance", "process"],
            "calculator": ["calculate", "math", "convert", "equation", "plus", "minus", "multiply"],
            "translator": ["translate", "language", "translation", "spanish", "french", "german"]
        }
    
    async def route_query(self, query: str, active_tools: List[str] = None) -> Dict[str, Any]:
        """
        Route query to appropriate tools
        
        Args:
            query: User query
            active_tools: List of currently active tools
            
        Returns:
            Dictionary with routing decisions
        """
        query_lower = query.lower()
        
        # Determine which tools match
        matched_tools = []
        
        for tool_name, keywords in self.tool_keywords.items():
            # Only consider active tools
            if active_tools and tool_name not in active_tools:
                continue
            
            # Check if any keyword matches
            for keyword in keywords:
                if keyword in query_lower:
                    matched_tools.append({
                        "tool": tool_name,
                        "confidence": self._calculate_confidence(query_lower, keywords)
                    })
                    break
        
        # Sort by confidence
        matched_tools.sort(key=lambda x: x["confidence"], reverse=True)
        
        return {
            "query": query,
            "matched_tools": matched_tools,
            "primary_tool": matched_tools[0]["tool"] if matched_tools else None,
            "requires_multiple_tools": len(matched_tools) > 1
        }
    
    def _calculate_confidence(self, query: str, keywords: List[str]) -> float:
        """Calculate confidence score for tool match"""
        matches = sum(1 for keyword in keywords if keyword in query)
        return min(matches / len(keywords) + 0.5, 1.0)
    
    async def execute_tool(
        self,
        tool_name: str,
        action: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a specific tool
        
        Args:
            tool_name: Name of the tool
            action: Action to perform
            params: Action parameters
            
        Returns:
            Tool execution result
        """
        try:
            tool = self.tool_registry.get_tool(tool_name)
            
            if not tool:
                return {
                    "success": False,
                    "error": f"Tool '{tool_name}' not found or not active"
                }
            
            if not tool.enabled:
                return {
                    "success": False,
                    "error": f"Tool '{tool_name}' is disabled"
                }
            
            logger.info(f"🔧 Executing {tool_name}.{action}")
            
            # Execute tool
            result = await tool.execute(action=action, **params)
            
            return {
                "success": True,
                "tool": tool_name,
                "action": action,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"❌ Tool execution error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "tool": tool_name
            }
    
    async def execute_multi_tool(
        self,
        tool_actions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Execute multiple tools in sequence
        
        Args:
            tool_actions: List of tool actions to execute
            
        Returns:
            Combined results
        """
        results = []
        
        for tool_action in tool_actions:
            result = await self.execute_tool(
                tool_action["tool"],
                tool_action["action"],
                tool_action.get("params", {})
            )
            results.append(result)
        
        return {
            "success": all(r.get("success", False) for r in results),
            "results": results,
            "count": len(results)
        }
    
    def suggest_tools(self, query: str) -> List[str]:
        """Suggest tools based on query analysis"""
        routing = self.route_query(query)
        return [match["tool"] for match in routing["matched_tools"]]
