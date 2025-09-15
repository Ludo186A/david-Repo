#!/usr/bin/env python3
"""
Simple test script for external SSD integration without full agent dependencies.
Tests core connection functionality for Ollama and Supabase services.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_ssd_mount():
    """Test if external SSD is properly mounted."""
    print("🔍 Testing External SSD Mount")
    print("-" * 30)
    
    try:
        ssd_path = Path("/Volumes/Extreme SSD")
        ollama_path = Path("/Volumes/Extreme SSD/ollama")
        supabase_path = Path("/Volumes/Extreme SSD/ict_project_2/supabase")
        
        # Check SSD mount
        ssd_mounted = ssd_path.exists() and ssd_path.is_mount()
        print(f"SSD Mount: {'✅' if ssd_mounted else '❌'}")
        
        # Check paths
        ollama_exists = ollama_path.exists()
        supabase_exists = supabase_path.exists()
        
        print(f"Ollama Path: {'✅' if ollama_exists else '❌'} ({ollama_path})")
        print(f"Supabase Path: {'✅' if supabase_exists else '❌'} ({supabase_path})")
        
        return ssd_mounted and ollama_exists and supabase_exists
        
    except Exception as e:
        print(f"❌ SSD mount test failed: {e}")
        return False


async def test_supabase_connection():
    """Test Supabase database connection."""
    print("\n💾 Testing Supabase Connection")
    print("-" * 30)
    
    try:
        import asyncpg
        
        # Database connection string
        db_url = "postgresql://postgres:postgres@localhost:54334/postgres"
        print(f"Connecting to: {db_url}")
        
        # Test connection
        conn = await asyncpg.connect(db_url)
        
        # Test basic query
        version = await conn.fetchval("SELECT version()")
        print(f"✅ Connected! PostgreSQL: {version.split(',')[0]}")
        
        # Test schema access
        result = await conn.fetchval("SELECT current_database()")
        print(f"✅ Database: {result}")
        
        await conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False


async def test_ollama_service():
    """Test Ollama service availability."""
    print("\n🦙 Testing Ollama Service")
    print("-" * 30)
    
    try:
        import httpx
        
        ollama_host = "http://localhost:11434"
        print(f"Testing Ollama at: {ollama_host}")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Test API availability
            response = await client.get(f"{ollama_host}/api/tags")
            
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                
                print(f"✅ Ollama API accessible")
                print(f"✅ Available models: {len(models)}")
                
                for model in models[:3]:
                    name = model.get('name', 'Unknown')
                    size = model.get('size', 0)
                    size_mb = size / (1024 * 1024) if size else 0
                    print(f"   • {name} ({size_mb:.1f} MB)")
                
                return True
            else:
                print(f"❌ Ollama API returned status {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Ollama service test failed: {e}")
        return False


async def test_connection_manager():
    """Test the connection manager module directly."""
    print("\n🔧 Testing Connection Manager")
    print("-" * 30)
    
    try:
        # Add current directory to path
        sys.path.insert(0, str(Path(__file__).parent))
        
        from connection_manager import connection_manager
        
        # Initialize
        await connection_manager.initialize()
        
        # Test SSD check
        ssd_ok = connection_manager.check_ssd_mounted()
        print(f"SSD Mount Check: {'✅' if ssd_ok else '❌'}")
        
        # Test service health checks
        ollama_ok = await connection_manager.check_ollama_health()
        print(f"Ollama Health: {'✅' if ollama_ok else '❌'}")
        
        supabase_ok = await connection_manager.check_supabase_health()
        print(f"Supabase Health: {'✅' if supabase_ok else '❌'}")
        
        # Full health check
        status = await connection_manager.full_health_check()
        overall_status = connection_manager._get_overall_status()
        print(f"Overall Status: {overall_status.upper()}")
        
        # Show any errors
        if status.error_messages:
            print("Errors:")
            for service, error in status.error_messages.items():
                print(f"  • {service}: {error}")
        
        await connection_manager.cleanup()
        return ssd_ok and supabase_ok
        
    except Exception as e:
        print(f"❌ Connection manager test failed: {e}")
        return False


async def run_simple_tests():
    """Run simplified test suite."""
    print("🚀 External SSD Simple Test Suite")
    print("=" * 40)
    
    tests = [
        ("SSD Mount", test_ssd_mount()),
        ("Supabase Connection", test_supabase_connection()),
        ("Ollama Service", test_ollama_service()),
        ("Connection Manager", test_connection_manager())
    ]
    
    results = {}
    for test_name, test_coro in tests:
        try:
            results[test_name] = await test_coro
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n📊 Test Results")
    print("=" * 20)
    
    passed = 0
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    total = len(results)
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! External SSD integration is working!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
    
    return passed == total


if __name__ == "__main__":
    try:
        success = asyncio.run(run_simple_tests())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test suite crashed: {e}")
        sys.exit(1)
