---
name: "ICT Backtesting Agent System PRP"
description: "Comprehensive PRP for building a two-agent Pydantic AI system for intelligent backtesting analysis"
---

## Purpose

Build a sophisticated two-agent system using Pydantic AI for intelligent backtesting analysis of financial markets. The system consists of a **Coordinator Agent** that interprets user queries and formulates strategic analysis plans, and a **Backtesting Sub-Agent** that executes technical database queries against a production PostgreSQL database containing 7.08 million OHLCV records with 60+ specialized SQL functions for market structure analysis.

## Core Principles

1. **Pydantic AI Multi-Agent Architecture**: Implement agent delegation patterns for coordinated workflow execution
2. **Type Safety First**: Leverage Pydantic AI's type-safe design and structured outputs for financial data validation
3. **Production Database Integration**: Utilize AsyncPG for high-performance PostgreSQL connectivity with 7M+ records
4. **ICT Analysis Specialization**: Focus on Inner Circle Trader methodologies with specialized SQL functions
5. **Comprehensive Testing**: Use TestModel and FunctionModel for thorough multi-agent validation

## ⚠️ Implementation Guidelines: Strategic Simplicity

**IMPORTANT**: This is a complex multi-agent system - maintain focus and avoid over-engineering.

- ✅ **Agent Separation of Concerns** - Coordinator handles strategy, Sub-Agent handles execution
- ✅ **Follow Pydantic AI Delegation Patterns** - Use proper agent delegation with RunContext and usage tracking
- ✅ **Database Connection Pooling** - Single AsyncPG connection pool shared between agents
- ✅ **Structured Communication Protocol** - JSON-based inter-agent communication with validation
- ✅ **Start with Core Functions** - Implement essential backtesting capabilities first

### Key Question:
**"Does this feature directly support ICT backtesting analysis or agent coordination?"**

If the answer is no, defer it. Focus on core backtesting functionality and clean agent communication.

---

## Goal

Create a production-ready two-agent system that enables sophisticated ICT backtesting analysis through natural language queries. The Coordinator Agent interprets user intent and formulates strategic analysis plans, while the Backtesting Sub-Agent executes technical database operations using 60+ specialized SQL functions against 7.08 million OHLCV records. The system should provide accurate, statistically validated results with proper error handling and performance optimization.

## Why

### Business Justification
- **Trading Strategy Validation**: Enable systematic backtesting of ICT methodologies with statistical rigor
- **Natural Language Interface**: Allow traders to query complex market data without SQL knowledge
- **Performance Analysis**: Provide sub-second query execution for real-time strategy evaluation
- **Risk Management**: Deliver statistically validated results with confidence levels and sample sizes

### Technical Necessity
- **Data Scale Challenge**: 7.08M records require specialized query optimization and connection pooling
- **Complex Analysis Requirements**: ICT methodologies need 60+ specialized SQL functions for market structure analysis
- **Multi-Step Workflows**: Strategic analysis requires coordination between interpretation and execution phases
- **Production Reliability**: Financial analysis demands robust error handling and data validation

## What

### Agent Type Classification
- [x] **Multi-Agent Workflow System**: Coordinator + Sub-Agent with delegation patterns
- [x] **Tool-Enabled Agents**: Database connectivity, RAG integration, and specialized analysis tools
- [x] **Structured Output Agents**: Financial data validation and statistical result formatting

### External Integrations
- [x] **PostgreSQL Database**: AsyncPG connection to Supabase local instance with ICT schema
- [x] **RAG System**: Supabase vector database for historical context and documentation
- [x] **Embedding Services**: OpenAI-compatible API for vector embeddings
- [x] **Multiple LLM Providers**: Ollama (local), OpenAI, Anthropic with fallback strategies

### Success Criteria
- [x] **Query Classification Accuracy**: >90% correct routing between RAG-first vs backtesting-first queries
- [x] **Sub-Agent Function Selection**: >95% accuracy in SQL function selection from strategic context
- [x] **Performance Requirements**: <10 second end-to-end query resolution, sub-second for standard analysis
- [x] **Statistical Validation**: 100% of analysis results include confidence levels and sample sizes
- [x] **Data Quality Assurance**: ≥70% coverage threshold for actionable insights
- [x] **System Reliability**: >99.5% database connection stability with graceful error handling

