# Stock Trading Strategies Analysis

## Introduction

This report outlines the methodology, data preprocessing steps, strategy development, and backtesting results for two stock trading strategies: 
- Trend Following  
- Mean Reversion. 

The analysis is based on historical stock data, aiming to identify profitable trading signals and evaluate the performance of each strategy.

## Methodology

### Data Preprocessing

The data preprocessing steps involve fetching historical stock data, which is then cleaned and prepared for analysis. The key steps include:

- **Data Fetching**: Historical stock data is fetched using the `fetch_symbol.py` script.
- **Normalization**: The 'Close' feature of the stock data is optionally normalized based on the `NORMALIZE_FEATURE_YN` setting in [`settings.py`](settings.py).
- **Aggregation**: Data is aggregated on a daily basis by default, as specified by the `DATA_AGGREGATION` setting in [`settings.py`](settings.py).

### Strategy Development

Two strategies are developed and analyzed:

1. **Trend Following**: This strategy uses Simple Moving Averages (SMA) to generate buy and sell signals. The implementation can be found in [`TrendFollowing`](utils/strategies/trend_following.py) class.
   
2. **Mean Reversion**: Utilizes Bollinger Bands to identify overbought or oversold conditions. The strategy is implemented in the [`MeanReversion`](utils/strategies/mean_reversion.py) class.

### Backtesting

Backtesting is performed using the [`Backtester`](utils/strategies/backtesting/backtester.py) class, which simulates trading based on the generated signals and calculates the performance of each strategy.

## Results

### Trend Following Strategy

- **Strengths**: Performs well in trending markets by capturing large movements.
- **Limitations**: May generate late signals in rapidly changing markets, leading to missed opportunities or losses.

### Mean Reversion Strategy

- **Strengths**: Effective in range-bound markets by capitalizing on price corrections.
- **Limitations**: Risky in trending markets as the assumption of mean reversion may not hold, leading to significant losses.

## Conclusion

Both the Trend Following and Mean Reversion strategies have their unique strengths and limitations. The choice of strategy should be based on market conditions and the trader's risk tolerance. Backtesting results indicate that a combination of these strategies or adaptive parameters could potentially enhance trading performance.

## Requirements

Before running the script, ensure you have the following:

- Python (3.7) installed on your system.
- All dependencies installed. This project uses poetry as dependency management.
- Use "poetry install" to create a venv and install all dependencies.

## Usage

The script can be executed from the command line in root directory. Here's the basic syntax:

```shell
(poetry run) python fetch_symbol.py <symbol> <start_date> <end_date>
(poetry run) python apply_strategy.py <symbol> <start_date> <end_date> backtest