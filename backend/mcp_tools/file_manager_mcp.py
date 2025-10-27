"""File Manager MCP Tool - Handle file operations"""

import os
import aiofiles
from typing import Dict, Any, List
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class FileManagerTool:
    """MCP tool for file management"""
    
    def __init__(self):
        self.name = "file_manager"
        self.description = "Read, write, list, and manage files"
        self.enabled = True
        self.base_path = Path("./workspace")
        self.base_path.mkdir(exist_ok=True)
        
    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute file operation
        
        Args:
            action: Operation type (read, write, list, delete, exists)
            **kwargs: Additional parameters based on action
            
        Returns:
            Dictionary with operation result
        """
        try:
            if action == "read":
                return await self._read_file(kwargs.get("path"))
            elif action == "write":
                return await self._write_file(kwargs.get("path"), kwargs.get("content"))
            elif action == "list":
                return await self._list_files(kwargs.get("path", "."))
            elif action == "delete":
                return await self._delete_file(kwargs.get("path"))
            elif action == "exists":
                return await self._file_exists(kwargs.get("path"))
            else:
                return {"success": False, "error": f"Unknown action: {action}"}
                
        except Exception as e:
            logger.error(f"❌ File operation error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _read_file(self, path: str) -> Dict[str, Any]:
        """Read file content"""
        file_path = self.base_path / path
        
        if not file_path.exists():
            return {"success": False, "error": "File not found"}
        
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            content = await f.read()
        
        return {
            "success": True,
            "path": path,
            "content": content,
            "size": file_path.stat().st_size
        }
    
    async def _write_file(self, path: str, content: str) -> Dict[str, Any]:
        """Write content to file"""
        file_path = self.base_path / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
            await f.write(content)
        
        return {
            "success": True,
            "path": path,
            "size": len(content)
        }
    
    async def _list_files(self, path: str) -> Dict[str, Any]:
        """List files in directory"""
        dir_path = self.base_path / path
        
        if not dir_path.exists():
            return {"success": False, "error": "Directory not found"}
        
        files = []
        for item in dir_path.iterdir():
            files.append({
                "name": item.name,
                "type": "directory" if item.is_dir() else "file",
                "size": item.stat().st_size if item.is_file() else 0
            })
        
        return {
            "success": True,
            "path": path,
            "files": files,
            "count": len(files)
        }
    
    async def _delete_file(self, path: str) -> Dict[str, Any]:
        """Delete file"""
        file_path = self.base_path / path
        
        if not file_path.exists():
            return {"success": False, "error": "File not found"}
        
        file_path.unlink()
        
        return {"success": True, "path": path}
    
    async def _file_exists(self, path: str) -> Dict[str, Any]:
        """Check if file exists"""
        file_path = self.base_path / path
        
        return {
            "success": True,
            "path": path,
            "exists": file_path.exists()
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
                        "enum": ["read", "write", "list", "delete", "exists"],
                        "description": "File operation to perform"
                    },
                    "path": {
                        "type": "string",
                        "description": "File or directory path"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write (for write action)"
                    }
                },
                "required": ["action"]
            }
        }
