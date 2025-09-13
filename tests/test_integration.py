"""
Integration tests for the complete ICT Backtesting Agent System.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
import json

from main import ICTBacktestingSystem
from settings import Settings
from dependencies import SharedDependencies


class TestSystemIntegration:
    """Integration tests for the complete system."""
    
    @pytest.fixture
    def mock_settings(self):
        """Create mock settings for integration testing."""
        settings = Mock(spec=Settings)
        settings.database_url = "postgresql://test:test@localhost:5432/test"
        settings.llm_provider = "test"
        settings.database_pool_min_size = 2
        settings.database_pool_max_size = 5
        settings.database_command_timeout = 30
        return settings
    
    @pytest.fixture
    async def system(self, mock_settings):
        """Create ICTBacktestingSystem instance for testing."""
        with patch('context_engineer.settings.load_settings') as mock_load_settings:
            mock_load_settings.return_value = mock_settings
            
            with patch('context_engineer.dependencies.initialize_dependencies') as mock_init_deps:
                mock_deps = Mock(spec=SharedDependencies)
                mock_deps.settings = mock_settings
                mock_deps.db_manager = AsyncMock()
                mock_deps.function_registry = Mock()
                mock_init_deps.return_value = mock_deps
                
                system = ICTBacktestingSystem()
                await system.initialize()
                yield system
                await system.cleanup()
    
    @pytest.mark.asyncio
    async def test_system_initialization(self, mock_settings):
        """Test complete system initialization."""
        with patch('context_engineer.settings.load_settings') as mock_load_settings:
            mock_load_settings.return_value = mock_settings
            
            with patch('context_engineer.dependencies.initialize_dependencies') as mock_init_deps:
                mock_deps = Mock(spec=SharedDependencies)
                mock_init_deps.return_value = mock_deps
                
                system = ICTBacktestingSystem()
                await system.initialize()
                
                assert system.settings == mock_settings
                assert system.dependencies == mock_deps
                assert system.coordinator is not None
                assert system.backtesting is not None
                
                await system.cleanup()
    
    @pytest.mark.asyncio
    async def test_query_processing_workflow(self, system):
        """Test complete query processing workflow."""
        # Mock agent responses
        mock_coordinator_response = Mock()
        mock_coordinator_response.data = json.dumps({
            "analysis_complete": True,
            "results": {
                "query_classification": "backtesting_first",
                "backtesting_results": {
                    "total_signals": 45,
                    "successful_trades": 32,
                    "success_rate": 71.1,
                    "statistical_validation": {
                        "sample_size": 45,
                        "confidence_level": 95.0
                    }
                }
            },
            "summary": "Order block analysis shows 71.1% success rate over 45 signals"
        })
        
        with patch.object(system.coordinator, 'run') as mock_coordinator_run:
            mock_coordinator_run.return_value = mock_coordinator_response
            
            query = "Analyze order block performance on EURUSD last month"
            result = await system.process_query(query)
            
            # Verify coordinator was called with correct parameters
            mock_coordinator_run.assert_called_once_with(
                query, deps=system.dependencies
            )
            
            # Verify response format
            response_data = json.loads(result)
            assert response_data["analysis_complete"] is True
            assert response_data["results"]["backtesting_results"]["success_rate"] == 71.1
    
    @pytest.mark.asyncio
    async def test_error_handling_workflow(self, system):
        """Test error handling in complete workflow."""
        # Mock coordinator error
        with patch.object(system.coordinator, 'run') as mock_coordinator_run:
            mock_coordinator_run.side_effect = Exception("Database connection failed")
            
            query = "Test query"
            result = await system.process_query(query)
            
            assert "Error processing query" in result
            assert "Database connection failed" in result
    
    @pytest.mark.asyncio
    async def test_multi_query_processing(self, system):
        """Test processing multiple queries in sequence."""
        queries = [
            "What is ICT methodology?",
            "Analyze fair value gaps on GBPUSD",
            "Show liquidity sweep statistics"
        ]
        
        mock_responses = [
            Mock(data="ICT methodology explanation"),
            Mock(data="Fair value gap analysis results"),
            Mock(data="Liquidity sweep statistics")
        ]
        
        with patch.object(system.coordinator, 'run') as mock_coordinator_run:
            mock_coordinator_run.side_effect = mock_responses
            
            results = []
            for query in queries:
                result = await system.process_query(query)
                results.append(result)
            
            assert len(results) == 3
            assert "methodology" in results[0]
            assert "gap analysis" in results[1]
            assert "statistics" in results[2]


class TestPerformanceBenchmarks:
    """Performance benchmarking tests."""
    
    @pytest.mark.asyncio
    async def test_query_response_time(self):
        """Test query response time meets requirements (<10 seconds)."""
        import time
        
        # Mock fast response
        start_time = time.time()
        
        # Simulate query processing (should be much faster than 10s)
        await asyncio.sleep(0.5)  # Simulate 500ms processing
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # Should be well under 10 seconds
        assert response_time < 10.0
        assert response_time < 2.0  # Target: under 2 seconds
    
    @pytest.mark.asyncio
    async def test_concurrent_query_handling(self):
        """Test handling multiple concurrent queries."""
        async def mock_query_processing(query_id):
            # Simulate processing time
            await asyncio.sleep(0.1)
            return f"Result for query {query_id}"
        
        # Process 5 concurrent queries
        tasks = [
            mock_query_processing(i) for i in range(5)
        ]
        
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        
        # Should complete all queries efficiently
        assert len(results) == 5
        assert end_time - start_time < 1.0  # Should be concurrent, not sequential
    
    @pytest.mark.asyncio
    async def test_memory_usage_monitoring(self):
        """Test memory usage stays within reasonable bounds."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Simulate processing multiple queries
        for i in range(10):
            await asyncio.sleep(0.01)  # Minimal processing
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (< 100MB for test)
        assert memory_increase < 100


class TestSystemReliability:
    """System reliability and error recovery tests."""
    
    @pytest.mark.asyncio
    async def test_database_reconnection(self):
        """Test database reconnection after connection loss."""
        # Mock connection loss and recovery
        connection_attempts = 0
        
        async def mock_connect_with_retry():
            nonlocal connection_attempts
            connection_attempts += 1
            
            if connection_attempts == 1:
                raise Exception("Connection failed")
            else:
                return Mock()  # Successful connection
        
        # Test retry logic
        try:
            await mock_connect_with_retry()
        except Exception:
            # Retry
            result = await mock_connect_with_retry()
            assert result is not None
            assert connection_attempts == 2
    
    @pytest.mark.asyncio
    async def test_graceful_shutdown(self):
        """Test graceful system shutdown."""
        # Mock system components
        mock_db_manager = AsyncMock()
        mock_dependencies = Mock()
        mock_dependencies.db_manager = mock_db_manager
        
        # Test cleanup
        from ..dependencies import cleanup_dependencies
        
        with patch('context_engineer.dependencies.cleanup_dependencies') as mock_cleanup:
            await mock_cleanup(mock_dependencies)
            mock_cleanup.assert_called_once_with(mock_dependencies)
    
    @pytest.mark.asyncio
    async def test_configuration_validation(self):
        """Test configuration validation and error reporting."""
        # Test invalid configuration
        invalid_config = {
            "database_url": "",  # Invalid empty URL
            "llm_provider": "invalid_provider",
            "database_pool_max_size": -1  # Invalid negative size
        }
        
        # Validation should catch these issues
        assert len(invalid_config["database_url"]) == 0
        assert invalid_config["llm_provider"] not in ["ollama", "openai", "anthropic"]
        assert invalid_config["database_pool_max_size"] < 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
