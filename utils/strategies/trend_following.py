import os
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

class TrendFollowing:
    def __init__(self, file_path, file_name, feature='Close'):
        self.data = pd.read_csv(os.path.join(file_path, file_name), index_col=0)
        self.data.index = pd.to_datetime(self.data.index)
        self.feature = feature
        self.data = self._generate_SMA_signals()
        self.data = self._generate_EMA_signals()
    def get_data(self):
        return self.data
    def _calculate_SMA(self, window=50):
        return self.data[self.feature].rolling(window=window).mean()
    
    def _calculate_EMA(self, values, smoothing=2):
        multiplier = smoothing / (len(values) + 1)
        return values[-1] * multiplier + self._calculate_EMA(values[:-1], smoothing) * (1 - multiplier) if len(values) > 1 else values[0]
        
    def _generate_SMA_signals(self):
        self.data['SMA50'] = self.data[self.feature].rolling(window=50).mean()
        self.data['SMA200'] = self.data[self.feature].rolling(window=200).mean()
        self.data['SMA_Signal'] = np.where(self.data['SMA50'] > self.data['SMA200'], 1, -1)
        self.data['SMA_Position'] = self.data['SMA_Signal'].diff()
        return self.data
    
    def _generate_EMA_signals(self):
        self.data['EMA50'] = self.data[self.feature].rolling(window=50).apply(self._calculate_EMA, raw=True)
        self.data['EMA200'] = self.data[self.feature].rolling(window=200).apply(self._calculate_EMA, raw=True)
        self.data['EMA_Signal'] = np.where(self.data['EMA50'] > self.data['EMA200'], 1, -1)
        self.data['EMA_Position'] = self.data['EMA_Signal'].diff()
        return self.data
    
    def save_data(self, file_path):
        self.data.to_csv(file_path)
    
    def visualize_data(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.data[self.feature], label='Close Price', alpha=0.5)
        plt.plot(self.data['SMA50'], label='SMA50', alpha=0.5)
        plt.plot(self.data['SMA200'], label='SMA200', alpha=0.5)
        #plt.plot(self.data['EMA50'], label='EMA50', alpha=0.5)
        #plt.plot(self.data['EMA200'], label='EMA200', alpha=0.5)
        plt.title('Trend Following Strategy')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.legend()
        plt.show()