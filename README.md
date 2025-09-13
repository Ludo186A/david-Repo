# ICT Backtesting Agent System

A sophisticated two-agent Pydantic AI system for intelligent backtesting analysis of financial markets using Inner Circle Trader (ICT) methodology.

## 🚀 System Overview

The ICT Backtesting Agent System provides natural language querying capabilities for comprehensive financial market analysis using ICT concepts including Order Blocks, Fair Value Gaps, Liquidity Sweeps, and Market Structure analysis.

### Architecture

- **Coordinator Agent**: Strategic query interpretation, classification, and analysis planning
- **Backtesting Sub-Agent**: Technical SQL execution with 60+ specialized ICT functions
- **Database**: PostgreSQL with 7,081,584 OHLCV records
- **Multi-Provider LLM Support**: Ollama (local), OpenAI, Anthropic with automatic fallback

## 📋 Features

- **Natural Language Queries**: Ask questions in plain English about ICT methodology
- **Comprehensive Backtesting**: Statistical analysis with confidence levels and validation
- **Multi-Agent Coordination**: Intelligent delegation between strategic and technical agents
- **Performance Optimized**: AsyncPG connection pooling, <10 second query resolution
- **Statistical Validation**: Sample size verification, confidence intervals, data coverage analysis

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- PostgreSQL database with ICT schema
- Ollama (recommended) or OpenAI/Anthropic API keys

### Setup

1. **Clone and install dependencies:**
```bash
git clone <repository-url>
cd context-engineer
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Database setup:**
```bash
# Ensure PostgreSQL is running with ICT schema
# Default: postgresql://supabase_admin:postgres@localhost:54334/postgres
```

4. **LLM Provider setup:**

**Option A: Ollama (Recommended)**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull required models
ollama pull llama3.1
ollama pull nomic-embed-text
```

**Option B: OpenAI/Anthropic**
```bash
# Add to .env file:
# OPENAI_API_KEY=your_key_here
# ANTHROPIC_API_KEY=your_key_here
```

## 🚀 Usage

### Command Line Interface

```bash
python -m main
```

### Example Queries

```
📈 ICT Query: What is the success rate of order blocks on EURUSD in the last month?
📈 ICT Query: Analyze fair value gap performance during London session
📈 ICT Query: Show liquidity sweep statistics for major pairs
📈 ICT Query: Explain ICT market structure methodology
```

### Programmatic Usage

```python
from main import ICTBacktestingSystem

async def analyze_market():
    system = ICTBacktestingSystem()
    await system.initialize()
    
    result = await system.process_query(
        "Analyze order block performance on EURUSD last month"
    )
    
    print(result)
    await system.cleanup()
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://supabase_admin:postgres@localhost:54334/postgres` |
| `LLM_PROVIDER` | Primary LLM provider | `ollama` |
| `OLLAMA_HOST` | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | Ollama model name | `llama3.1` |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |

### Database Configuration

```env
DATABASE_POOL_MIN_SIZE=5
DATABASE_POOL_MAX_SIZE=20
DATABASE_COMMAND_TIMEOUT=30
```

### Performance Tuning

```env
ENABLE_QUERY_CACHING=true
CACHE_TTL_SECONDS=3600
MAX_CONCURRENT_QUERIES=10
```

## 🧪 Testing

### Run Test Suite

```bash
# All tests
pytest

# Unit tests only
pytest -m unit

# Integration tests
pytest -m integration

# Performance tests
pytest -m performance

# Specific test file
pytest tests/test_agents.py -v
```

### Test Categories

- **Unit Tests**: Individual component testing with mocks
- **Integration Tests**: Multi-component workflow testing
- **Performance Tests**: Response time and throughput validation
- **Database Tests**: Connection pooling and query execution

## 📊 ICT Functions Available

| Function | Description |
|----------|-------------|
| `ict_order_blocks` | Identifies Order Block formations |
| `ict_fair_value_gaps` | Detects Fair Value Gap patterns |
| `ict_liquidity_sweeps` | Analyzes liquidity sweep events |
| `ict_market_structure` | Market structure and trend analysis |
| `ict_session_analysis` | Session-based performance metrics |
| `ict_premium_discount` | Premium/discount zone calculations |
| `ict_institutional_candles` | Institutional candle patterns |
| `ict_optimal_trade_entry` | Optimal entry point analysis |
| `ict_backtesting_summary` | Comprehensive backtesting results |
| `ict_time_based_analysis` | Time window performance analysis |

## 🔍 System Monitoring

### Health Check

```bash
# Check system status
curl http://localhost:8000/health

# Database connectivity
python -c "from database import DatabaseManager; import asyncio; asyncio.run(DatabaseManager().health_check())"
```

### Performance Metrics

- **Query Classification Accuracy**: >90% target
- **SQL Function Selection Accuracy**: >95% target  
- **End-to-End Response Time**: <10 seconds target
- **Statistical Validation**: All results include confidence levels

## 🛡️ Security

- **Parameterized Queries**: SQL injection prevention
- **Environment Variables**: No hardcoded credentials
- **Input Validation**: Pydantic model validation
- **Usage Limits**: Cost control and rate limiting

## 🐛 Troubleshooting

### Common Issues

**Database Connection Failed**
```bash
# Check PostgreSQL status
pg_isready -h localhost -p 54334

# Verify credentials in .env
echo $DATABASE_URL
```

**Ollama Model Not Found**
```bash
# List available models
ollama list

# Pull required model
ollama pull llama3.1
```

**Import Errors**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Debug Mode

```bash
# Enable debug logging
export DEBUG_MODE=true
export LOG_LEVEL=DEBUG

python -m main
```

## 📈 Performance Benchmarks

- **Query Processing**: <2 seconds average
- **Database Queries**: <500ms average
- **Memory Usage**: <512MB typical
- **Concurrent Users**: 10+ supported

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests (`pytest`)
4. Commit changes (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inner Circle Trader (ICT) methodology
- Pydantic AI framework
- AsyncPG PostgreSQL driver
- Ollama local LLM inference
