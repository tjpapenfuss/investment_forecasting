from utils.data_loader import generate_stock_data


if __name__ == '__main__':
    tickers_source='C:/Users/tjpap/sandbox/investment_forecasting/data/custom_allocation.csv'
    ticker_data = generate_stock_data(
        tickers_source=tickers_source, 
        start_date="2020-01-01", 
        end_date="2022-01-01", 
        interval="1d", 
        top_n=50, 
        to_pickle=True,
        save_location="pickle_files/top"
    )
    tickers_source='C:/Users/tjpap/sandbox/investment_forecasting/data/SPY.csv'
    ticker_data = generate_stock_data(
        tickers_source=tickers_source, 
        start_date="2020-01-01", 
        end_date="2022-01-01", 
        interval="1d", 
        top_n=1, 
        to_pickle=True,
        save_location="pickle_files/spy"
    )