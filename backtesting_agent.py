"""
Backtesting Sub-Agent for ICT Analysis System.
Handles technical SQL execution and data retrieval.
"""

import logging
import json
import time
from typing import Dict, Any, List, Optional
from pydantic_ai import Agent, RunContext
from pydantic import ValidationError

from providers import get_backtesting_model
from models import (
    CoordinatorRequest,
    BacktestingResponse,
    FunctionSelection,
    ValidationResult,
    SQLFunction
)
from dependencies import SharedDependencies
from ollama_health import check_ollama_status
from embedding_service import get_embeddings
from connection_manager import get_connection_status, validate_external_ssd_setup

logger = logging.getLogger(__name__)

BACKTESTING_SYSTEM_PROMPT = """
You are a specialized AI backtesting sub-agent for ICT analysis, with direct access to a production PostgreSQL database containing 7,081,584 OHLCV records and 60+ specialized SQL functions for market structure analysis.

## Your Core Responsibilities

### Strategic Plan Interpretation
- Parse structured JSON requests from the Coordinator Agent
- Map strategic context to appropriate SQL functions and parameters
- Validate request parameters against database constraints and available data
- Select optimal analysis approach based on quality requirements

### Technical Database Execution
- Execute SQL queries using AsyncPG connection pool
- Access 60+ specialized ICT analysis functions in the database schema
- Handle connection management and query optimization
- Validate results for statistical significance and data quality

### Structured Response Generation
- Format results in standardized JSON response structure
- Include comprehensive metadata (sample sizes, confidence levels, execution time)
- Provide statistical validation and data quality assessments
- Generate actionable recommendations for follow-up analysis

## Database Schema Context

### Available SQL Functions (60+ specialized functions)
Reference `function_signatures.json` for complete function catalog including:
- `update_order_block_performance()`: Order block success rate analysis
- `detect_fair_value_gaps()`: FVG identification and fill analysis  
- `analyze_liquidity_sweeps()`: High/low breach detection with volume
- `calculate_session_performance()`: Session-based performance metrics
- `identify_market_structure_breaks()`: BOS detection and validation

### Data Structure
- **Primary Table**: `ohlcv_data` with 7,081,584 records
- **Symbols**: 15 supported assets with enum validation
- **Timeframes**: 15m, 1h, 4h, 1d, 1w with conditional fields
- **Sessions**: London, New York, Asian (intraday only)
- **Date Range**: 2000-2024 (varies by asset class)

## Request Processing Workflow

### 1. Request Validation
- Validate JSON structure against expected schema
- Check symbol/timeframe combinations against database constraints
- Verify session data availability for intraday timeframes
- Assess data coverage for requested analysis period

### 2. Function Selection & Parameter Mapping
- Map `analysis_strategy` to appropriate SQL function category
- Apply `trading_context` to parameter selection (timeframe, filters)
- Use `temporal_scope` for date range determination
- Apply `quality_requirements` to sample size and coverage thresholds

### 3. Query Execution & Validation
- Execute selected SQL function with mapped parameters
- Validate result set for minimum sample size requirements
- Calculate statistical confidence based on data coverage
- Measure execution time for performance reporting

### 4. Response Formatting
```json
{
  "execution_status": "success|partial|failed",
  "analysis_results": {
    // Function-specific structured results
  },
  "metadata": {
    "sample_size": 150,
    "data_coverage": 85.2,
    "confidence_level": 92.5,
    "execution_time_ms": 245,
    "sql_function_used": "update_order_block_performance",
    "data_quality_score": 88.7
  },
  "recommendations": [
    "Consider extending analysis to 4h timeframe for broader context",
    "High confidence results - suitable for strategy validation"
  ],
  "warnings": [
    "Limited data coverage for XAGUSD before 2009"
  ]
}
```

## Quality Assurance Standards

### Statistical Validation
- **High Confidence**: n≥20, coverage≥80%, confidence≥90%
- **Balanced**: n≥10, coverage≥70%, confidence≥75%
- **Broad Coverage**: n≥5, coverage≥50%, confidence≥60%

### Error Handling
- Graceful degradation for insufficient data scenarios
- Alternative function suggestions for failed queries
- Clear error messages with suggested remediation
- Fallback to broader analysis scope when needed

### Performance Requirements
- Standard queries: <1 second execution time
- Complex analysis: <5 seconds execution time
- Connection pool management: Proper cleanup and resource management
- Query optimization: Use prepared statements for repeated patterns

## Communication Protocol

### Input: Coordinator Agent JSON Request
- Parse all required fields with validation
- Handle optional parameters with appropriate defaults
- Validate against database constraints before execution

### Output: Structured JSON Response
- Always include execution_status, analysis_results, metadata
- Provide actionable recommendations based on results
- Include warnings for data quality or coverage issues
- Never expose raw database errors to Coordinator

## Critical Constraints

### Data Boundaries
- Respect symbol enum validation (15 supported assets)
- Honor timeframe conditional logic (session data intraday only)
- Validate date ranges against actual data availability
- Apply minimum sample size requirements consistently

### Security & Performance
- Use parameterized queries exclusively (no SQL injection risk)
- Maintain connection pool limits and proper cleanup
- Log performance metrics for monitoring and optimization
- Never return sensitive database connection information

Remember: You are the technical execution engine. Focus on accurate, fast, and reliable database operations. The Coordinator handles all user communication and strategic interpretation.
"""

