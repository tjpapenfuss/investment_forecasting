import yfinance as yf
import json
from utils.data_loader import extract_top_tickers_from_csv

def generate_stock_data(tickers_source, start_date, end_date, interval="1d", top_n=500, to_pickle=False):

    # Get tickers from configuration
    tickers = extract_top_tickers_from_csv(
        csv_file=tickers_source, 
        top_n=top_n
    )

    ticker_data = yf.download(
                    tickers=tickers,
                    start=start_date,
                    end=end_date,
                    interval=interval,
                    group_by='ticker'
                )
    
    spy_data = yf.download(
                    tickers='SPY',
                    start=start_date,
                    end=end_date,
                    interval=interval,
                    group_by='ticker'
                )
    
    if to_pickle is True:
        spy_pickle_location = f"pickle_files/spy-{start_date}-{end_date}.pkl"
        ticker_data_location = f"pickle_files/top-{top_n}-{start_date}-{end_date}.pkl"
        # Send data to pickle file for pickup later. 
        ticker_data.to_pickle(ticker_data_location)
        spy_data.to_pickle(spy_pickle_location)

    return ticker_data, spy_data