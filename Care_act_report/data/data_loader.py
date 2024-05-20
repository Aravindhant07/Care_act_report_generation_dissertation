import pandas as pd
from datetime import datetime, timedelta

class DataLoader:
    @staticmethod
    def load_details(file_path):
        """Load details from an Excel file."""
        return pd.read_excel(file_path)

    @staticmethod
    def load_and_prepare_data(file_path, timeframe):
        """Load and preprocess data based on the specified timeframe."""
        df = pd.read_excel(file_path)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
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
