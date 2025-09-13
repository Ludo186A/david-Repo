# INITIAL.md - ICT Backtesting Agent System

## FEATURE:

Build a two-agent system using Pydantic AI for intelligent backtesting analysis. The system consists of a **Coordinator Agent** that interprets user queries and formulates strategic analysis plans, and a **Backtesting Sub-Agent** that executes technical database queries against a production PostgreSQL database containing 7.08 million OHLCV records. The coordinator handles strategic decision-making and context interpretation, while the sub-agent focuses on technical execution using 60+ specialized SQL functions for market structure analysis.

## ARCHITECTURE:

### Two-Agent Design
- **Coordinator Agent**: Strategic query interpretation, planning, and response synthesis
- **Backtesting Sub-Agent**: Technical SQL function execution and data retrieval

### Communication Flow
```
User Query → Coordinator Agent → Strategic Analysis Plan → Backtesting Sub-Agent → SQL Execution → Results → Coordinator → User Response
```

### Data Foundation
- **Production Database**: 7,081,584 OHLCV records successfully ingested
- **Asset Coverage**: 15 supported symbols with enum validation
- **Timeframe Coverage**: 5 timeframes (15m, 1h, 4h, 1d, 1w) with conditional field logic
- **Historical Range**: 2000-2024 for major pairs, varying coverage for other asset classes
- **Storage**: External SSD deployment with optimized indexing

## COORDINATOR AGENT

### Responsibilities
- Query classification (RAG-first vs backtesting-first vs hybrid)
- Strategic parameter extraction and validation
- RAG memory consultation for historical context
- Strategic analysis plan formulation
- Response synthesis and presentation

### Core Capabilities
- Natural language interpretation for trading queries
- Strategic decision-making for analysis approach
- Context preservation across multi-step analysis
- Result formatting and user communication

### Reference Documents
- `docs/planning_guide.md`: Query classification and routing logic
- `docs/backtesting_capabilities.md`: Available strategic analysis approaches

## BACKTESTING SUB-AGENT

### Responsibilities
- Strategic plan interpretation
- SQL function selection and parameter mapping
- Database query execution
- Raw result formatting and return

### Core Capabilities
- Technical function mapping from strategic context
- Database connectivity and query execution
- Error handling and fallback strategies
- Statistical result validation

### Reference Documents
- `database/function_signatures.json`: Complete technical function reference
- `database/schema_reference.md`: Database structure and constraints

## DEPENDENCIES

- Pydantic AI Framework: Agent creation and tool integration
- AsyncPG: PostgreSQL async connection pooling
- Database: Supabase local instance with complete ICT schema
- Python Environment: Python 3.8+ with async/await support
- RAG: Supabase local instance with complete ICT schema
- Embedding Client: OpenAI-compatible embedding API client for generating vector embeddings
- LLM Providers:
Ollama (local server for primary AI tasks, using models like Llama or Mistral)
OpenAI API client (for optional integration via openai Python library)
Anthropic API client (for Claude models via anthropic Python library)
- Embedding Providers:
Local embeddings via Ollama (if supported by the model) or Hugging Face Transformers (sentence-transformers library for models like all-MiniLM-L6-v2)
- OpenAI-compatible API (existing client, with fallback to OpenAI or other providers like Cohere if needed)

Configuration Notes: Use environment variables (e.g., OLLAMA_HOST, OPENAI_API_KEY, ANTHROPIC_API_KEY) for flexible switching between providers without code changes. Pydantic AI's model provider system allows dynamic selection via config.

## COORDINATOR AGENT SYSTEM PROMPT
You are an intelligent AI coordinator agent for ICT backtesting analysis, with access to a Backtesting Sub-Agent that executes technical SQL queries against a production PostgreSQL database containing over 7 million OHLCV records. Your primary capabilities include:

Query classification (RAG-first vs backtesting-first vs hybrid)
Strategic parameter extraction and validation
RAG memory consultation for historical context
Strategic analysis plan formulation using reference documents
Coordination with the Backtesting Sub-Agent via structured JSON requests
Response synthesis and presentation to the user

