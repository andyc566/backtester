import numpy as np 

def strategy(data):
    # Example strategy: buy when 10-day moving average crosses above 50-day
    data['10_MA'] = data['futures_price'].rolling(window=10).mean()
    data['50_MA'] = data['futures_price'].rolling(window=50).mean()
    data['signal'] = np.where(data['10_MA'] > data['50_MA'], 1, -1)  # 1 for buy, -1 for sell
    return data

def strategy_with_params(data, short_window, long_window):
    data['short_MA'] = data['futures_price'].rolling(window=short_window).mean()
    data['long_MA'] = data['futures_price'].rolling(window=long_window).mean()
    data['signal'] = np.where(data['short_MA'] > data['long_MA'], 1, -1)
    return data
