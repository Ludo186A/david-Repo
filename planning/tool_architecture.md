# Tool Architecture for ICT Backtesting Agent System

## Tool Integration Strategy

### Coordinator Agent Tools

#### 1. RAG Consultation Tool
```python
@coordinator_agent.tool
async def consult_rag_memory(
    ctx: RunContext[SharedDependencies],
    query: str,
    context_type: Literal["methodology", "historical", "documentation"]
) -> Dict[str, Any]:
    """
    Consult RAG system for historical context and ICT methodology information.
    
    Args:
        query: Natural language query for RAG search
        context_type: Type of context needed for analysis
    
    Returns:
        Dictionary with relevant context and source citations
    """
```

#### 2. Query Classification Tool
```python
@coordinator_agent.tool
async def classify_user_query(
    ctx: RunContext[SharedDependencies],
    user_query: str
) -> QueryClassification:
    """
    Classify user query to determine routing strategy.
    
    Args:
        user_query: Raw user input requiring analysis
    
    Returns:
        QueryClassification with routing decision and confidence
    """
```

#### 3. Backtesting Delegation Tool
```python
@coordinator_agent.tool
async def execute_backtesting_analysis(
    ctx: RunContext[SharedDependencies],
    analysis_request: CoordinatorRequest
) -> BacktestingResponse:
    """
    Delegate technical analysis to Backtesting Sub-Agent.
    
    Args:
        analysis_request: Structured request with strategic parameters
    
    Returns:
        BacktestingResponse with results and metadata
    """
```

### Backtesting Sub-Agent Tools

#### 1. Database Query Execution Tool
```python
@backtesting_agent.tool
async def execute_sql_function(
    ctx: RunContext[SharedDependencies],
    function_name: str,
    parameters: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Execute specialized SQL function against ICT database.
    
    Args:
        function_name: Name of SQL function from function_signatures.json
        parameters: Function parameters with validation
    
    Returns:
        Raw query results with execution metadata
    """
```

#### 2. Function Selection Tool
```python
@backtesting_agent.tool
async def select_optimal_function(
    ctx: RunContext[SharedDependencies],
    analysis_strategy: str,
    trading_context: str,
    quality_requirements: str
) -> FunctionSelection:
    """
    Select optimal SQL function based on strategic context.
    
    Args:
        analysis_strategy: Type of analysis required
        trading_context: Trading timeframe and approach
        quality_requirements: Statistical confidence requirements
    
    Returns:
        FunctionSelection with recommended function and parameters
    """
```

#### 3. Statistical Validation Tool
```python
@backtesting_agent.tool
async def validate_results(
    ctx: RunContext[SharedDependencies],
    raw_results: List[Dict[str, Any]],
    quality_requirements: str
) -> ValidationResults:
    """
    Validate query results for statistical significance.
    
    Args:
        raw_results: Raw database query results
        quality_requirements: Required confidence thresholds
    
    Returns:
        ValidationResults with confidence metrics and warnings
    """
```

## Pydantic Models for Tool Integration

### Communication Models

