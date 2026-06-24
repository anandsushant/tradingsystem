STOCKS = [
    'AAPL',      # Apple
    'MSFT',      # Microsoft
    'GOOGL',     # Google
    'TSLA',      # Tesla
    'AMZN',      # Amazon
    'NVDA',      # Nvidia
    'META',      # Meta (Facebook)
    'NFLX',      # Netflix
    'AMD',       # AMD
    'PYPL'       # PayPal
]

# backtesting period
START_DATE = '2020-01-01'      # Backtest start
END_DATE = '2025-05-25'        # Backtest end (today)
DATA_FETCH_INTERVAL = 'daily'  # Daily OHLCV data

# parameters for paper-trading
INITIAL_CAPITAL = 100000       # $100,000 starting money
COMMISSION = 0.001             # 0.1% brokerage fee per trade (round-trip = 0.2%)
SLIPPAGE = 0.001               # 0.1% slippage (price impact)

# ============================================
# 4. STRATEGY PARAMETERS (Dual Moving Average)
# ============================================
# Strategy: Buy when 50-day MA crosses above 200-day MA
#           Sell when 50-day MA crosses below 200-day MA

FAST_MA_PERIOD = 30            # Fast moving average (50 days)
SLOW_MA_PERIOD = 60           # Slow moving average (200 days)
VOLUME_MIN_THRESHOLD = 1000000 # Minimum volume to trade (liquidity check)

# ============================================
# 5. RISK MANAGEMENT PARAMETERS
# ============================================
POSITION_SIZE_METHOD = 'fixed'  # Options: 'fixed', 'kelly', 'volatility'
POSITION_SIZE_PERCENT = 0.1     # 10% of capital per trade (if fixed method)
STOP_LOSS_PERCENT = 0.05        # 5% stop-loss below entry
TAKE_PROFIT_PERCENT = 0.15      # 15% take-profit above entry (optional)

MAX_DAILY_LOSS = 0.02           # Stop trading if lost 2% in a day
MAX_PORTFOLIO_LOSS = 0.10       # Stop trading if lost 10% total
MAX_POSITIONS = 5               # Don't hold more than 5 stocks at once

# ============================================
# 6. DATA & FILE PATHS
# ============================================
DATA_RAW_PATH = './data/raw/'           # Where to save downloaded CSVs
DATA_PROCESSED_PATH = './processed/'   # trailing slashes are necessary after folder name
REPORTS_PATH = './reports/'
LOGS_PATH = './logs/'
PLOTS_PATH = './reports/plots/'

# ============================================
# 7. BACKTESTING ENGINE SETTINGS
# ============================================
CASH_BUFFER = 0.05              # Keep 5% cash buffer (don't use all capital)
USE_REALISTIC_SLIPPAGE = True   # Include slippage in backtest
AVOID_LOOKAHEAD_BIAS = True     # Use only past data (important!)

# ============================================
# 8. VISUALIZATION & REPORTING
# ============================================
GENERATE_EQUITY_CURVE = True    # Plot portfolio value over time
GENERATE_DRAWDOWN_CHART = True  # Plot max drawdown
GENERATE_SIGNALS_CHART = True   # Plot price + indicators + buy/sell signals
GENERATE_MONTHLY_RETURNS = True # Heatmap of monthly returns

# ============================================
# 9. PAPER TRADING (OPTIONAL - for live simulation)
# ============================================
PAPER_TRADING_ENABLED = False   # Set to True if doing live simulation
PAPER_TRADING_PERIOD = 30       # Days to run paper trading