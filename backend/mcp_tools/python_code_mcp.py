"""Python Code Execution MCP Tool - Execute Python code safely"""

from typing import Dict, Any
import sys
from io import StringIO
import logging

logger = logging.getLogger(__name__)

class PythonCodeTool:
    """MCP tool for Python code execution"""
    
    def __init__(self):
        self.name = "python_code"
        self.description = "Execute Python code and return results (safe sandbox)"
        self.enabled = True
        
    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute Python code operation
        
        Args:
            action: Operation type (run, validate, analyze)
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with operation result
        """
        try:
            if action == "run":
                return await self._run_code(kwargs.get("code"))
            elif action == "validate":
                return await self._validate_code(kwargs.get("code"))
            elif action == "analyze":
                return await self._analyze_code(kwargs.get("code"))
            else:
                return {"success": False, "error": f"Unknown action: {action}"}
                
        except Exception as e:
            logger.error(f"❌ Python code operation error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _run_code(self, code: str) -> Dict[str, Any]:
        """Execute Python code in a safe environment"""
        if not code:
            return {"success": False, "error": "No code provided"}
        
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        result = {
            "success": False,
            "action": "run",
            "code": code,
            "output": "",
            "error": None
        }
        
        try:
            # Create a restricted namespace
            namespace = {
                '__builtins__': {
                    'print': print,
                    'len': len,
                    'range': range,
                    'str': str,
                    'int': int,
                    'float': float,
                    'list': list,
                    'dict': dict,
                    'set': set,
                    'tuple': tuple,
                    'abs': abs,
                    'max': max,
                    'min': min,
                    'sum': sum,
                    'sorted': sorted,
                    'enumerate': enumerate,
                    'zip': zip,
                }
            }
            
            # Execute code
            exec(code, namespace)
            
            # Get output
            output = captured_output.getvalue()
            
            result["success"] = True
            result["output"] = output if output else "Code executed successfully (no output)"
            
        except SyntaxError as e:
            result["error"] = f"Syntax Error: {str(e)}"
        except Exception as e:
            result["error"] = f"Runtime Error: {str(e)}"
        finally:
            # Restore stdout
            sys.stdout = old_stdout
        
        return result
    
    async def _validate_code(self, code: str) -> Dict[str, Any]:
        """Validate Python code syntax"""
        if not code:
            return {"success": False, "error": "No code provided"}
        
        try:
            compile(code, '<string>', 'exec')
            return {
                "success": True,
                "action": "validate",
                "valid": True,
                "message": "Code syntax is valid"
            }
        except SyntaxError as e:
            return {
                "success": True,
                "action": "validate",
                "valid": False,
                "error": str(e),
                "line": e.lineno,
                "offset": e.offset
            }
    
    async def _analyze_code(self, code: str) -> Dict[str, Any]:
        """Analyze Python code"""
        if not code:
            return {"success": False, "error": "No code provided"}
        
        lines = code.split('\n')
        
        analysis = {
            "success": True,
            "action": "analyze",
            "lines": len(lines),
            "characters": len(code),
            "functions": code.count('def '),
            "classes": code.count('class '),
            "imports": code.count('import '),
            "comments": sum(1 for line in lines if line.strip().startswith('#')),
            "blank_lines": sum(1 for line in lines if not line.strip())
        }
        
        return analysis
    
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
                        "enum": ["run", "validate", "analyze"],
                        "description": "Code operation to perform"
                    },
                    "code": {
                        "type": "string",
                        "description": "Python code to execute/validate/analyze"
                    }
                },
                "required": ["action", "code"]
            }
        }
