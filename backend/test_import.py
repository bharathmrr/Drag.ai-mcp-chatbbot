"""Test imports to find errors"""

print("Testing imports...")

try:
    print("1. Importing config...")
    from config import settings
    print("   ✅ Config imported")
except Exception as e:
    print(f"   ❌ Config error: {e}")

try:
    print("2. Importing database service...")
    from services.db_service import DatabaseService
    print("   ✅ Database service imported")
except Exception as e:
    print(f"   ❌ Database service error: {e}")

try:
    print("3. Importing tool registry...")
    from utils.tool_registry import ToolRegistry
    print("   ✅ Tool registry imported")
except Exception as e:
    print(f"   ❌ Tool registry error: {e}")

try:
    print("4. Importing routes...")
    from routes import chat_routes, mcp_routes
    print("   ✅ Routes imported")
except Exception as e:
    print(f"   ❌ Routes error: {e}")

print("\n✅ All imports successful!")
