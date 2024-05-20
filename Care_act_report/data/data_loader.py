import pandas as pd
from datetime import datetime, timedelta

class DataLoader:
    def __init__(self, config):
        self.config = config

    def load_details(self):
        return pd.read_excel(self.config['details_path'])

    def load_and_prepare_data(self, file_path):
        df = pd.read_excel(file_path)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        timeframe = self.config['report_timeframe']

        if timeframe == 'yesterday':
            yesterday = datetime.now() - timedelta(days=1)
            df = df[df['Timestamp'].dt.date == yesterday.date()]
        elif timeframe == 'last_7_days':
            last_week = datetime.now() - timedelta(days=7)
            df = df[df['Timestamp'] >= last_week]
        elif timeframe == 'monthly':
            df = df.resample('1ME', on='Timestamp').mean()
        elif timeframe == 'quarterly':
            df = df.resample('3ME', on='Timestamp').mean()
        elif timeframe == 'half-yearly':
            df = df.resample('6ME', on='Timestamp').mean()
        elif timeframe == 'yearly':
            df = df.resample('1Y', on='Timestamp').mean()

        return df
