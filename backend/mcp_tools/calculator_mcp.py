"""Calculator MCP Tool - Perform mathematical calculations"""

from typing import Dict, Any
import math
import logging

logger = logging.getLogger(__name__)

class CalculatorTool:
    """MCP tool for mathematical calculations"""
    
    def __init__(self):
        self.name = "calculator"
        self.description = "Perform mathematical calculations and conversions"
        self.enabled = True
        
    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute calculator operation
        
        Args:
            action: Operation type (calculate, convert, solve)
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with operation result
        """
        try:
            if action == "calculate":
                return await self._calculate(kwargs.get("expression"))
            elif action == "convert":
                return await self._convert(
                    kwargs.get("value"),
                    kwargs.get("from_unit"),
                    kwargs.get("to_unit")
                )
            elif action == "solve":
                return await self._solve(kwargs.get("equation"))
            else:
                return {"success": False, "error": f"Unknown action: {action}"}
                
        except Exception as e:
            logger.error(f"❌ Calculator error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _calculate(self, expression: str) -> Dict[str, Any]:
        """Calculate mathematical expression"""
        if not expression:
            return {"success": False, "error": "No expression provided"}
        
        try:
            # Safe namespace with math functions
            namespace = {
                '__builtins__': {},
                'abs': abs,
                'round': round,
                'min': min,
                'max': max,
                'sum': sum,
                'pow': pow,
                'sqrt': math.sqrt,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'log': math.log,
                'log10': math.log10,
                'exp': math.exp,
                'pi': math.pi,
                'e': math.e,
            }
            
            result = eval(expression, namespace)
            
            return {
                "success": True,
                "action": "calculate",
                "expression": expression,
                "result": result
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Calculation error: {str(e)}"
            }
    
    async def _convert(self, value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
        """Convert between units"""
        if value is None or not from_unit or not to_unit:
            return {"success": False, "error": "Missing parameters"}
        
        # Conversion factors (to base unit)
        conversions = {
            # Length (meters)
            "m": 1, "km": 1000, "cm": 0.01, "mm": 0.001,
            "ft": 0.3048, "in": 0.0254, "mi": 1609.34,
            
            # Weight (grams)
            "g": 1, "kg": 1000, "mg": 0.001,
            "lb": 453.592, "oz": 28.3495,
            
            # Temperature (special case)
            "c": None, "f": None, "k": None,
        }
        
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()
        
        # Temperature conversions
        if from_unit in ["c", "f", "k"] or to_unit in ["c", "f", "k"]:
            return self._convert_temperature(value, from_unit, to_unit)
        
        if from_unit not in conversions or to_unit not in conversions:
            return {"success": False, "error": "Unknown unit"}
        
        # Convert to base unit, then to target unit
        base_value = value * conversions[from_unit]
        result = base_value / conversions[to_unit]
        
        return {
            "success": True,
            "action": "convert",
            "value": value,
            "from_unit": from_unit,
            "to_unit": to_unit,
            "result": round(result, 4)
        }
    
    def _convert_temperature(self, value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
        """Convert temperature units"""
        # Convert to Celsius first
        if from_unit == "c":
            celsius = value
        elif from_unit == "f":
            celsius = (value - 32) * 5/9
        elif from_unit == "k":
            celsius = value - 273.15
        else:
            return {"success": False, "error": "Unknown temperature unit"}
        
        # Convert from Celsius to target
        if to_unit == "c":
            result = celsius
        elif to_unit == "f":
            result = celsius * 9/5 + 32
        elif to_unit == "k":
            result = celsius + 273.15
        else:
            return {"success": False, "error": "Unknown temperature unit"}
        
        return {
            "success": True,
            "action": "convert",
            "value": value,
            "from_unit": from_unit.upper(),
            "to_unit": to_unit.upper(),
            "result": round(result, 2)
        }
    
    async def _solve(self, equation: str) -> Dict[str, Any]:
        """Solve simple equations"""
        return {
            "success": True,
            "action": "solve",
            "equation": equation,
            "note": "Equation solving requires symbolic math library (sympy)",
            "suggestion": "Use calculate action for numerical expressions"
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
                        "enum": ["calculate", "convert", "solve"],
                        "description": "Calculator operation to perform"
                    },
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to calculate"
                    },
                    "value": {
                        "type": "number",
                        "description": "Value to convert"
                    },
                    "from_unit": {
                        "type": "string",
                        "description": "Source unit (m, km, kg, lb, c, f, etc.)"
                    },
                    "to_unit": {
                        "type": "string",
                        "description": "Target unit"
                    },
                    "equation": {
                        "type": "string",
                        "description": "Equation to solve"
                    }
                },
                "required": ["action"]
            }
        }
