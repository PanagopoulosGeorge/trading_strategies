from utils.strategies.trend_following import TrendFollowing 
from utils.strategies.mean_reversion import MeanReversion
from utils.strategies.backtesting.backtester import Backtester
from dateutil.parser import parse
import sys
import os
from settings import REQUIRED_ARGS, DATA_DIR, STRATEGY, SIGNAL, SHORT_WINDOW, LONG_WINDOW, BB_SHORT_WINDOW

def print_help():
    help = """
        Usage: (poetry run) python apply_strategy.py <file_name>
        \n\tArguments:
                1. symbol: The symbol of the stock or asset to fetch (e.g. AAPL, GOOGL)
                2. start_date: The start date of the data (format: YYYY-MM-DD)
                3. end_date: The end date of the data (format: YYYY-MM-DD)
                4. (optional) "backtest" to backtest the strategy 
    """
    print(help)
if __name__ == '__main__':
    if len(sys.argv) < 3 or sys.argv[1] == "-h":
        print_help()
        sys.exit(0)
    if len(sys.argv) < REQUIRED_ARGS:
        print("Invalid number of arguments")
        print_help()
        sys.exit(0)
    symbol = sys.argv[1]
    start_date = parse(sys.argv[2])
    end_date = parse(sys.argv[3])
    backtest = False if sys.argv[4] != "backtest" else True
    file_prefix = f"{symbol}_{sys.argv[2]}_{sys.argv[3]}"
    if STRATEGY=="tf":
        strategy = TrendFollowing(DATA_DIR, f"{file_prefix}_processed.csv", feature='Close', short_window=SHORT_WINDOW, long_window=LONG_WINDOW)
        signals_df = strategy.generate_signals()
        strategy.save_signals(os.path.join(DATA_DIR, f"{file_prefix}_strategy.csv"))
        strategy.visualise_signals()
    elif STRATEGY=="mr":
        strategy = MeanReversion(DATA_DIR, f"{file_prefix}_processed.csv", feature='Close', window=BB_SHORT_WINDOW)
        signals_df = strategy.generate_signals(n_std=1.8)
        strategy.save_signals(os.path.join(DATA_DIR, f"{file_prefix}_strategy.csv"))
        strategy.visualise_signals()
    if backtest:
        backtester = Backtester(initial_capital=10000.0, risk_free_rate=0.04)
        backtester.backtest_strategy_single_asset(symbol, signals_df['Signal'], signals_df['Close'])
        backtester.print_summary()
        backtester.visualise_backtesting()
        

    
