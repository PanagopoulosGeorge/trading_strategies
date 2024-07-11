import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
# Daily aggregation during preprocessing | by default # W: Weekly, M: Monthly aggregation (using mean value)
DATA_AGGREGATION = 'D' 
# n: No normalization, y: Normalize the 'Close' feature
NORMALIZE_FEATURE_YN = 'n' 
REQUIRED_ARGS = 4
## Strategy to be applied
# tf: Trend Following
# mr: Mean Reversion (Bollinger Bands)
STRATEGY = 'mr'

## Trend Following Strategy
SIGNAL = 'SMA'
SHORT_WINDOW=50
LONG_WINDOW=200

# Mean Reversion Strategy (Bollinger Bands - BB)
BB_SHORT_WINDOW = 100
N_STD = 1.5