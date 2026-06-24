"""
Data Loader Module
Loads stock data from CSV files for backtesting
"""

import pandas as pd
import sys

sys.path.append('..')
from config import STOCKS, DATA_RAW_PATH


class DataLoader:
    """
    Loads stock data from CSV files
    """
    
    def __init__(self, data_path=None):
        """
        Initialize data loader
        
        Args:
            data_path (str): Path to CSV files
        """
        self.data_path = data_path or DATA_RAW_PATH
    
    
    def load_stock(self, ticker):
        """
        Load single stock from CSV
        
        Args:
            ticker (str): Stock ticker
            
        Returns:
            pandas.DataFrame: OHLCV data or None if error
        """
        try:
            filepath = f"{self.data_path}{ticker}.csv"
            
            # Load CSV with Date as index
            data = pd.read_csv(filepath)
            data['Date'] = pd.to_datetime(data['Date'])
            data = data.set_index('Date')
            
            # Convert to numeric
            for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                data[col] = pd.to_numeric(data[col], errors='coerce')
            
            # Remove NaN rows
            data = data.dropna()
            
            return data
            
        except Exception as e:
            print(f"Error loading {ticker}: {str(e)}")
            return None
    
    
    def load_all_stocks(self, tickers=None):
        """
        Load all stocks
        
        Args:
            tickers (list): List of tickers to load (default: from config)
            
        Returns:
            dict: {ticker: DataFrame}
        """
        if tickers is None:
            tickers = STOCKS
        
        print(f"Loading data from CSV files...")
        all_data = {}
        loaded = 0
        
        for ticker in tickers:
            data = self.load_stock(ticker)
            if data is not None:
                all_data[ticker] = data
                loaded += 1
                print(f"  Loaded {ticker} ({len(data)} days)")
            else:
                print(f"  Failed to load {ticker}")
        
        print(f"Successfully loaded {loaded}/{len(tickers)} stocks\n")
        return all_data