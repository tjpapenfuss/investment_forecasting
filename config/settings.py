# Default configuration settings
DEFAULT_CONFIG = {
    "initial_investment": 100000,
    "recurring_investment": 4000,
    "investment_frequency": "monthly",
    "portfolio_allocation": "equal",
    "start_date": "2020-01-01",
    "end_date": "2022-01-01",
    "sell_trigger": -10,
    "tickers_source": "C:/Users/tjpap/sandbox/investment_forecasting/data/custom_allocation.csv", 
    "top_n": 50,
    "rebalance_frequency":"yearly",
    "rebalance_threshold":50,
    "pickle_file":"C:/Users/tjpap/sandbox/investment_forecasting/pickle_files/top-50-2020-01-01-2022-01-01.pkl"
}

def validate_config(config):
    """Validate configuration parameters."""
    # Validation logic here
    return config