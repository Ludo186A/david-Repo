{
    "function_categories": {
      "data_validation": {
        "description": "Functions for validating data availability and quality",
        "functions": [
          {
            "name": "validate_symbol_timeframe_availability",
            "signature": "(p_symbol supported_symbol, p_timeframe supported_timeframe, p_start_date TIMESTAMP, p_end_date TIMESTAMP)",
            "returns": "JSONB",
            "description": "Validates symbol and timeframe data availability with coverage statistics",
            "strategic_use": ["data_quality_check", "pre_analysis_validation"],
            "execution_complexity": "low",
            "sample_query": "SELECT validate_symbol_timeframe_availability('eurusd', '1h', '2024-01-01', '2024-12-31')"
          },
          {
            "name": "calculate_data_coverage_stats",
            "signature": "(p_symbol supported_symbol, p_timeframe supported_timeframe, p_date_range JSONB DEFAULT NULL)",
            "returns": "JSONB",
            "description": "Calculates comprehensive data coverage statistics including gaps and quality metrics",
            "strategic_use": ["quality_assessment", "gap_analysis"],
            "execution_complexity": "medium",
            "sample_query": "SELECT calculate_data_coverage_stats('gbpusd', '4h', jsonb_build_object('start_date', '2024-01-01', 'end_date', '2024-12-31'))"
          }
        ]
      },
      "order_blocks": {
        "description": "Functions for order block detection and analysis",
        "functions": [
          {
            "name": "detect_order_blocks_v2",
            "signature": "(p_symbol supported_symbol, p_timeframe supported_timeframe, p_start_date TIMESTAMP, p_end_date TIMESTAMP, p_min_displacement INTEGER DEFAULT 3)",
            "returns": "JSONB",
            "description": "Detects order blocks with quality assessment and session filtering",
            "strategic_use": ["performance_analysis", "structure_detection"],
            "execution_complexity": "high",
            "applicable_contexts": ["scalping", "swing_trading"],
            "quality_thresholds": {
              "high_confidence": "institutional_grade = true, times_tested >= 3",
              "balanced": "ob_quality IN ('high_quality', 'medium_quality'), times_tested >= 2",
              "broad_coverage": "all order blocks"
            },
            "sample_query": "SELECT detect_order_blocks_v2('eurusd', '1h', CURRENT_TIMESTAMP - INTERVAL '30 days', CURRENT_TIMESTAMP, 3)"
          }
        ]
      },
      "market_structure": {
        "description": "Functions for market structure analysis",
        "functions": [
          {
            "name": "analyze_market_structure_flexible",
            "signature": "(p_symbols supported_symbol[] DEFAULT NULL, p_timeframes supported_timeframe[] DEFAULT ARRAY['1h'], p_sessions session_type[] DEFAULT NULL, p_date_range JSONB DEFAULT NULL, p_analysis_params JSONB DEFAULT NULL)",
            "returns": "JSONB",
            "description": "Flexible market structure analysis supporting multiple symbols and timeframes",
            "strategic_use": ["structure_detection", "performance_analysis"],
            "execution_complexity": "high",
            "applicable_contexts": ["swing_trading", "position_analysis"],
            "session_handling": "Automatically skips session filtering for daily/weekly timeframes",
            "sample_query": "SELECT analyze_market_structure_flexible(ARRAY['eurusd', 'gbpusd']::supported_symbol[], ARRAY['4h']::supported_timeframe[], ARRAY['London', 'New York']::session_type[])"
          }
        ]
      },
      "correlations": {
        "description": "Functions for correlation analysis",
        "functions": [
          {
            "name": "analyze_correlations_v2",
            "signature": "(p_base_symbols supported_symbol[], p_correlated_symbols supported_symbol[], p_timeframes supported_timeframe[] DEFAULT ARRAY['1h'], p_period_days INTEGER DEFAULT 30, p_sessions session_type[] DEFAULT NULL)",
            "returns": "JSONB",
            "description": "Calculates correlations between asset pairs with session-specific analysis",
            "strategic_use": ["correlation_study"],
            "execution_complexity": "very_high",
            "applicable_contexts": ["position_analysis", "swing_trading"],
            "statistical_requirements": {
              "high_confidence": "sample_size >= 60, p_value < 0.05",
              "balanced": "sample_size >= 30, p_value < 0.10",
              "broad_coverage": "sample_size >= 20"
            },
            "sample_query": "SELECT analyze_correlations_v2(ARRAY['eurusd']::supported_symbol[], ARRAY['gbpusd', 'usdjpy']::supported_symbol[], ARRAY['1h', '4h']::supported_timeframe[], 30)"
          }
        ]
      },
      "batch_processing": {
        "description": "Functions for batch analysis operations",
        "functions": [
          {
            "name": "execute_batch_analysis",
            "signature": "(p_analysis_requests JSONB)",
            "returns": "JSONB",
            "description": "Executes batch analysis for multiple symbols/timeframes",
            "strategic_use": ["multi_asset_analysis", "comprehensive_scanning"],
            "execution_complexity": "variable",
            "request_format": {
              "analysis_type": "order_blocks | market_structure | data_validation",
              "symbol": "supported_symbol",
              "timeframe": "supported_timeframe",
              "start_date": "timestamp",
              "end_date": "timestamp",
              "params": "optional JSONB"
            },
            "sample_query": "SELECT execute_batch_analysis('[{\"analysis_type\": \"order_blocks\", \"symbol\": \"eurusd\", \"timeframe\": \"1h\", \"start_date\": \"2024-01-01\", \"end_date\": \"2024-12-31\"}]'::jsonb)"
          }
        ]
      },
      "llm_query_processing": {
        "description": "Functions for natural language query processing",
        "functions": [
          {
            "name": "process_ict_llm_query_v2",
            "signature": "(p_user_query TEXT, p_session_uuid UUID DEFAULT NULL, p_context JSONB DEFAULT NULL)",
            "returns": "JSONB",
            "description": "Enhanced LLM query processor with enum validation and flexible routing",
            "strategic_use": ["query_interpretation", "automated_analysis"],
            "execution_complexity": "variable",
            "intent_recognition": [
              "order_block_analysis",
              "fair_value_gap_analysis",
              "market_structure_analysis",
              "correlation_analysis",
              "session_analysis",
              "key_levels_analysis",
              "liquidity_analysis",
              "volatility_analysis",
              "data_availability"
            ],
            "sample_query": "SELECT process_ict_llm_query_v2('Show me EURUSD order blocks from London session', gen_random_uuid())"
          }
        ]
      },
      "system_utilities": {
        "description": "System status and configuration functions",
        "functions": [
          {
            "name": "get_system_status",
            "signature": "()",
            "returns": "JSONB",
            "description": "Returns comprehensive system status for all supported assets",
            "strategic_use": ["system_health_check", "data_inventory"],
            "execution_complexity": "medium",
            "sample_query": "SELECT get_system_status()"
          },
          {
            "name": "get_optimal_analysis_timeframe",
            "signature": "(p_analysis_type VARCHAR(50), p_requested_timeframe supported_timeframe DEFAULT NULL)",
            "returns": "JSONB",
            "description": "Returns optimal timeframes for specific analysis types",
            "strategic_use": ["parameter_optimization"],
            "execution_complexity": "low",
            "analysis_types": [
              "scalping",
              "day_trading",
              "swing_trading",
              "position_trading",
              "order_block_analysis",
              "fair_value_gap_analysis",
              "market_structure_analysis",
              "session_analysis",
              "correlation_analysis"
            ],
            "sample_query": "SELECT get_optimal_analysis_timeframe('swing_trading', '4h')"
          }
        ]
      }
    },
    "parameter_mappings": {
      "strategic_to_technical": {
        "analysis_strategy": {
          "performance_analysis": ["detect_order_blocks_v2", "analyze_market_structure_flexible"],
          "correlation_study": ["analyze_correlations_v2"],
          "structure_detection": ["analyze_market_structure_flexible", "detect_order_blocks_v2"]
        },
        "trading_context": {
          "scalping": {
            "preferred_timeframes": ["15m", "1h"],
            "preferred_sessions": ["London", "New York"],
            "quality_priority": "balanced"
          },
          "swing_trading": {
            "preferred_timeframes": ["4h", "1d"],
            "preferred_sessions": "all",
            "quality_priority": "high_confidence"
          },
          "position_analysis": {
            "preferred_timeframes": ["1d", "1w"],
            "preferred_sessions": "all",
            "quality_priority": "high_confidence"
          }
        },
        "temporal_scope": {
          "recent_performance": "30 days",
          "historical_pattern": "90-180 days",
          "specific_period": "user_defined"
        },
        "quality_requirements": {
          "high_confidence": {
            "min_sample_size": 20,
            "min_coverage": 80,
            "statistical_significance": 0.05
          },
          "balanced": {
            "min_sample_size": 10,
            "min_coverage": 70,
            "statistical_significance": 0.10
          },
          "broad_coverage": {
            "min_sample_size": 5,
            "min_coverage": 50,
            "statistical_significance": 0.20
          }
        }
      }
    },
    "execution_guidelines": {
      "function_selection_priority": [
        "1. Check data availability first (validate_symbol_timeframe_availability)",
        "2. Select primary analysis function based on analysis_strategy",
        "3. Apply quality filters based on quality_requirements",
        "4. Include session filters for intraday timeframes only",
        "5. Return structured results with confidence metrics"
      ],
      "error_handling": {
        "insufficient_data": "Return partial results with coverage warning",
        "invalid_parameters": "Convert to nearest valid parameters",
        "execution_timeout": "Return cached results if available",
        "unknown_function": "Fallback to process_ict_llm_query_v2"
      },
      "performance_optimization": {
        "use_batch_processing": "When analyzing multiple symbols/timeframes",
        "cache_correlations": "For repeated correlation queries within 1 hour",
        "limit_date_ranges": "Maximum 1 year for initial queries"
      }
    },
    "supported_enums": {
      "supported_symbol": [
        "audusd", "eurusd", "eurgbp", "gbpusd", "grxeur", 
        "jpxjpy", "nsxusd",