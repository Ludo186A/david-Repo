#!/usr/bin/env python3
"""
Test script for external SSD integration with Ollama and Supabase services.
Validates the complete setup and connection management functionality.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from connection_manager import connection_manager, validate_external_ssd_setup, get_connection_status
from settings import load_settings
from dependencies import SharedDependencies
from backtesting_agent import backtesting_agent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_ssd_connection_manager():
    """Test the external SSD connection manager functionality."""
    print("\n🔍 Testing External SSD Connection Manager")
    print("=" * 50)
    
    try:
        # Initialize connection manager
        await connection_manager.initialize()
        
        # Test SSD mount detection
        print("\n1. Testing SSD Mount Detection:")
        ssd_mounted = connection_manager.check_ssd_mounted()
        print(f"   SSD Mounted: {'✅' if ssd_mounted else '❌'}")
        
        # Test individual service health checks
        print("\n2. Testing Individual Service Health:")
        
        # Ollama health check
        ollama_healthy = await connection_manager.check_ollama_health()
        print(f"   Ollama Service: {'✅' if ollama_healthy else '❌'}")
        
        # Supabase health check
        supabase_healthy = await connection_manager.check_supabase_health()
        print(f"   Supabase Database: {'✅' if supabase_healthy else '❌'}")
        
        # Full health check
        print("\n3. Full Health Check:")
        status = await connection_manager.full_health_check()
        print(f"   Overall Status: {status.ssd_mounted and status.supabase_available}")
        
        if status.error_messages:
            print("   Errors:")
            for service, error in status.error_messages.items():
                print(f"     • {service}: {error}")
        
        # Detailed service status
        print("\n4. Detailed Service Status:")
        service_status = await connection_manager.get_service_status()
        overall_status = service_status["overall_status"]
        print(f"   Overall Status: {overall_status.upper()}")
        
        return status.ssd_mounted and status.supabase_available
        
    except Exception as e:
        logger.error(f"Connection manager test failed: {e}")
        return False
    finally:
        await connection_manager.cleanup()


async def test_backtesting_agent_tools():
    """Test the backtesting agent SSD management tools."""
    print("\n🤖 Testing Backtesting Agent SSD Tools")
    print("=" * 50)
    
    try:
        # Load settings and create dependencies
        settings = load_settings()
        deps = SharedDependencies(settings=settings)
        
        # Test external SSD status tool
        print("\n1. Testing External SSD Status Tool:")
        status_result = await backtesting_agent.run(
            "Check the external SSD status",
            deps=deps
        )
        print("   Result:")
        print("   " + "\n   ".join(status_result.data.split("\n")))
        
        # Test SSD setup validation tool
        print("\n2. Testing SSD Setup Validation Tool:")
        validation_result = await backtesting_agent.run(
            "Validate the external SSD setup for ICT backtesting",
            deps=deps
        )
        print("   Result:")
        print("   " + "\n   ".join(validation_result.data.split("\n")))
        
        return True
        
    except Exception as e:
        logger.error(f"Backtesting agent tools test failed: {e}")
        return False


async def test_database_connection():
    """Test direct database connection to Supabase on external SSD."""
    print("\n💾 Testing Direct Database Connection")
    print("=" * 50)
    
    try:
        import asyncpg
        settings = load_settings()
        
        print(f"\n1. Connecting to: {settings.database_url}")
        
        # Test connection
        conn = await asyncpg.connect(settings.database_url)
        
        # Test basic query
        result = await conn.fetchval("SELECT version()")
        print(f"   PostgreSQL Version: {result[:50]}...")
        
        # Test table existence (if any)
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            LIMIT 5
        """)
        
        if tables:
            print(f"   Found {len(tables)} tables:")
            for table in tables[:3]:
                print(f"     • {table['table_name']}")
        else:
            print("   No tables found (fresh database)")
        
        await conn.close()
        print("   ✅ Database connection successful!")
        return True
        
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        print(f"   ❌ Database connection failed: {e}")
        return False


async def test_ollama_integration():
    """Test Ollama service integration."""
    print("\n🦙 Testing Ollama Integration")
    print("=" * 50)
    
    try:
        import httpx
        settings = load_settings()
        
        print(f"\n1. Testing Ollama API at: {settings.ollama_host}")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Test API availability
            response = await client.get(f"{settings.ollama_host}/api/tags")
            
            if response.status_code == 200:
                models = response.json()
                print(f"   ✅ Ollama API accessible")
                print(f"   Available models: {len(models.get('models', []))}")
                
                for model in models.get('models', [])[:3]:
                    print(f"     • {model.get('name', 'Unknown')}")
                
                return True
            else:
                print(f"   ❌ Ollama API returned status {response.status_code}")
                return False
                
    except Exception as e:
        logger.error(f"Ollama integration test failed: {e}")
        print(f"   ❌ Ollama integration failed: {e}")
        return False


async def run_comprehensive_test():
    """Run comprehensive test suite for external SSD integration."""
    print("🚀 External SSD Integration Test Suite")
    print("=" * 60)
    
    test_results = {}
    
    # Test 1: SSD Connection Manager
    test_results["connection_manager"] = await test_ssd_connection_manager()
    
    # Test 2: Database Connection
    test_results["database"] = await test_database_connection()
    
    # Test 3: Ollama Integration
    test_results["ollama"] = await test_ollama_integration()
    
    # Test 4: Backtesting Agent Tools
    test_results["agent_tools"] = await test_backtesting_agent_tools()
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 30)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! External SSD integration is working correctly.")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above for details.")
        return False


if __name__ == "__main__":
    try:
        success = asyncio.run(run_comprehensive_test())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Test suite failed: {e}")
        print(f"\n💥 Test suite crashed: {e}")
        sys.exit(1)
