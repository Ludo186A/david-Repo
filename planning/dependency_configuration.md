# Dependency Configuration for ICT Backtesting Agent System

## Environment Configuration with pydantic-settings

### settings.py
```python
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
```

### .env.example
```bash
# Database Configuration
DATABASE_URL=postgresql://supabase_admin:postgres@localhost:54334/postgres
DATABASE_POOL_MIN_SIZE=5
DATABASE_POOL_MAX_SIZE=20
DATABASE_COMMAND_TIMEOUT=30

# LLM Provider Configuration
LLM_PROVIDER=ollama

# Ollama Configuration (Primary)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.1

# OpenAI Configuration (Fallback)
# OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o
OPENAI_BASE_URL=https://api.openai.com/v1

# Anthropic Configuration (Fallback)
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# RAG Configuration
RAG_EMBEDDING_PROVIDER=ollama
RAG_EMBEDDING_MODEL=nomic-embed-text
RAG_VECTOR_DIMENSIONS=768

# Application Configuration
LOG_LEVEL=INFO
DEBUG_MODE=false
MAX_QUERY_TIMEOUT=300

# Performance Configuration
ENABLE_QUERY_CACHING=true
CACHE_TTL_SECONDS=3600
MAX_CONCURRENT_QUERIES=10
```

## Model Provider Configuration

### providers.py
```python
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.providers.anthropic import AnthropicProvider
from pydantic_ai.providers.ollama import OllamaProvider
from typing import Union
import logging

from .settings import load_settings

logger = logging.getLogger(__name__)

ModelType = Union[OllamaModel, OpenAIModel, AnthropicModel]

def get_llm_model(model_preference: str = None) -> ModelType:
    """Get configured LLM model with fallback strategy."""
    settings = load_settings()
    
    # Use preference or default from settings
    provider = model_preference or settings.llm_provider
    
    try:
        if provider == "ollama":
            return _get_ollama_model(settings)
        elif provider == "openai":
            return _get_openai_model(settings)
        elif provider == "anthropic":
            return _get_anthropic_model(settings)
        else:
            logger.warning(f"Unknown provider {provider}, falling back to ollama")
            return _get_ollama_model(settings)
    
    except Exception as e:
        logger.error(f"Failed to initialize {provider} model: {e}")
        return _get_fallback_model(settings, exclude=provider)

def _get_ollama_model(settings) -> OllamaModel:
    """Initialize Ollama model with configuration."""
    try:
        provider = OllamaProvider(base_url=settings.ollama_host)
        model = OllamaModel(settings.ollama_model, provider=provider)
        logger.info(f"Initialized Ollama model: {settings.ollama_model}")
        return model
    except Exception as e:
        logger.error(f"Ollama initialization failed: {e}")
        raise

def _get_openai_model(settings) -> OpenAIModel:
    """Initialize OpenAI model with configuration."""
    if not settings.openai_api_key:
        raise ValueError("OpenAI API key not configured")
    
    try:
        provider = OpenAIProvider(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url
        )
        model = OpenAIModel(settings.openai_model, provider=provider)
        logger.info(f"Initialized OpenAI model: {settings.openai_model}")
        return model
    except Exception as e:
        logger.error(f"OpenAI initialization failed: {e}")
        raise

def _get_anthropic_model(settings) -> AnthropicModel:
    """Initialize Anthropic model with configuration."""
    if not settings.anthropic_api_key:
        raise ValueError("Anthropic API key not configured")
    
    try:
        provider = AnthropicProvider(api_key=settings.anthropic_api_key)
        model = AnthropicModel(settings.anthropic_model, provider=provider)
        logger.info(f"Initialized Anthropic model: {settings.anthropic_model}")
        return model
    except Exception as e:
        logger.error(f"Anthropic initialization failed: {e}")
        raise

def _get_fallback_model(settings, exclude: str = None) -> ModelType:
    """Get fallback model when primary provider fails."""
    fallback_order = ["ollama", "openai", "anthropic"]
    
    if exclude:
        fallback_order = [p for p in fallback_order if p != exclude]
    
    for provider in fallback_order:
        try:
            if provider == "ollama":
                return _get_ollama_model(settings)
            elif provider == "openai" and settings.openai_api_key:
                return _get_openai_model(settings)
            elif provider == "anthropic" and settings.anthropic_api_key:
                return _get_anthropic_model(settings)
        except Exception as e:
            logger.warning(f"Fallback provider {provider} failed: {e}")
            continue
    
    raise RuntimeError("All LLM providers failed to initialize")

def get_coordinator_model() -> ModelType:
    """Get model specifically configured for Coordinator Agent."""
    # Coordinator handles complex reasoning, may benefit from more capable model
    settings = load_settings()
    
    if settings.openai_api_key:
        return get_llm_model("openai")  # Prefer OpenAI for strategic reasoning
    else:
        return get_llm_model()  # Use default configuration

def get_backtesting_model() -> ModelType:
    """Get model specifically configured for Backtesting Sub-Agent."""
    # Sub-agent handles structured execution, can use faster local model
    return get_llm_model("ollama")  # Prefer local model for speed
```

