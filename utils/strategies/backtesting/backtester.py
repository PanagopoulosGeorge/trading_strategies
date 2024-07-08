import pandas as pd

class Backtester:
    """Backtester class for backtesting trading strategies."""

    def __init__(
        self,
        initial_capital: float = 10000.0,
    ):
        self.initial_capital = initial_capital
        self.assets_data = {}
        self.portfolio = {} # Asset: Units

    def get_portfolio(self) -> dict:
        return self.portfolio

    def backtest_strategy(self, asset: str, signals: pd.Series, prices: pd.Series) -> None:
        for date, position in signals.items():
            price = prices[date]
            self.execute_trade(asset, position, price, date)
    
    def __str__(self, price: pd.Series):
        print("portfolio value: ", self.initial_capital + sum(self.portfolio.values()) * price)    


    def is_holding_asset(self, asset: str) -> bool:
        return asset in self.portfolio and self.portfolio[asset] > 0
    
    def buy_asset_unit(self, asset: str, price: float) -> None:
        if self.initial_capital >= price:
            self.initial_capital -= price
            self.portfolio[asset] = self.portfolio.get(asset, 0) + 1
            print(f"Bought 1 unit of asset {asset} at price {price}.")
            return f"Bought 1 unit of asset {asset} at price {price}."
        else:
            return f"Insufficient capital to buy asset {asset} at price {price}."
    
    def sell_asset_unit(self, asset: str, price: float) -> None:
        if self.is_holding_asset(asset):
            self.initial_capital += price
            self.portfolio[asset] = self.portfolio.get(asset, 0) - 1
            print(f"Sold 1 unit of asset {asset} at price {price}.")
            return f"Sold 1 unit of asset {asset} at price {price}."
        else:
            return f"No asset {asset} to sell."
    
    def execute_trade(self, asset: str, position: float, price: float, date:str) -> None:
        if position == 1:
            print("Current capital: ", self.initial_capital)
            print("Current portfolio: ", self.portfolio)
            print("Current date: ", date)
            return self.buy_asset_unit(asset, price)
        elif position == -1:
            print("Current capital: ", self.initial_capital)
            print("Current portfolio: ", self.portfolio)
            print("Current date: ", date)
            return self.sell_asset_unit(asset, price)
        else:
            return "No action taken."