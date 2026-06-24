"""
Main - Run entire algorithmic trading system
Fetches data -> Validates -> Loader -> Runs strategy -> Backtests -> Generates reports
"""

import sys
import pandas as pd
from datetime import datetime

# Import modules
from config import STOCKS
from data.data_loader import DataLoader
from strategy.dual_ma_strategy import DualMAStrategy
from backtesting.backtest_engine import BacktestEngine


def main():
    """
    Main function
    """
    
    print("\n" + "="*70)
    print("TRADING SYSTEM - ALGORITHMIC BACKTEST")
    print("="*70)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # =========================================================================
    # STEP 1: Load and Validate Data
    # =========================================================================
    print("STEP 1: Loading and Validating Data")
    print("-"*70)
    
    dataLoader = DataLoader()
    all_data = dataLoader.load_all_stocks()
    
    if len(all_data) == 0:
        print("Error: No data loaded. Please run data/fetch.py first.")
        return
    
    print(f"Loaded {len(all_data)} stocks")
    print(f"Data range: {list(all_data.values())[0].index[0].date()} to {list(all_data.values())[0].index[-1].date()}\n")
    
    # =========================================================================
    # STEP 2: Initialize Strategy
    # =========================================================================
    print("STEP 2: Initializing Strategy")
    print("-"*70)
    
    strategy = DualMAStrategy()
    strategy.print_strategy_info()
    print()
    
    # =========================================================================
    # STEP 3: Run Backtest
    # =========================================================================
    print("STEP 3: Running Backtest")
    print("-"*70)
    
    engine = BacktestEngine(strategy)
    results = engine.run(all_data)
    
    # =========================================================================
    # STEP 4: Print Results
    # =========================================================================
    print("\nSTEP 4: Backtest Results")
    print("-"*70)
    
    engine.print_summary(results)
    
    # =========================================================================
    # STEP 5: Per-Stock Analysis
    # =========================================================================
    print("STEP 5: Per-Stock Trade Summary")
    print("-"*70)
    
    if len(results['trades']) > 0:
        trades_df = results['trades']
        
        # Group trades by ticker
        for ticker in trades_df['ticker'].unique():
            ticker_trades = trades_df[trades_df['ticker'] == ticker]
            ticker_pnl = ticker_trades['pnl'].sum()
            ticker_trades_count = len(ticker_trades)
            ticker_win_rate = len(ticker_trades[ticker_trades['pnl'] > 0]) / ticker_trades_count * 100
            
            print(f"\n{ticker}:")
            print(f"  Trades: {ticker_trades_count}")
            print(f"  Total P&L: ${ticker_pnl:,.2f}")
            print(f"  Win Rate: {ticker_win_rate:.1f}%")
            print(f"  Avg Trade: ${ticker_pnl/ticker_trades_count:,.2f}")
    
    print("\n" + "-"*70)
    
    # =========================================================================
    # STEP 6: Display Sample Trades
    # =========================================================================
    print("\nSTEP 6: Sample Trades (First 5)")
    print("-"*70)
    
    if len(results['trades']) > 0:
        trades_df = results['trades']
        sample_trades = trades_df.head(5)
        
        for idx, trade in sample_trades.iterrows():
            print(f"\nTrade {idx+1}: {trade['ticker']}")
            print(f"  Entry:  {trade['entry_date'].date()} @ ${trade['entry_price']:.2f} ({trade['shares']} shares)")
            print(f"  Exit:   {trade['exit_date'].date()} @ ${trade['exit_price']:.2f}")
            print(f"  P&L:    ${trade['pnl']:,.2f} ({trade['pnl_percent']:.2f}%)")
            print(f"  Hold:   {trade['hold_days']} days")
    
    print("\n" + "-"*70)
    
    # =========================================================================
    # STEP 7: Daily Equity Curve
    # =========================================================================
    print("\nSTEP 7: Equity Curve Summary")
    print("-"*70)
    
    if len(results['daily_equity']) > 0:
        daily_equity_df = results['daily_equity']
        
        print(f"Starting Capital:  ${results['initial_capital']:,.2f}")
        print(f"Ending Capital:    ${results['final_portfolio_value']:,.2f}")
        print(f"Peak Capital:      ${daily_equity_df['value'].max():,.2f}")
        print(f"Lowest Capital:    ${daily_equity_df['value'].min():,.2f}")
    
    print("\n" + "="*70)
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")
    
    return results


if __name__ == "__main__":
    results = main()