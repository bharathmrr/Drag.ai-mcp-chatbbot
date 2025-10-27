from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from typing import Dict
from config import settings
from routes import chat_routes, mcp_routes, memory_routes, websocket_routes
from services.db_service import DatabaseService
from utils.tool_registry import ToolRegistry
from langgraph_pipeline.graph_builder import GraphBuilder

# Configure logging with colors
import sys
from datetime import datetime

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for terminal"""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
    }
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{self.BOLD}{record.levelname}{self.RESET}"
        record.name = f"{self.BOLD}{record.name}{self.RESET}"
        return super().format(record)

# Setup logging
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(ColoredFormatter(
    '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    datefmt='%H:%M:%S'
))

logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    handlers=[handler]
)
logger = logging.getLogger(__name__)

# Global instances
db_service = None
tool_registry = None
graph_builder = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global db_service, tool_registry, graph_builder
    
    # Startup banner
    print("\n" + "="*80)
    print("🚀 AI-MCP ORCHESTRATOR - SERVER STARTING")
    print("="*80)
    logger.info("Initializing system components...")
    
    try:
        # Initialize database
        db_service = DatabaseService()
        await db_service.connect()
        logger.info("✅ Database connected successfully")
        
        # Initialize tool registry
        tool_registry = ToolRegistry()
        await tool_registry.register_all_tools()
        active_tools = tool_registry.get_active_tools()
        logger.info(f"✅ Registered {len(active_tools)} MCP tools")
        
        # Log all registered tools
        print("\n📦 REGISTERED MCP TOOLS:")
        for tool_name in active_tools:
            print(f"   • {tool_name}")
        
        # Initialize LangGraph
        graph_builder = GraphBuilder(tool_registry)
        logger.info("✅ LangGraph pipeline initialized")
        
        # Server info
        print("\n" + "="*80)
        print(f"🌐 SERVER RUNNING")
        print(f"   • Host: {settings.HOST}")
        print(f"   • Port: {settings.PORT}")
        print(f"   • API: http://localhost:{settings.PORT}")
        print(f"   • Docs: http://localhost:{settings.PORT}/docs")
        print(f"   • Health: http://localhost:{settings.PORT}/health")
        print(f"   • Debug Mode: {'ON' if settings.DEBUG else 'OFF'}")
        print(f"   • Model: {settings.GEMINI_MODEL}")
        print("="*80 + "\n")
        logger.info("🎉 System ready! Waiting for requests...")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    print("\n" + "="*80)
    logger.info("🛑 Shutting down AI-MCP Orchestrator...")
    await db_service.disconnect()
    logger.info("✅ Cleanup complete")
    print("="*80 + "\n")

# Create FastAPI app
app = FastAPI(
    title="AI-MCP Orchestrator",
    description="ChatGPT-style AI system with LangChain, LangGraph, and 10+ MCP tools",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_routes.router, prefix="/api/chat", tags=["Chat"])
app.include_router(mcp_routes.router, prefix="/api/mcp", tags=["MCP Tools"])
app.include_router(memory_routes.router, prefix="/api/memory", tags=["Memory"])
app.include_router(websocket_routes.router, prefix="/api/ws", tags=["WebSocket"])

@app.get("/")
async def root():
    return {
        "message": "AI-MCP Orchestrator API",
        "version": "1.0.0",
        "status": "running",
        "active_tools": len(tool_registry.get_active_tools()) if tool_registry else 0
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected" if db_service and db_service.is_connected() else "disconnected",
        "tools_registered": len(tool_registry.get_active_tools()) if tool_registry else 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
