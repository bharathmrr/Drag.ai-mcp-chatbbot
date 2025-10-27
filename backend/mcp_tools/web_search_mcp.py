"""Web Search MCP Tool - Search the web using DuckDuckGo"""

import asyncio
from typing import Dict, Any, List
from duckduckgo_search import DDGS
import logging

logger = logging.getLogger(__name__)

class WebSearchTool:
    """MCP tool for web searching"""
    
    def __init__(self):
        self.name = "web_search"
        self.description = "Search the web for information using DuckDuckGo"
        self.enabled = True
        
    async def execute(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Execute web search
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            Dictionary with search results
        """
        try:
            logger.info(f"🔍 Web Search: {query}")
            
            # Run search in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None,
                self._search_sync,
                query,
                max_results
            )
            
            return {
                "success": True,
                "query": query,
                "results": results,
                "count": len(results)
            }
            
        except Exception as e:
            logger.error(f"❌ Web search error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "query": query
            }
    
    def _search_sync(self, query: str, max_results: int) -> List[Dict[str, str]]:
        """Synchronous search helper"""
        with DDGS() as ddgs:
            results = []
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", "")
                })
            return results
    
    def get_schema(self) -> Dict[str, Any]:
        """Return tool schema for LangChain"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }
