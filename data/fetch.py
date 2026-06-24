
import yfinance as yf
import pandas as pd
import os
from datetime import datetime
import sys

# Import config
sys.path.append('..')  # Go up one folder to find config.py
from config import STOCKS, START_DATE, END_DATE, DATA_RAW_PATH   # data_raw_path is ./raw/


class DataFetcher:
    
    def __init__(self, stocks=None, start_date=None, end_date=None, data_path=None):

        self.stocks = stocks or STOCKS
        self.start_date = start_date or START_DATE
        self.end_date = end_date or END_DATE
        self.data_path = data_path or DATA_RAW_PATH
        
        # Create directory if it doesn't exist
        os.makedirs(self.data_path, exist_ok=True)
        
        print(f" DataFetcher initialized")
        print(f" Stocks: {len(self.stocks)} stocks")
        print(f" Period: {self.start_date} to {self.end_date}")
        print(f" Save path: {self.data_path}")
    
    
    def fetch_stock_data(self, ticker):

        try:
            print(f"\n Downloading {ticker}...", end=' ')
            
            # Download from Yahoo Finance
            data = yf.download(
                ticker,
                start=self.start_date,
                end=self.end_date,
                progress=False  # Don't show progress bar
            )
            
            # Check if we got data
            if data.empty:
                print(f" No data found for {ticker}")
                return None
            
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.droplevel(1)

            print(f" {len(data)} days of data")
            return data
            
        except Exception as e:
            print(f" Error downloading {ticker}: {str(e)}")
            return None
    
    
    '''def save_to_csv(self, ticker, data):
        """
        Save downloaded data to CSV file
        
        Args:
            ticker (str): Stock ticker (e.g., 'AAPL')
            data (pandas.DataFrame): OHLCV data
        """
        try:
            filepath = f"{self.data_path}{ticker}.csv"
            data.to_csv(filepath)
            print(f"   Saved to {filepath}")
            return True
            
        except Exception as e:
            print(f"   Error saving {ticker}: {str(e)}")
            return False'''
        
    def save_to_csv(self, ticker, data):
        try:
            filepath = f"{self.data_path}{ticker}.csv"

            data = data.reset_index()   # Date becomes a normal column

            data.to_csv(filepath, index=False)

            print(f"   Saved to {filepath}")
            return True

        except Exception as e:
            print(f"   Error saving {ticker}: {str(e)}")
            return False

    
    def fetch_all_stocks(self):

        print(f"\n{'='*60}")
        print(f"DOWNLOADING DATA FOR {len(self.stocks)} STOCKS")
        print(f"{'='*60}")
        
        all_data = {}
        successful = 0
        failed = 0
        
        for ticker in self.stocks:
            data = self.fetch_stock_data(ticker)
            
            if data is not None:
                self.save_to_csv(ticker, data)
                all_data[ticker] = data
                successful += 1
            else:
                failed += 1
        
        # Summary
        print(f"\n{'='*60}")
        print(f"DOWNLOAD SUMMARY")
        print(f"{'-'*60}")
        print(f" Successful: {successful}/{len(self.stocks)}")
        print(f" Failed: {failed}/{len(self.stocks)}")
        print(f"{'-'*60}\n")
        
        return all_data
    
    
    def load_from_csv(self, ticker):

        try:
            filepath = f"{self.data_path}{ticker}.csv"
            data = pd.read_csv(filepath, index_col='Date', parse_dates=True)
            print(f" Loaded {ticker} from {filepath}")
            return data
            
        except FileNotFoundError:
            print(f" File not found: {filepath}")
            return None
        except Exception as e:
            print(f" Error loading {ticker}: {str(e)}")
            return None
    
    
    def load_all_from_csv(self):

        print(f"\nLoading data from CSV files...")
        all_data = {}
        
        for ticker in self.stocks:
            data = self.load_from_csv(ticker)
            if data is not None:
                all_data[ticker] = data
        
        print(f" Loaded {len(all_data)}/{len(self.stocks)} stocks\n")
        return all_data
    
    
    def get_data_info(self, ticker):

        data = self.load_from_csv(ticker)
        if data is not None:
            print(f"\n{ticker} Data Info:")
            print(f"  Date range: {data.index[0]} to {data.index[-1]}")
            print(f"  Total days: {len(data)}")
            print(f"  Columns: {', '.join(data.columns)}")
            print(f"\n  First 3 rows:\n{data.head(3)}")
            print(f"\n  Last 3 rows:\n{data.tail(3)}")


# ============================================
# EXAMPLE USAGE
# ============================================
if __name__ == "__main__":
    # Create fetcher
    fetcher = DataFetcher()
    
    # Download all stocks
    data = fetcher.fetch_all_stocks()
    
    # Show info for first stock
    if len(data) > 0:
        first_stock = list(data.keys())[0]
        fetcher.get_data_info(first_stock)