from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Database Configuration
    database_url: str = Field(
        default="postgresql://supabase_admin:postgres@localhost:54334/postgres",
        description="PostgreSQL database connection URL"
    )
    database_pool_min_size: int = Field(default=5, description="Minimum connection pool size")
    database_pool_max_size: int = Field(default=20, description="Maximum connection pool size")
    database_command_timeout: int = Field(default=30, description="Database command timeout in seconds")
    
    # LLM Provider Configuration
    llm_provider: str = Field(default="ollama", description="Primary LLM provider")
    
    # Ollama Configuration
    ollama_host: str = Field(default="http://localhost:11434", description="Ollama server URL")
    ollama_model: str = Field(default="llama3.1", description="Ollama model name")
    
    # OpenAI Configuration (fallback)
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    openai_model: str = Field(default="gpt-4o", description="OpenAI model name")
    openai_base_url: str = Field(default="https://api.openai.com/v1", description="OpenAI API base URL")
    
    # Anthropic Configuration (fallback)
    anthropic_api_key: Optional[str] = Field(default=None, description="Anthropic API key")
    anthropic_model: str = Field(default="claude-3-5-sonnet-20241022", description="Anthropic model name")
    
    # RAG Configuration
    rag_embedding_provider: str = Field(default="ollama", description="Embedding provider")
    rag_embedding_model: str = Field(default="nomic-embed-text", description="Embedding model name")
    rag_vector_dimensions: int = Field(default=768, description="Vector embedding dimensions")
    
    # Application Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    debug_mode: bool = Field(default=False, description="Enable debug mode")
    max_query_timeout: int = Field(default=300, description="Maximum query timeout in seconds")
    
    # Performance Configuration
    enable_query_caching: bool = Field(default=True, description="Enable query result caching")
    cache_ttl_seconds: int = Field(default=3600, description="Cache TTL in seconds")
    max_concurrent_queries: int = Field(default=10, description="Maximum concurrent database queries")

def load_settings() -> Settings:
    """Load settings with proper error handling and environment loading."""
    try:
        return Settings()
    except Exception as e:
        error_msg = f"Failed to load settings: {e}"
        if "database_url" in str(e).lower():
            error_msg += "\nMake sure DATABASE_URL is properly configured"
        if any(key in str(e).lower() for key in ["openai_api_key", "anthropic_api_key"]):
            error_msg += "\nAPI keys are optional but required for fallback providers"
        raise ValueError(error_msg) from e
