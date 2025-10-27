"""Wikipedia MCP Tool - Search and retrieve Wikipedia articles"""

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class WikipediaTool:
    """MCP tool for Wikipedia search and retrieval"""
    
    def __init__(self):
        self.name = "wikipedia"
        self.description = "Search Wikipedia and retrieve article summaries"
        self.enabled = True
        
    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute Wikipedia operation
        
        Args:
            action: Operation type (search, summary, content)
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with operation result
        """
        try:
            if action == "search":
                return await self._search(kwargs.get("query"), kwargs.get("limit", 5))
            elif action == "summary":
                return await self._get_summary(kwargs.get("title"))
            elif action == "content":
                return await self._get_content(kwargs.get("title"))
            else:
                return {"success": False, "error": f"Unknown action: {action}"}
                
        except Exception as e:
            logger.error(f"❌ Wikipedia operation error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _search(self, query: str, limit: int) -> Dict[str, Any]:
        """Search Wikipedia"""
        try:
            import wikipedia
            
            results = wikipedia.search(query, results=limit)
            
            return {
                "success": True,
                "action": "search",
                "query": query,
                "results": results,
                "count": len(results)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _get_summary(self, title: str) -> Dict[str, Any]:
        """Get article summary"""
        try:
            import wikipedia
            
            summary = wikipedia.summary(title, sentences=3)
            page = wikipedia.page(title)
            
            return {
                "success": True,
                "action": "summary",
                "title": title,
                "summary": summary,
                "url": page.url,
                "categories": page.categories[:5] if hasattr(page, 'categories') else []
            }
        except wikipedia.exceptions.DisambiguationError as e:
            return {
                "success": False,
                "error": "Disambiguation page",
                "options": e.options[:10]
            }
        except wikipedia.exceptions.PageError:
            return {
                "success": False,
                "error": f"Page '{title}' not found"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _get_content(self, title: str) -> Dict[str, Any]:
        """Get full article content"""
        try:
            import wikipedia
            
            page = wikipedia.page(title)
            
            return {
                "success": True,
                "action": "content",
                "title": page.title,
                "content": page.content[:2000],  # First 2000 chars
                "url": page.url,
                "images": page.images[:3] if hasattr(page, 'images') else [],
                "references": page.references[:5] if hasattr(page, 'references') else []
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
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
                        "enum": ["search", "summary", "content"],
                        "description": "Wikipedia operation to perform"
                    },
                    "query": {
                        "type": "string",
                        "description": "Search query (for search action)"
                    },
                    "title": {
                        "type": "string",
                        "description": "Article title (for summary/content actions)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of search results (default: 5)"
                    }
                },
                "required": ["action"]
            }
        }
