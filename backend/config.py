import os
from pydantic_settings import BaseSettings
from typing import Optional, List
from pydantic import field_validator

class Settings(BaseSettings):
    # API Keys
    GEMINI_API_KEY: str = "AIzaSyD-Zay55zScSxixu87JsLZcsCSzLKJRjuo"
    OPENAI_API_KEY: Optional[str] = None
    
    # Model Configuration
    GEMINI_MODEL: str = "gemini-2.0-flash-exp"
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 8192
    
    # Database Configuration
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "ai_mcp_orchestrator"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS Settings
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    # MCP Configuration
    MCP_TIMEOUT: int = 30
    MAX_CONCURRENT_TOOLS: int = 5
    
    # Email Configuration (for Email MCP)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # Google Drive Configuration
    GOOGLE_DRIVE_CREDENTIALS: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = 'utf-8'

# Try to load settings, fallback to defaults if .env doesn't exist
try:
    settings = Settings()
except Exception as e:
    print(f"⚠️  Warning: Could not load .env file, using defaults: {e}")
    settings = Settings(
        _env_file=None  # Don't try to load .env
    )
