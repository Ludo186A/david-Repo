---
name: "Ollama Local Integration Service for ICT Backtesting Agents"
description: "Pydantic AI agent system for managing Ollama local LLM integration with automatic fallback and embedding support"
priority: "high"
type: "integration"
---

## Purpose

Build a comprehensive Pydantic AI agent system that integrates Ollama running on external SSD (`/Volumes/Extreme SSD/ollama`) as the primary LLM provider for ICT backtesting agents, with automatic fallback to OpenAI and full embedding pipeline support for RAG operations.

## Core Principles

1. **Pydantic AI Best Practices**: Deep integration with Pydantic AI patterns for agent creation, tools, and structured outputs
2. **Type Safety First**: Leverage Pydantic AI's type-safe design and Pydantic validation throughout
3. **Context Engineering Integration**: Apply proven context engineering workflows to AI agent development
4. **Comprehensive Testing**: Use TestModel and FunctionModel for thorough agent validation

## ⚠️ Implementation Guidelines: Don't Over-Engineer

**IMPORTANT**: Keep your agent implementation focused and practical. Don't build unnecessary complexity.

- ✅ **Start simple** - Build the minimum viable agent that meets requirements
- ✅ **Add tools incrementally** - Implement only what the agent needs to function
- ✅ **Follow main_agent_reference** - Use proven patterns, don't reinvent
- ✅ **Use string output by default** - Only add result_type when validation is required
- ✅ **Test early and often** - Use TestModel to validate as you build

### Key Question:
**"Does this agent really need this feature to accomplish its core purpose?"**

If the answer is no, don't build it. Keep it simple, focused, and functional.

---

## Goal

Create a robust Pydantic AI agent system that seamlessly integrates Ollama as the primary LLM provider for ICT backtesting operations, providing:
- Automatic health monitoring and model validation
- Intelligent fallback to OpenAI when Ollama is unavailable
- High-performance embedding generation for RAG systems
- Sub-5-second response times for standard queries
- Production-ready error handling and retry mechanisms

## Why

The ICT backtesting system requires:
1. **Cost Efficiency**: Local Ollama reduces API costs for high-volume backtesting operations
2. **Performance Control**: Direct control over model performance and availability
3. **Data Privacy**: Local processing keeps sensitive trading data secure
4. **Reliability**: Automatic fallback ensures system availability even when Ollama is down
5. **Scalability**: Local embeddings support large-scale RAG operations without API limits

## What

### Agent Type Classification
- [x] **Tool-Enabled Agent**: Agent with external tool integration capabilities
- [x] **Workflow Agent**: Multi-step task processing and orchestration
- [ ] **Chat Agent**: Conversational interface with memory and context
- [ ] **Structured Output Agent**: Complex data validation and formatting

### External Integrations
- [x] Ollama API integration (`http://localhost:11434`)
- [x] OpenAI API fallback integration
- [x] File system operations (model validation, health checks)
- [ ] Database connections (specify type: PostgreSQL, MongoDB, etc.)
- [ ] REST API integrations (list required services)
- [ ] Web scraping or search capabilities
- [ ] Real-time data sources

### Success Criteria
- [ ] Ollama responds correctly on `http://localhost:11434`
- [ ] Required models (`llama3.2`, `nomic-embed-text`) are loaded and accessible
- [ ] Embedding generation works for RAG system with 768-dimension vectors
- [ ] Automatic fallback to OpenAI when Ollama unavailable (< 2 second detection)
- [ ] Response times under 5 seconds for standard queries
- [ ] Agent successfully handles health monitoring and model validation
- [ ] All tools work correctly with proper error handling
- [ ] Comprehensive test coverage with TestModel and FunctionModel
- [ ] Security measures implemented (API keys, input validation, rate limiting)
- [ ] Performance meets requirements (response time, throughput)

## All Needed Context

### Pydantic AI Documentation & Research

```yaml
# MCP servers
- mcp: Archon
  query: Query for anything in the Pydantic AI documentation (using RAG and code examples) to help with the implementation
  why: Core framework understanding and latest patterns

# ESSENTIAL PYDANTIC AI DOCUMENTATION - Must be researched
- url: https://ai.pydantic.dev/
  why: Official Pydantic AI documentation with getting started guide
  content: Agent creation, model providers, dependency injection patterns

- url: https://ai.pydantic.dev/agents/
  why: Comprehensive agent architecture and configuration patterns
  content: System prompts, output types, execution methods, agent composition

- url: https://ai.pydantic.dev/tools/
  why: Tool integration patterns and function registration
  content: @agent.tool decorators, RunContext usage, parameter validation

- url: https://ai.pydantic.dev/testing/
  why: Testing strategies specific to Pydantic AI agents
  content: TestModel, FunctionModel, Agent.override(), pytest patterns

- url: https://ai.pydantic.dev/models/
  why: Model provider configuration and authentication
  content: OpenAI, Anthropic, Gemini setup, API key management, fallback models

# Prebuilt examples
- path: examples/
  why: Reference implementations for Pydantic AI agents (extra emphasis on the main_agent_reference)
  content: A bunch of already built simple Pydantic AI examples to reference including how to set up models and providers

- path: examples/main_agent_reference/cli.py
  why: Shows real-world interaction with Pydantic AI agents
  content: Conversational CLI with streaming, tool call visibility, and conversation handling - demonstrates how users actually interact with agents
```

