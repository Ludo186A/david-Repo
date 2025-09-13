"""
Coordinator Agent for ICT Backtesting Analysis System.
Handles strategic query interpretation, planning, and response synthesis.
"""

import logging
import json
from typing import Dict, Any, List, Optional
from pydantic_ai import Agent, RunContext
from pydantic import ValidationError

from providers import get_coordinator_model
from models import (
    QueryClassification, 
    CoordinatorRequest, 
    BacktestingResponse
)
from dependencies import SharedDependencies
from backtesting_agent import backtesting_agent

logger = logging.getLogger(__name__)

COORDINATOR_SYSTEM_PROMPT = """
You are an intelligent AI coordinator agent for ICT backtesting analysis, with access to a Backtesting Sub-Agent that executes technical SQL queries against a production PostgreSQL database containing over 7 million OHLCV records.

## Your Core Capabilities

### Query Classification & Routing
- **RAG-first queries**: Historical context, methodology explanations, general ICT concepts
- **Backtesting-first queries**: Performance analysis, statistical validation, data-driven insights
- **Hybrid queries**: Complex analysis requiring both historical context and database execution

### Strategic Analysis Planning
- Extract key parameters from natural language queries
- Formulate structured analysis plans for the Backtesting Sub-Agent
- Validate query feasibility against data boundaries and constraints
- Provide context-aware recommendations for analysis approach

### Multi-Agent Coordination
- Delegate technical execution to Backtesting Sub-Agent via structured JSON requests
- Synthesize results from Sub-Agent responses into user-friendly format
- Handle error scenarios with alternative suggestions and explanations
- Maintain conversation context across multi-step analysis workflows

## ICT Methodology Context

You specialize in Inner Circle Trader (ICT) concepts including:
- **Order Blocks**: Institutional supply/demand zones with performance tracking
- **Fair Value Gaps**: Price imbalances requiring fill analysis across timeframes
- **Liquidity Sweeps**: High/low breach analysis with volume confirmation
- **Market Structure**: Break of structure detection and trend analysis
- **Session Analysis**: London, New York, Asian session performance metrics

## Data Boundaries & Constraints

### Supported Assets
- 15 symbols with enum validation: AUDUSD, EURUSD, GBPUSD, USDJPY, USDCHF, USDCAD, NZDUSD, XAUUSD, XAGUSD, US30, NAS100, SPX500, UK100, GER40, JPN225

### Timeframes & Coverage
- **Timeframes**: 15m, 1h, 4h, 1d, 1w with conditional field logic
- **Coverage**: Major pairs (2000+), metals (2009+), indices (2010+)
- **Session Data**: Only available for intraday timeframes (15m, 1h, 4h)

### Quality Requirements
- **High Confidence**: n≥20 sample size, ≥80% data coverage
- **Balanced**: n≥10 sample size, ≥70% data coverage  
- **Broad Coverage**: Maximum inclusion with statistical warnings

## Communication Protocol

### Sub-Agent Request Format
When delegating to the Backtesting Sub-Agent, use this structured format:

```json
{
  "analysis_strategy": "performance_analysis|correlation_study|structure_detection",
  "trading_context": "scalping|swing_trading|position_analysis",
  "temporal_scope": "recent_performance|historical_pattern|specific_period",
  "asset_focus": "major_pairs|cross_pairs|specific_symbol",
  "session_relevance": "high_liquidity|all_sessions|specific_session",
  "quality_requirements": "high_confidence|balanced|broad_coverage",
  "symbol": "optional_specific_symbol",
  "timeframe": "optional_specific_timeframe",
  "session": "optional_specific_session"
}
```

### Response Synthesis Guidelines
- Cite statistical metadata (sample sizes, confidence levels, execution time)
- Explain analysis approach and methodology used
- Highlight data quality considerations and limitations
- Provide actionable insights with proper context
- Suggest follow-up analysis when appropriate

## Error Handling & Fallbacks
- Gracefully handle data coverage issues with alternative suggestions
- Explain constraint violations with educational context
- Provide fallback analysis options when primary approach fails
- Maintain user engagement with constructive alternatives

## Response Style
- Professional yet accessible tone for financial professionals
- Clear explanation of statistical concepts and limitations
- Structured presentation with key findings highlighted
- Educational context for ICT methodology applications
- Transparent about analysis confidence and data quality

Remember: You coordinate strategy and communication. The Backtesting Sub-Agent handles all technical database execution. Focus on interpretation, planning, and user experience.
"""

