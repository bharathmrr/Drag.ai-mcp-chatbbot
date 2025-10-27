"""Chat Routes - Handle chat interactions"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    active_tools: Optional[List[str]] = None

class ChatResponse(BaseModel):
    success: bool
    response: str
    session_id: str
    tool_results: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """Send a chat message and get AI response"""
    from main import graph_builder, db_service
    
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Get active tools
        active_tools = request.active_tools or []
        
        # Run through LangGraph pipeline
        result = await graph_builder.run(
            query=request.query,
            session_id=session_id,
            active_tools=active_tools
        )
        
        # Save to database
        if db_service and db_service.is_connected():
            await db_service.save_chat_message(
                session_id=session_id,
                role="user",
                content=request.query
            )
            await db_service.save_chat_message(
                session_id=session_id,
                role="assistant",
                content=result.get("response", "")
            )
        
        return ChatResponse(
            success=result.get("success", False),
            response=result.get("response", ""),
            session_id=session_id,
            tool_results=result.get("tool_results"),
            error=result.get("error")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}")
async def get_chat_history(session_id: str, limit: int = 50):
    """Get chat history for a session"""
    from main import db_service, graph_builder
    
    try:
        # Try database first
        if db_service and db_service.is_connected():
            history = await db_service.get_chat_history(session_id, limit)
            return {"success": True, "history": history, "session_id": session_id}
        
        # Fall back to in-memory
        history = graph_builder.llm_agent.get_session_history(session_id)
        return {"success": True, "history": history, "session_id": session_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Clear a chat session"""
    from main import graph_builder
    
    try:
        graph_builder.llm_agent.clear_session(session_id)
        return {"success": True, "message": f"Session {session_id} cleared"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions")
async def list_sessions(limit: int = 20):
    """List recent chat sessions"""
    from main import db_service
    
    try:
        if db_service and db_service.is_connected():
            sessions = await db_service.get_sessions(limit)
            return {"success": True, "sessions": sessions}
        
        return {"success": True, "sessions": [], "message": "Database not connected"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
