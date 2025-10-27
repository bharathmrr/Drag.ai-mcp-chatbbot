"""Analytics MCP Tool - Analyze data and generate insights"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AnalyticsTool:
    """MCP tool for data analytics"""
    
    def __init__(self):
        self.name = "analytics"
        self.description = "Analyze data and generate insights"
        self.enabled = True
        
    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute analytics operation
        
        Args:
            action: Operation type (analyze, visualize, stats, trend)
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with operation result
        """
        try:
            if action == "analyze":
                return await self._analyze_data(kwargs.get("data"), kwargs.get("metrics"))
            elif action == "stats":
                return await self._calculate_stats(kwargs.get("data"))
            elif action == "trend":
                return await self._analyze_trend(kwargs.get("data"), kwargs.get("period"))
            elif action == "summary":
                return await self._generate_summary(kwargs.get("data"))
            else:
                return {"success": False, "error": f"Unknown action: {action}"}
                
        except Exception as e:
            logger.error(f"❌ Analytics error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _analyze_data(self, data: List[Dict], metrics: List[str] = None) -> Dict[str, Any]:
        """Analyze data with specified metrics"""
        if not data:
            return {"success": False, "error": "No data provided"}
        
        df = pd.DataFrame(data)
        
        analysis = {
            "total_records": len(df),
            "columns": list(df.columns),
            "data_types": df.dtypes.astype(str).to_dict()
        }
        
        # Calculate metrics for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            analysis["numeric_summary"] = df[numeric_cols].describe().to_dict()
        
        return {
            "success": True,
            "action": "analyze",
            "analysis": analysis
        }
    
    async def _calculate_stats(self, data: List[float]) -> Dict[str, Any]:
        """Calculate statistical metrics"""
        if not data:
            return {"success": False, "error": "No data provided"}
        
        arr = np.array(data)
        
        stats = {
            "count": len(arr),
            "mean": float(np.mean(arr)),
            "median": float(np.median(arr)),
            "std": float(np.std(arr)),
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
            "sum": float(np.sum(arr))
        }
        
        return {
            "success": True,
            "action": "stats",
            "statistics": stats
        }
    
    async def _analyze_trend(self, data: List[Dict], period: str = "daily") -> Dict[str, Any]:
        """Analyze data trends"""
        if not data:
            return {"success": False, "error": "No data provided"}
        
        df = pd.DataFrame(data)
        
        trend_analysis = {
            "period": period,
            "data_points": len(df),
            "trend": "stable"  # Simplified trend detection
        }
        
        # Check if there's a numeric column to analyze
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            first_col = numeric_cols[0]
            values = df[first_col].values
            
            if len(values) > 1:
                # Simple trend detection
                if values[-1] > values[0]:
                    trend_analysis["trend"] = "increasing"
                elif values[-1] < values[0]:
                    trend_analysis["trend"] = "decreasing"
                
                trend_analysis["change_percent"] = float(
                    ((values[-1] - values[0]) / values[0] * 100) if values[0] != 0 else 0
                )
        
        return {
            "success": True,
            "action": "trend",
            "analysis": trend_analysis
        }
    
    async def _generate_summary(self, data: List[Dict]) -> Dict[str, Any]:
        """Generate data summary"""
        if not data:
            return {"success": False, "error": "No data provided"}
        
        df = pd.DataFrame(data)
        
        summary = {
            "total_records": len(df),
            "columns": list(df.columns),
            "missing_values": df.isnull().sum().to_dict(),
            "unique_counts": {col: df[col].nunique() for col in df.columns}
        }
        
        return {
            "success": True,
            "action": "summary",
            "summary": summary
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
                        "enum": ["analyze", "stats", "trend", "summary"],
                        "description": "Analytics operation to perform"
                    },
                    "data": {
                        "description": "Data to analyze (list of dicts or numbers)"
                    },
                    "metrics": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Metrics to calculate"
                    },
                    "period": {
                        "type": "string",
                        "description": "Time period for trend analysis"
                    }
                },
                "required": ["action", "data"]
            }
        }