## All Needed Context

### Pydantic AI Multi-Agent Research

IMPORTANT: Make sure you continue to usse the Archon MCP server for Pydantic AI and graphiti documentation to aid in your develoment.

```yaml
# ESSENTIAL PYDANTIC AI DOCUMENTATION - Researched and Applied
- url: https://ai.pydantic.dev/multi-agent-applications/
  why: Official multi-agent patterns including agent delegation and programmatic hand-off
  content: Agent delegation with RunContext, usage tracking, dependency sharing patterns
  key_patterns:
    - Agent delegation: Parent agent calls delegate agent via tools, maintains control
    - Usage tracking: Pass ctx.usage to delegate agents for consolidated token counting
    - Dependency sharing: Shared deps_type between agents or subset dependencies
    - Multiple models: Different LLM providers per agent with UsageLimits for cost control

- url: https://ai.pydantic.dev/agents/
  why: Comprehensive agent architecture and configuration patterns
  content: System prompts, output types, execution methods, agent composition
  applied_patterns:
    - Agent creation with get_llm_model() from providers.py
    - System prompts as string constants with clear role definitions
    - Structured outputs with Pydantic models for financial data validation

- url: https://ai.pydantic.dev/tools/
  why: Tool integration patterns and function registration
  content: @agent.tool decorators, RunContext usage, parameter validation
  implementation_focus:
    - Database query tools with AsyncPG integration
    - RAG consultation tools for historical context
    - Inter-agent communication tools with JSON validation

- url: https://ai.pydantic.dev/testing/
  why: Testing strategies specific to multi-agent systems
  content: TestModel, FunctionModel, Agent.override(), pytest patterns
  testing_strategy:
    - TestModel for rapid development validation of both agents
    - Agent.override() for isolated testing of coordination logic
    - Integration tests for database connectivity and agent communication

# MCP Server Integration
- mcp: Archon
  query: "pydantic ai agent coordination patterns database integration"
  why: Latest patterns and code examples for multi-agent systems
  findings: Agent delegation patterns, dependency injection, structured communication
```

### Financial Data Architecture Research

```yaml
# PostgreSQL AsyncPG Integration Patterns
- url: https://www.tigerdata.com/blog/how-to-build-applications-with-asyncpg-and-postgresql
  why: Production patterns for financial data applications with AsyncPG
  content: Connection pooling, async query execution, TimescaleDB integration
  key_implementations:
    - Connection management: Single connection pool shared between agents
    - Query patterns: Async fetch with proper error handling and connection cleanup
    - Performance optimization: Prepared statements for repeated queries
    - Data conversion: pandas DataFrame integration for result processing

- url: https://medium.com/data-science/how-to-store-financial-market-data-for-backtesting-84b95fc016fc
  why: Financial market data storage patterns and performance optimization
  content: OHLCV data models, indexing strategies, query optimization
  applied_concepts:
    - Timestamp-based indexing for time series queries
    - Decimal precision for financial data accuracy
    - Query optimization for large datasets (7M+ records)
    - Performance considerations for backtesting workloads

# Database Schema Context
- existing_schema: "Complete ICT schema with 7,081,584 OHLCV records"
- supported_symbols: "15 assets with enum validation (audusd, eurusd, etc.)"
- timeframes: "5 timeframes (15m, 1h, 4h, 1d, 1w) with conditional field logic"
- functions: "60+ specialized SQL functions for market structure analysis"
- coverage: "Major pairs (2000+), metals (2009+), indices (2010+)"
```

### ICT Analysis Domain Knowledge

```yaml
# Inner Circle Trader Methodology Context
backtesting_capabilities:
  order_blocks: "Performance analysis with respect rates and session filtering"
  fair_value_gaps: "Gap detection and fill analysis across timeframes"
  liquidity_sweeps: "High/low breach analysis with volume confirmation"
  market_structure: "Break of structure detection and trend analysis"
  session_analysis: "London, New York, Asian session performance metrics"
  
analysis_strategies:
  performance_analysis: "Statistical validation of setup success rates"
  correlation_study: "Cross-asset and timeframe correlation analysis"
  structure_detection: "Automated pattern recognition and validation"
  
quality_requirements:
  high_confidence: "n≥20 sample size, ≥80% data coverage"
  balanced: "n≥10 sample size, ≥70% data coverage"
  broad_coverage: "Maximum data inclusion with statistical warnings"
```