# Initialize the coordinator agent
coordinator_agent = Agent(
    get_coordinator_model(),
    deps_type=SharedDependencies,
    system_prompt=COORDINATOR_SYSTEM_PROMPT
)

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
    try:
        # Simple classification logic based on keywords
        query_lower = user_query.lower()
        
        # Backtesting-first indicators
        backtesting_keywords = [
            "performance", "backtest", "statistics", "results", "data", 
            "analysis", "success rate", "win rate", "profit", "loss",
            "order block", "fair value gap", "liquidity sweep", "session"
        ]
        
        # RAG-first indicators
        rag_keywords = [
            "explain", "what is", "how does", "methodology", "concept",
            "definition", "theory", "principle", "strategy", "approach"
        ]
        
        backtesting_score = sum(1 for keyword in backtesting_keywords if keyword in query_lower)
        rag_score = sum(1 for keyword in rag_keywords if keyword in query_lower)
        
        if backtesting_score > rag_score:
            routing = "backtesting_first"
            confidence = min(90.0, 60.0 + (backtesting_score * 10))
            reasoning = f"Query contains {backtesting_score} backtesting indicators"
            approach = "Execute database analysis for data-driven insights"
        elif rag_score > backtesting_score:
            routing = "rag_first"
            confidence = min(90.0, 60.0 + (rag_score * 10))
            reasoning = f"Query contains {rag_score} conceptual indicators"
            approach = "Consult knowledge base for methodology explanation"
        else:
            routing = "hybrid"
            confidence = 70.0
            reasoning = "Query requires both conceptual and analytical components"
            approach = "Combine knowledge consultation with database analysis"
        
        return QueryClassification(
            routing_decision=routing,
            confidence=confidence,
            reasoning=reasoning,
            suggested_approach=approach
        )
        
    except Exception as e:
        logger.error(f"Query classification failed: {e}")
        return QueryClassification(
            routing_decision="hybrid",
            confidence=50.0,
            reasoning=f"Classification error: {str(e)}",
            suggested_approach="Use hybrid approach as fallback"
        )

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
    try:
        # Import here to avoid circular imports
        from .backtesting_agent import backtesting_agent
        
        # Convert request to JSON for sub-agent
        request_json = analysis_request.model_dump_json()
        
        logger.info(f"Delegating analysis: {analysis_request.analysis_strategy}")
        
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
            logger.error(f"Response parsing error: {e}")
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
        
    except Exception as e:
        logger.error(f"Backtesting delegation failed: {e}")
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
            error_details=f"Delegation error: {str(e)}"
        )

@coordinator_agent.tool
async def formulate_analysis_plan(
    ctx: RunContext[SharedDependencies],
    user_query: str,
    classification: QueryClassification
) -> CoordinatorRequest:
    """
    Formulate structured analysis plan based on user query and classification.
    
    Args:
        user_query: Original user query
        classification: Query classification result
    
    Returns:
        CoordinatorRequest with strategic parameters
    """
    try:
        query_lower = user_query.lower()
        
        # Determine analysis strategy
        if any(word in query_lower for word in ["performance", "success", "win rate", "profit"]):
            analysis_strategy = "performance_analysis"
        elif any(word in query_lower for word in ["correlation", "relationship", "compare"]):
            analysis_strategy = "correlation_study"
        else:
            analysis_strategy = "structure_detection"
        
        # Determine trading context
        if any(word in query_lower for word in ["scalp", "minute", "quick", "fast"]):
            trading_context = "scalping"
        elif any(word in query_lower for word in ["swing", "daily", "day", "week"]):
            trading_context = "swing_trading"
        else:
            trading_context = "position_analysis"
        
        # Determine temporal scope
        if any(word in query_lower for word in ["recent", "latest", "current", "today"]):
            temporal_scope = "recent_performance"
        elif any(word in query_lower for word in ["historical", "past", "history", "long term"]):
            temporal_scope = "historical_pattern"
        else:
            temporal_scope = "recent_performance"
        
        # Determine asset focus
        symbols = ["eurusd", "gbpusd", "usdjpy", "audusd", "usdchf", "usdcad", "nzdusd", 
                  "xauusd", "xagusd", "us30", "nas100", "spx500", "uk100", "ger40", "jpn225"]
        
        found_symbol = None
        for symbol in symbols:
            if symbol in query_lower:
                found_symbol = symbol.upper()
                break
        
        if found_symbol:
            asset_focus = "specific_symbol"
        elif any(word in query_lower for word in ["major", "eur", "gbp", "usd", "jpy"]):
            asset_focus = "major_pairs"
        else:
            asset_focus = "major_pairs"
        
        # Determine session relevance
        if any(word in query_lower for word in ["london", "new york", "asian", "session"]):
            session_relevance = "specific_session"
        elif any(word in query_lower for word in ["liquid", "volume", "active"]):
            session_relevance = "high_liquidity"
        else:
            session_relevance = "all_sessions"
        
        # Determine quality requirements
        if any(word in query_lower for word in ["accurate", "precise", "confident", "reliable"]):
            quality_requirements = "high_confidence"
        elif any(word in query_lower for word in ["broad", "comprehensive", "all", "everything"]):
            quality_requirements = "broad_coverage"
        else:
            quality_requirements = "balanced"
        
        return CoordinatorRequest(
            analysis_strategy=analysis_strategy,
            trading_context=trading_context,
            temporal_scope=temporal_scope,
            asset_focus=asset_focus,
            session_relevance=session_relevance,
            quality_requirements=quality_requirements,
            symbol=found_symbol
        )
        
    except Exception as e:
        logger.error(f"Analysis plan formulation failed: {e}")
        # Return default plan
        return CoordinatorRequest(
            analysis_strategy="performance_analysis",
            trading_context="swing_trading",
            temporal_scope="recent_performance",
            asset_focus="major_pairs",
            session_relevance="all_sessions",
            quality_requirements="balanced"
        )

# Convenience function to create coordinator agent with dependencies
def create_coordinator_agent(deps: SharedDependencies) -> Agent:
    """
    Create a coordinator agent with specified dependencies.
    
    Args:
        deps: Shared dependencies for the agent
        
    Returns:
        Configured coordinator agent
    """
    return coordinator_agent
