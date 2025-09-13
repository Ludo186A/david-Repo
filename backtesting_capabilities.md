# Backtesting Capabilities - Strategic Analysis Reference

## Available Analysis Strategies

### Performance Analysis
**Strategic Focus**: Success rates, efficiency metrics, comparative performance studies

**Applicable Contexts**:
- Scalping: High-frequency pattern success rates, session-based performance
- Swing Trading: Multi-day pattern reliability, structure-based success metrics  
- Position Analysis: Long-term pattern consistency, trend-following effectiveness

**Quality Considerations**:
- High Confidence: Sample sizes >100, statistical significance testing
- Balanced: Sample sizes >30, moderate confidence requirements
- Broad Coverage: Include all available data, accept lower confidence thresholds

**Temporal Applications**:
- Recent Performance: Focus on last 30 days for current market conditions
- Historical Pattern: 3-6 months for established trend identification
- Specific Period: Event-driven analysis, user-defined timeframes

### Correlation Study  
**Strategic Focus**: Relationship analysis, strength measurements, multi-asset dependencies

**Applicable Contexts**:
- Scalping: Short-term correlation patterns, session-specific relationships
- Swing Trading: Daily/weekly correlation stability, trend correlation analysis
- Position Analysis: Long-term dependency patterns, fundamental correlations

**Quality Considerations**:
- High Confidence: Minimum 60 data points, p-value <0.05
- Balanced: Minimum 30 data points, moderate statistical thresholds
- Broad Coverage: All available paired data, descriptive statistics focus

**Temporal Applications**:
- Recent Performance: Current market regime correlation patterns
- Historical Pattern: Stable relationship identification over extended periods
- Specific Period: Event-impact correlation analysis, regime-change studies

### Structure Detection
**Strategic Focus**: Pattern identification, frequency analysis, timing studies

**Applicable Contexts**:
- Scalping: Intraday structure patterns, session-based structure frequency
- Swing Trading: Daily structure patterns, multi-day structure sequences
- Position Analysis: Weekly/monthly structure trends, long-term pattern evolution

**Quality Considerations**:
- High Confidence: Clear pattern definitions, validated detection criteria
- Balanced: Moderate pattern thresholds, reasonable detection sensitivity
- Broad Coverage: Inclusive pattern detection, exploratory analysis

**Temporal Applications**:
- Recent Performance: Current structure patterns, immediate market context
- Historical Pattern: Established structure frequencies, seasonal pattern analysis
- Specific Period: Event-driven structure changes, market regime transitions

## Strategic Decision Framework

### Context-Driven Parameter Selection

#### Scalping Focus
- **Asset Priority**: Major pairs (highest liquidity)
- **Session Priority**: High liquidity sessions (London + New York)
- **Temporal Priority**: Recent performance (immediate relevance)
- **Quality Priority**: Balanced (speed vs accuracy trade-off)

#### Swing Trading Focus  
- **Asset Priority**: Major pairs + selected cross pairs
- **Session Priority**: All sessions (comprehensive view)
- **Temporal Priority**: Historical patterns (established trends)
- **Quality Priority**: High confidence (reliability for position sizing)

#### Position Analysis Focus
- **Asset Priority**: All available assets (diversification insights)
- **Session Priority**: All sessions (complete market cycle view)
- **Temporal Priority**: Historical patterns (long-term stability)
- **Quality Priority**: High confidence (fundamental decision support)

### Quality vs Coverage Trade-offs

#### High Confidence Requirements
- Minimum sample sizes enforced
- Statistical significance testing mandatory
- Confidence intervals and p-values included
- Conservative thresholds applied

**Trade-off**: Smaller result sets, potential missed opportunities

#### Broad Coverage Requirements
- Maximum data inclusion prioritized
- Descriptive statistics focus over inferential
- Pattern exploration over pattern confirmation
- Inclusive thresholds applied

**Trade-off**: Lower statistical confidence, higher false positive risk

