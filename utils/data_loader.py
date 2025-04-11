import yfinance as yf
from utils.date_utils import get_closest_trading_day
import pandas as pd
from datetime import datetime, timedelta

def download_stock_data(tickers, start_date, end_date, pickle_file=None, tickers_source=None, top_n=0, interval="1d"):
    """
    Download daily stock price data for the specified tickers and date range.
    """
    
    # Add buffer days before start date to calculate returns properly
    start_buffer = datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=5)
    
    try:
        if(pickle_file is not None):
            stock_data = pd.read_pickle(pickle_file)
        elif(tickers_source is not None):
            stock_data = generate_stock_data(
                tickers_source=tickers_source, 
                start_date=start_date, 
                end_date=end_date, 
                interval=interval, 
                top_n=top_n, 
                to_pickle=False,
             )
        else:
            print(f"Error downloading stock data. You must have a pickle file or a ticker source file.")
            return None, tickers
        
        # Handle failed tickers
        valid_tickers = [ticker for ticker in tickers if ticker in stock_data.columns.levels[0]]
        failed_tickers = [ticker for ticker in tickers if ticker not in stock_data.columns.levels[0]]
        
        if failed_tickers:
            print(f"Failed to download data for {len(failed_tickers)} tickers.")
        
        print(f"Successfully downloaded data for {len(valid_tickers)} tickers.")
        tickers = valid_tickers
        
        # Took out returning failed tickers. Can put this back in if necessary
        return valid_tickers, stock_data
        
    except Exception as e:
        print(f"Error downloading stock data: {e}")
        return None, tickers

def extract_top_tickers_from_csv(csv_file, top_n=10):
    try:
        # Read the CSV file
        try:
            csv_data = pd.read_csv(csv_file)
        except FileNotFoundError:
            print(f"Error: File '{csv_file}' not found.")
            return []
        except pd.errors.EmptyDataError:
            print(f"Error: File '{csv_file}' is empty.")
            return []
        except pd.errors.ParserError:
            print(f"Error: Unable to parse '{csv_file}'. Check if it's a valid CSV file.")
            return []
        
        # Check if required columns exist
        if 'Weight' not in csv_data.columns:
            print("Error: 'Weight' column not found in the CSV file.")
            return []
        if 'Symbol' not in csv_data.columns:
            print("Error: 'Symbol' column not found in the CSV file.")
            return []
        
        # Sort by Weight column in descending order
        sorted_data = csv_data.sort_values('Weight', ascending=False)
        
        # Handle case when data has fewer rows than requested top_n
        actual_n = min(top_n, len(sorted_data))
        if actual_n < top_n:
            print(f"Warning: Only {actual_n} tickers found, fewer than requested {top_n}.")
        
        # Take only the top n tickers
        top_tickers = sorted_data.head(actual_n)
        
        # Extract the symbols
        symbols = top_tickers['Symbol'].tolist()
        
        # Check for empty symbols list
        if not symbols:
            print("Warning: No ticker symbols were extracted.")
            return []
        
        # print(f"Selected top {len(symbols)} tickers by weight: {symbols}")
        
        return symbols
        
    except Exception as e:
        print(f"Unexpected error occurred: {str(e)}")
        return []

# Read the CSV file to extract the symbols and weights
# Read the CSV file to extract the symbols and weights
def extract_weights_from_csv(csv_file, top_n=10):
    try:
        # Read the CSV file
        try:
            csv_data = pd.read_csv(csv_file)
        except FileNotFoundError:
            print(f"Error: File '{csv_file}' not found.")
            return {}
        except pd.errors.EmptyDataError:
            print(f"Error: File '{csv_file}' is empty.")
            return {}
        except pd.errors.ParserError:
            print(f"Error: Unable to parse '{csv_file}'. Check if it's a valid CSV file.")
            return {}
        
        # Check if required columns exist
        if 'Symbol' not in csv_data.columns:
            print("Error: 'Symbol' column not found in the CSV file.")
            return {}
        if 'Weight' not in csv_data.columns:
            print("Error: 'Weight' column not found in the CSV file.")
            return {}
        
        # Check for duplicate symbols and warn the user
        if csv_data['Symbol'].duplicated().any():
            print("Warning: Duplicate symbols found in the CSV file. Using the last occurrence of each symbol.")
            # Keep the last occurrence of each symbol
            csv_data = csv_data.drop_duplicates(subset=['Symbol'], keep='last')
        
        # Sort by Weight column in descending order if top_n is specified
        if top_n is not None:
            # Sort by Weight column in descending order
            sorted_data = csv_data.sort_values('Weight', ascending=False)
            
            # Handle case when data has fewer rows than requested top_n
            actual_n = min(top_n, len(sorted_data))
            if actual_n < top_n:
                print(f"Warning: Only {actual_n} tickers found, fewer than requested {top_n}.")
            
            # Take only the top n tickers
            csv_data = sorted_data.head(actual_n)
            
            #print(f"Selected top {len(csv_data)} tickers by weight")
        
        # Create a dictionary mapping Symbol to Weight
        weights_dict = dict(zip(csv_data['Symbol'], csv_data['Weight']))
        
        # Check if the dictionary is empty
        if not weights_dict:
            print("Warning: No symbol-weight pairs were extracted.")
            
        return weights_dict
        
    except Exception as e:
        print(f"Unexpected error occurred: {str(e)}")
        return {}

def generate_stock_data(tickers_source, start_date, end_date, interval="1d", top_n=500, to_pickle=False, save_location="pickle_files/top"):

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
    
    if to_pickle is True:
        ticker_data_location = f"{save_location}-{top_n}-{start_date}-{end_date}.pkl"
        # Send data to pickle file for pickup later. 
        ticker_data.to_pickle(ticker_data_location)

    return ticker_data
