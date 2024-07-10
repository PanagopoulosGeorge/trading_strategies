import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
class TrendFollowing:
    def __init__(self, file_path, file_name, feature='Close', signal='SMA', short_window=50, long_window=200):
        self.data = pd.read_csv(os.path.join(file_path, file_name), index_col=0)
        self.data.index = pd.to_datetime(self.data.index)
        self.feature = feature
        if signal not in ['SMA', 'EMA']:
            raise ValueError("Signal must be either 'SMA' or 'EMA'")
        self.signal = signal
        self.short_window = short_window
        self.long_window = long_window
    
    def generate_signals(self):
        if self.signal == 'SMA':
            self._generate_SMA_signals()
        elif self.signal == 'EMA':
            self._generate_EMA_signals()
        return self.data

    def save_signals(self, file_path):
        self.data.to_csv(file_path)
        
    def _calculate_EMA(self, values, smoothing=2):
        multiplier = smoothing / (len(values) + 1)
        return values[-1] * multiplier + self._calculate_EMA(values[:-1], smoothing) * (1 - multiplier) if len(values) > 1 else values[0]
        
    def _generate_SMA_signals(self):
        self.data[f'SMA{self.short_window}'] = self.data[self.feature].rolling(window=self.short_window).mean()
        self.data[f'SMA{self.long_window}'] = self.data[self.feature].rolling(window=self.long_window).mean()
        self.data['Signal'] = np.where(self.data[f'SMA{self.short_window}'] > self.data[f'SMA{self.long_window}'] , 1, -1)
        self.data['Signal'] = np.where(self.data[f"SMA{self.long_window}"].isnull(), 0, self.data['Signal'])
        self.data['Position'] = self.data['Signal'].diff()
    
    def _generate_EMA_signals(self):
        self.data[f'EMA{self.short_window}'] = self.data[self.feature].rolling(window=self.short_window).apply(self._calculate_EMA, raw=True)
        self.data[f'EMA{self.long_window}'] = self.data[self.feature].rolling(window=self.long_window).apply(self._calculate_EMA, raw=True)
        self.data['Signal'] = np.where(self.data[f'EMA{self.short_window}'] > self.data[f'EMA{self.long_window}'], 1, -1)
        self.data['Signal'] = np.where(self.data[f'EMA{self.long_window}'].isnull(), 0, self.data['Signal'])
        self.data['Position'] = self.data['Signal'].diff()
    
    def visualise_signals(self):   

        plt.figure(figsize=(10, 5))
        plt.plot(self.data[self.feature], label='Close Price', color='black')
        plt.plot(self.data[f'{self.signal}{self.long_window}'], label=f'{self.signal}{self.long_window}', color = 'blue')
        plt.plot(self.data[f'{self.signal}{self.short_window}'], label=f'{self.signal}{self.short_window}',
                 color = 'grey')
        
        plt.plot(self.data[self.data['Signal'] == 1].index, 
                 self.data[f'{self.signal}{self.short_window}'][self.data['Signal'] == 1],
                 '^', markersize=1, color='g', lw=0, label='Buy Signal')
        plt.plot(self.data[self.data['Signal'] == -1].index, 
                 self.data[f'{self.signal}{self.short_window}'][self.data['Signal'] == -1],
                 '^', markersize=1, color='r', lw=0, label='Sell Signal')
        
        plt.title(f'{self.signal} Signals')
        plt.legend()
        plt.show()