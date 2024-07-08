import yfinance as yf

class DataPreprocessor:
    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        if self.start_date > self.end_date:
            raise ValueError("Start date must be before end date.")
        self.data = self._fetch_data()

    def _fetch_data(self):
        data = yf.download(self.symbol, start=self.start_date, end=self.end_date)
        return data
    
    def preprocess_data(self, *args, method='ffill', time_period='D', normalize_feature_yn='n'):
        self._replace_missing_values(method=method)
        if normalize_feature_yn == 'y':
            self._normalize_feature(feature=args[0] if args else 'Close')
        self._aggregate_data(time_period=time_period)
        
    def save_data(self, path):
        self.data.to_csv(path)
        print(f"Data saved to {path}")
    
    def get_data(self):
        return self.data
    
    def _replace_missing_values(self, method='ffill'):
        self.data.fillna(method= method, inplace=True)

    def _aggregate_data(self, time_period='D'):
        if time_period not in ['D', 'W', 'M']:
            raise ValueError("Invalid time period. Please choose from 'D', 'W', or 'M'.")
        if time_period == 'D':
            return
        self.data = self.data.resample(time_period).mean()
    
    def _normalize_feature(self, feature='Close'):
        self.data[feature] = (self.data[feature] - self.data[feature].mean()) / self.data[feature].std()