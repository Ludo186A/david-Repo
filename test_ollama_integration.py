"""
Test script for Ollama integration with ICT backtesting system.
"""

import asyncio
import logging
from backtesting_agent import backtesting_agent
from dependencies import create_shared_dependencies
from ollama_health import check_ollama_status, validate_ollama_setup
from embedding_service import validate_embedding_setup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_ollama_integration():
    """Test complete Ollama integration with ICT backtesting system."""
    
    print("🧪 Testing Ollama Integration with ICT Backtesting System\n")
    
    # Test 1: Ollama Health Check
    print("1️⃣ Testing Ollama Health Check...")
    try:
        deps = create_shared_dependencies()
        health_result = await backtesting_agent.run(
            "Check Ollama health status",
            deps=deps
        )
        print(health_result.output)
        print()
    except Exception as e:
        print(f"❌ Health check failed: {e}\n")
    
    # Test 2: Embedding Generation
    print("2️⃣ Testing Embedding Generation...")
    try:
        deps = create_shared_dependencies()
        embedding_result = await backtesting_agent.run(
            "Test embedding generation for ICT market analysis",
            deps=deps
        )
        print(embedding_result.output)
        print()
    except Exception as e:
        print(f"❌ Embedding test failed: {e}\n")
    
    # Test 3: System Validation
    print("3️⃣ Testing System Validation...")
    try:
        ollama_valid = await validate_ollama_setup()
        embedding_valid = await validate_embedding_setup()
        
        print(f"Ollama Setup Valid: {'✅' if ollama_valid else '❌'}")
        print(f"Embedding Setup Valid: {'✅' if embedding_valid else '❌'}")
        
        if ollama_valid and embedding_valid:
            print("🟢 System is ready for ICT backtesting with Ollama!")
        else:
            print("🟡 System needs configuration adjustments")
        print()
    except Exception as e:
        print(f"❌ System validation failed: {e}\n")
    
    # Test 4: Sample Backtesting Request
    print("4️⃣ Testing Sample Backtesting Request...")
    try:
        deps = create_shared_dependencies()
        sample_request = {
            "analysis_strategy": "performance_analysis",
            "trading_context": "swing_trading",
            "quality_requirements": "balanced",
            "symbol": "eurusd",
            "timeframe": "4h"
        }
        
        import json
        result = await backtesting_agent.run(
            f"Process this backtesting request: {json.dumps(sample_request)}",
            deps=deps
        )
        print("Sample backtesting request processed successfully!")
        print(f"Response length: {len(result.output)} characters")
        print()
    except Exception as e:
        print(f"❌ Backtesting request failed: {e}\n")
    
    print("✅ Ollama integration testing completed!")


if __name__ == "__main__":
    asyncio.run(test_ollama_integration())
