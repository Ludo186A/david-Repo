"""
Main entry point for ICT Backtesting Agent System.
Initializes both agents and provides CLI interface.
"""

import asyncio
import logging
import sys
from typing import Optional

from settings import load_settings
from dependencies import initialize_dependencies, cleanup_dependencies
from coordinator_agent import coordinator_agent
from backtesting_agent import backtesting_agent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ICTBacktestingSystem:
    """Main system orchestrator for ICT backtesting agents."""
    
    def __init__(self):
        self.settings = None
        self.dependencies = None
        self.coordinator = None
        self.backtesting = None
    
    async def initialize(self):
        """Initialize the complete system."""
        try:
            logger.info("Initializing ICT Backtesting Agent System...")
            
            # Load configuration
            self.settings = load_settings()
            logger.info(f"Configuration loaded - Provider: {self.settings.llm_provider}")
            
            # Initialize shared dependencies
            self.dependencies = await initialize_dependencies(self.settings)
            logger.info("Dependencies initialized successfully")
            
            # Agents are already initialized as global instances
            self.coordinator = coordinator_agent
            self.backtesting = backtesting_agent
            
            logger.info("System initialization complete")
            
        except Exception as e:
            logger.error(f"System initialization failed: {e}")
            raise
    
    async def process_query(self, user_query: str) -> str:
        """
        Process a user query through the complete agent workflow.
        
        Args:
            user_query: Natural language query from user
            
        Returns:
            Formatted response with analysis results
        """
        try:
            logger.info(f"Processing query: {user_query[:100]}...")
            
            # Run coordinator agent with the query
            result = await self.coordinator.run(
                user_query,
                deps=self.dependencies
            )
            
            return result.data
            
        except Exception as e:
            logger.error(f"Query processing failed: {e}")
            return f"Error processing query: {str(e)}"
    
    async def cleanup(self):
        """Clean shutdown of the system."""
        if self.dependencies:
            await cleanup_dependencies(self.dependencies)
        logger.info("System cleanup complete")

async def main():
    """Main CLI interface for the ICT Backtesting System."""
    system = ICTBacktestingSystem()
    
    try:
        # Initialize system
        await system.initialize()
        
        print("🚀 ICT Backtesting Agent System Ready!")
        print("📊 Connected to database with 7M+ OHLCV records")
        print("🤖 Two-agent system: Coordinator + Backtesting Sub-Agent")
        print("💡 Ask questions about ICT methodology or request backtesting analysis")
        print("Type 'quit' to exit\n")
        
        # Interactive loop
        while True:
            try:
                user_input = input("📈 ICT Query: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not user_input:
                    continue
                
                print("\n🔄 Processing...")
                response = await system.process_query(user_input)
                print(f"\n📋 Response:\n{response}\n")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
        
    except Exception as e:
        logger.error(f"System error: {e}")
        print(f"❌ System initialization failed: {e}")
        return 1
    
    finally:
        print("\n👋 Shutting down...")
        await system.cleanup()
    
    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
