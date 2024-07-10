import pandas as pd
from matplotlib import pyplot as plt

class Backtester:
    """Backtester class for backtesting trading strategies."""

    def __init__(
        self,
        initial_capital: float = 10000.0,
        risk_free_rate: float = 0.04,
        **kwargs
    ):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.portfolio = {} 
        self.daily_portfolio_values = pd.Series(name='daily_portfolio_value')
        self.daily_returns = pd.Series(name='daily_returns')
        self.sharpe_ratio = 0.0
        self.risk_free_rate = risk_free_rate
    def print_summary(self):
        print(f"Final Portfolio Value: {self.get_final_portfolio_value()}")
        print(f"Total Return: {round(self.get_total_return_pct(), 2)} %")
        print(f"{round(self.get_sharpe_ratio(), 2)}")
        print(f"Max Drawdown: {round(self.get_max_drawdown(),2)} %")
        
    def get_yearly_returns(self) -> pd.Series:
        return self.daily_portfolio_values.resample('Y').aggregate(lambda x: (x.iloc[-1] - x.iloc[0])/x.iloc[0] if len(x) > 0 else 0.0)
    def get_monthly_returns(self) -> pd.Series:
        return self.daily_portfolio_values.resample('M').aggregate(lambda x: (x.iloc[-1] - x.iloc[0])/x.iloc[0] if len(x) > 0 else 0.0)
    
    def get_yearly_volatilities(self) -> pd.Series:
        monthly_returns = self.get_monthly_returns()
        volatilities = monthly_returns.resample('Y').std()
        return volatilities
    def get_last_trading_day(self):
        return self.daily_portfolio_values.index[-1]
    def get_final_portfolio_value(self) -> float:
        return round(self.daily_portfolio_values.iloc[-1], 2)
    def get_total_return_pct(self) -> float:
        return round((self.daily_portfolio_values.iloc[-1] - self.initial_capital)/self.initial_capital * 100.0, 2)
    def get_sharpe_ratio(self) -> float:
        yearly_returns = self.get_yearly_returns()
        yearly_excess_returns = yearly_returns - self.risk_free_rate
        yearly_volatilities = self.get_yearly_volatilities()
        return yearly_excess_returns/yearly_volatilities 
         
    def get_max_drawdown(self) -> float:
        return round(self.daily_returns.min(), 2)
    
    def backtest_strategy_single_asset(self, asset: str, signals: pd.Series, prices: pd.Series) -> None:
        self.daily_portfolio_values = pd.Series(index=prices.index)
        self.signals = signals.shift(1) # Shift signals by one day ahead to avoid look-ahead bias
        self.signals.fillna(0, inplace=True)
        self.prices = prices
        for date, position in signals.items():
            price = prices[date]
            self.execute_trade(asset, position, price, date)
            self.daily_portfolio_values.loc[date] = self.capital + self.portfolio.get(asset, 0) * price
            self.daily_returns = self.daily_portfolio_values.pct_change()

    def is_holding_asset(self, asset: str) -> bool:
        return asset in self.portfolio and self.portfolio[asset] > 0
    
    def buy_asset_unit(self, asset: str, price: float) -> None:
        if self.capital >= price:
            self.capital -= price
            self.portfolio[asset] = self.portfolio.get(asset, 0) + 1

    
    def sell_asset_unit(self, asset: str, price: float) -> None:
        if self.is_holding_asset(asset):
            self.capital += price
            self.portfolio[asset] = self.portfolio.get(asset, 0) - 1
    
    def execute_trade(self, asset: str, position: float, price: float, date:str) -> None:

        if position == 1:
            #print(f"Executing buy trade for asset {asset} at price {price} on date {date}.")
            self.buy_asset_unit(asset, price)
        elif position == -1:
            #print(f"Executing sell trade for asset {asset} at price {price} on date {date}.")
            self.sell_asset_unit(asset, price)
        else:
            return "No action taken."
    
    def visualise_backtesting(self):
        fig, ax = plt.subplots(2, 1, figsize=(15, 10))
        ax[0].plot(self.daily_portfolio_values, label='Portfolio Value')
        ax[0].set_title('Daily Portfolio Value')
        ax[0].set_ylabel('Portfolio Value')
        ax[0].set_xlabel('Date')
        ax[0].legend()
        ax[1].plot(self.prices, label='Prices', color='b')
        ax[1].plot(self.signals[self.signals == 1], 'o', markersize=5, color='g', lw=0, label='Buy Signal')
        ax[1].plot(self.signals[self.signals == -1], 'o', markersize=5, color='r', lw=0, label='Sell Signal')
        ax[1].set_title('Trading Signals')
        ax[1].set_ylabel('Signals')
        ax[1].set_xlabel('Date')
        ax[1].legend()
        plt.show()