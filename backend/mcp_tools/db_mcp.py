"""Database MCP Tool - Query and manage database"""

from typing import Dict, Any, List
from config import settings
import logging

logger = logging.getLogger(__name__)

# Try to import motor, but make it optional
try:
    from motor.motor_asyncio import AsyncIOMotorClient
    MOTOR_AVAILABLE = True
except ImportError:
    MOTOR_AVAILABLE = False
    logger.warning("⚠️  Motor not installed - Database tool will be disabled")

class DatabaseTool:
    """MCP tool for database operations"""
    
    def __init__(self):
        self.name = "database"
        self.description = "Query and manage MongoDB database (requires motor package)"
        self.enabled = MOTOR_AVAILABLE
        self.client = None
        self.db = None
        
    async def initialize(self):
        """Initialize database connection"""
        if not MOTOR_AVAILABLE:
            logger.warning("⚠️  Motor not available - Database tool disabled")
            return
            
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URL, serverSelectionTimeoutMS=3000)
            self.db = self.client[settings.DATABASE_NAME]
            await self.client.admin.command('ping')
            logger.info("✅ Database tool initialized")
        except Exception as e:
            logger.warning(f"⚠️  Database initialization error: {str(e)} - tool disabled")
            self.enabled = False
    
    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute database operation
        
        Args:
            action: Operation type (find, insert, update, delete, count)
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with operation result
        """
        if not MOTOR_AVAILABLE or not self.enabled:
            return {
                "success": False,
                "error": "Database tool not available (motor package not installed)"
            }
            
        try:
            if not self.db:
                await self.initialize()
            
            if not self.db:
                return {"success": False, "error": "Database not connected"}
            
            collection_name = kwargs.get("collection", "default")
            collection = self.db[collection_name]
            
            if action == "find":
                return await self._find(collection, kwargs.get("query", {}), kwargs.get("limit", 10))
            elif action == "insert":
                return await self._insert(collection, kwargs.get("document"))
            elif action == "update":
                return await self._update(collection, kwargs.get("query"), kwargs.get("update"))
            elif action == "delete":
                return await self._delete(collection, kwargs.get("query"))
            elif action == "count":
                return await self._count(collection, kwargs.get("query", {}))
            else:
                return {"success": False, "error": f"Unknown action: {action}"}
                
        except Exception as e:
            logger.error(f"❌ Database operation error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _find(self, collection, query: Dict, limit: int) -> Dict[str, Any]:
        """Find documents"""
        cursor = collection.find(query).limit(limit)
        documents = []
        
        async for doc in cursor:
            doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
            documents.append(doc)
        
        return {
            "success": True,
            "action": "find",
            "documents": documents,
            "count": len(documents)
        }
    
    async def _insert(self, collection, document: Dict) -> Dict[str, Any]:
        """Insert document"""
        result = await collection.insert_one(document)
        
        return {
            "success": True,
            "action": "insert",
            "inserted_id": str(result.inserted_id)
        }
    
    async def _update(self, collection, query: Dict, update: Dict) -> Dict[str, Any]:
        """Update documents"""
        result = await collection.update_many(query, {"$set": update})
        
        return {
            "success": True,
            "action": "update",
            "matched_count": result.matched_count,
            "modified_count": result.modified_count
        }
    
    async def _delete(self, collection, query: Dict) -> Dict[str, Any]:
        """Delete documents"""
        result = await collection.delete_many(query)
        
        return {
            "success": True,
            "action": "delete",
            "deleted_count": result.deleted_count
        }
    
    async def _count(self, collection, query: Dict) -> Dict[str, Any]:
        """Count documents"""
        count = await collection.count_documents(query)
        
        return {
            "success": True,
            "action": "count",
            "count": count
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
                        "enum": ["find", "insert", "update", "delete", "count"],
                        "description": "Database operation to perform"
                    },
                    "collection": {
                        "type": "string",
                        "description": "Collection name"
                    },
                    "query": {
                        "type": "object",
                        "description": "Query filter"
                    },
                    "document": {
                        "type": "object",
                        "description": "Document to insert"
                    },
                    "update": {
                        "type": "object",
                        "description": "Update data"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Result limit (default: 10)"
                    }
                },
                "required": ["action"]
            }
        }
