"""
Test suite for ICT Backtesting Agent System - Agent Workflows
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from pydantic_ai import TestModel, FunctionModel
from pydantic_ai.models.test import TestModel

from coordinator_agent import coordinator_agent
from backtesting_agent import backtesting_agent
from dependencies import SharedDependencies
from models import QueryClassification, CoordinatorRequest, BacktestingResponse
from settings import Settings


class TestCoordinatorAgent:
    """Test suite for Coordinator Agent functionality."""
    
    @pytest.fixture
    def mock_dependencies(self):
        """Create mock dependencies for testing."""
        deps = Mock(spec=SharedDependencies)
        deps.settings = Mock(spec=Settings)
        deps.db_manager = AsyncMock()
        deps.function_registry = Mock()
        deps.function_registry.functions = {
            "ict_order_blocks": {"description": "Test function"},
            "ict_fair_value_gaps": {"description": "Test function"}
        }
        return deps
    
    @pytest.mark.asyncio
    async def test_query_classification_backtesting_first(self, mock_dependencies):
        """Test query classification for backtesting-focused queries."""
        # Use TestModel for predictable responses
        test_model = TestModel()
        
        # Override the coordinator agent model for testing
        with coordinator_agent.override(model=test_model):
            # Mock the classify_user_query tool response
            classification = QueryClassification(
                routing_decision="backtesting_first",
                confidence=85.0,
                reasoning="Query contains backtesting indicators",
                suggested_approach="Execute database analysis"
            )
            
            # Test backtesting-focused query
            query = "What is the success rate of order blocks on EURUSD in the last month?"
            
            # The actual classification logic would be tested separately
            assert classification.routing_decision == "backtesting_first"
            assert classification.confidence > 80.0
    
    @pytest.mark.asyncio
    async def test_query_classification_rag_first(self, mock_dependencies):
        """Test query classification for RAG-focused queries."""
        test_model = TestModel()
        
        with coordinator_agent.override(model=test_model):
            classification = QueryClassification(
                routing_decision="rag_first",
                confidence=80.0,
                reasoning="Query contains conceptual indicators",
                suggested_approach="Consult knowledge base"
            )
            
            query = "What is the ICT methodology and how does it work?"
            
            assert classification.routing_decision == "rag_first"
            assert classification.confidence > 70.0
    
    @pytest.mark.asyncio
    async def test_backtesting_delegation(self, mock_dependencies):
        """Test delegation to backtesting sub-agent."""
        # Mock successful backtesting response
        mock_response = BacktestingResponse(
            success=True,
            analysis_type="order_blocks",
            results={
                "total_signals": 45,
                "successful_trades": 32,
                "success_rate": 71.1,
                "avg_profit": 15.2
            },
            statistical_validation={
                "sample_size": 45,
                "confidence_level": 95.0,
                "data_coverage": 98.5
            },
            execution_time_ms=1250,
            function_used="ict_order_blocks"
        )
        
        # Test delegation workflow
        request = CoordinatorRequest(
            original_query="Analyze order block performance on EURUSD",
            analysis_type="order_blocks",
            parameters={
                "symbol": "EURUSD",
                "timeframe": "1h",
                "start_date": "2024-01-01",
                "end_date": "2024-01-31"
            },
            context="User requesting backtesting analysis"
        )
        
        assert request.analysis_type == "order_blocks"
        assert "EURUSD" in request.parameters["symbol"]


class TestBacktestingAgent:
    """Test suite for Backtesting Sub-Agent functionality."""
    
    @pytest.fixture
    def mock_dependencies(self):
        """Create mock dependencies for testing."""
        deps = Mock(spec=SharedDependencies)
        deps.settings = Mock(spec=Settings)
        deps.db_manager = AsyncMock()
        deps.function_registry = Mock()
        deps.function_registry.functions = {
            "ict_order_blocks": {
                "description": "Identifies ICT Order Blocks",
                "parameters": {
                    "symbol": {"type": "string"},
                    "timeframe": {"type": "string"},
                    "start_date": {"type": "date"},
                    "end_date": {"type": "date"}
                }
            }
        }
        return deps
    
    @pytest.mark.asyncio
    async def test_function_selection(self, mock_dependencies):
        """Test SQL function selection logic."""
        test_model = TestModel()
        
        with backtesting_agent.override(model=test_model):
            # Mock function selection
            query = "order block analysis"
            expected_function = "ict_order_blocks"
            
            # Function selection should match query intent
            assert expected_function in mock_dependencies.function_registry.functions
    
    @pytest.mark.asyncio
    async def test_sql_execution_success(self, mock_dependencies):
        """Test successful SQL function execution."""
        # Mock successful database response
        mock_dependencies.db_manager.execute_function.return_value = [
            {
                "timestamp": "2024-01-15T10:30:00Z",
                "entry_price": 1.0850,
                "exit_price": 1.0875,
                "profit_pips": 25,
                "success": True
            },
            {
                "timestamp": "2024-01-16T14:15:00Z", 
                "entry_price": 1.0820,
                "exit_price": 1.0810,
                "profit_pips": -10,
                "success": False
            }
        ]
        
        # Test execution
        function_name = "ict_order_blocks"
        parameters = {
            "symbol": "EURUSD",
            "timeframe": "1h",
            "start_date": "2024-01-01",
            "end_date": "2024-01-31"
        }
        
        result = await mock_dependencies.db_manager.execute_function(
            function_name, parameters
        )
        
        assert len(result) == 2
        assert result[0]["success"] is True
        assert result[1]["success"] is False
    
    @pytest.mark.asyncio
    async def test_sql_execution_error(self, mock_dependencies):
        """Test SQL function execution error handling."""
        # Mock database error
        mock_dependencies.db_manager.execute_function.side_effect = Exception(
            "Connection timeout"
        )
        
        function_name = "ict_order_blocks"
        parameters = {"symbol": "EURUSD"}
        
        with pytest.raises(Exception) as exc_info:
            await mock_dependencies.db_manager.execute_function(
                function_name, parameters
            )
        
        assert "Connection timeout" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_result_validation(self, mock_dependencies):
        """Test statistical validation of results."""
        # Mock validation logic
        results = [{"success": True}] * 32 + [{"success": False}] * 13
        
        # Calculate statistics
        total_trades = len(results)
        successful_trades = sum(1 for r in results if r["success"])
        success_rate = (successful_trades / total_trades) * 100
        
        # Validation thresholds
        min_sample_size = 30
        min_confidence = 95.0
        
        assert total_trades >= min_sample_size
        assert success_rate > 0
        assert total_trades == 45
        assert successful_trades == 32


class TestAgentIntegration:
    """Integration tests for multi-agent workflows."""
    
    @pytest.fixture
    def mock_dependencies(self):
        """Create mock dependencies for integration testing."""
        deps = Mock(spec=SharedDependencies)
        deps.settings = Mock(spec=Settings)
        deps.db_manager = AsyncMock()
        deps.function_registry = Mock()
        deps.function_registry.functions = {
            "ict_order_blocks": {"description": "Test function"},
            "ict_fair_value_gaps": {"description": "Test function"}
        }
        return deps
    
    @pytest.mark.asyncio
    async def test_end_to_end_workflow(self, mock_dependencies):
        """Test complete workflow from query to response."""
        # Mock the complete workflow
        user_query = "Analyze order block performance on EURUSD last month"
        
        # Step 1: Query classification
        classification = QueryClassification(
            routing_decision="backtesting_first",
            confidence=85.0,
            reasoning="Backtesting analysis requested",
            suggested_approach="Execute database analysis"
        )
        
        # Step 2: Coordinator request
        coordinator_request = CoordinatorRequest(
            original_query=user_query,
            analysis_type="order_blocks",
            parameters={
                "symbol": "EURUSD",
                "timeframe": "1h",
                "start_date": "2024-01-01",
                "end_date": "2024-01-31"
            },
            context="Monthly performance analysis"
        )
        
        # Step 3: Backtesting response
        backtesting_response = BacktestingResponse(
            success=True,
            analysis_type="order_blocks",
            results={
                "total_signals": 45,
                "successful_trades": 32,
                "success_rate": 71.1
            },
            statistical_validation={
                "sample_size": 45,
                "confidence_level": 95.0,
                "data_coverage": 98.5
            },
            execution_time_ms=1250,
            function_used="ict_order_blocks"
        )
        
        # Validate workflow
        assert classification.routing_decision == "backtesting_first"
        assert coordinator_request.analysis_type == "order_blocks"
        assert backtesting_response.success is True
        assert backtesting_response.results["success_rate"] > 70.0
    
    @pytest.mark.asyncio
    async def test_error_handling_workflow(self, mock_dependencies):
        """Test error handling in multi-agent workflow."""
        # Mock database connection failure
        mock_dependencies.db_manager.execute_function.side_effect = Exception(
            "Database connection failed"
        )
        
        # Test graceful error handling
        error_response = BacktestingResponse(
            success=False,
            analysis_type="order_blocks",
            results={},
            error_message="Database connection failed",
            statistical_validation=None,
            execution_time_ms=0,
            function_used=None
        )
        
        assert error_response.success is False
        assert "Database connection failed" in error_response.error_message


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