```python
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional, Literal
from datetime import datetime

class QueryClassification(BaseModel):
    """Result of query classification analysis"""
    routing_decision: Literal["rag_first", "backtesting_first", "hybrid"]
    confidence: float = Field(..., ge=0, le=100)
    reasoning: str
    suggested_approach: str

class CoordinatorRequest(BaseModel):
    """Structured request from Coordinator to Backtesting Sub-Agent"""
    analysis_strategy: Literal["performance_analysis", "correlation_study", "structure_detection"]
    trading_context: Literal["scalping", "swing_trading", "position_analysis"]
    temporal_scope: Literal["recent_performance", "historical_pattern", "specific_period"]
    asset_focus: Literal["major_pairs", "cross_pairs", "specific_symbol"]
    session_relevance: Literal["high_liquidity", "all_sessions", "specific_session"]
    quality_requirements: Literal["high_confidence", "balanced", "broad_coverage"]
    
    # Optional specific parameters
    symbol: Optional[str] = None
    timeframe: Optional[str] = None
    date_range: Optional[tuple[datetime, datetime]] = None
    session: Optional[str] = None

class BacktestingMetadata(BaseModel):
    """Statistical metadata for backtesting results"""
    sample_size: int
    data_coverage: float = Field(..., ge=0, le=100)
    confidence_level: float = Field(..., ge=0, le=100)
    execution_time_ms: int
    sql_function_used: str
    data_quality_score: float = Field(..., ge=0, le=100)

class BacktestingResponse(BaseModel):
    """Structured response from Backtesting Sub-Agent"""
    execution_status: Literal["success", "partial", "failed"]
    analysis_results: Dict[str, Any]
    metadata: BacktestingMetadata
    recommendations: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    error_details: Optional[str] = None

class FunctionSelection(BaseModel):
    """Result of SQL function selection process"""
    recommended_function: str
    parameters: Dict[str, Any]
    confidence: float = Field(..., ge=0, le=100)
    alternative_functions: List[str] = Field(default_factory=list)
    reasoning: str

class ValidationResults(BaseModel):
    """Statistical validation results"""
    is_valid: bool
    confidence_level: float = Field(..., ge=0, le=100)
    sample_size: int
    data_coverage: float = Field(..., ge=0, le=100)
    warnings: List[str] = Field(default_factory=list)
    quality_score: float = Field(..., ge=0, le=100)
```

### Database Integration Models

```python
class DatabaseConnection(BaseModel):
    """Database connection configuration"""
    host: str
    port: int
    database: str
    username: str
    password: str
    pool_size: int = 10
    max_overflow: int = 20

class SQLFunction(BaseModel):
    """SQL function definition from function_signatures.json"""
    name: str
    description: str
    parameters: Dict[str, str]  # parameter_name: type
    return_type: str
    category: str
    performance_tier: Literal["fast", "medium", "slow"]
    min_sample_size: int

class QueryExecution(BaseModel):
    """Query execution context and results"""
    function_name: str
    parameters: Dict[str, Any]
    execution_time_ms: int
    row_count: int
    success: bool
    error_message: Optional[str] = None
```

## Tool Implementation Patterns

### 1. RunContext Usage Pattern

```python
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass

@dataclass
class SharedDependencies:
    """Shared dependencies between both agents"""
    db_pool: asyncpg.Pool
    rag_client: RAGClient
    function_registry: Dict[str, SQLFunction]
    embedding_client: EmbeddingClient

@coordinator_agent.tool
async def example_tool(
    ctx: RunContext[SharedDependencies],
    parameter: str
) -> Dict[str, Any]:
    # Access shared database pool
    async with ctx.deps.db_pool.acquire() as conn:
        result = await conn.fetch("SELECT * FROM table WHERE col = $1", parameter)
    
    # Track usage for token accounting
    # Usage automatically tracked via ctx.usage
    
    return {"result": result}
```

### 2. Error Handling Pattern

```python
@backtesting_agent.tool
async def execute_sql_function(
    ctx: RunContext[SharedDependencies],
    function_name: str,
    parameters: Dict[str, Any]
) -> Dict[str, Any]:
    try:
        # Validate function exists
        if function_name not in ctx.deps.function_registry:
            return {
                "success": False,
                "error": f"Function {function_name} not found",
                "alternatives": list(ctx.deps.function_registry.keys())[:5]
            }
        
        # Execute with connection pool
        async with ctx.deps.db_pool.acquire() as conn:
            result = await conn.fetch(f"SELECT * FROM {function_name}($1)", parameters)
            
        return {
            "success": True,
            "data": [dict(row) for row in result],
            "row_count": len(result)
        }
        
    except asyncpg.PostgresError as e:
        return {
            "success": False,
            "error": f"Database error: {str(e)}",
            "suggestion": "Check parameter types and data availability"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "suggestion": "Contact system administrator"
        }
```

### 3. Agent Delegation Pattern

