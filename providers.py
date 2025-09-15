from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.providers.anthropic import AnthropicProvider
from pydantic_ai.providers.ollama import OllamaProvider
from typing import Union
import logging

from .settings import load_settings

logger = logging.getLogger(__name__)

ModelType = Union[OllamaModel, OpenAIModel, AnthropicModel]

def get_llm_model(model_preference: str = None) -> ModelType:
    """Get configured LLM model with fallback strategy."""
    settings = load_settings()
    
    # Use preference or default from settings
    provider = model_preference or settings.llm_provider
    
    try:
        if provider == "ollama":
            return _get_ollama_model(settings)
        elif provider == "openai":
            return _get_openai_model(settings)
        elif provider == "anthropic":
            return _get_anthropic_model(settings)
        else:
            logger.warning(f"Unknown provider {provider}, falling back to ollama")
            return _get_ollama_model(settings)
    
    except Exception as e:
        logger.error(f"Failed to initialize {provider} model: {e}")
        return _get_fallback_model(settings, exclude=provider)

def _get_ollama_model(settings) -> OllamaModel:
    """Initialize Ollama model with enhanced configuration and health check."""
    try:
        # Import health checker for validation
        from ollama_health import health_checker
        
        provider = OllamaProvider(base_url=settings.ollama_host)
        model = OllamaModel(settings.ollama_model, provider=provider)
        
        # Perform basic connectivity check
        import asyncio
        try:
            health_result = asyncio.run(health_checker.check_health())
            if not health_result.is_healthy:
                logger.warning(f"Ollama health check failed: {health_result.error_message}")
                logger.warning("Continuing with model initialization, but performance may be degraded")
        except Exception as health_error:
            logger.warning(f"Could not perform health check: {health_error}")
        
        logger.info(f"Initialized Ollama model: {settings.ollama_model} at {settings.ollama_host}")
        return model
    except Exception as e:
        logger.error(f"Ollama initialization failed: {e}")
        raise

def _get_openai_model(settings) -> OpenAIModel:
    """Initialize OpenAI model with configuration."""
    if not settings.openai_api_key:
        raise ValueError("OpenAI API key not configured")
    
    try:
        provider = OpenAIProvider(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url
        )
        model = OpenAIModel(settings.openai_model, provider=provider)
        logger.info(f"Initialized OpenAI model: {settings.openai_model}")
        return model
    except Exception as e:
        logger.error(f"OpenAI initialization failed: {e}")
        raise

def _get_anthropic_model(settings) -> AnthropicModel:
    """Initialize Anthropic model with configuration."""
    if not settings.anthropic_api_key:
        raise ValueError("Anthropic API key not configured")
    
    try:
        provider = AnthropicProvider(api_key=settings.anthropic_api_key)
        model = AnthropicModel(settings.anthropic_model, provider=provider)
        logger.info(f"Initialized Anthropic model: {settings.anthropic_model}")
        return model
    except Exception as e:
        logger.error(f"Anthropic initialization failed: {e}")
        raise

def _get_fallback_model(settings, exclude: str = None) -> ModelType:
    """Get fallback model when primary provider fails."""
    fallback_order = ["ollama", "openai", "anthropic"]
    
    if exclude:
        fallback_order = [p for p in fallback_order if p != exclude]
    
    for provider in fallback_order:
        try:
            if provider == "ollama":
                return _get_ollama_model(settings)
            elif provider == "openai" and settings.openai_api_key:
                return _get_openai_model(settings)
            elif provider == "anthropic" and settings.anthropic_api_key:
                return _get_anthropic_model(settings)
        except Exception as e:
            logger.warning(f"Fallback provider {provider} failed: {e}")
            continue
    
    raise RuntimeError("All LLM providers failed to initialize")

def get_coordinator_model() -> ModelType:
    """Get model specifically configured for Coordinator Agent."""
    # Coordinator handles complex reasoning, may benefit from more capable model
    settings = load_settings()
    
    if settings.openai_api_key:
        return get_llm_model("openai")  # Prefer OpenAI for strategic reasoning
    else:
        return get_llm_model()  # Use default configuration

def get_backtesting_model() -> ModelType:
    """Get model specifically configured for Backtesting Sub-Agent."""
    # Sub-agent handles structured execution, can use faster local model
    return get_llm_model("ollama")  # Prefer local model for speed
