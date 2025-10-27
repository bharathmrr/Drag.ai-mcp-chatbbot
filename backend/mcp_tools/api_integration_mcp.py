"""API Integration MCP Tool - Call external APIs"""

from typing import Dict, Any
import httpx
import logging

logger = logging.getLogger(__name__)

class APIIntegrationTool:
    """MCP tool for external API integration"""
    
    def __init__(self):
        self.name = "api_integration"
        self.description = "Call external REST APIs and integrate with third-party services"
        self.enabled = True
        
    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute API integration operation
        
        Args:
            action: Operation type (get, post, put, delete, custom)
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with operation result
        """
        try:
            url = kwargs.get("url")
            headers = kwargs.get("headers", {})
            data = kwargs.get("data")
            params = kwargs.get("params")
            
            if action == "get":
                return await self._make_request("GET", url, headers=headers, params=params)
            elif action == "post":
                return await self._make_request("POST", url, headers=headers, json=data)
            elif action == "put":
                return await self._make_request("PUT", url, headers=headers, json=data)
            elif action == "delete":
                return await self._make_request("DELETE", url, headers=headers)
            elif action == "custom":
                method = kwargs.get("method", "GET")
                return await self._make_request(method, url, headers=headers, json=data, params=params)
            else:
                return {"success": False, "error": f"Unknown action: {action}"}
                
        except Exception as e:
            logger.error(f"❌ API integration error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _make_request(
        self,
        method: str,
        url: str,
        headers: Dict = None,
        json: Any = None,
        params: Dict = None
    ) -> Dict[str, Any]:
        """Make HTTP request"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=json,
                    params=params
                )
                
                # Try to parse JSON response
                try:
                    response_data = response.json()
                except:
                    response_data = response.text
                
                return {
                    "success": response.is_success,
                    "status_code": response.status_code,
                    "data": response_data,
                    "headers": dict(response.headers)
                }
                
        except httpx.TimeoutException:
            return {
                "success": False,
                "error": "Request timeout"
            }
        except httpx.RequestError as e:
            return {
                "success": False,
                "error": f"Request error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
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
                        "enum": ["get", "post", "put", "delete", "custom"],
                        "description": "HTTP method to use"
                    },
                    "url": {
                        "type": "string",
                        "description": "API endpoint URL"
                    },
                    "headers": {
                        "type": "object",
                        "description": "HTTP headers"
                    },
                    "data": {
                        "description": "Request body data"
                    },
                    "params": {
                        "type": "object",
                        "description": "URL query parameters"
                    },
                    "method": {
                        "type": "string",
                        "description": "Custom HTTP method (for custom action)"
                    }
                },
                "required": ["action", "url"]
            }
        }