### Security and Production Considerations

```yaml
# Pydantic AI Security Patterns
security_requirements:
  api_management:
    environment_variables: ["OLLAMA_HOST", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "DATABASE_URL"]
    secure_storage: "Never commit API keys or database credentials to version control"
    rotation_strategy: "Environment-based configuration with pydantic-settings"
  
  input_validation:
    sanitization: "Validate all user inputs with Pydantic models"
    sql_injection: "Use parameterized queries and AsyncPG's built-in protection"
    prompt_injection: "Implement prompt injection prevention in system prompts"
  
  database_security:
    connection_pooling: "Secure connection management with proper cleanup"
    query_validation: "Validate SQL function calls against whitelist"
    data_filtering: "Ensure no sensitive data exposure in agent responses"
```

### Common Multi-Agent Gotchas (Researched and Addressed)

```yaml
# Agent Coordination Gotchas
implementation_gotchas:
  async_patterns:
    issue: "Mixing sync and async agent calls inconsistently"
    research: "Pydantic AI async/await best practices for multi-agent systems"
    solution: "Use async/await consistently, proper RunContext handling in tools"
  
  dependency_complexity:
    issue: "Complex dependency graphs between agents can be hard to debug"
    research: "Dependency injection best practices in Pydantic AI multi-agent systems"
    solution: "Shared dependency dataclass, clear separation of concerns"
  
  usage_tracking:
    issue: "Token usage not properly aggregated across agent calls"
    research: "Usage tracking patterns in agent delegation"
    solution: "Pass ctx.usage to delegate agents, use UsageLimits for cost control"
  
  database_connections:
    issue: "Connection pool exhaustion with multiple agents"
    research: "AsyncPG connection pooling in multi-agent environments"
    solution: "Single shared connection pool, proper connection lifecycle management"
  
  error_propagation:
    issue: "Errors in sub-agent can crash entire workflow"
    research: "Error handling and retry patterns for agent delegation"
    solution: "Graceful error handling with fallback strategies and user-friendly messages"
```

## Implementation Blueprint

### Technology Research Phase ✅ COMPLETED

**RESEARCH COMPLETED - Ready for implementation:**

✅ **Pydantic AI Multi-Agent Framework Deep Dive:**
- [x] Agent delegation patterns with RunContext and usage tracking
- [x] Model provider configuration with multiple LLM support
- [x] Tool integration patterns for database and RAG operations
- [x] Dependency injection system for shared resources
- [x] Testing strategies with TestModel for multi-agent validation

✅ **Financial Database Architecture Investigation:**
- [x] AsyncPG connection pooling patterns for high-performance queries
- [x] OHLCV data models and indexing strategies for 7M+ records
- [x] ICT-specific SQL function integration and parameter mapping
- [x] Error handling and retry mechanisms for database operations
- [x] Performance optimization for sub-second query execution

✅ **Security and Production Patterns:**
- [x] Environment-based configuration with pydantic-settings
- [x] SQL injection prevention with parameterized queries
- [x] Prompt injection prevention strategies
- [x] Connection pool security and resource management

### Multi-Agent Implementation Plan