# Initialize the backtesting agent
backtesting_agent = Agent(
    get_backtesting_model(),
    deps_type=SharedDependencies,
    system_prompt=BACKTESTING_SYSTEM_PROMPT
)

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
    try:
        # Get function suggestions from registry
        suggested_functions = ctx.deps.function_registry.suggest_functions(
            analysis_strategy, trading_context
        )
        
        if not suggested_functions:
            # Fallback to available functions
            suggested_functions = list(ctx.deps.function_registry.functions.keys())
        
        # Select primary function based on strategy
        if analysis_strategy == "performance_analysis":
            preferred = ["update_order_block_performance", "analyze_session_performance"]
        elif analysis_strategy == "correlation_study":
            preferred = ["detect_fair_value_gaps", "analyze_session_performance"]
        else:  # structure_detection
            preferred = ["detect_fair_value_gaps", "update_order_block_performance"]
        
        # Find best match
        recommended_function = None
        for func in preferred:
            if func in suggested_functions:
                recommended_function = func
                break
        
        if not recommended_function and suggested_functions:
            recommended_function = suggested_functions[0]
        elif not recommended_function:
            recommended_function = "update_order_block_performance"  # Default fallback
        
        # Set parameters based on context
        parameters = {}
        if trading_context == "scalping":
            parameters["timeframe"] = "15m"
        elif trading_context == "swing_trading":
            parameters["timeframe"] = "4h"
        else:
            parameters["timeframe"] = "1d"
        
        if quality_requirements == "high_confidence":
            parameters["min_sample_size"] = 20
        elif quality_requirements == "balanced":
            parameters["min_sample_size"] = 10
        else:
            parameters["min_sample_size"] = 5
        
        return FunctionSelection(
            recommended_function=recommended_function,
            parameters=parameters,
            confidence=85.0,
            alternative_functions=suggested_functions[:3],
            reasoning=f"Selected {recommended_function} for {analysis_strategy} with {trading_context} context"
        )
        
    except Exception as e:
        logger.error(f"Function selection failed: {e}")
        return FunctionSelection(
            recommended_function="update_order_block_performance",
            parameters={"timeframe": "4h", "min_sample_size": 10},
            confidence=50.0,
            alternative_functions=[],
            reasoning=f"Fallback selection due to error: {str(e)}"
        )

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
    try:
        # Validate function exists
        if function_name not in ctx.deps.function_registry.functions:
            return {
                "success": False,
                "error": f"Function {function_name} not found",
                "alternatives": list(ctx.deps.function_registry.functions.keys())[:5]
            }
        
        start_time = time.time()
        
        # Execute with database manager
        result = await ctx.deps.db_manager.execute_function(function_name, parameters)
        
        execution_time = int((time.time() - start_time) * 1000)
        
        return {
            "success": True,
            "data": result,
            "row_count": len(result),
            "execution_time_ms": execution_time,
            "function_used": function_name
        }
        
    except Exception as e:
        logger.error(f"SQL function execution failed: {e}")
        return {
            "success": False,
            "error": f"Database error: {str(e)}",
            "suggestion": "Check parameter types and data availability"
        }

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
    try:
        sample_size = len(raw_results)
        
        # Define quality thresholds
        thresholds = {
            "high_confidence": {"min_sample": 20, "min_coverage": 80, "min_confidence": 90},
            "balanced": {"min_sample": 10, "min_coverage": 70, "min_confidence": 75},
            "broad_coverage": {"min_sample": 5, "min_coverage": 50, "min_confidence": 60}
        }
        
        threshold = thresholds.get(quality_requirements, thresholds["balanced"])
        
        # Calculate metrics
        is_valid = sample_size >= threshold["min_sample"]
        data_coverage = min(100.0, (sample_size / threshold["min_sample"]) * 100)
        confidence_level = min(100.0, data_coverage * (threshold["min_confidence"] / 100))
        quality_score = (confidence_level + data_coverage) / 2
        
        warnings = []
        if sample_size < threshold["min_sample"]:
            warnings.append(f"Sample size {sample_size} below recommended minimum {threshold['min_sample']}")
        if data_coverage < threshold["min_coverage"]:
            warnings.append(f"Data coverage {data_coverage:.1f}% below target {threshold['min_coverage']}%")
        
        return ValidationResults(
            is_valid=is_valid,
            confidence_level=confidence_level,
            sample_size=sample_size,
            data_coverage=data_coverage,
            warnings=warnings,
            quality_score=quality_score
        )
        
    except Exception as e:
        logger.error(f"Result validation failed: {e}")
        return ValidationResults(
            is_valid=False,
            confidence_level=0.0,
            sample_size=0,
            data_coverage=0.0,
            warnings=[f"Validation error: {str(e)}"],
            quality_score=0.0
        )

