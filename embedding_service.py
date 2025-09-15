"""
Embedding service for RAG operations using Ollama integration.
"""

import asyncio
import time
import httpx
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from settings import load_settings

logger = logging.getLogger(__name__)


@dataclass
class EmbeddingResult:
    """Result of embedding generation."""
    embeddings: List[float]
    dimensions: int
    generation_time: float
    model_used: str
    success: bool
    error_message: Optional[str] = None


class OllamaEmbeddingService:
    """Embedding service using Ollama for RAG operations."""
    
    def __init__(self):
        self.settings = load_settings()
        self.client = httpx.AsyncClient(timeout=self.settings.ollama_timeout)
    
    async def generate_embeddings(self, text: str, model: str = None) -> EmbeddingResult:
        """
        Generate embeddings for given text using Ollama.
        
        Args:
            text: Text to generate embeddings for
            model: Model to use (defaults to settings.ollama_embedding_model)
        
        Returns:
            EmbeddingResult with embeddings and metadata
        """
        model = model or self.settings.ollama_embedding_model
        start_time = time.time()
        
        try:
            payload = {
                "model": model,
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
            
            if not embeddings:
                return EmbeddingResult(
                    embeddings=[],
                    dimensions=0,
                    generation_time=generation_time,
                    model_used=model,
                    success=False,
                    error_message="No embeddings returned from Ollama"
                )
            
            return EmbeddingResult(
                embeddings=embeddings,
                dimensions=len(embeddings),
                generation_time=generation_time,
                model_used=model,
                success=True
            )
            
        except Exception as e:
            generation_time = time.time() - start_time
            logger.error(f"Failed to generate embeddings: {e}")
            
            return EmbeddingResult(
                embeddings=[],
                dimensions=0,
                generation_time=generation_time,
                model_used=model,
                success=False,
                error_message=str(e)
            )
    
    async def generate_batch_embeddings(self, texts: List[str], model: str = None) -> List[EmbeddingResult]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to generate embeddings for
            model: Model to use (defaults to settings.ollama_embedding_model)
        
        Returns:
            List of EmbeddingResult objects
        """
        tasks = [self.generate_embeddings(text, model) for text in texts]
        return await asyncio.gather(*tasks)
    
    async def validate_embedding_dimensions(self, text: str = "test") -> Dict[str, Any]:
        """
        Validate that embedding dimensions match expected configuration.
        
        Args:
            text: Test text for validation
        
        Returns:
            Dictionary with validation results
        """
        result = await self.generate_embeddings(text)
        
        expected_dims = self.settings.rag_vector_dimensions
        actual_dims = result.dimensions
        
        return {
            "success": result.success,
            "expected_dimensions": expected_dims,
            "actual_dimensions": actual_dims,
            "dimensions_match": actual_dims == expected_dims,
            "model_used": result.model_used,
            "generation_time": result.generation_time,
            "error_message": result.error_message
        }
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


# Global embedding service instance
embedding_service = OllamaEmbeddingService()


async def get_embeddings(text: str) -> List[float]:
    """
    Convenience function to get embeddings for text.
    
    Args:
        text: Text to generate embeddings for
    
    Returns:
        List of embedding values
    """
    result = await embedding_service.generate_embeddings(text)
    if result.success:
        return result.embeddings
    else:
        logger.error(f"Embedding generation failed: {result.error_message}")
        return []


async def validate_embedding_setup() -> bool:
    """
    Validate that embedding service is properly configured.
    
    Returns:
        True if setup is valid, False otherwise
    """
    validation = await embedding_service.validate_embedding_dimensions()
    return validation["success"] and validation["dimensions_match"]