```yaml
Implementation Task 1 - Project Architecture Setup:
  CREATE project structure following main_agent_reference patterns:
    - settings.py: Environment configuration with database and LLM provider settings
    - providers.py: Model provider abstraction with get_llm_model() and fallback logic
    - database.py: AsyncPG connection pool management and query utilities
    - coordinator_agent.py: Strategic query interpretation and planning agent
    - backtesting_agent.py: Technical SQL execution and data retrieval agent
    - models.py: Pydantic models for inter-agent communication and data validation
    - dependencies.py: Shared dependency classes for database and RAG integration
    - tests/: Comprehensive test suite for multi-agent workflows

Implementation Task 2 - Database Integration Layer:
  IMPLEMENT database.py with AsyncPG integration:
    - Connection pool initialization with proper configuration
    - Query execution utilities with error handling and retry logic
    - SQL function registry with parameter validation
    - Result formatting and statistical validation utilities
    - Connection lifecycle management and cleanup

Implementation Task 3 - Coordinator Agent Development:
  DEVELOP coordinator_agent.py following delegation patterns:
    - Query classification logic (RAG-first vs backtesting-first vs hybrid)
    - Strategic parameter extraction and validation with Pydantic models
    - RAG memory consultation for historical context
    - Strategic analysis plan formulation with structured JSON output
    - Backtesting Sub-Agent delegation with proper usage tracking
    - Response synthesis and user-friendly presentation

Implementation Task 4 - Backtesting Sub-Agent Development:
  IMPLEMENT backtesting_agent.py for technical execution:
    - Strategic plan interpretation from Coordinator Agent JSON requests
    - SQL function selection and parameter mapping from reference documents
    - Database query execution using AsyncPG with connection pool
    - Raw result formatting and structured JSON return
    - Statistical validation and confidence level calculation
    - Error handling with alternative suggestions

Implementation Task 5 - Inter-Agent Communication Protocol:
  CREATE structured communication models in models.py:
    - CoordinatorRequest: Strategic analysis plan with validation
    - BacktestingResponse: Execution results with metadata and recommendations
    - Error handling models for graceful failure communication
    - Statistical validation models for confidence reporting
    - Input validation models for user query processing

Implementation Task 6 - RAG Integration and Tools:
  DEVELOP RAG integration tools:
    - Historical context consultation tools for Coordinator Agent
    - Documentation reference tools for function selection
    - Memory management for conversation context
    - Embedding generation and vector search utilities

Implementation Task 7 - Comprehensive Testing Suite:
  IMPLEMENT multi-agent testing patterns:
    - TestModel integration for rapid development validation
    - Agent.override() patterns for isolated testing
    - Integration tests for database connectivity and query execution
    - Multi-agent workflow tests with mock data
    - Performance testing for query execution times
    - Error scenario testing with graceful degradation validation
```

## Communication Protocol

### Coordinator → Sub-Agent Request Format
```python
from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime

class CoordinatorRequest(BaseModel):
    """Structured request from Coordinator to Backtesting Sub-Agent"""
    analysis_strategy: Literal["performance_analysis", "correlation_study", "structure_detection"]
    trading_context: Literal["scalping", "swing_trading", "position_analysis"]
    temporal_scope: Literal["recent_performance", "historical_pattern", "specific_period"]
    asset_focus: Literal["major_pairs", "cross_pairs", "specific_symbol"]
    session_relevance: Literal["high_liquidity", "all_sessions", "specific_session"]
    quality_requirements: Literal["high_confidence", "balanced", "broad_coverage"]
    
    # Optional specific parameters
    symbol: Optional[str] = Field(None, description="Specific symbol if asset_focus is 'specific_symbol'")
    timeframe: Optional[str] = Field(None, description="Specific timeframe for analysis")
    date_range: Optional[tuple[datetime, datetime]] = Field(None, description="Specific date range if temporal_scope is 'specific_period'")
    session: Optional[str] = Field(None, description="Specific session if session_relevance is 'specific_session'")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

### Sub-Agent → Coordinator Response Format
```python
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class BacktestingMetadata(BaseModel):
    """Statistical metadata for backtesting results"""
    sample_size: int = Field(..., description="Number of data points analyzed")
    data_coverage: float = Field(..., ge=0, le=100, description="Percentage of requested data available")
    confidence_level: float = Field(..., ge=0, le=100, description="Statistical confidence in results")
    execution_time_ms: int = Field(..., description="Query execution time in milliseconds")
    sql_function_used: str = Field(..., description="Primary SQL function executed")
    data_quality_score: float = Field(..., ge=0, le=100, description="Overall data quality assessment")

class BacktestingResponse(BaseModel):
    """Structured response from Backtesting Sub-Agent to Coordinator"""
    execution_status: Literal["success", "partial", "failed"]
    analysis_results: Dict[str, Any] = Field(..., description="Function-specific structured results")
    metadata: BacktestingMetadata
    recommendations: List[str] = Field(default_factory=list, description="Suggested follow-up analysis")
    warnings: List[str] = Field(default_factory=list, description="Data quality or coverage warnings")
    error_details: Optional[str] = Field(None, description="Error description if execution_status is 'failed'")