```python
@coordinator_agent.tool
async def execute_backtesting_analysis(
    ctx: RunContext[SharedDependencies],
    analysis_request: CoordinatorRequest
) -> BacktestingResponse:
    """Delegate to Backtesting Sub-Agent with proper usage tracking"""
    
    # Convert request to JSON for sub-agent
    request_json = analysis_request.model_dump_json()
    
    # Call sub-agent with usage tracking
    result = await backtesting_agent.run(
        request_json,
        deps=ctx.deps,  # Share dependencies
        usage=ctx.usage  # Track token usage
    )
    
    # Parse and validate response
    try:
        response_data = json.loads(result.data)
        return BacktestingResponse(**response_data)
    except (json.JSONDecodeError, ValidationError) as e:
        return BacktestingResponse(
            execution_status="failed",
            analysis_results={},
            metadata=BacktestingMetadata(
                sample_size=0,
                data_coverage=0.0,
                confidence_level=0.0,
                execution_time_ms=0,
                sql_function_used="none",
                data_quality_score=0.0
            ),
            error_details=f"Response parsing error: {str(e)}"
        )
```

## Database Integration Architecture

### Connection Pool Management

```python
import asyncpg
from typing import Optional

class DatabaseManager:
    """Manages AsyncPG connection pool for both agents"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool: Optional[asyncpg.Pool] = None
    
    async def initialize_pool(self) -> asyncpg.Pool:
        """Initialize connection pool with optimal settings"""
        self.pool = await asyncpg.create_pool(
            self.database_url,
            min_size=5,
            max_size=20,
            command_timeout=30,
            server_settings={
                'application_name': 'ict_backtesting_agents',
                'jit': 'off'  # Disable JIT for consistent performance
            }
        )
        return self.pool
    
    async def close_pool(self):
        """Clean shutdown of connection pool"""
        if self.pool:
            await self.pool.close()
    
    async def execute_function(
        self, 
        function_name: str, 
        parameters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Execute SQL function with proper error handling"""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")
        
        async with self.pool.acquire() as conn:
            # Use prepared statement for performance
            query = f"SELECT * FROM {function_name}($1)"
            result = await conn.fetch(query, json.dumps(parameters))
            return [dict(row) for row in result]
```

### Function Registry Integration

```python
class FunctionRegistry:
    """Registry of available SQL functions from function_signatures.json"""
    
    def __init__(self, signatures_path: str):
        self.signatures_path = signatures_path
        self.functions: Dict[str, SQLFunction] = {}
    
    async def load_functions(self):
        """Load function signatures from JSON file"""
        with open(self.signatures_path, 'r') as f:
            signatures = json.load(f)
        
        for func_data in signatures['functions']:
            self.functions[func_data['name']] = SQLFunction(**func_data)
    
    def get_function(self, name: str) -> Optional[SQLFunction]:
        """Get function definition by name"""
        return self.functions.get(name)
    
    def find_functions_by_category(self, category: str) -> List[SQLFunction]:
        """Find functions by analysis category"""
        return [
            func for func in self.functions.values() 
            if func.category == category
        ]
    
    def suggest_functions(
        self, 
        analysis_strategy: str, 
        trading_context: str
    ) -> List[str]:
        """Suggest appropriate functions based on context"""
        # Implementation logic for function selection
        # Based on analysis_strategy and trading_context mapping
        pass
```

## Performance Optimization Patterns

### 1. Connection Pool Optimization
- Minimum 5 connections, maximum 20 for concurrent agent operations
- Command timeout of 30 seconds for complex queries
- Prepared statements for repeated query patterns

### 2. Query Optimization
- Use parameterized queries exclusively for security
- Implement query result caching for repeated analysis
- Batch operations where possible to reduce round trips

### 3. Error Recovery
- Automatic retry for transient connection errors
- Graceful degradation with alternative function suggestions
- Circuit breaker pattern for database health monitoring

## Tool Testing Strategy

### 1. Unit Testing with TestModel
```python
from pydantic_ai.models.test import TestModel

async def test_coordinator_tools():
    test_model = TestModel()
    
    with coordinator_agent.override(model=test_model):
        result = await coordinator_agent.run(
            "Test query classification",
            deps=mock_dependencies
        )
        assert result.data is not None
```

### 2. Integration Testing
- Test database connectivity with real connection pool
- Validate agent delegation with actual sub-agent calls
- Performance testing for sub-second query requirements

### 3. Error Scenario Testing
- Database connection failures
- Invalid function parameters
- Insufficient data coverage scenarios