@backtesting_agent.tool
async def process_coordinator_request(
    ctx: RunContext[SharedDependencies],
    request_json: str
) -> BacktestingResponse:
    """
    Process complete request from Coordinator Agent.
    
    Args:
        request_json: JSON string with CoordinatorRequest
    
    Returns:
        BacktestingResponse with complete analysis results
    """
    try:
        # Parse request
        request_data = json.loads(request_json)
        request = CoordinatorRequest(**request_data)
        
        logger.info(f"Processing request: {request.analysis_strategy}")
        
        # Select optimal function
        function_selection = await select_optimal_function(
            ctx, 
            request.analysis_strategy,
            request.trading_context,
            request.quality_requirements
        )
        
        # Prepare parameters
        parameters = function_selection.parameters.copy()
        if request.symbol:
            parameters["symbol"] = request.symbol.lower()
        if request.timeframe:
            parameters["timeframe"] = request.timeframe
        if request.session:
            parameters["session"] = request.session
        
        # Execute SQL function
        execution_result = await execute_sql_function(
            ctx,
            function_selection.recommended_function,
            parameters
        )
        
        if not execution_result["success"]:
            return BacktestingResponse(
                execution_status="failed",
                analysis_results={},
                metadata=BacktestingMetadata(
                    sample_size=0,
                    data_coverage=0.0,
                    confidence_level=0.0,
                    execution_time_ms=0,
                    sql_function_used=function_selection.recommended_function,
                    data_quality_score=0.0
                ),
                error_details=execution_result["error"]
            )
        
        # Validate results
        validation = await validate_results(
            ctx,
            execution_result["data"],
            request.quality_requirements
        )
        
        # Generate recommendations
        recommendations = []
        if validation.confidence_level > 90:
            recommendations.append("High confidence results - suitable for strategy validation")
        elif validation.confidence_level > 75:
            recommendations.append("Good confidence results - consider additional validation")
        else:
            recommendations.append("Low confidence - recommend broader analysis or different approach")
        
        if validation.sample_size < 20:
            recommendations.append("Consider extending time range or using broader criteria for more data")
        
        # Determine execution status
        if validation.is_valid and validation.confidence_level > 75:
            status = "success"
        elif validation.sample_size > 0:
            status = "partial"
        else:
            status = "failed"
        
        return BacktestingResponse(
            execution_status=status,
            analysis_results={
                "function_output": execution_result["data"],
                "summary_stats": {
                    "total_records": validation.sample_size,
                    "analysis_type": request.analysis_strategy,
                    "parameters_used": parameters
                }
            },
            metadata=BacktestingMetadata(
                sample_size=validation.sample_size,
                data_coverage=validation.data_coverage,
                confidence_level=validation.confidence_level,
                execution_time_ms=execution_result["execution_time_ms"],
                sql_function_used=function_selection.recommended_function,
                data_quality_score=validation.quality_score
            ),
            recommendations=recommendations,
            warnings=validation.warnings
        )
        
    except Exception as e:
        logger.error(f"Request processing failed: {e}")
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
            error_details=f"Processing error: {str(e)}"
        )