### Ollama Integration Research

```yaml
# Ollama-specific Documentation
- url: https://ollama.ai/docs
  why: Official Ollama documentation for API integration
  content: REST API endpoints, model management, embedding generation

- url: https://github.com/ollama/ollama/blob/main/docs/api.md
  why: Complete API reference for Ollama integration
  content: Health checks, model loading, chat completions, embeddings

# Ollama Configuration Requirements
ollama_setup:
  installation_path: "/Volumes/Extreme SSD/ollama"
  api_endpoint: "http://localhost:11434"
  required_models:
    llm: "llama3.2"  # Primary reasoning model
    embedding: "nomic-embed-text"  # 768-dimension embeddings
  performance_targets:
    response_time: "< 5 seconds"
    availability: "99%+ uptime"
    fallback_time: "< 2 seconds"
```

### Agent Architecture Research

```yaml
# Pydantic AI Architecture Patterns (follow main_agent_reference)
agent_structure:
  configuration:
    - settings.py: Environment-based configuration with pydantic-settings
    - providers.py: Model provider abstraction with get_llm_model() and Ollama integration
    - Environment variables for API keys and Ollama configuration
    - Never hardcode model strings like "openai:gpt-4o"
  
  agent_definition:
    - Default to string output (no result_type unless structured output needed)
    - Use get_llm_model() from providers.py for model configuration
    - System prompts as string constants or functions
    - Dataclass dependencies for Ollama service integration
  
  tool_integration:
    - @agent.tool for context-aware tools with RunContext[DepsType]
    - Tool functions for Ollama health checks and model validation
    - Proper error handling and logging in tool implementations
    - Dependency injection through RunContext.deps
  
  testing_strategy:
    - TestModel for rapid development validation
    - FunctionModel for custom behavior testing  
    - Agent.override() for test isolation
    - Comprehensive tool testing with mocks for Ollama API
```

### Security Considerations

```yaml
# Pydantic AI Security Patterns (research required)
security_requirements:
  api_management:
    environment_variables: ["OPENAI_API_KEY", "OLLAMA_HOST", "OLLAMA_BASE_PATH"]
    secure_storage: "Never commit API keys to version control"
    rotation_strategy: "Plan for key rotation and management"
  
  input_validation:
    sanitization: "Validate all user inputs with Pydantic models"
    prompt_injection: "Implement prompt injection prevention strategies"
    rate_limiting: "Prevent abuse with proper throttling"
  
  output_security:
    data_filtering: "Ensure no sensitive data in agent responses"
    content_validation: "Validate output structure and content"
    logging_safety: "Safe logging without exposing secrets"
```

### Common Pydantic AI Gotchas (research and document)

```yaml
# Agent-specific gotchas to research and address
implementation_gotchas:
  async_patterns:
    issue: "Mixing sync and async agent calls inconsistently"
    research: "Pydantic AI async/await best practices"
    solution: "[To be documented based on research]"
  
  ollama_integration:
    issue: "Ollama API timeouts and connection failures"
    research: "Robust error handling for local LLM services"
    solution: "[To be documented based on research]"
  
  model_fallback:
    issue: "Seamless fallback between Ollama and OpenAI"
    research: "Provider switching patterns in Pydantic AI"
    solution: "[To be documented based on research]"
  
  embedding_consistency:
    issue: "Different embedding dimensions between providers"
    research: "Embedding standardization and validation"
    solution: "[To be documented based on research]"
```

## Implementation Blueprint

### Technology Research Phase

**RESEARCH REQUIRED - Complete before implementation:**

✅ **Pydantic AI Framework Deep Dive:**
- [ ] Agent creation patterns and best practices
- [ ] Model provider configuration and fallback strategies
- [ ] Tool integration patterns (@agent.tool vs @agent.tool_plain)
- [ ] Dependency injection system and type safety
- [ ] Testing strategies with TestModel and FunctionModel

✅ **Ollama Integration Investigation:**
- [ ] Ollama REST API patterns and authentication
- [ ] Health check and model validation endpoints
- [ ] Embedding generation API and dimension handling
- [ ] Error handling and timeout management
- [ ] Performance optimization for local LLM calls

