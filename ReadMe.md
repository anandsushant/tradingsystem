
PROJECT: Algorithmic Trading System

This guide provides step-by-step instructions to set up and run the trading
system on any Linux/WSL system from scratch.

TABLE OF CONTENTS

1. SYSTEM REQUIREMENTS
2. COMPLETE SETUP INSTRUCTIONS
3. HOW TO RUN THE SYSTEM
4. UNDERSTANDING THE RESULTS


1. SYSTEM REQUIREMENTS

REQUIRED:
- Linux, macOS, or Windows WSL (Windows Subsystem for Linux)
- Python 3.10 or higher

VERIFY YOUR SYSTEM:
```bash
python3 --version
pip --version
```

2. COMPLETE SETUP INSTRUCTIONS

STEP 1: OPEN TERMINAL

Open your terminal/command prompt and navigate to the project directory:

```
cd ~/main/dev/capstone/trading_system
```


STEP 2: CREATE VIRTUAL ENVIRONMENT

This isolates project dependencies from your system Python.

```
python3 -m venv venv
```

This creates a 'venv' folder with isolated Python.

STEP 3: ACTIVATE VIRTUAL ENVIRONMENT

On Linux/WSL/macOS:
```
source venv/bin/activate
```

On Windows (without WSL):
```
venv\Scripts\activate
```

VERIFICATION:
You should see (venv) at the start of your terminal prompt:
```
(venv) username@computer:~/trading_system$
```


STEP 4: UPGRADE PIP

Ensure pip is up to date:

```
pip install --upgrade pip
```


STEP 5: INSTALL DEPENDENCIES

Install all required Python libraries:

```
pip install -r requirements.txt
```

This installs:
- yfinance (download stock data)
- pandas (data manipulation)
- numpy (numerical computing)
- matplotlib (charts)
- scipy (statistics)
- Other utilities

STEP 6: VERIFY INSTALLATION

Test that all libraries imported correctly:

```
python3 checkenv.py
"
```
checkenv.py is written to verify required libraries

STEP 7: DOWNLOAD STOCK DATA

```
python3 data/fetch.py
```

NOTE: This downloads 5 years of historical data for 10 stocks.
You can change this in config.py

SETUP COMPLETE!

3. HOW TO RUN THE SYSTEM

BASIC EXECUTION (No parameters needed)

Simply run:

```
python3 main.py
```

This will:
1. Load stock data from CSV files
2. Initialize the trading strategy
3. Run backtest on 5 years of historical data (2020-2025)
4. Calculate performance metrics
5. Print detailed results


STEP-BY-STEP EXECUTION FLOW


When you run 'python3 main.py', the system performs 7 steps:

STEP 1: Load Data
- Loads 10 stocks from CSV files in data/raw/
- Verifies all 1,356 days of data (2020-2025)
- Checks for data quality

STEP 2: Initialize Strategy
- Creates Dual Moving Average Crossover strategy
- Sets up indicators (50-day MA, 200-day MA)

STEP 3: Run Backtest
- Simulates trading from 2020-01-02 to 2025-05-23
- For each trading day:
  * Calculates moving averages
  * Generates BUY/SELL/HOLD signals
  * Executes trades (if signal)
  * Tracks portfolio value
  * Records P&L

STEP 4: Display Backtest Summary
- Initial capital: $100,000
- Final portfolio value
- Total return %
- Maximum drawdown
- Win rate
- Number of trades

STEP 5: Per-Stock Analysis
- Breakdown by individual stock (AAPL, MSFT, etc.)
- P&L per stock
- Trade count per stock
- Win rate per stock

STEP 6: Sample Trades
- Shows first 5 trades executed
- Entry date, exit date
- Entry price, exit price
- Profit/loss amount and percentage
- Days held

STEP 7: Equity Curve Summary
- Starting capital
- Ending capital
- Peak capital reached
- Lowest capital reached

4. UNDERSTANDING THE RESULTS


KEY METRICS EXPLAINED


INITIAL CAPITAL: $100,000.00
- Virtual money you start with

FINAL PORTFOLIO VALUE: $95,871.38
- Portfolio value at end of backtest period (2025-05-23)

TOTAL RETURN: $-4,128.62
- Profit/loss in dollars
- Negative = strategy lost money
- Calculated as: Final - Initial

RETURN %: -4.13%
- Return as percentage
- Calculated as: (Final - Initial) / Initial * 100

MAX DRAWDOWN: -14.49%
- Largest loss from peak to trough
- Peak: $112,116.44
- Trough: $95,871.38
- Drawdown: (95,871 - 112,116) / 112,116 = -14.49%

TOTAL TRADES: 4
- Number of complete trades (buy + sell)
- Not all days have trades
- Strategy only trades when MA50 crosses MA200

WINNING TRADES: 0
- Number of profitable trades

LOSING TRADES: 4
- Number of trades with losses

WIN RATE: 0%
- Percentage of profitable trades
- 0 winning / 4 total = 0%

AVERAGE WIN: $0.00
- Average profit per winning trade
- No winning trades = $0

AVERAGE LOSS: -$1,032.16
- Average loss per losing trade
- Total losses / Number of losing trades


WHAT DO THESE RESULTS MEAN?

NEGATIVE RETURN (-4.13%):
The strategy lost 4.13% over 5 years.

