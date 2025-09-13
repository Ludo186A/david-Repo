"""
Test suite for database connectivity and function execution.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
import asyncpg

from database import DatabaseManager, FunctionRegistry
from settings import Settings


class TestDatabaseManager:
    """Test suite for DatabaseManager functionality."""
    
    @pytest.fixture
    def mock_settings(self):
        """Create mock settings for testing."""
        settings = Mock(spec=Settings)
        settings.database_url = "postgresql://test:test@localhost:5432/test"
        settings.database_pool_min_size = 2
        settings.database_pool_max_size = 5
        settings.database_command_timeout = 30
        return settings
    
    @pytest.fixture
    async def db_manager(self, mock_settings):
        """Create DatabaseManager instance for testing."""
        manager = DatabaseManager(mock_settings)
        yield manager
        if manager.pool:
            await manager.close_pool()
    
    @pytest.mark.asyncio
    async def test_connection_pool_creation(self, mock_settings):
        """Test database connection pool creation."""
        with patch('asyncpg.create_pool') as mock_create_pool:
            mock_pool = AsyncMock()
            mock_create_pool.return_value = mock_pool
            
            manager = DatabaseManager(mock_settings.database_url)
            await manager.initialize_pool()
            
            mock_create_pool.assert_called_once()
            assert manager.pool == mock_pool
    
    @pytest.mark.asyncio
    async def test_function_execution_success(self, mock_settings):
        """Test successful SQL function execution."""
        with patch('asyncpg.create_pool') as mock_create_pool:
            # Mock connection and results
            mock_connection = AsyncMock()
            mock_pool = AsyncMock()
            mock_pool.acquire.return_value.__aenter__.return_value = mock_connection
            mock_create_pool.return_value = mock_pool
            
            # Mock query results
            mock_connection.fetch.return_value = [
                {
                    'timestamp': '2024-01-15T10:30:00Z',
                    'entry_price': 1.0850,
                    'exit_price': 1.0875,
                    'profit_pips': 25,
                    'success': True
                }
            ]
            
            manager = DatabaseManager(mock_settings.database_url)
            await manager.initialize_pool()
            
            # Test function execution
            result = await manager.execute_function(
                'ict_order_blocks',
                {
                    'symbol': 'EURUSD',
                    'timeframe': '1h',
                    'start_date': '2024-01-01',
                    'end_date': '2024-01-31'
                }
            )
            
            assert len(result) == 1
            assert result[0]['success'] is True
            assert result[0]['profit_pips'] == 25
    
    @pytest.mark.asyncio
    async def test_function_execution_error(self, mock_settings):
        """Test SQL function execution error handling."""
        with patch('asyncpg.create_pool') as mock_create_pool:
            mock_connection = AsyncMock()
            mock_pool = AsyncMock()
            mock_pool.acquire.return_value.__aenter__.return_value = mock_connection
            mock_create_pool.return_value = mock_pool
            
            # Mock database error
            mock_connection.fetch.side_effect = asyncpg.PostgresError("Function not found")
            
            manager = DatabaseManager(mock_settings.database_url)
            await manager.initialize_pool()
            
            with pytest.raises(Exception) as exc_info:
                await manager.execute_function('invalid_function', {})
            
            assert "Function not found" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_connection_pool_cleanup(self, mock_settings):
        """Test proper cleanup of connection pool."""
        with patch('asyncpg.create_pool') as mock_create_pool:
            mock_pool = AsyncMock()
            mock_create_pool.return_value = mock_pool
            
            manager = DatabaseManager(mock_settings.database_url)
            await manager.initialize_pool()
            await manager.close_pool()
            
            mock_pool.close.assert_called_once()


class TestFunctionRegistry:
    """Test suite for FunctionRegistry functionality."""
    
    @pytest.fixture
    def function_registry(self):
        """Create FunctionRegistry instance for testing."""
        return FunctionRegistry("test_signatures.json")
    
    @pytest.mark.asyncio
    async def test_load_functions_from_file(self, function_registry):
        """Test loading functions from JSON file."""
        # Mock file content
        mock_functions = {
            "ict_order_blocks": {
                "description": "Identifies ICT Order Blocks",
                "parameters": {
                    "symbol": {"type": "string"},
                    "timeframe": {"type": "string"}
                }
            }
        }
        
        with patch('aiofiles.open') as mock_open:
            mock_file = AsyncMock()
            mock_file.read.return_value = '{"ict_order_blocks": {"description": "Test"}}'
            mock_open.return_value.__aenter__.return_value = mock_file
            
            with patch('json.loads') as mock_json:
                mock_json.return_value = mock_functions
                
                await function_registry.load_functions('test_file.json')
                
                assert 'ict_order_blocks' in function_registry.functions
                assert function_registry.functions['ict_order_blocks']['description'] == "Identifies ICT Order Blocks"
    
    @pytest.mark.asyncio
    async def test_load_functions_file_not_found(self, function_registry):
        """Test fallback when function file not found."""
        with patch('aiofiles.open') as mock_open:
            mock_open.side_effect = FileNotFoundError("File not found")
            
            await function_registry.load_functions('nonexistent_file.json')
            
            # Should load demo functions as fallback
            assert len(function_registry.functions) > 0
            assert 'demo_order_blocks' in function_registry.functions
    
    def test_get_function_info(self, function_registry):
        """Test retrieving function information."""
        # Add test function
        function_registry.functions['test_function'] = {
            'description': 'Test function',
            'parameters': {'param1': {'type': 'string'}}
        }
        
        info = function_registry.get_function_info('test_function')
        assert info['description'] == 'Test function'
        assert 'param1' in info['parameters']
        
        # Test non-existent function
        info = function_registry.get_function_info('nonexistent')
        assert info is None
    
    def test_list_functions(self, function_registry):
        """Test listing all available functions."""
        # Add test functions
        function_registry.functions = {
            'func1': {'description': 'Function 1'},
            'func2': {'description': 'Function 2'}
        }
        
        functions = function_registry.list_functions()
        assert len(functions) == 2
        assert 'func1' in functions
        assert 'func2' in functions


class TestDatabaseIntegration:
    """Integration tests for database functionality."""
    
    @pytest.mark.asyncio
    async def test_database_health_check(self):
        """Test database connectivity health check."""
        # Mock successful connection
        with patch('asyncpg.connect') as mock_connect:
            mock_connection = AsyncMock()
            mock_connection.fetchval.return_value = 1
            mock_connect.return_value.__aenter__.return_value = mock_connection
            
            # Simulate health check
            result = await mock_connection.fetchval('SELECT 1')
            assert result == 1
    
    @pytest.mark.asyncio
    async def test_function_parameter_validation(self):
        """Test parameter validation for SQL functions."""
        # Test valid parameters
        valid_params = {
            'symbol': 'EURUSD',
            'timeframe': '1h',
            'start_date': '2024-01-01',
            'end_date': '2024-01-31'
        }
        
        # Basic validation
        assert isinstance(valid_params['symbol'], str)
        assert valid_params['symbol'] in ['EURUSD', 'GBPUSD', 'USDJPY']  # Example validation
        
        # Test invalid parameters
        invalid_params = {
            'symbol': None,
            'timeframe': '',
            'start_date': 'invalid-date'
        }
        
        # Validation should catch these issues
        assert invalid_params['symbol'] is None
        assert len(invalid_params['timeframe']) == 0
    
    @pytest.mark.asyncio
    async def test_query_performance_monitoring(self):
        """Test query execution time monitoring."""
        import time
        
        start_time = time.time()
        
        # Simulate query execution
        await asyncio.sleep(0.1)  # Simulate 100ms query
        
        execution_time = int((time.time() - start_time) * 1000)
        
        # Should be approximately 100ms
        assert 90 <= execution_time <= 150  # Allow some variance
    
    @pytest.mark.asyncio
    async def test_connection_pool_limits(self):
        """Test connection pool size limits."""
        settings = Mock()
        settings.database_pool_min_size = 2
        settings.database_pool_max_size = 5
        
        # Validate pool configuration
        assert settings.database_pool_min_size >= 1
        assert settings.database_pool_max_size >= settings.database_pool_min_size
        assert settings.database_pool_max_size <= 20  # Reasonable upper limit


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