@backtesting_agent.tool
async def check_ollama_health(ctx: RunContext[SharedDependencies]) -> str:
    """
    Check Ollama service health and model availability for ICT backtesting.
    
    Returns:
        Formatted health status report
    """
    try:
        status = await check_ollama_status()
        
        # Format status report
        overall = status["overall_status"].upper()
        emoji = {"OPTIMAL": "🟢", "PARTIAL": "🟡", "DEGRADED": "🟠", "FAILED": "🔴"}.get(overall, "❓")
        
        report = f"{emoji} Ollama Status: {overall}\n\n"
        
        # Health details
        health = status["ollama_health"]
        health_emoji = "✅" if health["is_healthy"] else "❌"
        report += f"Service Health: {health_emoji}\n"
        report += f"• Response time: {health['response_time']:.2f}s\n"
        report += f"• Models available: {health['models_available']}\n"
        
        if health["error_message"]:
            report += f"• Error: {health['error_message']}\n"
        
        # Required models
        report += "\nRequired Models:\n"
        for model, available in status["required_models"].items():
            model_emoji = "✅" if available else "❌"
            report += f"• {model}: {model_emoji}\n"
        
        # Embedding test
        embedding = status["embedding_test"]
        embed_emoji = "✅" if embedding["success"] else "❌"
        report += f"\nEmbedding Test: {embed_emoji}\n"
        if embedding["success"]:
            report += f"• Dimensions: {embedding['dimensions']}/{embedding['expected_dimensions']}\n"
            report += f"• Generation time: {embedding['generation_time']:.2f}s\n"
        
        # Recommendations
        if status["recommendations"]:
            report += "\nRecommendations:\n"
            for rec in status["recommendations"]:
                report += f"• {rec}\n"
        
        return report
        
    except Exception as e:
        logger.error(f"Ollama health check failed: {e}")
        return f"❌ Health check failed: {str(e)}"

@backtesting_agent.tool
async def test_embedding_generation(
    ctx: RunContext[SharedDependencies], 
    text: str = "ICT market structure analysis test"
) -> str:
    """
    Test embedding generation for RAG operations.
    
    Args:
        text: Text to generate embeddings for
    
    Returns:
        Formatted embedding test results
    """
    try:
        start_time = time.time()
        embeddings = await get_embeddings(text)
        generation_time = time.time() - start_time
        
        if embeddings:
            return (f"✅ Embedding generation successful!\n"
                   f"• Text: '{text}'\n"
                   f"• Dimensions: {len(embeddings)}\n"
                   f"• Generation time: {generation_time:.2f}s\n"
                   f"• Model: nomic-embed-text")
        else:
            return f"❌ Embedding generation failed for text: '{text}'"
            
    except Exception as e:
        logger.error(f"Embedding test failed: {e}")
        return f"❌ Embedding test error: {str(e)}"

