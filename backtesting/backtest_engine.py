"""
Backtest Engine Module
Simulates trading strategy on historical data
"""

import pandas as pd
import numpy as np
from datetime import datetime
import sys

sys.path.append('..')
from config import (
    INITIAL_CAPITAL, COMMISSION, SLIPPAGE,
    STOP_LOSS_PERCENT, MAX_DAILY_LOSS, MAX_PORTFOLIO_LOSS, MAX_POSITIONS,
    CASH_BUFFER
)


class BacktestEngine:
    """
    Backtesting engine - simulates trading strategy on historical data
    """
    
    def __init__(self, strategy, initial_capital=None):
        """
        Initialize backtest engine
        
        Args:
            strategy: Strategy object (inherits from BaseStrategy)
            initial_capital (float): Starting capital in dollars
        """
        self.strategy = strategy
        self.initial_capital = initial_capital or INITIAL_CAPITAL
        
        # Portfolio tracking
        self.cash = self.initial_capital
        self.positions = {}  # {ticker: {entry_price, shares, entry_date}}
        self.portfolio_value = self.initial_capital
        
        # Results tracking
        self.trades = []  # List of completed trades
        self.daily_equity = []  # Portfolio value each day
        self.daily_cash = []  # Available cash each day
        self.daily_positions = []  # Open positions each day
        
        # Risk tracking
        self.peak_portfolio_value = self.initial_capital
        self.max_drawdown = 0
        self.daily_loss = 0
        self.daily_loss_limit_hit = False
        
        print(f"BacktestEngine initialized")
        print(f"  Strategy: {strategy.name}")
        print(f"  Initial Capital: ${self.initial_capital:,.2f}")
        print(f"  Commission: {COMMISSION*100:.2f}%")
        print(f"  Slippage: {SLIPPAGE*100:.2f}%")
    
    
    def calculate_position_size(self, current_price, percent_of_capital=0.1):
        """
        Calculate position size (number of shares to buy)
        Risk 'percent_of_capital' of available cash
        
        Args:
            current_price (float): Current stock price
            percent_of_capital (float): % of cash to risk
            
        Returns:
            int: Number of shares to buy
        """
        # Calculate available cash (keep buffer)
        usable_cash = self.cash * (1 - CASH_BUFFER)
        
        # Position size in dollars
        position_dollars = usable_cash * percent_of_capital
        
        # Shares to buy
        shares = position_dollars / current_price
        
        return int(shares)
    
    
    def calculate_entry_cost(self, entry_price, shares):
        """
        Calculate total cost including commission and slippage
        
        Args:
            entry_price (float): Price per share
            shares (int): Number of shares
            
        Returns:
            float: Total cost with fees
        """
        trade_value = entry_price * shares
        
        # Commission: 0.1% round-trip (buy + sell both have commission)
        # So on entry, we pay 0.1% commission
        commission = trade_value * COMMISSION
        
        # Slippage: price moved against us
        # On buy, we pay extra due to slippage
        slippage = trade_value * SLIPPAGE
        
        total_cost = trade_value + commission + slippage
        
        return total_cost
    
    
    def calculate_exit_proceeds(self, exit_price, shares):
        """
        Calculate proceeds from selling, minus costs
        
        Args:
            exit_price (float): Price per share
            shares (int): Number of shares
            
        Returns:
            float: Net proceeds after fees
        """
        trade_value = exit_price * shares
        
        # Commission on exit
        commission = trade_value * COMMISSION
        
        # Slippage on exit (price moved against us)
        slippage = trade_value * SLIPPAGE
        
        net_proceeds = trade_value - commission - slippage
        
        return net_proceeds
    
    
    def execute_buy(self, ticker, current_price, current_date):
        """
        Execute buy order
        
        Args:
            ticker (str): Stock ticker
            current_price (float): Buy price (Close price of day)
            current_date: Date of trade
            
        Returns:
            bool: True if successful, False if insufficient funds
        """
        # Calculate position size
        shares = self.calculate_position_size(current_price)
        
        if shares <= 0:
            return False
        
        # Calculate cost
        total_cost = self.calculate_entry_cost(current_price, shares)
        
        # Check if we have enough cash
        if total_cost > self.cash:
            return False
        
        # Check if we already have this position
        if ticker in self.positions:
            return False  # Don't average up
        
        # Execute trade
        self.cash -= total_cost
        self.positions[ticker] = {
            'entry_price': current_price,
            'entry_date': current_date,
            'shares': shares,
            'entry_cost': total_cost
        }
        
        return True
    
    
    def execute_sell(self, ticker, current_price, current_date):
        """
        Execute sell order
        
        Args:
            ticker (str): Stock ticker
            current_price (float): Sell price (Close price of day)
            current_date: Date of trade
            
        Returns:
            bool: True if successful, False if no position
        """
        # Check if we have this position
        if ticker not in self.positions:
            return False
        
        position = self.positions[ticker]
        shares = position['shares']
        entry_price = position['entry_price']
        entry_date = position['entry_date']
        entry_cost = position['entry_cost']
        
        # Calculate exit proceeds
        exit_proceeds = self.calculate_exit_proceeds(current_price, shares)
        
        # Calculate P&L
        realized_pnl = exit_proceeds - entry_cost
        realized_pnl_percent = (realized_pnl / entry_cost) * 100
        
        # Record trade
        trade = {
            'ticker': ticker,
            'entry_date': entry_date,
            'entry_price': entry_price,
            'exit_date': current_date,
            'exit_price': current_price,
            'shares': shares,
            'entry_cost': entry_cost,
            'exit_proceeds': exit_proceeds,
            'pnl': realized_pnl,
            'pnl_percent': realized_pnl_percent,
            'hold_days': (current_date - entry_date).days
        }
        self.trades.append(trade)
        
        # Update cash and remove position
        self.cash += exit_proceeds
        del self.positions[ticker]
        
        return True
    
    
    def update_portfolio_value(self, data, current_date):
        """
        Update portfolio value at end of day (mark-to-market)
        
        Args:
            data (dict): {ticker: price} dictionary
            current_date: Current date
        """
        # Start with cash
        total_value = self.cash
        
        # Add value of open positions
        for ticker, position in self.positions.items():
            current_price = data.get(ticker, 0)
            position_value = current_price * position['shares']
            total_value += position_value
        
        self.portfolio_value = total_value
        
        # Track peak for drawdown calculation
        if total_value > self.peak_portfolio_value:
            self.peak_portfolio_value = total_value
        
        # Calculate drawdown
        drawdown = (self.portfolio_value - self.peak_portfolio_value) / self.peak_portfolio_value
        if drawdown < self.max_drawdown:
            self.max_drawdown = drawdown
        
        # Record daily equity
        self.daily_equity.append({
            'date': current_date,
            'value': self.portfolio_value,
            'cash': self.cash,
            'open_positions': len(self.positions)
        })
    
    
    def check_stop_loss(self, ticker, current_price):
        """
        Check if position should be stopped out
        
        Args:
            ticker (string): Stock ticker
            current_price (float): Current price
            
        Returns:
            bool: True if stop-loss hit
        """
        if ticker not in self.positions:
            return False
        
        position = self.positions[ticker]
        entry_price = position['entry_price']
        
        # Calculate loss percentage
        loss_percent = (current_price - entry_price) / entry_price
        
        # Stop if down more than threshold
        if loss_percent < -STOP_LOSS_PERCENT:
            return True
        
        return False
    
    
    def check_daily_loss_limit(self):
        """
        Check if daily loss limit is hit
        
        Returns:
            bool: True if should stop trading today
        """
        daily_loss_percent = (self.portfolio_value - self.peak_portfolio_value) / self.peak_portfolio_value
        
        if daily_loss_percent < -MAX_DAILY_LOSS:
            return True
        
        return False
    
    
    def check_portfolio_loss_limit(self):
        """
        Check if portfolio loss limit is hit
        
        Returns:
            bool: True if should stop trading
        """
        total_loss_percent = (self.portfolio_value - self.initial_capital) / self.initial_capital
        
        if total_loss_percent < -MAX_PORTFOLIO_LOSS:
            return True
        
        return False
    
    
    def run(self, all_data):
        """
        Run backtest on all stocks
        
        Args:
            all_data (dict): {ticker: DataFrame} with OHLCV data
            
        Returns:
            dict: Backtest results
        """
        print(f"\nRunning backtest...")
        
        # Get list of stocks and date range
        tickers = list(all_data.keys())
        all_dates = pd.DatetimeIndex([])
        
        # Collect all dates from all stocks
        for ticker, data in all_data.items():
            all_dates = all_dates.union(data.index)
        
        all_dates = all_dates.sort_values()
        
        print(f"Backtesting period: {all_dates[0].date()} to {all_dates[-1].date()}")
        print(f"Number of trading days: {len(all_dates)}")
        print(f"Number of stocks: {len(tickers)}\n")
        
        # Loop through each trading day
        for day_idx, current_date in enumerate(all_dates):
            # Get data up to current date (no look-ahead bias!)
            data_so_far = {}
            current_prices = {}
            
            for ticker in tickers:
                # Get all data up to today for this stock
                ticker_data = all_data[ticker][:current_date]
                
                if len(ticker_data) == 0:
                    continue
                
                data_so_far[ticker] = ticker_data
                
                # Get current close price
                current_prices[ticker] = ticker_data['Close'].iloc[-1]
            
            # Skip if not enough data yet
            if len(data_so_far) == 0:
                continue
            
            # Check risk limits
            if self.check_portfolio_loss_limit():
                print(f"Portfolio loss limit hit on {current_date.date()}")
                break
            
            # Run strategy on all stocks
            all_signals = {}
            
            for ticker in tickers:
                if ticker not in data_so_far:
                    continue
                
                ticker_data = data_so_far[ticker]
                
                # Run strategy
                results = self.strategy.run(ticker_data)
                signals = results['signals']
                
                # Get signal for today
                if len(signals) > 0:
                    signal = signals.iloc[-1]
                    all_signals[ticker] = signal
            
            # Execute trades based on signals
            for ticker, signal in all_signals.items():
                current_price = current_prices[ticker]
                
                # Check stop-loss
                if self.check_stop_loss(ticker, current_price):
                    self.execute_sell(ticker, current_price, current_date)
                    continue
                
                # Check daily loss limit
                if self.check_daily_loss_limit():
                    self.daily_loss_limit_hit = True
                    continue
                
                # Execute signal
                if signal == 1:  # BUY
                    if len(self.positions) < MAX_POSITIONS:
                        self.execute_buy(ticker, current_price, current_date)
                
                elif signal == -1:  # SELL
                    self.execute_sell(ticker, current_price, current_date)
            
            # Update portfolio value
            self.update_portfolio_value(current_prices, current_date)
            
            # Print progress every 250 days
            if (day_idx + 1) % 250 == 0:
                print(f"  Day {day_idx+1}/{len(all_dates)}: Portfolio = ${self.portfolio_value:,.0f}, Trades = {len(self.trades)}")
        
        print(f"\nBacktest complete!")
        print(f"Total trades: {len(self.trades)}")
        print(f"Final portfolio value: ${self.portfolio_value:,.2f}")
        
        return self.get_results()
    
    
    def get_results(self):
        """
        Get backtest results
        
        Returns:
            dict: Contains trades, daily equity, and summary stats
        """
        results = {
            'trades': pd.DataFrame(self.trades),
            'daily_equity': pd.DataFrame(self.daily_equity),
            'initial_capital': self.initial_capital,
            'final_portfolio_value': self.portfolio_value,
            'total_return': self.portfolio_value - self.initial_capital,
            'total_return_percent': ((self.portfolio_value - self.initial_capital) / self.initial_capital) * 100,
            'max_drawdown': self.max_drawdown,
            'num_trades': len(self.trades),
            'open_positions': self.positions
        }
        
        return results
    
    
    def print_summary(self, results):
        """
        Print backtest summary
        
        Args:
            results (dict): Backtest results
        """
        print(f"\n{'='*60}")
        print(f"BACKTEST SUMMARY")
        print(f"{'='*60}")
        print(f"Initial Capital:        ${results['initial_capital']:,.2f}")
        print(f"Final Portfolio Value:  ${results['final_portfolio_value']:,.2f}")
        print(f"Total Return:           ${results['total_return']:,.2f}")
        print(f"Return %:               {results['total_return_percent']:.2f}%")
        print(f"Max Drawdown:           {results['max_drawdown']*100:.2f}%")
        print(f"Total Trades:           {results['num_trades']}")
        print(f"{'='*60}\n")
        
        # Trade statistics
        if len(results['trades']) > 0:
            trades_df = results['trades']
            winning_trades = len(trades_df[trades_df['pnl'] > 0])
            losing_trades = len(trades_df[trades_df['pnl'] <= 0])
            win_rate = (winning_trades / len(trades_df)) * 100
            avg_win = trades_df[trades_df['pnl'] > 0]['pnl'].mean() if winning_trades > 0 else 0
            avg_loss = trades_df[trades_df['pnl'] <= 0]['pnl'].mean() if losing_trades > 0 else 0
            
            print(f"TRADE STATISTICS")
            print(f"{'='*60}")
            print(f"Winning Trades:         {winning_trades}")
            print(f"Losing Trades:          {losing_trades}")
            print(f"Win Rate:               {win_rate:.2f}%")
            print(f"Avg Win:                ${avg_win:,.2f}")
            print(f"Avg Loss:               ${avg_loss:,.2f}")
            print(f"{'='*60}\n")