---
name: "External SSD Connection Manager"
description: "Reliable connection management for Ollama and Supabase on external SSD"
priority: "critical"
type: "infrastructure"
---

## Problem Statement

Database (Supabase) and LLM service (Ollama) are located on external SSD at `/Volumes/Extreme SSD/`. System needs reliable connection management to handle:
- SSD disconnection/reconnection events
- Service availability validation
- Automatic recovery mechanisms
- Connection state monitoring

## Specific Paths
- Ollama: `/Volumes/Extreme SSD/ollama`
- Supabase: `/Volumes/Extreme SSD/ict_project_2/supabase`

## Success Criteria
- [ ] System detects if external SSD is mounted before startup
- [ ] Automatic service validation for both Ollama and Supabase
- [ ] Graceful fallback to OpenAI/Anthropic if Ollama unavailable
- [ ] Health check endpoint showing connection status
- [ ] Auto-recovery when SSD reconnects

## Implementation Requirements
- Create `connection_manager.py` with SSD validation
- Add startup checks to `dependencies.py`
- Implement health monitoring in background task
- Add connection status to system logs
- Create fallback logic for LLM providers

## Key Questions
1. Should system fail fast if SSD not mounted, or wait for connection?
2. What's the recovery strategy if SSD disconnects during operation?
3. How often should health checks run (every 30 seconds)?
4. Should we cache recent queries if database becomes unavailable?

## Constraints
- Must not block main application startup
- Health checks should be async and non-blocking
- Fallback to cloud providers should be seamless
- Must log all connection state changes