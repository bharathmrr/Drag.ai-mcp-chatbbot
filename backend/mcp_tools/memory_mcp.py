"""Memory MCP Tool - Store and retrieve conversation memory"""

from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MemoryTool:
    """MCP tool for conversation memory management"""
    
    def __init__(self):
        self.name = "memory"
        self.description = "Store and retrieve conversation history and context"
        self.enabled = True
        self.memory_store = {}
        
    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute memory operation
        
        Args:
            action: Operation type (store, retrieve, search, clear)
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with operation result
        """
        try:
            if action == "store":
                return await self._store_memory(
                    kwargs.get("session_id"),
                    kwargs.get("key"),
                    kwargs.get("value")
                )
            elif action == "retrieve":
                return await self._retrieve_memory(kwargs.get("session_id"), kwargs.get("key"))
            elif action == "search":
                return await self._search_memory(kwargs.get("session_id"), kwargs.get("query"))
            elif action == "clear":
                return await self._clear_memory(kwargs.get("session_id"))
            else:
                return {"success": False, "error": f"Unknown action: {action}"}
                
        except Exception as e:
            logger.error(f"❌ Memory operation error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _store_memory(self, session_id: str, key: str, value: Any) -> Dict[str, Any]:
        """Store memory item"""
        if session_id not in self.memory_store:
            self.memory_store[session_id] = {}
        
        self.memory_store[session_id][key] = {
            "value": value,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return {
            "success": True,
            "action": "store",
            "session_id": session_id,
            "key": key
        }
    
    async def _retrieve_memory(self, session_id: str, key: str = None) -> Dict[str, Any]:
        """Retrieve memory item(s)"""
        if session_id not in self.memory_store:
            return {
                "success": True,
                "action": "retrieve",
                "session_id": session_id,
                "data": {}
            }
        
        if key:
            data = self.memory_store[session_id].get(key)
        else:
            data = self.memory_store[session_id]
        
        return {
            "success": True,
            "action": "retrieve",
            "session_id": session_id,
            "data": data
        }
    
    async def _search_memory(self, session_id: str, query: str) -> Dict[str, Any]:
        """Search memory items"""
        if session_id not in self.memory_store:
            return {
                "success": True,
                "action": "search",
                "results": []
            }
        
        results = []
        for key, item in self.memory_store[session_id].items():
            if query.lower() in str(item["value"]).lower():
                results.append({
                    "key": key,
                    "value": item["value"],
                    "timestamp": item["timestamp"]
                })
        
        return {
            "success": True,
            "action": "search",
            "query": query,
            "results": results,
            "count": len(results)
        }
    
    async def _clear_memory(self, session_id: str) -> Dict[str, Any]:
        """Clear session memory"""
        if session_id in self.memory_store:
            del self.memory_store[session_id]
        
        return {
            "success": True,
            "action": "clear",
            "session_id": session_id
        }
    
    def get_schema(self) -> Dict[str, Any]:
        """Return tool schema for LangChain"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["store", "retrieve", "search", "clear"],
                        "description": "Memory operation to perform"
                    },
                    "session_id": {
                        "type": "string",
                        "description": "Session identifier"
                    },
                    "key": {
                        "type": "string",
                        "description": "Memory key"
                    },
                    "value": {
                        "description": "Value to store"
                    },
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    }
                },
                "required": ["action", "session_id"]
            }
        }
