import os
from utils.data_loader import DataPreprocessor
from utils.strategies.trend_following import TrendFollowing
from utils.strategies.backtesting.backtester import Backtester
from dateutil.parser import parse
import sys
# set env
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATA_AGGREGATION = 'D' # Daily aggregation during preprocessing | by default # W: Weekly, M: Monthly aggregation (using mean value)
NORMALIZE_FEATURE_YN = 'n' # n: No normalization, y: Normalize the 'Close' feature
REQUIRED_ARGS = 4

if __name__ == '__main__':
    if len(sys.argv) < REQUIRED_ARGS:
        raise ValueError("Please provide the symbol, start date, and end date.") 
    symbol = sys.argv[1]
    start_date = parse(sys.argv[2])
    end_date = parse(sys.argv[3])
    file_prefix = f"{symbol}_{sys.argv[2]}_{sys.argv[3]}"
    if not os.path.exists(os.path.join(DATA_DIR, f"{file_prefix}_processed.csv")):
        data_preprocessor = DataPreprocessor(symbol, start_date, end_date)
        data_preprocessor.save_data(os.path.join(DATA_DIR, f"{file_prefix}_raw.csv"))
        data_preprocessor.preprocess_data(method='ffill', time_period=DATA_AGGREGATION, normalize_feature_yn=NORMALIZE_FEATURE_YN)
        data_preprocessor.save_data(os.path.join(DATA_DIR, f"{file_prefix}_processed.csv"))
        print("Data preprocessing completed.")
    tf_strategy = TrendFollowing(DATA_DIR, f"{file_prefix}_processed.csv")
    tf_strategy.visualize_data()
    tf_strategy.save_data(os.path.join(DATA_DIR, f"{file_prefix}_trend_following.csv"))
    print("Trend following strategy completed.")
    trend_following_positions = tf_strategy.get_data()['SMA_Signal']
    trend_following_prices = tf_strategy.get_data()['Close']
    print("Backtesting the trend following strategy.")
    backtester = Backtester(initial_capital=10000.0)
    backtester.backtest_strategy(symbol, trend_following_positions, trend_following_prices)
    print("Backtesting completed.")
    print("Final portfolio:")
    print(backtester.get_portfolio())
    print("Final capital:" + str(backtester.initial_capital))
    print(backtester.__str__(trend_following_prices.iloc[-1]))
    

