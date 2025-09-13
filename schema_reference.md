# Schema Reference - ICT Backtesting Database

## Database Connection
```
postgresql://supabase_admin:postgres@localhost:54334/postgres
```

## Core Schemas

### 1. market_data
Primary schema for OHLCV and tick data storage.

#### Key Table: `ohlcv`
- **Records**: 7,081,584 rows
- **Purpose**: Store all candlestick data with ICT-specific calculations
- **Unique Constraint**: (symbol, timeframe, timestamp)

**Critical Fields**:
- Basic OHLCV: open, high, low, close, volume
- ICT Metrics: range_points, body_size, upper_wick, lower_wick
- Conditional Fields:
  - `session`: Present for intraday (15m, 1h, 4h), NULL for daily/weekly
  - `time_of_day`: Present for intraday, NULL for daily/weekly
  - `quarter`: Present for daily/weekly, NULL for intraday

### 2. ict_analysis
Schema for all ICT pattern detection and analysis results.

#### Key Tables:
- **order_blocks**: Institutional order block detection and performance
  - Track respect rates, reaction metrics, session formation
  - Quality grades: institutional, high_quality, medium_quality, low_quality
  
- **fair_value_gaps**: Imbalance detection and fill tracking
  - Gap types: bullish_fvg, bearish_fvg, equilibrium
  - Fill status: unfilled, partially_filled, completely_filled
  
- **market_structure**: BOS, CHoCH, swing points
  - Structure types: BOS, CHoCH, swing_high, swing_low
  - Confirmation and invalidation tracking
  
- **session_analytics**: Session-specific performance metrics
  - Range analysis, liquidity events, structure shifts
  - Volume profiles and efficiency metrics

### 3. correlations
Cross-asset relationship analysis.

#### Key Table: `pair_correlations`
- Session-specific correlations (Asian, London, New York)
- Volatility correlations and lead-lag analysis
- Statistical significance metrics (p-values, confidence intervals)

### 4. backtesting
Strategy testing and trade analysis.

#### Key Tables:
- **ict_backtest_runs**: Test configuration and aggregate results
- **ict_trades**: Individual trade records with ICT context

### 5. vector_storage & rag_memory
RAG system for historical context and pattern matching.

#### Key Tables:
- **analysis_history**: Historical query results with embeddings
- **function_documentation**: SQL function reference with embeddings
- **ict_patterns**: Pattern knowledge base
- **performance_insights**: Cached insights for quick retrieval

## Supported Enums

### supported_symbol (15 assets)
```sql
'audusd', 'eurusd', 'eurgbp', 'gbpusd', 'grxeur', 
'jpxjpy', 'nsxusd', 'spxuds', 'ukxgbp', 'usdcad', 
'usdchf', 'usdjpy', 'wtiusd', 'xagusd', 'xauusd'
```

### supported_timeframe (5 timeframes)
```sql
'15m', '1h', '4h', '1d', '1w'
```

### session_type (3 sessions)
```sql
'Asian', 'London', 'New York'
```

## Data Coverage

### Forex Pairs
- **Major Pairs** (EURUSD, GBPUSD, USDJPY, USDCHF, USDCAD, AUDUSD): 2000-2024
- **Cross Pairs** (EURGBP): 2002-2024

### Metals
- **XAUUSD, XAGUSD**: 2009-2024

### Indices
- **GRXEUR, JPXJPY, NSXUSD, SPXUDS, UKXGBP**: 2010+ (variable coverage)

### Commodities
- **WTIUSD**: 2009-2024

## Conditional Field Logic

### Intraday Timeframes (15m, 1h, 4h)
- ✅ session (required)
- ✅ time_of_day (required)
- ✅ day_of_week (required)
- ❌ quarter (NULL)

### Daily Timeframe (1d)
- ❌ session (NULL)
- ❌ time_of_day (NULL)
- ✅ day_of_week (required)
- ✅ quarter (required)

### Weekly Timeframe (1w)
- ❌ session (NULL)
- ❌ time_of_day (NULL)
- ❌ day_of_week (NULL)
- ✅ quarter (required)

## Key Indexes for Performance

### Primary Query Patterns
```sql
-- Symbol + Timeframe + Time Range
idx_ohlcv_symbol_tf_time ON (symbol, timeframe, timestamp DESC)

-- Session-based queries (intraday only)
idx_ohlcv_session_time ON (session, timestamp DESC) WHERE session IS NOT NULL

-- Order blocks by validity and quality
idx_order_blocks_symbol_valid_quality ON (symbol, still_valid, ob_quality, created_timestamp DESC)

-- Vector similarity search (RAG)
idx_analysis_query_embedding USING hnsw (query_embedding vector_cosine_ops)
```

