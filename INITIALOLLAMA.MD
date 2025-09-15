---
name: "Ollama Local Integration Service"
description: "Configure and integrate Ollama running on external SSD for ICT agent system"
priority: "high"
type: "integration"
---

## Problem Statement

Ollama is installed at `/Volumes/Extreme SSD/ollama` and needs to be:
- Properly configured for the ICT backtesting agents
- Set as primary LLM provider with automatic fallback
- Configured for embedding generation (nomic-embed-text)
- Monitored for availability and performance

## Technical Requirements

### Ollama Configuration
- Base path: `/Volumes/Extreme SSD/ollama`
- Default port: 11434
- Required models:
  - LLM: `llama3.2` or `mixtral` for agent reasoning
  - Embeddings: `nomic-embed-text` (768 dimensions)

### Integration Points
1. Update `providers.py` to prioritize Ollama
2. Configure embedding service for RAG
3. Add Ollama-specific retry logic
4. Implement model loading validation

## Success Criteria
- [ ] Ollama responds on `http://localhost:11434`
- [ ] Required models are loaded and accessible
- [ ] Embedding generation works for RAG system
- [ ] Automatic fallback to OpenAI when Ollama unavailable
- [ ] Response times under 5 seconds for standard queries

## Implementation Tasks
1. Create `ollama_service.py` for Ollama management
2. Add Ollama health check to startup routine
3. Implement model validation (check if models are pulled)
4. Configure embedding pipeline for 768-dimension vectors
5. Add Ollama-specific error handling

## Configuration Updates Needed

### .env additions:
```env
OLLAMA_BASE_PATH=/Volumes/Extreme SSD/ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
OLLAMA_TIMEOUT=30