```

## System Constraints & Production Requirements

### Data Boundaries
- **Supported Symbols**: 15 assets with enum validation (audusd, eurusd, gbpusd, usdjpy, etc.)
- **Timeframe Logic**: Conditional fields based on timeframe (session data for intraday only)
- **Coverage Variations**: Major pairs (2000+), metals (2009+), indices (2010+)
- **Historical Range**: 2000-2024 for major pairs, varying coverage for other asset classes

### Performance Requirements
- **Query Response**: Sub-second execution for standard analysis (<1000ms)
- **Complex Analysis**: <10 seconds for multi-step correlation studies
- **Sample Size Minimums**: n≥20 for statistical reliability (high_confidence)
- **Data Quality Threshold**: ≥70% coverage for actionable insights
- **Connection Pool**: Maximum 20 concurrent connections with proper lifecycle management

### Technical Constraints
- **Database Connection**: Single AsyncPG connection pool shared between agents
- **Memory Management**: Large result sets require pagination (>10,000 records)
- **Error Recovery**: Graceful degradation with alternative suggestions
- **Token Limits**: UsageLimits for cost control across multi-agent workflows
- **Model Fallback**: Automatic fallback between Ollama → OpenAI → Anthropic

## Validation Loop

### Level 1: Multi-Agent Structure Validation

```bash
# Verify complete multi-agent project structure
find ict_backtesting_system -name "*.py" | sort
test -f ict_backtesting_system/coordinator_agent.py && echo "Coordinator Agent present"
test -f ict_backtesting_system/backtesting_agent.py && echo "Backtesting Sub-Agent present"
test -f ict_backtesting_system/database.py && echo "Database layer present"
test -f ict_backtesting_system/models.py && echo "Communication models present"

# Verify proper Pydantic AI multi-agent imports
grep -q "from pydantic_ai import Agent, RunContext" ict_backtesting_system/coordinator_agent.py
grep -q "@coordinator_agent.tool" ict_backtesting_system/coordinator_agent.py
grep -q "await backtesting_agent.run" ict_backtesting_system/coordinator_agent.py

# Expected: All required files with proper multi-agent delegation patterns
# If missing: Generate missing components with correct agent coordination
```

### Level 2: Agent Communication Validation

```bash
# Test agent delegation and communication protocol
python -c "
from ict_backtesting_system.coordinator_agent import coordinator_agent
from ict_backtesting_system.backtesting_agent import backtesting_agent
from ict_backtesting_system.models import CoordinatorRequest
print('Agents created successfully')
print(f'Coordinator tools: {len(coordinator_agent.tools)}')
print(f'Backtesting tools: {len(backtesting_agent.tools)}')
"

# Test with TestModel for multi-agent validation
python -c "
from pydantic_ai.models.test import TestModel
from ict_backtesting_system.coordinator_agent import coordinator_agent
test_model = TestModel()
with coordinator_agent.override(model=test_model):
    result = coordinator_agent.run_sync('Which EURUSD order blocks performed best?')
    print(f'Coordinator response: {result.output}')
"

# Expected: Agent instantiation works, delegation patterns functional, TestModel validation passes
# If failing: Debug agent coordination and communication protocol
```

### Level 3: Database Integration Validation

```bash
# Test database connectivity and query execution
python -c "
import asyncio
from ict_backtesting_system.database import get_connection_pool, execute_query
async def test_db():
    pool = await get_connection_pool()
    result = await execute_query('SELECT COUNT(*) FROM ohlcv_data LIMIT 1')
    print(f'Database connection successful: {result}')
asyncio.run(test_db())
"

# Test backtesting agent with real database
python -c "
import asyncio
from ict_backtesting_system.backtesting_agent import backtesting_agent
from ict_backtesting_system.models import CoordinatorRequest
async def test_backtesting():
    request = CoordinatorRequest(
        analysis_strategy='performance_analysis',
        trading_context='swing_trading',
        temporal_scope='recent_performance',
        asset_focus='specific_symbol',
        session_relevance='high_liquidity',
        quality_requirements='high_confidence',
        symbol='eurusd'
    )
    # Test with actual database connection
    result = await backtesting_agent.run(request.json())
    print(f'Backtesting result: {result.output}')