When processing user queries, always classify the query type and consult RAG memory for context before formulating a plan. Use the Backtesting Sub-Agent when technical database execution is needed for performance analysis, correlation studies, or structure detection. Reference `docs/planning_guide.md` for classification and routing logic, and `docs/backtesting_capabilities.md` for available strategic approaches. Formulate requests to the Sub-Agent in the specified JSON format, including fields like "analysis_strategy", "trading_context", "temporal_scope", "asset_focus", "session_relevance", and "quality_requirements". Synthesize results from the Sub-Agent's JSON response into a user-friendly format, citing sources such as function names, sample sizes, and confidence levels. Consider data boundaries like supported symbols (e.g., audusd, eurusd), timeframes (15m, 1h, 4h, 1d, 1w), and historical coverage variations.

Your responses should be accurate and based on available data, well-structured and easy to understand, comprehensive while remaining concise, and transparent about analysis strategies and limitations. Use the Backtesting Sub-Agent only when the query requires database execution; otherwise, rely on RAG or direct interpretation for strategic insights. Handle errors by providing alternatives and explanations.

## BACKTESTING SUB-AGENT SYSTEM PROMPT
You are an intelligent AI backtesting sub-agent specialized in technical execution for ICT analysis, with direct access to a production PostgreSQL database featuring 60+ specialized SQL functions for market structure analysis. Your primary capabilities include:

Strategic plan interpretation from the Coordinator Agent
SQL function selection and parameter mapping based on reference documents
Database query execution using AsyncPG
Raw result formatting and structured JSON return
Error handling and fallback strategies

When receiving a JSON request from the Coordinator Agent, interpret fields like "analysis_strategy", "trading_context", "temporal_scope", "asset_focus", "session_relevance", and "quality_requirements" to select appropriate SQL functions. Reference `database/function_signatures.json` for complete function details and `database/schema_reference.md` for structure and constraints. Execute queries respecting constraints such as supported symbols, timeframe logic, and minimum sample sizes (n≥20). Return results in the specified JSON format, including "execution_status", "analysis_results", "metadata" (with sample_size, data_coverage, confidence_level, execution_time_ms), and "recommendations" for follow-ups. Validate results statistically and handle errors gracefully, suggesting alternatives if data coverage is below 70%.

Your outputs should be strictly in JSON format, accurate and based on database execution, concise in metadata, and transparent about any limitations or low-confidence scenarios. Do not respond directly to users; only process Coordinator requests and return structured data.


## COMMUNICATION PROTOCOL

### Coordinator → Sub-Agent Request Format
```json
{
  "analysis_strategy": "performance_analysis|correlation_study|structure_detection",
  "trading_context": "scalping|swing_trading|position_analysis", 
  "temporal_scope": "recent_performance|historical_pattern|specific_period",
  "asset_focus": "major_pairs|cross_pairs|specific_symbol",
  "session_relevance": "high_liquidity|all_sessions|specific_session",
  "quality_requirements": "high_confidence|balanced|broad_coverage"
}
```

### Sub-Agent → Coordinator Response Format
```json
{
  "execution_status": "success|partial|failed",
  "analysis_results": {}, // Function-specific structured results
  "metadata": {
    "sample_size": "integer",
    "data_coverage": "percentage", 
    "confidence_level": "percentage",
    "execution_time_ms": "integer"
  },
  "recommendations": ["string"] // Suggested follow-up analysis
}
```

## SYSTEM CONSTRAINTS

### Data Boundaries
- **Supported Symbols**: 15 assets with enum validation (audusd, eurusd, etc.)
- **Timeframe Logic**: Conditional fields based on timeframe (session data for intraday only)
- **Coverage Variations**: Major pairs (2000+), metals (2009+), indices (2010+)

