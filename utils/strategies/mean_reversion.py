import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
class MeanReversion:
    def __init__(self, file_path, file_name, feature='Close', window=50, symbol = "AAPL"):
        self.symbol = symbol
        self.data = pd.read_csv(os.path.join(file_path, file_name), index_col=0)
        self.data.index = pd.to_datetime(self.data.index)
        self.feature = feature
        self.window = window
    
    def generate_signals(self, n_std=2):
        """Bollinger band signals."""
        self.data[f'SMA{self.window}'] = self.data[self.feature].rolling(window=self.window).mean()
        self.data[f'STD{self.window}'] = self.data[self.feature].rolling(window=self.window).std()
        self.data[f'SMA{self.window}_upper'] = self.data[f'SMA{self.window}'] + n_std * self.data[f'STD{self.window}']
        self.data[f'SMA{self.window}_lower'] = self.data[f'SMA{self.window}'] - n_std * self.data[f'STD{self.window}']
        self.data['Signal'] = np.where(self.data[self.feature]>self.data[f'SMA{self.window}_upper'], -1, 0)
        self.data['Signal'] = np.where(self.data[self.feature]<self.data[f'SMA{self.window}_lower'], 1, self.data['Signal'])
        self.data['Position'] = self.data['Signal'].diff()
        return self.data
    
    def save_signals(self, file_path):
        self.data.to_csv(file_path)
    
    def visualise_signals(self):
        """Visualise signals. lines for upper and lower with same color."""
        plt.figure(figsize=(10, 5))
        plt.plot(self.data[self.feature], label='Close Price', color='black')
        plt.plot(self.data[f'SMA{self.window}'], label=f'SMA{self.window}', color='grey')
        plt.plot(self.data[f'SMA{self.window}_upper'], label=f'SMA{self.window}_upper', color='blue')
        plt.plot(self.data[f'SMA{self.window}_lower'], label=f'SMA{self.window}_lower', color='blue')
        
        plt.title(f'SMA Signals for {self.symbol}')
        plt.legend()
        plt.show()
        