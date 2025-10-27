"""MCP Routes - Manage MCP tools"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

router = APIRouter()

class ToolToggleRequest(BaseModel):
    tool_name: str
    enabled: bool

class ToolExecuteRequest(BaseModel):
    tool_name: str
    action: str
    params: Optional[Dict[str, Any]] = {}

@router.get("/tools")
async def list_tools():
    """List all available MCP tools"""
    from main import tool_registry
    
    try:
        tools_info = tool_registry.get_all_tools_info()
        return {
            "success": True,
            "tools": tools_info,
            "count": len(tools_info)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tools/{tool_name}")
async def get_tool_info(tool_name: str):
    """Get information about a specific tool"""
    from main import tool_registry
    
    try:
        tool_info = tool_registry.get_tool_info(tool_name)
        
        if not tool_info:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
        
        return {"success": True, "tool": tool_info}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tools/toggle")
async def toggle_tool(request: ToolToggleRequest):
    """Enable or disable a tool"""
    from main import tool_registry
    
    try:
        if request.enabled:
            success = tool_registry.enable_tool(request.tool_name)
        else:
            success = tool_registry.disable_tool(request.tool_name)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Tool '{request.tool_name}' not found")
        
        return {
            "success": True,
            "tool_name": request.tool_name,
            "enabled": request.enabled
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tools/execute")
async def execute_tool(request: ToolExecuteRequest):
    """Execute a tool action"""
    from main import graph_builder
    
    try:
        result = await graph_builder.router.execute_tool(
            request.tool_name,
            request.action,
            request.params
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tools/active")
async def get_active_tools():
    """Get list of currently active tools"""
    from main import tool_registry
    
    try:
        active_tools = tool_registry.get_active_tools()
        return {
            "success": True,
            "active_tools": active_tools,
            "count": len(active_tools)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
