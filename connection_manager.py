"""
External SSD Connection Manager for Ollama and Supabase services.
Handles SSD mount detection, service validation, and automatic recovery.
"""

import asyncio
import os
import time
import logging
import asyncpg
import httpx
from typing import Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path

from settings import load_settings

logger = logging.getLogger(__name__)


@dataclass
class ConnectionStatus:
    """Status of external SSD connections."""
    ssd_mounted: bool
    ollama_available: bool
    supabase_available: bool
    last_check: float
    error_messages: Dict[str, str]


class ExternalSSDManager:
    """Manager for external SSD services (Ollama and Supabase)."""
    
    def __init__(self):
        self.settings = load_settings()
        self.status = ConnectionStatus(
            ssd_mounted=False,
            ollama_available=False,
            supabase_available=False,
            last_check=0.0,
            error_messages={}
        )
        self._http_client = None
        self._db_pool = None
    
    async def initialize(self):
        """Initialize HTTP client for health checks."""
        self._http_client = httpx.AsyncClient(timeout=10.0)
    
    async def cleanup(self):
        """Clean up resources."""
        if self._http_client:
            await self._http_client.aclose()
        if self._db_pool:
            await self._db_pool.close()
    
    def check_ssd_mounted(self) -> bool:
        """Check if external SSD is mounted."""
        try:
            ssd_path = Path("/Volumes/Extreme SSD")
            ollama_path = Path(self.settings.ollama_base_path)
            supabase_path = Path(self.settings.supabase_base_path)
            
            # Check if SSD is mounted and paths exist
            ssd_mounted = (
                ssd_path.exists() and 
                ssd_path.is_mount() and
                ollama_path.exists() and
                supabase_path.exists()
            )
            
            if not ssd_mounted:
                if not ssd_path.exists():
                    self.status.error_messages["ssd"] = "External SSD not found at /Volumes/Extreme SSD"
                elif not ssd_path.is_mount():
                    self.status.error_messages["ssd"] = "External SSD path exists but is not mounted"
                elif not ollama_path.exists():
                    self.status.error_messages["ssd"] = f"Ollama path not found: {ollama_path}"
                elif not supabase_path.exists():
                    self.status.error_messages["ssd"] = f"Supabase path not found: {supabase_path}"
            else:
                self.status.error_messages.pop("ssd", None)
            
            return ssd_mounted
            
        except Exception as e:
            self.status.error_messages["ssd"] = f"SSD check failed: {str(e)}"
            return False
    
    async def check_ollama_health(self) -> bool:
        """Check if Ollama service is available."""
        try:
            if not self._http_client:
                await self.initialize()
            
            response = await self._http_client.get(f"{self.settings.ollama_host}/api/tags")
            
            if response.status_code == 200:
                self.status.error_messages.pop("ollama", None)
                return True
            else:
                self.status.error_messages["ollama"] = f"Ollama HTTP {response.status_code}"
                return False
                
        except Exception as e:
            self.status.error_messages["ollama"] = f"Ollama connection failed: {str(e)}"
            return False
    
    async def check_supabase_health(self) -> bool:
        """Check if Supabase database is available."""
        try:
            # Test database connection
            conn = await asyncpg.connect(self.settings.database_url)
            await conn.execute("SELECT 1")
            await conn.close()
            
            self.status.error_messages.pop("supabase", None)
            return True
            
        except Exception as e:
            self.status.error_messages["supabase"] = f"Supabase connection failed: {str(e)}"
            return False
    
    async def full_health_check(self) -> ConnectionStatus:
        """Perform comprehensive health check of all external SSD services."""
        start_time = time.time()
        
        # Check SSD mount status
        self.status.ssd_mounted = self.check_ssd_mounted()
        
        # Only check services if SSD is mounted
        if self.status.ssd_mounted:
            # Check services concurrently
            ollama_task = asyncio.create_task(self.check_ollama_health())
            supabase_task = asyncio.create_task(self.check_supabase_health())
            
            self.status.ollama_available = await ollama_task
            self.status.supabase_available = await supabase_task
        else:
            self.status.ollama_available = False
            self.status.supabase_available = False
            self.status.error_messages["services"] = "Services unavailable - SSD not mounted"
        
        self.status.last_check = time.time()
        
        # Log status changes
        check_duration = time.time() - start_time
        logger.info(f"Health check completed in {check_duration:.2f}s - "
                   f"SSD: {'✅' if self.status.ssd_mounted else '❌'}, "
                   f"Ollama: {'✅' if self.status.ollama_available else '❌'}, "
                   f"Supabase: {'✅' if self.status.supabase_available else '❌'}")
        
        return self.status
    
    async def wait_for_ssd_connection(self, timeout: float = 60.0) -> bool:
        """Wait for external SSD to become available."""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.check_ssd_mounted():
                logger.info("External SSD connection established")
                return True
            
            logger.info("Waiting for external SSD connection...")
            await asyncio.sleep(5.0)
        
        logger.error(f"External SSD connection timeout after {timeout}s")
        return False
    
    async def get_service_status(self) -> Dict[str, Any]:
        """Get detailed service status for monitoring."""
        await self.full_health_check()
        
        return {
            "external_ssd": {
                "mounted": self.status.ssd_mounted,
                "ollama_path": self.settings.ollama_base_path,
                "supabase_path": self.settings.supabase_base_path
            },
            "services": {
                "ollama": {
                    "available": self.status.ollama_available,
                    "host": self.settings.ollama_host,
                    "model": self.settings.ollama_model
                },
                "supabase": {
                    "available": self.status.supabase_available,
                    "database_url": self.settings.database_url.replace("postgres:", "postgres:***@"),
                    "port": 54334
                }
            },
            "health_check": {
                "last_check": self.status.last_check,
                "errors": self.status.error_messages
            },
            "overall_status": self._get_overall_status()
        }
    
    def _get_overall_status(self) -> str:
        """Determine overall system status."""
        if not self.status.ssd_mounted:
            return "ssd_disconnected"
        elif self.status.ollama_available and self.status.supabase_available:
            return "optimal"
        elif self.status.supabase_available:
            return "database_only"
        elif self.status.ollama_available:
            return "llm_only"
        else:
            return "services_unavailable"


# Global connection manager instance
connection_manager = ExternalSSDManager()


async def validate_external_ssd_setup() -> bool:
    """
    Validate that external SSD setup is ready for ICT backtesting.
    
    Returns:
        True if setup is valid, False otherwise
    """
    status = await connection_manager.full_health_check()
    return status.ssd_mounted and status.supabase_available


async def get_connection_status() -> Dict[str, Any]:
    """
    Get current connection status for external SSD services.
    
    Returns:
        Dictionary with detailed connection status
    """
    return await connection_manager.get_service_status()


async def ensure_ssd_connection(wait_timeout: float = 30.0) -> bool:
    """
    Ensure external SSD is connected before proceeding.
    
    Args:
        wait_timeout: Maximum time to wait for connection
    
    Returns:
        True if SSD is connected, False otherwise
    """
    if connection_manager.check_ssd_mounted():
        return True
    
    logger.warning("External SSD not detected, waiting for connection...")
    return await connection_manager.wait_for_ssd_connection(wait_timeout)
