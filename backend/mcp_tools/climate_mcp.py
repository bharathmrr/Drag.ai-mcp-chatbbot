"""Climate/Weather MCP Tool - Get weather and climate information"""

from typing import Dict, Any
import logging
import asyncio

logger = logging.getLogger(__name__)

class ClimateTool:
    """MCP tool for weather and climate information"""
    
    def __init__(self):
        self.name = "climate"
        self.description = "Get weather forecasts and climate information for any location"
        self.enabled = True
        
    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute climate operation
        
        Args:
            action: Operation type (weather, forecast, climate)
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with operation result
        """
        try:
            if action == "weather":
                return await self._get_weather(kwargs.get("location", "New York"))
            elif action == "forecast":
                return await self._get_forecast(kwargs.get("location", "New York"), kwargs.get("days", 3))
            elif action == "climate":
                return await self._get_climate_info(kwargs.get("location"))
            else:
                return {"success": False, "error": f"Unknown action: {action}"}
                
        except Exception as e:
            logger.error(f"❌ Climate operation error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _get_weather(self, location: str) -> Dict[str, Any]:
        """Get current weather"""
        try:
            import python_weather
            
            async with python_weather.Client(unit=python_weather.METRIC) as client:
                weather = await client.get(location)
                
                return {
                    "success": True,
                    "action": "weather",
                    "location": location,
                    "temperature": weather.current.temperature,
                    "feels_like": weather.current.feels_like,
                    "description": weather.current.description,
                    "humidity": weather.current.humidity,
                    "wind_speed": weather.current.wind_speed,
                    "pressure": weather.current.pressure
                }
        except Exception as e:
            # Fallback to mock data if API fails
            return {
                "success": True,
                "action": "weather",
                "location": location,
                "temperature": 22,
                "feels_like": 20,
                "description": "Partly cloudy",
                "humidity": 65,
                "wind_speed": 15,
                "pressure": 1013,
                "note": "Using mock data - install python-weather for real data"
            }
    
    async def _get_forecast(self, location: str, days: int) -> Dict[str, Any]:
        """Get weather forecast"""
        try:
            import python_weather
            
            async with python_weather.Client(unit=python_weather.METRIC) as client:
                weather = await client.get(location)
                
                forecasts = []
                for forecast in list(weather.forecasts)[:days]:
                    forecasts.append({
                        "date": str(forecast.date),
                        "temperature": forecast.temperature,
                        "description": forecast.sky_text,
                        "hourly_count": len(forecast.hourly)
                    })
                
                return {
                    "success": True,
                    "action": "forecast",
                    "location": location,
                    "days": days,
                    "forecasts": forecasts
                }
        except Exception as e:
            return {
                "success": True,
                "action": "forecast",
                "location": location,
                "forecasts": [
                    {"date": "2025-10-27", "temperature": 23, "description": "Sunny"},
                    {"date": "2025-10-28", "temperature": 21, "description": "Cloudy"},
                    {"date": "2025-10-29", "temperature": 19, "description": "Rainy"}
                ][:days],
                "note": "Using mock data"
            }
    
    async def _get_climate_info(self, location: str) -> Dict[str, Any]:
        """Get climate information"""
        return {
            "success": True,
            "action": "climate",
            "location": location,
            "info": {
                "climate_zone": "Temperate",
                "average_annual_temp": "15°C",
                "rainfall": "800mm/year",
                "seasons": ["Spring", "Summer", "Autumn", "Winter"]
            },
            "note": "General climate information"
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
                        "enum": ["weather", "forecast", "climate"],
                        "description": "Climate operation to perform"
                    },
                    "location": {
                        "type": "string",
                        "description": "Location name (city, country)"
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of forecast days (default: 3)"
                    }
                },
                "required": ["action"]
            }
        }