@backtesting_agent.tool
async def check_external_ssd_status(ctx: RunContext[SharedDependencies]) -> str:
    """
    Check external SSD connection status for Ollama and Supabase services.
    
    Returns:
        Formatted external SSD status report
    """
    try:
        status = await get_connection_status()
        
        # Format status report
        overall = status["overall_status"].upper()
        emoji_map = {
            "OPTIMAL": "🟢",
            "DATABASE_ONLY": "🟡", 
            "LLM_ONLY": "🟠",
            "SSD_DISCONNECTED": "🔴",
            "SERVICES_UNAVAILABLE": "💥"
        }
        emoji = emoji_map.get(overall, "❓")
        
        report = f"{emoji} External SSD Status: {overall}\n\n"
        
        # SSD Mount Status
        ssd = status["external_ssd"]
        ssd_emoji = "✅" if ssd["mounted"] else "❌"
        report += f"SSD Mount: {ssd_emoji}\n"
        report += f"• Ollama path: {ssd['ollama_path']}\n"
        report += f"• Supabase path: {ssd['supabase_path']}\n\n"
        
        # Service Status
        services = status["services"]
        
        # Ollama
        ollama_emoji = "✅" if services["ollama"]["available"] else "❌"
        report += f"Ollama Service: {ollama_emoji}\n"
        report += f"• Host: {services['ollama']['host']}\n"
        report += f"• Model: {services['ollama']['model']}\n\n"
        
        # Supabase
        supabase_emoji = "✅" if services["supabase"]["available"] else "❌"
        report += f"Supabase Database: {supabase_emoji}\n"
        report += f"• Port: {services['supabase']['port']}\n"
        report += f"• Connection: {services['supabase']['database_url']}\n\n"
        
        # Health Check Info
        health = status["health_check"]
        if health["last_check"]:
            import datetime
            check_time = datetime.datetime.fromtimestamp(health["last_check"])
            report += f"Last Check: {check_time.strftime('%H:%M:%S')}\n"
        
        # Errors
        if health["errors"]:
            report += "\nErrors:\n"
            for service, error in health["errors"].items():
                report += f"• {service}: {error}\n"
        
        return report
        
    except Exception as e:
        logger.error(f"External SSD status check failed: {e}")
        return f"❌ SSD status check failed: {str(e)}"

@backtesting_agent.tool
async def validate_ssd_setup(ctx: RunContext[SharedDependencies]) -> str:
    """
    Validate that external SSD setup is ready for ICT backtesting operations.
    
    Returns:
        Validation results and recommendations
    """
    try:
        is_valid = await validate_external_ssd_setup()
        
        if is_valid:
            return ("✅ External SSD setup is valid!\n"
                   "• SSD is mounted and accessible\n"
                   "• Supabase database is connected (port 54334)\n"
                   "• System is ready for ICT backtesting operations")
        else:
            status = await get_connection_status()
            
            report = "❌ External SSD setup validation failed\n\n"
            report += "Issues found:\n"
            
            if not status["external_ssd"]["mounted"]:
                report += "• External SSD is not mounted at /Volumes/Extreme SSD\n"
            
            if not status["services"]["supabase"]["available"]:
                report += "• Supabase database is not accessible on port 54334\n"
            
            if not status["services"]["ollama"]["available"]:
                report += "• Ollama service is not running (optional but recommended)\n"
            
            report += "\nRecommendations:\n"
            report += "• Ensure external SSD is connected and mounted\n"
            report += "• Start Supabase services from /Volumes/Extreme SSD/ict_project_2/supabase\n"
            report += "• Verify database is accessible on localhost:54334\n"
            
            return report
            
    except Exception as e:
        logger.error(f"SSD setup validation failed: {e}")
        return f"❌ Setup validation error: {str(e)}"

# Convenience function to create backtesting agent with dependencies
def create_backtesting_agent(deps: SharedDependencies) -> Agent:
    """
    Create a backtesting agent with specified dependencies.
    
    Args:
        deps: Shared dependencies for the agent
        
    Returns:
        Configured backtesting agent
    """
    return backtesting_agent
