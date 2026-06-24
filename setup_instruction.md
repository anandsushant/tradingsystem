====================================
COMPLETE SETUP INSTRUCTIONS
====================================

STEP 1: OPEN TERMINAL

Open your terminal/command prompt and navigate to the project directory:

```
cd path/to/trading_system
```

Example on WSL:
```
cd ~/main/dev/capstone/trading_system
```


STEP 2: CREATE VIRTUAL ENVIRONMENT

This isolates project dependencies from your system Python.

```bash
python3 -m venv venv
```

This creates a 'venv' folder with isolated Python.


STEP 3: ACTIVATE VIRTUAL ENVIRONMENT

On Linux/WSL/macOS:
```bash
source .venv/bin/activate
```

On Windows (without WSL):
```bash
venv\Scripts\activate
```

VERIFICATION:
You should see (venv) at the start of your terminal prompt:
```
(venv) username@computer:~/trading_system$
```


STEP 4: UPGRADE PIP

Ensure pip is up to date:

```bash
pip install --upgrade pip
```


STEP 5: INSTALL DEPENDENCIES

Install all required Python libraries:

```bash
pip install -r requirements.txt
```

This installs:
- yfinance (download stock data)
- pandas (data manipulation)
- numpy (numerical computing)
- matplotlib (charts)
- scipy (statistics)
- Other utilities

Expected time: 2-5 minutes
You'll see many lines of output ending with "Successfully installed..."


STEP 6: VERIFY INSTALLATION

Test that all libraries imported correctly:

```bash
python3 checkenv.py
```


STEP 7: DOWNLOAD STOCK DATA (OPTIONAL)

The project includes pre-downloaded CSV files, but you can refresh them:

```bash
python3 data/fetch.py
```

Output will show:
```
DataFetcher initialized
Stocks: 10 stocks
Period: 2020-01-01 to 2025-05-25
Save path: ./data/raw/

Downloading AAPL...  1356 days of data
Saved to ./data/raw/AAPL.csv

Downloading MSFT...  1356 days of data
Saved to ./data/raw/MSFT.csv
... (continues for all 10 stocks)

Download complete!
```

NOTE: This downloads 5 years of historical data for 10 stocks.
Time: 30-60 seconds depending on internet speed.


SETUP COMPLETE!
You're now ready to run the system.