"""
Base Strategy Module
Abstract base class for all trading strategies
"""

import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
import sys

sys.path.append('..')
from config import VOLUME_MIN_THRESHOLD


class BaseStrategy(ABC):
    """
    Abstract base class for trading strategies
    All specific strategies inherit from this
    """
    
    def __init__(self, name="Strategy"):
        """
        Initialize strategy
        
        Args:
            name (str): Strategy name
        """
        self.name = name
        self.indicators = {}
        self.signals = {}
    
    
    @abstractmethod
    def calculate_indicators(self, data):
        """
        Calculate technical indicators
        MUST be implemented by child strategy
        
        Args:
            data (pandas.DataFrame): OHLCV data
            
        Returns:
            pandas.DataFrame: Data with indicators added
        """
        pass
    
    
    @abstractmethod
    def generate_signals(self, data):
        """
        Generate trading signals (BUY, SELL, HOLD)
        MUST be implemented by child strategy
        
        Args:
            data (pandas.DataFrame): Data with indicators
            
        Returns:
            pandas.Series: Trading signals (1=BUY, -1=SELL, 0=HOLD)
        """
        pass
    
    
    def check_volume(self, data, threshold=None):
        """
        Check if volume meets minimum threshold
        Don't trade if volume is too low (illiquid)
        
        Args:
            data (pandas.DataFrame): OHLCV data
            threshold (int): Minimum volume
            
        Returns:
            pandas.Series: Boolean - True if volume adequate
        """
        if threshold is None:
            threshold = VOLUME_MIN_THRESHOLD
        
        return data['Volume'] >= threshold
    
    
    def check_price_validity(self, data):
        """
        Check if price data is valid
        High >= Low, Close between High and Low, etc.
        
        Args:
            data (pandas.DataFrame): OHLCV data
            
        Returns:
            pandas.Series: Boolean - True if valid
        """
        valid = (
            (data['High'] >= data['Low']) &
            (data['Close'] >= data['Low']) &
            (data['Close'] <= data['High']) &
            (data['Open'] >= data['Low']) &
            (data['Open'] <= data['High']) &
            (data['Volume'] > 0)
        )
        return valid
    
    
    def calculate_returns(self, data):
        """
        Calculate daily returns
        
        Args:
            data (pandas.DataFrame): OHLCV data
            
        Returns:
            pandas.Series: Daily returns as percentage
        """
        returns = data['Close'].pct_change() * 100
        return returns
    
    
    def calculate_sma(self, data, period, column='Close'):
        """
        Calculate Simple Moving Average
        
        Args:
            data (pandas.DataFrame): OHLCV data
            period (int): Number of periods
            column (str): Which column to average (default: Close)
            
        Returns:
            pandas.Series: SMA values
        """
        sma = data[column].rolling(window=period).mean()
        return sma
    
    
    def calculate_ema(self, data, period, column='Close'):
        """
        Calculate Exponential Moving Average
        
        Args:
            data (pandas.DataFrame): OHLCV data
            period (int): Number of periods
            column (str): Which column to average (default: Close)
            
        Returns:
            pandas.Series: EMA values
        """
        ema = data[column].ewm(span=period, adjust=False).mean()
        return ema
    
    
    def calculate_volatility(self, data, period=20):
        """
        Calculate historical volatility (standard deviation of returns)
        
        Args:
            data (pandas.DataFrame): OHLCV data
            period (int): Number of periods
            
        Returns:
            pandas.Series: Volatility values
        """
        returns = self.calculate_returns(data)
        volatility = returns.rolling(window=period).std()
        return volatility
    
    
    def calculate_crossover(self, fast_line, slow_line):
        """
        Detect crossover points between two lines
        Useful for Moving Average strategies
        
        Args:
            fast_line (pandas.Series): Fast indicator line
            slow_line (pandas.Series): Slow indicator line
            
        Returns:
            pandas.Series: 1 if fast crosses above slow,
                          -1 if fast crosses below slow,
                          0 otherwise
        """
        crossover = pd.Series(0, index=fast_line.index)
        
        # Golden Cross: fast crosses above slow
        golden_cross = (fast_line.shift(1) <= slow_line.shift(1)) & (fast_line > slow_line)
        crossover[golden_cross] = 1
        
        # Death Cross: fast crosses below slow
        death_cross = (fast_line.shift(1) >= slow_line.shift(1)) & (fast_line < slow_line)
        crossover[death_cross] = -1
        
        return crossover
    
    
    def validate_signal(self, data, signals):
        """
        Apply filters to signals
        Remove invalid signals (low volume, price gaps, etc.)
        
        Args:
            data (pandas.DataFrame): OHLCV data
            signals (pandas.Series): Trading signals
            
        Returns:
            pandas.Series: Filtered signals
        """
        # Only trade if volume is adequate
        volume_filter = self.check_volume(data)
        
        # Only trade if price data is valid
        price_filter = self.check_price_validity(data)
        
        # Apply filters - set invalid signals to 0 (HOLD)
        filtered_signals = signals.copy()
        filtered_signals[~(volume_filter & price_filter)] = 0
        
        return filtered_signals
    
    
    def get_signal_name(self, signal):
        """
        Convert signal number to readable name
        
        Args:
            signal (int): Signal value (1, -1, 0)
            
        Returns:
            str: Signal name (BUY, SELL, HOLD)
        """
        if signal == 1:
            return "BUY"
        elif signal == -1:
            return "SELL"
        else:
            return "HOLD"
    
    
    def print_strategy_info(self):
        """
        Print strategy information
        """
        print(f"\nStrategy: {self.name}")
        print(f"Indicators: {list(self.indicators.keys())}")
        print(f"Signal count: {len(self.signals)}")
    
    
    def run(self, data):
        """
        Execute strategy on data
        
        Args:
            data (pandas.DataFrame): OHLCV data
            
        Returns:
            dict: Contains 'data' (with indicators) and 'signals'
        """
        # Calculate indicators
        data = self.calculate_indicators(data)
        self.indicators = data.columns.tolist()
        
        # Generate signals
        signals = self.generate_signals(data)
        
        # Validate signals
        signals = self.validate_signal(data, signals)
        self.signals = signals
        
        # Return results
        return {
            'data': data,
            'signals': signals
        }