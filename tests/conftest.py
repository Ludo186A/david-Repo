"""
Pytest configuration and shared fixtures for ICT Backtesting Agent System tests.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
import os
import sys

# Add the parent directory to the Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from settings import Settings
    from dependencies import SharedDependencies
    from database import DatabaseManager, FunctionRegistry
except ImportError:
    # Fallback for when running tests from different directory
    import sys
    import os
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    from settings import Settings
    from dependencies import SharedDependencies
    from database import DatabaseManager, FunctionRegistry


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_settings():
    """Create mock settings for testing."""
    settings = Mock(spec=Settings)
    settings.database_url = "postgresql://test:test@localhost:5432/test"
    settings.database_pool_min_size = 2
    settings.database_pool_max_size = 5
    settings.database_command_timeout = 30
    settings.llm_provider = "test"
    settings.log_level = "INFO"
    settings.debug_mode = False
    return settings


@pytest.fixture
def mock_db_manager():
    """Create mock database manager for testing."""
    manager = AsyncMock(spec=DatabaseManager)
    manager.pool = AsyncMock()
    manager.execute_function = AsyncMock()
    manager.initialize = AsyncMock()
    manager.close = AsyncMock()
    return manager


@pytest.fixture
def mock_function_registry():
    """Create mock function registry for testing."""
    registry = Mock(spec=FunctionRegistry)
    registry.functions = {
        "ict_order_blocks": {
            "description": "Identifies ICT Order Blocks",
            "parameters": {
                "symbol": {"type": "string"},
                "timeframe": {"type": "string"},
                "start_date": {"type": "date"},
                "end_date": {"type": "date"}
            }
        },
        "ict_fair_value_gaps": {
            "description": "Detects Fair Value Gaps",
            "parameters": {
                "symbol": {"type": "string"},
                "timeframe": {"type": "string"},
                "start_date": {"type": "date"},
                "end_date": {"type": "date"}
            }
        }
    }
    registry.load_functions = AsyncMock()
    registry.get_function_info = Mock()
    registry.list_functions = Mock(return_value=list(registry.functions.keys()))
    return registry


@pytest.fixture
def mock_dependencies(mock_settings, mock_db_manager, mock_function_registry):
    """Create mock shared dependencies for testing."""
    deps = Mock(spec=SharedDependencies)
    deps.settings = mock_settings
    deps.db_manager = mock_db_manager
    deps.function_registry = mock_function_registry
    return deps


@pytest.fixture
def sample_ohlcv_data():
    """Sample OHLCV data for testing."""
    return [
        {
            "timestamp": "2024-01-15T10:30:00Z",
            "open": 1.0845,
            "high": 1.0875,
            "low": 1.0840,
            "close": 1.0870,
            "volume": 1250000
        },
        {
            "timestamp": "2024-01-15T11:30:00Z",
            "open": 1.0870,
            "high": 1.0885,
            "low": 1.0860,
            "close": 1.0865,
            "volume": 980000
        },
        {
            "timestamp": "2024-01-15T12:30:00Z",
            "open": 1.0865,
            "high": 1.0880,
            "low": 1.0850,
            "close": 1.0855,
            "volume": 1100000
        }
    ]


@pytest.fixture
def sample_backtesting_results():
    """Sample backtesting results for testing."""
    return {
        "total_signals": 45,
        "successful_trades": 32,
        "failed_trades": 13,
        "success_rate": 71.1,
        "total_profit_pips": 485,
        "total_loss_pips": -165,
        "net_profit_pips": 320,
        "avg_profit_per_trade": 15.2,
        "max_drawdown": -45,
        "profit_factor": 2.94,
        "sharpe_ratio": 1.85
    }


@pytest.fixture
def sample_ict_patterns():
    """Sample ICT pattern data for testing."""
    return {
        "order_blocks": [
            {
                "timestamp": "2024-01-15T10:30:00Z",
                "type": "bullish",
                "entry_price": 1.0850,
                "stop_loss": 1.0830,
                "take_profit": 1.0890,
                "success": True,
                "profit_pips": 40
            },
            {
                "timestamp": "2024-01-15T14:15:00Z",
                "type": "bearish",
                "entry_price": 1.0820,
                "stop_loss": 1.0840,
                "take_profit": 1.0780,
                "success": False,
                "profit_pips": -20
            }
        ],
        "fair_value_gaps": [
            {
                "timestamp": "2024-01-16T09:00:00Z",
                "gap_start": 1.0865,
                "gap_end": 1.0875,
                "gap_size_pips": 10,
                "filled": True,
                "fill_time": "2024-01-16T11:30:00Z"
            }
        ],
        "liquidity_sweeps": [
            {
                "timestamp": "2024-01-17T08:30:00Z",
                "sweep_level": 1.0800,
                "direction": "upward",
                "success": True,
                "follow_through_pips": 25
            }
        ]
    }


# Test markers for different test categories
pytest_plugins = []

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as a performance test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


# Async test configuration
@pytest.fixture(autouse=True)
def setup_async_test():
    """Setup for async tests."""
    # Ensure clean state for each test
    pass
