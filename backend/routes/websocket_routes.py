"""WebSocket Routes - Real-time communication"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Active WebSocket connections
active_connections: Dict[str, Set[WebSocket]] = {}

@router.websocket("/chat/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time chat"""
    await websocket.accept()
    
    # Add to active connections
    if session_id not in active_connections:
        active_connections[session_id] = set()
    active_connections[session_id].add(websocket)
    
    logger.info(f"🔌 WebSocket connected: {session_id}")
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Process based on message type
            if message.get("type") == "chat":
                await handle_chat_message(websocket, session_id, message)
            elif message.get("type") == "tool_toggle":
                await handle_tool_toggle(websocket, message)
            elif message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
            
    except WebSocketDisconnect:
        # Remove from active connections
        active_connections[session_id].discard(websocket)
        if not active_connections[session_id]:
            del active_connections[session_id]
        
        logger.info(f"🔌 WebSocket disconnected: {session_id}")
    
    except Exception as e:
        logger.error(f"❌ WebSocket error: {str(e)}")
        await websocket.close()

async def handle_chat_message(websocket: WebSocket, session_id: str, message: Dict):
    """Handle chat message via WebSocket"""
    from main import graph_builder
    
    try:
        query = message.get("query", "")
        active_tools = message.get("active_tools", [])
        
        # Send acknowledgment
        await websocket.send_json({
            "type": "processing",
            "message": "Processing your request..."
        })
        
        # Run through pipeline
        result = await graph_builder.run(
            query=query,
            session_id=session_id,
            active_tools=active_tools
        )
        
        # Send response
        await websocket.send_json({
            "type": "response",
            "data": result
        })
        
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "error": str(e)
        })

async def handle_tool_toggle(websocket: WebSocket, message: Dict):
    """Handle tool toggle via WebSocket"""
    from main import tool_registry
    
    try:
        tool_name = message.get("tool_name")
        enabled = message.get("enabled")
        
        if enabled:
            success = tool_registry.enable_tool(tool_name)
        else:
            success = tool_registry.disable_tool(tool_name)
        
        await websocket.send_json({
            "type": "tool_status",
            "tool_name": tool_name,
            "enabled": enabled,
            "success": success
        })
        
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "error": str(e)
        })

async def broadcast_to_session(session_id: str, message: Dict):
    """Broadcast message to all connections in a session"""
    if session_id in active_connections:
        for connection in active_connections[session_id]:
            try:
                await connection.send_json(message)
            except:
                pass
