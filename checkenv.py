import sys
import importlib
from pathlib import Path

REQUIRED_PACKAGES = {
    "yfinance": "yfinance",
    "pandas": "pandas",
    "numpy": "numpy",
    "backtrader": "backtrader",
    "pandas_ta": "pandas-ta",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "scipy": "scipy",
    "dotenv": "python-dotenv",
}
    
def check_venv():

    print("CHECKING VIRTUAL ENVIRONMENT...")

    in_venv = sys.prefix != sys.base_prefix

    if in_venv:
        print(f"[OK] Virtual environment active")
        print(f"     Python executable: {sys.executable}")
    else:
        print("[ERROR] Virtual environment NOT active")
        print("Activate using:")
        print("source .venv/bin/activate")
        sys.exit(1)

# ============================================
# CHECK PACKAGE IMPORTS
# ============================================

def check_imports():

    print("CHECKING PACKAGE IMPORTS...")

    failed = []

    for module_name, package_name in REQUIRED_PACKAGES.items():
        try:
            module = importlib.import_module(module_name)

            version = getattr(module, "__version__", "unknown")

            print(f"[OK] {package_name:<15} Version: {version}")

        except Exception as e:
            print(f"[FAIL] {package_name:<15} Error: {e}")
            failed.append(package_name)

    return failed

# ============================================
# FUNCTIONALITY TESTS
# ============================================

def functionality_tests():

    print("RUNNING FUNCTIONALITY TESTS")

    try:
        import pandas as pd
        import numpy as np

        df = pd.DataFrame({
            "price": [100, 101, 102, 103]
        })

        mean_price = np.mean(df["price"])

        print(f"[OK] Pandas/Numpy working")
        print(f"     Mean price: {mean_price}")

    except Exception as e:
        print(f"[FAIL] Pandas/Numpy test failed: {e}")
        return False

    try:
        import matplotlib.pyplot as plt

        fig = plt.figure()
        plt.close(fig)

        print("[OK] Matplotlib working")

    except Exception as e:
        print(f"[FAIL] Matplotlib failed: {e}")
        return False

    try:
        import yfinance as yf

        ticker = yf.Ticker("AAPL")
        info = ticker.fast_info

        print("[OK] yfinance working")

    except Exception as e:
        print(f"[FAIL] yfinance failed: {e}")
        return False

    return True

def main():
    check_venv()

    failed_imports = check_imports()

    functionality_ok = functionality_tests()

    #print("\n" + "=" * 60)
    #print("FINAL STATUS")
    #print("=" * 60)

    if failed_imports:
        print(f"[FAIL] Missing/Broken packages:")
        for pkg in failed_imports:
            print(f"   - {pkg}")

    if not failed_imports and functionality_ok:
        print("[SUCCESS] Environment is fully ready")
        sys.exit(0)
    else:
        print("[ERROR] Environment has issues")
        sys.exit(1)

if __name__ == "__main__":
    main()