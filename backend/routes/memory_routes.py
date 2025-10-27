"""Memory Routes - Manage conversation memory"""

from fastapi import APIRouter, HTTPException
from typing import Optional

router = APIRouter()

@router.get("/logs")
async def get_tool_logs(
    session_id: Optional[str] = None,
    tool_name: Optional[str] = None,
    limit: int = 50
):
    """Get tool execution logs"""
    from main import db_service
    
    try:
        if db_service and db_service.is_connected():
            logs = await db_service.get_tool_logs(session_id, tool_name, limit)
            return {"success": True, "logs": logs, "count": len(logs)}
        
        return {"success": True, "logs": [], "message": "Database not connected"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_memory_stats():
    """Get memory and usage statistics"""
    from main import db_service, tool_registry
    
    try:
        stats = {
            "database_connected": db_service.is_connected() if db_service else False,
            "total_tools": len(tool_registry.get_all_tools()) if tool_registry else 0,
            "active_tools": len(tool_registry.get_active_tools()) if tool_registry else 0
        }
        
        return {"success": True, "stats": stats}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
