# Planning Guide - Coordinator Agent

## Query Processing Workflow

### Step 1: Query Classification

#### RAG-First Queries
Indicators: References to previous work, historical context, or stored analysis
- "What did our previous analysis show..."
- "Based on our last report..."
- "Update our existing research on..."
- "Compare with our baseline from..."

**Processing**: Query RAG memory first, proceed to backtesting only if context insufficient.

#### Backtesting-First Queries
Indicators: Request for fresh analysis, performance questions, current data needs
- "Which [instrument] performs best..."
- "What's the current correlation between..."
- "How often do [pattern] occur..."
- "Compare performance across..."

**Processing**: Skip RAG, route directly to backtesting sub-agent.

#### Hybrid Queries
Indicators: Combination of historical reference and new analysis request
- "Update our Q3 analysis with recent data"
- "How has performance changed since our last study"
- "Extend previous correlation study to include..."

**Processing**: RAG for context, then backtesting for new analysis, synthesize both.

### Step 2: Strategic Parameter Extraction

#### Analysis Strategy Classification
- **Performance Analysis**: Success rates, efficiency metrics, comparative studies
- **Correlation Study**: Relationship analysis, strength measurements, statistical significance
- **Structure Detection**: Pattern identification, frequency analysis, timing studies

#### Trading Context Identification
- **Scalping Focus**: Short-term patterns, high-frequency analysis, session-specific
- **Swing Trading**: Medium-term patterns, multi-day analysis, structure-based
- **Position Analysis**: Long-term trends, fundamental pattern correlation

#### Temporal Scope Determination
- **Recent Performance**: Last 30 days, current market conditions
- **Historical Pattern**: 3-6 months, established trend identification
- **Specific Period**: User-defined date range or event-based timeframe

#### Asset Focus Classification
- **Major Pairs**: EURUSD, GBPUSD, USDJPY (highest liquidity, most reliable data)
- **Cross Pairs**: EURGBP and other non-USD pairs
- **Specific Symbol**: User-mentioned instrument with validation

#### Session Relevance Assessment
- **High Liquidity**: London + New York sessions (for scalping/day trading context)
- **All Sessions**: Equal weight to Asian, London, New York (for structure analysis)
- **Specific Session**: User-mentioned session or context-implied session focus

#### Quality Requirements Setting
- **High Confidence**: Minimum sample sizes, strict statistical thresholds
- **Balanced**: Moderate confidence with reasonable sample sizes
- **Broad Coverage**: Maximum data inclusion, lower confidence acceptable

### Step 3: RAG Memory Consultation

#### Search Strategy
- Extract key terms from strategic classification
- Search for matching analysis types and instruments
- Include broader context if exact match not available

#### Sufficiency Assessment
RAG results sufficient when:
- Analysis type matches current request
- Instrument coverage overlaps significantly
- Data recency within acceptable threshold (7 days for performance data)
- Results include confidence metrics and sample sizes

#### Context Integration
- Use RAG results as baseline for comparison
- Identify gaps requiring new analysis
- Preserve historical insights for response synthesis

### Step 4: Sub-Agent Request Formulation

Generate strategic guidance for backtesting sub-agent:

```json
{
  "analysis_strategy": "[performance_analysis|correlation_study|structure_detection]",
  "trading_context": "[scalping|swing_trading|position_analysis]",
  "temporal_scope": "[recent_performance|historical_pattern|specific_period]",
  "asset_focus": "[major_pairs|cross_pairs|specific_symbol]",
  "session_relevance": "[high_liquidity|all_sessions|specific_session]",
  "quality_requirements": "[high_confidence|balanced|broad_coverage]"
}
```

### Step 5: Response Synthesis

#### Single Source Responses (RAG-only or Backtesting-only)
- Present results directly with confidence metrics
- Include data coverage and sample size information
- Suggest follow-up analysis opportunities

#### Multi-Source Responses (RAG + Backtesting)
- Lead with historical context from RAG
- Present new analysis results
- Highlight changes, confirmations, or contradictions
- Synthesize insights from both sources

#### Error and Limitation Handling
- Explain data coverage limitations clearly
- Suggest alternative approaches when requested analysis unavailable
- Provide partial results when full analysis not feasible
- Include confidence assessments for all presented data

## Decision Trees

### Context Classification Tree
```
User mentions specific timeframe? → Use timeframe context
├─ Mentions "scalping"/"quick"/"fast" → scalping context
├─ Mentions "swing"/"daily"/"weekly" → swing_trading context
└─ No specific mention → infer from analysis type

Analysis involves correlation/relationship? → correlation_study
├─ Analysis involves performance/success/rate? → performance_analysis  
└─ Analysis involves patterns/structure/breaks? → structure_detection
```

### Temporal Scope Decision
```
User specifies date range? → specific_period
├─ User mentions "recent"/"current"/"latest" → recent_performance
├─ User mentions "historical"/"pattern"/"trend" → historical_pattern
└─ No temporal indicator → recent_performance (default)
```

### Quality vs Coverage Trade-off
```
User emphasizes "reliable"/"confident"/"significant" → high_confidence
├─ User asks for "overview"/"general"/"broad" → broad_coverage
└─ No quality indicator → balanced (default)
```

## Error Recovery Strategies

### Insufficient RAG Results
- Proceed to backtesting analysis
- Note limitation in response
- Store new results for future RAG queries

### Backtesting Sub-Agent Failures
- Retry with simplified parameters
- Fall back to RAG-only response if available
- Explain limitation and suggest alternatives
- Request manual verification if persistent issues

### Parameter Validation Failures
- Convert to nearest valid parameters automatically
- Explain substitutions made to user
- Confirm major changes with user before proceeding

## Response Quality Standards

### Required Elements
- Data source identification (RAG, backtesting, or both)
- Confidence metrics and sample sizes for all quantitative claims
- Coverage assessment and data quality indicators
- Clear limitation statements when applicable

### Formatting Requirements
- Lead with key insights and actionable information
- Include specific metrics (percentages, counts, timeframes)
- Structure complex responses with clear sections
- Provide follow-up suggestions when appropriate

### Success Indicators
- Query intent correctly identified and addressed
- Appropriate data sources selected and utilized
- Results presented with proper confidence context
- User receives actionable insights within system constraints