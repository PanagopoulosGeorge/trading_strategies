import os
from utils.data_loader import DataPreprocessor
from dateutil.parser import parse
import sys
from settings import DATA_DIR, DATA_AGGREGATION, NORMALIZE_FEATURE_YN

REQUIRED_ARGS = 4

def print_help():
    print("\nfetch_symbol.py: Fetch stock data and preprocess it for backtesting.")
    
    help = """
        Usage: (poetry run) python fetch_symbol.py <symbol> <start_date> <end_date>
        \n\tArguments:
                1. symbol: The symbol of the stock or asset to fetch (e.g. AAPL, GOOGL)
                2. start_date: The start date of the data (format: YYYY-MM-DD)
                3. end_date: The end date of the data (format: YYYY-MM-DD)
    """
    print(help)

if __name__ == '__main__':
    
    if len(sys.argv) < REQUIRED_ARGS or sys.argv[1] == "-h":
        print_help()
        sys.exit(0)
    if len(sys.argv) < REQUIRED_ARGS:
        print("Invalid number of arguments")
        print_help()
        sys.exit(0)
    symbol = sys.argv[1]
    start_date = parse(sys.argv[2])
    end_date = parse(sys.argv[3])
    file_prefix = f"{symbol}_{sys.argv[2]}_{sys.argv[3]}"
    
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if os.path.exists(os.path.join(DATA_DIR, f"{file_prefix}_processed.csv")) and os.path.exists(os.path.join(DATA_DIR, f"{file_prefix}_raw.csv")):
        print("Data already exists")
        sys.exit(0)
    data_preprocessor = DataPreprocessor(symbol, start_date, end_date)
    data_preprocessor.save_data(os.path.join(DATA_DIR, f"{file_prefix}_raw.csv"))
    data_preprocessor.preprocess_data(method='ffill', time_period=DATA_AGGREGATION, normalize_feature_yn=NORMALIZE_FEATURE_YN)
    data_preprocessor.save_data(os.path.join(DATA_DIR, f"{file_prefix}_processed.csv"))
    print("Data preprocessing completed.")