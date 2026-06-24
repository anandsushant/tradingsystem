"""
Dual Moving Average Crossover Strategy
Buy when 50-day MA crosses above 200-day MA
Sell when 50-day MA crosses below 200-day MA
"""

import pandas as pd
import numpy as np
import sys

sys.path.append('..')
from config import FAST_MA_PERIOD, SLOW_MA_PERIOD, VOLUME_MIN_THRESHOLD
from strategy.base_strategy import BaseStrategy


class DualMAStrategy(BaseStrategy):
    """
    Dual Moving Average Crossover Strategy
    
    Logic:
    - Calculate 50-day and 200-day moving averages
    - BUY when 50-day crosses ABOVE 200-day (golden cross)
    - SELL when 50-day crosses BELOW 200-day (death cross)
    """
    
    def __init__(self):
        """
        Initialize strategy
        """
        super().__init__(name="Dual Moving Average Crossover")
        self.fast_period = FAST_MA_PERIOD
        self.slow_period = SLOW_MA_PERIOD
    
    
    def calculate_indicators(self, data):
        """
        Calculate moving averages
        
        Args:
            data (pandas.DataFrame): OHLCV data
            
        Returns:
            pandas.DataFrame: Data with MA indicators added
        """
        # Make a copy to avoid modifying original
        data = data.copy()
        
        # Calculate moving averages using inherited method
        data['MA_Fast'] = self.calculate_sma(data, self.fast_period)
        data['MA_Slow'] = self.calculate_sma(data, self.slow_period)
        
        return data
    
    
    def generate_signals(self, data):
        """
        Generate trading signals based on MA crossover
        
        Args:
            data (pandas.DataFrame): Data with indicators
            
        Returns:
            pandas.Series: Signals (1=BUY, -1=SELL, 0=HOLD)
        """
        # Initialize signals
        signals = pd.Series(0, index=data.index, dtype=int)
        
        # Get the moving averages
        ma_fast = data['MA_Fast']
        ma_slow = data['MA_Slow']
        
        # Calculate crossovers using inherited method
        crossovers = self.calculate_crossover(ma_fast, ma_slow)
        
        # Copy crossover signals
        signals = crossovers.copy()
        
        return signals