"""
Ollama health check and monitoring tools for ICT backtesting system.
"""

import asyncio
import time
import httpx
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from settings import load_settings

logger = logging.getLogger(__name__)


@dataclass
class OllamaHealthResult:
    """Result of Ollama health check."""
    is_healthy: bool
    response_time: float
    models_available: List[str]
    error_message: Optional[str] = None
    required_models_status: Dict[str, bool] = None


class OllamaHealthChecker:
    """Health checker for Ollama service integration."""
    
    def __init__(self):
        self.settings = load_settings()
        self.client = httpx.AsyncClient(timeout=self.settings.ollama_timeout)
    
    async def check_health(self) -> OllamaHealthResult:
        """
        Perform comprehensive health check on Ollama service.
        
        Returns:
            OllamaHealthResult with detailed status
        """
        start_time = time.time()
        
        try:
            # Check if Ollama is responding
            response = await self.client.get(f"{self.settings.ollama_host}/api/tags")
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                models = [model["name"] for model in data.get("models", [])]
                
                # Check required models
                required_models = [
                    self.settings.ollama_model,
                    self.settings.ollama_embedding_model
                ]
                
                required_status = {}
                for model in required_models:
                    # Check for exact match or partial match (models often have version suffixes)
                    is_available = any(
                        model in available_name or available_name.startswith(model)
                        for available_name in models
                    )
                    required_status[model] = is_available
                
                return OllamaHealthResult(
                    is_healthy=True,
                    response_time=response_time,
                    models_available=models,
                    required_models_status=required_status
                )
            else:
                return OllamaHealthResult(
                    is_healthy=False,
                    response_time=response_time,
                    models_available=[],
                    error_message=f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            response_time = time.time() - start_time
            return OllamaHealthResult(
                is_healthy=False,
                response_time=response_time,
                models_available=[],
                error_message=str(e)
            )
    
    async def test_embedding_generation(self, text: str = "test embedding") -> Dict[str, Any]:
        """
        Test embedding generation functionality.
        
        Args:
            text: Text to generate embeddings for
        
        Returns:
            Dictionary with embedding test results
        """
        start_time = time.time()
        
        try:
            payload = {
                "model": self.settings.ollama_embedding_model,
                "prompt": text
            }
            
            response = await self.client.post(
                f"{self.settings.ollama_host}/api/embeddings",
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            embeddings = data.get("embedding", [])
            generation_time = time.time() - start_time
            
            return {
                "success": True,
                "dimensions": len(embeddings),
                "expected_dimensions": self.settings.rag_vector_dimensions,
                "generation_time": generation_time,
                "model_used": self.settings.ollama_embedding_model,
                "meets_requirements": len(embeddings) == self.settings.rag_vector_dimensions
            }
            
        except Exception as e:
            generation_time = time.time() - start_time
            return {
                "success": False,
                "error": str(e),
                "generation_time": generation_time,
                "model_used": self.settings.ollama_embedding_model
            }
    
    async def get_system_status(self) -> Dict[str, Any]:
        """
        Get comprehensive system status for Ollama integration.
        
        Returns:
            Dictionary with complete system status
        """
        health_result = await self.check_health()
        embedding_test = await self.test_embedding_generation()
        
        # Determine overall status
        if health_result.is_healthy and embedding_test["success"]:
            if all(health_result.required_models_status.values()):
                overall_status = "optimal"
            else:
                overall_status = "partial"
        elif health_result.is_healthy:
            overall_status = "degraded"
        else:
            overall_status = "failed"
        
        # Generate recommendations
        recommendations = []
        if not health_result.is_healthy:
            recommendations.append("Ollama service is not responding - check if it's running")
            recommendations.append(f"Verify Ollama is accessible at {self.settings.ollama_host}")
        
        if health_result.required_models_status:
            missing_models = [
                model for model, available in health_result.required_models_status.items()
                if not available
            ]
            if missing_models:
                for model in missing_models:
                    recommendations.append(f"Pull missing model: ollama pull {model}")
        
        if embedding_test["success"] and not embedding_test["meets_requirements"]:
            recommendations.append(
                f"Embedding dimensions mismatch: got {embedding_test['dimensions']}, "
                f"expected {embedding_test['expected_dimensions']}"
            )
        
        if health_result.response_time > self.settings.performance_threshold:
            recommendations.append(
                f"Response time ({health_result.response_time:.2f}s) exceeds threshold "
                f"({self.settings.performance_threshold}s)"
            )
        
        if overall_status == "optimal":
            recommendations.append("Ollama integration is operating optimally")
        
        return {
            "overall_status": overall_status,
            "ollama_health": {
                "is_healthy": health_result.is_healthy,
                "response_time": health_result.response_time,
                "models_available": len(health_result.models_available),
                "error_message": health_result.error_message
            },
            "required_models": health_result.required_models_status or {},
            "embedding_test": embedding_test,
            "performance": {
                "meets_threshold": health_result.response_time <= self.settings.performance_threshold,
                "threshold": self.settings.performance_threshold
            },
            "recommendations": recommendations,
            "configuration": {
                "ollama_host": self.settings.ollama_host,
                "ollama_model": self.settings.ollama_model,
                "embedding_model": self.settings.ollama_embedding_model,
                "base_path": self.settings.ollama_base_path
            }
        }
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


# Global health checker instance
health_checker = OllamaHealthChecker()


async def check_ollama_status() -> Dict[str, Any]:
    """
    Convenience function to check Ollama status.
    
    Returns:
        Dictionary with system status
    """
    return await health_checker.get_system_status()


async def validate_ollama_setup() -> bool:
    """
    Validate that Ollama is properly set up for ICT backtesting.
    
    Returns:
        True if setup is valid, False otherwise
    """
    status = await check_ollama_status()
    return status["overall_status"] in ["optimal", "partial"]