## Shared Dependencies Configuration

### dependencies.py
```python
from dataclasses import dataclass
from typing import Dict, Any, Optional
import asyncpg
import json
import logging
from pathlib import Path

from .settings import Settings
from .database import DatabaseManager, FunctionRegistry
from .rag import RAGClient
from .embedding import EmbeddingClient

logger = logging.getLogger(__name__)

@dataclass
class SharedDependencies:
    """Shared dependencies between Coordinator and Backtesting agents."""
    
    # Database components
    db_pool: asyncpg.Pool
    db_manager: DatabaseManager
    function_registry: FunctionRegistry
    
    # RAG components
    rag_client: RAGClient
    embedding_client: EmbeddingClient
    
    # Configuration
    settings: Settings
    
    # Runtime state
    session_id: Optional[str] = None
    debug_mode: bool = False

async def initialize_dependencies(settings: Settings) -> SharedDependencies:
    """Initialize all shared dependencies with proper error handling."""
    
    logger.info("Initializing shared dependencies...")
    
    try:
        # Initialize database components
        db_manager = DatabaseManager(settings.database_url)
        db_pool = await db_manager.initialize_pool()
        logger.info("Database connection pool initialized")
        
        # Load SQL function registry
        function_registry = FunctionRegistry("database/function_signatures.json")
        await function_registry.load_functions()
        logger.info(f"Loaded {len(function_registry.functions)} SQL functions")
        
        # Initialize RAG components
        embedding_client = EmbeddingClient(
            provider=settings.rag_embedding_provider,
            model=settings.rag_embedding_model,
            dimensions=settings.rag_vector_dimensions
        )
        
        rag_client = RAGClient(
            db_pool=db_pool,
            embedding_client=embedding_client
        )
        await rag_client.initialize()
        logger.info("RAG system initialized")
        
        return SharedDependencies(
            db_pool=db_pool,
            db_manager=db_manager,
            function_registry=function_registry,
            rag_client=rag_client,
            embedding_client=embedding_client,
            settings=settings,
            debug_mode=settings.debug_mode
        )
        
    except Exception as e:
        logger.error(f"Failed to initialize dependencies: {e}")
        raise

async def cleanup_dependencies(deps: SharedDependencies):
    """Clean shutdown of all dependencies."""
    logger.info("Cleaning up dependencies...")
    
    try:
        if deps.rag_client:
            await deps.rag_client.close()
        
        if deps.db_manager:
            await deps.db_manager.close_pool()
        
        logger.info("Dependencies cleaned up successfully")
        
    except Exception as e:
        logger.error(f"Error during dependency cleanup: {e}")
```

## Database Integration Layer