✅ **Agent Architecture Investigation:**
- [ ] Project structure conventions (agent.py, tools.py, models.py, dependencies.py)
- [ ] System prompt design (static vs dynamic)
- [ ] Structured output validation with Pydantic models
- [ ] Async/sync patterns and streaming support
- [ ] Error handling and retry mechanisms

✅ **Security and Production Patterns:**
- [ ] API key management and secure configuration
- [ ] Input validation and prompt injection prevention
- [ ] Rate limiting and monitoring strategies
- [ ] Logging and observability patterns

### Agent Implementation Plan

```yaml
Implementation Task 1 - Ollama Service Integration:
  CREATE ollama service module:
    - ollama_service.py: Core Ollama API client with health checks
    - model_validator.py: Model availability and validation logic
    - embedding_service.py: Embedding generation with 768-dimension support
    - fallback_manager.py: Automatic OpenAI fallback logic
    - performance_monitor.py: Response time and availability tracking

Implementation Task 2 - Agent Architecture Setup (Follow main_agent_reference):
  CREATE agent project structure:
    - settings.py: Environment-based configuration with Ollama settings
    - providers.py: Enhanced model provider with Ollama + OpenAI fallback
    - agent.py: Main agent definition for Ollama management
    - tools.py: Ollama health check and model management tools
    - dependencies.py: Ollama service integrations (dataclasses)
    - tests/: Comprehensive test suite with Ollama mocks

Implementation Task 3 - Core Agent Development:
  IMPLEMENT agent.py following main_agent_reference patterns:
    - Use enhanced get_llm_model() with Ollama priority
    - System prompt for Ollama management and monitoring
    - Dependency injection with Ollama service dataclass
    - NO result_type unless structured output specifically needed
    - Error handling and logging for Ollama operations

Implementation Task 4 - Tool Integration:
  DEVELOP tools.py:
    - @agent.tool for Ollama health checks
    - @agent.tool for model validation and loading
    - @agent.tool for embedding generation testing
    - @agent.tool for performance monitoring
    - RunContext[DepsType] integration for service access
    - Parameter validation with proper type hints
    - Error handling and retry mechanisms

Implementation Task 5 - Data Models and Dependencies:
  CREATE models.py and dependencies.py:
    - Pydantic models for Ollama API responses
    - Health check result models
    - Embedding validation models
    - Dependency classes for Ollama service
    - Input validation models for tools
    - Custom validators and constraints

Implementation Task 6 - Comprehensive Testing:
  IMPLEMENT testing suite:
    - TestModel integration for rapid development
    - FunctionModel tests for Ollama behavior simulation
    - Agent.override() patterns for isolation
    - Mock Ollama API responses for testing
    - Integration tests with real Ollama instance
    - Tool validation and error scenario testing
```

### Environment Configuration

```yaml
Implementation Task 7 - Environment Setup:
  CREATE .env configuration:
    # Ollama Configuration
    OLLAMA_BASE_PATH=/Volumes/Extreme SSD/ollama
    OLLAMA_HOST=http://localhost:11434
    OLLAMA_MODEL=llama3.2
    OLLAMA_EMBEDDING_MODEL=nomic-embed-text
    OLLAMA_TIMEOUT=30
    
    # Fallback Configuration
    OPENAI_API_KEY=your_openai_key_here
    FALLBACK_MODEL=gpt-4
    FALLBACK_TIMEOUT=10
    
    # Performance Configuration
    MAX_RETRIES=3
    HEALTH_CHECK_INTERVAL=60
    PERFORMANCE_THRESHOLD=5.0
```

## Validation Loop

### Level 1: Ollama Service Validation

```bash
# Verify Ollama is running and accessible
curl -f http://localhost:11434/api/tags || echo "Ollama not accessible"

# Check required models are available
curl -s http://localhost:11434/api/tags | grep -q "llama3.2" || echo "llama3.2 not found"
curl -s http://localhost:11434/api/tags | grep -q "nomic-embed-text" || echo "nomic-embed-text not found"

# Test embedding generation
curl -X POST http://localhost:11434/api/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model": "nomic-embed-text", "prompt": "test"}' \
  | jq '.embedding | length' # Should return 768

# Expected: Ollama running, models loaded, embeddings working
# If failing: Start Ollama, pull required models
```

### Level 2: Agent Structure Validation