asyncio.run(test_backtesting())
"

# Expected: Database queries execute successfully, statistical validation works
# If failing: Debug database connection pool and SQL function integration
```

### Level 4: End-to-End Multi-Agent Workflow Validation

```bash
# Run complete multi-agent workflow tests
cd ict_backtesting_system
python -m pytest tests/test_multi_agent_workflow.py -v

# Test specific coordination scenarios
python -m pytest tests/test_coordinator_agent.py::test_query_classification -v
python -m pytest tests/test_backtesting_agent.py::test_sql_function_selection -v
python -m pytest tests/test_communication_protocol.py::test_request_response_validation -v

# Performance testing for production requirements
python -m pytest tests/test_performance.py::test_sub_second_queries -v
python -m pytest tests/test_performance.py::test_connection_pool_limits -v

# Expected: All tests pass, performance requirements met, error handling validated
# If failing: Fix implementation based on specific test failures
```

## Final Validation Checklist

### Multi-Agent Implementation Completeness

- [ ] **Complete project structure**: coordinator_agent.py, backtesting_agent.py, database.py, models.py, dependencies.py
- [ ] **Agent delegation patterns**: Proper RunContext usage, usage tracking, dependency sharing
- [ ] **Communication protocol**: Structured JSON requests/responses with Pydantic validation
- [ ] **Database integration**: AsyncPG connection pooling, SQL function registry, error handling
- [ ] **RAG integration**: Historical context consultation, documentation reference tools
- [ ] **Comprehensive testing**: TestModel validation, integration tests, performance benchmarks

### Pydantic AI Multi-Agent Best Practices

- [ ] **Type safety throughout**: Proper type hints, Pydantic model validation, structured outputs
- [ ] **Security patterns**: Environment variables, input validation, SQL injection prevention
- [ ] **Error handling**: Graceful degradation, retry mechanisms, user-friendly error messages
- [ ] **Performance optimization**: Connection pooling, query optimization, result caching
- [ ] **Async/sync consistency**: Proper async/await patterns, RunContext handling

### Production Readiness

- [ ] **Performance requirements met**: <10s end-to-end, <1s standard queries, >90% accuracy
- [ ] **Statistical validation**: Confidence levels, sample sizes, data quality scores
- [ ] **Monitoring and logging**: Structured logging, performance metrics, error tracking
- [ ] **Deployment configuration**: Environment variables, connection limits, fallback strategies
- [ ] **Documentation**: API documentation, deployment guide, troubleshooting procedures

---

## Anti-Patterns to Avoid

### Multi-Agent Development

- ❌ **Don't skip usage tracking** - Always pass ctx.usage to delegate agents for proper token accounting
- ❌ **Don't share connection objects** - Use connection pools, not direct connection sharing between agents
- ❌ **Don't ignore error boundaries** - Each agent should handle its own errors without cascading failures
- ❌ **Don't mix sync/async patterns** - Be consistent with async/await throughout the multi-agent workflow
- ❌ **Don't hardcode model strings** - Use get_llm_model() with environment-based configuration

### Database Integration

- ❌ **Don't create connections per query** - Use connection pooling for performance and resource management
- ❌ **Don't trust user input for SQL** - Always use parameterized queries and function whitelisting
- ❌ **Don't ignore statistical validation** - Always include sample sizes and confidence levels
- ❌ **Don't return raw database errors** - Provide user-friendly error messages with suggested alternatives

### Financial Data Handling

- ❌ **Don't ignore data quality** - Always validate coverage percentages and sample sizes
- ❌ **Don't mix timeframes without validation** - Ensure session data is only used for intraday timeframes
- ❌ **Don't assume data availability** - Always check coverage and provide alternatives for missing data
- ❌ **Don't skip decimal precision** - Use proper decimal types for financial calculations

**IMPLEMENTATION STATUS: READY FOR DEVELOPMENT** - Comprehensive research completed, multi-agent patterns validated, production requirements defined.
