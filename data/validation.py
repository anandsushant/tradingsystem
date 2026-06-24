
import pandas as pd
import os
import sys
#from pathlib import Path

sys.path.append('..')
from config import STOCKS, DATA_RAW_PATH


class DataValidator:
    """
    Validates downloaded data - checks files exist, are readable, and have correct format
    """
    
    def __init__(self, data_path=None):
        """
        Initialize validator
        
        Args:
            data_path (str): Path to CSV files
        """
        self.data_path = data_path or DATA_RAW_PATH
        self.validation_results = {}
    
    
    def check_file_exists(self, ticker):
        """
        Check if CSV file exists for a ticker
        
        Args:
            ticker (str): Stock ticker
            
        Returns:
            bool: True if file exists, False otherwise
        """
        filepath = f"{self.data_path}{ticker}.csv"
        exists = os.path.exists(filepath)
        
        if exists:
            file_size = os.path.getsize(filepath)
            print(f"   {ticker}.csv exists ({file_size/1024:.1f} KB)")
        else:
            print(f"   {ticker}.csv NOT FOUND")
        
        return exists
    
    
    # def load_csv(self, ticker):
    #     """
    #     Load CSV file into pandas DataFrame
        
    #     Args:
    #         ticker (str): Stock ticker
            
    #     Returns:
    #         pandas.DataFrame: Data from CSV or None if error
    #     """
    #     filepath = f"{self.data_path}{ticker}.csv"
        
    #     try:
    #         data = pd.read_csv(filepath, index_col='Date', parse_dates=True)
    #         return data
    #     except FileNotFoundError:
    #         print(f"   File not found: {filepath}")
    #         return None
    #     except Exception as e:
    #         print(f"   Error reading {ticker}: {str(e)}")
    #         return None
        
    def load_csv(self, ticker):
        """
        Load CSV file into pandas DataFrame - simple version

        Args:
            ticker (str): Stock ticker

        Returns:
            pandas.DataFrame: Data from CSV or None if error
        """
        filepath = f"{self.data_path}{ticker}.csv"

        try:
            # Load CSV with Date as index
            data = pd.read_csv(filepath)

            # Set Date column as index
            data['Date'] = pd.to_datetime(data['Date'])
            data = data.set_index('Date')

            return data

        except Exception as e:
            print(f"  Error reading {ticker}: {str(e)}")
            return None
    
    
    def validate_columns(self, ticker, data):
        """
        Check if CSV has required columns
        
        Args:
            ticker (str): Stock ticker
            data (pandas.DataFrame): Data to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        
        if data is None:
            return False
        
        missing = [col for col in required_columns if col not in data.columns]
        
        if missing:
            print(f"   Missing columns: {missing}")
            return False
        else:
            print(f"   All required columns present: {list(data.columns)}")
            return True
    
    
    def validate_data_types(self, ticker, data):
        """
        Check if columns have correct data types
        
        Args:
            ticker (str): Stock ticker
            data (pandas.DataFrame): Data to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if data is None:
            return False
        
        issues = []

        numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in numeric_cols:
            if col in data.columns:
                if not pd.api.types.is_numeric_dtype(data[col]):
                    issues.append(f"{col} is not numeric")
        
        if issues:
            print(f"   Data type issues: {issues}")
            return False
        else:
            print(f"   All data types correct")
            return True
    
    
    def check_missing_values(self, ticker, data):
        """
        Check for missing/NaN values
        
        Args:
            ticker (str): Stock ticker
            data (pandas.DataFrame): Data to validate
            
        Returns:
            bool: True if no missing values, False otherwise
        """
        if data is None:
            return False
        
        missing = data.isnull().sum()
        total_missing = missing.sum()
        
        if total_missing > 0:
            print(f"    Missing values found:")
            for col, count in missing[missing > 0].items():
                print(f"     {col}: {count} NaN values")
            return False
        else:
            print(f"   No missing values")
            return True
    
    
    def check_date_range(self, ticker, data):
        """
        Check date range and gaps
        
        Args:
            ticker (str): Stock ticker
            data (pandas.DataFrame): Data to validate
            
        Returns:
            bool: True if valid, False if not valid
        """
        if data is None or len(data) == 0:
            print(f"   No data rows")
            return False
        
        first_date = data.index[0]
        last_date = data.index[-1]
        total_days = len(data)
        
        print(f"   Date range: {first_date.date()} to {last_date.date()}")
        print(f"   Total trading days: {total_days}")
        
        return True
    
    
    def check_price_sanity(self, ticker, data):
        """
        Check if prices make sense (High >= Low, etc.)
        
        Args:
            ticker (str): Stock ticker
            data (pandas.DataFrame): Data to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if data is None:
            return False
        
        issues = []
        
        # Check if High >= Low
        if (data['High'] < data['Low']).any():
            issues.append("Found days where High < Low (impossible)")
        
        # Check if Close is between High and Low
        if ((data['Close'] > data['High']).any() or (data['Close'] < data['Low']).any()):
            issues.append("Found Close outside High-Low range")
        
        # Check if Open is between High and Low
        if ((data['Open'] > data['High']).any() or (data['Open'] < data['Low']).any()):
            issues.append("Found Open outside High-Low range")
        
        # Check if Volume is positive
        if (data['Volume'] <= 0).any():
            issues.append("Found days with zero/negative volume")
        
        if issues:
            print(f"   Price sanity issues:")
            for issue in issues:
                print(f"     - {issue}")
            return False
        else:
            print(f"   Price data looks valid")
            return True
    
    
    def show_sample_data(self, ticker, data, rows=3):
        """
        Display first and last N rows of data
        
        Args:
            ticker (str): Stock ticker
            data (pandas.DataFrame): Data to display
            rows (int): Number of rows to show
        """
        if data is None or len(data) == 0:
            print(f"   No data to display")
            return
        
        print(f"\n  First {rows} rows:")
        print(data.head(rows).to_string())
        
        print(f"\n  Last {rows} rows:")
        print(data.tail(rows).to_string())
    
    
    def show_statistics(self, ticker, data):
        """
        Display basic statistics
        
        Args:
            ticker (str): Stock ticker
            data (pandas.DataFrame): Data to analyze
        """
        if data is None or len(data) == 0:
            return
        
        print(f"\n  Statistics for {ticker}:")
        print(f"    Close Price - Min: ${data['Close'].min():.2f}, Max: ${data['Close'].max():.2f}, Avg: ${data['Close'].mean():.2f}")
        print(f"    Volume - Avg: {data['Volume'].mean():,.0f} shares")
        print(f"    Daily Return - Avg: {((data['Close'].pct_change().mean()) * 100):.3f}%")
    
    
    def validate_single_stock(self, ticker, verbose=True):
        """
        Validate a single stock file
        
        Args:
            ticker (str): Stock ticker
            verbose (bool): Print details
            
        Returns:
            dict: Validation results
        """
        if verbose:
            print(f"\n{'='*60}")
            print(f"VALIDATING: {ticker}")
            print(f"{'='*60}")
        
        results = {
            'ticker': ticker,
            'file_exists': False,
            'readable': False,
            'columns_valid': False,
            'data_types_valid': False,
            'no_missing_values': False,
            'date_range_valid': False,
            'price_sanity_valid': False,
            'overall_valid': False
        }
        
        # Check file exists
        if not self.check_file_exists(ticker):
            return results
        results['file_exists'] = True
        
        # Load CSV
        if verbose:
            print(f"\nReading CSV...")
        data = self.load_csv(ticker)
        if data is None:
            return results
        results['readable'] = True
        
        # Validate columns
        if verbose:
            print(f"Checking columns...")
        if not self.validate_columns(ticker, data):
            return results
        results['columns_valid'] = True
        
        # Validate data types
        if verbose:
            print(f"Checking data types...")
        if not self.validate_data_types(ticker, data):
            return results
        results['data_types_valid'] = True
        
        # Check missing values
        if verbose:
            print(f"Checking missing values...")
        if not self.check_missing_values(ticker, data):
            return results
        results['no_missing_values'] = True
        
        # Check date range
        if verbose:
            print(f"Checking date range...")
        if not self.check_date_range(ticker, data):
            return results
        results['date_range_valid'] = True
        
        # Check price sanity
        if verbose:
            print(f"Validating prices...")
        if not self.check_price_sanity(ticker, data):
            return results
        results['price_sanity_valid'] = True
        
        # Show sample data
        if verbose:
            self.show_sample_data(ticker, data, rows=3)
            self.show_statistics(ticker, data)
        
        # All checks passed
        results['overall_valid'] = True
        
        if verbose:
            print(f"\n {ticker} is VALID and READABLE \n")
        
        return results
    
    
    def validate_all_stocks(self, verbose=True):
        """
        Validate all stocks
        
        Args:
            verbose (bool): Print details
            
        Returns:
            dict: Results for all stocks
        """
        print(f"\n{'='*70}")
        print(f"VALIDATING ALL {len(STOCKS)} STOCKS")
        print(f"{'='*70}\n")
        
        all_results = {}
        
        for ticker in STOCKS:
            results = self.validate_single_stock(ticker, verbose=False)
            all_results[ticker] = results
            
            # Quick status
            if results['overall_valid']:
                print(f" {ticker}: VALID")
            else:
                print(f" {ticker}: INVALID")
                for key, value in results.items():
                    if not value and key != 'ticker':
                        print(f"   Failed: {key}")
        
        # Summary
        print(f"\n{'='*70}")
        valid_count = sum(1 for r in all_results.values() if r['overall_valid'])
        print(f"SUMMARY: {valid_count}/{len(STOCKS)} stocks are valid and readable")
        print(f"{'='*70}\n")
        
        return all_results
    
    
    def load_all_stocks(self):
        """
        Load all stock data into memory (for use by strategy)
        
        Returns:
            dict: {ticker: DataFrame} for all valid stocks
        """
        print(f"\nLoading all stock data...")
        all_data = {}
        
        for ticker in STOCKS:
            data = self.load_csv(ticker)
            if data is not None:
                all_data[ticker] = data
                print(f"   Loaded {ticker} ({len(data)} days)")
            else:
                print(f"   Failed to load {ticker}")
        
        print(f"\nSuccessfully loaded {len(all_data)}/{len(STOCKS)} stocks\n")
        return all_data


if __name__ == "__main__":
    # Create validator
    validator = DataValidator()
    
    # Option 1: Validate all stocks (quick summary)
    print("QUICK VALIDATION:\n")
    results = validator.validate_all_stocks(verbose=False)
    
    # Option 2: Detailed validation for one stock
    print("\nDETAILED VALIDATION (One Stock):\n")
    validator.validate_single_stock('AAPL', verbose=True)
    
    # Option 3: Load all data for use in strategy
    print("\nLOADING ALL DATA:\n")
    all_data = validator.load_all_stocks()
    
    # Show sample of loaded data
    if all_data:
        ticker = list(all_data.keys())[0]
        print(f"Sample - {ticker} data shape: {all_data[ticker].shape}")
        print(all_data[ticker].head(3))