```bash
# Verify complete agent project structure
find ollama_agent -name "*.py" | sort
test -f ollama_agent/agent.py && echo "Agent definition present"
test -f ollama_agent/tools.py && echo "Tools module present"
test -f ollama_agent/ollama_service.py && echo "Ollama service present"
test -f ollama_agent/dependencies.py && echo "Dependencies module present"

# Verify proper Pydantic AI imports
grep -q "from pydantic_ai import Agent" ollama_agent/agent.py
grep -q "@agent.tool" ollama_agent/tools.py
grep -q "import requests" ollama_agent/ollama_service.py

# Expected: All required files with proper Pydantic AI patterns
# If missing: Generate missing components with correct patterns
```

### Level 3: Agent Functionality Validation

```bash
# Test agent can be imported and instantiated
python -c "
from ollama_agent.agent import agent
print('Agent created successfully')
print(f'Model: {agent.model}')
print(f'Tools: {len(agent.tools)}')
"

# Test Ollama health check tool
python -c "
from pydantic_ai.models.test import TestModel
from ollama_agent.agent import agent
test_model = TestModel()
with agent.override(model=test_model):
    result = agent.run_sync('Check Ollama health')
    print(f'Health check result: {result.output}')
"

# Test embedding generation tool
python -c "
from ollama_agent.tools import generate_embeddings
result = generate_embeddings('test prompt')
print(f'Embedding dimensions: {len(result)}')
assert len(result) == 768, 'Incorrect embedding dimensions'
"

# Expected: Agent instantiation works, tools registered, health checks pass
# If failing: Debug agent configuration and Ollama connectivity
```

### Level 4: Integration Testing Validation

```bash
# Run complete test suite
cd ollama_agent
python -m pytest tests/ -v

# Test Ollama integration specifically
python -m pytest tests/test_ollama_integration.py::test_health_check -v
python -m pytest tests/test_ollama_integration.py::test_model_validation -v
python -m pytest tests/test_ollama_integration.py::test_embedding_generation -v

# Test fallback mechanism
python -m pytest tests/test_fallback.py::test_openai_fallback -v

# Performance testing
python -m pytest tests/test_performance.py::test_response_time -v

# Expected: All tests pass, performance targets met
# If failing: Fix implementation based on test failures
```

## Final Validation Checklist

### Ollama Integration Completeness

- [ ] Ollama service running on `http://localhost:11434`
- [ ] Required models (`llama3.2`, `nomic-embed-text`) loaded and accessible
- [ ] Health check endpoint responding correctly
- [ ] Embedding generation producing 768-dimension vectors
- [ ] Performance targets met (< 5 second response times)

### Agent Implementation Completeness

- [ ] Complete agent project structure: `agent.py`, `tools.py`, `ollama_service.py`, `dependencies.py`
- [ ] Agent instantiation with Ollama model provider configuration
- [ ] Tool registration with @agent.tool decorators and RunContext integration
- [ ] Fallback mechanism to OpenAI when Ollama unavailable
- [ ] Dependency injection properly configured and tested
- [ ] Comprehensive test suite with TestModel and FunctionModel

### Pydantic AI Best Practices

- [ ] Type safety throughout with proper type hints and validation
- [ ] Security patterns implemented (API keys, input validation, rate limiting)
- [ ] Error handling and retry mechanisms for robust operation
- [ ] Async/sync patterns consistent and appropriate
- [ ] Documentation and code comments for maintainability

### Production Readiness

- [ ] Environment configuration with .env files and validation
- [ ] Logging and monitoring setup for observability
- [ ] Performance optimization and resource management
- [ ] Deployment readiness with proper configuration management
- [ ] Maintenance and update strategies documented

---

## Anti-Patterns to Avoid

### Ollama Integration

- ❌ Don't assume Ollama is always available - implement robust fallback mechanisms
- ❌ Don't ignore timeout handling - Ollama can be slower than cloud APIs
- ❌ Don't skip model validation - ensure required models are loaded before use
- ❌ Don't hardcode Ollama paths - use environment variables for configuration
- ❌ Don't forget embedding dimension validation - ensure consistency across providers

### Pydantic AI Agent Development

- ❌ Don't skip TestModel validation - always test with TestModel during development
- ❌ Don't hardcode API keys - use environment variables for all credentials
- ❌ Don't ignore async patterns - Pydantic AI has specific async/sync requirements
- ❌ Don't create complex tool chains - keep tools focused and composable
- ❌ Don't skip error handling - implement simple yet effective retry and fallback mechanisms

### Agent Architecture

- ❌ Don't mix agent types - clearly separate tool and workflow patterns
- ❌ Don't ignore dependency injection - use proper type-safe dependency management
- ❌ Don't skip output validation - always use Pydantic models for structured responses
- ❌ Don't forget tool documentation - ensure all tools have proper descriptions and schemas

**RESEARCH STATUS: [TO BE COMPLETED]** - Complete comprehensive Pydantic AI and Ollama research before implementation begins.