#### Balanced Approach
- Moderate sample size requirements
- Basic statistical validation
- Confidence metrics included
- Reasonable detection thresholds

**Trade-off**: Compromise between coverage and confidence

### Temporal Scope Optimization

#### Recent Performance (30 days default)
- **Advantages**: Current market relevance, immediate applicability
- **Limitations**: Limited sample sizes, potential regime bias
- **Best For**: Trading decision support, current market assessment

#### Historical Pattern (3-6 months default)
- **Advantages**: Larger sample sizes, pattern stability assessment
- **Limitations**: Potential regime mixing, reduced immediate relevance
- **Best For**: Strategy development, baseline establishment

#### Specific Period (user-defined)
- **Advantages**: Targeted analysis, event-specific insights
- **Limitations**: Potential cherry-picking, limited generalizability
- **Best For**: Event analysis, hypothesis testing

## Asset Focus Guidelines

### Major Pairs (EURUSD, GBPUSD, USDJPY)
- **Data Quality**: Excellent (2000-2024)
- **Sample Sizes**: Largest available
- **Reliability**: Highest statistical confidence
- **Recommended For**: All analysis types, baseline studies

### Cross Pairs (EURGBP, etc.)
- **Data Quality**: Good (2002-2024)
- **Sample Sizes**: Moderate
- **Reliability**: Good statistical confidence
- **Recommended For**: Diversification studies, correlation analysis

### Metals (XAUUSD, XAGUSD)  
- **Data Quality**: Good (2009-2024)
- **Sample Sizes**: Moderate
- **Reliability**: Moderate statistical confidence
- **Recommended For**: Alternative asset analysis, correlation studies

### Indices (Limited availability)
- **Data Quality**: Variable (2010+, gaps possible)
- **Sample Sizes**: Limited
- **Reliability**: Lower statistical confidence
- **Recommended For**: Exploratory analysis only, require validation

## Session Relevance Strategy

### High Liquidity Focus
- **Target Sessions**: London + New York
- **Rationale**: Maximum institutional participation, highest reliability
- **Best For**: Scalping context, performance analysis
- **Quality Impact**: Higher confidence due to institutional participation

### All Sessions Inclusive
- **Target Sessions**: Asian + London + New York
- **Rationale**: Complete market cycle coverage, comprehensive patterns
- **Best For**: Structure detection, comprehensive correlation studies
- **Quality Impact**: Larger sample sizes, potential session-specific noise

### Specific Session Analysis
- **Target Sessions**: User-specified or context-implied
- **Rationale**: Focused analysis, session-specific insights  
- **Best For**: Session comparison studies, targeted trading strategies
- **Quality Impact**: Reduced sample sizes, higher session-specific confidence

## Output Strategy Selection

### Performance-Focused Outputs
- Emphasize success rates, reaction metrics, efficiency measures
- Include confidence intervals and statistical significance
- Focus on actionable insights for trading decisions
- Provide comparative rankings and performance distributions

### Relationship-Focused Outputs  
- Emphasize correlation coefficients, dependency measures
- Include statistical significance and stability metrics
- Focus on multi-asset interactions and regime analysis
- Provide correlation matrices and relationship evolution

### Pattern-Focused Outputs
- Emphasize frequency analysis, timing statistics
- Include pattern reliability and detection confidence
- Focus on structure identification and sequence analysis
- Provide pattern distributions and timing characteristics

## Strategic Guidance Summary

The coordinator should select strategic approaches based on:

1. **User Intent Recognition**: Match analysis strategy to query type
2. **Context Optimization**: Align trading context with appropriate parameters  
3. **Quality-Coverage Balance**: Choose requirements based on intended use
4. **Asset-Session Matching**: Optimize asset and session selection for analysis type
5. **Output Alignment**: Ensure output strategy matches user information needs

Each strategic choice impacts the technical execution approach while maintaining separation between strategic decision-making (coordinator) and technical implementation (sub-agent).