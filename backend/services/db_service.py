"""Database Service - MongoDB connection and operations"""

from config import settings
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class DatabaseService:
    """MongoDB database service (optional)"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self._connected = False
    
    async def connect(self):
        """Connect to MongoDB (optional - will work without it)"""
        try:
            from motor.motor_asyncio import AsyncIOMotorClient
            
            self.client = AsyncIOMotorClient(settings.MONGODB_URL, serverSelectionTimeoutMS=3000)
            self.db = self.client[settings.DATABASE_NAME]
            
            # Test connection
            await self.client.admin.command('ping')
            self._connected = True
            logger.info("✅ MongoDB connected successfully")
            
        except ImportError:
            logger.warning("⚠️  MongoDB driver not installed - running without database")
            self._connected = False
        except Exception as e:
            logger.warning(f"⚠️  MongoDB connection failed: {str(e)} - running without database")
            self._connected = False
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("✅ MongoDB disconnected")
    
    def is_connected(self) -> bool:
        """Check if database is connected"""
        return self._connected
    
    def get_collection(self, collection_name: str):
        """Get a collection"""
        if not self.db:
            logger.warning("Database not connected - operation skipped")
            return None
        return self.db[collection_name]
    
    async def save_chat_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Dict[str, Any] = None
    ) -> bool:
        """Save chat message to database"""
        if not self._connected:
            return False
        
        try:
            message = {
                "session_id": session_id,
                "role": role,
                "content": content,
                "metadata": metadata or {},
                "timestamp": "2025-10-26T20:57:35+05:30"
            }
            
            await self.db.chat_messages.insert_one(message)
            return True
            
        except Exception as e:
            logger.error(f"❌ Error saving message: {str(e)}")
            return False
    
    async def get_chat_history(
        self,
        session_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get chat history for session"""
        if not self._connected:
            return []
        
        try:
            cursor = self.db.chat_messages.find(
                {"session_id": session_id}
            ).sort("timestamp", -1).limit(limit)
            
            messages = []
            async for msg in cursor:
                msg['_id'] = str(msg['_id'])
                messages.append(msg)
            
            return list(reversed(messages))
            
        except Exception as e:
            logger.error(f"❌ Error retrieving history: {str(e)}")
            return []
    
    async def save_tool_log(
        self,
        session_id: str,
        tool_name: str,
        action: str,
        result: Dict[str, Any]
    ) -> bool:
        """Save tool execution log"""
        if not self._connected:
            return False
        
        try:
            log = {
                "session_id": session_id,
                "tool_name": tool_name,
                "action": action,
                "result": result,
                "timestamp": "2025-10-26T20:57:35+05:30"
            }
            
            await self.db.tool_logs.insert_one(log)
            return True
            
        except Exception as e:
            logger.error(f"❌ Error saving tool log: {str(e)}")
            return False
    
    async def get_tool_logs(
        self,
        session_id: str = None,
        tool_name: str = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get tool execution logs"""
        if not self._connected:
            return []
        
        try:
            query = {}
            if session_id:
                query["session_id"] = session_id
            if tool_name:
                query["tool_name"] = tool_name
            
            cursor = self.db.tool_logs.find(query).sort("timestamp", -1).limit(limit)
            
            logs = []
            async for log in cursor:
                log['_id'] = str(log['_id'])
                logs.append(log)
            
            return logs
            
        except Exception as e:
            logger.error(f"❌ Error retrieving logs: {str(e)}")
            return []
    
    async def get_sessions(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent chat sessions"""
        if not self._connected:
            return []
        
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$session_id",
                        "last_message": {"$last": "$timestamp"},
                        "message_count": {"$sum": 1}
                    }
                },
                {"$sort": {"last_message": -1}},
                {"$limit": limit}
            ]
            
            sessions = []
            async for session in self.db.chat_messages.aggregate(pipeline):
                sessions.append({
                    "session_id": session["_id"],
                    "last_message": session["last_message"],
                    "message_count": session["message_count"]
                })
            
            return sessions
            
        except Exception as e:
            logger.error(f"❌ Error retrieving sessions: {str(e)}")
            return []
