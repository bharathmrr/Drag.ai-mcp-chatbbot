"""System Monitor MCP Tool - Monitor system resources and performance"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class SystemMonitorTool:
    """MCP tool for system monitoring and resource tracking"""
    
    def __init__(self):
        self.name = "system_monitor"
        self.description = "Monitor CPU, memory, disk, network, and system performance"
        self.enabled = True
        
    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute system monitor operation
        
        Args:
            action: Operation type (cpu, memory, disk, network, overview)
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with operation result
        """
        try:
            if action == "cpu":
                return await self._get_cpu_info()
            elif action == "memory":
                return await self._get_memory_info()
            elif action == "disk":
                return await self._get_disk_info()
            elif action == "network":
                return await self._get_network_info()
            elif action == "overview":
                return await self._get_system_overview()
            elif action == "processes":
                return await self._get_top_processes(kwargs.get("limit", 5))
            else:
                return {"success": False, "error": f"Unknown action: {action}"}
                
        except Exception as e:
            logger.error(f"❌ System monitor error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _get_cpu_info(self) -> Dict[str, Any]:
        """Get CPU information"""
        try:
            import psutil
            import cpuinfo
            
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            cpu_freq = psutil.cpu_freq()
            cpu_info_data = cpuinfo.get_cpu_info()
            
            return {
                "success": True,
                "action": "cpu",
                "usage_percent": psutil.cpu_percent(interval=1),
                "usage_per_core": cpu_percent,
                "core_count": psutil.cpu_count(logical=False),
                "thread_count": psutil.cpu_count(logical=True),
                "frequency": {
                    "current": cpu_freq.current if cpu_freq else 0,
                    "min": cpu_freq.min if cpu_freq else 0,
                    "max": cpu_freq.max if cpu_freq else 0
                },
                "brand": cpu_info_data.get('brand_raw', 'Unknown'),
                "arch": cpu_info_data.get('arch', 'Unknown')
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _get_memory_info(self) -> Dict[str, Any]:
        """Get memory information"""
        try:
            import psutil
            
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return {
                "success": True,
                "action": "memory",
                "total_gb": round(memory.total / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "used_gb": round(memory.used / (1024**3), 2),
                "percent": memory.percent,
                "swap": {
                    "total_gb": round(swap.total / (1024**3), 2),
                    "used_gb": round(swap.used / (1024**3), 2),
                    "percent": swap.percent
                }
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _get_disk_info(self) -> Dict[str, Any]:
        """Get disk information"""
        try:
            import psutil
            
            partitions = psutil.disk_partitions()
            disk_info = []
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_info.append({
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "total_gb": round(usage.total / (1024**3), 2),
                        "used_gb": round(usage.used / (1024**3), 2),
                        "free_gb": round(usage.free / (1024**3), 2),
                        "percent": usage.percent
                    })
                except PermissionError:
                    continue
            
            return {
                "success": True,
                "action": "disk",
                "partitions": disk_info,
                "count": len(disk_info)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _get_network_info(self) -> Dict[str, Any]:
        """Get network information"""
        try:
            import psutil
            
            net_io = psutil.net_io_counters()
            
            return {
                "success": True,
                "action": "network",
                "bytes_sent_mb": round(net_io.bytes_sent / (1024**2), 2),
                "bytes_recv_mb": round(net_io.bytes_recv / (1024**2), 2),
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv,
                "errors_in": net_io.errin,
                "errors_out": net_io.errout,
                "drop_in": net_io.dropin,
                "drop_out": net_io.dropout
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _get_system_overview(self) -> Dict[str, Any]:
        """Get complete system overview"""
        try:
            import psutil
            import platform
            
            boot_time = psutil.boot_time()
            from datetime import datetime
            uptime = datetime.now().timestamp() - boot_time
            
            return {
                "success": True,
                "action": "overview",
                "platform": {
                    "system": platform.system(),
                    "release": platform.release(),
                    "version": platform.version(),
                    "machine": platform.machine(),
                    "processor": platform.processor()
                },
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent,
                "uptime_hours": round(uptime / 3600, 2),
                "process_count": len(psutil.pids())
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _get_top_processes(self, limit: int) -> Dict[str, Any]:
        """Get top processes by CPU/memory usage"""
        try:
            import psutil
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            top_processes = processes[:limit]
            
            return {
                "success": True,
                "action": "processes",
                "count": limit,
                "processes": top_processes
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
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
                        "enum": ["cpu", "memory", "disk", "network", "overview", "processes"],
                        "description": "System monitoring operation to perform"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of processes to return (for processes action)"
                    }
                },
                "required": ["action"]
            }
        }