## Query Optimization Guidelines

### 1. Always Filter by Symbol and Timeframe First
```sql
WHERE symbol = 'eurusd'::supported_symbol 
  AND timeframe = '1h'::supported_timeframe
```

### 2. Use Enum Casting for Type Safety
```sql
-- Correct
WHERE symbol = 'eurusd'::supported_symbol

-- Incorrect (will fail)
WHERE symbol = 'eurusd'
```

### 3. Handle Conditional Fields Properly
```sql
-- For intraday analysis
WHERE timeframe IN ('15m', '1h', '4h') 
  AND session = 'London'::session_type

-- For daily/weekly (skip session filter)
WHERE timeframe IN ('1d', '1w')
  -- No session filter here
```

### 4. Statistical Significance Thresholds
- **High Confidence**: n ≥ 20, coverage ≥ 80%
- **Balanced**: n ≥ 10, coverage ≥ 70%
- **Broad Coverage**: n ≥ 5, coverage ≥ 50%

## Common Query Patterns

### 1. Order Block Performance Analysis
```sql
SELECT symbol, ob_type, ob_quality, 
       AVG(respect_percentage) as avg_respect,
       COUNT(*) as total_blocks
FROM ict_analysis.order_blocks
WHERE symbol = ANY(ARRAY['eurusd', 'gbpusd']::supported_symbol[])
  AND still_valid = TRUE
  AND times_tested >= 2
GROUP BY symbol, ob_type, ob_quality
HAVING COUNT(*) >= 5;
```

### 2. Session-Specific Analysis
```sql
SELECT symbol, session, 
       AVG(session_range_pips) as avg_range
FROM ict_analysis.session_analytics
WHERE symbol = 'eurusd'::supported_symbol
  AND session IN ('London', 'New York')::session_type[]
  AND date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY symbol, session;
```

### 3. Correlation Analysis
```sql
SELECT base_symbol, correlated_symbol,
       correlation_coefficient,
       london_session_correlation,
       ny_session_correlation
FROM correlations.pair_correlations
WHERE base_symbol = 'eurusd'::supported_symbol
  AND timeframe = '1h'::supported_timeframe
  AND correlation_period_days = 30
ORDER BY ABS(correlation_coefficient) DESC;
```

## Error Handling Patterns

### 1. Invalid Symbol/Timeframe
```sql
-- Will raise: invalid input value for enum
-- Handle in application layer with proper enum validation
```

### 2. Missing Session Data
```sql
-- Check session availability first
SELECT COUNT(*) FILTER (WHERE session IS NOT NULL) as session_records
FROM market_data.ohlcv
WHERE symbol = ? AND timeframe = ?;
```

### 3. Insufficient Data Coverage
```sql
-- Always check coverage before analysis
SELECT validate_symbol_timeframe_availability(
  'eurusd'::supported_symbol,
  '1h'::supported_timeframe,
  start_date,
  end_date
);
```

## Performance Tips

1. **Use Batch Processing** for multiple symbols/timeframes
2. **Leverage Indexes** - queries should use indexed columns
3. **Limit Date Ranges** - start with smaller ranges, expand if needed
4. **Cache Correlations** - they're expensive to calculate
5. **Check Data Availability** before running complex analyses

## Vector Storage Integration

### Embedding Dimensions
- **OpenAI**: 1536 dimensions (text-embedding-3-small)
- **Ollama**: 768 dimensions (nomic-embed-text)

### Similarity Search
```sql
-- Find similar historical analyses
SELECT * FROM rag_memory.search_similar_analyses(
  query_embedding,  -- vector(1536)
  limit := 5,
  similarity_threshold := 0.7
);
```

## System Functions Quick Reference

### Validation Functions
- `validate_symbol_timeframe_availability()` - Check data coverage
- `calculate_data_coverage_stats()` - Detailed coverage metrics
- `get_system_status()` - Overall system health

### Analysis Functions
- `detect_order_blocks_v2()` - Order block detection
- `analyze_market_structure_flexible()` - Market structure analysis
- `analyze_correlations_v2()` - Correlation calculations
- `execute_batch_analysis()` - Batch processing

### Utility Functions
- `get_optimal_analysis_timeframe()` - Parameter optimization
- `process_ict_llm_query_v2()` - Natural language processing
- `convert_legacy_query()` - Legacy compatibility