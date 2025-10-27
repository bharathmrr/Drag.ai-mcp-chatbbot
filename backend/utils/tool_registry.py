"""Tool Registry - Register and manage MCP tools"""

from typing import Dict, Any, List, Optional
from mcp_tools import (
    WebSearchTool,
    FileManagerTool,
    DatabaseTool,
    EmailTool,
    DriveTool,
    AutomationTool,
    MemoryTool,
    AnalyticsTool,
    KnowledgebaseTool,
    APIIntegrationTool,
    ClimateTool,
    WikipediaTool,
    PythonCodeTool,
    ScreenMonitorTool,
    SystemMonitorTool,
    CalculatorTool,
    TranslatorTool
)
import logging

logger = logging.getLogger(__name__)

class ToolRegistry:
    """Registry for managing MCP tools"""
    
    def __init__(self):
        self.tools: Dict[str, Any] = {}
        self.tool_status: Dict[str, bool] = {}
    
    async def register_all_tools(self):
        """Register all available MCP tools"""
        tool_classes = [
            WebSearchTool,
            FileManagerTool,
            DatabaseTool,
            EmailTool,
            DriveTool,
            AutomationTool,
            MemoryTool,
            AnalyticsTool,
            KnowledgebaseTool,
            APIIntegrationTool,
            ClimateTool,
            WikipediaTool,
            PythonCodeTool,
            ScreenMonitorTool,
            SystemMonitorTool,
            CalculatorTool,
            TranslatorTool
        ]
        
        for tool_class in tool_classes:
            try:
                tool = tool_class()
                
                # Initialize if needed
                if hasattr(tool, 'initialize'):
                    await tool.initialize()
                
                self.tools[tool.name] = tool
                self.tool_status[tool.name] = tool.enabled
                
                logger.info(f"✅ Registered tool: {tool.name}")
                
            except Exception as e:
                logger.error(f"❌ Failed to register {tool_class.__name__}: {str(e)}")
    
    def get_tool(self, tool_name: str) -> Optional[Any]:
        """Get tool by name"""
        return self.tools.get(tool_name)
    
    def get_all_tools(self) -> Dict[str, Any]:
        """Get all registered tools"""
        return self.tools
    
    def get_active_tools(self) -> List[str]:
        """Get list of active tool names"""
        return [
            name for name, status in self.tool_status.items()
            if status
        ]
    
    def enable_tool(self, tool_name: str) -> bool:
        """Enable a tool"""
        if tool_name in self.tools:
            self.tools[tool_name].enabled = True
            self.tool_status[tool_name] = True
            logger.info(f"✅ Enabled tool: {tool_name}")
            return True
        return False
    
    def disable_tool(self, tool_name: str) -> bool:
        """Disable a tool"""
        if tool_name in self.tools:
            self.tools[tool_name].enabled = False
            self.tool_status[tool_name] = False
            logger.info(f"⏸️ Disabled tool: {tool_name}")
            return True
        return False
    
    def toggle_tool(self, tool_name: str) -> bool:
        """Toggle tool status"""
        if tool_name in self.tools:
            current_status = self.tool_status[tool_name]
            new_status = not current_status
            
            self.tools[tool_name].enabled = new_status
            self.tool_status[tool_name] = new_status
            
            logger.info(f"🔄 Toggled {tool_name}: {new_status}")
            return new_status
        return False
    
    def get_tool_info(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get tool information"""
        tool = self.tools.get(tool_name)
        if not tool:
            return None
        
        return {
            "name": tool.name,
            "description": tool.description,
            "enabled": tool.enabled,
            "schema": tool.get_schema() if hasattr(tool, 'get_schema') else None
        }
    
    def get_all_tools_info(self) -> List[Dict[str, Any]]:
        """Get information for all tools"""
        return [
            self.get_tool_info(name)
            for name in self.tools.keys()
        ]