### database.py
```python
import asyncpg
import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

from .settings import Settings

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages AsyncPG connection pool and query execution."""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool: Optional[asyncpg.Pool] = None
        self.settings = Settings()
    
    async def initialize_pool(self) -> asyncpg.Pool:
        """Initialize connection pool with optimal settings for financial data."""
        try:
            self.pool = await asyncpg.create_pool(
                self.database_url,
                min_size=self.settings.database_pool_min_size,
                max_size=self.settings.database_pool_max_size,
                command_timeout=self.settings.database_command_timeout,
                server_settings={
                    'application_name': 'ict_backtesting_agents',
                    'jit': 'off',  # Disable JIT for consistent performance
                    'shared_preload_libraries': 'pg_stat_statements',
                    'track_activity_query_size': '2048'
                }
            )
            
            # Test connection
            async with self.pool.acquire() as conn:
                result = await conn.fetchval("SELECT version()")
                logger.info(f"Connected to PostgreSQL: {result}")
            
            return self.pool
            
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            raise
    
    async def close_pool(self):
        """Clean shutdown of connection pool."""
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")
    
    async def execute_function(
        self, 
        function_name: str, 
        parameters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Execute SQL function with proper error handling and logging."""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")
        
        start_time = time.time()
        
        try:
            async with self.pool.acquire() as conn:
                # Prepare parameterized query
                param_json = json.dumps(parameters)
                query = f"SELECT * FROM {function_name}($1::jsonb)"
                
                # Execute with timeout
                result = await asyncio.wait_for(
                    conn.fetch(query, param_json),
                    timeout=self.settings.database_command_timeout
                )
                
                execution_time = int((time.time() - start_time) * 1000)
                
                logger.info(
                    f"Executed {function_name} in {execution_time}ms, "
                    f"returned {len(result)} rows"
                )
                
                return [dict(row) for row in result]
                
        except asyncio.TimeoutError:
            logger.error(f"Query timeout for {function_name} after {self.settings.database_command_timeout}s")
            raise
        except asyncpg.PostgresError as e:
            logger.error(f"PostgreSQL error in {function_name}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in {function_name}: {e}")
            raise
    
    async def validate_connection(self) -> bool:
        """Validate database connection health."""
        try:
            async with self.pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Database connection validation failed: {e}")
            return False

class FunctionRegistry:
    """Registry of available SQL functions from function_signatures.json."""
    
    def __init__(self, signatures_path: str):
        self.signatures_path = Path(signatures_path)
        self.functions: Dict[str, Dict[str, Any]] = {}
        self.categories: Dict[str, List[str]] = {}
    
    async def load_functions(self):
        """Load function signatures from JSON file."""
        try:
            if not self.signatures_path.exists():
                logger.warning(f"Function signatures file not found: {self.signatures_path}")
                return
            
            with open(self.signatures_path, 'r') as f:
                signatures = json.load(f)
            
            for func_data in signatures.get('functions', []):
                name = func_data['name']
                self.functions[name] = func_data
                
                # Group by category
                category = func_data.get('category', 'general')
                if category not in self.categories:
                    self.categories[category] = []
                self.categories[category].append(name)
            
            logger.info(f"Loaded {len(self.functions)} SQL functions from registry")
            
        except Exception as e:
            logger.error(f"Failed to load function signatures: {e}")
            raise
    
    def get_function(self, name: str) -> Optional[Dict[str, Any]]:
        """Get function definition by name."""
        return self.functions.get(name)
    
    def get_functions_by_category(self, category: str) -> List[str]:
        """Get function names by category."""
        return self.categories.get(category, [])
    
    def suggest_functions(
        self, 
        analysis_strategy: str, 
        trading_context: str
    ) -> List[str]:
        """Suggest appropriate functions based on analysis context."""
        
        # Mapping strategy for function selection
        strategy_mapping = {
            "performance_analysis": ["order_blocks", "session_analysis"],
            "correlation_study": ["correlation", "structure_analysis"],
            "structure_detection": ["market_structure", "pattern_detection"]
        }
        
        context_mapping = {
            "scalping": ["intraday", "high_frequency"],
            "swing_trading": ["daily", "weekly"],
            "position_analysis": ["long_term", "trend_analysis"]
        }
        
        suggested = []
        
        # Get functions by strategy
        for category in strategy_mapping.get(analysis_strategy, []):
            suggested.extend(self.get_functions_by_category(category))
        
        # Filter by trading context if needed
        # Additional filtering logic can be added here
        
        return suggested[:10]  # Limit to top 10 suggestions
```

## Requirements and Installation

### requirements.txt
```txt
# Core Pydantic AI
pydantic-ai[openai,anthropic]==0.0.14

# Database
asyncpg==0.29.0
psycopg2-binary==2.9.9

# Configuration
pydantic-settings==2.5.2
python-dotenv==1.0.1

# Data Processing
pandas==2.2.3
numpy==1.26.4

# Async Support
asyncio-mqtt==0.16.2
aiofiles==24.1.0

# Logging and Monitoring
structlog==24.4.0
rich==13.9.2

# Testing
pytest==8.3.3
pytest-asyncio==0.24.0
pytest-mock==3.14.0

# Development
black==24.10.0
ruff==0.7.4
mypy==1.13.0

# Optional: Local embedding support
sentence-transformers==3.2.1
torch==2.5.1
```

### Installation Script
```bash
#!/bin/bash
# install_dependencies.sh

echo "Setting up ICT Backtesting Agent System..."

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Create necessary directories
mkdir -p database
mkdir -p logs
mkdir -p cache

# Copy environment template
cp .env.example .env

echo "Dependencies installed successfully!"
echo "Please configure your .env file with appropriate values."
echo "Make sure your PostgreSQL database is running on the configured URL."
```

## Dependency Injection Pattern

### Agent Initialization
```python
from .dependencies import initialize_dependencies, SharedDependencies
from .providers import get_coordinator_model, get_backtesting_model
from .settings import load_settings

async def create_agents():
    """Initialize both agents with shared dependencies."""
    
    # Load configuration
    settings = load_settings()
    
    # Initialize shared dependencies
    deps = await initialize_dependencies(settings)
    
    # Create agents with appropriate models
    coordinator_agent = Agent(
        model=get_coordinator_model(),
        deps_type=SharedDependencies,
        system_prompt=COORDINATOR_SYSTEM_PROMPT
    )
    
    backtesting_agent = Agent(
        model=get_backtesting_model(),
        deps_type=SharedDependencies,
        system_prompt=BACKTESTING_SYSTEM_PROMPT
    )
    
    return coordinator_agent, backtesting_agent, deps
```

This dependency configuration provides:

1. **Environment-based Configuration**: All settings via environment variables
2. **Multi-Provider LLM Support**: Ollama primary, OpenAI/Anthropic fallback
3. **Robust Database Integration**: AsyncPG with connection pooling
4. **Shared Dependencies**: Single source of truth for both agents
5. **Proper Error Handling**: Graceful degradation and informative errors
6. **Performance Optimization**: Connection pooling, caching, timeouts
7. **Development Support**: Testing utilities and debugging configuration
