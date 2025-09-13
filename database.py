import asyncpg
import json
import logging
import time
import asyncio
from typing import Dict, Any, List, Optional
from pathlib import Path

from settings import Settings

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
                # Create a basic function registry for demo purposes
                self._create_demo_functions()
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
            # Fallback to demo functions
            self._create_demo_functions()
    
    def _create_demo_functions(self):
        """Create demo function registry for testing."""
        demo_functions = [
            {
                "name": "update_order_block_performance",
                "description": "Analyze order block performance with respect rates",
                "parameters": {"symbol": "str", "session": "str", "min_respect_rate": "int"},
                "return_type": "table",
                "category": "order_blocks",
                "performance_tier": "fast",
                "min_sample_size": 20
            },
            {
                "name": "detect_fair_value_gaps",
                "description": "Identify and analyze fair value gaps",
                "parameters": {"symbol": "str", "timeframe": "str", "lookback_days": "int"},
                "return_type": "table",
                "category": "fair_value_gaps",
                "performance_tier": "medium",
                "min_sample_size": 10
            },
            {
                "name": "analyze_session_performance",
                "description": "Calculate session-based performance metrics",
                "parameters": {"symbol": "str", "session": "str", "date_range": "str"},
                "return_type": "table",
                "category": "session_analysis",
                "performance_tier": "fast",
                "min_sample_size": 15
            }
        ]
        
        for func_data in demo_functions:
            name = func_data['name']
            self.functions[name] = func_data
            
            category = func_data.get('category', 'general')
            if category not in self.categories:
                self.categories[category] = []
            self.categories[category].append(name)
        
        logger.info(f"Created {len(self.functions)} demo SQL functions")
    
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
        
        # If no specific matches, return all available functions
        if not suggested:
            suggested = list(self.functions.keys())
        
        return suggested[:10]  # Limit to top 10 suggestions
