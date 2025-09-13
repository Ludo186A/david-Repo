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
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

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
