"""Screen Monitor MCP Tool - Capture and analyze screen information"""

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class ScreenMonitorTool:
    """MCP tool for screen monitoring and capture"""
    
    def __init__(self):
        self.name = "screen_monitor"
        self.description = "Monitor screen, capture screenshots, and get display information"
        self.enabled = True
        
    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute screen monitor operation
        
        Args:
            action: Operation type (info, screenshot, monitors)
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with operation result
        """
        try:
            if action == "info":
                return await self._get_screen_info()
            elif action == "screenshot":
                return await self._take_screenshot(kwargs.get("filename", "screenshot.png"))
            elif action == "monitors":
                return await self._get_monitors()
            elif action == "resolution":
                return await self._get_resolution()
            else:
                return {"success": False, "error": f"Unknown action: {action}"}
                
        except Exception as e:
            logger.error(f"❌ Screen monitor error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _get_screen_info(self) -> Dict[str, Any]:
        """Get screen information"""
        try:
            import screeninfo
            
            monitors = screeninfo.get_monitors()
            
            info = {
                "success": True,
                "action": "info",
                "monitor_count": len(monitors),
                "monitors": []
            }
            
            for i, monitor in enumerate(monitors):
                info["monitors"].append({
                    "index": i,
                    "name": monitor.name,
                    "width": monitor.width,
                    "height": monitor.height,
                    "width_mm": monitor.width_mm,
                    "height_mm": monitor.height_mm,
                    "is_primary": monitor.is_primary
                })
            
            return info
            
        except Exception as e:
            return {
                "success": True,
                "action": "info",
                "monitor_count": 1,
                "monitors": [{
                    "index": 0,
                    "name": "Primary",
                    "width": 1920,
                    "height": 1080,
                    "is_primary": True
                }],
                "note": "Using default values - install screeninfo for actual data"
            }
    
    async def _take_screenshot(self, filename: str) -> Dict[str, Any]:
        """Take a screenshot"""
        try:
            import pyautogui
            from pathlib import Path
            
            # Save to workspace
            workspace = Path("./workspace")
            workspace.mkdir(exist_ok=True)
            
            filepath = workspace / filename
            screenshot = pyautogui.screenshot()
            screenshot.save(str(filepath))
            
            return {
                "success": True,
                "action": "screenshot",
                "filename": filename,
                "path": str(filepath),
                "size": {
                    "width": screenshot.width,
                    "height": screenshot.height
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Screenshot failed: {str(e)}",
                "note": "Install pyautogui and pillow for screenshot functionality"
            }
    
    async def _get_monitors(self) -> Dict[str, Any]:
        """Get list of all monitors"""
        try:
            import screeninfo
            
            monitors = screeninfo.get_monitors()
            
            monitor_list = []
            for monitor in monitors:
                monitor_list.append({
                    "name": monitor.name,
                    "resolution": f"{monitor.width}x{monitor.height}",
                    "position": f"({monitor.x}, {monitor.y})",
                    "primary": monitor.is_primary
                })
            
            return {
                "success": True,
                "action": "monitors",
                "count": len(monitor_list),
                "monitors": monitor_list
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _get_resolution(self) -> Dict[str, Any]:
        """Get screen resolution"""
        try:
            import pyautogui
            
            size = pyautogui.size()
            
            return {
                "success": True,
                "action": "resolution",
                "width": size.width,
                "height": size.height,
                "resolution": f"{size.width}x{size.height}"
            }
            
        except Exception as e:
            return {
                "success": True,
                "action": "resolution",
                "width": 1920,
                "height": 1080,
                "resolution": "1920x1080",
                "note": "Using default values"
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
                        "enum": ["info", "screenshot", "monitors", "resolution"],
                        "description": "Screen operation to perform"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Screenshot filename (for screenshot action)"
                    }
                },
                "required": ["action"]
            }
        }
