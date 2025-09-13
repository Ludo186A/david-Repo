from dataclasses import dataclass
from typing import Dict, Any, Optional
import asyncpg
import json
import logging
from pathlib import Path

from settings import Settings
from database import DatabaseManager, FunctionRegistry

logger = logging.getLogger(__name__)

@dataclass
class SharedDependencies:
    """Shared dependencies between Coordinator and Backtesting agents."""
    
    # Database components
    db_pool: asyncpg.Pool
    db_manager: DatabaseManager
    function_registry: FunctionRegistry
    
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
        
        return SharedDependencies(
            db_pool=db_pool,
            db_manager=db_manager,
            function_registry=function_registry,
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
        if deps.db_manager:
            await deps.db_manager.close_pool()
        
        logger.info("Dependencies cleaned up successfully")
        
    except Exception as e:
        logger.error(f"Error during dependency cleanup: {e}")