### Performance Requirements
- **Query Response**: Sub-second execution for standard analysis
- **Sample Size Minimums**: n≥20 for statistical reliability
- **Data Quality Threshold**: ≥70% coverage for actionable insights

### Technical Constraints
- **Database Connection**: Single connection pool shared between agents
- **Memory Management**: Large result sets require pagination
- **Error Recovery**: Graceful degradation with alternative suggestions

## EXAMPLES:

### User Query Processing
```
User: "Which EURUSD order blocks performed best during London session?"

Coordinator Analysis:
- Classification: backtesting-first
- Strategy: performance_analysis
- Context: swing_trading (order blocks typically swing-level)
- Scope: recent_performance (30 days default)
- Focus: specific_symbol (EURUSD)
- Session: high_liquidity (London)

Sub-Agent Execution:
- Maps to: update_order_block_performance()
- Parameters: symbol='eurusd', session='London', min_respect_rate=60
- Executes SQL function with optimal timeframe selection
- Returns: structured performance metrics with confidence data
```

### Error Handling Example
```
User: "Show me JPXJPY correlation with DXY for last 5 years"

Coordinator: Identifies data coverage issue (JPXJPY limited to 2010-2012)
Sub-Agent: Returns coverage analysis with alternative suggestions
Coordinator: Presents limitation explanation and offers viable alternatives
```

## DOCUMENTATION REQUIREMENTS

### For Coordinator Agent
- Strategic analysis approaches and when to use them
- Query classification patterns and routing logic
- RAG integration strategies for historical context
- Response synthesis and formatting guidelines

### For Backtesting Sub-Agent  
- Complete function reference with parameters and return formats
- Database schema documentation with enum constraints
- Query optimization patterns and performance considerations
- Error codes and recovery strategies

## SUCCESS CRITERIA

### Performance Metrics
- Query classification accuracy >90%
- Sub-agent function selection accuracy >95%
- End-to-end query resolution <10 seconds
- Statistical confidence reporting in 100% of analysis results

### System Reliability
- Database connection stability >99.5%
- Graceful error handling for all constraint violations
- Fallback suggestions for insufficient data scenarios
- Consistent response formatting across all analysis types

## IMPLEMENTATION NOTES

- **Start Simple**: Implement basic coordinator routing first, add RAG integration second
- **Database First**: Sub-agent should validate database connectivity before coordinator integration
- **Error Boundaries**: Each agent handles its own errors without cascading failures
- **Logging Strategy**: Structured logging for debugging coordination between agents
- **Testing Approach**: Unit tests for each agent, integration tests for communication protocol

## CURRENT STATUS

- **Database**: Production-ready with 7M+ records and 60+ functions operational
- **Schema**: Complete ICT schema deployed with optimized indexes  
- **Data Pipeline**: Proven ingestion capability with comprehensive validation
- **Next Step**: Implement coordinator agent with reference to planning documentation

## EXAMPLES:
examples/basic_chat_agent - Basic chat agent with conversation memory
examples/tool_enabled_agent - Tool-enabled agent with web search capabilities
examples/structured_output_agent - Structured output agent for data validation
examples/testing_examples - Testing examples with TestModel and FunctionModel
examples/main_agent_reference - Best practices for building Pydantic AI agents
examples/rag_pipeline - RAG ingestion and also very important SQL DB and Graph DB util fils in utils/

## DOCUMENTATION:
Pydantic AI Official Documentation: https://ai.pydantic.dev/
Agent Creation Guide: https://ai.pydantic.dev/agents/
Tool Integration: https://ai.pydantic.dev/tools/
Testing Patterns: https://ai.pydantic.dev/testing/
Model Providers: https://ai.pydantic.dev/models/
Use Archon MCP server to query for Pydantic AI and Graphiti documentation and code examples

## OTHER CONSIDERATIONS:
Use environment variables for API key configuration instead of hardcoded model strings
Keep agents simple - default to string output unless structured output is specifically needed
Follow the main_agent_reference patterns for configuration and providers
Always include comprehensive testing with TestModel for development